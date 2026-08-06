# Linear Algebra — Glossary 33

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `@` / `matmul` | Operator | Matrix product; broadcasts leading batch dims |
| `cond` | Function | Condition number: s_max / s_min, error amplification factor |
| `dot` | Function | Inner product on vectors; 2-D same as matmul, higher dims differ |
| `eigh` | Function | Eigen-decomposition specialized for symmetric matrices |
| Eigenvalue | Concept | Scalar λ with A v = λ v for nonzero v |
| Eigenvector | Concept | Direction preserved by A, scaled by λ |
| Frobenius norm | Concept | Matrix default norm: sqrt(sum of squared entries) |
| `inv` | Function | Matrix inverse; nearly always the wrong tool for solving |
| `lstsq` | Function | Least-squares solver: minimize ‖A x − b‖₂ |
| Low-rank approximation | Concept | Best rank-k fit from truncated SVD; error = tail singular values |
| LU factorization | Concept | PA = LU; the engine inside `solve` |
| Norm | Concept | Size of a vector/matrix: L1, L2, infinity, Frobenius |
| QR factorization | Concept | A = QR with orthonormal Q, triangular R |
| `rcond` | Parameter | Relative condition cutoff for `lstsq`; pass `None` |
| Singular value | Concept | Diagonal of the SVD; s[i] measures variance along mode i |
| `solve` | Function | Direct solver for A x = b, square full-rank |
| SVD | Concept | A = U diag(s) Vh; the fundamental matrix decomposition |
| Truncated SVD | Pattern | Keep top-k singular vectors for compression/PCA |

## Detailed Definitions

### `@` / `matmul`
**Definition**: The matrix-product operator. `(m, k) @ (k, n) →
(m, n)`; `(n,) @ (n,)` is a scalar inner product; leading
dimensions broadcast for batched work.

**Example**:
```python
import numpy as np

X = np.random.default_rng(0).normal(size=(5, 8, 4))
W = np.random.default_rng(1).normal(size=(4, 3))
print((X @ W).shape)          # (5, 8, 3)
```

**Complexity**: O(m·k·n), BLAS-accelerated.
**Related**: `dot`, Broadcasting

---

### `cond`
**Definition**: `np.linalg.cond(A)` = largest singular value
divided by smallest. Error amplification bound:
`‖Δx‖/‖x‖ ≤ cond(A) · ‖Δb‖/‖b‖`.

**Example**:
```python
import numpy as np

i, j = np.indices((6, 6))
H = 1.0 / (i + j + 1.0)               # Hilbert 6
print(f"{np.linalg.cond(H):.2e}")     # ~1.5e7
```

**Complexity**: O(n³) — dominated by the SVD.
**Related**: Singular value, SVD

---

### `dot`
**Definition**: `np.dot(a, b)` on 1-D arrays is the inner
product; on 2-D it matches `@`; on 3-D it sums over the last axis
of `a` and the second-to-last of `b` — no batch broadcasting.

**Example**:
```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
print(np.dot(a, a))           # 14.0 -- inner product
```

**Complexity**: same as `matmul` for 2-D.
**Related**: `@`/`matmul`

---

### `eigh`
**Definition**: Eigen-decomposition for symmetric/Hermitian
matrices: returns real eigenvalues `w` and orthonormal
eigenvectors `V` satisfying `A V = V diag(w)`.

**Example**:
```python
import numpy as np

rng = np.random.default_rng(42)
S = rng.normal(size=(5, 5))
S = S + S.T
w, V = np.linalg.eigh(S)
print(np.isrealobj(w))                          # True
print(np.allclose(S @ V, V @ np.diag(w), atol=1e-10))  # True
```

**Complexity**: O(n³).
**Related**: Eigenvalue, Eigenvector

---

### Eigenvalue
**Definition**: A scalar λ such that `A v = λ v` for some nonzero
vector v. For symmetric matrices all eigenvalues are real.

**Example**:
```python
import numpy as np

D = np.diag([1.0, 2.0, 3.0])
print(np.linalg.eigvalsh(D))    # [1. 2. 3.]
```

**Complexity**: —.
**Related**: `eigh`, Eigenvector

---

### Eigenvector
**Definition**: A nonzero vector whose direction is preserved by
A, scaled by its eigenvalue. `eigh` returns them orthonormal.

**Example**:
```python
import numpy as np

S = np.diag([2.0, 5.0])
w, V = np.linalg.eigh(S)
print(V)                        # identity: standard basis
print(np.allclose(S @ V, V @ np.diag(w)))   # True
```

