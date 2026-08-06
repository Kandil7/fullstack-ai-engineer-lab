# Pandas for ML Quiz (Topic 43)

## Topic Overview
This quiz covers the pandas↔scikit-learn interface: train/test splits,
feature matrices vs targets, scaling without leakage, ColumnTransformer,
categorical encodings, dummies vs category dtype, pipelines, and honest
evaluation.

**Difficulty:** Intermediate to Advanced
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What shape does scikit-learn expect for the feature matrix X?**

A) A list
B) 2D — (n_samples, n_features)
C) 1D — (n_features,)
D) A dict of columns

**Correct Answer:** B
**Explanation:** X must be 2D: rows are samples, columns are features. A
single feature still needs shape (n, 1) or (n, 1)-like — `df[["x"]]`, not
`df["x"]`.

---

### Question 2 [Easy]
**What does `StandardScaler().fit_transform(X)` do?**

A) Fits the model on X
B) Learns mean/std from X and returns scaled X
C) Drops outliers
D) Converts X to category dtype

**Correct Answer:** B
**Explanation:** `fit` learns the mean and standard deviation of each
column; `transform` applies (x - mean) / std. `fit_transform` does both on
the SAME data — dangerous on test data.

---

### Question 3 [Easy]
**Why should you never `fit_transform` the test set?**

A) It is slow
B) It leaks test statistics into the scaler, so test features are no longer
truly unseen
C) It raises an error
D) It changes column names

**Correct Answer:** B
**Explanation:** The scaler must learn mean/std from TRAIN ONLY, then
`transform` (not fit) the test. Fitting on pooled data embeds test
information into the preprocessing — a classic leakage.

---

### Question 4 [Easy]
**What does `pd.get_dummies(df["color"])` produce?**

A) A single column
B) One 0/1 column per distinct color value
C) A Series of strings
D) A category dtype

**Correct Answer:** B
**Explanation:** `get_dummies` one-hot encodes: each distinct value becomes
a column of 0/1 indicators. It expands the column instead of compacting it
(that is `astype("category")`).

---

### Question 5 [Easy]
**Which of these is the correct target vector for classification?**

A) A 2D DataFrame of one column
B) A 1D Series of labels
C) A list of feature names
D) A scaler

**Correct Answer:** B
**Explanation:** y is 1D — one label per row. X is 2D, y is 1D. Passing a
single-column DataFrame as y works but warns in newer sklearn.

---

### Question 6 [Easy]
**What does `train_test_split(X, y, test_size=0.2)` return?**

A) One tuple
B) Four objects: X_train, X_test, y_train, y_test
C) Two objects
D) A dict

**Correct Answer:** B
**Explanation:** The classic 4-tuple unpack:
`X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)`.
The default `shuffle=True` is random — wrong for time-ordered data.

---

### Question 7 [Medium]
**Why must a time-ordered dataset be split WITHOUT shuffle?**

A) Shuffle is slower
B) Shuffling lets future rows enter training — a chronological split keeps
the max train date <= the min test date
C) Shuffle breaks dtypes
D) It does not matter

**Correct Answer:** B
**Explanation:** Random splitting on time series leaks the future into
training. `chrono_split` in the challenge takes the FIRST frac of rows as
train — the honest order-preserving split.

---

