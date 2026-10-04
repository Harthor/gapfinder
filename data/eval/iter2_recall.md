# Retrieval — iteración 2

R@N con N justo: las consultas de un caso se fusionan con RRF (k=60) en un único ranking y se corta a N. `raw` = título + descripción (iteración 1); `core` = query_core de Claude (en sintéticos, la necesidad); `llm5` = core + 4 reformulaciones de Claude; `tmpl4` = las 4 plantillas de la iteración 1. `hybrid` = RRF(embeddings + BM25). `n` = casos con algún item esperado en el índice.

## Tabla principal (sin búsqueda dirigida)

| casos | sistema | modelo | consultas | n | R@50 | R@200 | R@1000 |
|---|---|---|---|---|---|---|---|
| real | emb | minilm | raw | 12 | 0.08 | 0.33 | 0.67 |
| real | emb | minilm | core | 12 | 0.25 | 0.67 | 0.75 |
| real | emb | minilm | llm5 | 12 | 0.50 | 0.58 | 0.92 |
| real | emb | bge | raw | 12 | 0.33 | 0.42 | 0.58 |
| real | emb | bge | core | 12 | 0.33 | 0.58 | 0.83 |
| real | emb | bge | llm5 | 12 | 0.25 | 0.58 | 0.83 |
| real | bm25 | - | raw | 12 | 0.08 | 0.33 | 0.58 |
| real | bm25 | - | core | 12 | 0.25 | 0.58 | 0.67 |
| real | bm25 | - | llm5 | 12 | 0.17 | 0.58 | 0.83 |
| real | hybrid | minilm | raw | 12 | 0.17 | 0.25 | 0.58 |
| real | hybrid | minilm | core | 12 | 0.33 | 0.75 | 0.75 |
| real | hybrid | minilm | llm5 | 12 | 0.58 | 0.75 | 0.75 |
| real | hybrid | bge | raw | 12 | 0.33 | 0.42 | 0.50 |
| real | hybrid | bge | core | 12 | 0.42 | 0.67 | 0.83 |
| real | hybrid | bge | llm5 | 12 | 0.42 | 0.75 | 0.75 |
| real sin label_note | emb | minilm | raw | 9 | 0.11 | 0.44 | 0.78 |
| real sin label_note | emb | minilm | core | 9 | 0.33 | 0.78 | 0.89 |
| real sin label_note | emb | minilm | llm5 | 9 | 0.67 | 0.78 | 0.89 |
| real sin label_note | emb | bge | raw | 9 | 0.44 | 0.56 | 0.67 |
| real sin label_note | emb | bge | core | 9 | 0.44 | 0.67 | 0.89 |
| real sin label_note | emb | bge | llm5 | 9 | 0.33 | 0.67 | 0.89 |
| real sin label_note | bm25 | - | raw | 9 | 0.11 | 0.44 | 0.78 |
| real sin label_note | bm25 | - | core | 9 | 0.33 | 0.67 | 0.78 |
| real sin label_note | bm25 | - | llm5 | 9 | 0.22 | 0.78 | 1.00 |
| real sin label_note | hybrid | minilm | raw | 9 | 0.22 | 0.33 | 0.67 |
| real sin label_note | hybrid | minilm | core | 9 | 0.44 | 0.89 | 0.89 |
| real sin label_note | hybrid | minilm | llm5 | 9 | 0.78 | 0.89 | 0.89 |
| real sin label_note | hybrid | bge | raw | 9 | 0.44 | 0.56 | 0.67 |
| real sin label_note | hybrid | bge | core | 9 | 0.44 | 0.78 | 0.89 |
| real sin label_note | hybrid | bge | llm5 | 9 | 0.56 | 0.89 | 0.89 |
| partial sin heurísticos | emb | minilm | raw | 16 | 0.19 | 0.31 | 0.62 |
| partial sin heurísticos | emb | minilm | core | 16 | 0.25 | 0.31 | 0.56 |
| partial sin heurísticos | emb | minilm | llm5 | 16 | 0.25 | 0.31 | 0.62 |
| partial sin heurísticos | emb | bge | raw | 16 | 0.06 | 0.19 | 0.50 |
| partial sin heurísticos | emb | bge | core | 16 | 0.25 | 0.25 | 0.31 |
| partial sin heurísticos | emb | bge | llm5 | 16 | 0.25 | 0.31 | 0.44 |
| partial sin heurísticos | bm25 | - | raw | 16 | 0.19 | 0.31 | 0.44 |
| partial sin heurísticos | bm25 | - | core | 16 | 0.25 | 0.38 | 0.38 |
| partial sin heurísticos | bm25 | - | llm5 | 16 | 0.38 | 0.44 | 0.56 |
| partial sin heurísticos | hybrid | minilm | raw | 16 | 0.31 | 0.31 | 0.50 |
| partial sin heurísticos | hybrid | minilm | core | 16 | 0.38 | 0.38 | 0.44 |
| partial sin heurísticos | hybrid | minilm | llm5 | 16 | 0.44 | 0.44 | 0.56 |
| partial sin heurísticos | hybrid | bge | raw | 16 | 0.25 | 0.31 | 0.50 |
| partial sin heurísticos | hybrid | bge | core | 16 | 0.31 | 0.31 | 0.44 |
| partial sin heurísticos | hybrid | bge | llm5 | 16 | 0.44 | 0.50 | 0.56 |
| partial (todos) | emb | minilm | raw | 29 | 0.10 | 0.21 | 0.41 |
| partial (todos) | emb | minilm | core | 29 | 0.14 | 0.21 | 0.45 |
| partial (todos) | emb | minilm | llm5 | 29 | 0.14 | 0.21 | 0.45 |
| partial (todos) | emb | bge | raw | 29 | 0.07 | 0.14 | 0.34 |
| partial (todos) | emb | bge | core | 29 | 0.14 | 0.21 | 0.31 |
| partial (todos) | emb | bge | llm5 | 29 | 0.14 | 0.21 | 0.38 |
| partial (todos) | bm25 | - | raw | 29 | 0.10 | 0.17 | 0.24 |
| partial (todos) | bm25 | - | core | 29 | 0.17 | 0.28 | 0.31 |
| partial (todos) | bm25 | - | llm5 | 29 | 0.24 | 0.31 | 0.45 |
| partial (todos) | hybrid | minilm | raw | 29 | 0.17 | 0.17 | 0.34 |
| partial (todos) | hybrid | minilm | core | 29 | 0.24 | 0.24 | 0.38 |
| partial (todos) | hybrid | minilm | llm5 | 29 | 0.28 | 0.28 | 0.48 |
| partial (todos) | hybrid | bge | raw | 29 | 0.14 | 0.17 | 0.34 |
| partial (todos) | hybrid | bge | core | 29 | 0.21 | 0.21 | 0.41 |
| partial (todos) | hybrid | bge | llm5 | 29 | 0.28 | 0.38 | 0.45 |

