# Fase 2 — recall de retrieval

Un caso cuenta en @N si algún item esperado está en el top-N de alguna reformulación. `reform 1` = solo la necesidad; `reform 4` = unión de need / keywords / plain / show_hn. `dirigida` = índice con los items agregados por la búsqueda dirigida. `n` = casos con algún item esperado en ese índice (los demás miden cobertura, no retrieval).

## Recall por kind × modelo × reformulaciones × búsqueda dirigida

| kind | modelo | reform | dirigida | n | sin item | R@50 | R@200 | R@1000 |
|---|---|---|---|---|---|---|---|---|
| synthetic | e5 | 1 | sin | 64 | 0 | 0.14 | 0.19 | 0.34 |
| synthetic | e5 | 4 | sin | 64 | 0 | 0.17 | 0.23 | 0.50 |
| synthetic | e5 | 1 | con | 64 | 0 | 0.14 | 0.19 | 0.34 |
| synthetic | e5 | 4 | con | 64 | 0 | 0.16 | 0.23 | 0.48 |
| synthetic | minilm | 1 | sin | 64 | 0 | 0.38 | 0.61 | 0.81 |
| synthetic | minilm | 4 | sin | 64 | 0 | 0.48 | 0.67 | 0.86 |
| synthetic | minilm | 1 | con | 64 | 0 | 0.36 | 0.59 | 0.81 |
| synthetic | minilm | 4 | con | 64 | 0 | 0.45 | 0.66 | 0.86 |
| real | e5 | 1 | sin | 12 | 0 | 0.25 | 0.25 | 0.33 |
| real | e5 | 4 | sin | 12 | 0 | 0.25 | 0.25 | 0.58 |
| real | e5 | 1 | con | 12 | 0 | 0.25 | 0.25 | 0.33 |
| real | e5 | 4 | con | 12 | 0 | 0.25 | 0.25 | 0.58 |
| real | minilm | 1 | sin | 12 | 0 | 0.08 | 0.33 | 0.67 |
| real | minilm | 4 | sin | 12 | 0 | 0.17 | 0.42 | 0.67 |
| real | minilm | 1 | con | 12 | 0 | 0.08 | 0.25 | 0.67 |
| real | minilm | 4 | con | 12 | 0 | 0.17 | 0.33 | 0.67 |
| partial | e5 | 1 | sin | 29 | 29 | 0.00 | 0.10 | 0.21 |
| partial | e5 | 4 | sin | 29 | 29 | 0.07 | 0.21 | 0.38 |
| partial | e5 | 1 | con | 29 | 29 | 0.00 | 0.10 | 0.21 |
| partial | e5 | 4 | con | 29 | 29 | 0.07 | 0.21 | 0.38 |
| partial | minilm | 1 | sin | 29 | 29 | 0.10 | 0.21 | 0.41 |
| partial | minilm | 4 | sin | 29 | 29 | 0.14 | 0.28 | 0.52 |
| partial | minilm | 1 | con | 29 | 29 | 0.10 | 0.21 | 0.41 |
| partial | minilm | 4 | con | 29 | 29 | 0.14 | 0.28 | 0.52 |
| partial (sin heurísticos) | e5 | 1 | sin | 16 | 42 | 0.00 | 0.19 | 0.31 |
| partial (sin heurísticos) | e5 | 4 | sin | 16 | 42 | 0.06 | 0.25 | 0.50 |
| partial (sin heurísticos) | e5 | 1 | con | 16 | 42 | 0.00 | 0.19 | 0.31 |
| partial (sin heurísticos) | e5 | 4 | con | 16 | 42 | 0.06 | 0.25 | 0.50 |
| partial (sin heurísticos) | minilm | 1 | sin | 16 | 42 | 0.19 | 0.31 | 0.62 |
| partial (sin heurísticos) | minilm | 4 | sin | 16 | 42 | 0.19 | 0.44 | 0.62 |
| partial (sin heurísticos) | minilm | 1 | con | 16 | 42 | 0.19 | 0.31 | 0.62 |
| partial (sin heurísticos) | minilm | 4 | con | 16 | 42 | 0.19 | 0.44 | 0.62 |

