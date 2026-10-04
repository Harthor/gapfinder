# Candidatos a casos reales (absences de Constellate)

Evidencia: búsqueda web y search API de GitHub (no el retrieval de gapfinder).
Por cada idea: marcá `confirmado: sí` o `confirmado: no`, y dejá en `esperado:` las URLs que
cuentan como "lo que ya existía" (separadas por espacios; podés editar la lista propuesta).
Solo las URLs marcadas ✓ están hoy en el corpus: un caso sin ninguna ✓ mide cobertura del
corpus, no retrieval.

## 1 · 6f3848c8 · Missing: Runtime Governance for Commercial Agent Teams

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-6f3848c8.md`
- Idea: 3599 argues human-in-the-loop is theater, 3600 offers a toy deterministic safety gate, 1348 formalizes coalition dynamics, while 3467 and 750 sell agent teams handling real money and professional work. The gap is glaring: there is no production-grade policy engine that sits between multi-agent decisions and execution—programmable permissions, spend limits, audit trails, and escalation logic for agent teams. Everyone shipping commercial agents needs it; the only artifact here is a no-deps Python 
- Match (mi evaluación): **fuerte (no específico de "teams" comerciales)**
- Web (curado):
  - Microsoft Agent Governance Toolkit (MIT, abr-2026): policy engine, budgets/spend limits, audit trail, escalation para agentes -> https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/ [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/permguard/permguard ★68 · push 2026-09-22 — Permguard is the authorization engine for both worlds: enforce policies on today's systems, enforce continuity on tomorrow's. One engine for governance, AI agents, and distributed execution. [✗ fuera del corpus]
  - https://github.com/jnamaya/SAFi ★58 · push 2026-09-19 —  SAFi is an open source governance engine for AI agents that enforces your policies, governs agent actions, and records every decision for audit. [✗ fuera del corpus]
  - https://github.com/jeremylongshore/claude-code-slack-channel ★39 · push 2026-09-14 — Slack-native governance substrate for Claude Code and peer agents: every tool call passes a tiered policy engine and lands in a hash-chained, Ed25519-signed audit journal you can verify offline. The g [✗ fuera del corpus]
  - https://github.com/vectimus/vectimus ★38 · push 2026-09-01 — Deterministic governance for AI coding agents. Cedar-based policy engine that intercepts every agent action and evaluates it against deterministic rules before execution. [✓ en corpus (show_hn:47525283)]
  - https://github.com/rajfirke/provena ★17 · push 2026-09-22 — Context governance for agentic AI — tamper-evident audit trails, provenance validation, EU AI Act compliance. 6 framework adapters, MCP server, PostgreSQL, policy engine. [✓ en corpus (show_hn:48984491)]
- Prior art que había encontrado Constellate: SteerPlane https://github.com/systempromptio/awesome-ai-agent-governance; Cycles (runcycles.io) https://runcycles.io/blog/ai-agent-governance-runtime-enforcement-security-cost-compliance; Prefactor https://prefactor.tech/learn/what-is-runtime-enforcement; Guild (Authorization + Governance Layer) https://www.guild.ai/blog/agent-governance/your-authorization-platform-doesnt-govern-your-age

esperado: https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/
confirmado: 

---

## 2 · e1cc171a · Agents Get Credit Cards Before They Get Credit Scores

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-e1cc171a.md`
- Idea: Agents can now spend real money, install unverified skills that may not even exist, inherit unsafe behaviors invisibly through distillation, and we can benchmark their trajectories after the fact or gate them with static guardrails. What's missing is the middle layer: a runtime identity, reputation, and attestation system that scores an agent's trustworthiness before it acts—the equivalent of a credit score plus signed provenance for skills and behaviors. The pieces define the gap precisely: mon
- Match (mi evaluación): **parcial (estándar/servicios, no un producto único)**
- Web (curado):
  - IETF draft-sharif-agent-payment-trust (trust score 0-100 + límites por nivel) https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/ [✗ fuera del corpus]
  - spend controls en el rail de pago (Meow) https://www.meow.com/blog/spend-controls-ai-agents-caps-mcc-locks-approval-ladders [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/HwangTaehyun/oh-my-agentic-score ★27 · push 2026-03-07 — Oh My Agentic Score (OMAS) — Measure and visualize AI agent thread-based engineering capabilities. 4-dimension scoring: More (Parallelism), Longer (Autonomy), Thicker (Density), Fewer (Trust). [✗ fuera del corpus]
  - https://github.com/up2itnow0822/agent-wallet-sdk ★13 · push 2026-09-22 — Non-custodial crypto wallets for AI agents with on-chain spending limits. ERC-6551, x402 compatible, Base Mainnet. [✗ fuera del corpus]
  - https://github.com/arome3/tempo-mcp ★8 · push 2025-12-28 — MCP server enabling AI agents to execute autonomous stablecoin payments on Tempo blockchain. Supports single/batch payments, scheduled transfers, token swaps, and balance queries with built-in spendin [✗ fuera del corpus]
  - https://github.com/agentnameservice/agent-trust-discovery ★7 · push 2026-09-21 — Go reference implementation of the Agent Trust Discovery — indexes registered AI agents and serves explainable, five-dimension trust scores (integrity, identity, solvency, behavior, safety) through a  [✗ fuera del corpus]
  - https://github.com/DelegoLabs/Delego ★6 · push 2026-09-22 — Delego is an AI-powered commerce platform built on Stellar and Soroban that enables users to delegate purchasing tasks to intelligent agents through secure wallets, escrow, and permissioned payments w [✗ fuera del corpus]
- Prior art que había encontrado Constellate: ERC-8004 (Trustless Agents) https://eips.ethereum.org/EIPS/eip-8004; JFrog Agent Skills Registry (part of JFrog AI Catalog) https://jfrog.com/ai-catalog/skills-registry/; Super Agent Skill https://superagentskill.com/; Tessl Registry with Snyk security scoring https://snyk.io/blog/snyk-tessl-partnership/

esperado: https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/ https://www.meow.com/blog/spend-controls-ai-agents-caps-mcc-locks-approval-ladders
confirmado: 

---

## 3 · 197bf4f9 · Missing: The Glue Layer for Self-Hosters

- Constellate: 2026-07-16 · veredicto yes; prior-art manual en `prior-art/absence-197bf4f9.md`
- Idea: This neighborhood is dense with self-hosted apps (identity, marketing, finance, assets, media) but contains nothing that unifies them: no orchestration, SSO wiring, backup, or cross-app dashboard tool. Keycloak exists precisely because each of these apps has its own login, yet integrating it into each one is a manual chore. The missing piece is an opinionated 'self-hosted stack composer' that deploys these apps pre-wired with shared auth, backups, and monitoring — the Vercel of homelab back-offi
- Match (mi evaluación): **fuerte**
- Web (curado):
  - YunoHost (SSO entre apps, backups) https://github.com/YunoHost/yunohost [✓ en corpus (github:yunohost/yunohost)]
  - Cloudron (deploy, updates, backups, SSO) https://www.cloudron.io [✗ fuera del corpus]
  - Sandstorm, 1Panel
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/fosrl/pangolin ★22880 · push 2026-09-23 — Modern networking and security platform providing secure access and connectivity to apps, infrastructure, and AI workloads. Connect and protect your users. [✓ en corpus (github:fosrl/pangolin)]
  - https://github.com/BansheeTech/HomeDockOS ★915 · push 2026-08-24 — An intuitive, versatile, and powerful home server operating system for self-hosting. Featuring a curated app store and seamless multi-platform support, it’s designed to empower your personal cloud on  [✓ en corpus (github:bansheetech/homedockos)]
  - https://github.com/Peon-sh/Peon ★94 · push 2026-09-22 — Open-source, self-hostable deployment platform. Deploy Git apps, Docker Compose, databases, and static sites to your own servers, the open alternative to Vercel/Heroku. [✗ fuera del corpus]
  - https://github.com/vimalinx/Vimagram ★25 · push 2026-02-23 — Vimagram is a private server solution for openclaw (Clawdbot)(moltbot)(maybe others(? , enabling bots and mobile apps to communicate through self-hosted servers instead of centralized platforms. [✗ fuera del corpus]
  - https://github.com/unveroleone/save-sync ★19 · push 2026-08-19 — Save sync for modded handhelds. Self-hosted server, Rust client, cross-platform desktop app. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Cloudron https://www.cloudron.io/; YunoHost https://yunohost.org/; Cosmos Cloud https://cosmos-cloud.io/; Runtipi https://runtipi.io/

esperado: https://github.com/YunoHost/yunohost https://www.cloudron.io
confirmado: 

---

## 4 · 01fe2dbe · Missing: Zero-Knowledge Self-Hosted Messaging

- Constellate: 2026-07-16 · veredicto yes; prior-art manual en `prior-art/absence-01fe2dbe.md`
- Idea: The neighborhood covers self-hosted networking (Headscale), encrypted storage (Cryptomator), zero-knowledge sharing (PrivateBin), and open email (Thunderbird) — every pillar of a sovereign personal stack except real-time messaging. The privacy stack here handles data at rest and data shared asynchronously, but the highest-value channel, chat, is only represented by WeChat hacks that stay inside a closed platform. The logically implied missing piece is a Headscale-style self-hosted, E2E messaging
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Matrix/Synapse+Element (E2EE, self-hosted) https://github.com/element-hq/synapse [✓ en corpus (github:element-hq/synapse)]
  - Rocket.Chat E2E
  - chatalot (Signal protocol, self-hosted) https://github.com/purpleneutral/chatalot [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/giovantenne/lastsignal ★751 · push 2026-09-16 — A self-hosted dead man's switch for delivering encrypted messages (E2EE) to your loved ones — when you're gone or unresponsive. [✓ en corpus (github:giovantenne/lastsignal)]
  - https://github.com/aozorae/Edgechat ★722 · push 2026-09-20 — A modern, self-hosted team chat built on Cloudflare — realtime messaging, Telegram bridge, encrypted messages & files, and WebMCP. | 基于 Cloudflare 的现代自部署团队聊天系统：实时通信、Telegram 双向桥接、消息与文件加密，以及 WebMCP。 [✓ en corpus (github:aozorae/edgechat)]
  - https://github.com/anondotli/awesome-privacy-tools ★72 · push 2026-08-29 — Awesome privacy tools: encrypted messaging, anonymous email, VPNs, Tor, password managers, secure file sharing, browser privacy, and self-hosted privacy software. [✗ fuera del corpus]
  - https://github.com/shawnbure/elm-chat ★66 · push 2026-09-20 — Open-source, account-free, end-to-end encrypted chat rooms that self-destruct, with single-use invites and no persisted server-side transcript. [✗ fuera del corpus]
  - https://github.com/Scribblerockerz/cryptletter ★42 · push 2026-01-31 — Self-hosted micro-service for encrypted self-destructing messages [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Matrix / Synapse https://matrix.org/; SimpleX Chat https://simplex.chat/; Rocket.Chat https://www.rocket.chat/; Mattermost https://mattermost.com/

esperado: https://github.com/element-hq/synapse https://github.com/purpleneutral/chatalot
confirmado: 

---

## 5 · a6c38804 · Everyone Builds Agents, Nobody Watches Them

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-a6c38804.md`
- Idea: This neighborhood has self-evolving agents, agents that bypass site blocks, agents reading financial markets (4), plus mature observability and orchestration — but only for infrastructure, not for agents. The missing piece is an agent-native observability and governance layer: tracing what autonomous agents did on the web, what they mutated in their own genome, and kill-switches when behavior drifts. Every ingredient for runaway agents exists here; the monitoring plane for them does not. That ga
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Langfuse https://github.com/langfuse/langfuse [✓ en corpus (github:langfuse/langfuse)]
  - OpenLLMetry https://github.com/traceloop/openllmetry [✓ en corpus (github:traceloop/openllmetry)]
  - MLflow tracing
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/langfuse/langfuse ★34952 · push 2026-09-23 — 🪢 Open source agent evals & observability: Trace, evaluate, and improve LLM applications with one open platform. [✓ en corpus (github:langfuse/langfuse)]
  - https://github.com/comet-ml/opik ★22201 · push 2026-09-23 — Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards. [✓ en corpus (github:comet-ml/opik)]
  - https://github.com/raga-ai-hub/RagaAI-Catalyst ★16164 · push 2026-02-11 — Python SDK for Agent AI Observability, Monitoring and Evaluation Framework. Includes features like agent, llm and tools tracing, debugging multi-agentic system, self-hosted dashboard and advanced anal [✓ en corpus (github:raga-ai-hub/ragaai-catalyst)]
  - https://github.com/pinpoint-apm/pinpoint ★13872 · push 2026-09-23 — APM, (Application Performance Management) tool for large-scale distributed systems.  [✓ en corpus (github:pinpoint-apm/pinpoint)]
  - https://github.com/latitude-dev/latitude-llm ★4669 · push 2026-09-23 — Open-source observability for AI agents. Find where your agents fail, dispatch your coding agent to fix it, and verify the fix against real traces. [✓ en corpus (github:latitude-dev/latitude-llm)]
- Prior art que había encontrado Constellate: Galileo (Agent Observability & Guardrails Platform) https://galileo.ai/blog/best-ai-agent-observability-platforms; theaios-agent-monitor https://medium.com/@Cohorte-AI/your-ai-agent-needs-a-kill-switch-heres-how-to-build-one-b1b69a053a25; AgentGuard https://bmdpat.com/blog/ai-agent-needs-kill-switch; Datadog Agent Observability https://www.datadoghq.com/products/ai/agent-observability/

esperado: https://github.com/langfuse/langfuse https://github.com/traceloop/openllmetry
confirmado: 

---

## 6 · 81981bec · Everyone builds cloners and detectors; nobody builds provenance

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-81981bec.md`
- Idea: The neighborhood is dense with generation power — tokenizer-free cloning (6), expressive open TTS families, training-free speech editing — and with reactive forensics that admit they're losing (3138 documents a temporal generalization gap, 2894 retreats to interpretable classical methods). The structurally missing piece is generation-side provenance: robust audio watermarking and signed voice-consent infrastructure baked into these open TTS stacks. Detection-only defense is provably brittle agai
- Match (mi evaluación): **fuerte**
- Web (curado):
  - AudioSeal (Meta, watermark localizado de voz sintética) https://github.com/facebookresearch/audioseal [✓ en corpus (github:facebookresearch/audioseal)]
  - Chatterbox con watermark PerTh
  - Respeecher + C2PA https://contentauthenticity.org/blog/community-story-respeecher [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/facebookresearch/audioseal ★789 · push 2026-05-19 — Localized watermarking for AI-generated speech audios, with SOTA on robustness and very fast detector [✓ en corpus (github:facebookresearch/audioseal)]
  - https://github.com/pawel-kaczmarek/The-A-Files ★28 · push 2026-09-22 — Implementations of audio watermarking methods, speech quality metrics and attacks in different domains. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Resemble AI PerTh watermarking in Chatterbox Turbo (open-source TTS) https://www.resemble.ai/learn/models/chatterbox-turbo; Google DeepMind SynthID (audio) https://elevenlabs.io/blog/synthid; AudioSeal / WavMark / TimbreWatermarking (academic watermarking schemes) https://sokaudiowm.github.io/; C2PA (Coalition for Content Provenance and Authenticity) https://github.com/and-mill/Awesome-GenAI-Watermarking

esperado: https://github.com/facebookresearch/audioseal https://contentauthenticity.org/blog/community-story-respeecher
confirmado: 

---

## 7 · 25a4c842 · Missing: Diffusion Serving Infrastructure, Not Just LLM Serving

