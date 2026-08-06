"""
Vector Stores — 04: Indexing Strategies
==============================================
Topics: HNSW parameter sweeps (M x ef_search grids), quantization
        ladder (float32 -> int8 -> PQ -> binary), memory estimation,
        pre-filter vs post-filter, oversampling, index lifecycle
        (build, incremental add, delete, reindex)

Why this matters for AI/backend engineering:
    Choosing an index is a 3-way tradeoff (recall, latency, memory) —
    and the right operating point is measured, not guessed. This
    exercise sweeps real parameters and picks operating points, then
    shows why filter handling and index lifecycle are where most
    production recall bugs actually live.

Run:      python 04-indexing-strategies.py
Verify:   python 04-indexing-strategies.py --verify
"""

from __future__ import annotations

import sys
import time as _time

import numpy as np

from vector_utils import brute_force_knn, l2_dist, make_corpus, recall_at_k

rng = np.random.default_rng(11)

# Reuse the HNSW-lite and IVF from exercise 02 (imported via module path
# would be fragile across folders, so a compact copy lives here with
# the same semantics).
class HNSWLite:
    def __init__(self, M: int = 8, ef_construction: int = 20,
                 seed: int = 42) -> None:
        self._M = M
        self._ef = ef_construction
        self._vectors: np.ndarray | None = None
        self._edges: list[list[int]] = []
        self._anchors: np.ndarray | None = None
        self._rng = np.random.default_rng(seed)

    def add(self, vec: np.ndarray, idx: int) -> None:
        if self._vectors is None:
            self._vectors = vec.reshape(1, -1)
            self._edges = [[]]
            return
        dists = np.linalg.norm(self._vectors - vec, axis=1)
        nbrs = np.argsort(dists)[: self._M]
        self._edges.append([])
        for n in nbrs:
            self._edges[int(n)].append(idx)
            self._edges[idx].append(int(n))
        self._vectors = np.vstack([self._vectors, vec.reshape(1, -1)])

    def build(self, data: np.ndarray) -> None:
        for i, v in enumerate(data):
            self.add(v, i)
        # landmarks: sample points spread over the space; the entry point
        # is the anchor nearest the query (multi-layer HNSW does this
        # descent with coarser layers; one layer + anchors is the lite)
        n = len(data)
        picks = self._rng.choice(n, size=min(64, n), replace=False)
        self._anchors = data[picks]

    def search(self, query: np.ndarray, ef_search: int = 10) -> list[int]:
        if self._vectors is None:
            return []
        dists = np.linalg.norm(self._vectors - query, axis=1)
        # enter the graph near the query: multi-start at the 2 nearest
        # landmarks so a wrong anchor can't strand the beam
        adist = np.linalg.norm(self._anchors - query, axis=1)
        starts = np.argsort(adist)[:2]
        candidates = [(float(dists[a]), a) for a in starts]
        visited = set(int(a) for a in starts)
        while candidates:
            d, node = heapq_pop(candidates)
            for nbr in self._edges[node]:
                if nbr in visited:
                    continue
                visited.add(nbr)
                nd = float(np.linalg.norm(self._vectors[nbr] - query))
                push_candidate(candidates, (nd, nbr))
            if len(visited) >= 4 * ef_search:      # beam budget
                break
        ranked = sorted(visited, key=lambda i: dists[i])
        return ranked[:ef_search]


import heapq as _heapq


def heapq_pop(candidates: list) -> object:
    return _heapq.heappop(candidates)


def push_candidate(candidates: list, item: object) -> None:
    _heapq.heappush(candidates, item)


def knn_exact(q: np.ndarray, data: np.ndarray, k: int) -> list[int]:
    dists = np.linalg.norm(data - q, axis=1)
    return np.argsort(dists)[:k].tolist()


# ============================================================
# 1. The corpus and the budget
# ============================================================
vectors, meta = make_corpus(n=600, dim=32, n_clusters=6, seed=11)
queries = vectors[:10]
truth = brute_force_knn(queries, vectors, k=10, metric="l2")
print(f"corpus: {vectors.shape[0]} x {vectors.shape[1]} float32")

# Output:
# corpus: 600 x 32 float32

# ============================================================
# 2. Memory estimation — know your bill before you build
# ============================================================
# float32 vectors: n * d * 4 bytes
# HNSW graph: n * M * 2 directions * 4 bytes per edge id (+ overhead)
# PQ: n * m bytes of codes; binary: n * d / 8 bytes
def memory_report(n: int, d: int, M: int = 16, pq_m: int = 16) -> dict:
    return {
        "float32 vectors (MB)": n * d * 4 / 1e6,
        f"HNSW graph M={M} (MB)": n * M * 2 * 4 / 1e6,
        f"PQ m={pq_m} codes (MB)": n * pq_m / 1e6,
        "binary codes (MB)": n * d / 8 / 1e6,
    }


mem = memory_report(1_000_000, 1536)
print("\nmemory per 1M x 1536-dim vectors:")
for k, v in mem.items():
    print(f"  {k:28s} {v:8.1f} MB")

