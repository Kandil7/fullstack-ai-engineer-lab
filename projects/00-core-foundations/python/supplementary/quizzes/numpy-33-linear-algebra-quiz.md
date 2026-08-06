# NumPy 33 — Linear Algebra Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
import numpy as np
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
print(a @ b)
print((a @ b).shape)
```

- A) `32.0`, `(3,)`
- B) `32.0`, `()`
- C) `[4. 10. 18.]`, `(3,)`
- D) `32.0`, `(1,)`

**E2.** `A` is `(5, 3)` and `B` is `(3, 7)`. What is `(A @ B).shape`?

- A) `(5, 7)`
- B) `(3, 3)`
- C) `(7, 5)`
- D) `(5, 3)`

**E3 (code-output).** What prints?
```python
import numpy as np
x = np.array([3.0, -4.0])
print(np.linalg.norm(x))
print(np.linalg.norm(x, 1))
```

- A) `5.0`, `7.0`
- B) `5.0`, `1.0`
- C) `25.0`, `7.0`
- D) `5.0`, `-1.0`

**E4.** Which call solves `A x = b` most stably for a square full-rank `A`?

- A) `np.linalg.inv(A) @ b`
- B) `np.linalg.solve(A, b)`
- C) `np.linalg.det(A) * b`
- D) `np.linalg.svd(A)` then manual inversion

**E5.** `np.linalg.svd(M)` returns `U, s, Vh`. What do `U` and `Vh` have in common?

- A) Both are square
- B) Both have orthonormal columns/rows (`U.T @ U == I`, `Vh @ Vh.T == I`)
- C) Both contain the singular values on their diagonals
- D) Both are lower triangular

**E6 (code-output).** What prints?
```python
import numpy as np
M = np.array([[1.0, 2.0], [3.0, 4.0]])
print(np.linalg.norm(M))
```

- A) `5.477225575051661` (sqrt(30))
- B) `10.0`
- C) `5.0`
- D) `2.0`

---

## Medium

**M1 (code-output).** What prints?
```python
import numpy as np
X = np.random.default_rng(0).normal(size=(5, 8, 4))
W = np.random.default_rng(1).normal(size=(4, 3))
print((X @ W).shape)
print((X @ W.T).shape)
```

- A) `(5, 8, 3)`, `(5, 8, 3)`
- B) `(5, 8, 3)`, raises `ValueError`
- C) `(5, 8, 4)`, `(5, 8, 4)`
- D) `(40, 3)`, `(40, 3)`

**M2.** Why is `np.linalg.inv(A) @ b` worse than `np.linalg.solve(A, b)`?

- A) `inv` is O(n⁴); `solve` is O(n³)
- B) `inv` does more work and more rounding; `solve` solves directly via LU
- C) `inv` only works for symmetric matrices
- D) There is no difference; they are identical

**M3 (code-output).** What prints?
```python
import numpy as np
A = np.random.default_rng(42).normal(size=(6, 5))
U, s, Vh = np.linalg.svd(A)
recon = (U[:, :s.size] * s) @ Vh
print(np.allclose(recon, A, atol=1e-12))
print(U.shape, Vh.shape)
```

- A) `True`, `(6, 6)`, `(5, 5)`
- B) `True`, `(6, 5)`, `(5, 5)`
- C) `False`, `(6, 6)`, `(5, 5)`
- D) `True`, `(6, 6)`, `(6, 5)`

**M4.** The Eckart-Young error of the rank-k SVD approximation is:

- A) `s[k]` — the next singular value
- B) `sqrt(sum(s[k:]**2))` — the tail singular-value norm
- C) `s[0] - s[k]` — the spectrum width
- D) `k * s[-1]` — k times the smallest singular value

**M5 (code-output).** What prints?
```python
import numpy as np
A = np.random.default_rng(1).normal(size=(6, 4))
Q, R = np.linalg.qr(A)
print(np.allclose(Q.T @ Q, np.eye(4), atol=1e-12))
print(np.allclose(Q @ R, A, atol=1e-12))
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**M6.** For which matrix does `np.linalg.eigh` give the guarantee that `eig` does not?

- A) Any non-symmetric matrix — eigenvalues are always real
- B) A symmetric matrix — real eigenvalues and orthonormal eigenvectors
- C) Any matrix — `eigh` and `eig` are identical
- D) A singular matrix — `eigh` returns the null space

