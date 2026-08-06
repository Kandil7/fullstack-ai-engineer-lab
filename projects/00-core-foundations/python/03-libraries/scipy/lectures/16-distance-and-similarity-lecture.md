# SciPy 16 — Distance and Similarity

## Topic Overview

Retrieval, deduplication, clustering, and recommender ranking all
reduce to one question: *which stored vectors are closest to this
query?* This lecture covers the distance toolbox
(`pdist`/`cdist`, euclidean, manhattan, cosine), why cosine is
the default for embeddings, the normalize-then-euclidean trick,
exact neighbors with KD-trees, and the curse of dimensionality
that forces approximate nearest neighbor (ANN) search in real
RAG systems.

## Learning Objectives

By the end you can:

1. Compute pairwise distances with `pdist`/`squareform` and
   query-to-corpus distances with `cdist`.
2. Explain why cosine similarity is the default for embeddings
   (scale invariance) and when euclidean is appropriate.
3. Convert a cosine-ranking problem into a euclidean one by
   L2-normalizing vectors first.
4. Find exact nearest neighbors with `cKDTree` and verify them
   against brute force.
5. Explain the curse of dimensionality quantitatively
   (distance spread shrinks as `1/sqrt(d)`) and why it forces
   ANN indexes (HNSW, IVF) at scale.

## Prerequisites

- NumPy arrays and norms (topic 33 linear algebra).
- Sparse matrices and row normalization (topic 15 sparse
  matrices) — retrieval corpora are sparse before they are dense
  embeddings.

## Key Concepts

### 1. The distance toolbox

`scipy.spatial.distance` provides the three metrics used in
practice:

| Metric | Function | Meaning |
|---|---|---|
| euclidean | `cdist(X, Y, "euclidean")` | straight-line distance |
| manhattan | `cdist(X, Y, "cityblock")` | `sum|x − y|` — robust to outliers |
| cosine | `cdist(X, Y, "cosine")` | `1 − cos(angle)` — direction only |

Two shapes of call:

```python
pdist(X)                 # all pairwise distances within X: n(n-1)/2
squareform(pdist(X))     # the n x n symmetric matrix
cdist(Q, X)              # every query x every reference: (nq, n)
```

`pdist` is for clustering; `cdist` is for retrieval (one query,
many candidates).

### 2. Why cosine for embeddings

Embeddings — document vectors, user vectors, image vectors —
vary in magnitude for reasons that should not affect relevance:
a long document contains more words than a short one, but it is
about the same things.

- **Cosine ignores magnitude**: `cos(a, 2a) = 1` — identical
  direction, identical semantics.
- **Euclidean is dominated by magnitude**: `dist(a, 2a) = |a|`.

For **normalized** vectors the two coincide exactly:

```
euclidean(u, v)^2 = 2 * (1 - cos(u, v))     for |u| = |v| = 1
```

so cosine ranking is euclidean ranking on the unit sphere — the
reason RAG pipelines L2-normalize embeddings before storing them.

### 3. The normalize-then-euclidean pattern

```python
X = X / np.linalg.norm(X, axis=1, keepdims=True)
Q = Q / np.linalg.norm(Q, axis=1, keepdims=True)
dists = cdist(Q, X, metric="euclidean")     # == cosine ranking
idx = np.argsort(dists, axis=1)[:, :k]      # top-k neighbors
```

This matters beyond aesthetics: distance-based indexes (KD-trees,
and many ANN implementations) support euclidean natively but not
cosine. Normalize once at ingest, query in euclidean, get cosine
semantics for free.

### 4. Exact nearest neighbors with cKDTree

```python
from scipy.spatial import cKDTree

tree = cKDTree(points)          # build once
dist, idx = tree.query(queries, k=3)
```

The KD-tree partitions space with axis-aligned splits, pruning
whole branches that cannot contain a closer point. Results are
exact — identical to brute-force `cdist` argmin — but much faster
in low dimensions.

### 5. The curse of dimensionality — measured

For random unit vectors in `d` dimensions, pairwise cosine
distances have:

```
mean ~ 1.0        (random vectors are ~orthogonal)
std  ~ 1 / sqrt(d)
```

Measured: d=2 spread 0.707, d=128 spread 0.091 — the distance
**contrast collapses**. When every pair of points is about the
same distance apart, "nearest" stops meaning anything, and
space-partitioning (KD-trees) degenerates: measured on 20k
points, the KD-tree is 4× faster than brute force at d=2 but 4×
**slower** at d=64. Space-partitioning is fundamentally a
low-dimensional tool.

### 6. Brute force vs ANN

| Approach | Cost per query | When |
|---|---|---|
| brute force `cdist` | O(n · d) | n < ~10⁵, exact, simple |
| `cKDTree` | O(log n) low-d | d ≤ ~8, exact |
| ANN (HNSW, IVF, FAISS) | sub-linear, approximate | n ≥ 10⁶, d = 100–1000 |

At production scale (millions of embeddings), exact search is
too slow and KD-trees are useless — approximate nearest neighbor
indexes trade a tiny recall loss for orders of magnitude in
latency. The "A" is deliberate: retrieval quality is measured in
recall@k, not in exactness.

## Common Mistakes

1. **Using euclidean on raw embeddings.** Magnitude (document
   length, norm) dominates the ranking; cosine or normalized
   euclidean is the embedding default.
