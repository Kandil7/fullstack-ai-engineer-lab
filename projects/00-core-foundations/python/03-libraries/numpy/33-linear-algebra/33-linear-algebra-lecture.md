# NumPy 33 — Linear Algebra: matmul, solve, decompositions, norms

## Topic Overview

Linear algebra is the substrate of machine learning: every forward
pass is matrix multiplication, every recommender is a `solve` or a
`lstsq`, every embedding projector is an SVD, and every "how close
are these vectors" question is a norm. This lecture maps the
`numpy.linalg` surface you will actually use — `@`/`matmul`,
`solve` over `inv`, `lstsq`, `QR`, `SVD`, `eigh`, norms, and the
condition number — with the *engineering* judgment around each:
when to use which, what each costs, and how each breaks.

## Learning Objectives

By the end of this lecture you will be able to:

1. Multiply arrays with `@`/`np.matmul` and explain how broadcasting
   applies to batched matmuls.
2. Justify why `np.linalg.solve` beats `np.linalg.inv(A) @ b`.
3. Fit models with `np.linalg.lstsq` and interpret its residual.
4. Use QR and SVD, reconstruct matrices, and compute low-rank
   approximations with a provable error bound.
5. Verify eigenvalue/eigenvector pairs with `eigh` for symmetric
   matrices.
6. Compute L1/L2/infinity/Frobenius norms and the condition number,
   and interpret what they say about numerical health.

## Prerequisites

- NumPy 29 (broadcasting), 30 (vectorization), 32 (dtypes).
- Comfort with Python sequences and slicing.
- No formal linear algebra course assumed — definitions are given
  as you go, with the intuition first.

---

## Key Concepts

### 1. `@`, `np.matmul`, and `np.dot` — the shape grammar

Matrix multiplication is defined for `(m, k) @ (k, n) -> (m, n)`:
the inner dimension must match. Three ways to invoke it:

| Expression | Behavior |
|---|---|
| `a @ b` | The operator — use this. |
| `np.matmul(a, b)` | Function form of the same operation. |
| `np.dot(a, b)` | 2-D behaves identically; higher dims differ (sum over last of `a` vs second-to-last of `b`; no batch broadcasting). |

For 1-D arrays, `(n,) @ (n,)` is the inner product (a scalar) — a
special case that trips people reading shapes: a vector times a
vector is a *number*.

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
print(a @ b)                    # 32.0 -- scalar
A = np.arange(6.0).reshape(2, 3)
B = np.arange(12.0).reshape(3, 4)
print((A @ B).shape)            # (2, 4)
```

**Cost:** O(n³) for `(n, n) @ (n, n)`; O(m·k·n) in general. BLAS
handles the heavy lifting — always prefer vectorized matmul over
Python loops.

---

### 2. Batched matmul — broadcasting the leading dimensions

`np.matmul` broadcasts leading dimensions:

```python
X = np.random.default_rng(0).normal(size=(5, 8, 4))  # 5 batches
W = np.random.default_rng(1).normal(size=(4, 3))     # shared weights
print((X @ W).shape)                                 # (5, 8, 3)
```

`(5, 8, 4) @ (4, 3)` → `(5, 8, 3)`: the batch dim `5` broadcasts
against nothing on the right operand. This one line replaces an
explicit loop over 5 matrices — the single most common ML pattern
(next to `X @ W + b`).

**Common trap:** `(n,) @ (m, n)` fails; the 1-D array must be
reshaped or the shape rule violated. When in doubt, print shapes.

---

### 3. `solve` over `inv` — never invert to solve

To solve `A x = b`:

```python
x = np.linalg.solve(A, b)          # LU factorization + back-substitution
```

Why not `np.linalg.inv(A) @ b`?

1. **Stability.** `inv` computes the inverse via elimination, then
   multiplies — two sources of rounding. `solve` solves directly.
2. **Cost.** Both are O(n³), but `inv` does *more* work in the
   same class.
3. **Semantics.** You almost never want the inverse; you want the
   solution.

`np.linalg.solve` requires a square, full-rank `A`; otherwise it
raises `LinAlgError`. For rectangular or rank-deficient problems,
use `lstsq` (next section).

```python
import numpy as np

