# Polars 01 — Introduction Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df.shape)
print(df.columns)
```

- A) `(3, 2)` `['a', 'b']`
- B) `(2, 3)` `['a', 'b']`
- C) `(3, 2)` `['0', '1']`
- D) `(2, 3)` `['x', 'y', 'z']`

**E2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df["a"].to_list())
print(df["b"][1])
```

- A) `[1, 2, 3]` `y`
- B) `[1, 2, 3]` `x`
- C) `{'a': [1, 2, 3]}` `y`
- D) `[1, 2, 3]` `'y'`

**E3.** `df.select(pl.col("a").mean())` returns:

- A) a DataFrame with a single row and column
- B) a plain Python float
- C) a Series
- D) a LazyFrame

**E4 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df.head(2).to_dict(as_series=False))
```

- A) `{'a': [1, 2], 'b': ['x', 'y']}`
- B) `{'a': [1, 2, 3], 'b': ['x', 'y', 'z']}`
- C) `{'a': [2, 3], 'b': ['y', 'z']}`
- D) `[{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}]`

**E5.** Which of these filters rows in Polars?

- A) `df.filter(pl.col("a") > 1)`
- B) `df[df["a"] > 1]`
- C) `df.query("a > 1")`
- D) `df.loc[df["a"] > 1]`

**E6 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df["a"].sum())
print(df["b"].len())
```

- A) `6` `3`
- B) `6` `1`
- C) `[1, 2, 3]` `3`
- D) `3` `6`

---

## Medium

**M1.** Given
```python
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
```
`df.schema["b"]` is:

- A) `String`
- B) `str`
- C) `Utf8`
- D) `'<string>'`

**M2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [3, 1, 2]})
print(df.sort("a", descending=True)["a"].to_list())
```

- A) `[3, 2, 1]`
- B) `[1, 2, 3]`
- C) `[3, 1, 2]`
- D) `[2, 1, 3]`

**M3 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, None, 3]})
print(df.select(pl.col("a").sum()).item())
```

- A) `4`
- B) `null`
- C) `6`
- D) raises `TypeError`

**M4.** Which rows are returned by
`df.filter(pl.col("a").is_in([1, 3]))` on `{"a": [1, 2, 3]}`?

- A) rows 1 and 3
- B) row 1 only
- C) rows 1, 2 and 3
- D) nothing (an empty frame)

**M5 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df.filter([True, False, True]).rows())
```

- A) `[(1, 'x'), (3, 'z')]`
- B) `[(1, 'x'), (2, 'y')]`
- C) `[True, False, True]`
- D) raises `ShapeError`

**M6.** `df.describe()` includes which statistic rows (Polars 1.x)?

- A) count, null_count, mean, std, min, 25%, 50%, 75%, max
- B) count, mean, std, min, median, max
- C) count, null_count, mean, median, mode, max
- D) count, mean, std, skew, kurt, max

**M7 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
print(df.dtypes)
```

- A) `[Int64, String]`
- B) `[int, str]`
- C) `['int64', 'string']`
- D) `{'a': Int64, 'b': String}`

**M8.** Reading `pl.read_csv` on a CSV whose column contains `"3"` produces:

- A) an `Int64` column (inference)
- B) a `String` column always (strict, no coercion)
- C) a `Float64` column
- D) an error

**M9 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3]})
print(df.select(pl.col("a").mean()).item())
```

- A) `2.0`
- B) `2`
- C) `6.0`
- D) `[2.0]`

---

## Hard

**H1.** Which statement about
`df.lazy().filter(pl.col("a") > 1).collect()` is true?

- A) the filter is executed only at `collect()`
- B) the filter is executed at `.lazy()`
- C) the filter is executed at `.filter()`
- D) `collect()` just validates the plan without running it

**H2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": ["1", "2"]})
print(df.schema["a"])
```

- A) `String`
- B) `Int64`
- C) `Float64`
- D) `Int32`

**H3.** On a Windows cp1252 terminal, `print(df)` on a multi-column
Polars DataFrame:

- A) raises `UnicodeEncodeError` (box-drawing glyphs not encodable)
- B) prints a plain ASCII table
- C) prints nothing and returns silently
- D) crashes the interpreter

**H4.** Which is the O(1) way to get the row count of an eager frame?

- A) `df.height`
- B) `df.select(pl.len()).collect()`
- C) `len(df.to_numpy())`
- D) `df.describe()`

**H5.** Constructing `pl.DataFrame({"a": ["1", "2"]})` yields a
`String` column. Why?

- A) Polars construction is strict: strings are never auto-coerced to
  numbers
- B) Polars cannot parse `"1"` as an integer
- C) column names must be strings, so values stay strings too
- D) the default dtype is always `String`

---

## Answer Key

**E1 — A.** `shape` is (rows, columns) = (3, 2); `columns` lists the
column *names* `['a', 'b']`.
*Distractors:* B swaps rows/columns; C mislabels with positional
indices; D is the *values* of column `b`.

