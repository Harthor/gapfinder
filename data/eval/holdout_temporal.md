# Holdout temporal: ¿qué dice el sistema de ideas que todavía no existían?

Corte **T = 2024-01-01**. Corpus restringido: Show HN publicados y repos GitHub (>= 100★) creados antes de T (531,070 items; embeddings MiniLM existentes filtrados por fecha, sin re-embeber). Ideas: Show HN posteriores a T. Regla de la Fase 3: P(núcleo) >= 0.9 ya construido, 0.85-0.9 revisar, < 0.85 no.

## Cómo se eligieron las ideas

- Por qué T = 2024-01-01: deja ~136 mil Show HN y ~402 mil repos antes, y ~82 mil Show HN después (2024-2026). Un corte más tardío daría más corpus pero menos ventana posterior y más cerca de la fecha en que se midieron las estrellas.
- Filtro: >= 20 puntos, >= 400 caracteres de texto real (no title_only). Fuera versiones/relanzamientos: título con v2/2.0/relaunch/now with/is back/rewrite… (100), repo de GitHub enlazado creado antes de T (241), dominio con un Show HN anterior a T (235). Elegibles: 3,926.
- Muestra barajada con semilla 11; se generaron consultas para las primeras 40 y se quedaron las primeras 35 que Claude clasificó como herramienta de software (las otras: juegos, arte, demos).
- **35 ideas y no 50** por el tope de $2.00 de la sesión (Claude + Jev; ver Costos). Top-K = 1000 sin recortar.
- Descripciones: mismo método que los known cases (Claude, prompt v2, llm5 + RRF). No pueden nombrar producto, marca ni URL; `leakage_flag` si el nombre/dominio/repo del producto aparece igual: 2 ideas (hold-41124112 (['saas']), hold-46483550 (['mcp'])). Ambas son términos de categoría que coinciden con el nombre; se dejaron en la muestra marcadas.

## Resultado

Ideas verificadas completas: 35/35.

| decisión | ideas |
|---|---|
| ya construido | 8/35 (23%) |
| revisar | 7/35 (20%) |
| no | 20/35 (57%) |

Lectura: "ya construido" = el sistema encuentra un equivalente anterior a T (a adjudicar: ¿lo es de verdad?). "no" = candidata a hueco-en-T: no hay nada anterior a T en el corpus que Jev considere el núcleo.


## Candidatas a hueco-en-T (decisión: no) — 3 mejores candidatos

- `hold-39407162` · idea posterior a T: **I built an alternative to product tours** (2024-02-17, 69 pts)  
  https://vykee.co/  
  Necesidad: I need a way to reduce overwhelm for new users of a feature-heavy app by hiding advanced UI controls at first and revealing them gradually as the user becomes more experienced, instead of relying on onboarding walkthroughs. It should also track which features and UI elements actually get used so I know what to hide.
  - 0.37 · **Unhide** · creado 2020-01-23 · https://github.com/YJesus/Unhide
  - 0.37 · **angular-feature-flags** · creado 2013-09-03 · https://github.com/michaeltaranto/angular-feature-flags
  - 0.35 · **awarejs** · creado 2012-11-28 · https://github.com/xoxco/awarejs
- `hold-45485986` · idea posterior a T: **DidMySettingsChange – A tool that checks changed windows settings** (2025-10-05, 51 pts)  
  https://github.com/nolesapex/DidMySettingsChange  
  Necesidad: I disable Windows privacy and telemetry options, but updates silently turn them back on. I want something that monitors those settings and tells me when any of them have changed from how I set them.
  - 0.41 · **ossec-hids** · creado 2013-09-17 · https://github.com/ossec/ossec-hids
  - 0.39 · **open-audit** · creado 2015-08-10 · https://github.com/Opmantek/open-audit
  - 0.38 · **DSCEA** · creado 2017-02-15 · https://github.com/microsoft/DSCEA
- `hold-48907681` · idea posterior a T: **Low-latency local LLM runner via OpenJDK Panama FFM (Java 22)** (2026-07-14, 38 pts)  
  https://github.com/projectargus-cc/libargus.cc  
  Necesidad: I want to run local LLM and speech-to-text inference directly inside a Java application without spawning a separate HTTP server process, with low latency and no garbage-collection overhead on the inference path.
  - 0.54 · **onnxruntime-genai** · creado 2023-11-13 · https://github.com/microsoft/onnxruntime-genai
  - 0.43 · **Jlama** · creado 2023-07-31 · https://github.com/tjake/Jlama
  - 0.42 · **whisper-jni** · creado 2023-06-10 · https://github.com/GiviMAD/whisper-jni
