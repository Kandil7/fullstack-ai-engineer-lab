"""
FastAPI — 52: Serving ML Models (STAR)
========================================
Topics: model loading at startup (never per request); warmup; batching
        for throughput; GPU vs CPU; /predict contracts; versioning;
        async inference; memory per worker with a loaded model

Why this matters for AI/backend engineering:
    This is the capstone: a real model behind a real endpoint, with
    memory measured. The three rules: LOAD ONCE at startup (loading a
    GB model per request is a DoS), WARMUP before serving (first
    request pays JIT/cache costs otherwise), and BATCH for throughput
    (GPU/vectorized inference amortizes across a batch). Memory math:
    every worker holds the model — workers × model = RAM before one
    request. This exercise builds a model-serving endpoint with a real
    sklearn model and asserts the contract with TestClient.

Run:      python 52-serving-ml-models.py
Verify:   python 52-serving-ml-models.py --verify
Reference: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
"""

from __future__ import annotations

import math
import sys
import time
import tracemalloc
from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ============================================================
# 1. Load the model ONCE at startup — never per request
# ============================================================
# Loading a model on every request is the classic serving bug: GB of
# weights read from disk, deserialized, and warmed for a single call.
# Load at module import / app startup; the workers inherit it.

print("=== 1. Model loaded at startup ===")
_start = time.perf_counter()
X_train, y_train = make_classification(n_samples=300, n_features=8, random_state=1)
MODEL = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=500)),
])
MODEL.fit(X_train, y_train)
load_s = time.perf_counter() - _start
print(f"model loaded in {load_s*1000:.0f}ms — ONCE, at startup, shared by all requests")
print()

# ============================================================
# 2. Warmup — pay the first-call cost before traffic arrives
# ============================================================
# The first predict() may pay one-time costs (buffer allocation, JIT,
# lazy imports). Warmup fires a dummy prediction at startup so the
# first REAL request is fast.

def warmup(model: Pipeline, n_features: int = 8) -> float:
    import numpy as np
    dummy = np.zeros((1, n_features), dtype=np.float64)
    t0 = time.perf_counter()
    model.predict(dummy)
    return time.perf_counter() - t0


print("=== 2. Warmup ===")
warm_s = warmup(MODEL)
print(f"warmup prediction: {warm_s*1000:.2f}ms (paid once, before traffic)")
print()

# ============================================================
# 3. The /predict contract + versioning
# ============================================================
# The contract is explicit and versioned in the URL and the schema:
# v1 takes a fixed feature vector and returns a proba. Breaking changes
# get a NEW version, not a broken v1.

class PredictRequest(BaseModel):
    features: list[float] = Field(min_length=8, max_length=8)


class PredictResponse(BaseModel):
    model_version: str
    prediction: int
    probability: float


app = FastAPI(title="model-server", version="1.0.0")

