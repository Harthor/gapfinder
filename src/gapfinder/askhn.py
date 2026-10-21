"""Fase 4: lado de demanda con Ask HN del tipo "¿hay una herramienta para…?".

1. `collect`: búsquedas en HN Algolia (tags=ask_hn) con varias consultas; filtros baratos (puntos,
   comentarios, palabras de software); comentarios por la API de items de Algolia. Todo cacheado en
   data/cache/askhn/ (una request por consulta/página y por Ask).
2. `extract`: Claude (el modelo más barato que rinda) extrae si es un pedido de herramienta, la idea
   neutral (formato query_core), las herramientas sugeridas en los comentarios, señales de "no existe" y
   una etiqueta aproximada por comentarios. Las herramientas se mapean a items del corpus por URL.
3. `select` / `retrieve` / `verify`: hasta 40 Asks balanceados por etiqueta; consultas llm5 (prompt v2),
   top-1000 con MiniLM sobre el corpus anterior a la fecha de cada Ask (mismo enmascarado que el holdout)
   y Jev vía OpenRouter con tope de gasto.
4. `report`: data/eval/phase4_askhn.md.

Archivos en data/askhn/: asks.json, extractions.json, selected.json, llm_queries.json, candidates.json.
Veredictos: data/phase3/verdicts_jev_askhn.jsonl.
"""

from __future__ import annotations

import json
from pathlib import Path

DIR = Path("data/askhn")
CACHE = Path("data/cache/askhn")
ASKS = DIR / "asks.json"                 # en el repo: metadatos de cada Ask, sin el texto del OP
ASKS_TEXT = CACHE / "asks_text.json"     # local (no va al repo: es contenido de HN): {id: texto del OP}
EXTRACTIONS = DIR / "extractions.json"
SELECTED = DIR / "selected.json"
QUERIES = DIR / "llm_queries.json"
CANDIDATES = DIR / "candidates.json"
VERDICTS = "jev_askhn"


def case_id(ask_id: str) -> str:
    return f"ask-{ask_id}"


def _load(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def load_asks() -> dict[str, dict]:
    """Metadatos de asks.json más el texto del OP de la copia local (ASKS_TEXT), si existe."""
    text = _load(ASKS_TEXT, {})
    return {a["id"]: {**a, "text": text[a["id"]]} if a["id"] in text else a for a in _load(ASKS, {}).get("asks", [])}


def _op_text(ask: dict) -> str:
    if "text" not in ask:
        raise RuntimeError(f"falta el texto del OP del Ask {ask['id']}: está en {ASKS_TEXT} (local); "
                           "regeneralo con `gapfinder askhn collect`")
    return ask["text"]


def split_asks(rows: list[dict]) -> tuple[list[dict], dict[str, str]]:
    """(filas para el repo, sin "text"; {id: texto del OP} para la copia local)."""
    return [{k: v for k, v in r.items() if k != "text"} for r in rows], {r["id"]: r.get("text", "") for r in rows}


def load_extractions() -> dict[str, dict]:
    return _load(EXTRACTIONS, {})


def load_selected() -> list[str]:
    return _load(SELECTED, [])


# --- 1. recolección (sin LLM) ---------------------------------------------------------------------------

import hashlib  # noqa: E402
import html  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

log = logging.getLogger(__name__)

SEARCH = "https://hn.algolia.com/api/v1/search"
ITEM = "https://hn.algolia.com/api/v1/items/{}"
# Consultas de búsqueda (Algolia busca palabras, no la frase exacta; el filtro de título de abajo exige el pedido).
SEARCH_QUERIES = [
    "is there a tool", "is there an app", "is there a library", "is there a service", "is there software",
    "is there anything", "does anything exist", "does something exist", "looking for a tool",
    "looking for an app", "looking for software", "what tool do you use", "how do you", "I wish there was",
    "recommend a tool", "any tool for",
]
MIN_POINTS = 5
MIN_COMMENTS = 3
MIN_DATE = "2015-01-01"    # antes, el corpus enmascarado a la fecha del Ask es demasiado chico (< ~100 mil items)
PAGES = 10                 # Algolia devuelve como máximo 1000 resultados por consulta (10 páginas de 100)
# El título tiene que ser un pedido (no una encuesta de opinión ni "¿cómo hacen X en su empresa?").
REQUEST_RE = re.compile(
    r"\b(is there (a|an|any|some)\b|are there (any|good)\b|does (anything|something|such|any\w*)\b.*\bexists?\b|"
    r"looking for (a|an|some)\b|anyone know (of )?(a|an|any)\b|any (good )?(tool|app|library|service|software|way)s?\b|"
    r"what (tool|app|software|service|library)s? (do|would|should|can)\b|how do you\b|i wish there (was|were)\b|"
    r"recommend (a|an|me a)\b|need (a|an) (tool|app|library|service)\b)", re.IGNORECASE)
HOW_DO_YOU_RE = re.compile(r"how do you", re.IGNORECASE)
# Que sea software: palabras de herramienta en título o texto.
SOFTWARE_RE = re.compile(
    r"\b(tool|tools|app|apps|application|library|libraries|lib|software|service|saas|extension|plugin|add-?on|"
    r"program|script|cli|api|framework|utility|package|website|web ?site|platform|editor|ide|bot|dashboard|"
    r"open[- ]source|self[- ]hosted|github|android|ios|macos|linux|windows|browser)\b", re.IGNORECASE)
# Fuera: empleo, carrera, opinión general (no piden una herramienta).
OFF_TOPIC_RE = re.compile(r"\b(hiring|job|jobs|career|salary|interview|who is hiring|freelanc\w*|cofounder|co-founder)\b",
                          re.IGNORECASE)


def _clean(text: str | None) -> str:
    text = re.sub(r"<p>", "\n\n", text or "")
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def _cached_get(client, url: str, params: dict | None, path: Path) -> dict:
    from gapfinder.http import get_json

    if path.exists():
        return json.loads(path.read_text())
    data, _ = get_json(client, url, params)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return data


def _search(client, query: str) -> list[dict]:
    hits = []
    for page in range(PAGES):
        params = {"query": query, "tags": "ask_hn", "hitsPerPage": 100, "page": page,
                  "numericFilters": f"points>={MIN_POINTS},num_comments>={MIN_COMMENTS}"}
        key = hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16]
        data = _cached_get(client, SEARCH, params, CACHE / "search" / f"{key}.json")
        hits += data["hits"]
        if page + 1 >= data.get("nbPages", 0):
            break
    return hits


