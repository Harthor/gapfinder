"""Almacenamiento SQLite del corpus de oferta."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id               TEXT PRIMARY KEY,   -- '<source>:<native id>'
    source           TEXT NOT NULL,      -- 'show_hn' | 'github'
    url              TEXT NOT NULL,
    title            TEXT NOT NULL,
    description      TEXT NOT NULL DEFAULT '',
    readme           TEXT,               -- GitHub: README truncado (paso opcional)
    created_at       TEXT NOT NULL,      -- ISO 8601 UTC
    last_activity_at TEXT,               -- GitHub: pushed_at. HN: NULL
    stars            INTEGER,
    hn_points        INTEGER,
    hn_comments      INTEGER,
    archived         INTEGER,            -- GitHub: 0/1. HN: NULL
    extra            TEXT,               -- JSON con campos específicos de la fuente
    fetched_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);
CREATE INDEX IF NOT EXISTS items_source_created ON items(source, created_at);
CREATE INDEX IF NOT EXISTS items_id_lower ON items(lower(id));  -- join Show HN -> repo (GitHub no distingue mayúsculas)

-- Enriquecimiento de items sin descripción (hoy: Show HN). Una fila = intento hecho, aunque falle.
CREATE TABLE IF NOT EXISTS enrichment (
    item_id     TEXT PRIMARY KEY REFERENCES items(id),
    github_repo TEXT,                -- 'owner/repo' si la URL es un repo de GitHub
    method      TEXT NOT NULL,       -- github_corpus | github_readme | author_comment | author_reply | meta | failed
    text_origin TEXT,                -- 'author_comment' | 'author_reply' | 'current' | 'wayback' | 'title_only'
    snapshot_at TEXT,                -- timestamp del snapshot de Wayback usado
    description TEXT NOT NULL DEFAULT '',
    readme      TEXT,
    error       TEXT,
    fetched_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- Cache de comentarios del autor en su propio hilo de Show HN (vía Algolia /items/{id}).
-- Se guardan crudos para poder cambiar las reglas de extracción sin re-descargar.
CREATE TABLE IF NOT EXISTS hn_author_comments (
    item_id    TEXT PRIMARY KEY REFERENCES items(id),
    comments   TEXT NOT NULL,        -- JSON [{text, depth, created_at_i}] del autor, orden cronológico
    fetched_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- Estado de ingesta para reanudar sin re-descargar.
CREATE TABLE IF NOT EXISTS ingest_state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@dataclass(frozen=True, slots=True)
class Item:
    id: str
    source: str
    url: str
    title: str
    description: str
    created_at: str
    last_activity_at: str | None = None
    stars: int | None = None
    hn_points: int | None = None
    hn_comments: int | None = None
    archived: bool | None = None
    extra: str | None = None


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=120)  # espera si otro proceso está escribiendo
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(enrichment)")}
    for col in ("text_origin", "snapshot_at"):
        if col not in cols:
            conn.execute(f"ALTER TABLE enrichment ADD COLUMN {col} TEXT")
    conn.execute("UPDATE enrichment SET text_origin='current' WHERE text_origin IS NULL AND method LIKE 'github_%'")
    conn.commit()


def upsert_items(conn: sqlite3.Connection, items: list[Item]) -> int:
    """Inserta o actualiza (las señales de actividad cambian con el tiempo). Devuelve cuántos eran nuevos."""
    if not items:
        return 0
    before = count_items(conn)
    cols = list(Item.__dataclass_fields__)
    placeholders = ", ".join(f":{c}" for c in cols)
    updates = ", ".join(f"{c}=excluded.{c}" for c in cols if c != "id")
    conn.executemany(
        f"INSERT INTO items ({', '.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(id) DO UPDATE SET {updates}, fetched_at=strftime('%Y-%m-%dT%H:%M:%SZ', 'now')",
        [asdict(i) for i in items],
    )
    conn.commit()
    return count_items(conn) - before


def count_items(conn: sqlite3.Connection, source: str | None = None) -> int:
    if source is None:
        return conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    return conn.execute("SELECT COUNT(*) FROM items WHERE source=?", (source,)).fetchone()[0]


def get_state(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM ingest_state WHERE key=?", (key,)).fetchone()
    return row[0] if row else None


def set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO ingest_state (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()


def github_items_without_readme(conn: sqlite3.Connection, limit: int) -> list[str]:
    """full_name de repos sin README descargado, por estrellas descendente."""
    rows = conn.execute(
        "SELECT substr(id, 8) FROM items WHERE source='github' AND readme IS NULL "
        "ORDER BY stars DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [r[0] for r in rows]

