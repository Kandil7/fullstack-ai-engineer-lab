# 03-libraries/pandas — 39: Method Chaining

## Topic Overview

Method chaining is the style where a data transformation pipeline is written as
one expression: each method call returns a new object and the next call starts
from it. `df.query(...).assign(...).sort_values(...)` is a chain; the same
pipeline written as five intermediate variables is stepwise code. Both compute
the same thing — the difference is reviewability, testability, and safety.

For AI engineers this is the difference between a feature-engineering notebook
and a feature-engineering *system*. Chains force every transform to return a
new frame, which means no hidden mutation of shared state, and they make the
order of operations visible top-to-bottom. Chaining is also where the
infamous `SettingWithCopyWarning` lives: it fires exactly when you try to
*write through* a chain, and the fix — one `.loc` selection — is a chain
discipline. This lecture covers `.query`, `.assign`, `.pipe`, copy semantics,
and the production shape of a reviewed feature pipeline.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Convert a stepwise pipeline into an equivalent method chain
2. Filter with `.query()` including `@variable` references
3. Add columns with `.assign()`, using callables to see intermediate frames
4. Plug arbitrary functions into a chain with `.pipe()`
5. Explain exactly why chained assignment raises `SettingWithCopyWarning`
6. Write chained writes with a single `.loc` selection instead
7. Distinguish deep vs shallow copies and their mutation semantics
8. Build a production feature-engineering chain from named functions

## Prerequisites

| Need | Where |
|------|-------|
| Boolean filtering | `03-filtering-lecture.md` |
| `.loc` / `.iloc` | `02-indexing-selection-lecture.md` |
| `groupby` basics | `08-groupby-aggregation-lecture.md` |

## 1. What a Chain Is — and Why It Is Safer

A chain is a sequence of calls where each call *returns* the object the next
call consumes. The safety property is in the returns: most pandas methods
return **new** objects, so nothing in a chain mutates a frame you still hold.

```python
import pandas as pd

df = pd.DataFrame({"user": [1, 2, 3, 4], "spend": [50, 120, 300, 400]})

# Stepwise: five statements, five chances to touch the wrong frame
step1 = df[df["spend"] > 100]
step2 = step1.assign(rank=step1["spend"].rank(ascending=False))
step3 = step2.sort_values("spend", ascending=False)

# Chained: one expression, same result, read top to bottom
chained = (
    df[df["spend"] > 100]
    .assign(rank=lambda d: d["spend"].rank(ascending=False))
    .sort_values("spend", ascending=False)
)

print(step3.equals(chained))   # True
```

```text
True
```

The chain's contract: every link returns a new frame, so `df` is untouched at
the end. The stepwise version *also* leaves `df` untouched — but nothing
*enforces* it, and a later edit can slip in an in-place mutation.

## 2. `.query()` — SQL-Style Filtering in the Chain

`.query()` evaluates a string expression against the frame. It is equivalent
to boolean indexing but reads like SQL and removes the repeated `df["col"]`
noise. Local variables are referenced with `@name`.

```python
min_spend = 150.0
city = "SF"

df_geo = pd.DataFrame({
    "city": ["NYC", "SF", "LA", "SF", "NYC"],
    "spend": [50.0, 120.0, 300.0, 400.0, 25.0],
})

q1 = df_geo.query("spend > 150")
q2 = df_geo.query("spend > @min_spend and city == @city")

# Equivalent boolean indexing
b2 = df_geo[(df_geo["spend"] > min_spend) & (df_geo["city"] == city)]

print(q1["spend"].tolist())          # [300.0, 400.0]
print(q2["spend"].tolist())          # [300.0, 400.0]
print(q2.equals(b2))                 # True
```

```text
[300.0, 400.0]
[300.0, 400.0]
True
```

Rules to remember: string columns need quotes inside the expression
(`city == 'SF'` — or `@city`), `and`/`or`/`not` are the keywords (not
`&`/`|`/`~`), and index labels are available as bare names like any column.

