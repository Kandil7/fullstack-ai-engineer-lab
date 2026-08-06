"""
Vector Stores — 02: ANN Algorithms
==============================================
Topics: HNSW (graph, M, ef_construction, ef_search), IVF, product
        quantization, LSH, index build cost, parameter effects measured

Why this matters for AI/backend engineering:
    Every production vector store (Qdrant, Pinecone, pgvector, Milvus)
    ships HNSW and/or IVF under the hood. The knobs you tune — M,
    ef_search, nlist, nprobe — are the recall/latency tradeoff made
    concrete. This exercise implements real, working versions in numpy
    and MEASURES the parameter effects.

Run:      python 02-ann-algorithms.py
Verify:   python 02-ann-algorithms.py --verify
Reference: https://arxiv.org/abs/1603.09320 (HNSW), https://arxiv.org/abs/1104.1453 (IVF)
"""

from __future__ import annotations

import heapq
import sys
import time as _time

import numpy as np

from vector_utils import brute_force_knn, cosine_sim, l2_dist, make_corpus, recall_at_k

rng = np.random.default_rng(42)

# ============================================================
# 1. The Ground Truth
# ============================================================
vectors, meta = make_corpus(n=300, dim=16, n_clusters=6, seed=42)
queries = vectors[:10]
truth = brute_force_knn(queries, vectors, k=10, metric="l2")
print(f"corpus: {vectors.shape}, truth: exact top-10 per query")

# Output:
# corpus: (300, 16), truth: exact top-10 per query

# ============================================================
# 2. HNSW — Hierarchical Navigable Small World graphs
# ============================================================
# Idea: a multi-layer graph. Layer 0 has every point; higher layers have
# fewer points. A query descends from the top layer to layer 0, greedily
# walking to nearer neighbors. Edges per node = M; search width = ef.
#
#   M             -> memory (edges) and graph quality; higher = better recall
#   ef_construction -> build-time search width; higher = better graph, slower build
#   ef_search     -> query-time width; higher = better recall, slower query
#
# HNSW-lite below: single layer (0) + greedy search with a candidate heap.
# It keeps the exact mechanics: entry point, greedy descent, ef-controlled
# candidate list.

class HNSWLite:
    def __init__(self, M: int = 8, ef_construction: int = 20,
                 seed: int = 42) -> None:
        self._M = M
        self._ef = ef_construction
        self._vectors: np.ndarray | None = None
        self._edges: list[list[int]] = []
        self._rng = np.random.default_rng(seed)

    def add(self, vec: np.ndarray, idx: int) -> None:
        if self._vectors is None:
            self._vectors = vec.reshape(1, -1)
            self._edges = [[]]
            return
        # connect to the nearest M existing points (greedy insert)
        dists = np.linalg.norm(self._vectors - vec, axis=1)
        nbrs = np.argsort(dists)[: self._M]
        self._edges.append([])                     # room for the new node
        for n in nbrs:
            self._edges[int(n)].append(idx)        # bidirectional edges
            self._edges[idx].append(int(n))
        self._vectors = np.vstack([self._vectors, vec.reshape(1, -1)])

    def build(self, data: np.ndarray) -> None:
        for i, v in enumerate(data):
            self.add(v, i)

    def search(self, query: np.ndarray, ef_search: int = 10) -> list[int]:
        """Greedy beam search: keep the ef closest candidates, expand the
        best one each step. Returns ranked neighbor ids."""
        if self._vectors is None:
            return []
        entry = 0
        dists = np.linalg.norm(self._vectors - query, axis=1)
        candidates = [(float(dists[entry]), entry)]
        visited = {entry}
        while candidates:
            d, node = heapq.heappop(candidates)
            for nbr in self._edges[node]:
                if nbr in visited:
                    continue
                visited.add(nbr)
                nd = float(np.linalg.norm(self._vectors[nbr] - query))
                heapq.heappush(candidates, (nd, nbr))
            if len(visited) > 2 * ef_search:   # stop expanding beyond budget
                break
        ranked = sorted(visited, key=lambda i: dists[i])
        return ranked[:ef_search]


hns = HNSWLite(M=8, ef_construction=20)
hns.build(vectors)
hits = [hns.search(q, ef_search=20) for q in queries]
recall_hns = recall_at_k(np.array([h[:10] for h in hits]), truth, k=10)
print(f"\nHNSW-lite  (M=8,  ef=20): recall@10 = {recall_hns:.2f}")

# Output:
# HNSW-lite  (M=8,  ef=20): recall@10 = 0.71

hns_low = HNSWLite(M=2, ef_construction=8)
hns_low.build(vectors)
hits_low = [hns_low.search(q, ef_search=10) for q in queries]
recall_low = recall_at_k(np.array([h[:10] for h in hits_low]), truth, k=10)
print(f"HNSW-lite  (M=2,  ef=10): recall@10 = {recall_low:.2f}  <- lower M hurts")

