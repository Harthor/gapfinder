# gapfinder

**¿Alguien ya construyó esto?** gapfinder cruza pedidos reales de herramientas ("Ask HN: is there a tool
for…?") con un corpus de ~697 mil cosas ya construidas (Show HN + repos de GitHub con >= 100★), mirando solo
lo que existía *antes* de cada pedido, y separa lo que ya estaba resuelto de los huecos candidatos.

Lo interesante no es la lista de huecos, sino **cuánto se puede confiar en ella**: cada etapa se midió contra
casos conocidos y revisión humana, y varias hipótesis se descartaron con datos.

## Pipeline

```
Ask HN (pedido + comentarios)
  └─ extracción con LLM: ¿es un pedido real?, resumen del pedido, ¿los comentarios dicen que existe? (e/p/n)
       └─ retrieval: MiniLM + 5 consultas por pedido (Claude), fusionadas con RRF -> top-1000
            sobre el corpus anterior a la fecha del Ask (sin mirar el futuro)
            └─ verificador: Jev (vía OpenRouter) puntúa cada par (pedido, candidato): P(implementa el núcleo)
                 └─ niveles: ya construido (>= 0.85) · no es software · descartado · hueco fuerte · zona gris
```

## Resultados medidos

| Etapa | Cómo se midió | Resultado |
|---|---|---|
| Retrieval | ¿el item correcto aparece en el top-1000? (known cases) | reales **11/12 (0.92)**, sintéticos **0.92** (n=64), parciales 0.75 (n=16) |
| Verificador | acuerdo con revisión humana, 34 pares juzgados | **88%** en "implementa el núcleo"; todo núcleo humano tiene Jev >= 0.87 |
| Alarmas del verificador | 15 alarmas con Jev >= 0.90 adjudicadas a mano | **15/15** eran implementaciones reales no listadas, no errores |
| Huecos en el tiempo | holdout: ideas lanzadas después de 2024-01-01 contra el corpus anterior; 20 que el sistema llamó "hueco", adjudicadas a mano | **6/20 = 30%** eran hueco real (IC 95%: 15–52%); 50% tenían algo parcial; 20% un equivalente |
| Pedidos de Ask HN | 242 pedidos reales, veredictos cacheados | 123 ya construidos, 44 no son software, 44 los comentarios dicen que existen, 19 zona gris, **12 huecos fuertes** (sin adjudicar todavía) |

Costo de APIs en las corridas registradas: ~$12 (Fase 3 $2.83, holdout $1.90, Ask HN y huecos $7.04; OpenRouter
`usage.cost` + Anthropic).

## Qué aprendí

- **"Sin match" no es lo mismo que "hueco".** Con un corte binario (ningún candidato >= 0.85) salían 119 huecos,
  69 de ellos con comentarios que decían que la herramienta existía; el holdout confirma que solo ~30% de esos
  "no" son huecos reales. De ahí los niveles: el hueco fuerte exige puntaje bajo (< 0.60) *y* que los comentarios
  no digan que existe.
- **Los negativos por remoción no sirven.** Sacar el item esperado y ver si el verificador "alucina" otro parecía
  una buena medida de falsas alarmas; al adjudicarlas, todas las alarmas altas eran alternativas legítimas. Para
  necesidades comunes casi nunca hay una sola solución.
- **El retrieval no es el cuello de botella.** Encuentra el item correcto en 11 de 12 casos reales; lo que
  limita es el umbral del verificador y la cobertura del corpus (SaaS comerciales o recursos institucionales no
  están en Show HN ni en GitHub).
- **Las consultas reescritas por un LLM ayudan, con cuidado.** Pasar de la descripción cruda a 5 reformulaciones
  sube R@50 en reales de 0.08 a 0.50; el prompt prohíbe nombrar productos para no filtrar la respuesta.

## Huecos fuertes de ejemplo (sin adjudicar)

Pedidos de Ask HN sin nada parecido en el corpus anterior a la fecha del pedido, y donde los comentarios
tampoco señalan una herramienta existente. Lista completa: [`data/eval/gap_candidates.md`](data/eval/gap_candidates.md).

| Pedido | Año | Mejor candidato (P núcleo) |
|---|---|---|
| Conversor de texto a Comunicación No Violenta | 2022 | FoxType (0.29) |
| Parser de archivos `.one` de OneNote o formato abierto equivalente | 2018 | dtformats (0.32) |
| Buscar en datasets MIDI por progresión de acordes y tonalidad | 2022 | match.audio (0.36) |
| Servicio para registrar un sitio en datasets de entrenamiento de LLMs | 2024 | gi.st (0.47) |
| Analizador de PCAP que correlaciona varios streams a la vez | 2020 | CSI-SIEM (0.55) |

## Limitaciones

- Muestras chicas: 12 casos reales, 34 pares en el piloto, 20 ideas en el holdout; los intervalos son anchos.
- El umbral 0.60 del hueco fuerte no está calibrado; la cola `gapfinder review` → e) existe para adjudicar los 12 y
  medir su precisión.
