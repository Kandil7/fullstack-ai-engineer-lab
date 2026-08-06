"""
Challenge 31: Memory Contracts — Starter
==========================================
Fill in the three functions. Silver and Gold must contain no
Python loops or comprehensions; Gold's memory behavior is
verified with tracemalloc.
"""

from __future__ import annotations

import numpy as np


def column_view(X: np.ndarray, j: int) -> np.ndarray:
    """Return a VIEW of column j -- no copy, shared buffer.

    Args:
        X: float array of shape (n, d).
        j: column index in [0, d).

    Returns:
        View of shape (n,) that shares memory with X.
    """
    raise NotImplementedError("implement column_view")


def ensure_contiguous(x: np.ndarray) -> np.ndarray:
    """Return C-contiguous data: same object when already so,
    otherwise a C-contiguous copy of the same values.

    Args:
        x: any ndarray (any layout).

    Returns:
        C-contiguous ndarray with np.allclose(x, out) == True.
        Must not use Python loops.
    """
    raise NotImplementedError("implement ensure_contiguous")


def downcast_when_safe(X: np.ndarray) -> np.ndarray:
    """Return float32 data with zero copying when X is already
    float32, and a single float32 cast otherwise.

    Args:
        X: numeric ndarray.

    Returns:
        float32 ndarray; `out is X` for float32 input.
        Must not use Python loops.
    """
    raise NotImplementedError("implement downcast_when_safe")
