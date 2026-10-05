"""Holdout temporal: ¿cómo se comporta el sistema frente a ideas que todavía no existían?

Se elige una fecha de corte T. El corpus queda restringido a lo anterior a T (Show HN publicados y
repos creados antes de T); las ideas son Show HN posteriores a T. Para cada idea se describe la
necesidad sin nombrar el producto (mismo método que los known cases: prompt v2, llm5, RRF), se
recupera el top-1000 sobre el corpus restringido (embeddings MiniLM existentes, filtrados por fecha)
y se verifica con Jev. Un "no" es un candidato a hueco-en-T; un "ya construido" sugiere que la idea ya
tenía un equivalente antes de T.

Archivos en data/holdout/: ideas.json (muestra), llm_queries.json (consultas de Claude),
candidates.json (top-1000 por idea). Veredictos: data/phase3/verdicts_jev_holdout.jsonl.
"""

from __future__ import annotations

import json
import logging
import random
import re
import sqlite3
from pathlib import Path

import numpy as np

from gapfinder import embed, eval2
from gapfinder.real_cases import github_key, site_domain
from gapfinder.text import get_texts, iter_texts
from gapfinder.verify import CANDIDATE_CHARS, Pair

log = logging.getLogger(__name__)

T = "2024-01-01"
DIR = Path("data/holdout")
MIN_POINTS = 20
MIN_CHARS = 400
SEED = 11
K = 1000
# Versiones o relanzamientos de algo previo, por el título.
_RELAUNCH_RE = re.compile(
    r"\b(v\d+(\.\d+)*|\d+\.\d+(\.\d+)?|version \d+|relaunch\w*|re-launch\w*|launch\w* again|new version|"
    r"now with|is back|returns|reborn|rewrit\w*|revisited|redesign\w*|reboot\w*|updated?|updates)\b", re.IGNORECASE)


def _pre_t_index(conn: sqlite3.Connection, t: str) -> tuple[set[str], set[str]]:
    """Repos (github:owner/repo en minúsculas) creados antes de T y dominios de Show HN anteriores a T."""
    repos = {r[0].lower() for r in conn.execute(
        "SELECT id FROM items WHERE source = 'github' AND created_at < ?", (t,))}
    domains = set()
    for (url,) in conn.execute("SELECT url FROM items WHERE source = 'show_hn' AND created_at < ?", (t,)):
        if (d := site_domain(url)):
            domains.add(d)
    return repos, domains


