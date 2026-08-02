# MLOps — 12: CI/CD for ML

## Topic Overview

CI/CD for ML is the automation of the path from a code or data change to a
validated, deployed model — with **quality gates** at every stage: lint/type
checks, unit tests, data validation, golden-output tests, and eval-threshold
checks. Classic CI/CD tests *code*; ML CI/CD must also test *data, models,
and pipelines*. That distinction is what makes ML CI/CD hard — and it is
exactly what separates an ML codebase from an ML *platform*.

The standard pattern (DVC + GitHub Actions / GitLab CI, or cloud-native
SageMaker Pipelines / Vertex AI Pipelines):

```
push → lint + typecheck + unit tests → data validation → train smoke →
eval on golden set → gate (beat baseline) → register model → deploy to staging
→ shadow/canary → promote to production
```

The **eval gate** is the ML-specific heart: a candidate model is not
deployable unless it beats the current champion on a frozen evaluation set
within tolerance. Without it, "CI green" means nothing — a model can pass all
code tests and still be a regression.

Why this matters for an AI engineer: CI/CD is how quality becomes *automatic*
instead of *aspirational*. Every commit runs the gates; every candidate is
validated before it can touch production. The AI engineer designs the gates,
owns the golden datasets, and makes the pipeline the single path to
production — no manual "ssh and deploy" escapes.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Design an ML CI/CD pipeline with quality gates at every stage
2. Write an eval gate: candidate must beat champion on a frozen eval set
3. Automate data validation and golden-output tests in CI
4. Promote candidates to staging then production with gates
5. Use DVC to fetch the right data version in CI
6. Handle model-specific failure modes (flaky tests, nondeterminism)
7. Distinguish CI for code vs CI for data/models

## Prerequisites

| Need | Where |
|---|---|
| Reproducibility + seeds | `08-mlops/lectures/01-reproducibility-lecture.md` |
| Data validation | `08-mlops/lectures/10-data-validation-lecture.md` |
| Model registry | `08-mlops/lectures/04-model-registry-lecture.md` |
| Orchestration | `08-mlops/lectures/09-pipeline-orchestration-lecture.md` |
| Git | `00-core-foundations/git-linux/` |

## 1. Code CI vs ML CI: The Added Gates

| Stage | Code CI (all software) | ML CI (additions) |
|---|---|---|
| Lint/type | black, ruff, mypy | same |
| Unit tests | functions, services | + model purity, preprocessing units |
| Data | — | schema + stats validation (Lecture 10) |
| Model | — | golden-output test, eval gate vs champion |
| Deploy | build + push image | register version → staging → canary → prod |

The mental model: ML CI has everything code CI has, *plus* a data gate and a
model gate. Both new gates need **frozen artifacts**: a golden eval set and a
champion model reference — versioned like everything else (Lecture 03).

## 2. The Eval Gate: The ML Heart of CI

The eval gate is a script that: loads the candidate's metrics, loads the
champion's metrics, and fails the pipeline unless the candidate wins (or ties)
within tolerance. The eval set is **frozen and never touched by training** —
it is the referee both sides agree to.

```python
def eval_gate(candidate: dict, champion: dict, key: str = "val_acc",
              tol: float = 0.0) -> tuple[bool, str]:
    """Candidate passes only if it beats the champion (within tolerance)."""
    c = candidate[key]
    ch = champion[key]
    passed = c >= ch - tol
    reason = (f"PASS: candidate {c:.4f} >= champion {ch:.4f} - {tol}"
              if passed else f"FAIL: candidate {c:.4f} < champion {ch:.4f}")
    return passed, reason

print(eval_gate({"val_acc": 0.921}, {"val_acc": 0.918}))
print(eval_gate({"val_acc": 0.905}, {"val_acc": 0.918}))
```

Output (conceptually):
```
(True, 'PASS: candidate 0.9210 >= champion 0.9180')
(False, 'FAIL: candidate 0.9050 < champion 0.9180')
```

**Design rule:** the gate compares on a *frozen* eval set, never on the
training run's own val split (the candidate's own split is its own referee —
untrustworthy). Some teams add statistical significance: candidate must beat
champion by more than the eval-set's noise margin.

## 3. The CI Pipeline Definition

GitHub Actions example — the same pipeline shape in any runner:

