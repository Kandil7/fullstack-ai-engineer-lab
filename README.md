# Full-Stack AI Engineer Lab

A **Repo-Centric Agentic Workspace** — a learning + execution + review operating system for
becoming a production-level Full-Stack AI Engineer. This is not a notes folder; it is an
engineering environment where prompts, templates, workflows, ADRs, and reviews are
versioned **engineering artifacts**.

> The "agents" here are **prompted operating modes** (markdown under `.ai/`), not runtime
> processes. Orchestration is human-led and workflow-driven.

---

## Target Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| Backend (core)   | Go (auth, users, routing, billing)           |
| AI services      | FastAPI / Python (RAG, embeddings, agents)   |
| Mobile           | Flutter                                       |
| Web dashboard    | Next.js + TypeScript                          |
| Relational DB    | PostgreSQL                                    |
| Document DB      | MongoDB                                       |
| Cache / sessions | Redis                                         |
| Vector DB        | Qdrant                                        |
| Infra            | Docker / Docker Compose                       |

---

## Learning Strategy

**Write code yourself first**, then use AI as assistant — not replacement.

- **70% build** / 20% review / 10% theory
- Use AI for: quick explanations, code review, architecture hints, boilerplate
- Don't use AI for: writing entire systems you can't explain
- Every feature flows: `plan → design → build → review → fix → reflect`
- **Golden rule:** if you can't explain the code an hour later, AI wrote it for you, not with you

See [`docs/product/learning-strategy.md`](docs/product/learning-strategy.md) for the complete 5-axis resource system.
See [`docs/product/ai-learning-operating-manual.md`](docs/product/ai-learning-operating-manual.md) for the complete AI agent usage guide.

---

## Repository Map

```text
.ai/               # Prompt + workflow system (the "brain")
  prompts/         # system, roles, tasks, critics, repair
  workflows/       # feature, debugging, learning, architecture, evaluation
templates/         # Standardized artifact templates (ADR, review, plan, ...)
registries/        # YAML inventories: prompts, workflows, templates, decisions, skills
docs/
  roadmap/         # active-track-10-week (PLAN OF RECORD), milestones, dashboard
  decisions/       # ADRs
  reference/       # LLM production architecture, clean code, ML map, interviews
  learning/        # paths, deep-dives, daily-logs, source-summaries
  tracking/        # current-focus — what to work on right now
  plan/archive/    # superseded plans, kept for provenance
  product/         # workspace-goals, scope, feature-priorities, learning-strategy
  cheat-sheets/    # git, docker, postgres, qdrant, prompt-design
learning-sources/  # Source-driven learning (books, repos, notebooks, official-docs)
evaluations/       # Golden cases, regressions, RAG datasets, eval reports
projects/          # Phase folders 00→07 (devmate is the active project)
infra/             # docker-compose + PowerShell scripts
tests/             # repo-structure, templates, workflows, prompts validation
```

See [`docs/architecture/monorepo-structure.md`](docs/architecture/monorepo-structure.md) for the
full tree and rationale.

---

## Workflow Rules

1. **Plan before build.** Start every feature at `.ai/workflows/feature/01-plan.md`.
2. **Architecture before large implementation.** Touching system boundaries → ADR or architecture review is mandatory.
3. **Review before done.** No feature is complete without `ai-review.md`.
4. **Document every bug** in a debugging-session artifact.
5. **Deterministic paths.** Artifacts land where the workflow says — no ad-hoc locations.
6. **Registries are source of truth** for prompt/workflow/template inventory and versions.

---

## Daily Loop (5+ hours)

| Block  | Time | Activity                                      |
| ------ | ---- | --------------------------------------------- |
| Build  | 3h   | The week's deliverable — code first            |
| Learn  | 1h   | One topic, docs-first, **after** building it   |
| Review | 1h   | AI code review + debugging log                 |
| Recall | 30m  | Explain without notes + daily log + plan       |

Full cadence: [`docs/WEEKLY_PROTOCOL.md`](docs/WEEKLY_PROTOCOL.md)

---

## Active Plan

**[Active Track — 10-Week AI Engineer](docs/roadmap/active-track-10-week.md)** — adopted
2026-08-02 by [ADR-0004](docs/decisions/0004-adopt-10-week-ai-engineer-track.md).
Target: a remote AI/LLM engineering role. Vehicle: **DevMate**.

> **Governing rule:** no new lecture, glossary, or quiz file until DevMate is deployed at a
> public URL. The repo holds 6,947 lines of AI teaching material and zero running AI services;
> that ratio has to invert.

| Week | Milestone | Deliverable |
| ---- | --------- | ----------- |
| 0 | A1 | CI green + `devmate stats` CLI |
| 1 | A2 | LLM layer — streaming, traced, costed |
| 2–3 | A3 | RAG with a measured eval harness |
| 4 | A4 | **Deployed at a public URL** + SQL sprint |
| 5–6 | A5 | Agent with 4 tools + MCP server |
| 7 | A6 | Cache, guardrails, hardening |
| 8 | A7 | Portfolio — blog, README, CV |
| 9–10 | A8, A9 | 40 applications, first interview |
| 11+ | A10 | Deferred ML sprint (buffer weeks) |

**Right now:** [`docs/tracking/current-focus.md`](docs/tracking/current-focus.md) ·
**Status:** [`docs/roadmap/progress-dashboard.md`](docs/roadmap/progress-dashboard.md)

### Other tracks

| Track | Status |
| ----- | ------ |
| [Phase 2 — Athar & Baligh](docs/roadmap/phase-2-athar-baligh.md) | After A7 |
| [Long track — 12-month roadmap](docs/roadmap/master-roadmap.md) (Go, Flutter/Next.js, ThanaweyaGPT) | Deferred |

---

## Progress

### Workspace Build (Complete ✅)
- [x] Phase 0 — Foundations (repo skeleton, templates, prompts, registries)
- [x] Phase 1 — Core MVP (one end-to-end feature on `auth-service`)
- [x] Phase 2 — Reliability (learning workflows, source templates, tests)
- [x] Phase 3 — Scale (scaffolding scripts, repo validation, deep dives)
- [x] Phase 4 — Advanced (RAG eval harness, capstone structure, operating manual)

### Learning Journey
- [x] Python foundations — 1,128 files across 9 phases: core (41 topics), advanced (27), libraries (NumPy, Pandas, Matplotlib, SciPy), databases, web frameworks, DSA, ML, MLOps, GenAI
- [x] AI curriculum — 6,947+ lines across LLM APIs, RAG, agents, evaluation, safety, security (10 lectures + quizzes)
- [x] fast.ai Deep Learning track — 13 modules with lectures, exercises, and quizzes
- [ ] **A1 — CI green + first DevMate command** ← YOU ARE HERE
- [ ] A2–A10 — see the table above
- [ ] Deferred: Go, frontend, classical ML

---

## Getting Started

```powershell
# 1. Bring up local infra (Postgres / Redis / Qdrant / MongoDB / Langfuse)
docker compose -f infra/docker/docker-compose.yml up -d

# 2. Work on the active project
cd projects/04-ai-engineering/devmate

# 3. Create a new ADR
./infra/scripts/new-adr.ps1 "Adopt keyset pagination"

# 4. Start today's log
./infra/scripts/new-daily-log.ps1
```
