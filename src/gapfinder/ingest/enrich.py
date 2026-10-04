"""Enriquecimiento de items de Show HN sin descripción.

- URL a un repo de GitHub: se guarda el vínculo `owner/repo`. Si el repo ya está en el
  corpus, su descripción/README se toman de ahí al embeber (no se descarga nada).
  Si no, se baja el README de raw.githubusercontent.com.
- Cualquier otra URL: meta description (og/description/twitter, <title> como último recurso).
  1. author_comment: comentarios top-level del autor en su hilo (>= 100 chars).
  2. author_reply: primeras 3 intervenciones del autor a cualquier profundidad (>= 100 chars c/u).
  3. Posts recientes (< CURRENT_MAX_AGE): meta de la página actual.
  4. Wayback (opt-in por umbral de puntos): snapshot más cercano a la fecha del post,
     solo si cae en [post - 30 días, post + 6 meses]. Si no corre, el item queda
     title_only con error WAYBACK_NOT_TRIED y `wayback_on_demand` lo puede completar.
  5. Si nada sirve: title_only.
  El filtro de basura se aplica igual a la página actual y a Wayback.

Cada item procesado queda en `enrichment` con su `text_origin`
(author_comment | author_reply | current | wayback | title_only), así que re-correr no repite requests. Los items que
quedaron sin resolver por rate limit no se escriben y se reintentan en la próxima corrida.
"""

from __future__ import annotations

import logging
import re
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx

from gapfinder.http import RateLimiter
from gapfinder.ingest import hn_comments
from gapfinder.ingest.github import RateLimited, fetch_readme, github_repo_from_url

log = logging.getLogger(__name__)

MAX_DESC = 1000
MAX_HTML_BYTES = 256_000
BATCH = 200
USER_AGENT = "Mozilla/5.0 (compatible; gapfinder/0.1; research crawler)"
CURRENT_MAX_AGE = timedelta(days=730)
WAYBACK_BEFORE = timedelta(days=30)
WAYBACK_AFTER = timedelta(days=182)
CDX_API = "https://web.archive.org/cdx/search/cdx"
AVAILABLE_API = "https://archive.org/wayback/available"
_TS_FMT = "%Y%m%d%H%M%S"

# Dominios estacionados / en venta / páginas de error o challenge. Se compara en minúsculas.
_JUNK_PATTERNS = [
    r"domain (name )?(is|may be) for sale", r"buy this domain", r"this domain (is|has been) (for sale|parked|registered)",
    r"domain for sale", r"is for sale", r"listed at \$", r"make an offer", r"parked (free|domain|by)",
    r"hugedomains", r"\bsedo\b", r"afternic", r"dan\.com", r"godaddy", r"domain default page",
    r"\bslots?\b.*\b(online|gacor)\b", r"\bgacor\b", r"\btogel\b", r"\bjudi\b", r"\bsitus\b",
    r"account (has been )?suspended", r"^index of /", r"welcome to nginx", r"^it works!?$",
    r"^just a moment", r"attention required", r"^access denied", r"^40[34]\b", r"not found$",
    r"^page not found", r"^site not found", r"this site can.t be reached",
]
_JUNK_RE = re.compile("|".join(_JUNK_PATTERNS))
_PARKING_HOSTS = ("sedo.com", "dan.com", "afternic.com", "hugedomains.com", "godaddy.com", "sedoparking.com")


def is_junk(text: str, final_url: str = "") -> bool:
    host = (urlparse(final_url).hostname or "").lower()
    if any(host == h or host.endswith("." + h) for h in _PARKING_HOSTS):
        return True
    return bool(_JUNK_RE.search(text.lower().strip()))


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "meta":
            a = {k.lower(): (v or "") for k, v in attrs}
            key = (a.get("name") or a.get("property") or "").lower()
            if key in ("description", "og:description", "twitter:description") and a.get("content"):
                self.meta.setdefault(key, a["content"])
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def extract_meta_description(html: str) -> str:
    parser = _MetaParser()
    try:
        parser.feed(html)
    except Exception:  # HTML roto: nos quedamos con lo que se haya parseado
        pass
    for key in ("og:description", "description", "twitter:description"):
        if text := parser.meta.get(key, "").strip():
            return _normalize(text)
    return _normalize(parser.title)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()[:MAX_DESC]


