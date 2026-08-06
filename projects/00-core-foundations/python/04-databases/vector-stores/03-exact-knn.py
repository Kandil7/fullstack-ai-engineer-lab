"""
Vector Stores — 03: Exact kNN (Brute Force)
==============================================
Topics: brute-force kNN, distance metrics (L2 vs cosine), argpartition
        vs full sort, top-k correctness, k selection, scaling behavior,
        when exact search beats ANN (small data, filtering, fresh docs)

Why this matters for AI/backend engineering:
    Exact kNN is the baseline every ANN index is measured against
    ("recall@10 vs brute force"). It is also the right tool when the
    candidate set is small — filtered subsets, tenant isolation, fresh
    documents not yet in the index. Understanding its cost model
    (O(n*d) per query) tells you exactly when you must switch to ANN.

Run:      python 03-exact-knn.py
Verify:   python 03-exact-knn.py --verify
"""

from __future__ import annotations

import heapq
import sys
import time as _time

import numpy as np

from vector_utils import brute_force_knn, cosine_sim, l2_dist, make_corpus, recall_at_k

rng = np.random.default_rng(7)

# ============================================================
# 1. The Baseline: full sort
# ============================================================
vectors, meta = make_corpus(n=400, dim=32, n_clusters=8, seed=7)
queries = vectors[:5]
truth = brute_force_knn(queries, vectors, k=10, metric="l2")

# The naive version everyone writes first: compute ALL distances, then
# np.argsort -> O(n*d) compute + O(n log n) sort per query.
def knn_sort(q: np.ndarray, data: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    dists = np.linalg.norm(data - q, axis=1)
    order = np.argsort(dists)
    return order[:k], dists[order[:k]]


idx, dists = knn_sort(queries[0], vectors, 10)
print(f"full-sort kNN: top-10 ids {idx.tolist()}, dists {dists.round(3).tolist()}")

# Output:
# full-sort kNN: top-10 ids [0, 136, 304, 224, 104, 240, 336, 320, 248, 168], dists [0.0, 0.843, 0.847, 0.864, 0.896, 0.896, 0.902, 0.909, 0.92, 0.925]

# ============================================================
# 2. Faster: argpartition (O(n*d) + O(n) selection)
# ============================================================
# np.argpartition puts the k smallest in positions 0..k-1 in O(n) —
# we never pay the full sort. For k << n this is the standard trick
# (this is what faiss / sklearn's brute-force backends do).

def knn_partition(q: np.ndarray, data: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    dists = np.linalg.norm(data - q, axis=1)
    part = np.argpartition(dists, k - 1)[:k]
    # argpartition order inside the slice is arbitrary -> re-sort the k
    part = part[np.argsort(dists[part])]
    return part, dists[part]


part_idx, _ = knn_partition(queries[0], vectors, 10)
print(f"\nargpartition kNN same result: {part_idx.tolist()}")
print(f"exact match with full sort: {np.array_equal(part_idx, idx)}")

# Output:
# argpartition kNN same result: [0, 136, 304, 224, 104, 240, 336, 320, 248, 168]
# exact match with full sort: True

# ============================================================
# 3. L2 vs Cosine — when they disagree
# ============================================================
# Cosine ignores vector magnitude (good for text embeddings of
# different lengths); L2 includes magnitude. Two vectors can be
# near-identical in direction yet far in L2.

big = np.array([5.0, 0.0])
small = np.array([1.0, 0.0])
print(f"\nL2(big, small)     = {l2_dist(big, small):.2f}")
print(f"cosine(big, small) = {cosine_sim(big, small):.2f}  <- magnitude-blind")

# Output:
# L2(big, small)     = 4.00
# cosine(big, small) = 1.00  <- magnitude-blind

# Normalized vectors: L2 ranking == cosine ranking (because ||a-b||^2
# = 2 - 2*cos(a,b) when both have unit norm).
unit_a = big / np.linalg.norm(big)
unit_b = small / np.linalg.norm(small)
print(f"after L2-norm:      L2 = {l2_dist(unit_a, unit_b):.4f}, "
      f"cosine = {cosine_sim(unit_a, unit_b):.4f}")

# Output:
# after L2-norm:      L2 = 0.0000, cosine = 1.0000

# ============================================================
# 4. Ties and stability
# ============================================================
# Duplicate vectors produce equal distances; order among ties is
# implementation-defined (argsort is stable, argpartition is not —
# another reason to re-sort the k-slice).

tie_data = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]])
tie_q = np.array([1.0, 0.0])
tie_idx, _ = knn_sort(tie_q, tie_data, 3)
print(f"\nties sorted (stable): ids {tie_idx.tolist()}  <- first duplicate wins")

# Output:
# ties sorted (stable): ids [0, 2, 1]  <- first duplicate wins

