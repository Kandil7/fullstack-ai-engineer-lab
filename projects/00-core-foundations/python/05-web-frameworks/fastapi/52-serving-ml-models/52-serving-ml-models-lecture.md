# FastAPI — 52: Serving ML Models (STAR)

## Topic Overview

The capstone of the FastAPI track: a real model behind a real endpoint,
with memory measured. Three rules dominate serving:

1. **Load once at startup** — loading a GB-scale model per request is a
   self-inflicted DoS.
2. **Warmup before traffic** — the first prediction pays one-time costs
   (buffers, lazy imports, JIT) that should never hit a real user.
3. **Batch for throughput** — vectorized/GPU cores amortize across a
   batch; one call for 32 items beats 32 calls.

Two more decisions complete the picture: **version the /predict
contract** (add v2, never break v1) and **do the memory math** — every
worker holds the model, so workers × model = RAM before a single request
(connecting to topic 49). GPU vs CPU is the final dial: GPUs win on
batches, where transfer cost is amortized, and lose at batch size 1.

The mental model: serving is capacity math — time to load, memory per
worker, throughput per batch — and the endpoint is the contract that
exposes the model without exposing its internals.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Load a model once at startup and share it across requests.
2. Warm up before the first real request.
3. Design a versioned, validated `/predict` contract.
4. Add batching and explain the throughput math.
5. Compute worker capacity from model memory.

## Prerequisites

| Need | Where |
|---|---|
| Pydantic v2 | `26-pydantic-v2-deep-lecture.md` |
| Testing | `20-testing.py`, `42-security-testing.py` |
| Workers/memory | `49-uvicorn-gunicorn-lecture.md` |

---

## 1. Load once at startup

```python
MODEL = joblib.load("model.joblib")   # module level: once, at import

@app.post("/v1/predict")
def predict(req: PredictRequest):
    X = np.asarray(req.features).reshape(1, -1)
    return {"prediction": int(MODEL.predict(X)[0])}
```

Loading per request reads GB from disk and deserializes for a single
call. Loading at module scope means each worker loads it once at boot and
serves thousands of requests with it in memory. The model is a shared,
immutable, read-only resource.

## 2. Warmup

The first prediction can trigger lazy allocation and one-time
initialization. Fire a dummy prediction at startup so the first *real*
request is already fast:

```python
MODEL.predict(np.zeros((1, n_features)))   # warmup at startup
```

Warmup belongs in the startup lifecycle (topic 25/46) — before the
readiness probe turns green, so traffic never meets a cold model.

## 3. The /predict contract

The contract is explicit, validated, and versioned:

```python
class PredictRequest(BaseModel):
    features: list[float] = Field(min_length=8, max_length=8)

@app.post("/v1/predict")
def predict(req: PredictRequest): ...
```

- Pydantic enforces the input shape (wrong arity → 422, not a cryptic
  numpy error).
- The version lives in the URL and the response: breaking changes create
  `/v2/predict`; v1 keeps serving old clients.
- Never change a contract in place — that is how clients break silently.

## 4. Batching

Vectorized cores want batches. A batch endpoint takes N rows and returns
N predictions in one pass:

```python
@app.post("/v1/predict_batch")
def predict_batch(reqs: list[PredictRequest]):
    X = np.asarray([r.features for r in reqs])
    return [int(p) for p in MODEL.predict(X)]
```

Latency per item rises slightly; throughput rises a lot. In-server
queues (collect 32 requests or 50ms, then flush) trade latency for
throughput — the standard trick for GPU utilization.

## 5. Memory per worker

Every worker holds the model: 4 workers × 2GB = 8GB before one request.

```python
workers = floor(ram / (model_mb + overhead_mb) / 1000)
```

Measure the real model memory (tracemalloc, RSS via psutil) and compute
capacity — the memory math from topic 49 applied to serving. OOM
restarts under load are the symptom of skipping this.

## 6. GPU vs CPU

- **CPU**: fast singles, low cost, no transfer overhead — the default
  for latency-sensitive low-volume.
- **GPU**: transfer cost is per-call; it amortizes only over batches.
  GPU wins at batch 128, loses at batch 1.

The decision is batch-size × utilization, not "GPU is faster".

## Common Mistakes to Avoid

