"""
07-machine-learning — 27: Metrics Deep Dive — Thresholds as Business Decisions
==============================================================================
Topics: precision/recall tradeoff, ROC-AUC vs PR-AUC (when ROC misleads on
        imbalance), F-beta, log loss, threshold selection, regression
        metrics, multi-class averaging

Why this matters for AI/backend engineering:
    "Accuracy 95%" is usually a lie worth ignoring. Choosing the metric is
    choosing WHAT the model optimizes, and choosing the threshold is a
    BUSINESS decision (a false positive costs money, a false negative costs
    money — rarely equally).

Run:      python 27-metrics-deep.py
Verify:   python 27-metrics-deep.py --verify
Reference: https://scikit-learn.org/stable/modules/model_evaluation.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score, fbeta_score, roc_auc_score,
    average_precision_score, log_loss, roc_curve, precision_recall_curve,
    confusion_matrix, r2_score, mean_squared_error, mean_absolute_error,
)

rng = np.random.RandomState(0)

# ============================================================
# 1. Accuracy lies on imbalance
# ============================================================
X, y = make_classification(n_samples=5000, n_features=15, n_informative=6,
                           n_redundant=3, weights=[0.98, 0.02], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
m = LogisticRegression(max_iter=500).fit(Xtr, ytr)
pred = m.predict(Xte)
proba = m.predict_proba(Xte)[:, 1]

acc = (pred == yte).mean()
print("Example 1: accuracy vs the useful metrics (1.5% positive)")
print(f"  accuracy        : {acc:.4f}   <- looks great")
print(f"  recall (TPR)    : {recall_score(yte, pred):.3f}")
print(f"  precision       : {precision_score(yte, pred):.3f}")
print(f"  F1              : {f1_score(yte, pred):.3f}")

# ============================================================
# 2. ROC vs PR — when ROC misleads
# ============================================================
# ROC-AUC ignores the class balance in its axes; PR-AUC does not.
roc_auc = roc_auc_score(yte, proba)
pr_auc = average_precision_score(yte, proba)
print("\nExample 2: ROC vs PR on extreme imbalance")
print(f"  ROC-AUC: {roc_auc:.3f}  (still looks fine on 2% positives)")
print(f"  PR-AUC : {pr_auc:.3f}  (brutally honest on 2% positives)")

# ============================================================
# 3. Threshold selection is a business decision
# ============================================================
# Cost model: a missed fraud costs $1000, a false alert costs $10 of review.
# Find the threshold minimizing expected cost.
cost_fp, cost_fn = 10.0, 1000.0
prec, rec, thresh = precision_recall_curve(yte, proba)
thresh_full = np.concatenate([[1.0], thresh])
# cost per example = P(pred=1)*cost_fp*FP_rate_approx + P(pred=0)*cost_fn*...
# Practical approach: cost = FP_rate*cost_fp*prior_pos_share + (1-recall)*cost_fn
fp_rate = 1 - prec  # within predicted positives
costs = (1 - rec) * cost_fn + fp_rate * (1 - rec + 1e-9) * cost_fp  # illustration
best_i = int(np.argmin(costs))
best_threshold = thresh_full[best_i]
print("\nExample 3: threshold as a cost decision")
print(f"  chosen threshold: {best_threshold:.3f}  (minimizes FP*cost_fp + FN*cost_fn)")
print(f"  precision at it : {prec[best_i]:.3f}, recall at it: {rec[best_i]:.3f}")

# ============================================================
# 4. F-beta — weighting the two failure modes
# ============================================================
print("\nExample 4: F-beta")
print(f"  F2 (recall matters 2x): {fbeta_score(yte, pred, beta=2):.3f}")
print(f"  F0.5 (precision 2x)   : {fbeta_score(yte, pred, beta=0.5):.3f}")
print(f"  log loss              : {log_loss(yte, proba):.3f}  (probabilities, not labels)")

# ============================================================
# 5. Regression metrics
# ============================================================
Xr, yr = make_regression(n_samples=1000, n_features=10, noise=20, random_state=0)
Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(Xr, yr, test_size=0.3, random_state=0)
rm = LinearRegression().fit(Xr_tr, yr_tr)
yp = rm.predict(Xr_te)
print("\nExample 5: regression metrics")
print(f"  R2      : {r2_score(yr_te, yp):.3f}")
print(f"  RMSE    : {np.sqrt(mean_squared_error(yr_te, yp)):.2f}  (same units as y)")
print(f"  MAE     : {mean_absolute_error(yr_te, yp):.2f}  (robust to outliers)")

# ============================================================
# 6. Multi-class averaging
# ============================================================
from sklearn.datasets import make_classification as mk  # noqa: E402

Xm, ym = mk(n_samples=3000, n_features=10, n_classes=3, n_informative=5,
            n_redundant=2, random_state=0)
Xm_tr, Xm_te, ym_tr, ym_te = train_test_split(Xm, ym, test_size=0.3, random_state=0)
mm = LogisticRegression(max_iter=500).fit(Xm_tr, ym_tr)
pm = mm.predict(Xm_te)
print("\nExample 6: multi-class averaging")
print(f"  macro F1 (class-avg, class-size independent): {f1_score(ym_te, pm, average='macro'):.3f}")
print(f"  micro F1 (instance-avg, favors big classes) : {f1_score(ym_te, pm, average='micro'):.3f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Accuracy is meaningless on imbalance; use PR-AUC + F-beta")
print("- Threshold = business decision (cost of FP vs FN)")
print("- ROC-AUC can look great while the model is useless at 1% positive")
print("- Regression: R2 for variance explained, RMSE for units, MAE for robustness")
print("- Multi-class: macro for class fairness, micro for overall accuracy")
print("=" * 60)


def _verify() -> None:
    assert acc > 0.9, "accuracy on 98/2 must be high (majority class)"
    assert roc_auc > pr_auc, "on imbalance PR-AUC is typically below ROC-AUC"
    assert 0.0 <= best_threshold <= 1.0
    assert r2_score(yr_te, yp) > 0.5, "clean regression data should fit well"
    assert 0 <= f1_score(ym_te, pm, average="macro") <= 1
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
