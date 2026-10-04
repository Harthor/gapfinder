import math

from gapfinder import leakage


def test_terms_stems_and_drops_stopwords():
    assert leakage.terms("Tracking the trackers, easily!") == {"track"}
    assert "c++" in leakage.terms("a C++ library")


def test_check_flags_two_distinctive_or_one_rare():
    idf = leakage.Idf(n_docs=1_000_000, df={"search": 50_000, "elasticsearch": 3_000, "document": 8_000, "mixpanel": 40})
    item = "Calaca: search UI for Elasticsearch documents"
    ok = leakage.check("I want a quick way to search my indexed records", item, idf)
    assert not ok.flagged  # "search" no es distintivo (5%)
    two = leakage.check("A search page for my Elasticsearch documents", item, idf)
    assert two.flagged and [t for t, _ in two.distinctive] == ["elasticsearch", "document"]
    rare = leakage.check("aggregate mixpanel data", "MixpanelSelect uses the Mixpanel API", idf)
    assert rare.flagged and rare.rare[0][0] == "mixpanel"
    assert math.isclose(leakage.RARE_IDF, math.log(2000))
