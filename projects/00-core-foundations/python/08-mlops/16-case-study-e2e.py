"""
MLOps - 16: Case Study - End to End
====================================
Topics: validate -> train -> track -> register -> serve -> monitor ->
retrain. Ties the whole phase together with one small but complete flow,
using pure-Python stand-ins so it runs anywhere.

Why this matters for AI/backend engineering:
    The value of MLOps is the *loop*: every component in this phase was
    one piece; here they click together into a closed system that can
    detect drift and retrain itself.

Run:      python 16-case-study-e2e.py
Verify:   python 16-case-study-e2e.py --verify
Reference: https://mlflow.org/docs/latest/index.html
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any, Callable


# ============================================================
# Minimal building blocks (reused from earlier topics, compact)
# ============================================================

class Validator:
    """Data validation: type/range contract (topic 10)."""

    def __init__(self, min_val: float = 0.0, max_val: float = 100.0) -> None:
        self.min_val, self.max_val = min_val, max_val

    def check(self, data: list[float]) -> bool:
        return all(self.min_val <= v <= self.max_val for v in data)


class Tracker:
    """Experiment tracking: params + metrics (topic 02)."""

    def __init__(self) -> None:
        self.runs: list[dict[str, Any]] = []

    def log(self, params: dict[str, Any], metrics: dict[str, float]) -> None:
        self.runs.append({"params": params, "metrics": metrics})

    def best(self, metric: str) -> dict[str, Any]:
        return max(self.runs, key=lambda r: r["metrics"].get(metric, 0.0))


class Registry:
    """Model registry with gates (topic 04)."""

    def __init__(self, min_accuracy: float = 0.80) -> None:
        self.min_accuracy = min_accuracy
        self.production: dict[str, Any] | None = None

    def promote(self, name: str, accuracy: float) -> tuple[bool, str]:
        if accuracy < self.min_accuracy:
            return False, f"gate failed: {accuracy:.3f} < {self.min_accuracy}"
        self.production = {"name": name, "accuracy": accuracy}
        return True, f"promoted {name} ({accuracy:.3f})"


class DriftDetector:
    """PSI-style drift check (topic 11)."""

    def __init__(self, threshold: float = 0.25) -> None:
        self.threshold = threshold
        self.reference: list[float] = []

    def set_reference(self, values: list[float]) -> None:
        self.reference = list(values)

    def drift_score(self, current: list[float]) -> float:
        if not self.reference or not current:
            return 0.0
        m_ref = sum(self.reference) / len(self.reference)
        m_cur = sum(current) / len(current)
        return abs(m_cur - m_ref) / (abs(m_ref) + 1e-9)

    def alert(self, current: list[float]) -> bool:
        return self.drift_score(current) > self.threshold


# ============================================================
# The pipeline
# ============================================================

def train_stub(params: dict[str, Any]) -> dict[str, float]:
    """Toy training: accuracy depends on n_estimators + seed noise."""
    random.seed(params["seed"])
    accuracy = min(0.99, 0.70 + 0.003 * params["n_estimators"]
                   + random.uniform(-0.01, 0.01))
    return {"accuracy": round(accuracy, 4), "latency_ms": 2.0}


def run_e2e(data: list[float], configs: list[dict[str, Any]],
            min_accuracy: float = 0.80) -> dict[str, Any]:
    """The closed loop: validate -> train -> track -> register -> monitor."""
    # 1. VALIDATE - fail the pipeline, not the model
    validator = Validator(0.0, 100.0)
    if not validator.check(data):
        return {"status": "FAILED", "stage": "validate", "detail": "data out of range"}

    # 2-3. TRAIN + TRACK
    tracker = Tracker()
    for cfg in configs:
        metrics = train_stub(cfg)
        tracker.log(cfg, metrics)
    best = tracker.best("accuracy")

    # 4. REGISTER
    registry = Registry(min_accuracy=min_accuracy)
    ok, msg = registry.promote(best["params"].get("name", "model"),
                               best["metrics"]["accuracy"])
    if not ok:
        return {"status": "FAILED", "stage": "register", "detail": msg}

    # 5. MONITOR (baseline reference for later drift checks)
    detector = DriftDetector(threshold=0.25)
    detector.set_reference(data)
    return {
        "status": "OK",
        "stage": "monitoring",
        "best_config": best["params"],
        "best_accuracy": best["metrics"]["accuracy"],
        "drift_alert": detector.alert(data),
        "runs": len(tracker.runs),
        "message": msg,
    }


# ============================================================
# Worked example
# ============================================================
print("=== Case study: churn model, end to end ===")
data = [random.uniform(0, 100) for _ in range(500)]
configs = [
    {"name": "rf-100", "n_estimators": 100, "seed": 1},
    {"name": "rf-200", "n_estimators": 200, "seed": 2},
    {"name": "rf-300", "n_estimators": 300, "seed": 3},
]
result = run_e2e(data, configs)
print(f"  status: {result['status']}")
if result["status"] == "OK":
    print(f"  best: {result['best_config']['name']} "
          f"acc={result['best_accuracy']}")
    print(f"  tracked runs: {result['runs']}")
    print(f"  {result['message']}")
    print(f"  drift alert on training data: {result['drift_alert']}")

# Failing path: data outside the contract
bad_data = [random.uniform(-50, 50) for _ in range(100)]
bad_result = run_e2e(bad_data, configs)
print(f"\n  bad data -> {bad_result['status']} at stage {bad_result.get('stage')}")

# ============================================================
# Production Pattern
# ============================================================
# The loop continues after deployment: periodic drift checks on live
# features trigger a retrain - closing the circle.

def continuous_monitor(live_features: list[float],
                       detector: DriftDetector) -> str:
    if detector.alert(live_features):
        return "DRIFT - trigger retrain pipeline"
    return "stable - no action"


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: promoting a model whose data fails validation
# MISTAKE: no tracking - cannot say which config produced the winner
# MISTAKE: no drift monitor - the deployed model silently decays


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    v = Validator(0.0, 100.0)
    assert v.check([1.0, 50.0, 99.9]), "in-range data passes"
    assert not v.check([-1.0]), "out-of-range fails"

    t = Tracker()
    t.log({"a": 1}, {"accuracy": 0.7})
    t.log({"a": 2}, {"accuracy": 0.9})
    assert t.best("accuracy")["params"] == {"a": 2}, "best run found"

    r = Registry(min_accuracy=0.8)
    assert not r.promote("x", 0.5)[0], "below gate blocked"
    assert r.promote("x", 0.9)[0], "above gate promoted"

    d = DriftDetector(threshold=0.25)
    d.set_reference([10.0, 10.0, 10.0])
    assert not d.alert([10.0, 11.0, 9.0]), "stable data no alert"
    assert d.alert([50.0, 51.0, 49.0]), "massive drift alerts"

    res = run_e2e([50.0] * 100, [{"name": "m", "n_estimators": 100, "seed": 1}])
    assert res["status"] == "OK" and res["runs"] == 1, "e2e succeeds"
    assert run_e2e([-5.0] * 10, configs)["status"] == "FAILED", "bad data fails fast"

    assert continuous_monitor([50.0, 51.0, 49.0], d).startswith("DRIFT")
    assert continuous_monitor([10.0, 11.0, 9.0], d).startswith("stable")
    print("[OK] 16-case-study-e2e: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. The loop: validate -> train -> track -> register -> serve -> monitor.")
        print("2. Fail the pipeline, not the model.")
        print("3. Drift detection closes the loop and triggers retraining.")
        _verify()
