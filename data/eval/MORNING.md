# Estado (oct-2026): Fase 4 y candidatos a hueco

**Qué corrió**: 397 Ask HN "¿hay una herramienta para…?" (de 8.568) → extracción automática (gpt-oss) → 242 pedidos reales →
retrieval contra el corpus anterior a cada Ask + Jev (top-200, y top-1000 para los huecos). Además, 40 Asks con el método completo (Opus 5).

**Costo por proveedor**: OpenRouter $7.02 (Jev $6.24, extracciones $0.20, consultas Opus 5 $0.55, reformulaciones gpt-oss $0.04);
Anthropic $0.016 (quedó sin crédito, se siguió con Opus vía OpenRouter). Saldo OpenRouter: $3.93.

**Resultados**
- `data/eval/gap_candidates.md`: **119 huecos** (de 242), cada uno con etiqueta e/p/n/?, pedido, link y top-5 matches con score.
- Hueco por etiqueta de los comentarios: no existe 20/23 (87%), parcial 30/60 (50%), **existe 69/159 (43%)**: los "e" suelen ser
  productos que no están en el corpus (Ubuntu Studio, GovTrack…), es decir, límite de cobertura.
- Opción barata vs método completo (40 Asks): 2 de 18 matches pasan a hueco (`gap_compare_k200.md`). Cobertura: la mitad de las
  herramientas sugeridas como equivalentes (con URL) no está en el corpus (`phase4_askhn.md`).

**Qué te queda por revisar**
1. Leer `data/eval/gap_candidates.md` (empieza por los de menor score).
2. `uv run gapfinder review` → d) Fase 4, 84 pares. (a y b terminadas; c está oculta: `--evaluar`.)
3. ~~Rotar las keys de Anthropic y OpenRouter.~~ Hecho (2026-10-21): las keys viejas están revocadas; nunca
   estuvieron en el repo.