def wayback_window(post_date: datetime) -> tuple[str, str]:
    """Rango aceptado para snapshots, en formato CDX (YYYYMMDDhhmmss)."""
    return (post_date - WAYBACK_BEFORE).strftime(_TS_FMT), (post_date + WAYBACK_AFTER).strftime(_TS_FMT)


@dataclass(slots=True)
class Result:
    item_id: str
    github_repo: str | None
    method: str                      # github_corpus | github_readme | meta | failed
    text_origin: str                 # author_comment | author_reply | current | wayback | title_only
    description: str = ""
    readme: str | None = None
    error: str | None = None
    snapshot_at: str | None = None


# --- fetch --------------------------------------------------------------------


def _fetch_meta(client: httpx.Client, url: str) -> tuple[str, str | None]:
    """(descripción válida, error). Una descripción basura cuenta como error."""
    try:
        with client.stream("GET", url) as resp:
            if resp.status_code >= 400:
                return "", f"http {resp.status_code}"
            ctype = resp.headers.get("content-type", "")
            if "html" not in ctype:
                return "", f"content-type {ctype[:40]}"
            buf = b""
            for chunk in resp.iter_bytes():
                buf += chunk
                if len(buf) >= MAX_HTML_BYTES or b"</head>" in buf.lower():
                    break
            text = buf.decode(resp.encoding or "utf-8", errors="replace")
            final_url = str(resp.url)
    except (httpx.HTTPError, UnicodeError, ValueError) as e:
        return "", type(e).__name__
    desc = extract_meta_description(text)
    if not desc:
        return "", "sin meta"
    if is_junk(desc, final_url):
        return "", "basura"
    return desc, None


class Wayback:
    """Cliente de archive.org: ritmo global fijo (requests/min) y pausa compartida.

    web.archive.org bloquea la IP (conexión rechazada) si se excede su límite, así que
    todos los hilos comparten un único intervalo mínimo entre requests.
    """

    def __init__(self, workers: int, rpm: float) -> None:
        self.client = httpx.Client(timeout=httpx.Timeout(60.0, connect=10.0), follow_redirects=True,
                                   headers={"User-Agent": USER_AGENT})
        self.slots = threading.Semaphore(workers)
        self.limiter = RateLimiter(rpm, "wayback")

    def close(self) -> None:
        self.client.close()

    def _get(self, url: str, params: dict[str, str] | None = None, max_retries: int = 6) -> httpx.Response:
        for _ in range(max_retries):
            self.limiter.wait()
            with self.slots:
                try:
                    resp = self.client.get(url, params=params)
                except httpx.TimeoutException:
                    continue  # lentitud de archive.org, no rate limit
                except httpx.TransportError:
                    self.limiter.penalize("conexión rechazada")
                    continue
            if resp.status_code in (429, 503):
                ra = resp.headers.get("retry-after")
                self.limiter.penalize(f"http {resp.status_code}", float(ra) if ra and ra.isdigit() else None)
                continue
            self.limiter.success()
            return resp
        raise RateLimited(url)

    def closest_snapshot(self, url: str, post_date: datetime) -> tuple[str, str] | None:
        """(timestamp, url) del snapshot más cercano al post dentro de [post - 30d, post + 6m].

        La availability API es rápida pero devuelve el más cercano sin filtrar por rango.
        Si ese cae antes de la ventana puede haber uno válido después del post, y solo
        entonces se consulta CDX (lenta) por [post, post + 6m].
        """
        lo, hi = wayback_window(post_date)
        resp = self._get(AVAILABLE_API, {"url": url, "timestamp": post_date.strftime(_TS_FMT)})
        try:
            closest = resp.json().get("archived_snapshots", {}).get("closest") if resp.status_code == 200 else None
        except ValueError:
            closest = None
        if closest and closest.get("status") == "200":
            ts = closest["timestamp"]
            if lo <= ts <= hi:
                return ts, closest["url"].split(f"/web/{ts}/", 1)[-1]
            if ts > hi:
                return None  # el más cercano ya está después de la ventana: no hay nada adentro
        resp = self._get(CDX_API, {
            "url": url, "from": post_date.strftime(_TS_FMT), "to": hi, "output": "json",
            "fl": "timestamp,original", "filter": "statuscode:200", "limit": "1",
        })
        try:
            rows = resp.json() if resp.status_code == 200 else []
        except ValueError:
            rows = []
        return (rows[1][0], rows[1][1]) if len(rows) > 1 else None

    def meta(self, url: str, post_date: datetime) -> tuple[str, str | None, str | None]:
        """(descripción, snapshot_at, error)."""
        snap = self.closest_snapshot(url, post_date)
        if snap is None:
            return "", None, "wayback: sin snapshot en ventana"
        ts, original = snap
        resp = self._get(f"https://web.archive.org/web/{ts}id_/{original}")  # id_: HTML original sin toolbar
        if resp.status_code != 200:
            return "", ts, f"wayback: http {resp.status_code}"
        desc = extract_meta_description(resp.text[:MAX_HTML_BYTES])
        if not desc:
            return "", ts, "wayback: sin meta"
        if is_junk(desc):
            return "", ts, "wayback: basura"
        return desc, ts, None


