---
id: repair.retry-with-missing-context
layer: repair
version: 1.0.0
status: active
owner: workspace
trigger: missing-context
---

# Repair: Retry With Missing Context

Use when a previous run failed or guessed because inputs were missing.

## Steps

1. List precisely what was missing (files, constraints, decisions) under `## Missing Inputs`.
2. Do **not** re-attempt the task on assumptions.
3. Ask the smallest set of questions that unblocks the work.
4. Once provided, redo only the affected portion — not the whole artifact.

## Output

A `## Missing Inputs` block + targeted questions. No speculative content.
