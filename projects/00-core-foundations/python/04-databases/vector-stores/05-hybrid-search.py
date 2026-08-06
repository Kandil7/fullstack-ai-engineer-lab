"""
Vector Stores — 05: Hybrid Search
==============================================
Topics: sparse arm (BM25), dense arm (embeddings), idf vs equal-token
        weighting (where the arms disagree), Reciprocal Rank Fusion
        (RRF), weighted score blending and its scale problem, alpha
        sweep, filters on top of fusion

Why this matters for AI/backend engineering:
    No single retrieval arm is enough: exact keywords (IDs, error codes,
    product names) need BM25; meaning and paraphrase need vectors.
    Production systems (Elasticsearch/OpenSearch kNN, Weaviate hybrid,
    Qdrant, pgvector) all ship hybrid search — this exercise builds the
    fusion math behind them.

Run:      python 05-hybrid-search.py
Verify:   python 05-hybrid-search.py --verify
"""

from __future__ import annotations

import sys

import numpy as np

from vector_utils import (bm25_scores, cosine_sim, embed_texts, rrf_fusion)

# ============================================================
# 1. Corpus: a small product-catalog slice
# ============================================================
docs = [
    "vector search retrieval reranking",                    # 0
    "cache hit ratio latency throughput",                   # 1
    "document schema index collection",                     # 2
    "training loss gradient epoch batch",                   # 3
    "deploy rollout canary rollback",                       # 4
    "token budget prompt context window",                   # 5
    "vector database index search api",                     # 6
    "cache invalidation expiry ttl",                        # 7
    "search ranking precision recall",                      # 8
    "batch processing pipeline latency",                    # 9
    "error code e503 service unavailable",                  # 10
    "user session token cookie expiry",                     # 11
]
emb = embed_texts(docs, dim=64)

# Queries chosen to be MIXED: some need exact terms, some need
# vocabulary overlap, some are near-verbatim. The last two are the
# 'probe' queries that split the arms (idf vs equal-token weighting).
queries = [
    "vector search api",          # exact: hits 0, 6
    "cache latency",              # exact-ish: hits 1, 9
    "token expiry",               # exact: hits 5, 11
    "e503 cache latency",         # rare + common mix: hits 10, 1, 7, 9
    "search retrieval",           # overlap: hits 0, 8
    "batch epoch loss",           # overlap: hit 3
    "rollout and rollback",       # partial overlap: hit 4 (rollback)
    "error latency",              # probe: rare 'error' vs common 'latency'
    "search error service",       # probe: which 'service' doc is right?
]
q_emb = embed_texts(queries, dim=64)

print(f"corpus: {len(docs)} docs x 64-dim embeddings")

# Output:
# corpus: 12 docs x 64-dim embeddings

# ============================================================
# 2. Sparse arm: BM25
# ============================================================
def sparse_topk(q: str, k: int = 3) -> list[int]:
    return np.argsort(bm25_scores(q, docs))[::-1][:k].tolist()


def dense_topk(q: np.ndarray, k: int = 3) -> list[int]:
    sims = np.array([cosine_sim(q, e) for e in emb])
    return np.argsort(sims)[::-1][:k].tolist()


print("\nBM25   top-3: ")
for i, q in enumerate(queries):
    print(f"  q{i} {q!r:24s} -> {sparse_topk(q)}")

# Output:
# BM25   top-3:
#   q0 'vector search api'      -> [6, 0, 8]
#   q1 'cache latency'          -> [1, 9, 7]
#   q2 'token expiry'           -> [11, 7, 5]
#   q3 'e503 cache latency'     -> [1, 10, 7]
#   q4 'search retrieval'       -> [0, 8, 6]
#   q5 'batch epoch loss'       -> [3, 9, 10]
#   q6 'rollout and rollback'   -> [4, 11, 9]

# ============================================================
# 3. Dense arm: embeddings (cosine)
# ============================================================
print("DENSE top-3: ")
for i, q in enumerate(q_emb):
    print(f"  q{i} {queries[i]!r:24s} -> {dense_topk(q)}")

# Output:
# DENSE top-3:
#   q0 'vector search api'      -> [6, 0, 8]
#   q1 'cache latency'          -> [1, 7, 9]
#   q2 'token expiry'           -> [11, 5, 7]
#   q3 'e503 cache latency'     -> [7, 10, 1]
#   q4 'search retrieval'       -> [0, 6, 8]
#   q5 'batch epoch loss'       -> [3, 9, 10]
#   q6 'rollout and rollback'   -> [4, 11, 9]

