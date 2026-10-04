import json

from gapfinder import db
from gapfinder.ingest import github, hn


def test_parse_hn_hit_link_post():
    item = hn.parse_hit({
        "objectID": "123",
        "title": "Show HN: CatQueue – A zero-dependency job queue",
        "url": "https://github.com/x/catqueue",
        "created_at_i": 1790112214,
        "points": 42,
        "num_comments": 7,
        "author": "alice",
    })
    assert item is not None
    assert item.id == "show_hn:123"
    assert item.title == "CatQueue – A zero-dependency job queue"
    assert item.url == "https://github.com/x/catqueue"
    assert item.created_at == "2026-09-22T21:23:34Z"
    assert item.hn_points == 42
    assert json.loads(item.extra)["hn_url"] == "https://news.ycombinator.com/item?id=123"


def test_parse_hn_hit_text_post_uses_hn_url_and_cleans_html():
    item = hn.parse_hit({
        "objectID": "9",
        "title": "Show HN - My tool",
        "url": None,
        "story_text": "Hi HN,<p>It does <i>X</i> &amp; Y.",
        "created_at_i": 0,
    })
    assert item.url == "https://news.ycombinator.com/item?id=9"
    assert item.title == "My tool"
    assert item.description == "Hi HN,\nIt does X & Y."


def test_parse_hn_hit_without_title_is_skipped():
    assert hn.parse_hit({"objectID": "1", "title": None, "created_at_i": 1}) is None


def test_parse_github_repo():
    item = github.parse_repo({
        "full_name": "maybe-finance/maybe",
        "name": "maybe",
        "html_url": "https://github.com/maybe-finance/maybe",
        "description": "The personal finance app for everyone",
        "topics": ["finance", "ruby"],
        "created_at": "2024-01-01T22:23:46Z",
        "pushed_at": "2025-07-24T22:20:44Z",
        "stargazers_count": 54271,
        "archived": True,
        "language": "Ruby",
    })
    assert item.id == "github:maybe-finance/maybe"
    assert item.description == "The personal finance app for everyone\nTopics: finance, ruby"
    assert item.last_activity_at == "2025-07-24T22:20:44Z"
    assert item.archived is True
    assert item.stars == 54271


def test_clean_readme_strips_badges_code_and_links():
    raw = "# Title\n=====\n[![ci](b.svg)](ci)\n<!-- x -->\nSee [docs](http://d).\n```\ncode\n```\n- item"
    out = github.clean_readme(raw)
    assert "svg" not in out and "code" not in out and "http" not in out and "===" not in out
    assert "See docs." in out and "Title" in out


def test_clean_readme_rst():
    raw = """.. image:: https://readthedocs.org/badge/?version=latest
   :target: https://docs.example.io/
   :alt: Documentation Status
.. |demo| image:: https://s3/thumb.png
   :target: https://s3/video.mp4

SQL Explorer
============

`Official Website <https://www.sqlexplorer.io/>`_ and `docs`_.

|demo|

.. _docs: https://docs.example.io/

Run ``docker compose up`` to start::

    make run
"""
    out = github.clean_readme(raw)
    for noise in (".. image", ":target:", ":alt:", "|demo|", "`_", "``", "https://", "===="):
        assert noise not in out, noise
    assert "SQL Explorer" in out and "Official Website and docs." in out and "Run docker compose up to start:" in out
    # el resto que dejó la limpieza vieja (sin el <url>) también se limpia al re-limpiar
    assert github.clean_readme(".. image:: http://x.svg\n:target: http://y\nSQL Explorer\n`Official Website `_") == \
        "SQL Explorer\nOfficial Website"
    assert github.is_rst_noisy(".. image:: x\nfoo") and not github.is_rst_noisy(out)
    assert github.clean_readme("from the `Allen Human Brain\nAtlas <https://x>`_, a dataset") == \
        "from the Allen Human Brain Atlas, a dataset"
    assert github.clean_readme("Finds documents using `_.where`, updates") == "Finds documents using `_.where`, updates"
    assert github.clean_readme("Intro\n..\n   hidden comment\n   more\nVisible at `<https://x>`_.") == "Intro\nVisible at ."


