# 03-libraries/pandas — 44: Pandas Pitfalls

## Topic Overview

This lecture is a catalog of the most expensive pandas mistakes: chained
assignment that silently drops writes, index alignment that turns arithmetic
into NaN soup, `inplace=True` that cannot chain, `NaN != NaN`, silent dtype
upcasting, `pct_change` fabricating deltas across gaps, `iterrows` at Python
speed, merge cardinality explosions, and the copy-on-write semantics that
change between pandas 2.x and 3.x.

Every item here is a real production incident — a model trained on missing
rows, a feature table that doubled in size overnight, a join that produced
three times the expected rows. The pattern behind all of them: pandas is
forgiving. It returns NaN instead of raising, it writes to copies instead of
erroring, and it never tells you. This lecture turns each forgiveness into a
habit that fails loudly instead.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain and avoid chained assignment; write with one `.loc`
2. Predict when index alignment will produce NaN
3. Avoid `inplace=True`; use explicit rebinding
4. Use `isna()`/`notna()` instead of `== np.nan`
5. Detect silent dtype upcasting and its consequences
6. Explain why `pct_change` needs `fill_method=None` across gaps
7. Replace `iterrows` with `itertuples` or vectorized ops
8. Guard merges against duplicate-key explosions
9. Write code that behaves correctly under both CoW modes

## Prerequisites

| Need | Where |
|------|-------|
| Indexing | `02-indexing-selection-lecture.md` |
| Method chaining | `39-method-chaining-lecture.md` |
| Memory/dtypes | `40-memory-optimization-lecture.md` |

## 1. Chained Assignment — the Write That Never Happens

`df[mask]["col"] = x` is two selections. The second one may operate on a
copy; pandas warns, and the write vanishes.

```python
import warnings
import numpy as np
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [10.0, 20.0, 30.0, 40.0]})
df["flag"] = 0

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    sub = df[df["a"] > 2]
    sub["flag"] = 1
    warned = any(w.category.__name__ == "SettingWithCopyWarning"
                 for w in caught)

print("warned:", warned)                  # True
print("stuck:", int(df["flag"].sum()))    # 0

df.loc[df["a"] > 2, "flag"] = 1
print("after .loc:", int(df["flag"].sum()))   # 2
```

```text
warned: True
stuck: 0
after .loc: 2
```

## 2. Index Alignment — Labels, Not Positions

Arithmetic aligns on **labels**. Mismatched labels produce NaN instead of an
error — silently.

```python
left = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
right = pd.Series([10.0, 20.0, 30.0], index=[1, 2, 3])

print((left + right).tolist())                    # [nan, 12.0, 23.0, nan]
print((left.reset_index(drop=True)
       + right.reset_index(drop=True)).tolist())  # [11.0, 22.0, 33.0]
```

```text
[nan, 12.0, 23.0, nan]
[11.0, 22.0, 33.0]
```

Same values, same order — different index, different result. When features
come from different pipelines, check index compatibility before combining.

## 3. `inplace=True` — Neither Faster Nor Cleaner

`inplace=True` performs the same work, returns `None`, and cannot chain.
The "saves memory" belief is usually wrong — pandas still allocates
internally.

```python
df_ip = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
result = df_ip.dropna(inplace=True)
print(result)                  # None
print(len(df_ip))              # 2 (it did mutate, but returns None)
```

```text
None
2
```

## 4. `NaN != NaN` — Compare With `isna()`, Never With `==`

NaN is not equal to anything, including itself. `s[s != np.nan]` removes
nothing.

```python
s = pd.Series([1.0, np.nan, 3.0, np.nan])
print(len(s[s != np.nan]))          # 4  -- filtered nothing
print(s[s.notna()].tolist())        # [1.0, 3.0]
```

```text
4
[1.0, 3.0]
```

## 5. `pct_change` — the Fill That Fabricates Deltas

`pct_change()` default-fills missing values before computing deltas. A gap
becomes a fabricated "no change", and the next delta is computed against a
value that never existed.

```python
import warnings

s = pd.Series([10.0, np.nan, 20.0])

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    fabricated = s.pct_change()               # fill_method='pad' (deprecated)
    honest = s.pct_change(fill_method=None)

print("fabricated:", fabricated.tolist())     # [nan, 0.0, 1.0]
print("honest:    ", honest.tolist())         # [nan, nan, nan]
print("warned:    ", any(w.category.__name__ == "FutureWarning" for w in caught))
```

```text
fabricated: [nan, 0.0, 1.0]
honest:     [nan, nan, nan]
warned:     True
```

The `0.0` claims "no change" for a week with no data; the `1.0` claims 100%
growth against a filled value. On a financial dashboard both are lies. Pass
`fill_method=None` — gaps must surface as NaN, and the human decides how to
treat them.

