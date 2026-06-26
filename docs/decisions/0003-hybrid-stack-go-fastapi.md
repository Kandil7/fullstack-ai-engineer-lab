# ADR-0003: Hybrid stack — Go core + FastAPI AI layer

- **Status:** Accepted
- **Date:** 2026-06-26
- **Deciders:** Workspace owner
- **Tags:** architecture, backend, ai

## Context

The target products (ThanaweyaGPT, Athar, Baligh) need both a high-performance core backend and
a flexible AI/RAG layer. Choosing one language for everything forces a compromise: Go is strong
for scalable services but weaker for the AI ecosystem; Python/FastAPI is ideal for AI but slower
for the core.

## Decision Drivers

- Performance and scalability for auth/users/billing/routing.
- First-class AI/LLM/RAG ecosystem for embeddings, retrieval, agents.
- Operational cost and ease of deployment.

## Options Considered

### Option A — Go everywhere
- Pros: Uniform, fast. Cons: Poor AI ecosystem; slow AI iteration.

### Option B — FastAPI everywhere
- Pros: Great for AI; fast to build. Cons: Weaker for high-throughput core services.

### Option C — Hybrid: Go core + FastAPI AI service
- Pros: Best tool per layer; Go gateway fronts a Python AI service.
- Cons: Two runtimes; cross-service contract to maintain.

## Decision

Adopt the **hybrid stack** (Option C): **Go** for the core backend (auth, users, routing,
billing, rate limits) and **FastAPI/Python** for AI services (RAG, embeddings, agents). Mobile =
Flutter, Web dashboard = Next.js. Data = PostgreSQL + Redis + Qdrant.

## Consequences

- Positive: each layer uses the best-fit tool; Go gives performance, FastAPI gives AI velocity.
- Negative: two runtimes to operate; a clear HTTP contract between Go gateway and AI service is required.
- Follow-ups: define the `/ai/*` and `/auth/*` contracts; containerize both in `infra/docker`.

## Links

- Related ADRs: [0001](0001-repo-centric-workspace.md)
- Spec: `docs/plan/1) Executive Summary.md` section 11, and the Stack Decision conversation
