"""
Challenge 43: Pandas for ML — Starter
======================================
Fill in the bodies. Do not change signatures or docstrings.
"""

from __future__ import annotations

import pandas as pd


def chrono_split(df: pd.DataFrame, frac: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """First frac rows = train, rest = test. No shuffle."""
    raise NotImplementedError


def fit_scale_train_test(X_train: pd.DataFrame, X_test: pd.DataFrame,
                         scaler) -> tuple[pd.DataFrame, pd.DataFrame, object]:
    """Fit scaler on train ONLY, transform both. Return scaled + fitted scaler."""
    raise NotImplementedError


def evaluate_no_leak_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
    """Chrono split, train-fit scaling, Ridge. (model, rmse, scaled_test)"""
    raise NotImplementedError


def evaluate_leaky_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
    """Chrono split, POOLED scaling (leak), Ridge. (model, rmse, scaled_test)"""
    raise NotImplementedError
