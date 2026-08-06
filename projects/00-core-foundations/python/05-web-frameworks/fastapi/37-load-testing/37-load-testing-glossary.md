# Load Testing — Glossary 37

Companion lecture: `37-load-testing-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Bottleneck | Analysis | The measured layer limiting throughput |
| Capacity planning | Analysis | rps-per-node x nodes + headroom against an SLO |
| Closed model | Methodology | Users wait (think time) between requests |
| Cold path | Methodology | Requests that miss caches — the expensive reality |
| First-byte latency | Metric | Time to the first response bytes (streaming SLO) |
| Knee | Analysis | The saturation point where latency explodes |
| Latency distribution | Metric | The full shape of response times, not one number |
| Load generator | Tooling | The process creating test requests |
| Mean latency | Metric | The average — hides the tail, never an SLO |
| Open model | Methodology | Requests fire regardless of completion |
| p50 | Metric | Median latency |
| p95 | Metric | Latency exceeded by 5% of requests |
| p99 | Metric | Latency exceeded by 1% of requests — the SLO standard |
| Saturation | Analysis | Load beyond capacity; queueing and latency blowup |
| SLO | Metric | Service-level objective — e.g. p99 < 200ms |
| Soak test | Methodology | Long-running load test for leaks/degradation |
| Think time | Methodology | The wait between a user's requests |

## Detailed Definitions

### Bottleneck
**Definition**: The layer (CPU, DB pool, threadpool, lock) that measurement
shows limiting throughput — found by isolating layers, never by guessing.
**Related**: Saturation

### Capacity planning
**Definition**: Computing nodes needed as `ceil(target_rps / rps_per_node at
SLO) + headroom` using measured per-node capacity.
**Related**: SLO

### Closed model
**Definition**: A load model where each virtual user waits (think time)
between requests — realistic human pacing; latency stays flat until
concurrency spikes.
**Related**: Open model

### Cold path
**Definition**: A request that misses every cache — the expensive, realistic
case load tests must include alongside warm hits.
**Related**: Warm path

### First-byte latency
**Definition**: Time until the first bytes of a response arrive — the SLO
metric for streamed LLM responses.
**Related**: SLO

### Knee
**Definition**: The rps value where latency transitions from flat to
exploding — the saturation point found by sweeping load.
**Related**: Saturation

### Latency distribution
**Definition**: The full shape of response times (percentiles, histogram)
rather than a single average.
**Related**: p99

### Load generator
**Definition**: The tool/process creating test requests — must run on a
separate machine so it doesn't compete with the server.
**Related**: Load test

### Mean latency
**Definition**: The arithmetic average of latencies — hides the tail and is
never an SLO; report percentiles instead.
**Related**: p99

### Open model
**Definition**: A load model firing requests as fast as possible regardless
of completion — saturates the server and finds the ceiling.
**Related**: Closed model

### p50
**Definition**: The median latency — half of requests are faster, half slower.
**Related**: p95, p99

### p95
**Definition**: The latency exceeded by 5% of requests — the tail users feel
as "slow".
**Related**: p99

### p99
**Definition**: The latency exceeded by 1% of requests — the standard SLO
percentile.
**Related**: SLO

### Saturation
**Definition**: The state past capacity where requests queue and latency
grows superlinearly — the ceiling a load test must find.
**Related**: Knee

### SLO
**Definition**: Service-Level Objective — a measurable target such as
"p99 < 200ms at 500 rps" that capacity planning is done against.
**Related**: p99

### Soak test
**Definition**: A long-duration load test (hours) that reveals memory leaks,
connection leaks, and slow degradation invisible in short runs.
**Related**: Load test

### Think time
**Definition**: The simulated wait between a user's requests in a closed
model — makes load realistic.
**Related**: Closed model

## Key Concepts Summary

### The report
- p50/p95/p99/max — never the mean alone.
- SLOs are percentile-based because percentiles are what users feel.
- Report variance across runs.

### The models
- Open: fire without waiting — finds the saturation ceiling.
- Closed: think time between requests — models real users.
- Cold and warm paths both matter.

### The analysis
- Sweep load to find the knee.
- Isolate layers to find the true bottleneck.
- Capacity = rps-per-node at SLO x nodes + headroom.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The latency exceeded by 1% of requests — ___
2. Requests fire regardless of completion — ___
3. Users wait between requests — ___
4. The saturation point where latency explodes — ___
5. The measured layer limiting throughput — ___
6. The average that hides the tail — ___
7. A long test revealing leaks — ___
8. rps-per-node x nodes + headroom — ___

**Answers:** 1-p99, 2-open model, 3-closed model, 4-knee, 5-bottleneck,
6-mean latency, 7-soak test, 8-capacity planning
