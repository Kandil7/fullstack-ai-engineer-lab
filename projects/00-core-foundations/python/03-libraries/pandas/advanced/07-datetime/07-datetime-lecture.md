# 03-libraries/pandas (advanced) — 07: Datetime & Time Series

## Topic Overview

pandas brings full time-series support: `pd.Timestamp` and `pd.Timedelta`
scalars, `datetime64[ns]` columns, the `.dt` accessor, timezone awareness via
`tz_localize`/`tz_convert`, and — the centerpiece — resampling with
`resample()` for aggregating at any frequency.

For AI engineers, time is a first-class feature dimension: request timestamps,
sensor streams, log sequences. Time-based train/test splits, TTL logic,
feature lags, and drift windows all build on this layer. Combined with the
timezone rules from phase 1 topic 50 (store UTC, convert at the boundary),
this is the complete time toolchain.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Work with `pd.Timestamp` and `pd.Timedelta`
2. Parse and convert datetime columns with `to_datetime`
3. Use the `.dt` accessor for year/month/day/hour features
4. Localize and convert timezones correctly
5. Set a DatetimeIndex and slice by time
6. Resample to any frequency with aggregations
7. Compute rolling windows and lags
8. Avoid time-based train/test leakage

## Prerequisites

| Need | Where |
|------|-------|
| Core datetime rules | `01-core-python/50-datetime-and-timezones` lecture |
| Indexing | `02-indexing-selection-lecture.md` |
| GroupBy | `08-groupby-aggregation-lecture.md` |

## 1. Timestamp and Timedelta Scalars

```python
import pandas as pd

ts = pd.Timestamp("2026-08-06 09:30")
print(ts.year, ts.month, ts.day, ts.hour)     # 2026 8 6 9

span = pd.Timedelta("2h 15m")
print(ts + span)                              # 2026-08-06 11:45
```

`Timestamp` is the scalar datetime; `Timedelta` is the duration. Arithmetic
between them behaves exactly as in the `datetime` module — but vectorized.

## 2. Parsing and the DatetimeIndex

```python
df["created"] = pd.to_datetime(df["created"])     # parse strings
df = df.set_index("created").sort_index()         # DatetimeIndex

df["2026-08"]                      # slice one month
df.loc["2026-08-06":"2026-08-08"]  # date range slice (inclusive labels)
```

Setting a DatetimeIndex unlocks time slicing (`df["2026-08"]`), resampling,
and timezone operations. Sort the index once after setting it — many
time-based ops assume monotonic order.

## 3. The `.dt` Accessor — Date Features

```python
df["year"] = df["created"].dt.year
df["month"] = df["created"].dt.month
df["dow"] = df["created"].dt.dayofweek          # 0=Monday
df["hour"] = df["created"].dt.hour
df["is_weekend"] = df["created"].dt.dayofweek >= 5
```

`.dt` is the vectorized date-feature factory: year, month, day, hour, minute,
dayofweek, quarter, is_month_start, and more. Calendar features are cheap,
high-value model inputs (seasonality, weekly cycles).

## 4. Timezones — Localize Then Convert

```python
df["created"] = pd.to_datetime(df["created"]).dt.tz_localize("UTC")   # attach
df["created_local"] = df["created"].dt.tz_convert("Asia/Tokyo")       # convert
```

`tz_localize` attaches a zone to naive data (store in UTC); `tz_convert`
moves an aware column to another zone without changing the instant. Never
"convert" with arithmetic — these two methods are the whole timezone story.

## 5. Resampling — The Centerpiece

```python
hourly = df["count"].resample("1h").sum()       # hourly sums
daily_mean = df["count"].resample("1D").mean()  # daily means
weekly = df["count"].resample("W").max()
```

`resample` first buckets rows by frequency (offset strings like `1h`, `1D`,
`W`, `ME`), then aggregates each bucket. Missing buckets are filled with NaN —
`fillna(0)` or `.ffill()` as the semantics require. This is the API for
downgrading high-frequency logs to any decision frequency.

## 6. Rolling Windows and Lags

```python
df["rolling_7"] = df["count"].rolling(7).mean()         # trailing mean
df["ewm_7"] = df["count"].ewm(span=7).mean()            # weighted
df["lag_1"] = df["count"].shift(1)                      # previous value
df["diff_1"] = df["count"].diff()                       # first difference
```

Rolling/expanding/ewm windows (deep treatment in topic 11) plus `shift`/`diff`
lags are the feature-engineering layer for forecasting and anomaly detection.

## 7. The Leakage Rule — Time Splits

```python
cutoff = pd.Timestamp("2026-06-01", tz="UTC")
train = df[df.index < cutoff]
test = df[df.index >= cutoff]
```

Time-series splits are NEVER random: the future must not leak into training.
`TimeSeriesSplit` in sklearn implements this for cross-validation. Any
feature computed with future values (a centered rolling mean without
`center=False`, an ffill from the future) is leakage.

## 8. Production Pattern — Aggregation Builder

