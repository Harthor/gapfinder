"""Datos del sitio público (site/): los huecos fuertes y la zona gris con sus candidatos, más las cifras del método.

`export(conn)` escribe site/data.json desde los veredictos cacheados y los reportes de data/eval/; no llama a ninguna
API. El texto va en inglés: es lo que se muestra en el sitio.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from gapfinder import askhn, gaps

OUT = Path("site/data.json")
RECALL_REPORT = Path("data/eval/iter2_recall.md")
HOLDOUT_REPORT = Path("data/eval/holdout_review_result.md")
SAYS = {"e": "it exists", "p": "partly exists", "n": "does not exist", "?": "unclear"}
TIER_IDS = {"match": "already_built", "no_software": "not_software", "descartado": "said_to_exist",
            "gris": "grey_zone", "fuerte": "strong_gap"}
# Conteos de las revisiones humanas y casos conocidos (data/eval/*.md); el sitio calcula los intervalos.
METRICS = [
    {"stage": "Search", "metric": "Known answer among the top 1,000 candidates (real cases)", "k": 11, "n": 12,
     "source": "data/eval/iter2_recall.md"},
    {"stage": "Judge", "metric": "Agrees with a human on “does it implement the core need?”", "k": 30, "n": 34,
     "source": "data/eval/pilot_review_result.md"},
    {"stage": "Alarms", "metric": "Matches scored ≥ 0.90 that a human confirmed as real implementations", "k": 15,
     "n": 15, "source": "data/eval/phase3_report.md"},
    {"stage": "Holdout", "metric": "Ideas called a gap that a human confirmed as a real gap", "k": None, "n": None,
     "source": "data/eval/holdout_review_result.md"},
]


def recall_rows(text: str) -> list[dict]:
    """Filas `real · emb · minilm` de iter2_recall.md: R@50/200/1000 por estilo de consulta."""
    out = []
    for q, label in (("raw", "Raw description"), ("core", "Core need, rewritten"), ("llm5", "Core need + 4 rewrites")):
        m = re.search(rf"^\| real \| emb \| minilm \| {q} \| (\d+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|$", text, re.M)
        if m:
            n, a, b, c = m.groups()
            out.append({"query": q, "label": label, "n": int(n), "top_50": float(a), "top_200": float(b), "top_1000": float(c)})
    return out


def holdout_counts(text: str) -> dict[str, int]:
    """Ideas "no" del holdout según la revisión humana: hueco real, parcial, equivalente."""
    main = text.split("## Opcionales")[0]

    def get(pat: str) -> int:
        m = re.search(pat, main)
        return int(m.group(1)) if m else 0
    return {"real_gap": get(r"Hueco en T\*\*[^:]*: (\d+)/"), "partial": get(r"Alguno parcial: (\d+)/"),
            "equivalent": get(r"Equivalente real anterior a T\*\*[^:]*: (\d+)/")}


def gap_entry(r: dict, meta: dict, ver: dict) -> dict:
    a, d = r["ask"], r["v2"]
    cands = []
    for i in r["scored"][:3]:
        t, u, c = meta.get(i, ("?", "", ""))
        cands.append({"title": t, "url": u, "date": (c or "")[:10], "score": round(ver[(r["id"], i)].core, 2)})
    return {"id": r["id"], "tier": TIER_IDS[r["tier"]], "request": d["pedido_resumido"], "ask_title": a["title"],
            "hn_url": a["hn_url"], "date": a["created_at"][:10], "points": a["points"], "comments": a["num_comments"],
            "commenters_say": SAYS[d["etiqueta"]], "best_score": round(r["best"], 2), "candidates": cands}


def export(conn, out: Path = OUT) -> dict:
    from gapfinder.verify import load_done

    ver = load_done(gaps.VERDICTS)
    rows = gaps.tiered_rows(ver)
    shown = sorted((r for r in rows if r["tier"] in ("fuerte", "gris")), key=lambda r: r["best"])
    ids = sorted({i for r in shown for i in r["scored"][:3]})
    meta = {i: (t, u, c) for i, t, u, c in conn.execute(
        f"SELECT id, title, url, created_at FROM items WHERE id IN ({','.join('?' * len(ids))})", ids)} if ids else {}
    corpus = dict(conn.execute("SELECT source, COUNT(*) FROM items GROUP BY source").fetchall())
    funnel = json.loads(askhn.ASKS.read_text())["funnel"]
    holdout = holdout_counts(HOLDOUT_REPORT.read_text())
    metrics = [{**m, "k": holdout["real_gap"], "n": sum(holdout.values())} if m["stage"] == "Holdout" else m for m in METRICS]
    data = {
        "pipeline": {"show_hn": corpus.get("show_hn", 0), "github": corpus.get("github", 0),
                     "asks_found": funnel["bajados_unicos"], "asks_kept": funnel["filtrados"], "requests": len(rows),
                     "pairs": len(ver), "judge_cost_usd": round(sum(v.cost_usd or 0 for v in ver.values()), 2),
                     "threshold_built": gaps.HUECO, "threshold_strong": gaps.FUERTE},
        "tiers": {TIER_IDS[t]: sum(r["tier"] == t for r in rows) for t in TIER_IDS},
        "metrics": metrics,
        "recall": recall_rows(RECALL_REPORT.read_text()),
        "holdout": holdout,
        "gaps": [gap_entry(r, meta, ver) for r in shown],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return data
