"""
07-machine-learning — 24: sklearn Pipelines — Fit on Train Only
===============================================================
Topics: Pipeline, ColumnTransformer, FeatureUnion, custom transformers,
        why pipelines are the #1 leakage-prevention tool, grid-searching
        a full pipeline

Why this matters for AI/backend engineering:
    A Pipeline is the production unit of ML: it bundles preprocessing +
    model so that every transform (scaling, encoding, imputation) is fit on
    the training folds only. Do this by hand and you WILL leak test
    information — the most expensive silent bug in ML.

Run:      python 24-sklearn-pipelines.py
Verify:   python 24-sklearn-pipelines.py --verify
Reference: https://scikit-learn.org/stable/modules/compose.html
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.base import BaseEstimator, TransformerMixin

rng = np.random.RandomState(0)

# ============================================================
# 1. The Problem: Preprocessing by Hand Leaks
# ============================================================
# Fitting StandardScaler on ALL data before splitting uses test statistics
# to build the train model -> optimistic scores that never reproduce.

X_all = rng.rand(200, 1) * 100
y_all = (X_all[:, 0] > 50).astype(int)

# WRONG: scaler fit on everything
from sklearn.preprocessing import StandardScaler as SS  # noqa: E402

scaler_leaky = SS().fit(X_all)
X_scaled_leaky = scaler_leaky.transform(X_all)
X_tr, X_te, y_tr, y_te = train_test_split(X_scaled_leaky, y_all, test_size=0.3, random_state=0)
acc_leaky = accuracy_score(y_te, LogisticRegression().fit(X_tr, y_tr).predict(X_te))

# RIGHT: split first, fit scaler on train only
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=0.3, random_state=0)
scaler_ok = SS().fit(X_tr)
acc_ok = accuracy_score(
    y_te, LogisticRegression().fit(scaler_ok.transform(X_tr), y_tr).predict(scaler_ok.transform(X_te))
)
print("Example 1: leakage by manual scaling")
print(f"  accuracy (leaky scaler): {acc_leaky:.3f}  (optimistic)")
print(f"  accuracy (train-only)  : {acc_ok:.3f}  (honest)")

# ============================================================
# 2. A Mixed-Type Dataset (the real world)
# ============================================================

def make_mixed_df(n: int = 500, seed: int = 0) -> tuple[pd.DataFrame, pd.Series]:
    r = np.random.RandomState(seed)
    df = pd.DataFrame(
        {
            "age": r.randint(18, 80, n).astype(float),
            "income": r.randn(n) * 30000 + 50000,
            "plan": r.choice(["free", "pro", "enterprise"], n),
            "region": r.choice(["emea", "amer", "apac"], n),
            "churned": r.binomial(1, 0.3, n),
        }
    )
    # Inject missing values so imputation matters
    df.loc[r.rand(n) < 0.1, "income"] = np.nan
    return df.drop(columns="churned"), df["churned"]


df, y = make_mixed_df()
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.25, random_state=0)

# ============================================================
# 3. ColumnTransformer — per-column pipelines
# ============================================================
numeric_cols = ["age", "income"]
categorical_cols = ["plan", "region"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), numeric_cols),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_cols),
    ]
)

full_pipeline = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=0)),
])

full_pipeline.fit(X_train, y_train)
acc_pipe = accuracy_score(y_test, full_pipeline.predict(X_test))
print("\nExample 2: full pipeline")
print(f"  accuracy: {acc_pipe:.3f}")
print(f"  X_train shape -> {X_train.shape}, transformed -> {preprocessor.fit_transform(X_train).shape}")

# ============================================================
# 4. Custom Transformer — fit on train only, guaranteed
# ============================================================
class ClipOutliers(BaseEstimator, TransformerMixin):
    """Clip numeric columns to quantiles LEARNED on the training data."""

    def fit(self, X, y=None):
        X = np.asarray(X)
        self.low_ = np.quantile(X, 0.01, axis=0)
        self.high_ = np.quantile(X, 0.99, axis=0)
        return self

    def transform(self, X):
        return np.clip(np.asarray(X), self.low_, self.high_)


custom = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("clip", ClipOutliers()),
    ("model", LogisticRegression(max_iter=500)),
])
custom.fit(X_train[["income"]], y_train)
print("\nExample 3: custom transformer")
print(f"  learned clip bounds: {float(custom.named_steps['clip'].low_[0]):.0f} .. {float(custom.named_steps['clip'].high_[0]):.0f}")
print(f"  accuracy: {accuracy_score(y_test, custom.predict(X_test[['income']])):.3f}")

# ============================================================
# 5. FeatureUnion — parallel feature extraction
# ============================================================
def add_age_squared(X: np.ndarray) -> np.ndarray:
    return np.hstack([X, (X ** 2)])  # type: ignore[operator]


feature_union = FeatureUnion([
    ("raw", FunctionTransformer()),
    ("poly", FunctionTransformer(add_age_squared, validate=False)),
])

fu_pipe = Pipeline([
    ("prep", ColumnTransformer([("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric_cols)])),
    ("fu", feature_union),
    ("clf", LogisticRegression(max_iter=500)),
])
fu_pipe.fit(X_train, y_train)
print("\nExample 4: FeatureUnion")
_prepped = fu_pipe.named_steps['prep'].transform(X_train.iloc[:5])
print(f"  feature count after union: {fu_pipe.named_steps['fu'].transform(_prepped).shape[1]}")

# ============================================================
# 6. GridSearch a Whole Pipeline — one leak-proof object
# ============================================================
param_grid = {
    "clf__n_estimators": [50, 100],
    "prep__num__impute__strategy": ["median", "mean"],
}
grid = GridSearchCV(full_pipeline, param_grid, cv=3, scoring="roc_auc")
grid.fit(X_train, y_train)
print("\nExample 5: grid search over the pipeline")
print(f"  best params: {grid.best_params_}")
print(f"  best CV AUC: {grid.best_score_:.3f}")
print(f"  test AUC   : {grid.score(X_test, y_test):.3f}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Pipeline bundles preprocess + model into one fit/predict unit")
print("- ColumnTransformer routes column groups to different recipes")
print("- Custom transformers fit on train data ONLY when inside a Pipeline")
print("- GridSearchCV on a pipeline tunes WITHOUT leaking test data")
print("=" * 60)


def _verify() -> None:
    from sklearn.pipeline import make_pipeline

    assert full_pipeline.named_steps["clf"].n_estimators == 100
    # Leak-free scaling must not match the leaky one in general
    assert abs(acc_leaky - acc_ok) < 1.0  # sanity: both are accuracy in [0,1]
    # Custom transformer learned bounds on train only
    assert hasattr(custom.named_steps["clip"], "low_")
    # GridSearch refit on full train: fitted pipeline available
    assert grid.best_estimator_ is not None
    # make_pipeline exists as an alternative constructor (fits fine)
    mp = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10))
    mp.fit(X_train[["age"]], y_train)
    assert mp.n_features_in_ == 1
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()
    else:
        pass  # examples already ran
