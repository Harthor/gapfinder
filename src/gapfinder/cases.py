"""Known cases: hoja de trabajo para casos sintéticos y conversión a known_cases.json.

Formato de known_cases.json (lista):
    {
      "id": "syn-12345" | "<id libre para reales>",
      "kind": "synthetic" | "real" | "partial" | "negative",   # partial: el prior art cubre parte de la idea
      "author": "claude" | "human",            # quién escribió la necesidad (sintéticos)
      "pair_id": "pair-12345",                 # opcional: misma idea escrita por humano y por Claude
      "leakage_flag": true,                    # opcional: worksheet-check la marcó y se dejó igual
      "title": "la necesidad / idea, tal como se buscaría",
      "description": "",                       # opcional
      "expected_urls": ["https://..."],        # lo que ya existía
      "expected_item_ids": ["show_hn:12345"],  # si se conoce el item del corpus
      "meta": {...}                            # opcional: época, puntos, origen del texto, hoja de origen
    }
Los casos reales pueden traer solo `expected_urls`; el eval los mapea a items del corpus.
"""

from __future__ import annotations

import json
import logging
import random
import re
import sqlite3
from pathlib import Path

from gapfinder.text import get_texts

log = logging.getLogger(__name__)

ERAS = {"2009-14": ("2009", "2015"), "2015-19": ("2015", "2020"), "2020-26": ("2020", "2027")}
POINTS = {"0-9": (0, 9), ">=10": (10, 10**9)}
SNIPPET = 300
NEED_PREFIX = "necesidad:"
# En los items [humano]: la versión de Claude del mismo item, para el recall pareado human vs claude.
PAIR_PREFIX = "necesidad claude:"


def _cells(n: int) -> dict[tuple[str, str], int]:
    """Reparte n lo más parejo posible entre las 6 celdas época x puntos."""
    keys = [(e, p) for e in ERAS for p in POINTS]
    base, extra = divmod(n, len(keys))
    return {k: base + (i < extra) for i, k in enumerate(keys)}


def worksheet_item_ids(paths: list[Path]) -> set[str]:
    """Items que ya aparecen en otras hojas (para no repetirlos)."""
    ids: set[str] = set()
    for p in paths:
        if p.exists():
            ids.update(m.group(2) for m in _HEADER_RE.finditer(p.read_text()))
    return ids


def build_worksheet(
    conn: sqlite3.Connection,
    n: int,
    seed: int = 42,
    origins: dict[str, int] | None = None,
    exclude: set[str] | None = None,
) -> str:
    """Muestra estratificada época x puntos. Con `origins` ({origen: cantidad}) se estratifica
    dentro de cada origen de texto; si no, entre todos los items con texto."""
    rng = random.Random(seed)
    exclude = exclude or set()
    rows = [tuple(r) for r in conn.execute(
        "SELECT id, url, title, created_at, COALESCE(hn_points, 0) FROM items WHERE source='show_hn' ORDER BY id"
    ) if r[0] not in exclude]
    texts = get_texts(conn, [r[0] for r in rows])
    eligible = [r for r in rows if texts[r[0]].enriched]
    groups = {o: [r for r in eligible if texts[r[0]].origin == o] for o in origins} if origins else {None: eligible}
    quotas = origins or {None: n}

    blocks = [
        "# Hoja de casos sintéticos\n",
        "Para cada item escribí en `necesidad:` la necesidad que este producto resuelve, formulada como",
        "la escribiría alguien que *busca* algo así sin saber que existe (sin nombre del producto ni",
        "términos demasiado específicos de su página). Podés usar varias líneas; termina en el `---`.",
        "Los items con `necesidad:` vacía se ignoran al importar.\n",
    ]
    idx = 0
    for origin, quota in quotas.items():
        for (era, pts), k in _cells(quota).items():
            lo_y, hi_y = ERAS[era]
            lo_p, hi_p = POINTS[pts]
            pool = [r for r in groups[origin] if lo_y <= r[3][:4] < hi_y and lo_p <= r[4] <= hi_p]
            if len(pool) < k:
                log.warning("celda %s/%s/%s: pedidos %d, disponibles %d", origin or "todos", era, pts, k, len(pool))
            for item_id, url, title, created, points in rng.sample(pool, min(k, len(pool))):
                idx += 1
                t = texts[item_id]
                body = re.sub(r"\s+", " ", t.body)
                snippet = body[:SNIPPET] + ("…" if len(body) > SNIPPET else "")
                blocks += [
                    f"## {idx} · {item_id} · {created[:10]} · {points} pts · época {era} · texto: {t.origin}\n",
                    f"- URL: {url}",
                    f"- Título: {title}",
                    f"- Texto: {snippet}\n",
                    f"{NEED_PREFIX} \n",
                    "---\n",
                ]
    return "\n".join(blocks)


