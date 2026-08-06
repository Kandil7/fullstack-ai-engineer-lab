# FastAPI — 44: Metrics with Prometheus

## Topic Overview

Logs tell you what happened; metrics tell you how the service is doing
*right now*. The **four golden signals** — latency, traffic, errors,
saturation — are the same four numbers that decide whether an LLM service
is healthy. Three metric types map to them: **counters** (monotonic),
**gauges** (levels), **histograms** (distributions). Two frameworks tell
you what to instrument: **RED** (Rate, Errors, Duration — per request)
and **USE** (Utilization, Saturation, Errors — per resource). Two
disciplines keep metrics honest: **bounded label cardinality** (an
unbounded label kills the time-series database) and **SLOs** (an SLI
measured against a target, with an error budget spent deliberately).

The mental model: a counter counts events, a gauge measures a level, a
histogram records a distribution — and every metric is defined by its
labels, so label design is metric design.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose counter vs gauge vs histogram for a signal.
2. Implement the four golden signals with the prometheus client.
3. Apply RED (per request) and USE (per resource) perspectives.
4. Avoid cardinality explosions with bounded label sets.
5. Define SLIs, SLOs, and error budgets.

## Prerequisites

| Need | Where |
|---|---|
| FastAPI app | `01-introduction.py` |
| Structured logging | `43-structured-logging-lecture.md` |
| Background knowledge | `/metrics` scraping model |

---

## 1. The three metric types

```python
REQUESTS = Counter("http_requests_total", "...", ["path", "status"])
IN_FLIGHT = Gauge("http_in_flight", "...")
LATENCY = Histogram("http_request_duration_seconds", "...", buckets=(...))
```

- **Counter**: only increases — requests, tokens, errors. Query its rate.
- **Gauge**: up and down — in-flight requests, queue depth, GPU utilization.
- **Histogram**: distribution with buckets — latency, token counts. Gives
  p50/p95/p99 without storing raw samples.

## 2. The four golden signals

| Signal | Type | Example |
|---|---|---|
| Latency | histogram | request duration, alert on p95/p99 |
| Traffic | counter | requests per second |
| Errors | counter | 5xx per second, per endpoint |
| Saturation | gauge | in-flight, queue depth, utilization |

Never average latency — the p50 hides the tail that kills users. Alert on
percentiles.

## 3. RED and USE

- **RED** — per *request*: Rate, Errors, Duration. The service view.
- **USE** — per *resource*: Utilization, Saturation, Errors. The infra view.

An LLM service exposes both: RED on `/generate`, USE on the GPU and the
queue. A service can look perfect under RED while the GPU queue grows
unbounded — saturation is the signal RED cannot see.

## 4. Cardinality — the silent killer

Every unique label value creates a new time series. `user_id` or `prompt`
as a label means a new series per user per prompt — the TSDB's memory
grows without bound while the app looks healthy. Labels must be **bounded
sets**: path, status, model, tenant. Free-form text belongs in log lines,
never in metric labels. Rule of thumb: a label whose value set you cannot
count on one hand (or a small config) is a cardinality bomb.

## 5. SLI, SLO, error budget

- **SLI**: the measured indicator — "p95 latency of /generate".
- **SLO**: the target — "99% of /generate requests under 2s over 30 days".
- **Error budget**: the allowed misses — 1% of requests over 30 days.
  Spending the budget deliberately (releasing, experimenting) is the
  point; exceeding it is the pager.

## Common Mistakes to Avoid

### Mistake 1: Unbounded labels
```python
# WRONG - Counter(..., ["user_id"])  -> one series per user
# CORRECT - bounded sets: path, status, model, tenant
```

### Mistake 2: Average latency
```python
# WRONG - alerting on mean — the p99 can be 10x the mean
# CORRECT - histogram buckets; alert on p95/p99
```

### Mistake 3: No error counters
```python
# WRONG - "the service is up" while every call 500s
# CORRECT - counter per path+status; alert on error rate
```