```yaml
name: ml-pipeline
on: [push, pull_request]
jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements-dev.txt
      - run: black --check . && ruff check . && mypy .
      - run: pytest tests/unit -q

  data-validation:            # ML gate 1
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: dvc pull data          # fetch the pinned data version
      - run: python validate_data.py

  eval-gate:                  # ML gate 2
    runs-on: ubuntu-latest
    needs: [data-validation]
    steps:
      - run: python train_smoke.py          # small, deterministic
      - run: python eval_gate.py --champion champion_metrics.json
```

Output (conceptually):
```
✓ code-quality      (black, ruff, mypy, unit tests)
✓ data-validation   (schema + stats pass)
✓ eval-gate         (candidate beats champion)
```

## 4. Data in CI: `dvc pull` and Pinned Versions

CI runs in a clean checkout — it needs the *exact data version* the pipeline
expects. DVC fetches it deterministically from the object store (Lecture 03);
the pipeline references data by version, never by "whatever is in the
checkout".

```bash
dvc pull data -r s3-remote          # fetches the pinned dataset blobs
dvc data status                     # verify no unexpected changes
```

Output (conceptually):
```
data/train.parquet  — fetched (sha256:c9a3...)
data status: nothing to change, working tree clean
```

This is the reproducibility contract enforced in CI: the eval gate's numbers
are comparable across runs *because* every run used the same data version.

## 5. Promoting Through Stages: Staging → Canary → Production

CI ends at **staging**; production promotion is gated and observable:

1. CI validates candidate → registers version in the registry (stage: staging)
2. Shadow deploy: the candidate scores live traffic *without serving it* —
   predictions compared to champion for a day
3. Canary: 5% live traffic, monitored (Lecture 11) for a window
4. Full promote: registry stage → production; monitoring alert rules attach

```python
def promote_plan(candidate: str, shadow_pass: bool, canary_pass: bool) -> str:
    if not shadow_pass:
        return "hold: shadow test failed"
    if not canary_pass:
        return "rollback: canary metrics regressed"
    return "promote to production"
```

Output (conceptually):
```
promote to production  (after shadow + canary both pass)
```

The key discipline: **promotion is a pipeline decision**, recorded in the
registry (who/when/why from Lecture 04) — not a human "looks good, ship it".

## 6. ML-Specific CI Failures and Fixes

| Failure | Root cause | Fix |
|---|---|---|
| Flaky eval gate | unseeded runs (Lecture 01) | seed everything, freeze data |
| Golden test "passes locally, fails CI" | env drift (Lecture 06) | run CI in the same image |
| Eval gate always green | gate on training split | gate on frozen champion eval set |
| CI too slow | full training in CI | train_smoke (small subset) + nightly full eval |
| Data drift between runs | unversioned data | `dvc pull` pinned version |

The discipline: CI should run the *fast, deterministic* checks; the *heavy*
eval (full training, full eval set) runs nightly or on merge to main — with
the same gates.

## Every Use Case

- **Every code change**: unit + lint + type + data + golden gates automatically.
- **Every candidate model**: eval-gated against the champion before any deploy.
- **Data changes**: a dataset version bump triggers revalidation and eval.
- **Dependency bumps**: lockfile changes re-run the whole gate suite.
- **Nightly full eval**: complete retraining + eval with the frozen gate set.
- **Regulatory traceability**: every production model links to the CI run +
  eval gate + registry entry that promoted it.
- **Multi-team safety**: a shared pipeline means no team can ship an
  unvalidated model.

## Real-World Use Cases for AI Engineers

- **Fintech model governance**: a regulatory requirement that every model
  change is reviewed and tested is *operationalized* as the CI pipeline: the
  eval gate's pass record + the registry promotion entry are the audit
  evidence. An engineer cannot ship a model that doesn't beat the champion —
  the pipeline enforces policy.
- **E-commerce ranking team**: every PR runs lint + unit + data validation;
  every model candidate runs the eval gate. A candidate that "felt better"
  but lost the gate is rejected automatically — the gate removes politics
  from model selection.
- **ML platform team**: a shared CI template (Docker image + gates) means 20
  teams get the same quality bar with zero setup — the platform team's
  leverage is a good pipeline, not a review process.
- **Startup with 2 engineers**: one CI pipeline (unit tests + eval gate +
  auto-deploy to staging) lets the founders ship model changes safely on
  Friday afternoon — the gates catch what manual review would miss.
