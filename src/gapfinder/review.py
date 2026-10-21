"""`gapfinder review`: un solo menú para todas las colas de revisión humana.

Colas:
  a) etiquetas de reales: los positivos reales del piloto que juzgaste "no" (pilot.interactive_labels)
  b) holdout temporal, por idea: las 20 "no" en orden al azar (semilla fija); las de "ya construido"/"revisar"
     quedan como opcionales al final
  c) Ask HN, extracción: confirmar si es un pedido real (s/n) y la etiqueta de los comentarios (e/p/n/?)
  d) Fase 4, pares: por idea, la decisión del sistema y el mejor candidato (top-3 si dijo "no")
  e) candidatos a hueco: los huecos fuertes (y la zona gris al final), por pedido viendo sus 3 mejores candidatos;
     precisión = hueco real / juzgadas, con IC de Wilson (data/eval/gap_review_result.md)

Todas guardan cada respuesta al instante en un jsonl (la última respuesta por clave gana) y se retoman
donde quedaste; q guarda y vuelve al menú. Una cola cuyo paso todavía no terminó aparece como pendiente.
"""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import textwrap
from datetime import datetime, timezone
from pathlib import Path

from gapfinder import askhn, pilot
from gapfinder.verify import Pair, load_done

EXTRACT_REVIEW_PATH = Path("data/eval/askhn_extract_review_human.jsonl")
PHASE4_REVIEW_PATH = Path("data/eval/phase4_review_human.jsonl")
EXTRACT_LABELS = {"e": "existe", "p": "parcial", "n": "no existe", "?": "incierto"}
PHASE4_LEGEND = "[s] equivalente  [p] parcial  [n] no es lo mismo  [?] no sé"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- b) holdout temporal, por idea ----------------------------------------------------------------------

HOLDOUT_IDEAS_PATH = Path("data/eval/holdout_review_ideas.jsonl")
HOLDOUT_RESULT_PATH = Path("data/eval/holdout_review_result.md")
HOLDOUT_SEED = 5
HOLDOUT_KEYS = {"1": "equivalente (candidato 1)", "2": "equivalente (candidato 2)", "3": "equivalente (candidato 3)",
                "p": "alguno es parcial", "n": "ninguno: hueco en T", "?": "no sé"}


def holdout_ideas() -> tuple[list[dict], list[dict]]:
    """(principales, opcionales). Principales: las ideas con decisión "no", barajadas con semilla fija (si cortás
    a las 10, la muestra sigue siendo aleatoria). Opcionales: ya construido / revisar, después. Cada idea con
    sus 3 mejores candidatos por P(núcleo)."""
    import random

    from gapfinder import holdout

    chosen = json.loads((holdout.DIR / "selected.json").read_text())
    ideas = {i["item_id"]: i for i in json.loads((holdout.DIR / "ideas.json").read_text())["ideas"]}
    cand = json.loads((holdout.DIR / "candidates.json").read_text())
    queries = json.loads((holdout.DIR / "llm_queries.json").read_text())
    ver = load_done("jev_holdout")
    rows = []
    for iid in chosen:
        cid = f"hold-{iid.split(':')[1]}"
        scored = sorted((i for i in cand.get(cid, []) if (cid, i) in ver), key=lambda i: -ver[(cid, i)].core)
        if scored:
            rows.append({"case_id": cid, "idea": ideas[iid], "need": queries[cid]["query_core"],
                         "top": [(i, ver[(cid, i)].core) for i in scored[:3]],
                         "decision": holdout.decide(ver[(cid, scored[0])].core)})
    main = sorted([r for r in rows if r["decision"] == "no"], key=lambda r: r["case_id"])
    random.Random(HOLDOUT_SEED).shuffle(main)
    optional = sorted([r for r in rows if r["decision"] != "no"], key=lambda r: r["case_id"])
    random.Random(HOLDOUT_SEED).shuffle(optional)
    return main, optional


def _from_pairs(rows: list[dict]) -> dict[str, str]:
    """Respuestas del formato anterior (por par) convertidas a por idea: un "s" decide la idea como equivalente
    (con el número de ese candidato) aunque falten pares; si no, solo ideas con sus 3 candidatos respondidos:
    algún "p" -> p; todos "n" -> n; si no -> ?."""
    pairs = pilot.load_human(pilot.HOLDOUT_REVIEW_PATH)
    out = {}
    for r in rows:
        labels = [pairs.get((r["case_id"], i)) for i, _ in r["top"]]
        if "s" in labels:
            out[r["case_id"]] = str(labels.index("s") + 1)
        elif len(labels) == 3 and all(labels):
            out[r["case_id"]] = "p" if "p" in labels else "n" if all(x == "n" for x in labels) else "?"
    return out


