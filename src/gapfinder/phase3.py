"""Fase 3: verificador sobre el top-K del retrieval.

1. `retrieve`: top-K por caso (K=1000) con embeddings del modelo elegido + llm5 (RRF), sin búsqueda dirigida.
2. `pairs_for`: pares (idea, candidato). idea = query_core (real/partial) o la necesidad (sintéticos).
3. Negativos por remoción: del top-K se sacan los items esperados y sus gemelos obvios (el Show HN que
   linkea al repo esperado y viceversa, misma URL normalizada). Sobre el resto, falsa alarma = algún
   candidato con P(core) >= umbral. Las alarmas más altas se listan para revisión manual (pueden ser
   implementaciones reales no listadas).
4. Positivos: casos con el item esperado dentro del top-K; ¿el verificador le da P(core) alta?
   Curva de recall por umbral usando el máximo P(core) entre los items esperados presentes.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path

import numpy as np

from gapfinder import embed, eval2, leakage
from gapfinder.real_cases import github_key, normalize_url
from gapfinder.text import get_texts
from gapfinder.verify import CANDIDATE_CHARS, OUT_DIR, Pair, Verdict

log = logging.getLogger(__name__)

K = 1000
THRESHOLDS = (0.5, 0.7, 0.8, 0.9, 0.95)
KINDS = ("real", "synthetic")


LLM_V1 = Path("data/llm_queries.json")


def retrieve(conn: sqlite3.Connection, cases: list[dict], model: str, k: int = K, llm_path: Path = LLM_V1,
             suffix: str = "") -> dict[str, list[str]]:
    idf = leakage.load_idf(conn, Path("data/cache/idf.json"))
    llm = json.loads(llm_path.read_text())
    ids, mat = embed.load(model, "corpus")
    mat = mat.astype(np.float32)
    out = {}
    for c in cases:
        qs = eval2.query_sets(c, llm, idf)["llm5"]
        lists = []
        for q in embed.encode_queries(model, qs):
            s = mat @ q
            top = np.argpartition(-s, eval2.TOP_K)[:eval2.TOP_K]
            lists.append([ids[i] for i in top[np.argsort(-s[top])]])
        out[c["id"]] = eval2.rrf(lists)[:k]
    path = OUT_DIR / f"candidates_{model}{suffix}.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out))
    return out


_LINKS: dict[int, dict] = {}


def _links(conn: sqlite3.Connection) -> dict:
    """Índices en memoria (una pasada por conexión): URL normalizada -> ids, repo de GitHub -> Show HN que
    lo linkean (por URL o por enrichment.github_repo), Show HN -> repo, id en minúsculas -> id real."""
    if id(conn) not in _LINKS:
        by_url: dict[str, set[str]] = {}
        repo_to_hn: dict[str, set[str]] = {}
        hn_to_repo: dict[str, str] = {}
        real_id: dict[str, str] = {}
        for iid, url in conn.execute("SELECT id, url FROM items"):
            by_url.setdefault(normalize_url(url), set()).add(iid)
            real_id[iid.lower()] = iid
            if iid.startswith("show_hn:") and (key := github_key(url)):
                repo_to_hn.setdefault(key.lower(), set()).add(iid)
                hn_to_repo[iid] = key.lower()
        for iid, repo in conn.execute("SELECT item_id, github_repo FROM enrichment WHERE github_repo IS NOT NULL"):
            repo_to_hn.setdefault(f"github:{repo}".lower(), set()).add(iid)
            hn_to_repo.setdefault(iid, f"github:{repo}".lower())
        _LINKS[id(conn)] = {"by_url": by_url, "repo_to_hn": repo_to_hn, "hn_to_repo": hn_to_repo, "real_id": real_id,
                            "url_of": dict(conn.execute("SELECT id, url FROM items"))}
    return _LINKS[id(conn)]


def twins(conn: sqlite3.Connection, expected: list[str]) -> set[str]:
    """Items esperados + duplicados obvios: Show HN <-> repo linkeado y misma URL normalizada."""
    ix = _links(conn)
    out = set(expected)
    for iid in expected:
        if iid.startswith("github:"):
            out |= ix["repo_to_hn"].get(iid.lower(), set())   # mismo repo exacto (no owner/repo-extra)
        elif (repo := ix["hn_to_repo"].get(iid)) and repo in ix["real_id"]:
            out.add(ix["real_id"][repo])
        if (url := ix["url_of"].get(iid)):
            out |= ix["by_url"].get(normalize_url(url), set())
    return out


def idea_text(case: dict, llm: dict) -> str:
    return llm.get(case["id"], {}).get("query_core") or case["title"]


def pairs_for(conn: sqlite3.Connection, cases: list[dict], candidates: dict[str, list[str]],
              llm_path: Path = LLM_V1) -> list[Pair]:
    llm = json.loads(llm_path.read_text())
    all_ids = sorted({i for c in cases for i in candidates.get(c["id"], [])})
    texts = get_texts(conn, all_ids)
    return [Pair(c["id"], idea_text(c, llm), i, texts[i].title, texts[i].body[:CANDIDATE_CHARS])
            for c in cases for i in candidates.get(c["id"], [])]


# --- métricas -----------------------------------------------------------------------------------------


def metrics(conn: sqlite3.Connection, cases: list[dict], candidates: dict[str, list[str]],
            verdicts: dict[tuple[str, str], Verdict]) -> dict:
    """Falsas alarmas (negativos por remoción) y recall de positivos por umbral, por kind; `real` también
    sin los casos con label_note (etiqueta observada como dudosa, no reetiquetada)."""
    out: dict = {"false_alarm": {}, "positive_recall": {}, "top_alarms": []}
    groups = {k: [c for c in cases if c["kind"] == k] for k in KINDS}
    groups["real sin label_note"] = [c for c in groups["real"] if not c.get("label_note")]
    for kind, group in groups.items():
        sel = [c for c in group if c["id"] in candidates]
        neg_max, pos_max = [], []
        for c in sel:
            removed = twins(conn, c.get("expected_item_ids", []))
            rest = [i for i in candidates[c["id"]] if i not in removed and (c["id"], i) in verdicts]
            if rest:
                best = max(rest, key=lambda i: verdicts[(c["id"], i)].core)
                neg_max.append(verdicts[(c["id"], best)].core)
                if kind in KINDS:  # "real sin label_note" repetiría las mismas alarmas
                    out["top_alarms"].append({"case": c["id"], "item": best, **{
                        k: getattr(verdicts[(c["id"], best)], k) for k in ("core", "partial", "same_user")}})
            present = [i for i in c.get("expected_item_ids", []) if (c["id"], i) in verdicts]
            if present:
                pos_max.append(max(verdicts[(c["id"], i)].core for i in present))
        out["false_alarm"][kind] = {t: (sum(x >= t for x in neg_max) / len(neg_max) if neg_max else None)
                                    for t in THRESHOLDS} | {"n": len(neg_max)}
        out["positive_recall"][kind] = {t: (sum(x >= t for x in pos_max) / len(pos_max) if pos_max else None)
                                        for t in THRESHOLDS} | {"n": len(pos_max)}
    out["top_alarms"].sort(key=lambda a: -a["core"])
    return out


# --- estimación de costo -----------------------------------------------------------------------------

PRICES = {  # USD por millón de tokens
    "haiku": {"input": 1.00, "output": 5.00, "batch_discount": 0.5},   # claude-haiku-4-5
    "jev": {"input": 0.042, "output": 0.0},                             # jev-1.13: solo entrada
}


def estimate(conn: sqlite3.Connection, cases: list[dict], candidates: dict[str, list[str]], sample: int = 60,
             seed: int = 0) -> dict:
    """Tokens por par medidos con count_tokens de Anthropic (gratis) sobre una muestra; costo y tiempo
    para todos los pares. Jev: su tokenizer no es público; se usa el conteo de Claude del mismo texto
    (state + las tres preguntas) como aproximación."""
    import random

    import anthropic

    from gapfinder.verify import HAIKU_SYSTEM, QUESTIONS, haiku_params

    pairs = pairs_for(conn, cases, candidates)
    rng = random.Random(seed)
    sample_pairs = rng.sample(pairs, min(sample, len(pairs)))
    client = anthropic.Anthropic()
    haiku_in = []
    jev_in = []
    q_text = json.dumps({k: {"instructions": q["instructions"], "criteria": {"true": q["true"], "false": q["false"]}}
                         for k, q in QUESTIONS.items()})
    for p in sample_pairs:
        params = haiku_params(p)
        n = client.messages.count_tokens(model=params["model"], system=params["system"],
                                         messages=params["messages"]).input_tokens
        haiku_in.append(n)
        # Jev: state (idea + candidato en JSON) + las 3 preguntas; aproximado con el tokenizer de Claude
        jev_in.append(client.messages.count_tokens(model=params["model"], messages=[
            {"role": "user", "content": json.dumps(p.state()) + q_text}]).input_tokens)
    n_pairs = len(pairs)
    h_in, j_in, h_out = float(np.mean(haiku_in)), float(np.mean(jev_in)), 40.0  # salida: JSON con 3 números
    haiku_cost = n_pairs * (h_in * PRICES["haiku"]["input"] + h_out * PRICES["haiku"]["output"]) / 1e6
    return {
        "pairs": n_pairs, "cases": len({p.case_id for p in pairs}), "sample": len(sample_pairs),
        "haiku_tokens_per_pair": {"input_mean": h_in, "input_p95": float(np.percentile(haiku_in, 95)), "output_est": h_out},
        "jev_tokens_per_pair_approx": {"input_mean": j_in, "input_p95": float(np.percentile(jev_in, 95))},
        "haiku_cost_usd": {"standard": haiku_cost, "batch": haiku_cost * PRICES["haiku"]["batch_discount"]},
        "jev_cost_usd": n_pairs * j_in * PRICES["jev"]["input"] / 1e6,
        "jev_minutes_at_1200_rpm": n_pairs / 1200,
        "system_prompt_tokens_haiku": len(HAIKU_SYSTEM) // 4,
    }
