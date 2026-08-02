# MLOps — 16: Case Study — End-to-End ML System

## Topic Overview

This lecture is the capstone of Phase 8: the full lifecycle of a production ML
system, end to end — from raw data to a monitored, A/B-tested, cost-managed
model — integrated with every practice from Lectures 01–15. Where earlier
lectures covered single practices, this one shows the *system*: how
reproducibility, tracking, versioning, the registry, packaging, Docker,
serving, optimization, orchestration, validation, monitoring, CI/CD, feature
stores, A/B testing, and cost all interlock.

The scenario: **"ChurnShield"** — a churn-prediction system for a telecom. We
follow one model release through the entire stack. The case study's companion
exercise (`16-case-study-e2e.py`) implements the core loop; this lecture is
the architect's tour — the decisions, the order, and the *why* at every step.

The master lesson: **production ML is an assembly line, not a monolith.** Each
practice is a station; the pipeline is the conveyor; and the whole is only as
strong as its weakest gate. This lecture teaches you to see the entire line at
once — the senior-AI-engineer skill.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Trace a model from raw data to production across all 15 MLOps practices
2. Order the stations correctly (why validation before training, registry before serving)
3. Wire reproducibility artifacts into every downstream gate
4. Design the promotion path: CI → eval gate → shadow → A/B → production
5. Identify the system's weakest links from an architecture description
6. Build a runnable skeleton of the full loop
7. Explain each station's failure mode and its neighbor's guard

## Prerequisites

| Need | Where |
|---|---|
| All of Phase 8 | `08-mlops/lectures/01..15-*-lecture.md` |
| sklearn | `07-machine-learning/` |
| FastAPI | `05-web-frameworks/fastapi/` |
| Statistics | `07-machine-learning/` |

## 1. The Architecture: ChurnShield at a Glance

```
                    ┌────────────────────────────────────────────┐
 [Raw data] → [1 Reproducibility] → [3 Data Versioning]         │
      │                                                          │
      ▼                                                          │
 [10 Data Validation] → [9 Orchestration] → [13 Feature Store]  │
                                  │                              │
                                  ▼                              │
                    [2 Experiment Tracking] ← [Train]            │
                                  │                              │
                                  ▼                              │
                    [4 Model Registry] → [5 Packaging] →         │
                                  │        [6 Docker]            │
                                  ▼                              │
                    [7 Serving] ← [8 Optimization]               │
                                  │                              │
                    [11 Monitoring] → [12 CI/CD] → [14 A/B]      │
                                  │                              │
                    [15 Cost]  ← every station reports here      │
                    └────────────────────────────────────────────┘
```

Every station reads and writes the shared artifacts: run records, dataset
versions, registry entries, monitoring logs.

## 2. Station Order: Why This Sequence

The order is not arbitrary — each station depends on the one before it:

| Station | Depends on | Why |
|---|---|---|
| 1 Reproducibility | — | seeds/hashes underpin every comparison |
| 3 Data Versioning | 1 | content hashes are the data identity |
| 10 Validation | 3 | gates the versioned data |
| 9 Orchestration | 1,3,10 | runs the DAG with caching/retries |
| 13 Feature Store | 9 | features computed once, served twice |
| 2 Tracking | 1 | run records need the reproducibility fields |
| 4 Registry | 2 | registered versions carry tracked metrics |
| 5 Packaging | 4 | the registry stores *packaged* artifacts |
| 6 Docker | 5 | images contain packaged models |
| 7 Serving | 6 | endpoints serve the images |
| 8 Optimization | 7 | optimize after measuring serving |
| 11 Monitoring | 7 | watch the deployed model |
| 12 CI/CD | 1..11 | gates orchestrate the whole line |
| 14 A/B | 7,11 | final human-decision gate on real traffic |
| 15 Cost | all | unit costs and budgets across everything |

**The order rule:** you cannot validate data you haven't versioned; you cannot
serve a model you haven't packaged; you cannot A/B a model you aren't
monitoring. Respect the dependency chain.

## 3. One Release, Walked Through

### 3.1 Data arrives (Stations 1, 3, 10)
A new month of customer data lands. The ingest task computes `sha256` (L1),
writes it as version `v37` in the object store (L3), and runs the schema +
stats checks (L10). A `status` field violates its allowed set → 200 rows
quarantined, alert paged. The pipeline continues on the good rows.

### 3.2 Features computed (Stations 9, 13)
The orchestrated DAG (L9) computes features — `tenure`, `usage_delta`,
`support_calls` — once, into the feature store (L13). Point-in-time joins
guarantee no leakage. Cached: unchanged features are skipped.

### 3.3 Training and tracking (Stations 1, 2)
A 50-run hyperparameter sweep trains with `seed_all(42)` (L1); every run logs
params, metrics, and the data hash to tracking (L2). The best run is 0.921
val_acc on the *frozen* eval set.

