# FastAPI — 37: Load Testing

Companion exercise: `37-load-testing.py`

---

## Topic Overview

Before you scale anything, you must know where it breaks. Load testing answers
three questions: how many requests per second can this serve within my latency
budget, where does it saturate, and what is the actual bottleneck? This topic
covers the measurement discipline — percentiles not averages, open vs closed
load models, saturation curves, and capacity planning against a latency SLO.

The single most important habit: **never report an average latency.** The mean
hides the tail. p50/p95/p99 are what users actually feel and what SLOs are
written against.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compute p50/p95/p99 and explain why the mean lies.
2. Distinguish open from closed load models.
3. Find the saturation point where latency explodes.
4. Identify the real bottleneck instead of guessing.
5. Plan capacity against a p99 latency SLO.
6. Interpret a latency distribution, not a single number.
7. Run a minimal load test without external tools.
8. Explain when load tests lie about production.

## Prerequisites

| Need | Where |
|---|---|
| Async/sync endpoints | `32-async-endpoints-deep.py` |
| Caching | `34-caching-strategies.py` |
| Metrics concepts | `44-metrics-prometheus.py` |

## 1. Percentiles — Why Averages Lie

```python
def summarize(latencies):
    lat = sorted(latencies)
    def pct(p): return round(lat[int(p * len(lat))] * 1000, 2)
    return {"mean_ms": ..., "p50_ms": pct(0.5), "p95_ms": pct(0.95),
            "p99_ms": pct(0.99), "max_ms": ...}
```

Output:
```
# 90 requests at 10ms, 9 at 50ms, 1 at 500ms:
# mean: 16.9ms  p50: 10ms  p95: 50ms  p99: 500ms
```

The mean (16.9ms) looks fine; the p99 (500ms) is a disaster for the one user
in a hundred who hits it. SLOs are written against percentiles — "p99 < 200ms"
— because that is what users experience.

## 2. Open vs Closed Load Models

```python
def run_open_model(n):      # fire as fast as possible — saturates the server
    ...
def run_closed_model(n, think_ms):   # each 'user' waits between requests
    ...
```

Output:
```
# open model : latency grows as load exceeds capacity (saturation test)
# closed model: latency stays flat until concurrency spikes (user pacing)
```

- **Open model**: new requests arrive regardless of completion — finds the
  saturation point.
- **Closed model**: each virtual user waits (think time) between requests —
  models real human pacing.

Both have their place; open finds the ceiling, closed validates the realistic
experience.

## 3. Saturation — Where Latency Explodes

```python
def saturation_demo():
    # single server, target 10ms: latency flat until rps > 100, then queueing
```

Output:
```
rps   latency
50     10.0ms
80     10.0ms
100    10.0ms
120    34.0ms     <- queueing begins
150    58.0ms     <- saturation
```

Below capacity, latency is flat. Past it, requests queue and latency blows up
superlinearly. Finding that knee — the max rps at your SLO — is the deliverable
of a load test.

## 4. Finding the Real Bottleneck

Saturation has causes: CPU-bound handlers, a saturated database pool, sync
drivers blocking threads, lock contention, GC pauses. The discipline:

1. Test each layer in isolation (DB, cache, API).
2. Profile the server (cProfile, APM traces).
3. Watch queue depths and pool utilization.
4. Fix the measured bottleneck; re-test.

Never guess — the answer is usually not what the team suspects.

## 5. Capacity Planning Against an SLO

```python
# If p99 must stay < 200ms at 500 rps, and one node handles 300 rps at p99 150ms:
nodes = ceil(500 / 300) + headroom   # 2 nodes, or 3 with 50% headroom
```

Output:
```
# capacity = rps_per_node at SLO x nodes; plan with headroom
```

Capacity planning is math against a measured number: rps-per-node at your
target percentile, times nodes, plus headroom for spikes and failures.

## 6. Common Mistakes to Avoid

### Mistake 1: Reporting averages
```python
# WRONG — "mean latency 16ms" hides the 500ms p99
# CORRECT — p50/p95/p99; the mean is not an SLO
```

### Mistake 2: Testing only the happy path
```python
# WRONG — load test against a cached warm endpoint
# CORRECT — cold cache, errors, and realistic request mix
```

### Mistake 3: Confusing open and closed models
```python
# WRONG — using a saturation test to claim "real users see this"
# CORRECT — open finds the ceiling; closed models the experience
```

### Mistake 4: Load-testing the machine you're serving on
```python
# WRONG — the test client competes with the server for CPU
# CORRECT — separate the load generator from the target
```

### Mistake 5: No saturation curve
```python
# WRONG — one data point at one rps
# CORRECT — sweep rps and record the knee
```

## 7. Best Practices

1. Report p50/p95/p99/max — never the mean alone.
2. Sweep load to find the saturation knee.
3. Use open models to find the ceiling; closed models for realism.
4. Isolate and measure each layer before blaming one.
5. Plan capacity against the p99 SLO with headroom.
6. Test cold and warm paths.
7. Keep the load generator on a separate machine.
8. Repeat runs; report variance across runs.
9. Load-test before every capacity-affecting change.
10. Convert findings into an SLO-based alarm, not a one-off report.

## 8. Complexity and Cost

| Test | Cost | Purpose |
|---|---|---|
| Smoke (1 rps) | seconds | Correctness |
| Percentile summary | O(n log n) | The report |
| Saturation sweep | minutes | The knee |
| Full soak (hours) | expensive | Leaks and degradation |

The cheap tests (smoke, percentile, sweep) find most problems. Soak tests find
memory leaks and slow degradation — worth it before launches.

## 9. AI Engineering Relevance

**Where this shows up:** model-serving endpoints have brutal latency budgets —
LLM streaming, reranking, retrieval. Load testing decides GPU count, cache
strategy, and batching policy.

| Concept here | Used for |
|---|---|
| p99 SLOs | The contract for model-serving APIs |
| Saturation knee | How many concurrent LLM calls a worker handles |
| Bottleneck isolation | Embedding vs retrieval vs generation cost |
| Capacity math | GPU/worker sizing for inference |
| Closed models | Realistic user pacing for chat products |

**Scale note:** in LLM serving, the "latency" of a streamed response is
first-byte + token rate, not total — which changes what a percentile means.
SLOs for chat are written on time-to-first-token and tokens-per-second.

## 10. Summary

| Concept | Description |
|---|---|
| Percentiles | p50/p95/p99 — the honest latency report |
| Open model | Saturates; finds the ceiling |
| Closed model | Realistic user pacing |
| Saturation | The knee where latency explodes |
| Bottleneck | Found by measurement, not guessing |
| Capacity | rps-per-node at SLO x nodes + headroom |

## 11. Quick Reference

| Task | Idiom |
|---|---|
| Percentiles | `sorted(lat)[int(p * len(lat))]` |
| Open load | fire as fast as possible |
| Closed load | add think time between requests |
| Saturation | sweep rps; find the latency knee |
| Capacity | `ceil(target_rps / rps_per_node) + headroom` |
| Report | p50/p95/p99/max, never mean alone |

## 12. Next Steps

Next: **[38 — Auth Deep](38-auth-deep-lecture.md)** — the security layer that load tests stress.

Continues in: **[44 — Metrics Prometheus](44-metrics-prometheus-lecture.md)** — turning load-test findings into alarms.

Official docs: <https://grafana.com/blog/2021/06/09/load-testing-an-api-the-basics/> · <https://locust.io/>