- `hold-47230620` · idea posterior a T: **I made a zero-copy coroutine tracer to find my scheduler's lost wakeups** (2026-03-03, 49 pts)  
  https://github.com/lixiasky-back/coroTracer  
  Necesidad: I need a way to observe coroutine state transitions in an M:N scheduler from outside the process, with minimal overhead, so I can diagnose hangs like lost wakeups where a task never gets resumed and memory sanitizers show nothing.
  - 0.55 · **compio** · creado 2023-08-28 · https://github.com/compio-rs/compio
  - 0.53 · **perfetto** · creado 2019-12-10 · https://github.com/google/perfetto
  - 0.49 · **fgtrace** · creado 2022-09-17 · https://github.com/felixge/fgtrace
- `hold-38852257` · idea posterior a T: **Clutter-free, powerful Mac-native sample manager** (2024-01-03, 47 pts)  
  https://www.kickspro.app  
  Necesidad: I have thousands of audio samples from sound packs scattered in folders and need a fast desktop app to browse, tag, audition and search them by key, BPM and type. Ideally it extracts that info automatically from messy file names.
  - 0.56 · **quodlibet** · creado 2015-03-14 · https://github.com/quodlibet/quodlibet
  - 0.54 · **MediaChips** · creado 2020-11-09 · https://github.com/fupdec/MediaChips
  - 0.49 · **pulp** · creado 2023-02-14 · https://github.com/vincehi/pulp
- `hold-44960594` · idea posterior a T: **Project management system for Claude Code** (2025-08-20, 175 pts)  
  https://github.com/automazeio/ccpm  
  Necesidad: When using AI coding agents, context and specs get lost between tasks, so I need a lightweight way to turn requirements documents into epics and tasks tracked in the issue tracker of my repository, keeping parallel agent work traceable to the original spec.
  - 0.59 · **Auto-generate user stories, test plans, and more in Azure DevOps** · creado 2023-08-24 · https://marketplace.visualstudio.com/items?itemName=Neudesic.TachyonGPT
  - 0.53 · **Fable – Spec as the Source of Truth** · creado 2021-03-01 · https://news.ycombinator.com/item?id=26306115
  - 0.45 · **ticgit** · creado 2008-03-18 · https://github.com/schacon/ticgit
- `hold-44118174` · idea posterior a T: **Every problem and solution in Beyond Cracking the Coding Interview** (2025-05-28, 151 pts)  
  https://news.ycombinator.com/item?id=44118174  
  Necesidad: I want a free collection of coding interview problems with worked solutions, plus a way to practice them interactively with an AI interviewer that gives hints and feedback at chosen topics and difficulty levels.
  - 0.59 · **Practice coding interviews with tips and solution analysis with GPT** · creado 2023-08-18 · https://www.pgrammer.com
  - 0.54 · **theEmbeddedNewTestament.github.io** · creado 2020-07-15 · https://github.com/theEmbeddedGeorge/theEmbeddedNewTestament.github.io
  - 0.47 · **Interactive realistic challenges (CTF) with an AI-Based assistance** · creado 2022-04-08 · https://platform.interway.ai
- `hold-40010050` · idea posterior a T: **Running TempleOS in user space without virtualization** (2024-04-12, 228 pts)  
  https://github.com/1fishe2fishe/EXODUS  
  Necesidad: I want to run an experimental hobby operating system and its native programs directly on my existing desktop OS, without booting a virtual machine, so files are shared seamlessly and I can use its language from a normal command line.
  - 0.62 · **inferno-os** · creado 2021-03-22 · https://github.com/inferno-os/inferno-os
  - 0.58 · **lxroot** · creado 2020-02-02 · https://github.com/parke/lxroot
  - 0.58 · **enroot** · creado 2018-10-17 · https://github.com/NVIDIA/enroot
- `hold-44004827` · idea posterior a T: **SQL-tString a t-string SQL builder in Python** (2025-05-16, 85 pts)  
  https://github.com/pgjones/sql-tstring  
  Necesidad: I want to write SQL queries inline in Python using string interpolation syntax without risking SQL injection, with interpolated values automatically turned into bound parameters and identifiers validated against an allowlist. I also need parts of the WHERE clause to drop out automatically when a value isn't supplied, so I don't hand-build dynamic queries.
  - 0.64 · **jinjasql** · creado 2016-10-24 · https://github.com/sripathikrishnan/jinjasql
  - 0.64 · **JinjaSQL – Template Language for SQL** · creado 2020-06-02 · https://github.com/hashedin/jinjasql
  - 0.61 · **JinjaSQL – Generate SQL Queries using a Jinja Template** · creado 2016-11-04 · https://github.com/hashedin/jinjasql