def test_clean_readme_keeps_markdown_tables_and_code_spans():
    out = github.clean_readme("| Name | Value |\n|------|-------|\n| a | `b` |")
    assert "| Name | Value |" in out and "`b`" in out


def test_upsert_is_idempotent_and_updates_signals(tmp_path):
    conn = db.connect(tmp_path / "t.db")
    base = dict(id="github:a/b", source="github", url="u", title="b", description="", created_at="2024-01-01T00:00:00Z")
    assert db.upsert_items(conn, [db.Item(**base, stars=1)]) == 1
    assert db.upsert_items(conn, [db.Item(**base, stars=5)]) == 0
    assert conn.execute("SELECT stars FROM items").fetchone()[0] == 5


def test_github_repo_from_url():
    from gapfinder.ingest.github import github_repo_from_url as f

    assert f("https://github.com/Owner/Repo") == "Owner/Repo"
    assert f("https://github.com/owner/repo.git") == "owner/repo"
    assert f("http://www.github.com/o/r/tree/main/src?x=1") == "o/r"
    assert f("https://github.com/owner") is None
    assert f("https://github.com/features/actions") is None
    assert f("https://gist.github.com/o/abc") is None
    assert f("https://owner.github.io/repo") is None


def test_extract_meta_description_prefers_og_and_falls_back_to_title():
    from gapfinder.ingest.enrich import extract_meta_description as f

    page = '<html><head><title>T</title><meta name="description" content="plain">' \
           '<meta property="og:description" content="Rich &amp; nice"></head><body>x</body></html>'
    assert f(page) == "Rich & nice"
    assert f("<html><head><title> Only  title </title></head>") == "Only title"
    assert f("<html><head><meta name='description' content='x'") == ""  # roto: sin crash


def test_is_junk_detects_parked_and_error_pages():
    from gapfinder.ingest.enrich import is_junk

    assert is_junk("JAYATOP77: Platform JAYATOP 77 APK Situs Slot Online Akses HP")
    assert is_junk("2 sites already link to corporate.watch. Listed at $100 — keep the equity.")
    assert is_junk("This domain may be for sale!")
    assert is_junk("Just a moment...")
    assert is_junk("anything", final_url="https://www.sedo.com/search?domain=x")
    assert not is_junk("Coffitivity recreates the ambient sounds of a cafe to boost your creativity")
    assert not is_junk("A visual version of SQL for analysts")


def test_wayback_window_is_minus_30d_plus_6m():
    from datetime import datetime, timezone

    from gapfinder.ingest.enrich import wayback_window

    lo, hi = wayback_window(datetime(2016, 6, 6, 12, 0, tzinfo=timezone.utc))
    assert lo == "20160507120000"
    assert hi == "20161205120000"




def test_author_comment_and_reply_rules():
    from gapfinder.ingest import hn_comments as hc

    long = "x" * 120
    tree = {"children": [
        {"author": "bob", "text": "short top-level", "created_at_i": 1, "children": [
            {"author": "bob", "text": "reply one " + long, "created_at_i": 3, "children": []},
        ]},
        {"author": "alice", "text": "q", "created_at_i": 2, "children": [
            {"author": "bob", "text": "reply two " + long, "created_at_i": 4, "children": [
                {"author": "bob", "text": "reply three " + long, "created_at_i": 5, "children": []},
                {"author": "bob", "text": "reply four " + long, "created_at_i": 6, "children": []},
            ]},
        ]},
    ]}
    cs = hc.collect_author_comments(tree, "bob")
    assert [c["depth"] for c in cs] == [1, 2, 2, 3, 3]
    assert hc.author_comment(cs) == ""  # el top-level no llega a 100 chars
    reply = hc.author_reply(cs)
    assert reply.startswith("reply one") and "reply three" in reply and "reply four" not in reply

    cs2 = hc.collect_author_comments({"children": [{"author": "bob", "text": "Hi HN &amp; " + long}]}, "bob")
    assert hc.author_comment(cs2).startswith("Hi HN & ")
