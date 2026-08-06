# Challenge 34: Advanced Indexing — Retrieve, Bucket, Retrieve

Three tiers that mirror production patterns: Bronze returns top-k
scores without sorting everything; Silver assigns quantile
buckets in log time; Gold retrieves the k nearest rows to a query
while watching memory.

## 🥉 Bronze — Top-k Scores, O(n) (~15 min)

**Task:** Implement `top_k_indices(scores, k)` returning the
indices of the **k largest** scores — using `argpartition`, never
a full sort.

**Signature:**
```python
def top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[5.0, 1.0, 9.0, 2.0, 7.0]`, k=2 | `{2, 4}` (values 9.0, 7.0) |
| seeded `(100_000,)`, k=10 | set-equal to `argsort` top-10 |
| `[3.0, 3.0, 3.0]`, k=2 | any two indices (ties allowed) |
| `k == n` | all indices |

**Constraints:** n ≤ 10⁶. **No Python loops or comprehensions.**
The result set must match the full-sort top-k; the *order* is
unspecified (callers sort winners).

---

## 🥈 Silver — Quantile Buckets (~35 min)

**Task:** Implement `quantile_buckets(values, q)` returning an
integer array `labels` with `labels[i]` in `[0, q)` — the
quantile bucket of `values[i]`. Buckets are defined by
`np.quantile(values, linspace(0, 1, q + 1))` interior edges;
assign with `searchsorted(..., side="right")`.

**Signature:**
```python
def quantile_buckets(values: np.ndarray, q: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[0.0, 0.1, 0.5, 0.9, 1.0]`, q=5 | `[0, 1, 2, 3, 4]` (edges at 0.08/0.34/0.66/0.92) |
| seeded `(10_000,)` uniform, q=5 | every bucket within 10% of n/q |
| `[1.0, 1.0, 1.0, 1.0]`, q=4 | all labels equal (degenerate data) |
| seeded `(10_000,)` normal, q=10 | labels ∈ [0, 10), counts ≈ n/10 |

**Constraints:** n ≤ 10⁶, q ≥ 2. **No Python loops or
comprehensions.** `side="right"` semantics: a value equal to an
edge lands in the bucket *after* the edge.

---

## 🥇 Gold — Nearest-Neighbor Retrieval, Memory-Bounded (~75 min)

**Task:** Implement `retrieve_nearest(X, query, k)` returning the
indices of the `k` rows of `X` closest to `query` by Euclidean
distance — computed with `argpartition`, never a full sort.

**Signature:**
```python
def retrieve_nearest(X: np.ndarray, query: np.ndarray, k: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `X` = seeded `(5000, 32)`, `query` = a copied row, k=5 | the copied row's index is in the result |
| same `X`, arbitrary `query`, k=20 | set-equal to full-sort reference |
| `X` `(64, 8)` with a duplicate row | both duplicate indices may appear (ties) |

**Constraints:** n ≤ 10⁵ rows, d ≤ 256. **No Python loops or
comprehensions.** Peak allocation < 3× X bytes + 32 bytes × n
(tracemalloc-guarded: distance vector + index array only — no
full-sort index buffer, no distance matrix).

**Follow-up:** why is this exact computation the right baseline
before you reach for a KD-tree or an ANN index? (Answer: for
n = 10⁵ × d = 128, one matmul-based distance is ~10 ms; the
complexity wins matter at 10⁶+ rows or high-dimensional d, where
tree structures degrade. See SciPy 16.)

---

## Running

```bash
pytest 03-libraries/numpy/challenges/34-advanced-indexing/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/34-advanced-indexing/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + memory guards
```