def _flatten(node: dict, depth: int = 0) -> list[dict]:
    out = []
    for ch in node.get("children") or []:
        if ch.get("type") == "comment" and ch.get("text"):
            out.append({"id": str(ch["id"]), "author": ch.get("author"), "depth": depth, "text": _clean(ch["text"])})
        out += _flatten(ch, depth + 1)
    return out


def comments(ask_id: str) -> list[dict]:
    """Comentarios del Ask (cacheados), en el orden del árbol, con profundidad (0 = respuesta directa)."""
    import httpx

    path = CACHE / "items" / f"{ask_id}.json"
    with httpx.Client(timeout=30) as client:
        tree = _cached_get(client, ITEM.format(ask_id), None, path)
    return _flatten(tree)


def collect() -> dict:
    """Busca, filtra sin LLM y baja los comentarios de los que pasan. Guarda asks.json con el embudo y lo
    que aportó cada consulta (hits brutos, nuevos únicos, y cuántos de los que pasan el filtro trajo primero)."""
    import httpx

    seen: dict[str, dict] = {}
    per_query = {}
    with httpx.Client(timeout=30) as client:
        for q in SEARCH_QUERIES:
            hits = _search(client, q)
            new = 0
            for h in hits:
                if h["objectID"] not in seen:
                    seen[h["objectID"]] = {**h, "_query": q}
                    new += 1
            per_query[q] = {"hits": len(hits), "nuevos": new}
            log.info("askhn: %-22s %4d hits, %4d nuevos", q, len(hits), new)
    funnel = {"bajados_unicos": len(seen)}
    rows = []
    drop = {"antes_de_" + MIN_DATE: 0, "titulo_no_es_pedido": 0, "empleo_o_carrera": 0, "no_software": 0,
            "how_do_you_sin_software_en_titulo": 0}
    for aid, h in seen.items():
        title, text = h.get("title") or "", _clean(h.get("story_text"))
        if h["created_at"] < MIN_DATE:
            drop["antes_de_" + MIN_DATE] += 1
        elif not REQUEST_RE.search(title):
            drop["titulo_no_es_pedido"] += 1
        elif OFF_TOPIC_RE.search(title):
            drop["empleo_o_carrera"] += 1
        elif not SOFTWARE_RE.search(f"{title} {text}"):
            drop["no_software"] += 1
        elif all(HOW_DO_YOU_RE.fullmatch(m.group(0)) for m in REQUEST_RE.finditer(title)) and not SOFTWARE_RE.search(title):
            drop["how_do_you_sin_software_en_titulo"] += 1   # "How do you deal with…": consejo, no herramienta
        else:
            rows.append({"id": aid, "title": title, "text": text, "created_at": h["created_at"], "points": h["points"],
                         "num_comments": h["num_comments"], "hn_url": f"https://news.ycombinator.com/item?id={aid}",
                         "query": h["_query"]})
    funnel |= {"descartados": drop, "filtrados": len(rows)}
    for q in per_query:
        per_query[q]["pasan_filtro"] = sum(r["query"] == q for r in rows)
    with ThreadPoolExecutor(8) as pool:   # comentarios: una request por Ask, cacheada
        for r, cs in zip(rows, pool.map(lambda r: comments(r["id"]), rows)):
            r["comments_downloaded"] = len(cs)
    rows.sort(key=lambda r: r["id"])
    DIR.mkdir(parents=True, exist_ok=True)
    out = {"filters": {"min_points": MIN_POINTS, "min_comments": MIN_COMMENTS, "min_date": MIN_DATE,
                       "request_title_regex": REQUEST_RE.pattern, "software_regex": SOFTWARE_RE.pattern,
                       "off_topic_regex": OFF_TOPIC_RE.pattern},
           "queries": per_query, "funnel": funnel, "asks": split_asks(rows)[0]}
    ASKS.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    CACHE.mkdir(parents=True, exist_ok=True)
    ASKS_TEXT.write_text(json.dumps(split_asks(rows)[1], ensure_ascii=False))
    return {"queries": per_query, "funnel": funnel}


# --- 2. extracción con LLM barato (OpenRouter) ----------------------------------------------------------

EXTRACT_MODEL = "openai/gpt-oss-120b"   # $0.037/$0.17 por Mtok; elegido por precio, validado en 10 casos
# Con el schema estricto, gpt-oss degeneró en 36/397 respuestas ("....", nombres vacíos); se reintenta y el
# tercer intento usa un modelo sin razonamiento, igual de barato.
FALLBACK_MODEL = "qwen/qwen3-30b-a3b-instruct-2507"
DISCARDED = DIR / "extractions_descartadas.json"   # salidas inválidas reemplazadas (se conserva su costo)
OPENROUTER_CHAT = "https://openrouter.ai/api/v1/chat/completions"
OP_CHARS, COMMENT_CHARS, COMMENTS_CHARS = 2500, 500, 14000
# Tope total de la Fase 4, todos los proveedores: $0.90 al principio; con la recarga de OpenRouter ($5) se subió a
# $2.40 para procesar las 40 ideas (lo gastado + ~$0.051 por idea medido: Claude $0.017 + Jev $0.034).
BUDGET = 2.40

