import json

from gapfinder import askhn, review


def _setup(tmp_path, monkeypatch, asks, ext):
    monkeypatch.setattr(askhn, "ASKS", tmp_path / "asks.json")
    monkeypatch.setattr(askhn, "EXTRACTIONS", tmp_path / "ext.json")
    monkeypatch.setattr(askhn, "SELECTED", tmp_path / "sel.json")
    (tmp_path / "asks.json").write_text(json.dumps({"asks": asks}))
    (tmp_path / "ext.json").write_text(json.dumps(ext))


def _ask(i, points, date="2020-01-01T00:00:00Z"):
    return {"id": str(i), "title": f"Ask HN: is there a tool {i}", "text": "", "created_at": date, "points": points,
            "num_comments": 5, "hn_url": f"https://news.ycombinator.com/item?id={i}"}


def _ext(label, tools=(), request=True):
    return {"es_pedido_de_herramienta": request, "idea": "a tool", "etiqueta_comentarios": label,
            "herramientas_sugeridas": list(tools), "senales_no_existe": []}


def test_request_filters():
    assert askhn.REQUEST_RE.search("Ask HN: Is there a tool that diffs PDFs?")
    assert askhn.REQUEST_RE.search("Ask HN: Does anything like this exist?")
    assert not askhn.REQUEST_RE.search("Ask HN: Why is everyone leaving?")
    assert askhn.STORE_RE.search("https://itunes.apple.com/us/app/forest")
    assert not askhn.STORE_RE.search("https://heyfocus.com")


def test_group_requires_pre_ask_corpus_item():
    ask = _ask(1, 10, "2020-01-01T00:00:00Z")
    before = {"nombre": "x", "url": "", "relacion": "equivalente", "corpus_ids": ["github:a/x"],
              "corpus_created": {"github:a/x": "2019-05-01T00:00:00Z"}}
    after = {**before, "corpus_created": {"github:a/x": "2021-05-01T00:00:00Z"}}
    partial = {**before, "relacion": "parcial"}
    assert askhn.group_of(_ext("existe", [before]), ask) == "existe_con_item_en_corpus"
    assert askhn.group_of(_ext("existe", [after]), ask) == "existe_sin_item_en_corpus"
    assert askhn.group_of(_ext("existe", [partial]), ask) == "existe_sin_item_en_corpus"
    assert askhn.group_of(_ext("no_existe"), ask) == "no_existe"


def test_select_balances_and_interleaves(tmp_path, monkeypatch):
    asks = [_ask(i, 100 - i) for i in range(30)]
    ext = {str(i): _ext("parcial") for i in range(20)}
    ext |= {str(i): _ext("no_existe") for i in range(20, 23)}
    ext |= {"23": _ext("no_existe", request=False)}
    _setup(tmp_path, monkeypatch, asks, ext)
    monkeypatch.setattr(askhn, "MAX_IDEAS", 12)
    order = askhn.select()
    assert order[:3] == ["20", "21", "22"]          # no_existe primero; el que no es pedido queda fuera
    assert "23" not in order and len(order) == 12   # parcial llena el sobrante hasta MAX_IDEAS
    assert order[3:] == [str(i) for i in range(9)]  # por puntos


def test_review_menu_pending_and_extract_queue(tmp_path, monkeypatch):
    asks = [_ask(1, 10), _ask(2, 20)]
    _setup(tmp_path, monkeypatch, asks, {})
    monkeypatch.setattr(review, "EXTRACT_REVIEW_PATH", tmp_path / "human.jsonl")
    assert review.extract_queue() is None   # sin extracción: pendiente, no falla
    (tmp_path / "ext.json").write_text(json.dumps({"1": _ext("no_existe", request=False), "2": _ext("existe")}))
    assert review.extract_queue() == ["2", "1"]   # pedidos primero
    keys = iter(["s", "e", "n", "q"])
    out = []
    res = review.interactive_extract(getkey=lambda: next(keys), out=lambda *a, **k: out.append(a))
    assert res["total"] == 2
    got = review.load_extract_human()
    assert got["2"]["is_request"] == "s" and got["2"]["label"] == "e"
    assert got["1"]["is_request"] == "n" and got["1"]["label"] is None


def test_holdout_pairs_conversion_and_wilson(tmp_path, monkeypatch):
    from gapfinder import pilot

    path = tmp_path / "pairs.jsonl"
    monkeypatch.setattr(pilot, "HOLDOUT_REVIEW_PATH", path)
    rows = [{"case_id": c, "top": [("a", .8), ("b", .7), ("c", .6)]} for c in ("h1", "h2", "h3", "h4")]
    lines = [("h1", "b", "s"), ("h2", "a", "p"), ("h2", "b", "n"), ("h2", "c", "n"),
             ("h3", "a", "n"), ("h3", "b", "n"), ("h3", "c", "n"), ("h4", "a", "n")]
    path.write_text("\n".join(json.dumps({"case_id": c, "item_id": i, "label": lab}) for c, i, lab in lines))
    assert review._from_pairs(rows) == {"h1": "2", "h2": "p", "h3": "n"}   # h4 incompleta: no se convierte
    lo, hi = review.wilson(5, 10)
    assert round(lo, 3) == 0.237 and round(hi, 3) == 0.763
