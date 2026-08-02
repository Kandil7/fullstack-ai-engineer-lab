"""
MLOps - 15: Cost Optimization
==============================
Topics: GPU vs CPU economics, spot instances, autoscaling to zero, batch
vs real-time, caching, and cost per 1k predictions.

Why this matters for AI/backend engineering:
    ML is a cost center until it is a profit center. Every architecture
    decision - batch vs realtime, GPU vs CPU, cache or not - is a dollar
    decision. Cost-per-1k-predictions is the unit engineers can actually
    optimize.

Run:      python 15-cost-optimization.py
Verify:   python 15-cost-optimization.py --verify
Reference: https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-machine-learning/welcome.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ============================================================
# 1. Cost per 1k Predictions
# ============================================================
# The canonical unit. Everything else (instance size, utilization,
# batching) reduces this number.

@dataclass
class ServingCost:
    instance_per_hour: float   # $/hr
    predictions_per_second: float
    utilization: float = 1.0   # fraction of the hour actually inferring

    def per_1k(self) -> float:
        per_hour_predictions = self.predictions_per_second * 3600 * self.utilization
        return self.instance_per_hour / (per_hour_predictions / 1000)


# Example 1: compare CPU vs GPU per 1k predictions
cpu = ServingCost(instance_per_hour=0.10, predictions_per_second=50.0)
gpu = ServingCost(instance_per_hour=0.90, predictions_per_second=1000.0)
print("Example 1: cost per 1k predictions")
print(f"  CPU:  ${cpu.per_1k():.5f}/1k predictions")
print(f"  GPU:  ${gpu.per_1k():.5f}/1k predictions")
assert gpu.per_1k() < cpu.per_1k(), "GPU wins at high volume"

# ============================================================
# 2. Utilization Is Half the Story
# ============================================================
# An idle GPU still bills. Autoscaling to zero and sharing instances
# matter as much as the per-inference cost.

@dataclass
class UtilizationScenario:
    name: str
    utilization: float

    def wasted_percent(self) -> float:
        return (1.0 - self.utilization) * 100


# Example 2: idle capacity is wasted money
scenarios = [
    UtilizationScenario("always-on, 20% utilized", 0.20),
    UtilizationScenario("autoscaling, 70% utilized", 0.70),
]
print("\nExample 2: utilization")
for s in scenarios:
    print(f"  {s.name}: {s.wasted_percent():.0f}% of capacity wasted")
assert scenarios[1].wasted_percent() < scenarios[0].wasted_percent()

# ============================================================
# 3. Batch vs Real-Time
# ============================================================
# If nothing needs the answer in 100ms, batch it. Batch processing
# uses the same GPU at 10x the throughput.

@dataclass
class BatchDecision:
    batch_job: float      # $ per batch run
    realtime_job: float   # $ per realtime run
    latency_requirement_ms: float
    batch_latency_ms: float

    def recommended(self) -> str:
        if self.batch_latency_ms <= self.latency_requirement_ms:
            return f"BATCH (${self.batch_job} vs ${self.realtime_job})"
        return "REALTIME (latency cannot wait for a batch window)"


# Example 3: latency decides the mode
nightly = BatchDecision(batch_job=0.05, realtime_job=2.00,
                        latency_requirement_ms=3600_000, batch_latency_ms=1800_000)
chat = BatchDecision(batch_job=0.05, realtime_job=2.00,
                     latency_requirement_ms=300, batch_latency_ms=1800_000)
print("\nExample 3: batch vs realtime")
print(f"  nightly report: {nightly.recommended()}")
print(f"  chat inference: {chat.recommended()}")
assert nightly.recommended().startswith("BATCH")
assert chat.recommended().startswith("REALTIME")

# ============================================================
# 4. Caching
# ============================================================
# Repeat queries are the cheapest queries. A cache hit costs ~$0.000001;
# a model call costs ~$0.001+. Even a 20% hit rate changes the bill.

@dataclass
class CacheEconomics:
    cache_hit_cost: float
    model_cost: float

    def effective_cost(self, hit_rate: float) -> float:
        return (1 - hit_rate) * self.model_cost + hit_rate * self.cache_hit_cost

    def savings_percent(self, hit_rate: float) -> float:
        return (1 - self.effective_cost(hit_rate) / self.model_cost) * 100


# Example 4: cache math
cache = CacheEconomics(cache_hit_cost=0.000001, model_cost=0.001)
print("\nExample 4: caching economics")
for rate in [0.0, 0.2, 0.5, 0.8]:
    print(f"  hit rate {rate:.0%}: cost={cache.effective_cost(rate):.6f} "
          f"savings={cache.savings_percent(rate):.1f}%")
assert cache.effective_cost(0.8) < cache.effective_cost(0.0)

# ============================================================
# 5. Spot / Preemptible
# ============================================================
# Training tolerates interruption; serving does not. Spot for training,
# on-demand for serving.

@dataclass
class SpotDecision:
    workload: str
    interruptible: bool

    def recommend(self) -> str:
        if self.interruptible:
            return f"{self.workload}: use spot (up to ~70% cheaper, resumable)"
        return f"{self.workload}: on-demand (cannot tolerate interruption)"


# Example 5: workload fit
print("\nExample 5: spot vs on-demand")
print("  " + SpotDecision("training", interruptible=True).recommend())
print("  " + SpotDecision("serving", interruptible=False).recommend())

# ============================================================
# Production Pattern
# ============================================================
# The cost checklist before shipping any ML service:
def cost_checklist() -> list[str]:
    return [
        "compute cost per 1k predictions",
        "utilization target (autoscale to zero when idle)",
        "batch vs realtime decided by latency requirement",
        "cache hit-rate model for repeat queries",
        "spot for training, on-demand for serving",
    ]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: comparing GPU and CPU by hourly price, not per-prediction
# MISTAKE: 24/7 instances for a workload that runs once a day
# MISTAKE: ignoring that 20% of queries are the same query


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    c = ServingCost(1.0, 1000.0, 1.0)
    assert abs(c.per_1k() - 1.0 / 3600) < 1e-6, "per-1k math"
    cheap = ServingCost(1.0, 1000.0, 0.5)
    assert cheap.per_1k() > c.per_1k(), "lower utilization -> higher cost"

    ce = CacheEconomics(0.0, 1.0)
    assert ce.effective_cost(0.5) == 0.5, "50% hit rate halves cost"
    assert ce.savings_percent(0.5) == 50.0

    assert BatchDecision(1, 10, 100.0, 500.0).recommended().startswith("REALTIME"), \
        "batch slower than SLO -> realtime"
    assert BatchDecision(1, 10, 100.0, 5.0).recommended().startswith("BATCH"), \
        "batch fits SLO -> batch"

    u = UtilizationScenario("x", 0.25)
    assert u.wasted_percent() == 75.0

    assert SpotDecision("training", True).recommend().startswith("training: use spot")
    assert SpotDecision("serving", False).recommend().startswith("serving: on-demand")
    assert len(cost_checklist()) == 5, "checklist complete"
    print("[OK] 15-cost-optimization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Optimize cost per 1k predictions, not hourly price.")
        print("2. Utilization, batching, caching: the big levers.")
        print("3. Spot for training; on-demand for serving.")
        _verify()