- `hold-40539471` · idea posterior a T: **I built a directory about big life decisions/regrets** (2024-05-31, 121 pts)  
  https://www.didyouregretit.com/  
  Necesidad: I want a place to read other people's accounts of major life decisions and whether they ended up regretting them, so I can get perspective while facing a tough choice of my own.
  - 0.65 · **Settled Afar Podcast** · creado 2020-04-30 · https://news.ycombinator.com/item?id=23029354
  - 0.60 · **MCDM application designed to simplify complex decision-making processes** · creado 2023-04-11 · https://decisionmentor.app
  - 0.59 · **a platform for life stories. Featuring Sahil Lavingia of Gumroad.** · creado 2012-05-30 · http://www.storylane.com/profile/1100009916/sahil-lavingia
- `hold-47461529` · idea posterior a T: **Red Grid Link – peer-to-peer team tracking over Bluetooth, no servers** (2026-03-20, 54 pts)  
  https://github.com/RedGridTactical/RedGridLink  
  Necesidad: I need a way for my hiking group to see each other's locations on a map when there's no cell service, using only our phones with no servers or extra radios. It should work over short-range wireless between devices and show offline maps with last-known positions when someone goes out of range.
  - 0.67 · **peer to peer location sharing** · creado 2013-02-17 · http://linkstore.ru/wayn/help.jsp
  - 0.51 · **App for sharing location/speed without using data** · creado 2018-04-13 · https://play.google.com/store/apps/details?id=com.locate.imrighthere
  - 0.43 · **Graticule – an Android app for real-time location sharing** · creado 2014-10-07 · https://play.google.com/store/apps/details?id=com.emilburzo.graticule
- `hold-43760452` · idea posterior a T: **I built an app so I could read the 3 Body-Problem in Chinese** (2025-04-22, 29 pts)  
  https://readly.ink/  
  Necesidad: I want to read physical books in a foreign language without constantly stopping to look up words: an app that photographs a printed page, extracts the text, lets me tap any word for a translation, save it to flashcards, hear it read aloud, and ask questions about the passage.
  - 0.68 · **Manabi Reader – Learn Japanese by Reading on iOS and macOS (SwiftUI)** · creado 2023-07-10 · https://reader.manabi.io/#page-top
  - 0.58 · **pot-desktop** · creado 2023-02-26 · https://github.com/pot-app/pot-desktop
  - 0.49 · **GoldenDict-OCR** · creado 2022-04-06 · https://github.com/JingDict/GoldenDict-OCR
- `hold-41393005` · idea posterior a T: **A discovery-focused search engine for Hacker News** (2024-08-29, 193 pts)  
  https://hn.trieve.ai/  
  Necesidad: I want a better way to search and discover stories and comments on Hacker News, with semantic/vector search, filters by site, recommendations and AI chat over results, instead of plain keyword search.
  - 0.75 · **AI News Analyst** · creado 2023-10-21 · https://newsanalyst.vercel.app/
  - 0.73 · **An Embedding-Based Search Service over ShowHN, AskHN, GitHub, More** · creado 2023-10-25 · https://payperrun.com/%3E/search
  - 0.63 · **My recommendation engine for Hacker News** · creado 2023-06-19 · https://hn-recommend.julienc.me
- `hold-44501076` · idea posterior a T: **Sumble – knowledge graph for GTM data – query tech stack, key projects** (2025-07-08, 91 pts)  
  https://sumble.com  
  Necesidad: I need a way to find out what technologies specific teams inside large companies use, what projects they're working on, and who is involved, so I can target sales outreach precisely.
  - 0.76 · **Enrichify – Data Enrichment Aggregation and Orchestration** · creado 2023-11-14 · https://enrichifyapp.com/
  - 0.54 · **Enterprise company search engine for product outreach/sales** · creado 2014-11-21 · http://www.whatisnova.com
  - 0.52 · **LinkedInt** · creado 2017-07-12 · https://github.com/mdsecactivebreach/LinkedInt