EXTRACT_SYSTEM = """You read an "Ask HN" thread from Hacker News and extract structured data. Output English.

es_pedido_de_herramienta: true only if the original poster (OP) is asking whether a software tool, app, \
library, service or product exists (or asking for one) to solve a specific need. False for opinion polls, \
career/business advice, "how does your company do X" surveys, hardware shopping, or requests too vague to \
describe as a tool.

idea: the central need of the OP in 1-2 plain English sentences, as someone searching for a tool that \
fills it would state it. Use the standard category or technical terms practitioners use (e.g. "feature \
flag service", "reverse proxy"), but NEVER name existing products, companies, open-source projects, \
libraries or services, even ones mentioned in the thread. Write it even if es_pedido_de_herramienta is false.

herramientas_sugeridas: every concrete product/project the COMMENTERS suggest as an answer to the OP's \
need (not ones the OP already rejected as inadequate, not ones only mentioned in passing). For each: \
nombre (the name as written), url (copied from the comment if one is given, else empty string; never \
invent a URL), relacion: "equivalente" if the comment presents it as doing what the OP asks, "parcial" \
if it covers only part of the need, is a workaround, or the commenter hedges.

senales_no_existe: short verbatim-ish quotes (max 20 words each) where the OP or commenters say nothing \
like this exists, they searched and found nothing, they built their own because nothing existed, or \
"I would pay for this". Empty list if none.

etiqueta_comentarios: "existe" if at least one suggested tool is presented as an equivalent and nobody \
credibly refutes it; "parcial" if only partial tools/workarounds were suggested; "no_existe" if the \
thread says nothing exists (or people built their own) and no equivalent is suggested; "incierto" otherwise."""

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "es_pedido_de_herramienta": {"type": "boolean"},
        "idea": {"type": "string"},
        "herramientas_sugeridas": {"type": "array", "items": {
            "type": "object",
            "properties": {"nombre": {"type": "string"}, "url": {"type": "string"},
                           "relacion": {"type": "string", "enum": ["equivalente", "parcial"]}},
            "required": ["nombre", "url", "relacion"], "additionalProperties": False}},
        "senales_no_existe": {"type": "array", "items": {"type": "string"}},
        "etiqueta_comentarios": {"type": "string", "enum": ["existe", "parcial", "no_existe", "incierto"]},
    },
    "required": ["es_pedido_de_herramienta", "idea", "herramientas_sugeridas", "senales_no_existe",
                 "etiqueta_comentarios"],
    "additionalProperties": False,
}


def thread_text(ask: dict) -> str:
    """Título + texto del OP + comentarios (primero las respuestas directas y sus primeras réplicas, en el
    orden del hilo), recortados para que la entrada quede chica."""
    cs = [c for c in comments(ask["id"]) if c["depth"] <= 1]
    lines, total = [], 0
    for c in cs:
        t = re.sub(r"\s+", " ", c["text"])[:COMMENT_CHARS]
        line = f"[{'answer' if c['depth'] == 0 else 'reply'} by {c['author']}] {t}"
        if total + len(line) > COMMENTS_CHARS:
            break
        lines.append(line)
        total += len(line)
    return (f"Title: {ask['title']}\nPosted: {ask['created_at'][:10]}\n\nOP text:\n{_op_text(ask)[:OP_CHARS] or '(none)'}\n\n"
            f"Comments ({len(lines)} of {len(cs)} shown):\n" + "\n".join(lines))


class FatalAPIError(RuntimeError):
    pass


def _openrouter(client, model: str, system: str, user: str, schema: dict, name: str,
                max_tokens: int = 4000) -> tuple[dict, dict]:
    """max_tokens: tope de salida; gpt-oss a veces degenera y genera basura hasta el timeout."""
    import os
    import time

    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "response_format": {"type": "json_schema", "json_schema": {"name": name, "strict": True, "schema": schema}},
            "provider": {"require_parameters": True}, "usage": {"include": True}, "max_tokens": max_tokens}
    if "gpt-oss" in model:   # solo los modelos con razonamiento aceptan el parámetro
        body["reasoning"] = {"effort": "low"}
    headers = {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}
    for attempt in range(4):
        r = client.post(OPENROUTER_CHAT, json=body, headers=headers)
        if r.status_code in (401, 402, 403):
            raise FatalAPIError(f"OpenRouter {r.status_code}: {r.text[:300]}")
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 * 2 ** attempt)
            continue
        r.raise_for_status()
        d = r.json()
        try:
            return json.loads(d["choices"][0]["message"]["content"]), d.get("usage", {})
        except (KeyError, TypeError, json.JSONDecodeError):
            log.warning("respuesta no parseable (intento %d): %s", attempt + 1, str(d)[:200])
    raise RuntimeError("agotados los reintentos")


def _junk(x: str) -> bool:
    return len(re.findall(r"[A-Za-z0-9]{2,}", x or "")) == 0


def valid(e: dict) -> bool:
    """Salida degenerada si la idea tiene menos de 5 palabras o si quedan señales / nombres vacíos o hechos de
    puntos (ver `sanitize`, que saca esas entradas sueltas cuando la idea está bien)."""
    return (len(re.findall(r"[A-Za-z]{2,}", e.get("idea", ""))) >= 5
            and not any(_junk(x) for x in e.get("senales_no_existe", []))
            and not any(_junk(t.get("nombre", "")) for t in e.get("herramientas_sugeridas", [])))


def sanitize(e: dict) -> dict:
    """Si la idea está bien, saca las señales y herramientas basura sueltas (marcando que se limpió)."""
    if len(re.findall(r"[A-Za-z]{2,}", e.get("idea", ""))) < 5:
        return e
    s = [x for x in e["senales_no_existe"] if not _junk(x)]
    t = [x for x in e["herramientas_sugeridas"] if not _junk(x.get("nombre", ""))]
    if len(s) < len(e["senales_no_existe"]) or len(t) < len(e["herramientas_sugeridas"]):
        e = {**e, "senales_no_existe": s, "herramientas_sugeridas": t, "limpiada": True}
    return e


def _archive_cost(aid: str, cost: float, entry: dict | None = None) -> None:
    arch = _load(DISCARDED, [])
    arch.append({"ask_id": aid, "cost_usd": cost, **({"entry": entry} if entry else {})})
    DISCARDED.write_text(json.dumps(arch, indent=1, ensure_ascii=False))


def discard_invalid() -> list[str]:
    """Saca de extractions.json las salidas inválidas (quedan en DISCARDED con su costo) para re-extraerlas."""
    done = load_extractions()
    bad = [a for a, e in done.items() if not valid(e)]
    for a in bad:
        _archive_cost(a, done[a].get("cost_usd", 0), done.pop(a))
    EXTRACTIONS.write_text(json.dumps(done, indent=1, ensure_ascii=False))
    return bad


