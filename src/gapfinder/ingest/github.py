"""Ingesta de repos de GitHub vía la Search API.

La Search API devuelve como máximo 1000 resultados por consulta, así que se parte
el tiempo en ventanas de `created:` y se subdividen hasta que cada una tenga <=1000
resultados. Cada ventana terminada queda marcada en `ingest_state`, así que
re-correr no repite consultas. Se recorre de lo más reciente a lo más viejo.

Rate limits: search 10 req/min sin token, 30 req/min con GITHUB_TOKEN.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from urllib.parse import urlparse

import httpx

from gapfinder import db
from gapfinder.http import get_json

log = logging.getLogger(__name__)

API = "https://api.github.com/search/repositories"
SOURCE = "github"
PER_PAGE = 100
MAX_RESULTS = 1000
MAX_DESC = 1000
MAX_README = 2000
FIRST_DAY = date(2008, 1, 1)
SLICE_DAYS = 90  # ventana inicial; se subdivide si hace falta


# Primer segmento de path en github.com que no es un usuario/organización.
_GITHUB_RESERVED = {
    "orgs", "features", "marketplace", "topics", "collections", "trending", "sponsors",
    "settings", "about", "pricing", "apps", "search", "explore", "login", "join", "enterprise",
}


def github_repo_from_url(url: str) -> str | None:
    """'https://github.com/Owner/Repo/tree/main/x' -> 'Owner/Repo'. None si no es un repo."""
    u = urlparse(url.strip())
    if u.hostname not in ("github.com", "www.github.com"):
        return None
    parts = [p for p in u.path.split("/") if p]
    if len(parts) < 2 or parts[0].lower() in _GITHUB_RESERVED:
        return None
    repo = parts[1].removesuffix(".git")
    return f"{parts[0]}/{repo}" if repo else None


def parse_repo(repo: dict) -> db.Item:
    parts = [(repo.get("description") or "").strip()]
    if topics := repo.get("topics"):
        parts.append("Topics: " + ", ".join(topics))
    return db.Item(
        id=f"{SOURCE}:{repo['full_name']}",
        source=SOURCE,
        url=repo["html_url"],
        title=repo["name"],
        description="\n".join(p for p in parts if p)[:MAX_DESC],
        created_at=repo["created_at"],
        last_activity_at=repo.get("pushed_at"),
        stars=repo.get("stargazers_count"),
        archived=bool(repo.get("archived")),
        extra=json.dumps({
            "full_name": repo["full_name"],
            "language": repo.get("language"),
            "homepage": repo.get("homepage") or None,
            "forks": repo.get("forks_count"),
        }),
    )


def _client() -> httpx.Client:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    return httpx.Client(headers=headers, timeout=30)


class _Throttle:
    """Espaciado mínimo entre requests para no quemar el límite por minuto."""

    def __init__(self, per_minute: int) -> None:
        self.interval = 60.0 / per_minute
        self.last = 0.0

    def wait(self) -> None:
        delta = time.monotonic() - self.last
        if delta < self.interval:
            time.sleep(self.interval - delta)
        self.last = time.monotonic()


def _search(client: httpx.Client, throttle: _Throttle, q: str, page: int) -> dict:
    throttle.wait()
    data, _ = get_json(client, API, {"q": q, "sort": "stars", "order": "desc", "per_page": PER_PAGE, "page": page})
    return data


def _query(min_stars: int, start: date, end: date, max_stars: int | None = None) -> str:
    stars = f"{min_stars}..{max_stars}" if max_stars is not None else f">={min_stars}"
    return f"stars:{stars} created:{start.isoformat()}..{end.isoformat()}"


def ingest(conn: sqlite3.Connection, limit: int, min_stars: int, max_stars: int | None = None) -> int:
    """Trae repos con estrellas en [min_stars, max_stars] hasta tener `limit` items de GitHub.

    Para ampliar el umbral sin repetir trabajo: primero `min_stars=100`, después
    `min_stars=50, max_stars=99` (cada banda tiene sus propias ventanas marcadas).
    """
    throttle = _Throttle(28 if os.environ.get("GITHUB_TOKEN") else 9)
    if not os.environ.get("GITHUB_TOKEN"):
        log.warning("github: sin GITHUB_TOKEN, search limitada a ~10 req/min")
    today = date.today()
    # Pila de ventanas (más reciente arriba). La ventana en curso nunca se marca como hecha.
    windows: list[tuple[date, date]] = []
    start = FIRST_DAY
    while start <= today:
        end = min(start + timedelta(days=SLICE_DAYS - 1), today)
        windows.append((start, end))
        start = end + timedelta(days=1)

    added = 0
    with _client() as client:
        while windows:
            if db.count_items(conn, SOURCE) >= limit:
                log.info("github: límite %d alcanzado", limit)
                break
            start, end = windows.pop()
            q = _query(min_stars, start, end, max_stars)
            key = f"github:done:{q}"
            if db.get_state(conn, key):
                continue

            first = _search(client, throttle, q, 1)
            total = first["total_count"]
            if total > MAX_RESULTS and start < end:
                mid = start + (end - start) // 2
                windows.append((start, mid))
                windows.append((mid + timedelta(days=1), end))  # la mitad reciente se procesa primero
                continue
            if total > MAX_RESULTS:
                log.warning("github: %s tiene %d repos, solo se traen los 1000 con más estrellas", start, total)

            items = [parse_repo(r) for r in first["items"]]
            pages = min(-(-total // PER_PAGE), MAX_RESULTS // PER_PAGE)
            for page in range(2, pages + 1):
                items += [parse_repo(r) for r in _search(client, throttle, q, page)["items"]]
            added += db.upsert_items(conn, items)
            if end < today - timedelta(days=1):
                db.set_state(conn, key, "1")
            log.info("github: %s..%s %d repos (total %d)", start, end, len(items), db.count_items(conn, SOURCE))
    return added


def census(thresholds: list[int], first_year: int = FIRST_DAY.year) -> dict[int, dict[int, int]]:
    """Cuenta repos por año de creación y umbral de estrellas (solo total_count, 1 req por celda)."""
    throttle = _Throttle(28 if os.environ.get("GITHUB_TOKEN") else 9)
    out: dict[int, dict[int, int]] = {}
    with _client() as client:
        for year in range(first_year, date.today().year + 1):
            out[year] = {}
            for t in thresholds:
                throttle.wait()
                data, _ = get_json(client, API, {"q": _query(t, date(year, 1, 1), date(year, 12, 31)), "per_page": 1})
                out[year][t] = data["total_count"]
            log.info("census %d: %s", year, out[year])
    return out


# --- README (opcional) -------------------------------------------------------
# Se baja de raw.githubusercontent.com, que no consume la cuota de la API.

README_NAMES = ("README.md", "readme.md", "README.rst", "README", "Readme.md")
_MD_NOISE = [
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"!\[[^\]]*\]\([^)]*\)"),         # imágenes / badges
    re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)"),
    re.compile(r"<[^>]+>"),                      # html embebido
    re.compile(r"```.*?```", re.DOTALL),         # bloques de código
]


_RST_DIRECTIVE = re.compile(r"^\s*\.\.(?:\s|$)")                # .. image::, .. |x| image::, .. _ref: url, comentarios
_RST_OPTION = re.compile(r"^\s*:[\w-]+:")                     # :target: / :alt: / :height: debajo de una directiva
_RST_SUBST_DEF = re.compile(r"^\s*\.\.\s+\|([^|]+)\|", re.MULTILINE)
# `Texto <url>`_ -> Texto (también el resto `Texto `_ y textos partidos en dos líneas); no `_.where`
_RST_LINK = re.compile(r"`([^`<]{0,200}?)\s*(?:<[^>]*>)?`_{1,2}(?!\w)")
_RST_LITERAL = re.compile(r"``([^`\n]+)``")
_RST_ADORNMENT = re.compile(r"^\s*([=\-~^\"'`#*+:.])\1{3,}\s*$", re.MULTILINE)


def _clean_rst(text: str) -> str:
    """reStructuredText: directivas con sus opciones, sustituciones |x|, links y literales.
    Va antes de la limpieza de HTML, que si no se come el <url> de los links y deja `Texto `_."""
    for name in set(_RST_SUBST_DEF.findall(text)):
        text = re.sub(rf"\|{re.escape(name)}\|_{{0,2}}", " ", text)
    lines, in_directive, in_comment = [], False, False
    for line in text.splitlines():
        if _RST_DIRECTIVE.match(line):
            in_directive, in_comment = True, line.strip() == ".."  # ".." solo: comentario, cuerpo indentado
            continue
        if in_directive and (_RST_OPTION.match(line) or (in_comment and line[:1].isspace() and line.strip())):
            continue
        in_directive = in_comment = False
        lines.append(line)
    text = _RST_LINK.sub(lambda m: re.sub(r"\s+", " ", m.group(1)), "\n".join(lines))
    text = _RST_LITERAL.sub(r"\1", text)
    text = _RST_ADORNMENT.sub("", text)
    return re.sub(r"::$", ":", text, flags=re.MULTILINE)


def is_rst_noisy(text: str) -> bool:
    """README guardado con restos de reStructuredText (limpiado antes de que existiera _clean_rst)."""
    return bool(re.search(r"^\.\.(?:\s|$)|^:target:|[^`\s] ?`_{1,2}(?!\w)", text, re.MULTILINE))


def clean_readme(text: str) -> str:
    text = _clean_rst(text)
    for pat in _MD_NOISE:
        text = pat.sub(" ", text)
    text = re.sub(r"^\s*[=\-_*]{3,}\s*$", "", text, flags=re.MULTILINE)  # subrayados setext / separadores
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # links -> texto
    text = re.sub(r"^[#>*\-\s]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", "\n", text)
    return re.sub(r"[ \t]+", " ", text).strip()[:MAX_README]


class RateLimited(Exception):
    """El servidor sigue limitando después de los reintentos: dejar el item pendiente."""


def fetch_readme(client: httpx.Client, full_name: str, max_retries: int = 5) -> str:
    """README limpio, '' si el repo no tiene. Lanza RateLimited si no se pudo determinar."""
    headers = {"Authorization": f"Bearer {t}"} if (t := os.environ.get("GITHUB_TOKEN")) else {}
    for name in README_NAMES:
        url = f"https://raw.githubusercontent.com/{full_name}/HEAD/{name}"
        delay = 5.0
        for _ in range(max_retries):
            try:
                resp = client.get(url, headers=headers)
            except httpx.TransportError:
                time.sleep(delay)
                delay *= 2
                continue
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(float(resp.headers.get("retry-after", delay)))
                delay *= 2
                continue
            break
        else:
            raise RateLimited(full_name)
        if resp.status_code == 200:
            return clean_readme(resp.text)
    return ""


def _try_readme(client: httpx.Client, full_name: str) -> str | None:
    try:
        return fetch_readme(client, full_name)
    except RateLimited:
        return None


def fetch_readmes(conn: sqlite3.Connection, limit: int, workers: int = 8, batch: int = 500) -> int:
    names = db.github_items_without_readme(conn, limit)
    log.info("github: bajando README de %d repos", len(names))
    done = 0
    with httpx.Client(timeout=20, follow_redirects=True) as client, ThreadPoolExecutor(workers) as pool:
        for start in range(0, len(names), batch):
            chunk = names[start:start + batch]
            got = [(n, r) for n, r in zip(chunk, pool.map(lambda n: _try_readme(client, n), chunk))
                   if r is not None]  # None = limitado: queda pendiente para la próxima corrida
            # '' marca "intentado, sin README" para no reintentar. Una transacción corta por lote:
            # no bloquear otros escritores mientras se baja.
            conn.executemany("UPDATE items SET readme=? WHERE id=?", [(r, f"github:{n}") for n, r in got])
            conn.commit()
            done += len(got)
            log.info("github: %d/%d README", start + len(chunk), len(names))
    return done