## Punto 1: plantillas de la iteración 1, reform 1 vs reform 4 con RRF y N justo (embeddings, sin dirigida)

| casos | modelo | consultas | n | R@50 | R@200 | R@1000 |
|---|---|---|---|---|---|---|
| real | minilm | 1 (need) | 12 | 0.08 | 0.33 | 0.67 |
| real | minilm | 4 plantillas, RRF | 12 | 0.08 | 0.25 | 0.67 |
| real | bge | 1 (need) | 12 | 0.33 | 0.42 | 0.58 |
| real | bge | 4 plantillas, RRF | 12 | 0.25 | 0.50 | 0.58 |
| real sin label_note | minilm | 1 (need) | 9 | 0.11 | 0.44 | 0.78 |
| real sin label_note | minilm | 4 plantillas, RRF | 9 | 0.11 | 0.33 | 0.78 |
| real sin label_note | bge | 1 (need) | 9 | 0.44 | 0.56 | 0.67 |
| real sin label_note | bge | 4 plantillas, RRF | 9 | 0.33 | 0.67 | 0.67 |
| partial sin heurísticos | minilm | 1 (need) | 16 | 0.19 | 0.31 | 0.62 |
| partial sin heurísticos | minilm | 4 plantillas, RRF | 16 | 0.12 | 0.31 | 0.56 |
| partial sin heurísticos | bge | 1 (need) | 16 | 0.06 | 0.19 | 0.50 |
| partial sin heurísticos | bge | 4 plantillas, RRF | 16 | 0.06 | 0.31 | 0.44 |
| partial (todos) | minilm | 1 (need) | 29 | 0.10 | 0.21 | 0.41 |
| partial (todos) | minilm | 4 plantillas, RRF | 29 | 0.07 | 0.17 | 0.34 |
| partial (todos) | bge | 1 (need) | 29 | 0.07 | 0.14 | 0.34 |
| partial (todos) | bge | 4 plantillas, RRF | 29 | 0.07 | 0.21 | 0.31 |
| synthetic | minilm | 1 (need) | 64 | 0.38 | 0.61 | 0.81 |
| synthetic | minilm | 4 plantillas, RRF | 64 | 0.36 | 0.64 | 0.80 |
| synthetic | bge | 1 (need) | 64 | 0.50 | 0.72 | 0.83 |
| synthetic | bge | 4 plantillas, RRF | 64 | 0.42 | 0.66 | 0.78 |