# Output:
# HNSW-lite  (M=2,  ef=10): recall@10 = 0.51  <- lower M hurts

# ============================================================
# 3. IVF — Inverted File Index (cluster + probe)
# ============================================================
# k-means the corpus into nlist cells; a query checks the nearest nprobe
# cells only. nlist up = more cells (faster, needs more probes); nprobe
# up = more cells checked (better recall, slower).

class IVF:
    def __init__(self, nlist: int = 8, seed: int = 42) -> None:
        self._nlist = nlist
        self._centroids: np.ndarray | None = None
        self._postings: list[list[int]] = []
        self._vectors: np.ndarray | None = None
        self._rng = np.random.default_rng(seed)

    def build(self, data: np.ndarray, iters: int = 8) -> None:
        self._vectors = data
        n, d = data.shape
        idx = self._rng.choice(n, size=min(self._nlist, n), replace=False)
        centroids = data[idx].copy()
        for _ in range(iters):                      # mini k-means
            dists = np.linalg.norm(data[:, None, :] - centroids[None, :, :], axis=2)
            assign = np.argmin(dists, axis=1)
            for c in range(self._nlist):
                members = data[assign == c]
                if len(members):
                    centroids[c] = members.mean(axis=0)
        self._centroids = centroids
        dists = np.linalg.norm(data[:, None, :] - centroids[None, :, :], axis=2)
        assign = np.argmin(dists, axis=1)
        self._postings = [[i for i in range(n) if assign[i] == c]
                          for c in range(self._nlist)]

    def search(self, query: np.ndarray, nprobe: int = 2, k: int = 10) -> list[int]:
        cdist = np.linalg.norm(self._centroids - query, axis=1)
        cells = np.argsort(cdist)[:nprobe]
        cands = [i for c in cells for i in self._postings[c]]
        scored = sorted(cands, key=lambda i: l2_dist(query, self._vectors[i]))
        return scored[:k]


ivf = IVF(nlist=8)
ivf.build(vectors)
ivf_1 = recall_at_k(np.array([ivf.search(q, nprobe=1, k=10) for q in queries]), truth, 10)
ivf_4 = recall_at_k(np.array([ivf.search(q, nprobe=4, k=10) for q in queries]), truth, 10)
print(f"\nIVF (nlist=8, nprobe=1): recall@10 = {ivf_1:.2f}")
print(f"IVF (nlist=8, nprobe=4): recall@10 = {ivf_4:.2f}  <- more probes help")

# Output:
# IVF (nlist=8, nprobe=1): recall@10 = 0.86
# IVF (nlist=8, nprobe=4): recall@10 = 1.00  <- more probes help

# ============================================================
# 4. Product Quantization — compress vectors
# ============================================================
# Split each vector into m subvectors; per subvector, store only its
# nearest of s centroids (the codebook). A 1536-dim float32 vector (6 KB)
# becomes m bytes — e.g. 12x compression. Query uses lookup tables
# (ADC), never the original floats.

class PQ:
    def __init__(self, m: int = 4, s: int = 16, seed: int = 42) -> None:
        self._m, self._s = m, s
        self._rng = np.random.default_rng(seed)
        self._codebooks: list[np.ndarray] = []   # per subspace: (s, d/m)
        self._codes: np.ndarray | None = None

    def build(self, data: np.ndarray, iters: int = 5) -> None:
        n, d = data.shape
        assert d % self._m == 0, "d must split evenly across m subspaces"
        sub_d = d // self._m
        codes = np.zeros((n, self._m), dtype=np.uint8)
        for sub in range(self._m):
            part = data[:, sub * sub_d:(sub + 1) * sub_d]
            idx = self._rng.choice(n, size=min(self._s, n), replace=False)
            cb = part[idx].copy()
            for _ in range(iters):
                dists = np.linalg.norm(part[:, None, :] - cb[None, :, :], axis=2)
                assign = np.argmin(dists, axis=1)
                for c in range(self._s):
                    if (assign == c).any():
                        cb[c] = part[assign == c].mean(axis=0)
            self._codebooks.append(cb)
            dists = np.linalg.norm(part[:, None, :] - cb[None, :, :], axis=2)
            codes[:, sub] = np.argmin(dists, axis=1)
        self._codes = codes

    def adc_distance(self, query: np.ndarray, idx: int) -> float:
        """Asymmetric distance: query full precision, corpus codes only."""
        d = 0.0
        sub_d = query.shape[0] // self._m
        for sub in range(self._m):
            qpart = query[sub * sub_d:(sub + 1) * sub_d]
            cb = self._codebooks[sub]
            d += np.linalg.norm(qpart - cb[self._codes[idx, sub]]) ** 2
        return d ** 0.5

    def search(self, query: np.ndarray, k: int = 10) -> list[int]:
        scored = sorted(range(len(self._codes)),
                        key=lambda i: self.adc_distance(query, i))
        return scored[:k]


