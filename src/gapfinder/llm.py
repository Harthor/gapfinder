"""Consultas generadas con Claude para la iteración 2 de retrieval.

Por caso:
- real / partial: `query_core` (la necesidad central en 1-2 oraciones, sin jerga de Constellate) y
  `missing_piece_quote` (la frase de la descripción que dice qué falta, copiada textual, para medir
  en qué token cae).
- todos: 4 reformulaciones diversas y 3 consultas de palabras clave (búsqueda dirigida).

El prompt prohíbe nombrar productos o proyectos existentes: el modelo conoce muchos y nombrarlos
sería filtrar la respuesta al retrieval. Los resultados se guardan en data/llm_queries.json por caso
(con un hash de la entrada), así re-correr solo pide lo que falta o cambió.
"""

from __future__ import annotations

import hashlib
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

log = logging.getLogger(__name__)

MODEL = "claude-opus-5"
OUT = Path("data/llm_queries.json")
WORKERS = 8

SYSTEM = """You write search queries for a retrieval benchmark. Each case is an idea for a software \
product or tool (or a need someone has). The queries will be used to search a corpus of Show HN posts \
and GitHub repositories for things that already solve that need.

Rules for every string you write:
- English.
- Never name existing products, companies, open-source projects, libraries or services that might \
solve the need, even if you know some. Describe the need, not a known answer. Do not name specific \
websites or platforms (e.g. a particular news site, marketplace or social network) unless the case \
itself names them. (Naming a general technology the case itself names, like "Kubernetes" or "PDF", is fine.){category_rule}
- No internal jargon from the source: do not use words like "neighborhood", "constellation", \
"absence", "gap cluster", or numeric ids.

Reformulations: 4 queries that each describe the same need with clearly different vocabulary and \
level of abstraction, for example: (1) how a user would describe their problem, (2) how a product \
page would describe the tool, (3) a technical/implementation phrasing, (4) a broader category-level \
phrasing. One sentence each.

Keyword queries: 3 short queries of 2-4 words each, suitable for GitHub repository search (all words \
must match) and Hacker News search. Use words a project name or description would contain."""

# v2 (sep-2026): la v1 evitaba también el nombre de la categoría ("LLM router"), que es justo el vocabulario
# del corpus; RouteLLM quedaba en el rank 62.461 con query_core. Los nombres de productos siguen prohibidos.
CATEGORY_RULE = """
- Do use the standard category or technical terms practitioners use for this kind of tool (for example \
"LLM router", "feature flag service", "reverse proxy", "vector database"), including abbreviations. \
Category terms are not product names."""
PROMPT_VERSIONS = {1: SYSTEM.format(category_rule=""), 2: SYSTEM.format(category_rule=CATEGORY_RULE)}
SYSTEM = PROMPT_VERSIONS[1]

# Campos separados en vez de arrays: el schema no admite minItems/maxItems > 1 y la cantidad es fija.
_LISTS = {"reformulations": ("reformulation", 4), "keyword_queries": ("keyword_query", 3)}
_LIST_FIELDS = {f"{prefix}_{n}": {"type": "string"} for prefix, k in _LISTS.values() for n in range(1, k + 1)}
SCHEMA_IDEA = {
    "type": "object",
    "properties": {
        "query_core": {"type": "string", "description": "The central need or missing piece, 1-2 sentences."},
        "missing_piece_quote": {"type": "string", "description": "Verbatim substring of the DESCRIPTION "
                                "(copied exactly) that states what is missing; the shortest clause or sentence."},
        **_LIST_FIELDS,
    },
    "required": ["query_core", "missing_piece_quote", *_LIST_FIELDS],
    "additionalProperties": False,
}
SCHEMA_NEED = {"type": "object", "properties": _LIST_FIELDS, "required": list(_LIST_FIELDS), "additionalProperties": False}


def _lists(data: dict) -> dict:
    """reformulation_1..4 / keyword_query_1..3 -> listas."""
    for name, (prefix, k) in _LISTS.items():
        data[name] = [data.pop(f"{prefix}_{n}") for n in range(1, k + 1)]
    return data


def _prompt(case: dict) -> tuple[str, dict]:
    if case["kind"] in ("real", "partial"):
        return (f"Idea title: {case['title']}\n\nDESCRIPTION:\n{case.get('description', '')}\n\n"
                "Extract query_core: the central need or missing piece of this idea in 1-2 plain English "
                "sentences, as someone searching for a tool that fills it would state it. Also copy into "
                "missing_piece_quote the exact words from the DESCRIPTION that state what is missing. "
                "Then write the reformulations and keyword queries for query_core."), SCHEMA_IDEA
    return (f"Need (as written by someone searching):\n{case['title']}\n\n"
            "Write the reformulations and keyword queries for this need."), SCHEMA_NEED


def _key(case: dict, system: str = SYSTEM) -> str:
    text, _ = _prompt(case)
    return hashlib.sha256(f"{MODEL}\n{system}\n{text}".encode()).hexdigest()[:16]


def _call(client: anthropic.Anthropic, case: dict, system: str = SYSTEM) -> dict:
    text, schema = _prompt(case)
    for attempt in range(2):
        resp = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",  # si el modelo declina por política, el servidor reintenta con el recomendado
            system=system,
            output_config={"format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content": text}],
        )
        if resp.stop_reason == "refusal":
            raise RuntimeError(f"{case['id']}: refusal ({resp.stop_details})")
        data = _lists(json.loads(next(b.text for b in resp.content if b.type == "text")))
        quote = data.get("missing_piece_quote")
        if quote is None or quote in case.get("description", ""):
            data["model"] = resp.model
            return data
        log.warning("%s: la cita no es textual (intento %d)", case["id"], attempt + 1)
    data["missing_piece_quote_verbatim"] = False
    data["model"] = resp.model
    return data


def generate(cases: list[dict], out: Path = OUT, version: int = 1) -> dict:
    """version: 1 = prompt original; 2 = permite términos de categoría. Cada versión en su archivo."""
    system = PROMPT_VERSIONS[version]
    done = json.loads(out.read_text()) if out.exists() else {}
    todo = [c for c in cases if done.get(c["id"], {}).get("key") != _key(c, system)]
    log.info("llm: %d casos por pedir (%d ya hechos)", len(todo), len(cases) - len(todo))
    client = anthropic.Anthropic()

    def one(case: dict) -> tuple[str, dict | None]:
        try:
            return case["id"], {**_call(client, case, system), "key": _key(case, system), "prompt_version": version}
        except (anthropic.APIError, RuntimeError, json.JSONDecodeError) as e:
            log.error("llm %s: %s", case["id"], e)
            return case["id"], None

    with ThreadPoolExecutor(WORKERS) as pool:
        for n, (cid, res) in enumerate(pool.map(one, todo), 1):
            if res:
                done[cid] = res
            if n % 10 == 0 or n == len(todo):
                out.write_text(json.dumps(done, indent=1, ensure_ascii=False))
                log.info("llm: %d/%d", n, len(todo))
    out.write_text(json.dumps(done, indent=1, ensure_ascii=False))
    return {"ok": sum(c["id"] in done for c in cases), "failed": [c["id"] for c in cases if c["id"] not in done]}
