# SciPy 15 — Sparse Matrices

## Topic Overview

Sparse matrices store only the nonzero entries of a matrix —
the standard representation for TF-IDF document matrices,
adjacency matrices, and interaction matrices. This lecture covers
the three core formats (COO, CSR, CSC), when sparse beats dense,
sparse matmul and sparse linear solves, memory accounting, and
the handoff from `scipy.sparse` to sklearn.

## Learning Objectives

By the end you can:

1. Build a sparse matrix from COO triplets and convert between
   COO, CSR, and CSC.
2. Explain when sparse storage wins (density < ~10%) and measure
   the memory difference.
3. Multiply sparse with sparse and sparse with dense correctly.
4. Solve large sparse linear systems with `spsolve`.
5. Recognize that TF-IDF matrices are sparse and feed them to
   sklearn estimators unchanged.
6. Normalize rows of a sparse matrix without ever densifying it.

## Prerequisites

- NumPy arrays and matrix multiplication (topic 33 linear algebra).
- The concept of a vectorized operation (topic 30 vectorization).
- Basic understanding of TF-IDF text features (see `numpy`/`sklearn`
  topics in phase 3).

## Key Concepts

### 1. What a sparse matrix is

A matrix where the vast majority of entries are zero, stored as:

- `data` — the nonzero values,
- `indices` — where they live,
- `shape` — the logical dimensions.

The number of stored entries is `nnz`. A matrix is worth storing
sparsely when the density `nnz / (rows × cols)` is low — in
practice under ~10%, often under 1%.

```python
from scipy import sparse as sp
import numpy as np

coo = sp.coo_matrix(
    (np.array([1.0, 2.0, 3.0]),          # data
     (np.array([0, 1, 2]),               # row indices
      np.array([0, 1, 2]))),             # column indices
    shape=(3, 3))
print(coo.nnz, coo.shape)                # 3 (3, 3)
```

**Critical detail:** COO stores *triplets as given*. An explicit
`0.0` in the data counts toward `nnz`, and duplicate coordinates
are summed only when converting to CSR/CSC. Call
`eliminate_zeros()` to drop stored zeros.

### 2. The three formats

| Format | Layout | Best for |
|---|---|---|
| COO | raw `(row, col, value)` triplets | building matrices |
| CSR | compressed **row** pointers | row slicing, matmul, sklearn |
| CSC | compressed **column** pointers | column slicing, column ops |

CSR is the workhorse: it is what sklearn and most solvers want.
Access `A.getrow(i)` cheaply on CSR; `A.getcol(j)` cheaply on
CSC. Convert once — conversions copy the whole structure.

```python
csr = coo.tocsr()
csc = coo.tocsc()
```

### 3. When sparse wins — measured

For `n = 4000` (4000 × 4000 = 16M cells):

- dense `float64`: `16e6 × 8 B = 128 MB`, always, even if 99.5%
  of it is zero;
- sparse at 0.5% density (`nnz = 80_000`): `data (8 B) +
  indices (4 B) + indptr (4 B)` per entry ≈ 0.98 MB — **131×
  smaller**.

Sparse storage costs roughly `nnz × 16 B` (value + index), so the
break-even density against dense `float64` is around
`16 / 8 = 2` nonzero entries per row — far lower than people
guess. Dense `float32` storage halves the dense cost but does not
change the sparse math.

### 4. Sparse matrix multiplication

The `@` operator respects the operands' types:

```python
C = A_csr @ B_csr     # sparse @ sparse -> sparse
r = A_csr @ v         # sparse @ ndarray -> 1-D ndarray
D = A_csr @ dense     # sparse @ dense  -> dense ndarray
```

Mixing types densifies the result — often exactly what you do
*not* want at scale. Keep both sides sparse when the result will
be consumed by another sparse operation (chained matmul, solver).

### 5. Sparse linear algebra

`spsolve(A, b)` solves `A x = b` without materializing `A` dense:

```python
from scipy.sparse.linalg import spsolve

A = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(2000, 2000),
             format="csr")
x = spsolve(A, np.ones(2000))
```

The same system dense would be 32 MB for `float64`; the sparse
tridiagonal is ~90 KB. Residual `|A x − b|` lands at 1e-10.

### 6. TF-IDF matrices are sparse

