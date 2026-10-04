"""Filtro de fuga léxica para casos sintéticos.

Una necesidad escrita mirando el item puede copiarle términos distintivos ("elasticsearch",
"mixpanel") y volver el retrieval trivial. Se marca para reescribir si comparte con
título+texto del item:
- >= 2 términos distintivos (idf >= DISTINCTIVE_IDF, aparecen en <= 1% de los documentos), o
- cualquier término raro (idf >= RARE_IDF, <= 0,05% de los documentos).
El idf se calcula sobre título+descripción de todo el corpus y se cachea en disco.
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

DISTINCTIVE_IDF = math.log(100)
RARE_IDF = math.log(2000)

STOPWORDS = frozenset("""
a about above after again against all also am an and any are as at be because been before being below
between both but by can could did do does doing down during each easy easily even every few for from
further get gets getting got had has have having he her here hers him his how i if in into is it its
itself just let lets like make makes making me more most much must my need needs new no nor not now of
off on once one only or other our ours out over own per quick quickly really same she should simple
simply so some such than that the their theirs them then there these they this those through to too
under until up us use used uses using very via want wants was way we were what when where which while
who whom why will with within without would you your yours
""".split())

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#]*")
_SUFFIXES = ("ations", "ation", "ings", "ing", "ers", "er", "ies", "es", "ed", "ly", "s")


def stem(word: str) -> str:
    for suf in _SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 4:
            return word[: -len(suf)] + ("y" if suf == "ies" else "")
    return word


def terms(text: str) -> set[str]:
    return {stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and not t.isdigit() and len(t) > 1}


@dataclass(frozen=True, slots=True)
class Idf:
    n_docs: int
    df: dict[str, int]

    def __call__(self, term: str) -> float:
        return math.log(self.n_docs / max(self.df.get(term, 0), 1))


def load_idf(conn: sqlite3.Connection, cache: Path, refresh: bool = False) -> Idf:
    if cache.exists() and not refresh:
        data = json.loads(cache.read_text())
        return Idf(data["n_docs"], data["df"])
    df: Counter[str] = Counter()
    n = 0
    for title, desc in conn.execute("SELECT title, description FROM items"):
        df.update(terms(f"{title} {desc}"))
        n += 1
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"n_docs": n, "df": dict(df)}))
    return Idf(n, dict(df))


@dataclass(frozen=True, slots=True)
class Leak:
    distinctive: list[tuple[str, float]]  # términos compartidos con idf >= DISTINCTIVE_IDF
    rare: list[tuple[str, float]]         # subconjunto con idf >= RARE_IDF

    @property
    def flagged(self) -> bool:
        return len(self.distinctive) >= 2 or bool(self.rare)


def check(need: str, item_text: str, idf: Idf) -> Leak:
    shared = terms(need) & terms(item_text)
    scored = sorted(((t, round(idf(t), 1)) for t in shared), key=lambda x: -x[1])
    return Leak([s for s in scored if s[1] >= DISTINCTIVE_IDF], [s for s in scored if s[1] >= RARE_IDF])
