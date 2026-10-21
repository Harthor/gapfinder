"""Candidatos a hueco a partir de Ask HN: extracción automática (v2) y lista final para revisión humana.

1. `extract`: por cada uno de los Asks filtrados (data/askhn/asks.json) un output validado
   {id, pedido_real, etiqueta e/p/n/?, pedido_resumido, justificacion}, con gpt-oss vía OpenRouter, prompt con
   las definiciones de las etiquetas y 4 ejemplos few-shot. Cache JSONL por id (data/askhn/extract_v2.jsonl).
2. `run`: los pedido_real=true pasan al retrieval contra el corpus anterior a la fecha del Ask (mismo enmascarado
   que el holdout): query_core = pedido_resumido, 4 reformulaciones con gpt-oss y el prompt v2 (llm5 + RRF),
   top-K MiniLM y Jev vía OpenRouter. Primero K=200 para todos; los que quedan como hueco (ningún candidato
   >= 0.85) se re-corren con K=1000 (el top-200 es prefijo del top-1000: solo se verifican los 800 nuevos).
3. `compare`: misma opción barata sobre los 40 Asks de la Fase 4 (misma idea v1) contra el método completo.
4. `report`: data/eval/gap_candidates.md.

Frena ante 401/402/403 y si el saldo de OpenRouter baja de MIN_BALANCE.
"""

from __future__ import annotations

import json
import logging
import random
import re
from collections import Counter
from pathlib import Path

from gapfinder import askhn

log = logging.getLogger(__name__)

EXTRACT_V2 = askhn.DIR / "extract_v2.jsonl"
QUERIES = askhn.DIR / "gap_queries.json"
CANDIDATES = askhn.DIR / "gap_candidates.json"      # top-1000 por caso (se verifica el prefijo que toque)
STATE = askhn.DIR / "gap_state.json"                 # K verificado por caso
VERDICTS = "jev_gaps"
REPORT = Path("data/eval/gap_candidates.md")
COMPARE_REPORT = Path("data/eval/gap_compare_k200.md")
MIN_BALANCE = 0.50
K_FIRST, K_FULL = 200, 1000
HUECO = 0.85     # regla de la Fase 3: < 0.85 = no hay match fuerte
FUERTE = 0.60    # hueco fuerte: mejor P(núcleo) < 0.60 y los comentarios no dicen que existe
LABELS = {"e": "existe", "p": "parcial", "n": "no existe", "?": "incierto"}
TIERS = {"fuerte": "hueco fuerte", "gris": "zona gris", "descartado": "descartado (etiqueta e)",
         "match": f"match >= {HUECO}", "no_software": "no es software"}

# Filtro "no es software": el sintagma nominal del pedido (lo que va antes del primer "that/to/for/with/of…")
# o la forma del título del Ask.
_HEAD_STOP = r"\s(?:that|which|to|for|with|of|in|on|from|by|via|using|where|like|similar)\s"
_NO_SOFTWARE_HEAD = {
    "hardware": r"\b(device|phone(?!\s+(numbers?|calls?))|smart ?watch|watch|wristband|e-?reader|ebook reader|sensor|collar"
                r"|robot|robotics|hardware|wearable)s?\b",
    "contenido": r"\b(book|course|bootcamp|curriculum|tutorial|guide|template|license|list)s?\b",
}
_NO_SOFTWARE_TITLE = {
    "encuesta": r"\b(what|which)\s+(\w+\s+){0,2}(do|would|are)\s+you\b|\bhow do you\b|\bdo you use\b",
    "se puede": r"\bis there (a|any) way\b|\bany way (to|for)\b|\bis it possible\b",
}

# --- 1. extracción v2 -----------------------------------------------------------------------------------

