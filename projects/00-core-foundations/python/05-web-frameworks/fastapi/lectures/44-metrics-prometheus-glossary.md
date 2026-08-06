# Metrics with Prometheus — Glossary 44

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Cardinality | Risk | The number of label-value time series |
| Counter | Metric | Monotonic event counter; rate-able |
| Error budget | SLO | The allowed SLO misses over a window |
| Gauge | Metric | A level that goes up and down |
| Golden signals | Framework | Latency, traffic, errors, saturation |
| Histogram | Metric | Bucketed distribution → percentiles |
| Label | Metric | The dimension splitting a metric into series |
| p95 | Statistic | The 95th percentile — the tail that matters |
| Prometheus | System | Pull-based time-series monitoring |
| RED | Framework | Rate, Errors, Duration — per request |
| SLI | SLO | The measured indicator |
| SLO | SLO | The committed target for an SLI |
| USE | Framework | Utilization, Saturation, Errors — per resource |

## Detailed Definitions

### Cardinality
**Definition**: The number of unique label-value combinations, hence time
series. Unbounded labels (user_id, prompt) explode it and kill the TSDB.
**Related**: Label

### Counter
**Definition**: A metric that only increases — requests, tokens, errors.
Rates are derived by querying over time.
**Related**: Gauge

### Error budget
**Definition**: The permitted SLO misses over a window (1% of requests
per 30 days) — spent deliberately, paged on when exhausted.
**Related**: SLO

### Gauge
**Definition**: A metric representing a level that rises and falls —
in-flight requests, queue depth, GPU utilization.
**Related**: Counter

### Golden signals
**Definition**: The four numbers describing service health — latency,
traffic, errors, saturation.
**Related**: RED

### Histogram
**Definition**: A metric recording a distribution into buckets — latency,
token counts — enabling p50/p95/p99 without storing raw samples.
**Related**: p95

### Label
**Definition**: A dimension splitting a metric into series (`path`,
`status`, `model`). Must be a bounded set.
**Related**: Cardinality

### p95
**Definition**: The 95th percentile of a distribution — the tail that
users feel; alert here, never on the mean.
**Related**: Histogram

### Prometheus
**Definition**: The pull-based monitoring system that scrapes `/metrics`
and stores time series with labels.
**Related**: Label

### RED
**Definition**: Rate, Errors, Duration — the per-request view of a
service; the four golden signals for services.
**Related**: USE

### SLI
**Definition**: Service Level Indicator — the measured value ("p95
latency of /generate").
**Related**: SLO

### SLO
**Definition**: Service Level Objective — the committed target for an SLI
("99% of /generate under 2s over 30 days").
**Related**: Error budget

### USE
**Definition**: Utilization, Saturation, Errors — the per-resource view
(GPU, queue) that RED cannot see.
**Related**: RED

## Key Concepts Summary

### The type-to-signal map
- Counter: traffic, errors.
- Gauge: saturation (in-flight, queue, utilization).
- Histogram: latency distributions → p95/p99.

### The two perspectives
- RED: per request — Rate, Errors, Duration.
- USE: per resource — Utilization, Saturation, Errors.
- Both, or a saturated GPU hides behind a healthy request view.

### The disciplines
- Bounded labels or cardinality death.
- Percentiles, never means.
- SLI measured first, SLO committed second, budget spent deliberately.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Monotonic event counter — ___
2. Bucketed distribution — ___
3. Level that goes up and down — ___
4. Latency, traffic, errors, saturation — ___
5. Rate, Errors, Duration — ___
6. Utilization, Saturation, Errors — ___
7. The measured indicator — ___
8. The committed target — ___

**Answers:** 1-counter, 2-histogram, 3-gauge, 4-golden signals, 5-RED,
6-USE, 7-SLI, 8-SLO
