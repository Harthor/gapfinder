"""Búsqueda dirigida por idea (Fase 2).

Para cada caso de known_cases.json se arman consultas de palabras clave (las de mayor idf de la
necesidad; en real/partial también de su descripción) y se buscan en:
- la Search API de GitHub, sin filtro de estrellas (el corpus base solo tiene >= 100),
- Algolia HN, solo Show HN, por relevancia.
Lo que no estaba en el corpus se agrega a `items` y queda registrado en la tabla `targeted`
(origen `targeted`), así el eval puede reportar recall con y sin este paso. Cada consulta hecha queda
en `ingest_state`, así que re-correr no repite requests.
"""

from __future__ import annotations

import logging
import math
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

from gapfinder import db, leakage
from gapfinder.embed import ensure_targeted_table
from gapfinder.http import get_json
from gapfinder.ingest import github, hn

log = logging.getLogger(__name__)

HN_SEARCH = "https://hn.algolia.com/api/v1/search"
PER_QUERY = 30
MIN_DF = 20  # más raras que esto suelen ser errores de tipeo, compuestos únicos o nombres propios del texto
# Palabras de la forma de pedir, no del producto.
_ASK_WORDS = frozenset("""
want wants need needs looking like way tool tools app apps someone something help able find make without instead
into own i'd i'm im let lets allow allows simple simply easy quick quickly thing things place kind good best new
""".split())


def keywords(text: str, idf: leakage.Idf, k: int) -> list[str]:
    """Las k palabras más de producto y más distintivas, sin repetir raíz, en su forma original.

    Puntaje = especificidad técnica (log de frecuencia en el corpus / frecuencia en inglés general,
    wordfreq) + idf en el corpus. El idf solo favorece palabras comunes del inglés que casi no
    aparecen en descripciones de productos ("rather", "neighborhood"); la especificidad sola favorece
    vocabulario técnico genérico ("server", "code"). Palabras con df < MIN_DF quedan afuera.
    """
    from wordfreq import word_frequency

    words = {w for w in re.findall(r"[a-z0-9][a-z0-9+#.-]*[a-z0-9+#]", text.lower())
             if w not in leakage.STOPWORDS and w not in _ASK_WORDS and not w.isdigit() and len(w) > 2}
    scores = {}
    for w in words:
        df = idf.df.get(leakage.stem(w), 0)
        if df >= MIN_DF:
            specificity = math.log((df / idf.n_docs) / max(word_frequency(w, "en"), 1e-7))
            scores[w] = specificity + idf(leakage.stem(w))
    seen, ranked = set(), []
    for w in sorted(scores, key=lambda w: -scores[w]):
        if (s := leakage.stem(w)) not in seen:
            seen.add(s)
            ranked.append(w)
    return ranked[:k]


def case_queries(case: dict, idf: leakage.Idf) -> list[str]:
    desc = re.sub(r"\s+\S*$", "", case.get("description", "")[:400])  # sin cortar la última palabra
    text = case["title"] + (" " + desc if desc else "")
    words = keywords(text, idf, 3)
    return list(dict.fromkeys(q for q in (" ".join(words), " ".join(words[:2])) if q))


def ensure_llm_table(conn: sqlite3.Connection) -> None:
    """Qué items fuera del corpus base trajo cada consulta de palabras clave generada con Claude."""
    conn.execute(
        """CREATE TABLE IF NOT EXISTS targeted_llm (
               item_id TEXT NOT NULL REFERENCES items(id),
               case_id TEXT NOT NULL,
               query   TEXT NOT NULL,
               PRIMARY KEY (item_id, case_id, query))"""
    )
    conn.commit()


def run(conn: sqlite3.Connection, cases: list[dict], idf_path: Path = Path("data/cache/idf.json"),
        llm_queries: dict | None = None) -> dict:
    """llm_queries: {case_id: {"keyword_queries": [...]}} -> usa esas consultas (y registra los hits
    fuera del corpus base en `targeted_llm`); si no, las de plantilla (`case_queries`)."""
    ensure_targeted_table(conn)
    if llm_queries is not None:
        ensure_llm_table(conn)
    idf = leakage.load_idf(conn, idf_path)
    known = {r[0].lower() for r in conn.execute("SELECT id FROM items")}
    base = known - {r[0].lower() for r in conn.execute("SELECT item_id FROM targeted")}
    throttle = github._Throttle(28)
    stats = {"queries": 0, "github_new": 0, "show_hn_new": 0, "hits_outside_base": 0}
    with github._client() as gh, httpx.Client(timeout=30) as hc:
        for case in cases:
            queries = (llm_queries.get(case["id"], {}).get("keyword_queries", []) if llm_queries is not None
                       else case_queries(case, idf))
            for q in queries:
                for source in ("github", "show_hn"):
                    key = (f"targeted:llm:{source}:{case['id']}:{q}" if llm_queries is not None
                           else f"targeted:done:{source}:{q}")
                    if db.get_state(conn, key):
                        continue
                    if source == "github":
                        throttle.wait()
                        data, _ = get_json(gh, github.API, {"q": q, "per_page": PER_QUERY})
                        items = [github.parse_repo(r) for r in data.get("items", [])]
                    else:
                        data, _ = get_json(hc, HN_SEARCH, {"query": q, "tags": "show_hn", "hitsPerPage": PER_QUERY})
                        items = [i for h in data.get("hits", []) if (i := hn.parse_hit(h))]
                    fresh = [i for i in items if i.id.lower() not in known]
                    if llm_queries is not None:
                        outside = [i for i in items if i.id.lower() not in base]
                        conn.executemany("INSERT OR IGNORE INTO targeted_llm (item_id, case_id, query) VALUES (?, ?, ?)",
                                         [(i.id, case["id"], q) for i in outside])
                        stats["hits_outside_base"] += len(outside)
                    if fresh:
                        db.upsert_items(conn, fresh)
                        conn.executemany("INSERT OR IGNORE INTO targeted (item_id, case_id, query) VALUES (?, ?, ?)",
                                         [(i.id, case["id"], q) for i in fresh])
                        known.update(i.id.lower() for i in fresh)
                        stats[f"{source}_new"] += len(fresh)
                    db.set_state(conn, key, "1")
                    stats["queries"] += 1
            log.info("targeted: %s %s", case["id"], stats)
    stats["readmes"] = _fetch_readmes(conn)
    return stats


def _fetch_readmes(conn: sqlite3.Connection) -> int:
    """README de los repos agregados que todavía no lo tienen (mismo tratamiento que el bulk).
    Se calcula desde la base, así una corrida cortada los completa en la siguiente."""
    names = [r[0] for r in conn.execute(
        "SELECT substr(i.id, 8) FROM targeted t JOIN items i ON i.id = t.item_id "
        "WHERE i.source = 'github' AND i.readme IS NULL")]
    if not names:
        return 0
    with httpx.Client(timeout=20, follow_redirects=True) as client, ThreadPoolExecutor(8) as pool:
        got = [(r, f"github:{n}") for n, r in zip(names, pool.map(lambda n: github._try_readme(client, n), names))
               if r is not None]
    conn.executemany("UPDATE items SET readme=? WHERE id=?", got)
    conn.commit()
    return len(got)
