# 03-libraries/pandas — 43: Pandas for Machine Learning

## Topic Overview

Pandas is the data layer of an ML system: raw logs in, feature matrix out.
The work splits into feature engineering (turning strings, dates, and
categories into numbers), honest splitting (no leakage), encoding
(`get_dummies` vs sklearn encoders), and the pandas-to-numpy handoff that
sklearn consumes.

For AI engineers the stakes are correctness: leakage inflates validation
scores, encoding drift breaks serving, and random splits on time-ordered
data train models on the future. This lecture establishes the three
contracts that keep ML plumbing honest — split first, fit on train only,
and keep the column contract between train and serve.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Engineer numeric features from raw mixed-type logs
2. Explain why `get_dummies` output drifts and how to align it
3. Fit a scaler on train only and transform test with train statistics
4. Choose a time-based split over a random split for time-ordered data
5. Hand a pandas frame to sklearn as a numpy matrix with a column contract
6. Use `ColumnTransformer` for mixed numeric/categorical pipelines
7. Build one honest `prepare_features` function for train and serve

## Prerequisites

| Need | Where |
|------|-------|
| dtypes & astype | `05-data-types-lecture.md` |
| groupby features | `42-groupby-internals-lecture.md` |
| numpy basics | `03-libraries/numpy` |

## 1. Feature Engineering — pandas Builds the X Matrix

Models consume plain numbers. Everything else — strings, dates, categories —
must become numbers before the fit.

```python
import numpy as np
import pandas as pd

np.random.seed(42)

raw = pd.DataFrame({
    "user_id": np.arange(1, 101),
    "signup": pd.date_range("2023-01-01", periods=100, freq="D"),
    "plan": np.random.choice(["free", "pro", "enterprise"], 100),
    "age": np.random.randint(18, 70, 100).astype(float),
})

engineered = raw.assign(
    days_since_epoch=lambda d: (d["signup"] - pd.Timestamp("2023-01-01")).dt.days,
    is_pro=lambda d: (d["plan"] == "pro").astype(int),
    is_enterprise=lambda d: (d["plan"] == "enterprise").astype(int),
    age_squared=lambda d: d["age"] ** 2,
)
print(engineered.columns.tolist())
```

```text
['user_id', 'signup', 'plan', 'age', 'days_since_epoch', 'is_pro', 'is_enterprise', 'age_squared']
```

Date subtraction yields integers; plan equality yields flags; polynomial
terms are plain arithmetic. All vectorized, all reviewable.

## 2. `get_dummies` — Simple, but Watch Column Drift

