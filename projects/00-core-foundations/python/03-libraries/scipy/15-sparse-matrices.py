"""Topic 15: Sparse Matrices (scipy.sparse).

CSR / CSC / COO formats, when sparse wins, sparse matmul,
memory accounting, TF-IDF sparsity, and the handoff to sklearn.
Why this matters for AI/backend engineering: every TF-IDF and
count vectorizer, every adjacency matrix in graph ML, every
click/log interaction matrix is sparse. Storing them dense is
how you OOM a batch job at 1M documents.

Run:  python 03-libraries/scipy/15-sparse-matrices.py
"""

import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve

# ---------------------------------------------------------------------------
# Example 1: COO -- the human format
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
flat = rng.choice(80, size=30, replace=False)   # 30 unique cells
rows = flat // 8
cols = flat % 8
data = rng.uniform(0.1, 1.0, 30)

coo = sp.coo_matrix((data, (rows, cols)), shape=(10, 8))
print("# Example 1: COO triplets -> object")
print(f"   shape={coo.shape}  nnz={coo.nnz}  density={coo.nnz / np.prod(coo.shape):.3f}")
print(f"   toarray() == dense 10x8?  {coo.toarray().shape}")

# stored zeros are stored: they count in nnz until removed
with_zero = sp.coo_matrix((np.array([1.0, 0.0, 2.0]),
                           (np.array([0, 1, 2]), np.array([0, 1, 2]))),
                          shape=(3, 3))
cleaned = with_zero.tocsr()
cleaned.eliminate_zeros()          # in-place; returns None
print(f"   explicit zero: nnz before eliminate_zeros()={with_zero.nnz}, "
      f"after={cleaned.nnz}")

# ---------------------------------------------------------------------------
# Example 2: CSR vs CSC -- pick by access pattern
# ---------------------------------------------------------------------------
csr = coo.tocsr()
csc = coo.tocsc()
row0 = csr.getrow(0)          # O(1)-ish on CSR
col0 = csc.getcol(0)          # O(1)-ish on CSC
print("# Example 2: CSR vs CSC")
print(f"   nnz equal? {csr.nnz == csc.nnz == coo.nnz} "
      f"(coo counts raw triplets; duplicate cells are summed on conversion)")
print(f"   toarray equal? {np.array_equal(csr.toarray(), csc.toarray())}")
print(f"   getrow(0).nnz={row0.nnz}   getcol(0).nnz={col0.nnz}")
print("   rule: row slicing on CSR, column slicing on CSC; convert once")

# ---------------------------------------------------------------------------
# Example 3: when sparse wins -- measured memory
# ---------------------------------------------------------------------------
n = 4000
dense = np.zeros((n, n), dtype=np.float64)          # 128 MB dense
sparse = sp.random(n, n, density=0.005, format="csr",
                   random_state=42,
                   data_rvs=lambda k: rng.uniform(0.1, 1.0, size=k))
sp_bytes = (sparse.data.nbytes + sparse.indices.nbytes + sparse.indptr.nbytes)
ratio = dense.nbytes / sp_bytes
print("# Example 3: memory comparison (4000x4000, 0.5% filled)")
print(f"   dense:  {dense.nbytes / 1e6:.1f} MB")
print(f"   sparse: {sp_bytes / 1e6:.3f} MB  (nnz={sparse.nnz})")
print(f"   ratio:  {ratio:.0f}x -- sparse wins when density < ~10%")

# ---------------------------------------------------------------------------
# Example 4: sparse matmul -- keep both sides sparse
# ---------------------------------------------------------------------------
A_csr = sp.random(60, 50, density=0.1, format="csr", random_state=0)
B_csr = sp.random(50, 40, density=0.1, format="csr", random_state=1)
C_sparse = A_csr @ B_csr
C_dense = A_csr.toarray() @ B_csr.toarray()
v = np.ones(50)
print("# Example 4: sparse matmul")
print(f"   sparse @ sparse -> {type(C_sparse).__name__}  (nnz={C_sparse.nnz})")
print(f"   matches dense? {np.allclose(C_sparse.toarray(), C_dense)}")
print(f"   sparse @ ndarray -> {type(A_csr @ v).__name__} (1-D result)")