- "Hueco" significa "sin equivalente en este corpus antes del pedido", no "no existe en ningún lado".

## Correrlo

```bash
uv sync && uv run pytest              # tests: corren en un clon limpio, sin red ni datos locales
uv run gapfinder gaps report          # regenera data/eval/gap_candidates.md (necesita los datos locales)
uv run gapfinder review               # colas de revisión humana (ídem)
```

El corpus (`data/corpus.db`, 1,8 GB), los embeddings, el índice BM25 y los veredictos del verificador
(`data/phase3/*.jsonl`) no están en el repo; el corpus se reconstruye con `ingest`, `embed` y `bm25` (ver Fase 1 y
2). Los reportes, los casos conocidos y las revisiones humanas sí están en `data/eval/` y `data/`. De los Ask HN el
repo guarda solo metadatos (título, id, URL, fecha, puntos); el texto del OP queda en una copia local
(`data/cache/askhn/asks_text.json`) que `gapfinder askhn collect` regenera.

Licencia: [MIT](LICENSE).

---

# Detalle técnico por fase

## Fase 1 — corpus de oferta

```bash
uv sync
export GITHUB_TOKEN=...                        # para el bulk de GitHub (30 req/min de search)

uv run gapfinder ingest --source hn --limit 10000000              # Show HN completo (~209k)
uv run gapfinder census                                           # repos por año x umbral de estrellas
uv run gapfinder ingest --source github --min-stars 100 --limit 10000000 --readmes
uv run gapfinder ingest --source github --min-stars 50 --max-stars 99 --limit 10000000   # ampliar por banda
uv run gapfinder enrich                                           # Show HN sin descripción
uv run gapfinder reclean-readmes --refetch-rst                    # re-limpia README guardados (antes de embeber)
uv run gapfinder stats
```

Todo es idempotente y reanudable: HN guarda el rango de fechas cubierto, GitHub marca cada
ventana `created:` terminada, y el enriquecimiento registra cada intento (también los fallidos).

### Enriquecimiento de Show HN sin descripción (`enrich`)

- Link a repo de GitHub: si el repo está en el corpus se usa su texto; si no, se baja el README.
- Web, en cadena: `author_comment` (comentarios top-level del autor en su hilo, >=100 chars) ->
  `author_reply` (primeras 3 intervenciones del autor a cualquier profundidad, >=100 chars c/u) ->
  `current` (meta de la página actual, solo posts de <2 años, con filtro de dominios estacionados)
  -> `title_only`.
- Wayback está pausado en bulk: los `title_only` quedan con `error = 'wayback: no intentado'` y
  `enrich.wayback_on_demand()` los completa puntualmente (ventana [post - 30d, post + 6m]).
  Para activarlo en bulk: `enrich --wayback-min-points 10`.
- Rate limits: Algolia HN 10.000 req/h documentado (se usa 150/min); archive.org 15/min global.

`text.py` resuelve el texto final de cada item y su origen
(`native | github_corpus | current | author_comment | author_reply | wayback | title_only`).

### Casos sintéticos

```bash
uv run gapfinder worksheet                    # data/synthetic_worksheet.md (40, época x puntos)
uv run gapfinder worksheet --n 20 --origins author_comment=10,author_reply=10 \
    --out data/synthetic_worksheet_2.md
uv run gapfinder worksheet-import --worksheet data/synthetic_worksheet.md
```

Cada caso guarda su hoja de origen en `meta.worksheet`; el import solo reemplaza los de esa hoja.

## Fase 2 — embeddings + retrieval + eval de recall

```bash
uv run gapfinder embed --model all                 # data/cache/emb/<modelo>/corpus, por bloques de 20k (retoma)
uv run gapfinder targeted                          # búsqueda dirigida por caso -> items + tabla `targeted`
uv run gapfinder embed --model all --index targeted
uv run gapfinder eval                              # data/eval/phase2_recall.md + phase2_ranks.json
```

