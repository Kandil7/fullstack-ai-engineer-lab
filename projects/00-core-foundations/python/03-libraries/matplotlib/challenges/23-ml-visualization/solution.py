"""
Challenge 23: ML Visualization — Reference Solution
=====================================================
"""

from __future__ import annotations

import numpy as np

try:  # sklearn present -> use its metrics; else fall back to numpy
    from sklearn.metrics import confusion_matrix, roc_curve
    HAS_SKLEARN = True
except ImportError:  # pragma: no cover - fallback path
    HAS_SKLEARN = False

    def roc_curve(y_true: np.ndarray, y_score: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Minimal ROC: sweep thresholds over sorted scores."""
        order = np.argsort(y_score)[::-1]
        y_s, y_t = y_score[order], y_true[order]
        tps = np.cumsum(y_t)
        fps = np.cumsum(1 - y_t)
        tpr = np.concatenate([[0.0], tps / max(tps[-1], 1), [1.0]])
        fpr = np.concatenate([[0.0], fps / max(fps[-1], 1), [1.0]])
        return fpr, tpr, np.concatenate([[-np.inf], y_s, [np.inf]])

    def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, labels: list[int]) -> np.ndarray:
        """n x n confusion matrix from arrays."""
        cm = np.zeros((len(labels), len(labels)), dtype=int)
        for t, p in zip(y_true, y_pred):
            cm[labels.index(int(t)), labels.index(int(p))] += 1
        return cm


def roc_endpoints(y_true: np.ndarray, y_score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (fpr, tpr) from sklearn or a numpy fallback.

    Why this approach: the metric layer must be swappable so the same
    plotting code runs in environments with and without sklearn. The
    fallback is a textbook threshold sweep with the standard (0,0) /
    (1,1) padding.
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    return fpr, tpr


def confusion_stats(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    """Return {"shape": (n, n), "diagonal": int} for 3 classes.

    Why this approach: shape proves the matrix is square per class
    count, and the diagonal is the first thing a report reader checks —
    the total number of correct predictions.
    """
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    return {"shape": cm.shape, "diagonal": int(np.trace(cm))}


def learning_curve_improves() -> bool:
    """True iff the synthetic learning curve shows improvement.

    Why this approach: the three conditions encode the definition of a
    healthy learning curve — both scores rise with data and train stays
    above validation. Seeded noise keeps the verdict deterministic.
    """
    rng = np.random.default_rng(42)
    sizes = np.arange(100, 2001, 100)
    train = 0.94 - 0.06 * np.exp(-sizes / 400) + rng.normal(0, 0.004, sizes.size)
    valid = 0.90 - 0.12 * np.exp(-sizes / 500) + rng.normal(0, 0.005, sizes.size)
    return bool(train[-1] > train[0] and valid[-1] > valid[0] and np.all(train >= valid))
