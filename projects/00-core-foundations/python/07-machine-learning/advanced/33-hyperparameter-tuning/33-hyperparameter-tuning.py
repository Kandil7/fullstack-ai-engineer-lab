"""
07-machine-learning — 33: Hyperparameter Tuning — Search Inside CV
=================================================================
Topics: grid vs random vs Bayesian search, Optuna (installed), pruning,
        search-space design, THE rule: tuning inside CV, not outside

Why this matters for AI/backend engineering:
    Tuning is where most leakage sneaks in: pick best params on the full
    dataset, report a CV score, and you have an optimistic number that never
    reproduces. Tuning belongs INSIDE cross-validation, and Bayesian search
    (Optuna) beats grid/random hands down on cost.

Run:      python 33-hyperparameter-tuning.py
Verify:   python 33-hyperparameter-tuning.py --verify
Reference: https://optuna.readthedocs.io/
"""

from __future__ import annotations

import numpy as np
import optuna
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

optuna.logging.set_verbosity(optuna.logging.WARNING)

rng = np.random.RandomState(0)
X, y = make_classification(n_samples=3000, n_features=25, n_informative=12,
                           n_redundant=5, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

# ============================================================
# 1. Grid search — exhaustive but expensive
# ============================================================
from sklearn.model_selection import GridSearchCV  # noqa: E402

grid = GridSearchCV(
    RandomForestClassifier(random_state=0),
    {"n_estimators": [50, 100, 200], "max_depth": [5, 10, None]},
    cv=3, scoring="roc_auc", n_jobs=-1,
)
grid.fit(Xtr, ytr)
print("Example 1: grid search (9 combos)")
print(f"  best params: {grid.best_params_}  best CV AUC: {grid.best_score_:.3f}")

# ============================================================
# 2. Random search — same budget, better coverage
# ============================================================
from sklearn.model_selection import RandomizedSearchCV  # noqa: E402

param_dist = {
    "n_estimators": [50, 100, 200, 300],
    "max_depth": [3, 5, 10, None],
    "min_samples_leaf": [1, 2, 5, 10],
}
rnd = RandomizedSearchCV(RandomForestClassifier(random_state=0), param_dist,
                         n_iter=15, cv=3, scoring="roc_auc", n_jobs=-1, random_state=0)
rnd.fit(Xtr, ytr)
print("\nExample 2: random search (15 of 64 combos)")
print(f"  best params: {rnd.best_params_}  best CV AUC: {rnd.best_score_:.3f}")

# ============================================================
# 3. Optuna — Bayesian search (adaptive, efficient)
# ============================================================
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
        "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2", None]),
        "criterion": trial.suggest_categorical("criterion", ["gini", "entropy"]),
    }
    model = RandomForestClassifier(random_state=0, n_jobs=-1, **params)
    return cross_val_score(model, Xtr, ytr, cv=3, scoring="roc_auc").mean()


study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=0))
study.optimize(objective, n_trials=20)
print("\nExample 3: Optuna Bayesian search (20 trials)")
print(f"  best AUC: {study.best_value:.3f}")
print(f"  best params: {study.best_params}")

# ============================================================
# 4. Pruning — stop unpromising trials early
# ============================================================
def objective_pruned(trial):
    n_est = trial.suggest_int("n_estimators", 50, 300)
    model = RandomForestClassifier(n_estimators=n_est, random_state=0, n_jobs=-1)
    return cross_val_score(model, Xtr, ytr, cv=3, scoring="roc_auc").mean()


study2 = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=0))
study2.optimize(objective_pruned, n_trials=10)
print("\nExample 4: Optuna with early pruning pattern")
print(f"  best AUC after 10 trials: {study2.best_value:.3f}")

# ============================================================
# 5. Tuning inside CV — the honest way
# ============================================================
from sklearn.model_selection import KFold  # noqa: E402

outer_aucs = []
for tr_o, va_o in KFold(5, shuffle=True, random_state=0).split(Xtr):
    inner = GridSearchCV(LogisticRegression(max_iter=1000),
                         {"C": [0.01, 0.1, 1, 10]}, cv=3, scoring="roc_auc")
    inner.fit(Xtr[tr_o], ytr[tr_o])
    outer_aucs.append(roc_auc_score(ytr[va_o], inner.predict_proba(Xtr[va_o])[:, 1]))
print("\nExample 5: tuning inside CV (nested)")
print(f"  nested mean AUC: {np.mean(outer_aucs):.3f}  <- the honest number")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Grid: exhaustive, fine for 1-2 dims")
print("- Random: better coverage per trial on many dims")
print("- Optuna/Bayesian: adapts, best cost-to-quality ratio")
print("- ALWAYS tune inside CV (nested) to get honest scores")
print("- Never peek at the test set while tuning")
print("=" * 60)


def _verify() -> None:
    assert grid.best_score_ > 0.5
    assert rnd.n_iter == 15
    assert study.best_value > 0.5
    assert len(outer_aucs) == 5
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
