# gapfinder

Detecta huecos reales: ideas con demanda actual (`data/ideas.json`) cruzadas contra un corpus
histórico de cosas ya construidas (Show HN + GitHub).

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

## Fase 3 — verificador (preparada, sin correr contra Jev)

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
```

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

## Tests

```bash
uv run pytest
```
