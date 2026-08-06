"""
Challenge 30: Vectorize the Given Loop — Starter
==================================================
Fill in the three functions. Silver and Gold must contain no
Python loops or comprehensions -- the test suite inspects the
AST and rejects For/While/comprehension nodes.
"""

from __future__ import annotations

import numpy as np


def sigmoid(X: np.ndarray) -> np.ndarray:
    """Elementwise sigmoid: 1 / (1 + exp(-x)).

    Args:
        X: float array of any shape.

    Returns:
        Same-shape array of values in (0, 1).
    """
    raise NotImplementedError("implement sigmoid")


def clean_scores(scores: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Clamp scores into [lo, hi] and zero out |score| < 0.01.

    Args:
        scores: float array.
        lo: lower clamp bound.
        hi: upper clamp bound.

    Returns:
        Same-shape array: clamped, and small-magnitude values zeroed.
        Must not use Python loops.
    """
    raise NotImplementedError("implement clean_scores")


def softmax_rows(X: np.ndarray) -> np.ndarray:
    """Stable row-wise softmax: subtract row max before exp.

    Args:
        X: float array of shape (n, d).

    Returns:
        Float array of shape (n, d) whose rows sum to 1.
        Must not use Python loops.
    """
    raise NotImplementedError("implement softmax_rows")