### Question 8 [Medium]
**What is the output of the following?**

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
X = pd.DataFrame({"x": [0.0, 2.0]})
sc = StandardScaler().fit(X)
print(sc.transform(pd.DataFrame({"x": [0.0, 10.0]}))["x"].tolist())
```

A) `[0.0, 10.0]`
B) `[-1.0, 9.0]` — train mean 1, std 1
C) `[0.0, 5.0]`
D) `[-1.0, 5.0]`

**Correct Answer:** B
**Explanation:** The scaler learned mean=1, std=1 from [0, 2]. Test values
transform as (0-1)/1 = -1.0 and (10-1)/1 = 9.0. Scaling uses TRAIN
statistics, not the test's own.

---

### Question 9 [Medium]
**Why does a scaling leak change Ridge predictions but NOT plain
LinearRegression predictions?**

A) Ridge is random
B) OLS is invariant to affine feature transforms — the model absorbs the
shift/scale into its coefficients; Ridge's penalty depends on coefficient
magnitude, which changes with scale
C) LinearRegression cannot be scaled
D) Ridge ignores X

**Correct Answer:** B
**Explanation:** For OLS, scaling X is absorbed by adjusting w and b — the
fitted function (and RMSE) is identical. Ridge penalizes ||w||², so the
scale of X changes the solution — which is exactly why the leak shows up as
different RMSE. This is why leakage demos need a scale-sensitive model.

---

### Question 10 [Medium]
**Which sklearn estimator should be used for a continuous target with
leakage-aware scaling in a pipeline?**

A) `LinearRegression`
B) `Ridge(alpha=...)` or another scale-sensitive regressor inside a
`Pipeline([("scaler", StandardScaler()), ("model", ...)])`
C) `KNeighborsRegressor` with a single feature
D) `LogisticRegression`

**Correct Answer:** B
**Explanation:** A Pipeline fits the scaler on train folds and transforms
test with train statistics automatically. B is the honest design; C with a
single feature is scale-invariant for neighbor ORDER (monotone scaling
preserves it) and makes a poor leak demo.

---

### Question 11 [Medium]
**What does `ColumnTransformer` allow you to do?**

A) Replace all columns with their mean
B) Apply DIFFERENT transformers to different column groups in one step
C) Merge two DataFrames
D) Drop duplicate columns

**Correct Answer:** B
**Explanation:** `ColumnTransformer([("num", StandardScaler(), num_cols),
("cat", OneHotEncoder(), cat_cols)])` applies per-group preprocessing and
concatenates the results — the standard mixed-type feature builder.

---

### Question 12 [Medium]
**What is the output of the following?**

```python
import pandas as pd
df = pd.DataFrame({"v": [1.0, 2.0, 3.0], "c": ["a", "b", "a"]})
print(pd.get_dummies(df["c"]).shape)
```

A) `(3, 2)`
B) `(2, 3)`
C) `(3, 1)`
D) `(3, 3)`

**Correct Answer:** A
**Explanation:** 3 rows, 2 distinct categories (a, b) → one-hot matrix of
shape (3, 2): columns "a" and "b" with 0/1 indicators.

---

### Question 13 [Medium]
**Why is `df["color"].astype("category")` NOT a replacement for
`get_dummies` in a model?**

A) It is slower
B) Models need numeric columns; category labels are codes that a linear
model would treat as an ORDERED numeric feature
C) Category is deprecated
D) It drops rows

**Correct Answer:** B
**Explanation:** Category codes are arbitrary integers; feeding them to a
linear model imposes a meaningless ordering. `get_dummies` (or sklearn's
`OneHotEncoder`) creates proper 0/1 indicator columns for nominal data.

---

### Question 14 [Medium]
**In the challenge's `evaluate_no_leak_pipeline`, what is the ONLY
difference from the leaky version?**

A) The model
B) What data the scaler sees before `transform` — train-only vs pooled
C) The split fraction
D) The target

**Correct Answer:** B
**Explanation:** Both pipelines train models on train rows only. The leak
is entirely in preprocessing: the leaky version calls `scaler.fit(df[...])`
on the pooled frame, so test statistics enter the scaling.

---

### Question 15 [Medium]
**What is the output of the following code?**

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
X = pd.DataFrame({"x": [10.0, 20.0]})
y = pd.Series([1.0, 2.0])
train, test = X.iloc[:1], X.iloc[1:]
sc = StandardScaler().fit(train)
print(sc.scale_[0])
```

A) `0.0` — a single-row train has zero variance
B) `1.0`
C) `10.0`
D) `NaN`

**Correct Answer:** A
**Explanation:** `StandardScaler` with one training row computes std = 0
(population ddof=0). Scaling with a zero-variance column is degenerate —
one more reason splits need enough training rows and columns need checked
variance.

