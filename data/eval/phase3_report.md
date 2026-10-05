# Fase 3 — reporte final (verificador Jev)

Verificador: Jev 1.13 vía OpenRouter (`typesafe/jev-1.13-20260917`), sobre el top-1000 de MiniLM + llm5. Regla calibrada con la revisión humana: P(núcleo) >= 0.9 **ya construido**, 0.85-0.9 **revisar a mano**, < 0.85 **no**.

## Por qué esta regla

- Piloto (50 pares, revisión humana): todos los "núcleo" humanos tienen Jev >= 0.87; ningún parcial/no supera 0.82. Acuerdo en núcleo a 0.5 sobre 34 pares juzgados: Jev 88%, Haiku 88% (los desacuerdos: el modelo dice núcleo donde el humano ve parcial).
- Adjudicación de alarmas (23 de 47): Jev >= 0.90 -> 15/15 implementaciones reales no listadas, 0 errores; 0.85-0.90 -> 2 núcleo, 2 parcial, 1 error, 1 no sé. Con 15/15, el error real a >= 0.90 puede llegar a ~20% (intervalo 95%).

## Resultados por grupo

**Detección (punta a punta)**: el sistema dice "ya construido" si algún candidato del top-1000 tiene núcleo >= 0.90 (la adjudicación muestra que esas alarmas son implementaciones reales, así que cuenta aunque no sea el item listado). **Recall del item esperado**: entre los casos con el esperado en el top-1000, su núcleo. **Alarmas por remoción**: sacando el esperado y sus gemelos, el mejor candidato restante.

| grupo | casos | detección >= 0.90 | revisar (0.85-0.90, sin >= 0.90) | esperado en top-1000 | esperado >= 0.90 | esperado >= 0.85 | alarma >= 0.90 | alarma 0.85-0.90 |
|---|---|---|---|---|---|---|---|---|
| reales v1 | 12 | 5/12 (42%) | 2/12 (17%) | 11/12 (92%) | 1/11 (9%) | 1/11 (9%) | 5/12 (42%) | 2/12 (17%) |
| reales v1 sin label_note | 9 | 5/9 (56%) | 1/9 (11%) | 8/9 (89%) | 1/8 (12%) | 1/8 (12%) | 5/9 (56%) | 1/9 (11%) |
| reales v2 | 12 | 7/12 (58%) | 1/12 (8%) | 11/12 (92%) | 2/11 (18%) | 2/11 (18%) | 7/12 (58%) | 1/12 (8%) |
| reales v2 sin label_note | 9 | 6/9 (67%) | 1/9 (11%) | 9/9 (100%) | 2/9 (22%) | 2/9 (22%) | 6/9 (67%) | 1/9 (11%) |
| sintéticos | 64 | 37/64 (58%) | 14/64 (22%) | 59/64 (92%) | 24/59 (41%) | 37/59 (63%) | 29/64 (45%) | 11/64 (17%) |

## Alarmas por remoción, adjudicadas (v1)

La "falsa alarma" de `phase3 report` cuenta como error cualquier alarma; la adjudicación muestra que a >= 0.90 son alternativas reales.

| tramo | alarmas | adjudicadas reales (núcleo) | parcial | error del verificador | no sé | sin adjudicar |
|---|---|---|---|---|---|---|
| >= 0.95 | 17 | 11 | 0 | 0 | 0 | 6 |
| 0.90-0.95 | 17 | 4 | 0 | 0 | 2 | 11 |
| 0.85-0.90 | 13 | 2 | 2 | 1 | 1 | 7 |

## Reales: caso por caso (v1 -> v2)

| caso | label_note | esperado núcleo v1 | v2 | detección v1 | v2 | mejor alarma v1 | v2 |
|---|---|---|---|---|---|---|---|
| `real-01fe2dbe` |  | 0.44 | 0.50 | ya construido | revisar | 0.92 | 0.87 |
| `real-197bf4f9` |  | 0.84 | 0.90 | revisar | ya construido | 0.87 | 0.91 |
| `real-25a4c842` |  | 0.40 | 0.37 | no | no | 0.63 | 0.66 |
| `real-47bf5f9f` |  | 0.65 | 0.83 | no | no | 0.70 | 0.83 |
| `real-6eb5b382` |  | 0.74 | 0.72 | ya construido | ya construido | 0.94 | 0.92 |
| `real-6f3848c8` |  | 0.83 | 0.74 | ya construido | ya construido | 0.93 | 0.90 |
| `real-7c597ec1` | sí | 0.17 | 0.20 | no | no | 0.53 | 0.44 |
| `real-89c010f2` |  | 0.93 | 0.90 | ya construido | ya construido | 0.95 | 0.93 |
| `real-8b190bdc` | sí | 0.29 | fuera del top | no | no | 0.66 | 0.55 |
| `real-a6c38804` |  | 0.47 | 0.30 | no | ya construido | 0.81 | 0.91 |
| `real-ecad36a5` |  | fuera del top | 0.78 | ya construido | ya construido | 0.90 | 0.91 |
| `real-fbe3c4c2` | sí | 0.26 | 0.21 | revisar | ya construido | 0.89 | 0.90 |

## Costo y corridas

- v1: 76,000 pares (12 reales + 64 sintéticos x 1000); v2: 12,000 pares (12 reales con query_core v2). 0 errores.
- Costo facturado por OpenRouter (usage.cost): $2.83 en total (más $0.0017 del piloto). Haiku solo se usó en el piloto ($0.046).
- Latencia mediana ~0.3 s por par; ~1.200 pares por minuto.

## Limitaciones

- Muestras chicas: 12 reales, 34 pares juzgados en el piloto, 23 alarmas adjudicadas (24 sin adjudicar).
- Etiquetas de reales: 3 con label_note (esperados genéricos) y 4 positivos que la revisión humana juzgó "no".
- La regla se calibró con los mismos datos que se reportan; validarla en casos nuevos antes de usarla en producción.
- Sin negativos reales (Constellate no dio veredictos `no`): los negativos son por remoción.

