"""BM25 con SQLite FTS5 (iteración 2 de retrieval).

Índice en una base aparte (data/cache/fts.db) para no inflar corpus.db: por item, título + texto
resuelto (`text.get_texts`: descripción, README, comentarios del autor, meta, ...). Tokenizer porter
(raíces en inglés). Incremental: `build` solo agrega los items que falten (p. ej. los nuevos de la
búsqueda dirigida).

Consulta: las palabras de la query sin stopwords, las QUERY_TERMS más distintivas por idf, en OR,
ordenado por bm25 con el título pesando el doble que el cuerpo.
"""

from __future__ import annotations

import json
import logging
import math
import re
import sqlite3
from pathlib import Path

from gapfinder import leakage
from gapfinder.text import get_texts

log = logging.getLogger(__name__)

FTS_DB = Path("data/cache/fts.db")
CHUNK = 20_000
QUERY_TERMS = 24
MAX_DF_SHARE = 0.05   # términos en más del 5% de los docs: posting lists enormes y casi sin peso en bm25
TITLE_WEIGHT, BODY_WEIGHT = 2.0, 1.0


def connect(path: Path = FTS_DB) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5("
                 "item_id UNINDEXED, title, body, tokenize='porter unicode61')")
    return conn


def build(corpus: sqlite3.Connection, fts: sqlite3.Connection) -> int:
    have = {r[0] for r in fts.execute("SELECT item_id FROM docs")}
    ids = [r[0] for r in corpus.execute("SELECT id FROM items ORDER BY id") if r[0] not in have]
    for start in range(0, len(ids), CHUNK):
        chunk = ids[start:start + CHUNK]
        texts = get_texts(corpus, chunk)
        fts.executemany("INSERT INTO docs (item_id, title, body) VALUES (?, ?, ?)",
                        [(i, texts[i].title, texts[i].body) for i in chunk])
        fts.commit()
        log.info("fts: %d/%d", start + len(chunk), len(ids))
    return len(ids)


def match_query(text: str, idf: leakage.Idf, k: int = QUERY_TERMS) -> str:
    min_idf = math.log(1 / MAX_DF_SHARE)
    words = {w for w in re.findall(r"[a-z0-9]+", text.lower())
             if w not in leakage.STOPWORDS and not w.isdigit() and len(w) > 1 and idf(leakage.stem(w)) >= min_idf}
    best = sorted(words, key=lambda w: -idf(leakage.stem(w)))[:k]
    return " OR ".join(f'"{w}"' for w in best)


def search(fts: sqlite3.Connection, text: str, idf: leakage.Idf, limit: int) -> list[str]:
    """Top `limit` item_ids. Cacheado en la misma base (tabla search_cache) por consulta + límite:
    el resultado no depende del modelo de embeddings, así que cada eval lo reusa."""
    q = match_query(text, idf)
    if not q:
        return []
    fts.execute("CREATE TABLE IF NOT EXISTS search_cache (query TEXT, lim INTEGER, n_docs INTEGER, ids TEXT, "
                "PRIMARY KEY (query, lim, n_docs))")
    n_docs = fts.execute("SELECT max(rowid) FROM docs").fetchone()[0]  # cambia si el índice crece
    if (hit := fts.execute("SELECT ids FROM search_cache WHERE query=? AND lim=? AND n_docs=?",
                           (q, limit, n_docs)).fetchone()):
        return json.loads(hit[0])
    ids = [r[0] for r in fts.execute(
        f"SELECT item_id FROM docs WHERE docs MATCH ? ORDER BY bm25(docs, 0, {TITLE_WEIGHT}, {BODY_WEIGHT}) LIMIT ?",
        (q, limit))]
    fts.execute("INSERT OR REPLACE INTO search_cache VALUES (?, ?, ?, ?)", (q, limit, n_docs, json.dumps(ids)))
    fts.commit()
    return ids
