"""Challenge 34: Advanced Indexing — reference solution.

Top-k via argpartition, quantile edges + searchsorted for buckets,
and broadcast-subtract + argpartition for nearest retrieval.
No Python loops anywhere.
"""

import numpy as np


def top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k largest scores (order unspecified)."""
    if k <= 0:
        return np.empty(0, dtype=np.intp)
    k = min(k, scores.size)
    return np.argpartition(scores, -k)[-k:]


def quantile_buckets(values: np.ndarray, q: int) -> np.ndarray:
    """Integer bucket labels in [0, q) from quantile edges."""
    edges = np.quantile(values, np.linspace(0.0, 1.0, q + 1))[1:-1]
    return np.searchsorted(edges, values, side="right")


def retrieve_nearest(X: np.ndarray, query: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k rows of X closest to `query` (Euclidean)."""
    if k <= 0:
        return np.empty(0, dtype=np.intp)
    dist = np.linalg.norm(X - query, axis=1)
    k = min(k, dist.size)
    idx = np.argpartition(dist, k - 1)[:k]
    return idx[np.argsort(dist[idx])]
