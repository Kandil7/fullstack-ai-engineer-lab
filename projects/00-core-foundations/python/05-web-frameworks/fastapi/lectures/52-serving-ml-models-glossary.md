# Serving ML Models — Glossary 52

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Batch | Serving | N inputs in one model pass |
| Continuous batching | Serving | Adding new requests to an in-flight batch |
| Contract | API | The validated, versioned request/response shape |
| GPU | Hardware | Wins on batches; loses at batch size 1 |
| Load once | Rule | Model loaded at startup, shared across requests |
| Memory math | Capacity | workers × model ≤ RAM |
| Model registry | MLOps | Versioned store of model artifacts |
| Queue | Serving | In-server batching via short collection window |
| Throughput | Metric | Predictions per second (batch-amortized) |
| Versioning | API | /v1, /v2 — never break a live contract |
| Warmup | Rule | Dummy prediction before traffic |
| Worker | Process | One process holding the model in RAM |

## Detailed Definitions

### Batch
**Definition**: Passing N inputs through the model in one call —
amortizing vectorized/GPU work across items.
**Related**: Throughput

### Continuous batching
**Definition**: The in-server technique of adding new requests to an
in-flight batch as slots free — the vLLM-style answer to idle cores.
**Related**: Queue

### Contract
**Definition**: The explicit, validated, versioned shape of the
request/response — Pydantic-enforced arity and ranges.
**Related**: Versioning

### GPU
**Definition**: The accelerator whose per-batch transfer cost amortizes
over items — wins at high batch sizes, loses at batch 1.
**Related**: Batch

### Load once
**Definition**: Loading the model at startup so each worker holds it in
memory for thousands of requests — never per request.
**Related**: Warmup

### Memory math
**Definition**: The capacity computation `workers = floor(ram /
(model + overhead))` — the constraint that binds before cores.
**Related**: Worker

### Model registry
**Definition**: The versioned artifact store models ship from — the
source for reproducible serving (see CI/CD topic 51).
**Related**: Versioning

### Queue
**Definition**: The in-server collection window (e.g. 32 requests or
50ms) that turns scattered singles into batches.
**Related**: Continuous batching

### Throughput
**Definition**: Predictions per second — the metric batching optimizes,
at a small latency-per-item cost.
**Related**: Batch

### Versioning
**Definition**: Adding `/v2/predict` for breaking changes while v1 keeps
serving — never mutating a live contract in place.
**Related**: Contract

### Warmup
**Definition**: A dummy prediction at startup so one-time costs (JIT,
buffers, lazy imports) never hit the first real request.
**Related**: Load once

### Worker
**Definition**: One process running the app — each holds the model, so
the worker count is memory-bounded.
**Related**: Memory math

## Key Concepts Summary

### The three serving rules
- Load once at startup.
- Warmup before readiness.
- Batch for throughput.

### The two contracts
- /predict validated by Pydantic, versioned in the URL.
- Workers = floor(RAM / (model + overhead)).

### The GPU dial
- GPU total = transfer + per-item × batch.
- CPU total = per-item × batch.
- GPU wins only when its total beats CPU at your batch size.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. N inputs in one pass — ___
2. Dummy prediction before traffic — ___
3. Loaded at startup, never per request — ___
4. /v2 for breaking changes — ___
5. workers × model ≤ RAM — ___
6. Predictions per second — ___
7. The validated request shape — ___
8. Wins on batches, loses at batch 1 — ___

**Answers:** 1-batch, 2-warmup, 3-load once, 4-versioning, 5-memory math,
6-throughput, 7-contract, 8-GPU
