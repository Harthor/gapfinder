"""Texto de cada item para embeber/mostrar, con su origen.

Orígenes:
- native: descripción propia del item (cuerpo del Show HN, descripción/topics del repo) + README si hay.
- github_corpus: Show HN que linkea a un repo presente en el corpus -> texto de ese repo.
- current (README bajado o meta actual), author_comment, author_reply, wayback: ver ingest.enrich.
- title_only: no hay nada más que el título.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass

ENRICHED_ORIGINS = {"native", "github_corpus", "current", "author_comment", "author_reply", "wayback"}


@dataclass(frozen=True, slots=True)
class ItemText:
    item_id: str
    source: str
    title: str
    body: str
    origin: str

    @property
    def enriched(self) -> bool:
        return self.origin != "title_only"


_QUERY = """
SELECT i.id, i.source, i.title, i.description, i.readme,
       e.text_origin, e.description, e.readme,
       g.description, g.readme
FROM items i
LEFT JOIN enrichment e ON e.item_id = i.id
LEFT JOIN items g ON e.github_repo IS NOT NULL AND lower(g.id) = lower('github:' || e.github_repo)
"""


def _join(*parts: str | None) -> str:
    return "\n".join(p.strip() for p in parts if p and p.strip())


def _resolve(row: sqlite3.Row | tuple) -> ItemText:
    item_id, source, title, desc, readme, e_origin, e_desc, e_readme, g_desc, g_readme = row
    if desc or readme:
        return ItemText(item_id, source, title, _join(desc, readme), "native")
    if g_desc or g_readme:  # el repo linkeado está en el corpus: su texto es el más completo
        return ItemText(item_id, source, title, _join(g_desc, g_readme), "github_corpus")
    if body := _join(e_desc, e_readme):
        return ItemText(item_id, source, title, body, e_origin or "current")
    return ItemText(item_id, source, title, "", "title_only")


def iter_texts(conn: sqlite3.Connection, where: str = "", params: tuple = ()) -> Iterator[ItemText]:
    for row in conn.execute(_QUERY + (f" WHERE {where}" if where else ""), params):
        yield _resolve(tuple(row))


def get_texts(conn: sqlite3.Connection, item_ids: list[str]) -> dict[str, ItemText]:
    out: dict[str, ItemText] = {}
    for start in range(0, len(item_ids), 500):
        chunk = item_ids[start:start + 500]
        out.update((t.item_id, t) for t in iter_texts(conn, f"i.id IN ({','.join('?' * len(chunk))})", tuple(chunk)))
    return out
