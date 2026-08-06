"""Challenge 15: Sparse Matrices — reference solution.

Sparse audit, L2 row normalization, sparse matmul, sparse TF-IDF
retrieval, and a sparse tridiagonal solve. No Python loops and
no densifying of large matrices anywhere.
"""

import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import spsolve
from sklearn.feature_extraction.text import TfidfVectorizer


def sparse_stats(A) -> dict:
    """Audit a sparse matrix: nnz, density, storage bytes, shape."""
    A = A.tocsr()
    m, n = A.shape
    return {
        "nnz": A.nnz,
        "density": A.nnz / (m * n),
        "bytes": A.data.nbytes + A.indices.nbytes + A.indptr.nbytes,
        "shape": (m, n),
    }


def row_normalize_csr(X) -> sp.csr_matrix:
    """Scale every row to unit L2 norm; stay sparse."""
    X = X.tocsr()
    l2 = np.asarray(X.power(2).sum(axis=1)).ravel() ** 0.5
    if np.any(l2 == 0.0):
        raise ValueError("zero-norm row cannot be normalized")
    return sp.diags(1.0 / l2) @ X


def sparse_dot(A, B) -> sp.csr_matrix:
    """Return A @ B as a CSR matrix."""
    return (A.tocsr() @ B.tocsr()).tocsr()


def tfidf_retrieval(docs: list[str], query: str,
                    top_k: int = 3) -> np.ndarray:
    """Top-k doc indices by cosine similarity over sparse TF-IDF."""
    vec = TfidfVectorizer()
    vec.fit(docs)
    X = vec.transform(docs)                      # csr, stays sparse
    l2 = np.asarray(X.power(2).sum(axis=1)).ravel() ** 0.5
    Xn = sp.diags(1.0 / l2) @ X                  # unit-L2 rows
    q = vec.transform([query])
    ql = np.asarray(q.power(2).sum(axis=1)).ravel() ** 0.5
    qv = (sp.diags(1.0 / ql) @ q).toarray().ravel()   # tiny query row
    sim = np.asarray(Xn @ qv).ravel()            # cosine sims, sparse @ dense
    return np.argsort(sim)[::-1][:top_k]


def solve_sparse_system(n: int) -> np.ndarray:
    """Solve the tridiagonal (L+2I) system with spsolve."""
    A = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n),
                 format="csr")
    return spsolve(A, np.ones(n))