def load_holdout_answers(rows: list[dict]) -> dict[str, str]:
    """Convertidas del formato por par + respuestas por idea (estas pisan; la última por idea gana)."""
    out = _from_pairs(rows)
    if HOLDOUT_IDEAS_PATH.exists():
        for line in HOLDOUT_IDEAS_PATH.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[d["case_id"]] = d["label"]
    return out


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if not n:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return (max(0.0, mid - half), min(1.0, mid + half))


def write_holdout_result(main: list[dict], optional: list[dict], answers: dict[str, str]) -> str:
    def block(rows: list[dict], title: str) -> list[str]:
        got = [answers[r["case_id"]] for r in rows if r["case_id"] in answers]
        judged = [x for x in got if x != "?"]
        n = len(judged)
        eq = sum(x in "123" for x in judged)
        gap = sum(x == "n" for x in judged)
        par = sum(x == "p" for x in judged)

        def fmt(k):
            lo, hi = wilson(k, n)
            return f"{k}/{n} = {k / n:.0%} (IC 95%: {lo:.0%}–{hi:.0%})" if n else "–"
        return [f"## {title}\n", f"Respondidas {len(got)}/{len(rows)}; juzgadas (sin \"no sé\") **n = {n}**; no sé: {len(got) - n}.\n",
                f"- **Hueco en T** (ningún candidato es equivalente): {fmt(gap)}",
                f"- **Equivalente real anterior a T** (1/2/3): {fmt(eq)}",
                f"- Alguno parcial: {fmt(par)}", ""]
    L = ["# Holdout temporal: adjudicación humana por idea\n",
         "Una respuesta por idea viendo sus 3 mejores candidatos (P(núcleo) de Jev): 1/2/3 = ese candidato es un equivalente real "
         "anterior a T; p = alguno es parcial; n = ninguno (hueco en T dentro del corpus); ? = no sé. Intervalos de Wilson al 95%. "
         "Orden al azar con semilla fija: un corte temprano sigue siendo una muestra aleatoria. Incluye respuestas del formato "
         "anterior por par convertidas (un \"s\" decide la idea; si no, solo ideas con sus 3 pares respondidos).\n"]
    L += block(main, f"Ideas con decisión \"no\" del sistema ({len(main)}): ¿hueco real en T?")
    L += block(optional, f"Opcionales: ideas \"ya construido\" / \"revisar\" ({len(optional)})")
    L += ["## Respuestas\n", "| idea | decisión del sistema | respuesta |", "|---|---|---|"]
    for r in main + optional:
        if r["case_id"] in answers:
            L.append(f"| `{r['case_id']}` {r['idea']['title'][:70]} | {r['decision']} | {HOLDOUT_KEYS[answers[r['case_id']]]} |")
    text = "\n".join(L) + "\n"
    HOLDOUT_RESULT_PATH.write_text(text)
    return text


