# MLOps — 15: Cost Optimization

## Topic Overview

Cost optimization for ML is managing the recurring price of training,
storage, and inference so that model value exceeds model spend. ML cost is
special: it is **recurring and compounding** — every retraining run, every
serving request, every stored dataset version is a bill that never stops. An
ML engineer who ships models without thinking about cost ships models that
quietly drain the company.

The cost structure has three pillars:
1. **Training compute**: GPU/CPU hours per run × number of runs (experiments!).
2. **Storage**: datasets, model versions, artifacts — content-addressed
   storage (Lecture 03) dedupes, but history grows.
3. **Inference**: per-request cost × traffic — the *permanent* bill (Lectures
   07–08: quantization, batching, caching).

Why this matters for an AI engineer: cost is a *design property*, not an
afterthought. The levers — right-sizing, spot/preemptible instances,
quantization (Lecture 08), batching, caching (Lecture 18 in Phase 9),
sharing infrastructure (feature stores, Lecture 13) — are all engineering
decisions the AI engineer controls. This lecture is the playbook: measure
unit costs, find the multipliers, apply the cheapest lever.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Break an ML system's cost into training / storage / inference buckets
2. Compute unit costs (cost per training run, per 1M predictions)
3. Apply the biggest levers: spot instances, right-sizing, quantization, batching
4. Estimate experiment-hygiene savings (caching, dedup, fewer wasted runs)
5. Design a cost budget with alerts and dashboards
6. Justify a cost decision with numbers to a manager
7. Know when NOT to optimize (optimization itself costs time)

## Prerequisites

| Need | Where |
|---|---|
| Inference optimization | `08-mlops/lectures/08-inference-optimization-lecture.md` |
| Data versioning (dedup) | `08-mlops/lectures/03-data-versioning-lecture.md` |
| Serving | `08-mlops/lectures/07-model-serving-lecture.md` |
| Feature stores | `08-mlops/lectures/13-feature-stores-lecture.md` |
| Orchestration/caching | `08-mlops/lectures/09-pipeline-orchestration-lecture.md` |

## 1. The Three Cost Pillars and Their Unit Costs

| Pillar | Unit cost | Example |
|---|---|---|
| Training | $/GPU-hour × hours | 100 runs × 2h × $3 = $600/experiment-day |
| Storage | $/GB-month × GB | 500 dataset versions × 10GB = 5TB × $0.023 = $115/mo |
| Inference | $/1M predictions × rate | 10M preds/day × $0.80/1M = $8/day = $240/mo |

The arithmetic starts with **unit costs**. Compute them before optimizing:

```python
def unit_costs(gpu_hr_cost: float, run_hours: float, runs_per_month: int,
               storage_gb: float, gb_cost: float, preds_per_month: int,
               pred_cost_per_million: float) -> dict[str, float]:
    return {
        "training": gpu_hr_cost * run_hours * runs_per_month,
        "storage": storage_gb * gb_cost,
        "inference": preds_per_month / 1e6 * pred_cost_per_million,
    }

print(unit_costs(3.0, 2.0, 30, 5000, 0.023, 300_000_000, 0.80))
```

Output (conceptually):
```
{'training': 180.0, 'storage': 115.0, 'inference': 240.0}
```

With numbers like these, the optimization priority is obvious: inference is
the biggest recurring line, then training, then storage — spend effort where
the money is.

## 2. Training Cost: The Experiment Multiplier

Training cost scales with *runs*, not just *models*. The levers:

| Lever | Saving | Mechanism |
|---|---|---|
| Spot/preemptible instances | 60–90% off GPU | interrupts tolerated with checkpointing |
| Caching (Lecture 09) | skip unchanged steps | content-hash cache |
| Early stopping | 30–70% of run hours | stop converged runs early |
| Smaller models / distillation | 5-10x less compute | Lecture 08 |
| Experiment budget caps | stop runaway sweeps | quota per experiment |

```python
def training_budget(n_runs: int, run_hours: float, gpu_cost: float,
                    cache_hit_rate: float = 0.0) -> dict[str, float]:
    """With a cache hit rate, many runs cost ~0 compute."""
    billed_hours = run_hours * n_runs * (1 - cache_hit_rate)
    cost = billed_hours * gpu_cost
    return {"billed_hours": billed_hours, "cost": round(cost, 2)}

print(training_budget(30, 2.0, 3.0, cache_hit_rate=0.6))
```

Output (conceptually):
```
{'billed_hours': 24.0, 'cost': 72.0}   (vs $180 uncached)
```

**The highest-leverage habit:** before launching a 100-run sweep, ask "how
many of these runs will I actually use?" Caching, early stopping, and
parameter budgets convert wasted runs into saved dollars.

