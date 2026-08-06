# 03-libraries/pandas (advanced) — 11: Window Functions

## Topic Overview

Window functions compute a statistic over a moving slice of a series:
`rolling` (fixed-size trailing window), `expanding` (growing window from the
start), and `ewm` (exponentially weighted, recent values dominate). Combined
with `shift`/`diff`, they are the time-series feature factory.

For AI engineers, windows build the features that forecasting and anomaly
detection models learn from: 7-day rolling means, expanding baselines, ewm
smoothed latency, lag-1 deltas. The discipline that matters: **windows must
be backward-looking** (`center=False`) so no future value leaks into a
feature at time t.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compute rolling aggregations with `rolling`
2. Use `expanding` for cumulative statistics
3. Use `ewm` for exponentially weighted smoothing
4. Choose window size and handle NaN warm-up periods
5. Apply window functions with `apply` for custom statistics
6. Combine windows with lags for feature engineering
7. Keep windows trailing to avoid future leakage

## Prerequisites

| Need | Where |
|------|-------|
| Datetime & resample | `07-datetime-lecture.md` |
| Aggregations | `08-groupby-aggregation-lecture.md` |
| Time-series leakage | `07-datetime-lecture.md` §7 |

## 1. `rolling` — Fixed Trailing Window

```python
s = pd.Series([1, 2, 3, 4, 5])

s.rolling(3).mean()
# 0    NaN
# 1    NaN
# 2    2.0
# 3    3.0
# 4    4.0
```

The first `window-1` values are NaN (insufficient data) — the warm-up period.
`min_periods=` relaxes it (e.g. `rolling(7, min_periods=1)` starts averaging
from the first row), which is often the right call for short series.

## 2. `expanding` — Cumulative Window

```python
s.expanding().mean()        # running mean: 1, 1.5, 2, 2.5, 3
s.expanding().std()         # running std
```

`expanding` grows from the first element — cumulative statistics. Use for
baselines ("average so far") and for detecting drift from an evolving
distribution.

## 3. `ewm` — Exponential Weighting

```python
s.ewm(span=3).mean()        # recent values weigh more
s.ewm(alpha=0.1).mean()     # alpha controls the decay directly
```

`ewm` (exponentially weighted moving) weights recent observations more
heavily, reacting faster to change than a plain rolling mean. `span` and
`alpha` are two spellings of the same decay: `alpha = 2 / (span + 1)`.

## 4. Custom Statistics — `rolling().apply`

```python
s.rolling(5).apply(lambda w: np.percentile(w, 95))   # rolling 95th pct
s.rolling(5).apply(lambda w: w.max() - w.min())      # rolling range
```

For statistics the built-ins don't cover, `apply` runs a function per window —
slower than vectorized ops, so reserve it for what rolling's named methods
cannot express.

## 5. Window Sizing and Warm-Up

```python
s.rolling(7, min_periods=1).mean()   # no NaN warm-up
s.rolling(7).mean().fillna(0)        # or decide the NaN policy
```

Window size is a modeling hyperparameter: too small is noisy, too large lags
behind change. The warm-up NaNs must have an explicit policy (drop, min_periods,
fill) — leaking them into a model as NaN features is a real bug.

## 6. Windows + Lags — The Feature Combo

```python
df["mean_7"] = s.rolling(7).mean()
df["lag_1"] = s.shift(1)
df["diff_1"] = s.diff()
df["ewm_7"] = s.ewm(span=7).mean()
```

Rolling means capture level, lags capture memory, diffs capture momentum, ewm
captures recency — the standard forecasting feature set.

## 7. The Leakage Rule — Trailing Only

```python
s.rolling(7, center=True).mean()   # WRONG for features: sees the future
s.rolling(7).mean()                # CORRECT: only past + present
```

`center=True` centers the window on the current point, using future values —
correct for smoothing plots, WRONG for model features. Never build features
from centered windows; `shift` anything computed with future info.

## 8. Production Pattern — Feature Builder

```python
def add_window_features(df: pd.DataFrame, col: str, windows: tuple[int, ...]) -> pd.DataFrame:
    """Attach trailing rolling stats for several window sizes."""
    out = df.copy()
    for w in windows:
        out[f"{col}_mean_{w}"] = out[col].rolling(w, min_periods=1).mean()
        out[f"{col}_std_{w}"] = out[col].rolling(w, min_periods=1).std()
    out[f"{col}_ewm"] = out[col].ewm(span=7).mean()
    out[f"{col}_lag1"] = out[col].shift(1)
    return out
```