def interactive_holdout(conn: sqlite3.Connection, getkey=pilot._getkey, out=print) -> dict:
    import webbrowser

    from gapfinder.text import get_texts

    main, optional = holdout_ideas()
    answers = load_holdout_answers(main + optional)
    ids = sorted({i for r in main + optional for i, _ in r["top"]})
    texts = get_texts(conn, ids)
    meta = {i: (u, c) for i, u, c in conn.execute(
        f"SELECT id, url, created_at FROM items WHERE id IN ({','.join('?' * len(ids))})", ids)}
    width = min(shutil.get_terminal_size((100, 30)).columns, 110)

    def one_line(text: str, n: int) -> str:
        text = re.sub(r"\s+", " ", text or "").strip()
        return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"

    HOLDOUT_IDEAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    done_now = 0
    quit_ = False
    for section, rows in (("principal", main), ("opcional", optional)):
        for r in rows:
            if r["case_id"] in answers:
                continue
            if section == "opcional" and not any(o["case_id"] in answers for o in optional):
                out("\nTerminaste las 20 ideas \"no\". Siguen las opcionales (ya construido / revisar). "
                    "[c] continuar  [q] volver al menú")
                k = getkey()
                while k not in ("c", "q"):
                    k = getkey()
                if k == "q":
                    quit_ = True
                    break
            sec_rows = main if section == "principal" else optional
            n_done = sum(x["case_id"] in answers for x in sec_rows)
            idea = r["idea"]
            out("\033[2J\033[H" if getkey is pilot._getkey else "", end="")
            out(f"[{n_done + 1}/{len(sec_rows)}{' opcional' if section == 'opcional' else ''}]  {r['case_id']}  ·  "
                f"decisión del sistema: {r['decision']}")
            out(f"IDEA (posterior a T, {idea['created_at'][:10]}): {idea['title']}")
            for line in textwrap.wrap(one_line(r["need"], 2 * (width - 10)), width - 2):
                out("  " + line)
            out("")
            for n, (i, core) in enumerate(r["top"], 1):
                url, created = meta.get(i, ("", "?"))
                out(f"{n}) {texts[i].title[:width - 30]}  ·  {created[:10]}  ·  Jev {core:.2f}")
                out(f"   {one_line(texts[i].body, width - 4)}")
                out(f"   {url}")
            out("\n[1/2/3] ese candidato es equivalente real anterior a T  [p] alguno parcial  [n] ninguno (hueco)  "
                "[?] no sé  [o]+número abrir URL  [q] guardar y volver")
            while True:
                k = getkey()
                if k == "o":
                    m = getkey()
                    if m in ("1", "2", "3") and len(r["top"]) >= int(m):
                        webbrowser.open(meta.get(r["top"][int(m) - 1][0], ("",))[0])
                    continue
                if k in HOLDOUT_KEYS and (k not in "123" or len(r["top"]) >= int(k)) or k == "q":
                    break
            if k == "q":
                quit_ = True
                break
            rec = {"case_id": r["case_id"], "label": k, "at": _now()}
            if k in "123":
                rec["item_id"] = r["top"][int(k) - 1][0]
            with HOLDOUT_IDEAS_PATH.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            answers[r["case_id"]] = k
            done_now += 1
        if quit_:
            break
    text = write_holdout_result(main, optional, answers)
    out("\n" + text.split("## Respuestas")[0])
    out(f"Guardado en {HOLDOUT_IDEAS_PATH}; resultado en {HOLDOUT_RESULT_PATH}")
    return {"respondidas_ahora": done_now, "principales": f"{sum(r['case_id'] in answers for r in main)}/{len(main)}"}


# --- c) extracción de Ask HN ----------------------------------------------------------------------------


def load_extract_human(path: Path | None = None) -> dict[str, dict]:
    path = path or EXTRACT_REVIEW_PATH
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[d["ask_id"]] = d
    return out


def extract_queue() -> list[str] | None:
    """Asks con extracción: primero los elegidos para la Fase 4, después los pedidos según el LLM, al final
    el resto. None si la extracción todavía no corrió."""
    ext = askhn.load_extractions()
    if not ext:
        return None
    sel = askhn.load_selected()
    rest = sorted(ext, key=lambda a: (not ext[a].get("es_pedido_de_herramienta"), a))
    return [a for a in sel if a in ext] + [a for a in rest if a not in set(sel)]