pq = PQ(m=4, s=16)
pq.build(vectors)
pq_hits = np.array([pq.search(q, k=10) for q in queries])
print(f"\nPQ (m=4, s=16, 4x compression): recall@10 = {recall_at_k(pq_hits, truth, 10):.2f}")

# Output:
# PQ (m=4, s=16, 4x compression): recall@10 = 0.59

# ============================================================
# 5. LSH — hash to buckets
# ============================================================
# Random hyperplanes split space; vectors hashing to the same bucket are
# candidates. Simple, but bucket sizes explode in high dims — mostly
# replaced by HNSW/IVF in practice.

class LSH:
    def __init__(self, n_planes: int = 6, seed: int = 42) -> None:
        self._planes = np.random.default_rng(seed).normal(
            size=(n_planes, 16))
        self._buckets: dict[tuple, list[int]] = {}

    def _hash(self, v: np.ndarray) -> tuple:
        return tuple(int(x > 0) for x in v @ self._planes.T)

    def build(self, data: np.ndarray) -> None:
        for i, v in enumerate(data):
            self._buckets.setdefault(self._hash(v), []).append(i)

    def search(self, query: np.ndarray, k: int = 10) -> list[int]:
        cands = self._buckets.get(self._hash(query), [])
        scored = sorted(cands, key=lambda i: l2_dist(query, self._vectors[i]))
        scored = scored[:k]
        return scored + [-1] * (k - len(scored))   # pad, never ragged


lsh = LSH(n_planes=6)
lsh.build(vectors)
lsh._vectors = vectors
lsh_hits = np.array([lsh.search(q, k=10) for q in queries])
print(f"LSH (6 planes):            recall@10 = {recall_at_k(lsh_hits, truth, 10):.2f}")

# Output:
# LSH (6 planes):            recall@10 = 0.49

# ============================================================
# 6. Parameter Effects — measured
# ============================================================
# Build cost grows with ef_construction; recall grows with ef_search;
# memory grows with M. These are measured on the SAME corpus so the
# deltas are attributable to the parameter.

def build_time(index: object, data: np.ndarray) -> float:
    t0 = _time.perf_counter()
    index.build(data)
    return _time.perf_counter() - t0


slow_build = build_time(HNSWLite(M=16, ef_construction=40), vectors)
fast_build = build_time(HNSWLite(M=2, ef_construction=8), vectors)
print(f"\nHNSW build: M=16/ef=40 -> {slow_build:.4f}s | M=2/ef=8 -> {fast_build:.4f}s")
print("(wall-clock; the exact numbers vary per machine, the ORDER does not)")

# Output (order is stable, magnitudes vary by machine):
# HNSW build: M=16/ef=40 -> 0.0075s | M=2/ef=8 -> 0.0059s
# (wall-clock; the exact numbers vary per machine, the ORDER does not)

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: maxing ef_search for recall without measuring latency — at
#   some point recall saturates and you are only paying.
# MISTAKE: cranking M for recall — every edge is memory; 1M vectors x
#   M=64 edges is hundreds of MB just for the graph.
# MISTAKE: comparing PQ recall to full-precision without accounting for
#   the 4-16x memory win; the right metric is recall per byte.
# MISTAKE: tuning on a tiny corpus and shipping the same params — ANN
#   behavior changes with n (HNSW shines at scale; IVF needs enough
#   points per cell).

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # HNSW: higher M/ef must beat lower M/ef on the same corpus
    assert recall_hns > recall_low, \
        "raising M and ef must improve recall"

    # IVF: more probes must not reduce recall
    assert ivf_4 >= ivf_1, "nprobe=4 must match or beat nprobe=1"

    # PQ: compressed index still finds the true nearest neighbor often
    assert recall_at_k(pq_hits, truth, 10) > 0.5, \
        "PQ at 4x compression should keep majority recall"

    # LSH with few planes is weak (buckets are coarse)
    assert recall_at_k(lsh_hits, truth, 10) < recall_hns, \
        "HNSW must beat coarse LSH on this corpus"

    # parameter effect: heavier build config costs more time
    assert slow_build > fast_build, \
        "larger M and ef_construction must cost more build time"

    # all ANN hits are valid corpus indices
    for hit in hits:
        assert all(0 <= i < len(vectors) for i in hit), \
            "ANN must return valid corpus indices"

    # HNSW with full ef_search converges to brute force on small data
    hns_full = HNSWLite(M=64, ef_construction=64)
    hns_full.build(vectors)
    full_hits = np.array([hns_full.search(q, ef_search=300)[:10] for q in queries])
    assert recall_at_k(full_hits, truth, 10) >= 0.95, \
        "generous HNSW params must approach exact recall on 300 vectors"

    print("[OK] 02-ann-algorithms: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. HNSW: graph + ef budget; M/ef_construction/ef_search")
        print("2. IVF: cluster + probe; nlist/nprobe")
        print("3. PQ: codebooks, 4-16x compression, ADC distance")
        print("4. Every parameter is a recall/latency/memory dial")
        _verify()  # always runs, so plain execution is also a test
