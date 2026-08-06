"""
Challenge 23: ML Visualization — Starter Code
===============================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import numpy as np


def roc_endpoints(y_true: np.ndarray, y_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (fpr, tpr) from sklearn or a numpy fallback."""
    raise NotImplementedError


def confusion_stats(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    """Return {"shape": (n, n), "diagonal": int} for 3 classes."""
    raise NotImplementedError


def learning_curve_improves() -> bool:
    """True iff the synthetic learning curve shows improvement."""
    raise NotImplementedError
