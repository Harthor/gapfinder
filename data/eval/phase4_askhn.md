# Fase 4: lado de demanda con Ask HN "¿hay una herramienta para…?"

Pedidos reales de Hacker News (Ask HN) convertidos en ideas, con los comentarios como etiqueta aproximada ("sí, existe X" / "busqué y no hay"). Cada idea se corre contra el corpus **anterior a la fecha del Ask** (mismo enmascarado que el holdout, embeddings MiniLM existentes, sin re-embeber), con llm5 (prompt v2), top-1000 y Jev vía OpenRouter. Regla de la Fase 3: P(núcleo) >= 0.9 ya construido, 0.85-0.9 revisar, < 0.85 no.

## Embudo

| paso | Asks |
|---|---|
| bajados (únicos, 16 consultas, >= 5 puntos y >= 3 comentarios en Algolia) | 8,568 |
| − antes de 2015-01-01 | 2,791 |
| − titulo no es pedido | 4,440 |
| − empleo o carrera | 77 |
| − no software | 475 |
| − how do you sin software en titulo | 388 |
| filtrados (sin LLM) | 397 |
| extraídos con LLM | 397 |
| pedidos reales de herramienta (según el LLM) | 235 |
| elegidos (hasta 40, balanceados por etiqueta) | 40 |
| procesados completos (top-1000 verificado) | 40 |

### Lo que aportó cada consulta

Algolia busca por palabras (no la frase exacta) y devuelve como mucho 1000 resultados por consulta. "nuevos" = Asks que ninguna consulta anterior había traído; "pasan" = de esos, los que pasaron los filtros.

| consulta | hits | nuevos | pasan |
|---|---|---|---|
| is there a tool | 1000 | 1000 | 63 |
| is there an app | 1000 | 914 | 43 |
| is there a library | 438 | 349 | 13 |
| is there a service | 1000 | 754 | 43 |
| is there software | 1000 | 700 | 50 |
| is there anything | 1000 | 668 | 13 |
| does anything exist | 88 | 59 | 1 |
| does something exist | 243 | 169 | 6 |
| looking for a tool | 628 | 462 | 12 |
| looking for an app | 1000 | 738 | 14 |
| looking for software | 1000 | 594 | 14 |
| what tool do you use | 954 | 629 | 49 |
| how do you | 1000 | 898 | 52 |
| I wish there was | 222 | 134 | 1 |
| recommend a tool | 186 | 93 | 8 |
| any tool for | 1000 | 407 | 15 |

Filtros sin LLM: título con forma de pedido ("is there a/an/any", "looking for a", "any tool", "what tool do you", "how do you", "I wish there was"…), sin empleo/carrera, con una palabra de software en título o texto, Asks desde 2015-01-01 (antes, el corpus anterior al Ask es chico); los "how do you…" además necesitan la palabra de software en el título.

## Cobertura: ¿están en el corpus las herramientas que sugieren los comentarios?

Sobre los 235 pedidos reales. Mapeo por URL (repo de GitHub, URL exacta, repo cuya homepage es el dominio o Show HN del dominio, validados por nombre); sin URL, por nombre exacto de un repo cuyo dueño es el proyecto (heurístico). Las URLs de tiendas de apps no se mapean por dominio.

| herramientas sugeridas | total | en el corpus | NO en el corpus | en el corpus y anteriores al Ask |
|---|---|---|---|---|
| todas | 1427 | 408 (29%) | 1019 (71%) | 365 (26%) |
| con URL en el comentario | 752 | 319 (42%) | 433 (58%) | 283 (38%) |
| presentadas como equivalentes | 500 | 173 (35%) | 327 (65%) | 154 (31%) |
| equivalentes con URL | 300 | 150 (50%) | 150 (50%) | 134 (45%) |

Cómo se mapearon las que están: heurístico, revisar 133, nombre de repo (heurístico) 115, url exacta 80, repo 80.

La medida más limpia es "con URL": sin URL, el mapeo por nombre solo encuentra repos con nombre único, así que "todas" subestima la cobertura. Lo que no está suele ser producto comercial o app sin repo ni Show HN.

## Etiqueta de los comentarios × decisión del sistema

40 ideas procesadas. "existe con item en corpus" = algún comentario sugiere un equivalente que está en el corpus con fecha anterior al Ask (el sistema podía encontrarlo).

| etiqueta de los comentarios | ya construido | revisar | no | total |
|---|---|---|---|---|
| existe con item en corpus | 8 | 1 | 6 | 15 |
| existe sin item en corpus | 1 | 2 | 6 | 9 |
| parcial | 0 | 2 | 6 | 8 |
| no existe | 0 | 2 | 2 | 4 |
| incierto | 2 | 0 | 2 | 4 |
| **total** | 11 | 7 | 22 | 40 |

## Recall del item sugerido (cuando está en el corpus antes del Ask)

Para cada idea procesada con alguna herramienta sugerida en el corpus anterior al Ask: el mejor rank de sus items (repo y Show HN gemelos) en el top-1000 y su P(núcleo) de Jev.

