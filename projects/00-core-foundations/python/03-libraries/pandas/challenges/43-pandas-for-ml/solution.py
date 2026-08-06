"""
Challenge 43: Pandas for ML — Reference Solution
==================================================
Why this approach:
- chrono_split: head/tail on the original row order — the DataFrame's
  position IS the time axis here, so slicing is the honest split.
- fit_scale_train_test: scaler.fit(X_train) then transform both. Fitting on
  pooled data would embed test statistics into the transform — the leak.
- evaluate_no_leak_pipeline / evaluate_leaky_pipeline: the ONLY difference
  is what the scaler sees before transform. Models are always fit on train
  rows; the leak lives in the preprocessing step.
- rmse: mean of squared residuals, sqrt. Keep float64 end to end.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def chrono_split(df: pd.DataFrame, frac: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """First frac rows = train, rest = test. No shuffle."""
    n_train = int(np.floor(len(df) * frac))
    return df.iloc[:n_train].copy(), df.iloc[n_train:].copy()


def fit_scale_train_test(X_train: pd.DataFrame, X_test: pd.DataFrame,
                         scaler) -> tuple[pd.DataFrame, pd.DataFrame, object]:
    """Fit scaler on train ONLY, transform both. Return scaled + fitted scaler."""
    scaler.fit(X_train)
    train_scaled = pd.DataFrame(scaler.transform(X_train),
                                index=X_train.index, columns=X_train.columns)
    test_scaled = pd.DataFrame(scaler.transform(X_test),
                               index=X_test.index, columns=X_test.columns)
    return train_scaled, test_scaled, scaler


def _rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(np.sqrt(np.mean((y_true.to_numpy() - y_pred.to_numpy()) ** 2)))


def _build_scaled_test(df: pd.DataFrame, target: str, frac: float,
                       scaler, pooled: bool, alpha: float):
    train, test = chrono_split(df, frac)
    features = [c for c in df.columns if c != target]
    if pooled:
        scaler.fit(df[features])                      # LEAK: sees test stats
        train_scaled = pd.DataFrame(
            scaler.transform(train[features]),
            index=train.index, columns=features)
        test_scaled = pd.DataFrame(
            scaler.transform(test[features]),
            index=test.index, columns=features)
    else:
        train_scaled, test_scaled, _ = fit_scale_train_test(
            train[features], test[features], scaler)
    model = Ridge(alpha=alpha)   # scale-sensitive: the leak changes predictions
    model.fit(train_scaled, train[target])
    pred = pd.Series(model.predict(test_scaled), index=test.index)
    scaled_test = test_scaled.copy()
    scaled_test[target] = test[target].values
    scaled_test["prediction"] = pred.values
    return model, _rmse(test[target], pred), scaled_test


def evaluate_no_leak_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
    """Chrono split, train-fit scaling, Ridge. (model, rmse, scaled_test)"""
    return _build_scaled_test(df, target, frac, scaler, pooled=False, alpha=alpha)


def evaluate_leaky_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
    """Chrono split, POOLED scaling (leak), Ridge. (model, rmse, scaled_test)"""
    return _build_scaled_test(df, target, frac, scaler, pooled=True, alpha=alpha)
