import numpy as np

from gapfinder import eval as ev
from gapfinder.leakage import Idf


def test_ranks_and_ablation_override():
    scores = np.array([0.9, 0.5, 0.7, 0.1])
    assert ev.ranks(scores, [0, 2, 3]) == [1, 2, 4]
    # item 2 forzado a un score de 0.2: lo superan 0.9 y 0.5 (su propio 0.7 original no cuenta)
    assert ev.ranks(scores, [2], {2: 0.2}) == [3]
    # forzado hacia arriba: nadie lo supera
    assert ev.ranks(scores, [3], {3: 0.95}) == [1]


def test_reformulations_synthetic_and_real():
    idf = Idf(1000, {"aggreg": 30, "news": 200})
    syn = ev.reformulations({"title": "I want a news aggregator for tech stories", "description": ""}, idf)
    assert syn["need"] == "I want a news aggregator for tech stories"
    assert syn["plain"] == "A news aggregator for tech stories" and syn["show_hn"].startswith("Show HN: A news")
    real = ev.reformulations({"title": "Everyone Builds Agents", "description": "Agent observability layer."}, idf)
    assert real["need"] == "Everyone Builds Agents. Agent observability layer." and real["plain"] == "Agent observability layer."


def test_expected_resolves_targeted_urls_and_drops_heuristics():
    index = ev.Index(["github:a/b", "github:c/d", "show_hn:1"], [np.zeros((3, 2), np.float32)])
    case = {"expected_item_ids": ["github:a/b", "show_hn:1"], "expected_urls": ["https://github.com/C/D"],
            "meta": {"heuristic_item_ids": ["show_hn:1"]}}
    assert ev._expected(case, index, {}, True) == ["github:a/b", "show_hn:1"]
    assert ev._expected(case, index, {"github:c/d": "github:c/d"}, False) == ["github:a/b", "github:c/d"]


def test_rrf_and_first_rank():
    from gapfinder import eval2
    fused = eval2.rrf([["a", "b", "c"], ["b", "c", "d"]])
    assert fused[0] == "b" and set(fused) == {"a", "b", "c", "d"}
    assert eval2.first_rank(fused, {"c", "d"}) == fused.index("c") + 1
    assert eval2.first_rank(fused, {"z"}) == eval2.MISS


def test_phase3_twins_links_show_hn_and_repo(tmp_path):
    from gapfinder import db, phase3

    conn = db.connect(tmp_path / "t.db")
    mk = lambda i, u: db.Item(id=i, source=i.split(":")[0], url=u, title=i, description="", created_at="2020-01-01T00:00:00Z")
    db.upsert_items(conn, [mk("github:Acme/tool", "https://github.com/Acme/tool"),
                           mk("show_hn:1", "https://github.com/acme/tool"),          # linkea al repo esperado
                           mk("show_hn:2", "https://github.com/acme/tool-extra"),    # otro repo: no es gemelo
                           mk("show_hn:3", "https://acme.dev"),
                           mk("github:Other/x", "https://github.com/Other/x")])
    conn.execute("INSERT INTO enrichment (item_id, github_repo, method) VALUES ('show_hn:3', 'Other/x', 'github_corpus')")
    assert phase3.twins(conn, ["github:Acme/tool"]) == {"github:Acme/tool", "show_hn:1"}
    assert phase3.twins(conn, ["show_hn:3"]) == {"show_hn:3", "github:Other/x"}
    assert phase3.twins(conn, ["show_hn:1"]) == {"show_hn:1", "github:Acme/tool"}


def test_jev_questions_build_with_official_sdk():
    from typesafe_sdk import Noul

    from gapfinder.verify import QUESTIONS, JevVerifier
    q = JevVerifier.questions()
    assert set(q) == set(QUESTIONS) and all(isinstance(v, Noul) for v in q.values())
    assert q["core"].criteria["true"].startswith("The candidate provides")


