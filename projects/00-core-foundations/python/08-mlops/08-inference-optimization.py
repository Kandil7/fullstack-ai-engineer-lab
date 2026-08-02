"""
MLOps - 08: Inference Optimization
==================================
Topics: quantization (int8, fp16), pruning, distillation, ONNX Runtime,
batching tradeoffs, and the measured latency/accuracy curve.

Why this matters for AI/backend engineering:
    Inference cost is a line item: a model 10x slower or 4x bigger than
    it needs to be is a 10x cloud bill. Optimization is a measured
    tradeoff - you must quantify both the speedup and the accuracy cost
    before shipping.

Run:      python 08-inference-optimization.py
Verify:   python 08-inference-optimization.py --verify
Reference: https://onnxruntime.ai/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable


# ============================================================
# 1. Model Size Arithmetic
# ============================================================
# A float32 weight takes 4 bytes; float16 takes 2; int8 takes 1.

def size_bytes(num_params: int, bits: int) -> float:
    """Model size in MB for a given parameter count and bit width."""
    return num_params * bits / 8 / (1024 ** 2)


# Example 1: quantize a 100M-param model
n_params = 100_000_000
for bits, label in [(32, "fp32"), (16, "fp16"), (8, "int8")]:
    print(f"Example 1: {label} -> {size_bytes(n_params, bits):.1f} MB")
assert size_bytes(n_params, 8) < size_bytes(n_params, 32), "int8 must be smaller"

# ============================================================
# 2. The Latency/Accuracy Tradeoff Curve
# ============================================================
# Quantization usually costs a little accuracy for a lot of speed.
# The professional move: measure BOTH and plot the frontier.

@dataclass
class OptimizedModel:
    name: str
    latency_ms: float
    accuracy: float
    size_mb: float


# Example 2: candidate optimizations
candidates = [
    OptimizedModel("baseline-fp32", latency_ms=12.0, accuracy=0.950, size_mb=400.0),
    OptimizedModel("quantized-int8", latency_ms=4.0, accuracy=0.941, size_mb=100.0),
    OptimizedModel("pruned-50pct", latency_ms=7.5, accuracy=0.930, size_mb=200.0),
]
print("\nExample 2: optimization candidates")
for c in candidates:
    print(f"  {c.name:<16} lat={c.latency_ms}ms acc={c.accuracy} size={c.size_mb}MB")


def pick_best(cands: list[OptimizedModel], max_latency_ms: float,
              min_accuracy: float) -> OptimizedModel | None:
    """Choose the fastest model that respects both constraints."""
    eligible = [c for c in cands if c.latency_ms <= max_latency_ms
                and c.accuracy >= min_accuracy]
    return min(eligible, key=lambda c: c.latency_ms) if eligible else None


# Example 3: constraint-based selection
best = pick_best(candidates, max_latency_ms=10.0, min_accuracy=0.90)
print("\nExample 3: choose within SLO constraints")
print(f"  picked: {best.name if best else None}")
assert best is not None and best.name == "quantized-int8", "int8 wins under 10ms SLO"

# ============================================================
# 3. Batching Tradeoffs
# ============================================================
# Batch of N is usually cheaper per item than N individual calls, but
# adds latency (must wait for N items) and memory.

@dataclass
class BatchModel:
    base_ms: float   # fixed cost per batch
    per_item_ms: float

    def cost(self, batch_size: int) -> float:
        return self.base_ms + self.per_item_ms * batch_size

    def per_item(self, batch_size: int) -> float:
        return self.cost(batch_size) / batch_size


# Example 4: batching economy of scale
bm = BatchModel(base_ms=10.0, per_item_ms=1.0)
print("\nExample 4: batching")
for bs in [1, 8, 32]:
    print(f"  batch={bs:<3} total={bm.cost(bs):.1f}ms per-item={bm.per_item(bs):.2f}ms")
assert bm.per_item(32) < bm.per_item(1), "bigger batches amortize fixed cost"

# ============================================================
# 4. ONNX Runtime - portable optimized execution
# ============================================================
# ONNX is a portable graph format; ONNX Runtime applies graph-level
# optimizations and backend fusion. (Package check; full export needs a
# framework model.)

def onnx_available() -> bool:
    try:
        import onnxruntime  # noqa: F401
        return True
    except ImportError:
        return False


print("\nExample 5: ONNX Runtime availability")
print(f"  onnxruntime installed: {onnx_available()}")

# ============================================================
# Production Pattern
# ============================================================
def optimize_pipeline(fn: Callable[[float], float], budget_ms: float) -> tuple[float, bool]:
    """Run the candidate under a latency budget; report headroom."""
    import time
    t0 = time.perf_counter()
    fn(1.0)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return elapsed_ms, elapsed_ms <= budget_ms


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: quantizing without measuring accuracy loss
#   (0.95 -> 0.82 may be unacceptable for a fraud model)
# MISTAKE: assuming int8 is always faster (old CPUs can be slower)
# MISTAKE: ignoring memory - a smaller model fits more workers per GPU


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert size_bytes(1_000_000, 32) == pytest_approx(4 / (1024 ** 2)) if False else \
        size_bytes(1_000_000, 8) * 4 == size_bytes(1_000_000, 32), "int8 is 1/4 of fp32"

    cands = [
        OptimizedModel("a", 5.0, 0.95, 100.0),
        OptimizedModel("b", 3.0, 0.80, 50.0),   # too inaccurate
        OptimizedModel("c", 20.0, 0.97, 200.0),  # too slow
    ]
    best = pick_best(cands, max_latency_ms=10.0, min_accuracy=0.90)
    assert best is not None and best.name == "a", "only 'a' meets both constraints"
    assert pick_best(cands, max_latency_ms=1.0, min_accuracy=0.90) is None, \
        "no candidate under 1ms"

    bm = BatchModel(10.0, 1.0)
    assert bm.per_item(1) == 11.0, "single item pays full fixed cost"
    assert bm.per_item(10) == 2.0, "batch of 10 amortizes to 2ms/item"
    assert bm.per_item(10) < bm.per_item(1), "batching wins"
    print("[OK] 08-inference-optimization: all checks passed")


def pytest_approx(x: float) -> float:
    return x  # tiny helper to keep the assert readable


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Size = params x bits; int8 is 1/4 of fp32.")
        print("2. Measure the latency/accuracy curve, then pick within SLOs.")
        print("3. Batching amortizes fixed cost; ONNX adds portability.")
        _verify()
