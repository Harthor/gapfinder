# Opción barata (gpt-oss + top-200) vs método completo (Opus 5 + top-1000), mismos 40 Asks

Misma idea (extracción v1) como query_core en ambos; cambia el modelo de las reformulaciones (gpt-oss-120b vs claude-opus-5, mismo prompt v2) y K (200 vs 1000). Comparados: 40.

- **Match >= 0.85 con el método completo que pasan a hueco con la opción barata: 2** (de 18 con match).
- Hueco con el método completo que pasan a match con la opción barata: 0.
- Mismo lado del umbral 0.85: 38/40.

| completo → barato | ideas |
|---|---|
| no → no | 22 |
| revisar → no | 1 |
| revisar → revisar | 6 |
| ya construido → no | 1 |
| ya construido → ya construido | 10 |

## Ideas que cambian de lado

| Ask | completo | barato | mejor (completo) | mejor (barato) |
|---|---|---|---|---|
| [Ask HN: Is there a descentralized DB with a simple social co](https://news.ycombinator.com/item?id=31414459) | 0.85 | 0.75 | scuttlebutt | Noms – A new decentralized database base |
| [Ask HN: How do you know if AI agents will choose your tool?](https://news.ycombinator.com/item?id=47127532) | 0.91 | 0.64 | AgentDX – Open-source linter and LLM ben | Axiomeer – An open marketplace for AI ag |
