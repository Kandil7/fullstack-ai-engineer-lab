"""
Challenge 29: Broadcasting Without Explicit Loops — Reference
==============================================================
Why these implementations:
- add_bias: one broadcast expression; the (D,) vector aligns with the
  trailing axis of (B, D). No loop to write, none to optimize.
- row_zscore: keepdims=True keeps the mean/std at (n, 1) so the
  division broadcasts along columns; np.where repairs zero-std rows
  without branching.
- pairwise_distances: the squared-distance identity avoids the
  O(n*m*d) intermediate that a naive a[:, None, :] - b[None, :, :]
  would allocate; np.clip guards against -0.0 rounding noise before
  the sqrt.
"""

from __future__ import annotations

import numpy as np


def add_bias(batch: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """Add the (D,) bias vector to every row of a (B, D) batch.

    Broadcasting aligns bias with the trailing axis; the result has
    the shape of batch. A wrong-length bias raises ValueError from
    NumPy's broadcast checker -- no manual size test needed.
    """
    return batch + bias  # (B, D) + (D,) -> (B, D)


def row_zscore(X: np.ndarray) -> np.ndarray:
    """Z-score each row independently; zero-std rows become zeros.

    keepdims=True keeps the reduced axes at (n, 1), which broadcast
    against (n, d). np.where is a vectorized branch: it evaluates both
    arms but selects elementwise, keeping everything loop-free.
    """
    mu = X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, keepdims=True)
    z = (X - mu) / sd          # (n, d) / (n, 1) -> (n, d)
    return np.where(sd == 0, 0.0, z)   # repair 0/0 rows


def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Euclidean distances between rows of a and rows of b.

    Squared distance identity: |a-b|^2 = |a|^2 + |b|^2 - 2 a b^T.
    The only O(n*m*d) work is inside the BLAS matmul a @ b.T, which
    never materializes an (n, m, d) tensor -- peak memory stays
    O(n*m + n*d + m*d). Clip tiny negatives from float rounding.
    """
    a_sq = (a * a).sum(axis=1, keepdims=True)      # (n, 1)
    b_sq = (b * b).sum(axis=1, keepdims=True)      # (m, 1)
    sq = a_sq + b_sq.T - 2.0 * (a @ b.T)           # (n, m)
    return np.sqrt(np.clip(sq, 0.0, None))