- **RAG services (Phase 9)**: retrieval-eval gates (recall@k on a frozen
  eval set) run in CI for every chunking/embedding change — the same eval-gate
  pattern applied to RAG components.

## Common Mistakes to Avoid

### Mistake 1: No eval gate
"CI green" on a model means nothing without beating the champion on a frozen set.

### Mistake 2: Gating on the training run's own split
The candidate referees its own game. Gate on the frozen champion eval set.

### Mistake 3: Unseeded / nondeterministic gates
Flaky gates erode trust; seed everything (Lecture 01).

### Mistake 4: Running full training in every PR
Too slow → engineers start bypassing. Small smoke + nightly full eval.

### Mistake 5: Data not pinned in CI
The eval gate's numbers only compare if every run uses the same data version.

### Mistake 6: Manual production deploy escape hatch
"Just ssh and deploy it" breaks the audit trail. Make the pipeline the only path.

## Best Practices

1. Lint/type/unit gates for code; data + eval gates for ML
2. Gate candidates against a frozen champion eval set, not their own split
3. Pin data versions in CI with `dvc pull`
4. Run fast deterministic checks in PRs; heavy eval nightly
5. Record gate results in the registry (who/when/why)
6. Use the same Docker image in CI and production (Lecture 06)
7. Make promotion a pipeline decision with shadow/canary steps
8. Keep a frozen champion reference (metrics + eval set) per model
9. Alert on gate failures with the run ID
10. Treat pipeline changes as code: review them like code

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Lint + unit (per PR) | 1-3 min | O(1) | — |
| Data validation (per PR) | seconds-minutes | O(data) | sampled validation |
| Eval gate (per PR) | minutes | O(1) | train_smoke subset |
| Full nightly eval | hours | O(model) | — |
| DVC pull in CI | O(data) | O(data) | cache the object store locally |

## AI Engineering Relevance

**Where this shows up:** the single path from "code change" to "model in
production". ML CI/CD is how quality becomes automatic and how audits are
satisfied mechanically.

| Concept here | Used for |
|---|---|
| Eval gate | objective model selection |
| Data pinning | comparable eval numbers |
| Stage promotion | auditable, reversible deploys |
| Golden tests | no silent packaging regressions |

**Scale note:** at 20 teams × 50 models, a shared CI template is the only way
to keep a quality bar. The pipeline is the platform — its gates *are* the
governance.

## Practice Exercises

### Exercise 1: Eval Gate (Easy)
Implement `eval_gate(candidate, champion, key, tol)` and test pass/fail/tie
cases.

### Exercise 2: Gate Pipeline (Medium)
Write `run_gates(tests: dict[str, bool]) -> tuple[bool, list[str]]` that runs
code/data/eval gates in order, stops at the first failure, and returns the
failed stage name — the CI short-circuit logic.

### Exercise 3: Champion Management (Medium)
Implement `update_champion(candidate_metrics, champion_path)` that promotes
the candidate to champion only when the eval gate passes, writes the new
`champion_metrics.json`, and refuses to overwrite on failure.

### Exercise 4: CI Pipeline Design (Hard)
Design the full CI pipeline for a churn model (stages, gates, triggers,
nightly heavy eval, shadow/canary/promote), then implement the two most
important gates (eval gate + golden-output test) as runnable functions with
tests.

## Summary

| Concept | Description |
|---|---|
| Code gates | lint/type/unit — everything software already does |
| Data gate | schema + stats on pinned data (Lecture 10) |
| Eval gate | candidate must beat champion on frozen set |
| Promotion | staging → shadow → canary → production, recorded |
| Nightly eval | the heavy validation on a schedule |

ML CI/CD makes quality automatic: every change runs the gates, every candidate
is judged against the champion, and production is reached only through a
recorded, gated path. It is the difference between an ML codebase and an ML
platform.

## Quick Reference

| Task | Idiom |
|---|---|
| Add eval gate | candidate >= champion - tol on frozen set |
| Pin data in CI | `dvc pull data -r <remote>` |
| Run gates | pytest + validation script in CI stages |
| Promote | register → staging → shadow → canary → prod |
| Nightly heavy eval | scheduled workflow with full training |

## Next Steps

Next: **[13 Feature Stores](13-feature-stores-lecture.md)** — the shared,
versioned, online/offline feature infrastructure behind ML systems.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.github.com/en/actions, https://dvc.org/doc/start