## 3. `.assign()` — Adding Columns, With a Subtle Trap

`.assign()` returns a new frame with the given columns added. The trap is
*what* you pass: a precomputed `Series` is computed once, before the chain
runs; a **callable** `lambda d: ...` receives the frame as it exists *at that
point in the chain* — after all earlier filters and assigns.

```python
fresh = pd.DataFrame({
    "spend": [400.0, 350.0, 200.0, 50.0, 300.0],
    "plan": ["pro", "pro", "free", "free", "free"],
})

# Callable: ranks the FILTERED frame (free users only)
good = (
    fresh.query("plan == 'free'")
    .assign(rank=lambda d: d["spend"].rank(ascending=False))
)

# Precomputed Series: ranks the FULL frame — silently wrong
bad = fresh.query("plan == 'free'").assign(
    rank=fresh["spend"].rank(ascending=False)
)

print(good["rank"].tolist())   # [2.0, 3.0, 1.0]
print(bad["rank"].tolist())    # [4.0, 5.0, 3.0]
```

```text
[2.0, 3.0, 1.0]
[4.0, 5.0, 3.0]
```

The two results differ because removing the `pro` rows (the highest spends)
shifts every rank. The precomputed Series kept ranks 4 and 5 — values that
refer to rows that were filtered out. Always use a callable when the new
column depends on the *state of the frame inside the chain*.

## 4. `.pipe()` — Plugging Custom Functions In

`.pipe(f)` calls `f(current_frame)` and returns whatever `f` returns. This is
the extension point: any function — yours, another library's — joins the
chain, and it receives the frame as it is at that moment.

```python
def drop_missing_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.dropna()

def add_ratio(frame: pd.DataFrame, num: str, den: str, out: str) -> pd.DataFrame:
    return frame.assign(**{out: frame[num] / frame[den]})

def flag_high(frame: pd.DataFrame, col: str, threshold: float) -> pd.DataFrame:
    return frame.assign(**{col + "_high": frame[col] > threshold})

result = (
    df_geo
    .pipe(drop_missing_rows)
    .pipe(add_ratio, "spend", "spend", "ratio")
    .pipe(flag_high, "spend", 100.0)
)
print(result.columns.tolist())
```

```text
['city', 'spend', 'ratio', 'spend_high']
```

`pipe` is how chains stay readable past ~6 links: instead of one giant
lambda, each custom step becomes a named, unit-testable function.

## 5. Deep vs Shallow Copies — What `.copy()` Really Gives You

`copy(deep=True)` (the default) produces an independent frame: mutating the
copy never touches the original. `copy(deep=False)` shares the underlying
data blocks — it is cheap but writes propagate to the parent. Shallow copies
are for read-only reuse; any write through one is a potential bug.

```python
original = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

deep = original.copy(deep=True)
deep.iloc[0, 0] = 999
print(original["a"].tolist())   # [1, 2, 3]  -- untouched

shallow = original.copy(deep=False)
shallow.iloc[0, 0] = 999
print(original["a"].tolist())   # [999, 2, 3]  -- shares the block!
```

```text
[1, 2, 3]
[999, 2, 3]
```

Rule: `.copy()` default is safe; `copy(deep=False)` is a performance choice
you must be able to justify. When in doubt, deep.

## 6. `SettingWithCopyWarning` — Explained Properly

The warning fires when you set a value through a *chain of selections*:
`df[mask]["col"] = x` or `sub = df[mask]; sub["col"] = x`. pandas cannot
prove whether the intermediate object is a view or a copy, so it warns. In
pandas 2.2 the boolean-mask path warns **and** silently drops the write; the
iloc-slice path warns too. Either way the value does not reliably reach the
frame — and if it *does* reach it (view semantics), it lands where you did
not intend.

