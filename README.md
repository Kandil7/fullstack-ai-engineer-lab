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
docs/              # architecture, decisions (ADRs), learning, product, cheat-sheets
learning-sources/  # Source-driven learning (books, repos, notebooks, official-docs)
evaluations/       # Golden cases, regressions, RAG datasets, eval reports
projects/          # Phase folders 00→07 (auth-service is the live demo)
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

## Daily Loop (6 hours)

| Block | Time | Activity                                  |
| ----- | ---- | ----------------------------------------- |
| Learn | 1h   | One topic, docs-first, AI as teacher      |
| Build | 3h   | One feature in one continuous project     |
| Review| 1h   | AI code review + debugging session        |
| Recall| 1h   | Active recall + notes + plan tomorrow     |

---

## Progress Tracker

### Workspace Build (Complete ✅)
- [x] Phase 0 — Foundations (repo skeleton, templates, prompts, registries)
- [x] Phase 1 — Core MVP (one end-to-end feature on `auth-service`)
- [x] Phase 2 — Reliability (learning workflows, source templates, tests)
- [x] Phase 3 — Scale (scaffolding scripts, repo validation, deep dives)
- [x] Phase 4 — Advanced (RAG eval harness, capstone structure, operating manual)

### Learning Journey (In Progress)
- [ ] **Phase 0 — Foundations** ← YOU ARE HERE (Months 1–3)
  - [x] Week 1 scaffold: Exercise 01 + 02 created
  - [ ] Go Tour completion
  - [ ] HTML/CSS/JS portfolio
  - [ ] Git workflow mastery
- [ ] Phase 1 — Backend (Go + PostgreSQL)
- [ ] Phase 2 — Frontend (Flutter/Next.js)
- [ ] Phase 3 — AI Fundamentals
- [ ] Phase 4 — RAG Systems
- [ ] Phase 5 — AI Agents
- [ ] Phase 6 — System Design + DevOps
- [ ] Phase 7 — Capstone (ThanaweyaGPT)

See [`ROADMAP.md`](ROADMAP.md) for the full phase breakdown.
See [`docs/product/12-month-plan.md`](docs/product/12-month-plan.md) for the 12-month timeline.

---

## Getting Started

```powershell
# 1. Bring up local infra (optional — Postgres / Redis / Qdrant)
docker compose -f infra/docker/docker-compose.yml up -d

# 2. Run the live demo service
cd projects/01-backend-go/01-auth-service
go test ./...
go run .

# 3. Create a new ADR
./infra/scripts/new-adr.ps1 "Adopt keyset pagination"
```