# --- orquestación -------------------------------------------------------------

WAYBACK_NOT_TRIED = "wayback: no intentado"


def _github_one(client: httpx.Client, item_id: str, repo: str, in_corpus: set[str]) -> Result | None:
    if repo.lower() in in_corpus:
        return Result(item_id, repo, "github_corpus", "current")
    try:
        readme = fetch_readme(client, repo)
    except RateLimited:
        return None
    if readme:
        return Result(item_id, repo, "github_readme", "current", readme=readme)
    return Result(item_id, repo, "failed", "title_only", error="sin README")


def _from_comments(item_id: str, comments: list[hn_comments.Comment]) -> Result | None:
    if text := hn_comments.author_comment(comments):
        return Result(item_id, None, "author_comment", "author_comment", description=text)
    if text := hn_comments.author_reply(comments):
        return Result(item_id, None, "author_reply", "author_reply", description=text)
    return None


def _web_current(client: httpx.Client, item_id: str, url: str, created: datetime, points: int,
                 now: datetime, wayback_min_points: int | None) -> Result | None:
    """Resultado final, o None si le toca Wayback en esta corrida."""
    if url.startswith("https://news.ycombinator.com/"):
        return Result(item_id, None, "failed", "title_only", error="post de texto sin cuerpo")
    if now - created <= CURRENT_MAX_AGE:
        desc, _ = _fetch_meta(client, url)
        if desc:
            return Result(item_id, None, "meta", "current", description=desc)
    if wayback_min_points is None or points < wayback_min_points:
        return Result(item_id, None, "failed", "title_only", error=WAYBACK_NOT_TRIED)
    return None


def _web_wayback(wb: Wayback, item_id: str, url: str, created: datetime) -> Result | None:
    try:
        desc, ts, err = wb.meta(url, created)
    except RateLimited:
        return None
    if desc:
        return Result(item_id, None, "meta", "wayback", description=desc, snapshot_at=ts)
    return Result(item_id, None, "failed", "title_only", error=err, snapshot_at=ts)


def _save(conn: sqlite3.Connection, results: list[Result]) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO enrichment (item_id, github_repo, method, text_origin, snapshot_at, "
        "description, readme, error) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [(r.item_id, r.github_repo, r.method, r.text_origin, r.snapshot_at,
          r.description, r.readme, r.error) for r in results],
    )
    conn.commit()


