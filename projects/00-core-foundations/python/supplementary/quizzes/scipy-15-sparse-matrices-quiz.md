# SciPy 15 — Sparse Matrices Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · 8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** You need to slice rows of a sparse matrix repeatedly.
Which format is the right one?

- A) `COO`
- B) `CSR`
- C) `CSC`
- D) `LIL` is the only row-slicing format

**E2 (code-output).** What prints?
```python
import numpy as np
from scipy import sparse as sp

coo = sp.coo_matrix((np.array([1.0, 0.0]),
                     (np.array([0, 1]), np.array([0, 1]))),
                    shape=(2, 2))
print(coo.nnz)
```

- A) `1`
- B) `2`
- C) `4`
- D) `0`

**E3.** Sparse storage is the right call when the matrix density
is roughly:

- A) above 50%
- B) below ~10%
- C) exactly 0%
- D) irrelevant — sparse is always faster

**E4 (code-output).** What prints?
```python
import numpy as np

dense = np.zeros((4000, 4000), dtype=np.float64)
print(dense.nbytes / 1e6)
```

- A) `16.0`
- B) `128.0`
- C) `4000.0`
- D) `64.0`

**E5.** `spsolve(A, b)` from `scipy.sparse.linalg`:

- A) solves `A x = b` without materializing `A` as dense
- B) converts `A` to dense and calls `np.linalg.solve`
- C) only works for diagonal matrices
- D) solves `A x = 0` only

**E6.** `TfidfVectorizer().fit_transform(docs)` returns:

- A) a pandas `DataFrame`
- B) a dense `numpy.ndarray`
- C) a `csr_matrix`
- D) a Python `dict` of term frequencies

---

## Medium

**M1 (code-output).** What prints?
```python
import numpy as np
from scipy import sparse as sp

A = sp.eye(3, format="csr")
v = np.ones(3)
r = A @ v
print(type(r).__name__, r.ndim)
```

- A) `matrix 2`
- B) `ndarray 1`
- C) `csr_matrix 2`
- D) `ndarray 2`

**M2 (code-output).** What happens?
```python
import numpy as np
from scipy import sparse as sp

A = sp.coo_matrix((np.array([1.0, 0.0, 2.0]),
                   (np.array([0, 1, 2]), np.array([0, 1, 2]))),
                  shape=(3, 3)).tocsr()
print(A.eliminate_zeros().nnz)
```

- A) prints `2`
- B) prints `3`
- C) raises `AttributeError` — `eliminate_zeros()` returns `None`
- D) prints `9`

**M3.** A CSR matrix with `nnz = 100_000` and 10 000 rows
(float64 values, int32 indices) costs approximately:

- A) 100 KB
- B) 1.2 MB (`nnz × (8 + 4)` + pointer array)
- C) 10 MB
- D) 800 MB (`100 000 × 8` only)

**M4 (code-output).** What prints?
```python
import numpy as np
from scipy import sparse as sp

X = sp.random(50, 40, density=0.1, format="csr", random_state=0,
              data_rvs=lambda k: np.random.default_rng(1).uniform(0.1, 1.0, size=k))
l2 = np.asarray(X.power(2).sum(axis=1)).ravel() ** 0.5
Xn = sp.diags(1.0 / l2) @ X
print(Xn.nnz == X.nnz)
```

- A) `True` — diagonal scaling preserves the structure
- B) `False` — normalization always densifies
- C) `True`, but only because the matrix is square
- D) raises `ValueError` — `sp.diags` needs a 1-D input

**M5.** `X.sum(axis=1)` on a CSR matrix returns:

- A) a 1-D `ndarray`
- B) a 2-D matrix-like result — flatten with
  `np.asarray(...).ravel()` before dividing or building `sp.diags`
- C) a Python `float`
- D) a CSR row vector

**M6 (code-output).** In scipy 1.16, what happens?
```python
from scipy import sparse as sp

rng = np.random.default_rng(0)
A = sp.random(10, 10, density=0.1, format="csr",
              random_state=0, data_rvs=rng.uniform)
print(A.nnz)
```

- A) prints `10`
- B) raises `ValueError` — `data_rvs` receives `size` positionally,
  so `rng.uniform(size)` sets `low=size`