Implementado así (sep-2026):
- Reformulaciones (plantillas, sin LLM: no hay API key en esta máquina): `need` (la necesidad; en
  real/partial título + descripción), `keywords` (6 palabras de producto), `plain` (sin "I want/I
  need…"; en real/partial solo la descripción, sin el título de gancho) y `show_hn` (`plain` con el
  prefijo de los títulos del corpus). `reform 1` = solo `need`; `reform 4` = unión de las cuatro.
- Recall@N = algún item esperado en el top-N de alguna reformulación (la unión, que puede tener hasta
  4N candidatos; el reporte da su tamaño medio).
- Búsqueda dirigida: por caso, 2 consultas de palabras clave (puntaje = especificidad técnica frente
  al inglés general con `wordfreq` + idf del corpus; df >= 20) contra GitHub Search sin filtro de
  estrellas y Algolia (solo Show HN). Lo nuevo va a `items` y a la tabla `targeted`; el índice
  `corpus` no lo incluye, el `targeted` sí, y el eval reporta sin/con.

### Iteración 2 de retrieval (sep-2026)

```bash
uv run gapfinder llm-queries                        # Claude (claude-opus-5): query_core + 4 reformulaciones + 3 keyword queries
uv run gapfinder targeted --llm                     # OPCIONAL (fuera del pipeline): búsqueda dirigida -> targeted_llm
uv run gapfinder bm25                               # índice FTS5 en data/cache/fts.db (incremental)
uv run gapfinder embed --model all --index corpus targeted   # all = minilm + bge (e5 descartado)
uv run gapfinder eval2                              # data/eval/iter2_recall.md (+ --targeted para la variante dirigida)
```

- Varias consultas por caso se fusionan con RRF (k=60) en un único ranking cortado a N (antes: unión
  de hasta 4N candidatos).
- `query_core` (real/partial): la necesidad central en 1-2 oraciones, extraída por Claude sin jerga
  de Constellate; el prompt prohíbe nombrar productos, proyectos o plataformas existentes (sería
  filtrar la respuesta). Todo en `data/llm_queries.json`, cacheado por hash de la entrada.
- BM25: FTS5 (porter) sobre título + texto resuelto; consulta = hasta 24 términos por idf en OR,
  título x2. Híbrido = RRF(listas de embeddings + listas de BM25).