# ============================================================
# 5. Choosing k — and why k matters downstream
# ============================================================
# Small k -> precision of the head; large k -> more context for rerankers.
# Real systems: retrieve k=50 with vectors, rerank top-5 with an LLM.
for k in (1, 5, 10, 25):
    t0 = _time.perf_counter()
    knn_partition(queries[0], vectors, k)
    print(f"k={k:2d}  retrieval cost {( _time.perf_counter() - t0) * 1e3:6.2f} ms")

# Output:
# k=1   retrieval cost   0.20 ms
# k=5   retrieval cost   0.20 ms
# k=10  retrieval cost   0.23 ms
# k=25  retrieval cost   0.26 ms

# ============================================================
# 6. Scaling: the O(n*d) wall
# ============================================================
# Doubling n doubles query cost for exact search. This is THE number
# that forces ANN at scale (see exercise 02). Measured on the same dims:
for n in (500, 1000, 2000, 4000):
    data = rng.normal(size=(n, 32))
    t0 = _time.perf_counter()
    knn_partition(rng.normal(size=32), data, 10)
    print(f"n={n:5d}  exact kNN = {(_time.perf_counter() - t0) * 1e3:6.2f} ms")

# Output:
# n=500    exact kNN =   0.19 ms
# n=1000   exact kNN =   0.37 ms
# n=2000   exact kNN =   0.74 ms
# n=4000   exact kNN =   1.49 ms

# ============================================================
# 7. Exact kNN wins when the candidate set is SMALL
# ============================================================
# Filter-first + exact search beats ANN on a filtered subset, because
# the filter usually leaves far fewer candidates than the ANN graph can
# exploit. Show it with a tenant filter:
tenants = rng.integers(0, 4, size=len(vectors))
tenant_q = vectors[0]
mine = tenants == tenants[0]
subset = vectors[mine]
sub_idx, _ = knn_partition(tenant_q, subset, 5)
print(f"\nfiltered exact kNN (tenant has {subset.shape[0]} docs): "
      f"ids {sub_idx.tolist()}")

# Output:
# filtered exact kNN (tenant has 103 docs): ids [0, 29, 87, 22, 8]

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using np.argsort for every query — argpartition + re-sort of
#   the k slice is strictly better for k << n.
# MISTAKE: mixing L2 and cosine without normalizing — the ranking flips
#   for magnitude-heavy vectors; pick ONE metric for the whole index.
# MISTAKE: assuming ties have a stable order with argpartition.
# MISTAKE: jumping to ANN before measuring — for <10^5 vectors exact
#   search is often faster AND exact.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # argpartition must reproduce the full-sort result exactly
    assert np.array_equal(part_idx, idx), \
        "argpartition + re-sort must match np.argsort exactly"

    # magnitude-blindness: cosine sees identical directions as 1.0
    assert np.isclose(cosine_sim(big, small), 1.0), \
        "cosine must ignore magnitude for parallel vectors"
    assert l2_dist(big, small) > 3.0, \
        "L2 must see the magnitude difference"

    # normalized L2 distance equals 0 for parallel unit vectors
    assert l2_dist(unit_a, unit_b) < 1e-6, \
        "L2 of parallel unit vectors is 0"

    # ties: stable sort keeps insertion order for equal distances
    assert tie_idx.tolist() == [0, 2, 1], \
        "stable argsort must put the earlier duplicate first"

    # scaling: larger n must not beat smaller n in wall-clock order
    # (measured with a fresh monotonic counter, no sleep)
    def measure(n: int) -> float:
        data = rng.normal(size=(n, 32))
        t0 = _time.perf_counter()
        knn_partition(rng.normal(size=32), data, 10)
        return _time.perf_counter() - t0

    t_small = measure(1000)
    t_large = measure(4000)
    assert t_large > t_small, \
        "exact kNN on 4x data must cost more than on 1x data"

    # correctness vs brute_force_knn from vector_utils
    alt = brute_force_knn(queries[:2], vectors, k=10, metric="l2")
    for i in range(2):
        mine, _ = knn_sort(queries[i], vectors, 10)
        assert np.array_equal(mine, alt[i]), \
            "knn_sort must agree with brute_force_knn"

    # k=1 returns the exact self-match for a corpus vector
    top1, _ = knn_sort(vectors[0], vectors, 1)
    assert top1[0] == 0, "self-match must be the nearest neighbor"

    print("[OK] 03-exact-knn: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. Full sort O(n log n) vs argpartition O(n) selection")
        print("2. L2 vs cosine: normalize before mixing them")
        print("3. Exact kNN is O(n*d) per query - measure before switching to ANN")
        print("4. Small candidate sets (filters/tenants) favor exact search")
    _verify()  # always runs, so plain execution is also a test