def interactive_extract(getkey=pilot._getkey, out=print) -> dict:
    queue = extract_queue() or []
    asks, ext = askhn.load_asks(), askhn.load_extractions()
    human = load_extract_human()
    width = min(shutil.get_terminal_size((100, 30)).columns, 110)
    sel = set(askhn.load_selected())

    def wrap(text: str, limit: int | None = None) -> list[str]:
        text = re.sub(r"\s+", " ", text or "").strip()
        if limit and len(text) > limit:
            text = text[:limit].rsplit(" ", 1)[0] + " …"
        return textwrap.wrap(text, width - 12) or [""]

    def ask_key(prompt: str, allowed: str, a: dict) -> str:
        out(prompt)
        while True:
            k = getkey()
            if k == "o":
                import webbrowser
                webbrowser.open(a["hn_url"])
                continue
            if k == "m":
                out("\n--- texto completo del Ask ---")
                for line in wrap(a.get("text", "")):
                    out("           " + line)
                out("---")
                continue
            if k in allowed or k == "q":
                return k

    EXTRACT_REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    done_now = 0
    for aid in queue:
        if aid in human:
            continue
        a, e = asks.get(aid, {}), ext[aid]
        out("\033[2J\033[H" if getkey is pilot._getkey else "", end="")
        out(f"[{len(human) + 1}/{len(queue)}]  Ask HN {aid}  ·  {a.get('created_at', '')[:10]}  ·  "
            f"{a.get('points', '?')} pts  ·  {a.get('num_comments', '?')} comentarios" + ("  ·  elegido Fase 4" if aid in sel else ""))
        out("TÍTULO:    " + "\n           ".join(wrap(a.get("title", ""))))
        out("TEXTO:     " + "\n           ".join(wrap(a.get("text", "") or "(sin texto)", 500)))
        out(f"           {a.get('hn_url', '')}")
        out("")
        out(f"LLM:       pedido de herramienta = {'sí' if e.get('es_pedido_de_herramienta') else 'no'}   ·   "
            f"etiqueta comentarios = {e.get('etiqueta_comentarios', '?')}")
        out("IDEA:      " + "\n           ".join(wrap(e.get("idea", ""))))
        tools = e.get("herramientas_sugeridas", [])
        out(f"SUGERIDAS: {len(tools)}" + ("" if tools else " (ninguna)"))
        for t in tools[:8]:
            corpus = "en corpus" if t.get("corpus_ids") else "no en corpus"
            out(f"           - {t.get('nombre', '?')} [{t.get('relacion', '?')}] {t.get('url') or ''} ({corpus})")
        if len(tools) > 8:
            out(f"           … y {len(tools) - 8} más")
        for s in e.get("senales_no_existe", [])[:3]:
            out("NO EXISTE: " + "\n           ".join(wrap(s, 200)))
        out("")
        k1 = ask_key("¿Es un pedido real de herramienta?  [s] sí  [n] no   ([m] texto completo  [o] abrir  [q] guardar y volver)", "sn", a)
        if k1 == "q":
            break
        k2 = None
        if k1 == "s":
            k2 = ask_key("Etiqueta según los comentarios:  [e] existe  [p] parcial  [n] no existe  [?] incierto   ([q] volver)", "epn?", a)
            if k2 == "q":
                break
        with EXTRACT_REVIEW_PATH.open("a") as f:
            f.write(json.dumps({"ask_id": aid, "is_request": k1, "label": k2, "at": _now()}) + "\n")
        human[aid] = {"is_request": k1, "label": k2}
        done_now += 1
    got = load_extract_human()
    judged = [a for a in queue if a in got]
    agree_req = sum((got[a]["is_request"] == "s") == bool(ext[a].get("es_pedido_de_herramienta")) for a in judged)
    lab_map = {"e": "existe", "p": "parcial", "n": "no_existe", "?": "incierto"}
    lab_judged = [a for a in judged if got[a]["label"] and ext[a].get("es_pedido_de_herramienta")]
    agree_lab = sum(lab_map[got[a]["label"]] == ext[a].get("etiqueta_comentarios") for a in lab_judged)
    out(f"\nRevisados {len(judged)}/{len(queue)}. Acuerdo con el LLM: pedido {agree_req}/{len(judged)}, "
        f"etiqueta {agree_lab}/{len(lab_judged)}. Guardado en {EXTRACT_REVIEW_PATH}")
    return {"respondidos_ahora": done_now, "total": len(judged), "asks": len(queue)}


# --- d) pares de la Fase 4 ------------------------------------------------------------------------------


