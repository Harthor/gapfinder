import json

from gapfinder import gaps


def test_valid_v2_rejects_degenerate_outputs():
    good = {"pedido_resumido": "A web app to rate individual dishes on restaurant menus.",
            "justificacion": "Pide una app concreta; nadie conoce una."}
    assert gaps.valid_v2(good)
    assert not gaps.valid_v2({**good, "pedido_resumido": "...."})
    assert not gaps.valid_v2({**good, "pedido_resumido": "A web app to rate\ndishes on menus today."})
    assert not gaps.valid_v2({**good, "justificacion": "…"})


def test_load_v2_last_line_per_id_wins(tmp_path):
    path = tmp_path / "v2.jsonl"
    path.write_text("\n".join(json.dumps(d) for d in (
        {"id": "1", "ok": False, "error": "x"}, {"id": "1", "ok": True, "etiqueta": "e"}, {"id": "2", "ok": True})))
    got = gaps.load_v2(path)
    assert got["1"]["ok"] and got["1"]["etiqueta"] == "e" and set(got) == {"1", "2"}


def test_system_prompt_has_label_definitions_and_examples():
    s = gaps.system_with_examples()
    for lab in ('"e" (existe)', '"p" (parcial)', '"n" (no existe)', '"?" (incierto)'):
        assert lab in s
    assert s.count("### Example") == 4 and '"pedido_real": false' in s and '"pedido_real": true' in s


def test_wilson_bounds():
    from gapfinder.review import wilson
    assert wilson(0, 0) == (0.0, 0.0)
    lo, hi = wilson(0, 10)
    assert lo == 0.0 and 0.25 < hi < 0.35


def test_no_software_by_head_noun_and_title():
    ns = gaps.no_software
    assert ns("Ask HN: Is there a good hackable smart watch?", "A hackable smartwatch with GPS and audio recording.") == "hardware"
    assert ns("Ask HN: Is there a way to get notified when my cat has seizures?",
              "A collar-mounted sensor system (accelerometer/gyroscope) that detects feline seizures.") == "hardware"
    assert ns("Is there any eReader with a terminal?", "An e‑ink ebook reader that runs a Linux‑based OS.") == "hardware"
    assert ns("Ask HN: Is there a great book for understanding LLMs?", "A book that explains LLMs for developers.") == "contenido"
    assert ns("Ask HN: Is There an F-Droid for iOS?", "A curated list of open‑source iOS apps.") == "contenido"
    assert ns("Ask HN: Is there a MIT-like FOSS license?", "A FOSS license that prohibits LLM training.") == "contenido"
    assert ns("Ask HN: What tools do you use to diagram micro-service architectures?", "A tool to create diagrams.") == "encuesta"
    assert ns("Ask HN: What tool would you buy to make your life easier?", "A service that aggregates accounts.") == "encuesta"
    assert ns("Ask HN: How do you back up your Android phone?", "Offline backup solution for Android app data.") == "encuesta"
    assert ns("Ask HN: Any way to program Siri Shortcuts in iOS 12?", "A tool to generate Siri Shortcuts.") == "se puede"
    assert ns("Ask HN: Is there a good alternative to registration keys?", "A method for distributing activation codes.") == "se puede"


def test_no_software_keeps_software_that_mentions_hardware_or_content_words():
    ns = gaps.no_software
    assert ns("Ask HN: What app do you use for book recommendations?", "An app that recommends books.") == "encuesta"
    assert ns("Ask HN: Is there an app for book recommendations?", "An app that recommends books.") is None
    assert ns("Ask HN: Is there a service that escalates emails to SMS?",
              "A service that automatically sends SMS or phone call reminders.") is None
    assert ns("Ask HN: Is there a temp phone number like temp email?", "A temporary phone number service.") is None
    assert ns("Ask HN: Is there an app for reading newsletters?", "A newsletter reader service with a unique email.") is None
    assert ns("Ask HN: Is there a better VoIP provider than Skype?",
              "A consumer VoIP service (SIP or similar) accessible via tablet, phone and desktop apps.") is None
    assert ns("Ask HN: Any tool to look C++ template substitution?", "A tool that displays C++ template instantiation.") is None
    assert ns("Ask HN: Is there a better way to document software architectures?", "A documentation tool for architects.") is None
    assert ns("Ask HN: How to report bugs?", "A platform for disclosing vulnerabilities, with guidance for reporting.") is None


