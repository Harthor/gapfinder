# Lado de demanda: de dónde salen las "ideas con demanda"

Investigación (oct-2026), sin construir nada.

## Qué existe

- **gapfinder**: la primera línea del README dice "ideas con demanda actual (`data/ideas.json`)", pero ese
  archivo **no existe** y ningún código lo genera ni lo lee. No hay ninguna fuente de demanda implementada.
- **Constellate** (`~/Documents/constellate-engine`, leído en modo solo lectura) es de donde salieron los
  casos reales/parciales. Sus "ideas" son **oferta**, no demanda: 5.314 items en `constellate.db`, todos
  del 16 al 31 de julio de 2026: arXiv 3.000, HN 868, Dev.to 569, GitHub 507, Hugging Face 222, Product
  Hunt 100, YC 48. El motor tiene scrapers para GitHub Trending, HN, arXiv, Product Hunt, YC, BetaList,
  Dev.to, Papers With Code y Hugging Face (todo cosas ya lanzadas). Las "absences" son huecos que Claude
  infiere entre ideas existentes de un mismo vecindario, no algo que alguien haya pedido.
- `docs/custom-sources.md` de Constellate describe cómo agregar Reddit (OAuth2 obligatorio desde 2023),
  pero no está implementado.
- Recursos tuyos que podrían servir: una key de twitterapi.io (en tu memoria, usada por el bot de crypto
  sentiment) y el pipeline de investigación en redes que tenés planeado (Twitter/YouTube).

## Qué falta

Una fuente donde personas **pidan** algo: "¿hay una herramienta para X?", "ojalá existiera…", "estoy
pagando por algo que hace mal Y". Sin eso, todo el set sigue siendo oferta y "hueco" solo se puede medir
contra el pasado (como en el holdout temporal).

## Opciones para un lote de 30–50 ideas reales con demanda

### 1. Ask HN "¿existe una herramienta para…?" (recomendada para empezar)
- **Cómo:** la API de Algolia HN que ya usa el ingest, con `tags=ask_hn` y consultas como "is there a tool",
  "looking for", "what do you use for", "I wish there was". Filtrar por puntos/comentarios (demanda =
  votos + respuestas), y que Claude convierta cada pedido en una necesidad (mismo método que query_core).
- **A favor:** sin keys nuevas ni costo de datos; mismo ecosistema que el corpus (vocabulario parecido);
  las respuestas del hilo traen las alternativas que la gente propuso, o sea, una adjudicación parcial gratis.
- **En contra:** sesgo dev/tech; muchas preguntas ya tienen respuesta en el hilo (no son huecos); hay que
  filtrar a mano las que son consejo o empleo y no herramienta.

### 2. Reddit: r/SomebodyMakeThis, r/AppIdeas, r/selfhosted ("is there a…"), r/SaaS
- **Cómo:** API oficial con OAuth2 (registrar una app), top posts del último año, filtrar por score.
- **A favor:** demanda explícita, de usuarios no necesariamente devs; subreddits pensados para pedir cosas.
- **En contra:** requiere OAuth y respetar los términos de la API; ruido y pedidos vagos; muchos son ideas
  de un usuario sin demanda real (votos bajos); vocabulario más lejano al corpus de Show HN/GitHub.

### 3. Twitter/X con twitterapi.io (ya tenés key)
- **Cómo:** búsquedas tipo "\"I wish there was an app\"", "\"someone should build\"", "\"is there a tool that\"",
  con un mínimo de likes/retweets.
- **A favor:** key existente; señal de demanda medible (engagement); volumen alto.
- **En contra:** mucho ruido y humor; pedidos cortos sin contexto; costo por request de twitterapi.io; los
  términos de uso de datos de X; peor reproducibilidad (los tweets se borran).

## Recomendación

Empezar con la opción 1 para 30–50 pedidos (rápido, gratis y reproducible) y usar las respuestas del hilo
como adjudicación parcial. Con ese lote, correr el mismo pipeline (query_core v2 → MiniLM + llm5 → Jev con
la regla 0.90/0.85) sobre el corpus completo. Los que den "no" serían candidatos a hueco con demanda.