2. **Comparing cosine distances across differently-scaled
   vectors.** Cosine is scale-invariant by construction — that is
   the point — but if you mix normalized and unnormalized
   vectors in one store, rankings silently break.
3. **Forgetting `squareform`.** `pdist` returns a condensed
   vector; indexing it like a matrix gives wrong values, not an
   error.
4. **Applying KD-trees to embeddings.** `cKDTree` on 128-d
   vectors is slower than brute force — the curse of
   dimensionality is not optional.
5. **Using `pdist` on a full 1M corpus.** It builds an
   n²/2 array — 500 GB at n=1M. Use `cdist` (nq × n) or ANN.
6. **Treating cosine distance as a percentage.** `0.2` cosine
   distance does not mean "20% similar"; it is a pseudometric on
   direction.

## Best Practices

- Default to cosine (or normalize-then-euclidean) for embedding
  retrieval; use euclidean for raw numeric features and manhattan
  for sparse/binary features.
- Normalize once at ingest and store the unit vectors — never
  normalize per query.
- Verify exact indexes against brute force on a small sample
  before trusting them (KD-tree, FAISS, whatever).
- Check the distance spread of your corpus: if `std << mean`,
  retrieval is meaningless regardless of the index.
- Move to ANN (FAISS HNSW, scikit-learn `NearestNeighbors`
  wrappers, vector DBs) when n exceeds ~10⁵ and latency matters.

## Complexity / Cost

| Operation | Cost |
|---|---|
| `pdist(X)` | O(n² · d) time, O(n²) memory |
| `cdist(Q, X)` | O(nq · n · d), O(nq · n) memory |
| `cKDTree` build | O(n log n) low-d |
| `cKDTree` query | O(log n) low-d, degrades to O(n · d) high-d |
| brute force top-k | O(n · d + n log k) |

The constants matter: a 100-d × 1M corpus brute-forced is ~400
GB of distance computation per full pass — the ANN escape hatch
exists for a reason.

## AI Engineering Relevance

- **RAG retrieval:** the document-store query is a cosine
  (or normalized-euclidean) top-k over embedding vectors.
- **Embedding normalization** before storage is a
  correctness-vs-cost decision: unit vectors make inner product
  = cosine and unlock faster indexes.
- **Deduplication:** near-duplicate detection is pairwise
  distance with a threshold — `pdist` on hashes or embeddings.
- **Clustering:** k-means is euclidean; cosine-similarity
  clustering (spherical k-means) requires normalization.
- **ANN serving:** the production vector store (FAISS, HNSW,
  Milvus, etc.) exists because of the curse of dimensionality
  measured in this topic.

## Practice Exercises

1. Build a 1000 × 32 random embedding matrix, normalize it, and
   return the top-5 neighbors of a query via `cdist`; verify
   `cKDTree` returns the same set.
2. Show that cosine distance equals `euclidean²/2` on unit
   vectors (up to 1e-12) and that rankings agree on a random
   corpus.
3. Measure the pairwise cosine-distance spread for d in
   {4, 16, 64, 256} and confirm the `1/sqrt(d)` scaling.
4. Compare `cKDTree` vs `cdist` timing at d=2 and d=64 for 20k
   points; report the ratio and explain it.
5. Take two document vectors of different lengths (`v` and
   `10v`), show cosine is unchanged while euclidean explodes, and
   argue which metric belongs in a RAG index.

## Summary

- `pdist` = all pairs (condensed), `cdist` = query × reference,
  `squareform` = matrix view.
- Euclidean, manhattan, cosine: magnitude-sensitive, L1-robust,
  direction-only — pick by what "close" means for your data.
- Cosine is the embedding default (scale invariance); on unit
  vectors it is exactly `euclidean²/2`.
- Normalize at ingest; then euclidean search = cosine ranking.
- `cKDTree` gives exact neighbors fast only in low dimensions;
  the distance spread `1/sqrt(d)` kills it for embeddings.
- At scale, approximate neighbor search (HNSW/IVF/FAISS) is the
  only option; verify recall, not exactness.

## Quick Reference

```python
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist, pdist, squareform

D = squareform(pdist(X, metric="euclidean"))   # n x n
M = cdist(Q, X, metric="cosine")               # (nq, n); 1 - cos
M = cdist(Q, X, metric="cityblock")            # manhattan
Xn = X / np.linalg.norm(X, axis=1, keepdims=True)   # normalize
idx = np.argsort(cdist(Qn, Xn), axis=1)[:, :k]      # top-k euclid
tree = cKDTree(points)
dist, idx = tree.query(queries, k=3)           # exact, low-d only
```

## Next Steps

- Topic 15 → 16 connection: sparse TF-IDF retrieval (topic 15)
  and dense embedding retrieval (topic 16) are the two halves of
  RAG; both end in a top-k ranking.
- sklearn `NearestNeighbors` and `KDTree`/`BallTree` wrappers.
- ANN: FAISS (exact `IndexFlatL2` vs `IndexIVFFlat`/`IndexHNSW`),
  HNSWLib — measure recall@k vs latency.
- Vector databases (Pinecone, Qdrant, Milvus): production RAG
  stores built on the exact/ANN trade-off from this topic.

**Related docs:** [scipy.spatial.distance](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html) ·
[scipy.spatial.cKDTree](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html) ·
[Exercise](16-distance-and-similarity.py) · [Glossary](16-distance-and-similarity-glossary.md)
