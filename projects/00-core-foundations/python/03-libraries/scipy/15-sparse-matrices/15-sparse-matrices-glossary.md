# Sparse Matrices — Glossary 15

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `COO` | Format | Coordinate list: raw `(row, col, value)` triplets — the build format |
| `CSC` | Format | Compressed sparse **column**: cheap column access |
| `CSR` | Format | Compressed sparse **row**: row slicing, matmul, sklearn default |
| `data` | Field | The array of stored nonzero values |
| `density` | Metric | `nnz / (rows × cols)` — sparse wins below ~10% |
| `eliminate_zeros()` | Method | Drop stored zeros; in-place, returns `None` |
| `getcol(j)` | Method | Cheap column extraction on CSC |
| `getrow(i)` | Method | Cheap row extraction on CSR |
| `indices` | Field | Column (CSR) or row (CSC) positions of the nonzeros |
| `indptr` | Field | Row (CSR) or column (CSC) start pointers |
| `nnz` | Field | Number of stored entries (not logical cells) |
| `sp.diags` | Function | Build a diagonal matrix — the row-scaling trick |
| `sp.eye` | Function | Sparse identity matrix |
| `sp.random` | Function | Random sparse matrix with a target density |
| `spsolve` | Function | Direct solve of `A x = b` without densifying |
| `toarray()` | Method | Densify — only for small matrices |
| `tocsc()` / `tocsr()` | Method | Convert format (copies the whole structure) |
| `TfidfVectorizer` | Interop | sklearn text vectorizer returning `csr_matrix` |

## Detailed Definitions

### `COO`
**Definition**: Coordinate format — the human-readable build
format. Stores parallel arrays of row indices, column indices,
and values. Fast to build, useless for arithmetic until
converted.

**Example**:
```python
from scipy import sparse as sp
import numpy as np
coo = sp.coo_matrix((np.array([1.0, 2.0]),
                     (np.array([0, 1]), np.array([0, 1]))),
                    shape=(2, 2))
```

**Complexity**: O(nnz) to build; O(nnz) per conversion.
**Related**: `CSR`, `CSC`

---

### `CSC`
**Definition**: Compressed sparse column format: column pointers,
row indices, values. Column slicing is cheap; row slicing is not.

**Example**:
```python
csc = coo.tocsc()
col = csc.getcol(3)      # cheap
```

**Complexity**: O(nnz) storage; O(1)-ish column access.
**Related**: `CSR`, `COO`

---

### `CSR`
**Definition**: Compressed sparse row format: row pointers,
column indices, values. The workhorse — sklearn and most solvers
want CSR. Row slicing and matmul are cheap.

**Example**:
```python
csr = coo.tocsr()
row = csr.getrow(0)      # cheap
X = TfidfVectorizer().fit_transform(docs)   # csr_matrix
```

**Complexity**: O(nnz) storage; O(1)-ish row access.
**Related**: `CSC`, `COO`

---

### `data`
**Definition**: The 1-D array of stored nonzero values in a
sparse matrix. Its byte count is part of the storage cost.

**Example**:
```python
print(csr.data[:5])      # first stored values
```

**Complexity**: O(nnz).
**Related**: `nnz`, `indices`, `indptr`

---

### `density`
**Definition**: The fraction of logical cells that are nonzero:
`nnz / (rows × cols)`. Below ~10% sparse storage wins; above that
dense is usually cheaper and faster.

**Example**:
```python
density = A.nnz / (A.shape[0] * A.shape[1])
```

**Complexity**: O(1).
**Related**: `nnz`

---

### `eliminate_zeros()`
**Definition**: Removes explicit stored zeros from a sparse
matrix. In-place — returns `None` (a common bug).

**Example**:
```python
csr.eliminate_zeros()          # NOT csr = csr.eliminate_zeros()
print(csr.nnz)
```

**Complexity**: O(nnz).
**Related**: `nnz`

---

### `getcol(j)`
**Definition**: Extract column `j` as a sparse matrix. Cheap on
CSC, expensive on CSR.

**Example**:
```python
col = A.tocsc().getcol(2)
```

**Complexity**: O(1)-ish on CSC.
**Related**: `getrow`, `CSC`

---

### `getrow(i)`
**Definition**: Extract row `i` as a sparse matrix. Cheap on CSR.

**Example**:
```python
row = A.tocsr().getrow(0)
```

**Complexity**: O(1)-ish on CSR.
**Related**: `getcol`, `CSR`

---

### `indices`
**Definition**: The 1-D array of column positions (CSR) or row
positions (CSC) for each stored value.

**Example**:
```python
print(csr.indices[:5])
```

**Complexity**: O(nnz).
**Related**: `indptr`, `data`

