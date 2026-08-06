"""
Matplotlib — 23: ML Visualization
======================================
Topics: learning curves; confusion matrix; ROC/PR curves; residuals;
feature importance; embedding scatter. Synthetic data only (sklearn if
installed, else numpy) — no real models, no fitting cost.

Why this matters for AI/backend engineering:
    Every model you ship needs a report: does it generalize (learning
    curve), where does it err (confusion matrix, residuals), what is the
    best operating point (ROC/PR), and what drove the prediction (feature
    importance, embedding scatter). These six plots are the standard
    debugging kit for a training pipeline.

Run:      python 23-ml-visualization.py
Verify:   python 23-ml-visualization.py --verify
Reference: https://scikit-learn.org/stable/visualizations.html
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # MUST precede pyplot import: headless CI rendering

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parents[2] / "outputs" / "matplotlib"
os.makedirs(OUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)

try:  # sklearn present -> use its metrics; else fall back to numpy
    from sklearn.metrics import auc, confusion_matrix, roc_curve
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

    def auc(fpr: np.ndarray, tpr: np.ndarray) -> float:
        """Trapezoidal AUC."""
        return float(np.trapezoid(tpr, fpr))

    def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, labels: list[int]) -> np.ndarray:
        """2x2 confusion matrix from arrays."""
        cm = np.zeros((len(labels), len(labels)), dtype=int)
        for t, p in zip(y_true, y_pred):
            cm[labels.index(int(t)), labels.index(int(p))] += 1
        return cm


# ============================================================
# 1. Learning curve: does the model keep improving with data?
# ============================================================
# Train/validation score vs training-set size. Converging curves mean
# more data helps; a widening gap means overfitting.

def learning_curve_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Deterministic synthetic learning curve: train/val scores vs size."""
    sizes = np.arange(100, 2001, 100)
    # More data -> higher score; train above val; both saturate.
    train = 0.94 - 0.06 * np.exp(-sizes / 400) + rng.normal(0, 0.004, sizes.size)
    valid = 0.90 - 0.12 * np.exp(-sizes / 500) + rng.normal(0, 0.005, sizes.size)
    return sizes, train, valid


def plot_learning_curve() -> plt.Axes:
    """Draw the learning curve with train/val bands."""
    sizes, train, valid = learning_curve_data()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sizes, train, label="train", color="tab:blue")
    ax.plot(sizes, valid, label="validation", color="tab:orange")
    ax.set_xlabel("training rows")
    ax.set_ylabel("accuracy")
    ax.set_title("Learning curve")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-learning-curve.png", dpi=120)
    plt.close(fig)
    return ax


# ============================================================
# 2. Confusion matrix: where the errors land
# ============================================================
# Heatmap of true vs predicted class. The diagonal is the win; off-diagonal
# cells name the systematic confusion (e.g., 'cat' predicted as 'dog').

def plot_confusion() -> None:
    """Draw a 3x3 confusion matrix heatmap."""
    labels = ["setosa", "versicolor", "virginica"]
    y_true = rng.integers(0, 3, 300)
    y_pred = np.clip(y_true + rng.choice([-1, 0, 0, 0, 1], 300), 0, 2)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])

    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="viridis")
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(3), labels)
    ax.set_yticks(range(3), labels)
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black")
    ax.set_title("Confusion matrix")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-confusion.png", dpi=120)
    plt.close(fig)


# ============================================================
# 3. ROC and PR curves: choosing the operating point
# ============================================================
# ROC: TPR vs FPR across thresholds. PR: precision vs recall (better for
# rare positive classes). AUC summarizes the whole curve; the elbow is
# where you pick the deployment threshold.

def roc_pr_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    """Synthetic scores with a planted separation; return curves + AUCs."""
    n = 1000
    y_true = np.concatenate([np.zeros(700), np.ones(300)]).astype(int)
    y_score = np.concatenate([
        rng.normal(0.0, 1.0, 700), rng.normal(2.2, 1.0, 300)
    ])
    fpr, tpr, _ = roc_curve(y_true, y_score)
    # Precision-recall from the same threshold sweep.
    order = np.argsort(y_score)[::-1]
    y_s, y_t = y_score[order], y_true[order]
    tp = np.cumsum(y_t)
    fp = np.cumsum(1 - y_t)
    precision = tp / np.maximum(tp + fp, 1)
    recall = tp / max(int(tp[-1]), 1)
    precision = np.concatenate([[precision[0]], precision])
    recall = np.concatenate([[0.0], recall])
    pr_auc = float(np.trapezoid(precision, recall))
    return fpr, tpr, recall, precision, pr_auc, float(auc(fpr, tpr))


def plot_roc_pr() -> tuple[np.ndarray, np.ndarray]:
    """Draw ROC and PR side by side; return the ROC arrays."""
    fpr, tpr, recall, precision, pr_auc, roc_auc = roc_pr_data()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    ax1.plot(fpr, tpr, color="tab:blue")
    ax1.plot([0, 1], [0, 1], "k--", alpha=0.4)
    ax1.set_xlabel("FPR")
    ax1.set_ylabel("TPR")
    ax1.set_title(f"ROC (AUC={roc_auc:.3f})")
    ax2.plot(recall, precision, color="tab:orange")
    ax2.set_xlabel("recall")
    ax2.set_ylabel("precision")
    ax2.set_title(f"PR (AUC={pr_auc:.3f})")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-roc-pr.png", dpi=120)
    plt.close(fig)
    return fpr, tpr