## 6. Silent Dtype Upcasting

pandas picks the safest dtype when values mix: int + float -> float64;
int + string -> object. pandas 2.2 warns on incompatible setitem
(FutureWarning); pandas 3 will raise. Either way, the column's dtype
changes under you.

```python
df_up = pd.DataFrame({"id": [1, 2, 3]})
df_up.loc[2, "id"] = "oops"
print(df_up["id"].dtype)        # object -- the int contract is gone
```

```text
object
```

## 7. `iterrows` — the O(n x Python) Trap

`iterrows` builds a Series per row and runs Python per row — 100-1000x
slower than vectorized ops. When you must loop, `itertuples` is 20-50x
faster.

```python
n = 5_000
loop_df = pd.DataFrame({"a": np.arange(n), "b": np.arange(n) * 2})

def with_iterrows(f):
    total = 0.0
    for _, row in f.iterrows():
        if row["a"] % 2 == 0:
            total += row["b"]
    return total

def with_itertuples(f):
    total = 0.0
    for row in f.itertuples(index=False):
        if row.a % 2 == 0:
            total += row.b
    return total

def vectorized(f):
    return float(f.loc[f["a"] % 2 == 0, "b"].sum())

print(with_iterrows(loop_df) == with_itertuples(loop_df) == vectorized(loop_df))
```

```text
True
```

Same answer, three cost classes. Print timings for yourself — never assert
wall-clock in code.

## 8. Merge Cardinality Explosions

A merge multiplies rows by the number of matching keys. Duplicate keys on
either side turn a "simple join" into a cross product.

```python
orders = pd.DataFrame({"cust": ["a", "a", "b"], "amt": [1, 2, 3]})
profile = pd.DataFrame({"cust": ["a", "a", "a"], "city": ["NY", "LA", "SF"]})

merged = orders.merge(profile, on="cust")
print(len(orders), len(profile), "->", len(merged))   # 3 3 -> 6
```

```text
3 3 -> 6
```

Two `a` orders x three `a` profiles = 6 rows. The fix is a guard (see the
production pattern).

## 9. Copy-on-Write — the Future Default

pandas 2.x: CoW off by default — views and shallow copies can alias the
parent. pandas 3.x: CoW on — every write copies, so aliases break. Code
that mutates a shallow copy and *expects* the parent to change breaks under
CoW; code that mutates it and *doesn't expect* the parent to change
silently corrupts data today.

```python
def slice_mutation(frame: pd.DataFrame) -> list[float]:
    view = frame.copy(deep=False)   # shares blocks
    view.iloc[0, 0] = 99
    return frame["a"].tolist()

pd.set_option("mode.copy_on_write", False)
print(slice_mutation(pd.DataFrame({"a": [1, 2, 3]})))   # [99, 2, 3]
pd.set_option("mode.copy_on_write", True)
print(slice_mutation(pd.DataFrame({"a": [1, 2, 3]})))   # [1, 2, 3]
pd.set_option("mode.copy_on_write", False)
```

```text
[99, 2, 3]
[1, 2, 3]
```

## 10. Production Pattern — a Pre-Merge Contract Check

Three lines turn a silent row explosion into a loud, immediate error.

```python
def merge_with_contract(left: pd.DataFrame, right: pd.DataFrame,
                        key: str) -> pd.DataFrame:
    assert right[key].is_unique, \
        f"right side key '{key}' must be unique; found duplicates"
    return left.merge(right, on=key)
```

## Common Mistakes to Avoid

### Mistake 1: `df[mask]["col"] = x`

```python
# WRONG — warns and silently drops the write
df[df["a"] > 1]["flag"] = 1
# CORRECT — one .loc selection
df.loc[df["a"] > 1, "flag"] = 1
```

### Mistake 2: `== np.nan`

```python
# WRONG — NaN never equals NaN; the filter removes nothing
s[s != np.nan]
# CORRECT
s[s.notna()]
```

### Mistake 3: assuming merge is 1:1

```python
# WRONG — duplicate keys multiply rows silently
df.merge(other, on="key")
# CORRECT — guard first
assert other["key"].is_unique
df.merge(other, on="key")
```

### Mistake 4: "optimizing" with `inplace=True`

```python
# WRONG — returns None; cannot chain; no real savings
df.dropna(inplace=True).assign(x=1)   # AttributeError
# CORRECT
df = df.dropna().assign(x=1)
```

### Mistake 5: trusting `pct_change()` across gaps

```python
# WRONG — ffill fills the gap: [10, NaN, 20] -> [nan, 0.0, 1.0]
s.pct_change()
# CORRECT — gaps surface as NaN; the human decides how to treat them
s.pct_change(fill_method=None)
```

## Best Practices

