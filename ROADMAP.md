# Roadmap

This roadmap maps **learning phases** to **concrete projects** and to the **build phases**
defined in the architecture spec. Each "phase" is a sprint of 2–4 weeks, not a single day.

---

## Learning Phases → Projects

| Phase | Theme                          | Primary Project(s)                              |
| ----- | ------------------------------ | ----------------------------------------------- |
| 1     | Go + Backend + Databases       | `projects/01-backend-go/01-auth-service`        |
| 2     | Flutter + UI + API integration | `projects/02-frontend/flutter-app`              |
| 3     | AI fundamentals + Prompts      | `projects/04-ai-engineering/prompt-engineering` |
| 4     | RAG systems                    | `projects/04-ai-engineering/rag-system`         |
| 5     | AI agents                      | `projects/04-ai-engineering/agents`             |
| 6     | System design + DevOps         | `projects/05-system-design`, `projects/06-devops` |
| 7     | Capstone                       | `projects/07-capstone/thanaweyagpt`             |

---

## Build Phases (implementation status)

### Phase 0 — Foundations ✅
Repo skeleton, README, ROADMAP, all templates, core role prompts, registries, ADR system.
**Acceptance:** deterministic folder structure exists; first templates + prompts available.

### Phase 1 — Core MVP ✅
One end-to-end feature workflow operational on `auth-service`, with the full artifact chain:
`feature-spec → plan → architecture-review → build → ai-review → fix → reflect`.
**Acceptance:** at least one feature completed with all artifacts; no missing template in path.

### Phase 2 — Reliability
Learning workflows for docs/repo/book/notebook; source templates; prompt audits; tests for
prompts/workflows/templates.
**Acceptance:** source-learning path works on 2–3 real sources; prompt registry updated.

### Phase 3 — Scale / Optimization
Scaffolding scripts, repo validation tests, evaluation folders, improved registries,
project-level deep dives.
**Acceptance:** new project/service can be scaffolded rapidly; reviews + ADRs indexed.

### Phase 4 — Advanced Features
RAG eval harness, project-specific templates, advanced architecture docs, CI hooks, optional
local retrieval.
**Acceptance:** RAG project has eval reports + ADRs + design docs; capstone structure executable.

---

## Milestone 1 — Operational MVP Workspace

Considered done when one feature is completed inside `auth-service` with:
feature spec · plan · architecture note/ADR · implementation notes · code review ·
debug doc (if needed) · reflection/learning note. **(Reached in Phase 1.)**
