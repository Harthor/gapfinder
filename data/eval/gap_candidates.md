# Candidatos a hueco: pedidos de Ask HN sin match fuerte en el corpus

Pedidos reales (extracción automática v2) corridos contra el corpus anterior a la fecha de cada Ask, con Jev sobre el top-200 y, si no hubo match, el top-1000. Cada pedido cae en un nivel, en este orden:

1. **match**: algún candidato con P(núcleo) >= 0.85 (ya construido; no se lista).
2. **no es software**: el pedido es hardware, contenido (libro, curso, guía, plantilla, licencia, lista), una encuesta ("what tools do you use", "how do you…") o un "¿se puede…?". Heurístico sobre el título del Ask y el sintagma nominal del pedido (`gaps.no_software`).
3. **descartado**: los comentarios dicen que existe (etiqueta e).
4. **hueco fuerte**: mejor P(núcleo) < 0.6 y etiqueta n o p.
5. **zona gris**: el resto (mejor P(núcleo) 0.6–0.85).

- Pedidos reales: 242; verificados: 242.
- Por nivel: hueco fuerte 12, zona gris 19, descartado (etiqueta e) 44, match >= 0.85 123, no es software 44.
- No es software, por motivo: encuesta 20, hardware 8, se puede 8, contenido 8.
- **Huecos fuertes: 12** (no existe 7, parcial 5); zona gris: 19 (no existe 6, parcial 13).
- Costo: extracción v2 $0.075, reformulaciones $0.034, Jev $4.895 (OpenRouter, usage.cost).

Caveats: los veredictos son los cacheados (no se re-verificó nada); las reformulaciones son de gpt-oss y la primera pasada usa top-200 (ver `data/eval/gap_compare_k200.md`). Un hueco es "sin equivalente en este corpus (Show HN + GitHub >= 100★) antes del Ask", no prueba que no exista; el pedido_resumido lo escribe un LLM. El umbral 0.6 no está calibrado con revisión humana.

## Hueco fuerte (12)