`get_dummies` expands categories into one column per value. The silent trap:
if the test set (or tomorrow's batch) lacks a category, the column sets
**differ** — and sklearn raises a shape error at predict time.

```python
train_cat = pd.DataFrame({"plan": ["free", "pro", "enterprise", "pro"]})
test_cat = pd.DataFrame({"plan": ["free", "pro"]})

train_d = pd.get_dummies(train_cat, prefix="plan")
test_d = pd.get_dummies(test_cat, prefix="plan")
print(train_d.columns.tolist())   # ['plan_enterprise', 'plan_free', 'plan_pro']
print(test_d.columns.tolist())    # ['plan_free', 'plan_pro']

test_aligned = test_d.reindex(columns=train_d.columns, fill_value=0)
print(test_aligned.columns.tolist())
```

```text
['plan_enterprise', 'plan_free', 'plan_pro']
['plan_free', 'plan_pro']
['plan_enterprise', 'plan_free', 'plan_pro']
```

The fix: reindex the test frame to the train columns, filling 0 for absent
categories. In production, the **training column list** is part of the model
artifact.

## 3. The Leakage Bug — Fit Transformers on Train Only

`StandardScaler` computes mean/std from whatever it fits. Fitting on the
full dataset leaks test statistics into training: the scaler centers test
values using them, and validation scores stop matching production.

```python
from sklearn.preprocessing import StandardScaler

train_vals = np.array([1.0, 2.0, 3.0])
test_vals = np.array([100.0, 200.0])

correct = StandardScaler().fit(train_vals.reshape(-1, 1))
leaky = StandardScaler().fit(np.concatenate([train_vals, test_vals]).reshape(-1, 1))

print(correct.mean_[0], correct.transform(test_vals.reshape(-1, 1)).ravel().round(1))
# 2.0 [120.0 242.5]
print(leaky.mean_[0], leaky.transform(test_vals.reshape(-1, 1)).ravel().round(1))
# 61.2 [0.5 1.8]
```

```text
2.0 [120.0 242.5]
61.2 [0.5 1.8]
```

With the honest scaler, extreme test values stay extreme (120, 242). With the
leaky one they collapse toward zero (0.5, 1.8) — the test set was part of
the fit, so the model saw "normalized" test data during training.

## 4. Splitting — Random Is Not Always Right

For time-ordered data, a random split leaks the future into training. Use a
chronological cutoff: train on the past, test on the future.

```python
time_series = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "value": np.random.RandomState(3).normal(size=100).cumsum(),
})
cutoff = pd.Timestamp("2024-03-15")
train_ts = time_series[time_series["date"] < cutoff]
test_ts = time_series[time_series["date"] >= cutoff]
print(len(train_ts), len(test_ts))   # 74 26 (2024 is a leap year)
```

```text
74 26
```

The rule generalizes: any feature for a row may only use information
available before that row's timestamp.

## 5. The pandas -> NumPy Handoff

sklearn consumes numpy arrays. The handoff has two classic bugs: carrying
the index (arrays have none) and losing column names. Extract `.to_numpy()`
at the last moment, keep the names next to the matrix, assert shapes.

```python
X = engineered[["days_since_epoch", "is_pro", "is_enterprise", "age"]].to_numpy()
y = engineered["age_squared"].to_numpy()

print(X.shape, X.dtype, y.shape)   # (100, 4) float64 (100,)
print(X[0].tolist())
```

```text
(100, 4) float64 (100,)
[0.0, 0.0, 1.0, 61.0]
```

## 6. `ColumnTransformer` — One Pipeline, Mixed Types

`ColumnTransformer` routes columns to different transformers and concatenates
the outputs — the safe replacement for hand-rolled `get_dummies` + scaling
in a serving pipeline.

```python
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
print(transformed.shape)   # (20, 3)
```

```text
(20, 3)
```

One object learns both pipelines on train and replays them exactly on test
and at serving — the drift problem disappears.

## 7. Production Pattern — One Honest Feature Function

The senior shape: one function that takes raw data and returns `(X,
feature_names, y)`, never looking at `y` to build `X`. Split first; fit on
train; transform train and test separately.

```python
def prepare_features(frame: pd.DataFrame, ref_date: pd.Timestamp,
                     target: str) -> tuple[np.ndarray, list[str], np.ndarray]:
    feats = frame.assign(
        days_since_ref=lambda d: (d["signup"] - ref_date).dt.days,
        is_pro=lambda d: (d["plan"] == "pro").astype(int),
        is_enterprise=lambda d: (d["plan"] == "enterprise").astype(int),
    )
    feature_names = ["days_since_ref", "is_pro", "is_enterprise", "age"]
    X = feats[feature_names].to_numpy(dtype=float)
    y = feats[target].to_numpy(dtype=float)
    return X, feature_names, y
```

The column contract (`feature_names`) is what you save next to the model —
and what reindexes serving-time dummies.

## Common Mistakes to Avoid

### Mistake 1: fitting the scaler on train+test together

```python
# WRONG — test statistics leak into training
scaler.fit(X_all); X_all = scaler.transform(X_all)
# CORRECT — fit on train only
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
```

### Mistake 2: `get_dummies` independently on train and test

```python
# WRONG — missing category in test -> column drift -> shape error
pd.get_dummies(test)
# CORRECT — align to the train columns
test_d.reindex(columns=train_d.columns, fill_value=0)
```

### Mistake 3: random split on time-ordered data

```python
# WRONG — the future leaks into training
train_test_split(X, y, random_state=42)
# CORRECT — chronological cutoff
train = df[df["date"] < cutoff]; test = df[df["date"] >= cutoff]
```

### Mistake 4: carrying the index into numpy

```python
# WRONG — np array has no index; misalignment is invisible
X = engineered[cols].values
# CORRECT — explicit, dtype-stable
X = engineered[cols].to_numpy(dtype=float)
```

## Best Practices

1. Split FIRST, then engineer and fit per split
2. Fit every transformer (scaler, encoder) on train only
3. Keep the train column list as a model artifact
4. Use `ColumnTransformer` for mixed pipelines
5. Convert to numpy with `.to_numpy(dtype=float)` at the last moment
6. Assert `X.shape` and `len(names)` before every fit
7. Reindex serving dummies to the train columns with `fill_value=0`
8. Time-split whenever timestamps exist

## Complexity and Cost

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `.assign` engineering pass | O(n) per column | O(n) | vectorized |
| `get_dummies` | O(n x categories) | O(n x categories) | wide frame risk |
| `reindex(fill_value=0)` | O(n x cols) | O(n) | drift fix, cheap |
| `StandardScaler.fit/transform` | O(n) | O(n) | two passes |
| `ColumnTransformer` | O(n) total | O(n) | one object, replayable |
| `.to_numpy()` | O(n) | O(n) | copy unless contiguous |

**At scale:** one-hot on a high-cardinality column (1M users) creates a
1M-column matrix — 8 GB of zeros. Use `OneHotEncoder(handle_unknown="ignore")`
or target/hash encoding instead, and measure the matrix's `nbytes` before
training.

## AI Engineering Relevance

**Where this shows up:** every training pipeline and every feature-service
endpoint — the same `prepare_features` must run in both.

| Concept here | Used for |
|--------------|----------|
| engineering pass | raw logs -> numeric features |
| no-leakage split | honest validation for time-ordered models |
| train-only fit | scaler/encoder statistics that generalize |
| column contract | train/serve consistency, saved with the model |
| `ColumnTransformer` | one replayable preprocessing object |

**Scale note:** at 1M rows leakage costs you a wrong model; at 100M rows it
costs you a wasted training run of hours and the confusion of a model that
"worked" offline. The contracts here are cheap to write and expensive to
skip.

## Practice Exercises

### Exercise 1: Dummy Alignment (Easy)
Build train/test dummies with one absent category, align test to train, and
verify the column sets match and absent values are zero.

### Exercise 2: Honest Scaling (Medium)
Fit `StandardScaler` on train only; verify the test transform uses train
mean/std and that a leaky fit produces different (wrong) test values.

### Exercise 3: Time Split (Medium)
From a daily series, split at a cutoff and verify no future date is in
train and no past date is in test.

### Exercise 4: Full Feature Pipeline (Hard)
Write `prepare_features` for the raw frame, split chronologically, fit a
scaler on train, transform both splits, and verify the test matrix's
columns match `feature_names`.

## Summary

| Concept | Description |
|---------|-------------|
| engineering | strings/dates -> numbers, vectorized |
| `get_dummies` drift | absent categories; fix with reindex |
| leakage | fitting statistics on the test set; fix by fit-on-train |
| time split | chronological cutoff for time-ordered data |
| numpy handoff | `.to_numpy()` + column contract |
| `ColumnTransformer` | one object for mixed preprocessing |

Pandas-for-ML is a correctness discipline: split first, fit on train only,
keep the column contract. Those three habits prevent the most expensive bug
class in applied ML — models that win on validation and fail in production.

## Quick Reference

| Task | Idiom |
|------|-------|
| Engineering pass | `df.assign(f=lambda d: ..., g=...)` |
| One-hot | `pd.get_dummies(df, prefix="col")` |
| Align dummies | `test_d.reindex(columns=train_d.columns, fill_value=0)` |
| Fit on train | `scaler.fit(X_train)` |
| Transform test | `scaler.transform(X_test)` |
| Time split | `train = df[df["date"] < cutoff]` |
| To numpy | `X = df[cols].to_numpy(dtype=float)` |
| Mixed pipeline | `ColumnTransformer([...]).fit_transform(X)` |

## Next Steps

Next: **[44 — Pandas Pitfalls](44-pandas-pitfalls-lecture.md)** — the
incidents every pandas user eventually ships.
Continues in: **[43 — Pandas for ML challenge](../challenges/43-pandas-for-ml/README.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/scale.html
and https://scikit-learn.org/stable/modules/compose.html