SYSTEM_V2 = """You read an "Ask HN" thread from Hacker News (title, the original poster's text, and comments) and \
classify it. Output fields:

pedido_real (bool): true only if the original poster (OP) is asking whether a software tool, app, library, service \
or product exists, or asking for one, to solve a specific need they describe. False for: requests for business \
ideas ("what would you pay for?"), opinion polls and surveys ("how does your team do X?"), venting or general \
workflow advice, career/hiring questions, hardware shopping, or requests too vague to describe as one tool.

etiqueta: what the COMMENTS say about whether such a tool exists (fill it even if pedido_real is false):
- "e" (existe): at least one commenter suggests a concrete tool presented as doing what the OP asks, and nobody \
credibly refutes it.
- "p" (parcial): only tools that cover part of the need, workarounds, or hedged suggestions.
- "n" (no existe): the thread says nothing like this exists, people searched and found nothing, or they built \
their own because nothing existed; and no equivalent is suggested.
- "?" (incierto): anything else (no useful answers, off-topic replies, conflicting claims).

pedido_resumido: ONE line in English (max 30 words) saying what the OP wants built, as someone searching for such \
a tool would state it. Use standard category terms (e.g. "bookmarking service", "reverse proxy"), but NEVER name \
existing products, companies, projects or services, even ones in the thread.

justificacion: one short sentence in Spanish (max 25 words) explaining pedido_real and etiqueta, citing the \
thread."""

FEW_SHOT = [
    ("""Title: Ask HN: Is there a spiritual successor to del.icio.us?
OP text: Recently I found myself looking for a place to store bookmarks. I used to love del.icio.us, but it's no \
longer around. What is its spiritual successor? The most important things for me would be integration with \
browsers, maybe a dedicated app, and mobile / desktop support.
Comments:
[answer] pinboard.in
[answer] https://raindrop.io/
[answer] I moved from delicious to pinboard, then to nextcloud bookmarks, then finally to Evernote.""",
     {"pedido_real": True, "etiqueta": "e",
      "pedido_resumido": "A social bookmarking service to save and tag links, with browser integration and mobile and desktop apps.",
      "justificacion": "Pide un servicio concreto de marcadores; varios comentarios sugieren equivalentes directos sin objeciones."}),
    ("""Title: Ask HN: Is there an app that reviews/rates individual menu items in restaurants?
OP text: Restaurant review sites rate the whole place, but I want to know which dish to order. Is there an app \
where people rate individual menu items?
Comments:
[answer] I don't know of any, but seems like a great app idea.
[answer] I wanted to build this in 2011, didn't finish.
[answer] Some review sites let you attach photos of dishes, but you can't rate the dish itself.""",
     {"pedido_real": True, "etiqueta": "n",
      "pedido_resumido": "A mobile app where diners rate and review individual dishes on restaurant menus, not just the restaurant.",
      "justificacion": "Pide una app concreta; los comentarios dicen que no conocen ninguna y uno intentó construirla."}),
    ("""Title: Ask HN: What software would you pay for right now?
OP text: Looking for some ideas on what to build for small-medium sized businesses/startups.
Comments:
[answer] I would pay for a stripped down better designed version of soundcloud for producers to share samples.
[answer] Better automated webinar software. The existing solutions are good feature wise but the UX's are awful.""",
     {"pedido_real": False, "etiqueta": "?",
      "pedido_resumido": "Ideas for software products to build and sell to small and medium businesses.",
      "justificacion": "El OP pide ideas de negocio, no una herramienta para una necesidad propia; los comentarios proponen cosas dispares."}),
    ("""Title: Ask HN: How do you keep sane while developing for Android?
OP text: There's something wrong with the ecosystem. The official IDE is one of the worst pieces of software I've \
ever had to code with. Every time you post a question about the IDE, there's a flurry of down-votes.
Comments:
[answer] I develop for Android using C# with another IDE. The grass isn't necessarily greener on this side.
[answer] I sometimes just use a text editor and then use gradle and adb right from the command line.""",
     {"pedido_real": False, "etiqueta": "p",
      "pedido_resumido": "A more stable development environment and workflow for building Android apps.",
      "justificacion": "Es una queja y pedido de consejos, no un pedido de herramienta; las respuestas son workarounds parciales."}),
]

SCHEMA_V2 = {
    "type": "object",
    "properties": {
        "pedido_real": {"type": "boolean"},
        "etiqueta": {"type": "string", "enum": ["e", "p", "n", "?"]},
        "pedido_resumido": {"type": "string"},
        "justificacion": {"type": "string"},
    },
    "required": ["pedido_real", "etiqueta", "pedido_resumido", "justificacion"],
    "additionalProperties": False,
}


