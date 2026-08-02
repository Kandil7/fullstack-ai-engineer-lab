"""
MLOps - 01: Reproducibility
===========================
Topics: seed discipline, deterministic operations, environment capture,
data versioning, and why "it worked on my machine" is a production incident.

Why this matters for AI/backend engineering:
    A model that cannot be retrained to the same numbers cannot be debugged,
    audited, or shipped through a regulated pipeline. Every stochastic step
    (sampling, weight init, data shuffling) must be pinned or the "model"
    is actually many different models.

Run:      python 01-reproducibility.py
Verify:   python 01-reproducibility.py --verify
Reference: https://docs.python.org/3/library/random.html
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from dataclasses import dataclass, field

import numpy as np


# ============================================================
# 1. Seed Discipline
# ============================================================
# Set every RNG at process start, in one place. NumPy and Python's
# random are separate streams - seeding only one is a bug.

def seed_all(seed: int = 42) -> None:
    """Pin every RNG used by this process."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


# Example 1: identical draws from identical seeds
seed_all(42)
a = [random.randint(0, 1000) for _ in range(5)]
seed_all(42)
b = [random.randint(0, 1000) for _ in range(5)]
print("Example 1: same seed -> same stream")
print(f"  draw1={a}")
print(f"  draw2={b}")
assert a == b, "same seed must reproduce the same stream"

# ============================================================
# 2. Environment Capture
# ============================================================
# Record versions of the code, the data, and the libraries that
# produced a run. A run without these three is unreproducible.

def capture_environment() -> dict[str, str]:
    """Return a fingerprint of the runtime environment."""
    import platform
    import sys as _sys
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cwd_hash": hashlib.sha256(os.getcwd().encode()).hexdigest()[:12],
        "seed": os.environ.get("PYTHONHASHSEED", "not-set"),
        "executable": _sys.executable,
    }


# Example 2: capture and serialize the environment
env = capture_environment()
blob = json.dumps(env, sort_keys=True)
print("\nExample 2: environment fingerprint")
print(f"  {blob}")
assert "python" in env and "seed" in env

# ============================================================
# 3. Data Versioning - Content Addressing
# ============================================================
# Hash the *content* of a dataset, not its filename. Two files with
# the same name but different bytes must produce different versions.

def data_fingerprint(data: np.ndarray) -> str:
    """Content-addressed hash of a numpy array (deterministic bytes)."""
    return hashlib.sha256(np.ascontiguousarray(data).tobytes()).hexdigest()[:16]


# Example 3: content-addressed hashing
X1 = np.random.rand(10, 3)
X2 = X1.copy()
X2[0, 0] += 0.001
print("\nExample 3: content addressing")
print(f"  X1 hash: {data_fingerprint(X1)}")
print(f"  X2 hash: {data_fingerprint(X2)}")
assert data_fingerprint(X1) != data_fingerprint(X2), "different bytes -> different hash"
assert data_fingerprint(X1) == data_fingerprint(X1.copy()), "same bytes -> same hash"

# ============================================================
# 4. The "It Worked On My Machine" Failure
# ============================================================
# Example 4: the same pipeline, two machines, different numbers.
# The fix is not a different random state - it is capturing state.

@dataclass
class RunRecord:
    """Everything needed to re-run one training job."""
    seed: int
    data_hash: str
    env: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)


seed_all(7)
model_a_accuracy = round(0.5 + 0.4 * random.random(), 4)
seed_all(7)
model_b_accuracy = round(0.5 + 0.4 * random.random(), 4)
print("\nExample 4: same seed, same result")
print(f"  run A accuracy={model_a_accuracy}")
print(f"  run B accuracy={model_b_accuracy}")
assert model_a_accuracy == model_b_accuracy, "seeded runs must match"

# A run WITHOUT a seed drifts:
rng = np.random.default_rng()  # fresh entropy each process
drifted = [round(rng.random(), 3) for _ in range(3)]
print(f"  unseeded drift sample: {drifted}  (differs each run)")

# ============================================================
# Production Pattern
# ============================================================
def run_reproducibly(seed: int, X: np.ndarray) -> RunRecord:
    """Train a stub model and return a full audit trail."""
    seed_all(seed)
    idx = np.random.permutation(len(X))
    X_shuffled = X[idx]
    return RunRecord(
        seed=seed,
        data_hash=data_fingerprint(X_shuffled),
        metrics={"rows": int(len(X_shuffled))},
    )


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: seed inside a loop -> every fold uses the same split
#   for fold in range(5): np.random.seed(42)      # WRONG
# CORRECT: seed once at process start
#   seed_all(42); for fold in range(5): ...       # RIGHT


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    seed_all(123)
    r1 = [random.random() for _ in range(4)]
    seed_all(123)
    r2 = [random.random() for _ in range(4)]
    assert r1 == r2, "reseeded random stream must match"

    X = np.arange(12).reshape(4, 3)
    h1 = data_fingerprint(X)
    assert h1 == data_fingerprint(X.copy()), "copy must hash identically"
    assert h1 != data_fingerprint(X.astype(np.float64) if X.dtype != np.float64 else X), \
        "changed bytes must change the hash"

    rec = run_reproducibly(5, X)
    assert rec.seed == 5 and rec.metrics["rows"] == 4, "run record must capture state"

    env = capture_environment()
    assert "python" in env and "executable" in env, "environment capture must be complete"

    print("[OK] 01-reproducibility: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Seed every RNG once, at process start.")
        print("2. Record code + data + library versions with every run.")
        print("3. Hash dataset content, not filenames.")
        _verify()
