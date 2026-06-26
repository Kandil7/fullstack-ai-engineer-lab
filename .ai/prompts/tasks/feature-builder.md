---
id: task.feature-builder
layer: task
version: 1.0.0
status: active
owner: workspace
pairs_with_roles: [project-planner, pair-programmer]
constraints: [mvp-first, ordered-steps, repo-first]
---

# Task: Feature Builder

Help me implement a feature without doing it all for me.

## Steps

1. Break the feature into tasks.
2. Identify dependencies between tasks.
3. Suggest an implementation order (MVP-first).
4. For each task, name the file(s) and the interface shape — then let me implement.

## Constraints

- Keep the MVP slice tiny; defer extras.
- Do not emit a full implementation; guide step by step (see `roles/pair-programmer.md`).
- Reference the existing `plan.md` for the project rather than re-planning from scratch.
