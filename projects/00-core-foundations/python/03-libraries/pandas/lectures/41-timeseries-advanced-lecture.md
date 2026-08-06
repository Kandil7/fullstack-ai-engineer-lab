# 03-libraries/pandas — 41: Advanced Time Series

## Topic Overview

Advanced time series is the machinery for working with *timed* data: building
a `DatetimeIndex`, changing observation frequency with `resample`, lags with
`shift`, deltas with `diff`/`pct_change`, window statistics with `rolling`,
time zones, and business calendars. The common thread is a discipline about
what information exists at a given moment — the no-leakage rule.

For AI engineers this is the heart of forecasting, anomaly detection, and
every feature that answers "what did the world look like *before* this
event?". A rolling mean built without `shift(1)` includes the value you are
predicting, which makes validation look excellent and production fail. This
lecture makes the no-leakage rule a reflex: split by time, lag by time,
window over the past only, and store UTC.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build and inspect a `DatetimeIndex` with `pd.date_range`
2. Resample with `resample()` and know how it differs from `groupby(Grouper)`
3. Upsample with `asfreq()` and forward-fill with `ffill()`
4. Create lag/delta features with `shift`, `diff`, `pct_change`
5. Build rolling features that exclude the current row (no leakage)
6. Localize and convert time zones; store UTC
7. Use `CustomBusinessDay` calendars that skip holidays

## Prerequisites

| Need | Where |
|------|-------|
| `to_datetime` | `07-datetime-lecture.md` |
| `groupby` | `08-groupby-aggregation-lecture.md` |
| filtering/indexing | `02-indexing-selection-lecture.md` |

## 1. Building a DatetimeIndex

`pd.date_range` creates an index with a frequency (`D` days, `h` hours, `B`
business days, `W` weeks, `M` months…). A `DatetimeIndex` is what makes the
frame resamplable and sliceable by time labels.

```python
import numpy as np
import pandas as pd

idx = pd.date_range("2024-01-01", periods=10, freq="h")
ts = pd.Series(np.arange(10, dtype=float), index=idx)
print(ts.index.dtype, ts.index.freq)          # datetime64[ns] <Hour>

biz = pd.date_range("2024-01-01", periods=5, freq="B")
print(biz.strftime("%Y-%m-%d").tolist())
# ['2024-01-01' '2024-01-02' '2024-01-03' '2024-01-04' '2024-01-05']
```

```text
datetime64[ns] <Hour>
['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
```

## 2. `resample` — Downsampling

`resample(freq).agg()` groups rows into fixed time buckets and applies an
aggregation. The label defaults to the **end** of the bucket.

```python
daily = pd.Series(np.arange(1, 15, dtype=float),
                  index=pd.date_range("2024-01-01", periods=14, freq="D"))
weekly = daily.resample("W").mean()
print(weekly.round(2).tolist())                       # [4.0, 11.0]
print(weekly.index.strftime("%Y-%m-%d").tolist())     # week ends
```

```text
[4.0, 11.0]
['2024-01-07', '2024-01-14']
```

Week 1 holds Jan 1-7 (mean of 1..7 = 4); week 2 holds Jan 8-14 (mean of
8..14 = 11). There is no third bucket because Jan 15+ has no data — empty
buckets are dropped by default.

## 3. `resample` vs `groupby(Grouper)` — Same Engine

`resample` is sugar over a `Grouper`: both bucket by the same rule and
produce identical results.

```python
by_resample = daily.resample("W").mean()
by_grouper = daily.groupby(pd.Grouper(freq="W")).mean()
print(by_resample.equals(by_grouper))                 # True
```

```text
True
```

Use `resample` for time-only bucketing (it also handles upsampling and
offset alignment); use `groupby` when you need other keys alongside time.

## 4. Upsampling — `asfreq` + `ffill`

`asfreq` changes frequency **without aggregating**: values land on the new
grid and NaN fills the gaps. `ffill()` propagates the last known value —
the standard "as-of" fill for feature tables.

```python
hourly = daily.asfreq("h").ffill()
print(len(hourly))                                    # 313
print(hourly.loc["2024-01-02 01:00"])                 # 2.0 (Jan 2 value)
print(hourly.notna().all())                           # True
```

```text
313
2.0
True
```

## 5. Lags and Deltas — `shift`, `diff`, `pct_change`

`shift(k)` moves values **forward** by k periods: row t receives the value
from t-1. That is the entire no-leakage mechanism — at time t you may only
know t-1. `diff` is `value - shifted`, `pct_change` is the relative delta.