**E2 — A.** `df["a"]` returns a Series; `.to_list()` gives
`[1, 2, 3]`. `df["b"][1]` indexes the Series by position → `"y"`.
*Distractors:* B forgets 0-based indexing; C conflates the DataFrame
dict view; D shows a repr-quoted string.

**E3 — A.** Aggregations over a column return a 1×1 DataFrame.
`.item()` extracts the scalar; without it you hold a frame.
*Distractors:* B is what `.item()` gives; C is the intermediate
Series; D never happens with `select` on an eager frame.

**E4 — A.** `head(2)` keeps the first two rows; `to_dict(as_series=False)`
renders plain Python lists.
*Distractors:* B is no head at all; C is `tail(2)`; D is a list of row
dicts (a different orientation).

**E5 — A.** The canonical Polars filter takes an **expression**
(`pl.col("a") > 1`); a list mask also works, but the expression form
is the idiom.
*Distractors:* B/C/D are pandas idioms that do not exist on Polars
DataFrames (no `__getitem__` masking, no `.query`, no `.loc`).

**E6 — A.** `sum()` = 6; `.len()` on a Series of 3 rows = 3.
*Distractors:* B confuses rows with columns; C returns the whole
Series; D swaps the two answers.

**M1 — A.** `df.schema` maps names to Polars DataType classes;
`schema["b"]` is the `String` class (repr `String`).
*Distractors:* B is the Python builtin; C is the deprecated pre-1.0
name (`Utf8` was renamed to `String`); D is a string literal.

**M2 — A.** `sort(descending=True)` puts the largest first:
`[3, 2, 1]`.
*Distractors:* B is ascending; C/D are not sorted at all.

**M3 — A.** Aggregations skip nulls: `1 + 3 = 4`.
*Distractors:* B would apply if the result were null (it is not — sum
of non-null values); C adds the null as if 0; D confuses null-tolerant
Polars with NaN-propagating numpy.

**M4 — A.** `is_in([1, 3])` selects rows whose value is in the list —
rows 1 and 3.
*Distractors:* B drops row 3; C ignores the list; D is false — the
list is a membership test, not a mask.

**M5 — A.** A list of booleans is accepted as a row mask:
`(1, 'x')` and `(3, 'z')` survive.
*Distractors:* B is the wrong half; C returns the mask itself; D
confuses row masks with column counts (mask length must equal rows).

**M6 — A.** Polars 1.x `describe()` emits count, null_count, mean,
std, min, 25%, 50%, 75%, max.
*Distractors:* B is the old (pre-1.0) set; C invents mode/skew rows;
D is pandas-style describe.

**M7 — A.** `df.dtypes` is a list of Polars DataType classes in
column order.
*Distractors:* B is the numpy mapping; C is string reprs; D is the
`schema` dict shape.

**M8 — A.** CSV parsing infers `"3"` as `Int64`. (Contrast: DataFrame
*construction* is strict and keeps strings — H5.)
*Distractors:* B is true for construction, not for CSV inference; C
would need a decimal point; D is false — inference is the default.

**M9 — A.** `mean()` of `[1, 2, 3]` is `2.0`; `.item()` extracts the
scalar from the 1×1 frame.
*Distractors:* B loses the float type; C is the sum; D is the frame
value without `.item()`.

**H1 — A.** Lazy execution defers every step until `collect()` — that
is the entire contract of `LazyFrame`.
*Distractors:* B/C run eager; D inverts the semantics (`collect()`
runs the plan).

**H2 — A.** Polars 1.x construction is strict: string values stay
`String`. (Verified in the lab: even a single `"1"` is not coerced.)
*Distractors:* B is what pandas/CSV inference would do; C/D invent
numeric coercions.

**H3 — A.** The default table renderer uses box-drawing Unicode glyphs
that cp1252 cannot encode → `UnicodeEncodeError` on `print`. The safe
inspection is `df.to_dict(as_series=False)` / `df.rows()`.
*Distractors:* B is false — the glyphs are not ASCII; C is false — it
raises; D overstates (it is a catchable exception, not a crash).

**H4 — A.** `df.height` is a stored O(1) attribute.
*Distractors:* B scans the frame (O(n)); C materializes numpy (O(n));
D builds a full statistics table.

**H5 — A.** Construction is strict by design: no implicit coercion, so
`"1"` stays a string. Cast explicitly with `.cast(pl.Int64)`.
*Distractors:* B is false (Polars can parse strings); C confuses names
with values; D is false — dtypes are per-column, not fixed to String.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 01](03-libraries/polars/lectures/01-introduction-lecture.md) ·
[Glossary 01](03-libraries/polars/lectures/01-introduction-glossary.md) ·
[Challenge 01](03-libraries/polars/challenges/01-introduction/README.md)