```python
import warnings

df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
df["flag"] = 0

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    sub = df[df["a"] > 1]
    sub["flag"] = 1
    warned = any(w.category.__name__ == "SettingWithCopyWarning"
                 for w in caught)

print("warned:", warned)                  # True
print("stuck in df:", int(df["flag"].sum()))   # 0 -- the write vanished

# The fix: ONE .loc selection
df.loc[df["a"] > 1, "flag"] = 1
print("after .loc:", int(df["flag"].sum()))    # 2
```

```text
warned: True
stuck in df: 0
after .loc: 2
```

The fix is always the same shape: one `.loc[row_condition, column] = value`.
No intermediate, no ambiguity, no warning, no silent loss.

## 7. The Production Feature Chain

The senior shape: a single function that (1) copies defensively, (2) filters
early, (3) adds columns with callables, (4) pipes in named helpers, and
(5) sorts at the end — every step reviewable in isolation.

```python
def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Build the ML feature set for a user-spend dataset.

    Chain order matters: filter BEFORE group stats so the stats describe
    the cohort the model will actually see.
    """
    return (
        frame
        .copy()
        .pipe(drop_missing_rows)
        .query("spend > 0")
        .assign(
            log_spend=lambda d: np.log1p(d["spend"]),
            spend_rank=lambda d: d["spend"].rank(ascending=False),
            is_power_user=lambda d: d["spend"] >= d["spend"].quantile(0.8),
        )
        .pipe(flag_high, "spend", 300.0)
        .sort_values("spend", ascending=False)
    )
```

Because every step returns a new frame, the function is deterministic,
unit-testable at each stage, and safe to run in a pipeline where other code
still holds `frame`.

## Common Mistakes to Avoid

### Mistake 1: Writing through a chain and assuming it sticks

```python
# WRONG — the write lands in a copy and is lost
df[df["a"] > 1]["flag"] = 1
# CORRECT — one selection, always writes
df.loc[df["a"] > 1, "flag"] = 1
```

### Mistake 2: `.assign()` with a precomputed Series instead of a callable

```python
# WRONG — ranks the FULL frame, values refer to filtered-out rows
df.query("spend > 100").assign(rank=df["spend"].rank())
# CORRECT — sees the frame at this point in the chain
df.query("spend > 100").assign(rank=lambda d: d["spend"].rank())
```

### Mistake 3: `inplace=True` inside a chain

```python
# WRONG — dropna(inplace=True) returns None; the chain dies with
# 'NoneType' object has no attribute 'assign'
df.query("x > 0").dropna(inplace=True).assign(y=1)
# CORRECT — return the new frame
df.query("x > 0").dropna().assign(y=1)
```

### Mistake 4: Forgetting `@` for external variables in `.query()`

```python
# WRONG — NameError: name 'min_spend' is not defined
df.query("spend > min_spend")
# CORRECT
df.query("spend > @min_spend")
```

### Mistake 5: Mutating through a shallow copy

```python
# WRONG — copy(deep=False) shares blocks; the write hits the parent
tmp = df.copy(deep=False)
tmp.iloc[0, 0] = 999      # df changed too
# CORRECT — deep copy unless read-only
tmp = df.copy()
```

## Best Practices

1. Write every multi-step transform as a chain — one expression, top-to-bottom
2. Use callables (`lambda d: ...`) in `.assign()` whenever order matters
3. Use `@var` for external values in `.query()`
4. Put any non-pandas logic into a named function and `pipe` it
5. Write data with one `.loc` selection, never through a chain
6. Start chains with `.copy()` when the input frame is shared
7. Keep chains under ~10 links; split bigger pipelines into functions
8. Sort and select columns last, after filtering and assignment
9. Verify chain output against a stepwise version once during development
10. Never use `inplace=True` — it cannot chain and saves nothing

## Complexity and Cost

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `.query()` | O(n) | O(1) extra | vectorized string evaluation |
| `.assign()` | O(n) per column | O(n) | creates a new frame (no in-place) |
| `.pipe(f)` | cost of f | cost of f | no copying by itself |
| `.copy(deep=True)` | O(n) | O(n) | full duplication |
| `.copy(deep=False)` | O(1) | O(1) | shares blocks — writes propagate |
| chained write `df[m][c]=x` | O(n) | — | may silently write a copy: O(0) effect |
| `.loc[mask, col] = x` | O(n) | O(1) | the safe, single-pass write |