def enrich(
    conn: sqlite3.Connection,
    limit: int,
    workers: int = 32,
    wayback_workers: int = 3,
    wayback_rpm: float = 15,
    wayback_min_points: int | None = None,
    only: str | None = None,
    order: str = "points",
) -> dict[str, int]:
    """Cadena para posts web: author_comment -> author_reply -> página actual (posts recientes)
    -> Wayback (solo si wayback_min_points no es None y el post lo alcanza) -> title_only.
    Sin Wayback, los que quedan sin texto se marcan WAYBACK_NOT_TRIED para `wayback_on_demand`.

    only: 'github' | 'web' | None. order: 'points' (más votados primero) | 'random'.
    """
    order_sql = "i.hn_points DESC" if order == "points" else "random()"
    todo = conn.execute(
        f"""SELECT i.id, i.url, i.created_at, COALESCE(i.hn_points, 0) FROM items i
            LEFT JOIN enrichment e ON e.item_id = i.id
            WHERE i.source='show_hn' AND i.description='' AND e.item_id IS NULL
            ORDER BY {order_sql}"""
    ).fetchall()
    if only:
        todo = [r for r in todo if (github_repo_from_url(r[1]) is not None) == (only == "github")]
    todo = todo[:limit]
    in_corpus = {r[0].lower() for r in conn.execute("SELECT substr(id, 8) FROM items WHERE source='github'")}
    log.info("enrich: %d items pendientes (%d repos en corpus)", len(todo), len(in_corpus))

    now = datetime.now(timezone.utc)
    counts: dict[str, int] = {}
    client = httpx.Client(timeout=httpx.Timeout(10.0, connect=5.0), limits=httpx.Limits(max_connections=workers * 2),
                          follow_redirects=True, headers={"User-Agent": USER_AGENT})
    wb = Wayback(wayback_workers, wayback_rpm)
    try:
        with ThreadPoolExecutor(workers) as pool:
            for start in range(0, len(todo), BATCH):
                batch = todo[start:start + BATCH]
                github_rows = [(r[0], repo) for r in batch if (repo := github_repo_from_url(r[1]))]
                web_rows = [(r[0], r[1], datetime.fromisoformat(r[2]), r[3]) for r in batch
                            if github_repo_from_url(r[1]) is None]

                results = list(pool.map(lambda g: _github_one(client, g[0], g[1], in_corpus), github_rows))

                comments = hn_comments.fetch_author_comments(conn, [w[0] for w in web_rows])
                rest = []
                for w in web_rows:
                    if w[0] not in comments:
                        results.append(None)  # hilo no disponible por rate limit: queda pendiente
                    elif r := _from_comments(w[0], comments[w[0]]):
                        results.append(r)
                    else:
                        rest.append(w)

                current = list(pool.map(lambda w: _web_current(client, *w, now, wayback_min_points), rest))
                results += [c for c in current if c is not None]
                need_wb = [w for w, c in zip(rest, current) if c is None]
                results += list(pool.map(lambda w: _web_wayback(wb, *w[:3]), need_wb))

                done = [r for r in results if r is not None]
                _save(conn, done)
                for r in done:
                    counts[r.text_origin] = counts.get(r.text_origin, 0) + 1
                counts["pendiente"] = counts.get("pendiente", 0) + len(results) - len(done)
                log.info("enrich: %d/%d %s", start + len(batch), len(todo), counts)
    finally:
        client.close()
        wb.close()
    return counts


def wayback_on_demand(conn: sqlite3.Connection, item_ids: list[str], workers: int = 3, rpm: float = 15) -> int:
    """Wayback para items puntuales (p. ej. candidatos title_only en el top-N de una idea).
    Solo toca los marcados WAYBACK_NOT_TRIED. Devuelve cuántos consiguieron texto."""
    if not item_ids:
        return 0
    marks = ",".join("?" * len(item_ids))
    rows = conn.execute(
        f"""SELECT i.id, i.url, i.created_at FROM items i JOIN enrichment e ON e.item_id = i.id
            WHERE e.error = ? AND i.id IN ({marks})""",
        [WAYBACK_NOT_TRIED, *item_ids],
    ).fetchall()
    if not rows:
        return 0
    wb = Wayback(workers, rpm)
    try:
        with ThreadPoolExecutor(workers) as pool:
            results = list(pool.map(lambda r: _web_wayback(wb, r[0], r[1], datetime.fromisoformat(r[2])), rows))
    finally:
        wb.close()
    done = [r for r in results if r is not None]
    _save(conn, done)
    return sum(r.text_origin == "wayback" for r in done)
