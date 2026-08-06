"""Challenge 15: Sparse Matrices — starter template.

Implement the functions below. Read README.md for the behavior
contract and I/O tables.
"""

import numpy as np
from scipy import sparse as sp


def sparse_stats(A) -> dict:
    """Audit a sparse matrix: nnz, density, storage bytes, shape."""
    raise NotImplementedError


def row_normalize_csr(X) -> sp.csr_matrix:
    """Scale every row to unit L2 norm; stay sparse."""
    raise NotImplementedError


def sparse_dot(A, B) -> sp.csr_matrix:
    """Return A @ B as a CSR matrix."""
    raise NotImplementedError


def tfidf_retrieval(docs: list[str], query: str,
                    top_k: int = 3) -> np.ndarray:
    """Top-k doc indices by cosine similarity over sparse TF-IDF."""
    raise NotImplementedError


def solve_sparse_system(n: int) -> np.ndarray:
    """Solve the tridiagonal (L+2I) system with spsolve."""
    raise NotImplementedError
