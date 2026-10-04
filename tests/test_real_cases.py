import pytest

from gapfinder import real_cases as rc


def test_normalize_github_key_and_domain():
    assert rc.normalize_url("https://www.GitHub.com/Foo/Bar.git/") == "github.com/foo/bar"
    assert rc.github_key("https://github.com/Foo/Bar/tree/main") == "github:foo/bar"
    assert rc.github_key("https://example.com/x") is None
    assert rc.site_domain("https://docs.keygen.sh/api") == "keygen.sh"
    assert rc.site_domain("https://github.com/a/b") is None
    assert rc.site_domain("https://app.example.co.uk/x") == "example.co.uk"


def test_clean_explanation_strips_internal_ids_only():
    text = "Agents spend money (704), inherit behaviors (603, 1139), ID:2190 adds memory, see #900. It needs 111 tests."
    assert rc.clean_explanation(text) == "Agents spend money, inherit behaviors, adds memory, see. It needs 111 tests."


def test_scope_hash_matches_constellate():
    # sha256("nh|T|1,2") con ids deduplicados y ordenados, como absenceScopeHash en constellate
    import hashlib
    c = {"neighborhood_hash": "nh", "title": "T", "idea_ids": [2, 1, 2]}
    assert rc._scope_hash(c) == hashlib.sha256(b"nh|T|1,2").hexdigest()


def test_parse_manual_and_rubric():
    manual = ("**1. Portkey — https://portkey.ai/**\n- What it does: gateway.\n\n"
              "**DOES SOMETHING ALREADY COVER THIS GAP? PARTIALLY** — Portkey covers half.")
    verdict, reason, items = rc._parse_manual(manual)
    assert verdict == "partially" and reason.startswith("Portkey covers")
    assert items == [{"name": "Portkey", "url": "https://portkey.ai/", "what": "gateway."}]
    rubric = "## Run 1\n\n**Verdict: YES**\n\nAlready filled.\n\n**Prior art:**\n- [Keygen](https://keygen.sh/) — licensing API.\n"
    assert rc._parse_rubric(rubric) == [("yes", "Already filled.", [{"name": "Keygen", "url": "https://keygen.sh/", "what": "licensing API."}])]


def test_parse_candidates():
    md = """## 1 · aaaaaaaa · Missing: X

esperado: https://github.com/a/b https://x.com show_hn:42 github:Foo/bar
confirmado: real

---
## 2 · bbbbbbbb · Y

esperado:
confirmado: negativo

---
## 3 · cccccccc · Z

confirmado: descartar

---
## 4 · dddddddd · W

confirmado:

---
## 5 · eeeeeeee · V

esperado: https://portkey.ai/ !github:Portkey-AI/gateway
confirmado: parcial

---
"""
    marked, discarded, pending = rc.parse_candidates(md)
    assert marked == [{"hash": "aaaaaaaa", "kind": "real", "expected_urls": ["https://github.com/a/b", "https://x.com"],
                       "expected_ids": ["show_hn:42", "github:Foo/bar"], "excluded_ids": []},
                      {"hash": "bbbbbbbb", "kind": "negative", "expected_urls": [], "expected_ids": [], "excluded_ids": []},
                      {"hash": "eeeeeeee", "kind": "partial", "expected_urls": ["https://portkey.ai/"], "expected_ids": [],
                       "excluded_ids": ["github:Portkey-AI/gateway"]}]
    assert discarded == ["cccccccc"] and pending == ["dddddddd"]
    with pytest.raises(ValueError):
        rc.parse_candidates("## 1 · aaaaaaaa · X\n\nconfirmado: quizás\n")


def test_corpus_index_resolution(tmp_path):
    import json

    from gapfinder import db

    conn = db.connect(tmp_path / "t.db")
    db.upsert_items(conn, [
        db.Item(id="github:langfuse/langfuse", source="github", url="https://github.com/langfuse/langfuse",
                title="langfuse", description="", created_at="2023-01-01T00:00:00Z", stars=9000,
                extra=json.dumps({"homepage": "https://langfuse.com"})),
        db.Item(id="show_hn:1", source="show_hn", url="https://www.keygen.sh/", title="Keygen – licensing API",
                description="", created_at="2019-01-01T00:00:00Z"),
        db.Item(id="show_hn:2", source="show_hn", url="https://blog.langchain.com/x", title="Aidress – LangChain thing",
                description="", created_at="2025-01-01T00:00:00Z"),
    ])
    idx = rc.CorpusIndex(conn)
    assert idx.lookup("https://github.com/LangFuse/langfuse")[0] == "github:langfuse/langfuse"
    assert idx.lookup("https://langfuse.com/docs", "Langfuse")[0] == "github:langfuse/langfuse"  # homepage del repo
    assert idx.lookup("https://langfuse.com/docs", "Langfuse Cloud")[0] == "github:langfuse/langfuse"
    assert idx.lookup("https://langfuse.com/docs")[0] is None                                  # sin nombre no alcanza
    assert idx.lookup("https://docs.keygen.sh/api", "Keygen (keygen.sh)")[0] == "show_hn:1"  # dominio + nombre
    assert idx.lookup("https://smith.langchain.com/", "LangSmith")[0] is None               # dominio sin nombre
    assert idx.lookup("https://github.com/x/y") == (None, "repo fuera del bulk")


