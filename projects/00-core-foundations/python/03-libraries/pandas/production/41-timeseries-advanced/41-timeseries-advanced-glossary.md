# Advanced Time Series — Glossary 41 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `DatetimeIndex` | Type | Time index enabling resample/shift/rolling |
| `pd.date_range` | Function | Builds a DatetimeIndex with a frequency |
| freq string | Concept | `"D"`, `"h"`, `"W"`, `"B"`, `"M"` — the cadence of the index |
| `resample` | Method | Frequency change with aggregation; label = bucket end |
| `Grouper` | Object | groupby key for time bucketing; identical to resample |
| `asfreq` | Method | Frequency change WITHOUT aggregation (NaN gaps) |
| `ffill` | Method | Forward-fill last known value |
| `shift` | Method | Moves values forward/back by k periods |
| `diff` | Method | value - shifted value |
| `pct_change` | Method | Relative change vs previous period |
| `rolling` | Method | Sliding window statistics (includes current row) |
| leakage | Concept | Using future info in a feature; validation/production mismatch |
| `tz_localize` | Method | Attaches a time zone to naive timestamps |
| `tz_convert` | Method | Converts an aware index to another zone |
| `CustomBusinessDay` | Offset | Business-day calendar that can skip holidays |
| time-based split | Pattern | Train on the past, test on the future |

## Detailed Definitions

### `asfreq`
**Definition**: Changes the index frequency without aggregation: existing
values land on the new grid, gaps become NaN. Pair with `ffill` for as-of
filling.
**Example**:
```python
daily.asfreq("h").ffill()
```
**Complexity**: O(n) to O(new grid).
**Related**: `ffill`, `resample`

### `CustomBusinessDay`
**Definition**: An offset for business-day indexing that skips weekends and
any holidays you list — trading-calendar pipelines use it so windows never
span closed days.
**Example**:
```python
from pandas.tseries.offsets import CustomBusinessDay
pd.date_range("2024-01-11", periods=5, freq=CustomBusinessDay(holidays=[...]))
```
**Related**: freq string

### `DatetimeIndex`
**Definition**: An index of `datetime64` values with an attached frequency —
the precondition for resample, shift, rolling, and time slicing.
**Example**:
```python
idx = pd.date_range("2024-01-01", periods=10, freq="D")
```
**Related**: `pd.date_range`, freq string

### `diff`
**Definition**: `series - series.shift(1)` computed in one vectorized call:
the per-period absolute change.
**Example**:
```python
s.diff()   # [nan, 10.0, 10.0, 20.0] for [10, 20, 30, 50]
```
**Related**: `shift`, `pct_change`

### `ffill`
**Definition**: Forward-fill: each NaN becomes the most recent non-NaN
value. The standard fill after `asfreq` upsampling.
**Example**:
```python
s.asfreq("h").ffill()
```
**Complexity**: O(n) single pass.
**Related**: `asfreq`

### freq string
**Definition**: The shorthand describing an index cadence: `D` day, `h`
hour, `W` week (anchored Sunday), `B` business day, `M` month end.
**Related**: `DatetimeIndex`, `resample`

### `Grouper`
**Definition**: A groupby key that buckets by time frequency;
`groupby(pd.Grouper(freq="W"))` is equivalent to `resample("W")`.
**Example**:
```python
daily.groupby(pd.Grouper(freq="W")).mean()
```
**Related**: `resample`

### leakage
**Definition**: A feature that uses information not available at decision
time — most often a rolling statistic that includes the current row.
Validation looks great; production silently degrades.
**Example**:
```python
# LEAKED: rolling(5).mean() at row t includes row t
# HONEST: rolling(5).mean().shift(1)
```
**Related**: `rolling`, `shift`

### `pct_change`
**Definition**: Relative change vs the previous period:
`(value - shifted) / shifted`.
**Example**:
```python
s.pct_change()   # [nan, 1.0, 0.5, 0.667] for [10, 20, 30, 50]
```
**Related**: `diff`, `shift`

### `pd.date_range`
**Definition**: Builds a DatetimeIndex from a start, count, and frequency —
the standard constructor for time-indexed data.
**Example**:
```python
pd.date_range("2024-01-01", periods=5, freq="B")
```
**Related**: `DatetimeIndex`, freq string

### `resample`
**Definition**: Groups rows into fixed time buckets and aggregates. Label
defaults to the bucket end; empty buckets are dropped. Equivalent to
`groupby(Grouper)` for pure time keys.
**Example**:
```python
daily.resample("W").mean()
```
**Complexity**: O(n) vectorized.
**Related**: `Grouper`, freq string

### `rolling`
**Definition**: Sliding-window statistics: `rolling(k).mean()` at row t uses
rows `t-k+1..t` — it includes the current row. Shift the result for features
known before t.
**Example**:
```python
s.rolling(5).mean().shift(1)
```
**Complexity**: O(n) per built-in stat; O(n) Python calls for `.apply`.
**Related**: leakage, `shift`

### `shift`
**Definition**: Moves values by k periods: `shift(1)` puts yesterday's value
in today's row; `shift(-1)` pulls tomorrow's value back.
**Example**:
```python
s.shift(1)   # [nan, 10.0, 20.0, 30.0] for [10, 20, 30, 50]
```
**Complexity**: O(n).
**Related**: `diff`, `pct_change`, leakage

### time-based split
**Definition**: Splitting by timestamp cutoff instead of randomly — train on
the past, test on the future. Required whenever the data is time-ordered.
**Related**: leakage

### `tz_convert`
**Definition**: Converts an already-aware index from one zone to another;
the underlying instant is unchanged.
**Example**:
```python
utc.tz_convert("America/New_York")
```
**Related**: `tz_localize`

### `tz_localize`
**Definition**: Attaches a time zone to naive timestamps, turning
`datetime64[ns]` into `datetime64[ns, tz]`.
**Example**:
```python
pd.Timestamp("2024-01-01 00:00").tz_localize("UTC")
```
**Related**: `tz_convert`

## Key Concepts Summary

### The no-leakage rule
- `rolling` includes the current row; always `.shift(1)` window features
- `shift(k)` is the honest "past only" mechanism
- Split by time for time-ordered data

### Frequency machinery
- `resample` == `groupby(Grouper)` for pure time buckets
- `asfreq` changes frequency without aggregating; `ffill` fills gaps
- Business calendars skip weekends and holidays

### Time zones
- Store UTC; `tz_localize` at ingestion, `tz_convert` at display
- The instant (`timestamp()`) never changes across conversions

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `rolling` — ___
2. `shift(1)` — ___
3. `resample` — ___
4. leakage — ___
5. `tz_convert` — ___
6. `asfreq` — ___
7. `CustomBusinessDay` — ___
8. `pct_change` — ___

A. Frequency change without aggregation
B. Sliding window that includes the current row
C. Yesterday's value in today's row
D. Relative change vs previous period
E. Using future information in a feature
F. Aggregated frequency change; label = bucket end
G. Converts between time zones
H. Business-day calendar that skips holidays

**Answers:** 1-B, 2-C, 3-F, 4-E, 5-G, 6-A, 7-H, 8-D
