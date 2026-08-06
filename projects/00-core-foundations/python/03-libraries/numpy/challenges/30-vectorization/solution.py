"""
Challenge 30: Vectorize the Given Loop — Reference
====================================================
Why these implementations:
- sigmoid: one ufunc expression replaces the three-step loop.
- clean_scores: one combined mask expresses clamp-then-zero in a
  single pass; np.where keeps the output aligned with the input.
- softmax_rows: keepdims=True keeps the row max and row sum at
  (n, 1), so both broadcasts work; subtracting the max before exp
  is the numerical-stability fix that prevents inf/nan rows.
"""

from __future__ import annotations

import numpy as np


def sigmoid(X: np.ndarray) -> np.ndarray:
    """Elementwise sigmoid: 1 / (1 + exp(-x)).

    The loop version (out[i] = 1 / (1 + exp(-X[i]))) is replaced by
    the ufunc chain; np.exp is compiled, so the whole pass is one
    C-level loop with no interpreter steps.
    """
    return 1.0 / (1.0 + np.exp(-X))


def clean_scores(scores: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Clamp scores into [lo, hi] and zero out |score| < 0.01.

    Build ONE boolean mask for the zero-out rule, combine it with
    the clamp via np.where: np.clip does the clamp, then where
    replaces small-magnitude entries with 0. No branches, no loops.
    """
    clamped = np.clip(scores, lo, hi)
    return np.where(np.abs(scores) < 0.01, 0.0, clamped)


def softmax_rows(X: np.ndarray) -> np.ndarray:
    """Stable row-wise softmax: subtract row max before exp.

    m = X.max(axis=1, keepdims=True) keeps (n, 1) so X - m
    broadcasts along columns. exp(X - m) cannot overflow even for
    huge inputs; the row sums also use keepdims so the divide
    broadcasts back. One expression per stage, zero loops.
    """
    m = X.max(axis=1, keepdims=True)
    e = np.exp(X - m)
    return e / e.sum(axis=1, keepdims=True)
