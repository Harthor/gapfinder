"""Reporte final de la Fase 3 (Jev vía OpenRouter, regla por umbral calibrada con la revisión humana).
Escribe data/eval/phase3_report.md. Regla: P(núcleo) >= 0.90 ya construido; 0.85-0.90 revisar; < 0.85 no."""
import json, sqlite3
from pathlib import Path
from gapfinder import phase3, pilot
from gapfinder.verify import load_done

BUILT, REVIEW = 0.90, 0.85
conn = sqlite3.connect("file:data/corpus.db?mode=ro", uri=True)
cases = {c["id"]: c for c in json.load(open("data/known_cases.json"))}
cand_v1 = json.load(open("data/phase3/candidates_minilm.json"))
cand_v2 = json.load(open("data/phase3/candidates_minilm_v2_real.json"))
v1, v2 = load_done("jev_openrouter"), load_done("jev_openrouter_v2")
adj = pilot.load_human(pilot.ALARMS_HUMAN_PATH)
human_pilot = pilot.load_human()

def analyze(ids, cand, ver):
    rows = []
    for cid in ids:
        c = cases[cid]; top = cand[cid]
        removed = phase3.twins(conn, c["expected_item_ids"])
        exp_in = [i for i in c["expected_item_ids"] if i in top]
        exp_core = max((ver[(cid, i)].core for i in exp_in), default=None)
        rest = [i for i in top if i not in removed]
        best = max(rest, key=lambda i: ver[(cid, i)].core)
        rows.append({"case": cid, "exp_in_top": bool(exp_in), "exp_core": exp_core,
                     "alarm_item": best, "alarm_core": ver[(cid, best)].core,
                     "any_core": max(ver[(cid, i)].core for i in top)})
    return rows

def pct(a, b): return f"{a}/{b} ({a / b:.0%})" if b else "–"

groups = {
    "reales v1": ([c for c in cases if cases[c]["kind"] == "real"], cand_v1, v1),
    "reales v1 sin label_note": ([c for c in cases if cases[c]["kind"] == "real" and not cases[c].get("label_note")], cand_v1, v1),
    "reales v2": ([c for c in cases if cases[c]["kind"] == "real"], cand_v2, v2),
    "reales v2 sin label_note": ([c for c in cases if cases[c]["kind"] == "real" and not cases[c].get("label_note")], cand_v2, v2),
    "sintéticos": ([c for c in cases if cases[c]["kind"] == "synthetic"], cand_v1, v1),
}
L = ["# Fase 3 — reporte final (verificador Jev)\n",
     "Verificador: Jev 1.13 vía OpenRouter (`typesafe/jev-1.13-20260917`), sobre el top-1000 de MiniLM + llm5. "
     f"Regla calibrada con la revisión humana: P(núcleo) >= {BUILT} **ya construido**, {REVIEW}-{BUILT} **revisar a mano**, "
     f"< {REVIEW} **no**.\n",
     "## Por qué esta regla\n",
     "- Piloto (50 pares, revisión humana): todos los \"núcleo\" humanos tienen Jev >= 0.87; ningún parcial/no supera 0.82. "
     "Acuerdo en núcleo a 0.5 sobre 34 pares juzgados: Jev 88%, Haiku 88% (los desacuerdos: el modelo dice núcleo donde el humano ve parcial).",
     "- Adjudicación de alarmas (23 de 47): Jev >= 0.90 -> 15/15 implementaciones reales no listadas, 0 errores; "
     "0.85-0.90 -> 2 núcleo, 2 parcial, 1 error, 1 no sé. Con 15/15, el error real a >= 0.90 puede llegar a ~20% (intervalo 95%).\n",
     "## Resultados por grupo\n",
     "**Detección (punta a punta)**: el sistema dice \"ya construido\" si algún candidato del top-1000 tiene núcleo >= 0.90 "
     "(la adjudicación muestra que esas alarmas son implementaciones reales, así que cuenta aunque no sea el item listado). "
     "**Recall del item esperado**: entre los casos con el esperado en el top-1000, su núcleo. "
     "**Alarmas por remoción**: sacando el esperado y sus gemelos, el mejor candidato restante.\n",
     "| grupo | casos | detección >= 0.90 | revisar (0.85-0.90, sin >= 0.90) | esperado en top-1000 | esperado >= 0.90 | esperado >= 0.85 | alarma >= 0.90 | alarma 0.85-0.90 |",
     "|---|---|---|---|---|---|---|---|---|"]
