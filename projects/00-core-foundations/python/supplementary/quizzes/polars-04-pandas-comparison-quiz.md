# Polars 04 — pandas Comparison Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** `pl.from_pandas(pdf)` converts a pandas DataFrame into:

- A) a Polars DataFrame (memory copy)
- B) a view sharing memory with the pandas frame
- C) a LazyFrame
- D) a numpy array

**E2 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"i": [1, 2], "s": ["a", "b"]})
print(pl.from_pandas(pdf).dtypes)
```

- A) `[Int64, String]`
- B) `[int64, object]`
- C) `[Int64, Utf8]`
- D) `[i, s]`

**E3.** A Polars DataFrame has:

- A) no `index` — row positions are implicit
- B) an integer index like pandas, settable via `.set_index()`
- C) a string index by default
- D) an index only after `sort()`

**E4 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"f": [1.5, float("nan")]})
print(pl.from_pandas(pdf)["f"].to_list())
```

- A) `[1.5, None]`
- B) `[1.5, nan]`
- C) `[1.5, NaN]`
- D) `[1.5, 0.0]`

**E5.** The pandas method `.groupby("col")` is spelled in Polars as:

- A) `.group_by("col")`
- B) `.groupby("col")`
- C) `.group("col")`
- D) `.group_by_key("col")`

**E6 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"i": [1, 2], "s": ["a", "b"]})
print(pl.from_pandas(pdf)[["i", "s"]].columns)
```

- A) `['i', 's']`
- B) `['i']`
- C) `[0, 1]`
- D) raises `KeyError`

---

## Medium

**M1.** `df[["a", "b"]]` on a Polars DataFrame:

- A) returns a DataFrame with the two selected columns
- B) returns a Series
- C) is invalid — use `.select` only
- D) returns a numpy array

**M2 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"g": ["x", "y", "x"], "v": [1, 2, 3]})
out = (pl.from_pandas(pdf)
       .group_by("g")
       .agg(pl.col("v").sum().alias("sum_v"))
       .sort("g"))
print(out.rows())
```

- A) `[('x', 4), ('y', 2)]`
- B) `[('x', 4), ('y', 2)]` with an index column
- C) `[('x', 3), ('y', 2)]`
- D) `[('x', 1), ('y', 2), ('x', 3)]`

**M3.** After `pl.from_pandas(pdf)` where `pdf` has an object column,
the Polars column is:

- A) `String` — object/str maps to String
- B) `object`
- C) `Categorical`
- D) `Utf8` (deprecated alias kept only for pandas compat)

**M4.** Which pandas idiom has **no direct equivalent** in Polars
(and must be replaced)?

- A) boolean-mask filtering `pdf[pdf["a"] > 0]`
- B) `reset_index()` after a groupby
- C) `df.rename(columns={...})`
- D) `df.drop(columns=[...])`

**M5 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"a": [3, 1, 2]})
out = pl.from_pandas(pdf).sort("a")
print(out["a"].to_list())
print(type(out).__name__)
```

- A) `[1, 2, 3]` `DataFrame`
- B) `[3, 1, 2]` `DataFrame`
- C) `[1, 2, 3]` `Series`
- D) `[1, 2, 3]` `LazyFrame`

**M6.** `pl.from_pandas(pdf)` treats a float `NaN` as:

- A) Polars `null` (NaN is converted by default)
- B) an error — NaN is unsupported
- C) the float `0.0`
- D) a special `NaN` value distinct from `null`

**M7 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"s": ["a", "b"]})
back = pl.from_pandas(pdf).to_pandas()
print(back["s"].dtype)
```

- A) `object`
- B) `string`
- C) `String`
- D) `str`

**M8.** Which is the recommended migration path for a small dataframe
workflow?

- A) verify parity on a sample with both engines, then port the
  pipeline to expression-only Polars
- B) run pandas and Polars side by side forever in production
- C) convert every pandas call with `.apply()` ported one-to-one
- D) rewrite by writing SQL views

**M9.** Which of these is an *expression-only* Polars aggregation
(no row loops)?

- A) `df.group_by("g").agg(pl.col("v").mean())`
- B) `df.group_by("g").apply(lambda d: d["v"].mean())`
- C) `[row for row in df.iter_rows()]`
- D) `df.to_pandas().groupby("g").mean()`

---

## Hard

**H1.** Why does `reset_index()` have no Polars equivalent?

- A) Polars has no index — grouping produces flat key/aggregate
  columns directly
- B) Polars keeps the index but hides it from `columns`
- C) reset_index exists but only for LazyFrames
- D) pandas drops the index automatically after groupby in recent
  versions

**H2 (code-output).** What prints?
```python
import pandas as pd
import polars as pl
pdf = pd.DataFrame({"v": [1.0, 2.0, 3.0]})
print(pl.from_pandas(pdf).select(pl.col("v").mean()).item())
```

- A) `2.0`
- B) `2`
- C) `[2.0]`
- D) `6.0`

