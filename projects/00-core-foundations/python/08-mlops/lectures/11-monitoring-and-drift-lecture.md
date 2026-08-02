# MLOps — 11: Monitoring and Drift

## Topic Overview

Monitoring is watching a deployed model in production for the signs that its
performance is degrading — before users or regulators notice. Unlike classic
software monitoring (CPU, memory, error rates), ML monitoring has a unique
problem: **ground truth is often delayed or absent**. A fraud model's true
positive rate is only knowable weeks later when fraud is confirmed; a
recommendation model's "success" is a noisy proxy. So ML monitoring leans on
*proxies*: data drift (input distribution changed), prediction drift
(output distribution changed), and delayed ground-truth feedback loops.

The three classic monitoring layers for an ML system:

1. **System metrics**: latency, throughput, error rate (standard SRE).
2. **Input/data drift**: the serving inputs drifted from training — *the*
   tripwire for silent degradation (Lecture 10's skew detection, now
   continuous).
3. **Output/prediction drift + delayed labels**: the model's decisions changed
   distribution; or labels arrive late and reveal true performance.

Tools: **Evidently** (open-source ML monitoring, drift + quality reports),
**Prometheus + Grafana** (the standard time-series stack), **WhyLabs**,
**Arize**, **SageMaker Model Monitor**. The AI engineer must own the *semantics*
— which drift metric, which threshold, which alert route — not just the dashboards.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Instrument a serving endpoint with request + prediction logging
2. Compute and track data drift metrics (PSI, KL divergence, statistical tests)
3. Detect prediction drift and delayed-label performance degradation
4. Set alert thresholds that balance noise vs missed signals
5. Build a monitoring dashboard with Prometheus-style metrics
6. Distinguish drift (input/output) from performance (ground-truth) monitoring
7. Design the incident response: alert → triage → retrain/rollback

## Prerequisites

| Need | Where |
|---|---|
| Serving | `08-mlops/lectures/07-model-serving-lecture.md` |
| Data validation/skew | `08-mlops/lectures/10-data-validation-lecture.md` |
| Statistics | `07-machine-learning/` |
| Logging | `02-advanced-python/` |

## 1. Instrumentation: Every Prediction Is a Row

Monitoring starts at the endpoint: log the input vector (or a hash/sample),
the prediction, the latency, and a request ID. Without this log, drift and
quality analysis are impossible. Log to structured storage (a table, a
time-series DB) — sampled if volume demands.

```python
import time, hashlib, json

def predict_and_log(features: dict, predict_fn) -> dict:
    t0 = time.perf_counter()
    proba = float(predict_fn(features))
    latency_ms = (time.perf_counter() - t0) * 1000
    record = {
        "ts": int(time.time()),
        "req_id": hashlib.sha1(json.dumps(features, sort_keys=True).encode()).hexdigest()[:12],
        "features": features,          # or a feature hash for privacy
        "proba": proba,
        "latency_ms": latency_ms,
        "model_version": "v2",
    }
    _append(record)                    # structured log to monitoring store
    return record
```

Output (conceptually):
```
Logged: {'ts': ..., 'req_id': 'a3f9...', 'proba': 0.71, 'latency_ms': 8.2, ...}
```

**Privacy rule:** log feature *distributions* or hashes for sensitive data;
raw PII in logs is itself a compliance incident.

## 2. Data Drift Metrics

Data drift asks: *is the live input distribution still the one the model was
trained on?* Three standard metrics:

| Metric | What it measures | Range | Threshold |
|---|---|---|---|
| **PSI** (Population Stability Index) | shift in binned distribution | 0..∞ | <0.1 stable; 0.1-0.25 watch; >0.25 drift |
| **KL divergence** | divergence between distributions | 0..∞ | relative to baseline |
| **KS test / Welch t-test** | statistical difference | p-value | p < 0.05 → drift flag |

```python
import numpy as np

def psi(reference: np.ndarray, live: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index between two 1-D distributions."""
    edges = np.percentile(reference, np.linspace(0, 100, bins + 1))
    ref_h, _ = np.histogram(reference, edges)
    live_h, _ = np.histogram(live, edges)
    ref_p = ref_h / ref_h.sum() + 1e-6
    live_p = live_h / live_h.sum() + 1e-6
    return float(np.sum((live_p - ref_p) * np.log(live_p / ref_p)))

print("PSI:", round(psi(np.random.default_rng(0).normal(50, 10, 10000),
                        np.random.default_rng(1).normal(55, 12, 10000)), 3))
```

