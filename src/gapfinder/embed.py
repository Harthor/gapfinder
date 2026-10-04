"""Embeddings del corpus (Fase 2).

Modelos: all-MiniLM-L6-v2 vs multilingual-e5-small (prefijos `query: ` / `passage: `). Texto de cada
item: título + cuerpo resuelto (`text.get_texts`), truncado por el tokenizer de cada modelo a su
máximo (256 / 512 tokens).

Los vectores (normalizados, float16) se guardan por bloques en data/cache/emb/<modelo>/<índice>/,
así una corrida cortada retoma desde el último bloque completo. El orden de los items queda fijo en
ids.json al empezar el índice.
- índice "corpus": todos los items menos los agregados por la búsqueda dirigida.
- índice "targeted": solo los agregados por la búsqueda dirigida (tabla `targeted`).
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from gapfinder.text import ItemText, get_texts

os.environ.setdefault("HF_HUB_OFFLINE", "1")  # los modelos ya están en la cache de HuggingFace
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

log = logging.getLogger(__name__)

EMB_DIR = Path("data/cache/emb")
CHUNK = 20_000
BATCH = 64


@dataclass(frozen=True, slots=True)
class Model:
    name: str
    query_prefix: str = ""
    passage_prefix: str = ""
    max_seq: int | None = None  # None = el máximo del modelo


MODELS = {
    "minilm": Model("sentence-transformers/all-MiniLM-L6-v2"),
    "e5": Model("intfloat/multilingual-e5-small", "query: ", "passage: "),  # descartado en la iteración 2
    # instrucción de query recomendada para bge v1.5 en retrieval; los pasajes van sin prefijo
    "bge": Model("BAAI/bge-base-en-v1.5", "Represent this sentence for searching relevant passages: ", "", 256),
}

ACTIVE = ["minilm", "bge"]  # "all" en la CLI

_loaded: dict[str, object] = {}


def _model(key: str):
    if key not in _loaded:
        import torch
        from sentence_transformers import SentenceTransformer

        device = "mps" if torch.backends.mps.is_available() else "cpu"
        _loaded[key] = SentenceTransformer(MODELS[key].name, device=device)
        if MODELS[key].max_seq:
            _loaded[key].max_seq_length = MODELS[key].max_seq
    return _loaded[key]


def item_text(t: ItemText) -> str:
    return f"{t.title}\n{t.body}".strip()


def _encode(key: str, texts: list[str], prefix: str) -> np.ndarray:
    """Normalizados. Se ordena por largo para que cada batch tenga poco padding."""
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
    vecs = _model(key).encode([prefix + texts[i] for i in order], batch_size=BATCH,
                              normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False)
    out = np.empty_like(vecs)
    out[order] = vecs
    return out


def encode_queries(key: str, texts: list[str]) -> np.ndarray:
    return _encode(key, texts, MODELS[key].query_prefix).astype(np.float32)


def encode_passages(key: str, texts: list[str]) -> np.ndarray:
    return _encode(key, texts, MODELS[key].passage_prefix).astype(np.float32)


def index_ids(conn: sqlite3.Connection, name: str) -> list[str]:
    ensure_targeted_table(conn)
    if name == "corpus":
        sql = "SELECT id FROM items WHERE id NOT IN (SELECT item_id FROM targeted) ORDER BY id"
    elif name == "targeted":
        sql = "SELECT item_id FROM targeted ORDER BY item_id"
    else:
        raise ValueError(name)
    return [r[0] for r in conn.execute(sql)]


def ensure_targeted_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS targeted (
               item_id  TEXT PRIMARY KEY REFERENCES items(id),  -- item que NO estaba en el corpus base
               case_id  TEXT NOT NULL,                          -- primer caso cuya búsqueda lo trajo
               query    TEXT NOT NULL,
               added_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')))"""
    )
    conn.commit()


def build(conn: sqlite3.Connection, key: str, name: str = "corpus") -> int:
    """Embebe el índice `name` con el modelo `key`, retomando bloques ya hechos. Devuelve cuántos embebió."""
    out = EMB_DIR / key / name
    out.mkdir(parents=True, exist_ok=True)
    ids_path = out / "ids.json"
    ids = index_ids(conn, name)
    if ids_path.exists() and name == "corpus":
        ids = json.loads(ids_path.read_text())  # orden fijo: los bloques ya hechos dependen de él
    else:
        if ids_path.exists() and json.loads(ids_path.read_text()) != ids:  # targeted creció: rehacer
            for f in out.glob("*.npy"):
                f.unlink()
        ids_path.write_text(json.dumps(ids))
    done = 0
    for n, start in enumerate(range(0, len(ids), CHUNK)):
        path = out / f"{n:05d}.npy"
        if path.exists():
            continue
        chunk = ids[start:start + CHUNK]
        texts = get_texts(conn, chunk)
        vecs = encode_passages(key, [item_text(texts[i]) for i in chunk]).astype(np.float16)
        tmp = path.with_suffix(".tmp.npy")
        np.save(tmp, vecs)
        tmp.rename(path)
        done += len(chunk)
        log.info("embed %s/%s: %d/%d", key, name, start + len(chunk), len(ids))
    return done


def load(key: str, name: str = "corpus") -> tuple[list[str], np.ndarray]:
    out = EMB_DIR / key / name
    ids = json.loads((out / "ids.json").read_text())
    blocks = sorted(p for p in out.glob("*.npy") if not p.name.endswith(".tmp.npy"))
    mat = np.concatenate([np.load(p) for p in blocks]) if blocks else np.zeros((0, 384), np.float16)
    if len(mat) != len(ids):
        raise RuntimeError(f"índice {key}/{name} incompleto: {len(mat)} de {len(ids)} vectores")
    return ids, mat
