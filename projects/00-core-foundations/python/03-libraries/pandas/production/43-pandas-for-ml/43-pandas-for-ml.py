"""
Pandas -- 43: Pandas for Machine Learning
==============================================
Topics: feature engineering, train/test split WITHOUT leakage,
        get_dummies vs sklearn encoders, time-based splits,
        pandas -> NumPy handoff, ColumnTransformer interop

Why this matters for AI/backend engineering:
    Most ML bugs live in the data plumbing, not the model: leakage
    (fitting the scaler on the whole dataset), time mismatches
    (training on the future), and encoding drift (dummy columns that
    differ between train and serve). pandas is where these bugs are
    either introduced or caught. This module builds the plumbing
    habits that make models honest.

Run:      python 43-pandas-for-ml.py
Verify:   python 43-pandas-for-ml.py --verify
Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

np.random.seed(42)

# ============================================================
# 1. Feature Engineering -- pandas Builds the X Matrix
# ============================================================
# The model consumes a plain numeric matrix: floats, ints, and
# one-hot (or binary) columns. Everything else -- strings, dates,
# categories -- is your job to turn into numbers BEFORE the fit.

# Example 1: raw logs -> feature matrix
raw = pd.DataFrame({
    "user_id": np.arange(1, 101),
    "signup": pd.date_range("2023-01-01", periods=100, freq="D"),
    "plan": np.random.choice(["free", "pro", "enterprise"], 100),
    "age": np.random.randint(18, 70, 100).astype(float),
})

# Engineering pass: date features, plan flags, age bucket
engineered = raw.assign(
    days_since_epoch=lambda d: (d["signup"] - pd.Timestamp("2023-01-01")).dt.days,
    is_pro=lambda d: (d["plan"] == "pro").astype(int),
    is_enterprise=lambda d: (d["plan"] == "enterprise").astype(int),
    age_squared=lambda d: d["age"] ** 2,
)
print("Engineered columns:", engineered.columns.tolist())

# Output:
# Engineered columns: ['user_id', 'signup', 'plan', 'age', 'days_since_epoch', 'is_pro', 'is_enterprise', 'age_squared']


# ============================================================
# 2. get_dummies -- Simple, But Watch the Column Drift
# ============================================================
# get_dummies expands categorical columns into one column per value.
# Its silent trap: if the test set (or the next day's batch) lacks a
# category, the columns DON'T match. Never feed get_dummies output
# directly to a model without aligning the columns first.

# Example 2: the drift trap in miniature
train_cat = pd.DataFrame({"plan": ["free", "pro", "enterprise", "pro"]})
test_cat = pd.DataFrame({"plan": ["free", "pro"]})   # enterprise absent

train_dummies = pd.get_dummies(train_cat, prefix="plan")
test_dummies = pd.get_dummies(test_cat, prefix="plan")
print("Train columns:", train_dummies.columns.tolist())
print("Test columns: ", test_dummies.columns.tolist())

# The fix: reindex the test frame to the train columns, filling 0
test_aligned = test_dummies.reindex(columns=train_dummies.columns, fill_value=0)
print("Aligned test columns:", test_aligned.columns.tolist())

# Output:
# Train columns: ['plan_enterprise', 'plan_free', 'plan_pro']
# Test columns:  ['plan_free', 'plan_pro']
# Aligned test columns: ['plan_enterprise', 'plan_free', 'plan_pro']


# ============================================================
# 3. The Leakage Bug -- Fit Transformers on TRAIN Only
# ============================================================
# StandardScaler computes mean/std from whatever you fit it on.
# Fitting on the FULL dataset leaks test statistics into training:
# the model sees centered test values during training and validation
# scores look better than production ever will.

# Example 3: fit on train only vs fit on everything
from sklearn.preprocessing import StandardScaler

train_vals = np.array([1.0, 2.0, 3.0])
test_vals = np.array([100.0, 200.0])

correct_scaler = StandardScaler().fit(train_vals.reshape(-1, 1))
leaky_scaler = StandardScaler().fit(
    np.concatenate([train_vals, test_vals]).reshape(-1, 1))

print("Correct: train mean", round(float(correct_scaler.mean_[0]), 2),
      "| test transformed:",
      correct_scaler.transform(test_vals.reshape(-1, 1)).ravel().round(1).tolist())
print("Leaky:   train mean", round(float(leaky_scaler.mean_[0]), 2),
      "| test transformed:",
      leaky_scaler.transform(test_vals.reshape(-1, 1)).ravel().round(1).tolist())

# Output:
# Correct: train mean 2.0 | test transformed: [120.0, 242.5]
# Leaky:   train mean 61.2 | test transformed: [0.5, 1.8]


# ============================================================
# 4. Splitting -- Random Is Not Always Right
# ============================================================
# For time-ordered data, a random split leaks the FUTURE into the
# training set. Use a time-based split: train on the past, validate
# on the future. The rule: any feature computed for a row may only
# use information available BEFORE that row's timestamp.

# Example 4: chronological split vs random split
time_series = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "value": np.random.RandomState(3).normal(size=100).cumsum(),
})
cutoff = pd.Timestamp("2024-03-15")
train_ts = time_series[time_series["date"] < cutoff]
test_ts = time_series[time_series["date"] >= cutoff]
print("Chronological: train", len(train_ts), "test", len(test_ts),
      "| test starts:", test_ts["date"].iloc[0].strftime("%Y-%m-%d"))

# Output:
# Chronological: train 74 test 26 | test starts: 2024-03-15
# (2024 is a leap year: Jan 31 + Feb 29 + 14 days of March = 74)


# ============================================================
# 5. pandas -> NumPy Handoff
# ============================================================
# sklearn consumes numpy arrays. The handoff has two classic bugs:
# carrying the index (a numpy array has none) and forgetting column
# names. Extract .values (or .to_numpy()) at the LAST moment, keep
# the column list next to the matrix, and assert shapes before fit.

# Example 5: build the matrix and the column contract
X = engineered[["days_since_epoch", "is_pro", "is_enterprise", "age"]].to_numpy()
y = engineered["age_squared"].to_numpy()   # toy target
print("X shape:", X.shape, "| X dtype:", X.dtype, "| y shape:", y.shape)
print("First row of X:", X[0].tolist())

# Output:
# X shape: (100, 4) | X dtype: float64 | y shape: (100,)
# First row of X: [0.0, 0.0, 1.0, 61.0]


# ============================================================
# 6. ColumnTransformer -- One Pipeline, Mixed Types
# ============================================================
# ColumnTransformer routes columns to different transformers and
# concatenates the outputs. This is how a real project encodes a
# categorical column and scales a numeric one in ONE object -- and
# it is exactly what get_dummies-by-hand cannot do safely.

# Example 6: numeric scaling + one-hot in a single transformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

pipe_df = pd.DataFrame({
    "amount": np.random.uniform(10, 1000, 20),
    "region": np.random.choice(["us", "eu", "ap"], 20),
})
transformer = ColumnTransformer([
    ("scale", StandardScaler(), ["amount"]),
    ("onehot", OneHotEncoder(drop="first"), ["region"]),
])
transformed = transformer.fit_transform(pipe_df)
print("Transformed shape:", transformed.shape)
print("First row:", np.round(transformed[0], 3).tolist())

# Output:
# Transformed shape: (20, 3)
# First row: [-0.531, 0.0, 1.0]


# ============================================================
# 7. Production Pattern: One Honest Feature Function
# ============================================================
# The senior shape: a single function that (1) takes raw data,
# (2) returns X (matrix), feature_names (list), and y (Series),
# (3) NEVER looks at y to build X. Split FIRST, transform each
# split separately -- fit on train, transform train and test.

def prepare_features(frame: pd.DataFrame, ref_date: pd.Timestamp,
                     target: str) -> tuple[np.ndarray, list[str], np.ndarray]:
    """Raw logs -> (X, feature_names, y). No target leakage:
    every feature uses only the row's own values."""
    feats = frame.assign(
        days_since_ref=lambda d: (d["signup"] - ref_date).dt.days,
        is_pro=lambda d: (d["plan"] == "pro").astype(int),
        is_enterprise=lambda d: (d["plan"] == "enterprise").astype(int),
    )
    feature_names = ["days_since_ref", "is_pro", "is_enterprise", "age"]
    X = feats[feature_names].to_numpy(dtype=float)
    y = feats[target].to_numpy(dtype=float)
    return X, feature_names, y