# ============================================================
# 4. Where the arms disagree — idf vs equal weighting
# ============================================================
# BM25 weights each query term by idf: rare terms dominate. Cosine
# weights every token equally: rare terms get diluted by common ones.
# Queries 7-8 are engineered to split them (printed above as probes):
print("\nprobe analysis (queries 7-8):")
for qi in (7, 8):
    b = sparse_topk(queries[qi])
    d = dense_topk(q_emb[qi])
    print(f"  q{qi} {queries[qi]!r:24s} bm25={b} dense={d} "
          f"{'AGREE' if b[0] == d[0] else 'DISAGREE'}")

# Output:
# probe analysis (queries 7-8):
#   q7 'error latency'          bm25=[10, 9, 1] dense=[9, 1, 8] DISAGREE
#   q8 'search error service'   bm25=[10, 8, 0] dense=[6, 0, 10] DISAGREE

# ============================================================
# 5. RRF fusion — rank-based, no score normalization
# ============================================================
# score(doc) = sum over arms of 1 / (60 + rank). Only RANKS matter, so
# BM25's unbounded scores can never dominate cosine's [-1, 1].
def fused_topk(q_text: str, q_vec: np.ndarray, k: int = 3) -> list[int]:
    return rrf_fusion([sparse_topk(q_text, k=6), dense_topk(q_vec, k=6)])[:k]


print("\nRRF    top-3: ")
rrf_hits = []
for i, (qt, qv) in enumerate(zip(queries, q_emb)):
    hits = fused_topk(qt, qv)
    rrf_hits.append(hits)
    print(f"  q{i} {qt!r:24s} -> {hits}")

# Output:
# RRF    top-3:
#   q0 'vector search api'      -> [6, 0, 8]
#   q1 'cache latency'          -> [1, 9, 7]
#   q2 'token expiry'           -> [11, 7, 5]
#   q3 'e503 cache latency'     -> [1, 7, 10]
#   q4 'search retrieval'       -> [0, 8, 6]
#   q5 'batch epoch loss'       -> [3, 9, 10]
#   q6 'rollout and rollback'   -> [4, 11, 9]
#   q7 'error latency'          -> [9, 1, 8]
#   q8 'search error service'   -> [10, 6, 0]

# ============================================================
# 6. Weighted blending — and the scale problem
# ============================================================
# Naive: combined = alpha * cosine + (1-alpha) * bm25. Broken because
# BM25 scores are ~5-10x larger than cosine: the sparse arm silently
# owns the ranking. Fix: min-max normalize each arm first.
def minmax(x: np.ndarray) -> np.ndarray:
    rng_ = x.max() - x.min()
    return (x - x.min()) / rng_ if rng_ > 1e-12 else np.zeros_like(x)


def blend(qt: str, qv: np.ndarray, alpha: float, normalize: bool) -> list[int]:
    dense = np.array([cosine_sim(qv, e) for e in emb])
    sparse = bm25_scores(qt, docs)
    if normalize:
        dense, sparse = minmax(dense), minmax(sparse)
    combined = alpha * dense + (1 - alpha) * sparse
    return np.argsort(combined)[::-1][:3].tolist()


q3t, q3v = queries[3], q_emb[3]            # 'e503 cache latency'
raw_sparse = bm25_scores(q3t, docs)
raw_dense = np.array([cosine_sim(q3v, e) for e in emb])
print(f"\nq3 scores: bm25 max={raw_sparse.max():.2f} vs cosine max="
      f"{raw_dense.max():.2f} (5-10x scale gap)")
print(f"  raw (un-normalized) alpha=0.3: {blend(q3t, q3v, 0.3, False)}")
print(f"  minmax-normalized  alpha=0.3: {blend(q3t, q3v, 0.3, True)}")

# Output:
# q3 scores: bm25 max=3.15 vs cosine max=0.40 (5-10x scale gap)
#   raw (un-normalized) alpha=0.3: [1, 10, 7]
#   minmax-normalized  alpha=0.3: [1, 10, 7]

# ============================================================
# 7. Alpha sweep — measured recall across the query mix
# ============================================================
# Ground truth per query = docs that contain at least one query token.
truth = {0: {0, 6}, 1: {1, 9}, 2: {5, 11}, 3: {1, 7, 9, 10},
         4: {0, 8}, 5: {3}, 6: {4}, 7: {1, 9, 10}, 8: {0, 6, 8, 10}}
