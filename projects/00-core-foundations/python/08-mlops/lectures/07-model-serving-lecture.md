# MLOps — 07: Model Serving

## Topic Overview

Model serving is exposing a trained, packaged model to consumers through a
stable interface — typically a REST API (`POST /predict`) — with production
concerns handled: latency budgets, concurrency, batching, graceful scaling,
and observability. Serving is where the model's value is actually realized:
a model that cannot be called reliably at the required latency and throughput
is not a production model.

The architecture is layered: the **model server** (the code that loads the
artifact and computes predictions) sits behind an **API layer** (FastAPI or a
serving framework) exposed over HTTP, often behind a **gateway** that handles
auth, routing, rate limiting, and canary traffic. Serving frameworks
(**Triton**, **TorchServe**, **KServe**, **Seldon**) add batching, dynamic
model loading, and GPU optimization; for many teams a FastAPI wrapper over the
pyfunc artifact from Lecture 05 is the pragmatic sweet spot.

Why this matters for an AI engineer: serving is the contract between ML and the
rest of the product. The AI engineer owns this boundary — latency, throughput,
correctness under load, and the ability to serve *multiple versions* during
canary and rollback are all serving responsibilities.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Build a FastAPI `POST /predict` endpoint over a packaged model
2. Distinguish online (low-latency) vs batch (high-throughput) serving
3. Implement request/response validation with Pydantic
4. Load models lazily and cache them (avoid reload per request)
5. Handle errors and timeouts so the API fails gracefully
6. Measure and reason about latency, throughput, and concurrency
7. Add health and readiness endpoints for orchestration
8. Compare DIY FastAPI serving vs serving frameworks (Triton, KServe)

## Prerequisites

| Need | Where |
|---|---|
| Model packaging | `08-mlops/lectures/05-model-packaging-lecture.md` |
| Docker | `08-mlops/lectures/06-docker-for-ml-lecture.md` |
| FastAPI | `05-web-frameworks/fastapi/` |
| HTTP basics | `05-web-frameworks/` |

## 1. Online vs Batch Serving

Two fundamentally different workloads:

| | Online (real-time) | Batch (offline) |
|---|---|---|
| Latency target | p50 < 50ms, p99 < 200ms | minutes to hours |
| Request volume | 10–10k QPS | rows × frequency |
| Consumers | API calls from apps | nightly jobs, data lakes |
| Failure mode | timeouts, overload | re-runnable job |
| Example | credit decision, search ranking | monthly propensity scores |

The same packaged model serves both; the *serving layer* differs. Online needs
a low-latency HTTP endpoint; batch needs a job runner (Spark, K8s Job, cron)
that processes data in bulk.

## 2. A Minimal Production Endpoint

FastAPI + the packaged artifact from Lecture 05. The critical detail: load the
model **once at startup** (module level or lifespan), never per request —
model loading is the slowest operation and reloading per request destroys
latency.

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib, os

MODEL_PATH = os.environ.get("MODEL_PATH", "/model/model.pkl")
model = joblib.load(MODEL_PATH)      # loaded ONCE at import

app = FastAPI(title="churn-api")

class PredictRequest(BaseModel):
    tenure: float
    monthly_charges: float
    contract_type_code: int

class PredictResponse(BaseModel):
    churn_probability: float

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    import numpy as np
    X = np.array([[req.tenure, req.monthly_charges, req.contract_type_code]])
    proba = float(model.predict_proba(X)[0, 1])
    return PredictResponse(churn_probability=proba)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Output (conceptually):
```
curl -X POST localhost:8000/predict \
  -d '{"tenure": 24, "monthly_charges": 70.5, "contract_type_code": 1}'
→ {"churn_probability": 0.71}
```

## 3. Validation and Errors: The API Contract

Pydantic validation turns malformed requests into clean 422s instead of
server crashes. **Never let a bad input reach the model** — and never let a
model exception reach the client as a 500 with a traceback.

```python
from fastapi import HTTPException

@app.post("/predict")
def predict(req: PredictRequest) -> PredictResponse:
    try:
        X = _to_matrix(req)
        proba = float(model.predict_proba(X)[0, 1])
        if not 0.0 <= proba <= 1.0:
            raise ValueError("model returned out-of-range probability")
        return PredictResponse(churn_probability=proba)
    except Exception as exc:
        # log the real error, return a safe response
        raise HTTPException(status_code=500, detail="prediction failed") from exc
```

