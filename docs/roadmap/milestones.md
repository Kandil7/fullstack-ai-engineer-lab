# Milestones — Full-Stack AI Engineer Lab

> Trackable milestones with evidence. Update status at weekly reviews.
> Statuses: `Planned` · `In Progress` · `Blocked` · `Review` · `Done` · `Deferred`

**Last updated:** 2026-06-26

---

## Phase 0 — Foundations (Months 1–3)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M1 | Go basics + mini exercises | Month 1 | `projects/00-core-foundations/go/` | In Progress |
| M2 | HTML/CSS/JS portfolio | Month 1 | `projects/00-core-foundations/` | Planned |
| M3 | Git workflow mastery | Month 2 | `projects/00-core-foundations/git-linux/` | Planned |
| M6 | First source-learning workflow complete | Month 3 | `docs/learning/source-summaries/` | Planned |

### M1 — Go Basics + Mini Exercises
- **Description:** Complete Go Tour + 10 mini-exercises (structs, interfaces, HTTP handlers, error handling)
- **Owner:** Mohamed
- **Acceptance:** 10 exercises in `projects/00-core-foundations/go/`, each with `_test.go` passing
- **Blocked by:** Nothing

### M2 — HTML/CSS/JS Portfolio
- **Description:** Build a 3-page portfolio site demonstrating HTML/CSS/JS fundamentals
- **Owner:** Mohamed
- **Acceptance:** Deployed site (GitHub Pages or Vercel), responsive, 3+ pages
- **Blocked by:** Nothing

### M3 — Git Workflow Mastery
- **Description:** Demonstrate feature branch → commit → PR → merge → cleanup workflow
- **Owner:** Mohamed
- **Acceptance:** 5+ PRs with clean history, conventional commits, no merge conflicts
- **Blocked by:** Nothing

### M6 — First Source-Learning Workflow
- **Description:** Complete one full source-learning cycle (read → extract → apply → document)
- **Owner:** Mohamed
- **Acceptance:** Source summary in `docs/learning/source-summaries/`, exercise applied in project
- **Blocked by:** Nothing

---

## Phase 0 → Phase 1 Bridge (Month 3)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M4 | Auth-service MVP | Month 3 | `projects/01-backend-go/01-auth-service/` | Planned |
| M5 | PostgreSQL schema design | Month 3 | `projects/03-databases/postgres-design/` | Planned |

### M4 — Auth-Service MVP
- **Description:** Go auth service with register, login, JWT middleware, and basic error handling
- **Owner:** Mohamed
- **Acceptance:** `go test ./...` passes, API endpoints working, README with usage
- **Blocked by:** M1 (Go basics)

### M5 — PostgreSQL Schema Design
- **Description:** Design and implement PostgreSQL schema for auth + users + sessions
- **Owner:** Mohamed
- **Acceptance:** Migration files, schema documented, seed data, queries tested
- **Blocked by:** Nothing (can start in parallel)

---

## Phase 1 + Phase 2 (Months 4–6)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M7 | Frontend app (Flutter or Next.js) | Month 4 | `projects/02-frontend/` | Planned |
| M8 | Full-stack integration | Month 5 | Complete app (frontend + backend) | Planned |
| M9 | Docker deployment | Month 6 | `projects/06-devops/docker/` | Planned |

### M7 — Frontend App
- **Description:** Build frontend application (Flutter mobile OR Next.js web) with API integration
- **Owner:** Mohamed
- **Acceptance:** App connects to Go backend, auth flow works, responsive UI
- **Blocked by:** M4 (Auth-service MVP)

### M8 — Full-Stack Integration
- **Description:** End-to-end flow: frontend → backend → database → response
- **Owner:** Mohamed
- **Acceptance:** User can register, login, see dashboard with real data
- **Blocked by:** M7, M4, M5

### M9 — Docker Deployment
- **Description:** Docker Compose setup for full stack (Go + Frontend + PostgreSQL + Redis)
- **Owner:** Mohamed
- **Acceptance:** `docker compose up` runs entire stack, health checks pass
- **Blocked by:** M8

---

## Phase 3 — AI Fundamentals (Month 7)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M10 | AI foundations complete | Month 7 | `projects/04-ai-engineering/` | Planned |

### M10 — AI Foundations Complete
- **Description:** Python proficiency + ML basics + prompt engineering library
- **Owner:** Mohamed
- **Acceptance:** 20+ Python scripts, prompt library with 10+ prompts, ML classifier trained
- **Blocked by:** Nothing (can start after Phase 0)

---

## Phase 4 — RAG Systems (Month 10)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M11 | RAG system working | Month 10 | `projects/04-ai-engineering/rag-system/` | Planned |

### M11 — RAG System Working
- **Description:** End-to-end RAG pipeline with evaluation
- **Owner:** Mohamed
- **Acceptance:** Ingest → chunk → embed → store → retrieve → generate, evaluation report
- **Blocked by:** M10

---

## Phase 5 — AI Agents (Month 11)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M12 | Agent system working | Month 11 | `projects/04-ai-engineering/agents/` | Planned |

### M12 — Agent System Working
- **Description:** Agent with 3+ tools, multi-step reasoning, error handling
- **Owner:** Mohamed
- **Acceptance:** Agent completes tasks, tool accuracy > 80%, evaluation report
- **Blocked by:** M10

---

## Phase 7 — Capstone (Month 12)

| ID | Milestone | Due | Evidence | Status |
|----|-----------|-----|----------|--------|
| M13 | Capstone MVP | Month 12 | `projects/07-capstone/thanaweyagpt/` | Planned |

### M13 — ThanaweyaGPT MVP
- **Description:** Full-stack AI application integrating all learned skills
- **Owner:** Mohamed
- **Acceptance:** Working app with backend + frontend + RAG + agent, deployed
- **Blocked by:** M8, M11, M12, M9

---

## Milestone Summary

| Total | Done | In Progress | Blocked | Planned | Deferred |
|-------|------|-------------|---------|---------|----------|
| 13 | 0 | 0 | 0 | 13 | 0 |

### Dependency Graph

```
M1 (Go basics) ──────────→ M4 (Auth MVP) ──→ M7 (Frontend) ──→ M8 (Full-stack) ──→ M9 (Docker)
M2 (Portfolio)                                                                │
M3 (Git mastery)                                                              │
M5 (PostgreSQL) ──────────────────────────────────────────────────────────────→│
M6 (Source learning)                                                          │
M10 (AI foundations) ──→ M11 (RAG) ──→ M13 (ThanaweyaGPT) ←──────────────────┘
                   └──→ M12 (Agents) ──────────────────────────→ M13
```