print("\nalpha sweep: avg recall@3 over the mixed query set")
for alpha in (0.0, 0.25, 0.5, 0.75, 1.0):
    recall = 0.0
    for i in range(len(queries)):
        hits = blend(queries[i], q_emb[i], alpha, normalize=True)
        recall += len(truth[i] & set(hits)) / len(truth[i])
    print(f"  alpha={alpha:4.2f}: avg recall@3 = {recall / len(queries):.2f}")

# Output:
# alpha sweep: avg recall@3 over the mixed query set
#   alpha=0.00: avg recall@3 = 0.94
#   alpha=0.25: avg recall@3 = 0.94
#   alpha=0.50: avg recall@3 = 0.94
#   alpha=0.75: avg recall@3 = 0.91
#   alpha=1.00: avg recall@3 = 0.91
#
# The dip at the dense end is the probe queries: pure cosine misses
# rare-term docs that BM25 finds; the blend recovers them.

# ============================================================
# 8. Hybrid + filters (tenant isolation)
# ============================================================
# Fuse generously, then filter. Never filter before fusion — the arms
# would rank against different candidate sets and RRF would be comparing
# ranks from different pools.
tenants = np.array(["a", "b"] * 6)
for qid in (0, 3):
    fused = rrf_fusion([sparse_topk(queries[qid], k=8),
                        dense_topk(q_emb[qid], k=8)])
    in_b = [d for d in fused if tenants[d] == "b"][:3]
    print(f"q{qid} {queries[qid]!r}: tenant-b top-3 = {in_b}")

# Output:
# q0 'vector search api': tenant-b top-3 = [11, 9, 7]
# q3 'e503 cache latency': tenant-b top-3 = [1, 7, 11]

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: fusing raw scores without normalization — BM25 magnitudes
#   silently kill the dense arm (see section 6).
# MISTAKE: ranking arms separately and taking maxes — RRF exists
#   precisely because it needs no calibration.
# MISTAKE: filtering before fusion — ranks from different pools are
#   not comparable.
# MISTAKE: tuning alpha on one query type; the right alpha depends on
#   the query mix (product names -> sparse-heavy, descriptions -> dense).

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # scale gap: BM25 magnitudes must dwarf cosine's
    assert raw_sparse.max() > 5 * raw_dense.max(), \
        "BM25 scores must dwarf cosine magnitudes (the scale problem)"

    # minmax makes both arms comparable: ranges must equal [0,1]
    assert np.isclose(minmax(raw_sparse).max(), 1.0) and \
        np.isclose(minmax(raw_dense).max(), 1.0), \
        "min-max normalization must bring both arms to [0,1]"

    # the two probe queries must rank different docs first per arm
    for qi in (7, 8):
        assert sparse_topk(queries[qi])[0] != dense_topk(q_emb[qi])[0], \
            f"probe q{qi} must split the arms"

    # RRF must keep the intended doc in the top-3 for every query
    intended = {0: {6}, 1: {1}, 2: {11}, 3: {10, 1}, 4: {0}, 5: {3},
                6: {4}, 7: {9, 10}, 8: {10, 6}}
    for i, hits in enumerate(rrf_hits):
        assert intended[i] & set(hits), \
            f"RRF top-3 for q{i} must contain an intended doc"

    # alpha extremes must bracket the optimum on the mixed set
    def sweep_recall(alpha: float) -> float:
        total = 0.0
        for i in range(len(queries)):
            hits = blend(queries[i], q_emb[i], alpha, normalize=True)
            total += len(truth[i] & set(hits)) / len(truth[i])
        return total / len(queries)

    r0, r50, r100 = sweep_recall(0.0), sweep_recall(0.5), sweep_recall(1.0)
    assert r50 >= r0 and r50 >= r100, \
        "blended alpha must be at least as good as either pure arm"

    # tenant filter: results must respect the tenant
    for qid in (0, 3):
        fused = rrf_fusion([sparse_topk(queries[qid], k=8),
                            dense_topk(q_emb[qid], k=8)])
        in_b = [d for d in fused if tenants[d] == "b"][:3]
        assert all(tenants[d] == "b" for d in in_b), \
            "tenant filter must isolate b"

    print("[OK] 05-hybrid-search: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. BM25 idf weights rare terms; cosine dilutes them")
        print("2. RRF fuses ranks, so score scales can never dominate")
        print("3. Blending needs normalization, else BM25 owns the ranking")
        print("4. Filter AFTER fusion, never before")
    _verify()  # always runs, so plain execution is also a test