def test_openrouter_response_keeps_cost_and_answers():
    from gapfinder.verify import openrouter_response_model
    r = openrouter_response_model().model_validate({
        "id": "gen-dec-1", "model": "typesafe/jev-1.13-20260917", "provider": "TypeSafe",
        "answers": {"core": {"type": "noul", "noul": 0.9}},
        "usage": {"input_tokens": 476, "output_tokens": 70, "cost": 0.000019992}})
    assert r.usage.cost == 0.000019992 and r.answers["core"].noul == 0.9 and r.provider == "TypeSafe"


def test_openrouter_verifier_requires_key(monkeypatch):
    import pytest

    from gapfinder.verify import OpenRouterJevVerifier
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    v = OpenRouterJevVerifier()
    assert v.model == "typesafe/jev-1.13" and v.name == "jev_openrouter"
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        v.client_kwargs()
    monkeypatch.setenv("OPENROUTER_API_KEY", "x")
    assert v.client_kwargs()["base_url"] == "https://openrouter.ai/api"


def test_jev_stops_on_account_error(tmp_path, monkeypatch):
    import httpx2
    import pytest
    import typesafe_sdk

    from gapfinder import verify

    monkeypatch.setattr(verify, "OUT_DIR", tmp_path)
    calls = []

    class FakeClient:
        def __init__(self, **kw): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def system_one(self, *a, **kw):
            calls.append(1)
            raise typesafe_sdk.TypeSafeAPIError(402, {"error": "Insufficient credits"}, httpx2.Headers())

    monkeypatch.setattr(typesafe_sdk, "AsyncTypeSafeClient", FakeClient)
    pairs = [verify.Pair("c", "idea", f"i{n}", "t", "x") for n in range(2000)]
    with pytest.raises(RuntimeError, match="error de cuenta"):
        verify.JevVerifier(concurrency=1, name="t").verify(pairs)
    assert len(calls) < 10   # no sigue disparando requests después del primer 402


def test_pilot_review_order_and_agreement(tmp_path):
    from gapfinder import pilot
    from gapfinder.verify import Pair, Verdict

    pairs = [Pair("c", "i", f"x{n}", "t", "") for n in range(5)]
    cores = [0.2, 0.9, 0.45, 0.6, 0.05]
    jev = {(p.case_id, p.item_id): Verdict(p.case_id, p.item_id, c, c, 0.5) for p, c in zip(pairs, cores)}
    assert [p.item_id for p in pilot.review_order(pairs, jev)] == ["x1", "x3", "x2", "x0", "x4"]
    human = {("c", "x1"): "s", ("c", "x3"): "n", ("c", "x2"): "p", ("c", "x0"): "?"}
    a = pilot.agreement_vs_human(human, jev, {})
    assert a["jev"]["n"] == 3 and a["jev"]["nucleo"] == 2 / 3   # x3: Jev 0.6 dice núcleo, humano dice no
    assert a["haiku"] == {"n": 0}
    path = tmp_path / "h.jsonl"
    path.write_text('{"case_id": "c", "item_id": "x1", "label": "n"}\n{"case_id": "c", "item_id": "x1", "label": "s"}\n')
    assert pilot.load_human(path) == {("c", "x1"): "s"}   # la última respuesta pisa la anterior


def test_holdout_decide_leakage_terms_and_relaunch_filter():
    from gapfinder import holdout

    assert [holdout.decide(x) for x in (0.95, 0.90, 0.87, 0.85, 0.5)] == \
        ["ya construido", "ya construido", "revisar", "revisar", "no"]
    terms = holdout.leakage_terms(None, {"title": "Petrichor – a free, open-source, offline music player",
                                         "url": "https://github.com/kushalpandya/Petrichor"})
    assert "petrichor" in terms and "music" not in terms
    # sin separador de nombre, el título no aporta términos (no es un nombre de producto)
    assert holdout.leakage_terms(None, {"title": "A free tool to visualise scales on a guitar",
                                        "url": "https://news.ycombinator.com/item?id=1"}) == []
    assert holdout._RELAUNCH_RE.search("Foo v2 – now faster") and holdout._RELAUNCH_RE.search("Bar 2.0 is here")
    assert not holdout._RELAUNCH_RE.search("A tool for scales on a guitar")