**M7 (code-output).** What prints?
```python
import numpy as np
rng = np.random.default_rng(3)
S = rng.normal(size=(5, 5))
S = S + S.T
w, V = np.linalg.eigh(S)
print(np.isrealobj(w))
print(np.allclose(S @ V, V @ np.diag(w), atol=1e-10))
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**M8.** `np.linalg.lstsq(A, y, rcond=None)` returns 4 values. Which is the rank?

- A) `x` — the solution
- B) `residuals` — the squared errors
- C) the third value, `rank`
- D) `s` — the singular values

**M9.** You need cosine similarity between every pair of 10,000 rows of a `(10000, 128)` embedding matrix. What is the memory-bounded, single-expression approach?

- A) `np.linalg.norm(X @ X.T)` — normalize the product
- B) `X / np.linalg.norm(X, axis=1, keepdims=True)` then `@` — normalize rows, then one matmul
- C) `X @ X.T / 128` — divide by the dimension
- D) `np.corrcoef(X)` — correlation is identical to cosine

---

## Hard

**H1 (code-output).** What prints?
```python
import numpy as np
rng = np.random.default_rng(9)
A = rng.normal(size=(7, 4))
U, s, Vh = np.linalg.svd(A)
k = 3
approx = (U[:, :k] * s[:k]) @ Vh[:k, :]
print(np.allclose(np.linalg.norm(A - approx),
                  np.sqrt(np.sum(s[k:] ** 2)), rtol=1e-6))
print(np.linalg.norm(A - approx) <= np.linalg.norm(A - (U[:, :1] * s[:1]) @ Vh[:1, :]))
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**H2.** `H` is the 10×10 Hilbert matrix. `np.linalg.cond(H)` ≈ 1.6e13. A service solves `H x = b` in float32. Which statement is correct?

- A) float32 is fine — `solve` is always accurate to machine epsilon
- B) The condition number predicts up to ~1e13× relative error amplification; float32's ~1e-7 precision can produce garbage. Check `cond`, and use float64 or regularization
- C) The condition number only matters for `inv`, not for `solve`
- D) Hilbert matrices are symmetric, so `eigh` fixes the conditioning

**H3 (code-output).** What prints?
```python
import numpy as np
i, j = np.indices((6, 6))
H = 1.0 / (i + j + 1.0)
print(f"{np.linalg.cond(H):.1e}")
b = np.ones(6)
x = np.linalg.solve(H, b)
print(np.allclose(H @ x, b, atol=1e-6))
```

- A) `1.5e+07`, `True`
- B) `1.5e+07`, `False`
- C) `6.0e+00`, `True`
- D) `1.5e+07`, raises `LinAlgError`

**H4.** You fit a polynomial of degree 7 to 100 noisy points with `lstsq` and get a huge coefficient vector. The correct diagnosis is:

- A) `lstsq` is buggy — use `np.linalg.solve` on the normal equations instead
- B) High-degree polynomial fitting on noisy data is ill-conditioned; check the design matrix's condition number and prefer lower degrees or regularization
- C) The noise is the problem — remove outliers, then refit
- D) `rcond` must be set to 1e-3 to fix instability

**H5.** A `(2000, 128)` float32 embedding matrix is normalized and multiplied by its transpose for cosine retrieval, producing a `(2000, 2000)` result. The matmul needs ~32 MB for the output. Which statement about memory is true?

- A) The output dominates: the result is O(n²) while the input is O(n·d); budget for the result, not the input
- B) Memory is irrelevant — BLAS handles it
- C) The input dominates because 2000·128 > 2000·2000
- D) Cosine matrices are always computed in place with zero extra memory

---

## Answer Key