def system_with_examples() -> str:
    shots = "\n\n".join(f"### Example {n}\n{thread}\nOutput: {json.dumps(out, ensure_ascii=False)}"
                        for n, (thread, out) in enumerate(FEW_SHOT, 1))
    return f"{SYSTEM_V2}\n\n{shots}"


def valid_v2(d: dict) -> bool:
    """Descarta salidas degeneradas (gpt-oss con schema estricto a veces devuelve "...."): pedido_resumido con
    >= 5 palabras y una línea; justificación con >= 4 palabras."""
    line = d.get("pedido_resumido", "")
    return (len(re.findall(r"[A-Za-z]{2,}", line)) >= 5 and "\n" not in line.strip()
            and len(re.findall(r"\w{2,}", d.get("justificacion", ""))) >= 4)


def load_v2(path: Path | None = None) -> dict[str, dict]:
    """Cache por id: la última línea por id gana."""
    path = path or EXTRACT_V2
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[d["id"]] = d
    return out


def extract(limit: int | None = None, workers: int = 8) -> dict:
    """Procesa los Asks que faltan en el cache (reanudable). Hasta 3 intentos por Ask (el tercero con el modelo
    de respaldo); las respuestas inválidas no se guardan pero su costo sí (campo cost_usd del intento válido
    acumula los anteriores; si los 3 fallan, va a la línea de error)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    import httpx

    asks = askhn.load_asks()
    done = load_v2()
    todo = [a for a in sorted(asks) if a not in done or not done[a].get("ok")][:limit]
    log.info("extracción v2: %d por hacer (%d en cache)", len(todo), len(done))
    system = system_with_examples()

    def one(aid: str) -> dict:
        cost, last = 0.0, None
        for attempt, model in enumerate((askhn.EXTRACT_MODEL, askhn.EXTRACT_MODEL, askhn.FALLBACK_MODEL)):
            try:
                data, usage = askhn._openrouter(client, model, system, askhn.thread_text(asks[aid]), SCHEMA_V2, "ask_v2")
            except askhn.FatalAPIError:
                raise
            except Exception as e:  # noqa: BLE001
                last = str(e)
                continue
            cost += usage.get("cost", 0)
            if valid_v2(data):
                return {"id": aid, **data, "ok": True, "model": model, "attempts": attempt + 1, "cost_usd": cost}
            last = f"salida inválida: {data.get('pedido_resumido', '')[:60]!r}"
            log.warning("v2 %s intento %d: %s", aid, attempt + 1, last)
        return {"id": aid, "ok": False, "error": last, "cost_usd": cost}

    EXTRACT_V2.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=90) as client, ThreadPoolExecutor(workers) as pool, EXTRACT_V2.open("a") as f:
        futures = [pool.submit(one, a) for a in todo]
        for n, fut in enumerate(as_completed(futures), 1):
            rec = fut.result()
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if n % 25 == 0 or n == len(todo):
                log.info("extracción v2: %d/%d", n, len(todo))
    return summary(sample=25 if not limit else limit, only=todo if limit else None)


def summary(sample: int = 25, seed: int = 7, only: list[str] | None = None) -> dict:
    """Conteos por pedido_real y etiqueta, y `sample` extracciones al azar (semilla fija) en texto legible."""
    asks, v2 = askhn.load_asks(), load_v2()
    ok = {a: d for a, d in v2.items() if d.get("ok")}
    pick = [a for a in only if a in ok] if only else random.Random(seed).sample(sorted(ok), min(sample, len(ok)))
    lines = []
    for a in pick:
        d, ask = ok[a], asks[a]
        lines.append(f"\n[{a}] {ask['title']}\n  {ask['created_at'][:10]} · {ask['points']} pts · {ask['num_comments']} comentarios · {ask['hn_url']}\n"
                     f"  pedido_real: {'sí' if d['pedido_real'] else 'no'}   etiqueta: {d['etiqueta']} ({LABELS[d['etiqueta']]})\n"
                     f"  pedido_resumido: {d['pedido_resumido']}\n  justificación: {d['justificacion']}")
    real = [d for d in ok.values() if d["pedido_real"]]
    return {"procesados": len(ok), "fallidos": sum(not d.get("ok") for d in v2.values()),
            "pedido_real": dict(Counter("sí" if d["pedido_real"] else "no" for d in ok.values())),
            "etiqueta_todos": dict(Counter(d["etiqueta"] for d in ok.values())),
            "etiqueta_pedidos_reales": dict(Counter(d["etiqueta"] for d in real)),
            "costo_usd": round(sum(d.get("cost_usd", 0) for d in v2.values()), 4),
            "muestra": "\n".join(lines)}


# --- 2. retrieval + Jev ---------------------------------------------------------------------------------


def balance() -> float:
    import os

    import httpx

    r = httpx.get("https://openrouter.ai/api/v1/credits", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                  timeout=30)
    r.raise_for_status()
    d = r.json()["data"]
    return d["total_credits"] - d["total_usage"]


def _reformulations(case_id: str, query_core: str, store: dict) -> dict:
    """4 reformulaciones + 3 palabras clave con el prompt v2 (rama 'need'), con gpt-oss vía OpenRouter."""
    import httpx

    from gapfinder import llm

    if case_id in store:
        return store[case_id]
    text, schema = llm._prompt({"id": case_id, "kind": "need", "title": query_core})
    good, cost = None, 0.0
    with httpx.Client(timeout=120) as client:
        for attempt in range(4):
            try:
                raw, usage = askhn._openrouter(client, askhn.EXTRACT_MODEL, llm.PROMPT_VERSIONS[2], text, schema,
                                               "queries", max_tokens=2500)
                cost += usage.get("cost", 0)
                data = llm._lists(raw)
            except askhn.FatalAPIError:
                raise
            except (KeyError, RuntimeError, httpx.HTTPError) as e:   # truncado por max_tokens o sin JSON válido
                log.warning("%s: reformulaciones sin JSON válido (intento %d): %s", case_id, attempt + 1, str(e)[:80])
                continue
            if all(len(re.findall(r"[A-Za-z]{2,}", r)) >= 4 for r in data["reformulations"]):
                good = data
                break
            log.warning("%s: reformulaciones inválidas (intento %d)", case_id, attempt + 1)
    if good is None:
        raise RuntimeError(f"{case_id}: sin reformulaciones válidas en 4 intentos")
    store[case_id] = {**good, "query_core": query_core, "model": askhn.EXTRACT_MODEL, "prompt_version": 2,
                      "cost_usd": cost}
    return store[case_id]


def prefetch_reformulations(cases: list[dict], queries_path: Path, workers: int = 8) -> int:
    """Pide en paralelo las reformulaciones que faltan (gpt-oss tarda hasta ~1 min por llamada) y las guarda a
    medida que llegan. Devuelve cuántas quedaron sin reformulaciones válidas."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    store = askhn._load(queries_path, {})
    todo = [c for c in cases if c["id"] not in store]
    failed = 0
    with ThreadPoolExecutor(workers) as pool:
        futures = {pool.submit(_reformulations, c["id"], c["query_core"], {}): c for c in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            c = futures[fut]
            try:
                store[c["id"]] = fut.result()
            except askhn.FatalAPIError:
                raise
            except RuntimeError as e:
                failed += 1
                log.error("gaps: %s", e)
            if n % 10 == 0 or n == len(todo):
                queries_path.write_text(json.dumps(store, indent=1, ensure_ascii=False))
                log.info("gaps: reformulaciones %d/%d", n, len(todo))
    return failed


def _process(conn, masked, cases: list[dict], k: int, queries_path: Path, cand_path: Path, verdicts: str,
             reuse: str | None = None) -> str | None:
    """Para cada caso {id, ask_id, query_core}: reformulaciones, top-1000 anterior al Ask (se guarda) y Jev sobre el
    top-k. reuse: nombre de otro archivo de veredictos del que copiar pares con la misma idea (mismo input a Jev).
    Devuelve el motivo si se detuvo."""
    from dataclasses import asdict

    from gapfinder.verify import OpenRouterJevVerifier, Verdict, _append, load_done

    asks = askhn.load_asks()
    store = askhn._load(queries_path, {})
    cand = askhn._load(cand_path, {})
    verifier = OpenRouterJevVerifier(name=verdicts, concurrency=6)
    reused = load_done(reuse) if reuse else {}
    for n, c in enumerate(cases, 1):
        cid = c["id"]
        done = load_done(verdicts)
        if cid in cand and all((cid, i) in done for i in cand[cid][:k]):
            continue
        bal = balance()
        if bal < MIN_BALANCE:
            return f"saldo de OpenRouter ${bal:.2f} < ${MIN_BALANCE:.2f}"
        try:
            q = _reformulations(cid, c["query_core"], store)
        except askhn.FatalAPIError:
            raise
        except RuntimeError as e:
            log.error("gaps: %s; sigo con el próximo", e)
            continue
        queries_path.write_text(json.dumps(store, indent=1, ensure_ascii=False))
        if cid not in cand:
            cand[cid], _ = masked.top([q["query_core"], *q["reformulations"]], asks[c["ask_id"]]["created_at"], K_FULL)
            cand_path.write_text(json.dumps(cand))
        pairs = askhn._pairs(conn, cid, cand[cid][:k], q["query_core"])
        todo = []
        copies = []
        for p in pairs:
            if (p.case_id, p.item_id) in done:
                continue
            src = reused.get((c.get("reuse_id", cid), p.item_id))
            if src and c.get("reuse_id"):   # mismo input a Jev (misma idea, mismo candidato): se copia, costo 0
                copies.append(Verdict(**{**asdict(src), "case_id": cid, "cost_usd": 0.0,
                                         "model": f"{src.model} (copiado de {reuse})"}))
            else:
                todo.append(p)
        if copies:
            _append(verdicts, copies)
        log.info("gaps: %d/%d %s k=%d: %d pares nuevos, %d reutilizados, saldo $%.2f", n, len(cases), cid, k, len(todo),
                 len(copies), bal)
        verifier.verify(todo)
    return None


def _best(cid: str, items: list[str], ver: dict) -> tuple[float, list[str]]:
    scored = sorted((i for i in items if (cid, i) in ver), key=lambda i: -ver[(cid, i)].core)
    return (ver[(cid, scored[0])].core if scored else 0.0), scored


def compare(conn) -> str:
    """Los 40 Asks de la Fase 4 con la opción barata (misma idea v1 como query_core, reformulaciones gpt-oss,
    top-200) contra el método completo (Opus 5 + top-1000). Pares con la misma idea y el mismo candidato se
    reutilizan del método completo (mismo input a Jev)."""
    from gapfinder.holdout import decide
    from gapfinder.verify import load_done

    sel, ext = askhn.load_selected(), askhn.load_extractions()
    cases = [{"id": f"cmp-{a}", "ask_id": a, "query_core": ext[a]["idea"], "reuse_id": askhn.case_id(a)} for a in sel]
    stopped = _process(conn, askhn._Masked(conn), cases, K_FIRST, askhn.DIR / "cmp_queries.json",
                       askhn.DIR / "cmp_candidates.json", "jev_cmp", reuse=askhn.VERDICTS)
    full, cheap = load_done(askhn.VERDICTS), load_done("jev_cmp")
    fcand = askhn._load(askhn.CANDIDATES, {})
    ccand = askhn._load(askhn.DIR / "cmp_candidates.json", {})
    rows = []
    for a in sel:
        fid, cid = askhn.case_id(a), f"cmp-{a}"
        if fid not in fcand or cid not in ccand or any((cid, i) not in cheap for i in ccand[cid][:K_FIRST]):
            continue
        fb, fs = _best(fid, fcand[fid], full)
        cb, cs = _best(cid, ccand[cid][:K_FIRST], cheap)
        rows.append((a, fb, cb, fs[0], cs[0]))
    asks = askhn.load_asks()
    to_gap = [r for r in rows if r[1] >= HUECO and r[2] < HUECO]
    to_match = [r for r in rows if r[1] < HUECO and r[2] >= HUECO]
    dec = Counter((decide(r[1]), decide(r[2])) for r in rows)
    L = ["# Opción barata (gpt-oss + top-200) vs método completo (Opus 5 + top-1000), mismos 40 Asks\n",
         f"Misma idea (extracción v1) como query_core en ambos; cambia el modelo de las reformulaciones (gpt-oss-120b vs "
         f"claude-opus-5, mismo prompt v2) y K (200 vs 1000). Comparados: {len(rows)}."
         + (f" Detenido: {stopped}." if stopped else "") + "\n",
         f"- **Match >= {HUECO} con el método completo que pasan a hueco con la opción barata: {len(to_gap)}** "
         f"(de {sum(r[1] >= HUECO for r in rows)} con match).",
         f"- Hueco con el método completo que pasan a match con la opción barata: {len(to_match)}.",
         f"- Mismo lado del umbral 0.85: {len(rows) - len(to_gap) - len(to_match)}/{len(rows)}.\n",
         "| completo → barato | ideas |", "|---|---|"]
    for (a_, b_), n in sorted(dec.items()):
        L.append(f"| {a_} → {b_} | {n} |")
    L += ["", "## Ideas que cambian de lado\n", "| Ask | completo | barato | mejor (completo) | mejor (barato) |", "|---|---|---|---|---|"]
    titles = dict(conn.execute("SELECT id, title FROM items"))
    for a, fb, cb, fi, ci in to_gap + to_match:
        L.append(f"| [{asks[a]['title'][:60]}]({asks[a]['hn_url']}) | {fb:.2f} | {cb:.2f} | {titles.get(fi, fi)[:40]} | {titles.get(ci, ci)[:40]} |")
    text = "\n".join(L) + "\n"
    COMPARE_REPORT.write_text(text)
    return text


def gap_cases() -> list[dict]:
    v2 = load_v2()
    asks = askhn.load_asks()
    reals = [d for d in v2.values() if d.get("ok") and d["pedido_real"]]
    reals.sort(key=lambda d: (-asks[d["id"]]["points"], d["id"]))
    return [{"id": f"gap-{d['id']}", "ask_id": d["id"], "query_core": d["pedido_resumido"]} for d in reals]


def run(conn, rerun_first: int = 40) -> dict:
    """K=200 para todos los pedidos reales; después K=1000 para los que quedaron como hueco, empezando por los
    `rerun_first` primeros del orden de la lista (menor P(núcleo) máxima primero) y siguiendo mientras haya saldo."""
    from gapfinder.verify import load_done

    cases = gap_cases()
    if balance() < MIN_BALANCE:
        return {"detenido": "saldo bajo antes de empezar", "saldo": round(balance(), 3)}
    prefetch_reformulations(cases, QUERIES)
    masked = askhn._Masked(conn)
    stopped = _process(conn, masked, cases, K_FIRST, QUERIES, CANDIDATES, VERDICTS)
    if not stopped:
        ver, cand = load_done(VERDICTS), askhn._load(CANDIDATES, {})
        gaps = [c for c in cases if c["id"] in cand and _best(c["id"], cand[c["id"]][:K_FIRST], ver)[0] < HUECO]
        gaps.sort(key=lambda c: _best(c["id"], cand[c["id"]][:K_FIRST], ver)[0])
        log.info("gaps: %d huecos con K=%d; re-corro con K=%d (primero %d)", len(gaps), K_FIRST, K_FULL, rerun_first)
        stopped = _process(conn, masked, gaps[:rerun_first], K_FULL, QUERIES, CANDIDATES, VERDICTS)
        if not stopped:
            stopped = _process(conn, masked, gaps[rerun_first:], K_FULL, QUERIES, CANDIDATES, VERDICTS)
    return {"detenido": stopped, "saldo": round(balance(), 3)}


# --- 4. lista final -------------------------------------------------------------------------------------


def no_software(title: str, pedido: str) -> str | None:
    """Motivo por el que el pedido no es una herramienta de software (hardware, contenido, encuesta, "¿se puede…?"),
    o None. Hardware y contenido miran solo el sintagma nominal del pedido, para que "an app that recommends books"
    o "a service that sends SMS or phone calls" sigan siendo software; la encuesta y el "¿se puede…?" salen del
    título del Ask (y de un pedido que empieza con "a method/way")."""
    pedido = re.sub(r"[‐-―]", "-", pedido.lower())   # guiones unicode del LLM ("e‑ink") -> "-"
    sin_parentesis = re.sub(r"\([^)]*\)", "", pedido)
    head = re.split(_HEAD_STOP, f" {sin_parentesis} ", maxsplit=1)[0]
    if re.search(r"^(a|an)\s+(method|way)\b", pedido):
        return "se puede"
    for motivo, pat in _NO_SOFTWARE_HEAD.items():
        if re.search(pat, head):
            return motivo
    title = re.sub(r"^ask hn:\s*", "", title.lower())
    for motivo, pat in _NO_SOFTWARE_TITLE.items():
        if re.search(pat, title):
            return motivo
    return None


def tier(best: float, etiqueta: str, motivo: str | None = None) -> str:
    """Nivel del pedido. En orden: match (>= HUECO, ya construido: no es hueco); no es software; descartado (los
    comentarios dicen que existe); hueco fuerte (< FUERTE y etiqueta n o p); el resto (incluido "?" < FUERTE) es
    zona gris."""
    if best >= HUECO:
        return "match"
    if motivo:
        return "no_software"
    if etiqueta == "e":
        return "descartado"
    if best < FUERTE and etiqueta in ("n", "p"):
        return "fuerte"
    return "gris"


def report(conn, top: int = 5) -> str:
    from gapfinder.verify import load_done

    asks, v2 = askhn.load_asks(), load_v2()
    ver, cand = load_done(VERDICTS), askhn._load(CANDIDATES, {})
    meta = {i: (t, u, c) for i, t, u, c in conn.execute("SELECT id, title, url, created_at FROM items")}
    cases = gap_cases()
    rows = []
    for c in cases:
        cid = c["id"]
        if cid not in cand:
            continue
        k_done = K_FULL if all((cid, i) in ver for i in cand[cid][:K_FULL]) else K_FIRST if all(
            (cid, i) in ver for i in cand[cid][:K_FIRST]) else 0
        if not k_done:
            continue
        best, scored = _best(cid, cand[cid][:k_done], ver)
        a, d = asks[c["ask_id"]], v2[c["ask_id"]]
        motivo = no_software(a["title"], d["pedido_resumido"])
        rows.append({**c, "k": k_done, "best": best, "scored": scored, "v2": d, "ask": a, "motivo": motivo,
                     "tier": tier(best, d["etiqueta"], motivo)})
    by = {t: sorted((r for r in rows if r["tier"] == t), key=lambda r: r["best"]) for t in TIERS}
    pending = sum(r["k"] == K_FIRST and r["best"] < HUECO for r in rows)
    lab = {t: Counter(r["v2"]["etiqueta"] for r in by[t]) for t in TIERS}
    motivos = Counter(r["motivo"] for r in by["no_software"])
    cost_v2 = sum(d.get("cost_usd", 0) for d in v2.values())
    cost_q = sum(q.get("cost_usd", 0) for q in askhn._load(QUERIES, {}).values())
    cost_j = sum(v.cost_usd or 0 for v in ver.values())
    L = ["# Candidatos a hueco: pedidos de Ask HN sin match fuerte en el corpus\n",
         f"Pedidos reales (extracción automática v2) corridos contra el corpus anterior a la fecha de cada Ask, con Jev sobre "
         f"el top-{K_FIRST} y, si no hubo match, el top-{K_FULL}. Cada pedido cae en un nivel, en este orden:\n",
         f"1. **match**: algún candidato con P(núcleo) >= {HUECO} (ya construido; no se lista).",
         "2. **no es software**: el pedido es hardware, contenido (libro, curso, guía, plantilla, licencia, lista), una "
         "encuesta (\"what tools do you use\", \"how do you…\") o un \"¿se puede…?\". Heurístico sobre el título del Ask y "
         "el sintagma nominal del pedido (`gaps.no_software`).",
         "3. **descartado**: los comentarios dicen que existe (etiqueta e).",
         f"4. **hueco fuerte**: mejor P(núcleo) < {FUERTE} y etiqueta n o p.",
         f"5. **zona gris**: el resto (mejor P(núcleo) {FUERTE}–{HUECO}).\n",
         f"- Pedidos reales: {len(cases)}; verificados: {len(rows)}"
         + (f"; sin re-correr con top-{K_FULL}: {pending}" if pending else "") + ".",
         "- Por nivel: " + ", ".join(f"{TIERS[t]} {len(by[t])}" for t in TIERS) + ".",
         "- No es software, por motivo: " + ", ".join(f"{m} {n}" for m, n in motivos.most_common()) + ".",
         f"- **Huecos fuertes: {len(by['fuerte'])}** (no existe {lab['fuerte'].get('n', 0)}, parcial {lab['fuerte'].get('p', 0)}); "
         f"zona gris: {len(by['gris'])} (" + ", ".join(f"{LABELS[k]} {n}" for k, n in sorted(lab["gris"].items())) + ").",
         f"- Costo: extracción v2 ${cost_v2:.3f}, reformulaciones ${cost_q:.3f}, Jev ${cost_j:.3f} (OpenRouter, usage.cost).\n",
         "Caveats: los veredictos son los cacheados (no se re-verificó nada); las reformulaciones son de gpt-oss y la primera "
         f"pasada usa top-{K_FIRST} (ver `{COMPARE_REPORT}`). Un hueco es \"sin equivalente en este corpus (Show HN + GitHub "
         ">= 100★) antes del Ask\", no prueba que no exista; el pedido_resumido lo escribe un LLM. El umbral "
         f"{FUERTE} no está calibrado con revisión humana.\n"]

    def head(r: dict) -> str:
        a, d = r["ask"], r["v2"]
        return (f"**{d['pedido_resumido']}**  \n"
                f"   [{a['title'][:110]}]({a['hn_url']}) · {a['created_at'][:10]} · {a['points']} pts · {a['num_comments']} comentarios · "
                f"etiqueta **{d['etiqueta']}** ({LABELS[d['etiqueta']]}) · mejor P(núcleo) {r['best']:.2f} (top-{r['k']})")

    def cand_line(r: dict, i: str) -> str:
        t, u, c = meta.get(i, ("?", "", "?"))
        return f"{ver[(r['id'], i)].core:.2f} · {t[:80]} · {c[:10]} · {u}"

    def block(t: str, n_cands: int) -> None:
        L.append(f"## {TIERS[t].capitalize()} ({len(by[t])})\n")
        for n, r in enumerate(by[t], 1):
            L.append(f"{n}. {head(r)}  \n   _{r['v2']['justificacion']}_")
            L.extend(f"   - {cand_line(r, i)}" for i in r["scored"][:n_cands])
            L.append("")

    def cell(s: str, n: int) -> str:
        return s[:n].replace("|", "\\|")

    def compact(t: str, col: str, value) -> None:
        L.extend([f"## {TIERS[t].capitalize()} ({len(by[t])})\n",
                  f"| pedido | Ask | etiqueta | mejor | {col} |", "|---|---|---|---|---|"])
        for r in by[t]:
            a = r["ask"]
            L.append(f"| {cell(r['v2']['pedido_resumido'], 90)} | [{cell(a['title'], 60)}]({a['hn_url']}) | "
                     f"{r['v2']['etiqueta']} | {r['best']:.2f} | {cell(value(r), 50)} |")
        L.append("")

    def best_cand(r: dict) -> str:
        return meta.get(r["scored"][0], ("?",))[0] if r["scored"] else "–"

    block("fuerte", top)
    block("gris", 3)
    compact("descartado", "mejor candidato", best_cand)
    compact("no_software", "motivo", lambda r: r["motivo"])
    text = "\n".join(L) + "\n"
    REPORT.write_text(text)
    return text