```python
s = pd.Series([10.0, 20.0, 30.0, 50.0],
              index=pd.date_range("2024-01-01", periods=4, freq="D"))
print(s.shift(1).tolist())     # [nan, 10.0, 20.0, 30.0]
print(s.shift(-1).tolist())    # [20.0, 30.0, 50.0, nan]
print(s.diff().tolist())       # [nan, 10.0, 10.0, 20.0]
print(s.pct_change().round(3).tolist())  # [nan, 1.0, 0.5, 0.667]
```

```text
[nan, 10.0, 20.0, 30.0]
[20.0, 30.0, 50.0, nan]
[nan, 10.0, 10.0, 20.0]
[nan, 1.0, 0.5, 0.667]
```

## 6. Rolling Windows — the Leakage Trap

`rolling(k).mean()` at row t uses rows `t-k+1 .. t` — it **includes the
current value**. For a feature known *before* a prediction at t, shift the
window: `rolling(k).mean().shift(1)`.

```python
prices = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
print(prices.rolling(3).mean().tolist())          # [nan, nan, 2.0, 3.0, 4.0]
print(prices.rolling(3).mean().shift(1).tolist()) # [nan, nan, nan, 2.0, 3.0]
```

```text
[nan, nan, 2.0, 3.0, 4.0]
[nan, nan, nan, 2.0, 3.0]
```

The unshifted version knows today's price at today's row — a feature that
leaks the target. The shifted version is the honest feature.

## 7. Time Zones — UTC In, Local Out

Store UTC. `tz_localize` attaches a zone to naive data; `tz_convert` moves an
aware index to another zone. The instant (`timestamp()`) never changes.

```python
naive = pd.Timestamp("2024-01-01 00:00")
utc = naive.tz_localize("UTC")
nyc = utc.tz_convert("America/New_York")
print(utc)                       # 2024-01-01 00:00:00+00:00
print(nyc)                       # 2023-12-31 19:00:00-05:00
print(utc.timestamp() == nyc.timestamp())   # True
```

```text
2024-01-01 00:00:00+00:00
2023-12-31 19:00:00-05:00
True
```

## 8. Business Calendars

`CustomBusinessDay` lets you define which days count: skip weekends *and*
holidays. Trading-day pipelines use this so windows never span closed days.

```python
from pandas.tseries.offsets import CustomBusinessDay

holiday = pd.Timestamp("2024-01-15")
cal = CustomBusinessDay(holidays=[holiday])
dates = pd.date_range("2024-01-11", periods=5, freq=cal)
print(dates.strftime("%Y-%m-%d").tolist())
# ['2024-01-11', '2024-01-12', '2024-01-16', '2024-01-17', '2024-01-18']
```

```text
['2024-01-11', '2024-01-12', '2024-01-16', '2024-01-17', '2024-01-18']
```

## 9. Production Pattern — a No-Leakage Feature Builder

The pattern for ML features from a series: build each feature from **past
data only**, and verify the last row is complete before predicting.

```python
def build_features(series: pd.Series, window: int) -> pd.DataFrame:
    out = pd.DataFrame({"value": series})
    out["lag_1"] = series.shift(1)
    out["mean_w"] = series.rolling(window).mean().shift(1)  # no leakage
    out["pct_chg"] = series.pct_change()
    return out
```

Verification invariants: `lag_1` at t equals `value` at t-1; `mean_w` at t
equals the mean of rows `t-w .. t-1`. Assert both and your feature table
cannot silently leak.

## Common Mistakes to Avoid

### Mistake 1: rolling features that include the current row

```python
# WRONG — includes the value you are predicting
X["avg"] = price.rolling(5).mean()
# CORRECT — past only
X["avg"] = price.rolling(5).mean().shift(1)
```

### Mistake 2: naive timestamps from different machines

```python
# WRONG — local times without zones are not comparable
logs["ts"] = pd.to_datetime(logs["local_ts"])
# CORRECT — store UTC
logs["ts"] = pd.to_datetime(logs["local_ts"]).dt.tz_localize("UTC")
```

### Mistake 3: calendar-week resampling for trading data

```python
# WRONG — W buckets include weekend days
df.resample("W").mean()
# CORRECT — business anchored frequency
df.resample("W-FRI").mean()
```

### Mistake 4: `asfreq` when you wanted aggregation

```python
# WRONG — asfreq does NOT aggregate; duplicates become NaN
df.resample("D").asfreq()
# CORRECT — aggregate first if that is the intent
df.resample("D").mean()
```

## Best Practices

