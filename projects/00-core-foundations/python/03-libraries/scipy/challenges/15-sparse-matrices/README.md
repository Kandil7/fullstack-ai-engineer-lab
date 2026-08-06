# Challenge 15: Sparse Matrices — Measure, Normalize, Retrieve

Three tiers of sparse discipline: Bronze audits a matrix,
Silver manipulates it without densifying, Gold runs a sparse
TF-IDF retrieval + sparse solve under a memory budget.

## 🥉 Bronze — Sparse Audit (~15 min)

**Task:** Implement `sparse_stats(A)` that returns a dict with
`nnz`, `density`, `bytes` (storage cost of the sparse
representation), and `shape` for any `coo_matrix`/`csr_matrix`/
`csc_matrix`.

**Signature:**
```python
def sparse_stats(A) -> dict:
```

| Input | Expected |
|---|---|
| coo, 5 entries in 4×3 | `nnz=5, density=5/12, bytes=80, shape=(4, 3)` |
| coo with an explicit `0.0` | `nnz` counts the stored zero |
| csc input | same dict as its csr twin |

**Note:** bytes = `data.nbytes + indices.nbytes + indptr.nbytes`
(after converting to CSR). **No Python loops or comprehensions.**

---

## 🥈 Silver — Sparse Ops Without Densifying (~35 min)

**Task:** Implement two functions:

1. `row_normalize_csr(X)` — return a CSR matrix with every row
   scaled to unit L2 norm; `nnz` must be preserved; raise
   `ValueError` if any row has zero norm.
2. `sparse_dot(A, B)` — return `A @ B` as a CSR matrix.

**Signatures:**
```python
def row_normalize_csr(X) -> sp.csr_matrix:
def sparse_dot(A, B) -> sp.csr_matrix:
```

| Input | Expected |
|---|---|
| `X` 5×4 csr | all row L2 norms == 1 (atol 1e-9) |
| `X` with a zero row | raises `ValueError` |
| `X` passed as csc | same result (converts internally) |
| `A` 60×50, `B` 50×40, 10% dense | CSR output, matches dense `@` (atol 1e-12) |
| mismatched `A`/`B` dims | raises `ValueError` |

**Constraints:** **No Python loops or comprehensions.** Do not
call `.toarray()` or `.todense()` anywhere.

---

## 🥇 Gold — Sparse Retrieval + Sparse Solve (~75 min)

**Task:** Implement two functions:

1. `tfidf_retrieval(docs, query, top_k=3)` — fit a
   `TfidfVectorizer`, row-normalize the corpus matrix to unit L2
   *without densifying it*, transform the query, and return the
   `top_k` document indices ordered by cosine similarity
   (descending), as an `np.ndarray` of ints.
2. `solve_sparse_system(n)` — build the tridiagonal
   `A = diags([-1, 2, -1], [-1, 0, 1])` of size `n`, solve
   `A x = ones(n)` with `spsolve`, return `x`.

**Signatures:**
```python
def tfidf_retrieval(docs: list[str], query: str,
                    top_k: int = 3) -> np.ndarray:
def solve_sparse_system(n: int) -> np.ndarray:
```

| Input | Expected |
|---|---|
| 2000 docs (1000 class A + 1000 class B), query `"anchor_a"` | all top-3 indices < 1000 |
| query `"anchor_b"` | all top-3 indices ≥ 1000 |
| `top_k=5` | exactly 5 indices, similarity non-increasing |
| `solve_sparse_system(2000)` | max \|A x − b\| < 1e-8 |
| `solve_sparse_system(500)` | x[0] ≈ 250.5 (closed form: `x[i] = i(n+1−i)/2`) |

**Memory budgets (enforced by `tracemalloc`):**

- `tfidf_retrieval`: peak < 10 MB — the corpus matrix alone is
  2000 × ~5000 = **80 MB dense**; densifying fails the guard.
- `solve_sparse_system`: peak < 5 MB — a dense solve needs
  32 MB for `A` alone.

**Constraints:** **No Python loops or comprehensions.**
`.toarray()` is allowed only on the tiny transformed query row.

---

## Running

```bash
pytest 03-libraries/scipy/challenges/15-sparse-matrices/test_challenge.py -v
```

```text
collected ... items  (all tests pass against solution.py;
                      starter.py raises NotImplementedError by design)
```

## Test File Structure

```
challenges/15-sparse-matrices/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Correctness + memory guards + deterministic data
```