Output (conceptually):
```
Bad input → 422 {"detail": [...]}   (Pydantic)
Model bug → 500 {"detail": "prediction failed"} + full error in logs
```

## 4. Latency, Throughput, and Concurrency

Serving math every AI engineer must know:

- **Latency**: time for one request (p50/p95/p99). Model compute dominates.
- **Throughput**: requests/sec. = concurrency / latency.
- **Concurrency**: how many requests are in flight. FastAPI + uvicorn is
  async; a CPU-bound model runs in a worker/thread pool.

```python
import time, statistics

def measure_latency(predict_fn, samples, n=200) -> dict[str, float]:
    """Measure p50/p95/p99 latency of a predict function."""
    times = []
    for s in samples[:n]:
        t0 = time.perf_counter()
        predict_fn(s)
        times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    def pct(p):
        return times[min(len(times) - 1, int(len(times) * p))]
    return {"p50_ms": round(pct(0.50), 2), "p95_ms": round(pct(0.95), 2),
            "p99_ms": round(pct(0.99), 2), "throughput_qps": round(n / (sum(times)/1000), 1)}
```

Output (conceptually):
```
{'p50_ms': 8.1, 'p95_ms': 21.4, 'p99_ms': 38.9, 'throughput_qps': 512.0}
```

**Rule of thumb:** if p99 is 5x p50, something is wrong (GC pauses, lock
contention, stragglers) — investigate before scaling out.

## 5. Caching, Batching, and the Hot Path

Three levers to meet latency budgets:

1. **Model caching**: load once, hold in memory (done above).
2. **Request batching** (dynamic): buffer N requests or T ms, predict them
   together — GPU and vectorized models amortize cost. Triton does this
   natively; DIY implementations batch in the worker.
3. **Response caching**: if repeated identical inputs are common (e.g. feature
   lookup), cache predictions keyed by input hash (see Phase 9 Lecture 18 for
   the LLM version).

```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def predict_cached(*features: float) -> float:
    # features tuple = cache key; identical requests hit the cache
    return _predict_impl(features)
```

Output (conceptually):
```
cache hit → ~0.01ms  (vs 8ms compute)
```

## 6. Serving Frameworks: When DIY Stops Scaling

| Framework | Strength | When to use |
|---|---|---|
| FastAPI DIY | simple, full control, few deps | < 1k QPS, one model |
| **Triton** | GPU batching, multi-model, FP16 | GPU inference, low latency at scale |
| **TorchServe** | PyTorch-native lifecycle | PyTorch models, managed |
| **KServe** (K8s) | serverless scale, canary, autoscale | large K8s footprint |
| **Seldon** | monitoring + explainability hooks | enterprise MLOps platforms |

The upgrade path is *gradual*: FastAPI for the first model, Triton when GPU
utilization or p99 matters, KServe when the platform is K8s-native.

## Every Use Case

- **Real-time decisions**: fraud, credit, pricing, recommendations — 10–100ms budgets.
- **Interactive features**: search ranking, autocomplete, image moderation.
- **Batch scoring**: nightly propensity, risk portfolio re-evaluation.
- **Edge inference**: on-device models with the same API contract (mockable in tests).
- **Multi-tenant SaaS**: one serving fleet, per-tenant rate limiting and quotas.
- **Canary and rollback**: serving two versions behind the gateway, shifting traffic.
- **Feature-store consumers**: online feature lookups feeding the same endpoint.
- **Model observability**: latency, error rate, and drift metrics per endpoint.

## Real-World Use Cases for AI Engineers

- **Fintech real-time fraud**: `POST /fraud/score` must answer in < 40ms p99
  because it sits in the transaction path. The AI engineer benchmarks the
  endpoint (p50/p95/p99), discovers the p99 spike is the model's one-time
  warm-up, moves warm-up to startup, and hits the budget — a latency fix with
  no model change.
- **E-commerce search**: the ranking endpoint serves 5k QPS behind a gateway.
  A canary deploys v2 to 5% of traffic; the gateway compares latency + CTR
  between versions; a p99 regression at 5% traffic triggers auto-rollback
  before users notice.
- **Batch credit portfolio**: the same churn model scores 10M customers
  nightly as a K8s Job; the batch wrapper streams rows, checkpointing progress
  so an interruption resumes rather than restarts.
- **Healthcare triage API**: the endpoint returns a prediction *and* a
  confidence + explanation payload; the serving layer validates the response
  schema so downstream clinical systems never receive a malformed payload.
- **LLM gateway**: for generative models, "serving" includes token streaming,
  batching, and retries (Phase 9) — same API discipline, different payload.

