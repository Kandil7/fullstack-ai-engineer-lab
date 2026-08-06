# FastAPI — 51: CI/CD

## Topic Overview

CI/CD is how a change becomes a running service without a human clicking.
The pipeline is a **gauntlet** of stages — unit tests, lint, build,
CVE scan, migrate, deploy, health gate — where every stage that fails
stops the ship. Three structural decisions matter: **ordering** (fast
feedback first, expensive later), **matrix testing** (the change must
pass across supported Python versions and dependency sets, not just your
laptop), and **caching** (dependency installs keyed on the lockfile turn
minutes into seconds). Deploys add two more: **migrations run expand-
before / contract-after** so new code never queries a missing schema, and
**rollout math** — canary percentages or blue-green switching — with a
**rollback** that is just a code revert when the schema stayed
compatible.

The mental model: CI is a gauntlet with a budget (fast = cheap to run,
often; slow = expensive, run rarely) and deploys are traffic math with
health gates.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a pipeline stage order with fast feedback first.
2. Write a matrix across Python versions and dependency sets.
3. Cache dependencies by lockfile hash.
4. Order migrations expand-before, contract-after.
5. Choose canary vs blue-green and plan rollback.

## Prerequisites

| Need | Where |
|---|---|
| Testing | `20-testing.py`, `42-security-testing.py` |
| Docker | `48-docker-fastapi-lecture.md` |
| Health gates | `46-health-and-readiness-lecture.md` |

---

## 1. The gauntlet

```text
unit-tests -> lint -> build-image -> cve-scan -> migrate -> canary -> health -> 100%
```

Ordering is economics: unit tests catch 80% of breakage in 1 minute and
run on every push; builds and scans cost minutes and run on merge; the
deploy runs rarely. Every stage gates the next — a lint failure never
reaches the deploy.

## 2. Matrix testing

The matrix is the coverage contract:

```yaml
strategy:
  matrix:
    python: ["3.11", "3.12", "3.13"]
    deps: ["min", "latest"]
```

Every cell must pass. This is how "works on my laptop" dies: the change
is tested on the oldest supported Python with minimum dependencies and
the newest with latest. A red cell stops the merge.

## 3. Caching

`pip install` is the slowest stage. Key the cache on the lockfile hash:
unchanged lockfile → restore in seconds; changed → rebuild. Keying
correctly matters — too coarse serves stale deps, too fine never hits.

## 4. Migrations in the pipeline

Schema changes ship with code, and ordering is the correctness rule:

- **Expand** (additive: new column, new table) — before deploy.
- **Deploy** the new code.
- **Contract** (destructive: drop column) — after, once old code is gone.

New code queries the new column that already exists; old code (during
rollback or gradual rollout) still has its columns. This is why
expand/contract exists — and why rollback stays a code revert.

## 5. Rollout and rollback

- **Canary**: 5% → 25% → 100% with a health gate and metric check at
  each step — small blast radius, measurable, slower.
- **Blue-green**: flip a whole fleet — instant, all-or-nothing, big
  blast; the old fleet stays for instant rollback.

Both are traffic math with gates. The rollback story is the last gate:
with expand/contract, rolling back is reverting the image — the data
stayed compatible.

## Common Mistakes to Avoid

### Mistake 1: Expensive stages first
```python
# WRONG - a 5-minute build before a 1-second lint failure
# CORRECT - fast feedback first; expensive after
```

### Mistake 2: One Python version
```python
# WRONG - tested on 3.13 only, breaks on 3.11 in production
# CORRECT - matrix across supported versions and deps
```

### Mistake 3: No dependency cache
```python
# WRONG - 2 minutes of pip install on every run
# CORRECT - cache keyed on the lockfile hash
```

### Mistake 4: Migrations after deploy
```python
# WRONG - new code queries columns that don't exist yet
# CORRECT - expand before, contract after
```

### Mistake 5: Deploy without a rollback story
```python
# WRONG - the deploy is a point of no return
# CORRECT - expand/contract keeps rollback = code revert
```

## Best Practices

1. Fast feedback first: tests/lint on every push.
2. Matrix across supported versions and dependency sets.
3. Cache dependencies by lockfile hash.
4. Migrations expand-before, contract-after.
5. Canary for risky, blue-green for fast, gates everywhere.
6. Every deploy has a tested rollback path.
7. Health gates in the pipeline mirror the readiness probes.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Test stage | seconds | — |
| Build + scan | minutes | layer-cached images |
| Matrix | versions × cells | run rare cells on merge only |
| Canary rollout | minutes per step | blue-green for speed |
| Bad deploy | incident | gates + rollback |

The pipeline is a budget: cheap stages run often, expensive ones rarely,
and the deploy spends the budget only when everything else passed.

## AI Engineering Relevance

**Where this shows up:** model-version pipelines (test → eval → registry
→ serve), ML training CI (data validation gates), and the serving image
pipeline from topic 48.

| Concept here | Used for |
|---|---|
| matrix | torch/Python version coverage |
| eval gates | model quality thresholds in the pipeline |
| expand/contract | feature-store schema evolution |
| canary | serving a new model version to 5% |
| rollback | reverting a bad model deploy |

**Scale note:** a model pipeline adds an *eval gate* after tests — a
candidate model that fails eval never reaches the registry, the same way
a failing test never reaches the deploy.

## Practice Exercises

### Exercise 1: Gauntlet  (Difficulty: Easy)
Run a pipeline with a failing stage; assert the ship stops there.

### Exercise 2: Matrix  (Difficulty: Easy)
All-cells-pass semantics; assert a red cell fails the merge.

### Exercise 3: Cache key  (Difficulty: Medium)
Lockfile hash keying; assert hit on same hash, miss on change.

### Exercise 4: Migration order  (Difficulty: Medium)
Assert expand precedes deploy and contract follows it.

### Exercise 5: Rollout math  (Difficulty: Medium)
Canary percentages and health-gate aborts; assert both paths.

### Exercise 6: Full pipeline model  (Difficulty: Hard)
Model a pipeline with cache + matrix + eval gate + canary; assert the
worst-case wall time and the fail-stop behavior.

## Summary

| Concept | Description |
|---|---|
| gauntlet | stages gating each other |
| matrix | the coverage contract |
| caching | lockfile-keyed dependency installs |
| expand/contract | migration ordering |
| canary/blue-green | rollout traffic math |
| rollback | code revert when schema stays compatible |

CI/CD is a gauntlet with a budget and a rollback. Order it for fast
feedback, test the matrix, cache the deps, expand before and contract
after, and every deploy is a revertible, gated step.

## Quick Reference

| Task | Idiom |
|---|---|
| Fast stage | tests + lint on push |
| Matrix | python × deps cells |
| Cache | key = lockfile hash |
| Migrations | expand → deploy → contract |
| Canary | 5% → 25% → 100%, gate each |
| Rollback | revert image; schema compatible |

## Next Steps

Next: **[52 — Serving ML Models](52-serving-ml-models-lecture.md)** — the
payload that justifies the whole pipeline.

Continues in: **[system-design 01 — Fundamentals](../../05-web-frameworks/system-design/01-fundamentals.md)** —
the design vocabulary for the services this pipeline ships.

Official docs:
- GitHub Actions: https://docs.github.com/en/actions
- Expand/contract (Microsoft): https://learn.microsoft.com/en-us/azure/architecture/patterns/expand-contract