def phase4_queue(conn: sqlite3.Connection, with_pairs: bool = True):
    """Para ideas "ya construido"/"revisar": su mejor candidato; para "no": sus 3 mejores. Solo ideas con el
    top-1000 verificado completo. Orden: "no", revisar, ya construido. Devuelve (keys, pares, notas,
    veredictos, casos) o None si todavía no hay ninguna idea verificada completa."""
    from gapfinder import holdout

    sel, ext, asks = askhn.load_selected(), askhn.load_extractions(), askhn.load_asks()
    if not sel or not askhn.CANDIDATES.exists() or not askhn.QUERIES.exists():
        return None
    cand = json.loads(askhn.CANDIDATES.read_text())
    queries = json.loads(askhn.QUERIES.read_text())
    ver = load_done(askhn.VERDICTS)
    rows = []
    order = {"no": 0, "revisar": 1, "ya construido": 2}
    for aid in sel:
        cid = askhn.case_id(aid)
        items = cand.get(cid, [])
        if not items or any((cid, i) not in ver for i in items):
            continue
        scored = sorted(items, key=lambda i: -ver[(cid, i)].core)
        decision = holdout.decide(ver[(cid, scored[0])].core)
        rows.append((order[decision], aid, decision, scored[:3] if decision == "no" else scored[:1], items))
    if not rows:
        return None
    rows.sort(key=lambda r: r[0])
    keys = [(askhn.case_id(aid), i) for _, aid, _, picked, _ in rows for i in picked]
    if not with_pairs:
        return keys
    created = dict(conn.execute(f"SELECT id, created_at FROM items WHERE id IN ({','.join('?' * len(keys))})",
                                [k[1] for k in keys]))
    notes, cases = {}, []
    for _, aid, decision, picked, items in rows:
        a, e, cid = asks.get(aid, {}), ext.get(aid, {}), askhn.case_id(aid)
        cases.append({"id": cid, "kind": "askhn", "title": a.get("title", "")})
        sug = []
        for t in e.get("herramientas_sugeridas", []):
            hit = [i for i in t.get("corpus_ids", []) if i in items]
            if hit:
                i = min(hit, key=items.index)
                sug.append(f"{t['nombre']} rank {items.index(i) + 1} núcleo {ver[(cid, i)].core:.2f}")
            elif t.get("corpus_ids"):
                pre = any(c < a.get("created_at", "") for c in t.get("corpus_created", {}).values())
                sug.append(f"{t['nombre']} " + ("fuera del top-1000" if pre else "en corpus pero posterior al Ask"))
        for i in picked:
            notes[(cid, i)] = (f"(Ask {a.get('created_at', '')[:10]} {a.get('hn_url', '')} | decisión: {decision} | "
                               f"comentarios: {e.get('etiqueta_comentarios', '?')} | candidato creado: {created.get(i, '?')[:10]}"
                               + (f" | sugeridas: {'; '.join(sug)}" if sug else "") + ")")
    pairs = {(p.case_id, p.item_id): p for p in _pairs(conn, keys, queries)}
    return keys, [pairs[k] for k in keys], notes, ver, cases


def _pairs(conn: sqlite3.Connection, keys: list[tuple[str, str]], queries: dict) -> list[Pair]:
    from gapfinder.text import get_texts
    from gapfinder.verify import CANDIDATE_CHARS

    texts = get_texts(conn, sorted({i for _, i in keys}))
    return [Pair(cid, queries[cid]["query_core"], i, texts[i].title, texts[i].body[:CANDIDATE_CHARS]) for cid, i in keys]


def interactive_phase4(conn: sqlite3.Connection, getkey=pilot._getkey, out=print) -> dict:
    q = phase4_queue(conn)
    if q is None:
        out("Fase 4: todavía no hay ideas verificadas.")
        return {}
    keys, queue, notes, ver, cases = q
    done = pilot.review_loop(conn, cases, queue, len(queue), {"Jev": ver}, PHASE4_REVIEW_PATH, notes,
                             getkey=getkey, out=out, legend=PHASE4_LEGEND)
    got = pilot.load_human(PHASE4_REVIEW_PATH)
    out(f"\nGuardado en {PHASE4_REVIEW_PATH}: {sum(k in got for k in keys)}/{len(keys)}")
    return {"respondidos_ahora": done, "pares": len(keys)}


# --- e) candidatos a hueco: huecos fuertes y zona gris --------------------------------------------------

GAPS_REVIEW_PATH = Path("data/eval/gap_review_human.jsonl")
GAPS_RESULT_PATH = Path("data/eval/gap_review_result.md")
GAPS_SEED = 7
GAPS_KEYS = {"n": "hueco real", "1": "equivalente (candidato 1)", "2": "equivalente (candidato 2)",
             "3": "equivalente (candidato 3)", "x": "existe fuera de los candidatos", "p": "algo parcial",
             "s": "no es un pedido de software", "?": "no sé"}


def gap_queue() -> tuple[list[dict], list[dict]]:
    """(huecos fuertes, zona gris) de `gaps.tiered_rows`, cada uno barajado con semilla fija (un corte temprano
    sigue siendo una muestra aleatoria). Cada fila con sus 3 mejores candidatos por P(núcleo)."""
    import random

    from gapfinder import gaps

    rows = gaps.tiered_rows()
    out = []
    for t in ("fuerte", "gris"):
        rs = sorted((r for r in rows if r["tier"] == t), key=lambda r: r["id"])
        random.Random(GAPS_SEED).shuffle(rs)
        out.append(rs)
    return out[0], out[1]