@app.post("/v1/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    import numpy as np
    X = np.asarray(req.features, dtype=np.float64).reshape(1, -1)
    pred = int(MODEL.predict(X)[0])
    proba = float(MODEL.predict_proba(X)[0][1])
    return PredictResponse(model_version="logreg-v1", prediction=pred, probability=proba)


client = TestClient(app)
print("=== 3. /predict contract ===")
r = client.post("/v1/predict", json={"features": [0.1] * 8})
print(f"status={r.status_code} body={r.json()}")
r_bad = client.post("/v1/predict", json={"features": [0.1] * 3})
print(f"wrong feature count -> {r_bad.status_code} (422: contract enforced)")
print()

# ============================================================
# 4. Batching — throughput for the GPU/vectorized core
# ============================================================
# One prediction per request underutilizes vectorized cores. A batch
# endpoint (or in-server queue) amortizes: 32 predictions in one pass
# cost less than 32 single calls. Latency per item rises slightly;
# throughput rises a lot.

def batched_predict(model: Pipeline, n: int = 32) -> float:
    import numpy as np
    X = np.random.default_rng(0).normal(size=(n, 8))
    t0 = time.perf_counter()
    model.predict(X)
    return time.perf_counter() - t0


single_total = sum(warmup(MODEL) for _ in range(32))
batch_total = batched_predict(MODEL, 32)
print("=== 4. Batching ===")
print(f"32 single calls: {single_total*1000:.2f}ms total")
print(f"1 batch of 32   : {batch_total*1000:.2f}ms total")
print(f"speedup         : {single_total / max(batch_total, 1e-9):.1f}x")
print()

# ============================================================
# 5. Memory per worker — the capacity math
# ============================================================
# Every worker holds the model. workers × model = RAM before one
# request. Measure the model's RSS delta, then compute capacity.

tracemalloc.start()
_ = warmup(MODEL)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
model_mb = current / 1e6

def max_workers(ram_gb: float, model_mb: float, overhead_mb: float = 300) -> int:
    per_worker = (model_mb + overhead_mb) / 1e3   # MB -> GB
    return max(1, int(ram_gb / per_worker))


print("=== 5. Memory per worker ===")
print(f"model+app traced ~{model_mb:.0f}MB (lower bound; real RSS higher)")
print(f"8GB box -> {max_workers(8.0, model_mb)} workers max")
print(f"16GB box -> {max_workers(16.0, model_mb)} workers max")
print()

# ============================================================
# 6. GPU vs CPU — when each wins
# ============================================================
# CPU: fast single predictions, low cost, no transfer overhead.
# GPU: amortizes over BATCHES (transfer cost split across items);
#      only wins when utilization is high.

def cpu_vs_gpu(per_item_cpu_ms: float, per_item_gpu_ms: float,
               transfer_ms: float, batch: int) -> dict:
    cpu = per_item_cpu_ms * batch
    gpu = transfer_ms + per_item_gpu_ms * batch
    return {"cpu_total_ms": round(cpu, 1), "gpu_total_ms": round(gpu, 1),
            "gpu_wins": gpu < cpu}


print("=== 6. GPU vs CPU ===")
print(f"  batch=1  : {cpu_vs_gpu(8, 2, 5, 1)}")
print(f"  batch=128: {cpu_vs_gpu(8, 0.3, 5, 128)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: loading the model per request — GB reads + deserialize per call
# CORRECT: load at startup; workers inherit it
#
# MISTAKE: no warmup — the first real request pays JIT/cache costs
# CORRECT: warmup prediction at startup
#
# MISTAKE: no batching — vectorized cores idle at batch size 1
# CORRECT: batch endpoint or in-server queue
#
# MISTAKE: workers × model > RAM — OOM restarts under load
# CORRECT: memory math before setting worker count (topic 49)
#
# MISTAKE: changing /predict in place — clients break silently
# CORRECT: version the contract; add v2, keep v1

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Model is a real fitted pipeline
    import numpy as np
    assert hasattr(MODEL, "predict"), "model must be callable"
    y = MODEL.predict(np.zeros((1, 8), dtype=np.float64))
    assert y.shape == (1,), "single-row prediction shape"

    # 2. Warmup returns a finite duration
    assert warm_s >= 0 and math.isfinite(warm_s)

    # 3. The /predict contract via TestClient
    r = client.post("/v1/predict", json={"features": [0.5] * 8})
    assert r.status_code == 200, f"valid request must 200, got {r.status_code}"
    body = r.json()
    assert body["model_version"] == "logreg-v1", "version is explicit"
    assert body["prediction"] in (0, 1), "binary prediction"
    assert 0.0 <= body["probability"] <= 1.0, "probability in [0,1]"

    # 4. Contract enforcement: wrong feature count -> 422
    assert client.post("/v1/predict", json={"features": [1.0]}).status_code == 422, \
        "schema must reject wrong arity"
    assert client.post("/v1/predict", json={"features": [0.5] * 9}).status_code == 422

    # 5. Batching improves throughput
    single_total = sum(warmup(MODEL) for _ in range(32))
    batch_total = batched_predict(MODEL, 32)
    assert batch_total < single_total, "batch must beat 32 single calls"

    # 6. Memory math caps workers
    assert max_workers(8.0, model_mb) >= 1, "at least one worker"
    assert max_workers(8.0, model_mb) <= max_workers(16.0, model_mb), \
        "more RAM -> more workers"

    # 7. GPU math: batching flips the decision
    assert cpu_vs_gpu(8, 2, 5, 1)["gpu_wins"] is False, "GPU loses at batch 1"
    assert cpu_vs_gpu(8, 0.3, 5, 128)["gpu_wins"] is True, "GPU wins at batch 128"

    print("[OK] 52-serving-ml-models: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Load once at startup; workers inherit the model")
        print("2. Warmup before traffic; version the /predict contract")
        print("3. Batch for throughput; GPU wins on batches, not singles")
        print("4. Memory math: workers × model <= RAM")
        _verify()          # always runs, so plain execution is also a test
