# CI/CD — Glossary 51

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Blue-green | Deploy | Fleet-wide switch with the old fleet held for rollback |
| Cache key | CI | The lockfile hash identifying a restoreable cache |
| Canary | Deploy | Gradual traffic shift: 5% → 25% → 100% |
| Contract | Migration | Destructive schema step — after deploy |
| Continuous delivery | Pipeline | Every change shippable; deploy is gated |
| Continuous integration | Pipeline | Every change tested and merged automatically |
| Expand | Migration | Additive schema step — before deploy |
| Gate | Pipeline | A stage whose failure stops the ship |
| Health gate | Deploy | Post-deploy probe before more traffic |
| Matrix | CI | Testing across versions × dependency sets |
| Rollback | Deploy | Reverting code/data after a bad deploy |
| Gauntlet | Pipeline | Ordered stages where each gates the next |

## Detailed Definitions

### Blue-green
**Definition**: Running the old fleet (blue) and new fleet (green); the
switch is a traffic flip with instant rollback to blue.
**Related**: Canary

### Cache key
**Definition**: The lockfile hash identifying a dependency cache —
unchanged hash restores, changed hash rebuilds.
**Related**: Matrix

### Canary
**Definition**: Routing 5% → 25% → 100% of traffic to a new version with
a health/metric gate at each step — small blast, measurable.
**Related**: Blue-green

### Contract
**Definition**: The destructive migration (drop column) run AFTER the new
code serves — old code and rollbacks still work meanwhile.
**Related**: Expand

### Continuous delivery
**Definition**: The practice of keeping every change deployable; the
deploy step is a gated, repeatable stage.
**Related**: Continuous integration

### Continuous integration
**Definition**: Automatically testing and merging every change — the
gauntlet that runs on every push.
**Related**: Matrix

### Expand
**Definition**: The additive migration (new column/table) run BEFORE
deploy so new code queries an existing schema.
**Related**: Contract

### Gate
**Definition**: A pipeline stage whose failure stops the ship — the
unit test that blocks the build, the scan that blocks the deploy.
**Related**: Gauntlet

### Health gate
**Definition**: A post-deploy check (readiness probe, error-rate budget)
before routing more traffic — the canary step's decision point.
**Related**: Canary

### Matrix
**Definition**: Running the test suite across Python versions ×
dependency sets — the coverage contract proving "not just my laptop".
**Related**: Gate

### Rollback
**Definition**: Reverting a bad deploy — a code revert when
expand/contract kept the schema compatible, or a data restore when it
didn't.
**Related**: Blue-green

### Gauntlet
**Definition**: The ordered pipeline where every stage must pass before
the next runs — fast feedback first, expensive stages later.
**Related**: Gate

## Key Concepts Summary

### The gauntlet order
- unit tests → lint → build → scan → migrate → canary → health → 100%.
- A failure anywhere stops the ship.
- Fast stages run on every push; expensive ones rarely.

### The deploy math
- Canary: gradual, measurable, small blast.
- Blue-green: instant, all-or-nothing, instant rollback.
- Health gates decide each step.

### The migration rule
- Expand before deploy; contract after.
- Rollback stays a code revert when the schema stays compatible.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Stages where each gates the next — ___
2. A stage whose failure stops the ship — ___
3. Versions × dependency sets — ___
4. Additive migration before deploy — ___
5. Destructive migration after deploy — ___
6. 5% → 25% → 100% — ___
7. Fleet-wide switch with instant revert — ___
8. Reverting code after a bad deploy — ___

**Answers:** 1-gauntlet, 2-gate, 3-matrix, 4-expand, 5-contract, 6-canary,
7-blue-green, 8-rollback