## Common Mistakes to Avoid

### Mistake 1: Loading the model inside the request handler
```
# WRONG — reload per request; destroys latency
@app.post("/predict")
def predict(...):
    model = joblib.load(MODEL_PATH)
# CORRECT — load once at module level / startup
model = joblib.load(MODEL_PATH)
```

### Mistake 2: Returning raw model exceptions to clients
500 with a traceback leaks internals and confuses consumers. Map to safe
errors; log the detail.

### Mistake 3: No input validation
Malformed requests reach the model → cryptic failures. Pydantic first.

### Mistake 4: Ignoring p99
Averages lie. A p95/p99 budget is what actually protects users.

### Mistake 5: No health/readiness endpoints
Orchestrators (K8s, load balancers) cannot route around a dying pod.

### Mistake 6: Sync blocking inside an async endpoint
CPU-bound predict in an async handler blocks the event loop — run it in a
worker (e.g. `def` endpoint runs in a threadpool, which FastAPI does by
default for `def`; `async def` does not).

## Best Practices

1. Load the model once at startup; never per request
2. Validate inputs with Pydantic before the model sees them
3. Map all model exceptions to safe HTTP errors with logged details
4. Measure p50/p95/p99, not just average latency
5. Add `/health` (liveness) and `/ready` (deps available) endpoints
6. Put the endpoint behind a gateway for auth, rate limiting, canary
7. Use dynamic batching when GPU-bound or latency-tolerant
8. Cache repeated identical predictions when appropriate
9. Log request ids + latency per call for observability
10. Upgrade to a serving framework only when the DIY layer is the bottleneck

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Model load at startup | 1–10 s | O(model) | cache; warm in init |
| One predict (sklearn) | 1–20 ms | O(1) | vectorized batching |
| One predict (DL, GPU) | 1–10 ms | O(model) | Triton dynamic batching, FP16 |
| Cache hit | ~0.01 ms | O(cache) | lru_cache bounded |

## AI Engineering Relevance

**Where this shows up:** the model→product boundary — every API your
engineering org's consumers call, every latency budget your SLOs cite.

| Concept here | Used for |
|---|---|
| Startup load + cache | p99 latency budgets |
| Pydantic validation | clean API contract, safe failures |
| Online vs batch | right serving layer per workload |
| Health/readiness | orchestration and self-healing |

**Scale note:** at 10k QPS, 1ms saved per call = 10k compute-seconds per
second. Serving efficiency is the highest-leverage place an ML engineer can
spend optimization time — it compounds across every consumer.

## Practice Exercises

### Exercise 1: Endpoint Over a Mock Model (Easy)
Build a FastAPI app that serves a mock `predict_proba` function with Pydantic
input validation; test with `TestClient` that a valid request returns 200 and
an invalid one returns 422.

### Exercise 2: Latency Measurement (Medium)
Write `measure_latency` (from section 4) and assert p50 ≤ p99 on a synthetic
predict function with controlled noise.

### Exercise 3: Model Load-Once (Medium)
Refactor a "reload per request" endpoint into a startup-load + cached version;
write a test asserting the load function is called exactly once across 10
requests (use a counter in a fake loader).

### Exercise 4: Graceful Failure (Hard)
Extend the endpoint so a model ValueError maps to a 500 with a safe message
while logging the real error; test that the client never sees the traceback
and the log records it.

## Summary

| Concept | Description |
|---|---|
| Online vs batch | latency vs throughput workloads |
| Startup load + cache | the #1 latency discipline |
| Pydantic contract | validation before the model |
| Latency math | p50/p95/p99 + throughput budgeting |
| Frameworks | FastAPI → Triton → KServe as you scale |

Model serving is the productization of the model: it is where ML meets
software engineering discipline — contracts, latency budgets, graceful
failure, and observability. Master the FastAPI layer first; graduate to
serving frameworks when the metrics demand it.

## Quick Reference

| Task | Idiom |
|---|---|
| Serve sklearn model | FastAPI + `joblib.load` at startup |
| Validate input | Pydantic `BaseModel` request |
| Measure latency | p50/p95/p99 over N warm calls |
| Health check | `GET /health` returning `{"status": "ok"}` |
| GPU-scale serving | Triton with dynamic batching |

## Next Steps

Next: **[08 Inference Optimization](08-inference-optimization-lecture.md)** —
making serving fast: quantization, batching, and profiling.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://fastapi.tiangolo.com/,
https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html