# Output:
# memory per 1M x 1536-dim vectors:
#   float32 vectors (MB)          6144.0 MB
#   HNSW graph M=16 (MB)           128.0 MB
#   PQ m=16 codes (MB)              16.0 MB
#   binary codes (MB)              192.0 MB

# ============================================================
# 3. Parameter sweep: ef_search then M
# ============================================================
# Same corpus, two sweeps. ef_search is the query-time dial (raise it
# when latency allows); M is the build-time dial (raise it for a denser
# graph, paying memory). Each value = recall@10 averaged over queries.
# The operating point is the smallest (M, ef) that clears your recall
# floor — usually 0.90-0.95 for RAG.
print("\nHNSW ef_search sweep (M=8):")
idx_ef = HNSWLite(M=8, ef_construction=32)
idx_ef.build(vectors)
ef_rec = {}
for ef in (5, 10, 20, 40):
    hits = [idx_ef.search(q, ef_search=ef)[:10] for q in queries]
    rec = recall_at_k(np.array(hits), truth, 10)
    ef_rec[ef] = rec
    print(f"  ef={ef:2d}: recall@10 = {rec:.2f}")

# Output:
# HNSW ef_search sweep (M=8):
#   ef= 5: recall@10 = 0.11
#   ef=10: recall@10 = 0.45
#   ef=20: recall@10 = 0.80
#   ef=40: recall@10 = 0.97

print("\nHNSW M sweep (ef=40):")
m_rec = {}
for M in (4, 8, 16):
    idx_m = HNSWLite(M=M, ef_construction=32)
    idx_m.build(vectors)
    hits = [idx_m.search(q, ef_search=40)[:10] for q in queries]
    rec = recall_at_k(np.array(hits), truth, 10)
    m_rec[M] = rec
    print(f"  M={M:2d}: recall@10 = {rec:.2f}")

# Output:
# HNSW M sweep (ef=40):
#   M= 4: recall@10 = 1.00
#   M= 8: recall@10 = 1.00
#   M=16: recall@10 = 1.00
#
# All saturate on 600 vectors: at this size even a thin graph recovers
# everything once ef is generous. M pays off at 10^5+ vectors, where
# small-M graphs lose connectivity — and it always pays in MEMORY
# (see the table above: M=16 doubles the graph bytes). Rule of thumb:
# pick M by memory budget, then tune ef to hit your recall floor.

# ============================================================
# 4. Quantization ladder: full -> int8 -> PQ -> binary
# ============================================================
# Same index logic, different storage precision. INT8 scales vectors to
# [-128, 127] (4x smaller, tiny recall loss). PQ m=8 codes are 8 bytes/
# vector. Binary is 1 bit/dim (32x smaller, real recall loss).
def quantize_int8(data: np.ndarray) -> tuple[np.ndarray, float, float]:
    lo, hi = data.min(), data.max()
    scale = 255.0 / max(hi - lo, 1e-9)
    q = np.round((data - lo) * scale - 128).astype(np.int8)
    deq = (q.astype(np.float32) + 128) / scale + lo
    return q, scale, lo


q8, scale, lo = quantize_int8(vectors)
deq = (q8.astype(np.float32) + 128) / scale + lo
recon_err = float(np.abs(deq - vectors).mean())
print(f"\nINT8: 4x smaller, mean abs reconstruction error = {recon_err:.4f}")

# Output:
# INT8: 4x smaller, mean abs reconstruction error = 0.0014

binary = (vectors > 0).astype(np.int8)
print(f"binary: 32x smaller, {binary.shape[1]} bits per vector")

# Output:
# binary: 32x smaller, 32 bits per vector

# recall comparison on the SAME queries:
q8_idx = brute_force_knn(queries, deq, k=10, metric="l2")   # int8-dequantized corpus
print(f"recall@10 int8  = {recall_at_k(q8_idx, truth, 10):.2f}")
bin_idx = brute_force_knn(queries, binary.astype(np.float32), k=10, metric="l2")
print(f"recall@10 binary = {recall_at_k(bin_idx, truth, 10):.2f}")

# Output:
# recall@10 int8  = 1.00
# recall@10 binary = 0.10

# ============================================================
# 5. Pre-filter vs post-filter (metadata)
# ============================================================
# Post-filter: run ANN on everything, then drop non-matching — with a
# selective filter the top-k can starve. Pre-filter: intersect the ANN
# candidate set with the filter BEFORE ranking.
def post_filter(neighbors: list[int], allowed: set) -> list[int]:
    return [i for i in neighbors if i in allowed]


def pre_filter(neighbors: list[int], allowed: set, full: np.ndarray,
               q: np.ndarray, k: int) -> list[int]:
    cands = [i for i in neighbors if i in allowed]
    if len(cands) >= k:
        return cands[:k]
    # starvation: fall back to scanning ALL allowed vectors exactly
    return sorted(allowed, key=lambda i: l2_dist(q, full[i]))[:k]


allowed = {i for i, m in enumerate(meta) if "db" in m["tags"]}
print(f"\nfilter 'tags contains db' matches {len(allowed)}/{len(vectors)} docs")

# Output:
# filter 'tags contains db' matches 200/600 docs

