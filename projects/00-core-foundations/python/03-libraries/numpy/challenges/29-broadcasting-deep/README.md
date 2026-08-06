# Challenge 29: Broadcasting Without Explicit Loops

Broadcasting exists so batch math never touches a Python `for`. This
challenge proves it: every tier must be solved **without any Python
loop or comprehension** — the test suite counts operations.

## 🥉 Bronze — Bias Add (~15 min)

**Task:** Implement `add_bias(batch, bias)` that adds a per-dimension
bias vector to every row of a batch, using broadcasting — no loops.

**Signature:**
```python
def add_bias(batch: np.ndarray, bias: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `batch = [[1,2],[3,4]]`, `bias = [10, 20]` | `[[11, 22], [13, 24]]` |
| `batch` shape `(7, 3)`, `bias` shape `(3,)` | shape `(7, 3)`, each row `+ bias` |
| `batch` shape `(B, D)`, `bias` wrong length `(D+1,)` | `ValueError` |

**Constraints:** B ≤ 10³, D ≤ 10³. Any correct approach passes, but the
no-loop guard applies to Silver/Gold only.

---

## 🥈 Silver — Row Z-Score (~35 min)

**Task:** Implement `row_zscore(X)` that z-scores **each row**
independently: `z[i] = (X[i] - mean(X[i])) / std(X[i])`. Rows with
zero standard deviation (all identical values) must become all zeros,
not `nan`.

**Signature:**
```python
def row_zscore(X: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[[1, 2, 3], [4, 4, 4]]` | `[[-1, 0, 1], [0, 0, 0]]` |
| `X` shape `(100_000, 8)`, seeded | same shape; each row mean ≈ 0, std ≈ 1 |
| `X` shape `(1, 5)` | shape `(1, 5)` |

**Constraints:** n ≤ 10⁶ rows. **No Python loops or comprehensions** —
the test inspects your source and rejects `for`/`while`/comprehensions.
This forces `keepdims=True` (or `[:, None]`) broadcast math.

---

## 🥇 Gold — Pairwise Distances, Memory-Bounded (~75 min)

**Task:** Implement `pairwise_distances(a, b)` returning the `(n, m)`
matrix of Euclidean distances between rows of `a` and rows of `b`.
Must be **fully vectorized and memory-lean**: use the identity
`||a - b||² = ||a||² + ||b||² - 2·a·bᵀ` so you never materialize an
`(n, m, d)` tensor.

**Signature:**
```python
def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `a = [[0, 0]]`, `b = [[3, 4]]` | `[[5.0]]` (3-4-5 triangle) |
| `a` shape `(20, 8)`, `b` shape `(30, 8)`, seeded | `(20, 30)`, matches reference `sqrt(sum((a[i]-b[j])²))` |
| `a` shape `(2000, 64)`, `b` shape `(2000, 64)` | `(2000, 2000)`, diagonal ≈ 0, symmetric |

**Constraints:** n = m = 2000, d = 64, **peak memory < 200 MB** (the
naive `a[:, None, :] - b[None, :, :]` route needs ~2 GB here; a
broadcast-to-`(n,m,d)` approach is rejected by `tracemalloc`).
No Python loops or comprehensions.

**Follow-up:** what breaks first at n = m = 10⁵? (Answer: the `(n, m)`
result itself is 80 GB of float64 — the answer must become approximate:
ANN indexes, or block-wise computation writing to disk.)

---

## Running

```bash
pytest 03-libraries/numpy/challenges/29-broadcasting-deep/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/29-broadcasting-deep/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + op-count/memory guards
```
