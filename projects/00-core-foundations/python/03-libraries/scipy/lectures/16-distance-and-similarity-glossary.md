# Distance and Similarity — Glossary 16

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `cdist` | Function | Query × reference distance matrix, shape `(nq, n)` |
| `cityblock` | Metric | Manhattan distance: `sum |x − y|` — L1 |
| `cKDTree` | Structure | Exact nearest-neighbor index; fast only in low dims |
| Condensed | Format | `pdist` output: `n(n−1)/2` values, upper triangle |
| Contrast collapse | Concept | Distance spread shrinking as `1/sqrt(d)` — the curse |
| Cosine distance | Metric | `1 − cos(angle)` — direction only, scale-invariant |
| Cosine similarity | Metric | `cos(angle)` — the classic embedding score |
| Curse of dimensionality | Concept | High-d spaces make nearest ≈ farthest |
| Euclidean distance | Metric | Straight-line distance — magnitude-sensitive |
| L2 normalization | Operation | Divide by the norm: unit vectors, cosine = inner product |
| `pdist` | Function | All pairwise distances within one set (condensed) |
| `squareform` | Function | Condensed vector ↔ symmetric matrix |
| Scale invariance | Concept | Metric unchanged by vector magnitude |
| Spread | Metric | `std` of pairwise distances; contrast of the space |
| Top-k retrieval | Concept | Rank candidates by distance, return the k smallest |

## Detailed Definitions

### `cdist`
**Definition**: Computes the distance between every row of `Q`
(queries) and every row of `X` (references): result shape
`(len(Q), len(X))`. The retrieval workhorse.

**Example**:
```python
from scipy.spatial.distance import cdist
dists = cdist(Q, X, metric="euclidean")
top = np.argsort(dists, axis=1)[:, :k]
```

**Complexity**: O(nq · n · d) time, O(nq · n) memory.
**Related**: `pdist`, Top-k retrieval

---

### `cityblock`
**Definition**: Manhattan (L1) distance: `sum |x_i − y_i|`.
Robust to outlier coordinates; natural for sparse or binary
features.

**Example**:
```python
M = cdist(Q, X, metric="cityblock")
```

**Complexity**: O(d) per pair.
**Related**: Euclidean distance

---

### `cKDTree`
**Definition**: Exact nearest-neighbor index built by
partitioning space along axes. Fast in low dimensions, exact —
but degenerates for d ≳ 8–64, where it can be *slower* than
brute force.

**Example**:
```python
from scipy.spatial import cKDTree
tree = cKDTree(points)
dist, idx = tree.query(queries, k=3)
```

**Complexity**: O(n log n) build, O(log n) query (low-d).
**Related**: Curse of dimensionality, Top-k retrieval

---

### Condensed
**Definition**: The compact form returned by `pdist`: only the
`n(n−1)/2` upper-triangle distances, stored as one flat array.
Indexing it like a matrix silently yields wrong values.

**Example**:
```python
D = squareform(pdist(X))     # convert first
```

**Complexity**: O(n²) memory.
**Related**: `pdist`, `squareform`

---

### Contrast collapse
**Definition**: The observed symptom of the curse: the spread
(`std`) of pairwise distances shrinks as `1/sqrt(d)`, so nearest
and farthest neighbors become numerically indistinguishable.

**Example**:
```python
# d=2 spread 0.707 -> d=128 spread 0.091 (cosine, unit vectors)
```

**Complexity**: —.
**Related**: Curse of dimensionality, Spread

---

### Cosine distance
**Definition**: `1 − cos(θ)` — a pseudometric on direction:
0 = same direction, 1 = orthogonal, 2 = opposite. Not a
"percentage of dissimilarity".

**Example**:
```python
D = cdist(Q, X, metric="cosine")
```

**Complexity**: O(d) per pair.
**Related**: Cosine similarity, Scale invariance

---

### Cosine similarity
**Definition**: `cos(θ) = (u·v)/(|u||v|)` — the classic embedding
score. Cosine distance = `1 − similarity`.

**Example**:
```python
sim = 1.0 - cdist(Q, X, metric="cosine")
```

**Complexity**: O(d) per pair.
**Related**: Cosine distance

---

