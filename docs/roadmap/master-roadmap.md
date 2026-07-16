# Master Roadmap — Full-Stack AI Engineer Lab

> **Baseline plan.** This file is the single source of truth for the 12-month journey.
> Do not modify day-to-phase — update milestones and progress-dashboard instead.

**Last updated:** 2026-06-26

---

## Overview

| # | Phase | Duration | Months |
|---|-------|----------|--------|
| 0 | Foundations | 3 months | 1–3 |
| 1 | Backend Foundations (Go) | 3 months | 4–6 |
| 2 | Frontend (Flutter / Next.js) | 3 months | 4–6 |
| 3 | AI Fundamentals | 3 months | 7–9 |
| 4 | RAG Systems | 2 months | 10–11 |
| 5 | AI Agents | 1 month | 12 |
| 6 | System Design + DevOps | Ongoing | 8–12 |
| 7 | Capstone — ThanaweyaGPT | Final | 11–12 |

> Phases 1 and 2 run in parallel (backend + frontend). Phase 6 is interleaved from month 8 onward.

---

## Phase 0 — Foundations

**Duration:** Months 1–3 (12 weeks)
**Goal:** Build a solid web development foundation and establish a learning workflow that compounds.

### Projects
- `projects/00-core-foundations/` — HTML/CSS/JS portfolio, Go mini-exercises, Git workflow practice

### Skills Covered
- HTML5, CSS3, JavaScript ES6+ (DOM, fetch, async/await)
- Git branching, PR workflow, rebase, conventional commits
- Linux basics, command line proficiency
- Go language basics (structs, interfaces, HTTP handlers)
- Source-learning workflow (read → extract → apply → document)

### Key Resources
- FreeCodeCamp Responsive Web Design + JavaScript Algorithms
- The Odin Project — Foundations path
- Go Tour (tour.golang.org)
- Pro Git book (git-scm.com)

### Definition of Done
- [ ] Deployed portfolio site with 3+ pages (HTML/CSS/JS)
- [ ] 10 Go mini-exercises with tests passing
- [ ] Git workflow: feature branch → commit → PR → merge → cleanup
- [ ] First source-learning summary documented in `docs/learning/source-summaries/`
- [ ] All artifacts version-controlled with clean commit history

---

## Phase 1 — Backend Foundations (Go)

**Duration:** Months 4–6 (12 weeks)
**Goal:** Build a production-quality Go backend service with authentication, middleware, and database integration.

### Projects
- `projects/01-backend-go/01-auth-service/` — Auth service MVP (register, login, JWT, middleware)
- `projects/03-databases/postgres-design/` — PostgreSQL schema design for auth + users

### Skills Covered
- Go standard library (net/http, encoding/json, crypto)
- RESTful API design (routes, middleware, error handling)
- JWT authentication and session management
- PostgreSQL schema design, migrations, queries
- Redis caching patterns
- API testing (unit + integration)

### Key Resources
- Go standard library docs
- PostgreSQL official documentation
- Redis documentation
- "Go: Design Patterns" —书籍 or equivalent online resource

### Definition of Done
- [ ] Auth service: register, login, refresh-token endpoints working
- [ ] JWT middleware protecting routes
- [ ] PostgreSQL schema with users + sessions tables
- [ ] Redis caching for session data
- [ ] Integration tests passing (go test + testify)
- [ ] API documented (OpenAPI or README)

---

## Phase 2 — Frontend (Flutter / Next.js)

**Duration:** Months 4–6 (12 weeks, parallel with Phase 1)
**Goal:** Build a responsive frontend that integrates with the Go backend API.

### Projects
- `projects/02-frontend/flutter-app/` — Mobile app (Flutter) OR
- `projects/02-frontend/nextjs-web/` — Web dashboard (Next.js + TypeScript)

### Skills Covered
- Flutter: widgets, state management, navigation, HTTP client
- Next.js: pages, API routes, SSR/SSG, Tailwind CSS
- API integration (fetch, error handling, loading states)
- Responsive design and mobile-first principles
- State management patterns (BLoC for Flutter, Zustand for Next.js)

### Key Resources
- Flutter documentation (flutter.dev)
- Scrimba Next.js course
- App Academy Open (frontend)
- Tailwind CSS documentation

### Definition of Done
- [ ] Frontend app connects to Go backend API
- [ ] Authentication flow (login/register screens)
- [ ] Dashboard or home screen with real data
- [ ] Responsive on mobile + desktop
- [ ] Error handling and loading states
- [ ] Deployed (Flutter web or Vercel)

---

## Phase 3 — AI Fundamentals

**Duration:** Months 7–9 (12 weeks)
**Goal:** Understand ML concepts, master prompt engineering, and build Python proficiency for AI work.

### Projects
- `projects/04-ai-engineering/prompt-engineering/` — Prompt library + evaluation framework
- `projects/04-ai-engineering/` — Python scripts for ML basics

### Skills Covered
- Python: data structures, OOP, async, virtual environments
- ML fundamentals: supervised/unsupervised learning, evaluation metrics
- LLM basics: tokenization, context windows, temperature, top-p
- Prompt engineering: few-shot, chain-of-thought, structured output
- API integration with OpenAI / Anthropic / local models

### Key Resources
- ML for Beginners (Microsoft GitHub)
- Andrej Karpathy — Neural Networks: Zero to Hero
- Hugging Face NLP Course
- OpenAI prompt engineering guide
- Anthropic prompt engineering docs