## Sintéticos (sin dirigida)

| sistema | modelo | consultas | n | R@50 | R@200 | R@1000 |
|---|---|---|---|---|---|---|
| emb | minilm | core | 64 | 0.38 | 0.61 | 0.81 |
| emb | minilm | llm5 | 64 | 0.59 | 0.72 | 0.92 |
| emb | bge | core | 64 | 0.50 | 0.72 | 0.83 |
| emb | bge | llm5 | 64 | 0.64 | 0.78 | 0.94 |
| bm25 | - | core | 64 | 0.03 | 0.08 | 0.19 |
| bm25 | - | llm5 | 64 | 0.41 | 0.56 | 0.77 |
| hybrid | minilm | core | 64 | 0.33 | 0.48 | 0.78 |
| hybrid | minilm | llm5 | 64 | 0.61 | 0.84 | 0.95 |
| hybrid | bge | core | 64 | 0.39 | 0.64 | 0.78 |
| hybrid | bge | llm5 | 64 | 0.70 | 0.84 | 0.95 |

## Ablación title_only en sintéticos (embeddings, consulta = necesidad, sin dirigida)

| modelo | origen | n | R@50 real → title_only | R@200 | R@1000 |
|---|---|---|---|---|---|
| minilm | author_comment | 10 | 0.50 → 0.30 | 0.50 → 0.40 | 0.90 → 0.50 |
| minilm | author_reply | 10 | 0.30 → 0.50 | 0.40 → 0.60 | 0.60 → 0.80 |
| minilm | current | 8 | 0.12 → 0.12 | 0.38 → 0.12 | 0.62 → 0.38 |
| minilm | github_corpus | 12 | 0.33 → 0.33 | 0.58 → 0.50 | 0.83 → 0.75 |
| minilm | native | 24 | 0.46 → 0.29 | 0.83 → 0.42 | 0.92 → 0.62 |
| minilm | todos | 64 | 0.38 → 0.31 | 0.61 → 0.42 | 0.81 → 0.62 |
| bge | author_comment | 10 | 0.50 → 0.50 | 0.70 → 0.50 | 0.90 → 0.60 |
| bge | author_reply | 10 | 0.30 → 0.50 | 0.70 → 0.60 | 0.70 → 0.80 |
| bge | current | 8 | 0.25 → 0.12 | 0.38 → 0.25 | 0.62 → 0.38 |
| bge | github_corpus | 12 | 0.58 → 0.25 | 0.75 → 0.50 | 0.92 → 0.75 |
| bge | native | 24 | 0.62 → 0.33 | 0.83 → 0.54 | 0.88 → 0.67 |
| bge | todos | 64 | 0.50 → 0.34 | 0.72 → 0.50 | 0.83 → 0.66 |

## Pareado human vs claude (8 pares, sin dirigida)

Par con leakage_flag: pair-33480679 (filas `sin flag` lo excluyen).

