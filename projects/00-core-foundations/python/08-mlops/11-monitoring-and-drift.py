"""
MLOps - 11: Monitoring and Drift
=================================
Topics: data drift vs concept drift, PSI and KS tests, performance
monitoring with delayed labels, alerting thresholds.

Why this matters for AI/backend engineering:
    Models decay. The market shifts, users change, the data source breaks.
    Drift detection is the early warning system - catch it with statistics
    (PSI, KS) before the business metrics catch it the expensive way.

Run:      python 11-monitoring-and-drift.py
Verify:   python 11-monitoring-and-drift.py --verify
Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable


# ============================================================
# 1. Data Drift vs Concept Drift
# ============================================================
# Data drift: the input distribution changed (P(X) moved).
# Concept drift: the relationship changed (P(Y|X) moved).
# They need different responses.

@dataclass
class DriftType:
    name: str
    input_changed: bool
    relationship_changed: bool

    def response(self) -> str:
        if self.input_changed and not self.relationship_changed:
            return "retrain on recent data (distribution shift)"
        if self.relationship_changed:
            return "re-examine features/labels - the task itself moved"
        return "monitor"


# Example 1: classify drift
cases = [
    DriftType("data drift", input_changed=True, relationship_changed=False),
    DriftType("concept drift", input_changed=False, relationship_changed=True),
]
print("Example 1: drift types and responses")
for c in cases:
    print(f"  {c.name:<14} -> {c.response()}")
assert cases[1].response().startswith("re-examine")

# ============================================================
# 2. Population Stability Index (PSI)
# ============================================================
# PSI compares two distributions by bucketing them. Rule of thumb:
#   < 0.1 stable, 0.1-0.25 moderate shift, > 0.25 major shift.

def psi(reference: list[float], current: list[float], buckets: int = 10) -> float:
    """Population Stability Index between two 1-D distributions."""
    ref = sorted(reference)
    cur = sorted(current)
    edges = []
    for i in range(buckets):
        idx = int((i + 1) * len(ref) / buckets) - 1
        edges.append(ref[idx])
    edges[-1] = float("inf")

    def bucketize(values: list[float]) -> list[float]:
        counts = [0] * buckets
        for v in values:
            for b in range(buckets):
                lower = ref[int(b * len(ref) / buckets) - 1] if b > 0 else float("-inf")
                if lower <= v < edges[b]:
                    counts[b] += 1
                    break
        return [c / len(values) for c in counts]

    ref_pct = bucketize(ref)
    cur_pct = bucketize(cur)
    score = 0.0
    for r, c in zip(ref_pct, cur_pct):
        r = max(r, 1e-4)
        c = max(c, 1e-4)
        score += (r - c) * (__import__("math").log(r / c))
    return score


# Example 2: PSI on stable vs drifted data
import random
random.seed(42)
stable_ref = [random.gauss(0.0, 1.0) for _ in range(1000)]
stable_cur = [random.gauss(0.05, 1.0) for _ in range(1000)]
drifted_cur = [random.gauss(2.0, 1.0) for _ in range(1000)]

psi_stable = psi(stable_ref, stable_cur)
psi_drifted = psi(stable_ref, drifted_cur)
print("\nExample 2: PSI values")
print(f"  stable vs shifted-0.05: {psi_stable:.3f}")
print(f"  stable vs shifted-2.0:  {psi_drifted:.3f}")
assert psi_drifted > psi_stable, "bigger shift -> bigger PSI"

def psi_status(score: float) -> str:
    if score < 0.1:
        return "stable"
    if score < 0.25:
        return "moderate shift - investigate"
    return "major shift - alert"

# ============================================================
# 3. KS Test (two-sample)
# ============================================================
# KS measures the max gap between cumulative distributions.

def ks_stat(reference: list[float], current: list[float]) -> float:
    """Two-sample Kolmogorov-Smirnov statistic (no scipy needed)."""
    combined = sorted(reference + current)
    best = 0.0
    for x in combined:
        cdf_ref = sum(1 for v in reference if v <= x) / len(reference)
        cdf_cur = sum(1 for v in current if v <= x) / len(current)
        best = max(best, abs(cdf_ref - cdf_cur))
    return best


# Example 3: KS statistic
ks_s = ks_stat(stable_ref, stable_cur)
ks_d = ks_stat(stable_ref, drifted_cur)
print("\nExample 3: KS statistics")
print(f"  stable:   {ks_s:.3f}")
print(f"  drifted:  {ks_d:.3f}")
assert ks_d > ks_s, "drifted distributions have larger KS gap"

# ============================================================
# 4. Performance Monitoring with Delayed Labels
# ============================================================
# Real labels arrive late (fraud confirmed in 30 days). Monitor the
# proxy metrics now, the true metrics when labels land.

@dataclass
class DelayedLabelMonitor:
    label_delay_days: int
    proxy_metrics: dict[str, Callable] = None  # type: ignore[assignment]

    def report(self, predicted: list[float], actual_available: list[float] | None,
               proxies: dict[str, float]) -> str:
        line = f"proxies: {proxies}"
        if actual_available:
            line += f" | true accuracy vs {len(actual_available)} labels"
        else:
            line += f" | labels arrive in ~{self.label_delay_days}d"
        return line


# Example 4: delayed-label reporting
monitor = DelayedLabelMonitor(label_delay_days=30)
print("\nExample 4: delayed labels")
print("  " + monitor.report([0.9, 0.8], None, {"null_rate": 0.02, "call_volume": 1200}))
print("  " + monitor.report([0.9, 0.8], [1, 0], {"null_rate": 0.02}))

# ============================================================
# Production Pattern
# ============================================================
# Alerting thresholds must be set BEFORE deployment and reviewed - a
# monitor that never fires is dead weight.

@dataclass
class DriftMonitor:
    psi_threshold: float = 0.25
    ks_threshold: float = 0.20

    def evaluate(self, reference: list[float], current: list[float]) -> dict:
        p = psi(reference, current)
        k = ks_stat(reference, current)
        return {
            "psi": round(p, 4),
            "ks": round(k, 4),
            "alert": p > self.psi_threshold or k > self.ks_threshold,
            "psi_status": psi_status(p),
        }


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: monitoring only accuracy - by the time it drops it is old news
# MISTAKE: thresholds too tight -> alert fatigue -> alerts ignored
# MISTAKE: comparing current data to a stale reference baseline


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    import random as _r
    _r.seed(7)
    base = [_r.gauss(0, 1) for _ in range(500)]
    same = [_r.gauss(0, 1) for _ in range(500)]
    moved = [_r.gauss(3, 1) for _ in range(500)]

    p_same = psi(base, same)
    p_moved = psi(base, moved)
    assert p_moved > p_same, "PSI increases with shift"
    assert psi_status(0.05) == "stable"
    assert psi_status(0.30) == "major shift - alert"

    k_same = ks_stat(base, same)
    k_moved = ks_stat(base, moved)
    assert k_moved > k_same, "KS increases with shift"
    assert 0.0 <= k_moved <= 1.0, "KS bounded by [0,1]"

    m = DriftMonitor(psi_threshold=0.25, ks_threshold=0.2)
    r1 = m.evaluate(base, same)
    r2 = m.evaluate(base, moved)
    assert not r1["alert"], "same distribution - no alert"
    assert r2["alert"], "major shift - alert fires"
    print("[OK] 11-monitoring-and-drift: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Data drift vs concept drift need different responses.")
        print("2. PSI > 0.25 / KS gap growing = alert.")
        print("3. Monitor proxies now; true metrics when labels arrive.")
        _verify()
