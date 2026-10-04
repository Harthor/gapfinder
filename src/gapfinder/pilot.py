"""Piloto de la Fase 3: los mismos 50 pares para Jev y Haiku, más una hoja de revisión manual.

Selección estratificada (semilla fija) sobre data/phase3/candidates_<modelo>.json:
- 15 positivos: el item esperado de casos reales/sintéticos (dentro del top-1000).
- 15 near-miss: top-5 de casos donde el esperado quedó abajo (rank > 200 o ausente).
- 10 de rank medio: candidatos en posiciones 200-1000 que no son el esperado ni sus gemelos.
- 10 al azar del top-1000 (no esperados).
Los pares quedan en data/phase3/pilot_pairs.json; los veredictos en verdicts_pilot_<verificador>.jsonl.
"""

from __future__ import annotations

import json
import logging
import random
import re
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path

from gapfinder import phase3
from gapfinder.verify import OUT_DIR, Pair, Verdict, _append, haiku_params, load_done

log = logging.getLogger(__name__)

PAIRS_PATH = OUT_DIR / "pilot_pairs.json"
REVIEW_PATH = Path("data/eval/pilot_review.md")
DISAGREE = 0.3


def select(conn: sqlite3.Connection, cases: list[dict], candidates: dict[str, list[str]], seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    cases = [c for c in cases if c["kind"] in ("real", "synthetic") and c["id"] in candidates]
    rank = {}
    for c in cases:
        pos = {i: n for n, i in enumerate(candidates[c["id"]], 1)}
        rank[c["id"]] = min((pos[i] for i in c["expected_item_ids"] if i in pos), default=None)
    twins = {c["id"]: phase3.twins(conn, c["expected_item_ids"]) for c in cases}
    picked: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(c: dict, item: str, stratum: str) -> None:
        if (c["id"], item) not in seen:
            seen.add((c["id"], item))
            pos = candidates[c["id"]].index(item) + 1 if item in candidates[c["id"]] else None
            picked.append({"case_id": c["id"], "item_id": item, "stratum": stratum, "rank": pos})

    # positivos: todos los reales con esperado presente + sintéticos al azar hasta 15
    pos_cases = [c for c in cases if rank[c["id"]]]
    real_pos = [c for c in pos_cases if c["kind"] == "real"]
    syn_pos = [c for c in pos_cases if c["kind"] == "synthetic"]
    for c in rng.sample(real_pos, min(7, len(real_pos))) + rng.sample(syn_pos, 15 - min(7, len(real_pos))):
        best = min((i for i in c["expected_item_ids"] if i in candidates[c["id"]]), key=candidates[c["id"]].index)
        add(c, best, "positivo")
    # near-miss: top-5 de casos con el esperado abajo (> 200) o ausente; primero reales
    low = [c for c in cases if rank[c["id"]] is None or rank[c["id"]] > 200]
    low.sort(key=lambda c: (c["kind"] != "real", rng.random()))
    pool = [(c, i) for c in low for i in candidates[c["id"]][:5] if i not in twins[c["id"]]]
    per_case: dict[str, int] = {}
    for c, i in pool:
        if sum(p["stratum"] == "near-miss" for p in picked) >= 15:
            break
        if per_case.get(c["id"], 0) < 3:
            per_case[c["id"]] = per_case.get(c["id"], 0) + 1
            add(c, i, "near-miss")
    # rank medio y al azar
    for stratum, lo, hi, n in (("rank 200-1000", 200, 1000, 10), ("azar top-1000", 1, 1000, 10)):
        got = 0
        while got < n:
            c = rng.choice(cases)
            i = candidates[c["id"]][rng.randint(lo, min(hi, len(candidates[c["id"]]))) - 1]
            if i not in twins[c["id"]] and (c["id"], i) not in seen:
                add(c, i, stratum)
                got += 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PAIRS_PATH.write_text(json.dumps(picked, indent=1))
    return picked


def to_pairs(conn: sqlite3.Connection, cases: list[dict], picked: list[dict]) -> list[Pair]:
    by_id = {c["id"]: c for c in cases}
    cand = {}
    for p in picked:
        cand.setdefault(p["case_id"], []).append(p["item_id"])
    pairs = {(x.case_id, x.item_id): x for x in phase3.pairs_for(conn, [by_id[k] for k in cand], cand)}
    return [pairs[(p["case_id"], p["item_id"])] for p in picked]


def run_haiku(pairs: list[Pair], name: str = "haiku_pilot") -> dict:
    """Sincrónico (50 pares no justifican un batch). Mide latencia, tokens y errores de parsing/API."""
    import anthropic

    client = anthropic.Anthropic()
    done = load_done(name)
    errors = []
    for p in pairs:
        if (p.case_id, p.item_id) in done:
            continue
        t0 = time.perf_counter()
        try:
            msg = client.messages.create(**haiku_params(p))
        except anthropic.APIError as e:
            errors.append({"pair": [p.case_id, p.item_id], "error": f"api: {e}"})
            continue
        ms = (time.perf_counter() - t0) * 1000
        if msg.stop_reason != "end_turn":
            errors.append({"pair": [p.case_id, p.item_id], "error": f"stop_reason {msg.stop_reason}"})
            continue
        try:
            d = json.loads(next(b.text for b in msg.content if b.type == "text"))
            vals = [float(d[k]) for k in ("core", "partial", "same_user")]
        except (ValueError, KeyError, StopIteration) as e:
            errors.append({"pair": [p.case_id, p.item_id], "error": f"parse: {e}"})
            continue
        out_of_range = [v for v in vals if not 0 <= v <= 1]
        if out_of_range:
            errors.append({"pair": [p.case_id, p.item_id], "error": f"fuera de [0,1]: {out_of_range}"})
        clip = [min(max(v, 0.0), 1.0) for v in vals]
        _append(name, [Verdict(p.case_id, p.item_id, *clip, msg.usage.input_tokens, msg.usage.output_tokens,
                               msg.model, ms)])
    (OUT_DIR / f"errors_{name}.json").write_text(json.dumps(errors, indent=1))
    return {"errors": errors}


def summary(name: str, price_in: float, price_out: float) -> dict:
    v = list(load_done(name).values())
    if not v:
        return {"n": 0}
    lat = sorted(x.latency_ms for x in v)
    tin, tout = sum(x.input_tokens for x in v), sum(x.output_tokens for x in v)
    billed = [x.cost_usd for x in v if x.cost_usd is not None]
    return {"n": len(v), "latency_ms_p50": lat[len(lat) // 2], "latency_ms_p95": lat[int(len(lat) * 0.95) - 1],
            "input_tokens": tin, "output_tokens": tout,
            # costo real informado por el proveedor (OpenRouter usage.cost) si lo hay; si no, precio de lista
            "cost_usd": sum(billed) if len(billed) == len(v) else (tin * price_in + tout * price_out) / 1e6,
            "cost_source": "facturado por el proveedor" if len(billed) == len(v) else "precio de lista",
            "model": sorted({x.model for x in v})}


def agreement(pairs: list[Pair], a_name: str, b_name: str) -> dict:
    """Acuerdo entre dos verificadores sobre los mismos pares, por pregunta."""
    import numpy as np

    a, b = load_done(a_name), load_done(b_name)
    keys = [(p.case_id, p.item_id) for p in pairs if (p.case_id, p.item_id) in a and (p.case_id, p.item_id) in b]
    if len(keys) < 3:
        return {"n": len(keys)}
    out = {"n": len(keys), "faltan": len(pairs) - len(keys)}
    for q in ("core", "partial", "same_user"):
        x = np.array([getattr(a[k], q) for k in keys]); y = np.array([getattr(b[k], q) for k in keys])
        out[q] = {"diff_media_abs": round(float(np.abs(x - y).mean()), 3),
                  "pearson": round(float(np.corrcoef(x, y)[0, 1]), 3) if x.std() and y.std() else None,
                  "coinciden_a_0.5": round(float(((x >= 0.5) == (y >= 0.5)).mean()), 3),
                  "difieren_mas_de_0.3": int((np.abs(x - y) > DISAGREE).sum())}
    return out


def review(conn: sqlite3.Connection, cases: list[dict], picked: list[dict], pairs: list[Pair]) -> str:
    haiku = load_done("haiku_pilot")
    jev = load_done("jev_openrouter_pilot") or load_done("jev_pilot")   # OpenRouter si está; si no, TypeSafe nativo
    by_id = {c["id"]: c for c in cases}

    def fmt(v: Verdict | None) -> str:
        return (f"núcleo **{v.core:.2f}** · parcial {v.partial:.2f} · mismo usuario {v.same_user:.2f}"
                if v else "_pendiente_")

    rows, diffs = [], []
    for n, (meta, p) in enumerate(zip(picked, pairs), 1):
        k = (p.case_id, p.item_id)
        h, j = haiku.get(k), jev.get(k)
        diff = h is not None and j is not None and abs(h.core - j.core) > DISAGREE
        if diff:
            diffs.append(n)
        url = (conn.execute("SELECT url FROM items WHERE id = ?", (p.item_id,)).fetchone() or [""])[0]
        c = by_id[p.case_id]
        rows += [f"## {n}. {'⚠️ ' if diff else ''}{meta['stratum']} · `{p.case_id}` ({c['kind']}) · rank {meta['rank']}\n",
                 f"**Idea:** {p.idea}\n",
                 f"**Candidato:** `{p.item_id}` {url}  \n**{p.title}** — {re.sub(r'\\s+', ' ', p.text)[:600]}\n",
                 f"- Jev: {fmt(j)}", f"- Haiku: {fmt(h)}", "",
                 "mi veredicto: núcleo / parcial / no", "", "---\n"]
    jev_n = sum(1 for p in pairs if (p.case_id, p.item_id) in jev)
    head = ["# Piloto Fase 3: 50 pares, Jev vs Haiku\n",
            "Candidatos del top-1000 con embeddings MiniLM + llm5. Probabilidades de: implementa el núcleo, "
            "implementa al menos una parte real del núcleo, mismo usuario objetivo. Completá la línea "
            "`mi veredicto` de cada par.\n",
            f"Jev: {jev_n}/{len(pairs)} pares con respuesta. Haiku: "
            f"{sum(1 for p in pairs if (p.case_id, p.item_id) in haiku)}/{len(pairs)}.\n",
            f"**Pares donde Jev y Haiku difieren en núcleo por más de {DISAGREE}:** "
            + (", ".join(f"#{d}" for d in diffs) if diffs else ("ninguno" if jev_n else "— (falta correr Jev)")) + "\n",
            "---\n"]
    text = "\n".join(head + rows) + "\n"
    REVIEW_PATH.write_text(text)
    return text
