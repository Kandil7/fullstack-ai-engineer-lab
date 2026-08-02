"""
MLOps - 13: Feature Stores
==========================
Topics: offline vs online stores, point-in-time correctness, training/
serving skew, and when a feature store is overkill.

Why this matters for AI/backend engineering:
    The classic ML production bug: training on yesterday's data with
    today's features, then serving with different feature logic. Feature
    stores enforce one definition of each feature and, crucially,
    point-in-time correctness - no lookahead leakage.

Run:      python 13-feature-stores.py
Verify:   python 13-feature-stores.py --verify
Reference: https://docs.feast.dev/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any


# ============================================================
# 1. Offline vs Online
# ============================================================
# Offline store: big, batch, for training (historical data).
# Online store: small, fast, low-latency, for serving (current values).

@dataclass
class FeatureValue:
    entity_id: str
    feature: str
    value: float
    timestamp: float


class OfflineStore:
    """Historical feature log, append-only."""
    def __init__(self) -> None:
        self._rows: list[FeatureValue] = []

    def append(self, row: FeatureValue) -> None:
        self._rows.append(row)

    def as_of(self, entity_id: str, feature: str, at_time: float) -> float | None:
        """The feature value as of a given time (no future leak)."""
        eligible = [r for r in self._rows
                    if r.entity_id == entity_id and r.feature == feature
                    and r.timestamp <= at_time]
        if not eligible:
            return None
        return max(eligible, key=lambda r: r.timestamp).value


# Example 1: point-in-time retrieval
offline = OfflineStore()
offline.append(FeatureValue("u1", "spend_7d", 100.0, t := 100.0))  # noqa: F841
offline.append(FeatureValue("u1", "spend_7d", 150.0, 200.0))
print("Example 1: offline store as_of")
print(f"  as of t=150: {offline.as_of('u1', 'spend_7d', 150.0)}  (no future leak)")
print(f"  as of t=250: {offline.as_of('u1', 'spend_7d', 250.0)}")
assert offline.as_of("u1", "spend_7d", 150.0) == 100.0, "past value only"
assert offline.as_of("u1", "spend_7d", 250.0) == 150.0

# ============================================================
# 2. The Training/Serving Skew Bug
# ============================================================
# Skew: training computes a feature one way, serving computes it
# another way. The model sees different inputs at serving time.

def compute_feature_train(row: dict) -> float:
    return round(row["amount"] * 0.9, 2)   # old definition

def compute_feature_serving(row: dict) -> float:
    return round(row["amount"] * 0.9 + row.get("discount", 0.0), 2)  # new


# Example 2: divergent definitions
train_val = compute_feature_train({"amount": 100.0})
serve_val = compute_feature_serving({"amount": 100.0, "discount": 5.0})
print("\nExample 2: training/serving skew")
print(f"  train sees: {train_val}")
print(f"  serving sees: {serve_val}")
print(f"  skew: {serve_val - train_val:.2f} (silent behavior change)")
assert train_val != serve_val, "skew demonstrated"

# ============================================================
# 3. A Feature Store Enforces One Definition
# ============================================================
class FeatureStore:
    def __init__(self) -> None:
        self._definitions: dict[str, Any] = {}

    def define(self, name: str, fn: Any, ttl_days: int = 30) -> None:
        """One definition per feature - training and serving share it."""
        self._definitions[name] = {"fn": fn, "ttl_days": ttl_days}

    def compute(self, name: str, row: dict) -> float:
        if name not in self._definitions:
            raise KeyError(f"undefined feature: {name}")
        return self._definitions[name]["fn"](row)


# Example 3: one definition, two consumers
store = FeatureStore()
store.define("net_amount", lambda r: round(r["amount"] * 0.9 + r.get("discount", 0.0), 2))
train_feat = store.compute("net_amount", {"amount": 100.0, "discount": 5.0})
serve_feat = store.compute("net_amount", {"amount": 100.0, "discount": 5.0})
print("\nExample 3: single definition")
print(f"  train={train_feat} serving={serve_feat}  (identical by construction)")
assert train_feat == serve_feat

# ============================================================
# 4. Point-in-Time Correctness (Joins)
# ============================================================
# Training rows must join features as-of the row's timestamp - never
# features computed after the label was set.

def join_point_in_time(events: list[dict], features: OfflineStore,
                       feature_names: list[str]) -> list[dict]:
    """Join each event with feature values valid at its timestamp."""
    joined = []
    for ev in events:
        enriched = dict(ev)
        for fname in feature_names:
            enriched[fname] = features.as_of(ev["user"], fname, ev["ts"])
        joined.append(enriched)
    return joined


# Example 4: join without lookahead
events = [
    {"user": "u1", "ts": 150.0, "label": 1},
    {"user": "u1", "ts": 250.0, "label": 0},
]
joined = join_point_in_time(events, offline, ["spend_7d"])
print("\nExample 4: point-in-time joins")
for j in joined:
    print(f"  ts={j['ts']} label={j['label']} spend_7d={j['spend_7d']}")
assert joined[0]["spend_7d"] == 100.0, "first event sees only first value"
assert joined[1]["spend_7d"] == 150.0, "second event sees updated value"

# ============================================================
# Production Pattern
# ============================================================
# Decide deliberately: a feature store earns its complexity when many
# models share features or teams share a schema. For one model, keep
# features next to the model code.

def when_feature_store_wins() -> list[str]:
    return [
        "multiple models reuse the same features",
        "features have complex backfills / point-in-time logic",
        "multiple teams must agree on one schema",
    ]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: training on the CURRENT value of a feature that was unknown
#   at label time (lookahead leakage)
# MISTAKE: duplicated feature code in train and serve paths (skew)
# MISTAKE: adding a feature store for one model (over-engineering)


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    s = OfflineStore()
    s.append(FeatureValue("e", "f", 1.0, 10.0))
    s.append(FeatureValue("e", "f", 2.0, 20.0))
    assert s.as_of("e", "f", 15.0) == 1.0, "as-of must not see future"
    assert s.as_of("e", "f", 25.0) == 2.0
    assert s.as_of("e", "other", 25.0) is None, "unknown feature -> None"

    fs = FeatureStore()
    fs.define("x", lambda r: r["v"] * 2)
    assert fs.compute("x", {"v": 3}) == 6.0
    try:
        fs.compute("y", {})
        raised = False
    except KeyError:
        raised = True
    assert raised, "undefined feature raises"

    ev = [{"user": "e", "ts": 15.0, "label": 0}]
    j = join_point_in_time(ev, s, ["f"])
    assert j[0]["f"] == 1.0, "join is point-in-time"
    print("[OK] 13-feature-stores: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Offline store trains; online store serves.")
        print("2. One definition per feature kills training/serving skew.")
        print("3. Join as-of event time - never look ahead.")
        _verify()