### Definition of Done
- [ ] Python proficiency: 20+ scripts demonstrating core patterns
- [ ] Prompt library with 10+ tested prompts (in `.ai/prompts/`)
- [ ] Prompt evaluation framework with 5+ test cases
- [ ] ML basics project: train + evaluate a simple classifier
- [ ] All prompts version-controlled with evaluation results

---

## Phase 4 — RAG Systems

**Duration:** Months 10–11 (8 weeks)
**Goal:** Build a production-quality Retrieval-Augmented Generation pipeline with evaluation.

### Projects
- `projects/04-ai-engineering/rag-system/` — End-to-end RAG pipeline

### Skills Covered
- Embedding models (OpenAI, Cohere, sentence-transformers)
- Vector databases (Qdrant — primary, Pinecone — alternative)
- Chunking strategies (fixed-size, semantic, recursive)
- Retrieval patterns (hybrid search, reranking)
- RAG evaluation (context relevance, faithfulness, answer quality)
- LangChain / LlamaIndex basics

### Key Resources
- DeepLearning.AI — Building and Evaluating Advanced RAG
- Illustrated Transformer (Jay Alammar)
- Qdrant documentation
- LangChain RAG tutorial

### Definition of Done
- [ ] Working RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- [ ] At least 2 chunking strategies implemented and compared
- [ ] Hybrid search (semantic + keyword)
- [ ] Evaluation report with 5+ test queries
- [ ] RAG quality metrics documented (precision, recall, faithfulness)
- [ ] ADR on chunking strategy choice

---

## Phase 5 — AI Agents

**Duration:** Month 12 (4 weeks)
**Goal:** Build an agent system with tool calling, multi-step reasoning, and orchestration.

### Projects
- `projects/04-ai-engineering/agents/` — Agent system with tool calling

### Skills Covered
- Tool calling patterns (function calling, tool definitions)
- Agent architectures (ReAct, Plan-and-Execute, multi-agent)
- Memory and state management for agents
- Error handling and recovery in autonomous loops
- Agent evaluation (task completion rate, tool accuracy)

### Key Resources
- Hugging Face — Agents course
- Berkeley LLM Agents course
- Arize AI — Agent evaluation
- Anthropic tool use documentation

### Definition of Done
- [ ] Agent with 3+ tools (search, calculator, file reader)
- [ ] Multi-step reasoning demonstrated (plan → execute → reflect)
- [ ] Tool calling accuracy > 80% on test cases
- [ ] Error handling: graceful failure on tool errors
- [ ] Evaluation report with task completion metrics

---

## Phase 6 — System Design + DevOps

**Duration:** Months 8–12 (interleaved, 20 weeks)
**Goal:** Design scalable systems and deploy everything with production-grade infrastructure.

### Projects
- `projects/05-system-design/` — Architecture docs, ADRs, design diagrams
- `projects/06-devops/docker/` — Docker setup, CI/CD, deployment

### Skills Covered
- System design: scalability, availability, consistency trade-offs
- Docker: Dockerfile, docker-compose, multi-stage builds
- CI/CD: GitHub Actions, automated testing, deployment pipelines
- Monitoring: logging, metrics, alerting basics
- Cloud deployment (Vercel, Railway, or AWS basics)

### Key Resources
- Docker official documentation
- "System Design Interview" — Alex Xu
- GitHub Actions documentation
- Grafana / Prometheus basics

### Definition of Done
- [ ] Docker Compose for full stack (Go + Flutter/Next.js + PostgreSQL + Redis + Qdrant)
- [ ] CI pipeline: lint → test → build → deploy
- [ ] System design doc for ThanaweyaGPT architecture
- [ ] 5+ ADRs covering major technical decisions
- [ ] Monitoring setup (logs + basic metrics)

---

## Phase 7 — Capstone: ThanaweyaGPT

**Duration:** Months 11–12 (8 weeks, overlapping with Phases 5–6)
**Goal:** Build ThanaweyaGPT — a full-stack AI application integrating all learned skills.

### Projects
- `projects/07-capstone/thanaweyagpt/` — Complete application

### Skills Covered (synthesis)
- Full-stack integration (Go backend + Flutter/Next.js frontend)
- RAG pipeline for domain knowledge
- AI agent for interactive assistance
- Production deployment with monitoring
- End-to-end testing and evaluation

### Key Resources
- All previous resources combined
- Domain-specific knowledge (Arabic education content)
- User feedback and iteration

### Definition of Done
- [ ] Working ThanaweyaGPT application with:
  - Backend API (Go)
  - Frontend (Flutter or Next.js)
  - RAG pipeline for knowledge retrieval
  - Agent for interactive Q&A
  - Docker deployment
  - CI/CD pipeline
- [ ] End-to-end tests passing
- [ ] Performance benchmarks documented
- [ ] User acceptance testing with 3+ users
- [ ] Final architecture review and ADR

---

## Progress Tracking

| File | Purpose |
|------|---------|
| `milestones.md` | Trackable milestones with IDs, dates, evidence |
| `progress-dashboard.md` | Quick-read status summary |
| `skills-matrix.md` | Skill levels and next steps |
| `../tracking/current-focus.md` | Current execution window |
| `../reviews/weekly/` | Weekly review log |
| `../reviews/monthly/` | Monthly review log |

---

## Rules

1. **This roadmap is the baseline** — phases don't change, only timing adjustments in milestones.
2. **Evidence required** — every milestone needs a file path proving completion.
3. **Monthly reviews** — update progress-dashboard at month boundaries.
4. **30-day rule** — every 30 days something must work end-to-end.
5. **Parallel phases** — Phases 1+2 run together; Phase 6 interleaved; Phase 7 overlaps with 5+6.
