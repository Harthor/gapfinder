"""Ingesta de Show HN vía la API pública de Algolia.

Algolia devuelve como máximo 1000 hits por consulta, así que se pagina por fecha:
se pide `created_at_i <= cursor` en orden descendente y el cursor baja al hit más viejo.
El estado guarda el rango [oldest, newest] ya cubierto, así que re-correr solo
trae lo nuevo (arriba de newest) y sigue el backfill (abajo de oldest).
"""

from __future__ import annotations

import html
import json
import logging
import re
import sqlite3
import time
from datetime import datetime, timezone

import httpx

from gapfinder import db
from gapfinder.http import get_json

log = logging.getLogger(__name__)

API = "https://hn.algolia.com/api/v1/search_by_date"
PAGE_SIZE = 1000
SOURCE = "show_hn"
MAX_DESC = 2000

_TAG_RE = re.compile(r"<[^>]+>")
_PREFIX_RE = re.compile(r"^\s*show\s+hn\s*[:\-–—]\s*", re.IGNORECASE)


def clean_html(text: str) -> str:
    text = re.sub(r"<p>|<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = html.unescape(_TAG_RE.sub("", text))
    return re.sub(r"[ \t]+", " ", text).strip()


def parse_hit(hit: dict) -> db.Item | None:
    title = (hit.get("title") or "").strip()
    if not title or hit.get("created_at_i") is None:
        return None
    object_id = str(hit["objectID"])
    hn_url = f"https://news.ycombinator.com/item?id={object_id}"
    created = datetime.fromtimestamp(hit["created_at_i"], tz=timezone.utc)
    return db.Item(
        id=f"{SOURCE}:{object_id}",
        source=SOURCE,
        url=(hit.get("url") or "").strip() or hn_url,
        title=_PREFIX_RE.sub("", title),
        description=clean_html(hit.get("story_text") or "")[:MAX_DESC],
        created_at=created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        hn_points=hit.get("points"),
        hn_comments=hit.get("num_comments"),
        extra=json.dumps({"hn_url": hn_url, "author": hit.get("author")}),
    )


def _sweep(
    client: httpx.Client, conn: sqlite3.Connection, lower: int, upper: int, budget: int
) -> tuple[int, int | None]:
    """Baja desde `upper` hasta `lower` (exclusivo). Devuelve (nuevos, ts más viejo visto)."""
    new_total, cursor, oldest_seen = 0, upper, None
    while new_total < budget:
        params = {
            "tags": "show_hn",
            "hitsPerPage": PAGE_SIZE,
            "numericFilters": f"created_at_i>{lower},created_at_i<={cursor}",
        }
        data, _ = get_json(client, API, params)
        hits = data.get("hits", [])
        if not hits:
            break
        items = [i for h in hits if (i := parse_hit(h))]
        new_total += db.upsert_items(conn, items)
        page_min = min(h["created_at_i"] for h in hits)
        oldest_seen = page_min
        # Si toda la página comparte timestamp, forzamos avance para no ciclar.
        cursor = page_min if page_min < cursor else cursor - 1
        log.info("show_hn: hasta %s, +%d nuevos (total %d)",
                 datetime.fromtimestamp(page_min, tz=timezone.utc).date(), new_total, db.count_items(conn, SOURCE))
        if len(hits) < PAGE_SIZE:
            oldest_seen = lower + 1  # agotado el rango
            break
    return new_total, oldest_seen


def ingest(conn: sqlite3.Connection, limit: int) -> int:
    """Trae Show HN hasta tener `limit` items de esta fuente. Idempotente y reanudable."""
    now = int(time.time())
    newest = db.get_state(conn, "show_hn:newest_ts")
    oldest = db.get_state(conn, "show_hn:oldest_ts")
    added = 0
    with httpx.Client(timeout=30) as client:
        if newest is not None:
            # Puesta al día: lo publicado desde la última corrida. No cuenta contra el límite.
            n, _ = _sweep(client, conn, lower=int(newest), upper=now, budget=10**9)
            added += n
            db.set_state(conn, "show_hn:newest_ts", str(now))

        remaining = limit - db.count_items(conn, SOURCE)
        if remaining <= 0:
            log.info("show_hn: límite %d alcanzado", limit)
            return added
        if oldest == "0":
            log.info("show_hn: backfill completo")
            return added

        upper = int(oldest) if oldest is not None else now  # <= : el upsert deduplica el borde
        n, oldest_seen = _sweep(client, conn, lower=0, upper=upper, budget=remaining)
        added += n
        if newest is None:
            db.set_state(conn, "show_hn:newest_ts", str(now))
        if oldest_seen is not None:
            db.set_state(conn, "show_hn:oldest_ts", str(oldest_seen if oldest_seen > 1 else 0))
    return added