### Mistake 4: RED-only observability
```python
# WRONG - requests look fine while the GPU queue saturates
# CORRECT - USE on resources alongside RED on requests
```

### Mistake 5: SLOs without SLIs
```python
# WRONG - a target with nothing measured against it
# CORRECT - instrument the SLI first, then commit the SLO
```

## Best Practices

1. Counter/gauge/histogram matching the signal's shape.
2. Bounded label sets; free-form text in logs.
3. Alert on percentiles, never means.
4. RED per request + USE per resource.
5. Define SLIs first; commit SLOs with error budgets.
6. Export `/metrics` and scrape it; test the scrape in CI.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Counter inc | nanoseconds | — |
| Histogram observe | O(buckets) | — |
| Unbounded labels | memory × series | bounded label sets |
| Scrape /metrics | per-interval | — |

Metrics are nearly free at the source; the cost is entirely in
cardinality — which is a design decision, not a hardware one.

## AI Engineering Relevance

**Where this shows up:** LLM gateways (tokens, cost, latency per model),
GPU clusters (utilization, queue depth), RAG pipelines (retrieval
latency, quality proxies).

| Concept here | Used for |
|---|---|
| histogram latency | per-model p95 on /generate |
| counter tokens | usage metering per tenant |
| gauge in-flight | concurrency caps and queue depth |
| USE on GPU | saturation before it becomes latency |
| SLO | "99% of generations under 2s" |

**Scale note:** at 10k rps the histogram buckets decide storage — 7
buckets × bounded labels is tiny; a user_id label is a database death
warrant.

## Practice Exercises

### Exercise 1: Type choice  (Difficulty: Easy)
For five signals (errors, in-flight, latency, queue depth, tokens) pick
the type; assert the mapping.

### Exercise 2: Histogram percentiles  (Difficulty: Easy)
Observe known values; assert bucket counts and the sum/count math.

### Exercise 3: Golden signals  (Difficulty: Medium)
Run a simulated workload; compute the four signals; assert sane bounds.

### Exercise 4: Cardinality audit  (Difficulty: Medium)
Given label sets, compute series counts; assert bounded sets stay small.

### Exercise 5: SLO checker  (Difficulty: Medium)
Implement SLI-vs-SLO checks; assert pass/fail across error and latency
dimensions.

### Exercise 6: /metrics endpoint  (Difficulty: Hard)
Wire prometheus into a FastAPI app with a /metrics route; assert the
text-format output contains the counter and histogram families.

## Summary

| Concept | Description |
|---|---|
| counter | monotonic events (rate-able) |
| gauge | levels up and down |
| histogram | distributions → percentiles |
| golden signals | latency, traffic, errors, saturation |
| RED/USE | request view + resource view |
| cardinality | bounded labels or TSDB death |
| SLI/SLO | measured indicator vs committed target |

Metrics are the service's vital signs. Choose the right type, keep labels
bounded, watch both requests and resources, and commit SLOs you can
actually measure.

## Quick Reference

| Task | Idiom |
|---|---|
| Count events | `Counter(name, doc, ["path","status"]).labels(...).inc()` |
| Level | `Gauge(...).set(v)` / `.inc()` / `.dec()` |
| Latency | `Histogram(..., buckets=(...)).observe(t)` |
| p95 | `histogram_quantile(0.95, rate(...))` in PromQL |
| Bounded labels | path, status, model, tenant |
| SLO check | `error_rate <= target and p95 <= target` |

## Next Steps

Next: **[45 — Tracing with OpenTelemetry](45-tracing-opentelemetry-lecture.md)** —
latency as a tree, end to end, across services.

Continues in: **[46 — Health & Readiness](46-health-and-readiness-lecture.md)** —
the endpoints that let orchestrators decide your fate.

Official docs:
- Prometheus metric types: https://prometheus.io/docs/concepts/metric_types/
- SRE workbook (SLI/SLO): https://sre.google/workbook/implementing-slos/
