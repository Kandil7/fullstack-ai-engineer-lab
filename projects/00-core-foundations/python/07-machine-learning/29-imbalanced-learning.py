"""
07-machine-learning — 29: Imbalanced Learning — When 99% Accuracy Is Failure
============================================================================
Topics: why accuracy is useless at 1% positive, class weights,
        resampling (undersample/oversample/SMOTE-lite), threshold moving,
        evaluation under imbalance (PR-AUC, F-beta, stratified CV)

Why this matters for AI/backend engineering:
    Fraud detection, churn, disease screening, anomaly detection — the
    highest-value problems in industry are imbalanced. A model that predicts
    "no fraud" always is 99% accurate and 100% useless.

Run:      python 29-imbalanced-learning.py
Verify:   python 29-imbalanced-learning.py --verify
Reference: https://scikit-learn.org/stable/modules/imbalanced_learning.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    recall_score, precision_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix,
)

rng = np.random.RandomState(0)

# 2% positive class — classic fraud setup
X, y = make_classification(n_samples=10000, n_features=20, n_informative=8,
                           n_redundant=4, weights=[0.98, 0.02], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

# ============================================================
# 1. The naive model — 98% accurate, 0% useful
# ============================================================
naive = LogisticRegression(max_iter=500).fit(Xtr, ytr)
pred_naive = naive.predict(Xte)
acc_naive = (pred_naive == yte).mean()
rec_naive = recall_score(yte, pred_naive)
print("Example 1: the naive model")
print(f"  accuracy: {acc_naive:.4f}   recall: {rec_naive:.3f}")
print("  -> predicts 'no fraud' almost always; catches ~nothing")

# ============================================================
# 2. Class weights — tell the model the minority is precious
# ============================================================
weighted = LogisticRegression(max_iter=500, class_weight="balanced").fit(Xtr, ytr)
pred_w = weighted.predict(Xte)
print("\nExample 2: class_weight='balanced'")
print(f"  recall   : {recall_score(yte, pred_w):.3f}")
print(f"  precision: {precision_score(yte, pred_w):.3f}")
print(f"  F1       : {f1_score(yte, pred_w):.3f}")

# ============================================================
# 3. Manual SMOTE-lite — synthesize minority samples
# ============================================================
def smote_lite(X_minor, y_minor, k: int = 3, n_synth: int | None = None):
    """Nearest-neighbour interpolation — the core of SMOTE."""
    from sklearn.neighbors import NearestNeighbors

    n_synth = n_synth or len(X_minor)
    nn = NearestNeighbors(n_neighbors=k + 1).fit(X_minor)
    _, idx = nn.kneighbors(X_minor)
    synth = []
    for _ in range(n_synth):
        i = rng.randint(0, len(X_minor))
        neighbor = X_minor[idx[i][1 + rng.randint(0, k)]]  # skip self
        lam = rng.random()
        synth.append(X_minor[i] + lam * (neighbor - X_minor[i]))
    return np.vstack(synth), np.ones(n_synth, dtype=int)


X_minor = Xtr[ytr == 1]
X_synth, y_synth = smote_lite(X_minor, None, n_synth=len(Xtr[ytr == 1]) * 5)
X_bal = np.vstack([Xtr, X_synth])
y_bal = np.hstack([ytr, y_synth])
smoted = LogisticRegression(max_iter=500).fit(X_bal, y_bal)
print("\nExample 3: SMOTE-lite (nearest-neighbour interpolation)")
print(f"  train set: {Xtr.shape[0]} rows -> {X_bal.shape[0]} rows")
print(f"  recall   : {recall_score(yte, smoted.predict(Xte)):.3f}")
print(f"  precision: {precision_score(yte, smoted.predict(Xte)):.3f}")

# ============================================================
# 4. Threshold moving — keep the model, change the decision
# ============================================================
proba = weighted.predict_proba(Xte)[:, 1]
for th in [0.5, 0.2, 0.1, 0.05]:
    pred_th = (proba >= th).astype(int)
    print(f"\n  threshold {th:.2f}: "
          f"recall {recall_score(yte, pred_th):.3f}, "
          f"precision {precision_score(yte, pred_th):.3f}, "
          f"F1 {f1_score(yte, pred_th):.3f}")

# ============================================================
# 5. Evaluation under imbalance — the honest numbers
# ============================================================
print("\nExample 5: the honest evaluation set")
print(f"  PR-AUC  : {average_precision_score(yte, proba):.3f}  (primary metric on imbalance)")
print(f"  ROC-AUC : {roc_auc_score(yte, proba):.3f}")
print(f"  confusion matrix:\n{confusion_matrix(yte, (proba >= 0.2).astype(int))}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Accuracy is meaningless when positives are rare")
print("- class_weight='balanced' is the 1-line fix")
print("- SMOTE synthesizes minority samples (interpolate neighbors)")
print("- Threshold moving trades precision for recall at business level")
print("- PR-AUC + F-beta + stratified CV = honest report card")
print("=" * 60)


def _verify() -> None:
    assert acc_naive > 0.9, "naive model rides the majority class"
    assert rec_naive < 0.2, "naive model catches few positives"
    # Weighted model must catch meaningfully more positives
    assert recall_score(yte, pred_w) > rec_naive * 2, "class weights must help recall"
    assert X_bal.shape[0] > Xtr.shape[0], "SMOTE-lite adds rows"
    assert 0.0 <= proba.min() <= proba.max() <= 1.0
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