**Complexity**: —.
**Related**: Eigenvalue, `eigh`

---

### Frobenius norm
**Definition**: The default matrix norm in `np.linalg.norm`:
sqrt of the sum of squared entries. Measures the "size" of the
whole matrix; equals sqrt(sum of squared singular values).

**Example**:
```python
import numpy as np

M = np.array([[1.0, 2.0], [3.0, 4.0]])
print(np.linalg.norm(M))                # sqrt(30)
print(np.allclose(np.linalg.norm(M), np.sqrt(np.sum(M ** 2))))  # True
```

**Complexity**: O(m·n).
**Related**: Norm, Singular value

---

### `inv`
**Definition**: `np.linalg.inv(A)` computes the matrix inverse.
Numerically the inversion-plus-multiply path `inv(A) @ b` is
slower and less stable than `solve(A, b)` — invert only when the
inverse itself is the output you need.

**Example**:
```python
import numpy as np

A = np.random.default_rng(0).normal(size=(3, 3))
print(np.allclose(A @ np.linalg.inv(A), np.eye(3), atol=1e-12))  # True
```

**Complexity**: O(n³).
**Related**: `solve`, LU factorization

---

### `lstsq`
**Definition**: `np.linalg.lstsq(A, b, rcond=None)` minimizes
‖A x − b‖₂ for possibly rectangular or rank-deficient A; returns
`(x, residuals, rank, singular_values)`. Linear regression in one
call.

**Example**:
```python
import numpy as np

rng = np.random.default_rng(1)
t = np.linspace(0.0, 1.0, 20)
A = np.column_stack([np.ones_like(t), t])
y = 3.0 + 2.0 * t + rng.normal(scale=0.05, size=t.size)
coef, *_ = np.linalg.lstsq(A, y, rcond=None)
print(np.round(coef, 4))       # ~[3.0, 2.0]
```

**Complexity**: O(m·n²) for m ≥ n.
**Related**: `rcond`, `solve`

---

### Low-rank approximation
**Definition**: The best rank-k fit to A, given by the truncated
SVD `U_k diag(s_k) Vh_k`. Eckart-Young: the Frobenius error
equals sqrt of the squared tail singular values.

**Example**:
```python
import numpy as np

A = np.random.default_rng(2).normal(size=(6, 5))
U, s, Vh = np.linalg.svd(A)
k = 2
approx = (U[:, :k] * s[:k]) @ Vh[:k, :]
print(np.allclose(np.linalg.norm(A - approx),
                  np.sqrt(np.sum(s[k:] ** 2)), rtol=1e-6))   # True
```

**Complexity**: SVD O(m·n²) + k·(m+n) storage for the factors.
**Related**: SVD, Truncated SVD

---

### LU factorization
**Definition**: PA = LU with L unit-lower-triangular, U upper-
triangular, P a permutation. The engine inside `solve` and
`inv`; O(n³) with excellent stability due to pivoting.

**Example**:
```python
import numpy as np

from scipy.linalg import lu  # scipy exposes P, L, U separately

P, L, U = lu(np.array([[2.0, 1.0], [1.0, 3.0]]))
print(np.allclose(P @ L @ U, [[2.0, 1.0], [1.0, 3.0]]))  # True
```

**Complexity**: O(n³) factorization, O(n²) per solve.
**Related**: `solve`, `inv`

---

### Norm
**Definition**: A measure of vector/matrix size. L1 = sum|x|;
L2 = sqrt(sum x²); infinity = max|x|; Frobenius = the L2 of a
matrix flattened.

**Example**:
```python
import numpy as np

x = np.array([3.0, -4.0])
print(np.linalg.norm(x))          # 5.0
print(np.linalg.norm(x, 1))       # 7.0
print(np.linalg.norm(x, np.inf))  # 4.0
```

**Complexity**: O(n) per vector.
**Related**: Frobenius norm

---

### QR factorization
**Definition**: A = QR with Q orthonormal columns (Q.T Q = I) and
R upper triangular. The stable basis builder; underlies solve and
lstsq.

**Example**:
```python
import numpy as np

A = np.random.default_rng(3).normal(size=(6, 4))
Q, R = np.linalg.qr(A)
print(np.allclose(Q.T @ Q, np.eye(4), atol=1e-12))    # True
print(np.allclose(Q @ R, A, atol=1e-12))              # True
```

