"""
MLOps - 02: Experiment Tracking
===============================
Topics: params/metrics/artifacts, run comparison, nested runs, what to log
and what NOT to log. Uses a minimal local tracker (MLflow-compatible shape)
so the pattern is visible without a server.

Why this matters for AI/backend engineering:
    Untracked experiments are un-compareable: you cannot answer "which
    config produced the best model?" Tracking is the audit log that makes
    tuning reproducible, and it is what model registries gate on.

Run:      python 02-experiment-tracking.py
Verify:   python 02-experiment-tracking.py --verify
Reference: https://mlflow.org/docs/latest/tracking.html
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any


# ============================================================
# 1. The Run Object
# ============================================================
# A run is one training job: params (inputs) + metrics (outputs) +
# artifacts (files) + metadata (who/when).

@dataclass
class Run:
    run_id: str
    experiment: str
    params: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "experiment": self.experiment,
            "params": self.params,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "tags": self.tags,
            "created_at": self.created_at,
        }


# ============================================================
# 2. A Minimal Tracker
# ============================================================
# The API mirrors MLflow's three log_* methods so the mental model
# transfers directly to the real tool.

class ExperimentTracker:
    def __init__(self) -> None:
        self._runs: list[Run] = []
        self._counter = 0

    def start_run(self, experiment: str, **params: Any) -> Run:
        self._counter += 1
        run = Run(run_id=f"{experiment}-{self._counter:03d}", experiment=experiment, params=params)
        self._runs.append(run)
        return run

    def log_metric(self, run: Run, name: str, value: float) -> None:
        run.metrics[name] = value

    def log_artifact(self, run: Run, path: str) -> None:
        run.artifacts.append(path)

    def best_run(self, metric: str, maximize: bool = True) -> Run | None:
        """Best run by a metric; None if no run logged that metric."""
        scored = [r for r in self._runs if metric in r.metrics]
        if not scored:
            return None
        key = lambda r: r.metrics[metric]
        return max(scored, key=key) if maximize else min(scored, key=key)

    def export(self) -> str:
        return json.dumps([r.to_dict() for r in self._runs], indent=2)


# ============================================================
# 3. What to Log, What NOT to Log
# ============================================================
# Example 1: two comparable runs
tracker = ExperimentTracker()

run1 = tracker.start_run("iris-rf", n_estimators=100, max_depth=3, seed=42)
tracker.log_metric(run1, "accuracy", 0.9333)
tracker.log_metric(run1, "train_time_s", 0.42)
tracker.log_artifact(run1, "models/iris-rf-100.pkl")

run2 = tracker.start_run("iris-rf", n_estimators=300, max_depth=5, seed=42)
tracker.log_metric(run2, "accuracy", 0.9667)
tracker.log_metric(run2, "train_time_s", 1.10)

print("Example 1: logged runs")
print(f"  run1 accuracy={run1.metrics['accuracy']}, time={run1.metrics['train_time_s']}s")
print(f"  run2 accuracy={run2.metrics['accuracy']}, time={run2.metrics['train_time_s']}s")

# Example 2: comparison answers a question
best = tracker.best_run("accuracy")
print("\nExample 2: best run by accuracy")
print(f"  winner: {best.run_id} with {best.metrics['accuracy']}")
assert best is run2, "run2 has higher accuracy"

# Example 3: NOT to log - timestamps, absolute paths, big blobs,
# PII, or anything that changes between runs without changing the model.
print("\nExample 3: what NOT to log")
print("  - wall-clock start/end times (non-deterministic)")
print("  - absolute machine paths (breaks portability)")
print("  - full training datasets (store hashes instead)")
print("  - raw customer data (PII in the audit log = leak)")

# ============================================================
# Production Pattern
# ============================================================
def run_and_track(tracker: ExperimentTracker, n_estimators: int, seed: int) -> Run:
    """Train a stub and record everything meaningful."""
    run = tracker.start_run("demo", n_estimators=n_estimators, seed=seed)
    tracker.log_metric(run, "accuracy", round(0.9 + 0.01 * n_estimators / 100, 4))
    tracker.log_metric(run, "seed", float(seed))
    return run


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: logging metrics only after the run finishes
#   (if the process dies mid-training the run is lost)
# CORRECT: log incrementally after each epoch/fold
# MISTAKE: logging the dataset object into params
# CORRECT: log its content hash and row count


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    t = ExperimentTracker()
    a = t.start_run("e", lr=0.1)
    b = t.start_run("e", lr=0.01)
    t.log_metric(a, "acc", 0.8)
    t.log_metric(b, "acc", 0.9)
    assert t.best_run("acc") is b, "maximize must pick higher metric"
    assert t.best_run("acc", maximize=False) is a, "minimize must pick lower metric"
    assert t.best_run("missing") is None, "missing metric -> no winner"
    t.log_artifact(a, "x.pkl")
    assert a.artifacts == ["x.pkl"], "artifacts must be recorded"
    blob = t.export()
    assert '"lr": 0.1' in blob, "export must serialize params"
    r = t.start_run("e", seed=1)
    assert r.run_id.startswith("e-"), "run ids must be namespaced"
    print("[OK] 02-experiment-tracking: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. A run = params + metrics + artifacts + metadata.")
        print("2. Log incrementally; log hashes, not datasets.")
        print("3. Comparison is the point - always log what you tune.")
        _verify()