Output (conceptually):
```
PSI: 0.183   → watch (0.1–0.25 band)
```

PSI is the finance-industry standard (stable → watch → drift bands), which is
why AI engineers should know it cold.

## 3. Prediction Drift and Delayed Labels

Input drift is a *proxy*; the ground truth is whether predictions are still
good. Two realities:

- **Prediction drift**: the model's output distribution changed (e.g. the
  approval rate went from 15% to 40%). Not always bad, but always a signal to
  inspect.
- **Delayed labels**: for fraud/credit/clinical, true outcomes arrive late.
  Monitor *feedback*: when labels arrive, compute the realized precision/recall
  against the model's earlier predictions.

```python
def feedback_score(predictions: list[tuple[float, bool]]) -> dict[str, float]:
    """Precision at 0.5 after labels arrive (delayed ground truth)."""
    tp = sum(1 for p, y in predictions if p >= 0.5 and y)
    fp = sum(1 for p, y in predictions if p >= 0.5 and not y)
    fn = sum(1 for p, y in predictions if p < 0.5 and y)
    precision = tp / (tp + fp + 1e-9)
    recall = tp / (tp + fn + 1e-9)
    return {"precision": precision, "recall": recall,
            "n_positive": tp + fp, "n_labels": len(predictions)}
```

Output (conceptually):
```
{'precision': 0.42, 'recall': 0.68, 'n_positive': 1200, 'n_labels': 8000}
```

The monitoring loop: instrument → log → compute drift/feedback windows →
alert on thresholds → incident response.

## 4. Alerting: Signal vs Noise

The hardest monitoring decision is the threshold: too tight → alert fatigue
(everyone ignores alerts); too loose → silent degradation. Principles:

- Alert on **sustained** drift (e.g. 3 of 5 recent windows), not single points.
- Escalate by severity: page for "likely degraded" only when proxies agree
  (input drift + prediction drift + feedback drop).
- Log thresholds and review them quarterly — drift thresholds are not physics.

```python
def should_alert(window: list[float], threshold: float = 0.25, need: int = 3) -> bool:
    """Alert only when `need` of the last windows breached the threshold."""
    return sum(1 for v in window[-5:] if v > threshold) >= need

print(should_alert([0.12, 0.18, 0.31, 0.28, 0.33]))   # 3 of last 5 breach
```

Output (conceptually):
```
True   → alert (sustained drift, not a single spike)
```

## 5. The Monitoring Stack

| Layer | Tool | Role |
|---|---|---|
| Endpoint metrics | Prometheus | latency, QPS, error rate counters |
| Dashboards | Grafana | time-series views, alert rules |
| Drift reports | Evidently | PSI/KL/statistical drift per feature |
| Feedback | data warehouse | delayed labels joined to predictions |
| Alerts | PagerDuty/Slack | routed by severity |

Prometheus-style counter/histogram instrumentation is the baseline; Evidently
adds the ML-specific drift semantics on top. The AI engineer's job is the
*semantics layer*: which metrics, thresholds, and routes — the dashboards are
the easy part.

## Every Use Case

- **Fraud/credit models**: delayed-label feedback + approval-rate drift.
- **Recommendation/search**: CTR + prediction-distribution drift (a ranking
  model silently flattening its scores).
- **Healthcare triage**: prediction-drift alerting on clinical models.
- **NLP/LLM (Phase 9)**: input prompt drift, refusal-rate drift, output
  schema-violation rate, cost/latency drift.
- **Multi-tenant SaaS**: per-tenant drift dashboards and quota telemetry.
- **Batch models**: score-distribution comparison between batches.
- **Regulatory**: continuous monitoring evidence is part of model-risk review
  (SR 11-7 requires ongoing monitoring, not just validation at approval time).

## Real-World Use Cases for AI Engineers

- **Fintech fraud**: approval rate drifted from 4% to 12% over a month; PSI on
  `amount` flagged 0.31. The team traced it to a new merchant segment — the
  model wasn't broken, but the monitoring caught the business change the
  operations team hadn't reported. Without it, the fraud loss would have
  grown for weeks.
- **E-commerce ranking**: feedback (CTR) on the new ranking model dropped 8%
  while input drift looked clean. The delayed-label feedback loop caught what
  drift missed: the model was *confident but wrong*. The incident triggered a
  rollback to the previous version.
- **Credit decisioning**: a policy change shifted the applicant pool; PSI
  flagged 3 features in the "watch" band. The team retrained on the new
  distribution *proactively* — before the regulatory review flagged degraded
  performance.
