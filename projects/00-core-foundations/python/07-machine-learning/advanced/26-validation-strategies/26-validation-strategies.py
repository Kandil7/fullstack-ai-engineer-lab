"""
07-machine-learning — 26: Validation Strategies — When CV Lies
==============================================================
Topics: KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit, nested CV
        for tuning, train/val/test discipline, when cross-validation
        gives a lying estimate

Why this matters for AI/backend engineering:
    The number your model reports is a CLAIM about production. Choosing the
    right splitter is how you make that claim true. A mismatched splitter
    (random CV on temporal data, unstratified CV on imbalance) produces
    confident, wrong numbers.

Run:      python 26-validation-strategies.py
Verify:   python 26-validation-strategies.py --verify
Reference: https://scikit-learn.org/stable/modules/cross_validation.html
"""

from __future__ import annotations

import numpy as np
from sklearn.model_selection import (
    KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit,
    train_test_split, GridSearchCV, cross_val_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

rng = np.random.RandomState(0)

X, y = make_classification(n_samples=1000, n_features=20, n_informative=8,
                           n_redundant=4, weights=[0.9, 0.1], random_state=0)

# ============================================================
# 1. KFold vs StratifiedKFold on imbalance
# ============================================================
kf = KFold(n_splits=5, shuffle=True, random_state=0)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

folds_kf = [y[t].mean() for _, t in kf.split(X, y)]
folds_skf = [y[t].mean() for _, t in skf.split(X, y)]
print("Example 1: class balance per fold")
print(f"  KFold positive rate per fold      : {np.round(folds_kf, 3)}")
print(f"  StratifiedKFold positive rate     : {np.round(folds_skf, 3)}  (stable)")

# ============================================================
# 2. GroupKFold — keep groups intact
# ============================================================
groups = np.repeat(np.arange(100), 10)  # 100 groups of 10 rows
Xg, yg = X[:1000], y[:1000]
gkf = GroupKFold(n_splits=5)
train_groups = []
for tr, te in gkf.split(Xg, yg, groups):
    train_groups.append(len(np.unique(groups[tr])))
print("\nExample 2: GroupKFold")
print(f"  unique training groups per fold: {train_groups}  (no group straddles)")

# ============================================================
# 3. TimeSeriesSplit — expanding window
# ============================================================
# 24 months of data, validate forward
month = np.repeat(np.arange(24), 100)
Xt, yt = X[:2400], np.repeat(y[:2400], 1)[:2400]
tss = TimeSeriesSplit(n_splits=4)
for tr, te in tss.split(Xt):
    pass  # tr is a prefix of te's past
first_train, first_test = next(iter(tss.split(Xt)))
assert max(first_train) < min(first_test), "time split must be strictly ordered"
print("\nExample 3: TimeSeriesSplit")
print("  every training fold ends BEFORE its test fold begins")

# ============================================================
# 4. Nested CV — tuning inside CV, not outside
# ============================================================
# WRONG pattern: pick best params on the whole train set, then report CV.
# The CV score is now optimistic (the data was used to choose params).
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
grid = GridSearchCV(RandomForestClassifier(random_state=0),
                    {"n_estimators": [50, 100]}, cv=3, scoring="roc_auc")
grid.fit(Xtr, ytr)
print("\nExample 4: nested CV")
print(f"  outer-model test AUC (honest holdout): {roc_auc_score(yte, grid.predict_proba(Xte)[:, 1]):.3f}")
print(f"  inner best CV AUC (slightly optimistic): {grid.best_score_:.3f}")

# Full nested CV: inner loop picks params, outer loop scores the pipeline
from sklearn.model_selection import cross_val_score as cvs  # noqa: E402

outer_aucs = []
for tr_outer, te_outer in skf.split(X, y):
    inner = GridSearchCV(RandomForestClassifier(random_state=0),
                         {"n_estimators": [50, 100]}, cv=3, scoring="roc_auc")
    inner.fit(X[tr_outer], y[tr_outer])
    outer_aucs.append(roc_auc_score(y[te_outer], inner.predict_proba(X[te_outer])[:, 1]))
print(f"  nested CV mean AUC: {np.mean(outer_aucs):.3f}  (the number to trust)")

# ============================================================
# 5. Train / Validation / Test Discipline
# ============================================================
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xva, yva, test_size=0.5, stratify=yva, random_state=0)
print("\nExample 5: the 3-way split")
print(f"  train {Xtr.shape[0]} / val {Xva.shape[0]} / test {Xte.shape[0]}  (60/20/20)")

# ============================================================
# 6. When CV Lies
# ============================================================
print("\n" + "=" * 60)
print("When CV lies:")
print("- Random KFold on TIME-ORDERED data (future leaks into train)")
print("- No stratification on rare classes (fold missing the minority)")
print("- Groups split across folds (same patient in train+test)")
print("- Tuning outside CV (param choice baked into the score)")
print("- Leaky preprocessing fit on all data before CV")
print("=" * 60)


def _verify() -> None:
    assert np.std(folds_skf) < np.std(folds_kf), "stratification must stabilize fold balance"
    for tr, te in gkf.split(Xg, yg, groups):
        assert len(set(groups[tr]) & set(groups[te])) == 0, "no group in both splits"
    for tr, te in tss.split(Xt):
        assert max(tr) < min(te), "time folds must be ordered"
    assert len(outer_aucs) == 5
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
