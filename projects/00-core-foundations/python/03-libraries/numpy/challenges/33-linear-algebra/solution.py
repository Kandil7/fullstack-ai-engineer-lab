"""Challenge 33: Linear Algebra — reference solution.

Normalize-and-multiply for cosine, Vandermonde + lstsq for the
fit, and vectorized byte-budget selection for the compression.
No Python loops anywhere.
"""

import numpy as np


def cosine_matrix(X: np.ndarray) -> np.ndarray:
    """Return the (n, n) matrix of cosine similarities between rows."""
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    return Xn @ Xn.T


def fit_polynomial(t: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """Least-squares fit of degree-`degree` polynomial; return [c0 ... cd]."""
    V = np.vander(t, degree + 1, increasing=True)
    coef, *_ = np.linalg.lstsq(V, y, rcond=None)
    return coef


def compress_svd(A: np.ndarray, max_bytes: int) -> tuple[np.ndarray, int]:
    """Return (approx, k): largest-k truncated SVD fitting max_bytes."""
    m, n = A.shape
    min_bytes = (m + n + 1) * 8
    if max_bytes < min_bytes:
        raise ValueError(f"max_bytes {max_bytes} cannot hold rank 1 "
                         f"(needs {min_bytes})")
    U, s, Vh = np.linalg.svd(A)
    r = min(m, n)
    ks = np.arange(1, r + 1)
    fits = ks * (m + n + 1) * 8 <= max_bytes
    k = int(fits.sum())                    # largest rank that fits
    if k == 0:
        k = 1
    approx = (U[:, :k] * s[:k]) @ Vh[:k, :]
    return approx, k