- Modelos: MiniLM y bge-base-en-v1.5 (instrucción de query "Represent this sentence for searching
  relevant passages: ", pasajes sin prefijo, 256 tokens como MiniLM). e5-small se descartó: sin bug
  (prefijos una sola vez, vectores normalizados), pero sus cosenos quedan comprimidos en 0.72-0.88 y
  separa poco el item correcto del resto.
- Búsqueda dirigida: fuera del pipeline por defecto (flag `eval2 --targeted`). Con plantillas y con
  keyword queries de Claude no trajo ningún item esperado de los que faltaban y solo agregó
  competidores (~5.000 repos < 100★); el recall quedó igual o peor.

Resultado de la iteración 2 (sep-2026, `data/eval/iter2_recall.md`): se elige MiniLM + llm5 con
embeddings solos, por R@1000 en reales + parciales sin heurísticos (21/28 = 0.75; bge 0.61, BM25
0.68, híbridos 0.64). bge-base no mejora a MiniLM en reales/parciales (igual en sintéticos: 0.94 vs
0.92). El híbrido gana arriba de la lista (R@50) pero pierde en la cola. Los candidatos de la Fase 3
salen de este sistema (`phase3 candidates --model minilm`).

Prompt v2 de las consultas (`llm-queries --prompt-version 2`, `data/llm_queries_v2.json`): permite
términos de categoría ("LLM router") y sigue prohibiendo nombres de productos. Solo cambia real/partial.
Comparación en `data/eval/compare_prompt_v1_v2.md` (la tabla v1 queda en `data/eval/iter2_recall.md`):
con MiniLM + llm5, parciales sin heurísticos 0.62 -> 0.75 @1000 y reales sin label_note 0.89 -> 1.00;
RouteLLM pasa de fuera del top-2000 a rank 45; un real (8b190bdc, con label_note) sale del top-1000.

Plan original:

- Modelos: `all-MiniLM-L6-v2` vs `multilingual-e5-small` (prefijos `query: ` / `passage: `).
  Texto: título + cuerpo resuelto, truncado con el tokenizer de cada modelo. Cache por modelo.
- Retrieval: 3–4 reformulaciones por idea (plantillas; hook para Claude), top-N por cada una, unión.
- Búsqueda dirigida por idea: search API de GitHub sin filtro de estrellas (+ Algolia HN full-text),
  resultados agregados al corpus con origen `targeted`. Recall reportado con y sin este paso.
- Eval `known_cases.json`: recall@50/200/1000 por modelo x reformulaciones, **siempre por kind**
  (`synthetic`, `real`, `partial`; nunca un recall agregado que los mezcle), separado por origen del
  texto del item esperado (enriched vs title_only). Un caso cuenta como encontrado si cualquiera de
  sus `expected_item_ids` está en el top-N. Para casos reales no encontrados: estrellas del repo esperado.
- `partial` (absences con veredicto solo `partially`: el prior art cubre parte de la idea): el recall
  se reporta con y sin `meta.heuristic_item_ids` (items resueltos por dominio, no revisados a mano).
  Los casos real/partial sin ningún item esperado en el corpus miden cobertura, no retrieval: se
  cuentan aparte (`n sin item en corpus`) y no entran en el denominador del recall.
- Ablación (sintéticos): recall con el texto real del item esperado vs. forzándolo a `title_only`
  (solo ese item; el resto del índice igual). Caída por modelo y por origen original del texto.
- Recall separado también por `author` (claude/human) en sintéticos y por `verified_by` en reales.
- Recall pareado human vs claude: los casos con el mismo `pair_id` son la misma idea (mismo item
  esperado) escrita por Carla y por Claude. Se reporta sobre esos pares (8 en sep-2026): recall@N
  de cada autor y la tabla 2x2 (ambos / solo human / solo claude / ninguno) por modelo x reformulaciones.
  Las necesidades de Claude de los pares (y las 20 de `synthetic_worksheet_2.md`) las escribió un
  subagente que solo recibió título + texto de cada item, sin las necesidades humanas ni la hoja;
  mismas reglas y filtro de fuga (reescritas hasta pasar). Se reporta también excluyendo los pares
  con `leakage_flag`.
- Negativos (`kind: "negative"`, huecos confirmados): no cuentan para recall. Para cada uno se reporta
  el candidato más similar y su score, para ver qué tan cerca queda el "falso ya construido".
  En la Fase 3 se usan para medir falsos positivos del verificador.

### Known cases

- Sintéticos: `worksheet` / `worksheet-check` / `worksheet-import` (ver arriba). `worksheet-import`
  marca `leakage_flag: true` en los casos que el filtro de fuga marca y quedaron así. En los items
  `[humano]`, una línea `necesidad claude:` debajo de `necesidad:` genera el caso pareado
  `syn-<id>-claude` (`author: "claude"`, mismo `pair_id` que el humano).
- Reales, parciales y negativos: `gapfinder real-candidates` arma `data/real_candidates.md` con las
  absences verificadas por Constellate (web en `constellate.db`, manual en `prior-art/`, rúbrica en
  `rubric-test/`); `gapfinder real-import` importa lo marcado `real` / `parcial` / `negativo`.
  Veredicto `yes` -> propuesta real; `no` -> negativo; solo `partially` -> `kind: "partial"`, que ya
  viene `confirmado: parcial` con todas sus URLs de evidencia en `esperado:` (56 de 71 en sep-2026;
  más 2 reales pasadas a parcial en la revisión: 12 reales, 58 parciales, 1 descartada).
  `esperado:` acepta URLs y también ids del corpus (`show_hn:123`, `github:owner/repo`) para fijar un
  item concreto, y `!github:owner/repo` descarta un match revisado (la URL queda, el item no cuenta).
  Las URLs se resuelven con `CorpusIndex`: repo o URL exacta, o heurístico por dominio
  (homepage de un repo / Show HN del dominio) exigiendo que el nombre del producto calce con el item:
  la marca como segmento entero del repo y, si el nombre trae palabras propias ("NVIDIA Triton"),
  alguna presente en el item. Los heurísticos quedan en `meta.heuristic_item_ids`.
  `constellate.db` se abre siempre en solo lectura (`file:...?mode=ro`).

## Fase 3 — verificador (cerrada, oct-2026: ver `data/eval/phase3_report.md`)

Resultado: Jev 1.13 vía OpenRouter sobre el top-1000 de MiniLM + llm5, con la regla calibrada por
revisión humana (P(núcleo) >= 0.90 ya construido, 0.85-0.90 revisar, < 0.85 no). Detección punta a punta
("ya construido" en algún candidato): reales 42% (v1) / 58% (v2), sintéticos 58%. El item esperado
llega a >= 0.90 en pocos reales (9% v1 / 18% v2; muchos esperados de reales son parciales) y en 41% de
los sintéticos. Las alarmas por remoción >= 0.90 adjudicadas fueron todas implementaciones reales no
listadas (15/15). Costo total $2.83. Reporte reproducible: `uv run python data/eval/phase3_final.py`.

```bash
uv run gapfinder phase3 candidates --model <mejor modelo>        # top-1000 por caso, embeddings + llm5 (RRF)
uv run gapfinder phase3 estimate --model <mejor modelo>          # tokens por par (count_tokens, gratis) y costo
uv run gapfinder phase3 verify --verifier haiku|jev              # GASTA: Haiku vía Batches API / Jev vía typesafe-sdk
uv run gapfinder phase3 report --verifier haiku|jev              # falsas alarmas, curva de positivos, alarmas a revisar
# v2 de los reales: candidatos con llm_queries_v2 y verificación (solo pares nuevos con --only-new-vs)
uv run gapfinder phase3 candidates --kinds real --llm-queries data/llm_queries_v2.json --suffix _v2_real
uv run gapfinder phase3 verify --verifier jev-openrouter --kinds real --suffix _v2_real \
    --llm-queries data/llm_queries_v2.json --name jev_openrouter_v2 [--only-new-vs data/phase3/candidates_minilm.json]
uv run gapfinder pilot select|haiku|jev|jev-openrouter|review    # piloto: los mismos 50 pares -> data/eval/pilot_review.md
uv run gapfinder phase3 review-pilot                             # revisión humana interactiva de los 50 pares (teclas s/p/n/?/o/q)
uv run gapfinder phase3 review-alarms [--per-bin 6]              # adjudicar alarmas (la más alta por caso, núcleo >= 0.85; muestra por tramo)
```

Revisión humana del piloto (`phase3 review-pilot`): muestra cada par (idea, candidato recortado + URL,
núcleo de Jev y de Haiku) en orden Jev núcleo >= 0.5 -> 0.3-0.5 -> < 0.3; cada respuesta se guarda
al instante en `data/eval/pilot_review_human.jsonl` (se retoma donde quedó; una respuesta nueva pisa
la anterior). Al completar, `data/eval/pilot_review_result.md` con acuerdo humano vs Jev y vs Haiku a
umbral 0.5 (núcleo; y parcial-o-más) y la tabla de desacuerdos. No toca `pilot_review.md`.

Corridas completas con Jev vía OpenRouter (oct-2026): v1 = 76.000 pares (12 reales + 64 sintéticos ×
top-1000), `data/phase3/verdicts_jev_openrouter.jsonl`, 0 errores, $2.41 facturado (usage.cost),
p50 291 ms. La primera tanda se cortó con 402 (cuenta sin créditos); la reanudación solo saltea
veredictos válidos (los fallidos nunca se escriben) y el verificador ahora se detiene ante 401/402/403.
v2 de los reales (idea = query_core v2, 12.000 pares completos para no mezclar ideas v1/v2):
`data/phase3/verdicts_jev_openrouter_v2.jsonl`.

Revisión humana del piloto (oct-2026, `data/eval/pilot_review_result.md`): 4 núcleo, 4 parcial,
26 no, 16 no sé. Sobre los 34 juzgados, acuerdo en núcleo a 0.5: Jev 88%, Haiku 88%; los 4
desacuerdos son el modelo diciendo núcleo donde el humano ve parcial/no. Los núcleo humanos tienen
Jev >= 0.87 y ningún parcial/no supera 0.82: en esta muestra 0.85 separa el núcleo (se agregó a los
umbrales). 10 de los 16 "no sé" caen en Jev 0.68-0.93. En 4 positivos el humano dijo "no": revisar
esas etiquetas.

`phase3 report` (`data/phase3/metrics_jev_openrouter*.json`): a 0.85, falsa alarma por remoción
58% reales / 62% sintéticos; recall de positivos 9% reales / 63% sintéticos (v2 reales: 18%).
Las alarmas más altas son mayormente alternativas legítimas (plotext para gráficos en la terminal,
Snapbyte para digest de HN por mail, Pombo para formularios sin servidor): la remoción asume que el
item esperado es la única solución, y para necesidades comunes no lo es. Falta adjudicar las alarmas
a mano para separar errores del verificador de implementaciones no listadas: `phase3 review-alarms`
muestra la alarma más alta de cada caso con núcleo >= 0.85 (47 en v1), junto con el item esperado que
se removió; respuestas en `data/eval/alarms_review_human.jsonl` y resultado (error del verificador por
kind y por tramo de puntaje) en `data/eval/alarms_review_result.md`.

Adjudicación (oct-2026, 23 de 47 alarmas: las 11 más altas + muestra de 6 por tramo): Jev >= 0.90 ->
15/15 juzgadas son implementaciones reales no listadas (0 errores; 2 "no sé"); Jev 0.85-0.90 -> 2 núcleo,
2 parcial, 1 error (un Reddit genérico para un foro religioso), 1 "no sé". Lectura: a >= 0.90 las alarmas
por remoción son casi todas alternativas legítimas, no errores del verificador; 0.85-0.90 es zona de
revisión. Junto con el piloto (núcleo humano siempre >= 0.87), regla propuesta: >= 0.90 "ya construido",
0.85-0.90 "revisar a mano", < 0.85 "no".

Piloto (sep-2026, candidatos MiniLM): 50 pares estratificados (15 positivos, 15 near-miss, 10 de
rank 200-1000, 10 al azar). Haiku 4.5: 50/50 sin errores, ~770 tokens de entrada por par (la salida
estructurada suma ~37% sobre el conteo sin schema), $0.046, p50 1.15 s. Usa pocos valores discretos
(0.05…0.92), así que los umbrales altos discriminan poco. Casos con `label_note` (etiqueta dudosa,
no reetiquetada) se reportan con y sin ellos.

- Pares: (idea, candidato) para cada candidato del top-1000 de cada caso real y sintético (76 casos,
  76.000 pares). idea = `query_core` (real) o la necesidad (sintético); candidato = título + primeros
  1.500 caracteres del texto resuelto.
- Tres preguntas por par, cada una una probabilidad: `core` (implementa el núcleo), `partial`
  (implementa al menos una parte real del núcleo) y `same_user` (mismo usuario objetivo).
- `Verifier` con dos implementaciones (`verify.py`):
  - Jev (TypeSafe, SDK oficial `typesafe-sdk`, modelo fijado `jev-1.13.0`): un request por par con
    tres `Noul` con `criteria` de sí/no. State chico (idea + candidato), como recomiendan sus docs.
    Requiere `TYPESAFE_API_KEY`.
  - Jev vía OpenRouter (`OpenRouterJevVerifier`, registros de TypeSafe pausados): según los docs de
    OpenRouter, `POST https://openrouter.ai/api/v1/systemone` implementa el formato de TypeSafe (no es
    chat completions), así que se usa el mismo SDK con `base_url=https://openrouter.ai/api` y
    `OPENROUTER_API_KEY`. Modelo fijo `typesafe/jev-1.13` (no jev-router). OpenRouter devuelve
    `usage.cost` (lo cobrado); se guarda por par como `cost_usd` y es el costo que se compara.
  - Claude Haiku 4.5 (baseline): salida estructurada con las tres probabilidades, vía Message Batches.
  - Resultados en `data/phase3/verdicts_<verifier>.jsonl`, reanudable.
- Negativos por remoción: del top-1000 se sacan los items esperados y sus gemelos (Show HN ↔ repo
  linkeado, misma URL). Falsa alarma = algún candidato restante con P(core) >= umbral
  (0.5/0.7/0.8/0.9/0.95), por kind. Las alarmas más altas se revisan a mano: pueden ser
  implementaciones reales no listadas (en el análisis de fallos de la iteración 2, 4 de 5 reales
  tenían alternativas legítimas en el top-5).
- Positivos: casos con el item esperado dentro del top-1000; recall por umbral del máximo P(core)
  entre los items esperados presentes.
- Estimación (sep-2026, candidatos MiniLM): ~562 tokens de entrada por par (p95 ~750). Haiku 4.5:
  ~$35 con Batches (~$70 estándar, medido en el piloto: ~770 tokens/par) para 76.000 pares; Jev: ~$1.8 (solo entrada, $0.042/Mtok),
  ~63 min al límite de 1.200 req/min. Parciales opcionales: +29.000 pares (Haiku ~$13 batch, Jev ~$0.9).

## Holdout temporal (oct-2026): negativos plausibles

Todo el set de evaluación son cosas que ya existen; la remoción no sirve como negativo (las alarmas
adjudicadas eran implementaciones reales). El holdout mide qué dice el sistema de ideas que todavía no
existían en una fecha T. Reporte: `data/eval/holdout_temporal.md`.

```bash
uv run gapfinder holdout retrieve        # top-1000 sobre el corpus anterior a T (embeddings MiniLM filtrados)
uv run gapfinder holdout verify --budget 1.26   # Jev vía OpenRouter por tandas, con tope de gasto real
uv run gapfinder holdout report          # data/eval/holdout_temporal.md
uv run gapfinder holdout review          # adjudicación humana (data/eval/holdout_review_human.jsonl)
```

Decisiones de la sesión (sin supervisión; documentadas también en el reporte):
- **T = 2024-01-01**: ~136 mil Show HN y ~402 mil repos antes; ~82 mil Show HN después.
- Corpus restringido: Show HN publicados y repos creados antes de T (528.865 items), con los embeddings
  MiniLM existentes y los posteriores a T enmascarados (sin re-embeber).
- Ideas: Show HN posteriores a T con >= 20 puntos y >= 400 caracteres de texto real; fuera títulos de
  versión/relanzamiento, repos enlazados creados antes de T y dominios con Show HN previo (3.926
  elegibles). Muestra barajada (semilla 11); Claude clasifica si es software y se quedan las primeras 35.
- Descripciones con el mismo método que los known cases (Claude `claude-opus-5`, prompt v2, llm5 + RRF),
  sin nombrar producto/marca/URL; `leakage_flag` en 2 ideas cuyo nombre es un término de categoría.
- **35 ideas y no 50**: el tope de $2.00 se aplicó a todo el gasto de la sesión (Claude + Jev). Costo
  real: Claude $0.731 (40 ideas con consultas) + Jev $1.171 (35.000 pares, 0 errores) = **$1.90**.
  Saldo de OpenRouter antes de empezar: $2.17.
- Resultado: 8 ya construido (23%), 7 revisar (20%), 20 no (57%). Requiere adjudicación humana.

Adjudicación humana: ver `gapfinder review` (abajo). La cola del holdout es por idea: las 20 "no" en orden
al azar (semilla fija), una tecla por idea viendo sus 3 mejores candidatos -> `data/eval/holdout_review_ideas.jsonl`
y `data/eval/holdout_review_result.md` (% hueco y % equivalente con IC 95% de Wilson). Las respuestas del formato
anterior por par (`holdout_review_human.jsonl`) se convierten al cargar: un "s" decide la idea; si no, solo
ideas con sus 3 pares respondidos.

## Revisión humana: `gapfinder review`

Un solo menú con todas las colas y su progreso (hechos/total); cada respuesta se guarda al instante en un jsonl
y se retoma donde quedaste; `q` guarda y vuelve al menú. Una cola cuyo paso no terminó aparece "pendiente".

```bash
uv run gapfinder review
```

- a) etiquetas de reales: los 4 positivos del piloto juzgados "no" (k mantener / p parcial / d descartar /
  ? no sé) -> `data/eval/label_review_human.jsonl`; no toca known_cases.json.
