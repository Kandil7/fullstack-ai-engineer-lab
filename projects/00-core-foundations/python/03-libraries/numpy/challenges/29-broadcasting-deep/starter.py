"""
Challenge 29: Broadcasting Without Explicit Loops — Starter
============================================================
Fill in the three functions. The test suite rejects Python loops
(for/while/comprehensions) for Silver and Gold, so think in
broadcast expressions, keepdims, and matrix products.
"""

from __future__ import annotations

import numpy as np


def add_bias(batch: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """Add the (D,) bias vector to every row of a (B, D) batch.

    Args:
        batch: float array of shape (B, D).
        bias: float array of shape (D,).

    Returns:
        Array of shape (B, D) where row i equals batch[i] + bias.

    Raises:
        ValueError: if bias length is not compatible with D.
    """
    raise NotImplementedError("implement add_bias")


def row_zscore(X: np.ndarray) -> np.ndarray:
    """Z-score each row independently: (x - mean) / std per row.

    Rows with zero standard deviation become all zeros (not nan).

    Args:
        X: float array of shape (n, d).

    Returns:
        Float array of shape (n, d). Must not use Python loops.
    """
    raise NotImplementedError("implement row_zscore")


def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Euclidean distances between rows of a and rows of b.

    Use ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a b^T to keep memory at
    O(n*m), never materializing an (n, m, d) tensor.

    Args:
        a: float array of shape (n, d).
        b: float array of shape (m, d).

    Returns:
        Float array of shape (n, m) with dist[i, j] >= 0.
    """
    raise NotImplementedError("implement pairwise_distances")
