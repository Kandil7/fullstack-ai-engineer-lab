"""Challenge 14: Optimization Advanced — reference solution.

Bounded L-BFGS-B, robust least-squares line fitting, and a
max-Sharpe SLSQP allocation. No Python loops anywhere.
"""

import numpy as np
from scipy import optimize

_LOSSES = {"linear", "soft_l1", "huber", "cauchy"}


def minimize_box(func, x0: float, lo: float, hi: float) -> float:
    """Minimize `func` over [lo, hi]; return the argmin."""
    res = optimize.minimize(func, np.array([x0]), method="L-BFGS-B",
                            bounds=[(lo, hi)])
    if not res.success:
        raise RuntimeError(f"optimizer failed: {res.message}")
    return float(res.x[0])


def fit_robust_line(x: np.ndarray, y: np.ndarray,
                    loss: str) -> tuple[float, float]:
    """Least-squares line fit with the given robust loss."""
    if loss not in _LOSSES:
        raise ValueError(f"unknown loss: {loss!r}")
    res = optimize.least_squares(
        lambda p: p[0] * x + p[1] - y, x0=np.zeros(2), loss=loss)
    return float(res.x[0]), float(res.x[1])


def allocate_weights(mu: np.ndarray, cov: np.ndarray,
                     risk_free: float) -> np.ndarray:
    """Max-Sharpe long-only fully-invested weights via SLSQP."""
    n = mu.size

    def neg_sharpe(w):
        ret = mu @ w
        risk = np.sqrt(w @ cov @ w)
        return -(ret - risk_free) / risk

    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    res = optimize.minimize(neg_sharpe, np.full(n, 1.0 / n),
                            method="SLSQP",
                            bounds=[(0.0, 1.0)] * n, constraints=cons)
    if not res.success:
        raise RuntimeError(f"optimizer failed: {res.message}")
    return res.x