def load_gap_answers(path: Path | None = None) -> dict[str, dict]:
    path = path or GAPS_REVIEW_PATH
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                out[d["case_id"]] = d
    return out


def gap_metrics(labels: list[str]) -> dict:
    """Precisión de la lista de huecos sobre las respuestas juzgadas (sin "no sé"): hueco real / juzgadas, con IC de
    Wilson al 95%, y el desglose de los que no son hueco."""
    judged = [x for x in labels if x != "?"]
    n = len(judged)
    count = {"hueco": sum(x == "n" for x in judged), "equivalente": sum(x in ("1", "2", "3") for x in judged),
             "fuera": sum(x == "x" for x in judged), "parcial": sum(x == "p" for x in judged),
             "no_software": sum(x == "s" for x in judged)}
    return {"respondidas": len(labels), "juzgadas": n, "no_se": len(labels) - n, **count,
            "precision": count["hueco"] / n if n else None, "ic": wilson(count["hueco"], n)}


def write_gap_result(strong: list[dict], grey: list[dict], answers: dict[str, dict]) -> str:
    def block(rows: list[dict], title: str) -> list[str]:
        m = gap_metrics([answers[r["id"]]["label"] for r in rows if r["id"] in answers])
        n = m["juzgadas"]

        def fmt(k: int) -> str:
            lo, hi = wilson(k, n)
            return f"{k}/{n} = {k / n:.0%} (IC 95%: {lo:.0%}–{hi:.0%})" if n else "–"
        return [f"## {title}\n", f"Respondidas {m['respondidas']}/{len(rows)}; juzgadas (sin \"no sé\") **n = {n}**; "
                f"no sé: {m['no_se']}.\n",
                f"- **Precisión (hueco real)**: {fmt(m['hueco'])}",
                f"- Equivalente entre los 3 candidatos (error del verificador): {fmt(m['equivalente'])}",
                f"- Existe fuera de los candidatos (cobertura del corpus o del retrieval): {fmt(m['fuera'])}",
                f"- Algo parcial: {fmt(m['parcial'])}",
                f"- No es un pedido de software (se le escapó al filtro): {fmt(m['no_software'])}", ""]
    L = ["# Candidatos a hueco: adjudicación humana\n",
         "Una respuesta por pedido viendo sus 3 mejores candidatos (P(núcleo) de Jev) y el hilo de Ask HN: n = hueco real "
         "(nada de lo que ves ni de lo que conocés lo resuelve antes del Ask); 1/2/3 = ese candidato es equivalente; x = existe "
         "algo equivalente fuera de los candidatos; p = algo parcial; s = no es un pedido de software; ? = no sé. Precisión = "
         "hueco real / juzgadas; intervalos de Wilson al 95%. Orden al azar con semilla fija dentro de cada nivel. Niveles de "
         "`data/eval/gap_candidates.md`.\n"]
    L += block(strong, f"Huecos fuertes ({len(strong)})")
    L += block(grey, f"Zona gris ({len(grey)})")
    L += ["## Respuestas\n", "| pedido | nivel | mejor | respuesta | nota |", "|---|---|---|---|---|"]
    for r in strong + grey:
        if r["id"] in answers:
            a = answers[r["id"]]
            L.append(f"| [{r['v2']['pedido_resumido'][:80]}]({r['ask']['hn_url']}) | {r['tier']} | {r['best']:.2f} | "
                     f"{GAPS_KEYS[a['label']]} | {a.get('note', '').replace('|', '/')} |")
    text = "\n".join(L) + "\n"
    GAPS_RESULT_PATH.write_text(text)
    return text