**E1 — B.** `(n,) @ (n,)` is a scalar inner product: 1·4+2·5+3·6 = 32.0, shape `()`.
*Distractors:* A keeps the vector shape (that's element-wise `*`); C is element-wise multiplication; D invents a `(1,)` broadcast shape.

**E2 — A.** Inner dims (3, 3) contract; result is `(5, 7)`.
*Distractors:* B transposes the rule; C swaps the output dims; D is the input shape.

**E3 — A.** L2 = sqrt(9+16) = 5; L1 = 3+4 = 7.
*Distractors:* B is L1 misread as `sum(x)`; C squares the L2; D misreads `|x|`.

**E4 — B.** `solve` is the direct, stable LU-based path.
*Distractors:* A does extra inverse work with more rounding; C is the determinant (a scalar!) — nonsense; D is an SVD-pseudoinverse: works but is overkill and slower for square full-rank.

**E5 — B.** U has orthonormal columns, Vh orthonormal rows: `U.T @ U == I`, `Vh @ Vh.T == I`.
*Distractors:* A is true only for square matrices; C describes `diag(s)`; D describes R from QR.

**E6 — A.** Default matrix norm is Frobenius: sqrt(1+4+9+16) = sqrt(30).
*Distractors:* B sums entries; C is the L2 of the first row; D is the max singular value of the 2×2 (s_max = 5.46, s_min = 0.37 → s_max/s_min… no — 2.0 is cond, not a norm).

**M1 — B.** `(5, 8, 4) @ (4, 3)` → `(5, 8, 3)`; then `W.T` is `(3, 4)` — inner dims 8 vs 4 mismatch → `ValueError`.
*Distractors:* A assumes W.T also fits; C confuses input dims with output; D flattens the batch (matmul keeps it).

**M2 — B.** Both O(n³); `inv` solves twice plus pivoting overhead, adding rounding.
*Distractors:* A is wrong on cost; C is false (inv works generally); D is false — `solve` is measurably more stable.

**M3 — A.** With `full_matrices=True`, U is `(6, 6)`, Vh `(5, 5)`; slicing `U[:, :s.size]` restores the reconstruction.
*Distractors:* B is the reduced-mode shape; C claims reconstruction fails (it doesn't); D swaps Vh's shape.

**M4 — B.** Eckart-Young: the rank-k error in Frobenius norm equals the tail's squared-sum root.
*Distractors:* A is the marginal singular value, not the error; C/D have no basis in the theorem.

**M5 — A.** QR guarantees Q orthonormal and Q R == A (reduced mode: Q is `(6, 4)`).
*Distractors:* B/C/D break one or both invariants.

**M6 — B.** `eigh` is specialized: real eigenvalues and orthonormal eigenvectors, guaranteed, for symmetric/Hermitian input.
*Distractors:* A is false (non-symmetric can have complex eigenvalues); C is false (different algorithms, different guarantees); D is false (singularity is unrelated).

**M7 — A.** Symmetric input → `eigh` returns real w and V satisfying A V = V diag(w).
*Distractors:* B/C/D break the two invariants that `eigh` guarantees.

**M8 — C.** `lstsq` returns `(x, residuals, rank, s)` — the third element is the rank.
*Distractors:* A is the solution; B is residuals; D is singular values. (The `*_rest` unpacking in the exercise shows the same order.)

**M9 — B.** Normalize rows (unit L2), then one matmul — cosine in a single BLAS call.
*Distractors:* A normalizes the *product* (nonsense — it's already a scalar-ish matrix norm); C divides by dimension (not a normalization); D `corrcoef` is *centered* correlation — different from cosine (and it internally mean-centers).

**H1 — A.** Eckart-Young holds (True), and rank-3 error ≤ rank-1 error (True) — more singular vectors never hurt.
*Distractors:* B/C/D break the theorem or the monotonicity of approximation error with rank.

**H2 — B.** cond 1.6e13 means relative errors can be amplified by that factor; float32's ~1e-7 relative precision leaves essentially no correct digits. The bound is worst-case, but the risk is real — check `cond`, prefer float64, or regularize.
*Distractors:* A ignores conditioning entirely; C is false (solve is exactly the code path that suffers); D confuses symmetric eigen-structure with conditioning.

**H3 — A.** Hilbert-6 cond ≈ 1.5e7; `solve` still returns a solution with a small residual (the *forward* error is small; the *backward* error is what's stable).
*Distractors:* B claims the residual check fails (it doesn't at 1e-6); C is a nonsense small cond; D is false — Hilbert matrices are full-rank.

**H4 — B.** High-degree Vandermonde systems are ill-conditioned (cond grows exponentially with degree); the huge coefficients are the symptom. The fix is fewer degrees or regularization — not the normal equations, which are *worse* conditioned than `lstsq`.
*Distractors:* A recommends the numerically weaker path; C is a different problem; D misuses `rcond` (it's a rank cutoff, not a fix for bad conditioning).

**H5 — A.** The output is O(n²) = 4M entries = 32 MB float64 (or 16 MB float32) vs an O(n·d) input. Budget the result; chunked or approximate approaches exist when n is huge.
*Distractors:* B is never true; C compares the wrong sizes (n·d = 256K vs n² = 4M); D is false — matmul allocates the output plus BLAS workspace.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 33](03-libraries/numpy/lectures/33-linear-algebra-lecture.md) ·
[Glossary 33](03-libraries/numpy/lectures/33-linear-algebra-glossary.md) ·
[Challenge 33](03-libraries/numpy/challenges/33-linear-algebra/README.md)