HUMAN_TAG = "[humano]"
_HEADER_RE = re.compile(
    r"^## \d+(?: (\[humano\]))? · (show_hn:\d+) · (\S+) · (\d+) pts · época (\S+) · texto: (\S+)", re.MULTILINE
)


def parse_worksheet(text: str, sheet: str = "") -> tuple[list[dict], list[str]]:
    """Devuelve (casos sintéticos, ids con necesidad vacía). `sheet`: nombre de la hoja de origen."""
    cases, empty = [], []
    for block in re.split(r"^---\s*$", text, flags=re.MULTILINE):
        m = _HEADER_RE.search(block)
        if not m:
            continue
        human, item_id, date, points, era, origin = m.groups()
        url = re.search(r"^- URL: (\S+)", block, re.MULTILINE)
        # Solo la línea que *empieza* con "necesidad:" dentro del bloque (y lo que siga hasta el --- o la
        # versión de Claude); la introducción de la hoja también menciona "necesidad:".
        body = block[m.start():]
        nm = re.search(rf"^{NEED_PREFIX}(.*?)(?=^{PAIR_PREFIX}|\Z)", body, re.MULTILINE | re.DOTALL)
        pm = re.search(rf"^{PAIR_PREFIX}(.*)", body, re.MULTILINE | re.DOTALL) if human else None
        need = re.sub(r"\s+", " ", nm.group(1)).strip() if nm else ""
        pair = re.sub(r"\s+", " ", pm.group(1)).strip() if pm else ""
        if not need:
            empty.append(item_id)
            continue
        num = item_id.split(":")[1]
        base = {
            "kind": "synthetic",
            "description": "",
            "expected_urls": [url.group(1)] if url else [],
            "expected_item_ids": [item_id],
            "meta": {"date": date, "points": int(points), "era": era, "text_origin": origin, "worksheet": sheet},
        }
        author = "human" if human else "claude"
        cases.append({"id": f"syn-{num}", "author": author, "title": need, **base})
        if pair:
            cases[-1]["pair_id"] = f"pair-{num}"
            cases.append({"id": f"syn-{num}-claude", "author": "claude", "title": pair, "pair_id": f"pair-{num}",
                          **base, "meta": dict(base["meta"])})
    return cases, empty


def leakage_report(conn: sqlite3.Connection, parsed: list[dict], idf) -> list:
    """Leak por caso (filtro de fuga contra título + texto del item esperado), en el orden de `parsed`."""
    from gapfinder import leakage

    texts = get_texts(conn, [c["expected_item_ids"][0] for c in parsed])
    return [leakage.check(c["title"], f"{t.title}\n{t.body}", idf)
            for c in parsed for t in [texts[c["expected_item_ids"][0]]]]


def import_worksheet(worksheet: Path, cases_path: Path, flagged: set[str] | None = None) -> tuple[int, list[str]]:
    """Reemplaza en known_cases.json los casos de ESTA hoja (idempotente).
    Los casos de otras hojas y los reales se conservan. `flagged`: ids que el filtro de fuga marcó
    y quedaron como están (llevan leakage_flag: true)."""
    sheet = worksheet.name
    new, empty = parse_worksheet(worksheet.read_text(), sheet)
    for c in new:
        if c["id"] in (flagged or set()):
            c["leakage_flag"] = True
    existing = json.loads(cases_path.read_text()) if cases_path.exists() else []
    new_ids = {c["id"] for c in new}
    clash = [c["id"] for c in existing
             if c["id"] in new_ids and c.get("meta", {}).get("worksheet") not in (sheet, None)]
    if clash:
        raise ValueError(f"ids ya importados desde otra hoja: {', '.join(clash)}")
    kept = [c for c in existing if c.get("meta", {}).get("worksheet") != sheet]
    cases_path.write_text(json.dumps(kept + new, indent=2, ensure_ascii=False) + "\n")
    return len(new), empty
