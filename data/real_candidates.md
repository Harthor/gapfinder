# Candidatos: absences verificadas de Constellate

Veredictos de Constellate: `web` (Claude + búsqueda web), `manual` (prior-art/*.md), `rubric` (rubric-test/*.md).
Propuesta: `yes` -> real, `no` -> negativo, solo `partially` -> parcial.
Marcá `confirmado: real`, `confirmado: negativo` o `confirmado: descartar`. Para `real`, dejá en
`esperado:` las URLs que cuentan como "lo que ya existía" (podés editar la lista propuesta);
también acepta ids del corpus (`show_hn:123`, `github:owner/repo`) para fijar un item concreto.
Las parciales vienen con `confirmado: parcial` y todas sus URLs de evidencia en `esperado:`;
cambiá a `descartar` (o recortá `esperado:`) las que no sirvan.
Corpus: ✓ = está; ✗ = no está hoy. "repo" y "url exacta" son matches exactos; los marcados
"heurístico, revisar" salen del dominio (homepage de un repo o Show HN con el nombre del producto)
y pueden equivocarse. La búsqueda dirigida (Fase 2) todavía no existe: los ✗ se re-evalúan cuando esté.

Verificadas: 71 absences (manual 11, rúbrica 4, web 71; una absence puede tener varias).

## 1 · a6c38804 · Everyone Builds Agents, Nobody Watches Them

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: This neighborhood has self-evolving agents, agents that bypass site blocks, agents reading financial markets (4), plus mature observability and orchestration — but only for infrastructure, not for agents. The missing piece is an agent-native observability and governance layer: tracing what autonomous agents did on the web, what they mutated in their own genome, and kill-switches when behavior drifts. Every ingredient for runaway agents exists here; the monitoring plane for them does not. That ga
- Veredictos:
  - **partially** (web, output.json): Multiple emerging tools (Galileo, theaios-agent-monitor, AgentGuard, Datadog, MLflow) cover pieces of tracing, drift detection, and kill-switches for agents, but none unify web-action provenance, self-mutation ('genome') tracking, and governed kill-switches into a single lightweight SDK+dashboard as
  - **yes** (manual, prior-art/absence-a6c38804.md): agent-native observability is a crowded, mature category by 2026 (AgentOps, Phoenix, Langfuse, LangSmith, Braintrust, MLflow, Datadog) with kill-switches and drift detection already standard patterns. The one genuinely uncovered element is tracing what a *self-evolving* agent mutated in its own geno
- Evidencia (prior art citado por Constellate):
  - https://galileo.ai/blog/best-ai-agent-observability-platforms — Galileo (Agent Observability & Guardrails Platform): Provides tracing, graph/step-level views, agentic quality metrics, and runtime guardrails that intercept unsafe agent outputs before they reach users. [✗ sin repo ni Show HN en el corpus]
  - https://medium.com/@Cohorte-AI/your-ai-agent-needs-a-kill-switch-heres-how-to-build-one-b1b69a053a25 — theaios-agent-monitor: A governance-first observability tool that records agent events, tracks baselines, detects anomalies, and gives operators scoped kill switches for agents, sessi [✗ sin repo ni Show HN en el corpus]
  - https://bmdpat.com/blog/ai-agent-needs-kill-switch — AgentGuard: A local SDK plus hosted dashboard offering runtime guardrails, budget caps, loop detection, alerting, and a remote kill path for agents in production. [✗ sin repo ni Show HN en el corpus]
  - https://www.datadoghq.com/products/ai/agent-observability/ — Datadog Agent Observability: Extends Datadog's monitoring suite with an SDK that captures intra/inter-agent operations, tool usage, memory interactions, handoffs, and detects behavior drift [✗ sin repo ni Show HN en el corpus]
  - https://mlflow.org/ai-observability — MLflow AI Observability: Open-source tracing and monitoring for LLM/agent execution graphs, including tool calls, reasoning steps, drift tracking, and governance audit logs. [✓ github:mlflow/mlflow (heurístico, revisar: repo con homepage mlflow.org)]
  - https://www.agentops.ai/ — AgentOps: Agent-native observability SDK plus dashboard: session replay, per-step tracing of tool calls and reasoning, cost tracking, and the kill-switch/circuit-breaker  [✓ github:AgentOps-AI/agentops (heurístico, revisar: repo con homepage agentops.ai)]
  - https://phoenix.arize.com/ — Arize Phoenix: Open-source LLM and agent observability focused on behavioral drift, bias detection and LLM-as-a-judge scoring for relevance, toxicity and accuracy. [✓ github:Arize-ai/phoenix (heurístico, revisar: repo con homepage arize.com)]
  - https://langfuse.com/ — Langfuse: Open-source tracing and evaluation for LLM applications and agents, capturing every model call, tool execution and reasoning step as structured spans, self-host [✓ github:langfuse/langfuse (heurístico, revisar: repo con homepage langfuse.com)]
  - https://smith.langchain.com/ — LangSmith: Hosted tracing, evaluation and monitoring for agent workflows, with hierarchical trace replay. [✗ sin repo ni Show HN en el corpus]
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/ — OpenTelemetry GenAI semantic conventions: The standard, alongside OpenInference, for encoding agent behavior into interoperable spans that any backend can consume. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Langfuse https://github.com/langfuse/langfuse ; OpenLLMetry https://github.com/traceloop/openllmetry ; MLflow tracing [fuerte]

propuesta: real
esperado: https://github.com/AgentOps-AI/agentops https://github.com/langfuse/langfuse https://github.com/mlflow/mlflow
confirmado: real

---

## 2 · 25a4c842 · Missing: Diffusion Serving Infrastructure, Not Just LLM Serving

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: The neighborhood contains mature LLM inference infrastructure (TPU kernels, MoE mapping, token-phase optimization, edge benchmarks like 3259) and a growing wave of production-bound diffusion applications (climate 1633, medical 2518, time series 2955), with only a hobbyist C++ port bridging them. What's structurally absent is serious serving-systems work for diffusion workloads: batching across denoising steps, caching, hardware-aware schedulers—the vLLM equivalent for diffusion. The internal str
- Veredictos:
  - **yes** (web, output.json): vLLM-Omni is precisely the 'vLLM for diffusion' the gap describes, with xDiT and NIRVANA covering the parallelism and caching sub-pieces independently.
  - **yes** (manual, prior-art/absence-25a4c842.md): vLLM-Omni is precisely the "vLLM for diffusion" the gap describes (denoising-step caching, disaggregated scheduling, batched DiT serving), with xDiT and NIRVANA covering the parallelism and caching sub-pieces independently.
- Evidencia (prior art citado por Constellate):
  - https://github.com/vllm-project/vllm-omni — vLLM-Omni: Diffusion-aware serving engine with denoising-step caching, disaggregated scheduling and batched DiT serving. [✓ github:vllm-project/vllm-omni (repo)]
  - https://github.com/xdit-project/xdit — xDiT: Inference engine for diffusion transformers with multiple parallelism strategies across GPUs. [✓ github:xdit-project/xDiT (repo)]
  - https://www.usenix.org/conference/nsdi24/presentation/agarwal-shubham — NIRVANA (Adobe, NSDI '24): Approximate caching system for diffusion serving that reuses intermediate denoising states across requests. [✗ sin repo ni Show HN en el corpus]
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/tutorials/Popular_Models_Guide/StableDiffusion/README.html — NVIDIA Triton — Stable Diffusion deployment: General inference server with a documented TensorRT path for serving diffusion models. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2503.11972 — MoDM: Serving system for mixture-of-diffusion-models balancing quality and latency under load. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): OneDiffusion (BentoML, servir cualquier modelo de difusión en producción) https://www.bentoml.com/blog/introducing-onediffusion-run-any-diffusion-model-anywhere ; ComfyUI como backend ; SwiftDiffusion (paper) [fuerte]

propuesta: real
esperado: https://github.com/vllm-project/vllm-omni https://github.com/xdit-project/xDiT
confirmado: real

---

## 3 · 6f3848c8 · Missing: Runtime Governance for Commercial Agent Teams

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: 3599 argues human-in-the-loop is theater, 3600 offers a toy deterministic safety gate, 1348 formalizes coalition dynamics, while 3467 and 750 sell agent teams handling real money and professional work. The gap is glaring: there is no production-grade policy engine that sits between multi-agent decisions and execution—programmable permissions, spend limits, audit trails, and escalation logic for agent teams. Everyone shipping commercial agents needs it; the only artifact here is a no-deps Python 
- Veredictos:
  - **partially** (web, output.json): Multiple runtime governance/policy-enforcement products (SteerPlane, Cycles, Prefactor, Guild, HAI Guardian) already provide spend limits, permissions, audit trails, and escalation for AI agents, but none is explicitly unified around multi-agent commercial 'teams' with coalition-aware escalation, so
  - **yes** (web, claude-haiku-4-5 2026-08-10): Multiple production-grade policy engines now exist that sit between multi-agent decisions and execution, providing programmable permissions, spend limits, audit trails, and escalation logic—directly filling the described gap.
  - **yes** (web, claude-haiku-4-5 2026-08-10): Multiple production-grade policy engines already exist that enforce programmable permissions, spend limits, audit trails, and escalation logic for agent teams operating in commercial environments.
  - **partially** (manual, prior-art/absence-6f3848c8.md): Portkey and LiteLLM already ship the spend-limit and audit-trail halves at production grade, but the escalation and inter-agent decision layer the absence describes is still spread across gateways, authorization engines and one-vendor modules rather than existing as a single governance product for c
- Evidencia (prior art citado por Constellate):
  - https://github.com/systempromptio/awesome-ai-agent-governance — SteerPlane: Open-source runtime control plane for AI agents providing deterministic loop detection, per-session cost ceilings with mid-stream termination, and a hierarchica [✗ repo fuera del bulk, ★42]
  - https://runcycles.io/blog/ai-agent-governance-runtime-enforcement-security-cost-compliance — Cycles (runcycles.io): Runtime governance system that enforces hard dollar budgets and RISK_POINTS action-authority caps atomically across an organizational hierarchy (tenant/workspac [✓ show_hn:47417096 (heurístico, revisar: Show HN del dominio runcycles.io: "Cycles – hard limits on agent actions before execution")]
  - https://prefactor.tech/learn/what-is-runtime-enforcement — Prefactor: Runtime enforcement layer that evaluates agent identity, permissions, action, data, and context in milliseconds, returning allow/block/throttle/sandbox/escalate [✗ sin repo ni Show HN en el corpus]
  - https://www.guild.ai/blog/agent-governance/your-authorization-platform-doesnt-govern-your-age — Guild (Authorization + Governance Layer): Argues for and implements an outbound governance control plane that brokers credentials centrally, enforces workspace boundaries, and applies hard, enforced lim [✗ sin repo ni Show HN en el corpus]
  - https://www.holisticai.com/blog/runtime-agentic-monitoring-tools-access-control-cost — HAI Guardian (Holistic AI): SDK-based monitoring and enforcement pipeline that intercepts agent tool calls in real time, providing access control, cost tracking/control, and a full audit t [✗ sin repo ni Show HN en el corpus]
  - https://github.com/microsoft/agent-governance-toolkit — Agent Governance Toolkit: Microsoft open-source runtime policy enforcement, identity, execution sandboxing, and audit logging for AI agents across multiple frameworks. [✓ github:microsoft/agent-governance-toolkit (repo)]
  - https://airia.com/agent-constraints-a-technical-deep-dive-into-policy-based-ai-agent-governance/ — Airia Agent Constraints: Runtime interception of agent-to-tool interactions with policy-based constraint enforcement and audit trails. [✗ sin repo ni Show HN en el corpus]
  - https://www.openlegion.ai/en/learn/ai-agent-governance — OpenLegion: Agent governance platform with role-based access control, spend limit enforcement ($50/day, $200/month caps), audit trails, and compliance framework coverage. [✓ github:openlegion-ai/openlegion (heurístico, revisar: repo con homepage openlegion.ai)]
  - https://www.strongdm.com/blog/ai-agent-runtime-governance — StrongDM Policy Engine for AI Agents: Real-time context-aware policy enforcement before agent actions execute, with record/shadow/enforce progression and Cedar policy-based control. [✗ sin repo ni Show HN en el corpus]
  - https://www.spellguard.ai/blog/privilege-escalation-and-access-control — Spellguard: Action allowlisting and privilege escalation detection for agent tool calls with policy enforcement in trusted execution environment. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Microsoft Agent Governance Toolkit (MIT, abr-2026): policy engine, budgets/spend limits, audit trail, escalation para agentes -> https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/ [fuerte (no específico de "teams" comerciales)]

propuesta: real
esperado: https://github.com/microsoft/agent-governance-toolkit https://github.com/openlegion-ai/openlegion show_hn:47417096 show_hn:46693373 show_hn:23976597
confirmado: real

---

## 4 · 197bf4f9 · Missing: The Glue Layer for Self-Hosters

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: This neighborhood is dense with self-hosted apps (identity, marketing, finance, assets, media) but contains nothing that unifies them: no orchestration, SSO wiring, backup, or cross-app dashboard tool. Keycloak exists precisely because each of these apps has its own login, yet integrating it into each one is a manual chore. The missing piece is an opinionated 'self-hosted stack composer' that deploys these apps pre-wired with shared auth, backups, and monitoring — the Vercel of homelab back-offi
- Veredictos:
  - **yes** (web, output.json): Established self-hosting platforms like Cloudron and YunoHost already deploy apps pre-wired with shared SSO, automated backups, and centralized dashboards, substantially covering the described gap.
  - **partially** (web, claude-haiku-4-5 2026-08-10): The pieces exist—deployment platforms (Greffon, Openship), dashboards (Dashy, Homarr), and pre-orchestrated stacks (Supabase)—but nothing combines all of these to pre-wire arbitrary self-hosted apps with unified SSO, backups, and cross-app orchestration as described.
  - **no** (web, claude-haiku-4-5 2026-08-10): No existing product combines automated deployment, pre-configured SSO integration, unified backups, and cross-app orchestration into a single opinionated platform—the gap remains unfilled.
  - **yes** (manual, prior-art/absence-197bf4f9.md): YunoHost is exactly the described product (shared SSO, shared backups, unified app management) and Cloudron is its commercial equivalent; the absence appears to be an artifact of the corpus containing many self-hosted apps but none of the platforms that already compose them.
- Evidencia (prior art citado por Constellate):
  - https://www.cloudron.io/ — Cloudron: A self-hosted platform that lets users one-click install and manage 100+ web apps with automatic backups, updates, SSL, and single sign-on across all installed  [✓ show_hn:9976992 (heurístico, revisar: Show HN del dominio cloudron.io: "Cloudron – Get Your Own Cloud")]
  - https://yunohost.org/ — YunoHost: A Debian-based self-hosting operating system with a web admin that installs apps and integrates them with a shared LDAP/SSO portal, backups, and system monitori [✓ github:YunoHost/yunohost (heurístico, revisar: repo con homepage yunohost.org)]
  - https://cosmos-cloud.io/ — Cosmos Cloud: A self-hosted service manager combining reverse proxy, HTTPS/certificate handling, subdomain routing, built-in SSO, and Docker container management into one con [✓ github:azukaar/Cosmos-Server (heurístico, revisar: repo con homepage cosmos-cloud.io)]
  - https://runtipi.io/ — Runtipi: A Docker-based personal homeserver orchestrator with a curated app store (including Firefly III, Bookstack, Gitea, etc.) and a simple web interface for managing [✓ github:runtipi/runtipi (heurístico, revisar: repo con homepage runtipi.io)]
  - https://casaos.io/ — CasaOS: An open-source home cloud/server OS with a Docker-based app store, one-click installs, and a bundled dashboard for managing services on a home server. [✗ sin repo ni Show HN en el corpus]
  - https://github.com/Khrys-NovaTech/greffon — Greffon: Self-hosted deployment platform that handles orchestration, TLS, and lifecycle management for containerized applications using Docker Compose templates. [✗ repo fuera del bulk]
  - https://github.com/oblien/openship — Openship: Open-source, self-hostable deployment platform with built-in CI/CD, automatic domains, and Let's Encrypt TLS for containerized applications. [✓ github:oblien/openship (repo)]
  - https://dashy.to/ — Dashy: Self-hosted dashboard and launcher for homelab services with status checks, widgets, and customizable interface for accessing self-hosted applications. [✓ github:lissy93/dashy (heurístico, revisar: repo con homepage dashy.to)]
  - https://github.com/ajnart/homarr — Homarr: Open-source dashboard application that organizes and displays self-hosted services in a customizable interface with widgets and status monitoring. [✓ github:ajnart/homarr (repo)]
  - https://github.com/supabase/supabase — Supabase (Self-Hosted): Self-hosted backend platform with pre-orchestrated services including authentication, database APIs, real-time subscriptions, file storage, and edge functions u [✓ github:supabase/supabase (repo)]
- Búsqueda propia (sep-2026, complementaria): YunoHost (SSO entre apps, backups) https://github.com/YunoHost/yunohost ; Cloudron (deploy, updates, backups, SSO) https://www.cloudron.io ; Sandstorm, 1Panel [fuerte]

propuesta: real
esperado: https://github.com/YunoHost/yunohost https://github.com/azukaar/Cosmos-Server https://github.com/runtipi/runtipi https://github.com/SimpleHomelab/Deployrr show_hn:9976992 show_hn:30854912 show_hn:31657527
confirmado: real

---

## 5 · ecad36a5 · Missing: The Orchestrator That Spends Your Tokens Wisely

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: The neighborhood has quota monitors, a fallback gateway, an agent-building SDK, and cautionary tales of multi-agent waste — but no tool that actively decides which task deserves which model at which cost. Monitoring and routing exist; budget-aware task allocation does not. The obvious missing piece is a 'chief-of-staff' layer that assigns cheap models to boilerplate and expensive ones to hard reasoning, enforcing a spend budget per project. Every ingredient is already open-source in this list.
- Veredictos:
  - **partially** (web, output.json): Multiple open-source routers (RouteLLM, LiteLLM, Maestro, Morph Router, vLLM Semantic Router) already do complexity-based cheap/expensive model routing and some enforce spend caps, but none combine both into a single 'chief-of-staff' layer that actively allocates tasks under an explicit per-project 
  - **yes** (manual, prior-art/absence-ecad36a5.md): CodeRouter alone matches the described "chief-of-staff" layer almost exactly (task-difficulty-based cheap/expensive model allocation with budget awareness for coding agents), and Not Diamond Code plus LiteLLM's budget routing cover the same territory commercially and at the gateway level.
- Evidencia (prior art citado por Constellate):
  - https://github.com/BerriAI/litellm — LiteLLM: Open-source LLM gateway providing a unified OpenAI-compatible interface to 100+ providers with per-key/per-project spend budgets and virtual keys. [✓ github:BerriAI/litellm (repo)]
  - https://www.finout.io/blog/5-open-source-tools-to-control-your-ai-api-costs-at-the-code-level — RouteLLM: Open-source router from LMSYS/UC Berkeley that uses trained ML classifiers to route each prompt to either a strong (expensive) model or a weak (cheap) model bas [✗ sin repo ni Show HN en el corpus]
  - https://www.ayautomate.com/blog/open-source-llm-orchestration-tools — Maestro: Open-source LLM router described as strong for cheap-first routing with per-response cost transparency across hosted and local model pools (OpenAI, Anthropic, O [✗ sin repo ni Show HN en el corpus]
  - https://www.morphllm.com/llm-router — Morph Router: Classifies prompt difficulty in ~430ms and sends each request to the cheapest model tier that can handle it (e.g., Haiku for easy, Opus for hard), claiming 40-7 [✗ sin repo ni Show HN en el corpus]
  - https://vllm-semantic-router.com/ — vLLM Semantic Router: Open-source semantic router that proposes token-budget-aware pool routing, dispatching requests to short/long model pools based on estimated token budget to cut [✗ sin repo ni Show HN en el corpus]
  - https://github.com/Code-Router/CodeRouter — CodeRouter: An [✗ repo fuera del bulk]
  - https://www.notdiamond.ai/ — Not Diamond Code: An intelligent model router for long-horizon coding agents that integrates with any gateway and agent harness, including Claude Code, to automatically select th [✗ sin repo ni Show HN en el corpus]
  - https://github.com/musistudio/claude-code-router — claude-code-router (musistudio): A local model gateway and control plane for coding agents, giving Claude Code, Codex, and other clients one stable local endpoint with routing rules [✓ github:musistudio/claude-code-router (repo)]
  - https://docs.litellm.ai/docs/proxy/provider_budget_routing — LiteLLM (budget routing): An open-source gateway with [✓ github:BerriAI/litellm (heurístico, revisar: repo con homepage docs.litellm.ai)]
  - https://github.com/lm-sys/RouteLLM — RouteLLM (LMSYS): An open-source framework for routing requests between a stronger, costlier model and a cheaper, weaker one based on the difficulty of each query; its trained ro [✓ github:lm-sys/RouteLLM (repo)]
- Búsqueda propia (sep-2026, complementaria): RouteLLM (LMSYS) https://github.com/lm-sys/RouteLLM ; LiteLLM routing por costo ; gz-modelrouter (modelo más barato que pasa umbral de calidad) https://github.com/oke3/gz-modelrouter ; Not Diamond, OpenRouter [fuerte]

propuesta: real
esperado: https://github.com/BerriAI/litellm https://github.com/lm-sys/RouteLLM https://github.com/musistudio/claude-code-router
confirmado: real

---

## 6 · 01fe2dbe · Missing: Zero-Knowledge Self-Hosted Messaging

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: The neighborhood covers self-hosted networking (Headscale), encrypted storage (Cryptomator), zero-knowledge sharing (PrivateBin), and open email (Thunderbird) — every pillar of a sovereign personal stack except real-time messaging. The privacy stack here handles data at rest and data shared asynchronously, but the highest-value channel, chat, is only represented by WeChat hacks that stay inside a closed platform. The logically implied missing piece is a Headscale-style self-hosted, E2E messaging
- Veredictos:
  - **yes** (web, output.json): Matrix/Synapse has been the mature self-hosted end-to-end encrypted messaging control server for years, with SimpleX and Rocket.Chat covering adjacent postures.
  - **yes** (manual, prior-art/absence-01fe2dbe.md): Matrix/Synapse has been the mature answer to self-hosted end-to-end encrypted messaging for years, with SimpleX and Rocket.Chat covering adjacent postures; the absence looks like a corpus artifact, since a neighborhood built from Headscale, Cryptomator and PrivateBin simply happened not to include t
- Evidencia (prior art citado por Constellate):
  - https://matrix.org/ — Matrix / Synapse: Federated messaging protocol whose reference self-hosted homeserver relays only ciphertext it cannot read. [✓ github:wechaty/matrix-appservice (heurístico, revisar: repo con homepage matrix.org)]
  - https://simplex.chat/ — SimpleX Chat: Decentralized messenger with no user identifiers and self-hostable relay servers. [✓ show_hn:24862645 (url exacta)]
  - https://www.rocket.chat/ — Rocket.Chat: Open-source self-hosted team chat with end-to-end encryption and integrations. [✓ show_hn:10112932 (url exacta)]
  - https://mattermost.com/ — Mattermost: Self-hosted messaging platform aimed at organisations with data-sovereignty requirements. [✓ github:mattermost/mattermost (heurístico, revisar: repo con homepage mattermost.com)]
  - https://delta.chat/ — Delta Chat: Chat client that rides existing email infrastructure with end-to-end encryption. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Matrix/Synapse+Element (E2EE, self-hosted) https://github.com/element-hq/synapse ; Rocket.Chat E2E ; chatalot (Signal protocol, self-hosted) https://github.com/purpleneutral/chatalot [fuerte]

propuesta: real
esperado: https://github.com/element-hq/synapse show_hn:24862645 show_hn:10112932
confirmado: real

---

## 7 · 89c010f2 · Sandboxes Everywhere, but No Agent Firewall

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: Three separate projects (microsandbox, CubeSandbox, OpenShell) solve containment — keeping agents from breaking out — and others (codex, herdr) multiply agent activity. But nothing here governs what agents are *allowed* to do inside their permitted scope: no policy engine, permission prompt system, or audit log of agent actions across tools. The gap is an 'agent firewall': a lightweight layer that intercepts, logs, and approves agent side-effects (file writes, network calls, purchases) across an
- Veredictos:
  - **yes** (web, output.json): Multiple existing products (Preloop, Agent Action Firewall, Coder's Agent Firewall, AgentAudit) already implement policy engines, approval prompts, and audit logs for agent tool calls and side-effects, closely matching the described 'agent firewall' gap.
  - **partially** (manual, prior-art/absence-89c010f2.md): several guardrail/policy projects govern agent behavior in adjacent ways, but I could not verify (search unavailable) any single product that intercepts, logs, and approves agent side-effects across arbitrary sandboxes as described.
- Evidencia (prior art citado por Constellate):
  - https://glama.ai/mcp/servers/@yconst/preloop/tree/b1f7e8e473267657c23069541b85272078fbe60e — Preloop: An MCP firewall that gives complete control over what AI agents can do, with access policies, approval workflows, and audit trails; works with Claude Code, Curs [✗ sin repo ni Show HN en el corpus]
  - https://www.agentactionfirewall.com/ — Agent Action Firewall: A platform that lets you define who or what is allowed to act, routes high-risk actions to humans, blocks unauthorized actions in real time, and keeps cryptogra [✗ sin repo ni Show HN en el corpus]
  - https://coder.com/docs/ai-coder/agent-firewall — Coder Agent Firewall: A process-level firewall add-on that restricts and audits what autonomous AI agents can access, with network policy enforcement (allow/deny domains and HTTP ver [✗ sin repo ni Show HN en el corpus]
  - https://aiagentaudit.dev/ — AgentAudit: Compliance infrastructure that logs every agent action and tool call with chain-verified, hash-linked audit trails, and can flag or block behavior via defined p [✗ sin repo ni Show HN en el corpus]
  - https://developers.googleblog.com/announcing-genkit-middleware-intercept-extend-and-harden-your-agentic-apps/ — Genkit Middleware (ToolApproval): An open-source middleware layer for Genkit agents that intercepts tool calls and triggers human-in-the-loop approval interrupts for any tool not on an allowlist [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Pipelock (firewall de agentes para MCP/egress) https://github.com/luckyPipewrench/pipelock ; agentguard (permisos + kill switch) https://github.com/A386official/agentguard [fuerte]

propuesta: real
esperado: https://github.com/luckyPipewrench/pipelock show_hn:46693373 show_hn:49083015
confirmado: real

---

## 8 · e1cc171a · Agents Get Credit Cards Before They Get Credit Scores

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: Agents can now spend real money, install unverified skills that may not even exist, inherit unsafe behaviors invisibly through distillation, and we can benchmark their trajectories after the fact or gate them with static guardrails. What's missing is the middle layer: a runtime identity, reputation, and attestation system that scores an agent's trustworthiness before it acts—the equivalent of a credit score plus signed provenance for skills and behaviors. The pieces define the gap precisely: mon
- Veredictos:
  - **partially** (web, output.json): Multiple real projects (ERC-8004, JFrog Agent Skills Registry, Super Agent Skill, Tessl/Snyk, ACP) each cover one piece of the described trust layer—identity/reputation registries, signed skill provenance, or reputation portability—but none unifies runtime agent trustworthiness scoring, signed skill
  - **partially** (web, claude-haiku-4-5 2026-08-10): AgentGraph comes closest and covers identity, attestation, and reputation scoring; JFrog covers signed skill registries; AgentQuay provides reputation scoring; but no single product unifies agent identity, skill attestation, behavioral inheritance tracking, and unified trust scoring as a cohesive ru
  - **partially** (web, claude-haiku-4-5 2026-08-10): Multiple products cover individual pieces—reputation scoring, skill signing, identity—but none unifies them into a cohesive runtime identity and attestation system that gates spending, skill acquisition, and behavioral inheritance before agents act.
  - **partially** (manual, prior-art/absence-e1cc171a.md): the exact v1 the absence proposes is already occupied from both ends (AgentStamp for agent reputation, NVIDIA-Verified Skills for signed skill provenance), but nothing yet unifies identity, skill provenance and *behavioral inheritance* from distillation into one pre-action trust decision, which is t
- Evidencia (prior art citado por Constellate):
  - https://eips.ethereum.org/EIPS/eip-8004 — ERC-8004 (Trustless Agents): An Ethereum standard defining three on-chain registries — Identity, Reputation, and Validation — that give autonomous AI agents a portable identity, collect fee [✓ github:erc-8004/erc-8004-contracts (heurístico, revisar: repo con homepage eips.ethereum.org)]
  - https://jfrog.com/ai-catalog/skills-registry/ — JFrog Agent Skills Registry (part of JFrog AI Catalog): A private registry that scans, verifies, and cryptographically signs agent skills for vulnerabilities and malicious behavior, enforcing approval workflows and p [✗ sin repo ni Show HN en el corpus]
  - https://superagentskill.com/ — Super Agent Skill: A marketplace/registry where every submitted skill is Ed25519-signed, sandbox-certified against adversarial cases, and given a public Trust Score that travels w [✗ sin repo ni Show HN en el corpus]
  - https://snyk.io/blog/snyk-tessl-partnership/ — Tessl Registry with Snyk security scoring: A skills registry where every public skill carries a Snyk-generated security score, bringing package-manager-style trust signals (vulnerability scanning) to age [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2603.18829 — Agent Control Protocol (ACP) Reputation Snapshot Portability: A specification (ACP-REP-PORTABILITY-1.1) defining a cryptographically signed ReputationSnapshot object that carries an agent's reputation score across organiza [✗ sin repo ni Show HN en el corpus]
  - https://agentgraph.co — AgentGraph: Provides cryptographic agent identity (W3C DIDs), Composable Trust Evidence Format for attestations, and cross-emitter trust scores derived from accumulated att [✗ sin repo ni Show HN en el corpus]
  - https://docs.agent.tech/agentquay/trust-score/ — AgentQuay Trust Score: Assigns each indexed agent a Trust Score derived from public on-chain activity and verifiable profile data, combining Trading and Reputation components for rank [✗ sin repo ni Show HN en el corpus]
  - https://agentfacts.org/blockchain — AgentFacts for Blockchain: Provides immutable AI agent identity verification with on-chain provenance, compliance audit trails, and decentralized trust networks via hashed metadata anchor [✗ sin repo ni Show HN en el corpus]
  - https://knowthat.ai/ — KnowThat.ai: A shared reputation registry that provides trust scores and behavioral history for AI agents before granting access to servers and APIs. [✗ sin repo ni Show HN en el corpus]
  - https://agentstamp.org/ — AgentStamp: Cryptographic trust scoring platform with public registry, signing, reputation scores (0-100), and MCP tool integration for AI agents. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): IETF draft-sharif-agent-payment-trust (trust score 0-100 + límites por nivel) https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/ ; spend controls en el rail de pago (Meow) https://www.meow.com/blog/spend-controls-ai-agents-caps-mcc-locks-approval-ladders [parcial (estándar/servicios, no un producto único)]

propuesta: parcial
esperado: https://eips.ethereum.org/EIPS/eip-8004 https://jfrog.com/ai-catalog/skills-registry/ https://superagentskill.com/ https://snyk.io/blog/snyk-tessl-partnership/ https://arxiv.org/pdf/2603.18829 https://agentgraph.co https://docs.agent.tech/agentquay/trust-score/ https://agentfacts.org/blockchain https://knowthat.ai/ https://agentstamp.org/ https://www.mnemom.ai/blog/mnemom-research/credit-scores-for-ai-agents/ https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/ https://eco.com/support/en/articles/13221214-what-is-erc-8004-the-ethereum-standard-enabling-trustless-ai-agents https://datatracker.ietf.org/doc/draft-sharif-apki-agent-pki/00/ https://github.com/nolabs-ai/agent-sign
confirmado: parcial

---

## 9 · aca98da0 · Everyone Manages Agents, Nobody Grades Them

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: The neighborhood has agent employment (Multica), agent reliability harnesses (Archon), fleet orchestration (Orca), agents with memory (Rowboat), and agent debugging (DevTools-for-agents) — a full HR stack minus one piece: performance evaluation. There is no tool that scores agent output quality over time, compares agents against each other on real tasks, or decides which agent deserves more autonomy. If agents are 'teammates,' the missing product is their performance review — a benchmark/trust l
- Veredictos:
  - **partially** (web, output.json): Numerous evaluation, benchmarking, leaderboard, and trust-scoring tools exist that grade agent quality and compare agents, but none of the found products unify these signals into a feedback loop that governs task assignment or autonomy the way the described gap envisions.
  - **partially** (manual, prior-art/absence-aca98da0.md): every ingredient exists (continuous quality scoring in Braintrust/LangSmith, head-to-head agent comparison in Galileo/Artificial Analysis, and even trust-score-gated autonomy in AgentAnchor), but no widely-adopted product yet unifies longitudinal performance grading with automated autonomy/task-assi
- Evidencia (prior art citado por Constellate):
  - https://huggingface.co/spaces/galileo-ai/agent-leaderboard — Galileo AI (Agentic Evaluations + Agent Leaderboard): Provides an evaluation intelligence platform with dedicated Agentic Evaluations, hallucination detection, and a public Agent Leaderboard for comparing agent per [✓ show_hn:44593356 (url exacta)]
  - https://deepeval.com/guides/guides-ai-agent-evaluation — Confident AI / DeepEval: An LLM evaluation framework and platform that scores agent traces in development and production, tracks performance trends over time, and manages golden dataset [✗ sin repo ni Show HN en el corpus]
  - https://www.langchain.com/langsmith/evaluation — LangSmith Evaluation (LangChain): Lets teams run offline/online evaluations comparing agent versions, benchmarking performance, catching regressions, and scoring real-time production interaction [✗ sin repo ni Show HN en el corpus]
  - https://hal.cs.princeton.edu/ — Holistic Agent Leaderboard (HAL): A standardized, cost-aware, third-party leaderboard that evaluates agents on consistency, predictability, robustness, safety, and self-awareness beyond raw accu [✗ sin repo ni Show HN en el corpus]
  - https://cleanlab.ai/blog/agent-tlm-hallucination-benchmarking/ — Cleanlab Trust Scoring (TLM): Scores the trustworthiness of an agent's individual responses in real time and uses that trust score to guardrail or halt outputs below a threshold. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Agent scorecards de FutureAGI https://futureagi.com/glossary/agent-scorecard/ ; Scorecard.io https://www.scorecard.io/ ; Braintrust/Phoenix [parcial-fuerte (evaluación por agente, no "performance review" tipo RRHH)]

propuesta: parcial
esperado: https://huggingface.co/spaces/galileo-ai/agent-leaderboard https://deepeval.com/guides/guides-ai-agent-evaluation https://www.langchain.com/langsmith/evaluation https://hal.cs.princeton.edu/ https://cleanlab.ai/blog/agent-tlm-hallucination-benchmarking/
confirmado: parcial

---

## 10 · 81981bec · Everyone builds cloners and detectors; nobody builds provenance

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: The neighborhood is dense with generation power — tokenizer-free cloning (6), expressive open TTS families, training-free speech editing — and with reactive forensics that admit they're losing (3138 documents a temporal generalization gap, 2894 retreats to interpretable classical methods). The structurally missing piece is generation-side provenance: robust audio watermarking and signed voice-consent infrastructure baked into these open TTS stacks. Detection-only defense is provably brittle agai
- Veredictos:
  - **partially** (web, output.json): Generation-side watermarking and provenance standards (SynthID, PerTh/Chatterbox, AudioSeal, C2PA, MelShield) exist and are actively deployed, but they remain fragmented, mostly proprietary or single-vendor, and explicitly fail to cover open-source voice models, so no unified cryptographic attributi
  - **partially** (manual, prior-art/absence-81981bec.md): Robust synthesis-time audio watermarking (AudioSeal, SynthID, Perth) and signed provenance standards (C2PA) each exist and Resemble even combines them commercially, but no one has verifiably baked watermarking plus signed voice-consent into the open-weights TTS ecosystem (VoxCPM/MOSS-TTS-class model
- Evidencia (prior art citado por Constellate):
  - https://www.resemble.ai/learn/models/chatterbox-turbo — Resemble AI PerTh watermarking in Chatterbox Turbo (open-source TTS): Every audio file generated by Chatterbox Turbo is marked with the PerTh watermarker — imperceptible to listeners, but detectable for provenance and incident res [✗ sin repo ni Show HN en el corpus]
  - https://elevenlabs.io/blog/synthid — Google DeepMind SynthID (audio): A digital watermark embedded directly into audio generated by partner platforms like ElevenLabs and OpenAI's GPT-Live voice, inaudible and designed to survive e [✗ sin repo ni Show HN en el corpus]
  - https://sokaudiowm.github.io/ — AudioSeal / WavMark / TimbreWatermarking (academic watermarking schemes): Deep-learning audio watermarking schemes designed for detecting AI-generated speech, protecting copyright, and defending against voice cloning, evaluated system [✗ sin repo ni Show HN en el corpus]
  - https://github.com/and-mill/Awesome-GenAI-Watermarking — C2PA (Coalition for Content Provenance and Authenticity): A standard that enables authors of provenance data to securely bind statements of provenance to content instances using their credentials, via a trust model wit [✓ github:and-mill/Awesome-GenAI-Watermarking (repo)]
  - https://arxiv.org/pdf/2605.01515 — MelShield (Mel-domain audio watermarking research): Proposes robust mel-domain watermarking for provenance attribution of AI-generated synthesized speech, embedding a traceable signal during or around generation  [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): AudioSeal (Meta, watermark localizado de voz sintética) https://github.com/facebookresearch/audioseal ; Chatterbox con watermark PerTh ; Respeecher + C2PA https://contentauthenticity.org/blog/community-story-respeecher [fuerte]

propuesta: parcial
esperado: https://github.com/and-mill/Awesome-GenAI-Watermarking https://www.resemble.ai/learn/models/chatterbox-turbo https://elevenlabs.io/blog/synthid https://sokaudiowm.github.io/ https://arxiv.org/pdf/2605.01515
confirmado: parcial

---

## 11 · 75b40b56 · Missing: A Metric-Trustworthiness Auditor for Practitioners

- Verificada por: manual, web · corridas: 2026-07-16
- Idea: Four ideas diagnose that metrics deceive—prompt-optimization gains are noise, proxies fail per-segment, reliability is nonuniform, and competing measurement scores yield divergent conclusions—yet each offers only a bespoke academic framework. The missing piece is a general-purpose tool that takes any evaluation pipeline and reports where its metrics are directionally unreliable: per-segment sign flips, run-to-run variance versus claimed effect, and stratum-level confidence. The neighborhood has 
- Veredictos:
  - **partially** (web, output.json): Existing A/B platforms (Eppo, Statsig) and LLM-eval frameworks (Evidently AI, Confident AI/DeepEval) each supply pieces—guardrail thresholds, segment-effect detection, judge sanity checks—but no single general-purpose tool audits arbitrary evaluation pipelines for per-segment sign flips, run-to-run 
  - **partially** (manual, prior-art/absence-75b40b56.md): each component exists in isolation (experiment-validity diagnostics in Eppo, weak-segment detection in Deepchecks/Zeno/Giskard, variance-vs-effect statistics in the Error Bars methodology), but no verified product unifies them into a pipeline-agnostic auditor reporting per-segment sign flips, run-to
- Evidencia (prior art citado por Constellate):
  - https://www.geteppo.com/blog/what-are-guardrail-metrics-with-examples — Eppo: An experimentation platform that lets teams define guardrail metrics with statistical cutoffs and non-inferiority testing to catch metrics that shouldn't move,  [✗ sin repo ni Show HN en el corpus]
  - https://www.statsig.com/comparison/dev-first-alternative-statsig — Statsig: An experimentation and feature-flagging platform offering automated heterogeneous effect detection to surface which user segments respond differently to changes [✓ show_hn:27240243 (heurístico, revisar: Show HN del dominio statsig.com: "Statsig launches automated A/B Experiment Holdouts")]
  - https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/ — Microsoft ExP Patterns of Trustworthy Experimentation: A published methodology (not a downloadable tool) describing checks such as Sample Ratio Mismatch detection, per-metric imbalance checks, and weighting schemes  [✗ sin repo ni Show HN en el corpus]
  - https://www.evidentlyai.com/llm-guide/llm-evaluation-metrics — Evidently AI: An LLM evaluation platform/library providing reference-free metrics, LLM-as-judge scoring, and repeatable evaluation reports for RAG/agent systems. [✗ sin repo ni Show HN en el corpus]
  - https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation — Confident AI / DeepEval: An open-source LLM evaluation framework with 'auditable metrics', observability, and pre-deployment quality gates for LLM applications, including guidance to sa [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): BenchBrowser (paper, auditar validez de benchmarks) https://arxiv.org/pdf/2603.18019 ; toolkits de fairness por subgrupo (catálogo OECD) [débil (no hay un auditor de confiabilidad de métricas para practitioners)]

propuesta: parcial
esperado: https://www.statsig.com/comparison/dev-first-alternative-statsig https://www.geteppo.com/blog/what-are-guardrail-metrics-with-examples https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/ https://www.evidentlyai.com/llm-guide/llm-evaluation-metrics https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation
confirmado: parcial

---

## 12 · 1e7eb5cb · Missing: A Blast-Radius Firewall for Coding Agents

- Verificada por: rubric, web · corridas: 2026-07-31
- Idea: We have the symptom (agent modifies three pages outside its spec), the theory (agents need FSM-style constraints), the consequence (silent pipeline failures, AI-generated legacy code), and the audit failure (gates that don't catch sequences). What's absent is the obvious product: a tool that enforces a declared scope on agent edits — file allowlists, diff-radius limits, automatic rejection of out-of-spec changes at commit time. Every idea here circles the need for externally enforced boundaries,
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple point solutions exist (tool-call allowlist enforcers like Scopebound, IDE guardrail layers like Kirin, git hookflows, and DIY pre-commit scripts) that each implement pieces of scope/diff enforcement, but none packages declared per-task file allowlists, diff-radius limits, and automatic comm
  - **partially** (rubric, rubric-test/absence-1e7eb5cb.md run 1): Multiple tools already implement pieces of scope enforcement (file allowlists, pre-commit rejection, tool-call policy gates) but no single found product packages declared-scope-plus-diff-radius enforcement with automatic commit-time rejection as one coherent, cross-agent tool, and the field explicit
  - **yes** (rubric, rubric-test/absence-1e7eb5cb.md run 2): agent-guardrails already implements the exact wedge described — declared file allowlists, scope validation via git diff, and automatic rejection (merge-blocking) of out-of-spec changes — so the enforcement layer already exists as a shipped product, not just a theorized need.
- Evidencia (prior art citado por Constellate):
  - https://scopebound.ai/ — Scopebound: Zero-trust enforcement layer for AI agents that checks every tool call against a declared role with allowed_tools, parameter constraints, rate limits, and appro [✗ sin repo ni Show HN en el corpus]
  - https://www.knostic.ai/blog/ai-coding-agent-security — Kirin (Knostic): IDE-level security layer that enforces guardrails in real time for coding assistants like Cursor, Copilot, Claude Code, and Windsurf, inspecting MCP connections [✗ sin repo ni Show HN en el corpus]
  - https://htek.dev/articles/hookflows-governed-git-for-ai-agents — hookflows (Copilot CLI governance pattern): Declarative markdown-based hookflows that intercept raw git commands and redirect agents to governed tools enforcing workflow rules structurally, described as ' [✗ sin repo ni Show HN en el corpus]
  - https://usegitai.com/docs/agents/add-your-agent — Git AI (usegitai.com): A checkpoint-based git tool where agents declare which file paths they will edit before making changes, narrowing diffs to only AI-touched files for tracking an [✓ github:git-ai-project/git-ai (heurístico, revisar: repo con homepage usegitai.com)]
  - https://dev.to/alanwest/how-to-stop-ai-code-assistants-from-making-unauthorized-changes-eo8 — Pre-commit hook pattern for protected files (community guide): A DIY pre-commit hook script that blocks commits touching a hardcoded list of protected file patterns (e.g., .env, migrations, Dockerfile) unless explicitly ove [✗ sin repo ni Show HN en el corpus]
  - https://dev.to/onsen/ai-code-editing-gone-too-far-stop-over-editing-now-444m — Aider (file-scope CLI flags): A CLI coding agent that lets you declare which files the model may touch per session, reducing over-editing, but this is a user-declared advisory scope rather t [✗ sin repo ni Show HN en el corpus]
  - https://www.agentrulegen.com/guides/how-to-protect-files-from-ai-agents — Claude Code permissions.deny / settings.json: Tool-level deny rules that block an agent from reading or editing specific file patterns (e.g., .env), enforced regardless of what the model wants to do. [✗ sin repo ni Show HN en el corpus]
  - https://github.com/openclaw/openclaw/issues/12202 — openclaw – Per-agent file path access control (feature request #12202): An open, unimplemented design proposal for glob-based allowlist/denylist file access control per agent, enforced at the tool level before read/write/edit execut [✓ github:openclaw/openclaw (repo)]
  - https://dev.to/irrindar/blast-radius-series-agentic-engineering-framework-4km2 — Fabric / "Blast Radius" governance framework: An open-source dependency-impact analyzer that flags high-connectivity components an agent touched, but explicitly does not block commits or reject changes auto [✗ sin repo ni Show HN en el corpus]
  - https://travis.media/blog/safely-use-ai-coding-agents/ — pre-commit framework + custom hooks (generic infrastructure): A generic git hook framework used to reject bad commits (secrets, lint failures) at commit time; teams manually wire scope-diff checks into it themselves rather [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): solo guías/controles (sandbox, path allowlists, permisos de Claude Code) https://aurascape.ai/answers/ai-coding-agent-permissions-files-shell-git-cloud/ [parcial (no un "firewall" atado a la spec)]

propuesta: real
esperado: https://github.com/git-ai-project/git-ai
confirmado: parcial

---

## 13 · 47bf5f9f · No one monetizes backendless software

- Verificada por: rubric, web · corridas: 2026-07-31
- Idea: The neighborhood contains fully client-side apps and self-hosted commerce/payment stacks that all assume a PHP server. What's missing is the bridge: a monetization/licensing layer for zero-backend software — selling license keys, unlocks, or subscriptions for apps that have no server to validate against. The backendless builders explicitly avoid servers, while the payment tools require them, leaving indie devs of local-first tools with no native way to charge. A lightweight license-key + edge-ve
- Veredictos:
  - **yes** (web, claude-sonnet-5 2026-08-10): Multiple existing products, especially Keylight, already provide exactly the described lightweight license-key-plus-edge-verification layer with payment integration for backendless client-side software.
  - **yes** (rubric, rubric-test/absence-47bf5f9f.md run 1): Multiple existing, actively maintained products (Keygen, Cryptolens, Keylight, Keyforge, LicenseGate) already provide exactly the described bridge: license-key issuance, edge/offline cryptographic verification for backendless client apps, and payment-to-license automation via Stripe or similar, so t
  - **yes** (rubric, rubric-test/absence-47bf5f9f.md run 2): Multiple mature, actively marketed products (Keygen, Keylight, Keyforge, Keymint, Cryptolens, LicenseSeat) already offer exactly the described bridge — offline/edge-verifiable license keys with Stripe-driven, backend-free issuance for client-side apps and extensions.
- Evidencia (prior art citado por Constellate):
  - https://keylight.dev/ — Keylight: A hosted licensing layer that mints Ed25519-signed license keys tied to Stripe payments and verifies them locally in the client app with no runtime server call, [✗ sin repo ni Show HN en el corpus]
  - https://keygen.sh/ — Keygen: A software licensing and distribution API/SDK supporting node-locked, floating, offline, or subscription licensing for desktop and on-premise apps, with a Fair  [✓ show_hn:14538351 (url exacta)]
  - https://help.cryptolens.io/examples/key-verification — Cryptolens: A cloud-based license management platform offering key generation, activation management, and offline validation via SDKs, targeted at desktop software vendors. [✓ github:Cryptolens/cryptolens-python (heurístico, revisar: repo con homepage cryptolens.io)]
  - https://freemius.com/blog/software-licensing-solutions/ — Keymint: A developer-first licensing API for indie makers of desktop and SaaS software, offering offline licensing and floating sessions at low cost. [✗ sin repo ni Show HN en el corpus]
  - https://keyforge.dev/features/offline — Keyforge: License management service with payment integrations and a self-service customer portal that provides offline, JWT-based license verification usable from client [✓ show_hn:44635244 (url exacta)]
  - https://licensemanager.at/license-key-generator-tools/ — LicenseGate: Offers a free cloud licensing service enabling basic API-based license verification for apps without the developer needing to run a backend. [✗ sin repo ni Show HN en el corpus]
  - https://keymint.dev/ — Keymint: A developer-first licensing API supporting offline license files (Ed25519 JWTs) verified locally, machine activation, and floating sessions for desktop/CLI/plug [✗ sin repo ni Show HN en el corpus]
  - https://licenseseat.com/software-licensing-api — LicenseSeat: A software licensing API/service that validates license keys, manages device activations, checks entitlements, and supports offline licensing so vendors don't b [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Dodo Payments (license keys sin backend) https://dodopayments.com/blogs/monetize-chrome-extension ; Monetize.software https://monetize.software/en ; LicenseSeat [fuerte (coincide con el "yes" de constellate)]

propuesta: real
esperado: https://github.com/Cryptolens/cryptolens-python show_hn:14538351 show_hn:44635244
confirmado: real

---

## 14 · c9d908b1 · Everyone Densifies Rewards; Nobody Benchmarks Reward Densification

- Verificada por: rubric, web · corridas: 2026-07-31
- Idea: Five papers independently convert sparse outcome rewards into dense signals—via transitions, hierarchies, group reflection, counterfactual token credit, and unlearning-specific shaping—each with bespoke evaluation. What's missing is a standardized benchmark or diagnostic suite that measures dense-reward schemes head-to-head on credit-assignment fidelity, hackability, and transfer across tasks. Without it, the field cannot tell whether these methods are complementary, redundant, or reward-hacking
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several benchmarks exist for evaluating process/step-level reward models and reward hacking in specific settings (math reasoning, tool-use agents, rubric-based RL), but none provide a standardized, unified suite that head-to-head compares the diverse dense-reward densification techniques (transition
  - **partially** (rubric, rubric-test/absence-c9d908b1.md run 1): Existing benchmarks (PRMBench, RewardBench, RHB) evaluate reward models or hacking exploits in isolation but none puts dense-reward densification methods from different families through a shared head-to-head evaluation on credit-assignment fidelity, hackability, and transfer, leaving the described g
  - **partially** (rubric, rubric-test/absence-c9d908b1.md run 2): - **(a) Missing piece:** No existing artifact runs the actual dense-reward densification mechanisms themselves (transition-based, hierarchical, group-reflective, counterfactual-token, and unlearning-specific shaping) on shared tasks to score them head-to-head on credit-assignment fidelity, hackabili
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2501.03124 — PRMBench: A fine-grained benchmark for process-level reward models offering over 6,000 problems with 80,000 step annotations and multidimensional labels covering simplici [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2505.23474 — Socratic-PRMBench: A benchmark that systematically evaluates PRMs' error-detection ability across six reasoning patterns (Transformation, Decomposition, Regather, Deduction, Verif [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2605.02964v1 — Reward Hacking Benchmark (RHB): A multi-step tool-use benchmark with independent and chained task regimes across data pipeline, log forensics, performance optimization, and multi-file reconstr [✗ sin repo ni Show HN en el corpus]
  - https://www.emergentmind.com/topics/reward-hacking-benchmark-rhb — CHERRL (Reward Hacking in Rubric-Based Reinforcement Learning): Formalizes rubric-based RL as a contextual bandit and injects canonical biases (lexical, format, tone, self-praise) to reproduce and timestamp reward-hacking on [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2510.08049 — A Survey of Process Reward Models (benchmark section): Surveys and summarizes existing PRM benchmarks (PRMBench, ProcessBench, Socratic-PRMBench) noting differences in scale, domain, and evaluation focus for dense s [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2501.03124 — PRMBench: A process-level benchmark with 6,216 problems and 83,456 step-level labels that evaluates process reward models' fine-grained error-detection capabilities acros [✗ sin repo ni Show HN en el corpus]
  - https://www.emergentmind.com/topics/rewardbench-ef6d937c-a4c4-457d-a060-516a18476bd2 — RewardBench: An open benchmark suite with standardized datasets, protocols, and leaderboards to assess and compare reward models across chat, safety, reasoning, and multimod [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2605.02964 — Reward Hacking Benchmark (RHB): A suite of multi-step tool-use tasks with naturalistic shortcut opportunities used to measure how often LLM agents exploit reward/evaluation weaknesses rather t [✗ sin repo ni Show HN en el corpus]
  - https://github.com/xxzcc/Awesome-Credit-Assignment-in-LLM-RL — Awesome-Credit-Assignment-in-LLM-RL: A curated, regularly-updated catalog and taxonomy of 47+ credit-assignment methods for LLM RL along with a list of related benchmarks and a method decision guid [✓ github:xxzcc/Awesome-Credit-Assignment-in-LLM-RL (repo)]
  - https://arxiv.org/abs/2604.09459 — From Reasoning to Agentic: Credit Assignment in Reinforcement Learning for Large Language Models (survey + benchmark protocol spec): Surveys 47 credit-assignment/dense-reward methods and proposes a benchmark protocol specification with task families and controlled bifurcation tasks, plus a me [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://github.com/xxzcc/Awesome-Credit-Assignment-in-LLM-RL https://arxiv.org/pdf/2501.03124 https://arxiv.org/abs/2505.23474 https://arxiv.org/html/2605.02964v1 https://www.emergentmind.com/topics/reward-hacking-benchmark-rhb https://arxiv.org/pdf/2510.08049 https://arxiv.org/abs/2501.03124 https://www.emergentmind.com/topics/rewardbench-ef6d937c-a4c4-457d-a060-516a18476bd2 https://arxiv.org/abs/2605.02964 https://arxiv.org/abs/2604.09459 https://arxiv.org/html/2605.21384v1 https://arxiv.org/abs/2403.13787
confirmado: parcial

---

## 15 · 730e3203 · The missing glue: identity and interop for self-hosted stacks

- Verificada por: rubric, web · corridas: 2026-07-31
- Idea: Four apps that a single clinic, village office, or small business would plausibly run together — files, health/citizen records, invoicing — each with its own users, backups, and auth. The neighborhood's internal structure screams for the missing piece: a lightweight identity/SSO and data-sync layer that lets these self-hosted PHP monoliths behave like one coherent stack. Enterprise answers (Keycloak, LDAP) exist but are wildly over-scoped for the small institutions these tools target. The gap is
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Lightweight identity layers (Authelia, Authentik, LLDAP) and generic self-hosted app-management platforms (Cloudron, YunoHost) each solve part of the described gap — small-scale SSO or unified user/app management — but none combine an opinionated identity layer with cross-app data-sync tailored to a
  - **partially** (rubric, rubric-test/absence-730e3203.md run 1): Cloudron/YunoHost/Authentik already give small orgs a lightweight, opinionated identity/SSO control plane across self-hosted PHP monoliths, but the described 'data-sync' half of the gap (reconciling records across clinic/citizen/invoicing apps) remains unaddressed by any product found.
  - **partially** (rubric, rubric-test/absence-730e3203.md run 2): Cloudron and YunoHost are opinionated small-org 'control planes' that already bundle SSO, backups, and app management for self-hosted stacks, but their SSO glue depends on apps being pre-integrated into their own catalogs, leaving legacy vertical monoliths like OpenEMR/OpenSID without a plug-and-pla
- Evidencia (prior art citado por Constellate):
  - https://www.cloudron.io/store/com.nextcloud.cloudronapp.html — Cloudron: A self-hosted platform for installing, managing, and securing multiple web apps on one server, with centralized user accounts, backups, and automatic SSL/DNS —  [✓ show_hn:9976992 (heurístico, revisar: Show HN del dominio cloudron.io: "Cloudron – Get Your Own Cloud")]
  - https://yunohost.org/ — YunoHost: A Debian-based self-hosted server OS that automates installation and administration of web apps for individuals and small organizations, including a built-in si [✓ github:YunoHost/yunohost (heurístico, revisar: repo con homepage yunohost.org)]
  - https://goauthentik.io/ — Authentik: A full open-source identity provider with OIDC, SAML, LDAP, SCIM provisioning, enrollment flows and an admin UI, positioned as a middle ground between minimal a [✓ github:goauthentik/authentik (heurístico, revisar: repo con homepage goauthentik.io)]
  - https://www.authelia.com/ — Authelia: A lightweight, single-binary forward-auth gateway that adds centralized login, SSO, and MFA in front of self-hosted apps behind a reverse proxy. Authelia sits b [✓ github:authelia/authelia (heurístico, revisar: repo con homepage authelia.com)]
  - https://github.com/lldap/lldap — LLDAP: A minimal, lightweight LDAP directory server built for small self-hosted setups needing a shared user directory. LLDAP isn't an SSO solution — it's a minimal LD [✓ github:lldap/lldap (repo)]
  - https://www.cloudron.io/ — Cloudron: Open source self-hosting platform that provides one-click app installs, automated backups/updates, and centralized SSO/user management (via LDAP) so users share [✓ show_hn:9976992 (heurístico, revisar: Show HN del dominio cloudron.io: "Cloudron – Get Your Own Cloud")]
  - https://github.com/pocket-id/pocket-id — Pocket ID: Minimal, passkey-first self-hosted OIDC provider positioned as a low-overhead alternative for adding SSO to self-hosted apps. [✓ github:pocket-id/pocket-id (repo)]
  - https://www.keycloak.org/ — Keycloak: Full-featured open-source identity and access management system (already noted in the gap description as over-scoped for small institutions). [✓ github:keycloak/keycloak (heurístico, revisar: repo con homepage keycloak.org)]
- Búsqueda propia (sep-2026, complementaria): Authentik (SSO para stack self-hosted) https://github.com/goauthentik/authentik ; Zitadel ; Kopia para backups ; YunoHost [fuerte]

propuesta: parcial
esperado: https://github.com/lldap/lldap https://github.com/pocket-id/pocket-id https://www.cloudron.io/store/com.nextcloud.cloudronapp.html https://yunohost.org/ https://goauthentik.io/ https://www.authelia.com/ https://www.cloudron.io/ https://www.keycloak.org/
confirmado: parcial

---

## 16 · 8b190bdc · Everyone Audits Bias; Nobody Ships the Bias Firewall

- Verificada por: web · corridas: 2026-07-16
- Idea: Recommendation bias auditing, ideological drift under temperature, judge/generator asymmetry, and hallucination detection all diagnose how LLM curation and evaluation silently distort content. What's missing is the operational counterpart: a runtime middleware that intercepts LLM curation/judging outputs, scores them for ideological and pragmatic skew, and normalizes or flags them before they reach users. The neighborhood has abundant measurement instruments but no deployable mitigation layer—a 
- Veredictos:
  - **yes** (web, output.json): Runtime guardrail middleware that intercepts model output, scores it for bias and filters or flags it before users see it is a mature, widely deployed category rather than a missing one.
- Evidencia (prior art citado por Constellate):
  - https://www.guardrailsai.com/ — Guardrails AI: Open-source framework validating and correcting LLM outputs against declarative rules at runtime. [✓ github:guardrails-ai/guardrails (heurístico, revisar: repo con homepage guardrailsai.com)]
  - https://github.com/NVIDIA/NeMo-Guardrails — NVIDIA NeMo Guardrails: Programmable rails constraining LLM conversations and outputs, including bias and toxicity rails. [✗ repo fuera del bulk]
  - https://docs.langchain.com/oss/python/langchain/guardrails — LangChain guardrails middleware: Middleware hooks running checks around model and tool calls, before and after execution. [✗ sin repo ni Show HN en el corpus]
  - https://www.confident-ai.com/blog/llm-guardrails-the-ultimate-guide-to-safeguard-llm-systems — Confident AI / DeepEval guardrails: Production guardrail suite scoring outputs for bias, toxicity and leakage inline. [✗ sin repo ni Show HN en el corpus]
  - https://futureagi.com/blog/fairness-in-ai-how-to-detect-and-mitigate-bias-in-llm-outputs-using-future-agi-metrics/ — Future AGI fairness metrics: Bias detection and mitigation metrics applied to LLM outputs in production. [✓ github:future-agi/future-agi (heurístico, revisar: repo con homepage futureagi.com)]
- Búsqueda propia (sep-2026, complementaria): Guardrails AI (validadores incl. bias) https://github.com/guardrails-ai/guardrails ; NeMo Guardrails [fuerte]

propuesta: real
esperado: https://github.com/guardrails-ai/guardrails https://github.com/NVIDIA-NeMo/Guardrails
confirmado: real

---

## 17 · 7c597ec1 · Everyone Builds Benchmarks, Nobody Builds Benchmark Infrastructure

- Verificada por: web · corridas: 2026-07-16
- Idea: This neighborhood contains at least four new domain benchmarks (Vietnamese legal, European medical, advanced math, citation-grounded QA), while 364 explicitly diagnoses the field's failure to accumulate and reuse knowledge. The missing piece is the meta-layer: a system for composing, versioning, deduplicating, and tracking the lifespan of benchmarks so they accumulate rather than pile up. The community keeps shipping one-off evals that ironically reproduce the knowledge-fragmentation problem 364
- Veredictos:
  - **yes** (web, output.json): The meta-layer already exists: lm-evaluation-harness and Inspect AI compose and version benchmarks, and Every Eval Ever is explicitly a unifying schema and repository for accumulating evaluation results.
- Evidencia (prior art citado por Constellate):
  - https://github.com/EleutherAI/lm-evaluation-harness — EleutherAI lm-evaluation-harness: Unified framework with a task registry, versioned configs and 200+ benchmarks across 25+ model backends. [✓ github:EleutherAI/lm-evaluation-harness (repo)]
  - https://arxiv.org/pdf/2606.14516 — Every Eval Ever: Unifying schema and community repository translating results across incompatible eval harnesses. [✗ sin repo ni Show HN en el corpus]
  - https://inspect.aisi.org.uk/ — Inspect AI: UK AI Security Institute framework with 100+ composable evaluation templates. [✓ github:UKGovernmentBEIS/inspect_ai (heurístico, revisar: repo con homepage inspect.aisi.org.uk)]
  - https://crfm.stanford.edu/helm/ — Stanford HELM: Living benchmark suite tracking many scenarios and models over time with versioned releases. [✓ github:stanford-crfm/helm (heurístico, revisar: repo con homepage crfm.stanford.edu)]
  - https://github.com/open-compass/opencompass — OpenCompass: Evaluation platform aggregating a large catalogue of benchmarks behind one runner. [✓ github:open-compass/opencompass (repo)]
- Búsqueda propia (sep-2026, complementaria): lm-evaluation-harness (tareas en YAML, backend del Open LLM Leaderboard) https://github.com/EleutherAI/lm-evaluation-harness ; Inspect (UK AISI) https://github.com/UKGovernmentBEIS/inspect_ai [fuerte (coincide con el "yes" de constellate)]

propuesta: real
esperado: https://github.com/EleutherAI/lm-evaluation-harness https://github.com/UKGovernmentBEIS/inspect_ai https://github.com/open-compass/opencompass
confirmado: real

---

## 18 · a3ced3a9 · Everyone Edits Models, Nobody Verifies the Edit

- Verificada por: web · corridas: 2026-07-16
- Idea: Four papers intervene directly on model internals: pruning unsafe subnetworks, real-time unlearning, activation steering, and mechanistic bias localization. All assume the intervention worked, yet the neighborhood contains no tool for independently auditing whether an edit actually removed the behavior, preserved capabilities, and didn't create new failures. The missing piece is a standardized 'edit verification' layer — a diff-and-regression harness for model surgery, analogous to CI tests for 
- Veredictos:
  - **yes** (web, output.json): Edit verification is an established sub-field: MUSE, TOFU and RWKU test whether an intervention removed the behaviour while preserving capabilities, and capability regression is routinely measured with lm-evaluation-harness.
- Evidencia (prior art citado por Constellate):
  - https://muse-bench.github.io/ — MUSE: Six-way unlearning benchmark checking removal, privacy leakage, utility preservation, scalability and sustainability. [✗ sin repo ni Show HN en el corpus]
  - https://locuslab.github.io/tofu/ — TOFU: Benchmark evaluating unlearning with model-utility and forget-quality metrics on edited models. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2406.10890 — RWKU: Real-world knowledge unlearning benchmark probing whether targeted knowledge survives an edit. [✗ sin repo ni Show HN en el corpus]
  - https://github.com/EleutherAI/lm-evaluation-harness — lm-evaluation-harness (capability regression): Runs MMLU and similar suites before and after an intervention to detect capability loss. [✓ github:EleutherAI/lm-evaluation-harness (repo)]
  - https://arxiv.org/pdf/2602.14553 — Auditing for Machine Unlearning Compliance: Independent auditing procedures verifying that claimed unlearning actually occurred. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): MUSE (benchmark de unlearning, 6 propiedades) https://arxiv.org/abs/2407.06460 ; EasyEdit (evaluación de edición) https://github.com/zjunlp/EasyEdit [fuerte]

propuesta: real
esperado: https://github.com/zjunlp/EasyEdit
confirmado: parcial

---

## 19 · 6eb5b382 · Everyone builds agents; nobody builds agent identity

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood contains agent protocols, agentic workflows, agent orchestration, a secret scanner for humans' mistakes, and a tunnel client for secure access. What's structurally missing is the piece all of these imply: credential and identity management for autonomous agents — scoped, revocable, auditable secrets that agents can use without leaking them. Gitleaks catches human-committed secrets; nothing here prevents an agent with workflow permissions from exfiltrating or misusing them. Give
- Veredictos:
  - **yes** (web, claude-sonnet-5 2026-08-10): Multiple existing products (HashiCorp Vault's agentic security suite, Infisical Agent Vault, Astrix, Oasis Security, Defakto) already provide scoped, revocable, auditable credential/identity management specifically for AI agents, directly filling the described gap.
- Evidencia (prior art citado por Constellate):
  - https://www.hashicorp.com/en/products/vault/use-cases/agentic-runtime-security — HashiCorp Vault (Agentic Runtime Security): Issues dynamic, short-lived credentials and enforces least-privilege access for AI agents, with Boundary for session brokering and Vault Radar for secret scanni [✓ github:hashicorp/vault-secrets-operator (heurístico, revisar: repo con homepage hashicorp.com)]
  - https://github.com/Infisical/agent-vault — Infisical Agent Vault: An HTTP credential proxy and vault built specifically for AI agents (e.g., Claude Code) that injects credentials into outbound requests without exposing them to [✓ github:Infisical/agent-vault (repo)]
  - https://astrix.security/ — Astrix Security (now part of Cisco): Secures AI agent and non-human identities with governance, least-privilege access, centralized secret management, and full audit trails. [✗ sin repo ni Show HN en el corpus]
  - https://www.oasis.security/ — Oasis Security: Non-human identity management platform that secures AI agents and NHIs across cloud/SaaS/PaaS environments, integrating with existing vaults and IAM systems. [✗ sin repo ni Show HN en el corpus]
  - https://www.defakto.security/product/ — Defakto (Mind): Extends non-human identity management to AI agents and LLMs, replacing static API keys with dynamic, verifiable identities and scoped policies plus audit trails [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): ZeroID (identidad open source para agentes, delegación RFC 8693) https://www.helpnetsecurity.com/2026/04/13/zeroid-open-source-identity-platform-autonomous-ai-agents/ ; OpenAgents AgentID ; Ory [fuerte]

propuesta: real
esperado: https://github.com/Infisical/agent-vault
confirmado: real

---

## 20 · 07878479 · Missing: The Ambient Home Health Early-Warning Layer

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood contains camera-free WiFi vital sensing, cheap edge-deployable activity recognition, a framework for capturing multimodal ambient human data, longitudinal clinical anomaly scoring, and near-anomaly prediction before failure. Every ingredient exists for a passive, privacy-preserving system that watches a person's daily physiological and behavioral baseline and flags drift before a clinical event — yet no idea in the set connects sensing to longitudinal prediction. The gap is the
- Veredictos:
  - **yes** (web, claude-sonnet-5 2026-08-10): Multiple existing commercial and clinical-research systems (CarePredict Tempo, Sensorum Health, DomoHealth/Emfit-based HF decompensation studies) already implement the exact integration described: continuous passive ambient/physiological sensing feeding per-person baseline models that flag deviation
- Evidencia (prior art citado por Constellate):
  - https://www.carepredict.com/news/carepredict-launches-tempo-series-3 — CarePredict Tempo: An AI-powered wearable-plus-in-home-beacon platform that learns a senior's normal activity and behavior pattern and predicts the probability of health decline f [✗ sin repo ni Show HN en el corpus]
  - https://www.centerwatch.com/clinical-trials/listings/NCT05865184/evaluation-of-home-based-sensor-system-to-detect-health-decompensation-in-elderly-patients-with-history-of-chf-or-copd — Sensorum Health: A proprietary passive, ambient home-based sensor network with clinical staff-in-the-loop analytics that aims to identify early signals of health decompensation  [✗ sin repo ni Show HN en el corpus]
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11179017/ — DomoHealth / DomoSafety ambient sensor system with Emfit bed sensor: Combines passive infrared motion sensors and a contact-free under-mattress piezoelectric sensor to track activity, toilet visits, heart rate, respiration, and s [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2508.03436 — AI on the Pulse (UniTS-based ambient/wearable anomaly detection research prototype): A research system using a universal time-series model to learn patient-specific baselines from combined wearable and ambient home-care data and flag real-time d [✗ sin repo ni Show HN en el corpus]
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5746778/ — Radar-based smart sensor for ambient assisted living (UWB radar monitoring): Uses ultra-wideband radar for camera-free, privacy-preserving detection of vital signs (cardiorespiratory) and body movement abnormalities to catch early signs  [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Wi-Fi Sensing de Deutsche Telekom (caídas, respiración/pulso sin cámaras) https://www.telekom.com/en/newsroom/latest-updates/erklaerstuecke/2025/02/wi-fi-sensing ; WiLife (paper) [parcial-fuerte (sensado sí; capa de alerta temprana longitudinal no del todo)]

propuesta: real
esperado: 
confirmado: descartar

---

## 21 · fbe3c4c2 · Skills Get Made and Listed, Never Tested

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood has a full skill supply chain: automated generation from books, industrial prompt-template mining, packaging into agent runtimes via MCP, and curation lists. What's structurally missing is the quality layer: nothing here evaluates, benchmarks, or certifies whether a skill actually works, is safe, or degrades across model versions. As skills become distributable artifacts, an 'npm audit / CI for agent skills' is the obvious gap that lists alone can't fill.
- Veredictos:
  - **yes** (web, claude-sonnet-5 2026-08-10): Multiple existing tools (SkillTester, Cisco Skill Scanner, Snyk Agent Scan, skill-audit, and Anthropic's own skill-creator benchmarking) already provide security scanning, quality auditing, and cross-model-version benchmarking for agent skills, collectively covering the described 'npm audit / CI for
- Evidencia (prior art citado por Constellate):
  - https://skilltester.ai/ — SkillTester (skilltester.ai): A published tool and framework that benchmarks third-party agent skills on both utility and security, producing a utility score, a security score, and a three-l [✗ sin repo ni Show HN en el corpus]
  - https://github.com/cisco-ai-defense/skill-scanner — Cisco AI Defense Skill Scanner: Open-source CLI that scans Agent Skill packages (Codex, Cursor, and related formats) using YAML/YARA static rules, Python bytecode checks, dependency intelligen [✓ github:cisco-ai-defense/skill-scanner (repo)]
  - https://github.com/snyk/agent-scan — Snyk Agent Scan – Skill Inspector: Security scanner for AI agent skills and MCP servers that detects malicious skills, insecure configurations, and leaked secrets, with a CLI built for automation [✓ github:snyk/agent-scan (repo)]
  - https://github.com/dabit3/skill-audit — dabit3/skill-audit: CLI tool that audits skill definitions for security, completeness, and cross-platform compatibility (Codex, Claude Code, OpenClaw, etc.), producing quality scor [✗ repo fuera del bulk, ★47]
  - https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills — Anthropic skill-creator (with eval/benchmark mode): Official Anthropic tool that lets skill authors write evals, run a benchmark mode tracking pass rate/time/tokens, and detect regressions or 'outgrowth' as model [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): mcp-probe (CLI que puntúa servidores MCP antes de publicar) https://dev.to/incultnitollc/the-mcp-server-pre-publish-checklist-5h4e ; MCP Inspector [fuerte]

propuesta: real
esperado: https://github.com/cisco-ai-defense/skill-scanner https://github.com/snyk/agent-scan https://github.com/dabit3/skill-audit
confirmado: real

---

## 22 · 128b8602 · AI maintenance layer for the legacy PHP long tail

- Verificada por: web · corridas: 2026-07-31
- Idea: laravel/boost shows AI tooling arriving for modern PHP, while frontier models (DeepSeek-V4-Flash, MAI-Cyber-1) get cheap and specialized. Meanwhile the actual pain lives in ideas like the WooCommerce free-trial debugging saga and sprawling apps like Invoice Ninja: legacy plugin ecosystems where bugs hide in configuration and caching, not code. The missing piece is an MCP/AI agent purpose-built for WordPress/WooCommerce and legacy PHP maintenance — the market is enormous and utterly unserved comp
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Numerous MCP servers and AI agents already connect AI assistants to WordPress/WooCommerce for content and store management, and some (like InstaWP's debugging workflow or Angie's roadmap) touch on troubleshooting, but no found product is purpose-built as a maintenance/debugging specialist for legacy
- Evidencia (prior art citado por Constellate):
  - https://www.siteground.com/blog/siteground-ai-agent-for-wordpress — SiteGround AI Agent for WordPress: A hosting-integrated conversational AI agent that manages WordPress/WooCommerce maintenance tasks like plugin/theme updates, user management, and site settings  [✗ sin repo ni Show HN en el corpus]
  - https://elementor.com/products/angie-ai-for-wordpress/ — Elementor Angie: Agentic AI for WordPress site creation and management that supports WooCommerce and other major plugins, with a roadmap toward specialized troubleshooting agent [✗ sin repo ni Show HN en el corpus]
  - https://instawp.com/fix-wordpress-bug-ai/ — InstaWP AI-assisted WordPress debugging (with MCP): Provides a WordPress sandbox plus built-in MCP server so AI clients like Claude can inspect plugin data, site health, and help debug issues such as plugin confl [✗ sin repo ni Show HN en el corpus]
  - https://wordpress.org/plugins/wsp-mcp-ai-agents-connector/ — WSP MCP – AI Agents Connector: Turns a WordPress site into a native MCP server exposing posts, pages, WooCommerce (products, orders, refunds, coupons), ACF, Elementor, and Gravity Forms tools [✗ sin repo ni Show HN en el corpus]
  - https://developer.woocommerce.com/docs/features/mcp/ — WooCommerce official MCP integration: WooCommerce's own MCP layer built on the WordPress Abilities API, exposing product and order management abilities to AI agents. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Rector (upgrades y refactor automáticos de PHP 5.3->8.5) https://github.com/rectorphp/rector [parcial (automatización sí, "capa de mantenimiento con IA" para el long tail de WooCommerce no)]

propuesta: parcial
esperado: https://www.siteground.com/blog/siteground-ai-agent-for-wordpress https://elementor.com/products/angie-ai-for-wordpress/ https://instawp.com/fix-wordpress-bug-ai/ https://wordpress.org/plugins/wsp-mcp-ai-agents-connector/ https://developer.woocommerce.com/docs/features/mcp/
confirmado: parcial

---

## 23 · 6ec58e83 · Agents Can Talk Cross-Cloud but Nobody Verifies Who They Are

- Verificada por: web · corridas: 2026-07-31
- Idea: 5156 and 5171 show agent-to-agent protocols working across Google, Azure, and AWS; 4708 shows detectors can't even classify agent traffic; 4621 and 4197 show accountability and threat modeling breaking down under GenAI. The missing piece is an agent identity and attestation layer: verifiable credentials that let a receiving agent or website know which agent, on whose behalf, with what permissions, is calling. Interop is being built faster than identity, and every paper here dances around that ga
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple standards efforts (W3C Agent Identity CG, ANS, SPIFFE/SPIRE), academic DID/VC frameworks, and vertical products (Truvera, AP2, Visa Trusted Agent) each address pieces of agent identity and attestation, but none yet unifies them into the general-purpose, cross-cloud verifiable-identity layer
- Evidencia (prior art citado por Constellate):
  - https://www.w3.org/community/agent-identity/ — W3C Agent Identity Registry Protocol Community Group: Develops open specifications letting AI agents present cryptographically verifiable credentials binding them to controlling organizations for cross-org trust ne [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2505.10609 — Agent Name Service (ANS): A universal directory for AI agent discovery that defines agent identity as cryptographic identity (PKI certificate), logical identity (ANSName), and protocol-s [✗ sin repo ni Show HN en el corpus]
  - https://www.strata.io/glossary/agent-authentication/ — SPIFFE/SPIRE: An open standard and production implementation for issuing and rotating cryptographic workload identities, increasingly used in cloud-native agent deployments t [✗ sin repo ni Show HN en el corpus]
  - https://www.dock.io/post/ai-agent-digital-identity-verification — Truvera (Dock.io) Agent Identity: A commercial platform issuing verifiable, portable agent-identity credentials that cryptographically bind an agent to its creating organization and let any syst [✗ sin repo ni Show HN en el corpus]
  - https://eco.com/support/en/articles/15192005-agent-identity-verification-how-ai-agents-authenticate-purchases-in-2026 — Google AP2 / Visa Trusted Agent Protocol (agent payment attestation): Payment-specific attestation schemes (AP2 uses W3C Verifiable Credentials for auditable consent; Visa's protocol uses attestation headers carrying agent operato [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): sigstore-a2a (firma de Agent Cards) https://github.com/sigstore/sigstore-a2a ; propuesta A2A #1672 ; Agent Name Service (paper) [fuerte]

propuesta: parcial
esperado: https://www.w3.org/community/agent-identity/ https://arxiv.org/pdf/2505.10609 https://www.strata.io/glossary/agent-authentication/ https://www.dock.io/post/ai-agent-digital-identity-verification https://eco.com/support/en/articles/15192005-agent-identity-verification-how-ai-agents-authenticate-purchases-in-2026
confirmado: parcial

---

## 24 · ba4a9968 · Companion AI Has No Wellbeing Monitor

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood contains self-hosted AI companions, evaluation of role-play agents for emotional comfort, voice-based psychotherapy training, and speech biomarkers for depression. The missing piece is obvious once laid out: a passive layer that applies clinical speech-biomarker detection inside companion/role-play conversations to flag deteriorating user mental health and adapt or escalate. Everything needed exists — the intimate voice channel, the eval frameworks, the biomarkers — but no one 
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Clinical voice-biomarker platforms (Sonde Health, Kintsugi, CompanionMX) exist and companion apps (Replika, Wysa) have basic text-based distress detection, but no found product unifies validated clinical speech-biomarker detection inside an intimate companion/role-play AI conversation to passively f
- Evidencia (prior art citado por Constellate):
  - https://www.sondehealth.com/mental-health — Sonde Health (Sonde Mental Fitness / Vocal Biomarker API): A clinically validated vocal biomarker API/SDK that analyzes acoustic and prosodic features from brief voice samples to score mental fitness and flag depression [✗ sin repo ni Show HN en el corpus]
  - https://www.psychiatry.org/news-room/apa-blogs/vocal-biomarkers-for-mental-health — Kintsugi Voice Biomarker API (KiVA): An API-first platform that detects depression and anxiety from short clips of free-form speech using clinical voice biomarkers, integrating with call centers, t [✗ sin repo ni Show HN en el corpus]
  - https://www.fastcompany.com/90299135/mental-health-crisis-robots-chatbots-listeners — CompanionMX: An app that detects changes in mood by analyzing users' voice patterns and daily activity levels to support mental health tracking. [✗ sin repo ni Show HN en el corpus]
  - https://blog.replika.com/posts/creating-a-safe-replika-experience — Replika: An AI companion app that uses NLP (and some voice tone analysis) to detect emotional cues in conversation and offers crisis-category scripts and hotline redirec [✗ sin repo ni Show HN en el corpus]
  - https://clinicaltrials.gov/study/NCT05533190 — Wysa: A clinically validated AI-powered CBT companion chatbot with an 'emotionally intelligent' sentiment-detection layer that flags suicidal language and escalates c [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): SHIELD (supervisor LLM que detecta dinámicas emocionales riesgosas en companions; paper) https://arxiv.org/pdf/2510.15891 [parcial (investigación, no producto desplegado)]

propuesta: parcial
esperado: https://www.sondehealth.com/mental-health https://www.psychiatry.org/news-room/apa-blogs/vocal-biomarkers-for-mental-health https://www.fastcompany.com/90299135/mental-health-crisis-robots-chatbots-listeners https://blog.replika.com/posts/creating-a-safe-replika-experience https://clinicaltrials.gov/study/NCT05533190
confirmado: parcial

---

## 25 · eae1d11d · Everyone Audits Internals; Nobody Sells the Audit

- Verificada por: web · corridas: 2026-07-31
- Idea: These four ideas verify what happens inside opaque pipelines: certified constraint reformulation, causal audits of latent agent communication, representational probing of RL vs SFT models, and layered poisoning defenses for RAG. Each builds bespoke, one-off verification machinery for its own stack. What's conspicuously missing is a general-purpose, developer-facing 'trust layer'—a standardized toolkit that instruments any LLM pipeline (retrieval, agents, finetuning) with provenance checks and in
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Mature developer-facing observability/eval platforms like TruLens, Arize Phoenix, LangSmith, and Langfuse already provide general-purpose instrumentation and behavioral evaluation across retrieval and agent pipelines, but none combine this with certified formal verification, causal latent-communicat
- Evidencia (prior art citado por Constellate):
  - https://github.com/truera/trulens — TruLens: An open-source framework that instruments LLM apps (RAG, agents) with OpenTelemetry spans for every retrieval, generation, and tool call, then attaches feedback [✓ github:truera/trulens (repo)]
  - https://github.com/arize-ai/phoenix — Arize Phoenix: An open-source AI observability platform providing OpenTelemetry-based tracing, LLM-based evaluations (hallucination, faithfulness, relevance), dataset curation [✓ github:Arize-ai/phoenix (repo)]
  - https://arxiv.org/pdf/2606.09692 — LangSmith: A commercial LLM/agent observability platform giving developer-facing traces of LLM calls, tool invocations, and agent steps for debugging and monitoring, with  [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2606.04990 — Evidence Tracing / Execution Provenance framework (survey proposal): A proposed unified provenance framework/taxonomy connecting retrieval grounding, claim support, tool-use safety, memory lineage, and audit across agent pipeline [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://github.com/truera/trulens https://github.com/arize-ai/phoenix https://arxiv.org/pdf/2606.09692 https://arxiv.org/abs/2606.04990
confirmado: parcial

---

## 26 · 024eb0a0 · Everyone Builds Deepfake Engines, One Paper Builds Locks

- Verificada por: web · corridas: 2026-07-16
- Idea: This neighborhood is dense with generative video editing power: identity-consistent face editing, object insertion, frontier audio-video generation, and fully automated short-video engines. Only 2689 addresses protection, and only preemptively via adversarial perturbation of source content. Missing entirely: post-hoc detection, provenance watermarking, and verification tooling for generated/edited video — the defensive layer that this generative arsenal makes urgent. The gap is a video authentic
- Veredictos:
  - **partially** (web, output.json): Multiple real products (SynthID, C2PA/Content Credentials, Resemble AI, Attestiv, Steg.AI) already combine post-hoc detection, watermarking, and provenance verification for video, but each has significant limitations (model-specific coverage, opt-in provenance, enterprise-only pricing, or reliance o
- Evidencia (prior art citado por Constellate):
  - https://deepmind.google/models/synthid/ — Google SynthID (with SynthID Detector portal): Embeds imperceptible watermarks directly into AI-generated images, audio, text and video (e.g. via Veo) at creation time, and offers a verification portal where [✗ sin repo ni Show HN en el corpus]
  - https://contentcredentials.org/ — C2PA / Content Credentials (contentcredentials.org verify tool): An open standard and consumer verification tool that attaches cryptographically signed provenance manifests to media (including video) and lets anyone check ori [✗ sin repo ni Show HN en el corpus]
  - https://www.resemble.ai/deepfake-video-detection-guide/ — Resemble AI (Resemble Detect / DETECT-2B): A commercial multimodal deepfake detection platform offering real-time video/audio detection, invisible provenance watermarking (PerTH), and cross-modal (voice/ [✓ github:resemble-ai/resemble-unity-text-to-speech (heurístico, revisar: repo con homepage resemble.ai)]
  - https://attestiv.com/provenance-vs-forensics-the-best-solution-for-deepfake-detection/ — Attestiv: Attestiv provides authenticity and validation for digital photos, videos and documents using patented tamper-proofing and AI analysis, positioned as a forensic  [✗ sin repo ni Show HN en el corpus]
  - https://steg.ai/products/content-authentication/ — Steg.AI Content Verification: Steg AI invisibly watermarks digital content (images, videos, documents, audio) using in-house deep learning, and supports/extends the C2PA standard to allow la [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): PhotoGuard (MIT, inmuniza imágenes contra edición) https://github.com/MadryLab/photoguard ; MIRAGE (paper) [fuerte (imágenes; video menos)]

propuesta: parcial
esperado: https://www.resemble.ai/deepfake-video-detection-guide/ https://deepmind.google/models/synthid/ https://contentcredentials.org/ https://attestiv.com/provenance-vs-forensics-the-best-solution-for-deepfake-detection/ https://steg.ai/products/content-authentication/ !github:resemble-ai/resemble-unity-text-to-speech
confirmado: parcial

---

## 27 · ad6c4d56 · Everyone Builds Spatial Patches, Nobody Builds Spatial Memory

- Verificada por: web · corridas: 2026-07-16
- Idea: Geolocalization, street-view cognition, 3D-from-2D reasoning, temporal change detection, and navigation maps each bolt a domain-specific spatial scaffold onto a VLM. The structural gap: a shared, persistent spatial-temporal representation layer — a queryable world-state memory that any VLM task could read from and write to. Each paper reinvents fragments of it (knowledge graphs, latent anchors, semantic maps) as one-off, non-composable fixes. The missing piece is spatial memory as infrastructure
- Veredictos:
  - **partially** (web, output.json): Several research systems now build persistent queryable spatial memory (SuperMap, VL-KnG, VLM2), but each ships as its own framework, so the shared composable infrastructure layer the gap describes still does not exist.
- Evidencia (prior art citado por Constellate):
  - https://superodometry.com/supermap — SuperMap: Training-free 4D spatio-temporal mapping that yields a persistent, queryable scene graph used as unified spatial memory. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2510.01483 — VL-KnG: Builds spatiotemporal knowledge graphs from egocentric video as persistent scene memory for embodied QA. [✗ sin repo ni Show HN en el corpus]
  - https://sairlab.org/vlm2/ — VLM2: Vision-language model with a dual working/episodic memory module for spatial reasoning. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2510.08553 — Memoir: Imagination-guided retrieval over explicit viewpoint-anchored memory for vision-and-language navigation. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2606.08992 — SpaceVLN: Zero-shot navigation agent maintaining online spatial cognitive memory of explored regions and landmarks. [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://superodometry.com/supermap https://arxiv.org/abs/2510.01483 https://sairlab.org/vlm2/ https://arxiv.org/pdf/2510.08553 https://arxiv.org/pdf/2606.08992
confirmado: parcial

---

## 28 · 10e73cb1 · Everyone Claims Transfer; Nobody Measures It Comparably

- Verificada por: web · corridas: 2026-07-31
- Idea: Five papers claim cross-task, cross-scale, cross-domain, or cross-modal graph transfer, and 4163 explicitly complains about incompatible splits and protocols. Yet the neighborhood contains no shared benchmark or evaluation harness that stress-tests these transfer claims under one protocol. The missing piece is a 'transfer-GLUE for graphs': a standardized suite with controlled splits, negative-sampling conventions, and scale/domain/modality axes. Given how loudly each paper claims generalization,
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several recent benchmarks (GraphGLUE, GFMBench, GraphBench, GSTBench, and the text-space GFM benchmark) each standardize evaluation for a subset of transfer claims, but none unifies cross-task, cross-scale, cross-domain, and cross-modal axes with shared splits and negative-sampling conventions the w
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2603.00618 — GraphGLUE (from "Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models"): A named benchmark comparing cross-domain transfer learning performance across six representative domains (citation, co-purchase, social, knowledge graph, bioinf [✗ sin repo ni Show HN en el corpus]
  - https://dl.acm.org/doi/10.1145/3711896.3737410 — GFMBench: An open-source pipeline that standardizes the training, evaluation, and deployment of Graph Foundation Models, integrating state-of-the-art GFMs and datasets wi [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2512.04475 — GraphBench: A next-generation benchmarking suite spanning diverse domains (social networks, circuits, chip design, combinatorial optimization, SAT solving, algorithmic reas [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2509.06975 — GSTBench: The first systematic benchmark for evaluating the transferability of graph self-supervised learning methods, pretraining at scale on ogbn-papers100M and evaluat [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2406.10727 — Text-space Graph Foundation Models Benchmark: A benchmark designed for developing text-space GFMs with novel datasets and comprehensive evaluation protocols including in-context learning and fine-tuning acr [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/pdf/2603.00618 https://dl.acm.org/doi/10.1145/3711896.3737410 https://arxiv.org/html/2512.04475 https://arxiv.org/abs/2509.06975 https://arxiv.org/html/2406.10727
confirmado: parcial

---

## 29 · 5f3f3eaa · Everyone Composes Queries; Nobody Built the Composition Layer

- Verificada por: web · corridas: 2026-07-16
- Idea: Sketch+text retrieval, recipe-image retrieval via MLLMs, composed image retrieval, and agentic query reformulation for editing all wrestle with the same problem: users express intent through messy multi-modal fragments that must be fused into one query. Each paper builds a bespoke fusion for its modality pair. The missing piece is a modality-agnostic query composition layer—an interface/API that takes any mix of image, sketch, and text fragments, reformulates them (as 456 does for editing), and 
- Veredictos:
  - **partially** (web, output.json): Several commercial and research systems (Voyage AI, MagicLens, Marqo, Vertex AI/Azure multimodal embeddings, an Adobe sketch-canvas patent) already produce unified embeddings from mixed image/text (and in one patent, sketch) inputs, but none combine sketch+text+image inputs with an agentic reformula
- Evidencia (prior art citado por Constellate):
  - https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12271983 — Adobe unified multi-modal canvas embedding (patent US12271983): Describes a system that takes a canvas with sketch, brush, image, and text inputs, generates segment-level semantic and layout embeddings, and fuses them into a [✗ sin repo ni Show HN en el corpus]
  - https://zilliz.com/blog/combine-image-and-text-how-multimodal-retrieval-transforms-search — MagicLens: MagicLens uses Transformer models to process text and images in parallel, generating a unified embedding that captures both modalities and enhances retrieval pe [✗ sin repo ni Show HN en el corpus]
  - https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/ — voyage-multimodal-3 (Voyage AI): voyage-multimodal-3 vectorizes both modalities of data directly within the same transformer encoder, ensuring that text and visual features form a unified repre [✗ sin repo ni Show HN en el corpus]
  - https://github.com/api-evangelist/marqo — Marqo: Marqo is an open-source, multimodal vector search engine that lets developers index text and images, generate embeddings on the fly, and run tensor, lexical, an [✗ repo fuera del bulk]
  - https://cloud.google.com/blog/products/ai-machine-learning/combine-text-image-power-with-vertex-ai — Google Vertex AI Multimodal Embedding API: Vertex AI multimodal embedding API generates image embeddings and lets users query using text or images against a shared vector search index. [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12271983 https://zilliz.com/blog/combine-image-and-text-how-multimodal-retrieval-transforms-search https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/ https://github.com/api-evangelist/marqo https://cloud.google.com/blog/products/ai-machine-learning/combine-text-image-power-with-vertex-ai
confirmado: parcial

---

## 30 · c4350d18 · Everyone Detects Anomalies, Nobody Shares the Machinery

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood contains anomaly detectors for pixels, tables, EEG signals, malware binaries, and generated images — each rebuilding notions of normality, thresholds, and drift from scratch. CORE already proves unification pays off within tabular data alone. The missing piece is a modality-agnostic anomaly-detection layer or benchmark suite: shared calibration, threshold-setting, and drift-handling infrastructure that any domain detector plugs into. Its absence is conspicuous given five indepe
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): PyOD and PyThresh together supply much of the described shared-machinery vision (unified APIs, cross-modality detectors, modality-agnostic thresholding), but no single product fully unifies calibration, threshold-setting, and drift-handling across pixels, EEG, malware, and generated-image anomaly de
- Evidencia (prior art citado por Constellate):
  - https://github.com/yzhao062/pyod — PyOD (Python Outlier Detection) / PyOD 3: An open-source Python library providing 60+ anomaly/outlier detection algorithms under a unified API, spanning tabular, time series, graph, text, image, and aud [✓ github:yzhao062/pyod (repo)]
  - https://pythresh.readthedocs.io/en/stable/ — PyThresh: A companion toolkit to PyOD offering 30+ modality-agnostic algorithms for thresholding outlier likelihood scores into inlier/outlier binary labels, without requ [✗ sin repo ni Show HN en el corpus]
  - https://pyod.readthedocs.io/ — ADBench: A NeurIPS benchmark evaluating 30 anomaly detection algorithms across 57 tabular datasets, referenced within the PyOD ecosystem. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2510.03363 — UCF (Unified Cost-volume Filtering for Anomaly Detection): A generic post-hoc plug-in framework that reformulates unsupervised anomaly detection as feature extraction, cost volume construction, and cost volume filtering [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2604.19191 — Modality-Agnostic Medical Image Anomaly Detection (manifold refinement framework): A training-free framework inserting a manifold-refinement stage between feature extraction and anomaly scoring, evaluated across five imaging modalities (X-ray, [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): PyOD 3 (tabular, series, grafos, texto, imagen, audio) https://github.com/yzhao062/pyod ; RADAR ; anomalib [fuerte]

propuesta: parcial
esperado: https://github.com/yzhao062/pyod https://pythresh.readthedocs.io/en/stable/ https://pyod.readthedocs.io/ https://arxiv.org/html/2510.03363 https://arxiv.org/abs/2604.19191
confirmado: parcial

---

## 31 · b36b5f05 · Everyone Generates Synthetic Data, Nobody Certifies It

- Verificada por: web · corridas: 2026-07-31
- Idea: Procedural scratch rendering, self-play driving simulation, generative multi-date stereo data, and point cloud scene generation all manufacture training data because real annotations are scarce. Yet the neighborhood contains no method for validating that synthetic distributions actually transfer — each pipeline assumes its own realism. The missing piece is a sim-to-real fidelity auditor: a tool that scores a synthetic dataset's predictive value for a target deployment domain before you spend GPU
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several research frameworks (TrustFormers, the GCV transferability framework, SIQAC, SynthEval) and a driving-specific validation service each implement pieces of sim-to-real fidelity scoring, but none is a general, standalone auditor product that pre-scores arbitrary synthetic datasets against a ta
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/abs/2304.10819 — Auditing and Generating Synthetic Data with Controllable Trust Trade-offs (TrustFormers): Introduces a holistic auditing framework and 'trustworthiness index' that scores synthetic datasets on fidelity, utility, privacy, fairness, and robustness befo [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2509.11273 — Synthetic Dataset Evaluation Based on Generalized Cross Validation (GCV framework): A framework that trains task-specific models (e.g., YOLOv5s) on synthetic and real benchmarks to build a cross-performance matrix quantifying domain transferabi [✗ sin repo ni Show HN en el corpus]
  - https://www.techrxiv.org/doi/full/10.36227/techrxiv.173933581.11924651/v4 — Synthetic Image Quality Analysis Calculator (SIQAC): An open-source tool that computes image quality assessment metrics (SSIM, CW-SSIM) between paired synthetic and real images to predict sim2real detection transf [✗ sin repo ni Show HN en el corpus]
  - https://github.com/schneiderkamplab/syntheval — SynthEval: An open-source library that evaluates fidelity, utility, and privacy of tabular synthetic data compared to real data using a suite of preconfigured metrics. [✗ repo fuera del bulk]
  - https://keymakr.com/blog/validating-simulated-sensor-data-against-real-world-annotations-for-autonomous-driving/ — Keymakr Simulation Validation Dataset service: A validation methodology/service comparing simulated sensor outputs against real-world annotated data using IoU, mAP, RMSE and domain-gap scoring for autonomous [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): SDMetrics Quality Report https://github.com/sdv-dev/SDMetrics ; evaluación holdout (paper) [parcial-fuerte (tabular; no imágenes/nubes de puntos)]

propuesta: parcial
esperado: https://arxiv.org/abs/2304.10819 https://arxiv.org/html/2509.11273 https://www.techrxiv.org/doi/full/10.36227/techrxiv.173933581.11924651/v4 https://github.com/schneiderkamplab/syntheval https://keymakr.com/blog/validating-simulated-sensor-data-against-real-world-annotations-for-autonomous-driving/
confirmado: parcial

---

## 32 · 512fe792 · Everyone Measures Untrustworthiness; Nobody Ships a Trust Monitor

- Verificada por: web · corridas: 2026-07-31
- Idea: 4261 surveys uncertainty quantification, 4989 shows pooled data can silently reverse decisions, 4940 shows GNN explanations are non-canonical under symmetry, and 5068 handles evolving sensor graphs at test time. Each diagnoses a distinct failure mode of deployed models under real-world change, yet the neighborhood lacks the obvious integrating piece: a deployment-time reliability monitor that continuously flags when retraining, data pooling, or graph evolution has invalidated a model's prior dec
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several mature MLOps observability platforms (Fiddler, Arize, WhyLabs, Evidently, NannyML) already monitor drift, performance degradation, and explainability for deployed models, but none of the found products explicitly implement a 'regression test suite for model trust' that checks decision-orderi
- Evidencia (prior art citado por Constellate):
  - https://www.fiddler.ai/ml-model-monitoring — Fiddler AI: Enterprise ML observability platform that monitors data drift, model degradation, bias/fairness, and provides explainability (feature importance, counterfactual [✗ sin repo ni Show HN en el corpus]
  - https://alexsandu.substack.com/p/ml-model-monitoring-and-observability — Arize AI: Observability platform that monitors embedding/input/output drift and lets teams A/B compare model versions, environments, and time periods. [✗ sin repo ni Show HN en el corpus]
  - https://aisecurityandsafety.org/en/compare/fiddler-ai-tool-vs-whylabs/ — WhyLabs: AI observability platform using statistical data profiles to detect drift and quality issues in ML models and LLM applications in real time. [✗ sin repo ni Show HN en el corpus]
  - https://www.evidentlyai.com/ml-in-production/model-monitoring — Evidently AI: Open-source and hosted tool for monitoring ML model quality, data drift, and bias metrics such as predictive parity across production data. [✗ sin repo ni Show HN en el corpus]
  - https://medium.com/@tanish.kandivlikar1412/comprehensive-comparison-of-ml-model-monitoring-tools-evidently-ai-alibi-detect-nannyml-a016d7dd8219 — NannyML: Monitoring tool specialized in estimating model performance and detecting drift timing without requiring ground-truth labels, mainly for tabular data. [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://www.fiddler.ai/ml-model-monitoring https://alexsandu.substack.com/p/ml-model-monitoring-and-observability https://aisecurityandsafety.org/en/compare/fiddler-ai-tool-vs-whylabs/ https://www.evidentlyai.com/ml-in-production/model-monitoring https://medium.com/@tanish.kandivlikar1412/comprehensive-comparison-of-ml-model-monitoring-tools-evidently-ai-alibi-detect-nannyml-a016d7dd8219
confirmado: parcial

---

## 33 · 5b6356d3 · Everyone Steers Policies, Nobody Audits What Steering Broke

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood is full of interventions on trained policies: activation steering, value-guided steering, counterfactual probing, and manifold analysis. What's missing is the diagnostic layer: a tool that measures what a steering or fine-tuning intervention destroyed — lost solution modes, safety regressions, coverage collapse — before deployment. Given the triangulated evidence that post-training silently narrows behavior, a 'behavioral diff' tool comparing pre- and post-intervention policies
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple existing tools and methodologies (behavior-diff CLIs, model-diffing audits, MNEME's side-effect prediction, alignment-tax measurement checklists, and regression-testing platforms) each cover a slice of pre/post-intervention comparison, but none unify solution-mode loss, safety regression, a
- Evidencia (prior art citado por Constellate):
  - https://dev.to/nilofer_tweets/llm-behavior-diff-model-update-detector-3e7b — LLM Behavior Diff (Model Update Detector): An open-source CLI/API/MCP tool that runs the same prompt suite through two model versions, semantically scores divergence, classifies severity, and produces an [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2507.21084 — MNEME (Reviving Your MNEME): A sparse model-diffing method that predicts side effects of LLM unlearning and fine-tuning by identifying latent features amplified or degraded post-training, b [✗ sin repo ni Show HN en el corpus]
  - https://openreview.net/pdf/d4bc63faf941967e432dc29c89607f4d35aa8e4e.pdf — Auditing LLMs for Hidden Behaviors using Model Diffing: Introduces SVD rank truncation and adversarial decoding methods to compare a fine-tuned model's next-token distribution against a reference/base model to surfac [✗ sin repo ni Show HN en el corpus]
  - https://redteams.ai/topics/training-pipeline/fine-tuning/alignment-tax — Alignment Tax measurement methodology (redteams.ai): A practical methodology to measure the base model across a capability suite, evaluate the aligned model on the same suite, and flag domains where capability los [✗ sin repo ni Show HN en el corpus]
  - https://futureagi.com/glossary/llm-regression-testing/ — FutureAGI LLM Regression Testing platform: A regression-testing practice/product wiring golden-dataset evaluators (groundedness, tool selection, hallucination, schema validity) into CI pipelines to catch [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://dev.to/nilofer_tweets/llm-behavior-diff-model-update-detector-3e7b https://arxiv.org/pdf/2507.21084 https://openreview.net/pdf/d4bc63faf941967e432dc29c89607f4d35aa8e4e.pdf https://redteams.ai/topics/training-pipeline/fine-tuning/alignment-tax https://futureagi.com/glossary/llm-regression-testing/
confirmado: parcial

---

## 34 · 39d157d7 · Formal Methods for Agents: Everyone Circles, Nobody Ships

- Verificada por: web · corridas: 2026-07-31
- Idea: 3871 asks why formal methods aren't used; 4277, 4554, and 4609 each document AI systems failing in ways that only formal, layer-aware specifications could catch (invented procedure steps, incomplete deletion, cross-layer grounding faults). The neighborhood defines the gap precisely: a practical specification-and-verification toolkit for agentic LLM systems — contracts on tool calls, memory operations, and execution traces — that sits between benchmarks and full formal proof. Everyone measures fa
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several recent research prototypes (ABC, ToolGate, Lean4Agent, Agentic Model Checking, VeriAct) each formalize contracts or verification for parts of the agent stack—mostly tool calls or workflow structure—but none unify tool-call, memory-operation, and execution-trace contracts into one practical, 
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/html/2602.22302v1 — Agent Behavioral Contracts (ABC): Applies Design-by-Contract formalization (preconditions, postconditions, invariants) to autonomous LLM agents, with runtime enforcement across multi-turn sessio [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2601.04688 — ToolGate: A forward execution framework that formalizes each tool as a Hoare-style contract with pre/postconditions, maintaining a symbolic state space so tool results ar [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2606.06523 — Lean4Agent (FormalAgentLib): A three-layer Lean4 library for formally modeling and verifying agent workflows and trajectories, checking structural correctness of workflow graphs among other [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2605.21434 — Agentic Model Checking: Couples LLM agents with a bounded model checking backend where agents infer per-function pre/postconditions and a BMC solver discharges all soundness-relevant v [✗ sin repo ni Show HN en el corpus]
  - https://dev.to/aws/ai-agent-guardrails-rules-that-llms-cannot-bypass-596d — ATA: Autonomous Trustworthy Agents / neurosymbolic hook pattern: Describes using framework-level hooks (e.g., BeforeToolCallEvent) to enforce deterministic symbolic business rules on tool calls before execution, blocking inva [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/html/2602.22302v1 https://arxiv.org/abs/2601.04688 https://arxiv.org/pdf/2606.06523 https://arxiv.org/html/2605.21434 https://dev.to/aws/ai-agent-guardrails-rules-that-llms-cannot-bypass-596d
confirmado: parcial

---

## 35 · b7aa36fd · IoT Security Policies Are Verified; Fleets Aren't Orchestrated

- Verificada por: web · corridas: 2026-07-31
- Idea: ESPHome gives per-device configuration, 4318 formally verifies cross-device access-control information flow, and 4176 shows coupled end-to-end policy optimization for distributed networks. The missing piece is obvious once these are aligned: a tool that treats a home or building's IoT fleet as one coupled system — jointly optimizing and verifying device configs, trust boundaries, and automation policies end-to-end rather than device-by-device. Everything needed exists (declarative configs, flow 
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Enterprise IoT security orchestration platforms and academic smart-home verification tools each cover pieces of the gap (fleet-wide policy orchestration, trigger-action verification, provisioning automation), but no single tool jointly compiles declarative device configs, cross-device information-fl
- Evidencia (prior art citado por Constellate):
  - https://www.forescout.com/solutions/iot-security/ — Forescout Continuum / Vistaro Platform: Provides zero-trust policy orchestration, network segmentation, and automated risk-based access control across multi-vendor IoT/OT device fleets in enterprise s [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2102.01468 — TAPInspector: Performs safety and liveness verification of concurrent trigger-action IoT automation rules using formal model checking. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2203.01464 — Expat (Expectation-based Policy Analysis and Enforcement): Provides expectation-based policy analysis and enforcement for applified smart-home platforms to detect policy violations from apps. [✗ sin repo ni Show HN en el corpus]
  - https://aws.amazon.com/blogs/iot/how-to-automate-onboarding-of-iot-devices-to-aws-iot-core-at-scale-with-fleet-provisioning/ — AWS IoT Core Fleet Provisioning: Automates secure end-to-end device onboarding, identity provisioning, and permission assignment at fleet scale in AWS IoT Core. [✓ github:aws/aws-iot-device-sdk-java (heurístico, revisar: repo con homepage aws.amazon.com)]
- Búsqueda propia (sep-2026, complementaria): Fleet for ESPHome (flota de dispositivos, pinning, upgrades) https://github.com/weirded/distributed-esphome ; OpenRemote ; FleetDM [parcial (orquestación sí; políticas de seguridad verificadas no)]

propuesta: parcial
esperado: https://aws.amazon.com/blogs/iot/how-to-automate-onboarding-of-iot-devices-to-aws-iot-core-at-scale-with-fleet-provisioning/ https://www.forescout.com/solutions/iot-security/ https://arxiv.org/pdf/2102.01468 https://arxiv.org/pdf/2203.01464 !github:aws/aws-iot-device-sdk-java
confirmado: parcial

---

## 36 · 5018a38d · Medical AI Has Diagnosis, Missing the Trust Layer

- Verificada por: web · corridas: 2026-07-16
- Idea: Two of the three medical imaging papers (pancreatic resectability, PNI prediction) push architectural novelty for high-stakes clinical calls, while only the thyroid paper addresses calibration, selective referral, and dataset shift. The gap is a reusable, model-agnostic clinical trust layer: calibrated uncertainty, shift detection, and abstain-and-refer workflows that wrap any diagnostic model. Its absence is glaring given that all three tasks explicitly cite expert variability and high-stakes d
- Veredictos:
  - **partially** (web, output.json): Clinical uncertainty layers now exist as research frameworks (MedBayes-Lite, TRUECAM) covering calibration and abstain-and-refer, but neither ships as the reusable model-agnostic wrapper any diagnostic model could adopt.
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2511.16625 — MedBayes-Lite: Clinical uncertainty governance layer adding risk-aware confidence to medical decision support. [✗ sin repo ni Show HN en el corpus]
  - https://www.medrxiv.org/content/10.1101/2024.12.27.24319715v1.full — TRUECAM: Conformalized uncertainty-aware framework deferring uncertain or out-of-distribution cases to expert pathologists. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2603.21656v1 — TrustFed: Trustworthy medical AI framework operating under data privacy constraints. [✗ sin repo ni Show HN en el corpus]
  - https://www.sciencedirect.com/science/article/pii/S0933365724000721 — Uncertainty quantification in medical imaging — review: Unified review of uncertainty quantification methods for deep learning in medical image analysis. [✗ sin repo ni Show HN en el corpus]
  - https://www.sciencedirect.com/science/article/pii/S0169260726003093 — UQ in generative medical AI — systematic review: Systematic review of uncertainty quantification for generative AI in medical imaging. [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/pdf/2511.16625 https://www.medrxiv.org/content/10.1101/2024.12.27.24319715v1.full https://arxiv.org/html/2603.21656v1 https://www.sciencedirect.com/science/article/pii/S0933365724000721 https://www.sciencedirect.com/science/article/pii/S0169260726003093
confirmado: parcial

---

## 37 · 80942ef6 · Missing: A CI/CD Certification Suite for Agent Skills

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains skill-use verification, skill compilation, blind-spot discovery, readiness philosophy, and a production benchmark — but no tooling that ties them into a developer workflow. What's absent is a 'pytest for agent skills': a CI harness that runs counterfactual ablations, checks that skills causally alter decisions, enforces typed control flow, and gates deployment on readiness metrics. Every ingredient exists as research; nobody has shipped the practitioner tool. This is th
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several practitioner tools already provide pytest-style CI/CD testing and deployment gating for LLM agents and even skills, but none combine counterfactual skill ablation, typed control-flow enforcement, and readiness-metric gating into one unified 'pytest for agent skills' suite as described.
- Evidencia (prior art citado por Constellate):
  - https://github.com/sbroenne/pytest-skill-engineering — pytest-skill-engineering: A pytest-based testing framework that tests MCP tools, prompt templates, and Agent Skills with real LLMs, using LLM-as-judge assertions and catching skill stack [✗ repo fuera del bulk]
  - https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd — DeepEval: An Apache-2.0 pytest-style framework with 50+ metrics for scoring agents, RAG pipelines and chatbots, integrated into CI via assert_test() and deepeval test run [✓ github:confident-ai/deepeval (heurístico, revisar: repo con homepage deepeval.com)]
  - https://www.harness.io/products/ai-evals — Harness AI Evals: A CI/CD-native quality gate product that scores agents against golden datasets and blocks releases when scores drop below threshold, evaluating step, tool-call, [✗ sin repo ni Show HN en el corpus]
  - https://github.com/najeed/ai-agent-eval-harness — ai-agent-eval-harness (MultiAgentOps): An open-source evaluation/verification harness with CI/CD hard gating, cryptographic run certification, standardized YAML evaluation specs, and one-click GitHub [✗ repo fuera del bulk]
  - https://github.com/Nihal-Srivastava05/agent-test — agent-test: A pytest-like testing framework for AI agents and prompts. [✗ repo fuera del bulk]
- Búsqueda propia (sep-2026, complementaria): SkillCheck (valida Agent Skills contra el estándar, en CI) https://www.getskillcheck.com/ ; plugin validate del marketplace [fuerte]

propuesta: parcial
esperado: https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd https://github.com/sbroenne/pytest-skill-engineering https://www.harness.io/products/ai-evals https://github.com/najeed/ai-agent-eval-harness https://github.com/Nihal-Srivastava05/agent-test
confirmado: parcial

---

## 38 · 246e1998 · Missing: A Portable, Auditable Personal Memory-Permission Layer

- Verificada por: web · corridas: 2026-07-31
- Idea: Personalization work builds ever-richer persistent user state and cross-session memory, while safety work shows authorization must be context-dependent and risks accumulate over trajectories. The obvious missing piece is the intersection: a user-owned memory store with attached, evidence-backed permissions — deciding which agent may read, write, or act on which memories, with audit trails. Everyone here assumes memory exists or permissions exist, but nobody builds the substrate binding them. Thi
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple products (Verida, Zep's memory MCP server, AgentVault, Peta, Box) each combine pieces of user-scoped memory, permissioning, and audit logging, but none unify a portable, user-owned memory store with granular, evidence-backed, per-agent read/write/act permissions and trajectory-aware risk ac
- Evidencia (prior art citado por Constellate):
  - https://www.verida.ai/ — Verida (Personal Data Bridge / Verida Vault): A decentralized, user-owned personal data vault that lets individuals pull in data from platforms like Gmail, Meta, LinkedIn, and Strava, encrypts it under the  [✗ sin repo ni Show HN en el corpus]
  - https://blog.getzep.com/unified-agent-memory-in-any-mcp-client/ — Zep Memory MCP Server: A governed, cross-client user memory graph accessible via MCP where each authenticated user reads/writes only their own graph, write access is admin-gated, and  [✓ show_hn:41660503 (heurístico, revisar: Show HN del dominio getzep.com: "Zep – Open-Source Graph Memory for AI Apps")]
  - https://agentvault.inflectiv.ai/ — AgentVault: An encrypted vault combining agent credentials and memory storage, with permission profiles, audit logs of every credential/memory access attempt (timestamps, a [✗ sin repo ni Show HN en el corpus]
  - https://peta.io/ — Peta (Peta Core / Console / Desk): An MCP vault and zero-trust gateway that stores credentials and memory modules, enforces per-agent/per-tool RBAC/ABAC permissions, injects credentials just-in-t [✗ sin repo ni Show HN en el corpus]
  - https://blog.box.com/why-persistent-agentic-memory-requires-cognitive-vault — Box Cognitive Vault (persistent agentic memory in Box): Hosts agent memory inside Box's governed content platform, giving namespace isolation, granular permissions and downscoped tokens per agent folder, and an immut [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Memory OS (memoria personal portable con permisos por app, revocables) https://mymemoryos.com/ ; Walrus Memory ; proyecto Stanford Portable Memory [fuerte]

propuesta: parcial
esperado: https://blog.getzep.com/unified-agent-memory-in-any-mcp-client/ https://www.verida.ai/ https://agentvault.inflectiv.ai/ https://peta.io/ https://blog.box.com/why-persistent-agentic-memory-requires-cognitive-vault
confirmado: parcial

---

## 39 · 50a4f12d · Missing: A Runtime Abstention Layer for Embodied Agents

- Verificada por: web · corridas: 2026-07-31
- Idea: 4405 identifies that VLA policies lack failure recovery, 5006 defines graded trustworthiness levels for embodied systems, 4637 provides principled human-in-the-loop abstention for tabular decisions, and 4626 estimates partner capability on the fly. The obvious missing piece is the synthesis: a deployable middleware that gives any robot policy calibrated, cost-sensitive abstention with graceful handoff to humans — conformal prediction ported from spreadsheets to actuators. Everyone circles it; no
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple recent research frameworks (SAFECAST, FIPER, Conformal Decision Theory, ReconVLA, and sparse-feedback conformal safety work) already implement conformal-calibrated failure/abstention signals and backup-mode switching for individual robot policies, but none packages this as a general-purpose
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/html/2608.04246 — SAFE / SAFECAST (Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies): A probe trained on VLA rollouts predicts failure at every timestep, with the detection threshold calibrated using functional conformal prediction to give statis [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2510.09459 — FIPER (Failure Prediction at Runtime for Generative Robot Policies): A framework that predicts failure at runtime for generative imitation-learning policies using OOD detection and action-chunk entropy, calibrated via conformal p [✗ sin repo ni Show HN en el corpus]
  - https://conformal-decision.github.io/ — Conformal Decision Theory: A theoretical framework extending conformal prediction to calibrate autonomous decisions directly, including the choice of trusting a nominal policy versus swit [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2501.04823 — Learning Robot Safety from Sparse Human Feedback using Conformal Prediction: Learns a conformal 'suspicious' (SUS) region from sparse human feedback and uses it as a runtime warning system or to switch the policy to a backup safety mode, [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2604.16677 — ReconVLA: Augments a pretrained VLA policy with a CQR-based calibrated action-uncertainty estimator and a Mahalanobis-distance-based state monitor to proactively trigger  [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/html/2608.04246 https://arxiv.org/abs/2510.09459 https://conformal-decision.github.io/ https://arxiv.org/html/2501.04823 https://arxiv.org/html/2604.16677
confirmado: parcial

---

## 40 · caa34ef5 · Missing: A Supervision Layer for Autonomous Agents

- Verificada por: web · corridas: 2026-07-16
- Idea: Agents are hacking TVs, gambling money unsupervised, and self-improving, while the only oversight tool present (Stage, 242) covers just code review. The neighborhood's structure demands a general-purpose agent supervision product: budget caps, action audit trails, kill switches, and human-approval gates for arbitrary agent actions — not just diffs. Its absence is glaring given how much of the set documents agents misbehaving without guardrails.
- Veredictos:
  - **partially** (web, output.json): Individual pieces of the described supervision layer already exist — HumanLayer for approval gates and audit trails, RuntimeAI and Kosmoy for kill switches/sandboxing, and CalypsoAI/Lakera for governance and auditing of LLM/agent activity — but no single product unifies budget caps, universal action
- Evidencia (prior art citado por Constellate):
  - https://humanlayer.dev — HumanLayer: An API/SDK that lets tool-calling AI agents pause and request human approval, feedback, or advice before executing actions, with routing to Slack/email/SMS and  [✓ github:humanlayer/humanlayer (heurístico, revisar: repo con homepage humanlayer.dev)]
  - https://runtimeai.io/blog/2026-05-12-kill-switch.html — RuntimeAI: Provides a process-level 'kill switch' for autonomous agents with sub-100ms forced termination, a cryptographic agent identity registry (KYA), and signed activa [✗ sin repo ni Show HN en el corpus]
  - https://www.kosmoy.com/resources/blog/best-ai-agent-governance-platforms-2026/ — Kosmoy (Action Capsule): Offers kernel-enforced sandboxing for agents and MCP servers with per-task credentials and a kill switch as part of an enterprise agent governance platform. [✗ sin repo ni Show HN en el corpus]
  - https://www.eesel.ai/blog/lakera-alternatives — CalypsoAI (Moderator): An enterprise AI governance platform giving full auditability and control over LLM usage, including data-loss prevention and detailed audit trails of all LLM in [✗ sin repo ni Show HN en el corpus]
  - https://www.reco.ai/compare/ai-security-tools-for-enterprises — Lakera Guard: A runtime security and governance platform that intercepts prompts and model outputs to block prompt injection, data leakage, and unsafe content in real time. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): hoop.dev (gateway L7 con aprobación humana, MIT) https://hoop.dev/blog/human-in-the-loop-approval-best-practices-for-autonomous-agents ; LangGraph interrupts ; GreyCollar [fuerte]

propuesta: parcial
esperado: https://humanlayer.dev https://runtimeai.io/blog/2026-05-12-kill-switch.html https://www.kosmoy.com/resources/blog/best-ai-agent-governance-platforms-2026/ https://www.eesel.ai/blog/lakera-alternatives https://www.reco.ai/compare/ai-security-tools-for-enterprises
confirmado: parcial

---

## 41 · a13c1dd2 · Missing: A Trust Layer for Peer-to-Peer Inference

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood has local models beating cloud giants, idle Macs pooled for private inference, websites being audited for agent-readiness, and mesh-style signals surviving blackouts. What's structurally absent is the connective piece: a verification/reputation layer that lets strangers safely rent, route, and audit inference across untrusted consumer hardware. Without attestation of what model ran and whether data leaked, the distributed-AI economy these ideas gesture at can't clear transaction
- Veredictos:
  - **partially** (web, output.json): Multiple live networks (0G Compute, Ritual, OpenGradient, Phala, Bittensor) already implement pieces of attestation, reputation, and routing for decentralized inference, but they target blockchain/GPU-marketplace ecosystems rather than a unified, consumer-hardware-focused trust broker that ties toge
- Evidencia (prior art citado por Constellate):
  - https://compute.0g.ai/ — 0G Compute: A permissionless marketplace where independent GPU operators run inference for buyers, with jobs cryptographically routed, priced, and settled on-chain; it offe [✗ sin repo ni Show HN en el corpus]
  - https://equilibrium.co/writing/state-of-verifiable-inference — Ritual: <cite index="7-1,7-2">An incentive and coordination layer for decentralized inference, taking a modular approach to verifiable inference and computational integ [✗ sin repo ni Show HN en el corpus]
  - https://www.prnewswire.com/news-releases/opengradient-announces-9-5-million-in-total-funding-to-build-the-compute-layer-for-verifiable-ai-302741614.html — OpenGradient: <cite index="3-1">A dedicated compute layer that executes AI workloads and attaches cryptographic proofs to every inference, enabling downstream applications to [✗ sin repo ni Show HN en el corpus]
  - https://phala.com/ — Phala Network (Confidential AI Cloud): <cite index="17-3">Launches H100, H200, and B300 GPU capacity with TEE-backed runtime proof and public attestations</cite>, letting users run and verify confide [✗ sin repo ni Show HN en el corpus]
  - https://www.bittensor.com/whitepaper — Bittensor: <cite index="21-1">Connects developers who provide AI models ("miners") with validators who score their work, forming competitive markets for intelligence</cite [✓ github:RaoFoundation/bittensor (heurístico, revisar: repo con homepage bittensor.com)]
- Búsqueda propia (sep-2026, complementaria): TOPLOC (inferencia verificable) https://github.com/PrimeIntellect-ai/toploc ; LOGIC (inference.net) https://inference.net/blog/logic/ ; Theta EdgeCloud [parcial-fuerte]

propuesta: parcial
esperado: https://www.bittensor.com/whitepaper https://compute.0g.ai/ https://equilibrium.co/writing/state-of-verifiable-inference https://www.prnewswire.com/news-releases/opengradient-announces-9-5-million-in-total-funding-to-build-the-compute-layer-for-verifiable-ai-302741614.html https://phala.com/
confirmado: parcial

---

## 42 · e545e760 · Missing: A Verifier That Tells Models When to Reflect

- Verificada por: web · corridas: 2026-07-31
- Idea: The reflection-fails papers show self-critique wastes tokens in small models, while the RSI papers assume self-improvement loops work. The gap is a lightweight external verifier or router that decides per-task whether to resample blindly or invest in feedback-driven repair—the piece that would reconcile both findings. Nobody in this neighborhood is building the meta-controller for when introspection is worth the tokens.
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several research prototypes (AutoMix's meta-verifier, the Resample-or-Reroute policy, VRR-Stop, Self-REF confidence routing, and IoRT's dynamic instructor) each implement pieces of a verifier/router that governs resampling vs. reflection-like repair, but none is packaged as a general lightweight ext
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2310.12963 — AutoMix: Uses few-shot self-verification plus a learned router (interpretable as a meta-verifier) that decides whether an LLM's output should be accepted or escalated to [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2607.08665 — Resample or Reroute? Budget-Aware Test-Time Policy: Proposes an online allocation policy that decides, under a budget, whether to resample from a committed LLM or reroute to another model, based on estimated marg [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2607.17641 — Verify, Repair, Repeat, or Stop? (VRR-Stop): Formalizes when to stop iterative verify-repair loops in noisy agent systems, separating verifier false accept/reject from repair/damage behavior and stopping b [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2410.13284 — Self-REF (Learning to Route LLMs with Confidence Tokens): Trains the LLM itself to output calibrated confidence tokens during decoding, which are then used as a routing signal to decide whether to escalate/cascade to a [✗ sin repo ni Show HN en el corpus]
  - https://www.emergentmind.com/topics/rethinking-or-self-reflection — Iterative Reflection with Dynamic Instructions (IoRT): An instructor component uses meta-thoughts and a self-consistency classifier to issue dynamic 'refresh', 'stop', or 'select' instructions that govern whether an [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/pdf/2310.12963 https://arxiv.org/pdf/2607.08665 https://arxiv.org/html/2607.17641 https://arxiv.org/pdf/2410.13284 https://www.emergentmind.com/topics/rethinking-or-self-reflection
confirmado: parcial

---

## 43 · 32a82f3a · Missing: An Exit Kit for AI Vendor Lock-In

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood contains frontier-model dependence, arbitrary account bans, growing resistance, and a post-collapse open-source thesis — but no idea about the practical bridge: tooling that lets builders port prompts, workflows, and fine-tuning investments off a proprietary provider before or after a ban. Given the structure here, an 'AI portability layer' or ban-insurance product is the obvious missing node. Everyone is describing the trap or the aftermath; nobody is building the fire escape.
- Veredictos:
  - **partially** (web, output.json): Gateways and routers (LiteLLM, OpenRouter, Kong, Orq) already make the model call itself portable, but nothing ports prompts, evaluation corpora or fine-tuning investment off a provider, and no ban-insurance product exists.
- Evidencia (prior art citado por Constellate):
  - https://github.com/BerriAI/litellm — LiteLLM: Open-source gateway exposing 100+ providers behind one OpenAI-compatible interface with fallback routing. [✓ github:BerriAI/litellm (repo)]
  - https://openrouter.ai/ — OpenRouter: Hosted router giving one API across hundreds of models with automatic failover. [✓ github:OpenRouterArchived/openrouter-runner (heurístico, revisar: repo con homepage openrouter.ai)]
  - https://konghq.com/blog/learning-center/vendor-lock-in — Kong AI Gateway: API gateway with AI-specific routing, letting model choice become configuration rather than code. [✓ github:Kong/kong (heurístico, revisar: repo con homepage konghq.com)]
  - https://gateway.orq.ai/blog/llm-vendor-lock-in — Orq.ai LLM Gateway: Gateway combining routing with prompt versioning and an evaluation corpus kept outside the vendor. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Bifrost (gateway, cambio de proveedor con base URL) ; LiteLLM ; OpenRouter ; Tokonomics [parcial (portabilidad de API sí; "exit kit" de prompts/evals/memoria no del todo)]

propuesta: parcial
esperado: https://github.com/BerriAI/litellm https://openrouter.ai/ https://konghq.com/blog/learning-center/vendor-lock-in https://gateway.orq.ai/blog/llm-vendor-lock-in !github:OpenRouterArchived/openrouter-runner
confirmado: parcial

---

## 44 · 2a3fcc9d · Missing: An Independent Audit Service for AI-Generated Research

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood contains rubric generation for evaluating agent research, realistic deep-research evaluation, sabotage detection benchmarks, and leakage detection — all the ingredients of research verification, yet all framed as academic benchmarks. What's missing is the productized layer: a service or tool that takes an AI-generated report, paper, or codebase and runs automated integrity checks (leakage, rubric compliance, provenance, sabotage signals) and issues a trust score. As agent-produc
- Veredictos:
  - **partially** (web, output.json): Commercial AI-text/plagiarism detectors (Pangram, Turnitin, Copyleaks, Originality.AI) and a generic AI-trustworthiness-scoring patent (MTI) cover isolated pieces of the described gap, while the exact combination the gap describes — leakage + rubric compliance + provenance + sabotage detection bundl
- Evidencia (prior art citado por Constellate):
  - https://www.biorxiv.org/content/10.64898/2026.01.01.697311.full.pdf — Pangram (AI-text detection used in biomedical/academic publishing): A commercial AI-text detector deployed by publishers and conferences (e.g. flagging LLM text in peer-review reports and manuscripts) with reported ~99% accuracy [✗ sin repo ni Show HN en el corpus]
  - https://www.researchprospect.com/ai-detector-tools/ — Turnitin AI Writing Detection: Turnitin integrates AI writing detection alongside its plagiarism/similarity checking, evaluating linguistic features to flag AI-generated text in submitted wor [✗ sin repo ni Show HN en el corpus]
  - https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11748667 — MTI (Measurement of Relative Trustworthiness) Platform — US Patent 11,748,667: A patented platform/methodology where developers submit AI code/modules for an 'MTI audit' that generates a trustworthiness score and annotates the software mod [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): AI Research Evidence Verification (Apify actor) https://apify.com/suezcanal.xyz/research-verification ; citation auditing (paper) ; TAB-AUDIT (paper) [parcial (piezas, no un servicio independiente integral)]

propuesta: parcial
esperado: https://www.biorxiv.org/content/10.64898/2026.01.01.697311.full.pdf https://www.researchprospect.com/ai-detector-tools/ https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11748667
confirmado: parcial

---

## 45 · fa53f5d2 · Missing: CI for Agent Behavior, Not Model Outputs

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood has execution-failure evidence, a benchmark, training environments, and testing techniques battling flakiness — but no continuous, developer-facing tool that runs agents through realistic stateful scenarios on every model or prompt change and flags execution-layer regressions. Everyone diagnoses the gap between static metrics and agentic behavior; nobody in this set ships the 'pytest for agents' that closes it. Given the pieces already exist (env generation, semantic UI hooks, f
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several CI/CD-oriented agent testing tools (DeepEval, Confident AI, AgentV/LangWatch stack, Docker Cagent, AgentAssay) already target 'pytest for agents' style regression detection on prompt/model changes, but none combine generated stateful environments, accessibility-tree/semantic UI hooks, and a 
- Evidencia (prior art citado por Constellate):
  - https://mlflow.org/top-5-agent-evaluation-frameworks/ — DeepEval: An open-source evaluation library with a pytest-native interface—assert_test() calls, test discovery, fixtures—that covers agents, tool selection, planning qual [✗ sin repo ni Show HN en el corpus]
  - https://www.confident-ai.com/knowledge-base/compare/best-ci-cd-tools-testing-ai-agents-before-production-2026 — Confident AI: A CI/CD platform offering durable reports, release gates, span-level tool-call regression checks, full-run evals, and multi-turn simulation of realistic agent c [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2603.02601 — AgentAssay: An academic framework for token-efficient regression testing of non-deterministic agent workflows, using stochastic three-valued verdicts, coverage metrics, mut [✗ sin repo ni Show HN en el corpus]
  - https://www.infoq.com/Regression_Testing/news — Docker Cagent: A runtime from Docker positioned to bring deterministic testing back to AI agents for production agentic systems. [✗ sin repo ni Show HN en el corpus]
  - https://dev.to/thedailyagent/5-open-source-tools-for-testing-ai-agents-before-they-break-production-5d9c — AgentV / LangWatch / EvalView toolchain: A stitched pipeline where LangWatch simulations catch edge cases pre-ship, AgentV gates PR merges as 'pytest for agents,' agentevals scores staging traffic, and [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Agent CI https://agent-ci.com/ ; Galileo eval gates en CI https://galileo.ai/blog/continuous-integration-ci-ai-fundamentals [fuerte]

propuesta: parcial
esperado: https://mlflow.org/top-5-agent-evaluation-frameworks/ https://www.confident-ai.com/knowledge-base/compare/best-ci-cd-tools-testing-ai-agents-before-production-2026 https://arxiv.org/pdf/2603.02601 https://www.infoq.com/Regression_Testing/news https://dev.to/thedailyagent/5-open-source-tools-for-testing-ai-agents-before-they-break-production-5d9c
confirmado: parcial

---

## 46 · a3fb5892 · Missing: Continuous Formal-ish Assurance for Dependencies

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood has supply-chain risk detection, the lament that formal verification is unused, and heavyweight post-hoc analysis — but nothing bridging them. Absent is a lightweight tool that automatically checks behavioral properties of third-party dependencies on update: 'did this new version's API contract or side-effect surface change?' Dependency-Track tells you a component has a known CVE; nothing tells you a component quietly changed behavior. This gap is exactly where supply-chain atta
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several tools (Socket.dev, Capslock, Aikido, GitHub Dependency Review, deps.dev) already surface behavior or capability changes on dependency updates, but each covers only a narrow slice (malware heuristics, Go-only capability graphs, or vulnerability/license diffs) rather than a unified, lightweigh
- Evidencia (prior art citado por Constellate):
  - https://socket.dev — Socket.dev: Uses static analysis on every published package version across npm, PyPI, Go, Maven and more, and flags when a dependency update introduces new risky API usage  [✓ show_hn:30515090 (url exacta)]
  - https://github.com/google/capslock — Google Capslock: A capability analysis CLI for Go packages that follows transitive calls to privileged standard library operations, reporting which privileged operations (file I [✓ github:google/capslock (repo)]
  - https://github.com/actions/dependency-review-action — GitHub Dependency Review Action: A GitHub Action that scans pull requests for dependency changes and reports which dependencies were added, removed, or updated, along with known vulnerabilities [✓ github:actions/dependency-review-action (repo)]
  - https://www.aikido.dev/blog/software-supply-chain-security-vulnerabilities — Aikido Security scanner: A supply-chain scanner that goes beyond CVEs to look for suspicious package behavior and malware signatures, flagging anomalies such as a new version suddenly o [✗ sin repo ni Show HN en el corpus]
  - https://blog.deps.dev/capslock/ — deps.dev (Open Source Insights) with Capslock integration: Google's package insight service that centrally runs analyses (including Capslock capability analysis) on Go packages and publishes results, noting that new cap [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): SCA continuo (Sonar, Socket, FOSSA) https://www.sonarsource.com/solutions/security/sca/ ; awesome-software-supply-chain-security https://github.com/bureado/awesome-software-supply-chain-security [parcial (SCA sí; garantías "formal-ish" de capacidades no del todo, ver capslock)]

propuesta: parcial
esperado: https://socket.dev https://github.com/google/capslock https://github.com/actions/dependency-review-action https://www.aikido.dev/blog/software-supply-chain-security-vulnerabilities https://blog.deps.dev/capslock/
confirmado: parcial

---

## 47 · 69926e60 · Missing: Deliberate Skill-Building Tooling for the Post-AI Junior

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood diagnoses the broken junior pipeline, questions whether learning to code still matters, notes that understanding beats origin, and observes that AI made knowledge cheap but the 'joins' — architectural judgment — expensive. Even LLM-generated code tours only address onboarding, not skill formation. What's conspicuously absent is a product that deliberately trains the judgment layer: tools that force juniors to predict, verify, and debug AI output rather than accept it, converting
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Scenario-based review/scoring platforms like LearningTo.co and CodeSignal's AI-assisted assessments come close to training the judgment layer, but no found product deliberately structures a predict-then-verify-then-debug practice loop specifically to convert AI-assisted work into deliberate skill fo
- Evidencia (prior art citado por Constellate):
  - https://learningto.co/ — LearningTo.co: A free scenario-based training platform where developers review realistic AI-generated code, Copilot output, MCP configs, and agent tool calls, get scored on th [✓ show_hn:49643992 (url exacta)]
  - https://codesignal.com/resource/ai-assisted-coding-assessments/ — CodeSignal AI-Assisted Coding Assessments / AI Literacy Assessments: Realistic workplace simulations that score how candidates and employees use AI tools, evaluate outputs critically, and know when not to trust AI, including agen [✗ sin repo ni Show HN en el corpus]
  - https://www.lanetteam.com/ai-tools-for-training-and-development — Snyk Learn: A developer-focused learning platform that shows real security bugs in code and teaches developers how to fix them using hands-on, practical lessons. [✗ sin repo ni Show HN en el corpus]
  - https://www.softwareseni.com/testing-and-debugging-ai-generated-code-systematic-strategies-that-work/ — SoftwareSeni AI-code debugging training curriculum: A described internal training program with modules on pattern-based debugging, static analysis proficiency, review checklist mastery, and calibration exercises  [✗ sin repo ni Show HN en el corpus]
  - https://blog.newtum.com/learn-programming-with-ai-safely/ — Newtum's VAPE framework guide: An educational article proposing a 'Verification-First Learning System' and a VAPE (Verify, Ask, ...) critical-thinking framework for junior developers to inter [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): solo debate/investigación (Anthropic sobre skills) https://www.anthropic.com/research/AI-assistance-coding-skills [débil -> posible hueco real]

propuesta: parcial
esperado: https://learningto.co/ https://codesignal.com/resource/ai-assisted-coding-assessments/ https://www.lanetteam.com/ai-tools-for-training-and-development https://www.softwareseni.com/testing-and-debugging-ai-generated-code-systematic-strategies-that-work/ https://blog.newtum.com/learn-programming-with-ai-safely/
confirmado: parcial

---

## 48 · 26d6adce · Missing: One-Click Self-Hosted Business-in-a-Box

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains self-hosted storage (Nextcloud AIO shows the packaging pattern), self-hosted invoicing, and an argument that email is now buildable from borrowed parts — yet no idea packages these into a single deployable 'solo business OS.' The AIO installer proves the demand for turnkey bundling exists; the gap is a curated, integrated stack (files + invoicing + email + client portal) for freelancers fleeing SaaS subscriptions. Each component exists; the composition layer doesn't.
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): General-purpose self-hosting platforms like Cloudron and YunoHost let a freelancer manually assemble files, invoicing, email, and portal apps under one login, but no single curated product pre-integrates exactly that four-part stack as a turnkey 'solo business OS.'
- Evidencia (prior art citado por Constellate):
  - https://www.cloudron.io/ — Cloudron: A self-hosted platform with one-click app installs, single sign-on, and a built-in email server, offering an app store that includes file sharing, invoicing (In [✓ show_hn:9976992 (heurístico, revisar: Show HN del dominio cloudron.io: "Cloudron – Get Your Own Cloud")]
  - https://yunohost.org/ — YunoHost: An open-source self-hosting distribution offering one-click installs of apps like InvoiceNinja/InvoiceShelf alongside file storage and email apps, with shared u [✓ github:YunoHost/yunohost (heurístico, revisar: repo con homepage yunohost.org)]
  - https://www.g2.com/products/ahsuite/discuss — Ahsuite: A hosted client portal tool for agencies/freelancers that consolidates tasks, files, conversations, and embeddable dashboards into one login, explicitly positio [✗ sin repo ni Show HN en el corpus]
  - https://bloom.io/ — Bloom: An all-in-one business workspace for creative freelancers combining invoicing, payments, project management, scheduling, contracts, and a client portal. [✗ sin repo ni Show HN en el corpus]
  - https://invoiceninja.com/software/cloudron/ — Invoice Ninja (self-hosted, Cloudron/YunoHost packaged): Self-hosted invoicing platform with client portal, expense tracking, and time billing, packaged for one-click deployment on platforms like Cloudron and YunoHost [✓ github:invoiceninja/invoiceninja (heurístico, revisar: repo con homepage invoiceninja.com)]
- Búsqueda propia (sep-2026, complementaria): solo piezas (InvoiceShelf, Invoice Ninja, Nextcloud AIO) https://invoiceshelf.com/ ; empaquetado integral: ver YunoHost/Cloudron (197bf4f9) [parcial]

propuesta: parcial
esperado: https://www.cloudron.io/ https://yunohost.org/ https://invoiceninja.com/software/cloudron/ https://www.g2.com/products/ahsuite/discuss https://bloom.io/
confirmado: parcial

---

## 49 · 36d540d3 · Missing: Proof-Without-Identity Verification Layer

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains the political rejection of digital ID and age verification, the cryptographic machinery for privacy-preserving data collection, and infrastructure for trusted information sharing. What's absent is the piece connecting them: practical anonymous credential tooling — proving attributes (age, membership, non-maliciousness) without revealing identity. The internal structure screams for zero-knowledge attestation as the resolution of the ID-versus-privacy standoff, yet no ide
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple real projects (Microsoft Vega, Google's ZKP age tools, Truvera, Idemix, World ID) already implement zero-knowledge attestation for age/attribute proving without identity disclosure, but they remain fragmented, product-specific, or narrowly scoped rather than a unified, general-purpose anony
- Evidencia (prior art citado por Constellate):
  - https://www.microsoft.com/en-us/research/blog/vega-zero-knowledge-proofs-for-digital-identity-in-the-age-of-ai/ — Microsoft Vega: An open-source-bound zero-knowledge proof system that lets users prove facts from government-issued credentials—age, personhood, professional status—without rev [✗ sin repo ni Show HN en el corpus]
  - https://captaincompliance.com/education/googles-zero-knowledge-proof-open-source-move-promotes-privacy-in-age-assurance/ — Google ZKP Age-Assurance Libraries / Google Wallet Age Signals: Open-sourced (Apache 2.0) ZKP libraries integrated into Google Wallet that let users verify age for apps like Bumble via cryptographic proofs without exposing f [✗ sin repo ni Show HN en el corpus]
  - https://www.dock.io/feature/zero-knowledge-proofs — Truvera (Dock Labs) Zero-Knowledge Proof Credentials: Provides digital-ID infrastructure using ZK-SNARKs, Threshold Anonymous Credentials (BBS+/Coconut), and verifiable encryption so holders can prove attributes li [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2205.05847 — Idemix (Identity Mixer): An anonymous credential system for digital identities that relies on CL-signatures to prove validity of a credential offline without involving the issuing organ [✗ sin repo ni Show HN en el corpus]
  - https://factually.co/fact-checks/technology/mainstream-apps-using-zero-knowledge-proofs-attribute-based-age-verification-how-they-work-c7b0c1 — World ID: A privacy-first identity project that advertises on-device ZKP proofs to meet age gates and prove personhood without revealing underlying identity data. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Privacy Pass (tokens anónimos) ; Privado ID/iden3 (ZK, BBS+) https://github.com/iden3 ; zk-creds (paper, convierte documentos existentes en credenciales anónimas) https://www.cs.umd.edu/~imiers/pdf/zkcreds.pdf ; ZK-Access https://github.com/farouk-allani/ZK-Access [fuerte]

propuesta: parcial
esperado: https://www.microsoft.com/en-us/research/blog/vega-zero-knowledge-proofs-for-digital-identity-in-the-age-of-ai/ https://captaincompliance.com/education/googles-zero-knowledge-proof-open-source-move-promotes-privacy-in-age-assurance/ https://www.dock.io/feature/zero-knowledge-proofs https://arxiv.org/pdf/2205.05847 https://factually.co/fact-checks/technology/mainstream-apps-using-zero-knowledge-proofs-attribute-based-age-verification-how-they-work-c7b0c1
confirmado: parcial

---

## 50 · b54b6842 · Missing: Proof-of-Human Infrastructure for Creators

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood contains the demand signal (rising anti-AI sentiment, distrust of manufactured culture), the economic casualty (creator middle class dying), and the cognitive worry (offloaded thinking) — but no idea offering verifiable human provenance for creative work. Given this structure, the gap is a lightweight attestation layer that lets creators prove human authorship and lets audiences pay a premium for it. The market is literally being described by these posts; the tool serving it is 
- Veredictos:
  - **partially** (web, output.json): Several honor-system badges (Not By AI, By Human Not AI, VerifiedHuman, CertifyUSA) and one academic cryptographic protocol (ZK-PoP) address pieces of the gap, but none combines rigorous verifiable attestation with an integrated payment/premium mechanism for audiences, so the unifying infrastructure
- Evidencia (prior art citado por Constellate):
  - https://www.verifiedhuman.info/ — VerifiedHuman: A certification platform where creators across eight creative disciplines commit to transparency about AI use and receive a badge showing their work is human-ma [✗ sin repo ni Show HN en el corpus]
  - https://certifyusa.org/blog/ai-free-content-badge — CertifyUSA AI-Free Content Badge: Issues a verified trust seal after a certifying body reviews a site's editorial process and authorship credentials, confirming content is human-written. [✗ sin repo ni Show HN en el corpus]
  - https://notbyai.fyi/ — Not By AI: Lets creators add badges to websites, blogs, art, film, essays, books, or podcasts declaring at least 90% of the content is human-made, with free non-commercial [✗ sin repo ni Show HN en el corpus]
  - https://www.byhumannotai.com/ — By Human, Not AI: Provides free, no-signup badges creators can add to writing, design, or websites to declare the work was made by a person and not generated by AI. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2603.00179 — ZK-PoP (Zero-Knowledge Proof of Human Authorship): A research construction that verifies human authorship by capturing behavioral biometric signals (keystroke dynamics, editing behavior) during writing and gener [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): ProofIDidIt (verificación human-made) https://proofididit.com/hub/proofididit-no-ai-certification ; AI-Free Cert https://www.aifreecert.com/ ; VerifiedHuman ; CAWG identity assertions [fuerte]

propuesta: parcial
esperado: https://www.verifiedhuman.info/ https://certifyusa.org/blog/ai-free-content-badge https://notbyai.fyi/ https://www.byhumannotai.com/ https://arxiv.org/abs/2603.00179
confirmado: parcial

---

## 51 · 4eb18786 · Missing: Runtime Stance Monitor for Deployed Chatbots

- Verificada por: web · corridas: 2026-07-16
- Idea: 3232 defines relational lock-in as a measurable risk object, 2847 defines register shift as probeable, and 3125 proves tone causally changes recipient behavior—yet all three measure offline. The obvious missing piece is a runtime middleware that scores stance drift, epistemic register, and dependency-inducing positioning on live conversations and alerts or steers before harm accrues. Companies deploying companions, therapy-adjacent bots, or customer agents have no such instrument today.
- Veredictos:
  - **partially** (web, output.json): Several real-time guardrail and monitoring systems (EmoAgent, SHIELD, GAUGE, SonderMind's guardrail architecture, WitnessAI) address pieces of runtime emotional/behavioral risk detection in live chatbot conversations, but none unify stance drift, epistemic register shift, and dependency-inducing rel
- Evidencia (prior art citado por Constellate):
  - https://spectrum.ieee.org/amp/mental-health-chatbot-guardrails-2676699987 — EmoAgent: Proposed real-time intermediary system that monitors dialogue for distress signals and issues corrective feedback to the underlying AI mid-conversation. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2512.06193 — GAUGE (Guarding Affective Utterance Generation-Escalation): A logit-based framework for real-time detection of hidden conversational escalation and affective drift in AI chatbots, designed originally for child-safety con [✗ sin repo ni Show HN en el corpus]
  - https://finance.biggo.com/news/52d5f5fbe28b3370 — SonderMind independent guardrail modules: An architecture where clinically-reviewed, independent LLM-judge guardrail modules operate separately from the main model to flag and act on unsafe or over-esca [✗ sin repo ni Show HN en el corpus]
  - https://witness.ai/blog/monitor-ai-chatbot-live-for-hallucinations/ — WitnessAI runtime chatbot monitoring middleware: A middleware layer that intercepts incoming prompts and outgoing responses in production, checking for factual drift, policy violations, manipulation attempts,  [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): sin producto claro: auditorías de sycophancy en investigación ; tone analyzers genéricos (patentes) [débil -> posible hueco real]

propuesta: parcial
esperado: https://spectrum.ieee.org/amp/mental-health-chatbot-guardrails-2676699987 https://arxiv.org/pdf/2512.06193 https://finance.biggo.com/news/52d5f5fbe28b3370 https://witness.ai/blog/monitor-ai-chatbot-live-for-hallucinations/
confirmado: parcial

---

## 52 · e01b3b33 · Missing: Sync and Monetization Rails for Backendless Apps

- Verificada por: web · corridas: 2026-07-31
- Idea: The no-backend builders here all hit the same walls—frozen tabs, storage limits, no accounts, no way to charge (explicitly catalogued in 5273's 'everything that broke'). The neighborhood is full of fully-client-side tools but contains no infrastructure piece: a lightweight toolkit for licensing, payments, cross-device sync, and WASM/ONNX resource management that preserves the zero-server ethos. That missing layer is what would turn these hobby demos into sellable products, and every author is re
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Individual fragments of the gap—ledger-based licensing/payments (overhide), cross-device sync (Replicache, PowerSync, RxDB), and payment UI (Stripe)—already exist as separate products, but no single toolkit unifies licensing, payments, sync, and WASM/ONNX resource management for zero-server apps as 
- Evidencia (prior art citado por Constellate):
  - https://overhide.github.io/ledgers.js/ — overhide (ledgers.js + Remuneration API): A browser-only JavaScript library and companion 'remuneration API' that lets single-page apps add logins and in-app purchases via ledger-based (crypto/fiat) aut [✗ sin repo ni Show HN en el corpus]
  - https://replicache.dev/ — Replicache: A client-side datastore and sync framework for building realtime, collaborative, local-first web apps that works with most backend stacks. [✗ sin repo ni Show HN en el corpus]
  - https://www.askantech.com/offline-first-mobile-architecture-apps-without-internet/ — PowerSync: An offline-first sync engine that keeps client-side SQLite in sync with backend Postgres/MongoDB/MySQL databases across mobile and web. [✗ sin repo ni Show HN en el corpus]
  - https://rxdb.info/alternatives.html — RxDB: A reactive, offline-capable JavaScript database with replication, encryption, and multi-tab support, positioned as an alternative to Replicache, InstantDB, Yjs, [✓ github:pubkey/rxdb (heurístico, revisar: repo con homepage rxdb.info)]
  - https://stackademic.com/blog/top-payment-apis-and-checkout-sdks-for-developers-in-2026 — Stripe Checkout / Elements: Client-embeddable payment UI components (Stripe Checkout hosted page, Stripe Elements) that let developers accept payments with minimal integration work. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Replicache/Zero, Jazz, PowerSync, ElectricSQL (sync local-first) https://replicache.dev/ ; https://github.com/alexanderop/awesome-local-first ; cobros: ver 47bf5f9f (Dodo, Monetize.software) [parcial-fuerte (sync sí; sync+cobro en uno no)]

propuesta: parcial
esperado: https://rxdb.info/alternatives.html https://overhide.github.io/ledgers.js/ https://replicache.dev/ https://www.askantech.com/offline-first-mobile-architecture-apps-without-internet/ https://stackademic.com/blog/top-payment-apis-and-checkout-sdks-for-developers-in-2026
confirmado: parcial

---

## 53 · 384c5945 · Missing: The Cost-and-Ops Layer for Self-Hosted AI

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood has RAG infrastructure pain, GPU multi-tenancy breaking in unmeasured ways, model export to escape Python runtimes, and license risk when choosing open weights. Everyone is self-hosting AI, yet there's no piece covering the obvious next need: a tool that benchmarks, monitors, and prices self-hosted inference stacks — 'what does this model actually cost me per request on my hardware, and where does it break under load'. The gap sits exactly where these four ideas intersect: teams
- Veredictos:
  - **partially** (web, output.json): GuideLLM benchmarks self-hosted deployments and Datadog prices them, but the combined answer to 'what does this cost per request on my hardware and where does it break under load' is still assembled by hand from separate tools.
- Evidencia (prior art citado por Constellate):
  - https://github.com/vllm-project/guidellm — GuideLLM: Benchmarks self-hosted LLM deployments for throughput, latency and cost under simulated load. [✓ github:vllm-project/guidellm (repo)]
  - https://docs.datadoghq.com/llm_observability/monitoring/cost/ — Datadog LLM Observability: Monitors LLM cost, accepting manually supplied rates for self-hosted models. [✓ github:DataDog/datadog-agent (heurístico, revisar: repo con homepage docs.datadoghq.com)]
  - https://docs.vllm.ai/en/latest/contributing/benchmarks.html — vLLM benchmark suite: Serving benchmarks bundled with vLLM for throughput and latency across configurations. [✗ sin repo ni Show HN en el corpus]
  - https://mlcommons.org/benchmarks/inference-datacenter/ — MLPerf Inference: Standardised industry benchmark for inference hardware and serving systems. [✗ sin repo ni Show HN en el corpus]
  - https://bentoml.com/llm/inference-optimization/llm-performance-benchmarks — BentoML LLM inference handbook: Documented methodology plus tooling for measuring self-hosted inference performance. [✓ github:bentoml/BentoML (heurístico, revisar: repo con homepage bentoml.com)]
- Búsqueda propia (sep-2026, complementaria): OpenCost (costo de inferencia en k8s, llm-d) https://opencost.io/blog/opencost-llmd-inference-cost/ ; OpenObserve costo por GPU-hora https://openobserve.ai/blog/llm-cost-monitoring/ ; nOps [parcial-fuerte]

propuesta: parcial
esperado: https://github.com/vllm-project/guidellm https://docs.datadoghq.com/llm_observability/monitoring/cost/ https://bentoml.com/llm/inference-optimization/llm-performance-benchmarks https://docs.vllm.ai/en/latest/contributing/benchmarks.html https://mlcommons.org/benchmarks/inference-datacenter/ !github:DataDog/datadog-agent
confirmado: parcial

---

## 54 · 0bf9e9ec · Missing: The Local-Compute Exit Ramp

- Verificada por: web · corridas: 2026-07-16
- Idea: One idea proves consumer GPUs run 27B models at real speed, another shows desktop hardware demand outstripping supply, a third exposes the financial fragility of hyperscale GPU financing, and a fourth shows physical resistance to datacenter buildout. The neighborhood clearly wants an off-ramp from hyperscaler dependence, yet no idea addresses the missing piece: turnkey products and marketplaces that let individuals and small teams run serious AI workloads on owned or pooled consumer hardware. Th
- Veredictos:
  - **partially** (web, output.json): Consumer-GPU marketplaces (Vast.ai) and turnkey local runtimes (Ollama, LM Studio) each exist, but nothing packages owned plus pooled consumer hardware into the single productized off-ramp the neighborhood implies.
- Evidencia (prior art citado por Constellate):
  - https://vast.ai/ — Vast.ai: Marketplace renting out consumer and datacenter GPUs from independent hosts at spot prices. [✓ github:vast-ai/vast-cli (heurístico, revisar: repo con homepage vast.ai)]
  - https://ollama.com/ — Ollama: Turnkey local model runtime that makes running sizeable models on consumer hardware a single command. [✓ github:ollama/ollama (heurístico, revisar: repo con homepage ollama.com)]
  - https://lmstudio.ai/ — LM Studio: Desktop application for running and serving local models with a GUI and OpenAI-compatible endpoint. [✓ show_hn:36060435 (url exacta)]
  - https://www.runpod.io/ — RunPod: GPU cloud with per-second billing and community hosts undercutting hyperscaler pricing. [✗ sin repo ni Show HN en el corpus]
  - https://www.spheron.network/ — Spheron: Aggregated bare-metal GPU marketplace spanning several underlying providers. [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): exo (cluster de inferencia con dispositivos caseros) https://github.com/exo-explore/exo ; GPUStack https://github.com/gpustack/gpustack [fuerte]

propuesta: parcial
esperado: https://lmstudio.ai/ https://vast.ai/ https://ollama.com/ https://www.runpod.io/ https://www.spheron.network/ !github:vast-ai/vast-cli
confirmado: parcial

---

## 55 · e3b4803b · Missing: The On-Device Mobile Agent Runtime

- Verificada por: web · corridas: 2026-07-31
- Idea: This neighborhood has agent languages, agent protocols, JVM agent frameworks, and AI assistants embedded in desktop tools (Xcode, macOS video editing). It also has a dense cluster of native iOS/Android apps. Yet nothing bridges them: there is no native, privacy-first agent runtime that runs on the phone itself, the way Harper does grammar checking offline. Given the local-first ethos of the surrounding projects (Harper, Bitwarden, UTM), an on-device Swift/Kotlin agent host implementing the agent
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several on-device inference SDKs and agent-tooling frameworks exist for iOS and/or Android (Cactus, SwiftAgent, Google ADK, Synapse Bridge, Kuzco), and Cactus even ships agentic MCP tool-calling across both platforms, but none of them are a mature, protocol-conformant (agent-host-protocol), cross-pl
- Evidencia (prior art citado por Constellate):
  - https://github.com/cactus-compute/cactus — Cactus: A cross-platform on-device inference engine and SDK (Kotlin Multiplatform, Swift/Apple, Flutter, React Native) that runs LLMs, VLMs, embeddings and TTS locally  [✓ github:cactus-compute/cactus (repo)]
  - https://github.com/achimala/SwiftAgent — SwiftAgent (achimala): A Swift package for embedding an AI agent inside an iOS app, currently shipping Hermes as the first supported agent runtime. It embeds CPython, bundles Hermes a [✗ repo fuera del bulk]
  - https://developer.android.com/ai/adk — Google ADK for Kotlin / ADK for Android: Lets developers build agents that execute AI models on-device using Gemini Nano via ML Kit GenAI APIs, and use the ADK Kotlin agent API to build AI agents that  [✗ sin repo ni Show HN en el corpus]
  - https://github.com/topics/android-llm — Synapse Bridge: A mobile agent framework for Android that enables the installation of desktop LLMs or custom agent builds to interact through a secure local MCP-based middlewar [✗ repo fuera del bulk]
  - https://medium.com/@jc_builds/how-to-run-local-ai-models-on-ios-macos-devices-with-kuzco-42173ba376ce — Kuzco / Haplo AI: A Swift package wrapper around the battle-tested llama.cpp engine that lets developers integrate LLMs directly into iOS, macOS, and Mac Catalyst apps with no cl [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Mobilerun (runtime de agentes para Android/iOS) https://mobilerun.ai/framework/ ; mobile-use https://github.com/minitap-ai/mobile-use ; agent-device https://github.com/callstack/agent-device [fuerte (control del teléfono; LLM on-device no necesariamente)]

propuesta: parcial
esperado: https://github.com/cactus-compute/cactus https://github.com/achimala/SwiftAgent https://developer.android.com/ai/adk https://github.com/topics/android-llm https://medium.com/@jc_builds/how-to-run-local-ai-models-on-ios-macos-devices-with-kuzco-42173ba376ce
confirmado: parcial

---

## 56 · a9d3aabb · Missing: a fidelity benchmark for synthetic humans

- Verificada por: web · corridas: 2026-07-31
- Idea: Multiple papers here test whether LLMs can stand in for humans (participants, examinees, judges) and each builds its own ad-hoc comparison against ground-truth human data. What's absent is a standardized, cross-domain benchmark and tooling that scores an LLM's human-simulation fidelity, including variance, individual differences, and belief-update dynamics, before researchers deploy it as a proxy. Given growing use of LLMs in social science and edtech calibration, this gap is glaring and immedia
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several recent benchmarks (SimBench, HumanStudy-Bench, When Synthetic Users Fail, LLM-S3, OpinionQA) each cover pieces of LLM human-simulation fidelity validation, but none unifies cross-domain coverage, individual-difference/variance scoring, and belief-update dynamics into a single standardized pr
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/abs/2510.17516 — SimBench: A large-scale, standardized, cross-domain benchmark that unifies 20 diverse human-behavior datasets (moral decision-making, economic choice, psychological asses [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2602.00685 — HumanStudy-Bench: A benchmark and execution engine that reconstructs published human-subject experiments end-to-end (Filter–Extract–Execute–Evaluate), replaying trial sequences a [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2607.26348 — When Synthetic Users Fail (Cross-Domain Benchmark): A single protocol run across multiple LLMs and two independent survey domains (GSS and World Values Survey) that benchmarks LLM-simulated respondents against no [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2510.17516 — OpinionQA / GlobalOpinionQA: Benchmarks evaluating how accurately LLMs represent the opinions of specific demographic groups by comparing model outputs to real survey response distributions [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2509.06337 — LLM-S3 (Large Language Models as Virtual Survey Respondents): A diagnostic benchmark using metrics like PAS and FAS to evaluate how well LLMs generate sociodemographically consistent synthetic survey responses, helping res [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/abs/2510.17516 https://arxiv.org/html/2602.00685 https://arxiv.org/abs/2607.26348 https://arxiv.org/pdf/2510.17516 https://arxiv.org/pdf/2509.06337
confirmado: parcial

---

## 57 · d1d36433 · Missing: a general-purpose VLM trust auditor

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood contains bespoke audits for place recognition, pathology benchmarks, detection confidence, radiology hallucination, and KGQA faithfulness—each a one-off, domain-specific verification pipeline. What's structurally absent is the horizontal piece: a reusable auditing framework or product that stress-tests any deployed VLM for leakage, miscalibration, and hallucination before deployment. Every one of these papers is unknowingly a feature of that missing tool. The demand is proven fi
- Veredictos:
  - **partially** (web, output.json): VLM auditing exists densely per aspect and per domain (MedVH, OSCAR, diagnostic hallucination frameworks) and general LLM eval platforms cover text, but no reusable horizontal auditor stress-tests any deployed VLM for leakage, miscalibration and hallucination together.
- Evidencia (prior art citado por Constellate):
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12363988/ — MedVH: Systematic hallucination evaluation framework for large vision-language models across six task types. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2605.00323v1 — OSCAR: Online self-calibration framework reducing VLM hallucination via tree search and preference optimisation. [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2603.15557 — Anatomy of a Lie: Multi-stage diagnostic framework tracing hallucinations through a model's generation trajectory. [✗ sin repo ni Show HN en el corpus]
  - https://www.giskard.ai/ — Giskard: Open-source testing framework scanning LLM applications for hallucination, bias and robustness failures. [✓ show_hn:40535874 (heurístico, revisar: Show HN del dominio giskard.ai: "Automatic generation of LLM guardrails with NeMo and Giskard")]
  - https://phoenix.arize.com/ — Arize Phoenix: Open-source evaluation and observability with LLM-as-judge scoring for relevance and hallucination. [✓ github:Arize-ai/phoenix (heurístico, revisar: repo con homepage arize.com)]

propuesta: parcial
esperado: https://www.giskard.ai/ https://phoenix.arize.com/ https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12363988/ https://arxiv.org/html/2605.00323v1 https://arxiv.org/html/2603.15557
confirmado: parcial

---

## 58 · 82197c7d · Missing: a red-team benchmark for agent security

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood has agent governance tooling, real breach post-mortems, a personal attack suite that broke its own defenses, a general agent evaluation framework, and a culture of pre-registered benchmarks. What's conspicuously absent is the connective piece: a standardized, reproducible adversarial benchmark that scores agent deployments against sequence-composition and privilege-escalation attacks the way OWASP scores web apps. Everyone here is either defending, attacking, or evaluating—nobod
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several recent benchmarks (ART, AgentRedBench, RIFT-Bench, BountyBench) and frameworks (DeepTeam) cover pieces of agent adversarial evaluation—prompt injection, tool misuse, privilege escalation—but no single result is a pre-registered, OWASP-style standardized benchmark unifying sequence-compositio
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2507.20526 — Agent Red Teaming (ART) Benchmark: A curated, empirical benchmark built from a large-scale public red-teaming competition that evaluates LLM-powered agents against thousands of real, working prom [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2606.02240 — AgentRedBench: A dynamic redteaming and integration-aware defense benchmark for LLM agents over SaaS integrations, grounded in real-world disclosed incidents and OWASP's agent [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2606.23927 — RIFT-Bench: A dynamic red-teaming framework for agentic AI systems that discovers a structured representation of a target codebase and uses it to instantiate, execute, trac [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2602.02164 — BountyBench: A benchmark that evaluates end-to-end vulnerability lifecycles including exploitation, defense, and patching for AI agent/cyber systems, measuring real-world of [✗ sin repo ni Show HN en el corpus]
  - https://www.trydeepteam.com/guides/guide-safety-frameworks — DeepTeam: An LLM/agent red-teaming framework that supports multiple standardized safety taxonomies (OWASP Top 10 for LLMs, OWASP Top 10 for Agentic Applications, NIST AI  [✓ github:confident-ai/deepteam (heurístico, revisar: repo con homepage trydeepteam.com)]
- Búsqueda propia (sep-2026, complementaria): AgentDojo (benchmark de prompt injection para agentes) https://github.com/ethz-spylab/agentdojo ; AgentDojo-Inspect (NIST) ; DTap [fuerte]

propuesta: parcial
esperado: https://www.trydeepteam.com/guides/guide-safety-frameworks https://arxiv.org/pdf/2507.20526 https://arxiv.org/pdf/2606.02240 https://arxiv.org/html/2606.23927 https://arxiv.org/pdf/2602.02164
confirmado: parcial

---

## 59 · cf6a474e · Missing: an audit log and permission layer for agents

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood has agents acting on computers, agents needing identity verification, and users discovering unauthorized AI access after the fact. What's structurally absent is the middle piece: a permissions and audit layer — a 'firewall/OAuth for agents' that records what an agent did, under whose delegation, and with what scope. The 922 incident shows demand (people discover access retroactively), and 170 shows the identity primitive exists but not the accountability one.
- Veredictos:
  - **partially** (web, output.json): Several real products (Prefactor, Arcade, WorkOS, ScaleKit, ACT Platform) already implement permission-plus-audit layers for AI agents that closely match the described gap, but they are fragmented point solutions rather than one dominant, widely-adopted 'firewall/OAuth for agents' standard, so the g
- Evidencia (prior art citado por Constellate):
  - https://prefactor.tech/product/agent-authentication — Prefactor: An authentication and authorization platform built specifically for AI agents that provides human-delegated access control, policy-as-code, and detailed agent-l [✗ sin repo ni Show HN en el corpus]
  - https://www.arcade.dev/ — Arcade (Arcade.dev): An MCP runtime that handles agent authentication, OAuth-based authorization, policy enforcement, and tool execution, letting agents act only on behalf of authen [✗ sin repo ni Show HN en el corpus]
  - https://workos.com/blog/ai-agent-access-control — WorkOS (AI agent access control: Connect, RBAC, Audit Logs): Combines authentication (WorkOS Connect/M2M/MCP), role-based permissions (RBAC), and audit logs so that agent actions are traceable and scoped, treating agents  [✓ github:workos/workos-node (heurístico, revisar: repo con homepage workos.com)]
  - https://www.scalekit.com/blog/delegated-agent-access — ScaleKit (On-Behalf-Of authentication for AI agents): Provides delegated, scoped, and auditable authorization for agents acting on behalf of users via JWTs with nested claims and OAuth-based delegation flows, plus  [✗ sin repo ni Show HN en el corpus]
  - https://www.acttokens.com/why-oauth-is-not-enough — ACT Platform (ACT Tokens): Positions itself explicitly as governing 'what autonomous agents can do' with policy definition, runtime enforcement, instant revocation, and full-context audit [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): Shani (capa de autorización para agentes con audit trail a prueba de manipulación) https://dev.to/kmori_f732750cda96b27efe7/i-built-an-open-source-authorization-layer-for-ai-agents-heres-what-the-audit-trail-looks-like-n5g ; Bifrost audit trails ; MintMCP gateway [fuerte]

propuesta: parcial
esperado: https://workos.com/blog/ai-agent-access-control https://prefactor.tech/product/agent-authentication https://www.arcade.dev/ https://www.scalekit.com/blog/delegated-agent-access https://www.acttokens.com/why-oauth-is-not-enough !github:workos/workos-node
confirmado: parcial

---

## 60 · c521a33a · Missing: merge-based continual learning as the forgetting cure

- Verificada por: web · corridas: 2026-07-16
- Idea: 491 and 1000 both fight catastrophic forgetting by protecting a single evolving model; 590 shows the root cause is interference within one parameter space; 3124 shows separately-trained experts can be merged post hoc, and that WHEN you merge matters. The obvious synthesis is absent: a continual-learning system that spawns lightweight per-task experts and merges them on a schedule informed by training duration, sidestepping single-model preservation entirely. The pieces exist; nobody in this neig
- Veredictos:
  - **partially** (web, output.json): Multiple recent papers (AIMMerging, MINGLE, BECAME, Merge before Forget, CP-MoE) already connect model merging to continual learning and even use training-trajectory or interference signals to time merges, but none precisely matches the described 'spawn lightweight per-task experts, merge on a train
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2509.17348 — AIMMerging (Adaptive Iterative Model Merging Using Training Trajectories): A continual-learning framework for LLMs that uses learning and forgetting signals extracted from training trajectories to adaptively adjust when and how often t [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2505.11883 — MINGLE (Mixture of Null-Space Gated Low-Rank Experts for Test-Time Continual Model Merging): Continual model merging framework that maintains a mixture-of-experts architecture with parameter-efficient low-rank experts extracted from independently fine-t [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2504.02666 — BECAME (Bayesian Continual Learning with Adaptive Model Merging): A two-stage continual learning framework that combines gradient projection with a Bayesian-derived closed-form optimal merging coefficient adapted to task chara [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2512.23017 — Merge before Forget (Single LoRA Continual Learning via Continual Merging): A continual learning method for LLMs that merges LoRA adapters into a single evolving LoRA to prevent forgetting instead of accumulating separate adapters per t [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2605.20247 — CP-MoE (Consistency-Preserving Mixture-of-Experts for Continual Learning): A continual learning framework built around a transient expert that captures early task-specific updates and guides their integration into a set of stable, shar [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/pdf/2509.17348 https://arxiv.org/abs/2505.11883 https://arxiv.org/abs/2504.02666 https://arxiv.org/pdf/2512.23017 https://arxiv.org/html/2605.20247
confirmado: parcial

---

## 61 · a0dfabb1 · Missing: mission control for swarms of local agents

- Verificada por: web · corridas: 2026-07-31
- Idea: Goose runs autonomous agents, worktrunk manages git worktrees explicitly for parallel agent workflows, jcode optimizes the harness for RAM efficiency, and Vector pipes observability data at scale — yet nothing here watches, compares, or arbitrates between the parallel agents these tools clearly anticipate. The gap is an agent-fleet observability and orchestration layer: which of my 8 concurrent agent branches is winning, what did each cost, when should one be killed. Every piece of the substrate
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several existing tools (Weave Fleet, agent-fleet-o, octomux, Nimbalyst, Orchestratia) provide fleet-level dashboards, worktree isolation, and observability for parallel coding agents, but none of the found products explicitly combine per-branch cost tracking with a 'which agent is winning / when to 
- Evidencia (prior art citado por Constellate):
  - https://tryweave.io/fleet/ — Weave Agent Fleet: A web UI that spawns, monitors, and interacts with multiple parallel OpenCode agent sessions, each isolated in its own worktree, with parent agents reviewing di [✗ sin repo ni Show HN en el corpus]
  - https://github.com/escapeboy/agent-fleet-o — agent-fleet-o: Self-hosted open-source orchestration platform with OpenTelemetry-based distributed tracing, a live agent/human team graph, and a dashboard showing active exper [✗ repo fuera del bulk]
  - https://github.com/andyrewlee/awesome-agent-orchestrators — octomux: A local dashboard with a kanban fleet view, unified permission inbox across agents, and in-app diff review for coding agents. [✓ github:andyrewlee/awesome-agent-orchestrators (repo)]
  - https://nimbalyst.com/blog/best-git-worktree-tools-ai-coding-2026/ — Nimbalyst: A visual workspace where each AI coding session optionally spawns its own git worktree, shown in a session kanban with per-session diff review panels for scanni [✓ github:nimbalyst/nimbalyst (heurístico, revisar: repo con homepage nimbalyst.com)]
  - https://orchestratia.com/ — Orchestratia: A single dashboard to coordinate Claude Code, Gemini CLI, Codex, and other CLI-based AI coding agents across multiple servers, with centralized monitoring, task [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): mission-control (Builderz, control plane self-hosted) https://github.com/builderz-labs/mission-control ; Agent-Dashboard https://github.com/toliko-coding/Agent-Dashboard ; Claude Code Agent View [fuerte]

propuesta: parcial
esperado: https://github.com/andyrewlee/awesome-agent-orchestrators https://nimbalyst.com/blog/best-git-worktree-tools-ai-coding-2026/ https://tryweave.io/fleet/ https://github.com/escapeboy/agent-fleet-o https://orchestratia.com/
confirmado: parcial

---

## 62 · 7a687ca9 · Missing: provenance layer for machine-made artifacts

- Verificada por: web · corridas: 2026-07-16
- Idea: We have agents producing code, verifying circuits, training other models, and a cop chasing slop after the fact. What's missing is the upstream piece: a provenance/attestation standard that records which agent, model, and loop produced an artifact, so downstream policing isn't forensic guesswork. The neighborhood defines detection and generation but nothing signs the chain of custody in between. A lightweight 'signed-by-agent' metadata tool for git commits and CI artifacts is the obvious gap.
- Veredictos:
  - **partially** (web, output.json): Multiple concrete tools (git-ai, agentdiff, agentmark, agent-sign, Agent Trace) already implement signed-by-agent commit/artifact metadata, but search results confirm no ratified, unified provenance standard exists yet — the space is fragmented and competing rather than solved.
- Evidencia (prior art citado por Constellate):
  - https://github.com/git-ai-project/git-ai — Git AI (git-ai): Tracks AI-generated code at the Git level by linking AI-authored lines to the agent, model, prompt, and session metadata that produced them, stored in Git Notes [✓ github:git-ai-project/git-ai (repo)]
  - https://github.com/codeprakhar25/agentdiff — agentdiff: Git-native AI code provenance tool that records which AI agent wrote which line, signs each attribution with ed25519, and stores it in git history across agents [✗ repo fuera del bulk]
  - https://agentmark.dev/ — agentmark: agentmark proves that code traveled through a verified autonomous AI pipeline with no direct human write path, providing a cryptographic audit trail signed with [✗ sin repo ni Show HN en el corpus]
  - https://github.com/always-further/agent-sign — agent-sign (nono / nolabs-ai): Provides security provenance and agent attestations from source to runtime using Sigstore/in-toto/DSSE bundles tied to CI workflow identity for files and releas [✗ repo fuera del bulk]
  - https://www.thinkscientist.com/ai-code-provenance-the-accountability-gap-nobody-has-closed/ — Agent Trace (Cognition AI): A specification announced by Cognition AI (makers of Devin) for embedding AI-generated metadata into git commits so automated edits are auditable and reviewable [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): propuesta OpenSSF de predicado in-toto "AI authorship" / openfab/generation https://github.com/ossf/tac/issues/628 ; SLSA+Sigstore para artefactos de IA ; Atlas (paper) [parcial (estándar en borrador)]

propuesta: parcial
esperado: https://github.com/git-ai-project/git-ai https://github.com/codeprakhar25/agentdiff https://agentmark.dev/ https://github.com/always-further/agent-sign https://www.thinkscientist.com/ai-code-provenance-the-accountability-gap-nobody-has-closed/
confirmado: parcial

---

## 63 · 5041f789 · Missing: security-grade observability for MCP agent traffic

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains an agent intrusion post-mortem, agent telemetry that shocked its own builders, and a major MCP spec change to stateless transport that makes session-level auditing harder, not easier. What's structurally missing is the piece these four imply: an audit/anomaly-detection layer purpose-built for stateless MCP traffic — a 'flight recorder' for agent-tool interactions. Everyone here is either migrating the protocol or cleaning up after incidents; nobody is building the middl
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): A crowded ecosystem of MCP gateways, proxies, and audit-logging guides (MintMCP, Operant AI, Kong, Gravitee, Obot, plus OWASP guidance) already provides logging, alerting, and anomaly-detection building blocks for MCP traffic, but none are explicitly framed or engineered as a dedicated 'flight recor
- Evidencia (prior art citado por Constellate):
  - https://www.mintmcp.com/blog/agent-gateway-audit-logging-observability — MintMCP (Agent Gateway + Agent Monitor): An MCP proxy/gateway that provides conversation-level audit logging, real-time monitoring of tool calls, bash commands, and file operations, plus off-gateway 's [✗ sin repo ni Show HN en el corpus]
  - https://www.integrate.io/blog/best-mcp-gateways-and-ai-agent-security-tools/ — Operant AI (AI-DR / Shadow Escape detection): Combines an MCP gateway with dedicated security research, offering detection for zero-click exploits like 'Shadow Escape', inline redaction, and AI Detection &  [✗ sin repo ni Show HN en el corpus]
  - https://developer.konghq.com/plugins/ai-mcp-proxy/ — Kong AI Gateway – AI MCP Proxy plugin: A Kong plugin that bridges MCP traffic into Kong's gateway, applying existing traffic management, authentication, and observability/analytics features to MCP re [✓ github:Kong/kong (heurístico, revisar: repo con homepage konghq.com)]
  - https://www.gravitee.io/blog/mcp-proxy-how-it-works-and-why-architects-need-one — Gravitee MCP Proxy: An AI-gateway capability that sits between MCP clients and servers, presenting as an MCP server/client pair to inspect, authorize, and log every method call acr [✗ sin repo ni Show HN en el corpus]
  - https://obot.ai/blog/the-value-of-an-mcp-proxy-security-control-and-observability-for-enterprise-ai/ — Obot MCP Proxy: An MCP proxy that centralizes credential management, policy enforcement, and logging of interactions between clients and remote MCP servers, with webhook-based  [✓ github:obot-platform/obot (heurístico, revisar: repo con homepage obot.ai)]
- Búsqueda propia (sep-2026, complementaria): NGINX agentic observability (módulo MCP) https://blog.nginx.org/blog/introducing-agentic-observability-in-nginx-real-time-mcp-traffic-monitoring ; IBM ContextForge https://github.com/IBM/mcp-context-forge ; Microsoft MCP Gateway ; MintMCP [fuerte]

propuesta: parcial
esperado: https://developer.konghq.com/plugins/ai-mcp-proxy/ https://obot.ai/blog/the-value-of-an-mcp-proxy-security-control-and-observability-for-enterprise-ai/ https://www.mintmcp.com/blog/agent-gateway-audit-logging-observability https://www.integrate.io/blog/best-mcp-gateways-and-ai-agent-security-tools/ https://www.gravitee.io/blog/mcp-proxy-how-it-works-and-why-architects-need-one
confirmado: parcial

---

## 64 · fc5cc4b2 · Missing: spam-resistant reputation that isn't surveillance

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains the openness of email and the backlash against identity mandates, but no idea offering the middle layer: portable, privacy-preserving sender reputation or proof-of-humanity that stops abuse without a government ID. Every piece implies its necessity; none proposes it. This is the gap where cryptographic attestations or web-of-trust reputation tooling should sit.
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Proof-of-personhood and web-of-trust reputation systems like BrightID, Human Passport, and Kleros PoH already implement privacy-preserving, non-government-ID Sybil resistance, and an IETF draft even proposes cryptographic sender attestation for email, but none of these are unified into a portable, c
- Evidencia (prior art citado por Constellate):
  - https://www.brightid.org/ — BrightID: BrightID is a decentralized social identity network that lets users prove they hold only one unique account by building and analyzing a peer-to-peer social grap [✓ github:BrightID/BrightID (heurístico, revisar: repo con homepage brightid.org)]
  - https://passport.human.tech/ — Human Passport (formerly Gitcoin Passport): A decentralized, privacy-preserving identity/reputation aggregator that combines multiple 'Stamps' into a Unique Humanity Score to help apps prevent spam, bots, [✗ sin repo ni Show HN en el corpus]
  - https://docs.kleros.io/products/proof-of-humanity — Kleros Proof of Humanity (PoH): A decentralized registry where humans are vouched for by already-verified members via video submission and challenge periods, aiming to ensure one unique human  [✗ sin repo ni Show HN en el corpus]
  - https://datatracker.ietf.org/doc/draft-drake-email-hardware-attestation/ — Hardware Attestation for Email Sender Verification (IETF draft-drake-email-hardware-attestation): An IETF draft proposing that email senders attach hardware/TPM-based or SD-JWT cryptographic attestations to messages so receiving servers can verify sender leg [✗ sin repo ni Show HN en el corpus]
  - https://lwn.net/Articles/629196/ — Darkmail-style Web of Trust anti-spam concept (discussed on LWN): A discussion of using an end-to-end encrypted mail system (like Darkmail) combined with a web-of-trust of legitimate senders so spam filters can score messages  [✗ sin repo ni Show HN en el corpus]
- Búsqueda propia (sep-2026, complementaria): solo reputación convencional (SPF/DKIM, Spamhaus) ; Sandi (paper, accountability sin vigilancia) https://arxiv.org/pdf/2401.16759 [débil -> posible hueco real]

propuesta: parcial
esperado: https://www.brightid.org/ https://passport.human.tech/ https://docs.kleros.io/products/proof-of-humanity https://datatracker.ietf.org/doc/draft-drake-email-hardware-attestation/ https://lwn.net/Articles/629196/
confirmado: parcial

---

## 65 · 19e97add · No One Benchmarks FL Under Combined Adversity

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains defenses against server backdoors, client backdoors, privacy-preserving clustering, heterogeneous PEFT, and incentive-stable coalitions—yet each is evaluated in isolation under its own threat model and heterogeneity assumptions. Missing is a standardized adversarial-plus-heterogeneous FL harness, analogous to what 4342 does for data agents, where privacy attacks, backdoors, statistical skew, and strategic dropout co-occur. Without it, every defense's 'zero utility loss'
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Benchmarks like ATR-Bench and FLAT-Bench unify heterogeneity with adversarial/trust robustness, and BackFed/FedScale standardize backdoor or system-heterogeneity evaluation, but none of the found projects co-model privacy-inference attacks, backdoors, statistical skew, and strategic/incentive dropou
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/abs/2505.16850 — ATR-Bench: A Federated Learning Benchmark for Adaptation, Trust, and Reasoning: A unified benchmark that empirically evaluates FL methods jointly across statistical/domain heterogeneity ('Adaptation') and adversarial/unreliable-client robus [✗ sin repo ni Show HN en el corpus]
  - https://openreview.net/pdf?id=cmtX6JCqVR — FLAT-Bench: A Federated Learning Benchmark: A unified benchmark categorizing and empirically evaluating FL challenges across Adaptation (including federated LoRA fine-tuning) and Trustworthiness (robustne [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2507.04903 — BackFed: An Efficient & Standardized Benchmark Suite for Backdoor Attacks in Federated Learning: A standardized benchmark that unifies backdoor attacks and defenses in FL under realistic threat models, testing across IID/non-IID (Dirichlet) heterogeneity se [✗ sin repo ni Show HN en el corpus]
  - https://parsa.epfl.ch/course-info/cs723/papers/fedscale.pdf — FedScale: A large-scale FL benchmarking platform with real-world datasets, non-IID data partitioning, heterogeneous client system speeds, and dynamic client availability, [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2206.03436 — B-FHTL: A Benchmark for Federated Hetero-Task Learning: A benchmark generalizing FL to federated hetero-task learning, providing simulation datasets, protocols and a unified evaluation mechanism for tasks with increa [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/abs/2505.16850 https://openreview.net/pdf?id=cmtX6JCqVR https://arxiv.org/abs/2507.04903 https://parsa.epfl.ch/course-info/cs723/papers/fedscale.pdf https://arxiv.org/pdf/2206.03436
confirmado: parcial

---

## 66 · 160dbf81 · Nobody Benchmarks Whether World Models Actually Predict

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood has world model architectures, datasets, causal training, security threat models, and even a kill switch for agents—plus a separate cluster obsessed with broken verifiers and noisy quality gates. What's missing is the intersection: a faithfulness benchmark or runtime monitor that scores whether a world model's predicted futures match reality before an embodied agent acts on them. Security and kill switches assume you can detect a compromised or hallucinating predictive core, but
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Multiple recent benchmarks and research predictors (WR-Arena, Physics-IQ, WorldLens, WorldPrediction, and hallucination-predictor papers) address pieces of world-model faithfulness and hallucination detection, but none combine this into a runtime monitor that gates an embodied agent's actions using 
- Evidencia (prior art citado por Constellate):
  - https://www.researchgate.net/publication/408106936_Hallucination_in_World_Models_is_Predictable_and_Preventable — Hallucination in World Models is Predictable and Preventable: Develops training-free, label-free runtime predictors (e.g., tokenizer round-trip residual) that detect when a world model's rollout has diverged into a halluci [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2603.25887 — WR-Arena (World Reasoning Arena): A benchmark that evaluates world models on action simulation fidelity, long-horizon forecast consistency, and simulative reasoning/planning against ground truth [✗ sin repo ni Show HN en el corpus]
  - https://physics-iq.github.io/ — Physics-IQ: A benchmark using real filmed video that scores whether a model's predicted continuation/dynamics match real physical outcomes across mechanics, fluids, optics, [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2512.10958 — WorldLens: A full-spectrum benchmark evaluating driving world models across perception, geometry, function, and human alignment with over twenty standardized metrics. [✗ sin repo ni Show HN en el corpus]
  - https://www.researchgate.net/publication/392466733_WorldPrediction_A_Benchmark_for_High-level_World_Modeling_and_Long-horizon_Procedural_Planning — WorldPrediction: A benchmark for high-level world modeling and long-horizon procedural planning, testing whether models can predict plausible future states over extended action  [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://www.researchgate.net/publication/408106936_Hallucination_in_World_Models_is_Predictable_and_Preventable https://arxiv.org/html/2603.25887 https://physics-iq.github.io/ https://arxiv.org/pdf/2512.10958 https://www.researchgate.net/publication/392466733_WorldPrediction_A_Benchmark_for_High-level_World_Modeling_and_Long-horizon_Procedural_Planning
confirmado: parcial

---

## 67 · 7048229f · Nobody Built Interpretable Anomaly Detection for the Edge

- Verificada por: web · corridas: 2026-07-16
- Idea: The neighborhood contains interpretable prototype models for critical domains, lightweight edge anomaly detection, zero-shot foundation approaches, and evidence that real industrial data defeats benchmarks. The obvious missing piece: an interpretable, prototype-based, resource-constrained anomaly detector that tells an operator WHY a sensor reading is anomalous, on-device. Every ingredient exists in this cluster, but interpretability and edge efficiency are never combined — precisely the combina
- Veredictos:
  - **partially** (web, output.json): Interpretable plus edge-efficient anomaly detection is now common in IoT intrusion detection research (QAE-IDS, neuro-symbolic frameworks, SHAP-on-device), but not as a product for industrial sensor operators, and the papers themselves note accuracy is still traded against explainability.
- Evidencia (prior art citado por Constellate):
  - https://link.springer.com/article/10.1007/s10791-026-10310-x — QAE-IDS: Quantized edge intrusion detection combining lightweight on-device detection with explainable multiclass analysis. [✗ sin repo ni Show HN en el corpus]
  - https://link.springer.com/article/10.1007/s44397-026-00047-z — Neuro-symbolic edge IDS: Lightweight neural learning plus symbolic rule reasoning distilled for real-time edge deployment. [✗ sin repo ni Show HN en el corpus]
  - https://www.nature.com/articles/s41598-026-43578-6 — Lightweight interpretable edge AI for cardiac IoT: Interpretable edge intelligence for trustworthy arrhythmia detection on medical IoT devices. [✗ sin repo ni Show HN en el corpus]
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12845731/ — Explainable IDS for IoT — systematic review: Survey of explainable deep-learning intrusion detection across IoT networks. [✗ sin repo ni Show HN en el corpus]
  - https://www.researchgate.net/publication/362693104_An_edge_computing_based_anomaly_detection_method_in_IoT_industrial_sustainability — Edge computing anomaly detection for industrial IoT: Edge-based anomaly detection method for industrial IoT sustainability monitoring. [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://link.springer.com/article/10.1007/s10791-026-10310-x https://link.springer.com/article/10.1007/s44397-026-00047-z https://www.nature.com/articles/s41598-026-43578-6 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12845731/ https://www.researchgate.net/publication/362693104_An_edge_computing_based_anomaly_detection_method_in_IoT_industrial_sustainability
confirmado: parcial

---

## 68 · 1fd3aeb9 · Nobody Built the Model That Says 'I Don't Know'

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood documents confabulation, decoupled reasoning, noisy-feedback overfitting, and temporal blind spots, yet no idea proposes calibrated abstention: a medical VLM layer that detects insufficient evidence and refuses to answer. Given how thoroughly failure modes are mapped here, an evidence-sufficiency gate or confidence-audit wrapper is the obvious missing piece. It could be built as middleware over existing models rather than a new foundation model.
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Calibrated abstention for medical VLMs exists as an active research direction (CALM-VLM, ReCoVERR, conformal LVLM methods, Reliable VQA, MedAbstain), but no single found product unifies medical-specific evidence-sufficiency gating as reusable middleware over arbitrary existing medical VLMs.
- Evidencia (prior art citado por Constellate):
  - https://pubmed.ncbi.nlm.nih.gov/42039377/ — CALM-VLM (Calibration Mechanism for Vision-Language Models): Integrates temperature-scaling calibration and selective abstention into a generative 3D medical VLM (built on Med3DVLM) for brain MRI diagnosis, so the model w [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/abs/2402.15610 — ReCoVERR: An inference-time algorithm that sits on top of VLMs (BLIP2, InstructBLIP, LLaVA) and reduces unnecessary abstention by actively seeking additional visual evide [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2606.16667v3 — ConfLVLM / conformal abstention methods for LVLMs (e.g. CAP, CEBC): Distribution-free conformal frameworks that filter unreliable claims, learn per-instance conformal risk levels, or edit unsupported mentions in large vision-lan [✗ sin repo ni Show HN en el corpus]
  - https://ar5iv.labs.arxiv.org/html/2204.13631 — Reliable VQA ("Abstain Rather Than Answer Incorrectly"): Formalizes VQA as a selective prediction problem, enabling abstention capabilities on top of several existing VQA models and introducing a risk/coverage-based E [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2601.12471v2 — Knowing When to Abstain: Medical LLMs Under Clinical Uncertainty (MedAbstain): Evaluates and benchmarks abstention behavior of medical LLMs under clinical uncertainty, probing confidence/abstention correlation with an added abstention opti [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://pubmed.ncbi.nlm.nih.gov/42039377/ https://arxiv.org/abs/2402.15610 https://arxiv.org/html/2606.16667v3 https://ar5iv.labs.arxiv.org/html/2204.13631 https://arxiv.org/html/2601.12471v2
confirmado: parcial

---

## 69 · b52fedb0 · Nobody Is Building Deepfake Detection for Generated 3D/4D

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood contains powerful generative 3D/4D pipelines, a deepfake detector for 2D images, and a quality assessor for 3DGS scenes—but no forensic authenticity tool for generated 3D/4D content. As text-to-4D humans and re-shot videos become indistinguishable from captured footage, the 2D forensic toolkit won't transfer, and 4845 only measures quality, not provenance. The missing piece is a detector that flags whether a 3D scene or re-rendered video was measured or hallucinated—exactly the 
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Dedicated 3D forensic detectors like Fake3DGS and 3DDGD exist for static 3DGS manipulation and 3D face meshes, but no found tool addresses provenance detection for fully text-to-4D generated dynamic humans or re-shot video, leaving the core of the described gap open.
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/abs/2604.27590 — Fake3DGS: Introduces the first benchmark and detector formalizing 3D fake detection for 3D Gaussian Splatting scenes, using multi-view coherence and Gaussian-representati [✗ sin repo ni Show HN en el corpus]
  - https://www.researchgate.net/publication/395526840_A_Controllable_3D_Deepfake_Generation_Framework_with_Gaussian_Splatting — 3DDGD (3D Deepfake Generation and Detection Using 3D Face Meshes): A study creating a dataset of real and fake 3D face meshes and developing detection models (mesh-MLP, self-attention, TabTransformer) to distinguish real 3D fac [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2606.03499 — Characterizing Detectability in 3DGS Poisoning (Stage-wise Benchmark): Benchmarks detectors operating on stage-specific artifacts (multi-view images, geometry, training dynamics, Gaussian parameters) to detect poisoning/tampering a [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2509.11624 — A Controllable 3D Deepfake Generation Framework with Gaussian Splatting: Primarily a 3D deepfake generation method for Gaussian-Splatting-based face swapping/reenactment, but explicitly evaluates and discusses robustness against exis [✗ sin repo ni Show HN en el corpus]
  - https://sightengine.com/detect-ai-generated-videos — Sightengine AI Video Detector: A commercial pixel-based AI video detection API/tool that flags whether videos are AI-generated or deepfakes, working even when metadata/watermarks are stripped [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://arxiv.org/abs/2604.27590 https://www.researchgate.net/publication/395526840_A_Controllable_3D_Deepfake_Generation_Framework_with_Gaussian_Splatting https://arxiv.org/html/2606.03499 https://arxiv.org/pdf/2509.11624 https://sightengine.com/detect-ai-generated-videos
confirmado: parcial

---

## 70 · 7918616b · Nobody built access control for agent memory

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood has trust scoring (Σ-Mem), value-aware management (MemLens), poisoning tracking (MemSecBench), rollback (ChronoMem), and privacy-conscious storage — yet no idea addresses who and what may read or write which memories: permissions, scopes, provenance-based ACLs per agent, tool, or session. Every security and reliability problem in these papers is downstream of unrestricted write access. The missing piece is an authorization layer for agent memory — essentially IAM for memories — 
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several products and one academic framework implement pieces of memory-specific access control (privilege groups, scoped retrieval, provenance-tagged permission graphs), but none combine provenance-based ACLs, fine-grained read/write scopes per agent/tool/session, and integration with rollback/versi
- Evidencia (prior art citado por Constellate):
  - https://arxiv.org/pdf/2508.19870 — Collaborative Memory framework (Rezazadeh et al.): A multi-LLM memory architecture that encodes memory access permissions as a time-evolving bipartite graph, tagging each memory fragment with provenance and enfo [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2403.16971 — AIOS Access Manager: A kernel-level component of the AIOS LLM agent operating system that controls read/write permissions when agents request access to other agents' memory, using p [✗ sin repo ni Show HN en el corpus]
  - https://www.mintmcp.com/blog/long-term-memory-ai-agents — MintMCP Agent Gateway: An enterprise memory governance layer that scopes agent memory (private, team, organization, customer) to agent identity, providing authentication, authorizatio [✗ sin repo ni Show HN en el corpus]
  - https://workos.com/blog/agents-need-authorization-not-just-authentication — WorkOS Fine-Grained Authorization (FGA) for AI agents: A relationship-based fine-grained authorization system for AI agents that can anchor embeddings/context shards to FGA resource IDs and enforce role-based checks [✗ sin repo ni Show HN en el corpus]
  - https://www.cerbos.dev/blog/permission-management-for-ai-agents — Cerbos permission management for AI agents: A centralized policy engine that filters RAG/agent data access based on user permissions across data, API, and application layers, ensuring agents only access a [✓ github:cerbos/cerbos (heurístico, revisar: repo con homepage cerbos.dev)]
- Búsqueda propia (sep-2026, complementaria): mem0 governance/seguridad de memoria https://mem0.ai/blog/ai-memory-security-best-practices ; guías MindStudio (tiers con ACL) [parcial (prácticas y features, no capa dedicada)]

propuesta: parcial
esperado: https://www.cerbos.dev/blog/permission-management-for-ai-agents https://arxiv.org/pdf/2508.19870 https://arxiv.org/pdf/2403.16971 https://www.mintmcp.com/blog/long-term-memory-ai-agents https://workos.com/blog/agents-need-authorization-not-just-authentication
confirmado: parcial

---

## 71 · a5e2487c · Nobody evaluates whether agent memory is worth keeping

- Verificada por: web · corridas: 2026-07-31
- Idea: The neighborhood is dense with memory mechanisms — reconstruction, contribution scoring, episodic-to-parametric transfer, self-distillation, and harness evolution — but contains no benchmark or tooling that measures memory quality itself: contamination, staleness, negative transfer, or when accumulated experience actively hurts. Trace-level agent eval exists, but nothing audits the memory layer as a first-class artifact. The missing piece is a memory observability/eval suite: given an agent's me
- Veredictos:
  - **partially** (web, claude-sonnet-5 2026-08-10): Several products and papers address individual pieces of the gap — production memory observability (memgram), post-hoc poisoning attribution (MemAudit), staleness-specific benchmarks (STALE), and general memory-capability benchmarks (MemoryAgentBench) — plus a survey explicitly calling for the missi
- Evidencia (prior art citado por Constellate):
  - https://memgram.io/ — memgram: Production memory infrastructure that gives AI teams observable, controllable memory: traces every extraction, retrieval, deduplication, and supersession/contra [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2605.23723 — MemAudit: A post-hoc auditing framework for memory-augmented LLM agents that uses counterfactual causal attribution and structural anomaly detection to identify which sto [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/pdf/2605.06527 — STALE benchmark: A benchmark of expert-validated conflict scenarios testing whether LLM agents can detect when their memories are outdated, resist stale premises, and adapt beha [✗ sin repo ni Show HN en el corpus]
  - https://www.emergentmind.com/topics/memoryagentbench — MemoryAgentBench: A unified benchmark suite assessing LLM agent memory across accurate retrieval, test-time learning, long-range understanding, and conflict resolution using incr [✗ sin repo ni Show HN en el corpus]
  - https://arxiv.org/html/2603.07670v1 — "Memory for Autonomous LLM Agents" four-layer evaluation stack (survey proposal): Proposes a conceptual four-layer evaluation framework (task effectiveness, memory quality — precision/recall/contradiction/staleness, efficiency, governance) an [✗ sin repo ni Show HN en el corpus]

propuesta: parcial
esperado: https://memgram.io/ https://arxiv.org/html/2605.23723 https://arxiv.org/pdf/2605.06527 https://www.emergentmind.com/topics/memoryagentbench https://arxiv.org/html/2603.07670v1
confirmado: parcial

---

