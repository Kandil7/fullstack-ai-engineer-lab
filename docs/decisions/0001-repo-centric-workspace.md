# ADR-0001: Repo-centric agentic workspace

- **Status:** Accepted
- **Date:** 2026-06-26
- **Deciders:** Workspace owner
- **Tags:** architecture, workspace

## Context

The learning plan, projects, prompts, and reviews were scattered across chats, notebooks, and
ad-hoc files, making progress unstructured and unmeasurable. We need a single, organized system
that links learning to execution and review, while remaining executable by one person.

## Decision Drivers

- Single source of truth for learning + building + reviewing.
- Must be operable solo; avoid over-engineering an agent runtime.
- Must extend later toward production AI systems (Athar/Baligh/ThanaweyaGPT).

## Options Considered

### Option A — Repo-centric workspace (markdown artifacts, human-led orchestration)
- Pros: Simple, versioned, immediately usable, no runtime to maintain.
- Cons: Orchestration is manual, not automated.

### Option B — Multi-agent runtime platform (autonomous orchestrator)
- Pros: Automated workflows.
- Cons: Large build cost, premature; far beyond current need.

## Decision

Adopt the **repo-centric workspace** (Option A): content + project + workflow + prompt + template
+ evaluation layers in one monorepo, where "agents" are prompted operating modes and orchestration
is human-led + workflow-driven.

## Consequences

- Positive: low maintenance; every artifact is versioned and reviewable; fast to start; extensible.
- Negative: no automatic execution; the human must drive the workflow steps.
- Follow-ups: scaffolding scripts (Phase 3) reduce friction; optional local retrieval later.

## Links

- Related ADRs: [0002](0002-prompt-modularization.md), [0003](0003-hybrid-stack-go-fastapi.md)
- Spec: `docs/plan/1) Executive Summary.md` sections 4, 12