def discard_idea(aid: str) -> int:
    """Saca una idea ya procesada (p. ej. con extracción inválida): sus veredictos pasan a
    verdicts_jev_askhn_descartado.jsonl, sus consultas a llm_queries_descartadas.json y sale de candidates.
    Nada se borra y su costo sigue contando en spent()."""
    from gapfinder.verify import OUT_DIR

    cid = case_id(aid)
    src, dst = OUT_DIR / f"verdicts_{VERDICTS}.jsonl", OUT_DIR / f"verdicts_{VERDICTS}_descartado.jsonl"
    keep, moved = [], []
    for line in src.read_text().splitlines() if src.exists() else []:
        (moved if json.loads(line)["case_id"] == cid else keep).append(line)
    with dst.open("a") as f:
        f.writelines(x + "\n" for x in moved)
    src.write_text("".join(x + "\n" for x in keep))
    q, arch = _load(QUERIES, {}), _load(DIR / "llm_queries_descartadas.json", {})
    if cid in q:
        arch[cid] = q.pop(cid)
        QUERIES.write_text(json.dumps(q, indent=1, ensure_ascii=False))
        (DIR / "llm_queries_descartadas.json").write_text(json.dumps(arch, indent=1, ensure_ascii=False))
    cand = _load(CANDIDATES, {})
    if cand.pop(cid, None) is not None:
        CANDIDATES.write_text(json.dumps(cand))
    return len(moved)


def spent() -> dict:
    """Gasto acumulado de la Fase 4 por proveedor (USD), de lo guardado en disco."""
    from gapfinder.verify import load_done

    ext = load_extractions()
    q = _load(QUERIES, {}) | {f"descartada-{k}": v for k, v in _load(DIR / "llm_queries_descartadas.json", {}).items()}
    return {"openrouter_extraccion": sum(e.get("cost_usd", 0) for e in ext.values())
            + sum(d["cost_usd"] for d in _load(DISCARDED, [])),
            "anthropic_consultas": sum((v["usage"]["input_tokens"] * 5 + v["usage"]["output_tokens"] * 25) / 1e6
                                       for v in q.values() if "usage" in v and v.get("via") != "openrouter"),
            "openrouter_consultas": sum(v.get("cost_usd", 0) for v in q.values() if v.get("via") == "openrouter"),
            "openrouter_jev": sum(v.cost_usd or 0 for name in (VERDICTS, VERDICTS + "_descartado")
                                  for v in load_done(name).values())}


_INDEX = None


def _corpus_index(conn):
    from gapfinder.real_cases import CorpusIndex

    global _INDEX
    if _INDEX is None:
        targeted = {r[0] for r in conn.execute("SELECT item_id FROM targeted")}
        _INDEX = CorpusIndex(conn, exclude=targeted)
        from wordfreq import zipf_frequency
        names: dict[str, list] = {}
        for (iid, stars) in conn.execute("SELECT id, stars FROM items WHERE source = 'github'"):
            if iid not in targeted:
                owner, repo = iid.removeprefix("github:").lower().split("/", 1)
                if repo in owner:   # sphinx-doc/sphinx, mkdocs/mkdocs: el dueño es el proyecto (no un fork o wrapper)
                    names.setdefault(repo, []).append((stars or 0, iid))
        _INDEX.repo_by_name = {n: max(v)[1] for n, v in names.items() if len(n) >= 4 and zipf_frequency(n, "en") < 3.5}
    return _INDEX


STORE_RE = re.compile(r"(itunes|apps)\.apple\.com|play\.google\.com|chrome\.google\.com|chromewebstore\.google\.com|"
                      r"addons\.mozilla\.org|microsoft\.com/store|apps\.microsoft\.com")


def remap(conn) -> int:
    """Vuelve a mapear las herramientas ya extraídas (sin volver a llamar al LLM)."""
    done = load_extractions()
    for e in done.values():
        e["herramientas_sugeridas"] = [map_tool(conn, {k: t[k] for k in ("nombre", "url", "relacion")})
                                       for t in e["herramientas_sugeridas"]]
    EXTRACTIONS.write_text(json.dumps(done, indent=1, ensure_ascii=False))
    return len(done)


def map_tool(conn, tool: dict) -> dict:
    """Herramienta sugerida -> items del corpus. Por URL (CorpusIndex: repo, URL exacta, dominio validado por
    nombre); si no hay URL, por nombre exacto de un repo (solo nombres raros en inglés: heurístico)."""
    from gapfinder import phase3

    ix = _corpus_index(conn)
    item, how = (None, "sin URL")
    if tool.get("url") and STORE_RE.search(tool["url"]):
        how = "URL de tienda de apps"   # el dominio es de la tienda, no del producto
    elif tool.get("url"):
        item, how = ix.lookup(tool["url"], tool.get("nombre"))
    if not item:
        n = re.sub(r"[^a-z0-9.+-]", "", (tool.get("nombre") or "").lower().replace(" ", "-"))
        if n in ix.repo_by_name:
            item, how = ix.repo_by_name[n], "nombre de repo (heurístico)"
    ids = sorted(phase3.twins(conn, [item])) if item else []
    created = dict(conn.execute(f"SELECT id, created_at FROM items WHERE id IN ({','.join('?' * len(ids))})", ids)) if ids else {}
    return {**tool, "corpus_ids": ids, "mapeo": how, "corpus_created": created}


