"""Casos reales y negativos a partir de las absences verificadas de Constellate.

Constellate verificó parte de sus absences ("huecos") de tres maneras:
- web: Claude con búsqueda web (tabla api_call_attempts de constellate.db + output.json),
- manual: investigación a mano en prior-art/*.md,
- rubric: rúbrica estricta, 2 corridas, en rubric-test/*.md.
Veredicto "yes" (ya existía) -> candidato kind="real"; "no" -> candidato kind="negative";
solo "partially" -> kind="partial" (el prior art cubre parte de la idea): esperado = todas sus URLs
de evidencia, viene confirmado en la hoja y el recall se reporta aparte.

`build_candidates` arma data/real_candidates.md; `import_candidates` convierte lo marcado en
known_cases.json. La evidencia nunca sale del retrieval de gapfinder (no sesgar el eval).
constellate.db se abre siempre en solo lectura (URI mode=ro).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import httpx

SOURCE_TAG = "constellate"
CONFIRM_PREFIX = "confirmado:"
EXPECTED_PREFIX = "esperado:"
CONFIRM_VALUES = {"real": "real", "negativo": "negative", "negative": "negative", "parcial": "partial",
                  "partial": "partial", "descartar": None, "no": None}
CASE_PREFIX = {"real": "real", "negative": "neg", "partial": "part"}
KIND_LABEL = {"real": "real", "negative": "negativo", "partial": "parcial"}
_URL_RE = re.compile(r"https?://[^\s)\]>,*]+")
# En `esperado:` también se aceptan ids del corpus, para fijar un item que la URL no resuelve (un Show HN).
_ITEM_ID_RE = re.compile(r"(?<![\w/!])(?:show_hn:\d+|github:[\w.-]+/[\w.-]+)")
# `!github:owner/repo`: la URL de evidencia queda, pero ese item no cuenta (match revisado y descartado).
_EXCLUDED_ID_RE = re.compile(r"!((?:show_hn:\d+|github:[\w.-]+/[\w.-]+))")
# Referencias inequívocas a ids internos de Constellate: "(704)", "(4379, 4709)", "ID:2190", "#900".
_IDEA_REF_RE = re.compile(r"\s*\((?:ID:)?\d{2,5}(?:,\s*(?:ID:)?\d{2,5})*\)|\bID:\d+\b|\s*\(#\d+\)|\s*#\d{2,5}\b")
# Hosts donde un dominio no identifica un producto (no sirven para buscar su Show HN).
_GENERIC_HOSTS = {
    "github.com", "gitlab.com", "medium.com", "youtube.com", "apps.apple.com", "play.google.com", "dev.to",
    "substack.com", "news.ycombinator.com", "twitter.com", "x.com", "arxiv.org", "huggingface.co", "npmjs.com",
    "pypi.org", "docs.google.com", "linkedin.com", "reddit.com", "wikipedia.org", "producthunt.com",
    "techcommunity.microsoft.com", "blog.google", "businesswire.com", "helpnetsecurity.com", "readthedocs.io",
    "github.io", "gitbook.io", "vercel.app", "netlify.app", "herokuapp.com", "pages.dev", "nih.gov",
    "researchgate.net", "springer.com", "sciencedirect.com", "acm.org", "ieee.org", "notion.site", "google.com",
}


def _host(url: str) -> str:
    return (urlparse(url if "://" in url else f"https://{url}").hostname or "").removeprefix("www.")


# Palabras que no identifican un producto: "Cosmos Cloud", "Guardrails AI", "Coder Agent Firewall".
_GENERIC_WORDS = frozenset(
    "ai agent agents cloud core platform official open source app apps inc labs api sdk server service tool tools "
    "framework system llm llms the for of and with in on by to".split()
)


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _name_words(name: str | None) -> list[str]:
    """Palabras del nombre propio del producto, antes de aclaraciones: "NVIDIA Triton — Stable ..." ->
    [nvidia, triton]; "Guild (Authorization + ...)" -> [guild]; "Matrix / Synapse" -> [matrix];
    "Google ADK for Kotlin" -> [google, adk] (la plataforma no es el producto)."""
    head = re.split(r"\s\(|\s[—–/:-]\s|:\s|\sfor\s", (name or "").strip())[0]
    return _words(head)


def _names_product(name_words: list[str], item_id: str, text: str) -> bool:
    """El item es ese producto y no otro de la misma marca o dominio.

    - Repos: la marca tiene que ser un segmento entero del nombre del repo ("agent" no vale para
      magentic-ui, "guild" no vale para guildai) y el repo no puede ser el código del sitio web.
    - Si el nombre trae palabras propias además de la marca ("NVIDIA Triton", "Morph Router"), alguna
      tiene que aparecer en el título/descripción del item; si no, es otro producto de la empresa.
    """
    if not name_words:
        return False
    owner, _, repo = item_id.removeprefix("github:").lower().partition("/") if item_id.startswith("github:") else ("", "", "")
    extra = [w for w in name_words[1:] if w not in _GENERIC_WORDS]
    if repo:
        segments = re.split(r"[-_.]", repo)
        in_name = name_words[0] in segments or "".join(name_words) == "".join(segments)
        # la marca como dueño solo vale si el producto está en el nombre del repo
        # (NVIDIA/triton-inference-server, stanford-crfm/helm; no microsoft/malmo para "Microsoft ExP")
        if not in_name and not (name_words[0] in re.split(r"[-_.]", owner)
                                and any(w in segments or (len(w) > 3 and w in repo) for w in extra)):
            return False
        if "website" in segments or "." in repo:  # matrix-org/matrix.org, w3c/w3c-website
            return False
    if not extra:
        return True
    from gapfinder.leakage import stem, terms  # import local: leakage no depende de real_cases
    found = terms(text) | set(_words(text))
    return any(w in found or stem(w) in found or (len(w) > 3 and w in repo) for w in extra)


def normalize_url(url: str) -> str:
    u = url.strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.split("#")[0].rstrip("/")
    return u.removesuffix(".git")


def github_key(url: str) -> str | None:
    m = re.match(r"github\.com/([^/]+)/([^/?#]+)", normalize_url(url))
    return f"github:{m.group(1)}/{m.group(2)}" if m else None


def site_domain(url: str) -> str | None:
    host = (urlparse(url if "://" in url else f"https://{url}").hostname or "").removeprefix("www.")
    if not host or any(host == g or host.endswith("." + g) for g in _GENERIC_HOSTS):
        return None
    parts = host.split(".")
    # "app.example.co.uk" -> "example.co.uk"; "docs.keygen.sh" -> "keygen.sh"
    two_level = len(parts) > 2 and len(parts[-1]) == 2 and parts[-2] in {"co", "com", "org", "net", "ac", "gov", "edu"}
    return ".".join(parts[-3:] if two_level else parts[-2:])


def clean_explanation(text: str) -> str:
    """Saca referencias inequívocas a ids internos de Constellate; los números sueltos quedan."""
    text = _IDEA_REF_RE.sub("", text)
    return re.sub(r"\s{2,}", " ", text).strip()


class CorpusIndex:
    """Membresía de URLs en el corpus, por búsqueda exacta (no retrieval):
    repo de GitHub, URL exacta, repo cuyo homepage es ese dominio, o Show HN del mismo dominio
    cuyo título menciona el producto. Devuelve siempre el id tal como está en `items`."""

    def __init__(self, conn: sqlite3.Connection, exclude: set[str] | None = None) -> None:
        """exclude: ids que no son del corpus base (p. ej. los agregados por la búsqueda dirigida)."""
        exclude = exclude or set()
        self.by_url: dict[str, str] = {}
        self.github: dict[str, str] = {}  # id en minúsculas -> id real ("github:BerriAI/litellm")
        self.repo_by_homepage: dict[str, list[tuple[int, str]]] = {}
        self.showhn_by_domain: dict[str, list[tuple[str, str]]] = {}
        self.text: dict[str, str] = {}    # título + descripción de los candidatos heurísticos
        self.url_of: dict[str, str] = {}  # id real -> URL del item
        for item_id, url, title, desc, extra, stars in conn.execute(
                "SELECT id, url, title, description, extra, stars FROM items"):
            if item_id in exclude:
                continue
            self.by_url.setdefault(normalize_url(url), item_id)
            self.url_of[item_id] = url
            if item_id.startswith("github:"):
                self.github[item_id.lower()] = item_id
                homepage = json.loads(extra or "{}").get("homepage")
                if homepage and site_domain(homepage):  # descarta hosts compartidos (github.io, etc.)
                    self.repo_by_homepage.setdefault(_host(homepage), []).append((stars or 0, item_id))
                    self.text[item_id] = f"{title} {desc}"
            elif (d := site_domain(url)):
                self.showhn_by_domain.setdefault(d, []).append((item_id, title))
                self.text[item_id] = f"{title} {desc}"

    def resolve_id(self, item_id: str) -> str | None:
        """Id escrito a mano ('github:berriai/LiteLLM', 'show_hn:123') -> id real, o None si no está."""
        if item_id.lower().startswith("github:"):
            return self.github.get(item_id.lower())
        return item_id if item_id in self.url_of else None

    def lookup(self, url: str, name: str | None = None) -> tuple[str | None, str]:
        """(item_id, cómo se resolvió). `name` (nombre del producto) valida los matches por dominio."""
        if (key := github_key(url)):
            return (self.github[key.lower()], "repo") if key.lower() in self.github else (None, "repo fuera del bulk")
        if (item := self.by_url.get(normalize_url(url))):
            return item, "url exacta"
        d, host, words = site_domain(url), _host(url), _name_words(name)
        if d and words:
            # un mismo host puede alojar muchos productos (microsoft.com): siempre exigir el nombre
            for key in (host, d):
                if (repos := [r for r in self.repo_by_homepage.get(key, [])
                              if _names_product(words, r[1], self.text[r[1]])]):
                    return max(repos)[1], f"heurístico, revisar: repo con homepage {key}"
            for item_id, title in self.showhn_by_domain.get(d, []):
                if words[0] in _words(title) and _names_product(words, item_id, self.text[item_id]):
                    return item_id, f"heurístico, revisar: Show HN del dominio {d}: \"{title[:60]}\""
        return None, "sin repo ni Show HN en el corpus"


# --- recolección de veredictos --------------------------------------------------


@dataclass
class Verification:
    verified_by: str            # web | manual | rubric
    verdict: str                # yes | partially | no
    reason: str
    prior_art: list[dict]       # [{name, url, what}]
    detail: str = ""            # modelo/fecha/archivo


@dataclass
class Absence:
    hash: str
    full_hash: str
    title: str
    explanation: str
    runs: list[str] = field(default_factory=list)
    verifications: list[Verification] = field(default_factory=list)


def _scope_hash(c: dict) -> str:
    """Igual que absenceScopeHash en constellate-engine/src/pipeline/inputs.ts."""
    ids = sorted(set(c["idea_ids"]))
    return hashlib.sha256("|".join([c["neighborhood_hash"], c["title"], ",".join(map(str, ids))]).encode()).hexdigest()


def _parse_manual(text: str) -> tuple[str, str, list[dict]]:
    m = re.search(r"COVER THIS GAP\?\s*\**\s*([A-Z]+)\**\s*[—-]*\s*(.*)", text)
    verdict, reason = (m.group(1).lower(), m.group(2).strip()) if m else ("?", "")
    items = []
    for pm in re.finditer(r"\*\*\d+\.\s*(.+?)\s+—\s+(https?://\S+?)\*\*\s*\n- What it does:\s*(.+)", text):
        items.append({"name": pm.group(1), "url": pm.group(2), "what": pm.group(3).strip()})
    return verdict, reason, items


def _parse_rubric(text: str) -> list[tuple[str, str, list[dict]]]:
    runs = []
    for block in re.split(r"^## Run \d+", text, flags=re.MULTILINE)[1:]:
        vm = re.search(r"\*\*Verdict:\s*([A-Z]+)\*\*\s*\n+(.+)", block)
        items = [{"name": n, "url": u, "what": w.strip()}
                 for n, u, w in re.findall(r"^- \[(.+?)\]\((https?://[^)]+)\)\s*—\s*(.+)$", block, re.MULTILINE)]
        if vm:
            runs.append((vm.group(1).lower(), vm.group(2).strip(), items))
    return runs


def collect(root: Path) -> dict[str, Absence]:
    """Todas las absences de las salidas guardadas de Constellate, con sus verificaciones."""
    files = [root / "output.json", *sorted((root / "runs").glob("*.json")),
             *sorted(root.glob(".backups/*.json")), *sorted(root.glob("runs/.backups/*.json"))]
    out: dict[str, Absence] = {}
    by_scope: dict[str, str] = {}
    for f in files:
        d = json.loads(f.read_text())
        gen = (d.get("metadata") or {}).get("generated_at")
        for c in d.get("constellations", []):
            if c.get("constellation_type") != "absence":
                continue
            h = c["neighborhood_hash"][:8]
            a = out.setdefault(h, Absence(h, c["neighborhood_hash"], c["title"], c.get("explanation", "")))
            if gen and gen not in a.runs:
                a.runs.append(gen)
            by_scope[_scope_hash(c)] = h
            if c.get("coverage_verdict"):
                a.verifications.append(Verification(
                    "web", c["coverage_verdict"], c.get("coverage_reason") or "",
                    [{"name": p.get("name"), "url": p.get("url"), "what": p.get("what_it_does", "")}
                     for p in c.get("prior_art") or []], f.name))

    db = sqlite3.connect(f"file:{root / 'constellate.db'}?mode=ro", uri=True)
    try:
        rows = db.execute(
            "SELECT scope_hash, model, created_at, response_json FROM api_call_attempts "
            "WHERE stage='verification' AND status='valid' ORDER BY created_at"
        ).fetchall()
    finally:
        db.close()
    for scope, model, created, resp in rows:
        if scope not in by_scope:
            continue
        r = json.loads(resp)
        out[by_scope[scope]].verifications.append(Verification(
            "web", r.get("verdict", "?"), r.get("reason", ""),
            [{"name": p.get("name"), "url": p.get("url"), "what": p.get("what_it_does", "")} for p in r.get("prior_art", [])],
            f"{model} {created[:10]}"))

    for p in sorted((root / "prior-art").glob("absence-*.md")):
        h = p.stem.split("-")[1][:8]
        if h in out:
            verdict, reason, items = _parse_manual(p.read_text())
            out[h].verifications.append(Verification("manual", verdict, reason, items, f"prior-art/{p.name}"))
    for p in sorted((root / "rubric-test").glob("absence-*.md")):
        h = p.stem.split("-")[1][:8]
        if h in out:
            for i, (verdict, reason, items) in enumerate(_parse_rubric(p.read_text()), 1):
                out[h].verifications.append(Verification("rubric", verdict, reason, items, f"rubric-test/{p.name} run {i}"))

    for a in out.values():  # la misma verificación puede estar en el JSON y en la base
        seen, uniq = set(), []
        for v in a.verifications:
            key = (v.verified_by, v.verdict, tuple(sorted(p["url"] or "" for p in v.prior_art)))
            if key not in seen:
                seen.add(key)
                uniq.append(v)
        a.verifications = uniq
    return out


def proposal(a: Absence) -> str | None:
    verdicts = {v.verdict for v in a.verifications}
    if "yes" in verdicts:
        return "real"
    if "no" in verdicts:
        return "negative"
    if "partially" in verdicts:
        return "partial"
    return None


# --- documento de revisión ----------------------------------------------------


def _github_stars(urls: list[str]) -> dict[str, int | None]:
    """Estrellas de repos que no están en el corpus (para explicar por qué faltan)."""
    headers = {"Accept": "application/vnd.github+json"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    out: dict[str, int | None] = {}
    with httpx.Client(headers=headers, timeout=20) as c:
        for u in urls:
            if key := github_key(u):
                r = c.get(f"https://api.github.com/repos/{key.split(':', 1)[1]}")
                out[u] = r.json().get("stargazers_count") if r.status_code == 200 else None
    return out


def build_candidates(conn: sqlite3.Connection, root: Path, extra_notes: Path | None = None) -> tuple[str, dict]:
    absences = collect(root)
    verified = [a for a in absences.values() if a.verifications]
    by_source = {s: sum(any(v.verified_by == s for v in a.verifications) for a in verified)
                 for s in ("manual", "rubric", "web")}
    order = {"real": 0, "negative": 1, "partial": 2, None: 3}
    verified.sort(key=lambda a: (not any(v.verified_by == "manual" for v in a.verifications),
                                 not any(v.verified_by == "rubric" for v in a.verifications),
                                 order[proposal(a)], a.title))
    notes = {}
    if extra_notes and extra_notes.exists():
        for line in extra_notes.read_text().splitlines():
            if " | " in line and not line.startswith("#"):
                h, found, strength = (s.strip() for s in line.split(" | ", 2))
                notes[h] = (found, strength)

    idx = CorpusIndex(conn)
    missing_gh = sorted({p["url"] for a in verified if proposal(a) == "real" for v in a.verifications
                         for p in v.prior_art if p["url"] and github_key(p["url"]) and idx.lookup(p["url"], p.get("name"))[0] is None})
    stars = _github_stars(missing_gh)

    lines = [
        "# Candidatos: absences verificadas de Constellate\n",
        "Veredictos de Constellate: `web` (Claude + búsqueda web), `manual` (prior-art/*.md), `rubric` (rubric-test/*.md).",
        "Propuesta: `yes` -> real, `no` -> negativo, solo `partially` -> parcial.",
        "Marcá `confirmado: real`, `confirmado: negativo` o `confirmado: descartar`. Para `real`, dejá en",
        "`esperado:` las URLs que cuentan como \"lo que ya existía\" (podés editar la lista propuesta);",
        "también acepta ids del corpus (`show_hn:123`, `github:owner/repo`) para fijar un item concreto,",
        "y `!github:owner/repo` para descartar un match revisado (la URL queda, el item no cuenta).",
        "Las parciales vienen con `confirmado: parcial` y todas sus URLs de evidencia en `esperado:`;",
        "cambiá a `descartar` (o recortá `esperado:`) las que no sirvan.",
        "Corpus: ✓ = está; ✗ = no está hoy. \"repo\" y \"url exacta\" son matches exactos; los marcados",
        "\"heurístico, revisar\" salen del dominio (homepage de un repo o Show HN con el nombre del producto)",
        "y pueden equivocarse. La búsqueda dirigida (Fase 2) todavía no existe: los ✗ se re-evalúan cuando esté.\n",
        f"Verificadas: {len(verified)} absences (manual {by_source['manual']}, rúbrica {by_source['rubric']}, "
        f"web {by_source['web']}; una absence puede tener varias).\n",
    ]
    stats = {"verified": len(verified), "by_source": by_source, "real": 0, "negative": 0, "partial": 0, "none": 0,
             "real_without_corpus": [], "partial_without_corpus": []}
    for n, a in enumerate(verified, 1):
        prop = proposal(a)
        stats[prop or "none"] += 1
        sources = ", ".join(sorted({v.verified_by for v in a.verifications}))
        lines.append(f"## {n} · {a.hash} · {a.title}\n")
        lines.append(f"- Verificada por: {sources} · corridas: {', '.join(r[:10] for r in a.runs) or 'snapshot sin fecha'}")
        lines.append(f"- Idea: {clean_explanation(a.explanation)[:500]}")
        lines.append("- Veredictos:")
        for v in a.verifications:
            lines.append(f"  - **{v.verdict}** ({v.verified_by}, {v.detail}): {v.reason[:300]}")
        urls: dict[str, str] = {}
        names: dict[str, str] = {}
        for v in a.verifications:
            for p in v.prior_art:
                if p.get("url") and p["url"] not in urls:
                    urls[p["url"]] = f"{p.get('name')}: {(p.get('what') or '')[:160]}"
                    names[p["url"]] = p.get("name") or ""
        in_corpus, heuristic = [], []
        if urls:
            lines.append("- Evidencia (prior art citado por Constellate):")
            for u, desc in list(urls.items())[:10]:
                item, how = idx.lookup(u, names[u])
                if item:
                    (heuristic if how.startswith("heurístico") else in_corpus).append(u)
                    tag = f"✓ {item} ({how})"
                else:
                    extra = f", ★{stars[u]}" if stars.get(u) is not None else ""
                    tag = f"✗ {how}{extra}"
                lines.append(f"  - {u} — {desc} [{tag}]")
        if a.hash in notes:
            lines.append(f"- Búsqueda propia (sep-2026, complementaria): {notes[a.hash][0]} [{notes[a.hash][1]}]")
        if prop in ("real", "partial") and not in_corpus + heuristic:
            stats[f"{prop}_without_corpus"].append(a.hash)
        ranked = in_corpus + heuristic + [u for u in urls if u not in in_corpus + heuristic]
        proposed = ranked[:4] if prop == "real" else ranked if prop == "partial" else []
        confirmed = KIND_LABEL["partial"] if prop == "partial" else ""
        lines += ["", f"propuesta: {KIND_LABEL.get(prop, '—')}",
                  f"{EXPECTED_PREFIX} {' '.join(proposed)}", f"{CONFIRM_PREFIX} {confirmed}", "", "---\n"]
    return "\n".join(lines) + "\n", stats


# --- import -------------------------------------------------------------------

_BLOCK_HEADER = re.compile(r"^## \d+ · ([0-9a-f]{8}) · (.+)$", re.MULTILINE)


def parse_candidates(text: str) -> tuple[list[dict], list[str], list[str]]:
    """(marcados como {hash, kind, expected_urls, expected_ids, excluded_ids}, descartados, sin marcar)."""
    marked, discarded, pending = [], [], []
    for block in re.split(r"^---\s*$", text, flags=re.MULTILINE):
        m = _BLOCK_HEADER.search(block)
        if not m:
            continue
        h = m.group(1)
        cm = re.search(rf"^{CONFIRM_PREFIX}[ \t]*(\S*)", block, re.MULTILINE)
        answer = (cm.group(1) if cm else "").strip().lower()
        em = re.search(rf"^{EXPECTED_PREFIX}(.*)$", block, re.MULTILINE)
        urls = _URL_RE.findall(em.group(1)) if em else []
        ids = _ITEM_ID_RE.findall(_URL_RE.sub(" ", em.group(1))) if em else []
        excluded = _EXCLUDED_ID_RE.findall(em.group(1)) if em else []
        if not answer:
            pending.append(h)
        elif answer not in CONFIRM_VALUES:
            raise ValueError(f"{h}: 'confirmado: {answer}' no es real | negativo | parcial | descartar")
        elif CONFIRM_VALUES[answer] is None:
            discarded.append(h)
        else:
            marked.append({"hash": h, "kind": CONFIRM_VALUES[answer], "expected_urls": urls, "expected_ids": ids,
                           "excluded_ids": excluded})
    return marked, discarded, pending


def import_candidates(conn: sqlite3.Connection, candidates: Path, root: Path, cases_path: Path) -> dict:
    """Reemplaza en known_cases.json los casos de Constellate por los marcados en la hoja."""
    marked, discarded, pending = parse_candidates(candidates.read_text())
    absences = collect(root)
    # los esperados se resuelven contra el corpus base: los items de la búsqueda dirigida no cuentan
    has_targeted = conn.execute("SELECT 1 FROM sqlite_master WHERE name = 'targeted'").fetchone()
    targeted = {r[0] for r in conn.execute("SELECT item_id FROM targeted")} if has_targeted else set()
    idx = CorpusIndex(conn, exclude=targeted)
    new, outside = [], []
    for c in marked:
        a = absences[c["hash"]]
        names = {p["url"]: p.get("name") for v in a.verifications for p in v.prior_art if p.get("url")}
        case = {
            "id": f"{CASE_PREFIX[c['kind']]}-{c['hash']}",
            "kind": c["kind"],
            "title": re.sub(r"^Missing:\s*", "", a.title),
            "description": clean_explanation(a.explanation),
            "verified_by": sorted({v.verified_by for v in a.verifications}),
            "meta": {"source": SOURCE_TAG, "hash": c["hash"], "runs": a.runs,
                     "verdicts": sorted({f"{v.verified_by}:{v.verdict}" for v in a.verifications})},
        }
        if c["kind"] in ("real", "partial"):
            if not c["expected_urls"] and not c["expected_ids"]:
                raise ValueError(f"{c['hash']}: marcado {c['kind']} sin URLs ni ids en 'esperado:'")
            found = [idx.lookup(u, names.get(u)) for u in c["expected_urls"]]
            for raw in c["expected_ids"]:  # ids escritos a mano: revisados, cuentan como exactos
                if not (real := idx.resolve_id(raw)):
                    raise ValueError(f"{c['hash']}: {raw} no está en el corpus")
                found.append((real, "id"))
            excluded = {(idx.resolve_id(x) or x) for x in c["excluded_ids"]}
            item_ids = list(dict.fromkeys(i for i, _ in found if i and i not in excluded))
            exact = {i for i, how in found if i and not how.startswith("heurístico")}
            if not item_ids:
                outside.append(c["hash"])
            urls = list(c["expected_urls"])
            urls += [idx.url_of[i] for i, how in found if how == "id" and idx.url_of[i] not in urls]
            case["expected_urls"] = urls
            case["expected_item_ids"] = item_ids
            # match por dominio, no revisado a mano en las parciales: el eval reporta recall con y sin ellos
            case["meta"]["heuristic_item_ids"] = [i for i in item_ids if i not in exact]
        new.append(case)
    existing = json.loads(cases_path.read_text()) if cases_path.exists() else []
    notes = {c["id"]: c["label_note"] for c in existing if c.get("label_note")}
    for c in new:  # anotaciones manuales sobre la etiqueta: sobreviven al re-import
        if c["id"] in notes:
            c["label_note"] = notes[c["id"]]
    kept = [c for c in existing if c.get("meta", {}).get("source") != SOURCE_TAG]
    cases_path.write_text(json.dumps(kept + new, indent=2, ensure_ascii=False) + "\n")
    return {**{k: sum(c["kind"] == k for c in new) for k in ("real", "negative", "partial")},
            "outside": outside, "discarded": discarded, "pending": pending}
