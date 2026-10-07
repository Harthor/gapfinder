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
