"""
07-machine-learning — 34: Ensembling — Voting, Stacking, Blending
=================================================================
Topics: hard/soft voting, stacking with out-of-fold predictions, blending,
        diversity, when ensembling is NOT worth the complexity

Why this matters for AI/backend engineering:
    Ensembles are how Kaggle winners and production teams squeeze the last
    few points: combine models that make DIFFERENT mistakes. But complexity
    costs money — knowing when NOT to ensemble is a real engineering skill.

Run:      python 34-ensembling.py
Verify:   python 34-ensembling.py --verify
Reference: https://scikit-learn.org/stable/modules/ensemble.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import (
    VotingClassifier, StackingClassifier, RandomForestClassifier,
    GradientBoostingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, accuracy_score

rng = np.random.RandomState(0)
X, y = make_classification(n_samples=3000, n_features=25, n_informative=12,
                           n_redundant=6, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

rf = RandomForestClassifier(n_estimators=100, random_state=0)
gb = GradientBoostingClassifier(n_estimators=100, random_state=0)
lr = LogisticRegression(max_iter=1000)

# ============================================================
# 1. Baseline — each model alone
# ============================================================
models = {"RF": rf, "GB": gb, "LR": lr}
scores = {}
for name, m in models.items():
    m.fit(Xtr, ytr)
    scores[name] = roc_auc_score(yte, m.predict_proba(Xte)[:, 1])
print("Example 1: single models")
for name, s in scores.items():
    print(f"  {name}: {s:.4f}")

# ============================================================
# 2. Hard voting — majority label
# ============================================================
voting_hard = VotingClassifier(
    estimators=[("rf", RandomForestClassifier(n_estimators=100, random_state=0)),
                ("gb", GradientBoostingClassifier(random_state=0)),
                ("lr", LogisticRegression(max_iter=1000))],
    voting="hard",
).fit(Xtr, ytr)
print("\nExample 2: hard voting")
print(f"  accuracy: {accuracy_score(yte, voting_hard.predict(Xte)):.4f}")

# ============================================================
# 3. Soft voting — average probabilities
# ============================================================
voting_soft = VotingClassifier(
    estimators=[("rf", RandomForestClassifier(n_estimators=100, random_state=0)),
                ("gb", GradientBoostingClassifier(random_state=0)),
                ("lr", LogisticRegression(max_iter=1000))],
    voting="soft",
    weights=[1, 1, 1],
).fit(Xtr, ytr)
print("\nExample 3: soft voting (probability averaging)")
print(f"  AUC: {roc_auc_score(yte, voting_soft.predict_proba(Xte)[:, 1]):.4f}")

# ============================================================
# 4. Stacking — meta-model learns how to combine
# ============================================================
stack = StackingClassifier(
    estimators=[("rf", RandomForestClassifier(n_estimators=100, random_state=0)),
                ("gb", GradientBoostingClassifier(random_state=0)),
                ("svc", SVC(probability=True, random_state=0))],
    final_estimator=LogisticRegression(max_iter=1000),
    cv=5,
).fit(Xtr, ytr)
print("\nExample 4: stacking (meta-model on out-of-fold preds)")
print(f"  AUC: {roc_auc_score(yte, stack.predict_proba(Xte)[:, 1]):.4f}")

# ============================================================
# 5. Manual blending — weighted average (production favorite)
# ============================================================
preds = {name: m.predict_proba(Xte)[:, 1] for name, m in models.items()}
blend = 0.5 * preds["GB"] + 0.3 * preds["RF"] + 0.2 * preds["LR"]
print("\nExample 5: manual blending (weighted average)")
print(f"  AUC: {roc_auc_score(yte, blend):.4f}")

# ============================================================
# 6. Diversity — why ensembles work
# ============================================================
# Check correlation of the models' probability vectors
corr_rf_gb = np.corrcoef(preds["RF"], preds["GB"])[0, 1]
print("\nExample 6: diversity")
print(f"  corr(RF, GB) = {corr_rf_gb:.3f}  (lower correlation -> more to gain)")

# ============================================================
# 7. When NOT to ensemble
# ============================================================
print("\n" + "=" * 60)
print("When NOT to ensemble:")
print("- The single best model is within 0.001 AUC of the ensemble")
print("- You must explain every prediction (SHAP on 5 models x3 harder)")
print("- Serving latency/cost budget is tight (5x inference)")
print("- Your data pipeline changes often (retrain every model)")
print("=" * 60)
print("Ensemble value = diversity. Same models = same mistakes.")
print("=" * 60)


def _verify() -> None:
    assert scores["GB"] > 0.5
    best_ensemble = max(roc_auc_score(yte, voting_soft.predict_proba(Xte)[:, 1]),
                        roc_auc_score(yte, stack.predict_proba(Xte)[:, 1]),
                        roc_auc_score(yte, blend))
    assert best_ensemble >= min(scores.values()) - 0.05, "ensemble should not be much worse"
    assert -1 <= corr_rf_gb <= 1
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