- `hold-49524469` · idea posterior a T: **Newton's Orchard – Browser-based space/gravity playground** (2026-09-01, 33 pts)  
  https://newtonsorchard.app  
  Necesidad: I want an interactive browser-based gravity and orbital mechanics simulator where I can create and edit planets, run and rewind the simulation, and try preset scenarios, so students can explore how orbits work beyond simple two-body demos.
  - 0.78 · **Harmony-of-the-Spheres** · creado 2018-06-06 · https://github.com/TheHappyKoala/Harmony-of-the-Spheres
  - 0.70 · **SolarSim** · creado 2023-10-06 · https://github.com/jan-tennert/SolarSim
  - 0.59 · **Gravity-Simulator** · creado 2015-03-08 · https://github.com/HermannBjorgvin/Gravity-Simulator
- `hold-49361478` · idea posterior a T: **Anonymous age verification with passkey-powered encryption** (2026-08-19, 45 pts)  
  https://loginwithone.com/  
  Necesidad: I need a way to let users prove they're over 18 to my site without collecting or exposing their identity documents or personal data, ideally with a single sign-on flow where the user's ID data stays encrypted on their own device and doesn't have to be re-uploaded each time.
  - 0.79 · **irmamobile** · creado 2020-05-11 · https://github.com/privacybydesign/irmamobile
  - 0.78 · **self** · creado 2023-07-22 · https://github.com/selfxyz/self
  - 0.67 · **nl-wallet** · creado 2022-11-25 · https://github.com/MinBZK/nl-wallet
- `hold-41243901` · idea posterior a T: **A free tool to visualise scales on a guitar** (2024-08-14, 27 pts)  
  https://stringscales.com/  
  Necesidad: I want a free, customizable way to see guitar scales mapped out on the fretboard, including position systems like CAGED and three-notes-per-string, so I can practice and teach without paying for basic features.
  - 0.80 · **A tool to visualize scale/arpeggio shapes on a guitar fretboard** · creado 2023-05-11 · https://www.fretboard.website/
  - 0.80 · **gtr-cof** · creado 2016-10-10 · https://github.com/mikehadlow/gtr-cof
  - 0.79 · **fretboarder** · creado 2019-12-05 · https://github.com/cheap-glitch/fretboarder
- `hold-41124112` · idea posterior a T: **Non SaaS – Directory of Non SaaS Apps** (2024-07-31, 76 pts) · ⚠️ leakage_flag  
  https://nonsaas.com  
  Necesidad: I'm tired of monthly subscriptions and want a curated list of software I can buy once or self-host instead, organized by the SaaS tools they replace.
  - 0.81 · **awesome-vibecoded-saas** · creado 2023-05-06 · https://github.com/Anil-matcha/awesome-vibecoded-saas
  - 0.80 · **Opensource.builders, open-source alternatives to commercial software** · creado 2020-02-26 · https://opensource.builders
  - 0.77 · **open-source-alternatives** · creado 2023-05-22 · https://github.com/btw-so/open-source-alternatives
- `hold-46422812` · idea posterior a T: **Evidex – AI Clinical Search (RAG over PubMed/OpenAlex and SOAP Notes)** (2025-12-29, 36 pts)  
  https://www.getevidex.com  
  Necesidad: Clinicians need a fast, affordable way to ask clinical questions in plain language and get cited, evidence-based answers drawn from the latest medical literature and guidelines, plus help drafting patient notes.
  - 0.81 · **Ai-Healthcare-Chatbot** · creado 2019-12-11 · https://github.com/arvindsis11/Ai-Healthcare-Chatbot
  - 0.78 · **GalenAI – An AI Powered Search Engine for Clinicians** · creado 2023-06-07 · https://galenai.co
  - 0.72 · **Medical LLM API on par with Google Med-PaLM 2. 92% USMLE accuracy** · creado 2023-08-07 · https://medisearch.io/api
- `hold-45304911` · idea posterior a T: **Run Qwen3-Next-80B on 8GB GPU at 1tok/2s throughput** (2025-09-19, 123 pts)  
  https://github.com/Mega4alik/ollm  
  Necesidad: I want to run very large language models with 100k-token contexts on a consumer GPU with only 8GB of VRAM, without quantizing the weights, by streaming layers and KV cache from SSD or CPU memory.
  - 0.83 · **airllm** · creado 2023-06-12 · https://github.com/lyogavin/airllm
  - 0.61 · **BMInf** · creado 2021-08-24 · https://github.com/OpenBMB/BMInf
  - 0.51 · **PyTorch-LIT** · creado 2021-11-15 · https://github.com/AminRezaei0x443/PyTorch-LIT