| sistema | modelo | consultas | pares | @N | recall human | recall claude | ambos | solo human | solo claude | ninguno |
|---|---|---|---|---|---|---|---|---|---|---|
| emb | minilm | core | 8 (todos) | 50 | 0.38 | 0.50 | 2 | 1 | 2 | 3 |
| emb | minilm | core | 8 (todos) | 200 | 0.62 | 0.88 | 5 | 0 | 2 | 1 |
| emb | minilm | core | 8 (todos) | 1000 | 0.88 | 0.88 | 7 | 0 | 0 | 1 |
| emb | minilm | core | 7 (sin flag) | 50 | 0.43 | 0.57 | 2 | 1 | 2 | 2 |
| emb | minilm | core | 7 (sin flag) | 200 | 0.57 | 0.86 | 4 | 0 | 2 | 1 |
| emb | minilm | core | 7 (sin flag) | 1000 | 0.86 | 0.86 | 6 | 0 | 0 | 1 |
| emb | minilm | llm5 | 8 (todos) | 50 | 0.12 | 0.88 | 1 | 0 | 6 | 1 |
| emb | minilm | llm5 | 8 (todos) | 200 | 0.62 | 0.88 | 5 | 0 | 2 | 1 |
| emb | minilm | llm5 | 8 (todos) | 1000 | 0.88 | 1.00 | 7 | 0 | 1 | 0 |
| emb | minilm | llm5 | 7 (sin flag) | 50 | 0.00 | 0.86 | 0 | 0 | 6 | 1 |
| emb | minilm | llm5 | 7 (sin flag) | 200 | 0.57 | 0.86 | 4 | 0 | 2 | 1 |
| emb | minilm | llm5 | 7 (sin flag) | 1000 | 0.86 | 1.00 | 6 | 0 | 1 | 0 |
| emb | bge | core | 8 (todos) | 50 | 0.25 | 0.75 | 2 | 0 | 4 | 2 |
| emb | bge | core | 8 (todos) | 200 | 0.62 | 0.88 | 5 | 0 | 2 | 1 |
| emb | bge | core | 8 (todos) | 1000 | 0.75 | 0.88 | 6 | 0 | 1 | 1 |
| emb | bge | core | 7 (sin flag) | 50 | 0.29 | 0.86 | 2 | 0 | 4 | 1 |
| emb | bge | core | 7 (sin flag) | 200 | 0.57 | 0.86 | 4 | 0 | 2 | 1 |
| emb | bge | core | 7 (sin flag) | 1000 | 0.71 | 0.86 | 5 | 0 | 1 | 1 |
| emb | bge | llm5 | 8 (todos) | 50 | 0.38 | 0.62 | 2 | 1 | 3 | 2 |
| emb | bge | llm5 | 8 (todos) | 200 | 0.50 | 0.88 | 4 | 0 | 3 | 1 |
| emb | bge | llm5 | 8 (todos) | 1000 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |
| emb | bge | llm5 | 7 (sin flag) | 50 | 0.29 | 0.71 | 2 | 0 | 3 | 2 |
| emb | bge | llm5 | 7 (sin flag) | 200 | 0.43 | 0.86 | 3 | 0 | 3 | 1 |
| emb | bge | llm5 | 7 (sin flag) | 1000 | 1.00 | 1.00 | 7 | 0 | 0 | 0 |
| bm25 | - | core | 8 (todos) | 50 | 0.00 | 0.00 | 0 | 0 | 0 | 8 |
| bm25 | - | core | 8 (todos) | 200 | 0.25 | 0.00 | 0 | 2 | 0 | 6 |
| bm25 | - | core | 8 (todos) | 1000 | 0.50 | 0.12 | 0 | 4 | 1 | 3 |
| bm25 | - | core | 7 (sin flag) | 50 | 0.00 | 0.00 | 0 | 0 | 0 | 7 |
| bm25 | - | core | 7 (sin flag) | 200 | 0.29 | 0.00 | 0 | 2 | 0 | 5 |
| bm25 | - | core | 7 (sin flag) | 1000 | 0.43 | 0.14 | 0 | 3 | 1 | 3 |
| bm25 | - | llm5 | 8 (todos) | 50 | 0.25 | 0.50 | 2 | 0 | 2 | 4 |
| bm25 | - | llm5 | 8 (todos) | 200 | 0.38 | 0.50 | 2 | 1 | 2 | 3 |
| bm25 | - | llm5 | 8 (todos) | 1000 | 0.75 | 0.62 | 4 | 2 | 1 | 1 |
| bm25 | - | llm5 | 7 (sin flag) | 50 | 0.14 | 0.43 | 1 | 0 | 2 | 4 |
| bm25 | - | llm5 | 7 (sin flag) | 200 | 0.29 | 0.43 | 1 | 1 | 2 | 3 |
| bm25 | - | llm5 | 7 (sin flag) | 1000 | 0.71 | 0.57 | 3 | 2 | 1 | 1 |
| hybrid | minilm | core | 8 (todos) | 50 | 0.25 | 0.38 | 1 | 1 | 2 | 4 |
| hybrid | minilm | core | 8 (todos) | 200 | 0.50 | 0.62 | 2 | 2 | 3 | 1 |
| hybrid | minilm | core | 8 (todos) | 1000 | 0.88 | 1.00 | 7 | 0 | 1 | 0 |
| hybrid | minilm | core | 7 (sin flag) | 50 | 0.29 | 0.43 | 1 | 1 | 2 | 3 |
| hybrid | minilm | core | 7 (sin flag) | 200 | 0.57 | 0.57 | 2 | 2 | 2 | 1 |
| hybrid | minilm | core | 7 (sin flag) | 1000 | 0.86 | 1.00 | 6 | 0 | 1 | 0 |
| hybrid | minilm | llm5 | 8 (todos) | 50 | 0.25 | 0.75 | 2 | 0 | 4 | 2 |
| hybrid | minilm | llm5 | 8 (todos) | 200 | 0.88 | 1.00 | 7 | 0 | 1 | 0 |
| hybrid | minilm | llm5 | 8 (todos) | 1000 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |
| hybrid | minilm | llm5 | 7 (sin flag) | 50 | 0.14 | 0.71 | 1 | 0 | 4 | 2 |
| hybrid | minilm | llm5 | 7 (sin flag) | 200 | 0.86 | 1.00 | 6 | 0 | 1 | 0 |
| hybrid | minilm | llm5 | 7 (sin flag) | 1000 | 1.00 | 1.00 | 7 | 0 | 0 | 0 |
| hybrid | bge | core | 8 (todos) | 50 | 0.25 | 0.50 | 2 | 0 | 2 | 4 |
| hybrid | bge | core | 8 (todos) | 200 | 0.50 | 0.88 | 4 | 0 | 3 | 1 |
| hybrid | bge | core | 8 (todos) | 1000 | 0.75 | 1.00 | 6 | 0 | 2 | 0 |
| hybrid | bge | core | 7 (sin flag) | 50 | 0.29 | 0.57 | 2 | 0 | 2 | 3 |
| hybrid | bge | core | 7 (sin flag) | 200 | 0.43 | 0.86 | 3 | 0 | 3 | 1 |
| hybrid | bge | core | 7 (sin flag) | 1000 | 0.71 | 1.00 | 5 | 0 | 2 | 0 |
| hybrid | bge | llm5 | 8 (todos) | 50 | 0.50 | 0.88 | 4 | 0 | 3 | 1 |
| hybrid | bge | llm5 | 8 (todos) | 200 | 0.62 | 1.00 | 5 | 0 | 3 | 0 |
| hybrid | bge | llm5 | 8 (todos) | 1000 | 1.00 | 1.00 | 8 | 0 | 0 | 0 |
| hybrid | bge | llm5 | 7 (sin flag) | 50 | 0.43 | 0.86 | 3 | 0 | 3 | 1 |
| hybrid | bge | llm5 | 7 (sin flag) | 200 | 0.57 | 1.00 | 4 | 0 | 3 | 0 |
| hybrid | bge | llm5 | 7 (sin flag) | 1000 | 1.00 | 1.00 | 7 | 0 | 0 | 0 |

Negativos: no hay casos `negative`; se omiten.