- b) holdout temporal por idea (1/2/3 equivalente, p parcial, n hueco, ? no sé, o+número abre la URL).
- c) Ask HN, extracción: ¿es un pedido real? (s/n) y etiqueta según los comentarios (e existe / p parcial /
  n no existe / ? incierto). Los 40 elegidos para la Fase 4 van primero -> `data/eval/askhn_extract_review_human.jsonl`.
- d) Fase 4, pares: por idea la decisión del sistema y su mejor candidato (top-3 si dijo "no"); s/p/n/? y
  o abre la URL -> `data/eval/phase4_review_human.jsonl`.
- e) candidatos a hueco: los 12 huecos fuertes en orden al azar (semilla fija) y después, opcional, los 19 de zona
  gris; por pedido sus 3 mejores candidatos. n hueco real / 1-2-3 ese candidato es equivalente / x existe fuera de
  los candidatos / p parcial / s no es software / ? no sé (x, p y s piden una nota); h abre el hilo, o+número el
  candidato -> `data/eval/gap_review_human.jsonl` y `data/eval/gap_review_result.md` (precisión = hueco real /
  juzgadas, IC 95% de Wilson, por nivel).

## Fase 4 (oct-2026): lado de demanda con Ask HN

Pedidos reales ("Ask HN: is there a tool for…?") como ideas con demanda; los comentarios dan una etiqueta
aproximada ("sí, existe X" / "busqué y no hay"). Reporte: `data/eval/phase4_askhn.md`. Código: `askhn.py`.