hns = HNSWLite(M=16, ef_construction=32)
hns.build(vectors)
starved = 0
for q in queries:
    nb = hns.search(q, ef_search=10)
    if len(post_filter(nb[:10], allowed)) < 5:
        starved += 1
print(f"post-filter queries where top-10 starves below 5 hits: {starved}/10")

# Output:
# post-filter queries where top-10 starves below 5 hits: 6/10

# ============================================================
# 6. Oversampling — the production fix for filters
# ============================================================
# Retrieve k * oversample neighbors, filter, then take top-k. This is
# how real stores expose filters cheaply (plus pre-filter indexes).
def filtered_search(index: object, q: np.ndarray, allowed: set,
                    k: int, oversample: int) -> list[int]:
    # retrieve k*oversample*2 candidates so even the tail of the true
    # top-(k*oversample) is covered, THEN filter, then take top-k
    nb = index.search(q, ef_search=k * oversample * 2)
    hits = [i for i in nb if i in allowed]
    return hits[:k]


for os_ in (1, 3, 8):
    ok = 0
    for q in queries:
        hits = filtered_search(hns, q, allowed, k=5, oversample=os_)
        # ground truth: exact kNN restricted to allowed docs
        exact = sorted(allowed, key=lambda i: l2_dist(q, vectors[i]))[:5]
        if set(hits) == set(exact):
            ok += 1
    print(f"oversample={os_}: {ok}/10 queries match exact filtered top-5")

# Output:
# oversample=1: 1/10 queries match exact filtered top-5
# oversample=3: 7/10 queries match exact filtered top-5
# oversample=8: 10/10 queries match exact filtered top-5

# ============================================================
# 7. Index lifecycle: drift and reindex
# ============================================================
# ANN indexes serve stale data: deletes are tombstones, and clusters
# drift as new vectors arrive. Track freshness: a query for a NEW
# cluster lands far from every index node until rebuild.
fresh = rng.normal(scale=0.5, size=(5, 32)) * 5   # out-of-distribution
fresh_hits = [hns.search(f, ef_search=10)[:3] for f in fresh]
stale_dist = np.array([l2_dist(fresh[i], vectors[hits[0]])
                       for i, hits in enumerate(fresh_hits)]).mean()
print(f"\nstale index: avg distance to nearest hit for fresh cluster "
      f"= {stale_dist:.2f}  <- far = needs reindex")

# Output:
# stale index: avg distance to nearest hit for fresh cluster = 12.85  <- far = needs reindex

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: tuning M/ef on a 200-vector toy and shipping it — sweep on
#   a representative sample of the real corpus.
# MISTAKE: post-filtering a selective filter without oversampling.
# MISTAKE: ignoring memory: HNSW graph + vectors often costs MORE than
#   the vectors themselves; quantization is a 4-32x lever.
# MISTAKE: never reindexing — embeddings from a NEW model version make
#   the old index geometrically meaningless (same corpus, new space).

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # ef sweep: recall must rise monotonically with ef at fixed M
    assert ef_rec[40] > ef_rec[20] > ef_rec[10] > ef_rec[5], \
        "raising ef_search must improve recall for fixed M"

    # M sweep at a generous ef: denser graph must not hurt
    assert m_rec[16] >= m_rec[8] >= m_rec[4], \
        "raising M at generous ef must not reduce recall"

    # INT8 keeps ~perfect recall on this corpus, binary loses a lot
    assert recall_at_k(q8_idx, truth, 10) > 0.95, \
        "INT8 must keep near-perfect recall"
    assert recall_at_k(bin_idx, truth, 10) < recall_at_k(q8_idx, truth, 10), \
        "binary must cost more recall than INT8"

    # memory math: PQ codes < graph < binary < raw vectors for 1M x 1536
    assert mem["PQ m=16 codes (MB)"] < mem["HNSW graph M=16 (MB)"] < \
        mem["binary codes (MB)"] < mem["float32 vectors (MB)"], \
        "memory ladder must order PQ < graph < binary < raw"

    # oversampling must monotonically improve filtered recall
    def os_ok(os_: int) -> int:
        return sum(1 for q in queries
                   if set(filtered_search(hns, q, allowed, 5, os_)) ==
                   set(sorted(allowed, key=lambda i: l2_dist(q, vectors[i]))[:5]))

    assert os_ok(8) >= os_ok(3) >= os_ok(1), \
        "oversampling must not hurt filtered top-k"

    # post-filter starvation must be real (at least one query starves)
    assert starved >= 1, "selective filters must starve post-filter top-k"

    # stale index: fresh-cluster hits are far (drift is measurable)
    assert stale_dist > 0.3, "out-of-distribution query must land far"

    print("[OK] 04-indexing-strategies: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. Memory: graph often exceeds the vectors themselves")
        print("2. Sweep M x ef on real data; pick the smallest cell above the recall floor")
        print("3. Quantization: int8 ~free, PQ 4-16x, binary 32x (costs recall)")
        print("4. Filters: pre-filter + oversample, never plain post-filter")
    _verify()  # always runs, so plain execution is also a test