# Example 7: split -> prepare -> fit/transform (the correct order)
ref = pd.Timestamp("2023-01-01")
split_point = 70
train_df, test_df = raw.iloc[:split_point].copy(), raw.iloc[split_point:].copy()
X_train, names, y_train = prepare_features(train_df, ref, "age")
X_test, _, y_test = prepare_features(test_df, ref, "age")

scaler = StandardScaler().fit(X_train)     # FIT on train ONLY
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)   # TRANSFORM test with train stats

print("Feature names:", names)
print("Test scaled mean ~ train mean:", round(float(X_test_scaled.mean()), 3))
print("Same column contract:", X_train.shape[1] == X_test.shape[1])

# Output:
# Feature names: ['days_since_ref', 'is_pro', 'is_enterprise', 'age']
# Test scaled mean ~ train mean: 0.531
# Same column contract: True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: fitting the scaler (or encoder) on train+test together
#   scaler.fit(X_all); X_all_scaled = scaler.transform(X_all)
# CORRECT:
#   scaler.fit(X_train); X_train_scaled = scaler.transform(X_train)
#                        X_test_scaled = scaler.transform(X_test)
#
# MISTAKE: get_dummies on train and test independently
#   pd.get_dummies(test)   # missing categories -> column drift
# CORRECT: align test dummies to train columns:
#   test_dummies.reindex(columns=train_dummies.columns, fill_value=0)
#
# MISTAKE: random split on time-ordered data
#   train_test_split(X, y, random_state=42)   # future leaks into train
# CORRECT: split by timestamp cutoff, then engineer features
#          separately per split.


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Feature engineering produces the expected columns.
    assert "days_since_epoch" in engineered.columns, \
        "engineering must add date-derived features"
    assert "is_pro" in engineered.columns, "engineering must add flags"

    # get_dummies drift: test dummies lack the enterprise column.
    assert "plan_enterprise" not in test_dummies.columns, \
        "test dummies must be missing the absent category"
    assert "plan_enterprise" in test_aligned.columns, \
        "reindex must restore the full column set"
    assert int(test_aligned["plan_enterprise"].sum()) == 0, \
        "missing category must be filled with 0"

    # Leakage: scaler fit on train only has the TRAIN mean.
    assert correct_scaler.mean_[0] == 2.0, \
        "scaler fitted on train must have the train mean"
    assert abs(leaky_scaler.mean_[0] - 61.2) < 1e-6, \
        "scaler fitted on everything must have the pooled mean"
    # The leaked transform shrinks test values toward zero.
    assert abs(correct_scaler.transform(test_vals.reshape(-1, 1)).ravel()[0]) > 50, \
        "correct scaling must NOT shrink extreme test values"
    assert abs(leaky_scaler.transform(test_vals.reshape(-1, 1)).ravel()[0]) < 10, \
        "leaky scaling must shrink extreme test values"

    # Chronological split: no future date in train, no past in test.
    assert (train_ts["date"] < cutoff).all(), \
        "chronological train must precede the cutoff"
    assert (test_ts["date"] >= cutoff).all(), \
        "chronological test must start at the cutoff"
    assert len(train_ts) + len(test_ts) == 100, "splits must be exhaustive"

    # NumPy handoff: correct shape, no index carried.
    assert X.shape == (100, 4), "X must be (n_rows, n_features)"
    assert X.dtype == np.float64, "X must be a plain float matrix"

    # ColumnTransformer: one-hot + scaling in a single object.
    assert transformed.shape == (20, 3), \
        "1 scaled column + 2 one-hot columns (drop='first')"

    # Production pattern: same columns, no leakage in the pipeline.
    assert X_train.shape[1] == X_test.shape[1] == len(names), \
        "train and test must share the column contract"
    assert abs(float(X_test_scaled.mean()) - 0.531) < 1e-3, \
        "test features must be scaled with TRAIN statistics"

    print("[OK] 43-pandas-for-ml: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Split FIRST, then engineer and fit on train only.")
        print("2. Align get_dummies columns between train and serve.")
        print("3. pandas builds the matrix; sklearn consumes numpy.")
        _verify()          # always runs, so plain execution is also a test