def extract(conn, limit: int | None = None, workers: int = 16, show=print) -> dict:
    """Extrae los Asks filtrados que faltan (reanudable). Guarda cada tanda; frena ante 401/402/403 o si
    el gasto acumulado de la sesión se acerca al tope."""
    import httpx

    asks = list(load_asks().values())
    done = load_extractions()
    todo = [a for a in asks if a["id"] not in done][:limit]
    log.info("extracción: %d por hacer (%d hechos), modelo %s", len(todo), len(done), EXTRACT_MODEL)

    def one(a: dict):
        """Hasta 3 intentos; el tercero con el modelo de respaldo. Las salidas inválidas (degeneradas) no se
        guardan, pero su costo sí se acumula."""
        cost, err = 0.0, None
        for attempt, model in enumerate((EXTRACT_MODEL, EXTRACT_MODEL, FALLBACK_MODEL)):
            try:
                data, usage = _openrouter(client, model, EXTRACT_SYSTEM, thread_text(a), EXTRACT_SCHEMA, "ask_extraction")
            except FatalAPIError:
                raise
            except Exception as e:  # noqa: BLE001
                err = e
                continue
            cost += usage.get("cost", 0)
            if attempt == 2:   # último intento: rescatar lo que esté bien
                data = sanitize(data)
            if valid(data):
                return a, data, {**usage, "cost": cost, "model": model, "attempts": attempt + 1}, None
            err = ValueError(f"salida inválida (intento {attempt + 1}, {model}): {data.get('idea', '')[:60]!r}")
            log.warning("extracción %s: %s", a["id"], err)
        _archive_cost(a["id"], cost)
        return a, None, None, err

    from concurrent.futures import as_completed

    with httpx.Client(timeout=90) as client, ThreadPoolExecutor(workers) as pool:
        # sin barrera por tanda: se procesa a medida que llegan respuestas y se guarda cada 10
        futures = [pool.submit(one, a) for a in todo]
        for n, fut in enumerate(as_completed(futures), 1):
            a, data, usage, err = fut.result()
            if err:
                log.error("extracción %s: %s", a["id"], err)
            else:
                data["herramientas_sugeridas"] = [map_tool(conn, t) for t in data["herramientas_sugeridas"]]
                done[a["id"]] = {**data, "model": usage["model"], "attempts": usage["attempts"], "cost_usd": usage["cost"],
                                 "tokens": [usage.get("prompt_tokens"), usage.get("completion_tokens")]}
            if n % 10 == 0 or n == len(todo):
                EXTRACTIONS.write_text(json.dumps(done, indent=1, ensure_ascii=False))
                log.info("extracción: %d/%d, gasto extracción $%.4f", len(done), len(asks), spent()["openrouter_extraccion"])
                if sum(spent().values()) > BUDGET * 0.95:
                    log.warning("extracción: cerca del tope de $%.2f; me detengo", BUDGET)
                    for f in futures:
                        f.cancel()
                    break
    if limit:   # validación: mostrar en el log lo extraído
        asks_by = load_asks()
        for a in todo:
            if a["id"] in done:
                show(format_extraction(asks_by[a["id"]], done[a["id"]]))
    return {"hechos": len(done), "asks": len(asks), "gasto": spent()}


def format_extraction(a: dict, e: dict) -> str:
    tools = "\n".join(f"      - {t['nombre']} [{t['relacion']}] {t['url'] or ''} -> {t['corpus_ids'][:2] or '—'} ({t['mapeo']})"
                      for t in e["herramientas_sugeridas"]) or "      (ninguna)"
    return (f"\n=== {a['id']} {a['created_at'][:10]} {a['points']}pts {a['num_comments']}c: {a['title']}\n"
            f"   pedido={e['es_pedido_de_herramienta']} etiqueta={e['etiqueta_comentarios']} costo=${e['cost_usd']:.5f}\n"
            f"   idea: {e['idea']}\n   sugeridas:\n{tools}\n   no existe: {e['senales_no_existe']}")


# --- 3. selección, consultas, retrieval enmascarado por fecha y Jev --------------------------------------

MAX_IDEAS = 40
K = 1000
CLAUDE_PER_IDEA = 0.02         # estimado conservador (medido: $0.016) (consultas llm5, prompt v2, claude-opus-5) antes de pedirlas
JEV_PER_PAIR = 0.0000345       # medido en el holdout ($1.171 / 35.000 pares), con margen


def pre_ask_tools(e: dict, ask: dict, relation: str | None = None) -> list[dict]:
    """Herramientas sugeridas con algún item del corpus creado antes del Ask (las que el sistema podía encontrar)."""
    return [t for t in e["herramientas_sugeridas"] if (relation is None or t["relacion"] == relation)
            and any(c < ask["created_at"] for c in t.get("corpus_created", {}).values())]


def group_of(e: dict, ask: dict) -> str:
    lab = e["etiqueta_comentarios"]
    if lab == "existe":
        return "existe_con_item_en_corpus" if pre_ask_tools(e, ask, "equivalente") else "existe_sin_item_en_corpus"
    return lab


# Cupos por grupo (hasta 40) y orden de procesamiento cuando el presupuesto no alcanza: primero no_existe y
# existe-con-item-en-corpus intercalados (así hay de los dos aunque se corte temprano), después el resto.
QUOTAS = {"no_existe": 12, "existe_con_item_en_corpus": 12, "parcial": 8, "existe_sin_item_en_corpus": 4, "incierto": 4}
PRIORITY = [("no_existe", "existe_con_item_en_corpus"), ("parcial", "incierto", "existe_sin_item_en_corpus")]


def select() -> list[str]:
    """Hasta MAX_IDEAS pedidos reales (según el LLM) balanceados por grupo; dentro de cada grupo, los de más
    puntos primero (más demanda). Si un grupo no llena su cupo, el sobrante se completa con el resto por puntos.
    El orden de la lista es el orden de procesamiento."""
    asks, ext = load_asks(), load_extractions()
    reqs = [a for a, e in ext.items() if e["es_pedido_de_herramienta"] and e["idea"].strip()]
    by_group: dict[str, list[str]] = {}
    for a in sorted(reqs, key=lambda a: -asks[a]["points"]):
        by_group.setdefault(group_of(ext[a], asks[a]), []).append(a)
    picked = {g: v[:QUOTAS[g]] for g, v in by_group.items()}
    spare = MAX_IDEAS - sum(len(v) for v in picked.values())
    leftovers = sorted((a for g, v in by_group.items() for a in v[QUOTAS[g]:]), key=lambda a: -asks[a]["points"])
    for a in leftovers[:max(0, spare)]:
        picked[group_of(ext[a], asks[a])].append(a)
    order = []
    for tier in PRIORITY:
        lists = [list(picked.get(g, [])) for g in tier]
        while any(lists):
            for lst in lists:
                if lst:
                    order.append(lst.pop(0))
    SELECTED.write_text(json.dumps(order, indent=1))
    return order


def ask_case(aid: str, ext: dict) -> dict:
    """Caso para llm.generate: la idea extraída como necesidad (rama 'need': 4 reformulaciones + 3 palabras
    clave con el prompt v2). query_core = la idea extraída."""
    return {"id": case_id(aid), "kind": "askhn", "title": ext[aid]["idea"]}


CLAUDE_OPENROUTER = "anthropic/claude-opus-5"   # Anthropic sin crédito (oct-2026): mismo modelo vía OpenRouter