---

### Question 16 [Hard]
**The no-leak and leaky Ridge pipelines return different RMSE on the same
test set. What is the correct interpretation?**

A) The leaky RMSE is the optimistic one — always lower
B) The direction is data-dependent; the ONLY trustworthy number is the
no-leak RMSE, because the leaky features were computed with test statistics
C) The leaky RMSE is always higher
D) Both are valid; pick the lower one

**Correct Answer:** B
**Explanation:** In the challenge benchmark the leak INFLATES RMSE (1.82 vs
3.51) — the opposite of the "optimism" intuition. The direction depends on
data and model. The leak's number is untrustworthy regardless: it was
computed on features that saw the test set. Honest evaluation is the point.

---

### Question 17 [Hard]
**Why does `fit_scale_train_test` return the FITTED scaler?**

A) To reuse it on future data (e.g., production inference) with identical
transform semantics
B) To plot it
C) To refit it
D) For memory

**Correct Answer:** A
**Explanation:** The fitted scaler encodes the exact train statistics.
Production inference must apply the SAME transform to new rows —
`scaler.transform(new_X)` — not refit. Returning it makes the pipeline
reusable and testable.

---

### Question 18 [Hard]
**For `evaluate_leaky_pipeline` with a pooled scaler, which claim is
TRUE?**

A) The model saw test rows during training
B) The scaler saw test statistics; the model was still trained only on
train rows
C) Both model and scaler saw the test set
D) The leak is in the split

**Correct Answer:** B
**Explanation:** The leak is confined to preprocessing. The model's
training data never includes test rows — but the FEATURES it predicts on
were scaled by statistics computed on the test set. Preprocessing leaks are
just as damaging as row leaks, and harder to spot.

---

### Question 19 [Hard]
**What is the output of the following code?**

```python
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge
rng = np.random.RandomState(7)
x = np.linspace(0, 10, 100)
y = 2.0 * x + rng.normal(0, 1.0, 100)
df = pd.DataFrame({"x": x, "y": y})
train, test = df.iloc[:60], df.iloc[60:]
m = Ridge(alpha=10.0).fit(train[["x"]], train["y"])
pred = m.predict(test[["x"]])
print(round(float(np.sqrt(np.mean((test["y"] - pred) ** 2))), 4) > 0)
```

A) `True` — Ridge with alpha 10 shrinks, so RMSE > 0
B) `False` — perfect fit
C) `True` — but only because x is not scaled
D) `False` — Ridge always fits perfectly

**Correct Answer:** A
**Explanation:** A nonzero alpha penalizes coefficients, so the fitted
line is deliberately biased — RMSE is positive even on this near-linear
data. Scaling (not applied here) changes where the penalty bites.

---

### Question 20 [Hard]
**Which statement about the challenge's `verify_no_future_leak`-style
structural checks is correct?**

A) Comparing one statistic (e.g., mean) is enough
B) Comparing the ENTIRE feature table on overlapping rows (with tolerance)
is stronger — it pins every lag/window column against future influence
C) Structural checks are impossible
D) RMSE comparison is a structural check

**Correct Answer:** B
**Explanation:** A single statistic can coincide by luck; comparing every
value of every feature column on the overlapping rows proves the future
changed NOTHING in the past features. The challenge's
`verify_no_future_leak` does exactly this with `np.allclose(equal_nan=True)`.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | B | 16 | B |
| 2 | B | 7 | B | 12 | A | 17 | A |
| 3 | B | 8 | B | 13 | B | 18 | B |
| 4 | B | 9 | B | 14 | B | 19 | A |
| 5 | B | 10 | B | 15 | A | 20 | B |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you can build leak-free model pipelines |
| 14-17 | Proficient — review scaler semantics and ColumnTransformer |
| 10-13 | Developing — redo lecture 43 and the no-leak pipeline |
| < 10 | Beginner — study sklearn basics before proceeding |