A document-term TF-IDF matrix has shape `n_docs × n_vocab` — and
each document touches only a handful of the tens of thousands of
vocabulary terms. `TfidfVectorizer` returns a `csr_matrix`:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X = TfidfVectorizer().fit_transform(docs)   # csr_matrix
clf = LogisticRegression().fit(X, y)        # sklearn accepts sparse
```

At 1M documents × 50k terms, dense `float64` would be 400 GB.
Sparse keeps it at a few GB — this is why every text-ML pipeline
is sparse end to end.

### 7. Sparse-friendly row operations

Never call `.toarray()` just to rescale rows. Row-normalize
embeddings-style (unit L2) with a diagonal scaling:

```python
l2 = np.asarray(X.power(2).sum(axis=1)).ravel() ** 0.5
Xn = sp.diags(1.0 / l2) @ X          # sparse, nnz preserved
```

Row L2 norms of `Xn` are now 1 and the matrix is still sparse.

## Common Mistakes

1. **Calling `.toarray()` / `.todense()` at scale.** Densifying a
   1M × 50k TF-IDF matrix is a 400 GB OOM. Stay sparse.
2. **Forgetting that COO keeps duplicates and explicit zeros.**
   `nnz` counts raw triplets; convert and call
   `eliminate_zeros()` before trusting sizes.
3. **Mixing sparse and dense in `@`.** The result becomes dense
   silently; a later `sparse @ dense @ dense` chain stays dense.
4. **Assuming sparse indexing is always cheap.** Random element
   access `A[i, j]` on CSR is O(log) at best and can be O(nnz);
   slice along the format's axis (`getrow` on CSR, `getcol` on
   CSC).
5. **Using `sum(axis=1)` output without `np.asarray(...).ravel()`.**
   Sparse reductions return a 2-D matrix-like object; flatten
   before dividing or passing to `sp.diags`.
6. **Measuring the wrong thing.** Compare `dense.nbytes` against
   `data.nbytes + indices.nbytes + indptr.nbytes` — not against
   the Python object overhead.

## Best Practices

- Build with COO, then convert to CSR once; never build CSR by
  repeated insertion.
- Check `density = nnz / (rows × cols)` before choosing a
  representation; sparse below ~10%, dense above.
- Keep `@` operands both sparse when the pipeline continues
  sparse; densify only at the very end if a dense consumer
  requires it.
- Prefer `spsolve` over `np.linalg.solve` when `n > ~1000` and
  the matrix is sparse.
- Pass CSR matrices directly to sklearn estimators; they dispatch
  to sparse algorithms automatically.

## Complexity / Cost

| Operation | Dense | Sparse (nnz) |
|---|---|---|
| store | O(rows × cols) | O(nnz) |
| matmul C = A@B | O(n³) | O(nnz(A) × nnz_per_row(B)) |
| row L2 + scale | O(n²) | O(nnz) |
| solve (direct) | O(n³) | O(nnz^1.5) typical |

Sparse `@` cost scales with the *number of nonzeros*, not the
grid area — the reason 400 GB dense workloads run in GB of RAM.

## AI Engineering Relevance

- **RAG/IR:** TF-IDF and BM25 document matrices are sparse; the
  retrieval layer over millions of documents starts here.
- **Graph ML:** adjacency matrices are sparse by definition;
  GNN message passing is sparse matmul.
- **Recommendations:** user × item interaction matrices are >99%
  empty — the input to matrix factorization is sparse.
- **NLP pipelines:** vocab is 10⁴–10⁵ terms; dense one-hots are
  not an option.
- **Model serving:** sparse feature vectors shrink request
  payloads and inference memory by orders of magnitude.

## Practice Exercises

1. Build a 1000 × 1000 matrix with 5000 random entries via COO,
   convert to CSR, and report `nnz`, density, and storage bytes
   (value + index + ptr).
2. Row-slice a CSR matrix 100 times and time it against the same
   slicing on the CSC version; explain the difference.
3. Construct a tridiagonal Laplacian of size 5000, solve
   `(L + I) x = b` with `spsolve`, and check the residual.
4. Vectorize `TfidfVectorizer` on a corpus of 50 toy documents,
   print the density, fit a `LogisticRegression`, and normalize
   the matrix rows to unit L2 without densifying.
5. Compute `A @ A` for a 0.1%-dense 2000 × 2000 matrix both
   sparse and (on a 200 × 200 slice) dense; compare the `nnz` of
   the sparse product with the square of the input `nnz`.

## Summary

- Sparse = store only nonzeros: `data + indices + shape`, cost
  O(nnz) instead of O(rows × cols).
- COO builds, CSR reads rows / matmuls / sklearn, CSC reads
  columns — convert once, slice along the axis.
- Sparse wins below ~10% density; measure `data + indices +
  indptr` bytes against `dense.nbytes`.
- `spsolve` solves large systems without densifying.
- TF-IDF is the canonical sparse matrix in ML; keep it sparse
  from vectorizer to estimator, and normalize rows with a
  diagonal multiply, never `.toarray()`.

## Quick Reference

```python
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve

coo  = sp.coo_matrix((data, (rows, cols)), shape=(m, n))
csr  = coo.tocsr();  csc = coo.tocsc()
A.nnz, A.shape, A.density if hasattr(A, "density") else A.nnz / (m * n)
A.toarray()                       # ONLY for small matrices
C = A_csr @ B_csr                 # stays sparse
v = A_csr @ np.ones(n)            # 1-D ndarray
x = spsolve(A_csr, b)             # sparse solve
Xn = sp.diags(1.0 / l2) @ X       # row scaling, stays sparse
X = TfidfVectorizer().fit_transform(docs)   # csr_matrix
clf.fit(X, y)                     # sklearn accepts sparse
```

## Next Steps

- Topic 16: distance and similarity (`cdist`/`pdist`, cosine vs
  euclidean, why cosine for embeddings) — the retrieval half of
  RAG, which consumes exactly the sparse matrices from this topic.
- sklearn feature extraction and pipelines: `TfidfVectorizer`,
  `HashingVectorizer`, `ColumnTransformer` over sparse inputs.
- Graph algorithms on adjacency matrices (`networkx` interop via
  `nx.from_scipy_sparse_array`).

**Related docs:** [scipy.sparse reference](https://docs.scipy.org/doc/scipy/reference/sparse.html) ·
[scipy.sparse.linalg](https://docs.scipy.org/doc/scipy/reference/sparse.linalg.html) ·
[Exercise](15-sparse-matrices.py) · [Glossary](15-sparse-matrices-glossary.md)