### Curse of dimensionality
**Definition**: In high dimensions, volume concentrates in
shells; random vectors are nearly orthogonal and nearly
equidistant. Space-partitioning search strategies stop paying.

**Example**:
```python
# unit vectors in d dims: mean cosine distance ~ 1, std ~ 1/sqrt(d)
```

**Complexity**: —.
**Related**: Contrast collapse, `cKDTree`

---

### Euclidean distance
**Definition**: `sqrt(sum (x_i − y_i)²)` — straight-line distance.
Magnitude-sensitive: longer vectors are farther even with the
same direction.

**Example**:
```python
D = cdist(Q, X, metric="euclidean")
```

**Complexity**: O(d) per pair.
**Related**: Cosine distance, L2 normalization

---

### L2 normalization
**Definition**: Divide a vector by its norm so it lies on the
unit sphere. After normalizing both sides, euclidean search has
exactly cosine ranking: `euclid² = 2(1 − cos)`.

**Example**:
```python
Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
```

**Complexity**: O(n · d).
**Related**: Cosine distance, Top-k retrieval

---

### `pdist`
**Definition**: All pairwise distances within a single set,
returned in condensed form. For clustering and deduplication;
never for a 1M corpus (n²/2 memory).

**Example**:
```python
D = pdist(X, metric="euclidean")
```

**Complexity**: O(n² · d) time, O(n²) memory.
**Related**: `cdist`, Condensed, `squareform`

---

### `squareform`
**Definition**: Converts between the condensed vector and the
symmetric n × n distance matrix. Always use it before indexing
`pdist` output like a matrix.

**Example**:
```python
M = squareform(pdist(X))
```

**Complexity**: O(n²).
**Related**: Condensed, `pdist`

---

### Scale invariance
**Definition**: A metric unchanged by multiplying the vector by a
constant: `cos(a, 2a) = 1`, while `euclid(a, 2a) = |a|`. This is
why cosine is the embedding default — document length must not
change meaning.

**Example**:
```python
cdist([a], [2 * a], "cosine")[0, 0]        # 0.0
```

**Complexity**: —.
**Related**: Cosine distance

---

### Spread
**Definition**: The standard deviation of pairwise distances in a
corpus — the signal retrieval ranks on. When
`spread << mean`, neighbors are noise.

**Example**:
```python
spread = squareform(pdist(V, "cosine")).std()
```

**Complexity**: O(n²).
**Related**: Contrast collapse, Top-k retrieval

---

### Top-k retrieval
**Definition**: Ranking all candidates by distance and returning
the k smallest. The universal final step of RAG and
recommenders — everything upstream (index, metric, ANN) exists
to make this fast.

**Example**:
```python
idx = np.argsort(cdist(Q, X), axis=1)[:, :k]
```

**Complexity**: O(n · d + n log k).
**Related**: `cdist`, `cKDTree`

## Key Concepts Summary

### Metric choice
- Euclidean: raw numeric features; magnitude matters.
- Cosine: embeddings; direction matters, magnitude is noise.
- Manhattan: sparse/binary, outlier-robust.
- Normalized euclidean ≡ cosine ranking.

### The curse, quantitatively
- Random unit vectors: distance mean ~ 1, spread ~ `1/sqrt(d)`.
- KD-trees: fast and exact in low-d; slower than brute force in
  embedding dimensions.
- At scale, ANN (HNSW/IVF/FAISS) with recall@k measurement is
  the production answer.

### Retrieval discipline
- Normalize once at ingest.
- Verify exact indexes against brute force on a sample.
- Check the spread before trusting any ranking.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `cdist` — ___
2. Cosine distance — ___
3. `cKDTree` — ___
4. L2 normalization — ___
5. Contrast collapse — ___
6. Condensed — ___

**Answers:**
1. e, 2. d, 3. a, 4. f, 5. c, 6. b

a. Exact nearest-neighbor index; low-dimensional only
b. `pdist` output: n(n−1)/2 values, not a matrix
c. Distance spread shrinking as 1/sqrt(d)
d. 1 − cos(angle): direction only, scale-invariant
e. Query × reference distance matrix (nq, n)
f. Dividing by the norm so euclidean = cosine ranking

---

**Related docs:** [scipy.spatial.distance](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html) ·
[Back to lecture](16-distance-and-similarity-lecture.md)