rng = np.random.default_rng(42)
A = rng.normal(size=(5, 5))
x_true = rng.normal(size=5)
b = A @ x_true
x = np.linalg.solve(A, b)
print(np.allclose(x, x_true, atol=1e-10))     # True
```

---

### 4. `lstsq` — the least-squares workhorse

`np.linalg.lstsq(A, b, rcond=None)` finds `x` minimizing
`||A x - b||₂`. It accepts rectangular `A` (`(m, n)` with m ≥ n)
and rank-deficient matrices, returning `(x, residuals, rank, s)`.

```python
t = np.linspace(0.0, 1.0, 20)
A5 = np.column_stack([np.ones_like(t), t])          # design matrix
y = 3.0 + 2.0 * t + rng.normal(scale=0.05, size=t.size)
coef, *_ = np.linalg.lstsq(A5, y, rcond=None)
print(np.round(coef, 4))                            # ~[3.0, 2.0]
```

This is linear regression in one call. The same API serves
polynomial fits (add `t**2`, `t**3` columns), ridge-style problems
(regularize by appending rows), and recommenders (solve for user
and item factors).

**Cost:** O(m·n²) for `(m, n)` with m ≥ n.

---

### 5. QR — the stable triangular factorization

`A = Q R` where `Q` has orthonormal columns (`Q.T @ Q = I`) and
`R` is upper triangular.

```python
Q, R = np.linalg.qr(A6)
```

- `np.linalg.qr` returns the **reduced** form by default: for
  `(m, n)` with m ≥ n, `Q` is `(m, n)` and `R` is `(n, n)`.
- `Q` columns are an orthonormal basis of the column space.
- QR is what `solve` and `lstsq` use under the hood; `eigh` uses a
  variant (tridiagonalization).

QR is rarely called directly in ML, but it is the *answer* to "how
do I get an orthonormal basis without SVD" and it underlies most
stability guarantees you rely on.

---

### 6. SVD — decomposition, reconstruction, low-rank

Every `(m, n)` matrix factors as

```
A = U diag(s) Vh      (Vh = V.T)
```

- `U` `(m, m)`, `Vh` `(n, n)` orthonormal, `s` `(min(m,n),)` singular values, sorted descending.
- `np.linalg.svd(A)` defaults to `full_matrices=True`; reconstruct with `(U[:, :s.size] * s) @ Vh` (the extra U columns pair with zero singular values).

```python
U, s, Vh = np.linalg.svd(A7)
recon = (U[:, :s.size] * s) @ Vh
print(np.allclose(recon, A7, atol=1e-12))   # True
```

**Eckart-Young theorem:** the best rank-k approximation of `A` is
the truncated SVD `U[:, :k] @ diag(s[:k]) @ Vh[:k, :]`, and its
error in the Frobenius norm is exactly `sqrt(sum(s[k:]**2))` —
the tail of the singular values.

```python
k = 2
approx = U[:, :k] @ np.diag(s[:k]) @ Vh[:k, :]
print(np.allclose(np.linalg.norm(A7 - approx),
                  np.sqrt(np.sum(s[k:] ** 2)), rtol=1e-6))   # True
```

**AI relevance:** PCA, latent semantic analysis, embedding
compression, and weight pruning are all truncated SVDs. The
singular-value spectrum tells you the *effective rank* — how many
dimensions actually carry signal.

**Cost:** O(m·n²) for `(m, n)`; `svd` on huge matrices is why
`np.linalg.svd` is not for billion-scale data (that is `sklearn`
or randomized SVD territory).

---

### 7. Eigenvalues — and why symmetry matters

`np.linalg.eig` returns possibly complex eigenvalues for general
matrices. For symmetric (or Hermitian) matrices, eigenvalues are
real and `eigh` is the right tool — specialized, faster, and
guaranteed stable:

```python
A8 = rng.normal(size=(5, 5))
A_sym = A8 + A8.T                              # symmetric
w, V = np.linalg.eigh(A_sym)
print(np.isrealobj(w))                          # True
print(np.allclose(A_sym @ V, V @ np.diag(w), atol=1e-10))  # True
```

`eigh` returns orthonormal eigenvectors (`V.T @ V = I`) — the
basis every spectral method (PCA, spectral clustering, graph
Laplacians) builds on.

**Cost:** O(n³) for both `eig` and `eigh`; `eigh` wins on constant
factor and guaranteed real output.

---

### 8. Norms — measuring vectors and matrices

`np.linalg.norm` covers the everyday cases:

| Call | Meaning |
|---|---|
| `norm(x)` | L2 (Euclidean) for vectors; **Frobenius** for matrices — `sqrt(sum(x²))` |
| `norm(x, 1)` | L1 — `sum(|x|)` |
| `norm(x, np.inf)` | Infinity — `max(|x|)` |
| `norm(x, axis=1, keepdims=True)` | Row-wise norms, shape preserved |

```python
x = np.array([3.0, -4.0])
print(np.linalg.norm(x))                 # 5.0
print(np.linalg.norm(x, 1))              # 7.0
print(np.linalg.norm(x, np.inf))         # 4.0
```

The default for matrices is the Frobenius norm — the square root
of the sum of squared entries, *not* the induced 2-norm (largest
singular value). For `cond`-style analysis you need the latter,
which `np.linalg.cond` computes for you.

---

### 9. Condition number — how sensitive is your problem?

`np.linalg.cond(A)` = `s_max / s_min`. A large condition number
means small input perturbations become large output errors — the
system is *ill-conditioned*.

```python
def hilbert(n):
    i, j = np.indices((n, n))
    return 1.0 / (i + j + 1.0)

