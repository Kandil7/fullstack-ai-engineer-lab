# Datetime & Time Series — Glossary 07 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `pd.Timestamp` | Class | The pandas scalar datetime |
| `pd.Timedelta` | Class | The pandas duration scalar |
| `datetime64[ns]` | Dtype | Timestamp column dtype |
| `pd.to_datetime()` | Function | Parse strings/objects to timestamps |
| DatetimeIndex | Index | A column of timestamps used as the row index |
| `.dt` accessor | Accessor | Vectorized date-feature extraction |
| `tz_localize()` | Method | Attaches a timezone to naive data |
| `tz_convert()` | Method | Converts an aware column's zone (same instant) |
| `resample()` | Method | Bucket by frequency then aggregate |
| offset string | Concept | Frequency spec: `1h`, `1D`, `W`, `ME` |
| `.rolling()` | Method | Trailing window aggregations |
| `.ewm()` | Method | Exponentially weighted windows |
| `.shift()` | Method | Lag a column by k positions |
| `.diff()` | Method | First difference |
| `TimeSeriesSplit` | Concept | Temporal cross-validation without leakage |
| time-based leakage | Bug | Future data reaching training rows |

## Detailed Definitions

### `pd.Timestamp`
**Definition**: The pandas scalar timestamp with `.year/.month/.day/.hour`
and full datetime arithmetic.
**Example**:
```python
pd.Timestamp("2026-08-06 09:30").year   # 2026
```
**Related**: `pd.Timedelta`

### `pd.Timedelta`
**Definition**: The duration scalar; added/subtracted from Timestamps.
**Example**:
```python
pd.Timestamp("2026-08-06") + pd.Timedelta("2h")
```
**Related**: `pd.Timestamp`

### `datetime64[ns]`
**Definition**: The column dtype for timestamps — what `to_datetime` produces.
**Related**: `pd.to_datetime()`

### `pd.to_datetime()`
**Definition**: Parses strings (and mixed formats) into a datetime column.
**Example**:
```python
df["created"] = pd.to_datetime(df["created"])
```
**Related**: `datetime64[ns]`

### DatetimeIndex
**Definition**: The index when the frame's rows are timestamps; enables time
slicing, resampling, and tz operations.
**Example**:
```python
df = df.set_index("ts").sort_index()
```
**Related**: `resample()`

### `.dt` accessor
**Definition**: Vectorized access to date parts: `.dt.year`, `.dt.month`,
`.dt.dayofweek`, `.dt.hour`, etc.
**Example**:
```python
df["hour"] = df["ts"].dt.hour
```
**Related**: calendar features

### `tz_localize()`
**Definition**: Attaches a timezone to a NAIVE column (no instant change);
the storage step for UTC.
**Example**:
```python
df["ts"].dt.tz_localize("UTC")
```
**Related**: `tz_convert()`

### `tz_convert()`
**Definition**: Converts an AWARE column to another zone — same instant,
different wall clock.
**Example**:
```python
df["ts"].dt.tz_convert("Asia/Tokyo")
```
**Related**: `tz_localize()`

### `resample()`
**Definition**: Buckets a DatetimeIndex by frequency and aggregates each
bucket — the frequency-change workhorse.
**Example**:
```python
df["count"].resample("1h").sum()
```
**Related**: offset string, DatetimeIndex

### offset string
**Definition**: Frequency specifiers: `1h`, `1D`, `W` (week), `ME` (month
end), `5T` (5 minutes), etc.
**Related**: `resample()`

### `.rolling()`
**Definition**: Trailing-window aggregations (`rolling(7).mean()`); default is
backward-looking (no future leakage).
**Related**: `.ewm()`, `.shift()`

### `.ewm()`
**Definition**: Exponentially weighted moving window — recent values weigh
more; `span=` controls decay.
**Related**: `.rolling()`

### `.shift()`
**Definition**: Lags a column by k rows; `shift(1)` gives the previous value —
the forecasting feature builder.
**Related**: `.diff()`

### `.diff()`
**Definition**: First difference — `s.diff()` = `s - s.shift(1)`; detrends
series.
**Related**: `.shift()`

### `TimeSeriesSplit`
**Definition**: sklearn's temporal CV: each fold trains on the past, tests on
the future — no shuffle, no leakage.
**Related**: time-based leakage

### time-based leakage
**Definition**: Future information reaching training rows — via random
splits, centered windows, or statistics fit on the full series.
**Related**: `TimeSeriesSplit`, trailing windows

## Key Concepts Summary

### The toolchain
- Parse (`to_datetime`) -> index (`set_index`) -> features (`.dt`) -> aggregate (`resample`)
- Windows and lags: rolling/ewm/shift/diff

### Timezone discipline
- Store UTC (`tz_localize("UTC")`); display elsewhere (`tz_convert`)
- Never convert with arithmetic

### Leakage rules
- Chronological splits only; `TimeSeriesSplit` for CV
- Trailing windows (`center=False`); fit statistics on train

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `resample("1h")` — ___
2. `tz_convert()` — ___
3. `.dt` accessor — ___
4. `.rolling(7).mean()` — ___
5. `.shift(1)` — ___
6. DatetimeIndex — ___
7. `TimeSeriesSplit` — ___
8. `to_datetime()` — ___

A. Bucket hourly + aggregate
B. Calendar-feature extraction
C. Trailing 7-row mean
D. Parse strings to timestamps
E. Same instant, other zone
F. Previous-row lag
G. Temporal CV without leakage
H. Timestamp row index

**Answers:** 1-A, 2-E, 3-B, 4-C, 5-F, 6-H, 7-G, 8-D