def test_tier_precedence_and_boundaries():
    t = gaps.tier
    assert t(0.85, "n") == "match" and t(0.90, "e", "encuesta") == "match"   # un match no es hueco, sea lo que sea
    assert t(0.30, "n", "hardware") == "no_software"
    assert t(0.30, "e") == "descartado" and t(0.84, "e") == "descartado"
    assert t(0.59, "n") == "fuerte" and t(0.59, "p") == "fuerte"
    assert t(0.60, "n") == "gris" and t(0.84, "p") == "gris"
    assert t(0.30, "?") == "gris"   # sin etiqueta clara no es hueco fuerte


def test_gap_metrics_precision_excludes_unsure():
    from gapfinder import review
    m = review.gap_metrics(["n", "n", "1", "x", "p", "s", "?"])
    assert m["respondidas"] == 7 and m["juzgadas"] == 6 and m["no_se"] == 1
    assert (m["hueco"], m["equivalente"], m["fuera"], m["parcial"], m["no_software"]) == (2, 1, 1, 1, 1)
    assert m["precision"] == 2 / 6 and m["ic"] == review.wilson(2, 6)
    assert review.gap_metrics([])["precision"] is None and review.gap_metrics(["?"])["juzgadas"] == 0


def _gap_row(cid, tier, best, items):
    return {"id": cid, "ask_id": cid.split("-")[1], "tier": tier, "best": best, "scored": items,
            "v2": {"pedido_resumido": f"A tool for {cid}.", "etiqueta": "n", "justificacion": "nadie conoce una"},
            "ask": {"title": f"Ask HN: {cid}?", "hn_url": f"https://news.ycombinator.com/item?id={cid}",
                    "created_at": "2020-01-01", "points": 9, "num_comments": 3}}


def test_interactive_gaps_saves_each_answer_and_writes_precision(tmp_path, monkeypatch):
    import sqlite3

    from gapfinder import review, text
    from gapfinder.text import ItemText
    from gapfinder.verify import Verdict

    strong = [_gap_row("gap-1", "fuerte", 0.3, ["a", "b", "c"]), _gap_row("gap-2", "fuerte", 0.5, ["a", "b"])]
    grey = [_gap_row("gap-3", "gris", 0.7, ["b", "c"])]
    monkeypatch.setattr(review, "gap_queue", lambda: (strong, grey))
    monkeypatch.setattr(review, "GAPS_REVIEW_PATH", tmp_path / "gap_human.jsonl")
    monkeypatch.setattr(review, "GAPS_RESULT_PATH", tmp_path / "gap_result.md")
    ver = {(r["id"], i): Verdict(r["id"], i, 0.5, 0.5, 0.5) for r in strong + grey for i in r["scored"]}
    monkeypatch.setattr(review, "load_done", lambda name: ver)
    monkeypatch.setattr(text, "get_texts", lambda conn, ids: {i: ItemText(i, "github", f"item {i}", "body", "native") for i in ids})
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id TEXT, url TEXT, created_at TEXT)")
    conn.executemany("INSERT INTO items VALUES (?, ?, ?)", [(i, f"https://x/{i}", "2019-01-01") for i in "abc"])

    # gap-1: tecla inválida (se ignora) y n; gap-2: "3" se ignora (tiene 2 candidatos) y x con nota;
    # después "c" para entrar a la zona gris y "2" en gap-3.
    keys = iter(["z", "n", "3", "x", "c", "2"])
    notes = iter(["ExistingTool https://example.com"])
    out = []
    res = review.interactive_gaps(conn, getkey=lambda: next(keys), out=lambda *a, **k: out.append(a),
                                  ask_text=lambda prompt: next(notes))
    assert res == {"respondidas_ahora": 3, "fuertes": "2/2", "gris": "1/1"}
    got = review.load_gap_answers()
    assert got["gap-1"]["label"] == "n" and got["gap-1"]["tier"] == "fuerte"
    assert got["gap-2"]["label"] == "x" and got["gap-2"]["note"] == "ExistingTool https://example.com"
    assert got["gap-3"]["label"] == "2" and got["gap-3"]["item_id"] == "c"
    result = (tmp_path / "gap_result.md").read_text()
    assert "**Precisión (hueco real)**: 1/2 = 50%" in result   # fuertes: 1 hueco de 2 juzgados
    assert "**Precisión (hueco real)**: 0/1 = 0%" in result    # zona gris

    # se retoma donde quedó: nada pendiente, no pide teclas
    res = review.interactive_gaps(conn, getkey=lambda: (_ for _ in ()).throw(AssertionError("pidió tecla")),
                                  out=lambda *a, **k: None, ask_text=lambda p: "")
    assert res["respondidas_ahora"] == 0
