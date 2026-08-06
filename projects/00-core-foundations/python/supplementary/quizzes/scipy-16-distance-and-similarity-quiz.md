# SciPy 16 — Distance and Similarity Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · 8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** For embedding retrieval (RAG-style), the default metric is:

- A) euclidean — always
- B) cosine — direction matters, magnitude is length noise
- C) manhattan — embeddings are sparse
- D) chebyshev — it is the fastest

**E2 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import cdist

Q = np.ones((2, 3))
X = np.ones((4, 3))
print(cdist(Q, X).shape)
```

- A) `(2, 3)`
- B) `(4, 3)`
- C) `(2, 4)`
- D) `(6, 6)`

**E3.** `pdist(X, metric="euclidean")` on `n` points returns:

- A) an `n × n` matrix
- B) a condensed vector of `n(n−1)/2` distances
- C) `n` distances, one per point
- D) a `cKDTree`

**E4 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import cdist

a = np.array([1.0, 0.0])
print(np.round(cdist([a], [2 * a], "cosine")[0, 0], 6))
```

- A) `0.0` — same direction, cosine ignores magnitude
- B) `1.0` — the distance between the tips of the vectors
- C) `0.5`
- D) `2.0`

**E5.** `cKDTree(points).query(queries, k=3)` returns:

- A) just the neighbor indices
- B) `(dist, idx)` — distances and indices, sorted ascending
- C) a single nearest index
- D) the distances only

**E6 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
D = squareform(pdist(X, "euclidean"))
print(np.round(D[1, 2], 4), np.isclose(D[1, 2], D[2, 1]))
```

- A) `1.4142 True`
- B) `1.0 True`
- C) `1.4142 False`
- D) `0.0 True`

---

## Medium

**M1.** Document A is "cat" and document B is the same word
repeated 100 times. Cosine says the distance is 0. Why is that
desirable?

- A) cosine is broken for repeated tokens
- B) both vectors point in the same direction — length (document
  size) should not change the topic
- C) because 100 × word_count is too large for euclidean
- D) euclidean would also say 0

**M2 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import cdist

X = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
Xu = X / np.linalg.norm(X, axis=1, keepdims=True)
c = cdist(Xu, Xu, "cosine")
e2 = cdist(Xu, Xu, "euclidean") ** 2
print(np.allclose(c, e2 / 2))
```

- A) `True` — on unit vectors, cosine = euclidean²/2
- B) `False` — the two metrics are never comparable
- C) `True` for the first row only
- D) raises `ValueError`

**M3.** Which code correctly turns cosine ranking into euclidean
ranking?

- A) `cdist(Q, X, "euclidean")` on the raw vectors
- B) normalize both with `v / np.linalg.norm(v)`, then
  `cdist(..., "euclidean")`
- C) `cdist(Q, X, "cosine")` then square the result
- D) `cdist(Q * 2, X, "cosine")`

**M4 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

rng = np.random.default_rng(0)
V = rng.normal(size=(500, 2))
V /= np.linalg.norm(V, axis=1, keepdims=True)
print(round(float(squareform(pdist(V, "cosine")).std()), 2))
```

- A) `0.71` — spread ≈ `1/sqrt(2)`
- B) `1.00`
- C) `0.10`
- D) `0.50`

**M5.** The curse of dimensionality, measured as the spread of
pairwise cosine distances among random unit vectors:

- A) spread grows like `sqrt(d)`
- B) spread shrinks like `1/sqrt(d)` — contrast collapses
- C) spread is constant in every dimension
- D) spread is zero above d=64

**M6 (code-output).** What prints?
```python
import numpy as np