## 3. Storage Cost: Version History Compounds

Storage grows with every dataset version, model version, and artifact.
Levers: content-addressed dedup (Lecture 03 — same bytes stored once),
compression (Parquet/arrow vs CSV), lifecycle policies (archive old versions
to cold storage), and pruning stale experiments.

```python
def storage_forecast(versions_per_month: int, avg_gb: float, months: int,
                     gb_cost: float = 0.023) -> float:
    """Compounding storage bill with dedup savings applied."""
    total_gb = versions_per_month * avg_gb * months * 0.35  # ~65% dedup
    return round(total_gb * gb_cost, 2)

print(storage_forecast(20, 10, 12))
```

Output (conceptually):
```
193.2   (deduped 12-month history — vs $552 naive)
```

The discipline: **history is valuable, but not all of it is hot.** Cold-store
archived versions; keep the hot path lean.

## 4. Inference Cost: The Permanent Bill

Inference is the cost that never sleeps — it is paid on every request,
forever. The levers are exactly Lecture 08's: quantization (FP16/INT8),
ONNX optimization, batching, caching, and right-sizing instances. The
compounding effect:

```python
def inference_savings(preds_per_month: int, cost_per_million: float,
                      improvement: float) -> float:
    """Monthly savings from an X% cost-per-prediction improvement."""
    before = preds_per_month / 1e6 * cost_per_million
    return round(before * improvement, 2)

print("savings from 3x inference speedup:", inference_savings(300_000_000, 0.80, 0.66))
```

Output (conceptually):
```
savings from 3x inference speedup: 158.4 per month
```

At 300M predictions/month, a 3x speedup is ~$160/month — and it compounds
with every traffic increase. For LLMs (Phase 9), this is the difference
between a viable product and a money pit (caching + batching + cheaper
models).

## 5. Right-Sizing and Spot Instances

- **Right-size**: profile memory/GPU utilization; a model using 15% GPU is a
  candidate for a smaller instance or more batching.
- **Spot/preemptible**: 60–90% off, but reclaimable. Safe when work is
  checkpointed (Lecture 09) or idempotent (retryable).

```python
def instance_recommendation(gpu_util: float, latency_ok: bool) -> str:
    """Right-size by utilization and latency headroom."""
    if gpu_util < 0.3 and latency_ok:
        return "downsize or share GPU (batching)"
    if gpu_util > 0.85:
        return "upgrade or batch better (saturated)"
    return "well-sized"

print(instance_recommendation(0.18, True))
```

Output (conceptually):
```
downsize or share GPU (batching)
```

## 6. Budgets, Dashboards, and Alerts

Cost optimization without visibility is guesswork. Track per-model, per-pipeline
cost; set budgets with alerts at thresholds (50%/80%/100% of monthly budget).
Every training run should log its cost (GPU hours × rate) as a metric
(Lecture 02) — then "how much did experiments cost this month?" is a query.

```python
def budget_status(spent: float, budget: float) -> dict:
    pct = spent / budget
    alert = "OK" if pct < 0.5 else ("WARN" if pct < 0.8 else "ALERT")
    return {"spent": round(spent, 2), "budget": budget,
            "pct": round(pct, 2), "alert": alert}

print(budget_status(140.0, 200.0))
```

Output (conceptually):
```
{'spent': 140.0, 'budget': 200.0, 'pct': 0.7, 'alert': 'WARN'}
```

## Every Use Case

- **GPU experiment farms**: spot instances + caching + early stopping.
- **High-traffic serving**: quantization + batching (the permanent bill).
- **Multi-version storage**: dedup + lifecycle policies on dataset/model versions.
- **LLM products (Phase 9)**: prompt caching, model tiering (cheap model for
  easy queries), batching.
- **SaaS multi-tenant**: per-tenant cost attribution for pricing decisions.
- **Fintech/model-risk**: cost per decision tracked for profitability.
- **Capacity planning**: forecasting storage/inference growth before the bill
  surprises finance.

## Real-World Use Cases for AI Engineers

- **ML platform at a fintech**: the monthly bill had training at 60% of cost —
  the team moved experiments to spot GPUs with checkpointing (Lecture 09),
  cut experiment waste with caching, and training spend dropped 45% with
  zero impact on results. The CFO's question became "how much more can we
  train?"
- **E-commerce serving**: the ranking model's inference bill was the biggest
  line. ONNX + INT8 (Lecture 08) cut cost-per-prediction 3x; the saved budget
  funded a second model. Cost optimization *paid for* capability.