**H3.** A pandas pipeline `pdf.groupby("g")["v"].sum().reset_index()`
becomes in Polars:

- A) `pl.from_pandas(pdf).group_by("g").agg(pl.col("v").sum())` —
  the output is already flat
- B) the same call plus an explicit `reset_index()`
- C) `pl.from_pandas(pdf).group_by("g").sum("v")` — different result
- D) a pandas-to-polars `.to_lazy()` bridge

**H4.** Which statement about pandas `NaN` vs Polars `null` is true?

- A) pandas `NaN` is a float sentinel; Polars `null` is a typed
  missing value — aggregations skip both, but `null` works for any
  dtype
- B) they are the same object
- C) Polars `null` can only live in float columns
- D) pandas has no missing-value concept

**H5.** The fastest way to move a 10 GB pandas-loaded dataset into a
Polars-native pipeline is:

- A) write it to parquet once, then `pl.scan_parquet` it lazily
- B) call `pl.from_pandas` on the whole frame in one go
- C) iterate rows and append to a list
- D) convert via JSON

---

## Answer Key

**E1 — A.** `from_pandas` copies the data into a Polars DataFrame.
*Distractors:* B is false (a copy, not a view); C needs `.lazy()`
afterwards; D is a different structure.

**E2 — A.** int64 → `Int64`, object/str → `String`.
*Distractors:* B is the pandas dtypes; C uses the deprecated `Utf8`
name; D is column names, not types.

**E3 — A.** Polars has no index concept — row position is implicit.
*Distractors:* B/C describe pandas; D is false.

**E4 — A.** NaN converts to Polars `null` by default.
*Distractors:* B/C keep the pandas sentinel; D invents a zero-fill.

**E5 — A.** The Polars spelling is `group_by` (with underscore).
*Distractors:* B is pandas; C/D don't exist.

**E6 — A.** Polars supports column-list selection `df[["i", "s"]]`
and returns a DataFrame with those columns.
*Distractors:* B drops a column; C is positional labels; D is false —
this selection is valid.

**M1 — A.** Column-list selection returns a DataFrame.
*Distractors:* B is `df["a"]` (Series); C is false (the syntax is
supported); D is `to_numpy`.

**M2 — A.** x sums to 4, y to 2; no index column is added — the
output is flat.
*Distractors:* B invents an index; C miscounts x (1+3=4, not 3); D is
the ungrouped frame.

**M3 — A.** object/str → `String`.
*Distractors:* B is pandas dtype; C is a different mapping; D is the
old name (renamed to `String` in 1.0).

**M4 — B.** `reset_index` is meaningless in Polars because there is no
index.
*Distractors:* A works (expression filter); C/D have Polars
equivalents (`.rename`, `.drop`).

**M5 — A.** `sort("a")` returns a new DataFrame; `.to_list()` gives
`[1, 2, 3]`.
*Distractors:* B is the unsorted order; C is the wrong type (DataFrame,
not Series); D is wrong (eager sort stays eager).

**M6 — A.** `from_pandas` converts NaN to `null` by default
(`nan_to_null`).
*Distractors:* B is false; C is a fillna behavior, not default; D is
numpy's distinction, not Polars'.

**M7 — A.** The round trip maps `String` back to pandas `object`
dtype (verified).
*Distractors:* B is the pandas "string" dtype (opt-in); C is
`to_numpy`; D is the Python builtin.

**M8 — A.** The disciplined migration: prove parity on a sample, then
port to expression-only Polars.
*Distractors:* B is a maintenance anti-pattern; C keeps `.apply()`
row loops (the worst part of pandas); D changes the interface
entirely.

**M9 — A.** Expression-based aggregation — no Python loops.
*Distractors:* B is the `.apply()` row-loop antipattern; C is an
explicit loop; D re-imports pandas.

**H1 — A.** Grouping outputs flat key/aggregate columns; with no
index, there is nothing to reset.
*Distractors:* B is false (no index at all); C is false (not a
LazyFrame feature); D is about pandas, not Polars.

**H2 — A.** Mean of [1.0, 2.0, 3.0] = 2.0; `.item()` extracts the
scalar.
*Distractors:* B loses float; C is the frame value; D is the sum.

**H3 — A.** The Polars group_by output is already flat — no
reset_index step.
*Distractors:* B adds a nonexistent method; C changes the semantics;
D is not a real API.

**H4 — A.** pandas NaN is a float sentinel; Polars `null` is a
typed missing value available in every dtype.
*Distractors:* B is false; C is false (nulls live in String, Int64,
etc.); D is false.

**H5 — A.** Parquet + lazy scan is the recommended bridge: one
conversion, then streaming access.
*Distractors:* B materializes 10 GB in memory; C is row-by-row
Python; D is lossy and slow.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 04](03-libraries/polars/lectures/04-pandas-comparison-lecture.md) ·
[Glossary 04](03-libraries/polars/lectures/04-pandas-comparison-glossary.md) ·
[Challenge 04](03-libraries/polars/challenges/04-pandas-comparison/README.md)
