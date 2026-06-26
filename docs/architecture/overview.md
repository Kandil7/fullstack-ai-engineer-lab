# Architecture Overview

The Full-Stack AI Engineer Lab is a **Repo-Centric Agentic Workspace** organized in seven
logical layers. "Agents" are prompted operating modes (markdown), not runtime processes;
orchestration is human-led and workflow-driven.

## Layers

1. **Content Layer** (`docs/`) — roadmap, learning paths, deep dives, decision records.
2. **Project Layer** (`projects/`) — the actual code: auth-service, chat-service, rag-system, capstone.
3. **Workflow Layer** (`.ai/workflows/`) — step-by-step procedures for planning, building, reviewing, debugging, learning.
4. **Prompt Layer** (`.ai/prompts/`) — modular operating modes (system / roles / tasks / critics / repair).
5. **Template Layer** (`templates/`) — standardized artifact shapes.
6. **Evaluation Layer** (`evaluations/`) — golden cases, regressions, RAG datasets, reports.
7. **Delivery Layer** (`infra/`) — docker-compose, scripts.

## Request Lifecycle (feature example)

```text
feature request
  → feature/01-plan      (Project Planner → plan.md)
  → feature/02-design    (System Architect → architecture-review.md / ADR)   [if boundaries]
  → feature/03-build     (Pair Programmer → src/, tests/, notes.md)
  → feature/04-review    (Code Reviewer → ai-review.md)
  → feature/05-fix       (→ updated code, mistakes.md)
  → feature/06-reflect   (Learning Coach → learning notes)
  → DONE
```

## Control Flow

- Entry = one of: new feature, new bug, new source, new design question.
- The workflow selects template + prompt + target folder.
- Human executes/edits artifacts; outputs land at deterministic paths.
- Reviews feed fixes, ADRs, or learning notes.

## Memory Model

- **Short-term:** current task, workflow step, active source, project folder, prompt constraints.
- **Long-term:** explicit repo artifacts — ADRs, reviews, debugging sessions, learning notes, eval reports, mistakes logs.
- No hidden opaque memory. Retrieval is by path → registry → folder convention.

## Failure Points to Watch

Overly-broad prompts · duplication between docs and project notes · turning every capability into
an agent · missing naming conventions · reviews without follow-up · source learning without
project linkage.
