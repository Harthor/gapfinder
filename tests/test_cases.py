import json

from gapfinder import cases

SHEET = """# Hoja

Escribí en `necesidad:` la necesidad de cada item.

## 1 · show_hn:111 · 2012-05-01 · 3 pts · época 2009-14 · texto: native

- URL: https://example.com/a
- Título: A
- Texto: blah

necesidad: una forma de compartir listas
de compras en familia

---

## 2 [humano] · show_hn:222 · 2021-01-01 · 50 pts · época 2020-26 · texto: author_comment

- URL: https://example.com/b
- Título: B
- Texto: blah

necesidad: 

---
"""


def test_parse_worksheet_multiline_and_empty():
    parsed, empty = cases.parse_worksheet(SHEET)
    assert empty == ["show_hn:222"]
    assert parsed == [{
        "id": "syn-111", "kind": "synthetic", "author": "claude", "title": "una forma de compartir listas de compras en familia",
        "description": "", "expected_urls": ["https://example.com/a"], "expected_item_ids": ["show_hn:111"],
        "meta": {"date": "2012-05-01", "points": 3, "era": "2009-14", "text_origin": "native", "worksheet": ""},
    }]


def test_parse_marks_human_author():
    sheet = SHEET.replace("necesidad: \n\n---\n", "necesidad: need two\n\n---\n")
    parsed, _ = cases.parse_worksheet(sheet)
    assert [(c["id"], c["author"]) for c in parsed] == [("syn-111", "claude"), ("syn-222", "human")]


def test_parse_human_item_with_claude_pair():
    sheet = SHEET.replace("necesidad: \n\n---\n", "necesidad: need two\nsecond line\nnecesidad claude: claude version\n\n---\n")
    parsed, empty = cases.parse_worksheet(sheet)
    assert empty == []
    human, claude = parsed[1], parsed[2]
    assert (human["id"], human["author"], human["title"], human["pair_id"]) == ("syn-222", "human", "need two second line", "pair-222")
    assert (claude["id"], claude["author"], claude["title"], claude["pair_id"]) == ("syn-222-claude", "claude", "claude version", "pair-222")
    assert claude["expected_item_ids"] == human["expected_item_ids"] == ["show_hn:222"]
    assert "pair_id" not in parsed[0]
    # sin necesidad humana no hay par (ni caso de Claude suelto)
    sheet = SHEET.replace("necesidad: \n\n---\n", "necesidad: \nnecesidad claude: claude version\n\n---\n")
    assert [c["id"] for c in cases.parse_worksheet(sheet)[0]] == ["syn-111"]


def test_import_replaces_only_cases_from_same_sheet(tmp_path):
    sheet, out = tmp_path / "synthetic_worksheet.md", tmp_path / "k.json"
    sheet.write_text(SHEET)
    out.write_text(json.dumps([
        {"id": "r1", "kind": "real", "title": "x", "expected_urls": ["u"]},
        {"id": "syn-9", "kind": "synthetic", "title": "otra hoja", "meta": {"worksheet": "synthetic_worksheet_2.md"}},
        {"id": "syn-222", "kind": "synthetic", "title": "vieja", "meta": {"worksheet": "synthetic_worksheet.md"}},
    ]))
    assert cases.import_worksheet(sheet, out)[0] == 1
    assert cases.import_worksheet(sheet, out)[0] == 1  # idempotente
    got = json.loads(out.read_text())
    assert [c["id"] for c in got] == ["r1", "syn-9", "syn-111"]
    assert got[-1]["meta"]["worksheet"] == "synthetic_worksheet.md"


def test_import_marks_leakage_flag(tmp_path):
    sheet, out = tmp_path / "synthetic_worksheet.md", tmp_path / "k.json"
    sheet.write_text(SHEET)
    cases.import_worksheet(sheet, out, flagged={"syn-111"})
    assert json.loads(out.read_text())[0]["leakage_flag"] is True
    cases.import_worksheet(sheet, out)
    assert "leakage_flag" not in json.loads(out.read_text())[0]


def test_import_rejects_id_owned_by_other_sheet(tmp_path):
    import pytest

    sheet, out = tmp_path / "synthetic_worksheet.md", tmp_path / "k.json"
    sheet.write_text(SHEET)
    out.write_text(json.dumps([{"id": "syn-111", "kind": "synthetic", "meta": {"worksheet": "otra.md"}}]))
    with pytest.raises(ValueError, match="syn-111"):
        cases.import_worksheet(sheet, out)


def test_cells_split_evenly():
    assert sorted(cases._cells(40).values()) == [6, 6, 7, 7, 7, 7]
