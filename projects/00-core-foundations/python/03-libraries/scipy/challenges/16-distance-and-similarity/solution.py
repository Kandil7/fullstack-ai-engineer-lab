"""Challenge 16: Distance and Similarity — reference solution.

Brute-force top-k, hand-rolled cosine distance, normalize-then-
euclidean equivalence, pairwise spread, KD-tree exact neighbors,
and the curse-of-dimensionality spread ratio. No Python loops.
"""

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist, pdist, squareform


def nearest_brute(Q: np.ndarray, X: np.ndarray, k: int,
                  metric: str = "euclidean") -> tuple[np.ndarray, np.ndarray]:
    """Top-k nearest rows of X per query row, via cdist + argsort."""
    if k > len(X):
        raise ValueError(f"k={k} exceeds corpus size {len(X)}")
    dists = cdist(Q, X, metric=metric)
    idx = np.argsort(dists, axis=1)[:, :k]
    dist = np.take_along_axis(dists, idx, axis=1)
    return dist, idx


def cosine_pair(u: np.ndarray, v: np.ndarray) -> float:
    """Cosine distance computed by hand: 1 - (u.v)/(|u||v|)."""
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0.0 or nv == 0.0:
        raise ValueError("zero-norm vector has no direction")
    return float(1.0 - np.dot(u, v) / (nu * nv))


def normalized_topk(Q: np.ndarray, X: np.ndarray,
                    k: int) -> np.ndarray:
    """Top-k indices by euclidean on L2-normalized rows."""
    Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    dists = cdist(Qn, Xn, metric="euclidean")
    return np.argsort(dists, axis=1)[:, :k]


def spread(V: np.ndarray) -> float:
    """Std of all pairwise cosine distances in V."""
    return float(squareform(pdist(V, metric="cosine")).std())


def fast_neighbors(points: np.ndarray, queries: np.ndarray,
                   k: int) -> tuple[np.ndarray, np.ndarray]:
    """Exact top-k via cKDTree."""
    if k > len(points):
        raise ValueError(f"k={k} exceeds corpus size {len(points)}")
    return cKDTree(points).query(queries, k=k)


def spread_ratio(d_low: int, d_high: int, n: int = 2000,
                 seed: int = 42) -> float:
    """spread(d_low) / spread(d_high) for random unit vectors."""
    rng = np.random.default_rng(seed)

    def std_spread(d):
        V = rng.normal(size=(n, d))
        V /= np.linalg.norm(V, axis=1, keepdims=True)
        return spread(V)

    return std_spread(d_low) / std_spread(d_high)