details = {}
for g, (ids, cand, ver) in groups.items():
    rows = analyze(ids, cand, ver); details[g] = rows
    n = len(rows); inn = [r for r in rows if r["exp_in_top"]]
    L.append(f"| {g} | {n} | {pct(sum(r['any_core'] >= BUILT for r in rows), n)} | "
             f"{pct(sum(REVIEW <= r['any_core'] < BUILT for r in rows), n)} | {pct(len(inn), n)} | "
             f"{pct(sum(r['exp_core'] >= BUILT for r in inn), len(inn))} | {pct(sum(r['exp_core'] >= REVIEW for r in inn), len(inn))} | "
             f"{pct(sum(r['alarm_core'] >= BUILT for r in rows), n)} | {pct(sum(REVIEW <= r['alarm_core'] < BUILT for r in rows), n)} |")
L += ["", "## Alarmas por remoción, adjudicadas (v1)\n",
      "La \"falsa alarma\" de `phase3 report` cuenta como error cualquier alarma; la adjudicación muestra que a >= 0.90 son alternativas reales.\n",
      "| tramo | alarmas | adjudicadas reales (núcleo) | parcial | error del verificador | no sé | sin adjudicar |", "|---|---|---|---|---|---|---|"]
alarms = details["reales v1"] + details["sintéticos"]
for lo, hi, name in ((0.95, 1.01, ">= 0.95"), (0.90, 0.95, "0.90-0.95"), (0.85, 0.90, "0.85-0.90")):
    ks = [(r["case"], r["alarm_item"]) for r in alarms if lo <= r["alarm_core"] < hi]
    cnt = {lab: sum(adj.get(k) == lab for k in ks) for lab in "spn?"}
    L.append(f"| {name} | {len(ks)} | {cnt['s']} | {cnt['p']} | {cnt['n']} | {cnt['?']} | {len(ks) - sum(cnt.values())} |")
L += ["", "## Reales: caso por caso (v1 -> v2)\n",
      "| caso | label_note | esperado núcleo v1 | v2 | detección v1 | v2 | mejor alarma v1 | v2 |", "|---|---|---|---|---|---|---|---|"]
d1 = {r["case"]: r for r in details["reales v1"]}; d2 = {r["case"]: r for r in details["reales v2"]}
f = lambda x: "fuera del top" if x is None else f"{x:.2f}"
dec = lambda x: "ya construido" if x >= BUILT else "revisar" if x >= REVIEW else "no"
for cid in sorted(d1):
    a, b = d1[cid], d2[cid]
    L.append(f"| `{cid}` | {'sí' if cases[cid].get('label_note') else ''} | {f(a['exp_core'])} | {f(b['exp_core'])} | "
             f"{dec(a['any_core'])} | {dec(b['any_core'])} | {a['alarm_core']:.2f} | {b['alarm_core']:.2f} |")
cost = sum(x.cost_usd for x in v1.values()) + sum(x.cost_usd for x in v2.values())
L += ["", "## Costo y corridas\n",
      f"- v1: {len(v1):,} pares (12 reales + 64 sintéticos x 1000); v2: {len(v2):,} pares (12 reales con query_core v2). 0 errores.",
      f"- Costo facturado por OpenRouter (usage.cost): ${cost:.2f} en total (más $0.0017 del piloto). Haiku solo se usó en el piloto ($0.046).",
      "- Latencia mediana ~0.3 s por par; ~1.200 pares por minuto.\n",
      "## Limitaciones\n",
      "- Muestras chicas: 12 reales, 34 pares juzgados en el piloto, 23 alarmas adjudicadas (24 sin adjudicar).",
      "- Etiquetas de reales: 3 con label_note (esperados genéricos) y 4 positivos que la revisión humana juzgó \"no\".",
      "- La regla se calibró con los mismos datos que se reportan; validarla en casos nuevos antes de usarla en producción.",
      "- Sin negativos reales (Constellate no dio veredictos `no`): los negativos son por remoción.\n"]
Path("data/eval/phase3_report.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