H6 = hilbert(6)
print(f"{np.linalg.cond(H6):.2e}")       # ~1.5e7 -- ill-conditioned
```

The bound: `||Δx||/||x|| ≤ cond(A) · ||Δb||/||b||`. Hilbert
matrices are the canonical ill-conditioned family — a `1e-8`
perturbation of `b` can produce a `~1e-1` error in `x`.

**Engineering consequences:** condition numbers are why you
*standardize features* (avoid huge scale ratios), why `float64`
matters for `solve` on near-singular systems, and why you should
check `cond` before trusting a solution — it is the cheapest
diagnostic in the toolbox (`O(n²)` once the SVD is done).

---

## Common Mistakes to Avoid

1. **`np.linalg.inv(A) @ b` instead of `np.linalg.solve`.** Same
   O(n³) class, worse stability, more rounding. Solve directly.
2. **SVD reconstruction shape bugs.** `full_matrices=True` gives
   square `U`/`Vh`; slice with `U[:, :s.size]` (or use
   `full_matrices=False`) before `@`.
3. **`np.dot` on 3-D arrays.** `dot` does not batch-broadcast;
   `matmul`/`@` does. On 2-D they look identical — the bug hides
   until your data gains a batch dimension.
4. **Forgetting `rcond=None`.** `lstsq` without it raises a
   `FutureWarning` about the rcond default and gives unstable
   results on rank-deficient data.
5. **`eig` on symmetric matrices.** It works but returns complex
   types; `eigh` is faster, real, and orthonormal.
6. **Ignoring the condition number.** A `solve` that returns
   *a* solution may be returning *nonsense*; check `cond` when
   values are large or features are unscaled.
7. **Cosine similarity without normalization.** `X @ X.T` is not
   cosine unless rows are unit-length. Normalize first (see
   Example 3 of the exercise).

---

## Best Practices

- **Use `@` for matmul everywhere**; reserve `np.dot` for
  explicit inner products where the 1-D semantics are intended.
- **Normalize embeddings before `X @ X.T`** — one line,
  `X / np.linalg.norm(X, axis=1, keepdims=True)`, and you have
  cosine similarities for the whole batch.
- **Use the singular-value spectrum** to choose `k` for
  low-rank compression: plot `s`, pick the elbow.
- **Check `np.linalg.cond(A)`** before trusting `solve` or `inv`
  output on real-world feature matrices.
- **Keep data in float64 for decompositions**; float32 SVDs lose
  orthogonality faster (precision budget applies — see NumPy 32).
- **Prefer `eigh` for symmetric problems** and
  `np.linalg.eigvalsh` when you only need eigenvalues.

---

## Complexity and Cost

| Operation | Cost | Memory | Notes |
|---|---|---|---|
| `a @ b` | O(m·k·n) | O(m·n) output | BLAS-optimized; batched via leading dims |
| `np.linalg.solve` | O(n³) | O(n²) | LU + pivoting; stable |
| `np.linalg.inv` | O(n³) | O(n²) | ~2× solve work; avoid |
| `np.linalg.lstsq` | O(m·n²) | O(m·n) | m ≥ n typical; returns rank |
| `np.linalg.qr` | O(m·n²) | O(m·n) | reduced mode default |
| `np.linalg.svd` | O(m·n²) | O(m·n) | full_matrices default; slice U |
| `np.linalg.eigh` | O(n³) | O(n²) | symmetric only; real output |
| `np.linalg.norm` | O(n) / O(m·n) | O(1) | Frobenius for matrices |
| `np.linalg.cond` | O(n³) | O(n²) | dominant cost is the SVD |

---

## AI Engineering Relevance

- **Forward passes** are batched matmuls: `X @ W + b` in one
  expression — the single most executed line in deep learning.
- **Embedding search (RAG, semantic search)** is normalized
  matmul: `Xn @ Xn.T` scores every pair of candidates at once;
  `argmax` selects the top hit.
- **Recommenders and feature fitting** are `lstsq` problems —
  including ridge regularization by row augmentation.
- **PCA / LSA / compression** are truncated SVDs; the spectrum
  tells you the effective rank of your feature matrix.
- **Numerical health checks** (`cond`) explain why feature
  scaling and dtype choice (NumPy 32) are load-bearing: a matrix
  with cond 1e12 turns float32 noise into garbage solutions.
- **Low-rank weight pruning** approximates trained matrices with
  `U_k diag(s_k) Vh_k` at a fraction of the parameter count —
  the Eckart-Young bound is the accuracy contract.

---

## Practice Exercises

1. Build a `(100, 64)` random embedding matrix; normalize rows;
   compute the full cosine matrix with one matmul; assert the
   diagonal is 1 and the matrix is symmetric.
2. Solve `A x = b` for a `(6, 6)` random matrix via `solve` and
   via `inv(A) @ b`; assert they agree to 1e-10 and note the
   extra cost of the second path.
3. Fit a degree-3 polynomial to `y = 1 + 2t + 3t² + 4t³ + noise`
   using a Vandermonde design matrix and `lstsq`; assert the
   recovered coefficients are within 0.1 of the truth.
4. Take a `(20, 20)` random matrix, compute its SVD, and print
   the rank-3 approximation error next to `sqrt(sum(s[3:]**2))`;
   confirm the Eckart-Young identity.
5. Build `hilbert(10)`, print its condition number, then solve
   `H x = 1` with a `1e-10` perturbation and observe the
   amplified relative error.

---

## Summary

- **Multiply** with `@`; batched matmul broadcasts leading
  dimensions; `dot` differs on 3-D.
- **Solve** with `np.linalg.solve`, never `inv`; use `lstsq` for
  rectangular/rank-deficient systems — it *is* linear regression.
- **Decompose** with QR (orthonormal basis) and SVD
  (reconstruction, low-rank, Eckart-Young error bounds).
- **Eigen-decompose** symmetric matrices with `eigh` for real,
  orthonormal results.
- **Measure** with norms (L1/L2/Linf/Frobenius) and the condition
  number; `cond = s_max/s_min` and bounds the error amplification.

## Quick Reference

```python
import numpy as np

# multiply
C = A @ B                      # (m,n) = (m,k) @ (k,n)
C = X @ W                      # batched: (B,m,k) @ (k,n) -> (B,m,n)

# solve / fit
x = np.linalg.solve(A, b)      # square full-rank only
coef, res, rank, s = np.linalg.lstsq(A, y, rcond=None)

# decompose
Q, R = np.linalg.qr(A)                    # A = Q R, Q.T Q = I
U, s, Vh = np.linalg.svd(A)               # A = (U[:, :s.size]*s) @ Vh
approx = (U[:, :k] * s[:k]) @ Vh[:k, :]   # rank-k best approximation

# eigen
w, V = np.linalg.eigh(A_sym)              # A V = V diag(w), V orthonormal

# measure
norm2 = np.linalg.norm(x)                 # L2 / Frobenius
cond = np.linalg.cond(A)                  # s_max / s_min
```

## Next Steps

- Apply matmul thinking in SciPy 14 (optimization) and SciPy 16
  (distance metrics for embeddings).
- Read NumPy 34 (advanced indexing) to combine `argpartition`
  top-k retrieval with cosine matmul for a full retriever.
- Experiment with `np.linalg.svd` on a real feature matrix and
  inspect its spectrum before building a pipeline on top.