---

### `indptr`
**Definition**: The 1-D array of start offsets: row `i` occupies
`indices[indptr[i]:indptr[i+1]]`. This is what "compressed"
means — the grid is reconstructed from pointers, not stored.

**Example**:
```python
print(csr.indptr[:3])    # where each row starts
```

**Complexity**: O(rows + 1).
**Related**: `indices`, `data`

---

### `nnz`
**Definition**: The number of *stored* entries — not the number
of logically nonzero cells. COO counts raw triplets, including
duplicates and explicit zeros, until converted/cleaned.

**Example**:
```python
print(A.nnz)             # stored entries
```

**Complexity**: O(1).
**Related**: `density`, `eliminate_zeros`

---

### `sp.diags`
**Definition**: Build a sparse diagonal (or banded) matrix from a
1-D array. The key to row scaling: left-multiply by a diagonal.

**Example**:
```python
Xn = sp.diags(1.0 / l2) @ X     # rows of Xn have unit L2
```

**Complexity**: O(n).
**Related**: `sp.eye`

---

### `sp.eye`
**Definition**: Sparse identity matrix. Useful for adding a
regularization ridge `A + λI` without densifying.

**Example**:
```python
I = sp.eye(5, format="csr")
```

**Complexity**: O(n).
**Related**: `sp.diags`

---

### `sp.random`
**Definition**: Generate a random sparse matrix with a target
density. In scipy 1.16, `data_rvs` receives `size` positionally —
pass a callable `lambda k: rng.uniform(lo, hi, size=k)`.

**Example**:
```python
A = sp.random(100, 80, density=0.01, format="csr",
              random_state=42, data_rvs=lambda k: rng.uniform(size=k))
```

**Complexity**: O(nnz).
**Related**: `density`

---

### `spsolve`
**Definition**: `scipy.sparse.linalg.spsolve(A, b)` solves
`A x = b` using sparse direct methods, without ever building the
dense matrix.

**Example**:
```python
from scipy.sparse.linalg import spsolve
x = spsolve(A, b)
residual = np.max(np.abs(A @ x - b))      # ~1e-10
```

**Complexity**: superlinear in nnz, far below the dense O(n³).
**Related**: `spsolve` family in `sparse.linalg`

---

### `toarray()`
**Definition**: Densify the matrix into an `ndarray`. The
antipattern at scale: 1M × 50k TF-IDF → 400 GB. Only for small
matrices and debugging.

**Example**:
```python
small_dense = tiny_csr.toarray()
```

**Complexity**: O(rows × cols).
**Related**: `density`

---

### `tocsc()` / `tocsr()`
**Definition**: Convert formats. Copies the entire structure —
convert once, then stay in the format your access pattern needs.

**Example**:
```python
csc = csr.tocsc()      # one-time conversion
```

**Complexity**: O(nnz) copy.
**Related**: `CSR`, `CSC`

---

### `TfidfVectorizer`
**Definition**: sklearn's text → TF-IDF feature transformer.
Returns a `csr_matrix` — the canonical sparse matrix in ML — and
its output feeds estimators directly.

**Example**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
X = TfidfVectorizer().fit_transform(docs)   # csr_matrix
clf = LogisticRegression().fit(X, y)
```

**Complexity**: O(total token occurrences).
**Related**: `CSR`, `density`

## Key Concepts Summary

### Format choice
- COO to build → CSR to compute; CSC for column-oriented work.

### Storage cost
- Sparse ≈ `nnz × (8 B value + 4 B index)` + pointer array;
  break-even density ~10% against dense `float64`.

### Type discipline
- `sparse @ sparse → sparse`; `sparse @ ndarray → ndarray`;
  mixing densifies silently.

### Sparse recipes
- Row scaling: `sp.diags(1/l2) @ X` — never `.toarray()`.
- Solves: `spsolve`; ridge: `A + sp.eye(n)`.
- Text ML: keep `TfidfVectorizer` output sparse end to end.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `nnz` — ___
2. `CSR` — ___
3. `spsolve` — ___
4. `eliminate_zeros()` — ___
5. `density` — ___
6. `TfidfVectorizer` — ___

**Answers:**
1. c, 2. f, 3. a, 4. e, 5. b, 6. d

a. Sparse direct solve of A x = b without densifying
b. The fraction of cells that are nonzero — sparse wins below ~10%
c. Number of stored entries, including explicit zeros
d. sklearn text vectorizer returning a csr_matrix
e. In-place removal of stored zeros (returns None)
f. Compressed sparse row format — the sklearn/solver workhorse

---

**Related docs:** [scipy.sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html) ·
[Back to lecture](15-sparse-matrices-lecture.md)
