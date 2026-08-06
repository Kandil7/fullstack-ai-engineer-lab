# Challenge 41: Advanced Time Series — No-Leakage Features

The single most expensive time-series bug is leakage: a rolling feature that
includes the row you are predicting. This challenge builds the honest
versions — lag, window, and split — with tests that pin "past only".

## 🥉 Bronze — No-Leak Rolling Mean (~15 min)

**Task:** Implement `no_leak_rolling(series, window)` returning the rolling
mean **shifted by one**: at row `t` the value is the mean of rows
`t-window .. t-1` — never `t` itself. Use `series.rolling(window).mean().shift(1)`.

**Signature:**
```python
def no_leak_rolling(series: pd.Series, window: int) -> pd.Series:
```

| Input | Expected |
|---|---|
| `[1, 2, 3, 4, 5]`, window 3 | `[NaN, NaN, NaN, 2.0, 3.0]` |
| `[10, 20, 30]`, window 2 | `[NaN, NaN, 15.0]` (row 2 = mean of rows 0..1) |
| `[]`, window 3 | empty |

**Constraints:** `n <= 10^3`. A plain `rolling(window).mean()` (no shift)
fails the values test.

---

## 🥈 Silver — Feature Table From the Past (~35 min)

**Task:** Implement `build_features(series, window)`, returning a DataFrame
with columns `value` (the series), `lag_1` (`shift(1)`), `mean_w`
(no-leak rolling mean), and `pct_chg` (`pct_change`). Every column must be
computable *before* time `t`.

**Signature:**
```python
def build_features(series: pd.Series, window: int) -> pd.DataFrame:
```

| Input | Expected |
|---|---|
| `[10, 20, 30, 50]`, window 2 | `lag_1` = `[NaN, 10, 20, 30]`, `mean_w` = `[NaN, NaN, 15, 25]`, `pct_chg` = `[NaN, 1.0, 0.5, 0.667]` |
| 30 business days, window 5 | `mean_w[t] == mean(value[t-5:t-1])` for all t >= window |
| all-equal values | `pct_chg` all zero after the first row |

**Constraints:** `n <= 10^4`. The window test asserts **exclusion of row t**
— a window that includes the current value fails.

---

## 🥇 Gold — Future-Proof Features (~75 min)

**Task:** Implement `features_without_future(series, cutoff, window)`: build
the no-leak feature table (as in Silver) but **only for rows strictly before
`cutoff`** — the training window. Then implement `verify_no_future_leak(full,
truncated)` which returns True if the truncated frame's features for the
overlapping rows match the full frame's features exactly (up to float
tolerance) — i.e., the presence of the future changes nothing.

**Signature:**
```python
def features_without_future(series: pd.Series, cutoff: pd.Timestamp, window: int) -> pd.DataFrame:
def verify_no_future_leak(full: pd.DataFrame, truncated: pd.DataFrame) -> bool:
```

| Input | Expected |
|---|---|
| 30 days, cutoff = day 20, window 5 | truncated has 19 rows; matches `full` for rows 0..18 |
| spike of 10^6 right after cutoff | `verify_no_future_leak` still True — the spike changes nothing before it |
| cutoff before the first window | truncated is empty (no complete rows) |

**Constraints:** `n <= 10^4`. A feature builder that uses `series` *after*
filtering (including future values) fails `verify_no_future_leak`.

**Follow-up:** why is `verify_no_future_leak` a stronger test than comparing
mean values? (Answer: it pins the *structure* — every lag and window column
is identical with and without the future — not just one statistic.)

---

## Running

```bash
pytest challenges/41-timeseries-advanced/test_challenge.py -v
```

## Test File Structure

```
challenges/41-timeseries-advanced/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