- **LLM customer service (Phase 9)**: refusal-rate drift and response-length
  drift alerted the team to a prompt regression after a model-version bump —
  monitoring the *outputs* of a generative system, not just inputs.
- **Startup**: one engineer sets up Evidently + Prometheus on the first
  production model; the quarterly drift report is the evidence the board and
  auditors ask for.

## Common Mistakes to Avoid

### Mistake 1: No instrumentation
No prediction log → no drift analysis possible → incidents discovered by users.

### Mistake 2: Alerting on single-point spikes
Noise → fatigue → missed real alerts. Alert on sustained windows.

### Mistake 3: Only input drift, no feedback loop
Input drift is a proxy; delayed labels reveal the truth. Monitor both.

### Mistake 4: Treating drift as "the model is broken"
Drift can be a legitimate business change. Triage before panicking — the
monitoring report must support triage, not just alarm.

### Mistake 5: Logging PII into monitoring stores
Raw features can be a compliance incident. Log distributions or hashes.

### Mistake 6: Thresholds as set-and-forget
Review thresholds quarterly; business changes make stale thresholds
meaningless.

## Best Practices

1. Instrument every prediction at the endpoint (request id, features, proba, latency)
2. Log distributions/hashes for sensitive features
3. Track PSI + KL + statistical tests for input drift
4. Track prediction drift and delayed-label feedback separately
5. Alert on sustained windows with severity escalation
6. Give the alert a triage path: run ID, dashboard link, owner
7. Review thresholds quarterly
8. Monitor batch models' score distributions too
9. Version the reference statistics with the model version
10. Make monitoring evidence part of model-risk review (regulatory)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Log every prediction | O(1) per req | O(n) | sample at high volume |
| PSI per feature per window | O(n) | O(1) | pre-bucketed histograms |
| Feedback join | O(n) | O(n) | batch daily joins |
| Dashboard query | O(window) | O(1) | pre-aggregated time buckets |

## AI Engineering Relevance

**Where this shows up:** every production model after deployment — monitoring
is the difference between "users report a problem" and "you catch it in the
drift dashboard on Tuesday".

| Concept here | Used for |
|---|---|
| Prediction log | the raw material of all analysis |
| PSI/KL drift | early tripwire for silent degradation |
| Delayed labels | the truth behind the proxies |
| Sustained-window alerts | signal without fatigue |

**Scale note:** at 1M predictions/day, sampled logging (1%) still yields 10k
records/day — plenty for drift statistics. At any scale, monitoring is the
*only* thing standing between a silently degraded model and your users.

## Practice Exercises

### Exercise 1: PSI Calculator (Easy)
Implement `psi(reference, live, bins)` (section 2) and verify: identical
distributions → PSI ≈ 0; shifted distribution → PSI > 0.25.

### Exercise 2: Feedback Loop (Medium)
Write `feedback_score(predictions)` that computes precision/recall once labels
arrive; assert the scoring is correct on a known 10-sample set.

### Exercise 3: Alert Policy (Medium)
Implement `should_alert(window, threshold, need)` for sustained drift; test
that a single spike does not alert but 3-of-5 sustained does.

### Exercise 4: Monitoring Planner (Hard)
Design a monitoring plan for a deployed churn model: list the metrics
(latency, PSI per feature, approval-rate drift, feedback precision), the
thresholds, the alert routes, and the triage playbook — then implement the
metric-computation functions and the alerting decision.

## Summary

| Concept | Description |
|---|---|
| Instrumentation | every prediction is a logged record |
| Data drift | PSI/KL/KS: is the input still the trained one? |
| Prediction drift | did the model's outputs shift? |
| Delayed labels | the ground truth arriving late |
| Alert policy | sustained-window, severity-escalated |

Monitoring is the last line of defense between a model and its users. The AI
engineer's craft is the semantics — the right proxies, thresholds, and
triage paths — that turn dashboards into early-warning systems instead of
post-incident archaeology.

## Quick Reference

| Task | Idiom |
|---|---|
| Log prediction | structured record: ts, req_id, features, proba, latency |
| Compute PSI | binned distribution shift, stable/watch/drift bands |
| Drift alert | 3-of-5 windows > threshold |
| Feedback | join delayed labels → precision/recall |
| Dashboard | Prometheus counters + Grafana, Evidently reports |

## Next Steps

Next: **[12 CI/CD for ML](12-ci-cd-for-ml-lecture.md)** — automating the path
from code change to deployed model with quality gates.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://www.evidentlyai.com/, https://prometheus.io/docs/