def select_ideas(conn: sqlite3.Connection, n: int = 50, t: str = T, seed: int = SEED) -> list[dict]:
    """Show HN posteriores a T con >= MIN_POINTS puntos y >= MIN_CHARS de texto real (no title_only),
    sin versiones/relanzamientos de algo previo. Devuelve una lista barajada (semilla fija): se puede
    cortar a las primeras N si el presupuesto no alcanza. Guarda también los descartes y sus motivos."""
    repos, domains = _pre_t_index(conn, t)
    linked = dict(conn.execute("SELECT item_id, github_repo FROM enrichment WHERE github_repo IS NOT NULL"))
    eligible, excluded = [], {"titulo_relanzamiento": 0, "repo_anterior_a_T": 0, "dominio_con_show_hn_anterior": 0}
    meta = {i: (u, ts, p) for i, u, ts, p in conn.execute(
        "SELECT id, url, created_at, hn_points FROM items WHERE source = 'show_hn' AND created_at >= ? "
        "AND hn_points >= ? AND id NOT IN (SELECT item_id FROM targeted)", (t, MIN_POINTS))}
    for txt in iter_texts(conn, "i.source = 'show_hn' AND i.created_at >= ? AND i.hn_points >= ?", (t, MIN_POINTS)):
        if txt.item_id not in meta or txt.origin == "title_only" or len(txt.body) < MIN_CHARS:
            continue
        url, created, points = meta[txt.item_id]
        repo = (github_key(url) or (f"github:{linked[txt.item_id]}" if txt.item_id in linked else "")).lower()
        if _RELAUNCH_RE.search(txt.title):
            excluded["titulo_relanzamiento"] += 1
        elif repo and repo in repos:
            excluded["repo_anterior_a_T"] += 1
        elif (d := site_domain(url)) and d in domains:
            excluded["dominio_con_show_hn_anterior"] += 1
        else:
            eligible.append({"item_id": txt.item_id, "title": txt.title, "url": url, "created_at": created,
                             "points": points, "text_origin": txt.origin, "text_chars": len(txt.body)})
    eligible.sort(key=lambda x: x["item_id"])
    random.Random(seed).shuffle(eligible)
    DIR.mkdir(parents=True, exist_ok=True)
    out = {"T": t, "filters": {"min_points": MIN_POINTS, "min_chars": MIN_CHARS, "seed": seed,
                               "relaunch_title_regex": _RELAUNCH_RE.pattern},
           "eligible": len(eligible), "excluded": excluded, "ideas": eligible[:n]}
    (DIR / "ideas.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out["ideas"]


# --- consultas (mismo método que los known cases, prompt v2) ---------------------------------------


def idea_cases(conn: sqlite3.Connection, ideas: list[dict]) -> list[dict]:
    """Cada Show HN como un 'caso' para llm.generate: título + texto del producto."""
    texts = get_texts(conn, [i["item_id"] for i in ideas])
    return [{"id": f"hold-{i['item_id'].split(':')[1]}", "kind": "holdout", "item_id": i["item_id"],
             "title": texts[i["item_id"]].title, "description": texts[i["item_id"]].body[:2500]} for i in ideas]


def leakage_terms(conn: sqlite3.Connection, idea: dict) -> list[str]:
    """Nombre del producto (primer segmento del título si es raro en inglés), nombre del repo y del dominio."""
    from wordfreq import zipf_frequency

    parts = re.split(r"\s[–—|-]\s|:\s", idea["title"])
    terms = set()
    if len(parts) > 1:   # "Nombre – descripción": el primer segmento es el nombre del producto
        words = [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9.+#-]*", parts[0]) if len(w) > 2]
        terms |= {w.lower() for w in words if zipf_frequency(w.lower(), "en") < 3.0}   # raras = marca
    if (k := github_key(idea["url"])):
        terms.add(k.split("/")[-1].lower())
    if (d := site_domain(idea["url"])):
        terms.add(d.split(".")[0].lower())
    return sorted(t for t in terms if len(t) > 2)


def flag_leakage(conn: sqlite3.Connection, ideas: list[dict], queries: dict) -> dict[str, list[str]]:
    """{case_id: términos del producto que aparecen en query_core/reformulaciones/keywords}."""
    out = {}
    for case in idea_cases(conn, ideas):
        q = queries.get(case["id"])
        if not q:
            continue
        text = " ".join([q.get("query_core", "")] + q.get("reformulations", []) + q.get("keyword_queries", [])).lower()
        hits = [t for t in leakage_terms(conn, {"title": case["title"], "url": next(
            i["url"] for i in ideas if i["item_id"] == case["item_id"])}) if re.search(rf"\b{re.escape(t)}\b", text)]
        if hits:
            out[case["id"]] = hits
    return out


# --- retrieval sobre el corpus restringido -----------------------------------------------------------


def retrieve(conn: sqlite3.Connection, cases: list[dict], queries: dict, t: str = T, k: int = K) -> dict[str, list[str]]:
    """Top-k por idea con MiniLM + llm5 (RRF), solo entre items anteriores a T. Reutiliza los
    embeddings del índice corpus (no re-embebe): los posteriores a T quedan con score -inf."""
    ids, mat = embed.load("minilm", "corpus")
    mat = mat.astype(np.float32)
    created = dict(conn.execute("SELECT id, created_at FROM items"))
    allowed = np.array([created.get(i, "9999") < t for i in ids])
    log.info("holdout: %d de %d items anteriores a %s", int(allowed.sum()), len(ids), t)
    out = {}
    for case in cases:
        q = queries[case["id"]]
        texts = [q["query_core"], *q["reformulations"]]
        lists = []
        for v in embed.encode_queries("minilm", texts):
            s = mat @ v
            s[~allowed] = -np.inf
            top = np.argpartition(-s, eval2.TOP_K)[:eval2.TOP_K]
            lists.append([ids[i] for i in top[np.argsort(-s[top])]])
        out[case["id"]] = eval2.rrf(lists)[:k]
    (DIR / "candidates.json").write_text(json.dumps(out))
    return out


def pairs(conn: sqlite3.Connection, candidates: dict[str, list[str]], queries: dict) -> list[Pair]:
    all_ids = sorted({i for c in candidates.values() for i in c})
    texts = get_texts(conn, all_ids)
    return [Pair(cid, queries[cid]["query_core"], i, texts[i].title, texts[i].body[:CANDIDATE_CHARS])
            for cid, items in candidates.items() for i in items]


def selected_cases(conn: sqlite3.Connection) -> tuple[list[dict], list[dict], dict]:
    """Ideas elegidas (software, en el orden barajado), sus casos y sus consultas."""
    ideas = {i["item_id"]: i for i in json.loads((DIR / "ideas.json").read_text())["ideas"]}
    chosen = [ideas[i] for i in json.loads((DIR / "selected.json").read_text())]
    return chosen, idea_cases(conn, chosen), json.loads((DIR / "llm_queries.json").read_text())


def verify_with_budget(all_pairs: list[Pair], budget_usd: float, name: str = "jev_holdout",
                       per_pair_estimate: float = 0.000035, chunk: int = 5000) -> dict:
    """Jev vía OpenRouter por tandas; antes de cada tanda verifica que el gasto acumulado (usage.cost real)
    más el estimado de la tanda no supere el presupuesto. Reanudable (los pares hechos se saltean)."""
    from gapfinder.verify import OpenRouterJevVerifier, load_done

    verifier = OpenRouterJevVerifier(name=name)
    for start in range(0, len(all_pairs), chunk):
        done = load_done(name)
        spent = sum(v.cost_usd or 0 for v in done.values())
        part = [p for p in all_pairs[start:start + chunk] if (p.case_id, p.item_id) not in done]
        if not part:
            continue
        if spent + len(part) * per_pair_estimate > budget_usd:
            log.warning("holdout: presupuesto: gastado $%.3f, la próxima tanda (~$%.3f) superaría $%.2f; me detengo",
                        spent, len(part) * per_pair_estimate, budget_usd)
            break
        verifier.verify(part)
    done = load_done(name)
    return {"pares": len(done), "costo_usd": round(sum(v.cost_usd or 0 for v in done.values()), 4)}


BUILT, REVIEW = 0.90, 0.85   # regla calibrada en la Fase 3


def decide(core: float) -> str:
    return "ya construido" if core >= BUILT else "revisar" if core >= REVIEW else "no"


def report(conn: sqlite3.Connection, out_path: Path = Path("data/eval/holdout_temporal.md"),
           verdicts_name: str = "jev_holdout") -> str:
    from collections import Counter

    from gapfinder.verify import load_done

    sel = json.loads((DIR / "ideas.json").read_text())
    chosen, hcases, queries = selected_cases(conn)
    cand = json.loads((DIR / "candidates.json").read_text())
    ver = load_done(verdicts_name)
    meta = {i: (t, u, c) for i, t, u, c in conn.execute("SELECT id, title, url, created_at FROM items")}
    leaks = flag_leakage(conn, chosen, queries)
    claude_cost = sum((v["usage"]["input_tokens"] * 5 + v["usage"]["output_tokens"] * 25) / 1e6
                      for v in queries.values() if "usage" in v)
    jev_cost = sum(v.cost_usd or 0 for v in ver.values())
    rows = []
    for case, idea in zip(hcases, chosen):
        scored = sorted((i for i in cand.get(case["id"], []) if (case["id"], i) in ver), key=lambda i: -ver[(case["id"], i)].core)
        if len(scored) < len(cand.get(case["id"], [])):
            rows.append((case, idea, None, scored))   # verificación incompleta (presupuesto o error)
            continue
        rows.append((case, idea, decide(ver[(case["id"], scored[0])].core), scored))
    complete = [r for r in rows if r[2]]
    dist = Counter(r[2] for r in complete)
    L = ["# Holdout temporal: ¿qué dice el sistema de ideas que todavía no existían?\n",
         f"Corte **T = {T}**. Corpus restringido: Show HN publicados y repos GitHub (>= 100★) creados antes de T "
         f"({sum(1 for c in meta.values() if c[2] < T):,} items; embeddings MiniLM existentes filtrados por fecha, sin re-embeber). "
         f"Ideas: Show HN posteriores a T. Regla de la Fase 3: P(núcleo) >= {BUILT} ya construido, {REVIEW}-{BUILT} revisar, < {REVIEW} no.\n",
         "## Cómo se eligieron las ideas\n",
         f"- Por qué T = {T}: deja ~136 mil Show HN y ~402 mil repos antes, y ~82 mil Show HN después (2024-2026). "
         "Un corte más tardío daría más corpus pero menos ventana posterior y más cerca de la fecha en que se midieron las estrellas.",
         f"- Filtro: >= {sel['filters']['min_points']} puntos, >= {sel['filters']['min_chars']} caracteres de texto real "
         "(no title_only). Fuera versiones/relanzamientos: título con v2/2.0/relaunch/now with/is back/rewrite… "
         f"({sel['excluded']['titulo_relanzamiento']}), repo de GitHub enlazado creado antes de T ({sel['excluded']['repo_anterior_a_T']}), "
         f"dominio con un Show HN anterior a T ({sel['excluded']['dominio_con_show_hn_anterior']}). Elegibles: {sel['eligible']:,}.",
         f"- Muestra barajada con semilla {sel['filters']['seed']}; se generaron consultas para las primeras {len(queries)} y se "
         f"quedaron las primeras {len(chosen)} que Claude clasificó como herramienta de software (las otras: juegos, arte, demos).",
         f"- **{len(chosen)} ideas y no 50** por el tope de $2.00 de la sesión (Claude + Jev; ver Costos). Top-K = {K} sin recortar.",
         "- Descripciones: mismo método que los known cases (Claude, prompt v2, llm5 + RRF). No pueden nombrar producto, marca ni URL; "
         f"`leakage_flag` si el nombre/dominio/repo del producto aparece igual: {len(leaks)} ideas ({', '.join(f'{k} ({v})' for k, v in leaks.items()) or 'ninguna'}). "
         "Ambas son términos de categoría que coinciden con el nombre; se dejaron en la muestra marcadas.\n",
         "## Resultado\n",
         f"Ideas verificadas completas: {len(complete)}/{len(rows)}.\n",
         "| decisión | ideas |", "|---|---|"]
    for d in ("ya construido", "revisar", "no"):
        L.append(f"| {d} | {pct(dist.get(d, 0), len(complete))} |")
    L += ["", "Lectura: \"ya construido\" = el sistema encuentra un equivalente anterior a T (a adjudicar: ¿lo es de verdad?). "
          "\"no\" = candidata a hueco-en-T: no hay nada anterior a T en el corpus que Jev considere el núcleo.\n"]
    def cand_line(cid, i):
        t, u, c = meta.get(i, ("?", "", "?"))
        return f"  - {ver[(cid, i)].core:.2f} · **{t[:90]}** · creado {c[:10]} · {u}"
    for d, title in (("no", "## Candidatas a hueco-en-T (decisión: no) — 3 mejores candidatos"),
                     ("revisar", "## Revisar (0.85-0.90) — mejor candidato"),
                     ("ya construido", "## Ya construido (>= 0.90) — mejor candidato")):
        sel_rows = [r for r in complete if r[2] == d]
        L += ["", title + "\n"]
        for case, idea, _, scored in sorted(sel_rows, key=lambda r: ver[(r[0]["id"], r[3][0])].core):
            flag = " · ⚠️ leakage_flag" if case["id"] in leaks else ""
            L.append(f"- `{case['id']}` · idea posterior a T: **{idea['title'][:90]}** ({idea['created_at'][:10]}, {idea['points']} pts){flag}  \n"
                     f"  {idea['url']}  \n  Necesidad: {queries[case['id']]['query_core']}")
            for i in scored[:3 if d == "no" else 1]:
                L.append(cand_line(case["id"], i))
    incomplete = [r for r in rows if not r[2]]
    if incomplete:
        L += ["", f"## Sin verificar completas ({len(incomplete)})\n"] + [f"- `{r[0]['id']}` {r[1]['title'][:80]}" for r in incomplete]
    L += ["", "## Costos\n",
          f"- Claude (claude-opus-5, {len(queries)} ideas con consultas): ${claude_cost:.3f}, calculado con los tokens de cada respuesta a $5/$25 por millón.",
          f"- Jev vía OpenRouter: {len(ver):,} pares, ${jev_cost:.3f} (usage.cost facturado).",
          f"- Total de la sesión: ${claude_cost + jev_cost:.3f} (tope: $2.00).\n",
          "## Caveats\n",
          "- **Cobertura**: una idea posterior a T puede tener un equivalente anterior a T que no está en el corpus (Show HN + GitHub >= 100★). "
          "Un \"no\" no prueba que fuera un hueco; prueba que este corpus no lo tenía.",
          "- **Estrellas**: el umbral de >= 100★ se mide hoy, no en T. Repos creados antes de T que llegaron a 100★ después están en el corpus "
          "restringido, y repos que tenían >= 100★ en T pero no hoy faltan.",
          "- **Funcionalidad posterior**: un repo creado antes de T pudo agregar la funcionalidad después; su README es el de hoy. "
          "Un \"ya construido\" puede deberse a eso (el texto de los Show HN sí es el de su fecha).",
          "- **Ideas lanzadas en HN**: son productos que alguien construyó; un \"no\" es \"novedoso respecto del corpus en T\", no demanda.",
          "- Muestra chica (35) y regla calibrada en la Fase 3 con otros datos; las decisiones requieren adjudicación humana.\n"]
    text = "\n".join(L) + "\n"
    out_path.write_text(text)
    return text


def pct(a: int, b: int) -> str:
    return f"{a}/{b} ({a / b:.0%})" if b else "–"
