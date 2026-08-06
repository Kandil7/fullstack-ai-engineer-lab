# Challenge 43: Pandas for ML — Pipeline Without Leakage

Feature engineering feeds models; the cardinal sin is leaking test
information into training (or into the features themselves). This challenge
builds the clean split → scale → feature pipeline and proves the leakage
lesson with numbers.

## 🥉 Bronze — Chronological Split (~15 min)

**Task:** Implement `chrono_split(df, frac)`: split a time-ordered DataFrame
so the **first** `frac` of rows are training and the rest are test — no
shuffling.

**Signature:**
```python
def chrono_split(df: pd.DataFrame, frac: float) -> tuple[pd.DataFrame, pd.DataFrame]:
```

| Input | Expected |
|---|---|
| 10 rows, frac 0.6 | train rows 0..5, test rows 6..9 |
| 10 rows, frac 0.0 | empty train, 10 test |
| 10 rows, frac 1.0 | 10 train, empty test |

**Constraints:** `n <= 10^4`. A shuffled split breaks the chronological
guarantee: the max training date must be `<=` the min test date.

---

## 🥈 Silver — Scale-Without-Leakage (~35 min)

**Task:** Implement `fit_scale_train_test(X_train, X_test, scaler)`: fit the
scaler **on the training set only**, transform both, and return
`(X_train_scaled, X_test_scaled, scaler)`.

**Signature:**
```python
def fit_scale_train_test(X_train: pd.DataFrame, X_test: pd.DataFrame,
                         scaler) -> tuple[pd.DataFrame, pd.DataFrame, object]:
```

| Input | Expected |
|---|---|
| train `[0, 2]`, test `[0, 10]`, StandardScaler | test values scale with **train** mean 1, std 1: `[-1.0, 9.0]` |
| constant train column | scaled column all zeros |
| scaler fitted on pooled data | **different** (wrong) values — see Gold |

**Constraints:** `n <= 10^4`, 1–10 columns. Fit on pooled train+test is the
classic leak: test mean 5.5/std ~5.2 gives `[-1.058, 0.866]` — not `[-1.0, 9.0]`.

---

## 🥇 Gold — Pipeline Predictor (~75 min)

**Task:** Implement `evaluate_no_leak_pipeline(df, target, frac, scaler)`
and `evaluate_leaky_pipeline(df, target, frac, scaler)`.

Both must: split chronologically, build a **Ridge** model (alpha default
10.0 — scale-sensitive, so the scaling leak actually changes predictions),
and return `(model, test_rmse, scaled_test_df)` — the scaled test frame plus
predictions column. The **no-leak** version scales with a train-fit scaler;
the **leaky** version scales with a scaler fit on the pooled (train+test)
data.

**Signature:**
```python
def evaluate_no_leak_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
def evaluate_leaky_pipeline(df, target, frac, scaler, alpha: float = 10.0) -> tuple:
```

| Input | Expected |
|---|---|
| linear `y = 2x + noise`, frac 0.6 | no-leak rmse < leaky rmse (clean ≈ 1.82 vs leaky ≈ 3.51) |
| perfect linear `y = 3x`, `alpha=1e-12` | no-leak rmse ≈ 0 |
| target constant | both pipelines finite rmse |

**Constraints:** `n <= 10^3`, single feature. Use `Ridge(alpha).fit` on the
scaled training frame. The leak must be in the **scaler fit**, not in model
training — models are always trained on train rows only.

**Follow-up:** why is the direction of the leak's effect *not* the lesson?
(Answer: the leak's RMSE differs from the honest one — here it's inflated,
elsewhere it could be deflated. Either way it is **untrustworthy**: it was
computed on features that saw test statistics. The no-leak RMSE is the only
number you can trust out-of-sample — which is exactly why you must prevent
the leak instead of predicting its direction.)

---

## Running

```bash
pytest challenges/43-pandas-for-ml/test_challenge.py -v
```

## Test File Structure

```
challenges/43-pandas-for-ml/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
