"""
07-machine-learning — 30: Gradient Boosting — The Tabular Champion
=================================================================
Topics: boosting intuition (additive trees), GradientBoosting vs
        HistGradientBoosting, early stopping, key hyperparameters,
        categorical handling, why GBDTs beat neural nets on tabular data

Why this matters for AI/backend engineering:
    On tabular data (90% of business ML), gradient-boosted trees win most
    Kaggle competitions and most production leaderboards. XGBoost/LightGBM
    are the same algorithm — this exercise builds the foundation with
    sklearn's own implementation.

Run:      python 30-gradient-boosting.py
Verify:   python 30-gradient-boosting.py --verify
Reference: https://scikit-learn.org/stable/modules/ensemble.html
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    GradientBoostingClassifier, HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.metrics import roc_auc_score, mean_squared_error

rng = np.random.RandomState(0)

# ============================================================
# 1. Boosting intuition — learn from your mistakes
# ============================================================
X, y = make_classification(n_samples=5000, n_features=20, n_informative=10,
                           n_redundant=3, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

gb = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0,
).fit(Xtr, ytr)
auc_gb = roc_auc_score(yte, gb.predict_proba(Xte)[:, 1])
print("Example 1: gradient boosting classifier")
print(f"  AUC: {auc_gb:.3f}")

# ============================================================
# 2. Early stopping — find the right number of trees
# ============================================================
Xtr2, Xva, ytr2, yva = train_test_split(Xtr, ytr, test_size=0.2, random_state=0)
gb_es = GradientBoostingClassifier(
    n_estimators=1000, learning_rate=0.05, max_depth=3,
    validation_fraction=0.2, n_iter_no_change=10, random_state=0,
)
gb_es.fit(Xtr2, ytr2)
print("\nExample 2: early stopping")
print(f"  trees actually used: {gb_es.n_estimators_} / 1000")

# ============================================================
# 3. HistGradientBoosting — fast on big data
# ============================================================
hgb = HistGradientBoostingClassifier(
    max_iter=200, learning_rate=0.1, max_depth=5, random_state=0,
).fit(Xtr, ytr)
print("\nExample 3: HistGradientBoosting (LightGBM-style)")
print(f"  AUC: {roc_auc_score(yte, hgb.predict_proba(Xte)[:, 1]):.3f}")

# ============================================================
# 4. Key hyperparameters and what they do
# ============================================================
print("\nExample 4: hyperparameter effects")
print("  n_estimators/max_iter : number of trees (capacity)")
print("  learning_rate         : step size per tree (lower -> need more trees)")
print("  max_depth             : tree depth (interaction order)")
print("  subsample             : row sampling (variance reduction)")
print("  min_samples_leaf      : regularization (smoother predictions)")
print("  n_iter_no_change      : early stopping patience")

# ============================================================
# 5. Categorical handling (native in HistGB)
# ============================================================
import pandas as pd  # noqa: E402

cat_df = pd.DataFrame({
    "num": rng.randn(2000),
    "cat": rng.choice(["a", "b", "c", "d"], 2000),
})
cat_y = ((cat_df["num"] + (cat_df["cat"] == "a") * 2 + rng.randn(2000) > 0)).astype(int)

hgb_cat = HistGradientBoostingClassifier(
    categorical_features=[1], max_iter=100, random_state=0,
).fit(cat_df, cat_y)
print("\nExample 5: native categorical support (HistGB)")
print(f"  AUC with categorical column handled natively: {roc_auc_score(cat_y, hgb_cat.predict_proba(cat_df)[:, 1]):.3f}")

# ============================================================
# 6. Why GBDTs beat NNs on tabular — regression demo
# ============================================================
Xr, yr = fetch_california_housing(return_X_y=True)
Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(Xr, yr, test_size=0.3, random_state=0)
hgb_r = HistGradientBoostingClassifier(
    max_iter=150, learning_rate=0.08, random_state=0,
)
hgb_r.fit(Xr_tr, (yr_tr > yr_tr.mean()).astype(int))
auc_reg = roc_auc_score((yr_te > yr_tr.mean()).astype(int), hgb_r.predict_proba(Xr_te)[:, 1])
rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xr_tr, (yr_tr > yr_tr.mean()).astype(int))
auc_rf = roc_auc_score((yr_te > yr_tr.mean()).astype(int), rf.predict_proba(Xr_te)[:, 1])
print("\nExample 6: GBDT vs RandomForest (house price > median)")
print(f"  HistGB AUC : {auc_reg:.3f}")
print(f"  RF AUC     : {auc_rf:.3f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Boosting = additive sequence of shallow trees, each fixing errors")
print("- learning_rate vs n_estimators tradeoff (use early stopping)")
print("- HistGradientBoosting scales to big data + native categoricals")
print("- GBDTs are the default for tabular; NNs win on text/image/sound")
print("=" * 60)


def _verify() -> None:
    assert auc_gb > 0.7, "clean synthetic data should fit well"
    assert gb_es.n_estimators_ < 1000, "early stopping must stop early"
    assert hgb.n_features_in_ == 20
    assert abs(len(cat_df) - 2000) == 0
    assert 0.5 < auc_reg < 1.0
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