- Constellate: 2026-07-16 · veredicto yes; prior-art manual en `prior-art/absence-25a4c842.md`
- Idea: The neighborhood contains mature LLM inference infrastructure (TPU kernels, MoE mapping, token-phase optimization, edge benchmarks like 3259) and a growing wave of production-bound diffusion applications (climate 1633, medical 2518, time series 2955), with only a hobbyist C++ port bridging them. What's structurally absent is serious serving-systems work for diffusion workloads: batching across denoising steps, caching, hardware-aware schedulers—the vLLM equivalent for diffusion. The internal str
- Match (mi evaluación): **fuerte**
- Web (curado):
  - OneDiffusion (BentoML, servir cualquier modelo de difusión en producción) https://www.bentoml.com/blog/introducing-onediffusion-run-any-diffusion-model-anywhere [✗ fuera del corpus]
  - ComfyUI como backend
  - SwiftDiffusion (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/sgl-project/sglang ★36351 · push 2026-09-23 — SGLang is a high-performance serving framework for large language models and multimodal models. [✓ en corpus (github:sgl-project/sglang)]
  - https://github.com/vitoplantamura/OnnxStream ★2088 · push 2026-06-18 — Lightweight inference library for ONNX files, written in C++. It can run Stable Diffusion XL 1.0 on a RPI Zero 2 (or in 298MB of RAM) but also Mistral 7B on desktops and servers. ARM, x86, WASM, RISC- [✓ en corpus (github:vitoplantamura/onnxstream)]
  - https://github.com/ardanlabs/kronk ★817 · push 2026-09-22 — Go With Your Own Intelligence! Use Go for hardware accelerated local inference with llama.cpp, whisper.cpp, and stable-diffusion.cpp directly integrated into your Go applications. Kronk provides a hig [✓ en corpus (github:ardanlabs/kronk)]
  - https://github.com/gracezhao1997/Awesome-Video-World-Models-with-AR-Diffusion ★710 · push 2026-09-22 — A Curated List of Awesome Video World Models with AR Diffusion: Covering Algorithms, Applications, and Infrastructure, Aimed at Serving as a Comprehensive Resource for Researchers, Practitioners, and  [✓ en corpus (github:gracezhao1997/awesome-video-world-models-with-ar-diffusion)]
  - https://github.com/mstar-project/mstar ★89 · push 2026-09-23 — A high-performance, universal serving framework for any-to-any models.  [✗ fuera del corpus]
- Prior art que había encontrado Constellate: vLLM-Omni https://github.com/vllm-project/vllm-omni; xDiT https://github.com/xdit-project/xdit; NIRVANA (Adobe, NSDI '24) https://www.usenix.org/conference/nsdi24/presentation/agarwal-shubham; NVIDIA Triton — Stable Diffusion deployment https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/tutorials/Popular_Models_Guide/StableDiffusion/README.html

esperado: https://www.bentoml.com/blog/introducing-onediffusion-run-any-diffusion-model-anywhere
confirmado: 

---

## 8 · 75b40b56 · Missing: A Metric-Trustworthiness Auditor for Practitioners

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-75b40b56.md`
- Idea: Four ideas diagnose that metrics deceive—prompt-optimization gains are noise, proxies fail per-segment, reliability is nonuniform, and competing measurement scores yield divergent conclusions—yet each offers only a bespoke academic framework. The missing piece is a general-purpose tool that takes any evaluation pipeline and reports where its metrics are directionally unreliable: per-segment sign flips, run-to-run variance versus claimed effect, and stratum-level confidence. The neighborhood has 
- Match (mi evaluación): **débil (no hay un auditor de confiabilidad de métricas para practitioners)**
- Web (curado):
  - BenchBrowser (paper, auditar validez de benchmarks) https://arxiv.org/pdf/2603.18019 [✗ fuera del corpus]
  - toolkits de fairness por subgrupo (catálogo OECD)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/hj-n/steadiness-cohesiveness ★27 · push 2023-04-30 — Quality Metrics for evaluating the inter-cluster reliability of Multidimensional Projections [✗ fuera del corpus]
  - https://github.com/isle-dev/MetricEval ★12 · push 2023-11-06 — MetricEval: A framework that conceptualizes and operationalizes four main components of metric evaluation, in terms of reliability and validity [✗ fuera del corpus]
  - https://github.com/Anirudh2141-DS/LLM-Reliability-Evaluation-and-Council-Chat ★7 · push 2026-03-23 — Reproducible evaluation and governance framework for RAG-LLM systems. Runs controlled experiments across retrieval, context construction, and generation; logs full audit traces; detects hallucination, [✗ fuera del corpus]
  - https://github.com/choutos/agent-reliability-engineering ★7 · push 2026-03-26 — Agent Reliability Engineering: applying SRE principles to AI agent systems. Evals, imp@k metrics, self-improvement, config versioning, transfer experiments. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Eppo https://www.geteppo.com/blog/what-are-guardrail-metrics-with-examples; Statsig https://www.statsig.com/comparison/dev-first-alternative-statsig; Microsoft ExP Patterns of Trustworthy Experimentation https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/; Evidently AI https://www.evidentlyai.com/llm-guide/llm-evaluation-metrics

esperado: https://arxiv.org/pdf/2603.18019
confirmado: 

---

## 9 · ecad36a5 · Missing: The Orchestrator That Spends Your Tokens Wisely

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-ecad36a5.md`
- Idea: The neighborhood has quota monitors, a fallback gateway, an agent-building SDK, and cautionary tales of multi-agent waste — but no tool that actively decides which task deserves which model at which cost. Monitoring and routing exist; budget-aware task allocation does not. The obvious missing piece is a 'chief-of-staff' layer that assigns cheap models to boilerplate and expensive ones to hard reasoning, enforcing a spend budget per project. Every ingredient is already open-source in this list.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - RouteLLM (LMSYS) https://github.com/lm-sys/RouteLLM [✓ en corpus (github:lm-sys/routellm)]
  - LiteLLM routing por costo
  - gz-modelrouter (modelo más barato que pasa umbral de calidad) https://github.com/oke3/gz-modelrouter [✗ fuera del corpus]
  - Not Diamond, OpenRouter
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/fuxicodex/Fuxi ★3358 · push 2026-09-23 — FuXi is a fast, self-contained AI coding agent that lives in your terminal — edit code, run commands, and drive tools, with cost-aware routing across LLM providers. [✓ en corpus (github:fuxicodex/fuxi)]
  - https://github.com/NVIDIA-NeMo/Switchyard ★3204 · push 2026-09-23 — Switchyard lets LLM applications route traffic across models and providers while preserving native OpenAI and Anthropic API compatibility - enabling flexible model selection, benchmarking, and cost/pe [✓ en corpus (github:nvidia-nemo/switchyard)]
  - https://github.com/open-compress/claw-compactor ★2024 · push 2026-04-01 — 14-stage Fusion Pipeline for LLM token compression — reversible compression, AST-aware code analysis, intelligent content routing. Zero LLM inference cost. MIT licensed. [✓ en corpus (github:open-compress/claw-compactor)]
  - https://github.com/CommonstackAI/UncommonRoute ★699 · push 2026-06-26 — Automatic LLM router — 82% cost savings, 79.4% accuracy, 93.4% pass rate. Drop-in OpenAI proxy. [✓ en corpus (github:commonstackai/uncommonroute)]
  - https://github.com/Francis1998/nexus-llm-router ★125 · push 2026-09-22 — Intelligent multi-LLM router with task-aware routing strategies, cost optimization, and production safety controls — drop-in OpenAI-compatible API [✓ en corpus (github:francis1998/nexus-llm-router)]
- Prior art que había encontrado Constellate: LiteLLM https://github.com/BerriAI/litellm; RouteLLM https://www.finout.io/blog/5-open-source-tools-to-control-your-ai-api-costs-at-the-code-level; Maestro https://www.ayautomate.com/blog/open-source-llm-orchestration-tools; Morph Router https://www.morphllm.com/llm-router

esperado: https://github.com/lm-sys/RouteLLM https://github.com/oke3/gz-modelrouter
confirmado: 

---

## 10 · aca98da0 · Everyone Manages Agents, Nobody Grades Them

- Constellate: 2026-07-16 · veredicto partially; prior-art manual en `prior-art/absence-aca98da0.md`
- Idea: The neighborhood has agent employment (Multica), agent reliability harnesses (Archon), fleet orchestration (Orca), agents with memory (Rowboat), and agent debugging (DevTools-for-agents) — a full HR stack minus one piece: performance evaluation. There is no tool that scores agent output quality over time, compares agents against each other on real tasks, or decides which agent deserves more autonomy. If agents are 'teammates,' the missing product is their performance review — a benchmark/trust l
- Match (mi evaluación): **parcial-fuerte (evaluación por agente, no "performance review" tipo RRHH)**
- Web (curado):
  - Agent scorecards de FutureAGI https://futureagi.com/glossary/agent-scorecard/ [✗ fuera del corpus]
  - Scorecard.io https://www.scorecard.io/ [✗ fuera del corpus]
  - Braintrust/Phoenix
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/promptfoo/promptfoo ★25383 · push 2026-09-23 — Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line  [✓ en corpus (github:promptfoo/promptfoo)]
  - https://github.com/raga-ai-hub/RagaAI-Catalyst ★16164 · push 2026-02-11 — Python SDK for Agent AI Observability, Monitoring and Evaluation Framework. Includes features like agent, llm and tools tracing, debugging multi-agentic system, self-hosted dashboard and advanced anal [✓ en corpus (github:raga-ai-hub/ragaai-catalyst)]
  - https://github.com/tensortrade-org/tensortrade ★7135 · push 2026-02-19 — An open source reinforcement learning framework for training, evaluating, and deploying robust trading agents. [✓ en corpus (github:tensortrade-org/tensortrade)]
  - https://github.com/harbor-framework/harbor ★5518 · push 2026-09-23 — Framework for evaluating and improving agents  [✓ en corpus (github:harbor-framework/harbor)]
  - https://github.com/trpc-group/trpc-agent-go ★1820 · push 2026-09-23 — A Go framework for building production agent systems with graph workflows, tools, memory, A2A, AG-UI, MCP, evaluation, and observability. [✓ en corpus (github:trpc-group/trpc-agent-go)]
- Prior art que había encontrado Constellate: Galileo AI (Agentic Evaluations + Agent Leaderboard) https://huggingface.co/spaces/galileo-ai/agent-leaderboard; Confident AI / DeepEval https://deepeval.com/guides/guides-ai-agent-evaluation; LangSmith Evaluation (LangChain) https://www.langchain.com/langsmith/evaluation; Holistic Agent Leaderboard (HAL) https://hal.cs.princeton.edu/

esperado: https://futureagi.com/glossary/agent-scorecard/ https://www.scorecard.io/
confirmado: 

---

## 11 · 89c010f2 · Sandboxes Everywhere, but No Agent Firewall

- Constellate: 2026-07-16 · veredicto yes; prior-art manual en `prior-art/absence-89c010f2.md`
- Idea: Three separate projects (microsandbox, CubeSandbox, OpenShell) solve containment — keeping agents from breaking out — and others (codex, herdr) multiply agent activity. But nothing here governs what agents are *allowed* to do inside their permitted scope: no policy engine, permission prompt system, or audit log of agent actions across tools. The gap is an 'agent firewall': a lightweight layer that intercepts, logs, and approves agent side-effects (file writes, network calls, purchases) across an
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Pipelock (firewall de agentes para MCP/egress) https://github.com/luckyPipewrench/pipelock [✓ en corpus (github:luckypipewrench/pipelock)]
  - agentguard (permisos + kill switch) https://github.com/A386official/agentguard [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/hardenrun/aif ★1000 · push 2026-09-05 — On device Firewall for Coding and Personal Agents [✓ en corpus (github:hardenrun/aif)]
  - https://github.com/luckyPipewrench/pipelock ★895 · push 2026-09-23 — Open-source AI agent firewall for MCP security and agent egress. Scans mediated HTTP, MCP, A2A, and WebSocket traffic for exfiltration, SSRF, and prompt injection, and emits mediator-signed action rec [✓ en corpus (github:luckypipewrench/pipelock)]
  - https://github.com/cordum-io/cordum ★508 · push 2026-09-22 — The action firewall for AI agents. Enforce policy and human approval before risky tool calls, shell commands, workflows, and production changes, with auditable evidence. [✓ en corpus (github:cordum-io/cordum)]
  - https://github.com/samber/the-great-gpt-firewall ★100 · push 2026-09-07 — 🤖 A curated list of websites that restrict access to AI Agents, AI crawlers and GPTs [✓ en corpus (github:samber/the-great-gpt-firewall)]
  - https://github.com/mayankjain0141/nixis ★39 · push 2026-09-02 — AI agent firewall that intercepts tool calls (file, shell, network) and enforces deterministic policies at sub-microsecond latency using CEL, IFC, secret scanning, and audit logging. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Preloop https://glama.ai/mcp/servers/@yconst/preloop/tree/b1f7e8e473267657c23069541b85272078fbe60e; Agent Action Firewall https://www.agentactionfirewall.com/; Coder Agent Firewall https://coder.com/docs/ai-coder/agent-firewall; AgentAudit https://aiagentaudit.dev/

esperado: https://github.com/luckyPipewrench/pipelock https://github.com/A386official/agentguard
confirmado: 

---

## 12 · 32a82f3a · Missing: An Exit Kit for AI Vendor Lock-In

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood contains frontier-model dependence, arbitrary account bans, growing resistance, and a post-collapse open-source thesis — but no idea about the practical bridge: tooling that lets builders port prompts, workflows, and fine-tuning investments off a proprietary provider before or after a ban. Given the structure here, an 'AI portability layer' or ban-insurance product is the obvious missing node. Everyone is describing the trap or the aftermath; nobody is building the fire escape.
- Match (mi evaluación): **parcial (portabilidad de API sí; "exit kit" de prompts/evals/memoria no del todo)**
- Web (curado):
  - Bifrost (gateway, cambio de proveedor con base URL)
  - LiteLLM
  - OpenRouter
  - Tokonomics
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/NVIDIA-NeMo/Switchyard ★3204 · push 2026-09-23 — Switchyard lets LLM applications route traffic across models and providers while preserving native OpenAI and Anthropic API compatibility - enabling flexible model selection, benchmarking, and cost/pe [✓ en corpus (github:nvidia-nemo/switchyard)]
  - https://github.com/jolehuit/clother ★430 · push 2026-09-22 — Use multiple Claude Code–compatible LLM providers from one CLI, switching profiles instantly with simple clother-* commands. [✓ en corpus (github:jolehuit/clother)]
  - https://github.com/inference-gateway/inference-gateway ★210 · push 2026-09-23 — An open-source, cloud-native, high-performance gateway unifying multiple LLM providers, from local solutions like Ollama to major cloud providers such as OpenAI, Groq, Cohere, Anthropic, Cloudflare an [✓ en corpus (github:inference-gateway/inference-gateway)]
  - https://github.com/vals-ai/model-library ★25 · push 2026-09-21 — Simple provider agnostic LLM gateway [✗ fuera del corpus]
  - https://github.com/tmdgusya/gl-switcher ★24 · push 2026-06-18 — Zsh utility to switch Claude Code between LLM providers (GLM, Kimi, Claude) with tmux environment sync [✗ fuera del corpus]
- Prior art que había encontrado Constellate: LiteLLM https://github.com/BerriAI/litellm; OpenRouter https://openrouter.ai/; Kong AI Gateway https://konghq.com/blog/learning-center/vendor-lock-in; Orq.ai LLM Gateway https://gateway.orq.ai/blog/llm-vendor-lock-in

esperado: 
confirmado: 

---

## 13 · 7a687ca9 · Missing: provenance layer for machine-made artifacts

- Constellate: 2026-07-16 · veredicto partially
- Idea: We have agents producing code, verifying circuits, training other models, and a cop chasing slop after the fact. What's missing is the upstream piece: a provenance/attestation standard that records which agent, model, and loop produced an artifact, so downstream policing isn't forensic guesswork. The neighborhood defines detection and generation but nothing signs the chain of custody in between. A lightweight 'signed-by-agent' metadata tool for git commits and CI artifacts is the obvious gap.
- Match (mi evaluación): **parcial (estándar en borrador)**
- Web (curado):
  - propuesta OpenSSF de predicado in-toto "AI authorship" / openfab/generation https://github.com/ossf/tac/issues/628 [✓ en corpus (github:ossf/tac)]
  - SLSA+Sigstore para artefactos de IA
  - Atlas (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/microsoft/InvisMark ★62 · push 2026-04-13 — code share for paper InvisMark: Invisible and Robust Watermarking for AI-generated Image Provenance [✗ fuera del corpus]
  - https://github.com/kdcube/kdcube ★25 · push 2026-09-23 — Open-source, self-hosted runtime and SDK for AI applications. One tenant/project deployment serves many users and apps with governed tools, scoped credentials, isolated generated code, and cost contro [✗ fuera del corpus]
  - https://github.com/shapor/gitiq ★6 · push 2024-12-20 — An AI pair programmer that uses Git as its interface, generating complete Pull Requests instead of code snippets and preserving the provenance of AI-generated changes. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Git AI (git-ai) https://github.com/git-ai-project/git-ai; agentdiff https://github.com/codeprakhar25/agentdiff; agentmark https://agentmark.dev/; agent-sign (nono / nolabs-ai) https://github.com/always-further/agent-sign

esperado: https://github.com/ossf/tac/issues/628
confirmado: 

---

## 14 · cf6a474e · Missing: an audit log and permission layer for agents

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood has agents acting on computers, agents needing identity verification, and users discovering unauthorized AI access after the fact. What's structurally absent is the middle piece: a permissions and audit layer — a 'firewall/OAuth for agents' that records what an agent did, under whose delegation, and with what scope. The 922 incident shows demand (people discover access retroactively), and 170 shows the identity primitive exists but not the accountability one.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Shani (capa de autorización para agentes con audit trail a prueba de manipulación) https://dev.to/kmori_f732750cda96b27efe7/i-built-an-open-source-authorization-layer-for-ai-agents-heres-what-the-audit-trail-looks-like-n5g [✗ fuera del corpus]
  - Bifrost audit trails
  - MintMCP gateway
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/cerbos/cerbos ★4592 · push 2026-09-21 — Cerbos is an open-core authorization management platform for authorizing every identity and governing every action across applications, gateways, workloads, and AI agents. [✓ en corpus (github:cerbos/cerbos)]
  - https://github.com/clawvisor/clawvisor ★278 · push 2026-09-17 — API gateway for purpose-based authorization for AI agents. Human approval for tasks, AI-native enforcement for agents. [✓ en corpus (github:clawvisor/clawvisor)]
  - https://github.com/Garudex-Labs/caracal ★212 · push 2026-09-21 — 🐾 Authority, not credentials, for AI agents: policy-approved actions, delegation that can only narrow, instant revocation, tamper-evident audit. [✓ en corpus (github:garudex-labs/caracal)]
  - https://github.com/whataboutyou-ai/eunomia ★100 · push 2025-11-29 — Eunomia is the open-source authorization layer for AI Agents [✓ en corpus (github:whataboutyou-ai/eunomia)]
  - https://github.com/romanklis/openclaw-contained ★31 · push 2026-09-11 — TaskForge Platform runs AI agents in sandboxed Docker containers with capability-based security. Agents start with minimal permissions and must request new capabilities (packages, network access, tool [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Prefactor https://prefactor.tech/product/agent-authentication; Arcade (Arcade.dev) https://www.arcade.dev/; WorkOS (AI agent access control: Connect, RBAC, Audit Logs) https://workos.com/blog/ai-agent-access-control; ScaleKit (On-Behalf-Of authentication for AI agents) https://www.scalekit.com/blog/delegated-agent-access

esperado: https://dev.to/kmori_f732750cda96b27efe7/i-built-an-open-source-authorization-layer-for-ai-agents-heres-what-the-audit-trail-looks-like-n5g
confirmado: 

---

## 15 · b54b6842 · Missing: Proof-of-Human Infrastructure for Creators

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood contains the demand signal (rising anti-AI sentiment, distrust of manufactured culture), the economic casualty (creator middle class dying), and the cognitive worry (offloaded thinking) — but no idea offering verifiable human provenance for creative work. Given this structure, the gap is a lightweight attestation layer that lets creators prove human authorship and lets audiences pay a premium for it. The market is literally being described by these posts; the tool serving it is 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - ProofIDidIt (verificación human-made) https://proofididit.com/hub/proofididit-no-ai-certification [✗ fuera del corpus]
  - AI-Free Cert https://www.aifreecert.com/ [✗ fuera del corpus]
  - VerifiedHuman
  - CAWG identity assertions
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/LF-Decentralized-Trust-labs/proof-of-effort ★5 · push 2026-09-22 — Cryptographic Proof of Effort (CPoE) — IETF Internet-Draft specification for verifiable attestation of human cognitive involvement in digital content creation, built on the RATS architecture (RFC 9334 [✗ fuera del corpus]
- Prior art que había encontrado Constellate: VerifiedHuman https://www.verifiedhuman.info/; CertifyUSA AI-Free Content Badge https://certifyusa.org/blog/ai-free-content-badge; Not By AI https://notbyai.fyi/; By Human, Not AI https://www.byhumannotai.com/

esperado: https://proofididit.com/hub/proofididit-no-ai-certification https://www.aifreecert.com/
confirmado: 

---

## 16 · caa34ef5 · Missing: A Supervision Layer for Autonomous Agents

- Constellate: 2026-07-16 · veredicto partially
- Idea: Agents are hacking TVs, gambling money unsupervised, and self-improving, while the only oversight tool present (Stage, 242) covers just code review. The neighborhood's structure demands a general-purpose agent supervision product: budget caps, action audit trails, kill switches, and human-approval gates for arbitrary agent actions — not just diffs. Its absence is glaring given how much of the set documents agents misbehaving without guardrails.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - hoop.dev (gateway L7 con aprobación humana, MIT) https://hoop.dev/blog/human-in-the-loop-approval-best-practices-for-autonomous-agents [✗ fuera del corpus]
  - LangGraph interrupts
  - GreyCollar
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/sagents-ai/sagents ★273 · push 2026-09-18 — Build interactive AI agents in Elixir with OTP supervision, middleware composition, human-in-the-loop approvals, sub-agent delegation, and real-time Phoenix LiveView integration. Built on LangChain. [✓ en corpus (github:sagents-ai/sagents)]
  - https://github.com/JoyAgents-AI/JOYA ★117 · push 2026-03-04 — JOYA(Joy Agents) is a governance framework for teams of AI agents. It provides the rules, structure, and accountability mechanisms that let multiple agents collaborate safely under human oversight. [✓ en corpus (github:joyagents-ai/joya)]
  - https://github.com/zoharbabin/enterprise-ai-agents-spec ★53 · push 2026-07-03 — An open-source, detailed blueprint for implementing highly scalable swarms of specialized AI Agents in enterprise product development, emphasizing parallelization, robust governance, compliance, and m [✗ fuera del corpus]
  - https://github.com/calabamatex/AgentSentry ★33 · push 2026-07-02 — AgentSentry v0.5.0-beta — Standalone Agent Management Framework for AI agent oversight.  [✗ fuera del corpus]
  - https://github.com/microsoft/agents-humanoversight ★23 · push 2026-04-21 · archivado — Human Oversight for Autonomous AI Agents using Azure Logic Apps + Python [✗ fuera del corpus]
- Prior art que había encontrado Constellate: HumanLayer https://humanlayer.dev; RuntimeAI https://runtimeai.io/blog/2026-05-12-kill-switch.html; Kosmoy (Action Capsule) https://www.kosmoy.com/resources/blog/best-ai-agent-governance-platforms-2026/; CalypsoAI (Moderator) https://www.eesel.ai/blog/lakera-alternatives

esperado: https://hoop.dev/blog/human-in-the-loop-approval-best-practices-for-autonomous-agents
confirmado: 

---

## 17 · a13c1dd2 · Missing: A Trust Layer for Peer-to-Peer Inference

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood has local models beating cloud giants, idle Macs pooled for private inference, websites being audited for agent-readiness, and mesh-style signals surviving blackouts. What's structurally absent is the connective piece: a verification/reputation layer that lets strangers safely rent, route, and audit inference across untrusted consumer hardware. Without attestation of what model ran and whether data leaked, the distributed-AI economy these ideas gesture at can't clear transaction
- Match (mi evaluación): **parcial-fuerte**
- Web (curado):
  - TOPLOC (inferencia verificable) https://github.com/PrimeIntellect-ai/toploc [✗ fuera del corpus]
  - LOGIC (inference.net) https://inference.net/blog/logic/ [✗ fuera del corpus]
  - Theta EdgeCloud
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Nehanth/swarmllm ★434 · push 2026-09-20 — Every device brings a slice. Together they run the whole model. Peer-to-peer LLM inference across browser tabs: a from-scratch WebGPU engine and a WebRTC runtime that split a 27B model over the device [✓ en corpus (github:nehanth/swarmllm)]
  - https://github.com/theblitlabs/parity-protocol ★50 · push 2025-10-25 — A decentralized protocol for verifiable distributed compute.   Sandboxed execution with modular verification, powering LLM inference and federated learning at scale. [✗ fuera del corpus]
  - https://github.com/enapt/SwarmLLM ★48 · push 2026-09-23 — Decentralized peer-to-peer LLM inference network. Single Rust binary, BitTorrent-inspired incentives, OpenAI-compatible API. [✗ fuera del corpus]
  - https://github.com/pur4v/p2ptokens ★30 · push 2026-07-15 — Distributed, peer-to-peer, decentralized network for LLM inference — peers seed & leech completions, metered by BitTorrent-protocol-style upload/download ratios. OpenAI-compatible · Rust · libp2p. [✗ fuera del corpus]
  - https://github.com/InfernetProtocol/infernet-protocol ★30 · push 2026-09-14 — Infernet: A Peer-to-Peer Distributed GPU Inference Protocol [✗ fuera del corpus]
- Prior art que había encontrado Constellate: 0G Compute https://compute.0g.ai/; Ritual https://equilibrium.co/writing/state-of-verifiable-inference; OpenGradient https://www.prnewswire.com/news-releases/opengradient-announces-9-5-million-in-total-funding-to-build-the-compute-layer-for-verifiable-ai-302741614.html; Phala Network (Confidential AI Cloud) https://phala.com/

esperado: https://github.com/PrimeIntellect-ai/toploc https://inference.net/blog/logic/
confirmado: 

---

## 18 · 0bf9e9ec · Missing: The Local-Compute Exit Ramp

- Constellate: 2026-07-16 · veredicto partially
- Idea: One idea proves consumer GPUs run 27B models at real speed, another shows desktop hardware demand outstripping supply, a third exposes the financial fragility of hyperscale GPU financing, and a fourth shows physical resistance to datacenter buildout. The neighborhood clearly wants an off-ramp from hyperscaler dependence, yet no idea addresses the missing piece: turnkey products and marketplaces that let individuals and small teams run serious AI workloads on owned or pooled consumer hardware. Th
- Match (mi evaluación): **fuerte**
- Web (curado):
  - exo (cluster de inferencia con dispositivos caseros) https://github.com/exo-explore/exo [✓ en corpus (github:exo-explore/exo)]
  - GPUStack https://github.com/gpustack/gpustack [✓ en corpus (github:gpustack/gpustack)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/b4rtaz/distributed-llama ★3061 · push 2026-07-05 — Distributed LLM inference. Connect home devices into a powerful cluster to accelerate LLM inference. More devices means faster inference. [✓ en corpus (github:b4rtaz/distributed-llama)]
  - https://github.com/NVIDIA/Personal-AI-Router ★1480 · push 2026-09-23 — Router that virtually distributes inference across connected devices in the home. [✓ en corpus (github:nvidia/personal-ai-router)]
- Prior art que había encontrado Constellate: Vast.ai https://vast.ai/; Ollama https://ollama.com/; LM Studio https://lmstudio.ai/; RunPod https://www.runpod.io/

esperado: https://github.com/exo-explore/exo https://github.com/gpustack/gpustack
confirmado: 

---

## 19 · 384c5945 · Missing: The Cost-and-Ops Layer for Self-Hosted AI

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood has RAG infrastructure pain, GPU multi-tenancy breaking in unmeasured ways, model export to escape Python runtimes, and license risk when choosing open weights. Everyone is self-hosting AI, yet there's no piece covering the obvious next need: a tool that benchmarks, monitors, and prices self-hosted inference stacks — 'what does this model actually cost me per request on my hardware, and where does it break under load'. The gap sits exactly where these four ideas intersect: teams
- Match (mi evaluación): **parcial-fuerte**
- Web (curado):
  - OpenCost (costo de inferencia en k8s, llm-d) https://opencost.io/blog/opencost-llmd-inference-cost/ [✗ fuera del corpus]
  - OpenObserve costo por GPU-hora https://openobserve.ai/blog/llm-cost-monitoring/ [✗ fuera del corpus]
  - nOps
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/bricks-cloud/BricksLLM ★1228 · push 2025-01-05 — 🔒 Enterprise-grade API gateway that helps you monitor and impose cost or rate limits per API key. Get fine-grained access control and monitoring per user, application, or environment. Supports OpenAI, [✓ en corpus (github:bricks-cloud/bricksllm)]
  - https://github.com/ongridio/ongrid ★1076 · push 2026-09-23 — An ops AI Agent that understands your infrastructure, finds the root cause, and fixes it — right from Slack, Telegram, Lark or DingTalk. [✓ en corpus (github:ongridio/ongrid)]
  - https://github.com/qinshihu/itops-agent-platform ★939 · push 2026-09-21 — China's 1st enterprise multi-agent IT ops platform. LLM-powered auto-remediation for Zabbix/Prometheus. Docker deploy. [✓ en corpus (github:qinshihu/itops-agent-platform)]
  - https://github.com/tugcantopaloglu/openclaw-dashboard ★702 · push 2026-03-17 — 🔐 Secure, real-time monitoring dashboard for OpenClaw AI agents. Auth, TOTP MFA, cost tracking, live feed, memory browser and more. [✓ en corpus (github:tugcantopaloglu/openclaw-dashboard)]
  - https://github.com/langfuse/oss-llmops-stack ★152 · push 2026-07-28 — Modular, open source LLMOps stack that separates concerns: LiteLLM unifies LLM APIs, manages routing and cost controls, and ensures high-availability, while Langfuse focuses on detailed observability, [✓ en corpus (github:langfuse/oss-llmops-stack)]
- Prior art que había encontrado Constellate: GuideLLM https://github.com/vllm-project/guidellm; Datadog LLM Observability https://docs.datadoghq.com/llm_observability/monitoring/cost/; vLLM benchmark suite https://docs.vllm.ai/en/latest/contributing/benchmarks.html; MLPerf Inference https://mlcommons.org/benchmarks/inference-datacenter/

esperado: https://opencost.io/blog/opencost-llmd-inference-cost/ https://openobserve.ai/blog/llm-cost-monitoring/
confirmado: 

---

## 20 · 2a3fcc9d · Missing: An Independent Audit Service for AI-Generated Research

- Constellate: 2026-07-16 · veredicto partially
- Idea: The neighborhood contains rubric generation for evaluating agent research, realistic deep-research evaluation, sabotage detection benchmarks, and leakage detection — all the ingredients of research verification, yet all framed as academic benchmarks. What's missing is the productized layer: a service or tool that takes an AI-generated report, paper, or codebase and runs automated integrity checks (leakage, rubric compliance, provenance, sabotage signals) and issues a trust score. As agent-produc
- Match (mi evaluación): **parcial (piezas, no un servicio independiente integral)**
- Web (curado):
  - AI Research Evidence Verification (Apify actor) https://apify.com/suezcanal.xyz/research-verification [✗ fuera del corpus]
  - citation auditing (paper)
  - TAB-AUDIT (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/0xSteph/pentest-ai-agents ★2260 · push 2026-08-16 — Turn Claude Code into your offensive security research assistant. Specialized AI subagents for authorized penetration testing plan engagements, analyze recon, research exploits, build detections, audi [✓ en corpus (github:0xsteph/pentest-ai-agents)]
  - https://github.com/nexscope-ai/Amazon-Skills ★706 · push 2026-08-26 — Free AI agent skills for Amazon sellers—  keyword research, competitor analysis, listing audit & more. Works with OpenClaw, Claude Code, Cursor, Windsurf, Codex and any agent that supports the Skills  [✓ en corpus (github:nexscope-ai/amazon-skills)]
  - https://github.com/damonwan1/AutoScholarLoop ★224 · push 2026-09-16 — A multi-agent AUTO Research loop for idea discovery, experiment execution, evidence-grounded paper writing, quality audit, and live Web observation from AI group, CNIC, CAS. [✓ en corpus (github:damonwan1/autoscholarloop)]
  - https://github.com/forefy/.context ★148 · push 2026-09-22 — AI Agent Skills, Goals and Dynamic Workflows for Security Auditing, Pentesting and Research [✓ en corpus (github:forefy/.context)]
  - https://github.com/longsizhuo/openInvest ★84 · push 2026-09-23 — Research-grade investment decision engine for AI agents: isolated multi-agent committee, auditable verdicts, backtests with lookahead protection, published negative results [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Pangram (AI-text detection used in biomedical/academic publishing) https://www.biorxiv.org/content/10.64898/2026.01.01.697311.full.pdf; Turnitin AI Writing Detection https://www.researchprospect.com/ai-detector-tools/; Copyleaks https://www.researchprospect.com/ai-detector-tools/; Originality.AI https://www.researchprospect.com/ai-detector-tools/

esperado: https://apify.com/suezcanal.xyz/research-verification
confirmado: 

---

## 21 · 8b190bdc · Everyone Audits Bias; Nobody Ships the Bias Firewall

- Constellate: 2026-07-16 · veredicto yes
- Idea: Recommendation bias auditing, ideological drift under temperature, judge/generator asymmetry, and hallucination detection all diagnose how LLM curation and evaluation silently distort content. What's missing is the operational counterpart: a runtime middleware that intercepts LLM curation/judging outputs, scores them for ideological and pragmatic skew, and normalizes or flags them before they reach users. The neighborhood has abundant measurement instruments but no deployable mitigation layer—a 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Guardrails AI (validadores incl. bias) https://github.com/guardrails-ai/guardrails [✓ en corpus (github:guardrails-ai/guardrails)]
  - NeMo Guardrails
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/tiberius-security/tiberius ★13 · push 2026-07-02 — LLM Testing Library for Java: Fault Injections, Prompt Injections, Adversarial Attacks, Guardrails Testing, Bias Testing [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Guardrails AI https://www.guardrailsai.com/; NVIDIA NeMo Guardrails https://github.com/NVIDIA/NeMo-Guardrails; LangChain guardrails middleware https://docs.langchain.com/oss/python/langchain/guardrails; Confident AI / DeepEval guardrails https://www.confident-ai.com/blog/llm-guardrails-the-ultimate-guide-to-safeguard-llm-systems

esperado: https://github.com/guardrails-ai/guardrails
confirmado: 

---

## 22 · 7c597ec1 · Everyone Builds Benchmarks, Nobody Builds Benchmark Infrastructure

- Constellate: 2026-07-16 · veredicto yes
- Idea: This neighborhood contains at least four new domain benchmarks (Vietnamese legal, European medical, advanced math, citation-grounded QA), while 364 explicitly diagnoses the field's failure to accumulate and reuse knowledge. The missing piece is the meta-layer: a system for composing, versioning, deduplicating, and tracking the lifespan of benchmarks so they accumulate rather than pile up. The community keeps shipping one-off evals that ironically reproduce the knowledge-fragmentation problem 364
- Match (mi evaluación): **fuerte (coincide con el "yes" de constellate)**
- Web (curado):
  - lm-evaluation-harness (tareas en YAML, backend del Open LLM Leaderboard) https://github.com/EleutherAI/lm-evaluation-harness [✓ en corpus (github:eleutherai/lm-evaluation-harness)]
  - Inspect (UK AISI) https://github.com/UKGovernmentBEIS/inspect_ai [✓ en corpus (github:ukgovernmentbeis/inspect_ai)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/deer-flow/llm-space ★1927 · push 2026-09-13 — A desktop app to prototype agent ideas, inspect every harness step, replay failures, and evaluate performance, all in one place. Local-first, cloud-ready for managed agents. [✓ en corpus (github:deer-flow/llm-space)]
  - https://github.com/claw-eval/claw-eval ★773 · push 2026-09-22 — Claw-Eval is an evaluation harness for evaluating LLM as agents. All tasks verified by humans. [✓ en corpus (github:claw-eval/claw-eval)]
  - https://github.com/ZubinGou/math-evaluation-harness ★279 · push 2024-04-26 — A simple toolkit for benchmarking LLMs on mathematical reasoning tasks. 🧮✨ [✓ en corpus (github:zubingou/math-evaluation-harness)]
  - https://github.com/agentscope-ai/PawBench ★112 · push 2026-08-03 — A benchmark for evaluating LLM × harness performance. [✓ en corpus (github:agentscope-ai/pawbench)]
  - https://github.com/project-etalon/etalon ★85 · push 2025-02-25 — LLM Serving Performance Evaluation Harness [✗ fuera del corpus]
- Prior art que había encontrado Constellate: EleutherAI lm-evaluation-harness https://github.com/EleutherAI/lm-evaluation-harness; Every Eval Ever https://arxiv.org/pdf/2606.14516; Inspect AI https://inspect.aisi.org.uk/; Stanford HELM https://crfm.stanford.edu/helm/

esperado: https://github.com/EleutherAI/lm-evaluation-harness https://github.com/UKGovernmentBEIS/inspect_ai
confirmado: 

---

## 23 · a3ced3a9 · Everyone Edits Models, Nobody Verifies the Edit

- Constellate: 2026-07-16 · veredicto yes
- Idea: Four papers intervene directly on model internals: pruning unsafe subnetworks, real-time unlearning, activation steering, and mechanistic bias localization. All assume the intervention worked, yet the neighborhood contains no tool for independently auditing whether an edit actually removed the behavior, preserved capabilities, and didn't create new failures. The missing piece is a standardized 'edit verification' layer — a diff-and-regression harness for model surgery, analogous to CI tests for 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - MUSE (benchmark de unlearning, 6 propiedades) https://arxiv.org/abs/2407.06460 [✗ fuera del corpus]
  - EasyEdit (evaluación de edición) https://github.com/zjunlp/EasyEdit [✓ en corpus (github:zjunlp/easyedit)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/TIGER-AI-Lab/EditReward ★160 · push 2026-07-26 — EditReward: A Human-Aligned Reward Model for Instruction-Guided Image Editing [ICLR 2026] [✓ en corpus (github:tiger-ai-lab/editreward)]
  - https://github.com/gnueaj/Machine-Unlearning-Comparator ★101 · push 2026-09-12 — A Visual Analytics System for Comparative Evaluation of Machine Unlearning Methods (TVCG 2026) [✓ en corpus (github:gnueaj/machine-unlearning-comparator)]
  - https://github.com/edenbiran/RippleEdits ★57 · push 2024-04-15 — Evaluating the Ripple Effects of Knowledge Editing in Language Models [✗ fuera del corpus]
  - https://github.com/nuprl/CanItEdit ★51 · push 2025-09-13 — Can It Edit? Evaluating the Ability of Large Language Models to Follow Code Editing Instructions [✗ fuera del corpus]
  - https://github.com/open-compass/GenEditEvalKit ★50 · push 2026-04-12 — The first unified, efficient, and extensible evaluation toolkit for evaluating image generation and editing models across multiple benchmarks. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: MUSE https://muse-bench.github.io/; TOFU https://locuslab.github.io/tofu/; RWKU https://arxiv.org/pdf/2406.10890; lm-evaluation-harness (capability regression) https://github.com/EleutherAI/lm-evaluation-harness

esperado: https://github.com/zjunlp/EasyEdit https://arxiv.org/abs/2407.06460
confirmado: 

---

## 24 · 4eb18786 · Missing: Runtime Stance Monitor for Deployed Chatbots

- Constellate: 2026-07-16 · veredicto partially
- Idea: 3232 defines relational lock-in as a measurable risk object, 2847 defines register shift as probeable, and 3125 proves tone causally changes recipient behavior—yet all three measure offline. The obvious missing piece is a runtime middleware that scores stance drift, epistemic register, and dependency-inducing positioning on live conversations and alerts or steers before harm accrues. Companies deploying companions, therapy-adjacent bots, or customer agents have no such instrument today.
- Match (mi evaluación): **débil -> posible hueco real**
- Web (curado):
  - sin producto claro: auditorías de sycophancy en investigación
  - tone analyzers genéricos (patentes)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Exponential-OS/prompt-engineering-in-action ★9 · push 2026-09-14 — Co-Dialectic: catch your AI agreeing with you to please you, not because you're right. Sycophancy detection, cross-family judging, and prompt coaching that runs during the conversation rather than aud [✗ fuera del corpus]
  - https://github.com/Bhavik-Jikadara/ai-customer-service-agent ★6 · push 2025-10-25 — This production-ready AI system automates customer support with multi-step workflows, tool integration, stateful conversations, and real-time performance monitoring. [✗ fuera del corpus]
- Prior art que había encontrado Constellate: EmoAgent https://spectrum.ieee.org/amp/mental-health-chatbot-guardrails-2676699987; SHIELD (Supervisory Helper for Identifying Emotional Limits and Dynamics) https://spectrum.ieee.org/amp/mental-health-chatbot-guardrails-2676699987; GAUGE (Guarding Affective Utterance Generation-Escalation) https://arxiv.org/pdf/2512.06193; SonderMind independent guardrail modules https://finance.biggo.com/news/52d5f5fbe28b3370

esperado: 
confirmado: 

---

## 25 · 024eb0a0 · Everyone Builds Deepfake Engines, One Paper Builds Locks

- Constellate: 2026-07-16 · veredicto partially
- Idea: This neighborhood is dense with generative video editing power: identity-consistent face editing, object insertion, frontier audio-video generation, and fully automated short-video engines. Only 2689 addresses protection, and only preemptively via adversarial perturbation of source content. Missing entirely: post-hoc detection, provenance watermarking, and verification tooling for generated/edited video — the defensive layer that this generative arsenal makes urgent. The gap is a video authentic
- Match (mi evaluación): **fuerte (imágenes; video menos)**
- Web (curado):
  - PhotoGuard (MIT, inmuniza imágenes contra edición) https://github.com/MadryLab/photoguard [✓ en corpus (github:madrylab/photoguard)]
  - MIRAGE (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/ozdentarikcan/DiffVax ★22 · push 2026-02-16 — [ICLR 2026] DiffVax: Optimization-Free Image Immunization Against Diffusion-Based Editing [✗ fuera del corpus]
  - https://github.com/multimodal-ai-lab/VETO ★5 · push 2026-07-31 — VETO: Towards Protecting Images From Frontier AI Editing [✗ fuera del corpus]
- Prior art que había encontrado Constellate: Google SynthID (with SynthID Detector portal) https://deepmind.google/models/synthid/; C2PA / Content Credentials (contentcredentials.org verify tool) https://contentcredentials.org/; Resemble AI (Resemble Detect / DETECT-2B) https://www.resemble.ai/deepfake-video-detection-guide/; Attestiv https://attestiv.com/provenance-vs-forensics-the-best-solution-for-deepfake-detection/

esperado: https://github.com/MadryLab/photoguard
confirmado: 

---

## 26 · 49948ece · Missing: Real-time Collaborative Content Rehearsal Platform

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: WeFlow and Postiz handle social media scheduling, sub2api manages API aggregation for shared access, and Textream provides solo teleprompting. What's absent is a collaborative rehearsal and approval workflow tool that bridges content creation, team review, and delivery scheduling with real-time feedback loops. Current tools treat content as static assets moving through a pipeline rather than iterative performances refined through collaboration.
- Match (mi evaluación): **fuerte (aprobación sí; "ensayo" con teleprompter no)**
- Web (curado):
  - Planable (colaboración y aprobación de contenido social, incl. guiones de video) https://planable.io/blog/approval-software/ [✗ fuera del corpus]
  - Filestage
  - Hootsuite approvals
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Freespirits/social-auto-engine ★27 · push 2026-07-18 — Multi-channel social media platform. Manage Facebook, Instagram, LinkedIn, TikTok, and X from one dashboard. AI content generation, approval workflows, 17 content skills, scales to 100 pages. [✗ fuera del corpus]
  - https://github.com/usegalaxy-eu/galaxy-social ★9 · push 2026-09-21 — Repository for democratising of Galaxy's social media activity - encourage collaboration, editing, peer-review of toots 🐘 and more [✗ fuera del corpus]

esperado: https://planable.io/blog/approval-software/
confirmado: 

---

## 27 · e888547c · Missing: macOS Workflow Orchestration Layer

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Multiple specialized macOS utilities (menu bar managers, clipboard tools, media players) exist in isolation, but there's no meta-tool that orchestrates them into coherent workflows. Users must manually configure each app and mentally manage their interactions. The gap is a macOS-native workflow automation layer that treats these utilities as composable primitives—something between Apple Shortcuts and a full automation framework, but specifically designed for power users who've already assembled 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Keyboard Maestro, Alfred workflows, Hammerspoon, Shortcuts https://textexpander.com/blog/keyboard-maestro-alternatives [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/totec448-spec/chat-on-steroids ★3948 · push 2026-09-22 — Cross-platform local MCP capabilities for ChatGPT with Chrome integration, Goal, Compact & Resume, and durable multi-agent workflows. [✓ en corpus (github:totec448-spec/chat-on-steroids)]
  - https://github.com/linsa-io/alfred-workflows ★2776 · push 2026-05-01 — Amazing Alfred Workflows [✓ en corpus (github:linsa-io/alfred-workflows)]
  - https://github.com/moazbuilds/CodeMachine-CLI ★2512 · push 2026-02-25 — CodeMachine is an open-source tool that orchestrates AI coding agents into repeatable, long-running workflows. ⚡️ [✓ en corpus (github:moazbuilds/codemachine-cli)]
  - https://github.com/ghostwright/ghost-os ★1666 · push 2026-03-23 — Full computer-use for AI agents. Self-learning workflows. Native macOS. No screenshots required. [✓ en corpus (github:ghostwright/ghost-os)]
  - https://github.com/Git-Agni/prod-FARM-IOS-Core ★1549 · push 2026-09-07 — A farm of real iPhones, run from your Mac. Open-source iOS device automation with live control, a Postgres-backed scheduler, and TikTok workflows. Self-hosted, Apache-2.0. [✓ en corpus (github:git-agni/prod-farm-ios-core)]

esperado: https://textexpander.com/blog/keyboard-maestro-alternatives
confirmado: 

---

## 28 · b6545a2e · Missing: Privacy-Preserving AI Traffic Analysis

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Multiple ideas involve watching what AI tools access (Nginx logs from prompts, ad placements based on prompts, shopping experiences, meeting transcription). Yet there's no tool helping users understand what data their AI assistants are leaking or how to audit prompt-based information flows. The gap is a privacy layer that sits between users and AI services, showing what context is being sent where—especially critical as AI gets embedded everywhere from Excel to shopping.
- Match (mi evaluación): **débil-parcial (orientado a empresa, no al usuario)**
- Web (curado):
  - auditoría de red de apps locales de IA (local-llm.net) https://www.local-llm.net/blog/local-ai-privacy-audit/ [✗ fuera del corpus]
  - monitores corporativos (Cyberhaven, Swif)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/sgasser/pasteguard ★754 · push 2026-08-25 — AI gets the context. Not your private data. Local-first privacy proxy for browser chat, AI APIs, and coding agents. [✓ en corpus (github:sgasser/pasteguard)]
  - https://github.com/inkdust2021/VibeGuard ★220 · push 2026-03-26 — Uses just 1% memory while protecting 99% of your personal privacy. [✓ en corpus (github:inkdust2021/vibeguard)]
  - https://github.com/voidmind-io/voidllm ★136 · push 2026-09-17 — Privacy-first LLM proxy and AI gateway - load balancing, multi-provider routing, API key management, usage tracking, rate limiting. Self-hosted. Zero knowledge of your prompts. [✓ en corpus (github:voidmind-io/voidllm)]
  - https://github.com/CassiopeiaCode/CosyRedactGateway ★94 · push 2026-09-18 — Lightweight, stateless privacy gateway for LLM APIs — redact secrets before OpenAI/Anthropic upstreams and restore them transparently in SSE and tool calls. [✗ fuera del corpus]
  - https://github.com/rohansx/cloakpipe ★43 · push 2026-08-30 — Privacy middleware for LLM & RAG pipelines - consistent pseudonymization, encrypted vault, SSE streaming rehydration.  [✗ fuera del corpus]

esperado: https://www.local-llm.net/blog/local-ai-privacy-audit/
confirmado: 

---

## 29 · 8e2e16e5 · Missing: AI Content Debugger Across Modalities

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Pegasus extracts time-based metadata from video, Libertify converts documents to interactive video, and Makko generates game art and playables. All three transform content across formats, but none help you understand WHY the AI made specific creative or structural choices. The missing piece: a meta-tool that explains AI-generated content decisions across modalities—why this visual style, why this pacing, why this interaction model—enabling creators to iterate with understanding rather than blind
- Match (mi evaluación): **débil -> posible hueco real (o idea vaga)**
- Web (curado):
  - sin resultados relevantes (solo explicaciones genéricas)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/gonicolas12/My_AI ★10 · push 2026-09-21 — Local-first AI assistant — 9 specialized agents (code, web, debug, security…), 10M-token vector memory, multimodal (vision + local image generation), two-way voice (dictation + read-aloud), slash comm [✗ fuera del corpus]

esperado: 
confirmado: 

---

## 30 · fbaa9603 · No Simulator for AI Agent Failure Modes

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Astropad gives agents desktop access, Vantage simulates team scenarios for humans, and Chinilla simulates system breakage points—but nothing simulates *how AI agents will fail* in production contexts before deployment. We have guardrails (ElevenAgents) and monitoring (Waydev), but no pre-deployment sandbox that stress-tests agent behavior under adversarial inputs, edge cases, or multi-agent conflicts. The gap is a chaos engineering platform specifically for agentic systems.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - agent-chaos (chaos engineering para agentes) https://github.com/deepankarm/agent-chaos [✓ en corpus (show_hn:46445261)]
  - SREGym (benchmark)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/future-agi/simulate-sdk ★59 · push 2026-06-30 — Enterprise Grade, Voice AI simulation SDK for testing your AI Agents [✗ fuera del corpus]
  - https://github.com/Mentat-Lab/preclinical ★18 · push 2026-06-21 — Preclinical is an open-source healthcare AI safety testing platform. It simulates realistic adversarial patient interactions against your agent, stores transcripts, and grades outcomes against safety  [✗ fuera del corpus]
  - https://github.com/radanliev/Red-Teaming-Multi-Agent-AI-Systems- ★11 · push 2025-08-01 · archivado — Red Teaming Multi-Agent AI Systems - Learn how to simulate, test, and defend against coordinated cyber-attacks on autonomous agent networks.  [✗ fuera del corpus]
  - https://github.com/tenro-ai/tenro-python ★7 · push 2026-06-09 — Open-source simulation harness for testing AI agents. Simulate LLM and tool calls to test edge cases, failure paths, and agent logic without live API calls. [✗ fuera del corpus]
  - https://github.com/nanameru/agent-skills ★5 · push 2026-09-15 — Security-focused chaos engineering skill for AI coding agents. Analyze codebases for vulnerabilities through failure scenario simulation. [✗ fuera del corpus]

esperado: https://github.com/deepankarm/agent-chaos
confirmado: 

---

## 31 · 84077248 · Missing: Development Environment Orchestration Layer

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: VS Code Remote Tunnels, parallel Claude agents, and K8s AI assistance all point to developers managing increasingly complex, ephemeral development environments—but there's no unified orchestration tool. The gap is a lightweight "dev environment router" that dynamically provisions, switches between, and tears down isolated development contexts based on task, not manual setup. Something between tmux sessions and full Kubernetes, purpose-built for the multi-agent, multi-context developer workflow.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Kaiden (agentes de código en sandboxes efímeros) https://openkaiden.ai/ [✗ fuera del corpus]
  - Composio Agent Orchestrator
  - awesome-agent-orchestrators https://github.com/andyrewlee/awesome-agent-orchestrators [✓ en corpus (github:andyrewlee/awesome-agent-orchestrators)]
  - Coder/DevPod
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/generalaction/emdash ★5807 · push 2026-09-22 — Emdash is the Open-Source Agentic Development Environment (🧡 YC W26). Run multiple coding agents in parallel. Use any provider. [✓ en corpus (github:generalaction/emdash)]
  - https://github.com/azukiapp/azk ★894 · push 2019-04-26 · archivado — azk is a lightweight open source development environment orchestration tool. Instantly & safely run any environment on your local machine. [✓ en corpus (github:azukiapp/azk)]
  - https://github.com/kdlbs/kandev ★830 · push 2026-09-23 — AI Kanban & Development Environment. Orchestrate multiple agents, review changes, open PRs. Multi-provider, self-hostable, no telemetry. [✓ en corpus (github:kdlbs/kandev)]
  - https://github.com/lxdock/lxdock ★362 · push 2020-03-02 · archivado — Build and orchestrate your development environments with LXD - a.k.a. Vagrant is Too Heavy™ [✓ en corpus (github:lxdock/lxdock)]
  - https://github.com/cocoonstack/cocoon ★226 · push 2026-09-23 — Lightweight MicroVM engine built on Cloud Hypervisor. Features include OCI and cloud image support, instant snapshot and clone via reflink, Windows 11 guest support, CNI networking with TC redirect, m [✓ en corpus (github:cocoonstack/cocoon)]

esperado: https://github.com/andyrewlee/awesome-agent-orchestrators https://openkaiden.ai/
confirmado: 

---

## 32 · a5a33a2d · Living Authority Graph for Evolving Knowledge Bases

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: These ideas reveal a missing primitive: a system that tracks not just versions or signatures, but the formal supersession relationships between documents across time. Legal docs void predecessors, commits can be revoked, security lists deprecate entries—but no tool models the "active frontier" of authoritative knowledge as a first-class, queryable graph structure. Current version control shows history; this would show what's currently binding.
- Match (mi evaluación): **débil -> posible hueco real**
- Web (curado):
  - solo gestión documental genérica con versionado (LawVu)

esperado: 
confirmado: 

---

## 33 · 87fb2520 · Missing: Hardware Abstraction for Heterogeneous Computing

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Cerebras S-1, ROCm/Strix Halo impressions, and supercurrent diode research all expose specialized hardware emerging without unified development frameworks. The gap is a true hardware abstraction layer that lets developers write once and deploy across neuromorphic, quantum, photonic, and traditional silicon without per-architecture rewrites. What's missing is the 'browser for hardware'—a compile target that handles radical architectural differences transparently.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - SYCL (Khronos) https://www.khronos.org/sycl/ [✗ fuera del corpus]
  - Mojo/MAX https://mojolang.org/ [✗ fuera del corpus]
  - alpaka
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Void-Compute/AMD-Ghost-Enviroment ★103 · push 2026-09-08 — Advanced interoperability middleware for GPGPU acceleration. Facilitates cross vendor hardware abstraction and API translation for parallel computing frameworks. Engineered for research into heterogen [✓ en corpus (github:void-compute/amd-ghost-enviroment)]
  - https://github.com/renning22/glm-5.2-4090 ★83 · push 2026-06-24 — First known correct serving of GLM-5.2 (DeepSeek-Sparse-Attention) on consumer RTX 4090 GPUs — a portable Ada/sm_89 port of the DSA kernel stack. [✗ fuera del corpus]

esperado: https://www.khronos.org/sycl/ https://mojolang.org/
confirmado: 

---

## 34 · 74917578 · Missing: Provenance Layer for Synthetic Media

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: We have slop detection, AI security concerns, generative design tools competing with incumbents, and public trust in institutions eroding—but no robust system for marking genuine human-created work or verifying content origins. The gap is a lightweight, decentralized provenance protocol that doesn't require blockchain maximalism but does create tamper-evident chains of custody for media and ideas. Everyone is building generators; nobody's building authenticators.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - C2PA / Content Credentials + herramientas open source del CAI https://contentauthenticity.org/how-it-works [✗ fuera del corpus]
  - c2pa-rs https://github.com/contentauth/c2pa-rs [✓ en corpus (github:contentauth/c2pa-rs)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/guillaumemeyer/watermarks-remover ★22625 · push 2026-09-22 — A privacy-first app that strips AI watermarks from content you own. [✓ en corpus (github:guillaumemeyer/watermarks-remover)]
  - https://github.com/contentauth/c2pa-rs ★423 · push 2026-09-23 — Rust SDK for the core C2PA (Coalition for Content Provenance and Authenticity) specification [✓ en corpus (github:contentauth/c2pa-rs)]
  - https://github.com/iqlusioninc/veriform ★121 · push 2023-01-17 — Security-oriented protobuf-like serialization format with "Merkleized" content hashing support [✓ en corpus (github:iqlusioninc/veriform)]
  - https://github.com/numbersprotocol/pyc2pa ★44 · push 2022-06-22 — Python implementation of C2PA: Coalition for Content Provenance and Authenticity. [✗ fuera del corpus]
  - https://github.com/indranilbanerjee/contentforge ★30 · push 2026-08-17 — An open-source editorial production system that researches, verifies, drafts, and delivers publication-ready long-form content with human review and provenance built in. [✗ fuera del corpus]

esperado: https://github.com/contentauth/c2pa-rs https://contentauthenticity.org/how-it-works
confirmado: 

---

## 35 · 2c12528f · Missing: Domain-Specific AI Data Governance Tools

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: GPT for life sciences, AI companies buying failed startup Slack data, and Amazon's internal AI data mess all expose the same gap: specialized tooling for AI data provenance, consent, and lineage in domain contexts. We have general AI infrastructure but lack middleware that tracks data rights, scientific reproducibility requirements, and compliance across the AI pipeline. The absence is particularly acute for regulated domains (healthcare, finance) where data governance isn't optional but legally
- Match (mi evaluación): **parcial (genérico, no específico de dominio)**
- Web (curado):
  - Relyance AI (lineage de datos de entrenamiento) https://www.relyance.ai/solutions/ai-data-lineage-training-runtime [✗ fuera del corpus]
  - Verifywise data lineage mapper https://verifywise.ai/tools/data-lineage-mapper [✗ fuera del corpus]
  - Atlan
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/facebookresearch/content-seal ★243 · push 2026-07-08 — Content Seal is a state-of-the-art framework for invisible, robust watermarking across all modalities audio, image, video, and text. This suite spans the entire generative lifecycle, from training dat [✓ en corpus (github:facebookresearch/content-seal)]
  - https://github.com/znxzsy/AlignLedger ★100 · push 2026-08-27 — Auditable human-feedback annotation, review, provenance, and frozen training-data export. [✓ en corpus (github:znxzsy/alignledger)]
  - https://github.com/rishin-sharma/CorpusCustody ★51 · push 2026-09-04 — Training-data license and provenance gate: resolve SPDX obligations, check compatibility against a declared purpose, and gate corpus ingestion. [✗ fuera del corpus]
  - https://github.com/ananjiahhao/CorpusCustody ★16 · push 2026-09-20 — Offline gate for training-data licenses and provenance: SPDX compatibility, obligation matrix, and deterministic reports. [✗ fuera del corpus]
  - https://github.com/tsubotti63/garmin-running-data-normalizer ★11 · push 2026-09-03 — Local-first Python CLI that turns Garmin Account Data Export into reproducible running, FIT, sleep, HRV, and training datasets with QA and provenance. [✗ fuera del corpus]

esperado: https://www.relyance.ai/solutions/ai-data-lineage-training-runtime https://verifywise.ai/tools/data-lineage-mapper
confirmado: 

---

## 36 · a8d458b3 · The Missing AI Development Ops Layer

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: We have tutorials for building AI agents (Bedrock), CLI tools for app development (Android CLI), and post-mortems on integration gaps (MCP). What's conspicuously absent is tooling that bridges the gap: observability, debugging, and operational infrastructure specifically for AI-augmented development workflows. Developers are building agents to write code faster, but have no standardized way to monitor, test, or validate AI-generated changes in CI/CD pipelines.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Agenta (LLMOps open source) https://github.com/Agenta-AI/agenta [✓ en corpus (github:agenta-ai/agenta)]
  - Langfuse
  - Lunary
  - Helicone
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/tensorzero/tensorzero ★11721 · push 2026-06-11 · archivado — TensorZero is an open-source LLMOps platform that unifies an LLM gateway, observability, evaluation, optimization, and experimentation. [✓ en corpus (github:tensorzero/tensorzero)]
  - https://github.com/tensorchord/Awesome-LLMOps ★5944 · push 2026-05-21 — An awesome & curated list of best LLMOps tools for developers [✓ en corpus (github:tensorchord/awesome-llmops)]
  - https://github.com/PacktPublishing/LLM-Engineers-Handbook ★5347 · push 2026-04-22 — The LLM's practical guide: From the fundamentals to deploying advanced LLM and RAG apps to AWS using LLMOps best practices [✓ en corpus (github:packtpublishing/llm-engineers-handbook)]
  - https://github.com/decodingai-magazine/second-brain-ai-assistant-course ★3094 · push 2026-04-06 — Learn to build your Second Brain AI assistant with LLMs, agents, RAG, fine-tuning, LLMOps and AI systems techniques. [✓ en corpus (github:decodingai-magazine/second-brain-ai-assistant-course)]
  - https://github.com/clearml/clearml-agent ★313 · push 2026-09-16 — ClearML Agent - MLOps/LLMOps made easy. MLOps/LLMOps scheduler & orchestration solution [✓ en corpus (github:clearml/clearml-agent)]

esperado: https://github.com/Agenta-AI/agenta
confirmado: 

---

## 37 · 4929df32 · Missing: AI Service Audit Layer

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Gas Town allegedly stealing credits, vendor verification tools emerging, and shuttered startups selling training data all point to a missing infrastructure piece: continuous third-party auditing of AI service providers. The gap is a 'trustless verification layer' for AI services—something like certificate transparency logs but for model serving, credit usage, and data handling. No one is building the independent watchdog infrastructure that this emerging market desperately needs.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Vaudit TokenAudit (auditoría de facturación de tokens) https://www.businesswire.com/news/home/20260630108235/en/ [✗ fuera del corpus]
  - api-relay-audit (detecta sustitución de modelo en proxies) https://github.com/toby-bridges/api-relay-audit [✓ en corpus (github:toby-bridges/api-relay-audit)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/LeenHawk/gproxy ★242 · push 2026-09-23 — gproxy is a Rust-based multi-channel LLM proxy that exposes OpenAI / Claude / Gemini-style APIs through a unified gateway, with a built-in admin console, user/key management, and request/usage auditin [✓ en corpus (github:leenhawk/gproxy)]
  - https://github.com/Bigduang/new-api-audit-for-company ★11 · push 2026-09-11 — Independent token usage and work-purpose audit service for New-API, with SQLite, LLM classification, HTML [✗ fuera del corpus]

esperado: https://github.com/toby-bridges/api-relay-audit https://www.businesswire.com/news/home/20260630108235/en/
confirmado: 

---

## 38 · 13057e1b · Missing: AI Agents That Actually Test and Verify

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Multiple AI agent products claim to "build, verify, and ship" or "ship real code," yet idea 2557 reveals production-ready code requires 111 tests, 17 PDFs, and 44-item checklists. The absence is glaring: no AI agent system currently tackles the unglamorous verification layer—automated generation of comprehensive test suites, security checklists, and compliance documentation that separate demos from production. The "verify" claim in current products is marketing vapor.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - TestSprite (verificación de agentes de código) https://www.testsprite.com/blog/your-ai-agent-writes-fast-who-checks-its-work [✗ fuera del corpus]
  - Shiplight agent-first testing
  - Claude Code TDD
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/vxcontrol/pentagi ★24881 · push 2026-09-10 — Fully autonomous AI Agents system capable of performing complex penetration testing tasks [✓ en corpus (github:vxcontrol/pentagi)]
  - https://github.com/SanMuzZzZz/LuaN1aoAgent ★1317 · push 2026-09-15 — LuaN1aoAgent is a fully autonomous AI-driven penetration testing agent powered by graph-based cognitive reasoning. [✓ en corpus (github:sanmuzzzzz/luan1aoagent)]
  - https://github.com/aielte-research/HackSynth ★318 · push 2025-06-24 — LLM Agent and Evaluation Framework for Autonomous Penetration Testing  [✓ en corpus (github:aielte-research/hacksynth)]
  - https://github.com/pensarai/apex ★312 · push 2026-09-22 — AI-powered offensive security testing using autonomous agents, directly in your terminal. [✓ en corpus (github:pensarai/apex)]
  - https://github.com/gbessoni/seobuild-onpage ★251 · push 2026-09-03 — SEOBuild Onpage - The first AI agent that writes pages Google ranks AND LLMs cite. One command in, ranking page out. Built on DeerFlow, powered by 2026 SEO + GEO strategies tested / working. Forensic  [✓ en corpus (github:gbessoni/seobuild-onpage)]

esperado: https://www.testsprite.com/blog/your-ai-agent-writes-fast-who-checks-its-work
confirmado: 

---

## 39 · a82c30fc · Missing: Prompt Robustness Testing Framework

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Three papers explore prompt-based detection systems (visual prompts for objects, textual prompts for OOD detection, metaphor detection generalization), yet none addresses systematic testing of prompt brittleness or transferability. notes visual prompts outperform text for rare categories; shows test-time textual adaptation improves OOD detection; questions whether models learn transferable patterns or memorize cues. The gap: a unified framework for evaluating prompt robustness across modalities 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - PromptBench (Microsoft) https://github.com/microsoftarchive/promptbench [✓ en corpus (github:microsoftarchive/promptbench)]
  - Brittlebench (paper)
  - promptfoo
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/langgptai/LangGPT ★12547 · push 2026-09-11 — LangGPT: Empowering everyone to become a prompt expert! 🚀  📌 结构化提示词（Structured Prompt）提出者 📌 元提示词（Meta-Prompt）发起者   📌 最流行的提示词落地范式 | Language of GPT  The pioneering framework for structured & meta-promp [✓ en corpus (github:langgptai/langgpt)]
  - https://github.com/adrianhajdin/project_next_14_ai_prompt_sharing ★2959 · push 2024-06-30 — Next.js recently became the official React framework as outlined in React docs. In this course, you'll learn the most important Next.js concepts and how they fit into the React ecosystem. Finally, you [✓ en corpus (github:adrianhajdin/project_next_14_ai_prompt_sharing)]
  - https://github.com/praetorian-inc/augustus ★290 · push 2026-09-21 — LLM security testing framework for detecting prompt injection, jailbreaks, and adversarial attacks — 190+ probes, 28 providers, single Go binary [✓ en corpus (github:praetorian-inc/augustus)]
  - https://github.com/Hellsender01/LLMMap ★206 · push 2026-03-14 — Automated prompt injection testing framework for LLM-integrated applications with dual-LLM architecture. [✓ en corpus (github:hellsender01/llmmap)]
  - https://github.com/ShadowHackrs/prompt-generating ★90 · push 2026-09-16 — is an elite, highly advanced command-line framework designed for generating complex prompt structures. It is built to push the boundaries of AI models by testing their alignment, safety filters, and o [✗ fuera del corpus]

esperado: https://github.com/microsoftarchive/promptbench
confirmado: 

---

## 40 · b05991cf · The Missing Bridge: Production ML Spec Templates

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Multiple builders document complete end-to-end ML systems (support tickets, predictions, IPL AI, audio detection), but they all start from scratch with custom architectures. What's missing is a meta-layer: reusable specification templates that capture the *decision structure* of building production ML—not code, but the architectural choices, data pipeline patterns, and evaluation frameworks that these posts reinvent each time. A library of ML system blueprints.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - ml-systems-blueprints https://github.com/vipul957/ml-systems-blueprints [✗ fuera del corpus]
  - getindata quickstart-ml-blueprints https://github.com/getindata/quickstart-ml-blueprints [✗ fuera del corpus]
  - cookiecutter-data-science
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/eugeneyan/ml-design-docs ★716 · push 2023-03-16 — 📝  Design doc template & examples for machine learning systems (requirements, methodology, implementation, etc.) [✓ en corpus (github:eugeneyan/ml-design-docs)]
  - https://github.com/ml-tooling/ml-project-template ★115 · push 2019-08-05 — ML project template facilitating both research and production phases. [✓ en corpus (github:ml-tooling/ml-project-template)]
  - https://github.com/wahyudesu/Fastapi-AI-Production-Template ★114 · push 2026-04-16 — Simple starter template for your ML/AI projects (uv package manager, RestAPI with FastAPI and Dockerfile support) [✓ en corpus (github:wahyudesu/fastapi-ai-production-template)]
  - https://github.com/thanhhau097/ml_project_template ★102 · push 2022-12-13 — Machine Learning Project Template - Ready to production [✓ en corpus (github:thanhhau097/ml_project_template)]
  - https://github.com/DanielhCarranza/ml-production-template ★43 · push 2020-11-25 — This codebase is a starting point to get your Machine Learning project into Production. [✗ fuera del corpus]

esperado: https://github.com/vipul957/ml-systems-blueprints https://github.com/getindata/quickstart-ml-blueprints
confirmado: 

---

## 41 · 08b2faf0 · Missing: Cross-System Agent Observability Protocol

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: The neighborhood has evaluation platforms, agent definitions, drift detection, and memory systems—but no standardized observability layer that connects them. Each builder invents their own instrumentation for tracking agent behavior across RAG retrieval, tool calls, memory updates, and output quality. What's absent is a protocol or open standard for agent telemetry that would let these disparate quality-assurance approaches interoperate, similar to what OpenTelemetry did for microservices.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - OpenTelemetry GenAI semantic conventions (agentes) https://opentelemetry.io/blog/2025/ai-agent-observability/ [✗ fuera del corpus]
  - https://github.com/open-telemetry/semantic-conventions-genai [✓ en corpus (github:open-telemetry/semantic-conventions-genai)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/pydantic/logfire ★4487 · push 2026-09-23 — AI observability platform for production LLM and agent systems. [✓ en corpus (github:pydantic/logfire)]
  - https://github.com/openlit/openlit ★2788 · push 2026-09-22 — Open-source observability & evaluation platform for AI agents and coding agents. Trace LLMs, tools, prompts, costs & agent workflows with OpenTelemetry. [✓ en corpus (github:openlit/openlit)]
  - https://github.com/superloglabs/superlog ★1452 · push 2026-09-20 — Open-source observability tool that uses AI agents to self-heal your software [✓ en corpus (github:superloglabs/superlog)]
  - https://github.com/strands-agents/samples ★860 · push 2026-09-21 — Agent samples built using the Strands Agents SDK. [✓ en corpus (github:strands-agents/samples)]
  - https://github.com/agentscope-ai/agentscope-studio ★652 · push 2026-09-02 — A development-oriented visualization toolkit [✓ en corpus (github:agentscope-ai/agentscope-studio)]

esperado: https://github.com/open-telemetry/semantic-conventions-genai https://opentelemetry.io/blog/2025/ai-agent-observability/
confirmado: 

---

## 42 · 5496cd3b · Missing: Qwen Model Integration Development Tools

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Four Qwen AI models exist (image generation, image editing, 3D camera angles, omnimodal) with hundreds of thousands of downloads, but no corresponding developer tooling, debugging interfaces, or integration frameworks appear in this neighborhood. The gap suggests a missing layer between these powerful models and production deployment—no SDKs, no model chaining orchestrators, no prompt management tools specifically for the Qwen ecosystem. This is especially glaring given that collectively these m
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Qwen-Agent https://github.com/QwenLM/Qwen-Agent [✓ en corpus (github:qwenlm/qwen-agent)]
  - Qwen Code
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/open-responses/open-responses ★229 · push 2025-04-02 — Self-hosted alternative to OpenAI's Responses API compatible with Agents SDK and works with all model providers (Claude/R1/Qwen/Ollama etc) [✓ en corpus (github:open-responses/open-responses)]
  - https://github.com/cnblogs/dashscope-sdk ★119 · push 2026-09-14 — An unofficial DashScope（ SDK for .NET maintained by Cnblogs. [✓ en corpus (github:cnblogs/dashscope-sdk)]
  - https://github.com/iimeta/fastapi-sdk ★47 · push 2026-09-20 — 企业级 LLM API 快速集成系统，支持OpenAI、Azure、文心一言、讯飞星火、通义千问、智谱GLM、Gemini、DeepSeek、Anthropic Claude以及OpenAI格式的模型等，简洁的页面风格，轻量高效且稳定，支持Docker一键部署。 [✗ fuera del corpus]
  - https://github.com/oldmanpushcart/dashscope4j ★37 · push 2026-08-31 — 灵积 / 通义千问 Java SDK [✗ fuera del corpus]
  - https://github.com/Younis-Ahmed/qwen-ai-provider ★30 · push 2025-10-27 — Community-built Qwen AI Provider for Vercel AI SDK - Integrate Alibaba Cloud's Qwen models with Vercel's AI application framework [✗ fuera del corpus]

esperado: https://github.com/QwenLM/Qwen-Agent
confirmado: 

---

## 43 · d1025d96 · Missing: Hyperlocal Environmental Action Coordinator

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Arara Watch monitors global disasters, GheiaGrid reimagines urban farming systems, and EcoQuest maps green spaces—all operate at either planetary or infrastructural scale. What's missing is the coordination layer: a tool that translates these macro insights into specific, immediate actions a person can take in their actual neighborhood today. Not monitoring, not systems design, but the 'what should I personally do right now' connector between awareness and hyper-local action.
- Match (mi evaluación): **débil -> posible hueco real**
- Web (curado):
  - solo piezas separadas: VolunTie (voluntariado barrial) https://blog.voluntie.com/neighborhood-associations-and-local-communities/ [✗ fuera del corpus]
  - monitoreo hiperlocal

esperado: https://blog.voluntie.com/neighborhood-associations-and-local-communities/
confirmado: 

---

## 44 · 921e7d74 · Missing: Continuous Testing for Model Drift

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: We have AI drift detection theory, SRE/observability frameworks for agents, static analyzers for code, and parallel test runners for apps—but no one has built the obvious synthesis: a Playwright-style testing framework specifically for detecting behavioral drift in AI systems over time. The gap is a tool that runs versioned test scenarios against models in production, comparing outputs longitudinally and flagging semantic drift before it becomes a reliability incident.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Passmark (regresión con IA sobre Playwright) https://passmark.dev/ [✗ fuera del corpus]
  - DeepEval https://github.com/confident-ai/deepeval [✓ en corpus (github:confident-ai/deepeval)]
  - Deepchecks
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Jwuthri/Tracely-ai ★1360 · push 2026-09-21 — Trace-native CI/CD for AI agents — production failures become regression tests that block the PR. Auto-detect, cluster, freeze into hermetic cases, replay in CI for $0. [✓ en corpus (github:jwuthri/tracely-ai)]
  - https://github.com/hidai25/eval-view ★135 · push 2026-09-05 — Regression testing for AI agents. Snapshot behavior,diff tool calls,catch regressions in CI. Works with LangGraph, CrewAI, OpenAI, Anthropic. [✓ en corpus (github:hidai25/eval-view)]
  - https://github.com/vuphongle/oss-pr-reviewer ★114 · push 2026-08-29 — AI-powered CLI for reviewing GitHub pull requests, detecting potential bugs, security risks, regressions, and missing tests, with structured Markdown reports for open-source maintainers. [✓ en corpus (github:vuphongle/oss-pr-reviewer)]
  - https://github.com/he-yufeng/AgentProbe ★33 · push 2026-09-06 — Drop-in pytest plugin for regression-testing AI agents — snapshot baselines, semantic comparison, mock LLMs [✗ fuera del corpus]
  - https://github.com/Cozymori/VectorWave ★22 · push 2026-08-20 — One decorator for semantic caching + golden-data regression testing of LLM functions (Python). [✓ en corpus (show_hn:46400118)]

esperado: https://github.com/confident-ai/deepeval https://passmark.dev/
confirmado: 

---

## 45 · f594e3c2 · Anime-to-Real Style Transfer Bridge

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: The neighborhood contains specialist anime/manga models (OrangeMixs, waifu-diffusion) and photorealistic models (dreamlike-photoreal, SD3.5, SDXL-Lightning) but nothing that explicitly bridges these aesthetic domains. Given the popularity of both styles and IP-Adapter-FaceID's existence for identity preservation, a model that translates anime character designs into photorealistic renderings while preserving stylistic intent is conspicuously missing. This would serve concept artists, game develop
- Match (mi evaluación): **fuerte (en HF/Civitai, no GitHub)**
- Web (curado):
  - Anything2Real (QwenEdit) https://huggingface.co/lrzjason/QwenEdit-Anything2Real_Alpha [✗ fuera del corpus]
  - Anime-to-Photoreal LoRA https://huggingface.co/Hyperccino/Qwen-Edit-2511-Anime-to-Photoreal-v1.1 [✗ fuera del corpus]
  - Anime2Reality (Civitai)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/TachibanaYoshino/AnimeGAN ★4607 · push 2022-08-03 — A Tensorflow implementation of AnimeGAN for fast photo animation  ! This is the Open source of the paper 「AnimeGAN: a novel lightweight GAN for photo animation」, which uses the GAN framwork to transfo [✓ en corpus (github:tachibanayoshino/animegan)]
  - https://github.com/the-database/mpv-AnimeJaNai ★743 · push 2026-09-19 — Real-time anime upscaling to 4K in mpv with lightweight super-resolution models [✓ en corpus (github:the-database/mpv-animejanai)]
  - https://github.com/sweetbbak/toru ★390 · push 2024-10-24 — Bittorrent streaming CLI tool. Stream anime torrents, real-time with no waiting for downloads.  [✓ en corpus (github:sweetbbak/toru)]
  - https://github.com/goldhuang/SRGAN-PyTorch ★87 · push 2018-12-15 — A PyTorch implementation of SRGAN specific for Anime Super Resolution based on "Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network". And another PyTorch WGAN-gp imple [✗ fuera del corpus]
  - https://github.com/tan5o/anime2clothing ★76 · push 2020-08-28 — Pytorch official implementation of Anime to Real Clothing: Cosplay Costume Generation via Image-to-Image Translation. [✗ fuera del corpus]

esperado: https://huggingface.co/lrzjason/QwenEdit-Anything2Real_Alpha https://huggingface.co/Hyperccino/Qwen-Edit-2511-Anime-to-Photoreal-v1.1
confirmado: 

---

## 46 · 4ea0e1e6 · Climate Awareness Without Climate Action Infrastructure

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Four Earth Day projects focus on monitoring, visualizing, and gamifying climate data, but none provide tools for users to take direct action or measure personal impact reduction. They diagnose but don't prescribe—showing the problem without connecting to carbon footprint calculators, offset purchasing, behavioral change tracking, or local action networks. The missing piece is a "climate action OS" that turns awareness into measurable, personalized intervention.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Earth Hero (acciones + tracker) https://play.google.com/store/apps/details?id=com.earthheroorg.earthhero [✗ fuera del corpus]
  - Klima https://klima.com/ [✓ en corpus (show_hn:25360861)]
  - De-Carbonify https://github.com/kylen21/DeCarbonify [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/NMF-earth/nmf-app ★539 · push 2026-03-13 — Understand and reduce your carbon footprint 🌱 iOS & Android. [✓ en corpus (github:nmf-earth/nmf-app)]
  - https://github.com/Daminoup88/WattSeal ★203 · push 2026-09-23 — Real-time PC power consumption monitor - see watts per app & per component, track your carbon footprint & electricity cost. [✓ en corpus (github:daminoup88/wattseal)]
  - https://github.com/yogakalyaani40-cloud/smart-carbon-footprint-tracker ★51 · push 2026-02-12 — A web-based carbon footprint tracking system that calculates, visualizes, and helps reduce personal carbon emissions using daily activity data. [✗ fuera del corpus]
  - https://github.com/mesutdmn/Carbon-Footprint-Calculator-App ★33 · push 2024-10-01 — The Carbon Footprint Calculator project is a user-friendly web application designed to empower individuals to assess and understand their environmental impact. [✗ fuera del corpus]
  - https://github.com/suvnshr/C1O2 ★22 · push 2021-10-31 — A futuristic app which calculates your carbon footprint due to Travel, Food and Household activities. Gives you tips to reduce your carbon footprints. [✗ fuera del corpus]

esperado: https://klima.com/ https://play.google.com/store/apps/details?id=com.earthheroorg.earthhero https://github.com/kylen21/DeCarbonify
confirmado: 

---

## 47 · ecfdef76 · Missing: Real-Time Carbon Cost Dashboard for Developers

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Four Earth Day projects address environmental awareness (spending tracking, AI futures, code minimalism, token reduction) but none provides real-time feedback during development itself. What's missing is a tool that shows developers the carbon cost of their code as they write it—tracking API calls, token usage, database queries, and compute time—turning environmental impact from a philosophical concern into immediate actionable metrics in the IDE.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - CodeCarbon + extensión VS Code (emisiones en vivo en la barra de estado) https://github.com/mlco2/vscode-extension-codecarbon [✗ fuera del corpus]
  - Carbonara (plugin de editor)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Root-Branch/cardamon-core ★42 · push 2026-03-01 — 🌱 A tool for measuring the power consumption and carbon footprint of your software. [✗ fuera del corpus]
  - https://github.com/TaylorPrewitt/carbon-awareAPI ★25 · push 2021-11-11 — Increasing carbon efficiency and footprint awareness for software applications.  [✗ fuera del corpus]
  - https://github.com/Green-Software-Foundation/if-carmen ★22 · push 2026-08-25 — Implement the Impact Framework at scale to measure the carbon footprint of cloud-based software at both infrastructure and application levels. [✗ fuera del corpus]
  - https://github.com/chandrakant6492/DeDuCE ★15 · push 2026-04-24 — Code for Deforestation Driver and Carbon Emission (DeDuCE) model [✗ fuera del corpus]
  - https://github.com/SDIAlliance/carbon-footprint-ssa ★12 · push 2022-06-18 — A framework for assessing the carbon footprint of server-side software applications (SSA). [✗ fuera del corpus]

esperado: https://github.com/mlco2/vscode-extension-codecarbon
confirmado: 

---

## 48 · 9f85e76d · Missing: Self-Hosted SLAM Orchestration for Edge Robotics

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: Headscale enables self-hosted mesh networking, Coolify orchestrates self-hosted app deployment, and Wazuh provides self-hosted security monitoring. Yet ORB-SLAM3 stands isolated—no self-hosted orchestration layer exists for deploying, managing, and securing SLAM workloads across distributed robotics fleets. The pattern of taking cloud-dependent infrastructure and making it self-hostable hasn't reached spatial computing and robotics deployment pipelines.
- Match (mi evaluación): **débil-parcial (no hay capa de orquestación self-hosted para flotas)**
- Web (curado):
  - solo imágenes Docker de ORB-SLAM3 (ORB-SLAM3-ROS2-Docker) https://github.com/suchetanrs/ORB-SLAM3-ROS2-Docker [✓ en corpus (github:suchetanrs/orb-slam3-ros2-docker)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Airbotics/backend ★5 · push 2023-08-14 — Open-source backend for robotics fleet management. [✗ fuera del corpus]
  - https://github.com/aws-samples/ros2-ota-firmware-updates ★5 · push 2026-09-13 — Reference implementation for Over-The-Air (OTA) firmware updates for ROS2-based robotics fleets using AWS IoT Jobs, Greengrass v2, and Docker. Includes automated deployment tracking, rollback capabili [✗ fuera del corpus]

esperado: https://github.com/suchetanrs/ORB-SLAM3-ROS2-Docker
confirmado: 

---

## 49 · 7fe437a5 · Missing: Privacy-Preserving Identity Primitives

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: The neighborhood shows failed centralized verification alongside open model proliferation, but lacks the cryptographic middle ground: zero-knowledge proofs, age tokens, or decentralized identity systems that could verify attributes without surveillance. What's absent is the technical infrastructure that makes verification possible without creating honeypots of personal data or relying on easily-broken apps.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Google longfellow-zk (ZKP de edad open source) https://www.helpnetsecurity.com/2025/07/03/google-zero-knowledge-proofs-zkp/ [✗ fuera del corpus]
  - blueprint de verificación de edad de la UE
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/mozilla/multi-account-containers ★3146 · push 2026-09-22 — Firefox Multi-Account Containers lets you keep parts of your online life separated into color-coded tabs that preserve your privacy. Cookies are separated by container, allowing you to use the web wit [✓ en corpus (github:mozilla/multi-account-containers)]
  - https://github.com/motiful/cc-gateway ★3045 · push 2026-04-02 — AI API identity gateway — reverse proxy that normalizes device fingerprints and telemetry for privacy-preserving API proxying [✓ en corpus (github:motiful/cc-gateway)]
  - https://github.com/w3c-fedid/FedCM ★472 · push 2026-08-01 — A privacy preserving identity exchange Web API [✓ en corpus (github:w3c-fedid/fedcm)]
  - https://github.com/anon-aadhaar/anon-aadhaar ★252 · push 2025-04-21 — Anon Aadhaar is a zero-knowledge protocol that allows Aadhaar ID owners to prove their identity in a privacy preserving way. [✓ en corpus (github:anon-aadhaar/anon-aadhaar)]
  - https://github.com/liqd/thentos ★55 · push 2016-11-23 · archivado — A tool for privacy-preserving identity management (PPIM) [✗ fuera del corpus]

esperado: https://www.helpnetsecurity.com/2025/07/03/google-zero-knowledge-proofs-zkp/
confirmado: 

---

## 50 · bdba92b5 · Missing: Self-Hosted Environmental Impact Analytics Platform

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: This neighborhood contains open-source alternatives to commercial platforms (Qualtrics, Tailscale, Laravel eCommerce/admin) alongside Earth Day hackathon projects calculating environmental impact. The gap is glaring: there's no self-hosted, open-source platform for businesses to track and analyze their environmental footprint with the same sovereignty and customizability these tools offer for surveys, networking, and commerce. The Laravel ecosystem (Bagisto, Filament) proves demand for business 
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Kabaun (gestión de carbono open source, self-hosted) https://www.kabaun.com/en/open-source [✗ fuera del corpus]
  - topic carbon-accounting
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/ibuilder/massing ★139 · push 2026-09-18 — Open, self-hosted, IFC-native AEC platform: web BIM viewer + modeling, a ~100-module GC portal (RFIs, pay apps, CPM, construction accounting — double-entry GL/WIP → QuickBooks, e-sign), AI assist, IDS [✓ en corpus (github:ibuilder/massing)]
  - https://github.com/RuminantFarmSystems/RuFaS ★40 · push 2026-09-23 — Ruminant Farm Systems (RuFaS) is an open-source, next-generation, whole-farm modeling environment that simulates dairy farm production and environmental impact. [✗ fuera del corpus]
  - https://github.com/DigitalPebble/spruce ★28 · push 2026-09-11 — SPRUCE is an open-source  enrichment platform for GreenOps which helps quantify and reduce the environmental impact of cloud computing. [✗ fuera del corpus]
  - https://github.com/Stellar-IndigoPay/Stellar-IndigoPay ★27 · push 2026-09-13 — Stellar-IndigoPay is an open-source climate donation platform built on the Stellar network. Donors give XLM directly to verified environmental projects — funds never touch a custodian. Every donation  [✗ fuera del corpus]

esperado: https://www.kabaun.com/en/open-source
confirmado: 

---

## 51 · dfaf3d15 · Missing: Synthetic Identity Degradation Tools

- Constellate: snapshot sin fecha (jul-2026) · sin verificar
- Idea: The neighborhood contains precise reconstruction and synthesis of human signatures (3D behavior, speech editing, TTS control) but lacks tools for intentional degradation—systems that let users strategically reduce the fidelity of their digital traces. Given SocialMirror's reconstruction capabilities and speech synthesis precision, there's a clear gap for consumer-facing tools that add controlled noise, temporal jitter, or biometric anonymization before data leaves devices.
- Match (mi evaluación): **fuerte (herramientas de investigación)**
- Web (curado):
  - Fawkes (cloaking de caras) https://en.wikipedia.org/wiki/Fawkes_(software) [✗ fuera del corpus]
  - V-CLOAK (anonimización de voz, USENIX'23) https://www.usenix.org/system/files/usenixsecurity23-deng-jiangyi-v-cloak.pdf [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/hukkelas/DeepPrivacy ★1315 · push 2023-11-19 — DeepPrivacy: A Generative Adversarial Network for Face Anonymization [✓ en corpus (github:hukkelas/deepprivacy)]
  - https://github.com/DigitalPhonetics/speaker-anonymization ★105 · push 2025-07-04 — Speaker anonymization pipeline for hiding the identity of the speaker of a recording by changing the voice in it. [✓ en corpus (github:digitalphonetics/speaker-anonymization)]
  - https://github.com/Plachtaa/StreamVoiceAnon ★95 · push 2026-06-23 — [ICASSP'26] Real-time streaming voice anonymization & voice conversion [✗ fuera del corpus]
  - https://github.com/Voice-Privacy-Challenge/Voice-Privacy-Challenge-2022 ★69 · push 2026-07-13 — Baseline Recipe for VoicePrivacy Challenge 2022: anonymization systems and evaluation software [✗ fuera del corpus]
  - https://github.com/Voice-Privacy-Challenge/Voice-Privacy-Challenge-2024 ★63 · push 2026-07-13 — Baseline Recipe for VoicePrivacy Challenge 2024: anonymization systems and evaluation software  [✗ fuera del corpus]

esperado: https://en.wikipedia.org/wiki/Fawkes_(software https://www.usenix.org/system/files/usenixsecurity23-deng-jiangyi-v-cloak.pdf
confirmado: 

---

## 52 · 6eb5b382 · Everyone builds agents; nobody builds agent identity

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood contains agent protocols, agentic workflows, agent orchestration, a secret scanner for humans' mistakes, and a tunnel client for secure access. What's structurally missing is the piece all of these imply: credential and identity management for autonomous agents — scoped, revocable, auditable secrets that agents can use without leaking them. Gitleaks catches human-committed secrets; nothing here prevents an agent with workflow permissions from exfiltrating or misusing them. Give
- Match (mi evaluación): **fuerte**
- Web (curado):
  - ZeroID (identidad open source para agentes, delegación RFC 8693) https://www.helpnetsecurity.com/2026/04/13/zeroid-open-source-identity-platform-autonomous-ai-agents/ [✗ fuera del corpus]
  - OpenAgents AgentID
  - Ory
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/ComposioHQ/composio ★30292 · push 2026-09-23 — Composio powers 1000+ toolkits, tool search, context management, authentication, and a sandboxed workbench to help you build AI agents that turn intent into action. [✓ en corpus (github:composiohq/composio)]
  - https://github.com/GetBindu/Bindu ★9820 · push 2026-09-06 — Bindu: The identity, communication, and payments layer for AI agents. [✓ en corpus (github:getbindu/bindu)]
  - https://github.com/microsoft/agent-governance-toolkit ★6318 · push 2026-09-23 — AI Agent Governance Toolkit — Policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering for autonomous AI agents. Covers 10/10 OWASP Agentic Top 10. [✓ en corpus (github:microsoft/agent-governance-toolkit)]
  - https://github.com/letta-ai/letta-code ★3409 · push 2026-09-23 — Stateful agents that are like people, with memory, identity, and the ability to learn and adapt [✓ en corpus (github:letta-ai/letta-code)]
  - https://github.com/awslabs/agentcore-samples ★3395 · push 2026-09-22 — Amazon Bedrock Agentcore accelerates AI agents into production with the scale, reliability, and security, critical to real-world deployment. [✓ en corpus (github:awslabs/agentcore-samples)]

esperado: https://www.helpnetsecurity.com/2026/04/13/zeroid-open-source-identity-platform-autonomous-ai-agents/
confirmado: 

---

## 53 · 1e7eb5cb · Missing: A Blast-Radius Firewall for Coding Agents

- Constellate: 2026-07-31 · sin verificar; prior-art manual en `rubric-test/absence-1e7eb5cb.md`
- Idea: We have the symptom (agent modifies three pages outside its spec), the theory (agents need FSM-style constraints), the consequence (silent pipeline failures, AI-generated legacy code), and the audit failure (gates that don't catch sequences). What's absent is the obvious product: a tool that enforces a declared scope on agent edits — file allowlists, diff-radius limits, automatic rejection of out-of-spec changes at commit time. Every idea here circles the need for externally enforced boundaries,
- Match (mi evaluación): **parcial (no un "firewall" atado a la spec)**
- Web (curado):
  - solo guías/controles (sandbox, path allowlists, permisos de Claude Code) https://aurascape.ai/answers/ai-coding-agent-permissions-files-shell-git-cloud/ [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/kenryu42/cc-safety-net ★1555 · push 2026-09-23 — A pre-execution guard for AI coding agents. It blocks destructive Git and file system commands, plus common attempts to access sensitive files, before a tool call runs. Supports Amp Code, Antigravity  [✓ en corpus (github:kenryu42/cc-safety-net)]

esperado: https://aurascape.ai/answers/ai-coding-agent-permissions-files-shell-git-cloud/
confirmado: 

---

## 54 · 82197c7d · Missing: a red-team benchmark for agent security

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood has agent governance tooling, real breach post-mortems, a personal attack suite that broke its own defenses, a general agent evaluation framework, and a culture of pre-registered benchmarks. What's conspicuously absent is the connective piece: a standardized, reproducible adversarial benchmark that scores agent deployments against sequence-composition and privilege-escalation attacks the way OWASP scores web apps. Everyone here is either defending, attacking, or evaluating—nobod
- Match (mi evaluación): **fuerte**
- Web (curado):
  - AgentDojo (benchmark de prompt injection para agentes) https://github.com/ethz-spylab/agentdojo [✓ en corpus (github:ethz-spylab/agentdojo)]
  - AgentDojo-Inspect (NIST)
  - DTap
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/BitterSecurity/Decepticon ★5577 · push 2026-09-19 — Autonomous Hacking Agent for Red Team [✓ en corpus (github:bittersecurity/decepticon)]
  - https://github.com/FunnyWolf/Viper ★5313 · push 2026-05-31 — Adversary simulation and Red teaming platform with AI [✓ en corpus (github:funnywolf/viper)]
  - https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming ★3652 · push 2026-09-18 — A repo for jailbreaking various LLMs, mainly Claude [✓ en corpus (github:goochbeater/spiritual-spell-red-teaming)]
  - https://github.com/confident-ai/deepteam ★2933 · push 2026-09-21 — DeepTeam is a framework to red team LLMs and AI agents. [✓ en corpus (github:confident-ai/deepteam)]
  - https://github.com/msoedov/agentic_security ★2005 · push 2026-09-22 — Agentic LLM Vulnerability Scanner / AI red teaming kit 🧪 [✓ en corpus (github:msoedov/agentic_security)]

esperado: https://github.com/ethz-spylab/agentdojo
confirmado: 

---

## 55 · fbe3c4c2 · Skills Get Made and Listed, Never Tested

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood has a full skill supply chain: automated generation from books, industrial prompt-template mining, packaging into agent runtimes via MCP, and curation lists. What's structurally missing is the quality layer: nothing here evaluates, benchmarks, or certifies whether a skill actually works, is safe, or degrades across model versions. As skills become distributable artifacts, an 'npm audit / CI for agent skills' is the obvious gap that lists alone can't fill.
- Match (mi evaluación): **fuerte**
- Web (curado):
  - mcp-probe (CLI que puntúa servidores MCP antes de publicar) https://dev.to/incultnitollc/the-mcp-server-pre-publish-checklist-5h4e [✗ fuera del corpus]
  - MCP Inspector
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/seleniumbase/SeleniumBase ★13032 · push 2026-09-22 — Browser automation, web scraping, and testing. CDP Mode provides a Stealthy Chromium instance that bypasses bot-detection systems. Includes an MCP server. [✓ en corpus (github:seleniumbase/seleniumbase)]
  - https://github.com/modelcontextprotocol/inspector ★10930 · push 2026-09-23 — Visual testing tool for MCP servers [✓ en corpus (github:modelcontextprotocol/inspector)]
  - https://github.com/deanpeters/Product-Manager-Skills ★7050 · push 2026-09-01 — Product Management skills framework built on battle-tested methods for Claude Code, Cowork, Codex, and AI agents. [✓ en corpus (github:deanpeters/product-manager-skills)]
  - https://github.com/addyosmani/web-quality-skills ★2827 · push 2026-08-24 — Agent Skills for optimizing web quality based on Lighthouse and Core Web Vitals. [✓ en corpus (github:addyosmani/web-quality-skills)]
  - https://github.com/FrancyJGLisboa/agent-skills-platform ★2403 · push 2026-09-15 — Build tested agent skills and govern their lifecycle through a user-defined marketplace: evidence, discovery, updates, rollback, quarantine, and 17-platform distribution. [✓ en corpus (github:francyjglisboa/agent-skills-platform)]

esperado: https://dev.to/incultnitollc/the-mcp-server-pre-publish-checklist-5h4e
confirmado: 

---

## 56 · fa53f5d2 · Missing: CI for Agent Behavior, Not Model Outputs

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood has execution-failure evidence, a benchmark, training environments, and testing techniques battling flakiness — but no continuous, developer-facing tool that runs agents through realistic stateful scenarios on every model or prompt change and flags execution-layer regressions. Everyone diagnoses the gap between static metrics and agentic behavior; nobody in this set ships the 'pytest for agents' that closes it. Given the pieces already exist (env generation, semantic UI hooks, f
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Agent CI https://agent-ci.com/ [✓ en corpus (show_hn:45464765)]
  - Galileo eval gates en CI https://galileo.ai/blog/continuous-integration-ci-ai-fundamentals [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/promptfoo/promptfoo ★25383 · push 2026-09-23 — Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line  [✓ en corpus (github:promptfoo/promptfoo)]
  - https://github.com/GoogleCloudPlatform/agent-starter-pack ★6559 · push 2026-07-21 — Ship AI Agents to Google Cloud in minutes, not months. Production-ready templates with built-in CI/CD, evaluation, and observability. [✓ en corpus (github:googlecloudplatform/agent-starter-pack)]
  - https://github.com/qawolf/cli ★3450 · push 2026-09-22 — QA Wolf from anywhere — your terminal, your CI, your AI agent. [✓ en corpus (github:qawolf/cli)]
  - https://github.com/antonbabenko/terraform-skill ★2377 · push 2026-07-03 — Terraform & OpenTofu Skill for AI Agents - testing, modules, CI/CD, and production patterns [✓ en corpus (github:antonbabenko/terraform-skill)]
  - https://github.com/Jwuthri/Tracely-ai ★1360 · push 2026-09-21 — Trace-native CI/CD for AI agents — production failures become regression tests that block the PR. Auto-detect, cluster, freeze into hermetic cases, replay in CI for $0. [✓ en corpus (github:jwuthri/tracely-ai)]

esperado: https://agent-ci.com/ https://galileo.ai/blog/continuous-integration-ci-ai-fundamentals
confirmado: 

---

## 57 · 80942ef6 · Missing: A CI/CD Certification Suite for Agent Skills

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood contains skill-use verification, skill compilation, blind-spot discovery, readiness philosophy, and a production benchmark — but no tooling that ties them into a developer workflow. What's absent is a 'pytest for agent skills': a CI harness that runs counterfactual ablations, checks that skills causally alter decisions, enforces typed control flow, and gates deployment on readiness metrics. Every ingredient exists as research; nobody has shipped the practitioner tool. This is th
- Match (mi evaluación): **fuerte**
- Web (curado):
  - SkillCheck (valida Agent Skills contra el estándar, en CI) https://www.getskillcheck.com/ [✗ fuera del corpus]
  - plugin validate del marketplace
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/sickn33/agentic-awesome-skills ★46811 · push 2026-09-22 — AAS Core is the local, agent-first control plane for complete catalog discovery, agent-owned selection, stack validation, and planning, backed by 2,445+ agentic skills. Includes CLI, local MCP, catalo [✓ en corpus (github:sickn33/agentic-awesome-skills)]
  - https://github.com/K-Dense-AI/scientific-agent-skills ★46183 · push 2026-09-21 — Turn any AI agent into an AI Scientist. The #1 Agent Skills library for science, used by 190,000+ scientists worldwide. 165 ready-to-use validated skills plus 100+ scientific databases covering biolog [✓ en corpus (github:k-dense-ai/scientific-agent-skills)]
  - https://github.com/microsoft/SkillOpt ★17377 · push 2026-09-05 — SkillOpt is a text-space optimizer that trains reusable natural-language skills for frozen LLM agents through trajectory-driven edits, validation-gated updates, and deployable best_skill.md artifacts. [✓ en corpus (github:microsoft/skillopt)]
  - https://github.com/deanpeters/Product-Manager-Skills ★7050 · push 2026-09-01 — Product Management skills framework built on battle-tested methods for Claude Code, Cowork, Codex, and AI agents. [✓ en corpus (github:deanpeters/product-manager-skills)]
  - https://github.com/tech-leads-club/agent-skills ★6669 · push 2026-09-20 — The secure, validated skill registry for professional AI coding agents. Extend Antigravity, Claude Code, Cursor, Copilot and more with absolute confidence. [✓ en corpus (github:tech-leads-club/agent-skills)]

esperado: https://www.getskillcheck.com/
confirmado: 

---

## 58 · ba4a9968 · Companion AI Has No Wellbeing Monitor

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood contains self-hosted AI companions, evaluation of role-play agents for emotional comfort, voice-based psychotherapy training, and speech biomarkers for depression. The missing piece is obvious once laid out: a passive layer that applies clinical speech-biomarker detection inside companion/role-play conversations to flag deteriorating user mental health and adapt or escalate. Everything needed exists — the intimate voice channel, the eval frameworks, the biomarkers — but no one 
- Match (mi evaluación): **parcial (investigación, no producto desplegado)**
- Web (curado):
  - SHIELD (supervisor LLM que detecta dinámicas emocionales riesgosas en companions; paper) https://arxiv.org/pdf/2510.15891 [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Okes2024/Building-a-Chatbot-for-Mental-Health-Support ★59 · push 2025-09-23 — This project demonstrates building a synthetic mental health support chatbot. It generates a labeled dataset, trains an intent classifier, and implements a safety-first conversational engine with empa [✗ fuera del corpus]
  - https://github.com/Institute4FutureHealth/MentalHealthSafetyEval ★9 · push 2024-11-10 — Building Trust in Mental Health Chatbots: Safety Metrics and LLM-Based Evaluation Tools [✗ fuera del corpus]

esperado: https://arxiv.org/pdf/2510.15891
confirmado: 

---

## 59 · e3b4803b · Missing: The On-Device Mobile Agent Runtime

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood has agent languages, agent protocols, JVM agent frameworks, and AI assistants embedded in desktop tools (Xcode, macOS video editing). It also has a dense cluster of native iOS/Android apps. Yet nothing bridges them: there is no native, privacy-first agent runtime that runs on the phone itself, the way Harper does grammar checking offline. Given the local-first ethos of the surrounding projects (Harper, Bitwarden, UTM), an on-device Swift/Kotlin agent host implementing the agent
- Match (mi evaluación): **fuerte (control del teléfono; LLM on-device no necesariamente)**
- Web (curado):
  - Mobilerun (runtime de agentes para Android/iOS) https://mobilerun.ai/framework/ [✗ fuera del corpus]
  - mobile-use https://github.com/minitap-ai/mobile-use [✓ en corpus (github:minitap-ai/mobile-use)]
  - agent-device https://github.com/callstack/agent-device [✓ en corpus (github:callstack/agent-device)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/droidrun/mobilerun ★9441 · push 2026-09-16 — Automate your mobile devices with natural language commands - an LLM agnostic mobile Agent 🤖 [✓ en corpus (github:droidrun/mobilerun)]
  - https://github.com/AAswordman/Operit ★8081 · push 2026-09-22 — The most powerful AI agent and AI chat software on Android/Operit是一款Android上能力最为强大、发展最久的AI Agent [✓ en corpus (github:aaswordman/operit)]
  - https://github.com/rikkahub/rikkahub ★7797 · push 2026-09-22 — RikkaHub is an Android APP that supports for multiple LLM providers. [✓ en corpus (github:rikkahub/rikkahub)]
  - https://github.com/omnimind-ai/OmniBot ★2008 · push 2026-09-23 — Your on-phone / mobile AI Agent / Claw, capable of operating terminals and performing a wide range of tasks in the Android world || 你的手机 AI 代理，她可以操作终端，也可以完成 Android 世界的广泛任务  [✓ en corpus (github:omnimind-ai/omnibot)]
  - https://github.com/kellyvv/PhoneClaw ★1262 · push 2026-08-06 — PhoneClaw turns phones into local AI agent runtimes with on-device models, native mobile Skills, LiveLand, and optional Mac Gateway inference. [✓ en corpus (github:kellyvv/phoneclaw)]

esperado: https://github.com/minitap-ai/mobile-use https://github.com/callstack/agent-device https://mobilerun.ai/framework/
confirmado: 

---

## 60 · a0dfabb1 · Missing: mission control for swarms of local agents

- Constellate: 2026-07-31 · sin verificar
- Idea: Goose runs autonomous agents, worktrunk manages git worktrees explicitly for parallel agent workflows, jcode optimizes the harness for RAM efficiency, and Vector pipes observability data at scale — yet nothing here watches, compares, or arbitrates between the parallel agents these tools clearly anticipate. The gap is an agent-fleet observability and orchestration layer: which of my 8 concurrent agent branches is winning, what did each cost, when should one be killed. Every piece of the substrate
- Match (mi evaluación): **fuerte**
- Web (curado):
  - mission-control (Builderz, control plane self-hosted) https://github.com/builderz-labs/mission-control [✓ en corpus (github:builderz-labs/mission-control)]
  - Agent-Dashboard https://github.com/toliko-coding/Agent-Dashboard [✗ fuera del corpus]
  - Claude Code Agent View
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/smtg-ai/claude-squad ★8523 · push 2026-08-20 — Manage multiple AI terminal agents like Claude Code, Codex, OpenCode, and Amp. [✓ en corpus (github:smtg-ai/claude-squad)]
  - https://github.com/agent-of-empires/agent-of-empires ★3283 · push 2026-09-22 — Manage multiple Claude Code, OpenCode agents from either TUI or Web for easy access on mobile. Also supports Mistral Vibe, Codex CLI, Gemini CLI, Pi.dev, Copilot CLI, Factory Droid Coding. [✓ en corpus (github:agent-of-empires/agent-of-empires)]
  - https://github.com/chriswritescode-dev/opencode-manager ★884 · push 2026-09-20 — Mobile-first web interface for OpenCode AI agents. Manage, control, and code with multiple OpenCode agents from any device - your phone, tablet, or desktop. Features Git integration, file management,  [✓ en corpus (github:chriswritescode-dev/opencode-manager)]
  - https://github.com/crossoverJie/SkillDeck ★565 · push 2026-09-22 — Native macOS SwiftUI app for managing multiple AI code agent skills [✓ en corpus (github:crossoverjie/skilldeck)]
  - https://github.com/mixpeek/amux ★493 · push 2026-09-23 — Open-source control plane for AI coding agents. Run an AI engineering team: parallel Claude Code, Codex, and Gemini workers with a shared board, atomic tasks, schedules, loops, origin-stamped messagin [✓ en corpus (github:mixpeek/amux)]

esperado: https://github.com/builderz-labs/mission-control https://github.com/toliko-coding/Agent-Dashboard
confirmado: 

---

## 61 · 7918616b · Nobody built access control for agent memory

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood has trust scoring (Σ-Mem), value-aware management (MemLens), poisoning tracking (MemSecBench), rollback (ChronoMem), and privacy-conscious storage — yet no idea addresses who and what may read or write which memories: permissions, scopes, provenance-based ACLs per agent, tool, or session. Every security and reliability problem in these papers is downstream of unrestricted write access. The missing piece is an authorization layer for agent memory — essentially IAM for memories — 
- Match (mi evaluación): **parcial (prácticas y features, no capa dedicada)**
- Web (curado):
  - mem0 governance/seguridad de memoria https://mem0.ai/blog/ai-memory-security-best-practices [✗ fuera del corpus]
  - guías MindStudio (tiers con ACL)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/Kocoro-lab/Kocoro ★409 · push 2026-09-05 — A Mac-native AI agent with memory, local computer access, browser control, IM channels, and MCP-native integrations. Built on Shannon. [✓ en corpus (github:kocoro-lab/kocoro)]
  - https://github.com/jin-bo/agentao ★306 · push 2026-09-23 — Local-first, governed AI agent runtime for Python — embed it in your app, or run it as a CLI or ACP server. Permissions, MCP, memory and audit replay built in. [✓ en corpus (github:jin-bo/agentao)]
  - https://github.com/prasenjeet-symon/ogcode ★136 · push 2026-09-21 — An open-source, local-first AI teammate and agent operating environment for turning intent into completed work—with tools, memory, permissions, and human oversight. [✓ en corpus (github:prasenjeet-symon/ogcode)]
  - https://github.com/vstorm-co/pydantic-ai-backend ★129 · push 2026-09-21 — File Storage & Sandbox Backends for Pydantic AI: console tools for file operations, Docker-isolated sandboxes for safe execution, and permission system with presets for access control. Enables secure  [✓ en corpus (github:vstorm-co/pydantic-ai-backend)]
  - https://github.com/ahwurm/localharness ★37 · push 2026-09-21 — An open-source, model-agnostic agent harness for local LLMs. Define agents in YAML (tools, memory, deny-first permissions) and run them against any OpenAI-compatible endpoint: vLLM, Ollama, LM Studio, [✗ fuera del corpus]

esperado: https://mem0.ai/blog/ai-memory-security-best-practices
confirmado: 

---

## 62 · 6ec58e83 · Agents Can Talk Cross-Cloud but Nobody Verifies Who They Are

- Constellate: 2026-07-31 · sin verificar
- Idea: 5156 and 5171 show agent-to-agent protocols working across Google, Azure, and AWS; 4708 shows detectors can't even classify agent traffic; 4621 and 4197 show accountability and threat modeling breaking down under GenAI. The missing piece is an agent identity and attestation layer: verifiable credentials that let a receiving agent or website know which agent, on whose behalf, with what permissions, is calling. Interop is being built faster than identity, and every paper here dances around that ga
- Match (mi evaluación): **fuerte**
- Web (curado):
  - sigstore-a2a (firma de Agent Cards) https://github.com/sigstore/sigstore-a2a [✗ fuera del corpus]
  - propuesta A2A #1672
  - Agent Name Service (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/ComposioHQ/composio ★30292 · push 2026-09-23 — Composio powers 1000+ toolkits, tool search, context management, authentication, and a sandboxed workbench to help you build AI agents that turn intent into action. [✓ en corpus (github:composiohq/composio)]
  - https://github.com/awslabs/agentcore-samples ★3395 · push 2026-09-22 — Amazon Bedrock Agentcore accelerates AI agents into production with the scale, reliability, and security, critical to real-world deployment. [✓ en corpus (github:awslabs/agentcore-samples)]
  - https://github.com/mvanhorn/agentcookie ★835 · push 2026-09-21 — Your agent runs on a Mac that isn't your daily driver. agentcookie keeps its sessions in sync with the Mac you actually browse on, continuously, encrypted over Tailscale, so OpenClaw, Hermes, or any o [✓ en corpus (github:mvanhorn/agentcookie)]
  - https://github.com/cuviper/ssh-pageant ★363 · push 2022-04-28 — An SSH authentication agent for Cygwin/MSYS to PuTTY's Pageant. [✓ en corpus (github:cuviper/ssh-pageant)]
  - https://github.com/dendrite-systems/dendrite-python-sdk ★312 · push 2025-01-08 — Tools to build web AI agents that can authenticate, interact with and extract data from any website. [✓ en corpus (github:dendrite-systems/dendrite-python-sdk)]

esperado: https://github.com/sigstore/sigstore-a2a
confirmado: 

---

## 63 · 07878479 · Missing: The Ambient Home Health Early-Warning Layer

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood contains camera-free WiFi vital sensing, cheap edge-deployable activity recognition, a framework for capturing multimodal ambient human data, longitudinal clinical anomaly scoring, and near-anomaly prediction before failure. Every ingredient exists for a passive, privacy-preserving system that watches a person's daily physiological and behavioral baseline and flags drift before a clinical event — yet no idea in the set connects sensing to longitudinal prediction. The gap is the
- Match (mi evaluación): **parcial-fuerte (sensado sí; capa de alerta temprana longitudinal no del todo)**
- Web (curado):
  - Wi-Fi Sensing de Deutsche Telekom (caídas, respiración/pulso sin cámaras) https://www.telekom.com/en/newsroom/latest-updates/erklaerstuecke/2025/02/wi-fi-sensing [✗ fuera del corpus]
  - WiLife (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/ruvnet/RuView ★94793 · push 2026-09-23 — π RuView turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, and presence detection — all without a single pixel of video. [✓ en corpus (github:ruvnet/ruview)]
  - https://github.com/lucasjosesilva94-a11y/wifi-densepose ★16 · push 2026-03-02 — WiFi DensePose turns commodity WiFi signals into real-time human pose estimation, vital sign monitoring, and presence detection — all without a single pixel of video.  [✗ fuera del corpus]
  - https://github.com/outputlayer/espectre-sense ★5 · push 2026-03-23 — ESP32 WiFi CSI room presence detection, movement tracking, vital signs monitoring & sleep analysis — 3-node triangulation with real-time heatmap visualization [✗ fuera del corpus]

esperado: https://www.telekom.com/en/newsroom/latest-updates/erklaerstuecke/2025/02/wi-fi-sensing
confirmado: 

---

## 64 · 5041f789 · Missing: security-grade observability for MCP agent traffic

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood contains an agent intrusion post-mortem, agent telemetry that shocked its own builders, and a major MCP spec change to stateless transport that makes session-level auditing harder, not easier. What's structurally missing is the piece these four imply: an audit/anomaly-detection layer purpose-built for stateless MCP traffic — a 'flight recorder' for agent-tool interactions. Everyone here is either migrating the protocol or cleaning up after incidents; nobody is building the middl
- Match (mi evaluación): **fuerte**
- Web (curado):
  - NGINX agentic observability (módulo MCP) https://blog.nginx.org/blog/introducing-agentic-observability-in-nginx-real-time-mcp-traffic-monitoring [✗ fuera del corpus]
  - IBM ContextForge https://github.com/IBM/mcp-context-forge [✓ en corpus (github:ibm/mcp-context-forge)]
  - Microsoft MCP Gateway
  - MintMCP
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/hoophq/hoop ★819 · push 2026-09-22 — One gateway in front of every protocol. Same policy across MCP, LLMs, databases and containers. Wire-level enforcement at under 5ms. [✓ en corpus (github:hoophq/hoop)]
  - https://github.com/apache/casbin-gateway ★636 · push 2026-09-19 — Casbin AI & MCP security gateway for HTTP, online demo: https://door.caswaf.com [✓ en corpus (github:apache/casbin-gateway)]
  - https://github.com/TheLunarCompany/lunar ★498 · push 2026-09-22 — lunar.dev: Agent native MCP Gateway for governance and security [✓ en corpus (github:thelunarcompany/lunar)]
  - https://github.com/enkryptai/secure-mcp-gateway ★57 · push 2026-08-24 — Secure MCP Gateway - Setup Admin level gateway functionality for MCP servers - with guardrails at each MCP server to overcome multiple security issues with using MCPs [✗ fuera del corpus]
  - https://github.com/ningzimu/claude-code-lens ★31 · push 2026-05-17 — Local monitor for Claude Code API traffic, logs, prompts, and tools [✗ fuera del corpus]

esperado: https://github.com/IBM/mcp-context-forge https://blog.nginx.org/blog/introducing-agentic-observability-in-nginx-real-time-mcp-traffic-monitoring
confirmado: 

---

## 65 · b36b5f05 · Everyone Generates Synthetic Data, Nobody Certifies It

- Constellate: 2026-07-31 · sin verificar
- Idea: Procedural scratch rendering, self-play driving simulation, generative multi-date stereo data, and point cloud scene generation all manufacture training data because real annotations are scarce. Yet the neighborhood contains no method for validating that synthetic distributions actually transfer — each pipeline assumes its own realism. The missing piece is a sim-to-real fidelity auditor: a tool that scores a synthetic dataset's predictive value for a target deployment domain before you spend GPU
- Match (mi evaluación): **parcial-fuerte (tabular; no imágenes/nubes de puntos)**
- Web (curado):
  - SDMetrics Quality Report https://github.com/sdv-dev/SDMetrics [✓ en corpus (github:sdv-dev/sdmetrics)]
  - evaluación holdout (paper)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/human-3d/Human3D ★88 · push 2024-02-25 — We propose the first multi-human body-part segmentation model, called Human3D 🧑‍🤝‍🧑, that directly operates on 3D scenes. In an extensive analysis, we validate the benefits of training on synthetic da [✗ fuera del corpus]
  - https://github.com/Danau5tin/tbench-agentic-data-pipeline ★74 · push 2025-07-28 — Multi-agent synthetic data generation pipeline capable of generating and validating long horizon terminal/coding tasks for RL training [✗ fuera del corpus]
  - https://github.com/Okes2024/Air-Quality-Index-Prediction-Using-ML-and-IoT-Sensor-Data ★69 · push 2025-10-14 — This project simulates IoT sensor data to predict Air Quality Index (AQI) using machine learning. It generates synthetic datasets, computes AQI, trains multiple models, and provides evaluation metrics [✗ fuera del corpus]
  - https://github.com/mirkovicdev/CLUSTERING-MARKET-REGIMES ★68 · push 2025-12-29 — Python implementation of "Clustering Market Regimes Using the Wasserstein Distance" (Horvath et al., 2021). Detects bull/bear market regimes using optimal transport distance on return distributions.   [✗ fuera del corpus]
  - https://github.com/schneiderkamplab/syntheval ★44 · push 2026-06-18 — Software for evaluating the quality of synthetic data compared with real data. [✗ fuera del corpus]

esperado: https://github.com/sdv-dev/SDMetrics
confirmado: 

---

## 66 · 730e3203 · The missing glue: identity and interop for self-hosted stacks

- Constellate: 2026-07-31 · sin verificar; prior-art manual en `rubric-test/absence-730e3203.md`
- Idea: Four apps that a single clinic, village office, or small business would plausibly run together — files, health/citizen records, invoicing — each with its own users, backups, and auth. The neighborhood's internal structure screams for the missing piece: a lightweight identity/SSO and data-sync layer that lets these self-hosted PHP monoliths behave like one coherent stack. Enterprise answers (Keycloak, LDAP) exist but are wildly over-scoped for the small institutions these tools target. The gap is
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Authentik (SSO para stack self-hosted) https://github.com/goauthentik/authentik [✓ en corpus (github:goauthentik/authentik)]
  - Zitadel
  - Kopia para backups
  - YunoHost

esperado: https://github.com/goauthentik/authentik
confirmado: 

---

## 67 · 47bf5f9f · No one monetizes backendless software

- Constellate: 2026-07-31 · sin verificar; prior-art manual en `rubric-test/absence-47bf5f9f.md`
- Idea: The neighborhood contains fully client-side apps and self-hosted commerce/payment stacks that all assume a PHP server. What's missing is the bridge: a monetization/licensing layer for zero-backend software — selling license keys, unlocks, or subscriptions for apps that have no server to validate against. The backendless builders explicitly avoid servers, while the payment tools require them, leaving indie devs of local-first tools with no native way to charge. A lightweight license-key + edge-ve
- Match (mi evaluación): **fuerte (coincide con el "yes" de constellate)**
- Web (curado):
  - Dodo Payments (license keys sin backend) https://dodopayments.com/blogs/monetize-chrome-extension [✗ fuera del corpus]
  - Monetize.software https://monetize.software/en [✗ fuera del corpus]
  - LicenseSeat
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/michealbalogun/Horizon-dashboard ★23 · push 2019-05-06 —  Copyright 2012 United States Government as represented by the # Administrator of the National Aeronautics and Space Administration. # All Rights Reserved. # # Copyright 2012 Nebula, Inc. # #    Licen [✗ fuera del corpus]
  - https://github.com/amir2510/script ★18 · push 2018-02-20 — <!DOCTYPE html>  <html lang="en" dir="ltr" data-cast-api-enabled="true"> <head><meta name="viewport" content="width=device-width, initial-scale=1"><style name="www-roboto" >@font-face{font-family:'Rob [✗ fuera del corpus]

esperado: https://dodopayments.com/blogs/monetize-chrome-extension https://monetize.software/en
confirmado: 

---

## 68 · 69926e60 · Missing: Deliberate Skill-Building Tooling for the Post-AI Junior

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood diagnoses the broken junior pipeline, questions whether learning to code still matters, notes that understanding beats origin, and observes that AI made knowledge cheap but the 'joins' — architectural judgment — expensive. Even LLM-generated code tours only address onboarding, not skill formation. What's conspicuously absent is a product that deliberately trains the judgment layer: tools that force juniors to predict, verify, and debug AI output rather than accept it, converting
- Match (mi evaluación): **débil -> posible hueco real**
- Web (curado):
  - solo debate/investigación (Anthropic sobre skills) https://www.anthropic.com/research/AI-assistance-coding-skills [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/MedUnes/go-kata ★2357 · push 2026-07-09 — A collection of daily coding challenges designed to help you master idiomatic Go through deliberate, repetitive practice. [✓ en corpus (github:medunes/go-kata)]
  - https://github.com/Commando-X/vuln-bank ★933 · push 2026-09-22 — A deliberately vulnerable banking application designed for practicing Security Testing of Web App, APIs, AI integrated App and secure code reviews. Features common vulnerabilities found in real-world  [✓ en corpus (github:commando-x/vuln-bank)]
  - https://github.com/dnuffer/dpcode ★47 · push 2018-02-21 — My deliberate practice code [✗ fuera del corpus]
  - https://github.com/Dheeraj-02NK/Machice-Learning-Fundamentals ★14 · push 2024-04-02 — Machine Learning (ML) is a field of artificial intelligence (AI) that focuses on developing algorithms and models capable of learning from data to make predictions or decisions without explicit progra [✗ fuera del corpus]
  - https://github.com/weasteam/coursera_machine_learning ★12 · push 2017-01-09 — About this course: Machine learning is the science of getting computers to act without being explicitly programmed. In the past decade, machine learning has given us self-driving cars, practical speec [✗ fuera del corpus]

esperado: https://www.anthropic.com/research/AI-assistance-coding-skills
confirmado: 

---

## 69 · e01b3b33 · Missing: Sync and Monetization Rails for Backendless Apps

- Constellate: 2026-07-31 · sin verificar
- Idea: The no-backend builders here all hit the same walls—frozen tabs, storage limits, no accounts, no way to charge (explicitly catalogued in 5273's 'everything that broke'). The neighborhood is full of fully-client-side tools but contains no infrastructure piece: a lightweight toolkit for licensing, payments, cross-device sync, and WASM/ONNX resource management that preserves the zero-server ethos. That missing layer is what would turn these hobby demos into sellable products, and every author is re
- Match (mi evaluación): **parcial-fuerte (sync sí; sync+cobro en uno no)**
- Web (curado):
  - Replicache/Zero, Jazz, PowerSync, ElectricSQL (sync local-first) https://replicache.dev/ [✗ fuera del corpus]
  - https://github.com/alexanderop/awesome-local-first [✓ en corpus (github:alexanderop/awesome-local-first)]
  - cobros: ver 47bf5f9f (Dodo, Monetize.software)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/anyproto/any-sync ★1717 · push 2026-09-22 — An open-source protocol enabling high-performance, local-first, peer-to-peer, end-to-end encrypted collaborative apps. [✓ en corpus (github:anyproto/any-sync)]
  - https://github.com/LinkoraApp/Linkora ★919 · push 2026-09-12 — Local-first multiplatform link organizer with optional self-hosted sync. [✓ en corpus (github:linkoraapp/linkora)]
  - https://github.com/moneymanagerex/android-money-manager-ex ★710 · push 2026-09-22 — Local-first personal finance app. Encrypted, self-hosted, sync across devices. [✓ en corpus (github:moneymanagerex/android-money-manager-ex)]
  - https://github.com/jackwener/tg-cli ★289 · push 2026-03-15 — A CLI for Telegram — local-first sync, search, export via MTProto [✓ en corpus (github:jackwener/tg-cli)]
  - https://github.com/jaredly/local-first ★225 · push 2026-07-30 — data syncing, storage, and collaboration. that works [✓ en corpus (github:jaredly/local-first)]

esperado: https://github.com/alexanderop/awesome-local-first https://replicache.dev/
confirmado: 

---

## 70 · 246e1998 · Missing: A Portable, Auditable Personal Memory-Permission Layer

- Constellate: 2026-07-31 · sin verificar
- Idea: Personalization work builds ever-richer persistent user state and cross-session memory, while safety work shows authorization must be context-dependent and risks accumulate over trajectories. The obvious missing piece is the intersection: a user-owned memory store with attached, evidence-backed permissions — deciding which agent may read, write, or act on which memories, with audit trails. Everyone here assumes memory exists or permissions exist, but nobody builds the substrate binding them. Thi
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Memory OS (memoria personal portable con permisos por app, revocables) https://mymemoryos.com/ [✗ fuera del corpus]
  - Walrus Memory
  - proyecto Stanford Portable Memory
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/EverMind-AI/EverOS ★13149 · push 2026-09-22 — One portable memory layer for every AI agent: local-first, Markdown-native, user-owned, and self-evolving across apps, tools, and workflows. [✓ en corpus (github:evermind-ai/everos)]
  - https://github.com/campfirein/byterover-cli ★4964 · push 2026-06-25 — ByteRover CLI (brv) - The portable memory layer for  autonomous coding agents (formerly Cipher) [✓ en corpus (github:campfirein/byterover-cli)]
  - https://github.com/kentcdodds/kody ★667 · push 2026-09-23 — 🐨 Your assistant's home — the memory, keys, code, and automations your AI agent keeps, portable across every MCP host. Built on Cloudflare Workers. [✓ en corpus (github:kentcdodds/kody)]
  - https://github.com/atomicstrata/atomicmemory ★430 · push 2026-09-23 — Portable semantic memory for AI agents: core engine, TypeScript SDK, framework adapters, MCP server, CLI, and host plugins. [✓ en corpus (github:atomicstrata/atomicmemory)]
  - https://github.com/santhoshravindran7/portable-agent-memory ★19 · push 2026-08-06 — Portable Agent Memory: Cryptographically-verified memory transfer across heterogeneous AI agents. Open protocol + Python SDK. [✗ fuera del corpus]

esperado: https://mymemoryos.com/
confirmado: 

---

## 71 · c4350d18 · Everyone Detects Anomalies, Nobody Shares the Machinery

- Constellate: 2026-07-31 · sin verificar
- Idea: This neighborhood contains anomaly detectors for pixels, tables, EEG signals, malware binaries, and generated images — each rebuilding notions of normality, thresholds, and drift from scratch. CORE already proves unification pays off within tabular data alone. The missing piece is a modality-agnostic anomaly-detection layer or benchmark suite: shared calibration, threshold-setting, and drift-handling infrastructure that any domain detector plugs into. Its absence is conspicuous given five indepe
- Match (mi evaluación): **fuerte**
- Web (curado):
  - PyOD 3 (tabular, series, grafos, texto, imagen, audio) https://github.com/yzhao062/pyod [✓ en corpus (github:yzhao062/pyod)]
  - RADAR
  - anomalib
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/unit8co/darts ★9523 · push 2026-09-18 — A python library for user-friendly forecasting and anomaly detection on time series. [✓ en corpus (github:unit8co/darts)]
  - https://github.com/AIStream-Peelout/flow-forecast ★2301 · push 2026-09-11 — Deep learning PyTorch library for time series forecasting, classification, and anomaly detection (originally for flood forecasting). [✓ en corpus (github:aistream-peelout/flow-forecast)]
  - https://github.com/pygod-team/pygod ★1495 · push 2024-11-14 — A Python Library for Graph Outlier Detection (Anomaly Detection) [✓ en corpus (github:pygod-team/pygod)]
  - https://github.com/sintel-dev/Orion ★1370 · push 2026-09-21 — Unsupervised time series anomaly detection library [✓ en corpus (github:sintel-dev/orion)]
  - https://github.com/linkedin/luminol ★1231 · push 2025-08-22 — Anomaly Detection and Correlation library [✓ en corpus (github:linkedin/luminol)]

esperado: https://github.com/yzhao062/pyod
confirmado: 

---

## 72 · b7aa36fd · IoT Security Policies Are Verified; Fleets Aren't Orchestrated

- Constellate: 2026-07-31 · sin verificar
- Idea: ESPHome gives per-device configuration, 4318 formally verifies cross-device access-control information flow, and 4176 shows coupled end-to-end policy optimization for distributed networks. The missing piece is obvious once these are aligned: a tool that treats a home or building's IoT fleet as one coupled system — jointly optimizing and verifying device configs, trust boundaries, and automation policies end-to-end rather than device-by-device. Everything needed exists (declarative configs, flow 
- Match (mi evaluación): **parcial (orquestación sí; políticas de seguridad verificadas no)**
- Web (curado):
  - Fleet for ESPHome (flota de dispositivos, pinning, upgrades) https://github.com/weirded/distributed-esphome [✗ fuera del corpus]
  - OpenRemote
  - FleetDM
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/jettbrains/-L- ★160 · push 2021-08-18 — W3C Strategic Highlights  September 2019  This report was prepared for the September 2019 W3C Advisory Committee Meeting (W3C Member link). See the accompanying W3C Fact Sheet — September 2019. For th [✓ en corpus (github:jettbrains/-l-)]

esperado: https://github.com/weirded/distributed-esphome
confirmado: 

---

## 73 · 26d6adce · Missing: One-Click Self-Hosted Business-in-a-Box

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood contains self-hosted storage (Nextcloud AIO shows the packaging pattern), self-hosted invoicing, and an argument that email is now buildable from borrowed parts — yet no idea packages these into a single deployable 'solo business OS.' The AIO installer proves the demand for turnkey bundling exists; the gap is a curated, integrated stack (files + invoicing + email + client portal) for freelancers fleeing SaaS subscriptions. Each component exists; the composition layer doesn't.
- Match (mi evaluación): **parcial**
- Web (curado):
  - solo piezas (InvoiceShelf, Invoice Ninja, Nextcloud AIO) https://invoiceshelf.com/ [✗ fuera del corpus]
  - empaquetado integral: ver YunoHost/Cloudron (197bf4f9)
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/jasoncheng7115/jt-doc-tools ★220 · push 2026-09-23 — An all-in-one PDF and Office document platform: self-hosted, open source, under your control. 整合式 PDF / Office 文件處理平台，自架、開源、可控。 [✓ en corpus (github:jasoncheng7115/jt-doc-tools)]
  - https://github.com/braedonsaunders/openbooks ★13 · push 2026-09-23 — Open-source business suite. Run on open books. [✗ fuera del corpus]
  - https://github.com/kitokoh/leopardo-hr ★13 · push 2026-09-23 — Leopardo — the open-source business suite for field-based companies: HR & payroll, attendance, leave, CRM, accounting and operations, on web, mobile and kiosks. Multi-tenant, self-hostable, with tenan [✗ fuera del corpus]
  - https://github.com/intabia-fusion/platform ★10 · push 2026-09-23 — All-in-one open-source team platform: issue tracking, chat, documents, virtual office and AI. SAAS/Self-hosted. [✗ fuera del corpus]

esperado: https://invoiceshelf.com/
confirmado: 

---

## 74 · a3fb5892 · Missing: Continuous Formal-ish Assurance for Dependencies

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood has supply-chain risk detection, the lament that formal verification is unused, and heavyweight post-hoc analysis — but nothing bridging them. Absent is a lightweight tool that automatically checks behavioral properties of third-party dependencies on update: 'did this new version's API contract or side-effect surface change?' Dependency-Track tells you a component has a known CVE; nothing tells you a component quietly changed behavior. This gap is exactly where supply-chain atta
- Match (mi evaluación): **parcial (SCA sí; garantías "formal-ish" de capacidades no del todo, ver capslock)**
- Web (curado):
  - SCA continuo (Sonar, Socket, FOSSA) https://www.sonarsource.com/solutions/security/sca/ [✗ fuera del corpus]
  - awesome-software-supply-chain-security https://github.com/bureado/awesome-software-supply-chain-security [✓ en corpus (github:bureado/awesome-software-supply-chain-security)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/DependencyTrack/dependency-track ★4229 · push 2026-09-22 — Dependency-Track is an intelligent Component Analysis platform that allows organizations to identify and reduce risk in the software supply chain. [✓ en corpus (github:dependencytrack/dependency-track)]
  - https://github.com/XmirrorSecurity/OpenSCA-cli ★1133 · push 2026-05-15 — OpenSCA is an open source software supply chain security solution that supports the detection of open source dependencies, vulnerabilities and license compliance with a widely noticed accuracy by the  [✓ en corpus (github:xmirrorsecurity/opensca-cli)]
  - https://github.com/bureado/awesome-software-supply-chain-security ★380 · push 2026-06-07 — A compilation of resources in the software supply chain security domain, with emphasis on open source [✓ en corpus (github:bureado/awesome-software-supply-chain-security)]
  - https://github.com/skills/secure-repository-supply-chain ★212 · push 2026-05-30 — Secure your supply chain, understand dependencies in your environment, know about vulnerabilities in those dependencies and patch them [✓ en corpus (github:skills/secure-repository-supply-chain)]
  - https://github.com/dennisdoomen/packageguard ★77 · push 2026-09-23 — Dependency scanner for NuGet and NPM with SBOM, vulnerabilities and risk analysis [✗ fuera del corpus]

esperado: https://github.com/bureado/awesome-software-supply-chain-security https://www.sonarsource.com/solutions/security/sca/
confirmado: 

---

## 75 · 36d540d3 · Missing: Proof-Without-Identity Verification Layer

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood contains the political rejection of digital ID and age verification, the cryptographic machinery for privacy-preserving data collection, and infrastructure for trusted information sharing. What's absent is the piece connecting them: practical anonymous credential tooling — proving attributes (age, membership, non-maliciousness) without revealing identity. The internal structure screams for zero-knowledge attestation as the resolution of the ID-versus-privacy standoff, yet no ide
- Match (mi evaluación): **fuerte**
- Web (curado):
  - Privacy Pass (tokens anónimos)
  - Privado ID/iden3 (ZK, BBS+) https://github.com/iden3 [✗ fuera del corpus]
  - zk-creds (paper, convierte documentos existentes en credenciales anónimas) https://www.cs.umd.edu/~imiers/pdf/zkcreds.pdf [✗ fuera del corpus]
  - ZK-Access https://github.com/farouk-allani/ZK-Access [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/nymtech/nym ★1950 · push 2026-09-22 — Nym provides strong network-level privacy against sophisticated end-to-end attackers, and anonymous transactions using blinded, re-randomizable, decentralized credentials. [✓ en corpus (github:nymtech/nym)]
  - https://github.com/xlab-si/emmy ★238 · push 2022-11-25 — Library for zero-knowledge proof based applications (like anonymous credentials) [✓ en corpus (github:xlab-si/emmy)]
  - https://github.com/asonnino/coconut ★69 · push 2021-01-19 — Coconut: Threshold Issuance Selective Disclosure Credentials with Applications to Distributed Ledgers. [✗ fuera del corpus]
  - https://github.com/whotracksme/anonymous-credentials ★27 · push 2024-06-17 — (sin descripción) [✗ fuera del corpus]
  - https://github.com/cloudflareresearch/anonymous-credentials-agent-demo ★27 · push 2026-04-24 — Demo for Anonymous Credentials Token for Rate-Limiting Agents [✗ fuera del corpus]

esperado: https://github.com/iden3 https://www.cs.umd.edu/~imiers/pdf/zkcreds.pdf https://github.com/farouk-allani/ZK-Access
confirmado: 

---

## 76 · 128b8602 · AI maintenance layer for the legacy PHP long tail

- Constellate: 2026-07-31 · sin verificar
- Idea: laravel/boost shows AI tooling arriving for modern PHP, while frontier models (DeepSeek-V4-Flash, MAI-Cyber-1) get cheap and specialized. Meanwhile the actual pain lives in ideas like the WooCommerce free-trial debugging saga and sprawling apps like Invoice Ninja: legacy plugin ecosystems where bugs hide in configuration and caching, not code. The missing piece is an MCP/AI agent purpose-built for WordPress/WooCommerce and legacy PHP maintenance — the market is enormous and utterly unserved comp
- Match (mi evaluación): **parcial (automatización sí, "capa de mantenimiento con IA" para el long tail de WooCommerce no)**
- Web (curado):
  - Rector (upgrades y refactor automáticos de PHP 5.3->8.5) https://github.com/rectorphp/rector [✓ en corpus (github:rectorphp/rector)]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/rectorphp/rector ★10427 · push 2026-09-22 — Instant Upgrades and Automated Refactoring of any PHP 5.3+ code [✓ en corpus (github:rectorphp/rector)]
  - https://github.com/Atanamo/PHP-Codeshift ★32 · push 2022-10-23 — A small PHP toolkit for running codemods (code transformations) over multiple PHP files. [✗ fuera del corpus]
  - https://github.com/wallter/laravel-ai-code-analysis ★18 · push 2026-04-15 — Laravel AI Code Analysis Project: A Laravel-based tool leveraging OpenAI’s language models and PHP AST analysis for automated documentation, refactoring suggestions, and performance assessments. Enhan [✓ en corpus (show_hn:42707135)]

esperado: https://github.com/rectorphp/rector
confirmado: 

---

## 77 · fc5cc4b2 · Missing: spam-resistant reputation that isn't surveillance

- Constellate: 2026-07-31 · sin verificar
- Idea: The neighborhood contains the openness of email and the backlash against identity mandates, but no idea offering the middle layer: portable, privacy-preserving sender reputation or proof-of-humanity that stops abuse without a government ID. Every piece implies its necessity; none proposes it. This is the gap where cryptographic attestations or web-of-trust reputation tooling should sit.
- Match (mi evaluación): **débil -> posible hueco real**
- Web (curado):
  - solo reputación convencional (SPF/DKIM, Spamhaus)
  - Sandi (paper, accountability sin vigilancia) https://arxiv.org/pdf/2401.16759 [✗ fuera del corpus]
- GitHub search API (por palabras clave, sin curar):
  - https://github.com/poise116/Decentralized-Reputation-Proof ★6 · push 2025-09-08 — Decentralized Reputation Proof (DRP) is a privacy-preserving identity vApp that lets users prove their trustworthiness across platforms using zero-knowledge proofs on Soundness Layer, without exposing [✗ fuera del corpus]
  - https://github.com/microsoft/Sandi ★6 · push 2026-04-23 — This is a Rust implementation of the Sandi privacy-preserving reputation system described in https://arxiv.org/abs/2401.16759 [✗ fuera del corpus]

esperado: https://arxiv.org/pdf/2401.16759
confirmado: 

---

## No buscados (44)

Huecos de investigación (su prior art serían papers, fuera del corpus) o ideas demasiado vagas.
Si querés alguno como caso real, avisame y lo busco.

| hash | alcance | título |
|---|---|---|
| c521a33a | research | Missing: merge-based continual learning as the forgetting cure |
| ad6c4d56 | research | Everyone Builds Spatial Patches, Nobody Builds Spatial Memory |
| d1d36433 | research | Missing: a general-purpose VLM trust auditor |
| 5f3f3eaa | research | Everyone Composes Queries; Nobody Built the Composition Layer |
| 7048229f | research | Nobody Built Interpretable Anomaly Detection for the Edge |
| 5018a38d | research | Medical AI Has Diagnosis, Missing the Trust Layer |
| d058c6d3 | research | Missing: Agent Forgetting and Knowledge Pruning Mechanisms |
| 296f3882 | research | Runtime Architecture Self-Modification |
| b7fe9e3a | research | Multi-Objective Reward Composition Tools Missing |
| 4d4d923a | research | Missing: Adversarial Unlearning Under Self-Play Dynamics |
| f40259fd | research | Missing: Adaptive Pipeline Orchestration Under Uncertainty |
| a01b629b | research | Missing: Multimodal Query Interface for Embodied Experiences |
| 6de91766 | research | Missing: Mechanistic Theory of Adaptive Architectural Components |
| ea5e3415 | research | Missing: Runtime Adaptation Decision Validation Layer |
| ee4a2437 | vague | Missing: Transparent Alternative to Elite Exit Systems |
| 5d3d1366 | vague | Missing: Tool for Forensic Comparison of Software Nostalgia |
| 60292a27 | research | Missing: Cross-Domain Video Editing Benchmark with Temporal Metrics |
| 0153f91c | research | Missing: Compositional Edit Propagation Across Modalities |
| 352c4dc9 | research | Missing: Adaptive Multilingual Token Economics |
| 96753236 | research | Missing: Reasoning-Aware Tool Selection and Routing |
| 4a516ad5 | research | Missing: Hierarchical Reasoning Debugger for Complex Structures |
| 552cd299 | research | Missing: Context-Aware Modality Routing Layer |
| 9ad83fb4 | research | Missing: Cross-Lingual Domain Transfer Benchmarks |
| 6766f3b6 | research | Missing: Quantum-Classical Architecture Search Optimizer |
| 899dd2ed | research | Federated Safe RL for Distributed Infrastructure |
| 430b5785 | research | Missing: Runtime Pluralistic Evaluation Frameworks |
| 1c0b1fab | research | Missing: Adaptive Precision Scheduling for Compute Efficiency |
| 6526dbf2 | vague | Missing: The Post-Hackathon Operationalization Layer |
| cabfd9ca | vague | Missing: Ground Truth Climate Action Infrastructure |
| cb3eb292 | research | Missing: Spatial Audio Control for Multi-Subject Scene Generation |
| 1fd3aeb9 | research | Nobody Built the Model That Says 'I Don't Know' |
| 160dbf81 | research | Nobody Benchmarks Whether World Models Actually Predict |
| e545e760 | research | Missing: A Verifier That Tells Models When to Reflect |
| a5e2487c | research | Nobody evaluates whether agent memory is worth keeping |
| b52fedb0 | research | Nobody Is Building Deepfake Detection for Generated 3D/4D |
| 39d157d7 | research | Formal Methods for Agents: Everyone Circles, Nobody Ships |
| 19e97add | research | No One Benchmarks FL Under Combined Adversity |
| eae1d11d | vague | Everyone Audits Internals; Nobody Sells the Audit |
| 50a4f12d | research | Missing: A Runtime Abstention Layer for Embodied Agents |
| a9d3aabb | research | Missing: a fidelity benchmark for synthetic humans |
| c9d908b1 | research | Everyone Densifies Rewards; Nobody Benchmarks Reward Densification |
| 5b6356d3 | research | Everyone Steers Policies, Nobody Audits What Steering Broke |
| 10e73cb1 | research | Everyone Claims Transfer; Nobody Measures It Comparably |
| 512fe792 | research | Everyone Measures Untrustworthiness; Nobody Ships a Trust Monitor |
