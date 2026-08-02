# Model Serving — Glossary 07

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Batch | Serving | Grouping requests to amortize inference cost |
| Concurrency | Serving | Number of in-flight requests/workers |
| Cold Load | Serving | Loading the model into memory |
| Hot Path | Serving | The per-request execution after load |
| Latency Budget | Serving | Allocated ms per stage of a request |
| Memory Budget | Serving | RAM cap for model workers |
| p95/p99 | SLO | The 95th/99th percentile latency |
| Serving | MLOps | Exposing a model over an API |
| SLO | SLO | A service-level objective (e.g. p99 < 100ms) |
| Worker | Serving | A process/thread serving requests |

## Detailed Definitions
### Batch
**Definition**: Collecting requests and running them together so fixed
inference cost is shared.
```python
batcher.run_batch([x1, x2, x3])  # one call, three results
```
**Related**: Hot Path

### Concurrency
**Definition**: The number of simultaneous requests a server handles; bounded
by memory and CPU.
**Related**: Worker, Memory Budget

### Cold Load
**Definition**: The one-time cost of loading the model; paid at startup, not
per request.
**Related**: Hot Path

### Hot Path
**Definition**: The code executed for each request after the model is loaded.
**Related**: Cold Load

### Latency Budget
**Definition**: A breakdown of allowed ms: network + preprocess + inference +
postprocess <= SLO.
**Related**: SLO

### Memory Budget
**Definition**: The RAM available for model replicas; workers =
budget / model_gb.
**Related**: Worker

### p95/p99
**Definition**: Latency percentiles; p99 < SLO is the usual production target.
**Related**: SLO

### Serving
**Definition**: Exposing a model over an HTTP (or similar) API.
**Related**: Worker

### SLO
**Definition**: A service-level objective - a quantitative target like "p99
latency under 100ms at 1k rps."
**Related**: Latency Budget

### Worker
**Definition**: A serving process or thread holding its own model copy.
**Related**: Concurrency, Memory Budget

## Key Concepts Summary
### The Serving Triad
- Load once, serve many
- Batch to amortize
- Size workers to memory

### The Budget
- network + preprocess + inference + postprocess <= SLO

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Hot path — ___
2. Batch — ___
3. SLO — ___
4. Worker — ___
5. Latency budget — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=stage-by-stage ms plan, b=per-
request code, c=grouped requests, d=quantitative objective, e=serving process.
