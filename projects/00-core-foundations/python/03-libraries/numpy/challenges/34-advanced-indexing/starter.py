"""Challenge 34: Advanced Indexing — starter template.

Implement the three functions below. Read README.md for the
behavior contract and I/O tables.
"""

import numpy as np


def top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k largest scores (order unspecified)."""
    raise NotImplementedError


def quantile_buckets(values: np.ndarray, q: int) -> np.ndarray:
    """Integer bucket labels in [0, q) from quantile edges."""
    raise NotImplementedError


def retrieve_nearest(X: np.ndarray, query: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k rows of X closest to `query` (Euclidean)."""
    raise NotImplementedError