sim = np.array([0.3, 0.8, 0.1, 0.6])
print(np.argsort(sim)[::-1][:2])
```

- A) `[1 3]`
- B) `[3 1]`
- C) `[0 2]`
- D) `[1 0]`

**M7.** `cKDTree` on 100-d embedding vectors (n = 100k) will
likely be:

- A) much faster than brute force — trees always win
- B) about as fast or slower than brute force — the curse of
  dimensionality degrades space partitioning
- C) exact and fast — KD-trees are dimension-proof
- D) unusable, it refuses to build above d=32

**M8 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist

rng = np.random.default_rng(1)
pts = rng.uniform(size=(100, 2))
q = rng.uniform(size=(2, 2))
tree = cKDTree(pts)
d, i = tree.query(q, k=2)
brute = np.sort(cdist(q, pts), axis=1)[:, :2]
print(np.allclose(d, brute, atol=1e-9))
```

- A) `True` — KD-tree results are exact
- B) `False` — KD-trees are approximate by design
- C) `True` only because `atol=1e-9`
- D) raises `ValueError`

**M9.** The scipy metric name for Manhattan distance is:

- A) `"manhattan"`
- B) `"cityblock"`
- C) `"l1"`
- D) `"minkowski"`

---

## Hard

**H1.** A document corpus has vectors of wildly different lengths
(documents 1 to 10k tokens). Ranking by raw euclidean distance:

- A) is equivalent to cosine ranking
- B) is dominated by document length — a long, unrelated document
  can be "closer" than a short relevant one
- C) is always better than cosine at scale
- D) only works after applying `squareform`

**H2.** The distance spread of a corpus is `std = 0.05` with
`mean = 1.0` (cosine). What does this mean for retrieval?

- A) retrieval will be very precise — small distances are common
- B) nearest and farthest neighbors are nearly indistinguishable;
  rankings are close to noise
- C) the KD-tree will be extremely fast
- D) euclidean would fix it

**H3 (code-output).** What prints?
```python
import numpy as np
from scipy.spatial.distance import cdist

X = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 0.0]])
d = cdist([[0.0, 0.0]], X, "euclidean")[0]
print(int(np.argmin(d)), int(d[np.argmin(d)]))
```

- A) `2 1` — the nearest *other* point
- B) `0 0` — the query is itself in the corpus
- C) `1 5`
- D) `1 0`

**H4.** At 5M × 128-d vectors with a 10 ms latency budget, the
right tool is:

- A) `pdist` — condensed form saves memory
- B) `cKDTree` — exact and fast
- C) an ANN index (HNSW/IVF/FAISS or a vector DB) with
  recall@k measurement
- D) brute-force `cdist` on a bigger machine

**H5.** Why does `cKDTree` degenerate for embeddings while
`pdist`-based brute force does not?

- A) brute force ignores the curse; trees suffer from it
- B) in high dimensions, axis-aligned partitions cannot prune:
  every branch may contain the neighbor, so the tree visits
  ~everything — and pays tree overhead on top
- C) KD-trees only work on integers
- D) trees need sorted input; embeddings are never sorted

---

## Answer Key

**E1. B — cosine.**
Embedding magnitude is length/word-count noise; cosine keeps only
the direction. Euclidean (A) is dominated by magnitude;
manhattan/chebyshev (C/D) are for other data types.

**E2. C — `(2, 4)`.**
`cdist(Q, X)` returns one row per query and one column per
reference: `(len(Q), len(X)) = (2, 4)`.
*Distractors:* A/B are input shapes; D is the all-pairs size.

**E3. B — condensed.**
`pdist` returns the upper triangle as `n(n−1)/2` values.
`squareform` converts to the `n × n` matrix (A). C/D are other
APIs.

**E4. A — `0.0`.**
`a` and `2a` share a direction: cosine distance is exactly 0 —
the scale-invariance property that makes cosine the embedding
metric. B would be the euclidean answer; C/D are invented.

**E5. B — `(dist, idx)` sorted ascending.**
`query` returns both arrays; `k=3` gives the 3 nearest, ordered
by distance. A/C/D each miss half the contract.

**E6. A — `1.4142 True`.**
`pdist`/`squareform` give the distance matrix; `D[1,2]` is the
distance between `[1,0]` and `[0,1]` = `sqrt(2) ≈ 1.4142`, and
the matrix is symmetric by construction.
*Distractors:* C forgets symmetry; B/D confuse the values.

**M1. B — direction is the topic.**
Document length is magnitude, and length must not change the
topic. Cosine ignores it; euclidean (D) would report a large
distance, which is why raw euclidean fails for text. A/C are
misreads of the metric.

**M2. A — `True`.**
On unit vectors, `euclidean(u,v)² = 2(1 − cos(u,v)) = 2·cosine_distance`,
verified for all pairs. This is the mathematical basis of
normalize-then-euclidean.

**M3. B — normalize both, then euclidean.**
After L2 normalization the two rankings coincide exactly. A
mixes metrics (raw euclidean ≠ cosine); C squares distances
(does not change ranking but neither does it turn cosine into
euclidean); D scales queries and changes nothing for cosine.

**M4. A — `0.71`.**
For unit vectors in d=2, pairwise cosine-distance spread ≈
`1/sqrt(2) ≈ 0.707` — the deterministic seed reproduces 0.71.
*Distractors:* B is the mean (~1.0), C is the d=128 value, D is
half the d=2 value.

**M5. B — spread shrinks like `1/sqrt(d)`.**
Random unit vectors become nearly equidistant: contrast
collapses, and "nearest" loses meaning. A inverts the scaling;
C/D contradict the measurement (0.707 → 0.091 from d=2 to 128).

**M6. A — `[1 3]`.**
`argsort` ascending = `[2 0 3 1]`; reversed = `[1 3 0 2]`; the
top-2 are indices 1 (0.8) and 3 (0.6).
*Distractors:* B swaps the order; C/D pick wrong elements.

**M7. B — degenerates toward brute force.**
Measured on 20k points: KD-tree 4× *faster* than brute at d=2
but 4× *slower* at d=64. Trees are a low-dimensional tool;
embeddings need ANN. A/C/D contradict the measurement.

**M8. A — `True`.**
`cKDTree` is exact: its distances match brute-force `cdist`
exactly (same data, same metric). KD-trees are *fast* heuristics
in search order, but their results are provably exact.
*Distractors:* B is the ANN misconception; C invents a tolerance
effect; D is wrong.

**M9. B — `"cityblock"`.**
scipy's name for Manhattan is `cityblock` (the L1 metric).
`"manhattan"` (A) does not exist, `"l1"` (C) is not a scipy
alias, `"minkowski"` (D) is a family with `p` parameter.

**H1. B — dominated by length.**
Raw euclidean distance includes magnitude: `dist(v, 10v) = |v|`,
so a long irrelevant document can beat a short relevant one.
Cosine (A) is invariant to length; normalization makes euclidean
equal cosine (the fix, not a property of raw euclidean).

**H2. B — ranking is close to noise.**
With mean 1.0 and spread 0.05, every pair is about the same
distance apart — the contrast-collapse signature. No metric or
index fix recovers signal that is not in the distances (the
spread is a property of the *data*, not the tool).

**H3. B — `0 0`.**
The query `[0,0]` is itself the first row of `X`: distance 0,
argmin 0. The nearest *other* point would be `[1,0]` (index 2,
distance 1) — a nice trap for readers who ignore self-matches
in corpora.

**H4. C — ANN with recall@k measurement.**
5M × 128-d exact search cannot meet a 10 ms budget; ANN
(HNSW/IVF/FAISS) trades a tiny recall loss for sub-linear
latency, and you must *measure* recall@k to verify the trade.
`pdist` (A) is O(n²) memory; `cKDTree` (B) degenerates in 128-d;
bigger hardware (D) is linear scaling against a quadratic
problem.

**H5. B — partitions cannot prune.**
High-dimensional volume concentrates in shells; any axis-aligned
box may contain the neighbor, so the tree visits most leaves —
and then pays its overhead on top. Brute force (A) is simply
linear and has no such overhead; C/D invent mechanical limits.
This is why production ANN uses graphs/quantization instead of
space partitioning.
