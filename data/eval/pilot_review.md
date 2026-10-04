# Piloto Fase 3: 50 pares, Jev vs Haiku

Candidatos del top-1000 con embeddings MiniLM + llm5. Probabilidades de: implementa el núcleo, implementa al menos una parte real del núcleo, mismo usuario objetivo. Completá la línea `mi veredicto` de cada par.

Jev: 50/50 pares con respuesta. Haiku: 50/50.

**Pares donde Jev y Haiku difieren en núcleo por más de 0.3:** #19

---

## 1. positivo · `real-89c010f2` (real) · rank 56

**Idea:** I need a lightweight layer that sits between an AI agent and the outside world, intercepting every side effect it tries to perform — file writes, network requests, payments, tool calls — and either logging it, asking me for approval, or blocking it based on rules. Containment sandboxes exist, but nothing governs what an agent is allowed to do inside its permitted scope.

**Candidato:** `show_hn:49083015` https://github.com/preloop/preloop  
**Preloop: Open-source control plane for AI agents. See, govern, cut cost** — The open-source AI agent control plane: MCP firewall, model gateway with budgets, human approvals, runtime observability, and audit trails
Topics: agentops, ai-agent-control-plane, ai-agents, ai-gateway, ai-safety, automation, claude-code, firewall, governance, guardrails, human-in-the-loop, llm, llm-gateway, mcp, mcp-proxy, observability, policy-as-code, self-hosted
Preloop
The open-source AI agent control plane.** See them, govern them, cut their cost.
Preloop is one self-hostable service that sits between your AI agents and everything they reach, so every tool call and every model call is g

- Jev: núcleo **0.93** · parcial 0.93 · mismo usuario 0.91
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.90

mi veredicto: núcleo / parcial / no

---

## 2. positivo · `real-6f3848c8` (real) · rank 25

**Idea:** I need a production-ready policy layer that intercepts actions from teams of autonomous AI agents before they execute, enforcing programmable permissions, spending caps, audit logging, and human escalation rules.

**Candidato:** `github:microsoft/agent-governance-toolkit` https://github.com/microsoft/agent-governance-toolkit  
**agent-governance-toolkit** — AI Agent Governance Toolkit — Policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering for autonomous AI agents. Covers 10/10 OWASP Agentic Top 10.
Topics: agent-framework, ai-agents, ai-safety, compliance, governance, microsoft, owasp, policy-engine, python, security, trust, zero-trust
🌍 English | 日本語 | 简体中文 | 한국어
Agent Governance Toolkit
Ship agents to production without losing sleep
🚀 Quick Start ·
📋 Specifications ·
📦 PyPI ·
📝 Changelog 
brightgreen)
[!IMPORTANT]
Public Preview** -- production-quality public preview releases. May have breaking changes befo

- Jev: núcleo **0.82** · parcial 0.81 · mismo usuario 0.92
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.90

mi veredicto: núcleo / parcial / no

---

## 3. positivo · `real-47bf5f9f` (real) · rank 41

**Idea:** I need a way to sell license keys, one-time unlocks, or subscriptions for apps that run entirely in the browser or on the user's device, with no server of my own to validate purchases. Something lightweight that handles checkout and offline/edge-verifiable license checks for client-side apps and browser extensions.

**Candidato:** `show_hn:44635244` https://keyforge.dev/features/offline  
**I made a simple offline licensing system with JWTs** — Hey HN,
Around 2 months ago, I launched my project, a simple to use licensing system for developers that works anywhere.
And now I'm launching a new feature, offline licensing. For this, a token is generated for a license and verified on the client with a public key, without needing the internet.
Would love to get any feedback, on the feature itself or even on my feature page!

- Jev: núcleo **0.66** · parcial 0.86 · mismo usuario 0.85
- Haiku: núcleo **0.85** · parcial 0.95 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 4. positivo · `real-a6c38804` (real) · rank 27

**Idea:** I need a way to monitor and control autonomous AI agents at runtime: a trace of every action they take on the web and every change they make to their own code or prompts, with alerts and a kill switch when their behavior drifts. It should be a lightweight SDK plus a dashboard, not infrastructure monitoring.

**Candidato:** `github:AgentOps-AI/agentops` https://github.com/AgentOps-AI/agentops  
**agentops** — Python SDK for AI agent monitoring, LLM cost tracking, benchmarking, and more. Integrates with most LLMs and agent frameworks including CrewAI, Agno, OpenAI Agents SDK, Langchain, Autogen, AG2, and CamelAI
Topics: agent, agentops, agents-sdk, ai, anthropic, autogen, cost-estimation, crewai, evals, evaluation-metrics, groq, langchain, llm, mistral, ollama, openai, openai-agents
Observability and DevTool platform for AI Agents 
AgentOps helps developers build, evaluate, and monitor AI agents. From prototype to production.
Open Source
The AgentOps app is open source under the MIT license. Explore

- Jev: núcleo **0.47** · parcial 0.81 · mismo usuario 0.79
- Haiku: núcleo **0.35** · parcial 0.65 · mismo usuario 0.85

mi veredicto: núcleo / parcial / no

---

## 5. positivo · `real-8b190bdc` (real) · rank 668

**Idea:** I need a runtime layer that sits between an LLM's curation or judging output and the end user, scoring each response for ideological or framing skew and then rebalancing or flagging it before delivery. Existing work only measures bias offline; I want an enforceable mitigation component in production.

**Candidato:** `github:NVIDIA-NeMo/Guardrails` https://github.com/NVIDIA-NeMo/Guardrails  
**Guardrails** — NeMo Guardrails is an open-source toolkit for easily adding programmable guardrails to LLM-based conversational systems.
Topics: agents, generative-ai, guardrails, llm-safety, llm-security, llms, nvidia, python, safety
NVIDIA NeMo Guardrails Library
LATEST RELEASE / DEVELOPMENT VERSION**: The develop branch tracks the latest top of tree development. The latest released version is 0.24.1.
✨✨✨
📌 **The official NeMo Guardrails library documentation is available at docs.nvidia.com/nemo/guardrails.**
✨✨✨
NVIDIA NeMo Guardrails library is an open-source toolkit for easily adding *programmable guardr