## Revisar (0.85-0.90) — mejor candidato

- `hold-48871547` · idea posterior a T: **Clx – Compile Lua to Native Executables Through C++20** (2026-07-11, 143 pts)  
  https://github.com/samyeyo/clx  
  Necesidad: I want to turn my Lua scripts into standalone native executables that run fast without shipping an interpreter, ideally by compiling ahead of time with my normal system compiler toolchain.
  - 0.85 · **luastatic** · creado 2015-10-24 · https://github.com/ers35/luastatic
- `hold-42041368` · idea posterior a T: **AI Agents for engineering use cases like debugging, LLD,testing etc.** (2024-11-04, 26 pts)  
  https://github.com/potpie-ai/potpie  
  Necesidad: I want AI agents that understand my whole codebase so they can help with debugging, low-level design, writing integration tests and reviewing pull requests, and I'd like to configure custom agents for my own engineering workflows.
  - 0.85 · **codefuse-chatbot** · creado 2023-09-28 · https://github.com/codefuse-ai/codefuse-chatbot
- `hold-39613021` · idea posterior a T: **Piping logs, visualizing in a web app – just suffix "| npx logscreen"** (2024-03-06, 128 pts)  
  https://github.com/soorajshankar/logScreen  
  Necesidad: I want to pipe the output of any terminal command into a browser-based viewer so I can read, search and filter streaming logs in real time instead of squinting at the terminal.
  - 0.87 · **node-bcat** · creado 2014-01-18 · https://github.com/kessler/node-bcat
- `hold-43946066` · idea posterior a T: **Code Claude Code** (2025-05-10, 117 pts)  
  https://github.com/RVCA212/codesys  
  Necesidad: I want to automate my repetitive AI coding assistant workflow by calling the agent CLI programmatically from a script, instead of typing prompts by hand each time.
  - 0.88 · **GPTMe, a CLI to interact with LLMs, able to execute code locally** · creado 2023-09-05 · https://github.com/ErikBjare/gptme
- `hold-45656952` · idea posterior a T: **Katakate – Dozens of VMs per node for safe code exec** (2025-10-21, 124 pts)  
  https://github.com/Katakate/k7  
  Necesidad: I need to run untrusted or AI-generated code in strongly isolated sandboxes, packing many lightweight VMs onto each server, without the risks and complexity of nested containers. I want a simple CLI and Python API instead of hand-rolling VM orchestration and networking.
  - 0.88 · **Run LLM-generated code in sandboxed envs** · creado 2023-09-27 · https://e2b.dev/docs/playgrounds/execute
- `hold-41683407` · idea posterior a T: **Open-source app builder for comfy workflows** (2024-09-28, 59 pts)  
  https://github.com/ViewComfy/ViewComfy  
  Necesidad: I have node-based image generation workflows that are too complex for non-technical users, and I want to expose them as a simple web app with input fields for text and images and an output gallery.
  - 0.89 · **comfyui-openrouter-ai** · creado 2023-03-04 · https://github.com/dulaiduwang003/comfyui-openrouter-ai
- `hold-44447233` · idea posterior a T: **a community for collaborating on sideprojects** (2025-07-02, 48 pts)  
  https://relentlessly.no/  
  Necesidad: I need a place to find collaborators for my side project — someone with complementary skills like a developer, designer or marketer — with profile pages so I can see who they are and what they've built before reaching out.
  - 0.89 · **CollabFinder, find developers and designers for your next great project** · creado 2012-04-17 · http://collabfinder.com

## Ya construido (>= 0.90) — mejor candidato

- `hold-46483550` · idea posterior a T: **Comet MCP – Give Claude Code a browser that can click** (2026-01-04, 28 pts) · ⚠️ leakage_flag  
  https://github.com/hanzili/comet-mcp  
  Necesidad: I want my AI coding assistant to be able to handle tasks on websites that have no API — logging into dashboards, clicking through admin panels, generating keys — by delegating the browsing to an autonomous browser agent instead of driving every click itself and filling up its context window.
  - 0.90 · **openbrowser** · creado 2019-04-11 · https://github.com/ntegrals/openbrowser
