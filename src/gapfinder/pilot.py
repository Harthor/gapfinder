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


# --- revisión humana interactiva -----------------------------------------------------------------------

HUMAN_PATH = Path("data/eval/pilot_review_human.jsonl")
RESULT_PATH = Path("data/eval/pilot_review_result.md")
LABELS = {"s": "núcleo", "p": "parcial", "n": "no", "?": "no sé"}
JEV_PILOT = ("jev_openrouter_pilot", "jev_pilot")


def _jev_verdicts() -> dict:
    for name in JEV_PILOT:
        if (v := load_done(name)):
            return v
    return {}


def review_order(pairs: list[Pair], jev: dict) -> list[Pair]:
    """Primero Jev núcleo >= 0.5 (de mayor a menor), después cerca del umbral (0.3-0.5), al final < 0.3."""
    def key(p: Pair):
        core = jev[(p.case_id, p.item_id)].core if (p.case_id, p.item_id) in jev else 0.0
        group = 0 if core >= 0.5 else 1 if core >= 0.3 else 2
        return (group, -core if group == 0 else abs(core - 0.5))
    return sorted(pairs, key=key)


def load_human(path: Path | None = None) -> dict[tuple[str, str], str]:
    """Última respuesta por par (se puede cortar y retomar; una respuesta nueva pisa la anterior)."""
    path = path or HUMAN_PATH
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[(d["case_id"], d["item_id"])] = d["label"]
    return out


def agreement_vs_human(human: dict, jev: dict, haiku: dict, threshold: float = 0.5) -> dict:
    """Acuerdo a umbral: modelo núcleo >= umbral vs humano 's'; y parcial >= umbral vs humano 's' o 'p'.
    Los '?' no cuentan."""
    out = {}
    judged = {k: v for k, v in human.items() if v in ("s", "p", "n")}
    for name, model in (("jev", jev), ("haiku", haiku)):
        keys = [k for k in judged if k in model]
        if not keys:
            out[name] = {"n": 0}
            continue
        core_ok = sum((model[k].core >= threshold) == (judged[k] == "s") for k in keys)
        part_ok = sum((model[k].partial >= threshold) == (judged[k] in ("s", "p")) for k in keys)
        out[name] = {"n": len(keys), "nucleo": core_ok / len(keys), "parcial_o_mas": part_ok / len(keys)}
    return out


def write_result(conn: sqlite3.Connection, picked: list[dict], pairs: list[Pair], complete: bool) -> str:
    human, jev, haiku = load_human(), _jev_verdicts(), load_done("haiku_pilot")
    agr = agreement_vs_human(human, jev, haiku)
    strata = {(p["case_id"], p["item_id"]): p["stratum"] for p in picked}
    counts = {lab: sum(v == lab for v in human.values()) for lab in LABELS}
    L = ["# Piloto Fase 3: revisión humana vs Jev y Haiku\n",
         f"{'Revisión completa' if complete else 'Revisión PARCIAL'}: {len(human)}/{len(pairs)} pares respondidos "
         f"({', '.join(f'{LABELS[k]} {v}' for k, v in counts.items())}). Umbral 0.5. "
         "Núcleo: modelo P(núcleo) >= 0.5 vs humano = núcleo. Parcial o más: P(parcial) >= 0.5 vs humano = "
         "núcleo o parcial. Los \"no sé\" no cuentan.\n",
         "| modelo | pares | acuerdo núcleo | acuerdo parcial o más |", "|---|---|---|---|"]
    for name in ("jev", "haiku"):
        a = agr[name]
        L.append(f"| {name} | {a['n']} | " + (f"{a['nucleo']:.0%} | {a['parcial_o_mas']:.0%} |" if a["n"] else "– | – |"))
    L += ["", "## Desacuerdos en núcleo (umbral 0.5)\n",
          "| # | estrato | caso | candidato | humano | Jev núcleo | Haiku núcleo | quién difiere |", "|---|---|---|---|---|---|---|---|"]
    order = {(p.case_id, p.item_id): n for n, p in enumerate(pairs, 1)}  # numeración de pilot_review.md
    for p in pairs:
        k = (p.case_id, p.item_id)
        if human.get(k) not in ("s", "p", "n"):
            continue
        h_pos = human[k] == "s"
        who = [name for name, m in (("Jev", jev), ("Haiku", haiku)) if k in m and (m[k].core >= 0.5) != h_pos]
        if who:
            fmt = lambda m: f"{m[k].core:.2f}" if k in m else "–"
            L.append(f"| {order[k]} | {strata.get(k, '')} | `{p.case_id}` | {p.title[:50]} | {LABELS[human[k]]} | "
                     f"{fmt(jev)} | {fmt(haiku)} | {' y '.join(who)} |")
    text = "\n".join(L) + "\n"
    RESULT_PATH.write_text(text)
    return text