def interactive_gaps(conn: sqlite3.Connection, getkey=pilot._getkey, out=print, ask_text=input) -> dict:
    import webbrowser

    from gapfinder import gaps
    from gapfinder.text import get_texts

    strong, grey = gap_queue()
    answers = load_gap_answers()
    ver = load_done(gaps.VERDICTS)
    ids = sorted({i for r in strong + grey for i in r["scored"][:3]})
    texts = get_texts(conn, ids)
    meta = {i: (u, c) for i, u, c in conn.execute(
        f"SELECT id, url, created_at FROM items WHERE id IN ({','.join('?' * len(ids))})", ids)}
    width = min(shutil.get_terminal_size((100, 30)).columns, 110)

    def one_line(text: str, n: int) -> str:
        text = re.sub(r"\s+", " ", text or "").strip()
        return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"

    GAPS_REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    done_now = 0
    quit_ = False
    for section, rows in (("fuerte", strong), ("gris", grey)):
        for r in rows:
            if r["id"] in answers:
                continue
            if section == "gris" and not any(g["id"] in answers for g in grey):
                out(f"\nTerminaste los {len(strong)} huecos fuertes. Sigue la zona gris ({len(grey)}). "
                    "[c] continuar  [q] volver al menú")
                k = getkey()
                while k not in ("c", "q"):
                    k = getkey()
                if k == "q":
                    quit_ = True
                    break
            a, d, top = r["ask"], r["v2"], r["scored"][:3]
            n_done = sum(x["id"] in answers for x in rows)
            out("\033[2J\033[H" if getkey is pilot._getkey else "", end="")
            out(f"[{n_done + 1}/{len(rows)} {'hueco fuerte' if section == 'fuerte' else 'zona gris'}]  {r['id']}  ·  "
                f"etiqueta comentarios: {d['etiqueta']} ({gaps.LABELS[d['etiqueta']]})  ·  mejor Jev {r['best']:.2f}")
            out(f"ASK ({a['created_at'][:10]}, {a['points']} pts, {a['num_comments']} comentarios): {a['title']}")
            out(f"     {a['hn_url']}")
            for line in textwrap.wrap(f"PEDIDO: {d['pedido_resumido']}", width - 2):
                out("  " + line)
            for line in textwrap.wrap(f"LLM: {d['justificacion']}", width - 2):
                out("  " + line)
            out("")
            for n, i in enumerate(top, 1):
                url, created = meta.get(i, ("", "?"))
                out(f"{n}) {texts[i].title[:width - 30]}  ·  {created[:10]}  ·  Jev {ver[(r['id'], i)].core:.2f}")
                out(f"   {one_line(texts[i].body, width - 4)}")
                out(f"   {url}")
            out("\n[n] hueco real  [1/2/3] ese candidato es equivalente  [x] existe fuera de estos  [p] algo parcial  "
                "[s] no es software  [?] no sé\n[h] abrir el hilo de HN  [o]+número abrir candidato  [q] guardar y volver")
            while True:
                k = getkey()
                if k == "h":
                    webbrowser.open(a["hn_url"])
                    continue
                if k == "o":
                    m = getkey()
                    if m in ("1", "2", "3") and len(top) >= int(m):
                        webbrowser.open(meta.get(top[int(m) - 1], ("",))[0])
                    continue
                if k in GAPS_KEYS and (k not in "123" or len(top) >= int(k)) or k == "q":
                    break
            if k == "q":
                quit_ = True
                break
            rec = {"case_id": r["id"], "ask_id": r["ask_id"], "tier": r["tier"], "best": round(r["best"], 4),
                   "label": k, "at": _now()}
            if k in "123":
                rec["item_id"] = top[int(k) - 1]
            if k in ("x", "p", "s"):
                note = ask_text("  nota (nombre/URL de lo que existe, o por qué; Enter para omitir): ").strip()
                if note:
                    rec["note"] = note
            with GAPS_REVIEW_PATH.open("a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            answers[r["id"]] = rec
            done_now += 1
        if quit_:
            break
    text = write_gap_result(strong, grey, answers)
    out("\n" + text.split("## Respuestas")[0])
    out(f"Guardado en {GAPS_REVIEW_PATH}; resultado en {GAPS_RESULT_PATH}")
    return {"respondidas_ahora": done_now, "fuertes": f"{sum(r['id'] in answers for r in strong)}/{len(strong)}",
            "gris": f"{sum(r['id'] in answers for r in grey)}/{len(grey)}"}


# --- menú -----------------------------------------------------------------------------------------------


def _labels_progress() -> tuple[int, int] | None:
    if not pilot.PAIRS_PATH.exists():
        return None
    human = pilot.load_human()
    targets = [(p["case_id"], p["item_id"]) for p in json.loads(pilot.PAIRS_PATH.read_text())
               if p["stratum"] == "positivo" and human.get((p["case_id"], p["item_id"])) == "n" and p["case_id"].startswith("real-")]
    got = pilot.load_human(pilot.LABELS_REVIEW_PATH)
    return sum(k in got for k in targets), len(targets)


def _holdout_progress() -> tuple[int, int] | None:
    from gapfinder import holdout

    if not (holdout.DIR / "candidates.json").exists():
        return None
    main, optional = holdout_ideas()
    answers = load_holdout_answers(main + optional)
    return sum(r["case_id"] in answers for r in main), len(main)


def _extract_progress() -> tuple[int, int] | None:
    q = extract_queue()
    if q is None:
        return None
    got = load_extract_human()
    return sum(a in got for a in q), len(q)


def _phase4_progress(conn: sqlite3.Connection) -> tuple[int, int] | None:
    keys = phase4_queue(conn, with_pairs=False)
    if keys is None:
        return None
    got = pilot.load_human(PHASE4_REVIEW_PATH)
    return sum(k in got for k in keys), len(keys)


QUEUES = {
    "a": ("Etiquetas de reales (positivos del piloto que juzgaste \"no\")", "falta el piloto"),
    "b": ("Holdout temporal, por idea (las 20 \"no\"; opcionales al final)", "falta el holdout"),
    "c": ("Ask HN: extracción (pedido real s/n, etiqueta e/p/n/?)", "falta el paso 2 (extracción)"),
    "d": ("Fase 4: pares (decisión del sistema y mejor candidato)", "falta el paso 3 (verificación)"),
    "e": ("Candidatos a hueco (huecos fuertes; zona gris al final)", "falta gaps run"),
}


def _gaps_progress() -> tuple[int, int] | None:
    from gapfinder import gaps

    if not gaps.CANDIDATES.exists():
        return None
    strong, _ = gap_queue()
    got = load_gap_answers()
    return sum(r["id"] in got for r in strong), len(strong)


def progress(conn: sqlite3.Connection) -> dict[str, tuple[int, int] | None]:
    return {"a": _labels_progress(), "b": _holdout_progress(), "c": _extract_progress(), "d": _phase4_progress(conn),
            "e": _gaps_progress()}


def menu(conn: sqlite3.Connection, cases: list[dict], getkey=pilot._getkey, out=print, evaluar: bool = False) -> None:
    """evaluar: muestra también la cola c) (confirmar a mano la extracción de Ask HN). Por defecto queda oculta:
    la extracción la hace un LLM y lo que se revisa es data/eval/gap_candidates.md."""
    queues = {k: v for k, v in QUEUES.items() if evaluar or k != "c"}
    while True:
        prog = progress(conn)   # se recalcula cada vez: los pasos de la Fase 4 pueden terminar mientras revisás
        out("\033[2J\033[H" if getkey is pilot._getkey else "", end="")
        out("gapfinder review — colas de revisión\n")
        for k, (name, missing) in queues.items():
            p = prog[k]
            state = f"pendiente: {missing}" if p is None else f"{p[0]}/{p[1]}" + ("  ✓" if p[0] >= p[1] else "")
            if k == "c" and p is not None and (sel := askhn.load_selected()):
                got = load_extract_human()
                state += f"  (elegidos Fase 4: {sum(a in got for a in sel)}/{len(sel)}, van primero)"
            out(f"  {k}) {name:<62} {state}")
        if not evaluar:
            out(f"\n  (la cola c, confirmar la extracción de Ask HN a mano, está oculta: gapfinder review --evaluar)")
        out("\n  q) salir\n\nElegí una cola: ", end="")
        key = getkey()
        if key == "q":
            out("")
            return
        if key not in queues:
            continue
        if prog[key] is None:
            out(f"\n\nLa cola {key} está pendiente: {QUEUES[key][1]}. [cualquier tecla] volver")
            getkey()
            continue
        if key == "a":
            pilot.interactive_labels(conn, cases, getkey=getkey, out=out)
        elif key == "b":
            interactive_holdout(conn, getkey=getkey, out=out)
        elif key == "c":
            interactive_extract(getkey=getkey, out=out)
        elif key == "d":
            interactive_phase4(conn, getkey=getkey, out=out)
        elif key == "e":
            interactive_gaps(conn, getkey=getkey, out=out)
        out("\n[cualquier tecla] volver al menú")
        getkey()
