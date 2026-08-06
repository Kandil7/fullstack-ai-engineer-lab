"""Challenge 14: Optimization Advanced — starter template.

Implement the three functions below. Read README.md for the
behavior contract and I/O tables.
"""

import numpy as np


def minimize_box(func, x0: float, lo: float, hi: float) -> float:
    """Minimize `func` over [lo, hi]; return the argmin."""
    raise NotImplementedError


def fit_robust_line(x: np.ndarray, y: np.ndarray,
                    loss: str) -> tuple[float, float]:
    """Least-squares line fit with the given robust loss."""
    raise NotImplementedError


def allocate_weights(mu: np.ndarray, cov: np.ndarray,
                     risk_free: float) -> np.ndarray:
    """Max-Sharpe long-only fully-invested weights via SLSQP."""
    raise NotImplementedError