**Complexity**: O(m·n²).
**Related**: LU factorization, SVD

---

### `rcond`
**Definition**: The relative condition-number cutoff in `lstsq`;
singular values below `rcond * s_max` are treated as zero.
Always pass `rcond=None` (NumPy chooses a sane default) to avoid
the FutureWarning.

**Example**:
```python
import numpy as np

A = np.arange(12.0).reshape(6, 2)   # rank 2
b = np.ones(6)
x, res, rank, s = np.linalg.lstsq(A, b, rcond=None)
print(rank)                          # 2
```

**Complexity**: —.
**Related**: `lstsq`, `cond`

---

### Singular value
**Definition**: The diagonal entries of the SVD, sorted
descending. s[i] measures how much variance mode i carries; the
ratio s_max/s_min is the condition number.

**Example**:
```python
import numpy as np

A = np.random.default_rng(4).normal(size=(5, 3))
s = np.linalg.svd(A, compute_uv=False)
print(np.all(np.diff(s) <= 0))       # True -- descending
```

**Complexity**: SVD O(m·n²).
**Related**: SVD, `cond`

---

### `solve`
**Definition**: `np.linalg.solve(A, b)` solves A x = b for square
full-rank A via LU with pivoting — the stable, direct way to
solve. Raises `LinAlgError` on singular input.

**Example**:
```python
import numpy as np

rng = np.random.default_rng(5)
A = rng.normal(size=(4, 4))
x_true = rng.normal(size=4)
b = A @ x_true
print(np.allclose(np.linalg.solve(A, b), x_true, atol=1e-10))  # True
```

**Complexity**: O(n³).
**Related**: `inv`, `lstsq`, LU factorization

---

### SVD
**Definition**: The singular value decomposition
`A = U diag(s) Vh`. Exists for every matrix; U and Vh are
orthonormal; s contains the nonnegative singular values.

**Example**:
```python
import numpy as np

A = np.random.default_rng(6).normal(size=(6, 5))
U, s, Vh = np.linalg.svd(A)
recon = (U[:, :s.size] * s) @ Vh     # slice U to (6,5)
print(np.allclose(recon, A, atol=1e-12))   # True
```

**Complexity**: O(m·n²).
**Related**: Truncated SVD, Singular value, Low-rank approximation

---

### Truncated SVD
**Definition**: Keeping only the top-k singular vectors:
`A ≈ U_k diag(s_k) Vh_k`. The storage drops from m·n to
k·(m + n + 1) — the basis of PCA, LSA, and weight pruning.

**Example**:
```python
import numpy as np

A = np.random.default_rng(7).normal(size=(200, 50))
U, s, Vh = np.linalg.svd(A)
k = 10
params_full = A.size                 # 10000
params_rankk = 200 * k + k + k * 50  # 2510
print(params_rankk < params_full)    # True
```

**Complexity**: SVD dominates; storage k·(m+n).
**Related**: SVD, Low-rank approximation

## Key Concepts Summary

### The shape grammar
- `(m,k) @ (k,n) → (m,n)`; `(n,) @ (n,)` → scalar; leading dims broadcast.

### Solve, don't invert
- `solve` = LU + pivoting; `inv` = extra work, extra rounding.
- `lstsq` for rectangular/rank-deficient; always `rcond=None`.

### Decompositions as tools
- QR → orthonormal basis; SVD → spectrum, reconstruction, low-rank
  with Eckart-Young error; eigh → real spectrum for symmetric.

### Health checks
- `cond = s_max/s_min`; the amplification bound makes it the first
  diagnostic to run on real data.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Eckart-Young — ___
2. Condition number — ___
3. `lstsq` — ___
4. Frobenius norm — ___
5. `eigh` — ___
6. `rcond` — ___

**Answers:**
1. e, 2. b, 3. f, 4. a, 5. c, 6. d

a. sqrt of sum of squared entries — the matrix default norm
b. s_max / s_min — the error amplification factor
c. Symmetric-only eigen-decomposition with real, orthonormal output
d. Relative cutoff in `lstsq`; pass `None`
e. Rank-k truncation error equals the tail singular-value norm
f. Minimizes ‖A x − b‖₂ for rectangular or rank-deficient A

---

**Related docs:** [numpy.linalg](https://numpy.org/doc/stable/reference/routines.linalg.html) ·
[`np.linalg.svd`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html) ·
[Back to lecture](33-linear-algebra-lecture.md)