# ============================================================
# 4. Residuals: prediction error vs prediction
# ============================================================
# Residual = y_true - y_pred. A horizontal cloud around zero means the
# model is unbiased; a funnel shape means variance grows with magnitude.

def plot_residuals() -> plt.Axes:
    """Scatter of residuals against predictions with a zero line."""
    x = rng.normal(0, 1, 400)
    y_pred = 2.0 * x + rng.normal(0, 0.4, 400)
    residual = y_pred - (2.0 * x)            # "true" model minus prediction noise
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(y_pred, residual, s=12, alpha=0.6, color="tab:blue")
    ax.axhline(0.0, color="tab:red", lw=1.2, ls="--")
    ax.set_xlabel("predicted")
    ax.set_ylabel("residual")
    ax.set_title("Residuals vs predicted")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-residuals.png", dpi=120)
    plt.close(fig)
    return ax


# ============================================================
# 5. Feature importance: what drove the decision
# ============================================================
# Horizontal bar chart, top features first. This is the plot that goes
# into the model card and the fairness review.

def plot_feature_importance() -> plt.Axes:
    """Bar chart of synthetic feature importances."""
    names = ["emb_dim", "lr", "batch", "dropout", "depth", "width"]
    importance = np.array([0.31, 0.24, 0.17, 0.12, 0.09, 0.07])
    order = np.argsort(importance)
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.barh(np.array(names)[order], importance[order], color="tab:green")
    ax.set_xlabel("importance")
    ax.set_title("Feature importance")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-importance.png", dpi=120)
    plt.close(fig)
    return ax


# ============================================================
# 6. Embedding scatter: 2D view of high-dim vectors
# ============================================================
# Two synthetic clusters projected to 2D (what t-SNE/UMAP would produce).
# Color by label so structure is visible at a glance.

def plot_embedding() -> plt.Axes:
    """Scatter of a synthetic 2D embedding, colored by class."""
    a = rng.normal([-2, -2], 0.7, size=(120, 2))
    b = rng.normal([2, 2], 0.7, size=(120, 2))
    points = np.vstack([a, b])
    labels = np.array([0] * 120 + [1] * 120)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    ax.scatter(points[:, 0], points[:, 1], c=labels, cmap="viridis", s=14)
    ax.set_title("Embedding scatter (2D projection)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "23-embedding.png", dpi=120)
    plt.close(fig)
    return ax


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: reporting only accuracy, never the confusion matrix
#   print(f"{acc:.3f}")                    # hides class confusion
# CORRECT: matrix + ROC + residuals, one figure each
#
# MISTAKE: plotting PR for a balanced problem, ROC for a rare class
#   # PR collapses to a horizontal line when positives are common
# CORRECT: ROC for balanced; PR when the positive class is rare
#
# MISTAKE: not closing figures in a loop (runs out of memory)
# CORRECT: plt.close(fig) after every savefig


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    ax_lc = plot_learning_curve()
    assert len(ax_lc.lines) == 2, \
        "learning curve must draw train and validation lines"
    sizes, train, valid = learning_curve_data()
    assert train[-1] > train[0], "train score must improve with data"
    assert valid[-1] > valid[0], "validation score must improve with data"
    assert np.all(train >= valid), "train must stay above validation"

    plot_confusion()
    cm = confusion_matrix(np.array([0, 1, 2]), np.array([0, 1, 1]), labels=[0, 1, 2])
    assert cm.shape == (3, 3), "confusion matrix must be square (n_classes)"
    assert int(cm[0, 0]) == 1, "diagonal counts true positives"

    fpr, tpr = plot_roc_pr()
    assert fpr[0] == 0.0 and tpr[0] == 0.0, "ROC must start at (0, 0)"
    assert abs(fpr[-1] - 1.0) < 1e-12 and abs(tpr[-1] - 1.0) < 1e-12, \
        "ROC must end at (1, 1)"
    _, _, _, _, pr_auc, roc_auc = roc_pr_data()
    assert 0.0 <= roc_auc <= 1.0, "AUC must lie in [0, 1]"
    assert roc_auc > 0.85, "planted separation must give a strong AUC"
    assert pr_auc > 0.85, "PR AUC must also be strong on this synthetic data"

    ax_res = plot_residuals()
    assert len(ax_res.collections) == 1, \
        "residual scatter must add exactly one collection"

    ax_imp = plot_feature_importance()
    assert len(ax_imp.patches) == 6, "one bar per feature"

    ax_emb = plot_embedding()
    assert len(ax_emb.collections) == 1, \
        "embedding scatter must add exactly one collection"

    for name in ("learning-curve", "confusion", "roc-pr", "residuals",
                 "importance", "embedding"):
        png = OUT_DIR / f"23-{name}.png"
        assert png.exists() and png.stat().st_size > 1000, \
            f"{name} artifact must exist and be non-trivial"

    print("[OK] 23-ml-visualization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        plot_learning_curve()
        plot_confusion()
        plot_roc_pr()
        plot_residuals()
        plot_feature_importance()
        plot_embedding()
        print("\n--- Summary ---")
        print("1. Six canonical ML plots: curve, matrix, ROC/PR, residuals, importance, embedding")
        print("2. All synthetic: no models fitted, deterministic with seed 42")
        print("3. sklearn metrics used when available; numpy fallback otherwise")
        _verify()   # always runs, so plain execution is also a test