def _queries_for(cases: list[dict]) -> dict:
    """Consultas llm5 con el mismo método que los known cases: claude-opus-5, system prompt v2, el mismo texto de
    usuario y el mismo schema que llm.generate (rama 'need'). Se piden vía OpenRouter porque la cuenta de Anthropic
    quedó sin crédito; el costo facturado queda en cost_usd."""
    import httpx

    from gapfinder import llm

    q = _load(QUERIES, {})
    system = llm.PROMPT_VERSIONS[2]
    with httpx.Client(timeout=180) as client:
        for c in cases:
            text, schema = llm._prompt(c)
            data, usage = _openrouter(client, CLAUDE_OPENROUTER, system, text, schema, "queries")
            data = llm._lists(data)
            q[c["id"]] = {**data, "query_core": c["title"], "prompt_version": 2, "model": CLAUDE_OPENROUTER,
                          "via": "openrouter", "cost_usd": usage.get("cost", 0),
                          "usage": {"input_tokens": usage.get("prompt_tokens"), "output_tokens": usage.get("completion_tokens")}}
    QUERIES.write_text(json.dumps(q, indent=1, ensure_ascii=False))
    return q


class _Masked:
    """Matriz MiniLM del índice corpus cargada una vez; cada consulta enmascara lo creado desde la fecha del Ask."""

    def __init__(self, conn):
        import numpy as np

        from gapfinder import embed

        self.ids, mat = embed.load("minilm", "corpus")
        self.mat = mat.astype(np.float32)
        created = dict(conn.execute("SELECT id, created_at FROM items"))
        self.created = np.array([created.get(i, "9999") for i in self.ids])

    def top(self, texts: list[str], before: str, k: int = K) -> tuple[list[str], int]:
        import numpy as np

        from gapfinder import embed, eval2

        allowed = self.created < before
        lists = []
        for v in embed.encode_queries("minilm", texts):
            s = self.mat @ v
            s[~allowed] = -np.inf
            top = np.argpartition(-s, eval2.TOP_K)[:eval2.TOP_K]
            lists.append([self.ids[i] for i in top[np.argsort(-s[top])]])
        return eval2.rrf(lists)[:k], int(allowed.sum())


def run(conn, budget: float = BUDGET) -> dict:
    """Procesa los Asks elegidos en orden: consultas -> top-1000 anterior al Ask -> Jev. Antes de cada idea,
    gasto real acumulado + estimado de la idea <= budget; si no, se detiene (relanzar retoma). Frena ante
    401/402/403 (el verificador levanta RuntimeError)."""
    from gapfinder.verify import OpenRouterJevVerifier, load_done

    order = load_selected() or select()
    asks, ext = load_asks(), load_extractions()
    cand = _load(CANDIDATES, {})
    meta = _load(DIR / "corpus_sizes.json", {})
    masked = None
    verifier = OpenRouterJevVerifier(name=VERDICTS, concurrency=6)
    stopped = None
    for n, aid in enumerate(order, 1):
        cid = case_id(aid)
        done = load_done(VERDICTS)
        q = _load(QUERIES, {})
        if cid in cand and all((cid, i) in done for i in cand[cid]):
            continue
        need_claude = cid not in q
        pending = len([i for i in cand.get(cid, range(K)) if (cid, i) not in done])
        est = (CLAUDE_PER_IDEA if need_claude else 0) + pending * JEV_PER_PAIR
        total = sum(spent().values())
        if total + est > budget:
            stopped = f"presupuesto: gastado ${total:.3f}, la idea {n} ({aid}) costaría ~${est:.3f} y superaría ${budget:.2f}"
            log.warning("askhn: %s; me detengo (relanzar `gapfinder askhn run` retoma)", stopped)
            break
        if need_claude:
            try:
                q = _queries_for([ask_case(aid, ext)])
            except FatalAPIError as e:   # 401/402/403: frenar, no seguir recorriendo
                stopped = f"error de cuenta en las consultas: {e}"
                log.error("askhn: %s; me detengo", stopped)
                break
        if cid not in cand:
            masked = masked or _Masked(conn)
            cand[cid], meta[cid] = masked.top([q[cid]["query_core"], *q[cid]["reformulations"]], asks[aid]["created_at"])
            CANDIDATES.write_text(json.dumps(cand))
            (DIR / "corpus_sizes.json").write_text(json.dumps(meta))
        pairs = _pairs(conn, cid, cand[cid], q[cid]["query_core"])
        log.info("askhn: idea %d/%d %s (%s, corpus anterior al Ask: %s items): %d pares",
                 n, len(order), aid, group_of(ext[aid], asks[aid]), meta.get(cid), len(pairs))
        verifier.verify([p for p in pairs if (p.case_id, p.item_id) not in done])
        log.info("askhn: gasto acumulado %s", {k: round(v, 4) for k, v in spent().items()})
    done = load_done(VERDICTS)
    complete = [a for a in order if case_id(a) in cand and all((case_id(a), i) in done for i in cand[case_id(a)])]
    return {"elegidos": len(order), "completos": len(complete), "detenido": stopped,
            "gasto": {k: round(v, 4) for k, v in spent().items()}, "total": round(sum(spent().values()), 4)}


def _pairs(conn, cid: str, items: list[str], idea: str):
    from gapfinder.text import get_texts
    from gapfinder.verify import CANDIDATE_CHARS, Pair

    texts = get_texts(conn, items)
    return [Pair(cid, idea, i, texts[i].title, texts[i].body[:CANDIDATE_CHARS]) for i in items]


# --- 4. reporte -----------------------------------------------------------------------------------------

REPORT = Path("data/eval/phase4_askhn.md")


