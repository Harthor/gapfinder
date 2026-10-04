"""Compara retrieval con consultas v1 vs v2 (v2 permite términos de categoría). MiniLM, sin dirigida."""
import json
from pathlib import Path
v1 = [r for r in json.load(open("data/eval/iter2_ranks.json")) if r["model"] in ("minilm", "-")]
v2 = json.load(open("data/eval/iter2_v2/iter2_ranks.json"))
cases = {c["id"]: c for c in json.load(open("data/known_cases.json"))}
GROUPS = [("real", lambda r: r["kind"] == "real"),
          ("real sin label_note", lambda r: r["kind"] == "real" and not r.get("label_note")),
          ("partial sin heurísticos", lambda r: r["kind"] == "partial" and not r["heuristic"]),
          ("partial (todos)", lambda r: r["kind"] == "partial" and r["heuristic"])]
def rec(rows, n):
    rows = [r for r in rows if r["n_expected"]]
    return sum(r["rank"] <= n for r in rows) / len(rows), len(rows)
L = ["# query_core v1 vs v2 (v2 permite términos de categoría)\n",
     "MiniLM, sin búsqueda dirigida. Sintéticos no cambian (mismas consultas). v1 = data/eval/iter2_recall.md; "
     "v2 = data/eval/iter2_v2/iter2_recall.md.\n",
     "| casos | sistema | consultas | n | R@50 v1 → v2 | R@200 v1 → v2 | R@1000 v1 → v2 |", "|---|---|---|---|---|---|---|"]
for gname, f in GROUPS:
    for system in ("emb", "hybrid", "bm25"):
        for qs in ("core", "llm5"):
            a = [r for r in v1 if f(r) and r["variant"] == "sin" and r["system"] == system and r["queries"] == qs]
            b = [r for r in v2 if f(r) and r["variant"] == "sin" and r["system"] == system and r["queries"] == qs]
            cells = [f"{rec(a, n)[0]:.2f} → {rec(b, n)[0]:.2f}" for n in (50, 200, 1000)]
            L.append(f"| {gname} | {system} | {qs} | {rec(a, 50)[1]} | " + " | ".join(cells) + " |")
L += ["", "## Reales: rank del primer item esperado (emb MiniLM + llm5)\n", "| caso | label_note | v1 | v2 |", "|---|---|---|---|"]
key = lambda rows: {r["case"]: r["rank"] for r in rows if r["kind"] == "real" and r["variant"] == "sin" and r["system"] == "emb" and r["queries"] == "llm5"}
k1, k2 = key(v1), key(v2)
fmt = lambda x: "—" if x >= 10**9 else str(x)
for cid in sorted(k1):
    L.append(f"| {cid} | {'sí' if cases[cid].get('label_note') else ''} | {fmt(k1[cid])} | {fmt(k2[cid])} |")
Path("data/eval/compare_prompt_v1_v2.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