### 3.4 Registry and packaging (Stations 4, 5)
The winning run registers as `churn-predictor v3` in the registry with its
full lineage (L4). The whole pipeline — scaler + model — is packaged as a
pyfunc artifact with a signature (L5). Golden-output tests pass.

### 3.5 Containerization (Station 6)
A multi-stage Dockerfile builds a slim serving image (L6): pinned deps, the
packaged artifact, healthcheck, env-var config, tagged `churn-serve:v3`.

### 3.6 Serving and optimization (Stations 7, 8)
The endpoint loads the model once at startup, validates inputs via Pydantic
(L7). Benchmark: p99 24ms → ONNX export → p99 6ms → INT8 → p99 2.8ms with a
golden-validated ≤0.5% agreement loss (L8).

### 3.7 CI/CD and promotion (Stations 12, 4)
The eval gate runs in CI: `v3 >= champion v2` on the frozen eval set (L12).
The gate passes → registered as `staging`. Shadow-scoring runs a day (L12),
then canary 5% of traffic.

### 3.8 A/B test (Station 14)
The canary is a real A/B test: retention (the primary metric) is measured on
the 5% treatment vs 5% control. Chi-squared: p=0.02, +1.1% retention,
guardrails green (L14). The verdict — recorded in the registry — is `promote`.

### 3.9 Monitoring (Station 11)
Post-promotion: PSI per feature, prediction drift, delayed-label feedback,
latency SLOs (L11). Alert rules attached; thresholds reviewed quarterly.

### 3.10 Cost (Station 15)
Every station reports cost: training spend (spot + caching), storage (dedup +
cold-store old versions), inference (INT8 + batching). Monthly: `churn-serve`
at $0.32/1M preds vs $1.10/1M pre-optimization (L15).

## 4. The Shared Skeleton (Companion Exercise)

The companion `16-case-study-e2e.py` implements the core loop with mock
versions of every station. Its shape is the pattern to internalize:

```python
def run_release(data_bytes: bytes, config: dict) -> dict:
    """One release through the full pipeline (mock stations)."""
    data_version = content_hash(data_bytes)                # L1, L3
    validate(data_bytes, schema)                           # L10
    metrics = train(data_bytes, seed=config["seed"])       # L1, L2
    assert metrics["val_acc"] >= champion_metrics["val_acc"]  # L12 gate
    version = register("churn-predictor", metrics)         # L4
    artifact = package(version)                            # L5
    ab = ab_test(artifact)                                 # L14
    decision = "promote" if ab["verdict"] == "win" else "hold"
    return {"version": version, "decision": decision, "metrics": metrics}
```

Output (conceptually):
```
{'version': 3, 'decision': 'promote', 'metrics': {'val_acc': 0.921, ...}}
```

## 5. Failure Modes and the Guarding Station

Each station has a characteristic failure — and a *neighboring* station that
guards it:

| Station failure | Guard |
|---|---|
| Unseeded run (L1) | eval gate (L12) can't compare |
| Dataset silently changed (L3) | validation (L10) + monitoring (L11) |
| Corrupt data slips through (L10) | monitoring drift (L11) catches it live |
| Champion eval-set tampering (L12) | frozen, versioned eval set (L3) |
| Package missing preprocessor (L5) | golden-output test (L12) |
| Serving latency regressions (L7) | monitoring latency SLO (L11) |
| A/B peeking (L14) | pre-registered sample size (L14 discipline) |

The system is robust *because* failures are caught by adjacent stations, not
because any single station never fails. That redundancy is the architecture.

## Every Use Case

- **New model release**: the full walkthrough above — the template for any
  model.
- **Model rollback**: promote the previous registry version; monitoring
  confirms recovery (L4 + L11).
- **Data source change**: new version + validation + eval gate before any
  retrain (L3 + L10 + L12).
- **New team / new model**: the same assembly line with different data — the
  stations don't change.
- **LLM system (Phase 9)**: the same line applies to RAG/agents — data
  (corpus) versioning, eval gates on retrieval metrics, serving (LLM
  gateway), monitoring (drift, refusal rate), cost (token budgets).
- **Regulatory audit**: the run records, registry entries, CI gate logs, and
  A/B evidence *are* the audit file (L1/L2/L4/L12/L14).

## Real-World Use Cases for AI Engineers

- **Fintech fraud platform**: ChurnShield's shape, applied to fraud — the
  full assembly line is what the bank's model-risk committee reviews. The
  "weakest link" review: they found the monitoring station (L11) wasn't
  wired to delayed-label feedback and fixed it before the regulator asked.
- **E-commerce ranking**: the same line ships a ranking model weekly. The
  eval gate (L12) + A/B (L14) are what make weekly releases safe — without
  them, a weekly release cadence would be a weekly gamble.
- **Healthcare triage**: the full line, plus the *evidence* requirement — the
  clinical board reviews the registry audit (L4) and monitoring reports (L11)
  quarterly. The assembly line turns "the model is safe" into a demonstrable
  chain of gates.