# ---------------------------------------------------------------------------
# Example 5: identity and diagonals
# ---------------------------------------------------------------------------
I5 = sp.eye(5, format="csr")
A5 = sp.random(5, 5, density=0.5, format="csr", random_state=3)
print("# Example 5: identity / diagonals")
print(f"   I @ A == A?  {np.array_equal((I5 @ A5).toarray(), A5.toarray())}")
print(f"   trace via .diagonal() = {A5.diagonal().sum():.3f}")

# ---------------------------------------------------------------------------
# Example 6: solving large sparse linear systems
# ---------------------------------------------------------------------------
m = 2000
tri = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(m, m), format="csr")
b = np.ones(m)
x = spsolve(tri, b)
residual = np.max(np.abs(tri @ x - b))
print("# Example 6: spsolve on a 2000x2000 tridiagonal system")
print(f"   max |A x - b| = {residual:.2e}  (sparse direct solve, no dense 32 MB)")

# ---------------------------------------------------------------------------
# Example 7: TF-IDF is sparse -- handoff to sklearn
# ---------------------------------------------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

docs = [
    "cats chase mice in the kitchen",
    "cats sleep all day on the sofa",
    "dogs chase cats in the park",
    "dogs bark at night in the yard",
]
y = np.array([0, 0, 1, 1])
X_tfidf = TfidfVectorizer().fit_transform(docs)
n_docs, n_terms = X_tfidf.shape
density = X_tfidf.nnz / (n_docs * n_terms)
clf = LogisticRegression().fit(X_tfidf, y)
print("# Example 7: TF-IDF -> sparse -> sklearn")
print(f"   type={type(X_tfidf).__name__}  shape={X_tfidf.shape}  "
      f"density={density:.2f}")
print(f"   LogisticRegression on sparse matrix score={clf.score(X_tfidf, y):.2f}")

# ---------------------------------------------------------------------------
# Example 8: row-normalize embeddings-style rows, stay sparse
# ---------------------------------------------------------------------------
l2n = np.asarray(X_tfidf.power(2).sum(axis=1)).ravel() ** 0.5   # row L2
scale = sp.diags(1.0 / l2n)
Xn = scale @ X_tfidf                                # sparse row scaling
l2 = np.asarray(Xn.power(2).sum(axis=1)).ravel()
print("# Example 8: row normalization without densifying")
print(f"   Xn still {type(Xn).__name__}  nnz preserved? {Xn.nnz == X_tfidf.nnz}")
print(f"   all row L2 norms == 1? {np.allclose(l2, 1.0, atol=1e-9)}")


# ---------------------------------------------------------------------------
def _verify():
    """Assert the facts the examples demonstrate."""
    assert csr.toarray().shape == (10, 8)
    assert np.array_equal(csr.toarray(), coo.toarray())
    assert csr.nnz == csc.nnz == coo.nnz
    assert dense.nbytes / sp_bytes > 50, "sparse must beat dense by 50x+"
    assert np.allclose(C_sparse.toarray(), C_dense, atol=1e-12)
    assert isinstance(A_csr @ v, np.ndarray) and (A_csr @ v).ndim == 1
    assert np.array_equal((I5 @ A5).toarray(), A5.toarray())
    assert residual < 1e-8
    assert isinstance(X_tfidf, sp.csr_matrix)
    assert density < 0.5, "TF-IDF toy set must be majority zeros"
    assert clf.score(X_tfidf, y) == 1.0
    assert isinstance(Xn, sp.csr_matrix) and Xn.nnz == X_tfidf.nnz
    assert np.allclose(l2, 1.0, atol=1e-9)
    print("\n[OK] all 8 checks passed")


if __name__ == "__main__":
    _verify()
