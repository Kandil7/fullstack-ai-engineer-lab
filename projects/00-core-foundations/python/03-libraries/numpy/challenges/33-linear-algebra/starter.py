"""Challenge 33: Linear Algebra — starter template.

Implement the three functions below. Read README.md for the
behavior contract and I/O tables.
"""

import numpy as np


def cosine_matrix(X: np.ndarray) -> np.ndarray:
    """Return the (n, n) matrix of cosine similarities between rows."""
    raise NotImplementedError


def fit_polynomial(t: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """Least-squares fit of degree-`degree` polynomial; return [c0 ... cd]."""
    raise NotImplementedError


def compress_svd(A: np.ndarray, max_bytes: int) -> tuple[np.ndarray, int]:
    """Return (approx, k): largest-k truncated SVD fitting max_bytes."""
    raise NotImplementedError
