"""Análisis de fallos: reales fuera del top-200 con embeddings MiniLM + llm5 (RRF). Escribe
data/eval/failures_real.md con query_core, rank de cada item esperado, su texto embebido y el top-5."""
import json, re, sqlite3
from pathlib import Path
import numpy as np
from gapfinder import embed, eval2, leakage
from gapfinder.text import get_texts

CASES = ["real-197bf4f9", "real-ecad36a5", "real-8b190bdc", "real-7c597ec1", "real-fbe3c4c2"]
ro = sqlite3.connect("file:data/corpus.db?mode=ro", uri=True)
idf = leakage.load_idf(ro, Path("data/cache/idf.json"))
llm = json.loads(Path("data/llm_queries.json").read_text())
cases = {c["id"]: c for c in json.loads(Path("data/known_cases.json").read_text())}
ids, mat = embed.load("minilm"); mat = mat.astype(np.float32)
def snip(t, n=320): return re.sub(r"\s+", " ", t)[:n]
L = ["# Fallos en reales: embeddings MiniLM + llm5 (RRF), sin búsqueda dirigida\n"]
for cid in CASES:
    c = cases[cid]; qs = eval2.query_sets(c, llm, idf)["llm5"]
    Q = embed.encode_queries("minilm", qs)
    lists = []
    for q in Q:
        s = mat @ q; top = np.argpartition(-s, eval2.TOP_K)[:eval2.TOP_K]
        lists.append([ids[i] for i in top[np.argsort(-s[top])]])
    fused = eval2.rrf(lists); pos = {i: n for n, i in enumerate(fused, 1)}
    exp = c["expected_item_ids"]; texts = get_texts(ro, exp + fused[:5])
    L += [f"## {cid} — {c['title']}\n", f"**query_core:** {qs[0]}\n", "**Items esperados** (rank en la lista fusionada; — = fuera del top-2000 de las 5 consultas):\n"]
    for e in sorted(exp, key=lambda e: pos.get(e, 10**9)):
        t = texts[e]
        L.append(f"- `{e}` rank **{pos.get(e, '—')}** · text_origin `{t.origin}` · {len(t.body)} chars\n  > {t.title} — {snip(t.body)}")
    L.append("\n**Top-5 que trajo:**\n")
    for n, i in enumerate(fused[:5], 1):
        t = texts[i]
        url = ro.execute("SELECT url FROM items WHERE id=?", (i,)).fetchone()[0]
        L.append(f"{n}. `{i}` ({t.origin}) {url}\n   > {t.title} — {snip(t.body, 220)}")
    L.append("")
Path("data/eval/failures_real.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
