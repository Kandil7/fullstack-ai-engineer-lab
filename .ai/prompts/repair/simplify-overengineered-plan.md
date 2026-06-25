---
id: repair.simplify-overengineered-plan
layer: repair
version: 1.0.0
status: active
owner: workspace
trigger: over-engineering
---

# Repair: Simplify Over-Engineered Plan

Use when a plan or architecture has grown more complex than the problem requires.

## Steps

1. Restate the **actual** requirement and its MVP.
2. List every component/layer/agent and ask: does the MVP need this now?
3. Remove anything not justified by a real driver (YAGNI).
4. Collapse speculative generality into the simplest thing that works.
5. Preserve scope — simplify the solution, not the goal.

## Output

A simplified plan/architecture with a short "Removed and why" list. Flag anything genuinely
deferred (not deleted) as future scope.