def report(conn) -> str:
    from collections import Counter

    from gapfinder.holdout import BUILT, REVIEW, decide
    from gapfinder.verify import load_done

    data = _load(ASKS, {})
    asks, ext, order = load_asks(), load_extractions(), load_selected()
    cand, q, sizes = _load(CANDIDATES, {}), _load(QUERIES, {}), _load(DIR / "corpus_sizes.json", {})
    ver = load_done(VERDICTS)
    meta = {i: (t, u, c) for i, t, u, c in conn.execute("SELECT id, title, url, created_at FROM items")}
    reqs = [a for a, e in ext.items() if e["es_pedido_de_herramienta"]]
    rows = []
    for aid in order:
        cid = case_id(aid)
        items = cand.get(cid, [])
        if not items or any((cid, i) not in ver for i in items):
            continue
        scored = sorted(items, key=lambda i: -ver[(cid, i)].core)
        rows.append({"aid": aid, "cid": cid, "group": group_of(ext[aid], asks[aid]), "items": items, "scored": scored,
                     "best": ver[(cid, scored[0])].core, "decision": decide(ver[(cid, scored[0])].core)})
    sp = spent()
    L = ["# Fase 4: lado de demanda con Ask HN \"¿hay una herramienta para…?\"\n",
         "Pedidos reales de Hacker News (Ask HN) convertidos en ideas, con los comentarios como etiqueta aproximada "
         "(\"sí, existe X\" / \"busqué y no hay\"). Cada idea se corre contra el corpus **anterior a la fecha del Ask** "
         "(mismo enmascarado que el holdout, embeddings MiniLM existentes, sin re-embeber), con llm5 (prompt v2), top-1000 y "
         f"Jev vía OpenRouter. Regla de la Fase 3: P(núcleo) >= {BUILT} ya construido, {REVIEW}-{BUILT} revisar, < {REVIEW} no.\n",
         "## Embudo\n", "| paso | Asks |", "|---|---|",
         f"| bajados (únicos, {len(data['queries'])} consultas, >= {MIN_POINTS} puntos y >= {MIN_COMMENTS} comentarios en Algolia) | {data['funnel']['bajados_unicos']:,} |"]
    for k, v in data["funnel"]["descartados"].items():
        L.append(f"| − {k.replace('_', ' ')} | {v:,} |")
    L += [f"| filtrados (sin LLM) | {data['funnel']['filtrados']} |",
          f"| extraídos con LLM | {len(ext)} |",
          f"| pedidos reales de herramienta (según el LLM) | {len(reqs)} |",
          f"| elegidos (hasta {MAX_IDEAS}, balanceados por etiqueta) | {len(order)} |",
          f"| procesados completos (top-{K} verificado) | {len(rows)} |", "",
          "### Lo que aportó cada consulta\n",
          "Algolia busca por palabras (no la frase exacta) y devuelve como mucho 1000 resultados por consulta. \"nuevos\" = "
          "Asks que ninguna consulta anterior había traído; \"pasan\" = de esos, los que pasaron los filtros.\n",
          "| consulta | hits | nuevos | pasan |", "|---|---|---|---|"]
    for qq, v in data["queries"].items():
        L.append(f"| {qq} | {v['hits']} | {v['nuevos']} | {v['pasan_filtro']} |")
    L += ["", "Filtros sin LLM: título con forma de pedido (\"is there a/an/any\", \"looking for a\", \"any tool\", \"what tool do you\", "
          "\"how do you\", \"I wish there was\"…), sin empleo/carrera, con una palabra de software en título o texto, Asks desde "
          f"{MIN_DATE} (antes, el corpus anterior al Ask es chico); los \"how do you…\" además necesitan la palabra de software en el título.\n"]
    # cobertura
    tools = [(a, t) for a in reqs for t in ext[a]["herramientas_sugeridas"]]
    with_url = [(a, t) for a, t in tools if t["url"]]

    def cov(lst):
        inn = sum(bool(t["corpus_ids"]) for _, t in lst)
        pre = sum(bool(pre_ask_tools({"herramientas_sugeridas": [t]}, asks[a])) for a, t in lst)
        n = len(lst)
        return f"{n} | {inn} ({inn / n:.0%}) | {n - inn} ({(n - inn) / n:.0%}) | {pre} ({pre / n:.0%})" if n else "0 | – | – | –"
    how = Counter(t["mapeo"].split(":")[0] for _, t in tools if t["corpus_ids"])
    L += ["## Cobertura: ¿están en el corpus las herramientas que sugieren los comentarios?\n",
          f"Sobre los {len(reqs)} pedidos reales. Mapeo por URL (repo de GitHub, URL exacta, repo cuya homepage es el dominio o Show HN "
          "del dominio, validados por nombre); sin URL, por nombre exacto de un repo cuyo dueño es el proyecto (heurístico). "
          "Las URLs de tiendas de apps no se mapean por dominio.\n",
          "| herramientas sugeridas | total | en el corpus | NO en el corpus | en el corpus y anteriores al Ask |", "|---|---|---|---|---|",
          f"| todas | {cov(tools)} |", f"| con URL en el comentario | {cov(with_url)} |",
          f"| presentadas como equivalentes | {cov([x for x in tools if x[1]['relacion'] == 'equivalente'])} |",
          f"| equivalentes con URL | {cov([x for x in with_url if x[1]['relacion'] == 'equivalente'])} |", "",
          "Cómo se mapearon las que están: " + ", ".join(f"{k} {v}" for k, v in how.most_common()) + ".\n",
          "La medida más limpia es \"con URL\": sin URL, el mapeo por nombre solo encuentra repos con nombre único, así que "
          "\"todas\" subestima la cobertura. Lo que no está suele ser producto comercial o app sin repo ni Show HN.\n"]
    # matriz
    groups = ["existe_con_item_en_corpus", "existe_sin_item_en_corpus", "parcial", "no_existe", "incierto"]
    decs = ["ya construido", "revisar", "no"]
    L += ["## Etiqueta de los comentarios × decisión del sistema\n",
          f"{len(rows)} ideas procesadas. \"existe con item en corpus\" = algún comentario sugiere un equivalente que está en el corpus "
          "con fecha anterior al Ask (el sistema podía encontrarlo).\n",
          "| etiqueta de los comentarios | " + " | ".join(decs) + " | total |", "|---|" + "---|" * (len(decs) + 1)]
    for g in groups:
        rs = [r for r in rows if r["group"] == g]
        if rs:
            L.append(f"| {g.replace('_', ' ')} | " + " | ".join(str(sum(r['decision'] == d for r in rs)) for d in decs) + f" | {len(rs)} |")
    L.append(f"| **total** | " + " | ".join(str(sum(r['decision'] == d for r in rows)) for d in decs) + f" | {len(rows)} |")
    # recall del sugerido
    L += ["", "## Recall del item sugerido (cuando está en el corpus antes del Ask)\n",
          "Para cada idea procesada con alguna herramienta sugerida en el corpus anterior al Ask: el mejor rank de sus items "
          "(repo y Show HN gemelos) en el top-1000 y su P(núcleo) de Jev.\n",
          "| Ask | etiqueta | herramienta sugerida (relación) | rank | P(núcleo) | decisión del sistema |", "|---|---|---|---|---|---|"]
    found = tot = 0
    for r in rows:
        a = asks[r["aid"]]
        for t in pre_ask_tools(ext[r["aid"]], a):
            ids = [i for i in t["corpus_ids"] if t["corpus_created"].get(i, "9") < a["created_at"]]
            hit = [i for i in ids if i in r["items"]]
            tot += 1
            if hit:
                i = min(hit, key=r["items"].index)
                found += 1
                L.append(f"| [{r['aid']}]({a['hn_url']}) | {r['group'].replace('_', ' ')} | {t['nombre'][:40]} ({t['relacion']}) | "
                         f"{r['items'].index(i) + 1} | {ver[(r['cid'], i)].core:.2f} | {r['decision']} |")
            else:
                L.append(f"| [{r['aid']}]({a['hn_url']}) | {r['group'].replace('_', ' ')} | {t['nombre'][:40]} ({t['relacion']}) | "
                         f"> {K} | – | {r['decision']} |")
    L += ["", f"Dentro del top-{K}: {found}/{tot}." if tot else "Ninguna idea procesada tiene herramientas sugeridas en el corpus.", ""]
    # detalle por idea
    L += ["## Ideas procesadas\n"]
    for r in sorted(rows, key=lambda r: (decs.index(r["decision"]), -r["best"])):
        a, e = asks[r["aid"]], ext[r["aid"]]
        sug = "; ".join(f"{t['nombre'][:30]} ({t['relacion']}{', en corpus' if t['corpus_ids'] else ''})"
                        for t in e["herramientas_sugeridas"][:6]) or "ninguna"
        L.append(f"- **{r['decision']}** ({r['best']:.2f}) · [{a['title'][:100]}]({a['hn_url']}) · {a['created_at'][:10]} · "
                 f"{a['points']} pts · comentarios: {r['group'].replace('_', ' ')} · corpus anterior: {sizes.get(r['cid'], '?'):,} items  \n"
                 f"  Idea: {e['idea']}  \n  Sugeridas en el hilo: {sug}")
        for i in r["scored"][:3 if r["decision"] == "no" else 1]:
            t, u, c = meta.get(i, ("?", "", "?"))
            L.append(f"  - {ver[(r['cid'], i)].core:.2f} · {t[:80]} · creado {c[:10]} · {u}")
    pend = [a for a in order if a not in {r["aid"] for r in rows}]
    if pend:
        L += ["", f"## Elegidos sin procesar ({len(pend)}): quedan para `uv run gapfinder askhn run` cuando haya saldo\n"]
        L += [f"- {a} · {group_of(ext[a], asks[a]).replace('_', ' ')} · {asks[a]['title'][:90]}" for a in pend]
    jev_pairs = sum(1 for k in ver)
    L += ["", "## Costos\n",
          f"- OpenRouter, extracción ({EXTRACT_MODEL}, {len(ext)} Asks, con reintentos): ${sp['openrouter_extraccion']:.3f} (usage.cost facturado).",
          f"- Anthropic, consultas llm5 (claude-opus-5 directo): ${sp['anthropic_consultas']:.3f} (una idea, antes de que la cuenta "
          "quedara sin crédito; tokens a $5/$25 por millón).",
          f"- OpenRouter, consultas llm5 (anthropic/claude-opus-5, prompt v2, {sum(1 for v in q.values() if v.get('via') == 'openrouter')} ideas): "
          f"${sp['openrouter_consultas']:.3f} (usage.cost facturado).",
          f"- OpenRouter, Jev ({jev_pairs:,} pares válidos + 1.000 descartados): ${sp['openrouter_jev']:.3f} (usage.cost facturado).",
          f"- **Total: ${sum(sp.values()):.3f}**. Tope: $0.90 al principio; con la recarga de OpenRouter ($5) se subió a ${BUDGET:.2f} "
          "para procesar las 40 ideas.\n",
          "## Incidentes y decisiones\n",
          f"- Extracción: {EXTRACT_MODEL} con schema estricto degeneró en 39/397 salidas (idea \"....\", nombres vacíos). Se agregó "
          f"validación + reintento (tercer intento con {FALLBACK_MODEL}); las salidas inválidas quedan en "
          "`data/askhn/extractions_descartadas.json` con su costo, que cuenta en el total.",
          "- Una idea llegó a procesarse con una extracción degenerada (Claude inventó una necesidad a partir de \"....\"): sus "
          "1.000 veredictos están archivados en `verdicts_jev_askhn_descartado.jsonl` y no entran en ningún resultado.",
          "- La cuenta de Anthropic se quedó sin crédito (error 400 de saldo, tratado como un 402): se frenó y, con el OK del usuario, "
          "las consultas siguieron con el mismo modelo y el mismo prompt vía OpenRouter.\n",
          "## Caveats\n",
          "- **Los comentarios no son la verdad completa.** \"No existe\" puede ser ignorancia de quien comenta o del OP; \"existe\" puede "
          "ser una sugerencia que no cumple lo pedido (el LLM distingue equivalente/parcial, pero lo hace leyendo el hilo, no probando la herramienta).",
          "- **Sesgo de selección de Ask HN:** pedidos de devs, en inglés, con votos y respuestas (>= 5 puntos, >= 3 comentarios); "
          "los pedidos sin respuesta (quizá los huecos más reales) quedan fuera por el filtro de comentarios.",
          "- **Etiqueta en la fecha del Ask:** el corpus se restringe a lo creado antes del Ask, pero los README de GitHub son los de hoy "
          "(un repo anterior pudo agregar la funcionalidad después) y las estrellas se miden hoy (>= 100★ hoy, no en la fecha del Ask).",
          "- **Cobertura del corpus:** una herramienta sugerida que no está en el corpus no se puede encontrar; un \"no\" del sistema con "
          "etiqueta \"existe sin item en corpus\" es un límite de cobertura, no un error del verificador.",
          "- **Extracción automática:** etiqueta e idea vienen de un LLM barato; la cola c) de `gapfinder review` las confirma o corrige.",
          f"- Muestra chica ({len(rows)} ideas procesadas): los porcentajes son orientativos.\n"]
    text = "\n".join(L) + "\n"
    REPORT.write_text(text)
    return text
