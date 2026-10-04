# query_core v1 vs v2 (v2 permite términos de categoría)

MiniLM, sin búsqueda dirigida. Sintéticos no cambian (mismas consultas). v1 = data/eval/iter2_recall.md; v2 = data/eval/iter2_v2/iter2_recall.md.

| casos | sistema | consultas | n | R@50 v1 → v2 | R@200 v1 → v2 | R@1000 v1 → v2 |
|---|---|---|---|---|---|---|
| real | emb | core | 12 | 0.25 → 0.42 | 0.67 → 0.58 | 0.75 → 0.75 |
| real | emb | llm5 | 12 | 0.50 → 0.50 | 0.58 → 0.75 | 0.92 → 0.92 |
| real | hybrid | core | 12 | 0.33 → 0.33 | 0.75 → 0.58 | 0.75 → 0.83 |
| real | hybrid | llm5 | 12 | 0.58 → 0.50 | 0.75 → 0.67 | 0.75 → 0.83 |
| real | bm25 | core | 12 | 0.25 → 0.17 | 0.58 → 0.50 | 0.67 → 0.75 |
| real | bm25 | llm5 | 12 | 0.17 → 0.25 | 0.58 → 0.50 | 0.83 → 0.83 |
| real sin label_note | emb | core | 9 | 0.33 → 0.56 | 0.78 → 0.78 | 0.89 → 0.89 |
| real sin label_note | emb | llm5 | 9 | 0.67 → 0.67 | 0.78 → 1.00 | 0.89 → 1.00 |
| real sin label_note | hybrid | core | 9 | 0.44 → 0.44 | 0.89 → 0.78 | 0.89 → 0.89 |
| real sin label_note | hybrid | llm5 | 9 | 0.78 → 0.67 | 0.89 → 0.89 | 0.89 → 1.00 |
| real sin label_note | bm25 | core | 9 | 0.33 → 0.22 | 0.67 → 0.67 | 0.78 → 0.78 |
| real sin label_note | bm25 | llm5 | 9 | 0.22 → 0.33 | 0.78 → 0.67 | 1.00 → 0.78 |
| partial sin heurísticos | emb | core | 16 | 0.25 → 0.25 | 0.31 → 0.38 | 0.56 → 0.69 |
| partial sin heurísticos | emb | llm5 | 16 | 0.25 → 0.25 | 0.31 → 0.44 | 0.62 → 0.75 |
| partial sin heurísticos | hybrid | core | 16 | 0.38 → 0.31 | 0.38 → 0.50 | 0.44 → 0.69 |
| partial sin heurísticos | hybrid | llm5 | 16 | 0.44 → 0.38 | 0.44 → 0.62 | 0.56 → 0.81 |
| partial sin heurísticos | bm25 | core | 16 | 0.25 → 0.31 | 0.38 → 0.31 | 0.38 → 0.50 |
| partial sin heurísticos | bm25 | llm5 | 16 | 0.38 → 0.38 | 0.44 → 0.50 | 0.56 → 0.69 |
| partial (todos) | emb | core | 29 | 0.14 → 0.14 | 0.21 → 0.24 | 0.45 → 0.48 |
| partial (todos) | emb | llm5 | 29 | 0.14 → 0.14 | 0.21 → 0.31 | 0.45 → 0.45 |
| partial (todos) | hybrid | core | 29 | 0.24 → 0.21 | 0.24 → 0.31 | 0.38 → 0.48 |
| partial (todos) | hybrid | llm5 | 29 | 0.28 → 0.28 | 0.28 → 0.41 | 0.48 → 0.59 |
| partial (todos) | bm25 | core | 29 | 0.17 → 0.21 | 0.28 → 0.21 | 0.31 → 0.41 |
| partial (todos) | bm25 | llm5 | 29 | 0.24 → 0.28 | 0.31 → 0.34 | 0.45 → 0.59 |

## Reales: rank del primer item esperado (emb MiniLM + llm5)

| caso | label_note | v1 | v2 |
|---|---|---|---|
| real-01fe2dbe |  | 10 | 60 |
| real-197bf4f9 |  | 241 | 82 |
| real-25a4c842 |  | 14 | 4 |
| real-47bf5f9f |  | 41 | 28 |
| real-6eb5b382 |  | 6 | 13 |
| real-6f3848c8 |  | 25 | 7 |
| real-7c597ec1 | sí | 965 | 746 |
| real-89c010f2 |  | 56 | 18 |
| real-8b190bdc | sí | 668 | — |
| real-a6c38804 |  | 27 | 148 |
| real-ecad36a5 |  | — | 45 |
| real-fbe3c4c2 | sí | 227 | 320 |
