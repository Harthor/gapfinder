"""Eval de retrieval, iteración 2.

Cambios respecto de `eval` (iteración 1):
- Varias consultas por caso se fusionan con RRF (k=60) en UN ranking y se corta a N: la comparación
  entre 1 consulta y 4-5 consultas es justa (antes la unión podía tener hasta 4N candidatos).
- Sistemas: embeddings (MiniLM / bge-base), BM25 (FTS5) e híbrido = RRF(embeddings + BM25).
- Consultas: `raw` (título + descripción, la de la iteración 1), `core` (query_core de Claude en
  real/partial; la necesidad en sintéticos), `tmpl4` (las 4 plantillas de la iteración 1) y `llm5`
  (core + 4 reformulaciones de Claude).
- "con dirigida" = corpus base + los items fuera del corpus que trajeron las consultas de palabras
  clave de Claude (tabla `targeted_llm`).
Rank = posición del primer item esperado en la lista fusionada (listas de TOP_K por consulta);
fuera de todas las listas = no encontrado.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from collections import defaultdict
from pathlib import Path

import numpy as np

from gapfinder import bm25, embed, leakage
from gapfinder.eval import _origin_group, ranks, reformulations
from gapfinder.real_cases import github_key, normalize_url
from gapfinder.text import get_texts

log = logging.getLogger(__name__)

NS = (50, 200, 1000)
TOP_K = 2000
RRF_K = 60
MISS = 10**9


def rrf(lists: list[list[str]], k: int = RRF_K) -> list[str]:
    score: dict[str, float] = defaultdict(float)
    for lst in lists:
        for pos, item in enumerate(lst):
            score[item] += 1.0 / (k + pos + 1)
    return sorted(score, key=lambda i: -score[i])


def first_rank(ranking: list[str], expected: set[str]) -> int:
    for pos, item in enumerate(ranking[:TOP_K], 1):
        if item in expected:
            return pos
    return MISS


def query_sets(case: dict, llm: dict, idf: leakage.Idf) -> dict[str, list[str]]:
    q = llm.get(case["id"], {})
    t = reformulations(case, idf)
    core = q.get("query_core") or t["need"]
    return {"raw": [t["need"]], "core": [core], "tmpl4": [t[r] for r in ("need", "keywords", "plain", "show_hn")],
            "llm5": [core, *q.get("reformulations", [])]}


def run(conn: sqlite3.Connection, cases: list[dict], models: list[str], out_dir: Path,
        targeted: bool = False, llm_path: Path = Path("data/llm_queries.json")) -> dict:
    """targeted: agrega la variante "con" (corpus + hits de la búsqueda dirigida). Fuera por defecto:
    en la iteración 2 no mejoró el recall y suma ~5.000 competidores."""
    variants = ("sin", "con") if targeted else ("sin",)
    idf = leakage.load_idf(conn, Path("data/cache/idf.json"))
    llm = json.loads(llm_path.read_text())
    qsets = {c["id"]: query_sets(c, llm, idf) for c in cases}
    texts_all = sorted({t for qs in qsets.values() for ts in qs.values() for t in ts})

    targeted_all = {r[0] for r in conn.execute("SELECT item_id FROM targeted")}
    llm_hits = {r[0] for r in conn.execute("SELECT item_id FROM targeted_llm")}
    allowed = {"sin": set(), "con": llm_hits}   # items fuera del corpus base permitidos en cada variante
    hit_map = {}
    for iid, url in conn.execute("SELECT i.id, i.url FROM items i WHERE i.id IN (SELECT item_id FROM targeted_llm)"):
        hit_map[iid.lower()] = iid
        hit_map[normalize_url(url)] = iid

    def expected(case: dict, variant: str, heuristic: bool) -> set[str]:
        exp = list(case.get("expected_item_ids", []))
        if not heuristic:
            exp = [i for i in exp if i not in set(case.get("meta", {}).get("heuristic_item_ids", []))]
        if variant == "con":
            for u in case.get("expected_urls", []):
                key = (github_key(u) or "").lower() or normalize_url(u)
                if key in hit_map:
                    exp.append(hit_map[key])
        # solo cuenta lo que está en el índice de esta variante (el corpus base, más los hits dirigidos en "con")
        return {i for i in exp if i not in targeted_all or i in allowed[variant]}

    # --- BM25: una consulta FTS por texto, filtrada por variante -------------------------------
    fts = bm25.connect()
    bm25_lists: dict[str, dict[str, list[str]]] = {"sin": {}, "con": {}}
    for n, text in enumerate(texts_all, 1):
        raw = bm25.search(fts, text, idf, TOP_K + len(targeted_all))
        for v in variants:
            bm25_lists[v][text] = [i for i in raw if i not in targeted_all or i in allowed[v]][:TOP_K]
        if n % 200 == 0:
            log.info("bm25: %d/%d consultas", n, len(texts_all))

    # --- embeddings -----------------------------------------------------------------------------
    emb_lists: dict[tuple[str, str], dict[str, list[str]]] = {}
    ablation: dict[tuple[str, str], int] = {}          # (modelo, caso) -> rank con el item esperado en title_only
    all_exp = sorted({i for c in cases for i in c.get("expected_item_ids", [])})
    exp_texts = get_texts(conn, all_exp)
    origin = {i: t.origin for i, t in exp_texts.items()}
    for key in models:
        ids, mat = embed.load(key, "corpus")
        mats, all_ids = [mat.astype(np.float32)], list(ids)
        del mat
        t_ids, t_mat = embed.load(key, "targeted")
        mats.append(t_mat.astype(np.float32))
        all_ids += t_ids
        n_base = len(ids)
        q_vecs = embed.encode_queries(key, texts_all)
        pos = {i: n for n, i in enumerate(all_ids)}
        con_mask = np.zeros(len(all_ids), bool)
        con_mask[:n_base] = True
        con_mask[[pos[i] for i in llm_hits if i in pos]] = True
        syn = [c for c in cases if c["kind"] == "synthetic"]
        t_vecs = embed.encode_passages(key, [exp_texts[c["expected_item_ids"][0]].title for c in syn])
        syn_q = {c["id"]: (qsets[c["id"]]["core"][0], t_vecs[n]) for n, c in enumerate(syn)}
        for v in variants:
            emb_lists[(key, v)] = {}
        for n, (text, q) in enumerate(zip(texts_all, q_vecs)):
            scores = np.concatenate([m @ q for m in mats])
            for v in variants:
                s = scores.copy()
                s[n_base:] = -np.inf if v == "sin" else np.where(con_mask[n_base:], s[n_base:], -np.inf)
                top = np.argpartition(-s, TOP_K)[:TOP_K]
                emb_lists[(key, v)][text] = [all_ids[i] for i in top[np.argsort(-s[top])]]
            for cid, (qt, tv) in syn_q.items():   # ablación: solo el vector del item esperado cambia
                if qt == text:
                    t = pos[cases_by_id(cases)[cid]["expected_item_ids"][0]]
                    base_scores = scores[:n_base]
                    ablation[(key, cid)] = ranks(base_scores, [t], {t: float(tv @ q)})[0]
        log.info("eval2 %s listo", key)
        del mats

    # --- rankings por caso x sistema x consultas x variante ------------------------------------
    rows = []
    for c in cases:
        for v in variants:
            for heur in ((True, False) if c["kind"] == "partial" else (True,)):
                exp = expected(c, v, heur)
                base = {"case": c["id"], "kind": c["kind"], "variant": v, "heuristic": heur, "n_expected": len(exp),
                        "author": c.get("author"), "pair_id": c.get("pair_id"), "leakage_flag": bool(c.get("leakage_flag")),
                        "label_note": bool(c.get("label_note")),
                        "origin": _origin_group(c, sorted(exp), origin)}
                for qs_name, qtexts in qsets[c["id"]].items():
                    if not qtexts:
                        continue
                    b = [bm25_lists[v][t] for t in qtexts]
                    rows.append({**base, "system": "bm25", "model": "-", "queries": qs_name,
                                 "rank": first_rank(rrf(b) if len(b) > 1 else b[0], exp)})
                    for key in models:
                        e = [emb_lists[(key, v)][t] for t in qtexts]
                        rows.append({**base, "system": "emb", "model": key, "queries": qs_name,
                                     "rank": first_rank(rrf(e) if len(e) > 1 else e[0], exp)})
                        rows.append({**base, "system": "hybrid", "model": key, "queries": qs_name,
                                     "rank": first_rank(rrf(e + b), exp)})
                if c["kind"] == "synthetic" and v == "sin":
                    for key in models:
                        rows.append({**base, "system": "emb", "model": key, "queries": "core_title_only",
                                     "rank": ablation.get((key, c["id"]), MISS)})
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "iter2_ranks.json").write_text(json.dumps(rows, indent=0))
    (out_dir / "iter2_recall.md").write_text(render(rows, cases, models))
    return {"rows": len(rows), "llm_hits_outside_base": len(llm_hits)}


_cases_by_id: dict[int, dict] = {}


def cases_by_id(cases: list[dict]) -> dict:
    if id(cases) not in _cases_by_id:
        _cases_by_id[id(cases)] = {c["id"]: c for c in cases}
    return _cases_by_id[id(cases)]


# --- reporte ------------------------------------------------------------------------------------


def _sel(rows, **kw):
    return [r for r in rows if all(r[k] == v for k, v in kw.items())]


def _cells(rows: list[dict]) -> tuple[int, str]:
    rows = [r for r in rows if r["n_expected"]]
    if not rows:
        return 0, " | ".join("–" for _ in NS)
    return len(rows), " | ".join(f"{sum(r['rank'] <= n for r in rows) / len(rows):.2f}" for n in NS)


GROUPS = [("real", dict(kind="real")), ("real sin label_note", dict(kind="real", label_note=False)),
          ("partial sin heurísticos", dict(kind="partial", heuristic=False)),
          ("partial (todos)", dict(kind="partial", heuristic=True)), ("synthetic", dict(kind="synthetic"))]
SYSTEMS = [("emb", "minilm"), ("emb", "bge"), ("bm25", "-"), ("hybrid", "minilm"), ("hybrid", "bge")]


def render(rows: list[dict], cases: list[dict], models: list[str]) -> str:
    systems = [(s, m) for s, m in SYSTEMS if m == "-" or m in models]
    L = ["# Retrieval — iteración 2\n",
         "R@N con N justo: las consultas de un caso se fusionan con RRF (k=60) en un único ranking y se "
         "corta a N. `raw` = título + descripción (iteración 1); `core` = query_core de Claude (en "
         "sintéticos, la necesidad); `llm5` = core + 4 reformulaciones de Claude; `tmpl4` = las 4 "
         "plantillas de la iteración 1. `hybrid` = RRF(embeddings + BM25). `n` = casos con algún item "
         "esperado en el índice.\n"]
    present = {r["variant"] for r in rows}
    for title, variant in (("## Tabla principal (sin búsqueda dirigida)", "sin"),
                           ("## Con búsqueda dirigida (consultas de palabras clave de Claude)", "con")):
        if variant not in present:
            continue
        L += [title + "\n", "| casos | sistema | modelo | consultas | n | R@50 | R@200 | R@1000 |", "|---|---|---|---|---|---|---|---|"]
        for gname, g in GROUPS[:3] if variant == "con" else GROUPS[:4]:
            for s, m in systems:
                for qs in ("raw", "core", "llm5"):
                    n, cells = _cells(_sel(rows, variant=variant, system=s, model=m, queries=qs, **g))
                    L.append(f"| {gname} | {s} | {m} | {qs} | {n} | {cells} |")
        L.append("")
    L += ["## Punto 1: plantillas de la iteración 1, reform 1 vs reform 4 con RRF y N justo (embeddings, sin dirigida)\n",
          "| casos | modelo | consultas | n | R@50 | R@200 | R@1000 |", "|---|---|---|---|---|---|---|"]
    for gname, g in GROUPS:
        for m in models:
            for qs, label in (("raw", "1 (need)"), ("tmpl4", "4 plantillas, RRF")):
                n, cells = _cells(_sel(rows, variant="sin", system="emb", model=m, queries=qs, **g))
                L.append(f"| {gname} | {m} | {label} | {n} | {cells} |")
    L += ["", "## Sintéticos (sin dirigida)\n", "| sistema | modelo | consultas | n | R@50 | R@200 | R@1000 |", "|---|---|---|---|---|---|---|"]
    for s, m in systems:
        for qs in ("core", "llm5"):
            n, cells = _cells(_sel(rows, variant="sin", system=s, model=m, queries=qs, kind="synthetic"))
            L.append(f"| {s} | {m} | {qs} | {n} | {cells} |")
    L += ["", "## Ablación title_only en sintéticos (embeddings, consulta = necesidad, sin dirigida)\n",
          "| modelo | origen | n | R@50 real → title_only | R@200 | R@1000 |", "|---|---|---|---|---|---|"]
    for m in models:
        for o in sorted({r["origin"] for r in _sel(rows, kind="synthetic")}) + ["todos"]:
            f = {} if o == "todos" else {"origin": o}
            real = _sel(rows, variant="sin", system="emb", model=m, queries="core", kind="synthetic", **f)
            abl = _sel(rows, variant="sin", system="emb", model=m, queries="core_title_only", kind="synthetic", **f)
            if real:
                a, b = _cells(real)[1].split(" | "), _cells(abl)[1].split(" | ")
                L.append(f"| {m} | {o} | {len(real)} | " + " | ".join(f"{x} → {y}" for x, y in zip(a, b)) + " |")
    flagged = sorted({c["pair_id"] for c in cases if c.get("pair_id") and c.get("leakage_flag")})
    L += ["", "## Pareado human vs claude (8 pares, sin dirigida)\n",
          f"Par con leakage_flag: {', '.join(flagged) or 'ninguno'} (filas `sin flag` lo excluyen).\n",
          "| sistema | modelo | consultas | pares | @N | recall human | recall claude | ambos | solo human | solo claude | ninguno |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, m in systems:
        for qs in ("core", "llm5"):
            by = defaultdict(dict)
            for r in _sel(rows, variant="sin", system=s, model=m, queries=qs, kind="synthetic"):
                if r["pair_id"]:
                    by[r["pair_id"]][r["author"]] = r["rank"]
            for scope, pairs in (("todos", by), ("sin flag", {k: v for k, v in by.items() if k not in flagged})):
                for n in NS:
                    hh = [(p["human"] <= n, p["claude"] <= n) for p in pairs.values() if len(p) == 2]
                    if hh:
                        L.append(f"| {s} | {m} | {qs} | {len(hh)} ({scope}) | {n} | {sum(h for h, _ in hh)/len(hh):.2f} | "
                                 f"{sum(c for _, c in hh)/len(hh):.2f} | {sum(h and c for h, c in hh)} | "
                                 f"{sum(h and not c for h, c in hh)} | {sum(c and not h for h, c in hh)} | "
                                 f"{sum(not h and not c for h, c in hh)} |")
    L += ["", "Negativos: no hay casos `negative`; se omiten.\n"]
    return "\n".join(L) + "\n"
