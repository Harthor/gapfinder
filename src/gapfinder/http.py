"""GET con reintentos y respeto de rate limits."""

from __future__ import annotations

import logging
import threading
import time

import httpx

log = logging.getLogger(__name__)

RETRY_STATUS = {429, 500, 502, 503, 504}


def get_json(
    client: httpx.Client, url: str, params: dict[str, str | int] | None = None, max_retries: int = 6
) -> tuple[dict, httpx.Headers]:
    delay = 2.0
    for attempt in range(max_retries):
        try:
            resp = client.get(url, params=params)
        except httpx.TransportError as e:
            log.warning("error de red (%s), reintento en %.0fs", e, delay)
            time.sleep(delay)
            delay *= 2
            continue

        # GitHub: 403 con remaining=0 o retry-after es rate limit, no permisos.
        rate_limited = resp.status_code == 403 and (
            resp.headers.get("x-ratelimit-remaining") == "0" or "retry-after" in resp.headers
        )
        if resp.status_code in RETRY_STATUS or rate_limited:
            wait = _wait_seconds(resp.headers, delay)
            log.warning("HTTP %s en %s, espero %.0fs", resp.status_code, url, wait)
            time.sleep(wait)
            delay *= 2
            continue

        resp.raise_for_status()
        return resp.json(), resp.headers
    raise RuntimeError(f"agotados {max_retries} reintentos para {url}")


def _wait_seconds(headers: httpx.Headers, fallback: float) -> float:
    if ra := headers.get("retry-after"):
        return float(ra) + 1
    if headers.get("x-ratelimit-remaining") == "0" and (reset := headers.get("x-ratelimit-reset")):
        return max(1.0, float(reset) - time.time() + 1)
    return fallback


class RateLimiter:
    """Ritmo global (requests/min) compartido entre hilos, con pausa común ante 429/bloqueos."""

    def __init__(self, rpm: float, name: str, base_backoff: float = 60.0) -> None:
        self.interval = 60.0 / rpm
        self.name = name
        self.base_backoff = base_backoff
        self.backoff = base_backoff
        self.next_slot = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        """Bloquea hasta el próximo turno global."""
        with self._lock:
            now = time.monotonic()
            slot = max(now, self.next_slot)
            self.next_slot = slot + self.interval
        time.sleep(slot - now)

    def success(self) -> None:
        with self._lock:
            self.backoff = max(self.base_backoff, self.backoff * 0.8)

    def penalize(self, reason: str, retry_after: float | None = None) -> None:
        """Pausa global. No escala si ya hay una pausa larga en curso (fallos simultáneos)."""
        with self._lock:
            now = time.monotonic()
            if self.next_slot - now >= self.backoff / 2:
                return
            wait = retry_after if retry_after is not None else self.backoff
            self.next_slot = now + wait
            self.backoff = min(self.backoff * 2, 1800.0)
        log.warning("%s: %s, pausa global %.0fs", self.name, reason, wait)