- C) prints `0`
- D) raises `TypeError` — `data_rvs` must be a string

**M7.** The correct way to L2-normalize the rows of a large CSR
matrix is:

- A) `X / np.asarray(X.sum(axis=1)).ravel()[:, None]`
- B) `sp.diags(1.0 / l2) @ X` with `l2` the row norms — stays
  sparse, `nnz` preserved
- C) `X.toarray()` then divide row-wise, then rebuild sparse
- D) `X.multiply(1.0 / l2)` — multiply always broadcasts 1-D

**M8 (code-output).** What prints?
```python
import numpy as np
from scipy import sparse as sp

A = sp.random(4, 3, density=0.5, format="csr", random_state=0,
              data_rvs=lambda k: np.random.default_rng(0).uniform(0.0, 1.0, size=k))
D = np.ones((3, 2))
print(type(A @ D).__name__)
```

- A) `csr_matrix`
- B) `ndarray`
- C) `coo_matrix`
- D) `csc_matrix`

**M9.** Why can you pass the `TfidfVectorizer` output straight
into `LogisticRegression`?

- A) sklearn estimators detect `csr_matrix` and dispatch to
  sparse algorithms — no dense conversion
- B) sklearn converts it to dense automatically (safe for small
  corpora only)
- C) it is actually a dense matrix in disguise
- D) logistic regression ignores the matrix entirely

---

## Hard

**H1.** A document-term matrix for 1M documents and a 50k-term
vocabulary, stored dense as float64, costs:

- A) 400 GB
- B) 4 GB
- C) 40 GB
- D) 4 TB

**H2 (code-output).** What prints?
```python
from scipy import sparse as sp

A = sp.eye(3, format="csr")
B = sp.eye(3, format="csc")
C = A @ B
print(type(C).__name__, C.nnz)
```

- A) `csr_matrix 3`
- B) `csc_matrix 3`
- C) `ndarray 9`
- D) `csr_matrix 9`

**H3.** A 5000 × 5000 tridiagonal solve with `spsolve` compared
with dense `np.linalg.solve`:

- A) both need ~200 MB for the matrix
- B) sparse needs ~240 KB of storage (`3·n·16 B`) and solves far
  below the dense O(n³); dense would need 200 MB
- C) sparse is only valid for n < 1000
- D) `spsolve` requires `A` to be symmetric positive definite

**H4.** In a retrieval pipeline over a 2000 × 5000 TF-IDF matrix
(80 MB dense), a `tracemalloc` guard with `peak < 10 MB` will
fail if the code:

- A) calls `X.toarray()` anywhere on the corpus matrix
- B) uses `sp.diags` for row scaling
- C) transforms the query with the fitted vectorizer
- D) converts `X` to CSC once

**H5 (code-output).** What prints?
```python
import numpy as np

sim = np.array([0.2, 0.9, 0.5])
print(np.argsort(sim)[::-1])
```

- A) `[0 1 2]`
- B) `[1 2 0]`
- C) `[2 1 0]`
- D) `[0 2 1]`

---

## Answer Key

**E1. B — CSR.**
CSR stores row pointers, so `getrow(i)` is cheap; CSC stores
column pointers for cheap `getcol`. COO is for building. LIL is
legacy and slower for arithmetic.
*Distractors:* A (build-only), C (column access), D (LIL is not
the only option and is rarely the answer).

**E2. B — `2`.**
`nnz` counts *stored entries*, not logical nonzeros: the explicit
`0.0` is stored until `eliminate_zeros()` runs.
*Distractors:* A ignores the stored zero; C is the number of
cells; D confuses "all zeros" with "stored zeros".

**E3. B — below ~10%.**
Sparse wins when `nnz/(rows×cols)` is small; the break-even for
float64 is around 2 stored values per row (≈ a few percent). D
is wrong: sparse has overhead (indices/pointers) and can be
slower than dense SIMD matmul on high density.

**E4. B — `128.0`.**
`4000 × 4000 = 16e6` cells × 8 bytes = 128 MB — spent even
though every entry is zero. This is the case for sparse storage.
*Distractors:* A counts rows only; C is the dimension; D is the
float32 cost.

