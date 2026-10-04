"""Precalcula (y deja en la caché de fts.db) las búsquedas BM25 que usa eval2."""
import json, logging, sqlite3
from pathlib import Path
from gapfinder import bm25, eval2, leakage
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
ro = sqlite3.connect("file:data/corpus.db?mode=ro", uri=True)
idf = leakage.load_idf(ro, Path("data/cache/idf.json"))
llm = json.loads(Path("data/llm_queries.json").read_text())
cases = json.loads(Path("data/known_cases.json").read_text())
texts = sorted({t for c in cases for ts in eval2.query_sets(c, llm, idf).values() for t in ts})
limit = eval2.TOP_K + ro.execute("SELECT COUNT(*) FROM targeted").fetchone()[0]
fts = bm25.connect()
for n, t in enumerate(texts, 1):
    bm25.search(fts, t, idf, limit)
    if n % 50 == 0:
        logging.info("bm25 precompute: %d/%d", n, len(texts))
logging.info("bm25 precompute: listo (%d consultas, límite %d)", len(texts), limit)