- **RAG service (Phase 9)**: embedding cost was exploding with re-indexing.
  Incremental indexing (Lecture 03 hashes) + batching cut embedding compute
  70%; LLM cost dropped via prompt caching (Lecture 18). The service's
  cost-per-query became the product's margin.
- **Startup**: 2 engineers, one GPU budget. The cost dashboard (spent vs
  budget per model) keeps the founders honest — the "ALERT" at 80% triggers
  a cleanup of stale experiment versions instead of a surprise bill.
- **Healthcare**: a multi-tenant imaging platform attributes storage cost per
  hospital; dedup + cold-storage policies keep per-tenant costs predictable
  for contracts.

## Common Mistakes to Avoid

### Mistake 1: Optimizing before measuring
"No idea where the money goes, let's buy cheaper GPUs" — measure unit costs
first.

### Mistake 2: Ignoring the experiment multiplier
One "cheap" run × 500 experiments is the real training bill. Cap sweeps.

### Mistake 3: Storage hoarding
Every version kept hot forever. Cold-store archives; dedupe by content hash.

### Mistake 4: Treating inference cost as fixed
Quantization/batching/caching are *recurring* savings — the highest-leverage
line.

### Mistake 5: No budget or alerts
Costs drift silently. Set budgets, log cost per run (Lecture 02), alert at
thresholds.

### Mistake 6: Over-optimizing
An hour spent saving $5/month is a waste. Apply the 80/20: fix the big lines
first.

## Best Practices

1. Measure unit costs before optimizing (training/storage/inference buckets)
2. Apply the biggest lever first (usually inference or experiment waste)
3. Use spot instances for checkpointed/idempotent training
4. Cache unchanged pipeline steps and dataset hashes
5. Quantize and batch serving models (Lecture 08)
6. Dedupe storage by content hash; cold-store archives
7. Log cost as a metric per run; budget + alert per model
8. Right-size instances by utilization, not habit
9. Set experiment caps (max runs, max hours per sweep)
10. Review the cost dashboard monthly with the team

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Unit-cost measurement | minutes | O(1) | — |
| Quantization | minutes-hours | 0.25x | FP16 first |
| Spot instances | config | — | checkpoint + retry |
| Storage lifecycle | config | — | cold-store archives |
| Cost dashboards | setup | O(1) | per-run cost metric + spreadsheet |

## AI Engineering Relevance

**Where this shows up:** every GPU bill, storage bucket, and inference fleet —
cost is the third axis of ML quality (after performance and reliability).

| Concept here | Used for |
|---|---|
| Unit costs | knowing where the money goes |
| Experiment caps | the training multiplier |
| Quantize/batch/cache | the permanent inference bill |
| Budgets + alerts | no silent cost drift |

**Scale note:** ML cost compounds with traffic and history — the levers applied
early compound too. A 3x inference improvement today is a 3x improvement on
next year's 10x traffic. Cost engineering is the AI engineer's permanent
second job.

## Practice Exercises

### Exercise 1: Unit-Cost Breakdown (Easy)
Implement `unit_costs` and rank the three pillars for a given scenario; state
the priority of effort.

### Exercise 2: Experiment Budget (Medium)
Write `training_budget(n_runs, run_hours, gpu_cost, cache_hit_rate)` and show
the savings of 50% caching + early stopping on a 40-run sweep.

### Exercise 3: Inference Savings (Medium)
Write `inference_savings(preds, cost_per_million, improvement)` and compare
3x speedup vs 10x speedup monthly savings at 500M preds/month.

### Exercise 4: Cost Policy (Hard)
Implement `cost_policy(runs, storage_versions, preds, budget)` that: caps
runs via caching, cold-stores versions older than N months, and alerts when
the projection exceeds budget — with unit tests for the three behaviors.

## Summary

| Concept | Description |
|---|---|
| Unit costs | measure before optimizing |
| Training | spot + caching + caps on the experiment multiplier |
| Storage | dedup + lifecycle on version history |
| Inference | quantize + batch + cache the permanent bill |
| Budgets | track, alert, review monthly |

Cost optimization is the third pillar of production ML: models must not only
be correct and reliable, but affordable at scale. The playbook is simple —
measure unit costs, apply the biggest lever, track budgets — and the savings
compound on every future run and request.

## Quick Reference

| Task | Idiom |
|---|---|
| Measure | unit-cost table: training/storage/inference |
| Train cheaper | spot instances + caching + early stopping |
| Serve cheaper | INT8/ONNX + batching (Lecture 08) |
| Store cheaper | dedup + cold-store archives |
| Stay honest | per-run cost metric + budget alerts |

## Next Steps

Next: **[16 Case Study: E2E](16-case-study-e2e-lecture.md)** — the full
lifecycle, from data to production, in one integrated case study.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/