```python
def aggregate_to(df: pd.DataFrame, freq: str, agg: dict) -> pd.DataFrame:
    """Resample a timestamp-indexed frame and aggregate columns."""
    return df.resample(freq).agg(agg)


agg = {
    "count": "sum",
    "latency_ms": "mean",
    "errors": "sum",
}
hourly = aggregate_to(df.set_index("ts"), "1h", agg)
```

One function, declared aggregation rules, reused across metrics — the
operations-dashboard pattern.

## Common Mistakes to Avoid

### Mistake 1: Random splits on time series

```python
# WRONG — shuffling a time series leaks the future into training
train_test_split(df, shuffle=True)
# CORRECT — chronological split
```

### Mistake 2: Resampling before setting the index

```python
# WRONG — resample needs a DatetimeIndex
df.resample("1D").mean()
# CORRECT
df.set_index("ts").resample("1D").mean()
```

### Mistake 3: tz_convert on naive data

```python
# WRONG — assumes UTC, silently wrong for other zones
df["ts"].dt.tz_convert("Asia/Tokyo")
# CORRECT — localize first
df["ts"].dt.tz_localize("UTC").dt.tz_convert("Asia/Tokyo")
```

### Mistake 4: Center-of-window features leaking

```python
# WRONG — centered window sees future values
df["x"].rolling(7, center=True).mean()
# CORRECT — trailing window only (default)
df["x"].rolling(7).mean()
```

## Best Practices

1. Parse to `datetime64` at intake; set the DatetimeIndex once, sort it
2. Store UTC; `tz_localize` then `tz_convert` for display
3. Use `.dt` for calendar features before modeling
4. `resample` for frequency changes; `rolling`/`shift` for windows/lags
5. Never random-split time series; use chronological or `TimeSeriesSplit`
6. Keep windows trailing (`center=False`) to avoid future leakage
7. Name resample aggregation rules in functions (reviewable contracts)

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `to_datetime` | O(n) | parse pass |
| `.dt` features | O(n) | vectorized extraction |
| `set_index` | O(n log n) + sort | do once |
| time slicing | O(log n) | sorted DatetimeIndex lookup |
| `resample` | O(n) | bucket + aggregate |
| `rolling` | O(n x w) | windowed pass |
| `shift`/`diff` | O(n) | vectorized |

**At scale:** 10M-row logs resample in seconds. The costs to watch are the
windowed ops (rolling over huge windows) and the index sort — both one-time
or amortized.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| resample | downgrading request logs to hourly metrics |
| `.dt` features | seasonality/hour-of-day inputs to demand models |
| time splits | leak-free train/test for forecasting |
| rolling/lags | features for anomaly detection and forecasting |
| tz handling | aligning multi-region logs on UTC |
| `TimeSeriesSplit` | honest temporal cross-validation |

**Scale note:** every forecast/anomaly model inherits its evaluation honesty
from the time split. A single future-leaking feature (centered window,
global scaling before split) silently inflates every metric — the same class
of leak as the missing-data mean, but harder to see.

## Practice Exercises

### Exercise 1: Calendar Features (Easy)
Parse a `ts` column, extract year/month/dayofweek/hour features, and verify
the dtypes.

### Exercise 2: Resample (Medium)
Resample a minute-level `count` series to hourly sums and daily means; verify
bucket boundaries and NaN behavior on empty buckets.

### Exercise 3: Leak-Free Split (Hard)
Write `chrono_split(df, frac=0.8)` returning train/test by cutoff time, plus
a check that `TimeSeriesSplit` folds never contain future data in training.

## Summary

| Concept | Description |
|---------|-------------|
| Timestamp/Timedelta | scalar time and duration |
| DatetimeIndex | enables slicing, resampling, tz ops |
| `.dt` accessor | vectorized calendar features |
| tz_localize/tz_convert | attach then convert — never arithmetic |
| `resample` | bucket + aggregate at any frequency |
| rolling/ewm/shift/diff | windows and lags |
| time splits | chronological only — no future leakage |

Time is the axis most datasets are ordered by — and the axis most often
leaked. With the datetime layer plus the timezone rules, your time handling
becomes correct by construction.

## Quick Reference

| Task | Idiom |
|------|-------|
| Parse | `pd.to_datetime(s)` |
| Set index | `df.set_index("ts").sort_index()` |
| Month slice | `df["2026-08"]` |
| Calendar features | `s.dt.dayofweek`, `s.dt.hour` |
| Attach zone | `s.dt.tz_localize("UTC")` |
| Convert zone | `s.dt.tz_convert("Asia/Tokyo")` |
| Resample | `s.resample("1h").sum()` |
| Rolling mean | `s.rolling(7).mean()` |
| Lag | `s.shift(1)` |
| Diff | `s.diff()` |

## Next Steps

Next: **[08-groupby-aggregation](08-groupby-aggregation-lecture.md)** — split-apply-combine.
Continues in: **[08-mlops — 11 monitoring and drift](../../../../08-mlops/lectures/11-monitoring-and-drift-lecture.md)** (time windows on drift).
Official docs: https://pandas.pydata.org/docs/user_guide/timeseries.html