- Jev: núcleo **0.28** · parcial 0.63 · mismo usuario 0.69
- Haiku: núcleo **0.25** · parcial 0.45 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 6. positivo · `real-01fe2dbe` (real) · rank 10

**Idea:** I need a real-time chat system I can run on my own server, where messages are end-to-end encrypted so the server operator can't read them, and with clients that feel as polished as commercial apps.

**Candidato:** `show_hn:10112932` https://rocket.chat/  
**Host your own open source Slack-like chat platform** — 

- Jev: núcleo **0.25** · parcial 0.49 · mismo usuario 0.58
- Haiku: núcleo **0.25** · parcial 0.65 · mismo usuario 0.85

mi veredicto: núcleo / parcial / no

---

## 7. positivo · `real-7c597ec1` (real) · rank 965

**Idea:** I need shared infrastructure for managing AI evaluation datasets themselves "" a layer that lets you compose benchmarks from parts, version them, detect duplicate or overlapping test items across suites, and track when a benchmark becomes saturated or obsolete. Right now every new evaluation is a one-off that doesn't build on the ones before it.

**Candidato:** `github:EleutherAI/lm-evaluation-harness` https://github.com/EleutherAI/lm-evaluation-harness  
**lm-evaluation-harness** — A framework for few-shot evaluation of language models.
Topics: evaluation-framework, language-model, transformer
Language Model Evaluation Harness
Latest News 📣
[2026/09] **Plugins**: model backends, filters, metrics and aggregations can now be registered from your own package instead of forking — declare an `lm_eval.*` entry point for zero-config discovery, or point `--plugins` at a local module. See the Plugin Guide.
[2025/12] **CLI refactored** with subcommands (`run`, `ls`, `validate`) and YAML config file support via `--config`. See the CLI Reference and Configuration Guide.
[2025/12] **

- Jev: núcleo **0.17** · parcial 0.49 · mismo usuario 0.42
- Haiku: núcleo **0.25** · parcial 0.35 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 8. positivo · `syn-2879393` (synthetic) · rank 21

**Idea:** I want a recurring monthly package of foreign sweets and treats shipped to my home.

**Candidato:** `show_hn:2879393` https://news.ycombinator.com/item?id=2879393  
**Just Launched, subscription to candies from the world. TheHoneyDay.com** — the site is http://thehoneyday.com
Original idea is from bemmu (candyjapan.com), but we are targeting different market and different goals. This is the mvp version, if enough interest, we are thinking of making it like a "pandora for snacks".
Feedbacks and inputs are very much appreciated

- Jev: núcleo **0.80** · parcial 0.69 · mismo usuario 0.79
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.88

mi veredicto: núcleo / parcial / no

---

## 9. positivo · `syn-44939278` (synthetic) · rank 1

**Idea:** Before a trip to Europe from North Africa I need a proof-of-coverage document that consulates accept, available immediately online.

**Candidato:** `show_hn:44939278` https://e-mai.ma/calculateur-dassurance-voyage-maroc/  
**Instant visa-compliant insurance certificates for Moroccan travelers** — Useful for Schengen, UK, Canada, and Umrah travelers. It includes a pricing calculator and instant PDF generation. Built for embassies

- Jev: núcleo **0.90** · parcial 0.85 · mismo usuario 0.89
- Haiku: núcleo **0.85** · parcial 0.95 · mismo usuario 0.90

mi veredicto: núcleo / parcial / no

---

## 10. positivo · `syn-4770645-claude` (synthetic) · rank 16

**Idea:** Is there an app that lets me see what's happening at a bar, park or venue right now, so I can check the crowd before I go?

**Candidato:** `show_hn:4770645` https://itunes.apple.com/us/app/live-vibe/id564543684?mt=8&ign-mpt=uo%3D4  
**Live Vibe** — Live Vibe app allows you to get a live perspective of any place in real time.

- Jev: núcleo **0.82** · parcial 0.72 · mismo usuario 0.89
- Haiku: núcleo **0.75** · parcial 0.85 · mismo usuario 0.80

mi veredicto: núcleo / parcial / no

---

## 11. positivo · `syn-13551907` (synthetic) · rank 25

**Idea:** I'm looking for an unbiased, continuously maintained record of what states and public authorities across the globe have decided and done.

**Candidato:** `show_hn:13551907` https://github.com/govtra/govtracker-data/blob/master/README.md  
**Up to date list of political decisions around the world** — GovTracker.org data
GovTracker.org // Sources on Github
Our goal is to keep track, while keeping a neutral point of view, of the decisions and steps taken by the different governments around the world.
Additionally, for exceptional apolitical news of importance an `important` folder is created. This was originally done to report the famine in South Sudan.
Participate
All entries must contain two things: a concise description of the entry's topic and a source (primary source ideally). Additionally we appreciate if articles providing in deep analysis are added as extra.
There are two ways how to

- Jev: núcleo **0.87** · parcial 0.89 · mismo usuario 0.91
- Haiku: núcleo **0.75** · parcial 0.85 · mismo usuario 0.80

mi veredicto: núcleo / parcial / no

---

## 12. positivo · `syn-33480679` (synthetic) · rank 8

**Idea:** I need quick personalized clothing

**Candidato:** `show_hn:33480679` https://www.1sewn.com/  
**Stable Diffusion print-on-demand apparel** — Hey HN,
Obviously we are experiencing a surge of stable-diffusion based apps at the moment, but I have yet to see anyone try and map the outputs onto actual physical products that can be delivered to your door.
I wanted to make it easy to:
- pick an artistic style
- hit 'record' and speak into your phone / tablet / desktop or whatever, and describe the kind of design you want your clothing to have (since speaking is more spontaneous that typing)
- swipe among a variety of mockups (t-shirts, hoodies etc.) featuring your design, and order it to your door with the click of a button
The product is

- Jev: núcleo **0.92** · parcial 0.91 · mismo usuario 0.90
- Haiku: núcleo **0.85** · parcial 0.95 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 13. positivo · `syn-4770645` (synthetic) · rank 98

**Idea:** I want to take a look at some place in real time

**Candidato:** `show_hn:4770645` https://itunes.apple.com/us/app/live-vibe/id564543684?mt=8&ign-mpt=uo%3D4  
**Live Vibe** — Live Vibe app allows you to get a live perspective of any place in real time.