| Ask | etiqueta | herramienta sugerida (relación) | rank | P(núcleo) | decisión del sistema |
|---|---|---|---|---|---|
| [18508284](https://news.ycombinator.com/item?id=18508284) | existe con item en corpus | PlantUML (equivalente) | 95 | 0.45 | no |
| [18508284](https://news.ycombinator.com/item?id=18508284) | existe con item en corpus | Mermaid (equivalente) | 64 | 0.35 | no |
| [18508284](https://news.ycombinator.com/item?id=18508284) | existe con item en corpus | Gaphor (equivalente) | 268 | 0.27 | no |
| [18508284](https://news.ycombinator.com/item?id=18508284) | existe con item en corpus | Nomnoml (equivalente) | > 1000 | – | no |
| [18508284](https://news.ycombinator.com/item?id=18508284) | existe con item en corpus | Monodraw (equivalente) | > 1000 | – | no |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Raindrop (equivalente) | > 1000 | – | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Zotero (parcial) | > 1000 | – | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | LinkAce (equivalente) | 18 | 0.61 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Linkding (equivalente) | 11 | 0.82 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Wallabag (equivalente) | 917 | 0.61 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Buku (equivalente) | 118 | 0.38 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Shiori (equivalente) | 105 | 0.61 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | ArchiveBox (equivalente) | 202 | 0.22 | ya construido |
| [32506168](https://news.ycombinator.com/item?id=32506168) | existe con item en corpus | Shaarli (equivalente) | 168 | 0.47 | ya construido |
| [9444470](https://news.ycombinator.com/item?id=9444470) | existe con item en corpus | Graylog (equivalente) | > 1000 | – | ya construido |
| [9444470](https://news.ycombinator.com/item?id=9444470) | existe con item en corpus | Sentry (equivalente) | > 1000 | – | ya construido |
| [9444470](https://news.ycombinator.com/item?id=9444470) | existe con item en corpus | Papertrail (equivalente) | 358 | 0.14 | ya construido |
| [9444470](https://news.ycombinator.com/item?id=9444470) | existe con item en corpus | Logrotate (parcial) | 340 | 0.16 | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | Hasura (parcial) | > 1000 | – | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | Noria (equivalente) | 66 | 0.83 | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | Materialize (equivalente) | 7 | 0.91 | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | PipelineDB (parcial) | 17 | 0.30 | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | GraphJin (parcial) | > 1000 | – | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | Supabase (parcial) | > 1000 | – | ya construido |
| [26901352](https://news.ycombinator.com/item?id=26901352) | existe con item en corpus | Debezium (parcial) | 39 | 0.15 | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | Jitsi Meet (equivalente) | 2 | 0.95 | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | OpenVidu (parcial) | 12 | 0.86 | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | Janus (equivalente) | > 1000 | – | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | BigBlueButton (equivalente) | 89 | 0.92 | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | Matrix (Synapse) + Riot.im (parcial) | > 1000 | – | ya construido |
| [22591543](https://news.ycombinator.com/item?id=22591543) | existe con item en corpus | DuoBango (parcial) | > 1000 | – | ya construido |
| [15823597](https://news.ycombinator.com/item?id=15823597) | existe con item en corpus | OpenAmbit project (Suunto Ambit data ext (equivalente) | 171 | 0.55 | no |
| [31083131](https://news.ycombinator.com/item?id=31083131) | existe con item en corpus | Jira (parcial) | > 1000 | – | ya construido |
| [31083131](https://news.ycombinator.com/item?id=31083131) | existe con item en corpus | Zephyr (parcial) | > 1000 | – | ya construido |
| [31083131](https://news.ycombinator.com/item?id=31083131) | existe con item en corpus | Doorstop (equivalente) | 131 | 0.90 | ya construido |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Kibi (parcial) | > 1000 | – | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Lumify (equivalente) | > 1000 | – | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Aleph (equivalente) | 192 | 0.76 | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Neo4j (parcial) | 316 | 0.44 | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Linkurious (parcial) | 212 | 0.31 | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Gransk (equivalente) | 248 | 0.28 | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Gephi (parcial) | > 1000 | – | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | igraph (R) (parcial) | 793 | 0.19 | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Elasticsearch (parcial) | > 1000 | – | no |
| [13488795](https://news.ycombinator.com/item?id=13488795) | existe con item en corpus | Gaffer (parcial) | 166 | 0.36 | no |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | Visidata (equivalente) | 677 | 0.57 | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | OctoSQL (equivalente) | 10 | 0.62 | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | dbt (parcial) | > 1000 | – | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | Airflow (parcial) | > 1000 | – | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | Prefect (parcial) | > 1000 | – | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | pandas (Python) (parcial) | > 1000 | – | revisar |
| [22034101](https://news.ycombinator.com/item?id=22034101) | existe con item en corpus | EasyDataTransform (equivalente) | 4 | 0.88 | revisar |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | active_scaffold (equivalente) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | JHipster (equivalente) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | React Admin (equivalente) | 444 | 0.81 | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Hasura (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Prisma (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | UserFrosting (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Strapi (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Directus (parcial) | 9 | 0.83 | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Cockpit (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Hyperfiddle (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Hof (parcial) | 427 | 0.24 | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Anvil Runtime (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Warthog (parcial) | > 1000 | – | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | Daptin (parcial) | 353 | 0.40 | ya construido |
| [23264850](https://news.ycombinator.com/item?id=23264850) | existe con item en corpus | OpenXava (parcial) | > 1000 | – | ya construido |
| [31549303](https://news.ycombinator.com/item?id=31549303) | existe con item en corpus | Monome NORNS (equivalente) | > 1000 | – | no |
| [31549303](https://news.ycombinator.com/item?id=31549303) | existe con item en corpus | Pisound / Patchbox OS (parcial) | > 1000 | – | no |
| [31549303](https://news.ycombinator.com/item?id=31549303) | existe con item en corpus | musnix (equivalente) | > 1000 | – | no |
| [15497837](https://news.ycombinator.com/item?id=15497837) | existe con item en corpus | Puppeteer (equivalente) | > 1000 | – | no |
| [15497837](https://news.ycombinator.com/item?id=15497837) | existe con item en corpus | Typometer (equivalente) | 869 | 0.09 | no |
| [15497837](https://news.ycombinator.com/item?id=15497837) | existe con item en corpus | browser-perf (equivalente) | 3 | 0.80 | no |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | JUCE (equivalente) | > 1000 | – | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | Fyne (equivalente) | > 1000 | – | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | wxWidgets (equivalente) | 100 | 0.43 | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | FLTK (parcial) | > 1000 | – | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | Tauri (equivalente) | > 1000 | – | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | NodeGui (equivalente) | 88 | 0.80 | ya construido |
| [28484658](https://news.ycombinator.com/item?id=28484658) | existe con item en corpus | Godot (parcial) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | Pastel (equivalente) | 67 | 0.68 | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | BugHerd (equivalente) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | Smort.io (equivalente) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | PixelSnap (parcial) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | ZipBoard (equivalente) | 676 | 0.38 | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | Kontxt (equivalente) | 28 | 0.37 | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | SingleFile (parcial) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | Hypothesis (open source widget) (equivalente) | > 1000 | – | ya construido |
| [32315035](https://news.ycombinator.com/item?id=32315035) | existe con item en corpus | Usersnap (parcial) | > 1000 | – | ya construido |
| [27615562](https://news.ycombinator.com/item?id=27615562) | existe con item en corpus | GitBook (equivalente) | > 1000 | – | no |
| [27615562](https://news.ycombinator.com/item?id=27615562) | existe con item en corpus | Aha! (equivalente) | > 1000 | – | no |
| [27615562](https://news.ycombinator.com/item?id=27615562) | existe con item en corpus | Redmine (parcial) | > 1000 | – | no |
| [21991260](https://news.ycombinator.com/item?id=21991260) | parcial | OppsDaily (parcial) | > 1000 | – | revisar |
| [14008085](https://news.ycombinator.com/item?id=14008085) | parcial | Horde (parcial) | > 1000 | – | no |
| [14008085](https://news.ycombinator.com/item?id=14008085) | parcial | Teamup (parcial) | 111 | 0.28 | no |
| [14008085](https://news.ycombinator.com/item?id=14008085) | parcial | FullCalendar (parcial) | 262 | 0.17 | no |
| [14008085](https://news.ycombinator.com/item?id=14008085) | parcial | SOGo (parcial) | > 1000 | – | no |
| [14008085](https://news.ycombinator.com/item?id=14008085) | parcial | Moo.do (parcial) | > 1000 | – | no |
| [29078836](https://news.ycombinator.com/item?id=29078836) | existe sin item en corpus | bundlescanner.com (parcial) | 2 | 0.65 | no |
| [33595879](https://news.ycombinator.com/item?id=33595879) | parcial | Jellyfin (parcial) | > 1000 | – | no |
| [33595879](https://news.ycombinator.com/item?id=33595879) | parcial | Navidrome (parcial) | 256 | 0.31 | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | libtorrent (parcial) | > 1000 | – | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | libp2p (rust) (parcial) | 29 | 0.22 | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | Tribler / IPv8 (parcial) | > 1000 | – | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | Dat (Rust implementation) (parcial) | > 1000 | – | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | Firestr (parcial) | 88 | 0.38 | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | Orbit‑Db (parcial) | > 1000 | – | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | rust-web3 (parcial) | > 1000 | – | no |
| [18511911](https://news.ycombinator.com/item?id=18511911) | parcial | Zerotier SDK (parcial) | 204 | 0.08 | no |
| [21920142](https://news.ycombinator.com/item?id=21920142) | existe sin item en corpus | security.txt (parcial) | 302 | 0.09 | no |
| [13963698](https://news.ycombinator.com/item?id=13963698) | existe sin item en corpus | Product Hunt (parcial) | > 1000 | – | no |
| [13963698](https://news.ycombinator.com/item?id=13963698) | existe sin item en corpus | StartupLister (parcial) | 855 | 0.07 | no |
| [14733562](https://news.ycombinator.com/item?id=14733562) | parcial | PiggyDB (parcial) | > 1000 | – | no |
| [14733562](https://news.ycombinator.com/item?id=14733562) | parcial | scikit-learn (parcial) | > 1000 | – | no |
| [14733562](https://news.ycombinator.com/item?id=14733562) | parcial | Gensim (parcial) | 162 | 0.30 | no |
| [11595129](https://news.ycombinator.com/item?id=11595129) | existe sin item en corpus | Bootstrap (parcial) | > 1000 | – | revisar |

Dentro del top-1000: 51/116.

## Ideas procesadas

- **ya construido** (0.96) · [Ask HN: How do you find developers for open source bug bounties?](https://news.ycombinator.com/item?id=40682632) · 2024-06-14 · 64 pts · comentarios: existe sin item en corpus · corpus anterior: 549,472 items  
  Idea: A service or platform where I can post a paid bounty or contract to locate qualified open‑source developers who can fix specific bugs or implement features in existing projects.  
  Sugeridas en el hilo: algora.io (equivalente); openbugbounty.org (equivalente); polar.sh (equivalente); bountycaster.xyz (equivalente); Hydra (hydraoss.io) (equivalente); Igalia (parcial)
  - 0.96 · Algora – Open source coding bounties · creado 2023-10-04 · https://console.algora.io/hacktoberfest
- **ya construido** (0.95) · [Ask HN: Are there good self-hosted video conference tools?](https://news.ycombinator.com/item?id=22591543) · 2020-03-16 · 198 pts · comentarios: existe con item en corpus · corpus anterior: 353,008 items  
  Idea: Looking for a self‑hosted video‑conferencing solution that can run on our own servers for small to medium sized meetings, ideally with browser‑based clients, screen sharing and low CPU usage.  
  Sugeridas en el hilo: Jitsi Meet (equivalente, en corpus); Nextcloud Talk (equivalente, en corpus); Kurento (parcial, en corpus); OpenVidu (parcial, en corpus); Janus (equivalente, en corpus); BigBlueButton (equivalente, en corpus)
  - 0.95 · jitsi-meet · creado 2013-12-16 · https://github.com/jitsi/jitsi-meet
- **ya construido** (0.93) · [Ask HN: Is there any open source tool for creating simple CRUD Apps?](https://news.ycombinator.com/item?id=23264850) · 2020-05-21 · 114 pts · comentarios: existe con item en corpus · corpus anterior: 365,746 items  
  Idea: A tool that lets you quickly generate CRUD applications with forms for data entry and updates, preferably open‑source and easy to integrate with existing back‑ends.  
  Sugeridas en el hilo: Retool (equivalente, en corpus); Active Admin (equivalente); active_scaffold (equivalente, en corpus); JHipster (equivalente, en corpus); React Admin (equivalente, en corpus); Hasura (parcial, en corpus)
  - 0.93 · Flask-AppBuilder · creado 2013-11-09 · https://github.com/dpgaspar/Flask-AppBuilder
- **ya construido** (0.92) · [Ask HN: How do you create a cross-platform GUI without using Electron?](https://news.ycombinator.com/item?id=28484658) · 2021-09-10 · 92 pts · comentarios: existe con item en corpus · corpus anterior: 429,916 items  
  Idea: Find a cross‑platform GUI framework or stack that lets me build a desktop app (Windows, Linux/GTK, macOS) that talks to a web API, with a small binary size and native OS integration, as an alternative to Electron.  
  Sugeridas en el hilo: Qt (equivalente); imgui (parcial); JUCE (equivalente, en corpus); Blazor Desktop (parcial); Fyne (equivalente, en corpus); GTK (parcial)
  - 0.92 · tauri · creado 2019-07-13 · https://github.com/tauri-apps/tauri
- **ya construido** (0.92) · [Ask HN: Is there a tool / product that enables commenting on HTML elements?](https://news.ycombinator.com/item?id=32315035) · 2022-08-02 · 91 pts · comentarios: existe con item en corpus · corpus anterior: 466,476 items  
  Idea: A commercial product that lets users add comments/annotations directly on specific HTML elements in a web page and share those comments with an organization, similar to Google Docs comments but for the DOM.  
  Sugeridas en el hilo: Ybug.io (equivalente); Userback (equivalente); Jam.dev (equivalente, en corpus); Snippyly (equivalente); Cactus Comments (equivalente); Hypothes.is (equivalente)
  - 0.92 · Juntoo – A tool for front-end devs and PMs to annotate web projects · creado 2015-11-10 · https://juntoo.co/fd.html
- **ya construido** (0.92) · [Ask HN: Is there an instant messaging app which has a tree like view?](https://news.ycombinator.com/item?id=23859456) · 2020-07-16 · 23 pts · comentarios: incierto · corpus anterior: 375,148 items  
  Idea: A messaging application that can display conversation threads in a hierarchical, tree‑like visual interface.  
  Sugeridas en el hilo: ninguna
  - 0.92 · treeverse · creado 2016-10-28 · https://github.com/paulgb/treeverse
- **ya construido** (0.91) · [Ask HN: Is there a spiritual successor to del.icio.us?](https://news.ycombinator.com/item?id=32506168) · 2022-08-18 · 223 pts · comentarios: existe con item en corpus · corpus anterior: 468,170 items  
  Idea: Looking for a modern bookmarking service that lets me save, tag, and sync URLs across browsers, with dedicated mobile/desktop apps and optional social sharing, as a spiritual successor to del.icio.us.  
  Sugeridas en el hilo: Pinboard (equivalente); Raindrop (equivalente, en corpus); Nextcloud Bookmarks (parcial); Evernote (parcial); Notion (parcial); Zotero (parcial, en corpus)
  - 0.91 · brace-client · creado 2020-02-26 · https://github.com/stxapps/brace-client
- **ya construido** (0.91) · [Ask HN: How do you log application events?](https://news.ycombinator.com/item?id=9444470) · 2015-04-27 · 221 pts · comentarios: existe con item en corpus · corpus anterior: 115,103 items  
  Idea: Looking for a logging system that stores application events in a way that they can be queried and debugged easily, while keeping the overall size of the logs manageable through retention, compression, or archiving.  
  Sugeridas en el hilo: segment.io (equivalente); Elasticsearch + Logstash + Kib (equivalente); Graylog (equivalente, en corpus); Sentry (equivalente, en corpus); Splunk (equivalente); Papertrail (equivalente, en corpus)
  - 0.91 · elsa · creado 2014-09-09 · https://github.com/mcholste/elsa
- **ya construido** (0.91) · [Ask HN: Is there a way to efficiently subscribe to an SQL query for changes?](https://news.ycombinator.com/item?id=26901352) · 2021-04-22 · 200 pts · comentarios: existe con item en corpus · corpus anterior: 413,514 items  
  Idea: A system that can deliver real‑time incremental updates for the result of an arbitrary SQL query (including joins and hierarchical queries) without re‑executing the whole query each time the underlying tables change.  
  Sugeridas en el hilo: Hasura (parcial, en corpus); Noria (equivalente, en corpus); Materialize (equivalente, en corpus); PipelineDB (parcial, en corpus); ClickHouse (experimental featu (parcial); GraphJin (parcial, en corpus)
  - 0.91 · materialize · creado 2019-02-22 · https://github.com/MaterializeInc/materialize
- **ya construido** (0.91) · [Ask HN: How do you know if AI agents will choose your tool?](https://news.ycombinator.com/item?id=47127532) · 2026-02-23 · 38 pts · comentarios: incierto · corpus anterior: 642,840 items  
  Idea: The OP wants a way to evaluate or simulate how autonomous AI agents discover and choose a given API or service among many similar options, to optimize documentation, schema, and description for better agent selection.  
  Sugeridas en el hilo: ninguna
  - 0.91 · AgentDX – Open-source linter and LLM benchmark for MCP servers · creado 2026-02-18 · https://github.com/agentdx/agentdx
- **ya construido** (0.90) · [Ask HN: How do you keep track of software requirements and test them?](https://news.ycombinator.com/item?id=31083131) · 2022-04-19 · 195 pts · comentarios: existe con item en corpus · corpus anterior: 454,959 items  
  Idea: A lightweight way to capture and trace software requirements to tests for a small team, preferably using an open‑source or low‑cost tool.  
  Sugeridas en el hilo: Jira (parcial, en corpus); Zephyr (parcial, en corpus); Enzyme (parcial); CucumberJS (parcial); Gitlab (requirements feature) (parcial); Asana (parcial)
  - 0.90 · openfasttrace · creado 2015-12-27 · https://github.com/itsallcode/openfasttrace
- **revisar** (0.88) · [Ask HN: What tools do you use for data munging and merging?](https://news.ycombinator.com/item?id=22034101) · 2020-01-13 · 114 pts · comentarios: existe con item en corpus · corpus anterior: 343,647 items  
  Idea: Looking for a desktop application that can clean, merge, and transform various data sources (CSV, JSON, databases, etc.) without relying on a web interface.  
  Sugeridas en el hilo: Talend (equivalente); Alteryx (equivalente); KNIME (equivalente); Altova MapForce (equivalente); Visidata (equivalente, en corpus); OctoSQL (equivalente, en corpus)
  - 0.88 · Transform Data Without Programming · creado 2019-10-05 · https://www.easydatatransform.com
- **revisar** (0.87) · [Ask HN: Is domain squatting still profitable? Is there a solution?](https://news.ycombinator.com/item?id=28106113) · 2021-08-08 · 98 pts · comentarios: parcial · corpus anterior: 425,958 items  
  Idea: A service or tool that monitors expiring domains and automatically registers or renews them (or otherwise prevents domain squatting) so that owners don’t lose their domains to squatters.  
  Sugeridas en el hilo: HugeDomains (parcial)
  - 0.87 · Backordr – An honest ccTLD drop catching service · creado 2019-05-28 · https://backordr.com/
- **revisar** (0.86) · [Ask HN: Is there a platform for sharing ideas that people want to “give away”?](https://news.ycombinator.com/item?id=21991260) · 2020-01-08 · 287 pts · comentarios: parcial · corpus anterior: 342,953 items  
  Idea: A platform where people can post small side‑project ideas, receive feedback, and find collaborators without focusing on business‑oriented pitches.  
  Sugeridas en el hilo: /r/AppIdeas (parcial); IdeasDrop (Product Hunt) (parcial); Halfbakery (parcial); makeithappen.dev (parcial); Brief Ideas (parcial); r/SomebodyMakeThis (parcial)
  - 0.86 · Side Racket - create, discover & join amazing projects · creado 2013-10-29 · https://sideracket.com
- **revisar** (0.86) · [Ask HN: Is there any work being done in speech-to-code with deep learning?](https://news.ycombinator.com/item?id=23497756) · 2020-06-12 · 172 pts · comentarios: existe sin item en corpus · corpus anterior: 369,522 items  
  Idea: A conversational speech‑to‑code system that lets a programmer dictate code naturally without the abrupt, command‑driven style that strains the throat.  
  Sugeridas en el hilo: Serenade (equivalente, en corpus); Talon Voice (equivalente); Caster (with Dragonfly) (equivalente); VoiceCode (parcial); Kaldi‑active‑grammar (by daanz (parcial); Vosk (parcial)
  - 0.86 · CodeSpeak, the beginnings of a web-based speech-to-code tool · creado 2019-05-27 · https://github.com/sethwilsonUS/codespeak
- **revisar** (0.85) · [Ask HN: Is there a descentralized DB with a simple social conflict resolution?](https://news.ycombinator.com/item?id=31414459) · 2022-05-17 · 8 pts · comentarios: no existe · corpus anterior: 458,084 items  
  Idea: A decentralized, append‑only database where operations are signed by public‑key agents, form a Merkle‑DAG, and conflict resolution is handled socially rather than by complex consensus algorithms.  
  Sugeridas en el hilo: ninguna
  - 0.85 · scuttlebutt · creado 2012-07-25 · https://github.com/dominictarr/scuttlebutt
- **revisar** (0.85) · [Ask HN: Is there a service that escalates emails to SMS or Phone call reminders?](https://news.ycombinator.com/item?id=18432459) · 2018-11-12 · 5 pts · comentarios: no existe · corpus anterior: 284,905 items  
  Idea: A service that automatically sends a reminder via SMS, email, or phone call to the original email recipient if they have not replied within a specified time window.  
  Sugeridas en el hilo: ninguna
  - 0.85 · Simple Email Reminders · creado 2017-04-07 · http://remindmebro.com/
- **revisar** (0.85) · [Ask HN: How do you write concepts? (Structure / Tools / Howto)](https://news.ycombinator.com/item?id=11595129) · 2016-04-29 · 63 pts · comentarios: existe sin item en corpus · corpus anterior: 159,351 items  
  Idea: The OP wants a way to create, organize and sketch mockups, diagrams and structured concepts for a web project, including UI wireframes, data models and feature lists.  
  Sugeridas en el hilo: Balsamiq (equivalente); draw.io (equivalente); Sketch (equivalente); Keynote (equivalente); Creately (equivalente); webpagestickynotes.com (parcial)
  - 0.85 · pencil · creado 2014-06-19 · https://github.com/evolus/pencil
- **no** (0.83) · [Ask HN: How do you security-audit external software using NPM packages?](https://news.ycombinator.com/item?id=29078836) · 2021-11-02 · 106 pts · comentarios: existe sin item en corpus · corpus anterior: 435,618 items  
  Idea: The OP needs a way to perform security audits of WordPress plugins that include bundled and minified JavaScript built from npm packages, even when no package.json or source repository is available.  
  Sugeridas en el hilo: WhiteSource (parcial); trivy (equivalente); Snyk (equivalente); Dependency‑Check (maven‑depend (parcial); Nexus Lifecycle / Nexus Audito (parcial); requiresecurity.com (parcial)
  - 0.83 · retire.js · creado 2013-08-30 · https://github.com/RetireJS/retire.js
  - 0.80 · js-x-ray · creado 2020-03-26 · https://github.com/NodeSecure/js-x-ray
  - 0.73 · burp-retire-js · creado 2014-11-26 · https://github.com/h3xstream/burp-retire-js
- **no** (0.80) · [Ask HN: How do you measure performance of your client-side application?](https://news.ycombinator.com/item?id=15497837) · 2017-10-18 · 94 pts · comentarios: existe con item en corpus · corpus anterior: 230,933 items  
  Idea: Collect detailed client‑side performance data such as reflows, repaints, layout thrashing, paint timings, and other runtime metrics for web applications.  
  Sugeridas en el hilo: Lighthouse (equivalente); Puppeteer (equivalente, en corpus); Typometer (equivalente, en corpus); browser-perf (equivalente, en corpus); MachMetrics (equivalente, en corpus)
  - 0.80 · browser-perf · creado 2013-12-09 · https://github.com/axemclion/browser-perf
  - 0.79 · boomerang · creado 2010-05-20 · https://github.com/YahooArchive/boomerang
  - 0.79 · speedracer · creado 2017-05-01 · https://github.com/speedracer/speedracer
- **no** (0.79) · [Ask HN: Is there a better way to document complex software architectures?](https://news.ycombinator.com/item?id=18508284) · 2018-11-22 · 406 pts · comentarios: existe con item en corpus · corpus anterior: 286,198 items  
  Idea: A tool or platform that lets software architects model, document, and keep architecture diagrams in sync with code, rather than manually drawing static Visio/PowerPoint artifacts.  
  Sugeridas en el hilo: Sparx Enterprise Architect (equivalente); MagicDraw (equivalente); Qualiware (equivalente); PlantUML (equivalente, en corpus); Mermaid (equivalente, en corpus); Structurizr (equivalente, en corpus)
  - 0.79 · java · creado 2014-06-09 · https://github.com/structurizr/java
  - 0.76 · oovaide · creado 2014-02-08 · https://github.com/animatedb/oovaide
  - 0.76 · Ardoq.com – developer friendly documentation tool [video] · creado 2014-05-02 · https://vimeo.com/93350435
- **no** (0.76) · [Ask HN: Is there an open source equivalent to Palantir?](https://news.ycombinator.com/item?id=13488795) · 2017-01-26 · 159 pts · comentarios: existe con item en corpus · corpus anterior: 193,754 items  
  Idea: A platform that lets journalists or activists ingest unstructured data, link entities, visualise networks and timelines, and perform the kind of link‑analysis and intelligence‑analyst style investigations that Palantir provides.  
  Sugeridas en el hilo: J++ (JPlusPlus) (parcial); Kibi (parcial, en corpus); Lumify (equivalente, en corpus); TimeFlow (parcial); Aleph (equivalente, en corpus); Neo4j (parcial, en corpus)
  - 0.76 · aleph · creado 2014-08-27 · https://github.com/alephdata/aleph
  - 0.66 · marija · creado 2016-10-13 · https://github.com/dutchcoders/marija
  - 0.60 · The Codex – a graph database project for the digital humanities · creado 2016-01-24 · http://the-codex.net
- **no** (0.76) · [Ask HN: Is there a powerful open-source Google Calendar replacement?](https://news.ycombinator.com/item?id=14008085) · 2017-03-31 · 219 pts · comentarios: parcial · corpus anterior: 203,143 items  
  Idea: A powerful, developer‑friendly, open‑source calendar system that is modular, extensible and can be self‑hosted, providing the full feature set and usability of Google Calendar.  
  Sugeridas en el hilo: Horde (parcial, en corpus); Nextcloud Calendar (parcial); Citadel (parcial, en corpus); OpenXchange (parcial); Teamup (parcial, en corpus); FullCalendar (parcial, en corpus)
  - 0.76 · katana · creado 2015-02-17 · https://github.com/sabre-io/katana
  - 0.63 · calagator · creado 2009-01-11 · https://github.com/calagator/calagator
  - 0.62 · Busybook – Open-Source Calendar/Reminder (CalDAV) Server Built on Rails · creado 2016-08-24 · https://github.com/seiyanuta/busybook
- **no** (0.70) · [Ask HN: Is there any Linux distro dedicated to music performance?](https://news.ycombinator.com/item?id=31549303) · 2022-05-29 · 107 pts · comentarios: existe con item en corpus · corpus anterior: 459,463 items  
  Idea: A minimal, boot‑fast Linux distribution that boots directly into a DAW or plugin host for live music performance, with only the necessary audio stack (ALSA/Jack/PipeWire) and no desktop or extra applications.  
  Sugeridas en el hilo: Ubuntu Studio (equivalente); ZynthianOS (equivalente); Monome NORNS (equivalente, en corpus); AV Linux (equivalente); Pisound / Patchbox OS (parcial, en corpus); Audiophile Linux (equivalente)
  - 0.70 · elk-pi · creado 2019-12-13 · https://github.com/elk-audio/elk-pi
  - 0.42 · pi-stomp · creado 2020-02-15 · https://github.com/TreeFallSound/pi-stomp
  - 0.29 · essence · creado 2017-07-13 · https://github.com/nakst/essence
- **no** (0.67) · [Ask HN: Any tools to easily cluster ideas/notes by similarity?](https://news.ycombinator.com/item?id=14733562) · 2017-07-10 · 70 pts · comentarios: parcial · corpus anterior: 217,010 items  
  Idea: A tool that can ingest Evernote notes and automatically group them into clusters of similar ideas or topics.  
  Sugeridas en el hilo: DevonThink (parcial); PiggyDB (parcial, en corpus); Docear (parcial); scikit-learn (parcial, en corpus); Gensim (parcial, en corpus); Jekyll similar‑post plugin (parcial)
  - 0.67 · keeeb - social bookmarking reinvented · creado 2012-11-23 · http://www.keeeb.com
  - 0.57 · gensim-simserver · creado 2011-12-02 · https://github.com/piskvorky/gensim-simserver
  - 0.55 · Lexos · creado 2013-05-13 · https://github.com/WheatonCS/Lexos
- **no** (0.66) · [Ask HN: Is there a GDPR compliance privacy statement template for small blogs?](https://news.ycombinator.com/item?id=33113283) · 2022-10-06 · 6 pts · comentarios: no existe · corpus anterior: 473,374 items  
  Idea: A concise GDPR privacy statement template that small self‑hosted blog owners can use to disclose how they handle personal data such as comment names and IP addresses.  
  Sugeridas en el hilo: ninguna
  - 0.66 · gdpr · creado 2018-10-17 · https://github.com/aeris/gdpr
  - 0.54 · oprvc.github.io · creado 2021-01-03 · https://github.com/oprvc/oprvc.github.io
  - 0.52 · PrivacyPage – Create your own branded privacy page for GDPR and CCPA · creado 2021-06-25 · https://privacypage.com
- **no** (0.64) · [Ask HN: Is there a tool to extract ALL emails, learn "me", draft responses](https://news.ycombinator.com/item?id=40096424) · 2024-04-20 · 5 pts · comentarios: no existe · corpus anterior: 542,391 items  
  Idea: A tool that can ingest all of a user's emails and other communication channels, build a personal model with GPT‑4, and automatically draft replies and perform actions across integrations like Slack, Messenger, Twilio, Todoist, etc., continuously updating the knowledge base with new messages.  
  Sugeridas en el hilo: ninguna
  - 0.64 · I’m an introvert, made an app to maintain relationships, added more AI · creado 2023-06-24 · https://play.google.com/store/apps/details?id=dev.mtc.ga&hl=en_US
  - 0.64 · CowAgent · creado 2022-08-07 · https://github.com/zhayujie/CowAgent
  - 0.60 · A ChatGPT-like assistant that builds itself from your own data · creado 2023-03-02 · https://moveo.ai/
- **no** (0.64) · [Ask HN: Any good tools for viewing congressional bills?](https://news.ycombinator.com/item?id=44202110) · 2025-06-06 · 114 pts · comentarios: existe sin item en corpus · corpus anterior: 595,013 items  
  Idea: A readable viewer or renderer for congressional bill documents (XML or plain text) that formats the content nicely, supports navigation, and optionally provides diff/comparison features.  
  Sugeridas en el hilo: GovTrack (equivalente); congress.dev (equivalente); govinfo XSLT stylesheets (bill (parcial); Congressional Rag (parcial); Easy Congress (iOS app) (parcial); dogeAI chat (parcial)
  - 0.64 · Archeo-Lex · creado 2014-08-04 · https://github.com/Legilibre/Archeo-Lex
  - 0.50 · Voyant · creado 2011-09-27 · https://github.com/sgsinclair/Voyant
  - 0.46 · Voyant · creado 2021-03-24 · https://github.com/voyanttools/Voyant
- **no** (0.64) · [Ask HN: Is there a “product launch as a service” company?](https://news.ycombinator.com/item?id=13963698) · 2017-03-26 · 82 pts · comentarios: existe sin item en corpus · corpus anterior: 202,356 items  
  Idea: Looking for a service/company that can handle the end‑to‑end launch of a startup product, including marketing, PR, social media, and early customer acquisition.  
  Sugeridas en el hilo: GrowthGeeks (equivalente); LaunchRock (parcial); Product Hunt (parcial, en corpus); StartupLister (parcial, en corpus); BlueChilli (parcial); Smart Foundations (parcial)
  - 0.64 · Growthdock-Sameday actionable growth, marketing and startup traction help · creado 2016-01-30 · http://www.growthdock.com
  - 0.49 · Co+create makes becoming an entrepreneur more attainable to anyone · creado 2015-08-07 · http://www.cocreatellc.com
  - 0.47 · Momentum – Automated marketing for solo founders · creado 2014-04-14 · https://news.ycombinator.com/item?id=7586868
- **no** (0.62) · [Ask HN: Any tools to do generic WiFi imaging?](https://news.ycombinator.com/item?id=40946613) · 2024-07-12 · 97 pts · comentarios: existe sin item en corpus · corpus anterior: 552,745 items  
  Idea: A tool that can generate a 3‑D density map of the interior of walls using Wi‑Fi (or similar radio) signals, without having to make holes.  
  Sugeridas en el hilo: Walabot (equivalente); endoscope (borescope) (parcial); ExpEYES (parcial); SEELab 3.0 (parcial); FarField inductive listening d (parcial); Thought Emporium Wi‑Fi camera  (parcial)
  - 0.62 · WiFi-Vision · creado 2017-09-16 · https://github.com/AideTechBot/WiFi-Vision
  - 0.41 · MIMO-SAR-mmWave-Imaging-Toolbox · creado 2020-04-19 · https://github.com/meminyanik/MIMO-SAR-mmWave-Imaging-Toolbox
  - 0.27 · RadioDiff · creado 2024-06-20 · https://github.com/UNIC-Lab/RadioDiff
- **no** (0.61) · [Ask HN: Is there any tool for benchmarking responsiveness for Linux?](https://news.ycombinator.com/item?id=30209366) · 2022-02-04 · 100 pts · comentarios: existe sin item en corpus · corpus anterior: 446,159 items  
  Idea: A tool that can measure and report numeric metrics of Linux scheduling latency and overall desktop responsiveness (e.g., time from a process being marked runnable to actual execution, input‑to‑display latency, etc.).  
  Sugeridas en el hilo: SchedLat (equivalente); interbench (equivalente); sysprof (parcial); cyclictest (parcial); linux‑rt test programs (parcial); eBPF script (runqlat) (parcial)
  - 0.61 · perfetto · creado 2019-12-10 · https://github.com/google/perfetto
  - 0.58 · KUtrace · creado 2019-07-08 · https://github.com/dicksites/KUtrace
  - 0.58 · lmbench · creado 2018-07-31 · https://github.com/intel/lmbench
- **no** (0.60) · [Ask HN: Is there a cloud music library that doesn't keep deleting my music?](https://news.ycombinator.com/item?id=33595879) · 2022-11-14 · 92 pts · comentarios: parcial · corpus anterior: 477,450 items  
  Idea: A cloud music storage service that lets the user upload their legally purchased audio files and guarantees the tracks will not be removed due to licensing or geographic restrictions.  
  Sugeridas en el hilo: S3 (parcial); Funkwhale (parcial); Plex (parcial); Jellyfin (parcial, en corpus); Navidrome (parcial, en corpus); YouTube Music (upload feature) (parcial)
  - 0.60 · Relar – an open source music hosting and streaming service · creado 2021-01-24 · https://relar.app
  - 0.59 · Streem.io - Media Center on the Cloud · creado 2013-02-22 · http://www.streem.io
  - 0.53 · Viberr · creado 2016-03-28 · https://github.com/buckyroberts/Viberr
- **no** (0.57) · [Ask HN: What software do you use to gather requirements?](https://news.ycombinator.com/item?id=27615562) · 2021-06-24 · 88 pts · comentarios: existe con item en corpus · corpus anterior: 421,020 items  
  Idea: Looking for a tool that lets a team collect and organize requirements and work‑breakdown structures in an itemised way, with built‑in version control and easy change tracking, and ideally the ability to link requirements to WBS items.  
  Sugeridas en el hilo: GitBook (equivalente, en corpus); Slack (parcial); Miro (parcial); Roam Research (parcial); IBM DOORS (equivalente); Excel (parcial)
  - 0.57 · openproject · creado 2012-11-28 · https://github.com/opf/openproject
  - 0.53 · doorstop · creado 2013-04-01 · https://github.com/doorstop-dev/doorstop
  - 0.47 · NearBeach · creado 2017-01-20 · https://github.com/nearbeach/NearBeach
- **no** (0.55) · [Ask HN: Is there a fitness wristband that is hackable?](https://news.ycombinator.com/item?id=15823597) · 2017-12-01 · 197 pts · comentarios: existe con item en corpus · corpus anterior: 237,249 items  
  Idea: A fitness wristband or watch that includes GPS, heart‑rate monitoring and a pedometer, and that lets the user export the raw sensor data without using proprietary cloud services or software.  
  Sugeridas en el hilo: Garmin Fenix 3 / Fenix 5X (equivalente); Garmin Forerunner FR220 (USB m (equivalente); Gadgetbridge (open‑source Andr (parcial); MBientlab (hardware platform) (parcial); TI EZ430‑Chronos (development  (parcial); Pebble (smartwatch, community‑ (parcial)
  - 0.55 · openambit · creado 2014-01-31 · https://github.com/openambitproject/openambit
  - 0.53 · ttwatch · creado 2014-10-24 · https://github.com/ryanbinns/ttwatch
  - 0.43 · Gadgetbridge · creado 2015-01-05 · https://github.com/Freeyourgadget/Gadgetbridge
- **no** (0.51) · [Ask HN: How do you responsibly report security bugs to open-source projects?](https://news.ycombinator.com/item?id=21920142) · 2019-12-31 · 84 pts · comentarios: existe sin item en corpus · corpus anterior: 341,844 items  
  Idea: A platform or service that lets security researchers responsibly disclose vulnerabilities in open‑source projects, especially when the maintainer is unresponsive, and provides guidance, coordination, and possibly bounty handling.  
  Sugeridas en el hilo: GitHub Security Lab (security  (equivalente); security.txt (parcial, en corpus); CVE request process (MITRE) (parcial); US‑CERT coordination service (parcial); Linux distribution security te (parcial)
  - 0.51 · advisories · creado 2019-02-26 · https://github.com/ssd-secure-disclosure/advisories
  - 0.29 · crowdsourced penetration tests via bug bounties · creado 2014-07-01 · https://blog.bugcrowd.com/flex-bug-bounty-two-week-assessment/
  - 0.27 · We just created this brand new (free) bug reporting tool – Garage · creado 2019-07-30 · https://garage.fueled.com
- **no** (0.40) · [Ask HN: Is there a DNA/genealogy site you trust?](https://news.ycombinator.com/item?id=24395628) · 2020-09-06 · 21 pts · comentarios: incierto · corpus anterior: 383,094 items  
  Idea: A privacy‑focused DNA testing and genealogy service that lets users build family trees without risking their genetic data being resold or retained.  
  Sugeridas en el hilo: 23andMe (equivalente)
  - 0.40 · genealogy-old · creado 2018-05-30 · https://github.com/liberu-genealogy/genealogy-old
  - 0.35 · silsilah · creado 2017-08-16 · https://github.com/nafiesl/silsilah
  - 0.33 · webtrees · creado 2013-08-02 · https://github.com/fisharebest/webtrees
- **no** (0.40) · [Ask HN: Is there a way to get notified when my cat has seizures?](https://news.ycombinator.com/item?id=40939333) · 2024-07-11 · 71 pts · comentarios: parcial · corpus anterior: 552,638 items  
  Idea: A wearable sensor (accelerometer/gyroscope, vibration, heart‑rate or EEG) that can be attached to a cat’s collar or harness, detect the characteristic movements or physiological changes during a seizure, and send a push notification to the owner’s phone.  
  Sugeridas en el hilo: Aqara Zigbee vibration sensor (parcial); Tractive GPS tracker for cats (parcial); Whistle pet tracker (dog‑orien (parcial); PineTime smart watch (parcial); RuuviTag BLE beacon with accel (parcial); Open Seizure Detector (softwar (parcial)
  - 0.40 · PebbleSeizureDetect · creado 2015-11-30 · https://github.com/PebbleSeizureDetect/PebbleSeizureDetect
  - 0.30 · H-Watch · creado 2020-11-04 · https://github.com/ETH-PBL/H-Watch
  - 0.26 · animatedSensor-card · creado 2022-07-22 · https://github.com/4TWIGGERS/animatedSensor-card
- **no** (0.38) · [Ask HN: Can you recommend a modern, accessible P2P framework/library?](https://news.ycombinator.com/item?id=18511911) · 2018-11-22 · 78 pts · comentarios: parcial · corpus anterior: 286,285 items  
  Idea: Looking for a modern, well‑documented, easy‑to‑use peer‑to‑peer framework or library (preferably with Rust or Python bindings) that can serve as a foundation for building GUI applications.  
  Sugeridas en el hilo: libtorrent (parcial, en corpus); libp2p (rust) (parcial, en corpus); Holochain (parcial, en corpus); aiortc (WebRTC for Python) (parcial); hypercore / hyperdrive (datpro (parcial); Tribler / IPv8 (parcial, en corpus)
  - 0.38 · firestr · creado 2013-03-04 · https://github.com/mempko/firestr
  - 0.37 · kivy · creado 2010-11-03 · https://github.com/kivy/kivy
  - 0.36 · lbry-sdk · creado 2015-08-20 · https://github.com/lbryio/lbry-sdk
- **no** (0.36) · [Ask Dang: What tools do you use for moderating HN?](https://news.ycombinator.com/item?id=34920400) · 2023-02-24 · 278 pts · comentarios: parcial · corpus anterior: 489,164 items  
  Idea: A tool or set of utilities that assist the moderator in reviewing, flagging, deleting, and otherwise managing Hacker News comments and submissions in real time.  
  Sugeridas en el hilo: custom browser extension (parcial); killfile (parcial); ChatGPT (parcial)
  - 0.36 · (EARLY) Phoenix LiveView Reddit-Like Site · creado 2019-12-24 · https://github.com/smileys-tavern/gabbler
  - 0.34 · Dashboard I've Built · creado 2018-12-28 · https://demo.architectui.com/architect-landing
  - 0.33 · Hacker Reads, something I made for fun. · creado 2012-09-07 · http://www.hackerreads.com/
- **no** (0.34) · [Ask HN: What tool would you buy to make your life easier?](https://news.ycombinator.com/item?id=31303358) · 2022-05-08 · 31 pts · comentarios: incierto · corpus anterior: 457,056 items  
  Idea: A unified account management tool that can discover all of a user's accounts across various services, display the authentication methods used (password, social login, etc.), and allow merging, renaming, or deleting accounts and sign‑in methods without cumbersome confirmation steps or support tickets.  
  Sugeridas en el hilo: ninguna
  - 0.34 · midpoint · creado 2013-12-30 · https://github.com/Evolveum/midpoint
  - 0.31 · ManageYum A unified control panel to manage all your services. · creado 2014-02-11 · http://manageyum.com/
  - 0.28 · LdapCherry, a simple web ui to manage users in multiple directories · creado 2015-11-03 · https://github.com/kakwa/ldapcherry

## Costos

- OpenRouter, extracción (openai/gpt-oss-120b, 397 Asks, con reintentos): $0.123 (usage.cost facturado).
- Anthropic, consultas llm5 (claude-opus-5 directo): $0.016 (una idea, antes de que la cuenta quedara sin crédito; tokens a $5/$25 por millón).
- OpenRouter, consultas llm5 (anthropic/claude-opus-5, prompt v2, 40 ideas): $0.554 (usage.cost facturado).
- OpenRouter, Jev (40,000 pares válidos + 1.000 descartados): $1.330 (usage.cost facturado).
- **Total: $2.023**. Tope: $0.90 al principio; con la recarga de OpenRouter ($5) se subió a $2.40 para procesar las 40 ideas.

## Incidentes y decisiones

- Extracción: openai/gpt-oss-120b con schema estricto degeneró en 39/397 salidas (idea "....", nombres vacíos). Se agregó validación + reintento (tercer intento con qwen/qwen3-30b-a3b-instruct-2507); las salidas inválidas quedan en `data/askhn/extractions_descartadas.json` con su costo, que cuenta en el total.
- Una idea llegó a procesarse con una extracción degenerada (Claude inventó una necesidad a partir de "...."): sus 1.000 veredictos están archivados en `verdicts_jev_askhn_descartado.jsonl` y no entran en ningún resultado.
- La cuenta de Anthropic se quedó sin crédito (error 400 de saldo, tratado como un 402): se frenó y, con el OK del usuario, las consultas siguieron con el mismo modelo y el mismo prompt vía OpenRouter.

## Caveats

- **Los comentarios no son la verdad completa.** "No existe" puede ser ignorancia de quien comenta o del OP; "existe" puede ser una sugerencia que no cumple lo pedido (el LLM distingue equivalente/parcial, pero lo hace leyendo el hilo, no probando la herramienta).
- **Sesgo de selección de Ask HN:** pedidos de devs, en inglés, con votos y respuestas (>= 5 puntos, >= 3 comentarios); los pedidos sin respuesta (quizá los huecos más reales) quedan fuera por el filtro de comentarios.
- **Etiqueta en la fecha del Ask:** el corpus se restringe a lo creado antes del Ask, pero los README de GitHub son los de hoy (un repo anterior pudo agregar la funcionalidad después) y las estrellas se miden hoy (>= 100★ hoy, no en la fecha del Ask).
- **Cobertura del corpus:** una herramienta sugerida que no está en el corpus no se puede encontrar; un "no" del sistema con etiqueta "existe sin item en corpus" es un límite de cobertura, no un error del verificador.
- **Extracción automática:** etiqueta e idea vienen de un LLM barato; la cola c) de `gapfinder review` las confirma o corrige.
- Muestra chica (40 ideas procesadas): los porcentajes son orientativos.

