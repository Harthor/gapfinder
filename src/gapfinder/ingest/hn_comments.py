"""Comentarios del autor en su propio hilo de Show HN, como fuente de descripción.

Muchos Show HN con link externo no tienen cuerpo, pero el autor suele explicar el
proyecto en el hilo. Se baja el árbol con Algolia (`/api/v1/items/{id}`) y se guardan
crudos los comentarios del autor (texto, profundidad, fecha). Dos extracciones:

- author_comment: comentarios top-level del autor de >= MIN_CHARS, concatenados.
- author_reply (fallback): las primeras MAX_REPLIES intervenciones del autor a cualquier
  profundidad, cada una >= MIN_CHARS, concatenadas.

Rate limit documentado de Algolia HN: 10.000 requests/hora por IP (~166/min).
Se usa un RateLimiter global a 150/min por margen.
"""

from __future__ import annotations

import json
import logging
import random
import sqlite3
import statistics
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

import httpx

from gapfinder.http import RateLimiter
from gapfinder.ingest.github import RateLimited, github_repo_from_url
from gapfinder.ingest.hn import clean_html

log = logging.getLogger(__name__)

ITEMS_API = "https://hn.algolia.com/api/v1/items/{}"
DEFAULT_RPM = 150
MAX_TEXT = 1500
MIN_CHARS = 100
MAX_REPLIES = 3

_limiter: RateLimiter | None = None


def limiter(rpm: float = DEFAULT_RPM) -> RateLimiter:
    """Limiter único por proceso para hn.algolia.com."""
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter(rpm, "hn-items", base_backoff=30.0)
    return _limiter


class Comment(TypedDict):
    text: str
    depth: int
    created_at_i: int


def collect_author_comments(tree: dict, author: str) -> list[Comment]:
    """Todos los comentarios del autor en el hilo, limpios, en orden cronológico."""
    out: list[Comment] = []

    def walk(node: dict, depth: int) -> None:
        for c in node.get("children", []):
            if author and c.get("author") == author and c.get("text"):
                out.append(Comment(text=clean_html(c["text"]), depth=depth, created_at_i=c.get("created_at_i") or 0))
            walk(c, depth + 1)

    walk(tree, 1)
    return sorted(out, key=lambda c: c["created_at_i"])


def author_comment(comments: list[Comment]) -> str:
    valid = [c["text"] for c in comments if c["depth"] == 1 and len(c["text"]) >= MIN_CHARS]
    return "\n".join(valid)[:MAX_TEXT]


def author_reply(comments: list[Comment]) -> str:
    valid = [c["text"] for c in comments if len(c["text"]) >= MIN_CHARS][:MAX_REPLIES]
    return "\n".join(valid)[:MAX_TEXT]


def _fetch_tree(client: httpx.Client, lim: RateLimiter, hn_id: str, max_retries: int = 6) -> dict | None:
    for _ in range(max_retries):
        lim.wait()
        try:
            resp = client.get(ITEMS_API.format(hn_id))
        except httpx.TimeoutException:
            continue
        except httpx.TransportError:
            lim.penalize("conexión rechazada")
            continue
        if resp.status_code in (429, 503):
            ra = resp.headers.get("retry-after")
            lim.penalize(f"http {resp.status_code}", float(ra) if ra and ra.isdigit() else None)
            continue
        lim.success()
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    raise RateLimited(hn_id)


def fetch_author_comments(
    conn: sqlite3.Connection, item_ids: list[str], workers: int = 8
) -> dict[str, list[Comment]]:
    """Comentarios del autor por item, bajando solo los que no están en cache.
    Los items que no se pudieron bajar (rate limit persistente) no aparecen en el resultado."""
    if not item_ids:
        return {}
    marks = ",".join("?" * len(item_ids))
    got: dict[str, list[Comment]] = {
        r[0]: json.loads(r[1])
        for r in conn.execute(f"SELECT item_id, comments FROM hn_author_comments WHERE item_id IN ({marks})", item_ids)
    }
    missing = [i for i in item_ids if i not in got]
    if not missing:
        return got

    marks = ",".join("?" * len(missing))
    authors = {
        r[0]: (json.loads(r[1] or "{}").get("author") or "")
        for r in conn.execute(f"SELECT id, extra FROM items WHERE id IN ({marks})", missing)
    }
    lim = limiter()

    def one(item_id: str) -> tuple[str, list[Comment]] | None:
        try:
            tree = _fetch_tree(client, lim, item_id.split(":", 1)[1])
        except RateLimited:
            return None
        return item_id, collect_author_comments(tree or {}, authors.get(item_id, ""))

    with httpx.Client(timeout=30) as client, ThreadPoolExecutor(workers) as pool:
        fetched = [r for r in pool.map(one, missing) if r is not None]
    # Una sola transacción corta al final: no bloquear otros escritores mientras se baja.
    conn.executemany("INSERT OR REPLACE INTO hn_author_comments (item_id, comments) VALUES (?, ?)",
                     [(i, json.dumps(c)) for i, c in fetched])
    conn.commit()
    got.update(fetched)
    return got


# --- sonda de cobertura -------------------------------------------------------

STRATA = {"0-2": (0, 2), "3-9": (3, 9), ">=10": (10, 10**9)}


def probe(conn: sqlite3.Connection, per_stratum: int, examples: int, seed: int = 7) -> str:
    """Muestra estratificada de posts web sin descripción. Devuelve el reporte en texto."""
    rng = random.Random(seed)
    rows = conn.execute(
        "SELECT id, url, title, COALESCE(hn_points, 0), created_at FROM items "
        "WHERE source='show_hn' AND description='' AND url NOT LIKE 'https://news.ycombinator.com/%'"
    ).fetchall()
    web = [tuple(r) for r in rows if github_repo_from_url(r[1]) is None]

    sample: dict[str, list[tuple]] = {}
    for name, (lo, hi) in STRATA.items():
        pool = sorted(r for r in web if lo <= r[3] <= hi)
        sample[name] = rng.sample(pool, min(per_stratum, len(pool)))

    all_ids = [r[0] for rs in sample.values() for r in rs]
    got = fetch_author_comments(conn, all_ids)

    lines = [f"estrato  n   author_comment  +author_reply  largo mediano (comment)   [mín {MIN_CHARS} chars]"]
    for name, rs in sample.items():
        cs = [got[r[0]] for r in rs if r[0] in got]
        ac = [author_comment(c) for c in cs]
        ar = [not a and bool(author_reply(c)) for a, c in zip(ac, cs)]
        med = int(statistics.median(len(a) for a in ac if a)) if any(ac) else 0
        n = max(len(cs), 1)
        lines.append(f"{name:<7} {len(cs):>3}   {sum(map(bool, ac)) / n:>13.0%}  "
                     f"{(sum(map(bool, ac)) + sum(ar)) / n:>13.0%}  {med:>10}")

    with_text = [(name, r) for name, rs in sample.items() for r in rs if r[0] in got and author_comment(got[r[0]])]
    lines.append(f"\n{examples} ejemplos al azar (author_comment)")
    for name, r in rng.sample(with_text, min(examples, len(with_text))):
        text = author_comment(got[r[0]]).replace("\n", " ⏎ ")
        lines.append(f"\n[{name} pts={r[3]} {r[4][:4]}] {r[2]}\n  {text[:400]}{'…' if len(text) > 400 else ''}")
    return "\n".join(lines)