```bash
uv run gapfinder askhn collect    # Algolia (tags=ask_hn), 16 consultas, filtros sin LLM, comentarios; cache en data/cache/askhn/
uv run gapfinder askhn extract    # LLM barato vía OpenRouter: pedido, idea, herramientas sugeridas, etiqueta (reanudable)
uv run gapfinder askhn select     # hasta 40 pedidos balanceados por etiqueta (data/askhn/selected.json)
uv run gapfinder askhn run        # por idea: consultas llm5 -> top-1000 anterior al Ask -> Jev; con tope de gasto, reanudable
uv run gapfinder askhn report     # data/eval/phase4_askhn.md
```

Decisiones (documentadas también en el reporte):
- **Recolección**: >= 5 puntos y >= 3 comentarios (filtro de Algolia), Asks desde 2015-01-01 (antes, el corpus
  enmascarado a la fecha del Ask queda chico), título con forma de pedido, sin empleo/carrera, palabra de
  software en título o texto; los "How do you…" además necesitan la palabra de software en el título (si no, son
  consejos: "How do you deal with…"). 8.568 Asks únicos -> 397 filtrados.
- **Extracción**: `openai/gpt-oss-120b` vía OpenRouter ($0.037/$0.17 por Mtok, ~$0.0003 por Ask), validado en 10
  casos (`data/askhn/extract_validation.log`). Con el schema estricto degeneró en 39/397 salidas ("....", nombres
  vacíos): validación + reintento, tercer intento con `qwen/qwen3-30b-a3b-instruct-2507`; las salidas inválidas
  quedan archivadas con su costo (`extractions_descartadas.json`).
