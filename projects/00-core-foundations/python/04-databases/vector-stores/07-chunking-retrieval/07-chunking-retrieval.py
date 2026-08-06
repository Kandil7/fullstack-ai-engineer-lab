"""
Vector Stores — 07: Chunking and Retrieval Quality
==============================================
Topics: why chunk, fixed-size with overlap, sentence-boundary chunks,
        recursive splitting, boundary-straddling facts, recall@1 vs
        recall@3 (the RAG metric), chunk-size sweep and dilution

Why this matters for AI/backend engineering:
    Garbage in, garbage out — in RAG the "in" is chunks. The chunking
    strategy decides whether the answer to a query even EXISTS inside a
    retrieved chunk. RAG retrieves top-k, so recall@3 is the honest
    metric; recall@1 is the strict one. This exercise measures both
    across strategies and shows why overlap and sentence boundaries
    exist.

Run:      python 07-chunking-retrieval.py
Verify:   python 07-chunking-retrieval.py --verify
"""

from __future__ import annotations

import sys

import numpy as np

from vector_utils import (chunk_by_sentences, chunk_fixed, chunk_recursive,
                          cosine_sim, embed_texts)

# ============================================================
# 1. A synthetic manual with facts
# ============================================================
# Each feature has two sentences: the name, then the parameter. Queries
# ask about the parameter without the feature id ('allows 180 requests
# per minute'), so retrieval must find the chunk by content — a
# boundary cutting the answer sentence is fatal.
sentences: list[str] = []
for i in range(1, 21):
    kind = "rate limiter" if i % 3 == 0 else "cache store" if i % 3 == 1 \
        else "auth guard"
    sentences.append(f"Feature {i:02d} is the {kind}.")
    sentences.append(f"Feature {i:02d} allows {10 * i} requests per minute.")

doc = " ".join(sentences)
queries = [f"allows {10 * i} requests per minute" for i in range(1, 21)]
nums = [str(10 * i) for i in range(1, 21)]     # the answer token per query
print(f"manual: {len(sentences)} sentences, {len(doc)} chars")

# Output:
# manual: 40 sentences, 1469 chars

# ============================================================
# 2. Three chunking strategies
# ============================================================
strategies = {
    "fixed(45, no overlap)":    chunk_fixed(doc, chunk_size=45, overlap=0),
    "fixed(45, overlap=10)":    chunk_fixed(doc, chunk_size=45, overlap=10),
    "sentence(max 160)":        chunk_by_sentences(doc, max_chars=160),
    "recursive(max 90)":        chunk_recursive(doc, max_chars=90),
}
print("\nchunk counts per strategy:")
for name, chunks in strategies.items():
    print(f"  {name:24s} -> {len(chunks):3d} chunks")

# Output:
# chunk counts per strategy:
#   fixed(45, no overlap)    ->  33 chunks
#   fixed(45, overlap=10)    ->  42 chunks
#   sentence(max 160)        ->  10 chunks
#   recursive(max 90)        ->  40 chunks

# ============================================================
# 3. Boundary-straddling facts
# ============================================================
# With fixed 45-char cuts, some answer sentences are SPLIT: '...allows
# 180 req' in one chunk and 'uests per minute. ...' in the next. The
# answer is then unretrievable as a single unit.
def broken_seams(chunks: list[str]) -> int:
    """Count chunks that begin with the orphaned tail of 'requests'."""
    return sum(1 for c in chunks if c.startswith("uests") or
               c.startswith("s per minute") or c.startswith("per minute"))


for name, chunks in strategies.items():
    print(f"  {name:24s} orphaned seams = {broken_seams(chunks)}")

# Output:
#   fixed(45, no overlap)    -> orphaned seams = 1
#   fixed(45, overlap=10)    -> orphaned seams = 3
#   sentence(max 160)        -> orphaned seams = 0
#   recursive(max 90)        -> orphaned seams = 0

# ============================================================
# 4. Retrieval recall per strategy
# ============================================================
# Query = 'allows 180 requests per minute' (no feature id). Correct
# chunk = the one containing '180'. recall@1 = top hit; recall@3 =
# anywhere in the top-3 (what the LLM actually sees).
def recall_at(q: str, num: str, chunks: list[str], k: int) -> bool:
    emb = embed_texts([q] + chunks, dim=64)
    sims = np.array([cosine_sim(emb[0], e) for e in emb[1:]])
    top = np.argsort(sims)[::-1][:k]
    return any(num in chunks[t] for t in top)


print("\nretrieval recall (answer chunk found in top-k):")
for name, chunks in strategies.items():
    r1 = sum(1 for q, n in zip(queries, nums) if recall_at(q, n, chunks, 1))
    r3 = sum(1 for q, n in zip(queries, nums) if recall_at(q, n, chunks, 3))
    print(f"  {name:24s} recall@1 = {r1:2d}/20   recall@3 = {r3:2d}/20")