def test_proposal_by_verdict():
    def absence(*verdicts):
        a = rc.Absence("h", "h", "T", "")
        a.verifications = [rc.Verification("web", v, "", []) for v in verdicts]
        return a

    assert rc.proposal(absence("partially", "yes")) == "real"
    assert rc.proposal(absence("partially", "no")) == "negative"
    assert rc.proposal(absence("partially", "partially")) == "partial"
    assert rc.proposal(absence("?")) is None


def test_corpus_index_real_ids_and_product_guard(tmp_path):
    import json

    from gapfinder import db

    def repo(full, homepage, desc=""):
        return db.Item(id=f"github:{full}", source="github", url=f"https://github.com/{full}", title=full.split("/")[1],
                       description=desc, created_at="2020-01-01T00:00:00Z", stars=500,
                       extra=json.dumps({"homepage": homepage}))

    conn = db.connect(tmp_path / "t.db")
    db.upsert_items(conn, [
        repo("BerriAI/litellm", "https://litellm.ai", "AI Gateway"),
        repo("guildai/guildai", "https://guild.ai", "Experiment tracking, ML developer tools"),
        repo("microsoft/magentic-ui", "https://microsoft.com", "Agent in the browser"),
        repo("NVIDIA/nvidia-settings", "https://nvidia.com", "NVIDIA driver control panel"),
        repo("NVIDIA/triton-inference-server", "https://nvidia.com", "Triton Inference Server"),
        repo("matrix-org/matrix.org", "https://matrix.org", "matrix.org public website"),
        repo("invoiceninja/invoiceninja", "https://invoiceninja.com", "Invoices, quotes and time tracking"),
        db.Item(id="show_hn:9", source="show_hn", url="https://morphllm.com/", title="Morph – Videos of AI testing your PR",
                description="", created_at="2025-01-01T00:00:00Z"),
    ])
    idx = rc.CorpusIndex(conn)
    assert idx.lookup("https://github.com/berriai/LiteLLM") == ("github:BerriAI/litellm", "repo")  # id real, no lowercased
    assert idx.lookup("https://guild.ai/blog", "Guild (Authorization + Governance Layer)")[0] is None  # guildai != guild
    assert idx.lookup("https://microsoft.com/x", "Agent Governance Toolkit (Microsoft)")[0] is None   # "agent" dentro de "magentic"
    assert idx.lookup("https://docs.nvidia.com/triton", "NVIDIA Triton — Stable Diffusion")[0] == "github:NVIDIA/triton-inference-server"
    assert idx.lookup("https://matrix.org/", "Matrix / Synapse")[0] is None                       # repo del sitio web
    assert idx.lookup("https://invoiceninja.com/x", "Invoice Ninja (self-hosted)")[0] == "github:invoiceninja/invoiceninja"
    assert idx.lookup("https://morphllm.com/llm-router", "Morph Router")[0] is None              # otro producto de la marca
    assert idx.resolve_id("github:berriai/LITELLM") == "github:BerriAI/litellm"
    assert idx.resolve_id("show_hn:9") == "show_hn:9" and idx.resolve_id("show_hn:10") is None


def test_corpus_index_excludes_non_base_items(tmp_path):
    from gapfinder import db

    conn = db.connect(tmp_path / "t.db")
    db.upsert_items(conn, [db.Item(id="github:a/b", source="github", url="https://github.com/a/b", title="b",
                                   description="", created_at="2020-01-01T00:00:00Z")])
    assert rc.CorpusIndex(conn).lookup("https://github.com/a/b")[0] == "github:a/b"
    assert rc.CorpusIndex(conn, exclude={"github:a/b"}).lookup("https://github.com/a/b")[0] is None