- `hold-44515266` · idea posterior a T: **Petrichor – a free, open-source, offline music player for macOS** (2025-07-09, 202 pts)  
  https://github.com/kushalpandya/Petrichor  
  Necesidad: I have a large collection of local music files and want a desktop app for macOS that can organize, browse, and play them offline, with playlists, a play queue, and fast search across thousands of tracks.
  - 0.91 · **harmonoid** · creado 2020-08-04 · https://github.com/harmonoid/harmonoid
- `hold-42203895` · idea posterior a T: **Yami – An Open Source Music Player with Spotdl Integration** (2024-11-21, 88 pts)  
  https://github.com/DevER-M/yami  
  Necesidad: I want a simple, ad-free desktop music player that plays my local audio files and can also fetch and download tracks from online streaming sources into my library.
  - 0.92 · **FLB-Music-Player** · creado 2021-08-27 · https://github.com/FLB-Music/FLB-Music-Player
- `hold-45226277` · idea posterior a T: **I made a small site to share text and files** (2025-09-12, 41 pts)  
  https://www.dum.pt/  
  Necesidad: I need a quick way to send a snippet of text or a file to someone else over the web without creating an account, with links that expire after a short time.
  - 0.92 · **pastebin-worker** · creado 2023-02-01 · https://github.com/xiadd/pastebin-worker
- `hold-45558611` · idea posterior a T: **I built a simple ambient sound app with no ads or subscriptions** (2025-10-12, 314 pts)  
  https://ambisounds.app/  
  Necesidad: I want a simple app that plays and mixes background ambient sounds like rain, waves, and wind for focus or sleep, with no ads, paywalls, or subscriptions, and that works offline.
  - 0.94 · **moodist** · creado 2023-10-05 · https://github.com/remvze/moodist
- `hold-46331364` · idea posterior a T: **Netrinos – A keep it simple Mesh VPN for small teams** (2025-12-19, 93 pts)  
  https://netrinos.com  
  Necesidad: I need an easy way to connect my computers, servers, NAS and IoT devices across different networks as if they were on the same LAN, without port forwarding, VPN appliances or exposing anything to the internet. It should handle NAT traversal automatically and give each device a stable address for remote desktop and SSH.
  - 0.95 · **ZeroTierOne** · creado 2013-04-24 · https://github.com/zerotier/ZeroTierOne
- `hold-44650567` · idea posterior a T: **Any-LLM – Lightweight router to access any LLM Provider** (2025-07-22, 125 pts)  
  https://github.com/mozilla-ai/any-llm  
  Necesidad: I want a single unified way to call many different large language model providers from my code, so switching between models or vendors is just a config/string change instead of rewriting integration code. It should be a lightweight library I can import, not a separate proxy or gateway server to run.
  - 0.95 · **LiteLLM -Open-Source Library for Anthropic,Azure,OpenAI, etc. API Calls** · creado 2023-08-08 · https://litellm.ai/
- `hold-43930554` · idea posterior a T: **Extension for full-text browser history search** (2025-05-08, 29 pts)  
  https://rearview-ai.vercel.app/  
  Necesidad: I want to search the full text of pages I've visited before, not just URLs and titles, so I can find a page I remember reading but can't recall the site name, with everything stored locally on my machine.
  - 0.96 · **full-text-tabs-forever** · creado 2023-08-12 · https://github.com/iansinnott/full-text-tabs-forever

## Costos

- Claude (claude-opus-5, 40 ideas con consultas): $0.731, calculado con los tokens de cada respuesta a $5/$25 por millón.
- Jev vía OpenRouter: 35,000 pares, $1.171 (usage.cost facturado).
- Total de la sesión: $1.901 (tope: $2.00).

## Caveats

- **Cobertura**: una idea posterior a T puede tener un equivalente anterior a T que no está en el corpus (Show HN + GitHub >= 100★). Un "no" no prueba que fuera un hueco; prueba que este corpus no lo tenía.
- **Estrellas**: el umbral de >= 100★ se mide hoy, no en T. Repos creados antes de T que llegaron a 100★ después están en el corpus restringido, y repos que tenían >= 100★ en T pero no hoy faltan.
- **Funcionalidad posterior**: un repo creado antes de T pudo agregar la funcionalidad después; su README es el de hoy. Un "ya construido" puede deberse a eso (el texto de los Show HN sí es el de su fecha).
- **Ideas lanzadas en HN**: son productos que alguien construyó; un "no" es "novedoso respecto del corpus en T", no demanda.
- Muestra chica (35) y regla calibrada en la Fase 3 con otros datos; las decisiones requieren adjudicación humana.

