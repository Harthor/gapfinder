# Buen día — sesión nocturna (holdout temporal)

- **Qué corrió:** holdout temporal con T = 2024-01-01. 35 Show HN posteriores a T (≥20 pts, ≥400 caracteres, sin relanzamientos, solo software) contra el corpus anterior a T (528.865 items), con top-1000 MiniLM + llm5 y Jev vía OpenRouter: 35.000 pares, 0 errores.
- **Costo:** $1,90 de $2 (Claude $0,73 + Jev $1,17). Bajé de 50 a 35 ideas porque apliqué el tope a todo el gasto; las 15 restantes saldrían ~$0,80.
- **Resultado:** 8 ya construido (23%), 7 revisar (20%), 20 "no" (57%). En los known cases, que existen todos, daba "ya construido" en 42–58%: el sistema distingue algo. Ver `data/eval/holdout_temporal.md`.
- **Candidatas a hueco interesantes:** gestor de proyectos para Claude Code, constructor de SQL con t-strings de Python, tracer de corrutinas para wakeups perdidos (sus mejores candidatos son parecidos, no iguales).
- **Fugas:** 2 ideas con `leakage_flag` (`saas`, `mcp`): son términos de categoría que coinciden con el nombre.
- **Lado de demanda:** `data/ideas.json` nunca existió y Constellate también es oferta. Opciones en `data/eval/demand_side_notes.md` (recomiendo Ask HN).
- **Qué falló:** nada. Ajusté el control de fuga (marcaba palabras comunes como "workflows") antes de usarlo.

**Lo que tenés que hacer vos** (desde `~/dev/projects/gapfinder`):
1. Las 4 etiquetas: `uv run gapfinder phase3 review-labels` (k mantener · p parcial · d descartar · ? no sé)
2. El holdout, 75 pares, empezando por los "no": `uv run gapfinder holdout review` (s equivalente real anterior a T · p parcial · n no · ? no sé)
3. Leer `data/eval/holdout_temporal.md` y `data/eval/demand_side_notes.md`.
4. Rotar las claves de Anthropic y OpenRouter. Saldo de OpenRouter restante: ~$1.