- **Mapeo al corpus** con `CorpusIndex` (repo, URL exacta, dominio validado por nombre); sin URL, por nombre exacto
  de un repo cuyo dueño es el proyecto (`sphinx-doc/sphinx` sí, `zdavatz/spreadsheet` no); URLs de tiendas de apps
  no se mapean por dominio.
- **Selección**: cupos no_existe 12, existe-con-item-en-corpus 12, parcial 8, existe-sin-item 4, incierto 4 (el
  sobrante se completa por puntos); orden de proceso: no_existe y existe-con-item intercalados primero.
- **Corpus por Ask**: items creados antes de la fecha de cada Ask, con los embeddings MiniLM existentes (sin
  re-embeber). idea extraída = query_core; reformulaciones con claude-opus-5 y prompt v2 (rama "need").
- **Anthropic se quedó sin crédito** a mitad de la corrida (se frenó como un 402): las consultas siguen con el
  mismo modelo y prompt vía OpenRouter (`anthropic/claude-opus-5`). La única idea procesada antes tenía una
  extracción degenerada: sus veredictos quedaron archivados en `verdicts_jev_askhn_descartado.jsonl`.
- **Tope de gasto**: $0.90 al principio; con la recarga de OpenRouter, $2.40 para las 40 ideas (~$0.051 por idea:
  Claude $0.017 + Jev $0.034).

