"""Eval de recall de la Fase 2 sobre known_cases.json.

Para cada caso se arman reformulaciones (plantillas) y cada una recupera por similitud coseno sobre
el índice de embeddings. Un caso cuenta como encontrado en @N si alguno de sus items esperados está
en el top-N de alguna reformulación (la unión que después ve el verificador). Se reporta:
- recall@50/200/1000 por kind x modelo x reformulaciones (1 = solo la necesidad, 4 = unión)
  x búsqueda dirigida (sin/con) x origen del texto del item esperado,
- partial con y sin los items resueltos por heurística de dominio,
- ablación en sintéticos: el item esperado forzado a title_only (solo ese vector cambia),
- recall pareado human vs claude (mismo item, `pair_id`), marcando los casos con leakage_flag.
Los casos sin ningún item esperado en el índice no entran en el denominador (se cuentan aparte).
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from gapfinder import embed, leakage
from gapfinder.real_cases import github_key, normalize_url
from gapfinder.targeted import keywords
from gapfinder.text import get_texts

log = logging.getLogger(__name__)

NS = (50, 200, 1000)
TOP = max(NS)
REFORMS = ("need", "keywords", "plain", "show_hn")
_ASK_PREFIX = re.compile(
    r"^(?:i'?d (?:really )?like|i want|i need|i'?m looking for|looking for|is there|how can i|where can i find|"
    r"i wish there (?:was|were)|we need|our team needs)\s+(?:to\s+|a way to\s+)?", re.IGNORECASE)


def reformulations(case: dict, idf: leakage.Idf) -> dict[str, str]:
    """need: la necesidad (real/partial: título + descripción); keywords: palabras de producto;
    plain: sin la forma de pedir (real/partial: solo la descripción, sin el título de gancho);
    show_hn: plain con el prefijo de los títulos del corpus."""
    title, desc = case["title"].strip(), (case.get("description") or "").strip()
    need = f"{title}. {desc}" if desc else title
    if desc:
        plain = desc
    else:
        plain = _ASK_PREFIX.sub("", title)
        plain = plain[:1].upper() + plain[1:]
    return {"need": need, "keywords": " ".join(keywords(need, idf, 6)) or need,
            "plain": plain, "show_hn": f"Show HN: {plain}"}


@dataclass
class Index:
    ids: list[str]
    mats: list[np.ndarray]               # float32, normalizados; se consultan por partes (sin copiar)
    pos: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.pos = {i: n for n, i in enumerate(self.ids)}

    def scores(self, q: np.ndarray) -> np.ndarray:
        return np.concatenate([m @ q for m in self.mats])


def ranks(scores: np.ndarray, targets: list[int], override: dict[int, float] | None = None) -> list[int]:
    """Rank (1 = primero) de cada índice en `targets`. `override`: score reemplazado para un índice
    (ablación: ese item con otro vector), el resto del índice igual."""
    out = []
    for t in targets:
        s = override[t] if override and t in override else scores[t]
        higher = int((scores > s).sum())
        if override and t in override and scores[t] > s:
            higher -= 1  # su propio score original no compite contra sí mismo
        out.append(higher + 1)
    return out


def _expected(case: dict, index: Index, targeted_map: dict[str, str], use_heuristic: bool = True) -> list[str]:
    exp = list(case.get("expected_item_ids", []))
    if not use_heuristic:
        heur = set(case.get("meta", {}).get("heuristic_item_ids", []))
        exp = [i for i in exp if i not in heur]
    for u in case.get("expected_urls", []):  # con búsqueda dirigida, una URL fuera del corpus puede aparecer
        key = (github_key(u) or "").lower() or normalize_url(u)
        if key in targeted_map:
            exp.append(targeted_map[key])
    return [i for i in dict.fromkeys(exp) if i in index.pos]


def run(conn: sqlite3.Connection, cases: list[dict], models: list[str], out_dir: Path) -> dict:
    idf = leakage.load_idf(conn, Path("data/cache/idf.json"))
    reforms = {c["id"]: reformulations(c, idf) for c in cases}
    embed.ensure_targeted_table(conn)
    t_rows = conn.execute("SELECT i.id, i.url FROM targeted t JOIN items i ON i.id = t.item_id").fetchall()
    targeted_map = {}
    for iid, url in t_rows:
        targeted_map[iid.lower()] = iid
        targeted_map[normalize_url(url)] = iid
    all_exp = sorted({i for c in cases for i in c.get("expected_item_ids", [])})
    texts = get_texts(conn, all_exp)
    origin = {i: t.origin for i, t in texts.items()}
    title_only_text = {i: t.title for i, t in texts.items()}

    results: list[dict] = []   # una fila por caso x modelo x variante de índice x uso de heurísticos
    union_sizes: dict[tuple, list[int]] = defaultdict(list)
    for key in models:
        ids, mat = embed.load(key, "corpus")
        base = Index(ids, [mat.astype(np.float32)])
        del mat
        variants = {"sin": base}
        if (embed.EMB_DIR / key / "targeted" / "ids.json").exists():
            t_ids, t_mat = embed.load(key, "targeted")
            variants["con"] = Index(ids + t_ids, base.mats + [t_mat.astype(np.float32)])
        q_texts = [(c["id"], r, reforms[c["id"]][r]) for c in cases for r in REFORMS]
        q_vecs = embed.encode_queries(key, [t for *_, t in q_texts])
        q_of = {(cid, r): q_vecs[n] for n, (cid, r, _) in enumerate(q_texts)}
        syn_items = sorted({c["expected_item_ids"][0] for c in cases if c["kind"] == "synthetic"})
        t_vecs = dict(zip(syn_items, embed.encode_passages(key, [title_only_text[i] for i in syn_items])))
        for vname, index in variants.items():
            for c in cases:
                scores_of = {r: index.scores(q_of[(c["id"], r)]) for r in REFORMS}
                for use_heur in ((True, False) if c["kind"] == "partial" else (True,)):
                    exp = _expected(c, index, targeted_map, use_heur)
                    row = {"case": c["id"], "kind": c["kind"], "model": key, "targeted": vname,
                           "heuristic": use_heur, "author": c.get("author"), "pair_id": c.get("pair_id"),
                           "leakage_flag": bool(c.get("leakage_flag")), "n_expected": len(exp),
                           "origin": _origin_group(c, exp, origin), "ranks": {}, "ablation_ranks": {}}
                    if exp:
                        targets = [index.pos[i] for i in exp]
                        for r in REFORMS:
                            scores = scores_of[r]
                            row["ranks"][r] = min(ranks(scores, targets))
                            if c["kind"] == "synthetic":
                                t = targets[0]
                                row["ablation_ranks"][r] = ranks(scores, [t], {t: float(t_vecs[exp[0]] @ q_of[(c["id"], r)])})[0]
                            if use_heur:
                                k = min(TOP, len(scores) - 1)
                                top = np.argpartition(-scores, k)[:k]
                                union_sizes[(key, vname, c["id"])].append(top[np.argsort(-scores[top])])
                    results.append(row)
            log.info("eval %s/%s listo", key, vname)
        del base, variants
    sizes = {}
    for (key, vname, _), tops in union_sizes.items():
        for n in NS:
            sizes.setdefault((key, vname, n), []).append(len(set().union(*(set(t[:n].tolist()) for t in tops))))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "phase2_ranks.json").write_text(json.dumps(results, indent=1))
    report = render(results, {k: float(np.mean(v)) for k, v in sizes.items()}, cases)
    (out_dir / "phase2_recall.md").write_text(report)
    return {"rows": len(results)}


def _origin_group(case: dict, exp: list[str], origin: dict[str, str]) -> str:
    if case["kind"] == "synthetic":
        return origin.get(case["expected_item_ids"][0], "?")
    return "title_only" if exp and all(origin.get(i) == "title_only" for i in exp) else "enriched"


# --- reporte ------------------------------------------------------------------


def _hit(row: dict, n: int, reforms: tuple[str, ...], field: str = "ranks") -> bool:
    return any(row[field].get(r, 10**9) <= n for r in reforms)


def _recall(rows: list[dict], n: int, reforms: tuple[str, ...], field: str = "ranks") -> str:
    rows = [r for r in rows if r["n_expected"]]
    return f"{sum(_hit(r, n, reforms, field) for r in rows) / len(rows):.2f}" if rows else "–"


def render(results: list[dict], sizes: dict, cases: list[dict]) -> str:
    one, four = ("need",), REFORMS
    models = sorted({r["model"] for r in results})
    variants = [v for v in ("sin", "con") if any(r["targeted"] == v for r in results)]
    L = ["# Fase 2 — recall de retrieval\n",
         "Un caso cuenta en @N si algún item esperado está en el top-N de alguna reformulación. "
         "`reform 1` = solo la necesidad; `reform 4` = unión de need / keywords / plain / show_hn. "
         "`dirigida` = índice con los items agregados por la búsqueda dirigida. "
         "`n` = casos con algún item esperado en ese índice (los demás miden cobertura, no retrieval).\n"]

    def groups():
        for kind in ("synthetic", "real", "partial"):
            rows = [r for r in results if r["kind"] == kind and r["heuristic"]]
            yield kind, rows
            if kind == "partial":
                yield "partial (sin heurísticos)", [r for r in results if r["kind"] == kind and not r["heuristic"]]

    L += ["## Recall por kind × modelo × reformulaciones × búsqueda dirigida\n",
          "| kind | modelo | reform | dirigida | n | sin item | R@50 | R@200 | R@1000 |", "|---|---|---|---|---|---|---|---|---|"]
    for kind, rows in groups():
        for m in models:
            for v in variants:
                sel = [r for r in rows if r["model"] == m and r["targeted"] == v]
                for label, rf in (("1", one), ("4", four)):
                    L.append(f"| {kind} | {m} | {label} | {v} | {sum(1 for r in sel if r['n_expected'])} | "
                             f"{sum(1 for r in sel if not r['n_expected'])} | " + " | ".join(_recall(sel, n, rf) for n in NS) + " |")
    L += ["", "Tamaño medio de la unión de candidatos (reform 4), por caso:\n",
          "| modelo | dirigida | @50 | @200 | @1000 |", "|---|---|---|---|---|"]
    for m in models:
        for v in variants:
            L.append(f"| {m} | {v} | " + " | ".join(f"{sizes.get((m, v, n), 0):.0f}" for n in NS) + " |")

    v = variants[-1]
    L += ["", f"## Por origen del texto del item esperado (reform 4, dirigida = {v})\n",
          "| kind | origen | modelo | n | R@50 | R@200 | R@1000 |", "|---|---|---|---|---|---|---|"]
    for kind, rows in groups():
        for o in sorted({r["origin"] for r in rows}):
            for m in models:
                sel = [r for r in rows if r["origin"] == o and r["model"] == m and r["targeted"] == v]
                if any(r["n_expected"] for r in sel):
                    L.append(f"| {kind} | {o} | {m} | {sum(1 for r in sel if r['n_expected'])} | "
                             + " | ".join(_recall(sel, n, four) for n in NS) + " |")

    L += ["", "## Ablación en sintéticos: item esperado forzado a title_only (reform 4, dirigida = sin)\n",
          "| origen original | modelo | n | R@50 real → title_only | R@200 | R@1000 |", "|---|---|---|---|---|---|"]
    syn = [r for r in results if r["kind"] == "synthetic" and r["targeted"] == "sin"]
    for o in sorted({r["origin"] for r in syn}) + ["todos"]:
        for m in models:
            sel = [r for r in syn if r["model"] == m and (o == "todos" or r["origin"] == o)]
            if sel:
                L.append(f"| {o} | {m} | {len(sel)} | " + " | ".join(
                    f"{_recall(sel, n, four)} → {_recall(sel, n, four, 'ablation_ranks')}" for n in NS) + " |")

    L += ["", "## Pareado human vs claude (mismo item; dirigida = sin)\n",
          "Pares donde uno de los dos casos tiene `leakage_flag`: "
          + (", ".join(sorted({c["pair_id"] for c in cases if c.get("pair_id") and c.get("leakage_flag")})) or "ninguno")
          + ". Filas `sin flag` los excluyen.\n",
          "| modelo | reform | pares | @N | recall human | recall claude | ambos | solo human | solo claude | ninguno |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    flagged_pairs = {c["pair_id"] for c in cases if c.get("pair_id") and c.get("leakage_flag")}
    for m in models:
        by_pair = defaultdict(dict)
        for r in results:
            if r["pair_id"] and r["model"] == m and r["targeted"] == "sin":
                by_pair[r["pair_id"]][r["author"]] = r
        for scope, pairs in (("todos", by_pair), ("sin flag", {k: v for k, v in by_pair.items() if k not in flagged_pairs})):
            for label, rf in (("1", one), ("4", four)):
                for n in NS:
                    hh = [(_hit(p["human"], n, rf), _hit(p["claude"], n, rf)) for p in pairs.values()
                          if "human" in p and "claude" in p]
                    if not hh:
                        continue
                    L.append(f"| {m} | {label} | {len(hh)} ({scope}) | {n} | {sum(h for h, _ in hh) / len(hh):.2f} | "
                             f"{sum(c for _, c in hh) / len(hh):.2f} | {sum(h and c for h, c in hh)} | "
                             f"{sum(h and not c for h, c in hh)} | {sum(c and not h for h, c in hh)} | "
                             f"{sum(not h and not c for h, c in hh)} |")
    L += ["", "Negativos: no hay casos `negative` (Constellate no dio veredictos `no`); se omiten.\n"]
    return "\n".join(L) + "\n"
