"""
07-machine-learning — 32: Feature Selection — Fewer, Better Features
===================================================================
Topics: filter (variance, correlation), wrapper (RFE), embedded
        (SelectFromModel, L1, tree importance), multicollinearity/VIF,
        permutation importance, stability

Why this matters for AI/backend engineering:
    Feature selection is a cost optimization: fewer features = cheaper
    pipelines, faster training, less overfitting, easier deployment and
    monitoring. It also removes noise that silently degrades models.

Run:      python 32-feature-selection.py
Verify:   python 32-feature-selection.py --verify
Reference: https://scikit-learn.org/stable/modules/feature_selection.html
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import (
    RFE, SelectFromModel, VarianceThreshold, mutual_info_classif, f_classif,
    SelectKBest,
)
from sklearn.metrics import roc_auc_score

rng = np.random.RandomState(0)

# 40 features, only 10 informative + 10 redundant (so ~20 useful)
X, y = make_classification(n_samples=3000, n_features=40, n_informative=10,
                           n_redundant=10, n_repeated=2, random_state=0)
feature_names = [f"f{i}" for i in range(40)]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

# ============================================================
# 1. Filter methods — cheap, model-agnostic
# ============================================================
print("Example 1: filter methods")
# Variance: drop near-constant features
sel_v = VarianceThreshold(threshold=0.05)
n_kept_v = sel_v.fit(Xtr).transform(Xtr).shape[1]
print(f"  VarianceThreshold kept {n_kept_v}/40")

# Univariate: ANOVA F or mutual information, keep top k
skb = SelectKBest(f_classif, k=20).fit(Xtr, ytr)
print(f"  SelectKBest(ANOVA, k=20) selected {skb.get_support().sum()} features")

mi = mutual_info_classif(Xtr, ytr)
print(f"  top-5 mutual information: {np.argsort(mi)[-5:][::-1]}")

# ============================================================
# 2. Wrapper: RFE — recursive elimination
# ============================================================
print("\nExample 2: RFE (recursive feature elimination)")
rfe = RFE(LogisticRegression(max_iter=1000), n_features_to_select=15)
rfe.fit(Xtr, ytr)
print(f"  ranking (1 = kept): {rfe.ranking_}")
print(f"  selected {rfe.n_features_} features")

# ============================================================
# 3. Embedded: L1 + tree importance + SelectFromModel
# ============================================================
print("\nExample 3: embedded methods")
l1 = LogisticRegression(penalty="l1", solver="liblinear", C=0.5, max_iter=1000).fit(Xtr, ytr)
n_l1 = (np.abs(l1.coef_[0]) > 1e-6).sum()
print(f"  L1 zeroed {40 - n_l1}/40 coefficients")

sfm = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=0), threshold="median")
sfm.fit(Xtr, ytr)
print(f"  SelectFromModel(RF, median) kept {sfm.transform(Xtr).shape[1]} features")

# ============================================================
# 4. Multicollinearity & VIF
# ============================================================
def vif(X_cols: np.ndarray, names: list[str]) -> pd.Series:
    """Variance Inflation Factor per column via aux regressions."""
    from sklearn.linear_model import LinearRegression

    out = {}
    for i, name in enumerate(names):
        y_col = X_cols[:, i]
        x_cols = np.delete(X_cols, i, axis=1)
        r2 = LinearRegression().fit(x_cols, y_col).score(x_cols, y_col)
        out[name] = 1.0 / (1.0 - r2)
    return pd.Series(out)


X_redundant = X[:, :12]  # includes redundant/repeated block
vif_scores = vif(X_redundant, feature_names[:12])
print("\nExample 4: VIF (multicollinearity)")
print(vif_scores.round(1))
print("  VIF > 10 suggests a column is predictable from the others")

# ============================================================
# 5. Permutation importance — how much each feature matters
# ============================================================
print("\nExample 5: permutation importance")
rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)
from sklearn.inspection import permutation_importance  # noqa: E402

pi = permutation_importance(rf, Xte, yte, n_repeats=5, random_state=0)
order = np.argsort(pi.importances_mean)[::-1]
print("  top 5 by permutation importance:", [feature_names[i] for i in order[:5]])

# ============================================================
# 6. Stability — selection should not flip on resamples
# ============================================================
sel_sets = []
for seed in range(5):
    Xs, Xs2, ys, ys2 = train_test_split(X, y, test_size=0.3, random_state=seed)
    s = SelectKBest(f_classif, k=15).fit(Xs, ys)
    sel_sets.append(set(np.where(s.get_support())[0]))
overlap = len(set.intersection(*sel_sets)) / 15
print(f"\nExample 6: stability across 5 resamples -> {overlap:.0%} overlap")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Filter: fast, model-agnostic (variance, F, mutual info)")
print("- Wrapper (RFE): model-aware but expensive")
print("- Embedded: L1 zeros weights, trees rank by importance")
print("- VIF > 10: collinear columns to drop")
print("- Validate selection stability before shipping")
print("=" * 60)


def _verify() -> None:
    assert n_kept_v <= 40 and n_kept_v >= 0
    assert rfe.n_features_ == 15
    assert n_l1 < 40, "L1 must zero some coefficients"
    assert 0 <= overlap <= 1
    assert pi.importances_mean.shape[0] == 40
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