1. **A service that evaluates Windows 7 updates and provides a curated list of updates to avoid.**  
   [Ask HN: Looking for a Windows 7 Update curator](https://news.ycombinator.com/item?id=11074625) · 2016-02-10 · 5 pts · 4 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.22 (top-1000)  
   _El OP solicita explícitamente un sitio/servicio que cura actualizaciones de Windows 7; los comentarios no citan ningún recurso existente, solo hablan de la necesidad._
   - 0.22 · DarunGrim · 2010-08-14 · https://github.com/ohjeongwook/DarunGrim
   - 0.18 · BlockWindows · 2015-08-26 · https://github.com/WindowsLies/BlockWindows
   - 0.15 · The reverse package manager · 2011-11-07 · https://github.com/spiceapps/cupboard
   - 0.14 · PatchPae2 · 2016-02-01 · https://github.com/wj32/PatchPae2
   - 0.14 · Those Pesky Release Notes · 2014-02-06 · http://blog.aha.io/index.php/those-pesky-release-notes-and-product-management/

2. **A public website that aggregates SSD wear statistics for operating system and application beta releases.**  
   [Ask HN: Is there a website that tracks excessive writes to SSDs in OS/app betas?](https://news.ycombinator.com/item?id=49022990) · 2026-07-23 · 31 pts · 30 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.25 (top-1000)  
   _El OP solicita una herramienta concreta (sitio web) para rastrear escrituras excesivas en SSDs; los comentarios no mencionan ninguna solución existente._
   - 0.25 · One Metric – Collect and calculate metrics onto shared dashboards · 2019-06-12 · https://www.onemetric.io
   - 0.23 · tsviewdb · 2013-09-16 · https://github.com/google/tsviewdb
   - 0.20 · Wizard, Mac Statistics App by Evan Miller · 2013-08-31 · http://www.wizardmac.com/
   - 0.19 · statsite · 2012-05-01 · https://github.com/statsite/statsite
   - 0.19 · A status dashboard for non-automated systems · 2019-11-13 · https://devrig.com

3. **An app that converts normal language into Non‑Violent Communication phrasing.**  
   [Ask HN: Is There a Non-Violent Communication Language Converter?](https://news.ycombinator.com/item?id=30349970) · 2022-02-15 · 6 pts · 4 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.29 (top-1000)  
   _El OP busca una herramienta concreta; los comentarios indican que no existe ninguna y solo sugieren construir una._
   - 0.29 · FoxType – Using NLP to help you write more politely · 2015-10-12 · https://labs.foxtype.com
   - 0.28 · Slack chatbot for quick text analysis · 2019-02-04 · https://slack.com/apps/A8ME24FNG-summarizebot
   - 0.26 · We are the same, app for practicing compassion · 2012-05-25 · http://wearethesameapp.com
   - 0.25 · A modern “what you see is what you MEAN writing” app · 2020-02-25 · https://www.kickstarter.com/projects/wolfoliver/monsterwriter
   - 0.24 · I made this FB app to make a political statement. With source code · 2015-12-02 · http://customizemypic.com/welcome

4. **A parser library for Microsoft OneNote .one files or an open‑source note‑taking file format.**  
   [Ask HN: Is there a OneNote file parser? Or an equivalent opensource note format?](https://news.ycombinator.com/item?id=18219219) · 2018-10-15 · 11 pts · 7 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.32 (top-1000)  
   _El OP busca un parser o formato abierto; se menciona un proyecto concreto pero con problemas, sin confirmación clara de que funciona._
   - 0.32 · dtformats · 2017-04-23 · https://github.com/libyal/dtformats
   - 0.28 · Productivity-Tools · 2014-04-14 · https://github.com/ArthurHub/Productivity-Tools
   - 0.27 · deark · 2014-04-20 · https://github.com/jsummers/deark
   - 0.24 · Open-Source Parse (Startup School 2014) · 2014-10-11 · http://www.divide.io/
   - 0.24 · extract · 2015-05-07 · https://github.com/ICIJ/extract

5. **A public registry linking companies to their bank account numbers for verification.**  
   [Ask HN: Is there a register which company uses which bank?](https://news.ycombinator.com/item?id=35179186) · 2023-03-16 · 5 pts · 5 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.35 (top-1000)  
   _El OP pide un servicio concreto de registro de cuentas bancarias de empresas; los comentarios indican que no existe tal servicio público, solo datos parciales no accesibles._
   - 0.35 · Launched our first product - Accthub.com · 2012-05-14 · https://accthub.com
   - 0.23 · Open source list of ICOs financial information · 2018-10-23 · https://wentransparency.com
   - 0.23 · QwickUp, open-source lookup tool. · 2014-05-24 · http://qwickup.com/
   - 0.22 · Ask and Tally · 2012-04-23 · http://www.askandtally.com/
   - 0.20 · BankSpot.org · 2018-10-23 · https://www.bankspot.org/

6. **A tool to search public MIDI datasets for clips matching specific chord progressions and keys.**  
   [Ask HN: Is there a OS tool which queries MIDI datasets by chord progression/key?](https://news.ycombinator.com/item?id=34140098) · 2022-12-26 · 9 pts · 19 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.36 (top-1000)  
   _El OP quiere una herramienta concreta; los comentarios solo ofrecen partial solutions and libraries, no una herramienta ya existente._
   - 0.36 · I built this to make sharing from music services better · 2014-12-05 · https://match.audio/google/album/B4t6yqqvhnb2hy4st4uisjrcsrm
   - 0.30 · choco · 2022-02-23 · https://github.com/smashub/choco
   - 0.26 · Filter music based on mood, key, tempo, energy and other properties · 2019-07-15 · https://beta.skrrt.fun
   - 0.26 · RiffBank – A reverse guitar tab search engine · 2013-12-06 · http://riffbank.com/
   - 0.26 · Try my musician-savvy bot · 2012-02-20 · http://dev.bandscape.net/scapebot

7. **A privacy‑focused DNA testing and genealogy service for building family trees without data resale.**  
   [Ask HN: Is there a DNA/genealogy site you trust?](https://news.ycombinator.com/item?id=24395628) · 2020-09-06 · 21 pts · 15 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.43 (top-1000)  
   _El OP pide un servicio concreto de pruebas genéticas con privacidad; los comentarios advierten que no hay ninguno fiable y no se menciona ninguna herramienta existente._
   - 0.43 · genealogy-old · 2018-05-30 · https://github.com/liberu-genealogy/genealogy-old
   - 0.30 · geneweb · 2013-11-12 · https://github.com/geneweb/geneweb
   - 0.30 · silsilah · 2017-08-16 · https://github.com/nafiesl/silsilah
   - 0.26 · Free genetic reports from your genome · 2018-11-20 · https://meports.com
   - 0.25 · snpr · 2011-06-07 · https://github.com/openSNP/snpr

8. **A service to submit and monitor website content for inclusion in large language model training datasets.**  
   [Ask HN: Are there any movements to create the equivalent of a sitemap for LLM's?](https://news.ycombinator.com/item?id=40516685) · 2024-05-29 · 10 pts · 4 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.47 (top-1000)  
   _El OP pide una herramienta concreta para registrar sitios en los entrenamientos de LLM; los comentarios indican que no existe tal servicio y solo ofrecen soluciones parciales._
   - 0.47 · gi.st – the gist of the web · 2015-07-07 · http://thegi.st
   - 0.31 · In-application web training platform · 2016-01-07 · https://www.synergyse.com/platform/
   - 0.29 · Author Scan, a service that lets you monitor the web · 2013-11-13 · http://www.authorscan.com/
   - 0.29 · Use of AI to monitor 15M corporate websites · 2018-11-28 · https://twitter.com/aiHitPulse
   - 0.27 · Website Content Crawler to feed vector databases and LLMs via LangChain · 2023-04-06 · https://apify.com/apify/website-content-crawler

9. **A platform that connects patients with rare cancers to a worldwide pool of oncologists for case review and advice.**  
   [Ask HN: I'm afraid my wife is dying. Is there a “quora.com” for rare cancers?](https://news.ycombinator.com/item?id=28955982) · 2021-10-22 · 56 pts · 25 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.49 (top-1000)  
   _El OP busca un sitio tipo Quora para oncólogos; los comentarios ofrecen alternativas parciales (forums, segunda opinión), sin una solución exacta._
   - 0.49 · Tesse, a new interactive search engine · 2017-03-23 · https://news.ycombinator.com/item?id=13939339
   - 0.46 · Looking for a mentor/expert for advice? Wiser is here to help you · 2020-11-17 · https://getwiser.net/
   - 0.36 · Instawell, an anonymous community for our health + New API · 2013-06-21 · https://news.ycombinator.com/item?id=5917425
   - 0.35 · A new peer advice platform and knowledge marketplace · 2020-12-07 · https://www.thesageboard.com
   - 0.29 · Create your own Google Helpouts for any niche · 2015-02-14 · http://collaborg.com

10. **A PCAP analysis tool that lets you view and correlate multiple streams at once, e.g., with tabbed or linked stream views.**  
   [Ask HN: Is there a better PCAP analyzer than Wireshark?](https://news.ycombinator.com/item?id=25129228) · 2020-11-17 · 6 pts · 4 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.55 (top-1000)  
   _El OP pide una herramienta concreta para analizar capturas con múltiples flujos; los comentarios ofrecen alternativas que solo cubren parte de la necesidad._
   - 0.55 · CSI-SIEM · 2020-06-28 · https://github.com/Information-Warfare-Center/CSI-SIEM
   - 0.54 · netcap · 2018-11-28 · https://github.com/dreadl0ck/netcap
   - 0.54 · pi-list · 2017-10-18 · https://github.com/ebu/pi-list
   - 0.51 · wireshark · 2013-09-27 · https://github.com/boundary/wireshark
   - 0.50 · Malcolm · 2019-05-13 · https://github.com/cisagov/Malcolm

11. **A tool to generate 3D density maps of interior walls using Wi‑Fi signals.**  
   [Ask HN: Any tools to do generic WiFi imaging?](https://news.ycombinator.com/item?id=40946613) · 2024-07-12 · 97 pts · 68 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.56 (top-1000)  
   _El OP pide una herramienta específica de imagenología con Wi‑Fi; los comentarios solo ofrecen dispositivos similares (Walabot, stud finders) pero no una solución Wi‑Fi directa._
   - 0.56 · WiFi-Vision · 2017-09-16 · https://github.com/AideTechBot/WiFi-Vision
   - 0.50 · RadioDiff · 2024-06-20 · https://github.com/UNIC-Lab/RadioDiff
   - 0.34 · voxeltastic · 2015-02-13 · https://github.com/cnlohr/voxeltastic
   - 0.29 · Heimdall-WiFi-Radar · 2018-03-30 · https://github.com/G4lile0/Heimdall-WiFi-Radar
   - 0.21 · Radar, a new way to discover what's around you · 2016-12-29 · https://rrradarrr.com/

12. **A browser extension that blocks or warns about Amazon sellers with many fake or poor reviews.**  
   [Ask HN: Is there an extension to block sellers on Amazon?](https://news.ycombinator.com/item?id=17820655) · 2018-08-22 · 12 pts · 5 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.56 (top-1000)  
   _El OP solicita una herramienta concreta; los comentarios no mencionan ninguna extensión existente y sugieren crearla._
   - 0.56 · Fakespot – identify fake reviews  Amazon · 2015-01-21 · http://www.fakespot.com
   - 0.48 · Freshdill.com – Search Amazon and identify products with fake reviews · 2018-04-30 · http://freshdill.com
   - 0.44 · Amazon is littered with fake reviews, see through them – Freshdill.com · 2018-05-14 · http://freshdill.com
   - 0.44 · A Neural Networks Based Amazon Review Summarizer · 2017-11-21 · https://thereviewindex.com
   - 0.42 · Our app analyzes product ratings when you're at the store · 2012-07-02 · http://vimeo.com/daring/private-beta

## Zona gris (19)

1. **A tool or standard that automatically generates API client IDs and secrets for various services.**  
   [Ask HN: Is there an API key generator?](https://news.ycombinator.com/item?id=16334369) · 2018-02-08 · 5 pts · 4 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.65 (top-1000)  
   _El OP solicita una solución para generar claves API; los comentarios ofrecen generadores genéricos y mencionan estándares emergentes, pero sin una herramienta completa._
   - 0.65 · credhub · 2016-04-25 · https://github.com/cloudfoundry/credhub
   - 0.61 · My side project, a RESTful API to create authentications for your apps · 2011-05-16 · http://www.authdog.com/
   - 0.57 · osiam · 2015-04-28 · https://github.com/osiam/osiam

2. **An AI-powered tool that converts PDFs, including complex layouts and scanned documents, into ePub format.**  
   [Ask HN: Are there any AI-enhanced solutions for converting PDFs to ePub?](https://news.ycombinator.com/item?id=37468080) · 2023-09-11 · 7 pts · 5 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.70 (top-1000)  
   _El OP pide una solución concreta de OCR/AI para pasar PDFs a ePub; los comentarios no presentan una herramienta que haga eso, solo menciones parciales._
   - 0.70 · pdf2epubEX · 2020-07-05 · https://github.com/dodeeric/pdf2epubEX
   - 0.70 · pdf-converter · 2017-02-10 · https://github.com/jmrozanec/pdf-converter
   - 0.66 · ebook-converter-bot · 2021-08-25 · https://github.com/yshalsager/ebook-converter-bot

3. **A multi‑cloud storage aggregation service that can provision and delete storage across major cloud providers on demand.**  
   [Ask HN: Is there any multi-cloud storage aggregator company?](https://news.ycombinator.com/item?id=32426700) · 2022-08-11 · 9 pts · 5 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.71 (top-1000)  
   _El OP busca un servicio concreto de agregación de almacenamiento; los comentarios solo ofrecen parciales (blockchain storage, MinIO) sin un producto existente._
   - 0.71 · Object Store Manipulator – curl for cloud storage · 2017-03-11 · https://github.com/appscode/osm
   - 0.65 · cloud-pipeline · 2019-03-06 · https://github.com/epam/cloud-pipeline
   - 0.64 · osm · 2016-10-26 · https://github.com/appscode/osm

4. **A note‑taking app that syncs video, audio, transcripts and user notes in a single interface.**  
   [Is there any note-taking software/app for video?](https://news.ycombinator.com/item?id=33352743) · 2022-10-27 · 14 pts · 5 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.72 (top-1000)  
   _El OP busca una herramienta concreta; las respuestas solo mencionan parciales o extensiones, sin una solución completa existente._
   - 0.72 · Transnote – Video Notes by Timestamps · 2020-04-08 · https://get.transnote.co/M3e
   - 0.71 · PodNotes · 2022-07-02 · https://github.com/chhoumann/PodNotes
   - 0.65 · We Opened Up Our Transcription Tool · 2014-06-17 · https://news.ycombinator.com/item?id=7905996

5. **An app to log where personal items are stored and retrieve their location later.**  
   [Ask HN: Is there an app that reminds me where I stashed stuff?](https://news.ycombinator.com/item?id=10873151) · 2016-01-09 · 5 pts · 8 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.72 (top-1000)  
   _El OP pide una aplicación para registrar y buscar objetos, y los comentarios solo ofrecen soluciones parciales como hojas de cálculo o notas._
   - 0.72 · Online Inventory System for Individuals & Businesses - Want Feedback · 2012-08-02 · https://news.ycombinator.com/item?id=4330459
   - 0.67 · iPhone app for keeping track of your stuff · 2012-05-20 · http://www.RayMckaig.com/Lender
   - 0.67 · Simplifying searching on Android - Bean Search · 2015-04-21 · https://play.google.com/store/apps/details?id=in.beanify.beansearch

6. **A cloud email service that minimizes the risk of being deplatformed, ideally with domain ownership and strong encryption.**  
   [Ask HN: Is there a cloud-based email service where one cannot be deplaotformed?](https://news.ycombinator.com/item?id=26805374) · 2021-04-14 · 5 pts · 6 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.75 (top-1000)  
   _El OP busca un servicio de correo con cero riesgo de desactivación; los comentarios ofrecen alternativas y mitigaciones, pero ninguno garantiza esa garantía total._
   - 0.75 · sovereign · 2013-08-19 · https://github.com/sovereign/sovereign
   - 0.69 · docker-mailserver · 2016-05-31 · https://github.com/jeboehm/docker-mailserver
   - 0.67 · lemon.email-dApp · 2017-03-24 · https://github.com/DevanaLabs/lemon.email-dApp

7. **A budgeting and cost‑tracking tool for freelance digital projects that shows remaining dollars per project.**  
   [Ask HN: Leaking hours and money. I need a tool to keep digital projects in check](https://news.ycombinator.com/item?id=11532852) · 2016-04-20 · 15 pts · 13 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.76 (top-1000)  
   _El OP pide una herramienta específica de seguimiento de costos y horas; las respuestas ofrecen varias opciones, pero ninguna cubre exactamente su necesidad, solo parciales._
   - 0.76 · erpnext · 2011-06-08 · https://github.com/frappe/erpnext
   - 0.70 · hledger · 2013-04-08 · https://github.com/hledgerorg/hledger
   - 0.64 · Online timesheets and project cost managing and rich 3rd party integrations · 2015-11-12 · http://cronforce.com/

8. **A website that aggregates and tracks newly created programming languages and trends.**  
   [Is there a "distrowatch" like site for programming languages?](https://news.ycombinator.com/item?id=41638263) · 2024-09-24 · 10 pts · 8 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.76 (top-1000)  
   _El OP busca un recurso específico; los comentarios ofrecen varios sitios relacionados pero ninguno cumple exactamente con la descripción._
   - 0.76 · languish · 2020-01-22 · https://github.com/tjpalmer/languish
   - 0.53 · Language Health – Compare programming language health over time · 2017-12-12 · https://www.languagehealth.com
   - 0.48 · Programming Languages Database · 2023-09-06 · https://programminglanguages.co

9. **Open‑source platform for network, timeline and unstructured‑data analysis similar to intelligence‑analyst software.**  
   [Ask HN: Is there an open source equivalent to Palantir?](https://news.ycombinator.com/item?id=13488795) · 2017-01-26 · 159 pts · 45 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.77 (top-1000)  
   _El OP busca una herramienta comparable a Palantir; los comentarios ofrecen varios proyectos parciales (graph DB, visualización, análisis) sin un equivalente completo._
   - 0.77 · marija · 2016-10-13 · https://github.com/dutchcoders/marija
   - 0.74 · Facster.com technology demonstration · 2010-09-22 · https://news.ycombinator.com/item?id=1715461
   - 0.67 · aleph · 2014-08-27 · https://github.com/alephdata/aleph

10. **A service that automatically sends SMS or phone call reminders when an email receives no reply within a set time.**  
   [Ask HN: Is there a service that escalates emails to SMS or Phone call reminders?](https://news.ycombinator.com/item?id=18432459) · 2018-11-12 · 5 pts · 6 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.77 (top-1000)  
   _El OP pide explícitamente una herramienta concreta; los comentarios no mencionan ningún servicio existente y ninguno lo ofrece._
   - 0.77 · Simple Email Reminders · 2017-04-07 · http://remindmebro.com/
   - 0.72 · MsgMe.at - an ultra simple reminder service · 2011-03-30 · http://msgme.at
   - 0.63 · Reminder Hero - Automatic e-mail and text message reminders · 2013-10-05 · http://reminderhero.com

11. **A customizable trading dashboard that aggregates charts, order flow, news, and social feeds in a single interface.**  
   [Any tools for a customizable trading dashboard (charts, order flow, news, etc.)?](https://news.ycombinator.com/item?id=43520743) · 2025-03-30 · 5 pts · 9 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.77 (top-1000)  
   _El OP busca una herramienta específica para unificar fuentes de trading; las respuestas ofrecen solo soluciones parciales o hardware._
   - 0.77 · online_trading_platform · 2019-07-17 · https://github.com/reshinto/online_trading_platform
   - 0.77 · profitmaker · 2018-09-24 · https://github.com/suenot/profitmaker
   - 0.76 · ConvexValue – Financial Analytics Browser · 2024-09-29 · https://convexvalue.com/

12. **A paid cloud music storage service that keeps my uploaded personal tracks intact, without removing them due to licensing or location restrictions.**  
   [Ask HN: Is there a cloud music library that doesn't keep deleting my music?](https://news.ycombinator.com/item?id=33595879) · 2022-11-14 · 92 pts · 123 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.81 (top-1000)  
   _El OP busca un servicio pago que almacene su música sin borrarla; los comentarios no citan ninguno que cumpla eso y solo proponen auto‑hosting o servicios que ya fallaron._
   - 0.81 · Streem.io - Media Center on the Cloud · 2013-02-22 · http://www.streem.io
   - 0.76 · Viberr · 2016-03-28 · https://github.com/buckyroberts/Viberr
   - 0.70 · Cubbit, accessible like Dropbox, secure like your hard drive · 2020-09-09 · https://business.cubbit.io

13. **A decentralized database with append‑only history, signed operations, and conflict resolution handled via social mechanisms rather than complex consensus.**  
   [Ask HN: Is there a descentralized DB with a simple social conflict resolution?](https://news.ycombinator.com/item?id=31414459) · 2022-05-17 · 8 pts · 10 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.81 (top-1000)  
   _El OP busca una herramienta concreta; los comentarios no citan ninguna solución existente que cumpla esos requisitos, sólo críticas y discusiones._
   - 0.81 · scuttlebutt · 2012-07-25 · https://github.com/dominictarr/scuttlebutt
   - 0.73 · ssb-server · 2014-10-28 · https://github.com/ssbc/ssb-server
   - 0.68 · Noms – A new decentralized database based on ideas from Git · 2016-08-02 · https://medium.com/@aboodman/noms-init-98b7f0c3566#.ojb6eaz94

14. **An AI assistant that extracts emails and messages, learns personal style, and drafts replies across multiple platforms.**  
   [Ask HN: Is there a tool to extract ALL emails, learn "me", draft responses](https://news.ycombinator.com/item?id=40096424) · 2024-04-20 · 5 pts · 3 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.81 (top-1000)  
   _El OP busca una herramienta concreta; las respuestas solo ofrecen trabajo a medida o ideas parciales, sin producto existente._
   - 0.81 · inbox-zero · 2023-07-12 · https://github.com/elie222/inbox-zero
   - 0.81 · I’m an introvert, made an app to maintain relationships, added more AI · 2023-06-24 · https://play.google.com/store/apps/details?id=dev.mtc.ga&hl=en_US
   - 0.70 · Ellie – Your GPT-3 email assistant · 2022-12-15 · https://ellieai.com

15. **A diagramming tool for visualizing data lineage and ETL transformation rules with drill‑down navigation.**  
   [Ask HN: Any tool to create diagram for data lineage and ETL rules?](https://news.ycombinator.com/item?id=27258919) · 2021-05-23 · 12 pts · 6 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.82 (top-1000)  
   _El OP pide una herramienta concreta para diagramas de linaje y reglas ETL; los comentarios ofrecen varias opciones que solo cubren parte de la necesidad o carecen de la funcionalidad completa._
   - 0.82 · sqlflow_public · 2019-10-22 · https://github.com/sqlparser/sqlflow_public
   - 0.73 · data-lineage · 2020-03-17 · https://github.com/tokern/data-lineage
   - 0.73 · marquez · 2018-07-05 · https://github.com/MarquezProject/marquez

16. **A voice‑controlled programming system that lets me code conversationally without strain, using deep‑learning speech recognition.**  
   [Ask HN: Is there any work being done in speech-to-code with deep learning?](https://news.ycombinator.com/item?id=23497756) · 2020-06-12 · 172 pts · 61 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.83 (top-1000)  
   _El OP busca una solución de dictado de código más natural; los comentarios citan varias herramientas existentes (Serenade, Talon, Caster, etc.) que cubren parte del problema pero no ofrecen un enfoque totalmente basado en deep learning para generar código._
   - 0.83 · CodeSpeak, the beginnings of a web-based speech-to-code tool · 2019-05-27 · https://github.com/sethwilsonUS/codespeak
   - 0.83 · codespeak · 2019-04-12 · https://github.com/sethwilsonUS/codespeak
   - 0.82 · VimSpeak · 2013-05-05 · https://github.com/AshleyF/VimSpeak

17. **An open‑source platform to collect, discuss, and coordinate climate‑change ideas and solutions.**  
   [Ask HN: Is There Any Interest in an Open Source Solution for Climate Change](https://news.ycombinator.com/item?id=19248518) · 2019-02-25 · 26 pts · 14 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.83 (top-1000)  
   _El OP pide crear una herramienta concreta para gestionar ideas climáticas; los comentarios solo proponen conceptos o proyectos diferentes, sin mencionar una solución existente._
   - 0.83 · your-priorities-app · 2014-08-22 · https://github.com/CitizensFoundation/your-priorities-app
   - 0.82 · plots2 · 2013-06-05 · https://github.com/publiclab/plots2
   - 0.80 · openideal · 2014-02-07 · https://github.com/linnovate/openideal

18. **A browser extension that shades AI‑generated text based on detection confidence, fading it toward the background color.**  
   [Ask HN: Is there a browser plugin that will fade AI generated text to gray?](https://news.ycombinator.com/item?id=36830583) · 2023-07-22 · 7 pts · 12 comentarios · etiqueta **n** (no existe) · mejor P(núcleo) 0.84 (top-1000)  
   _El OP solicita una herramienta concreta (plugin); los comentarios solo hablan de detectores y niegan que exista tal extensión, por lo que se marca como no existente._
   - 0.84 · UserScript to detect GPT generated comments on Hacker News · 2022-12-08 · https://github.com/chryzsh/GPTCommentDetector
   - 0.50 · Is this Chrome extension a useful application of AI? · 2020-08-19 · https://crammer.app/
   - 0.47 · Domai.nr Chrome Extension · 2011-07-20 · https://news.ycombinator.com/item?id=2784741

19. **A tool that automatically generates a GUI from incoming structured data streams (JSON, MessagePack, etc.)**  
   [Ask HN: Is there an automatic GUI builder from structured data?](https://news.ycombinator.com/item?id=27820141) · 2021-07-13 · 5 pts · 6 comentarios · etiqueta **p** (parcial) · mejor P(núcleo) 0.84 (top-1000)  
   _El OP pide una herramienta concreta para crear interfaces a partir de datos estructurados; los comentarios solo ofrecen soluciones parciales o aproximadas._
   - 0.84 · EverLayout · 2017-02-04 · https://github.com/acrocat/EverLayout
   - 0.83 · oui · 2016-02-26 · https://github.com/wearekuva/oui
   - 0.82 · Instantly turn any API into a native app, with a single JSON markup · 2016-06-09 · https://news.ycombinator.com/item?id=11868903

## Descartado (etiqueta e) (44)

| pedido | Ask | etiqueta | mejor | mejor candidato |
|---|---|---|---|---|
| A service that tracks and compares cryptocurrency projects' energy consumption and carbon  | [Ask HN: Is there a tool that tracks cryptocurrency energy me](https://news.ycombinator.com/item?id=26093536) | e | 0.39 | Cryptocurrency Heatmap |
| A tool to view congressional bills in a readable, nicely formatted way (HTML/PDF) with nav | [Ask HN: Any good tools for viewing congressional bills?](https://news.ycombinator.com/item?id=44202110) | e | 0.48 | CLI for generating PDFs for offline reading |
| A real-time crowdsourced service that provides immediate yes/no image classification. | [Ask HN: Is there a realtime mechanical turk service?](https://news.ycombinator.com/item?id=14053666) | e | 0.51 | Instant object recognition |
| A service that manages end‑to‑end product launch, including marketing, PR, and initial cus | [Ask HN: Is there a “product launch as a service” company?](https://news.ycombinator.com/item?id=13963698) | e | 0.53 | Growthdock-Sameday actionable growth, marketing an |
| A service that aggregates multiple SaaS subscriptions into a single consolidated invoice. | [Ask HN: Is there a service that consolidates various SaaS bi](https://news.ycombinator.com/item?id=15085742) | e | 0.53 | Aggregate your bills and expenses – BillerHub |
| Open source seed‑to‑sale software for cannabis businesses. | [Ask HN: Is there any free open source Cannabis seed to sale ](https://news.ycombinator.com/item?id=21032945) | e | 0.53 | pos |
| A modern, well-documented peer-to-peer framework/library for building GUI applications in  | [Ask HN: Can you recommend a modern, accessible P2P framework](https://news.ycombinator.com/item?id=18511911) | e | 0.56 | cedar |
| A web app for manually entering blood test results, visualizing trends, comparing to refer | [Ask HN: Is there a webapp to input/store your blood test res](https://news.ycombinator.com/item?id=36025977) | e | 0.60 | Glimpse |
| A solar panel comparison tool listing specs such as wattage, dimensions, price, technology | [Ask HN: Is there a comprehensive solar panel comparison tool](https://news.ycombinator.com/item?id=17778531) | e | 0.60 | Cluelet – Your notebook for objective and visual c |
| A benchmarking tool that measures Linux desktop scheduling and input latency to quantify s | [Ask HN: Is there any tool for benchmarking responsiveness fo](https://news.ycombinator.com/item?id=30209366) | e | 0.61 | lmbench |
| A constraint‑solver based framework to specify register‑level rules and automatically gene | [Is there a language/framework can describe a model and gener](https://news.ycombinator.com/item?id=31954611) | e | 0.63 | protoc-gen-validate |
| A minimal Linux distribution that boots straight into a DAW for live music performance, wi | [Ask HN: Is there any Linux distro dedicated to music perform](https://news.ycombinator.com/item?id=31549303) | e | 0.65 | elk-pi |
| A gamification service that tracks GitHub activity with daily/weekly quests and achievemen | [Ask HN: Is there any GitHub based/supporting gamification se](https://news.ycombinator.com/item?id=13490297) | e | 0.65 | Earn achievements while using GitHub |
| A free integration service to capture Facebook and TikTok lead form data and forward it to | [Ask HN: Is there a free Zapier that works with Facebook Lead](https://news.ycombinator.com/item?id=30492354) | e | 0.65 | Leadngin.com finally launched my startup after 18m |
| A service that returns hostnames and their page URLs with HTML from Common Crawl via an AP | [Ask HN: Is there a service that offers Common Crawl as an AP](https://news.ycombinator.com/item?id=43942956) | e | 0.65 | WWW search powered by OSS and common data |
| A tool that analyzes a website’s CSS and provides breakdowns of specificity, unused rules, | [Ask HN: Is there any tool for testing a site's CSS specifici](https://news.ycombinator.com/item?id=12488842) | e | 0.68 | core |
| A tool that visualizes long email chains as diagrams or graphs to clarify participants and | [Ask HN: Are there any tools to diagram long email chains?](https://news.ycombinator.com/item?id=29840119) | e | 0.72 | InboxGraph – Constructing directed graphs of email |
| Software that automatically assesses spoken English proficiency, evaluating pronunciation, | [Ask HN: Is there any software capable of testing your spoken](https://news.ycombinator.com/item?id=30175830) | e | 0.72 | gopt |
| A programming language that supports high-level system design concepts for large-scale sof | [Ask HN: Are there any languages for programming-in-the-large](https://news.ycombinator.com/item?id=32536886) | e | 0.73 | neva |
| A tool that clusters or groups notes by similarity, ingesting content from note‑taking app | [Ask HN: Any tools to easily cluster ideas/notes by similarit](https://news.ycombinator.com/item?id=14733562) | e | 0.74 | keeeb - social bookmarking reinvented |
| A lightweight operating system with minimal UI and no animations, focused on fast app laun | [Ask HN: Are there any lean operating systems left?](https://news.ycombinator.com/item?id=36721743) | e | 0.74 | kolibrios |
| A forum platform for unrestricted political discussion without phone‑verification requirem | [Is there a place on the internet that is appropriate for tal](https://news.ycombinator.com/item?id=44719317) | e | 0.76 | Do you have a controversial opinion? Well Prove it |
| A captcha service that offers intentionally very hard challenge‑response puzzles to block  | [Ask HN: Is there a captcha service that is intentionally har](https://news.ycombinator.com/item?id=16179289) | e | 0.77 | testcookie-nginx-module |
| A documentation tool for software architects to create, maintain, and sync architecture di | [Ask HN: Is there a better way to document complex software a](https://news.ycombinator.com/item?id=18508284) | e | 0.78 | Ardoq.com – developer friendly documentation tool  |
| A functional programming language that compiles quickly to a single binary, runs fast, and | [Ask HN: Is there a functional programming language with the ](https://news.ycombinator.com/item?id=29971945) | e | 0.79 | yona |
| A SaaS that syncs third‑party application data directly into your own database. | [Ask HN: Are there any SaaS services that access your databas](https://news.ycombinator.com/item?id=9390972) | e | 0.79 | cenit |
| A library of tiny monochrome bitmap fonts and graphics for ultra‑low‑resolution (e.g., 20× | [Ask HN: Are there any standard monochrome low resolution res](https://news.ycombinator.com/item?id=26934352) | e | 0.80 | raster-fonts |
| A personal finance manager that properly classifies spending, investments, and account tra | [Ask HN: Is there a better way to manage assets and transacti](https://news.ycombinator.com/item?id=10473925) | e | 0.80 | firefly-iii |
| An AI service that takes a list of URLs on the same topic and generates a unified summary  | [Ask HN: Is there an AI service to interpret a collection of ](https://news.ycombinator.com/item?id=33869332) | e | 0.80 | Trimmed News – Read Summarized News Created by a M |
| A platform for remote developers to discover and meet up with other developers, locally or | [Ask HN: Is there a platform for remote devs to meetup?](https://news.ycombinator.com/item?id=13588495) | e | 0.80 | codebuddies |
| A high-level library that can generate terminal user interfaces from a config file or with | [Ask HN: Are there any high-level TUI tools?](https://news.ycombinator.com/item?id=31596561) | e | 0.80 | pytermgui |
| A video archiving service that caches video links for permanent, no‑ads access. | [Ask HN: Is there an archive of videos like archive.today?](https://news.ycombinator.com/item?id=37959678) | e | 0.80 | Watch/Download/Organize Public Video URLs |
| A SaaS service for monitoring container resource utilization across multiple container eng | [Ask HN: Is there a good tool for container resource monitori](https://news.ycombinator.com/item?id=15090421) | e | 0.80 | scope |
| A paid service that reviews and gives feedback on engineering manager resumes. | [Ask HN: Is there a service to get your engineering resume re](https://news.ycombinator.com/item?id=15560766) | e | 0.81 | Professional profile management tool built using R |
| A platform to post small software ideas, receive feedback and find collaborators without c | [Ask HN: Is there a platform for sharing ideas that people wa](https://news.ycombinator.com/item?id=21991260) | e | 0.82 | ToBuildSomething – Find side project collaborators |
| A free cross‑platform desktop GUI framework for building commercial applications without d | [Ask HN: What software do I use to create a commercial deskto](https://news.ycombinator.com/item?id=27073394) | e | 0.82 | yue |
| A tool that imports the accounts you follow on Twitter into Mastodon by matching their Mas | [Ask HN: Is there a tool to follow all the people I follow in](https://news.ycombinator.com/item?id=33663134) | e | 0.82 | fedifinder |
| A UI tool to query and search AWS CloudWatch logs. | [Ask HN: Is there an alternative CloudWatch UI?](https://news.ycombinator.com/item?id=33286260) | e | 0.83 | apilogs |
| A tool that displays C++ template instantiation and substitution results prior to compilat | [Ask HN: Any tool to look C++ interpretation template form sy](https://news.ycombinator.com/item?id=32969667) | e | 0.83 | cppinsights |
| An open‑source, developer‑friendly calendar platform with full‑featured UI, extensibility  | [Ask HN: Is there a powerful open-source Google Calendar repl](https://news.ycombinator.com/item?id=14008085) | e | 0.84 | calagator |
| A text‑based tool to generate timeline diagrams from plain text. | [Ask HN: Is there a text-based tool to create a timeline diag](https://news.ycombinator.com/item?id=26935278) | e | 0.84 | mdline |
| A markup language or schema to define forms once and generate/render them across back‑end  | [Ask HN: Is there a markup language for forms?](https://news.ycombinator.com/item?id=21963056) | e | 0.84 | supler |
| A consumer VoIP service (SIP or similar) accessible via tablet, phone and desktop apps, re | [Ask HN: Is there a better VoIP provider than Skype?](https://news.ycombinator.com/item?id=40800423) | e | 0.84 | How to use a phone without a carrier contract |
| An AI-powered code-to-speech tool that reads source code with syntax-aware emphasis and ex | [Ask HN: Is there an AI that can read code aloud and explain ](https://news.ycombinator.com/item?id=44893785) | e | 0.84 | I built Explain-o-matic – AI voice guide for LLM c |

## No es software (44)

| pedido | Ask | etiqueta | mejor | motivo |
|---|---|---|---|---|
| A collar-mounted sensor system (accelerometer/gyroscope/heart‑rate) that detects feline se | [Ask HN: Is there a way to get notified when my cat has seizu](https://news.ycombinator.com/item?id=40939333) | p | 0.37 | hardware |
| A method to programmatically generate Siri Shortcuts on iOS without using the drag‑and‑dro | [Ask HN: Any way to program Siri Shortcuts in iOS 12 besides ](https://news.ycombinator.com/item?id=18025254) | e | 0.38 | se puede |
| An app that covertly records ambient conversation and serves targeted ads based on spoken  | [Ask HN: Is there any way an app can listen conversations sec](https://news.ycombinator.com/item?id=18071861) | p | 0.38 | se puede |
| Access to historical dark‑pool trading data for individual traders. | [Ask HN: HN Any way for individual to gain access to Dark Poo](https://news.ycombinator.com/item?id=23250611) | n | 0.41 | se puede |
| A bootcamp or course teaching developers basic legal compliance, contracts, and privacy fu | [Ask HN: Is there a “law/legal” bootcamp for developers?](https://news.ycombinator.com/item?id=28304105) | n | 0.43 | contenido |
| A service that aggregates and lets you view, rename, merge, and delete all of your online  | [Ask HN: What tool would you buy to make your life easier?](https://news.ycombinator.com/item?id=31303358) | n | 0.47 | encuesta |
| A programming learning environment usable via voice dictation and screen‑reader, without n | [Ask HN: I can barely read, is there a way I could still lear](https://news.ycombinator.com/item?id=9374306) | e | 0.48 | se puede |
| An e‑ink ebook reader that runs a Linux‑based OS and provides a terminal for coding while  | [Is there any eReader with a terminal?](https://news.ycombinator.com/item?id=32118727) | e | 0.50 | hardware |
| A programmable feature phone with an open OS that lets you write and run custom apps while | [Ask HN: Are there any programmable 'feature' phones?](https://news.ycombinator.com/item?id=15565877) | e | 0.55 | hardware |
| A practical guide that compares databases and their trade‑offs to help choose the right on | [Ask HN: Is there a resource to help choose the right DB for ](https://news.ycombinator.com/item?id=25911870) | e | 0.56 | contenido |
| A requirements‑management and WBS tool with itemized tracking, built‑in versioning and tra | [Ask HN: What software do you use to gather requirements?](https://news.ycombinator.com/item?id=27615562) | e | 0.57 | encuesta |
| Open source small‑scale farming robot platform for tasks such as weeding, seeding, and fer | [Ask HN: Does anyone know of an open source Farming robot, pr](https://news.ycombinator.com/item?id=41152824) | e | 0.58 | hardware |
| A platform for responsibly disclosing security vulnerabilities in open‑source projects, wi | [Ask HN: How do you responsibly report security bugs to open-](https://news.ycombinator.com/item?id=21920142) | p | 0.59 | encuesta |
| A service that manages Excel file upload, validation, parsing and export, handling large f | [Ask HN: How do you handle Excel import/exports in your apps](https://news.ycombinator.com/item?id=19495662) | e | 0.64 | encuesta |
| A curated list of open‑source iOS apps free of trackers and anti‑features, similar to F‑Dr | [Ask HN: Is There an F-Droid for iOS?](https://news.ycombinator.com/item?id=27560347) | p | 0.64 | contenido |
| A GDPR‑compliant privacy statement template for small self‑hosted blogs. | [Ask HN: Is there a GDPR compliance privacy statement templat](https://news.ycombinator.com/item?id=33113283) | n | 0.66 | contenido |
| A web UI prototyping tool that lets you quickly create mockups and generate placeholder da | [Ask HN: What tools do you use to prototype web UI?](https://news.ycombinator.com/item?id=12843440) | e | 0.68 | encuesta |
| A hackable fitness wristband with GPS, heart‑rate monitor and pedometer that lets you expo | [Ask HN: Is there a fitness wristband that is hackable?](https://news.ycombinator.com/item?id=15823597) | e | 0.69 | hardware |
| A tool that aggregates and offers advanced search across Meetup and Eventbrite events. | [Ask HN: What tools do you use to search for Meetups?](https://news.ycombinator.com/item?id=15351116) | e | 0.69 | encuesta |
| A list of command-line tools that embed telemetry/analytics and the environment variables  | [Ask HN: Is there a reference of CLI tools with analytics?](https://news.ycombinator.com/item?id=32762863) | p | 0.69 | contenido |
| A collaborative web‑based technical documentation platform with diagramming, version‑contr | [Ask HN: What tools do you use to write techinal documents](https://news.ycombinator.com/item?id=26302253) | e | 0.71 | encuesta |
| A hobbyist robotics stack of modular hardware and software tools that lets users focus on  | [Is there an existing “Stack” for getting into robotics?](https://news.ycombinator.com/item?id=11883293) | e | 0.73 | hardware |
| A lightweight Linux tool for quickly adding calendar events with a single keyboard shortcu | [Ask HN: How do you quickly add calendar events in Linux?](https://news.ycombinator.com/item?id=29307245) | p | 0.74 | encuesta |
| A hackable smartwatch with GPS, cellular/data connectivity and audio recording capability. | [Ask HN: Is there a good hackable smart watch?](https://news.ycombinator.com/item?id=42001650) | n | 0.74 | hardware |
| A book that explains large language models for experienced developers, balancing depth and | [Ask HN: Is there a great book for understanding LLMs?](https://news.ycombinator.com/item?id=38879188) | e | 0.75 | contenido |
| A way to prevent animated Google Doodles from playing when opening a new tab in Chrome. | [Ask HN: Is there a way to stop the animated Google Doodles?](https://news.ycombinator.com/item?id=48587539) | e | 0.76 | se puede |
| Assistive screen‑reading tools for blind programmers to develop software. | [Ask HN: Are any of you blind programmers and what tools do y](https://news.ycombinator.com/item?id=8893728) | e | 0.76 | encuesta |
| A heart rate monitor device that records data locally and can be downloaded to a computer  | [Ask HN: Is there a no-nonsense device that lets me measure m](https://news.ycombinator.com/item?id=21797092) | e | 0.76 | hardware |
| A tool to create visually appealing, high‑level public roadmap presentations from GitHub/G | [Ask HN: What tools do you use to create project's public roa](https://news.ycombinator.com/item?id=30117559) | p | 0.77 | encuesta |
| A FOSS license that prohibits large language models from scanning or training on the repos | [Ask HN: Is there a MIT-like FOSS license that prevents LLMs ](https://news.ycombinator.com/item?id=38142722) | n | 0.78 | contenido |
| Offline backup solution for Android app data and device state without requiring root. | [Ask HN: How do you back up your Android phone?](https://news.ycombinator.com/item?id=29213246) | p | 0.80 | encuesta |
| A tool to automate provisioning and verification of single‑tenant SaaS deployments. | [Ask HN: As a SaaS company, how do you manage your single-ten](https://news.ycombinator.com/item?id=34620594) | p | 0.80 | encuesta |
| A way to expose a friend’s M1 GPU over the network as an API for running AI models without | [Ask HN: Any way to borrow compute from Apple M1](https://news.ycombinator.com/item?id=40952294) | e | 0.81 | se puede |
| A tool that simulates and measures how AI agents choose between competing APIs or services | [Ask HN: How do you know if AI agents will choose your tool?](https://news.ycombinator.com/item?id=47127532) | n | 0.81 | encuesta |
| A system to serve and update static marketing and legal pages alongside a dynamic SaaS app | [Ask HN: How do you manage “static” pages on your micro SaaS ](https://news.ycombinator.com/item?id=31547285) | e | 0.81 | encuesta |
| An app that recommends books based on a user's favorite authors using collaborative filter | [Ask HN: What app do you use for book recommendations?](https://news.ycombinator.com/item?id=37531580) | e | 0.81 | encuesta |
| A security auditing solution for external software that can identify and assess npm packag | [Ask HN: How do you security-audit external software using NP](https://news.ycombinator.com/item?id=29078836) | e | 0.82 | encuesta |
| An intermediate programming course or book that bypasses basics and teaches deeper problem | [Ask HN: Are there any good intermediate level programming co](https://news.ycombinator.com/item?id=15433955) | e | 0.82 | contenido |
| A tool to create diagrams of micro‑service architectures, showing services, connections an | [Ask HN: What tools do you use to diagram micro-service archi](https://news.ycombinator.com/item?id=11238113) | e | 0.82 | encuesta |
| A tool to automatically limit and enforce kids' screen time on tablets, locking the device | [Ask HN: Do you use any apps or tools to limit your kids' scr](https://news.ycombinator.com/item?id=37057747) | p | 0.83 | encuesta |
| A cross‑language project scaffolding tool that sets up code, configuration, documentation, | [Ask HN: How do you bootstrap your software projects?](https://news.ycombinator.com/item?id=38545961) | e | 0.83 | encuesta |
| A method to perform OAuth/OIDC authentication for dynamically created short‑lived preview  | [Ask HN: How do you handle auth when AI dev agents spin up sh](https://news.ycombinator.com/item?id=46846055) | e | 0.83 | se puede |
| A lightweight platform for quickly building and testing product or app ideas with minimal  | [Ask HN: How do you quickly test out new product/app ideas?](https://news.ycombinator.com/item?id=16297262) | p | 0.84 | encuesta |
| A method for distributing short‑term activation codes for an app without user accounts, ea | [Ask HN: Is there a good alternative to software registration](https://news.ycombinator.com/item?id=18198546) | p | 0.84 | se puede |