def _getkey() -> str:
    """Una tecla sin Enter si hay terminal; si no (tests, pipes), una línea."""
    import sys

    if not sys.stdin.isatty():
        return (sys.stdin.readline() or "q").strip()[:1].lower()
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return "q" if ch in ("\x03", "\x04") else ch.lower()   # Ctrl-C / Ctrl-D = salir guardando


def interactive_review(conn: sqlite3.Connection, cases: list[dict], getkey=_getkey, out=print) -> dict:
    import shutil
    import textwrap
    import webbrowser
    from datetime import datetime, timezone

    picked = json.loads(PAIRS_PATH.read_text())
    pairs = to_pairs(conn, cases, picked)
    jev, haiku = _jev_verdicts(), load_done("haiku_pilot")
    human = load_human()
    queue = [p for p in review_order(pairs, jev) if (p.case_id, p.item_id) not in human]
    width = min(shutil.get_terminal_size((100, 30)).columns, 110)
    wrap = lambda s, n, lines: textwrap.wrap(re.sub(r"\s+", " ", s)[:n], width - 4)[:lines]
    HUMAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    done_now = 0
    for p in queue:
        k = (p.case_id, p.item_id)
        url = (conn.execute("SELECT url FROM items WHERE id = ?", (p.item_id,)).fetchone() or [""])[0]
        fmt = lambda m: f"{m[k].core:.2f}" if k in m else "–"
        out("\033[2J\033[H" if getkey is _getkey else "", end="")
        out(f"[{len(human) + 1}/{len(pairs)}]  {p.case_id}")
        out("IDEA:      " + "\n           ".join(wrap(p.idea, 260, 2)))
        out(f"CANDIDATO: {p.title}")
        for line in wrap(p.text, 360, 3):
            out("           " + line)
        out(f"           {url}")
        out(f"NÚCLEO:    Jev {fmt(jev)}   |   Haiku {fmt(haiku)}")
        out("\n[s] núcleo   [p] parcial   [n] no es lo mismo   [?] no sé   [o] abrir URL   [q] guardar y salir")
        while True:
            key = getkey()
            if key == "o":
                if url:
                    webbrowser.open(url)
                continue
            if key in LABELS or key == "q":
                break
        if key == "q":
            break
        with HUMAN_PATH.open("a") as f:   # se guarda enseguida: cortar y retomar no pierde nada
            f.write(json.dumps({"case_id": p.case_id, "item_id": p.item_id, "label": key,
                                "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}) + "\n")
        human[k] = key
        done_now += 1
    complete = len(load_human()) >= len(pairs)
    text = write_result(conn, picked, pairs, complete)
    out("\n" + text.split("\n## ")[0])
    out(f"{'Revisión completa' if complete else 'Guardado; retomás donde quedaste'}. Resultado en {RESULT_PATH}")
    return {"respondidos_ahora": done_now, "total": len(load_human()), "completo": complete}
