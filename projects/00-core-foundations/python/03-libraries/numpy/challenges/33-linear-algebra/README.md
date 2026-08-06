# Challenge 33: Linear Algebra — Cosine, Fit, Compress

Three tiers, one theme: turn linear algebra vocabulary into
runnable decisions. Bronze normalizes and multiplies; Silver fits
a model; Gold spends a byte budget on a low-rank approximation.

## 🥉 Bronze — Cosine Similarity Matrix (~15 min)

**Task:** Implement `cosine_matrix(X)` returning the `(n, n)`
matrix `S` with `S[i, j]` = cosine similarity between rows `i, j`
of `X`. One normalized matmul — no loops.

**Signature:**
```python
def cosine_matrix(X: np.ndarray) -> np.ndarray:
```

| Input | Expected |
|---|---|
| `[[1, 0], [0, 1]]` | `[[1, 0], [0, 1]]` (orthogonal rows) |
| `[[2, 0], [4, 0]]` | `[[1, 1], [1, 1]]` (collinear rows) |
| seeded `(50, 32)` | diagonal ≈ 1, symmetric, all entries in [-1, 1] |

**Constraints:** n ≤ 10⁴. **No Python loops or comprehensions.**
Numerical expectations are exact (dot products of orthogonal/
collinear vectors round cleanly at 1e-12).

---

## 🥈 Silver — Polynomial Fit (~35 min)

**Task:** Implement `fit_polynomial(t, y, degree)` that fits
`y ≈ c₀ + c₁ t + c₂ t² + ... + c_d t^d` by least squares and
returns the coefficient vector `[c₀ ... c_d]`.

**Signature:**
```python
def fit_polynomial(t: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| clean cubic data, degree 3 | coefficients ≈ truth (atol 1e-6) |
| noisy line, degree 1 | intercept/slope within 0.2 |
| noisy line fitted with degree 5 | length-6 coefficient vector, residual ≤ noisy line's |
| 4 points, degree 3 | exact interpolation (atol 1e-6) |

**Constraints:** n ≤ 10⁵, degree ≤ 8. **No Python loops or
comprehensions.** Build the Vandermonde columns with
`np.vander(t, degree + 1, increasing=True)` or `np.column_stack`.

---

## 🥇 Gold — Byte-Budget SVD Compression (~75 min)

**Task:** Implement `compress_svd(A, max_bytes)` that returns
`(approx, k)` where `approx` is the truncated-SVD approximation of
`A` using the **largest** rank `k` whose factors fit in
`max_bytes`, with storage counted as `k * (m + n + 1) * 8` bytes
(float64 factors).

**Signature:**
```python
def compress_svd(A: np.ndarray, max_bytes: int) -> tuple[np.ndarray, int]:
```

| Input | Expected |
|---|---|
| seeded `(64, 64)`, max_bytes huge | `k == 64`, `approx == A` (atol 1e-12) |
| seeded `(64, 64)`, max_bytes = 8·(64+64+1)·k | exactly rank `k` |
| `max_bytes < 8·(m+n+1)` | raises `ValueError` |

**Constraints:** `m, n ≤ 256`. **No Python loops or
comprehensions** (choose `k` with vectorized masking — e.g.
`np.arange` and `sum` of a boolean). Peak allocation < 6× input
bytes (tracemalloc-guarded; a rank-k reconstruction must not copy
`A` or materialize `np.diag(s)` of full shape).

**Follow-up:** the Eckart-Young error of your chosen `k` equals
`sqrt(sum(s[k:]**2))` — print it and the compression ratio
`A.size / (k*(m+n+1))`.

---

## Running

```bash
pytest 03-libraries/numpy/challenges/33-linear-algebra/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/33-linear-algebra/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + edge cases + memory guards
```
