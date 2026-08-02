"""
MLOps - 04: Model Registry
===========================
Topics: model stages, versioning, signatures, promotion gates, rollback.

Why this matters for AI/backend engineering:
    A registry is the difference between "which model is live?" being a
    guess and being a lookup. Stages (staging -> production) with explicit
    promotion gates make deployment an auditable decision, not a copy-paste.

Run:      python 04-model-registry.py
Verify:   python 04-model-registry.py --verify
Reference: https://mlflow.org/docs/latest/model-registry.html
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import Any


# ============================================================
# 1. Stages and Lifecycle
# ============================================================
# A model moves: None -> Staging -> Production -> Archived.
# Only a promotion (with a reason and an approver) moves it forward.

@dataclass
class RegisteredModel:
    name: str
    version: int
    stage: str = "None"
    metrics: dict[str, float] = field(default_factory=dict)
    signature: dict[str, Any] = field(default_factory=dict)
    promoted_by: str | None = None
    promotion_reason: str | None = None
    created_at: float = field(default_factory=time.time)


VALID_STAGES = {"None", "Staging", "Production", "Archived"}
# Promotion gates: minimum metric thresholds that must hold before a model
# may move to a given stage. Tuple is (threshold, direction): "min" means
# the metric must be >= threshold (accuracy), "max" means it must be
# <= threshold (latency, cost).
GATES = {
    "Production": {"accuracy": (0.90, "min"), "latency_ms": (100.0, "max")},
}


# ============================================================
# 2. The Registry
# ============================================================

class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, list[RegisteredModel]] = {}

    def register(self, name: str, metrics: dict[str, float],
                 signature: dict[str, Any]) -> RegisteredModel:
        versions = self._models.setdefault(name, [])
        version = max((m.version for m in versions), default=0) + 1
        model = RegisteredModel(name=name, version=version,
                                metrics=metrics, signature=signature)
        versions.append(model)
        return model

    def promote(self, model: RegisteredModel, to_stage: str,
                by: str, reason: str, force: bool = False) -> tuple[bool, str]:
        """Promote a model to a stage, enforcing gates.

        ``force=True`` bypasses gates - reserved for rollbacks, where an
        operator decides to revert a regression even though the older model
        no longer meets today's thresholds. The decision is still logged.
        """
        if to_stage not in VALID_STAGES:
            return False, f"invalid stage: {to_stage}"

        if not force:
            gates = GATES.get(to_stage, {})
            for metric, (threshold, direction) in gates.items():
                actual = model.metrics.get(metric)
                if actual is None:
                    return False, f"gate failed: {metric} not logged"
                violated = actual < threshold if direction == "min" else actual > threshold
                if violated:
                    return False, f"gate failed: {metric}={actual} vs {direction} {threshold}"

        # One model per name may be in Production at a time.
        if to_stage == "Production":
            for other in self._models[model.name]:
                if other.stage == "Production":
                    other.stage = "Archived"

        model.stage = to_stage
        model.promoted_by = by
        model.promotion_reason = reason
        return True, f"{model.name} v{model.version} -> {to_stage}"

    def get_stage(self, name: str, stage: str) -> RegisteredModel | None:
        for m in self._models.get(name, []):
            if m.stage == stage:
                return m
        return None


# ============================================================
# 3. Worked Example
# ============================================================

registry = ModelRegistry()

# Example 1: register two candidate models
m1 = registry.register("churn", metrics={"accuracy": 0.88, "latency_ms": 5.0},
                       signature={"input": ["int"], "output": ["float"]})
m2 = registry.register("churn", metrics={"accuracy": 0.94, "latency_ms": 8.0},
                       signature={"input": ["int"], "output": ["float"]})
print("Example 1: registered versions")
print(f"  {m1.name} v{m1.version}: accuracy={m1.metrics['accuracy']}")
print(f"  {m2.name} v{m2.version}: accuracy={m2.metrics['accuracy']}")

# Example 2: m1 fails the production gate, m2 passes
ok1, msg1 = registry.promote(m1, "Production", by="alice", reason="backup")
ok2, msg2 = registry.promote(m2, "Production", by="alice", reason="best CV score")
print("\nExample 2: promotion gates")
print(f"  v{m1.version}: {msg1} (ok={ok1})")
print(f"  v{m2.version}: {msg2} (ok={ok2})")
assert not ok1, "m1 accuracy 0.88 must fail the 0.90 gate"
assert ok2, "m2 must pass the gate"

# Example 3: production lookup + auto-archival of the previous champ
live = registry.get_stage("churn", "Production")
print("\nExample 3: what is live right now?")
print(f"  {live.name} v{live.version} promoted by {live.promoted_by}")
assert live is m2, "only one model in production"

# Example 4: rollback = force-promote the archived version. Gates apply
# to NEW promotions; a rollback is an explicit operator decision to revert
# a regression, so it is forced but still fully logged.
ok3, msg3 = registry.promote(m1, "Production", by="bob",
                             reason="rollback: m2 regression", force=True)
print(f"\nExample 4: rollback (forced, logged) -> {msg3} (ok={ok3})")
assert ok3 and registry.get_stage("churn", "Production") is m1, "rollback must swap live model"

# ============================================================
# Production Pattern
# ============================================================
def deploy_candidate(registry: ModelRegistry, name: str, metrics: dict[str, float]) -> str:
    """Register, gate, promote - the standard CI entry point."""
    model = registry.register(name, metrics, signature={"input": [], "output": []})
    ok, msg = registry.promote(model, "Production", by="ci-bot", reason="pipeline gate")
    return msg


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: promoting on accuracy alone (deployed model is slower than SLA)
# CORRECT: multi-metric gates (accuracy AND latency AND drift)
# MISTAKE: two models live in production with no owner record
# CORRECT: one per name, with promoted_by + reason captured


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    r = ModelRegistry()
    a = r.register("x", {"accuracy": 0.99, "latency_ms": 1.0}, {})
    b = r.register("x", {"accuracy": 0.99, "latency_ms": 150.0}, {})
    # b fails latency gate (150ms > 100ms max)
    ok, msg = r.promote(b, "Production", "t", "test")
    assert not ok and "latency_ms" in msg, "latency gate must block b"
    # a passes both gates (0.99 acc, 1ms latency)
    ok, _ = r.promote(a, "Production", "t", "test")
    assert ok, "a must pass gates"
    assert r.get_stage("x", "Production") is a, "a is live"
    # promoting b archives a; b is forced because its latency exceeds the
    # gate but an operator chose it anyway (scenario: load testing shows
    # real latency is 60ms, not the pessimistic 150ms estimate)
    ok, _ = r.promote(b, "Production", "t", "test2", force=True)
    assert ok and r.get_stage("x", "Production") is b, "b becomes live"
    assert r.get_stage("x", "Archived") is a, "a is archived"
    # invalid stage
    ok, msg = r.promote(a, "Nowhere", "t", "x")
    assert not ok, "invalid stage rejected"
    # force bypasses gates (rollback path) but still records the reason
    forced, fmsg = r.promote(a, "Production", "ops", "rollback", force=True)
    assert forced and r.get_stage("x", "Production") is a, "forced rollback works"
    assert a.promotion_reason == "rollback", "forced promotions are logged"
    # versioning increments
    c = r.register("x", {"accuracy": 1.0, "latency_ms": 1.0}, {})
    assert c.version == 3, "versions increment"
    print("[OK] 04-model-registry: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Stages + gates make promotion an auditable decision.")
        print("2. One model per stage per name; promote archives the old champ.")
        print("3. Rollback is a re-promotion of an archived version.")
        _verify()