1. Write with one `.loc` selection — never through a chain
2. Use `isna()`/`notna()` exclusively for missing-value logic
3. Prefer explicit rebinding (`df = df.dropna()`) over `inplace`
4. Assert key uniqueness before every merge
5. Check index alignment before combining series from different sources
6. Loop with `itertuples` or vectorize; reserve `iterrows` for debugging
7. Check dtypes after any setitem that mixes types
8. Write and test under both CoW modes; never rely on aliasing
9. Pass `fill_method=None` to `pct_change` when gaps must not fabricate deltas

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| chained write | O(n) work, O(0) effect | — | `.loc[mask, col] = x` — O(n) |
| `iterrows` | O(n) Python + Series | O(n) | `itertuples` — O(n) tuples |
| `itertuples` | O(n) tuple | O(n) | vectorized — O(n) C-speed |
| merge with dup keys | O(n x m) | O(n x m) | guard + dedup keys first |
| `df.copy(deep=False)` write | O(1) alias | shared | deep copy for isolation |
| alignment mismatch | O(n) | O(n) NaN | `reset_index`/`set_axis` |

**At scale:** at 10M rows the pitfalls stop being cosmetic: a merge
explosion turns 10M rows into 300M, an `iterrows` loop runs for an hour, and
a chained write silently drops 40% of your labels. The guards cost three
lines; the incidents cost a day each.

## AI Engineering Relevance

**Where this shows up:** every batch job, every feature pipeline, every
model re-run — the silent-data class of failures.

| Concept here | Used for |
|--------------|----------|
| chained assignment | label/annotation writes that vanish |
| alignment NaN | features from different sources combining wrong |
| `NaN != NaN` | filters that keep missing rows |
| dtype upcasting | string landing in an int id column |
| `iterrows` | accidental O(n^2)-class preprocessing |
| merge explosion | join-based feature tables doubling silently |
| CoW semantics | code that works under pandas 2 AND 3 |
| `pct_change` ffill | fabricated deltas across missing values |

**Scale note:** in an offline notebook a pitfall costs a re-run; in a
scheduled pipeline it costs a bad model artifact that nobody notices until
production. The discipline is the same at every scale: fail loudly, assert
shapes, and never trust pandas to tell you when it forgave a bug.

## Practice Exercises

### Exercise 1: Spot the Vanished Write (Easy)
Create a frame, perform a chained write, and verify with `_verify`-style
asserts that the frame was unchanged — then fix with `.loc`.

### Exercise 2: Alignment Diagnosis (Medium)
Build two Series with shifted indices, add them, and explain which entries
are NaN and why. Then align with `reindex` and redo.

### Exercise 3: Merge Guard (Medium)
Implement `merge_with_contract`; verify it raises on duplicate right keys
and passes on unique ones.

### Exercise 4: CoW-Compatible Code (Hard)
Write a function that sets the first two rows of column `b` to 99 and
returns the frame — and verify it produces identical results under both
CoW modes (hint: deep copy first).

### Exercise 5: Gap-Honest Deltas (Medium)
Compute `pct_change` on `[10, NaN, 20, 30]` with and without
`fill_method=None`; explain which numbers are fabricated and which are
real, then fix the code to surface the gap as NaN.

## Summary

| Concept | Description |
|---------|-------------|
| chained assignment | warns; write vanishes; use one `.loc` |
| index alignment | label-based; mismatches become NaN |
| `inplace=True` | returns None; cannot chain |
| `NaN != NaN` | use `isna()`/`notna()` |
| dtype upcasting | int+string -> object, silently |
| `iterrows` | Python-per-row; use `itertuples` or vectorize |
| merge explosions | duplicate keys multiply rows |
| copy-on-write | aliasing semantics change between 2.x and 3.x |
| `pct_change` ffill | gaps silently become fabricated deltas |

Every pitfall here is pandas being forgiving. The antidote is the same in
all nine cases: assert what you believe about shape, values, and dtypes —
and let the machine fail loudly when reality disagrees.

## Quick Reference

| Task | Idiom |
|------|-------|
| Safe write | `df.loc[mask, "col"] = value` |
| Missing check | `s.isna()` / `s.notna()` |
| Explicit rebind | `df = df.dropna()` |
| Loop cheaply | `for row in df.itertuples(index=False):` |
| Merge guard | `assert right[key].is_unique` |
| Align series | `left.reindex(right.index)` |
| CoW on/off | `pd.set_option("mode.copy_on_write", True/False)` |

## Next Steps

Next: **[45 — Data Contracts & Validation](45-data-contracts-lecture.md)** —
defining what "good data" means before it reaches the model.
Continues in: **[44 — Pandas Pitfalls challenge](../challenges/44-pandas-pitfalls/README.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/indexing.html
and https://pandas.pydata.org/docs/user_guide/copy_on_write.html
