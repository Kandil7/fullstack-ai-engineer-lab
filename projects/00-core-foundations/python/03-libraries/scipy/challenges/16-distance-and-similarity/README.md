# Challenge 16: Distance and Similarity — Rank, Normalize, Escape

Three tiers of retrieval discipline: Bronze ranks by brute
force, Silver makes cosine and euclidean agree, Gold uses
KD-trees exactly and quantifies the curse of dimensionality.

## 🥉 Bronze — Brute-Force Top-k (~15 min)

**Task:** Implement `nearest_brute(Q, X, k, metric="euclidean")`
that returns `(dist, idx)` where `idx[i]` are the indices of the
`k` nearest rows of `X` to query `Q[i]` (sorted ascending by
distance) and `dist[i]` their distances.

**Signature:**
```python
def nearest_brute(Q: np.ndarray, X: np.ndarray, k: int,
                  metric: str = "euclidean") -> tuple[np.ndarray, np.ndarray]:
```

| Input | Expected |
|---|---|
| `Q=[[0,0]]`, `X=[[1,0],[0,3]]`, k=1 | `idx == [[0]]` (dist 1.0 < 3.0) |
| k=3 on 5 points | `dist.shape == (nq, 3)`, rows sorted ascending |
| `metric="cosine"` on 10×4 | works; cosine distance ∈ [0, 2] |
| k > `len(X)` | raises `ValueError` |

**Constraints:** **No Python loops or comprehensions.** Use
`np.argsort(..., axis=1)[:, :k]`.

---

## 🥈 Silver — Cosine ≡ Normalized Euclidean (~35 min)

**Task:** Implement three functions:

1. `cosine_pair(u, v)` — cosine distance computed by hand:
   `1 − (u·v)/(|u||v|)`; zero-norm inputs raise `ValueError`.
2. `normalized_topk(Q, X, k)` — L2-normalize both arrays, then
   return top-k indices by **euclidean** distance (sorted
   ascending). Must equal cosine top-k up to index order ties.
3. `spread(V)` — the standard deviation of all pairwise cosine
   distances in `V` (via `pdist` + `squareform`), as a float.

**Signatures:**
```python
def cosine_pair(u: np.ndarray, v: np.ndarray) -> float:
def normalized_topk(Q: np.ndarray, X: np.ndarray,
                    k: int) -> np.ndarray:
def spread(V: np.ndarray) -> float:
```

| Input | Expected |
|---|---|
| `u=[1,0]`, `v=[0,1]` | `0.0` (orthogonal) |
| `u=[1,0]`, `v=[5,0]` | `0.0` (scale-invariant) |
| `u=[0,0]`, `v=[1,1]` | raises `ValueError` |
| 50×20 random, k=5 | top-k == cosine cdist top-k (same set) |
| 2000 random unit vectors, d=2 | spread ≈ 0.707 (± 0.05) |
| 2000 random unit vectors, d=128 | spread ≈ 0.088 (± 0.02) |

**Constraints:** **No Python loops or comprehensions.** No
calling `cdist` with `"cosine"` inside `normalized_topk` — the
point is that normalization turns cosine into euclidean.

---

## 🥇 Gold — KD-Tree and the Curse (~75 min)

**Task:** Implement two functions:

1. `fast_neighbors(points, queries, k)` — exact nearest neighbors
   via `cKDTree`, returning `(dist, idx)` sorted ascending.
2. `spread_ratio(d_low, d_high, n=2000, seed=42)` — build random
   unit vectors in both dimensions and return
   `spread(d_low) / spread(d_high)`.

**Signatures:**
```python
def fast_neighbors(points: np.ndarray, queries: np.ndarray,
                   k: int) -> tuple[np.ndarray, np.ndarray]:
def spread_ratio(d_low: int, d_high: int, n: int = 2000,
                 seed: int = 42) -> float:
```

| Input | Expected |
|---|---|
| 500 pts, 3 queries, k=3, d=2 | identical to brute-force `cdist` top-3 |
| 50 000 pts, 1000 queries, k=3, d=2 | peak memory < 10 MB (cdist would need ~400 MB) |
| `spread_ratio(2, 128)` | ≈ 8 (theory: `sqrt(128/2)`), assert > 4 |
| `spread_ratio(8, 32)` | ≈ 2 (theory: `sqrt(32/8)`), assert > 1.5 |
| k > `len(points)` | raises `ValueError` |

**Constraints:** **No Python loops or comprehensions.**
`tracemalloc` guards the KD-tree path only.

---

## Running

```bash
pytest 03-libraries/scipy/challenges/16-distance-and-similarity/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/16-distance-and-similarity/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + memory guards + deterministic data
```
