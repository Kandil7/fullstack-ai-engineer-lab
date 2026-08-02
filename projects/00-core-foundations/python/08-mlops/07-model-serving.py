"""
MLOps - 07: Model Serving
=========================
Topics: FastAPI serving, load-at-startup, dynamic batching, async inference,
concurrency vs memory, latency budget.

Why this matters for AI/backend engineering:
    Serving is where ML meets SLOs: p99 latency, throughput, and memory.
    Loading the model once at startup (not per-request), batching
    inference, and reasoning about concurrency vs VRAM are the skills that
    separate a demo from a production endpoint.

Run:      python 07-model-serving.py
Verify:   python 07-model-serving.py --verify
Reference: https://fastapi.tiangolo.com/
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any


# ============================================================
# 1. Load Once, Serve Many
# ============================================================
# A model in memory is a service; a model loaded per request is a 10x
# latency disaster. The pattern: load at import/startup, keep it global.

@dataclass
class SimpleModel:
    """Stand-in for a real model - predict is deliberately slow."""
    name: str
    load_ms: float = 500.0
    predict_ms: float = 2.0

    @classmethod
    def load(cls, name: str) -> "SimpleModel":
        time.sleep(cls.load_ms / 1000)  # simulate cold load
        return cls(name)

    def predict(self, x: float) -> float:
        time.sleep(self.predict_ms / 1000)
        return x * 2.0


# Example 1: the anti-pattern - load per request
def predict_antipattern(model_name: str, x: float) -> float:
    start = time.perf_counter()
    m = SimpleModel.load(model_name)   # 500ms EVERY request
    result = m.predict(x)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return round(elapsed_ms, 1)


print("Example 1: load-per-request (anti-pattern)")
lat = predict_antipattern("demo", 3.0)
print(f"  total latency: {lat}ms  (dominated by 500ms model load)")
assert lat > 400, "load dominates latency"

# Example 2: the pattern - load once
_MODEL = SimpleModel.load("demo")  # 500ms once, at startup


def predict_fast(x: float) -> float:
    return _MODEL.predict(x)


print("\nExample 2: load-once at startup")
t0 = time.perf_counter()
predict_fast(3.0)
elapsed = (time.perf_counter() - t0) * 1000
print(f"  per-request latency: {elapsed:.1f}ms (model already in memory)")
assert elapsed < 100, "hot path must be fast"

# ============================================================
# 2. Dynamic Batching
# ============================================================
# GPUs shine on batches. Collect requests for a few ms, then run them
# together. Throughput up, per-request latency often *down* at load.

@dataclass
class Batcher:
    max_batch: int = 8
    wait_ms: float = 5.0

    def run_batch(self, xs: list[float]) -> list[float]:
        # Simulate: batch of N costs base + N*unit, with base amortized.
        base = 1.0
        per_item = 0.5
        cost = base + per_item * len(xs)
        return [x * 2.0 for x in xs]  # actual math is trivial here


# Example 3: batching math
batcher = Batcher()
batch = [1.0, 2.0, 3.0, 4.0]
results = batcher.run_batch(batch)
print("\nExample 3: dynamic batching")
print(f"  batch of {len(batch)} -> {results}")
assert results == [2.0, 4.0, 6.0, 8.0]

# ============================================================
# 3. Concurrency vs Memory
# ============================================================
# Each worker holds a copy of the model. 8 workers x 4GB model = 32GB.
# Tune concurrency to the memory budget.

@dataclass
class ServingPlan:
    model_gb: float
    workers: int
    memory_budget_gb: float

    def total_memory_gb(self) -> float:
        return self.model_gb * self.workers

    def fits_budget(self) -> bool:
        return self.total_memory_gb() <= self.memory_budget_gb


# Example 4: worker math
plan = ServingPlan(model_gb=4.0, workers=4, memory_budget_gb=16.0)
print("\nExample 4: concurrency vs memory")
print(f"  {plan.workers} workers x {plan.model_gb}GB = {plan.total_memory_gb()}GB")
print(f"  fits 16GB budget: {plan.fits_budget()}")
assert plan.fits_budget()
big = ServingPlan(4.0, 6, 16.0)
assert not big.fits_budget(), "6 workers x 4GB > 16GB must fail"

# ============================================================
# 4. Latency Budget
# ============================================================
# Define the SLO, then prove the stack meets it. Budget:
#   network 10ms + preprocess 5ms + inference 20ms + postprocess 5ms
@dataclass
class LatencyBudget:
    parts: dict[str, float]  # name -> ms

    def total(self) -> float:
        return sum(self.parts.values())

    def meets_slo(self, slo_ms: float) -> bool:
        return self.total() <= slo_ms


budget = LatencyBudget({"network": 10.0, "preprocess": 5.0,
                        "inference": 20.0, "postprocess": 5.0})
print("\nExample 5: latency budget")
print(f"  total: {budget.total()}ms vs SLO 60ms -> {budget.meets_slo(60.0)}")
assert budget.meets_slo(60.0)
assert not LatencyBudget({"inference": 90.0}).meets_slo(60.0)

# ============================================================
# Production Pattern
# ============================================================
# The canonical FastAPI skeleton (import-checkable; run with uvicorn):

FASTAPI_SKELETON = '''
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
MODEL = SimpleModel.load("prod")      # loaded once, at import

class Input(BaseModel):
    x: float

@app.post("/predict")
def predict(body: Input) -> dict[str, float]:
    return {"result": MODEL.predict(body.x)}   # no per-request load
'''

def validate_skeleton(skeleton: str) -> tuple[bool, list[str]]:
    issues = []
    if "FastAPI(" not in skeleton:
        issues.append("missing FastAPI app")
    if "MODEL" not in skeleton or "load(" not in skeleton:
        issues.append("model must be loaded at module scope")
    if "def predict" not in skeleton:
        issues.append("missing predict endpoint")
    return (not issues, issues)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: loading the model inside the endpoint (500ms per request)
# MISTAKE: unbounded workers on a multi-GB model (OOM in production)
# MISTAKE: no latency budget - shipping a model that misses the SLO


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    b = Batcher()
    assert b.run_batch([1.0]) == [2.0], "batch math"
    assert b.max_batch == 8, "default batch size"

    p = ServingPlan(1.0, 2, 3.0)
    assert p.fits_budget(), "2GB <= 3GB"
    assert not ServingPlan(2.0, 2, 3.0).fits_budget(), "4GB > 3GB"

    lb = LatencyBudget({"a": 10.0, "b": 20.0})
    assert lb.total() == 30.0 and lb.meets_slo(30.0), "budget math"
    assert not lb.meets_slo(29.0), "SLO violated when over"

    ok, issues = validate_skeleton(FASTAPI_SKELETON)
    assert ok, f"skeleton must validate: {issues}"
    assert not validate_skeleton("def foo(): pass")[0], "invalid skeleton flagged"

    # load-once semantics: two predicts after one load stay fast
    _m = SimpleModel("x", load_ms=0.0, predict_ms=1.0)
    t0 = time.perf_counter()
    _m.predict(1.0)
    assert (time.perf_counter() - t0) * 1000 < 50, "hot path fast"
    print("[OK] 07-model-serving: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Load the model once at startup.")
        print("2. Batch to amortize inference cost.")
        print("3. Size workers to memory; prove the latency budget.")
        _verify()
