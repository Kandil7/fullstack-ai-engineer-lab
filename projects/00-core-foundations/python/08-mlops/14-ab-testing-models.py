"""
MLOps - 14: A/B Testing Models
===============================
Topics: shadow, canary, A/B traffic splitting, statistical significance,
guardrail metrics, and when to stop an experiment.

Why this matters for AI/backend engineering:
    Offline metrics lie (the online world has latency, leakage, and user
    reaction). Deployment strategies - shadow, canary, A/B - let you test
    a model against reality with bounded blast radius, and statistics
    tell you when the difference is real versus noise.

Run:      python 14-ab-testing-models.py
Verify:   python 14-ab-testing-models.py --verify
Reference: https://docs.scipy.org/doc/scipy/reference/stats.html
"""

from __future__ import annotations

import math
import sys
import random
from dataclasses import dataclass, field


# ============================================================
# 1. Deployment Strategies
# ============================================================

@dataclass
class Strategy:
    name: str
    blast_radius: str
    observes_real_users: bool

    def describe(self) -> str:
        return f"{self.name}: blast radius {self.blast_radius}, " \
               f"{'sees' if self.observes_real_users else 'does not affect'} real users"


# Example 1: the deployment ladder
strategies = [
    Strategy("shadow", "none - logs only", False),
    Strategy("canary", "small % of traffic", True),
    Strategy("A/B", "controlled 50/50 split", True),
    Strategy("full rollout", "100%", True),
]
print("Example 1: deployment strategies")
for s in strategies:
    print(f"  {s.describe()}")

# ============================================================
# 2. Traffic Splitting
# ============================================================
# Deterministic bucketing: hash the user id, route by bucket.

def bucket_of(user_id: str, pct_a: float) -> str:
    """Return 'A' or 'B' deterministically for a user."""
    h = hash(user_id) % 1000
    return "A" if h < int(pct_a * 10) else "B"


# Example 2: 50/50 split is roughly even
random.seed(42)
users = [f"user-{i}" for i in range(10_000)]
counts = {"A": 0, "B": 0}
for u in users:
    counts[bucket_of(u, 50.0)] += 1
print("\nExample 2: 50/50 traffic split")
print(f"  A={counts['A']} B={counts['B']} "
      f"(ratio {counts['A']/sum(counts.values()):.2f})")
total = sum(counts.values())
assert abs(counts["A"] / total - 0.5) < 0.05, "split is approximately even"
assert bucket_of("user-1", 50.0) == bucket_of("user-1", 50.0), "bucketing is stable"

# ============================================================
# 3. Statistical Significance (z-test on proportions)
# ============================================================

def z_test_proportions(n_a: int, conv_a: int, n_b: int, conv_b: int) -> float:
    """Two-proportion z-test; returns the z statistic."""
    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    return (p_a - p_b) / se if se > 0 else 0.0


def is_significant(z: float, threshold: float = 1.96) -> bool:
    """|z| > 1.96 ~ p < 0.05 (two-tailed)."""
    return abs(z) > threshold


# Example 3: real difference vs noise
sig = z_test_proportions(5000, 450, 5000, 550)   # 9.0% vs 11.0%
noise = z_test_proportions(5000, 450, 5000, 452)  # 9.0% vs 9.04%
print("\nExample 3: statistical significance")
print(f"  9.0% vs 11.0% -> z={sig:.2f} significant={is_significant(sig)}")
print(f"  9.0% vs 9.04% -> z={noise:.2f} significant={is_significant(noise)}")
assert is_significant(sig), "large gap is significant"
assert not is_significant(noise), "small gap is noise"

# ============================================================
# 4. Guardrail Metrics
# ============================================================
# The treatment must not only win the target metric; it must not wreck
# the guardrails (latency, error rate, retention).

@dataclass
class ABResult:
    target_metric: str
    target_win: bool
    guardrails: dict[str, bool] = field(default_factory=dict)

    def can_roll_out(self) -> bool:
        return self.target_win and all(self.guardrails.values())


# Example 4: win the metric, hold the guardrails
r1 = ABResult("ctr", True, {"p95_latency": True, "error_rate": True})
r2 = ABResult("ctr", True, {"p95_latency": False, "error_rate": True})
print("\nExample 4: guardrails")
print(f"  ctr win + all guardrails ok: rollout={r1.can_roll_out()}")
print(f"  ctr win + latency regressed: rollout={r2.can_roll_out()}")
assert r1.can_roll_out()
assert not r2.can_roll_out(), "latency regression blocks rollout"

# ============================================================
# Production Pattern
# ============================================================
# Pre-register stopping rules BEFORE the experiment: minimum sample,
# significance threshold, and guardrail budget. Then let the experiment
# run until one of the stopping conditions fires.

@dataclass
class ABExperiment:
    min_sample: int
    significance_threshold: float = 1.96

    def evaluate(self, n_a: int, ca: int, n_b: int, cb: int,
                 guardrails_ok: bool) -> tuple[str, bool]:
        if n_a < self.min_sample or n_b < self.min_sample:
            return "continue - sample too small", False
        z = z_test_proportions(n_a, ca, n_b, cb)
        if not is_significant(z, self.significance_threshold):
            return "continue - not significant", False
        winner = "A" if ca / n_a > cb / n_b else "B"
        if not guardrails_ok:
            return f"{winner} wins target but guardrails failed - stop", True
        return f"roll out {winner}", True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: peeking at the metric every hour and stopping on the first
#   significant blip (multiple-comparisons inflation)
# MISTAKE: shipping a model that wins the target but triples latency
# MISTAKE: no minimum sample - declaring victory on 30 users


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    exp = ABExperiment(min_sample=1000)
    verdict, done = exp.evaluate(100, 10, 100, 20, True)
    assert "continue" in verdict and not done, "tiny sample continues"

    verdict, done = exp.evaluate(5000, 450, 5000, 550, True)
    assert done and "roll out" in verdict, "significant + guardrails ok -> rollout"

    verdict, done = exp.evaluate(5000, 450, 5000, 550, False)
    assert done and "guardrails failed" in verdict, "guardrail failure stops"

    # stability of bucketing
    assert bucket_of("u", 50.0) == bucket_of("u", 50.0)

    # z-test sanity: equal rates -> z near 0
    assert abs(z_test_proportions(1000, 100, 1000, 100)) < 0.5

    r = ABResult("x", True, {"g": False})
    assert not r.can_roll_out(), "failed guardrail blocks"
    print("[OK] 14-ab-testing-models: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Shadow -> canary -> A/B -> full rollout.")
        print("2. Use z-tests to separate signal from noise.")
        print("3. Guardrails can veto a target-metric win.")
        _verify()
