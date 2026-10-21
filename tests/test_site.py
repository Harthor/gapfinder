from gapfinder import site
from gapfinder.verify import Verdict


def test_recall_rows_reads_real_minilm_rows_only():
    text = "\n".join([
        "| real | emb | minilm | raw | 12 | 0.08 | 0.33 | 0.67 |",
        "| real | emb | bge | raw | 12 | 0.33 | 0.42 | 0.58 |",
        "| real sin label_note | emb | minilm | llm5 | 9 | 0.67 | 0.78 | 0.89 |",
        "| real | emb | minilm | llm5 | 12 | 0.50 | 0.58 | 0.92 |",
    ])
    rows = site.recall_rows(text)
    assert [r["query"] for r in rows] == ["raw", "llm5"]   # "core" no está: se omite
    assert rows[1] == {"query": "llm5", "label": "Core need + 4 rewrites", "n": 12, "top_50": 0.5, "top_200": 0.58,
                       "top_1000": 0.92}


def test_holdout_counts_reads_main_block_not_optionals():
    text = ("## Ideas con decisión \"no\" del sistema (20)\n"
            "- **Hueco en T** (ningún candidato es equivalente): 6/20 = 30% (IC 95%: 15%–52%)\n"
            "- **Equivalente real anterior a T** (1/2/3): 4/20 = 20% (IC 95%: 8%–42%)\n"
            "- Alguno parcial: 10/20 = 50% (IC 95%: 30%–70%)\n"
            "## Opcionales: ideas \"ya construido\" / \"revisar\" (15)\n"
            "- **Hueco en T** (ningún candidato es equivalente): 1/3 = 33%\n")
    assert site.holdout_counts(text) == {"real_gap": 6, "partial": 10, "equivalent": 4}


def test_gap_entry_keeps_top_three_candidates_with_scores():
    r = {"id": "gap-1", "tier": "fuerte", "best": 0.41, "scored": ["a", "b", "c", "d"],
         "v2": {"pedido_resumido": "A tool for X.", "etiqueta": "n"},
         "ask": {"title": "Ask HN: X?", "hn_url": "https://news.ycombinator.com/item?id=1", "created_at": "2020-05-01T00:00:00Z",
                 "points": 9, "num_comments": 3}}
    ver = {("gap-1", i): Verdict("gap-1", i, s, 0.0, 0.0) for i, s in zip("abcd", (0.41, 0.3, 0.2, 0.1))}
    meta = {"a": ("Alpha", "https://a", "2019-01-02T00:00:00"), "b": ("Beta", "https://b", None)}
    e = site.gap_entry(r, meta, ver)
    assert e["tier"] == "strong_gap" and e["commenters_say"] == "does not exist" and e["date"] == "2020-05-01"
    assert [c["title"] for c in e["candidates"]] == ["Alpha", "Beta", "?"]
    assert e["candidates"][0] == {"title": "Alpha", "url": "https://a", "date": "2019-01-02", "score": 0.41}
    assert e["candidates"][1]["date"] == ""