1. Store UTC; localize only at ingestion, convert only at display
2. Shift before rolling — never leak the current row
3. Build features per split (train/test), never across the boundary
4. Prefer `resample` for pure time buckets; `Grouper` for mixed keys
5. Fill gaps explicitly (`asfreq().ffill()`) instead of assuming alignment
6. Use business calendars for trading-day pipelines
7. Assert the last feature row is complete before predicting
8. Keep the frequency (`freq`) attached — it is part of the contract

## Complexity and Cost

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `resample("W").mean()` | O(n) | O(buckets) | vectorized bucket scan |
| `asfreq("h")` | O(n) | O(new grid) | allocates the target index |
| `ffill()` | O(n) | O(1) | single pass |
| `shift(k)` | O(n) | O(n) | allocates the shifted series |
| `rolling(k).mean()` | O(n) | O(k) | sliding window |
| `tz_convert` | O(n) | O(n) | rebuilds the index |
| `CustomBusinessDay` | O(n) | O(1) | calendar lookup |

**At scale:** rolling windows dominate cost on long series — `rolling(k)` on
a 10M-row series is one vectorized pass, but `rolling(k).apply(python_fn)` is
10M Python calls. Keep window functions built-in; move exotic statistics to
`numba`-backed `.apply` only when measured.

## AI Engineering Relevance

**Where this shows up:** demand forecasting, anomaly detection, churn
prediction, and every "features at decision time" service.

| Concept here | Used for |
|--------------|----------|
| `shift`/`diff` | lagged features; the only honest view of the past |
| `rolling().shift(1)` | window statistics without target leakage |
| `resample` | aggregating events to the decision cadence (daily/hourly) |
| time zones | joining logs from multiple regions correctly |
| business calendars | trading/finance features on non-holiday days |
| time-based split | chronological train/test — never random on time data |

**Scale note:** leakage is not a performance issue — it is a *correctness*
issue that quietly overstates validation. At 1M rows it is a bug you debug;
at 10M rows it is a model you ship that underperforms in production with no
obvious cause. The `shift(1)` discipline is what keeps validation honest.

## Practice Exercises

### Exercise 1: Resample by Hour (Easy)
Take a minute-frequency series and `resample("h").mean()`. Verify the number
of hourly buckets matches `minutes // 60`.

### Exercise 2: Lag Features (Medium)
Build `lag_1`, `lag_7`, and `diff_7` for a daily series; verify
`lag_7[t] == value[t-7]` for all t >= 7.

### Exercise 3: No-Leakage Window (Medium)
For `window=5`, verify `rolling(5).mean().shift(1)` at row t equals the mean
of rows `t-5..t-1` — not `t-4..t`.

### Exercise 4: Multi-Zone Joins (Hard)
Create two tz-aware series (UTC and Asia/Tokyo) representing the same
instants; join them and verify alignment by instant, then explain what a
naive-string join would have corrupted.

## Summary

| Concept | Description |
|---------|-------------|
| `DatetimeIndex` | time index enabling resample/shift/rolling |
| `resample` | frequency change with aggregation (== `Grouper`) |
| `asfreq` + `ffill` | upsampling with last-known-value fill |
| `shift`/`diff`/`pct_change` | lags and deltas — the past, honestly |
| `rolling().shift(1)` | window stats without current-row leakage |
| time zones | UTC storage, local display |
| business calendars | skip weekends and holidays |

Advanced time series is 80% discipline: lag before you window, split by
time, store UTC. Get those three right and the machinery — resample, asfreq,
custom calendars — becomes routine rather than a source of silent bugs.

## Quick Reference

| Task | Idiom |
|------|-------|
| Build index | `pd.date_range("2024-01-01", periods=n, freq="h")` |
| Downsample | `s.resample("W").mean()` |
| Same via Grouper | `s.groupby(pd.Grouper(freq="W")).mean()` |
| Upsample + fill | `s.asfreq("h").ffill()` |
| Lag | `s.shift(1)` |
| Delta | `s.diff()` |
| Relative delta | `s.pct_change()` |
| Window, no leakage | `s.rolling(5).mean().shift(1)` |
| Attach zone | `s.tz_localize("UTC")` |
| Convert zone | `s.tz_convert("America/New_York")` |
| Holiday calendar | `pd.date_range(start, periods=k, freq=CustomBusinessDay(holidays=[...]))` |

## Next Steps

Next: **[42 — GroupBy Internals](42-groupby-internals-lecture.md)** —
split-apply-combine and when to use agg/transform/filter/apply.
Continues in: **[41 — Advanced Time Series challenge](../challenges/41-timeseries-advanced/README.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/timeseries.html