Tamaño medio de la unión de candidatos (reform 4), por caso:

| modelo | dirigida | @50 | @200 | @1000 |
|---|---|---|---|---|
| e5 | sin | 139 | 533 | 2520 |
| e5 | con | 138 | 531 | 2517 |
| minilm | sin | 124 | 467 | 2187 |
| minilm | con | 124 | 466 | 2184 |

## Por origen del texto del item esperado (reform 4, dirigida = con)

| kind | origen | modelo | n | R@50 | R@200 | R@1000 |
|---|---|---|---|---|---|---|
| synthetic | author_comment | e5 | 10 | 0.10 | 0.10 | 0.30 |
| synthetic | author_comment | minilm | 10 | 0.60 | 0.60 | 1.00 |
| synthetic | author_reply | e5 | 10 | 0.20 | 0.30 | 0.50 |
| synthetic | author_reply | minilm | 10 | 0.30 | 0.50 | 0.70 |
| synthetic | current | e5 | 8 | 0.00 | 0.38 | 0.38 |
| synthetic | current | minilm | 8 | 0.25 | 0.50 | 0.75 |
| synthetic | github_corpus | e5 | 12 | 0.08 | 0.17 | 0.58 |
| synthetic | github_corpus | minilm | 12 | 0.33 | 0.58 | 0.83 |
| synthetic | native | e5 | 24 | 0.25 | 0.25 | 0.54 |
| synthetic | native | minilm | 24 | 0.58 | 0.83 | 0.92 |
| real | enriched | e5 | 12 | 0.25 | 0.25 | 0.58 |
| real | enriched | minilm | 12 | 0.17 | 0.33 | 0.67 |
| partial | enriched | e5 | 28 | 0.07 | 0.21 | 0.39 |
| partial | enriched | minilm | 28 | 0.14 | 0.29 | 0.50 |
| partial | title_only | e5 | 1 | 0.00 | 0.00 | 0.00 |
| partial | title_only | minilm | 1 | 0.00 | 0.00 | 1.00 |
| partial (sin heurísticos) | enriched | e5 | 16 | 0.06 | 0.25 | 0.50 |
| partial (sin heurísticos) | enriched | minilm | 16 | 0.19 | 0.44 | 0.62 |

## Ablación en sintéticos: item esperado forzado a title_only (reform 4, dirigida = sin)

| origen original | modelo | n | R@50 real → title_only | R@200 | R@1000 |
|---|---|---|---|---|---|
| author_comment | e5 | 10 | 0.10 → 0.20 | 0.10 → 0.20 | 0.30 → 0.40 |
| author_comment | minilm | 10 | 0.60 → 0.40 | 0.60 → 0.60 | 1.00 → 0.80 |
| author_reply | e5 | 10 | 0.20 → 0.30 | 0.30 → 0.50 | 0.50 → 0.70 |
| author_reply | minilm | 10 | 0.30 → 0.50 | 0.50 → 0.70 | 0.70 → 0.80 |
| current | e5 | 8 | 0.00 → 0.12 | 0.38 → 0.25 | 0.38 → 0.25 |
| current | minilm | 8 | 0.38 → 0.12 | 0.50 → 0.38 | 0.75 → 0.50 |
| github_corpus | e5 | 12 | 0.17 → 0.42 | 0.17 → 0.42 | 0.67 → 0.67 |
| github_corpus | minilm | 12 | 0.33 → 0.42 | 0.58 → 0.58 | 0.83 → 0.75 |
| native | e5 | 24 | 0.25 → 0.29 | 0.25 → 0.38 | 0.54 → 0.54 |
| native | minilm | 24 | 0.62 → 0.38 | 0.88 → 0.58 | 0.92 → 0.71 |
| todos | e5 | 64 | 0.17 → 0.28 | 0.23 → 0.36 | 0.50 → 0.53 |
| todos | minilm | 64 | 0.48 → 0.38 | 0.67 → 0.58 | 0.86 → 0.72 |

