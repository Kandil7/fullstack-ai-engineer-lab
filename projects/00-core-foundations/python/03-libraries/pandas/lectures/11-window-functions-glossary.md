# Window Functions — Glossary 11 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `rolling()` | Method | Fixed-size trailing window aggregations |
| `expanding()` | Method | Growing window from the series start |
| `ewm()` | Method | Exponentially weighted window (recency) |
| `span=` | Argument | ewm decay in span form |
| `alpha=` | Argument | ewm decay directly (0..1) |
| `min_periods=` | Argument | Minimum observations before emitting a value |
| warm-up NaN | Concept | Leading NaN while the window is not full |
| `center=True` | Argument | Centers the window — uses FUTURE values |
| trailing window | Concept | Backward-looking window (feature-safe) |
| `.apply()` | Method | Custom per-window function (slow) |
| `.shift()` | Method | Lag by k positions |
| `.diff()` | Method | First difference |
| window size | Hyperparameter | How many observations each statistic uses |

## Detailed Definitions

### `rolling()`
**Definition**: Applies an aggregation over a fixed-size trailing window.
**Example**:
```python
s.rolling(7).mean()
```
**Complexity**: O(n) for named methods.
**Related**: window size, trailing window

### `expanding()`
**Definition**: The window grows from the first element — cumulative
statistics.
**Example**:
```python
s.expanding().mean()
```
**Related**: cumulative baseline

### `ewm()`
**Definition**: Exponentially weighted moving statistics — recent values
dominate; `span` and `alpha` are two spellings of the same decay.
**Example**:
```python
s.ewm(span=7).mean()
```
**Related**: `span=`, `alpha=`

### `span=`
**Definition**: ewm decay expressed as a span; `alpha = 2/(span+1)`.
**Related**: `alpha=`

### `alpha=`
**Definition**: ewm decay weight directly (higher alpha = more recency).
**Related**: `span=`

### `min_periods=`
**Definition**: The minimum number of observations required before a window
emits a value — eliminates warm-up NaNs.
**Example**:
```python
s.rolling(7, min_periods=1).mean()
```
**Related**: warm-up NaN

### warm-up NaN
**Definition**: The leading `window-1` values of a rolling result are NaN —
an explicit policy is required (min_periods, fill, drop).
**Related**: `min_periods=`

### `center=True`
**Definition**: Centers the window on the current point, using future values —
fine for smoothing, a leak for model features.
**Related**: trailing window

### trailing window
**Definition**: A backward-looking window (default) using only past + present
values — the leak-free feature form.
**Related**: `center=True`

### `.apply()`
**Definition**: Runs a Python function on each window for custom statistics —
O(n x window), use only when named methods cannot express the statistic.
**Example**:
```python
s.rolling(5).apply(lambda w: np.percentile(w, 95))
```
**Related**: rolling

### `.shift()`
**Definition**: Lags a series by k positions — the memory feature.
**Related**: `.diff()`

### `.diff()`
**Definition**: `s - s.shift(1)` — the momentum/detrend feature.
**Related**: `.shift()`

### window size
**Definition**: The number of observations per statistic — a model
hyperparameter trading noise vs lag.
**Related**: `rolling()`

## Key Concepts Summary

### The three windows
- rolling: fixed trailing
- expanding: cumulative from start
- ewm: exponential recency

### Leak discipline
- Features use trailing windows only (`center=False`)
- Warm-up NaNs need an explicit policy
- Window size is tuned, not guessed

### Performance
- Named methods O(n); `.apply` O(n x w) — avoid on big series

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `rolling(7).mean()` — ___
2. `expanding()` — ___
3. `ewm(span=7)` — ___
4. `min_periods=1` — ___
5. `center=True` — ___
6. `.diff()` — ___
7. `.shift(1)` — ___
8. warm-up NaN — ___

A. Cumulative window from start
B. Trailing 7-point mean
C. Exponentially weighted recency
D. Uses future values (smoothing only)
E. Eliminates leading NaNs
F. First difference
G. Previous-row lag
H. Leading NaN while the window fills

**Answers:** 1-B, 2-A, 3-C, 4-E, 5-D, 6-F, 7-G, 8-H