- **RAG service at a startup (Phase 9 synergy)**: the same architecture with
  different stations: corpus versioning (L3), retrieval eval gates (L12),
  LLM gateway serving (L7), token cost (L15). The team that mastered Phase 8
  deploys a production RAG system in days, not months.
- **ML platform team**: the assembly line is the product — every team in the
  company gets the stations as shared services (registry, feature store,
  monitoring, CI templates). The platform's value is the integrated line.

## Common Mistakes to Avoid

### Mistake 1: Building stations in the wrong order
Serving before packaging, A/B before monitoring — the dependency chain exists
for a reason.

### Mistake 2: Treating stations as optional
"Skipping validation this once" is how silent incidents start. The line is
only as strong as its weakest gate.

### Mistake 3: No run records anywhere
Without L1's records, every downstream audit query is impossible.

### Mistake 4: Manual promotion
Bypassing the gates (L12 + L14) breaks the audit trail and the safety.

### Mistake 5: Forgetting cost
A perfectly built line that loses money on every prediction is a failing
product (L15).

### Mistake 6: Redundancy as "waste"
Validation *and* monitoring *and* A/B look redundant — that redundancy is
the robustness. Each catches what the others miss.

## Best Practices

1. Build stations in dependency order; never skip a gate
2. Make every station write to the shared records (run record, registry, logs)
3. Promote only through the gated path (eval → shadow → A/B)
4. Design the audit trail as a first-class output, not an afterthought
5. Review the whole line quarterly — weakest link analysis
6. Add a new station only when the adjacent guard is insufficient
7. Make each station's failure mode explicit and owned
8. Reuse the line for new models (it's the platform, not a one-off)
9. Extend the same architecture to GenAI systems (Phase 9)
10. Track cost at every station; the line must be affordable

## Complexity and Cost

| Station | Typical cost |
|---|---|
| Validation + versioning | seconds, near-zero |
| Training sweep | hours, the big training bill (L15 levers) |
| Registry + packaging | minutes |
| Serving fleet | the permanent inference bill (L8 levers) |
| Monitoring | low compute, high value |

The assembly line's cost is dominated by two stations (training, inference);
everything else is cheap insurance.

## AI Engineering Relevance

**Where this shows up:** every production ML system you will build or operate.
The ChurnShield shape — data gates → tracked training → gated promotion →
monitored serving → costed operations — is the industry-standard architecture,
whether the model is a tabular classifier or an LLM agent.

| Concept here | Used for |
|---|---|
| Assembly line | thinking about systems, not scripts |
| Station dependencies | correct build order |
| Redundant guards | robustness by design |
| Audit evidence | every gate is a record |

**Scale note:** at one model, the line feels like overhead; at fifty models,
it is the only way to operate. The AI engineer who builds and maintains the
line — not just one station — is the one who runs production ML.

## Practice Exercises

### Exercise 1: Order the Stations (Easy)
Given a shuffled list of the 15 stations, put them in dependency order and
justify three of the edges.

### Exercise 2: Weakest-Link Audit (Medium)
Read a description of an ML system (e.g. "models deployed by copying files,
no monitoring, no eval gate") and list its three weakest links with the
concrete incident each invites.

### Exercise 3: Release Walkthrough (Hard)
Write `run_release(data_bytes, config)` (section 4) with mock stations and
assert: a candidate that fails the eval gate never registers; a candidate that
wins A/B promotes; a data-hash change forces a new version.

### Exercise 4: Architecture Diagram (Medium)
Draw (in markdown or text) the ChurnShield architecture with every station's
input/output, and mark the redundancy pairs (which stations guard which).

## Summary

| Concept | Description |
|---|---|
| Assembly line | the full lifecycle as ordered stations |
| Dependencies | build in the right order |
| Redundant guards | robustness by design |
| Audit trail | every gate is a recorded decision |
| Cost | the third axis, tracked at every station |

Production ML is an assembly line: fifteen practices, ordered by dependency,
guarding each other's failures, all leaving audit records. The ChurnShield
case study is the template — and the same line, with different stations,
carries GenAI systems too (Phase 9). Master the line, and you can build any
ML system.

## Quick Reference

| Task | Idiom |
|---|---|
| Build the line | data → train → registry → serve → monitor → promote |
| Keep gates | eval + shadow + A/B before production |
| Audit | run records + registry + CI logs |
| Fail safe | redundant guards at every boundary |
| Stay cheap | cost at every station (L15) |

## Next Steps

This completes **Phase 8 — MLOps**. Continue to the GenAI phase:
**[Phase 9 — GenAI](../../09-genai/lectures/01-llm-fundamentals-lecture.md)** —
LLM systems built on this same assembly line.
Official docs: https://mlflow.org/docs/latest/, https://dvc.org/doc/start
