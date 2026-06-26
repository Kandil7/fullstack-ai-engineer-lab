# ADR-0002: Prompt modularization & `.ai` namespace

- **Status:** Accepted
- **Date:** 2026-06-26
- **Deciders:** Workspace owner
- **Tags:** architecture, prompts

## Context

The original plan offered both a single mega-prompt style and a scattered `99-ai-workflow/`
folder. A monolithic prompt is hard to version, audit, and reuse. We also needed to pick one
canonical root for the AI workspace.

## Decision Drivers

- Prompts must be versioned, owned, and individually auditable.
- Format rules should not be duplicated across prompts (DRY).
- A clear, conventional namespace separating machine workspace from human docs.

## Options Considered

### Option A — Modular prompts under `.ai/` (layered: system/roles/tasks/critics/repair)
- Pros: Reusable, auditable, registry-friendly, layered composition.
- Cons: More files to manage.

### Option B — Monolithic prompts under `99-ai-workflow/`
- Pros: Fewer files.
- Cons: Prompt sprawl inside files; hard to version/audit; format duplication.

## Decision

Adopt **modular, layered prompts** under **`.ai/`** (Option A). Layering order:
governor → role → task → output-format-rules → critic/repair. Shared format lives once in
`.ai/prompts/system/output-format-rules.md`.

## Consequences

- Positive: each prompt is small, owned, versioned in `registries/prompt-registry.yaml`; the
  prompt-auditor critic can validate each in isolation; no format duplication.
- Negative: more files; requires registry discipline to avoid drift.
- Follow-ups: prompt regression evals (`evaluation/prompt-regression`) guard against drift.

## Links

- Related ADRs: [0001](0001-repo-centric-workspace.md)
- Spec: `docs/plan/1) Executive Summary.md` sections 8, 15 (namespace open question)
