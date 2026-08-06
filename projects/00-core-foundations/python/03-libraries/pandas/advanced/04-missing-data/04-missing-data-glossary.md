# Missing Data — Glossary 04 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| NaN | Sentinel | Float missing marker (`np.nan`) |
| `None` | Sentinel | Python missing; cast to NaN in float columns |
| `pd.NA` | Sentinel | Type-aware missing for nullable dtypes |
| `isna()` | Method | Element-wise missing mask |
| `notna()` | Method | Inverse of `isna()` |
| missing fraction | Concept | `isna().mean()` — share missing per column |
| `dropna()` | Method | Remove rows/columns with missing values |
| `how="all"` | Option | Drop only rows where everything is missing |
| `thresh=` | Option | Keep rows/columns with >= N non-null |
| `subset=` | Option | Columns that must be complete |
| `fillna()` | Method | Fill missing with constants/statistics |
| `ffill()` | Method | Forward-fill the previous value |
| `bfill()` | Method | Backward-fill the next value |
| `interpolate()` | Method | Fill by fitting along the index |
| MCAR / MNAR | Concept | Missing completely/not-at-random |
| leakage | Concept | Using test data (e.g. global mean) to fill train |

## Detailed Definitions

### NaN
**Definition**: `np.nan` — the float missing marker; propagates through
arithmetic and compares unequal to itself.
**Example**:
```python
import numpy as np
x = np.nan
print(x == x)   # False
```
**Related**: `isna()`, `None`

### `None`
**Definition**: Python's missing object; in float columns it becomes `NaN`;
in object columns it stays `None`.
**Related**: NaN, `pd.NA`

### `pd.NA`
**Definition**: The nullable-dtype sentinel with type awareness — used with
`Int64`, `string`, `boolean` dtypes.
**Example**:
```python
s = pd.Series([1, 2, None], dtype="Int64")   # stays integer-typed
```
**Related**: nullable dtypes, NaN

### `isna()`
**Definition**: Element-wise boolean mask of missing values; `.sum()` counts,
`.mean()` gives fractions.
**Example**:
```python
df.isna().mean()
```
**Related**: `notna()`, missing fraction

### `notna()`
**Definition**: Element-wise inverse of `isna()` — True where data exists.
**Related**: `isna()`

### missing fraction
**Definition**: The per-column share of missing values (`isna().mean()`); the
input to the drop-vs-impute decision.
**Related**: `isna()`

### `dropna()`
**Definition**: Removes rows (or columns via `axis=1`) containing missing
values; configurable via `how`, `thresh`, `subset`.
**Example**:
```python
df.dropna(subset=["score"])
```
**Complexity**: O(n) copy.
**Related**: `thresh=`

### `how="all"`
**Definition**: `dropna` option dropping rows only when *every* selected
column is missing.
**Related**: `dropna()`

### `thresh=`
**Definition**: `dropna` option keeping rows/columns with at least N non-null
values — the data-quality gate.
**Example**:
```python
df.dropna(axis=1, thresh=int(0.8 * len(df)))
```
**Related**: `dropna()`

### `subset=`
**Definition**: The column list that must be complete for a row to survive
`dropna`.
**Related**: `dropna()`

### `fillna()`
**Definition**: Fills missing with a constant, a statistic (mean/median), or
a per-group transform.
**Example**:
```python
df["score"].fillna(df["score"].mean())
```
**Related**: imputation, leakage

### `ffill()`
**Definition**: Forward-fill — each missing gets the previous observed value;
the time-series default.
**Related**: `bfill()`, ordered data

### `bfill()`
**Definition**: Backward-fill — each missing gets the next observed value.
**Related**: `ffill()`

### `interpolate()`
**Definition**: Fills by fitting a curve along the index (linear, time,
quadratic) — smarter than constants for ordered data.
**Example**:
```python
df["temp"].interpolate(method="time")
```
**Related**: `ffill()`, time series

### MCAR / MNAR
**Definition**: Missing completely at random vs missing not at random. MNAR
means missingness itself carries information — encode it as a feature.
**Related**: missingness flag, isna

### leakage
**Definition**: Using information from outside the training rows (e.g. the
global mean computed on the full dataset) to fill training data — inflates
eval scores.
**Example**:
```python
# WRONG
df["c"] = df["c"].fillna(df["c"].mean())   # before the split
```
**Related**: imputation, train/test discipline

## Key Concepts Summary

### Sentinel semantics
- float columns: `None` -> NaN; `pd.NA` for type-aware nullable dtypes
- NaN propagates and never equals itself

### The decision inputs
- `isna().mean()` maps the missingness
- fractions ~0: drop rows; ~0.3: impute deliberately; ~0.95: drop column or flag

### The leakage rule
- Fit imputation statistics (means, medians) on train only
- Apply the same fitted values to test/val

### Missingness as signal
- MNAR patterns deserve an `isna()` flag column, not blind imputation

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `pd.NA` — ___
2. `isna().mean()` — ___
3. `thresh=` — ___
4. `ffill()` — ___
5. `interpolate()` — ___
6. leakage — ___
7. MNAR — ___
8. `fillna()` — ___

A. Missing-not-at-random: missingness is informative
B. Type-aware missing sentinel
C. Keep rows/cols with >= N non-null
D. Missing fraction per column
E. Filling with the previous value
F. Test-data statistics leaking into train
G. Filling by fitting along the index
H. The imputation method family

**Answers:** 1-B, 2-D, 3-C, 4-E, 5-G, 6-F, 7-A, 8-H