**E5. A — solves without densifying.**
`spsolve` uses sparse direct methods (SuperLU) on the stored
nonzeros. B is exactly what sparse solves avoid; C/D invent
restrictions.

**E6. C — a `csr_matrix`.**
Text vectorizers emit CSR by construction. Dense (B) is the
400 GB mistake at scale; the matrix is consumed by sklearn
directly.

**M1. B — `ndarray 1`.**
`sparse @ ndarray` returns a 1-D `ndarray`. The result type
follows the right operand: dense in, dense out (1-D here).
*Distractors:* A/C are sparse-shaped; D is wrong on ndim.

**M2. C — `AttributeError`.**
`eliminate_zeros()` modifies in place and returns `None`, so
chaining `.nnz` fails — a classic sparse bug.
*Distractors:* A (the correct *concept* — after the call nnz
would be 2 — but the chain itself crashes), B/D ignore the
in-place contract.

**M3. B — ~1.2 MB.**
`nnz × (8 B data + 4 B index)` = 1.2 MB for the values+indices,
plus the 10 001-entry pointer array (~40 KB). A forgets the
index; D counts only values; C is 10× too high.

**M4. A — `True`.**
Left-multiplying by a diagonal only rescales the stored values —
`nnz` and structure are untouched. This is the sparse-friendly
normalization.
*Distractors:* B is the antipattern (`.toarray()` densifies);
C invents a square-matrix condition; D is wrong — `l2` is
already 1-D.

**M5. B — a 2-D matrix-like result.**
Sparse reductions keep a 2-D shape for axis semantics; flatten
with `np.asarray(...).ravel()` before `sp.diags` or broadcast
division. A/C/D are the shapes people *assume*.
*Distractors:* A is the NumPy behavior, not SciPy's; C/D make no
sense for a reduction.

**M6. B — raises `ValueError`.**
Since scipy ~1.15/1.16, `data_rvs` receives `size` positionally;
`rng.uniform(size)` binds it to `low`, producing `high − low < 0`.
Use `data_rvs=lambda k: rng.uniform(lo, hi, size=k)`.
*Distractors:* A/C assume it works; D mistakes the failure mode.

**M7. B — diagonal scaling.**
`sp.diags(1.0/l2) @ X` rescales stored values only. A's
broadcast division would attempt dense alignment; C densifies
(80 MB → OOM); D is wrong — sparse `.multiply` does not
broadcast a 1-D vector the way NumPy does.

**M8. B — `ndarray`.**
The right operand is dense, so the product is dense: the output
type follows the operand types. Sparse results (A/C/D) only
happen for sparse × sparse.
*Distractors:* A ignores the dense operand; C/D are other sparse
formats.

**M9. A — sklearn dispatches on sparse input.**
Estimators check for `csr_matrix` and use sparse-specific
solvers (e.g., liblinear). B is the OOM path; C/D are false.

**H1. A — 400 GB.**
`1e6 × 5e4 × 8 B = 4e11 B = 400 GB`. This is the canonical
"TF-IDF must be sparse" number.
*Distractors:* B/C/D misplace the decimal.

**H2. A — `csr_matrix 3`.**
Mixed-format sparse products are legal; the result comes back
CSR with `nnz = 3` — only the three diagonal entries exist.
*Distractors:* B assumes the left format is kept (CSR wins as
the matmul format); C would mean densification; D miscounts.

**H3. B — ~240 KB vs 200 MB.**
`3n − 2` nonzeros × 16 B ≈ 240 KB, and sparse direct solves
scale with the structure, not the grid area. A is the dense
world; C/D invent restrictions — `spsolve` handles general
square sparse matrices.

**H4. A — densifying the corpus.**
`.toarray()` on the 2000 × 5000 matrix allocates 80 MB in one
call — far over the 10 MB guard. The other options are all
sparse-safe operations.
*Distractors:* B/C/D are the correct sparse pipeline steps.

**H5. B — `[1 2 0]`.**
`argsort` ascending gives `[0 2 1]`; reversing gives
`[1 2 0]` — the top similarity first. This is the retrieval
ranking idiom.
*Distractors:* A is ascending order; C is a full reverse of the
sorted array (would require `sim` sorted first); D is the
indices of a manually sorted version.