## Pareado human vs claude (mismo item; dirigida = sin)

Pares donde uno de los dos casos tiene `leakage_flag`: pair-33480679. Filas `sin flag` los excluyen.

| modelo | reform | pares | @N | recall human | recall claude | ambos | solo human | solo claude | ninguno |
|---|---|---|---|---|---|---|---|---|---|
| e5 | 1 | 8 (todos) | 50 | 0.00 | 0.12 | 0 | 0 | 1 | 7 |
| e5 | 1 | 8 (todos) | 200 | 0.00 | 0.12 | 0 | 0 | 1 | 7 |
| e5 | 1 | 8 (todos) | 1000 | 0.25 | 0.38 | 1 | 1 | 2 | 4 |
| e5 | 4 | 8 (todos) | 50 | 0.12 | 0.12 | 0 | 1 | 1 | 6 |
| e5 | 4 | 8 (todos) | 200 | 0.12 | 0.12 | 0 | 1 | 1 | 6 |
| e5 | 4 | 8 (todos) | 1000 | 0.62 | 0.50 | 3 | 2 | 1 | 2 |
| e5 | 1 | 7 (sin flag) | 50 | 0.00 | 0.14 | 0 | 0 | 1 | 6 |
| e5 | 1 | 7 (sin flag) | 200 | 0.00 | 0.14 | 0 | 0 | 1 | 6 |
| e5 | 1 | 7 (sin flag) | 1000 | 0.29 | 0.43 | 1 | 1 | 2 | 3 |
| e5 | 4 | 7 (sin flag) | 50 | 0.14 | 0.14 | 0 | 1 | 1 | 5 |
| e5 | 4 | 7 (sin flag) | 200 | 0.14 | 0.14 | 0 | 1 | 1 | 5 |
| e5 | 4 | 7 (sin flag) | 1000 | 0.57 | 0.57 | 3 | 1 | 1 | 2 |
| minilm | 1 | 8 (todos) | 50 | 0.38 | 0.50 | 2 | 1 | 2 | 3 |
| minilm | 1 | 8 (todos) | 200 | 0.62 | 0.88 | 5 | 0 | 2 | 1 |
| minilm | 1 | 8 (todos) | 1000 | 0.88 | 0.88 | 7 | 0 | 0 | 1 |
| minilm | 4 | 8 (todos) | 50 | 0.38 | 0.62 | 2 | 1 | 3 | 2 |
| minilm | 4 | 8 (todos) | 200 | 0.62 | 0.88 | 5 | 0 | 2 | 1 |
| minilm | 4 | 8 (todos) | 1000 | 0.88 | 0.88 | 7 | 0 | 0 | 1 |
| minilm | 1 | 7 (sin flag) | 50 | 0.43 | 0.57 | 2 | 1 | 2 | 2 |
| minilm | 1 | 7 (sin flag) | 200 | 0.57 | 0.86 | 4 | 0 | 2 | 1 |
| minilm | 1 | 7 (sin flag) | 1000 | 0.86 | 0.86 | 6 | 0 | 0 | 1 |
| minilm | 4 | 7 (sin flag) | 50 | 0.43 | 0.57 | 2 | 1 | 2 | 2 |
| minilm | 4 | 7 (sin flag) | 200 | 0.57 | 0.86 | 4 | 0 | 2 | 1 |
| minilm | 4 | 7 (sin flag) | 1000 | 0.86 | 0.86 | 6 | 0 | 0 | 1 |

Negativos: no hay casos `negative` (Constellate no dio veredictos `no`); se omiten.