One function, declared windows, trailing-only — the forecasting feature
pipeline.

## Common Mistakes to Avoid

### Mistake 1: Centered windows as features

```python
# WRONG — future values leak into the feature
s.rolling(7, center=True).mean()
# CORRECT — trailing only for features
s.rolling(7).mean()
```

### Mistake 2: Ignoring the warm-up NaN period

```python
# WRONG — NaN features flow into the model silently
df["mean_7"] = s.rolling(7).mean()
# CORRECT — decide the policy (min_periods, fill, or drop those rows)
```

### Mistake 3: Recomputing windows in a loop

```python
# WRONG — O(n*window) instead of O(n)
means = [s[i-w+1:i+1].mean() for i in range(len(s))]
# CORRECT — vectorized
s.rolling(w).mean()
```

### Mistake 4: Using `apply` where a built-in exists

```python
# WRONG — rolling.apply(np.mean) is ~100x slower than .mean()
s.rolling(5).apply(np.mean)
# CORRECT
s.rolling(5).mean()
```

## Best Practices

1. Rolling for fixed windows; expanding for cumulative; ewm for recency
2. Features: trailing windows only (`center=False` always)
3. Decide warm-up NaN policy explicitly (`min_periods`, fill, drop)
4. Window size is a hyperparameter — tune it, don't guess
5. Use `.apply` only for statistics the named methods lack
6. Bundle window features in one named builder function

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `rolling().mean()` | O(n) | vectorized, window-independent |
| `rolling().apply(fn)` | O(n x w) | Python per window |
| `expanding()` | O(n) | one pass |
| `ewm()` | O(n) | recursive |
| `shift`/`diff` | O(n) | vectorized |

**At scale:** named rolling methods are O(n) regardless of window size —
cheap at 10M rows. `apply` multiplies by the window and is the one to avoid
on big series.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| rolling means | load/forecast features over hours/days |
| expanding | drift baselines from "all history so far" |
| ewm | smoothed latency/error-rate metrics |
| lags + diffs | autoregressive features for forecasting |
| trailing-only | the leak-free guarantee for time features |
| rolling percentiles | anomaly bands (p95/p99) |

**Scale note:** every time-based model inherits its honesty from window
discipline. One centered window or one future-ffilled lag silently leaks
tomorrow into today's features — the hardest-to-see leak in ML.

## Practice Exercises

### Exercise 1: Rolling Means (Easy)
Compute `rolling(3).mean()` and confirm the first two values are NaN; then
repeat with `min_periods=1`.

### Exercise 2: Feature Set (Medium)
Build the `add_window_features` feature set for a 1,000-point series and
verify the lag-1 column equals the shifted original.

### Exercise 3: Leak-Free Check (Hard)
Write `assert_no_future_leak(df, feature_cols, t_col)` that verifies each
feature at time t depends only on rows with `t_col <= t` (recompute features
on a truncated frame and compare).

## Summary

| Concept | Description |
|---------|-------------|
| `rolling` | fixed trailing window |
| `expanding` | growing cumulative window |
| `ewm` | exponentially weighted recency |
| warm-up NaN | explicit policy: min_periods/fill/drop |
| trailing-only | the no-future-leak rule for features |
| lags + diffs | memory and momentum features |
| `apply` | custom per-window stats — sparingly |

Windows turn a raw series into the features models actually learn from. Keep
them trailing, size them deliberately, and the forecasting feature set is
leak-free by construction.

## Quick Reference

| Task | Idiom |
|------|-------|
| Trailing mean | `s.rolling(7).mean()` |
| No warm-up NaN | `s.rolling(7, min_periods=1).mean()` |
| Running mean | `s.expanding().mean()` |
| EWM smooth | `s.ewm(span=7).mean()` |
| Rolling p95 | `s.rolling(7).apply(lambda w: np.percentile(w, 95))` |
| Lag | `s.shift(1)` |
| Difference | `s.diff()` |
| Leak-free | never `center=True` in features |

## Next Steps

Next: **[12-apply-map](12-apply-map-lecture.md)** — custom transformations.
Continues in: **[08-mlops — 11 monitoring and drift](../../../../08-mlops/lectures/11-monitoring-and-drift-lecture.md)** (windows in drift detection).
Official docs: https://pandas.pydata.org/docs/user_guide/window.html