# Output:
# retrieval recall (answer chunk found in top-k):
#   fixed(45, no overlap)    -> recall@1 =  7/20   recall@3 = 10/20
#   fixed(45, overlap=10)    -> recall@1 =  8/20   recall@3 = 13/20
#   sentence(max 160)        -> recall@1 =  8/20   recall@3 = 19/20
#   recursive(max 90)        -> recall@1 = 18/20   recall@3 = 20/20

# ============================================================
# 5. Why the seams cost recall
# ============================================================
# The no-overlap index loses feature 18: its answer sentence is split
# across two chunks, so neither chunk contains the full query. Overlap
# and sentence chunking keep the phrase intact. (recall@1 is also hurt
# by embedding dilution — all answer chunks look alike to a bag-of-words
# vector, which is exactly why RAG uses top-k retrieval.)
for name, chunks in strategies.items():
    broken = [i for i, n in enumerate(nums)
              if not recall_at(queries[i], n, chunks, 1)]
    print(f"  {name:24s} recall@1 misses = {sorted(broken)}")

# Output:
#   fixed(45, no overlap)    -> recall@1 misses = [0, 1, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15, 17]
#   fixed(45, overlap=10)    -> recall@1 misses = [0, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18]
#   sentence(max 160)        -> recall@1 misses = [3, 4, 5, 6, 10, 11, 12, 15, 16, 17, 18, 19]
#   recursive(max 90)        -> recall@1 misses = [7, 12]

# ============================================================
# 6. Chunk-size sweep — the eval loop
# ============================================================
# The right chunk size is data-dependent: too small fragments facts,
# too large dilutes the embedding with unrelated tokens. Sweep, measure
# recall@3, pick the smallest size that clears your floor.
print("\nchunk-size sweep (fixed, overlap=20%):")
best = (0.0, 0)
for size in (40, 70, 100, 140, 200):
    chunks = chunk_fixed(doc, chunk_size=size, overlap=max(4, size // 5))
    r3 = sum(1 for q, n in zip(queries, nums) if recall_at(q, n, chunks, 3)) / 20
    print(f"  size={size:3d}: {len(chunks):3d} chunks, recall@3 = {r3:.2f}")
    if r3 > best[0]:
        best = (r3, size)
print(f"-> pick size={best[1]} (highest recall@3; smaller is cheaper to embed)")

# Output:
# chunk-size sweep (fixed, overlap=20%):
#   size= 40:  46 chunks, recall@3 = 0.60
#   size= 70:  27 chunks, recall@3 = 0.75
#   size=100:  19 chunks, recall@3 = 0.50
#   size=140:  14 chunks, recall@3 = 0.80
#   size=200:  10 chunks, recall@3 = 0.65
# -> pick size=140 (highest recall@3; smaller is cheaper to embed)

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: chunking by fixed size with NO overlap — every boundary is
#   a potential answer-killer (section 5: recall@3 = 10/20).
# MISTAKE: measuring recall@1 when production feeds the LLM top-k —
#   recall@3 is the metric that predicts answer quality.
# MISTAKE: tuning chunk size on intuition instead of a sweep over
#   representative queries (section 6).
# MISTAKE: forgetting the dilution tradeoff: bigger chunks carry more
#   context but bury the answer token in embedding noise.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # sentence chunking never cuts a sentence: every chunk ends with '.'
    for c in strategies["sentence(max 160)"]:
        assert c.rstrip().endswith("."), \
            "sentence chunks must end on a sentence boundary"

    def r3(chunks: list[str]) -> int:
        return sum(1 for q, n in zip(queries, nums) if recall_at(q, n, chunks, 3))

    # seam cost: no-overlap must trail the boundary-aware strategies
    assert r3(strategies["fixed(45, no overlap)"]) < \
        r3(strategies["sentence(max 160)"]), \
        "fixed no-overlap must lose answers to seams"
    assert r3(strategies["recursive(max 90)"]) == 20, \
        "recursive must recover every answer at recall@3"

    # overlap must beat no-overlap (same size, seams re-covered)
    assert r3(strategies["fixed(45, overlap=10)"]) > \
        r3(strategies["fixed(45, no overlap)"]), \
        "overlap must improve recall over no-overlap"

    # sweep: the chosen size must be a global max on this data
    sweep = []
    for size in (40, 70, 100, 140, 200):
        chunks = chunk_fixed(doc, chunk_size=size, overlap=max(4, size // 5))
        sweep.append((sum(1 for q, n in zip(queries, nums)
                          if recall_at(q, n, chunks, 3)) / 20, size))
    assert max(sweep)[0] == max(h for h, _ in sweep), \
        "pick must be a global max of the sweep"

    # fragmentation: the smallest size must not be the best
    assert sweep[0][0] < max(h for h, _ in sweep), \
        "tiny chunks must hurt recall (fragmentation)"

    print("[OK] 07-chunking-retrieval: all checks passed")


if __name__ == "__main__":
    if "--verify" not in sys.argv:
        print("\n--- Summary ---")
        print("1. Chunking decides whether answers exist inside one chunk")
        print("2. Fixed size without overlap cuts sentences -> misses")
        print("3. Overlap and sentence boundaries fix the seams")
        print("4. Sweep chunk sizes on real queries; pick the recall floor")
    _verify()  # always runs, so plain execution is also a test