**At scale:** every `.assign` allocates a new frame, so a 50-step chain on a
200M-row frame pays 50 allocations. Measure with `memory_usage`; if memory is
the constraint, switch to `copy(deep=False)` in a controlled, read-mostly
pipeline — or use `polars`-style lazy frames. Correctness first, though: a
leaked write through a shallow copy is worse than a few extra allocations.

## AI Engineering Relevance

**Where this shows up:** feature engineering for training, online inference
preprocessing, and ETL into feature stores — any code path where raw rows
become model-ready columns.

| Concept here | Used for |
|--------------|----------|
| `.query()` | filtering cohorts before statistics (train/valid skew guard) |
| `.assign()` with callables | lagged/derived features that depend on filtered state |
| `.pipe()` | plugging `sklearn` transformers into a pandas pipeline |
| `.copy()` discipline | preventing batch jobs from mutating shared frames |
| single-`.loc` writes | safe label/annotation columns in eval datasets |

**Scale note:** at 1M rows a chain is still interactive. At 100M rows each
link's allocation matters and `SettingWithCopyWarning`-style bugs become
multi-hour recomputes. Chain for reviewability, then optimize the hot links —
never the other way around.

## Practice Exercises

### Exercise 1: Chain a Filter+Sort (Easy)
From `df_geo`, write one chain that keeps `spend > 100`, adds a
`log_spend` column with `np.log1p`, and sorts by spend descending. Compare
with the stepwise version with `.equals`.

### Exercise 2: Callable vs Precomputed (Medium)
On `fresh`, build the "free" cohort and add `rank` (descending) with a
callable. Then build the wrong version with a precomputed Series and explain
in a comment which values are wrong and why.

### Exercise 3: Pipe a Custom Function (Medium)
Write `add_bucket(frame, col, edges, labels)` that uses
`pd.cut` and add it to a chain with `.pipe`.

### Exercise 4: The Write Trap (Hard)
Reproduce the `SettingWithCopyWarning` on a boolean-mask sub-frame; capture
it with `warnings.catch_warnings`; verify the write did not stick; then fix
with `.loc` and verify it does.

## Summary

| Concept | Description |
|---------|-------------|
| Chain | one expression of transforms, each returning a new frame |
| `.query()` | SQL-style filter; `@var` for external values |
| `.assign()` | adds columns; callables see the intermediate frame |
| `.pipe(f)` | plugs named functions into the chain |
| deep vs shallow copy | deep is independent; shallow shares blocks |
| `SettingWithCopyWarning` | fires on chained writes; fix with one `.loc` |
| production chain | copy -> filter -> assign -> pipe -> sort |

Method chaining is the reviewable, mutation-safe style for data
transformation. The two skills that matter most: callables in `.assign()`
and one-`.loc` writes. Master both and your feature pipelines become
readable top-to-bottom and safe against the silent-write class of bugs.

## Quick Reference

| Task | Idiom |
|------|-------|
| Filter in a chain | `df.query("spend > @min and city == @c")` |
| Add a column from filtered state | `.assign(rank=lambda d: d["spend"].rank())` |
| Plug in a function | `.pipe(my_func, arg=1)` |
| Safe write | `df.loc[mask, "col"] = value` |
| Copy for reuse | `df.copy()` |
| Share blocks (read-only) | `df.copy(deep=False)` |
| Chain start | `df.copy().query(...).assign(...)` |

## Next Steps

Next: **[40 — Memory Optimization](40-memory-optimization-lecture.md)** —
downcasting and categories, the cheapest optimization in the stack.
Continues in: **[41 — Advanced Time Series](41-timeseries-advanced-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html
and https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy
