"""
Vector Stores — 01: Vector Search Fundamentals
==============================================
Topics: embeddings as points, cosine / dot / L2 similarity, brute-force
        kNN O(n*d), why ANN exists, recall vs latency as the central
        tradeoff

Why this matters for AI/backend engineering:
    RAG retrieval quality starts here: the query is embedded, the corpus
    is embedded, and "most similar" means nearest in vector space. Before
    touching any vector database, you must be able to compute similarity
    and measure retrieval quality by hand — that is what this exercise
    does with numpy only.

Run:      python 01-vector-search-fundamentals.py
Verify:   python 01-vector-search-fundamentals.py --verify
Reference: https://en.wikipedia.org/wiki/Cosine_similarity
"""

from __future__ import annotations

import sys

import numpy as np

from vector_utils import (brute_force_knn, cosine_sim, dot_sim, embed_text,
                          embed_texts, l2_dist, make_corpus, recall_at_k,
                          seed_all)

seed_all(42)

# ============================================================
# 1. Embeddings Are Points
# ============================================================
# A model maps text -> vector of floats; semantically similar texts land
# near each other. We stand in for a real embedding model with a
# deterministic hashed embedding (same string -> same vector, always).

q = embed_text("vector search retrieval", dim=16)
c1 = embed_text("vector search retrieval reranking", dim=16)
c2 = embed_text("document schema index collection", dim=16)
print(f"query dims: {q.shape}, norm: {np.linalg.norm(q):.3f}")
print(f"sim(q, related corpus)    = {cosine_sim(q, c1):.3f}")
print(f"sim(q, unrelated corpus)  = {cosine_sim(q, c2):.3f}")

# Output:
# query dims: (16,), norm: 1.000
# sim(q, related corpus)    = 0.926
# sim(q, unrelated corpus)  = 0.198

# ============================================================
# 2. Three Similarity Metrics
# ============================================================
# cosine  = angle only, ignores magnitude        -> text embeddings
# dot     = angle AND magnitude (equals cosine for normalized vectors)
# L2 dist = straight-line distance               -> lower = more similar

a = np.array([1.0, 0.0])
b = np.array([0.0, 1.0])
c = np.array([2.0, 0.0])          # same direction as a, twice the size
print(f"\ncosine(a, c) = {cosine_sim(a, c):.2f}  (angle ignores scale)")
print(f"dot(a, c)    = {dot_sim(a, c):.2f}  (dot sees scale)")
print(f"l2(a, c)     = {l2_dist(a, c):.2f}  (distance sees scale)")

# Output:
# cosine(a, c) = 1.00  (angle ignores scale)
# dot(a, c)    = 2.00  (dot sees scale)
# l2(a, c)     = 1.00  (distance sees scale)

# ============================================================
# 3. Brute-Force kNN — the exact baseline
# ============================================================
# Scan every corpus vector, score it, take top-k. O(n*d) per query:
# at 1M vectors x 1536 dims that is 1.5 GFLOP per query — too slow for
# interactive search. Exact, correct, and the reference for everything
# that follows.

vectors, meta = make_corpus(n=120, dim=16, n_clusters=6, seed=42)
queries = vectors[:3]                    # query with corpus members
neighbors = brute_force_knn(queries, vectors, k=5)
print(f"\nbrute-force kNN: query 0 -> {neighbors[0].tolist()}")
print(f"self-match is rank 0 (distance 0)")

# Output:
# brute-force kNN: query 0 -> [0, 60, 72, 108, 18]
# self-match is rank 0 (distance 0)

# ============================================================
# 4. Ground Truth and Recall@k
# ============================================================
# To judge an ANN index you need ground truth: the exact top-k from
# brute force. recall@k = how many true top-k the index returned.

truth = brute_force_knn(queries, vectors, k=10)
print(f"\ntruth top-10 for query 0: {truth[0].tolist()}")
print(f"recall@10 of exact search = {recall_at_k(truth, truth, k=10):.2f}")

# Output:
# truth top-10 for query 0: [0, 60, 72, 108, 18, 96, 102, 84, 66, 42]
# recall@10 of exact search = 1.00

# ============================================================
# 5. Why ANN: the Complexity Cliff
# ============================================================
# O(n*d) does not scale. An approximate index trades a few points of
# recall for orders of magnitude in speed:

def flops_brute_force(n: int, d: int) -> float:
    return n * d  # multiply-adds per query


print(f"\nbrute force @ 10k vectors: {flops_brute_force(10_000, 1536)/1e6:.0f} MFLOP/query")
print(f"brute force @ 10M vectors: {flops_brute_force(10_000_000, 1536)/1e9:.1f} GFLOP/query")

# Output:
# brute force @ 10k vectors: 15 MFLOP/query
# brute force @ 10M vectors: 15.4 GFLOP/query

# The central tradeoff of every vector store:
#   recall (how many of the true top-k came back)
#   vs. latency (query time at a given corpus size)
# Everything else — HNSW parameters, quantization, filtering — is a dial
# on this curve.

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: comparing unnormalized vectors with cosine and expecting
#   magnitude to not matter — it never does with cosine; if you care
#   about scale use dot/L2.
# MISTAKE: L2 for text embeddings that were trained with cosine loss —
#   rankings can differ; always match the metric the embedding model
#   was trained with.
# MISTAKE: measuring recall@k against brute force on a corpus that is
#   NOT the production distribution — measure on production-shaped data.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # embeddings are normalized and deterministic
    assert abs(np.linalg.norm(q) - 1.0) < 1e-9, "embeddings must be unit vectors"
    assert np.allclose(embed_text("hello"), embed_text("hello")), \
        "same text must produce the same vector (deterministic)"

    # cosine is scale-invariant, dot is not
    assert abs(cosine_sim(a, c) - 1.0) < 1e-9, "cosine must ignore magnitude"
    assert abs(dot_sim(a, c) - 2.0) < 1e-9, "dot must include magnitude"
    assert abs(l2_dist(a, c) - 1.0) < 1e-9, "L2 distance of (1,0)->(2,0) is 1"

    # related text scores higher than unrelated text
    assert cosine_sim(q, c1) > cosine_sim(q, c2), \
        "semantically related text must embed closer"

    # brute force: self-match is the nearest neighbor
    nn = brute_force_knn(queries[:1], vectors, k=1)[0][0]
    assert nn == 0, "a corpus vector must retrieve itself first"

    # recall of exact search is 1.0
    assert recall_at_k(truth, truth, k=10) == 1.0, \
        "brute force must achieve perfect recall against itself"

    # complexity math: 10M x 1536 is in the GFLOP range
    assert flops_brute_force(10_000_000, 1536) > 1e9, \
        "10M vectors must be computationally prohibitive for exact search"

    # embedding matrix shape
    mat = embed_texts(["a", "b", "c"], dim=16)
    assert mat.shape == (3, 16), "embed_texts must stack into (n, dim)"

    print("[OK] 01-vector-search-fundamentals: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Embeddings are points; similarity is geometry")
        print("2. cosine/dot/L2 differ in how they treat magnitude")
        print("3. Brute force is exact but O(n*d)")
        print("4. Recall vs latency is THE central vector-store tradeoff")
        _verify()  # always runs, so plain execution is also a test