- Jev: núcleo **0.92** · parcial 0.81 · mismo usuario 0.95
- Haiku: núcleo **0.85** · parcial 0.95 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 14. positivo · `syn-13406648` (synthetic) · rank 221

**Idea:** need to see graphics in the terminal while coding

**Candidato:** `show_hn:13406648` https://github.com/daleroberts/itermplot  
**Backend for Matplotlib so you can plot directly in your terminal** — An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.
Topics: command-line, iterm2, matplotlib, plot, python, visualization
itermplot
An awesome iTerm2 backend for Matplotlib, so you can plot directly in your terminal.
The above is achieved with zero modifications to your Python script. For example, the above
plots are generated with the following code:
Note: you need to run `plt.show()` to display the figure.
Reverse video
If you use a dark background in your terminal, you can enable "reverse video" mode by adding this to your `.profile`:
TMUX support
itermplot 

- Jev: núcleo **0.91** · parcial 0.93 · mismo usuario 0.95
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.88

mi veredicto: núcleo / parcial / no

---

## 15. positivo · `syn-18642575` (synthetic) · rank 26

**Idea:** I want a native editor and REPL for writing Lisp programs on a PC without a Unix compatibility layer.

**Candidato:** `show_hn:18642575` https://github.com/sharplispers/cormanlisp/issues/40  
**The upcoming release of Corman Lisp 3.1** — Corman Lisp
Topics: common-lisp, ide
Corman Lisp
This is the open-source source release of Corman Lisp. The canonical
home of this release is https://github.com/sharplispers/cormanlisp.
From the Corman Lisp 'Features' page:
Corman Lisp is a Common Lisp development environment for Microsoft Windows operating systems running on Intel platforms. Corman Lisp consists of a Common Lisp native code compiler for Intel processors, 80x86 assembler and disassembler, incremental linker and multi-window text editor. It requires a system running a Microsoft Windows operating system (such as Windows XP, Wind

- Jev: núcleo **0.77** · parcial 0.87 · mismo usuario 0.89
- Haiku: núcleo **0.85** · parcial 0.95 · mismo usuario 0.90

mi veredicto: núcleo / parcial / no

---

## 16. near-miss · `real-fbe3c4c2` (real) · rank 1

**Idea:** A way to automatically test, benchmark and certify reusable agent skills or prompt packages, checking that they actually work, are safe, and don't break when the underlying model changes. Essentially continuous integration and security auditing for distributable agent skill artifacts.

**Candidato:** `show_hn:47270208` https://agents.zalor.ai/  
**Automated Testing for AI Agents** — Hi Hacker News! We're launching Zalor, an agent testing platform.
Agents often break when you tweak system prompts, swap models, or add tools. Zalor automatically generates test scenarios and evaluates your agent so you know it's reliable before deploying to production.
We currently support the OpenAI Agents SDK and are onboarding other frameworks. A GitHub integration is coming so you can get feedback on every update.
Looking forward to hearing feedback from people building agents.

- Jev: núcleo **0.80** · parcial 0.83 · mismo usuario 0.81
- Haiku: núcleo **0.75** · parcial 0.85 · mismo usuario 0.80

mi veredicto: núcleo / parcial / no

---

## 17. near-miss · `real-fbe3c4c2` (real) · rank 2

**Idea:** A way to automatically test, benchmark and certify reusable agent skills or prompt packages, checking that they actually work, are safe, and don't break when the underlying model changes. Essentially continuous integration and security auditing for distributable agent skill artifacts.

**Candidato:** `github:FrancyJGLisboa/agent-skills-platform` https://github.com/FrancyJGLisboa/agent-skills-platform  
**agent-skills-platform** — Build tested agent skills and govern their lifecycle through a user-defined marketplace: evidence, discovery, updates, rollback, quarantine, and 17-platform distribution.
Topics: agent-skills, ai-agents, claude-code, codex, cursor, developer-tools, evals, github-copilot, governance, skill-marketplace
Agent Skills Platform
Turn a real workflow into a tested, installable agent skill—then publish it safely to your team.**
Website ·
Installation ·
Worker runbook ·
Team marketplace ·
Product scope
Agent Skills Platform turns the way people already work into tested, installable agent
skills. Give it

- Jev: núcleo **0.79** · parcial 0.85 · mismo usuario 0.75
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.85

mi veredicto: núcleo / parcial / no

---

## 18. near-miss · `real-fbe3c4c2` (real) · rank 3

**Idea:** A way to automatically test, benchmark and certify reusable agent skills or prompt packages, checking that they actually work, are safe, and don't break when the underlying model changes. Essentially continuous integration and security auditing for distributable agent skill artifacts.

**Candidato:** `show_hn:48898280` https://www.agentsproof.dev/  
**AgentsProof – a small project for testing AI agents** — I built AgentsProof as a learning side-project to better understand agent evals and observability. It lets me trace runs, create eval cases, and see where an agent succeeds or fails.
Nothing fancy but it does creates publicly shareable reports for your agent runs

- Jev: núcleo **0.29** · parcial 0.72 · mismo usuario 0.31
- Haiku: núcleo **0.35** · parcial 0.62 · mismo usuario 0.55

mi veredicto: núcleo / parcial / no

---

## 19. ⚠️ near-miss · `real-ecad36a5` (real) · rank 1

**Idea:** I need a layer that decides, per task, which language model to use based on difficulty and price — cheap models for routine work, expensive ones for hard reasoning — while enforcing a spending budget per project.

**Candidato:** `github:zscole/model-hierarchy-skill` https://github.com/zscole/model-hierarchy-skill  
**model-hierarchy-skill** — OpenClaw skill for cost-optimized model routing based on task complexity
model-hierarchy-skill
Cost-optimize AI agent operations by routing tasks to appropriate models based on complexity.
The Problem
Most AI agents run everything on expensive models. But 80% of agent tasks are routine: file reads, status checks, formatting, simple Q&A. You're paying $15-75/M tokens for work that $0.14/M tokens handles fine.
The Solution
A skill that teaches agents to classify tasks and route them to the cheapest model that can handle them:
| Task Type | Model Tier | Cost | Examples |
|-----------|------------

- Jev: núcleo **0.59** · parcial 0.81 · mismo usuario 0.74
- Haiku: núcleo **0.92** · parcial 0.95 · mismo usuario 0.85

mi veredicto: núcleo / parcial / no

---

## 20. near-miss · `real-ecad36a5` (real) · rank 2

**Idea:** I need a layer that decides, per task, which language model to use based on difficulty and price — cheap models for routine work, expensive ones for hard reasoning — while enforcing a spending budget per project.

**Candidato:** `show_hn:44454454` https://soloagents.directoryfa.st  
**AI Agents That Work as Hard as You Do** — 

- Jev: núcleo **0.07** · parcial 0.06 · mismo usuario 0.32
- Haiku: núcleo **0.35** · parcial 0.55 · mismo usuario 0.40

mi veredicto: núcleo / parcial / no

---

## 21. near-miss · `real-ecad36a5` (real) · rank 3

**Idea:** I need a layer that decides, per task, which language model to use based on difficulty and price — cheap models for routine work, expensive ones for hard reasoning — while enforcing a spending budget per project.

**Candidato:** `github:adamwlarson/RooCodeMicroManager` https://github.com/adamwlarson/RooCodeMicroManager  
**RooCodeMicroManager** — A local coding team for RooCode
RooCode MicroManager
Motivation
In the evolving landscape of AI development, where free access to powerful models is becoming increasingly limited, cost optimization becomes crucial. RooCode MicroManager addresses this challenge through intelligent task orchestration:
Cost-Efficient Workflow**: Instead of using the most expensive model for every task, MicroManager intelligently delegates work to appropriately sized models based on task complexity
Model Optimization**: Each specialized mode is configured with the most cost-effective model that can handle its spec

- Jev: núcleo **0.62** · parcial 0.81 · mismo usuario 0.69
- Haiku: núcleo **0.85** · parcial 0.90 · mismo usuario 0.70

mi veredicto: núcleo / parcial / no

---

## 22. near-miss · `real-7c597ec1` (real) · rank 1

**Idea:** I need shared infrastructure for managing AI evaluation datasets themselves "" a layer that lets you compose benchmarks from parts, version them, detect duplicate or overlapping test items across suites, and track when a benchmark becomes saturated or obsolete. Right now every new evaluation is a one-off that doesn't build on the ones before it.

**Candidato:** `github:evaleval/every_eval_ever` https://github.com/evaleval/every_eval_ever  
**every_eval_ever** — Every Eval Ever is a shared schema and crowdsourced eval database. It defines a standardized metadata format for storing AI evaluation results — from leaderboard scrapes and research papers to local evaluation runs — so that results from different frameworks can be compared, reproduced, and reused.
Topics: agent-evaluation, ai-evaluation, evaluations, infra, llm-evaluation
Every Eval Ever
EvalEval Coalition — "We are a researcher community developing scientifically grounded research outputs and robust deployment infrastructure for broader impact evaluations."
📄 **Paper (arXiv:2606.14516)**
Eve

- Jev: núcleo **0.17** · parcial 0.34 · mismo usuario 0.45
- Haiku: núcleo **0.25** · parcial 0.60 · mismo usuario 0.70

mi veredicto: núcleo / parcial / no

---

## 23. near-miss · `real-7c597ec1` (real) · rank 2

**Idea:** I need shared infrastructure for managing AI evaluation datasets themselves "" a layer that lets you compose benchmarks from parts, version them, detect duplicate or overlapping test items across suites, and track when a benchmark becomes saturated or obsolete. Right now every new evaluation is a one-off that doesn't build on the ones before it.

**Candidato:** `show_hn:31742441` https://marketplace.visualstudio.com/items?itemName=Iterative.dvc  
**Extension for VS Code to track ML experiments** — Hi everyone, I’m one of the maintainers of Data Version Control – DVC (https://dvc.org) – a popular open source tool for ML engineers. We’ve been building DVC for 5 years with a goal to bring software engineering best practices (version control, CI, and GitOps) to MLOps.
Today, VS Code is the fastest growing IDE among data scientists. That’s why we decided to bring DVC’s functionality natively to VS Code without any infrastructure overhead. We spent the past year building the DVC extension and I’m glad to present it to the community today.
In a nutshell, what DVC provides right from VS Code: 


- Jev: núcleo **0.10** · parcial 0.27 · mismo usuario 0.36
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.70

mi veredicto: núcleo / parcial / no

---

## 24. near-miss · `real-7c597ec1` (real) · rank 3

**Idea:** I need shared infrastructure for managing AI evaluation datasets themselves "" a layer that lets you compose benchmarks from parts, version them, detect duplicate or overlapping test items across suites, and track when a benchmark becomes saturated or obsolete. Right now every new evaluation is a one-off that doesn't build on the ones before it.

**Candidato:** `show_hn:38893298` https://github.com/DeployQL/retri-evals  
**Retrieval Evaluations Framework** — Hey all,
Matt here. We've been working on building retrieval pipelines for LLMs, and like many others we questioned how changes to our pipeline (e.g. chunking, cleaning) would affect the overall outcome.
We also faced a problem of what data to evaluate against. MTEB datasets are used in the literature, but we found it difficult to use our existing processing pipelines with it. We also didn't want to manually label a dataset, because it would be difficult to hand-label a representative dataset.
Retri-evals is hoping to solve these problems. We pulled out our MTEB abstractions that let us evalua

- Jev: núcleo **0.15** · parcial 0.35 · mismo usuario 0.37
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.45

mi veredicto: núcleo / parcial / no

---

## 25. near-miss · `real-8b190bdc` (real) · rank 1

**Idea:** I need a runtime layer that sits between an LLM's curation or judging output and the end user, scoring each response for ideological or framing skew and then rebalancing or flagging it before delivery. Existing work only measures bias offline; I want an enforceable mitigation component in production.

**Candidato:** `show_hn:47417594` https://news.ycombinator.com/item?id=47417594  
**SkeptAI – adversarial reasoning agent that challenges LLM outputs** — I built this after Claude cited an API feature that doesn't exist in a work analysis that I almost forwarded to a client. CRIT (the custom framework that I built behind it) runs four structured adversarial passes on any LLM output and delivers a scored verdict. Cross-model critique (Claude output gets challenged by GPT-4o and vice versa) to prevent self-referential bias. Free playground, open source framework. Think of it as a "Digital Devil's Advocate". Check it out and let me know what you think.
skeptai.dev | github.com/datonpope/skeptai

- Jev: núcleo **0.30** · parcial 0.50 · mismo usuario 0.37
- Haiku: núcleo **0.35** · parcial 0.62 · mismo usuario 0.45

mi veredicto: núcleo / parcial / no

---

## 26. near-miss · `real-8b190bdc` (real) · rank 2

**Idea:** I need a runtime layer that sits between an LLM's curation or judging output and the end user, scoring each response for ideological or framing skew and then rebalancing or flagging it before delivery. Existing work only measures bias offline; I want an enforceable mitigation component in production.

**Candidato:** `github:conversationai/unintended-ml-bias-analysis` https://github.com/conversationai/unintended-ml-bias-analysis  
**unintended-ml-bias-analysis** — Unintended ML Bias Analysis
This project was archived in Feb 2026 and has not been updated in several years.
This repository contains the Sentence Templates datasets we use to evaluate and
mitigate unintended machine learning bias in Perspective
API. See our accompanying blog post to learn more about how we created these datasets.
This work is part of the Conversation AI
project, a collaborative research effort exploring ML as a tool for better
discussions online.
NOTE: We moved outdated scripts, notebooks, and other resources to the
archive subdirectory. We no longer maintain those resources,

- Jev: núcleo **0.06** · parcial 0.11 · mismo usuario 0.13
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.30

mi veredicto: núcleo / parcial / no

---

## 27. near-miss · `real-8b190bdc` (real) · rank 3

**Idea:** I need a runtime layer that sits between an LLM's curation or judging output and the end user, scoring each response for ideological or framing skew and then rebalancing or flagging it before delivery. Existing work only measures bias offline; I want an enforceable mitigation component in production.

**Candidato:** `github:princeton-nlp/QuRating` https://github.com/princeton-nlp/QuRating  
**QuRating** — [ICML 2024] Selecting High-Quality Data for Training Language Models
QuRating: Selecting High-Quality Data for Training Language Models
This is the official repository for our ICML'24 paper QuRating: Selecting High-Quality Data for Training Language Models
and contains code for (1) collecting LLM quality judgments (2) training QuRater models (3) selecting and sampling data (4) training LMs (5) reproducing the analysis in the paper *(in-progress)*.
Guidance on Responsible Use**
In the paper, we document various types of bias that are present in the quality ratings/QuRater model (biases related 

- Jev: núcleo **0.07** · parcial 0.14 · mismo usuario 0.10
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 28. near-miss · `real-197bf4f9` (real) · rank 1

**Idea:** I want one tool that installs and runs a whole set of self-hosted applications together, automatically wiring them to a shared login, automated backups, and monitoring, with a single dashboard across all of them. Today each app has to be deployed and integrated with single sign-on by hand.

**Candidato:** `show_hn:42793327` https://openalternative.co/self-hosted  
**A collection of 150 self-hosted alternatives to popular software** — Self-hosting involves running and managing applications on your own server(s) rather than utilizing SaaS providers. Find services and web applications that…

- Jev: núcleo **0.04** · parcial 0.06 · mismo usuario 0.37
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.70

mi veredicto: núcleo / parcial / no

---

## 29. near-miss · `real-197bf4f9` (real) · rank 2

**Idea:** I want one tool that installs and runs a whole set of self-hosted applications together, automatically wiring them to a shared login, automated backups, and monitoring, with a single dashboard across all of them. Today each app has to be deployed and integrated with single sign-on by hand.

**Candidato:** `show_hn:46597062` https://github.com/zdunecki/selfhosted  
**Selfhosted – One click self hosted apps** — SelfHosted - Self-Hosted App Installer
⚠️ **Early Stage**: This project is in very early development. Features may be incomplete, APIs may change, and there may be bugs. Use at your own risk.
A modern tool to deploy self-hosted applications to multiple cloud providers with a single click. Features a beautiful web-based wizard UI and native desktop app wrapper.
Features
Multi-provider support**: Deploy to DigitalOcean, Scaleway, UpCloud, Vultr, and Google Cloud Platform
Multi-app support**: Deploy analytics, session replay, and more
Automatic**: DNS setup, SSL certificates, app installation
No 

- Jev: núcleo **0.17** · parcial 0.61 · mismo usuario 0.46
- Haiku: núcleo **0.35** · parcial 0.55 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 30. near-miss · `real-197bf4f9` (real) · rank 3

**Idea:** I want one tool that installs and runs a whole set of self-hosted applications together, automatically wiring them to a shared login, automated backups, and monitoring, with a single dashboard across all of them. Today each app has to be deployed and integrated with single sign-on by hand.

**Candidato:** `github:openrundev/openrun` https://github.com/openrundev/openrun  
**openrun** — Deployment platform for teams to deploy internal tools. Deploy web apps declaratively, on a single-node or on Kubernetes, with OIDC/SAML auth and RBAC.
Topics: appserver, containers, deployment, devops-tools, docker, golang, htmx, internal-tools, kubernetes, kubernetes-deployment, openrun, self-hosted, starlark
Open-source, self-hosted GitOps platform for deploying web apps and internal tools to Docker or Kubernetes. Declarative deployments, SSO, RBAC, database service bindings, SQLite backups to S3 and scale-to-zero. 
Menu
Overview
Ways To Manage Apps
FAQ
Architecture Overview
Database Servic

- Jev: núcleo **0.68** · parcial 0.89 · mismo usuario 0.77
- Haiku: núcleo **0.72** · parcial 0.85 · mismo usuario 0.78

mi veredicto: núcleo / parcial / no

---

## 31. rank 200-1000 · `syn-17181315` (synthetic) · rank 777

**Idea:** I need to see if different microservices can be combined.

**Candidato:** `github:baranbartu/microservices-with-fastapi` https://github.com/baranbartu/microservices-with-fastapi  
**microservices-with-fastapi** — Microservices, API Gateway, Authentication with FastAPI, non-blocking i/o
Microservices, API Gateway, Authentication with FastAPI, non-blocking i/o
This repo is composed of a bunch of small microservices considering API gateway approach
Expected number of microservices was two, but considering that services
should not create dependency on each other to prevent SPOF, also to prevent duplicate codes,
I decided to put one API gateway in front that does JWT authentication for both services
which I am inspired by Netflix/Zuul
We have 3 services including gateway.
Only gateway can access internal mi

- Jev: núcleo **0.82** · parcial 0.88 · mismo usuario 0.80
- Haiku: núcleo **0.75** · parcial 0.90 · mismo usuario 0.80

mi veredicto: núcleo / parcial / no

---

## 32. rank 200-1000 · `syn-13406648-claude` (synthetic) · rank 833

**Idea:** I want my Python charts to show up right inside my command-line window when I run a script, instead of opening a separate window or saving image files.

**Candidato:** `github:microsoft/flint-chart` https://github.com/microsoft/flint-chart  
**flint-chart** — 🪄 Flint is a visualization language that lets AI agents reliably create expressive, good-looking charts from simple, human-editable chart specs.
Topics: ai-agents, charting-library, data-visualization, mcp-server
Flint: A Visualization Language for the AI Era 
Please visit:** **Flint Project Site** | **Visual Themes** | **MCP Server Guide** | **中文主页**
Flint is a visualization intermediate language that lets **AI agents turn
simple, human-editable chart specs into expressive, polished visualizations**.
Rather than requiring agents to hardcode verbose parameters for scales, axes,
spacing, labels

- Jev: núcleo **0.08** · parcial 0.11 · mismo usuario 0.14
- Haiku: núcleo **0.15** · parcial 0.20 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 33. rank 200-1000 · `syn-17800530` (synthetic) · rank 708

**Idea:** I need to run computations on encrypted data without decrypting it, fast enough by using the GPU from Python.

**Candidato:** `github:Billy1900/Awesome-Differential-Privacy` https://github.com/Billy1900/Awesome-Differential-Privacy  
**Awesome-Differential-Privacy** — Differential private machine learning
Topics: differential-privacies, differential-privacy, differential-privacy-learning, differentially-private, dpsgd, privacy-preserving, survey
Differential-Privacy
Differential privacy learning and integration
1. Intuitive explanation
Differential privacy explaining
Differential Privacy - Simply Explained 
Differential Privacy A Primer for a Non-technical Audience
Differential privacy introduction Reading (not so much mathematics, but intuition)
Laplacian Noisy Counting mechanism illustratioin
2. Academic paper
2.1 Survey
The Algorithm foundation of Differ

- Jev: núcleo **0.03** · parcial 0.05 · mismo usuario 0.15
- Haiku: núcleo **0.05** · parcial 0.08 · mismo usuario 0.15

mi veredicto: núcleo / parcial / no

---

## 34. rank 200-1000 · `real-ecad36a5` (real) · rank 637

**Idea:** I need a layer that decides, per task, which language model to use based on difficulty and price — cheap models for routine work, expensive ones for hard reasoning — while enforcing a spending budget per project.

**Candidato:** `show_hn:41487944` https://chromewebstore.google.com/detail/etenus-automate-tasks-wit/cjofcncnolkimapbjiajldocanlljfdn  
**Automate Your to Do List with AI Agent** — 

- Jev: núcleo **0.06** · parcial 0.07 · mismo usuario 0.15
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.30

mi veredicto: núcleo / parcial / no

---

## 35. rank 200-1000 · `syn-36030350` (synthetic) · rank 676

**Idea:** Very long comment sections on a tech forum are hard to follow on my phone; I want an app that lets me go through one reply chain at a time.

**Candidato:** `show_hn:47901504` https://github.com/gerritsxd/chatforge  
**Chatforge – drag two local LLM conversations together to merge context** — CHATFORGE
Drag two conversations together. The model remembers everything.**
A local AI chat interface where conversations are living objects — merge them, compile them into weights, and build a model that compounds knowledge over time. Fully local, fully yours, nothing leaves your machine.
What makes it different
| Feature | CHATFORGE | typical local chat UI |
|---|---|---|
| Drag-to-merge conversations | ✅ | ❌ |
| Persistent cross-session memory | ✅ | ❌ |
| Auto fact extraction per exchange | ✅ | ❌ |
| Runs 100% locally on your GPU | ✅ | sometimes |
| LoRA compilation *(coming)* | 🔜 | ❌ |
Co

- Jev: núcleo **0.05** · parcial 0.06 · mismo usuario 0.08
- Haiku: núcleo **0.05** · parcial 0.10 · mismo usuario 0.15

mi veredicto: núcleo / parcial / no

---

## 36. rank 200-1000 · `real-6eb5b382` (real) · rank 664

**Idea:** I need a way to give autonomous AI agents credentials and identities that are narrowly scoped, revocable, and fully audited, so an agent can call APIs and cloud services without ever seeing or leaking the raw secrets.

**Candidato:** `show_hn:48323417` https://www.integuru.com  
**Integuru – Integrate with platforms via the source code** — Hey HN! We’re Alan and Richard from Integuru (YC W24). We generate fast, reliable integrations for platforms lacking official APIs. About 2 years ago, we released the first agent that reverse-engineers network traffic to build integrations (https://github.com/Integuru-AI/Integuru). Since then, we’ve developed a new approach to reverse-engineer platforms’ source code directly. This solution also includes authentication support. Here’s a demo: https://youtu.be/4l2L8fILC2g?si=nbWbDiFrWZIWRPM7.
Many AI products need to integrate with web apps, but platforms often lack official APIs. So far, there 

- Jev: núcleo **0.10** · parcial 0.19 · mismo usuario 0.20
- Haiku: núcleo **0.15** · parcial 0.10 · mismo usuario 0.35

mi veredicto: núcleo / parcial / no

---

## 37. rank 200-1000 · `syn-8757899` (synthetic) · rank 506

**Idea:** I'm looking for an extremely slim cover for my Apple phone that protects it without adding bulk.

**Candidato:** `show_hn:30470578` https://javier.xyz/blog/turn-a-kindle-into-a-picture-frame  
**Make ebooks with custom covers to use as lockscreen images on a Kindle** — 

- Jev: núcleo **0.01** · parcial 0.01 · mismo usuario 0.02
- Haiku: núcleo **0.05** · parcial 0.02 · mismo usuario 0.00

mi veredicto: núcleo / parcial / no

---

## 38. rank 200-1000 · `syn-21462993` (synthetic) · rank 384

**Idea:** I need to keep tabs on many moving vehicles or animals through video footage in Python, choosing between different neural detectors.

**Candidato:** `github:chenhaoxing/Awesome-AI-Generated-Video-Detection` https://github.com/chenhaoxing/Awesome-AI-Generated-Video-Detection  
**Awesome-AI-Generated-Video-Detection** — ✨✨Latest Papers on AI-Generated Video Detection and Related Areas
Awesome-AI-Generated-Video-Detection
✨✨Latest Papers on AI-Generated Video Detection and Related Areas
Contents
Survey
Dataset
Competition
Papers
Survey
| Title | Venue | Year |
| :----------------------------------------------------------- | :------------: | :--: |
| A Survey on Deepfake Video Detection | IET Biometrics | 2021 |
Dataset
| Dataset | Title | Venue | Year | Task |
| :----------- | :----------------------------------------------------------- | :-------------------------------: | :--: | :------: |
| ComGenVid | Trai

- Jev: núcleo **0.03** · parcial 0.03 · mismo usuario 0.05
- Haiku: núcleo **0.05** · parcial 0.05 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 39. rank 200-1000 · `syn-21462993` (synthetic) · rank 283

**Idea:** I need to keep tabs on many moving vehicles or animals through video footage in Python, choosing between different neural detectors.

**Candidato:** `github:avs-abhishek123/Computer-Vision-Projects` https://github.com/avs-abhishek123/Computer-Vision-Projects  
**Computer-Vision-Projects** — All Computer Vision Projects - Beginner to Advanced
Topics: artificial-intelligence, computer-vision, deep-learning, object-detection, object-recognition, object-tracking, opencv, pillow, python3
Computer Vision Projects
keep supporting this repository with stars that will encourage me to add more!*
Star History
| Project Name | Contents | Link |
|---|---|---|
| Blur_detection | Blur_detection_using_laplacian.py | Link |
| boundingbox_draw | solid_blue_rectangle_on_a_whitebg.py | Link |
| Cartooning-an-Image-using-Machine-Learning | cartoonising_an_image_using_ML.ipynb | Link |
| | README.md |

- Jev: núcleo **0.29** · parcial 0.67 · mismo usuario 0.70
- Haiku: núcleo **0.25** · parcial 0.45 · mismo usuario 0.75

mi veredicto: núcleo / parcial / no

---

## 40. rank 200-1000 · `real-7c597ec1` (real) · rank 507

**Idea:** I need shared infrastructure for managing AI evaluation datasets themselves "" a layer that lets you compose benchmarks from parts, version them, detect duplicate or overlapping test items across suites, and track when a benchmark becomes saturated or obsolete. Right now every new evaluation is a one-off that doesn't build on the ones before it.

**Candidato:** `github:epuerta9/kitchenai` https://github.com/epuerta9/kitchenai  
**kitchenai** — Open Source LLMOps tool for AI teams
Topics: ai, devops, devops-tools, llm, llm-inference, llmops, open-source, testing-tools, tools
KitchenAI
KitchenAI** is a control plane for AI implementations — designed to bridge the gap between application developers and AI teams. Our platform simplifies AI integration with a loosely coupled, modular architecture that delivers production-grade reliability while letting your teams focus on what they do best.
🚀 Quick Start
Explore Our Interactive Playground:** 
Try KitchenAI in Action
Take a Guided Tour:** 
Watch the Guided Tour
🌟 What Makes KitchenAI Uniq

- Jev: núcleo **0.09** · parcial 0.11 · mismo usuario 0.29
- Haiku: núcleo **0.10** · parcial 0.15 · mismo usuario 0.30

mi veredicto: núcleo / parcial / no

---

## 41. azar top-1000 · `real-197bf4f9` (real) · rank 507

**Idea:** I want one tool that installs and runs a whole set of self-hosted applications together, automatically wiring them to a shared login, automated backups, and monitoring, with a single dashboard across all of them. Today each app has to be deployed and integrated with single sign-on by hand.

**Candidato:** `show_hn:46304050` https://github.com/pgEdge/pgedge-postgres-mcp  
**Open-Source Postgres MCP Server and Natural Language Agent** — pgEdge MCP Server.  A PostgreSQL MCP server with a Natural Language Agent CLI and Web UI.
Topics: ai, llm, mcp, postgres, postgresql, server
pgEdge Postgres MCP Server and Natural Language Agent
About the pgEdge Postgres MCP Server
pgEdge Postgres MCP Server
Choosing the Right Solution
Best Practices - Querying the Server
Installing the MCP Server
Quick Start
Quickstart Demo with Northwind
Deploying on Docker
Deploying from Source
Testing the MCP Server Deployment
Configuring the MCP Server
Specifying Configuration Preferences
Using Environment Variables to Specify Options
Including Provider E

- Jev: núcleo **0.03** · parcial 0.08 · mismo usuario 0.09
- Haiku: núcleo **0.05** · parcial 0.08 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 42. azar top-1000 · `syn-41298789` (synthetic) · rank 747

**Idea:** I want visitors' entries on my site's contact fields to arrive by email without me running any server code.

**Candidato:** `show_hn:40270537` https://mly.fyi/docs/introduction  
**I made an open-source tool to send and monitor emails** — 

- Jev: núcleo **0.39** · parcial 0.58 · mismo usuario 0.49
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.30

mi veredicto: núcleo / parcial / no

---

## 43. azar top-1000 · `syn-2320614` (synthetic) · rank 295

**Idea:** I want to sort my contacts into separate friend groups and share posts only with specific groups, instead of broadcasting to everyone.

**Candidato:** `show_hn:4157553` http://foundd.com/groups/landing/sggKBy9OSX/4fce73537d1e03e46e227ac2  
**Movie Recommendations for several people to watch together** — We've been working on a custom engineered collaborative filtering algorithm not only to recommend movies for one person but for several to watch together, at the same time.
We're still in closed beta but would love to get feedback before launching.

- Jev: núcleo **0.03** · parcial 0.03 · mismo usuario 0.14
- Haiku: núcleo **0.05** · parcial 0.02 · mismo usuario 0.15

mi veredicto: núcleo / parcial / no

---

## 44. azar top-1000 · `syn-17181315-claude` (synthetic) · rank 121

**Idea:** Looking for a sample codebase showing how to split a server application into small independent pieces in different programming languages that call each other and run on a local container cluster.

**Candidato:** `github:microsoft-foundry/Foundry-Local-Lab` https://github.com/microsoft-foundry/Foundry-Local-Lab  
**Foundry-Local-Lab** — Microsoft Foundry Local - Workshop - Build AI apps locally with Foundry Local - RAG, agents, and multi-agent workflows in Python, JS, and C#. No cloud required.
Topics: agent, csharp, foundrylocal, javascript, microsoft, microsoftagentframework, python, rag
Foundry Local Workshop - Build AI Apps On-Device
A hands-on workshop for running language models on your own machine and building intelligent applications with Foundry Local and the Microsoft Agent Framework.
What is Foundry Local?** Foundry Local is a lightweight runtime that lets you download, manage, and serve language models entirely on

- Jev: núcleo **0.21** · parcial 0.28 · mismo usuario 0.25
- Haiku: núcleo **0.15** · parcial 0.20 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 45. azar top-1000 · `real-25a4c842` (real) · rank 429

**Idea:** I need production-grade serving infrastructure built specifically for diffusion models — a runtime that batches requests across denoising steps, caches intermediate results, and schedules work in a hardware-aware way, the way existing high-throughput text-generation servers do for language models.

**Candidato:** `github:mosheman5/DNP` https://github.com/mosheman5/DNP  
**DNP** — Audio Denoising with Deep Network Priors
DNP
Speech Denoising by Accumulating Per-Frequency Modeling Fluctuations
This repository provides a PyTorch implementation of "Speech Denoising by Accumulating Per-Frequency Modeling Fluctuations" (paper)
The method trains on noisy audio signal and provides a the clean underlying signal. **Comparison with traditional unsupervised methods can be found here**
The method is completely unsupervised and only trains on the specific audio clip that is being denoised.
The algorithm is based on the observation that modeling noise in the signal is harder than a c

- Jev: núcleo **0.03** · parcial 0.04 · mismo usuario 0.04
- Haiku: núcleo **0.05** · parcial 0.02 · mismo usuario 0.05

mi veredicto: núcleo / parcial / no

---

## 46. azar top-1000 · `syn-2774322` (synthetic) · rank 776

**Idea:** I lose too much time checking a tech news aggregator all day; I'd rather get just the top stories once a day by email.

**Candidato:** `show_hn:39333086` https://ignition-news.com/  
**A newsletter covering nuclear energy** — Hi everyone; longtime HN user here. My co-founder and I launched Payload three years ago. It's now the leading B2B media company covering the space industry.
This week we launched Ignition, a media company covering the business and policy of nuclear energy. We are starting with a twice-weekly free newsletter that takes less than 5 minutes to read.
The first edition goes out on February 22nd.
Me + my cofounder started Payload last year to cover the space industry, from seed round to SPAC and beyond. Our first (and primary) product is a daily newsletter covering the business and policy of space.

- Jev: núcleo **0.42** · parcial 0.67 · mismo usuario 0.42
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.40

mi veredicto: núcleo / parcial / no

---

## 47. azar top-1000 · `syn-41298789` (synthetic) · rank 156

**Idea:** I want visitors' entries on my site's contact fields to arrive by email without me running any server code.

**Candidato:** `show_hn:5638479` https://grouptalent.com/filter/  
**An Inbox for Recruiting Spam** — 

- Jev: núcleo **0.17** · parcial 0.14 · mismo usuario 0.20
- Haiku: núcleo **0.15** · parcial 0.20 · mismo usuario 0.05

mi veredicto: núcleo / parcial / no

---

## 48. azar top-1000 · `syn-41599941` (synthetic) · rank 432

**Idea:** I want to see what the newest iPhone sells for in different countries, converted into my own money, to find where it's cheapest to buy.

**Candidato:** `show_hn:2779046` http://locational.net  
**Locational - Take full advantage of your iPhone's GPS today** — 

- Jev: núcleo **0.03** · parcial 0.04 · mismo usuario 0.13
- Haiku: núcleo **0.05** · parcial 0.05 · mismo usuario 0.10

mi veredicto: núcleo / parcial / no

---

## 49. azar top-1000 · `syn-7034317-claude` (synthetic) · rank 986

**Idea:** I want a simple web tool where coworkers can pull data with lookup commands, save and pass them around, and also explore spreadsheet files, with an AI helper suggesting code.

**Candidato:** `show_hn:44523409` https://www.browseros.com/  
**Open source alternative to Perplexity Comet** — Hey HN, we're a YC startup building an open-source, privacy-first alternative to Perplexity Comet.
No invite system unlike bunch of others – you can download it today from our website or GitHub: https://github.com/browseros-ai/BrowserOS
--- Why bother building an alternative? We believe browsers will become the new operating systems, where we offload much bunch of our work to AI agents. But these agents will have access to all your sensitive data – emails, docs, on top of your browser history. Open-source, privacy-first alternatives need to exist.
We're not a search or ad company, so no weird 

- Jev: núcleo **0.09** · parcial 0.17 · mismo usuario 0.17
- Haiku: núcleo **0.15** · parcial 0.25 · mismo usuario 0.20

mi veredicto: núcleo / parcial / no

---

## 50. azar top-1000 · `syn-17181315-claude` (synthetic) · rank 783

**Idea:** Looking for a sample codebase showing how to split a server application into small independent pieces in different programming languages that call each other and run on a local container cluster.

**Candidato:** `github:same7ammar/kube-composer` https://github.com/same7ammar/kube-composer  
**kube-composer** — Open-Source Kubernetes YAML Builder with Intuitive Web Interface and Dynamic Visualization for Developers and DevOps Engineers
Topics: containers, devops, kubernetes, kubernetes-deployment, yaml, yaml-processor
Kube Composer
A modern, intuitive **Kubernetes YAML generator** that simplifies deployment configuration for developers and DevOps teams.
🌐 Live Demo
🔗 Try Kube Composer Now**
Generate your first Kubernetes deployment in under 2 minutes!
🐳 Quick Start with Docker
Run Kube Composer locally in seconds:
Then open http://localhost:8080 in your browser.
🚀 Features
🎨 **Visual Deployment Edito

- Jev: núcleo **0.06** · parcial 0.12 · mismo usuario 0.27
- Haiku: núcleo **0.10** · parcial 0.15 · mismo usuario 0.20

mi veredicto: núcleo / parcial / no

---