## Candidatos a hueco (oct-2026): extracción automática y lista para revisar

En vez de etiquetar a mano los 397 Asks, un LLM hace la extracción y lo que se revisa es la lista final de
huecos (`data/eval/gap_candidates.md`). Código: `gaps.py`.

```bash
uv run gapfinder gaps extract --limit 10   # prueba; sin --limit procesa los 397 (cache JSONL por id, reanudable)
uv run gapfinder gaps compare              # opción barata vs método completo sobre los 40 de la Fase 4
uv run gapfinder gaps run                  # pedidos reales: top-200 para todos y K=1000 para los huecos; reanudable
uv run gapfinder gaps report               # data/eval/gap_candidates.md
```

- Extracción v2 (`gpt-oss-120b` vía OpenRouter, $0.075 los 397): `{id, pedido_real, etiqueta e/p/n/?,
  pedido_resumido, justificacion}`, prompt con la definición de las etiquetas y 4 ejemplos few-shot
  (`data/askhn/extract_v2.jsonl`). 242 pedidos reales.
- Retrieval: query_core = pedido_resumido, reformulaciones con gpt-oss y el prompt v2 (no Opus 5: costo), corpus
  anterior a la fecha del Ask, top-200 y Jev; los que quedan sin match >= 0.85 se re-corren con K=1000 antes de
  entrar a la lista. En los 40 de la Fase 4, la opción barata pasó 2 de 18 matches a hueco
  (`data/eval/gap_compare_k200.md`).
- Frena ante 401/402/403 y si el saldo de OpenRouter baja de $0.50.
- Niveles del reporte (oct-2026, offline sobre los veredictos cacheados; antes era hueco = sin match >= 0.85, 119
  huecos con 69 "existe"): match >= 0.85 (123) -> no es software (44: encuesta 20, hardware 8, "¿se puede…?" 8,
  contenido 8; heurístico `gaps.no_software` sobre el título del Ask y el sintagma nominal del pedido) -> descartado
  por etiqueta e (44) -> **hueco fuerte** < 0.60 con etiqueta n/p (12) -> zona gris (19). El 0.60 no está calibrado.

## Tests

```bash
uv run pytest
```