### Mistake 1: Loading per request
```python
# WRONG - joblib.load inside the endpoint = GB reads per call
# CORRECT - load at startup; workers inherit it
```

### Mistake 2: No warmup
```python
# WRONG - the first user pays JIT/cache costs
# CORRECT - warmup prediction before readiness turns green
```

### Mistake 3: No batching
```python
# WRONG - vectorized cores idle at batch size 1
# CORRECT - batch endpoint or in-server queue
```

### Mistake 4: Ignoring memory per worker
```python
# WRONG - workers × model > RAM = OOM under load
# CORRECT - memory math before setting worker count
```

### Mistake 5: Breaking the contract in place
```python
# WRONG - changing /predict's shape, breaking clients
# CORRECT - add /v2; keep v1 serving
```

## Best Practices

1. Load once at startup; the model is shared read-only state.
2. Warmup before readiness; traffic never meets a cold model.
3. Versioned, validated /predict contracts.
4. Batch where throughput matters; measure both.
5. Compute workers from measured model memory.
6. GPU for high-utilization batches, CPU for low-volume latency.
7. Monitor model-serving metrics (topic 44): p95, tokens, errors.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Model load | once per worker boot | — |
| Per-request predict | O(features × model) | batching |
| Batch predict | amortized per item | — |
| Workers × model | RAM × workers | fewer workers + batching |
| GPU transfer | per batch, not per item | larger batches |

The serving cost function is memory × workers plus batch-size efficiency.
Both are design decisions, not hardware luck.

## AI Engineering Relevance

**Where this shows up:** every LLM gateway, embedding service, and
classification endpoint — the pattern is identical whether the "model" is
a pipeline, a torch module, or an external API call.

| Concept here | Used for |
|---|---|
| load once | shared model across requests |
| warmup | cold-start-free first requests |
| /v1/predict contract | stable client contract |
| batching | GPU/vectorized throughput |
| memory math | worker capacity planning |

**Scale note:** the same three rules apply to LLM serving — load the
weights once (they are GB), warm up the first token, and batch (continuous
batching) — which is exactly how vLLM and friends work.

## Practice Exercises

### Exercise 1: Startup load  (Difficulty: Easy)
Assert the model is loaded once and callable.

### Exercise 2: Warmup  (Difficulty: Easy)
Warmup prediction returns a finite duration; assert it ran.

### Exercise 3: /predict contract  (Difficulty: Medium)
Via TestClient: valid → 200 with version; wrong arity → 422.

### Exercise 4: Batching math  (Difficulty: Medium)
32 singles vs one batch of 32; assert the batch wins.

### Exercise 5: Memory capacity  (Difficulty: Medium)
Compute max workers from model memory; assert the math binds.

### Exercise 6: Full serving service  (Difficulty: Hard)
Load at startup, warm, serve /v1/predict + /v1/predict_batch, version
the contract, and assert metrics are emitted for each call.

## Summary

| Concept | Description |
|---|---|
| load once | shared startup model |
| warmup | cold-start-free first requests |
| /predict contract | validated, versioned |
| batching | throughput via amortization |
| memory math | workers × model ≤ RAM |
| GPU vs CPU | batch-size × utilization |

Serving is capacity math plus a clean contract: load once, warm up,
batch, count memory, version the endpoint. The same three rules that run
this exercise's logistic regression run the LLM gateways of production.

## Quick Reference

| Task | Idiom |
|---|---|
| Load once | module-level `joblib.load` / `MODEL = ...` |
| Warmup | `MODEL.predict(dummy)` at startup |
| Contract | `BaseModel` request + versioned path |
| Batch | N rows in, N predictions out, one pass |
| Workers | `floor(ram / (model + overhead))` |
| GPU decision | `gpu_total < cpu_total` at your batch size |

## Next Steps

**FastAPI track complete (01–52).** Continue to:
- **[system-design 01 — Fundamentals](../../05-web-frameworks/system-design/01-fundamentals.md)** —
  the design vocabulary above the service.
- **[07 — Designing an LLM API](../../05-web-frameworks/system-design/07-designing-an-llm-api.md)** —
  the capstone service at platform scale.

Official docs:
- FastAPI model serving patterns: https://fastapi.tiangolo.com/advanced/response-directly/
- vLLM (LLM serving): https://docs.vllm.ai/
