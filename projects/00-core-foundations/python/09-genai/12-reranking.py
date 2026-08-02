"""
GenAI - 12: Reranking
=====================
Topics: cross-encoders, latency vs quality, two-stage retrieval, k
tuning, cost per query.

Why this matters for AI/backend engineering:
    Bi-encoders (embeddings) are fast but coarse; cross-encoders are
    precise but slow. Two-stage retrieval - cheap recall first, precise
    rerank second - gives you both. Knowing WHEN to rerank and how many
    candidates to rerank is the optimization.

Run:      python 12-reranking.py
Verify:   python 12-reranking.py --verify
Reference: https://www.sbert.net/examples/applications/retrieve_rerank/README.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ============================================================
# 1. Bi-Encoder vs Cross-Encoder
# ============================================================
# Bi-encoder: embed query and docs separately (fast, precomputable).
# Cross-encoder: score query+doc TOGETHER through the model (slow,
# per-pair, but much more accurate).

@dataclass
class Retriever:
    name: str
    latency_ms: float
    quality: float  # 0..1

    def describe(self) -> str:
        return (f"{self.name}: {self.latency_ms}ms per query, "
                f"quality {self.quality:.2f}")


# Example 1: the tradeoff
bi = Retriever("bi-encoder", latency_ms=5.0, quality=0.60)
cross = Retriever("cross-encoder", latency_ms=120.0, quality=0.92)
print("Example 1: two-stage components")
print(f"  {bi.describe()}")
print(f"  {cross.describe()}")
assert cross.latency_ms > bi.latency_ms and cross.quality > bi.quality

# ============================================================
# 2. Two-Stage Retrieval
# ============================================================
# Stage 1: recall 50-100 candidates cheaply. Stage 2: rerank the top-k
# with the cross-encoder. Total latency stays small because the slow
# model only sees a handful of pairs.

def two_stage(query: str, stage1_candidates: list[str], rerank_scores: dict[str, float],
              rerank_k: int = 3) -> list[str]:
    """Retrieve broadly, then rerank precisely."""
    top_k = stage1_candidates[:rerank_k]
    scored = sorted(top_k, key=lambda d: rerank_scores.get(d, 0.0), reverse=True)
    return scored


# Example 2: rerank changes the order
candidates = ["d1", "d4", "d2", "d3", "d5"]
rerank_scores = {"d4": 0.95, "d1": 0.90, "d2": 0.60, "d3": 0.10, "d5": 0.05}
final = two_stage("query", candidates, rerank_scores, rerank_k=3)
print("\nExample 2: two-stage retrieval")
print(f"  stage-1 top-3: {candidates[:3]}")
print(f"  after rerank:  {final}")
assert final[0] == "d4", "reranker pulls d4 to the top"

# ============================================================
# 3. k Tuning: The Cost/Quality Frontier
# ============================================================
# Reranking more candidates = better recall ceiling, higher latency and
# cost. Find the k where quality stops improving.

def rerank_economics(candidates_available: int, rerank_latency_ms: float,
                     quality_at_k: dict[int, float]) -> dict:
    best_k = max(quality_at_k, key=quality_at_k.get)
    best = quality_at_k[best_k]
    return {
        "best_k": best_k,
        "best_quality": best,
        "latency_ms_at_best": rerank_latency_ms * best_k,
        "candidates_available": candidates_available,
    }


# Example 3: quality plateaus at k=5 - reranking more adds nothing
quality_at_k = {1: 0.55, 2: 0.70, 3: 0.80, 4: 0.82, 5: 0.83, 10: 0.83}
econ = rerank_economics(candidates_available=50, rerank_latency_ms=5.0, quality_at_k=quality_at_k)
print("\nExample 3: k tuning")
print(f"  quality plateaus at k={econ['best_k']} -> quality {econ['best_quality']}")
print(f"  rerank latency at that k: {econ['latency_ms_at_best']}ms")
assert econ["best_k"] <= 5, "quality plateaus; don't rerank everything"

# ============================================================
# 4. Cost per Query
# ============================================================
# Reranking costs real money and latency: k pairs through a big model.
# Budget the rerank stage explicitly.

def cost_per_query(stage1_cost: float, rerank_k: int, rerank_pair_cost: float) -> dict:
    return {
        "stage1": stage1_cost,
        "rerank": rerank_k * rerank_pair_cost,
        "total": stage1_cost + rerank_k * rerank_pair_cost,
    }


# Example 4: budget math
costs = cost_per_query(stage1_cost=0.0001, rerank_k=5, rerank_pair_cost=0.0005)
print("\nExample 4: cost per query")
print(f"  stage-1 ${costs['stage1']:.5f} + rerank ${costs['rerank']:.5f} "
      f"= ${costs['total']:.5f}/query")
assert costs["total"] == 0.0001 + 5 * 0.0005

# ============================================================
# Production Pattern
# ============================================================
# Decide WHEN reranking pays: only when the baseline retrieval quality
# is the bottleneck AND the budget allows the extra latency/cost.

def should_rerank(baseline_quality: float, target_quality: float,
                  latency_budget_ms: float, rerank_latency_ms: float) -> tuple[bool, str]:
    if baseline_quality >= target_quality:
        return False, "baseline already meets target - skip reranking"
    if rerank_latency_ms > latency_budget_ms:
        return False, "rerank exceeds latency budget"
    return True, "rerank is worth it: quality gap + latency fits"


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: reranking all 10k candidates (latency/cost explosion)
# MISTAKE: adding reranking when embeddings already meet the target
# MISTAKE: not tuning k - quality plateaus and you pay anyway
# MISTAKE: ignoring that cross-encoders need GPU to stay fast


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert two_stage("q", ["a", "b", "c"], {"c": 1.0, "a": 0.1}, 3)[0] == "c"
    assert two_stage("q", ["a", "b"], {"a": 0.1, "b": 0.9}, 2)[0] == "b"

    assert rerank_economics(10, 5.0, {1: 0.5, 2: 0.9})["best_k"] == 2
    assert rerank_economics(10, 5.0, {1: 0.9, 2: 0.9})["best_k"] == 1, "first max wins on plateau"

    c = cost_per_query(0.001, 3, 0.01)
    assert c["total"] == 0.031, "cost math"

    ok, _ = should_rerank(0.9, 0.95, 50.0, 100.0)
    assert not ok, "latency budget blocks rerank"
    ok2, msg2 = should_rerank(0.7, 0.95, 500.0, 100.0)
    assert ok2, "gap + budget -> rerank"
    ok3, _ = should_rerank(0.99, 0.95, 50.0, 10.0)
    assert not ok3, "no gap -> no rerank"
    print("[OK] 12-reranking: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Bi-encoders recall broadly; cross-encoders rerank precisely.")
        print("2. Two-stage = cheap recall, then rerank only the top-k.")
        print("3. Tune k at the quality plateau; budget cost and latency.")
        _verify()
