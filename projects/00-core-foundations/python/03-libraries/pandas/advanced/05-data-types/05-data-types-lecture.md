# 03-libraries/pandas (advanced) — 05: Data Types & Conversion

## Topic Overview

Every pandas column has a dtype — and the dtype decides what operations are
possible, how much memory the column uses, and what the model will see.
`astype()` converts between them; `to_datetime()` and `to_numeric()` parse
strings into real types; the `category` dtype compresses repeated labels.

For AI engineers, dtype discipline is a first-class modeling concern: a label
column read as `object` silently becomes 10,000 one-hot columns; a `category`
feature gets ordinal codes; a datetime string column blocks all time logic;
and every `object` column costs ~50 bytes per cell versus 1–8 for a real
dtype. The intake dtype audit (topic 01) exists precisely because of this.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read and explain the pandas dtype families (object, numeric, bool, datetime, category)
2. Convert with `astype()` safely and handle failure
3. Parse strings with `to_datetime()` and `to_numeric()`
4. Use nullable dtypes (`Int64`, `boolean`, `string`) with `pd.NA`
5. Convert to/from `category` and understand its cost
6. Control float precision and memory with dtype choice
7. Plan an intake type contract before building features

## Prerequisites

| Need | Where |
|------|-------|
| Inspecting dtypes | `01-inspecting-data-lecture.md` |
| NumPy dtypes | `03-libraries/numpy/lectures/06-data-types-lecture.md` |
| Missing data | `04-missing-data-lecture.md` |

## 1. The dtype Families

```python
df.dtypes
# user_id       int64
# score        float64
# active          bool
# created    datetime64[ns]
# city        category
# name          object
```

- `int64`/`float64` — numeric workhorses
- `bool` — True/False (also `boolean` nullable)
- `datetime64[ns]` — timestamps (also `datetime64[ns, tz]` aware)
- `category` — compressed repeated labels
- `object` — Python objects; usually strings; slow, ~50 B/cell

## 2. `astype()` — Explicit Conversion

```python
df["user_id"].astype(str)                # int -> string
df["score"].astype("float32")            # halve numeric memory
df["active"].astype(int)                 # bool -> 0/1
df["split"].astype("category")           # -> category codes
```

`astype` is a promise: it converts or raises (`ValueError` on non-convertible
strings, `TypeError` on impossible casts). For messy string->number parsing,
use `to_numeric(..., errors="coerce")` instead.

## 3. `to_datetime` / `to_numeric` — Parsing Real Types

```python
df["created"] = pd.to_datetime(df["created"])          # parse ISO strings
df["score"] = pd.to_numeric(df["score"], errors="coerce")
```

`errors="coerce"` turns unparseable values into `NaN` instead of raising —
the realistic choice for dirty data, followed by a missing-data decision.
`pd.to_datetime` also handles columns of mixed formats, with
`format=` available for speed on known layouts.

## 4. Nullable Dtypes — Int64, boolean, string

```python
df["user_id"] = df["user_id"].astype("Int64")     # int + pd.NA
df["active"] = df["active"].astype("boolean")
df["name"] = df["name"].astype("string")
```

Standard `int64` cannot hold missing values (a NaN silently forces float);
`Int64` can. `string` dtype is a true pandas string type (vs `object`
containing str). Use them when missingness is real and the type matters.

## 5. The category dtype — Compression with Rules

```python
df["split"] = df["split"].astype("category")
df["split"].cat.codes       # integer codes 0..n-1
df["split"].cat.categories  # the label list
```

`category` stores each unique label once and references it by code — smaller
and faster for low-cardinality columns. It also gives *ordinal ordering* when
you set ordered categories:

```python
df["size"] = pd.Categorical(df["size"], categories=["s", "m", "l"], ordered=True)
```

Watch the trap: `category` columns passed to sklearn are still strings unless
you take `.cat.codes` — category is not automatically numeric.

## 6. Memory — The dtype Is the Budget

```python
df.memory_usage(deep=True)               # per-column bytes
df["score"].astype("float32").memory_usage(deep=True)  # ~half
```

float64 -> float32 halves memory; int64 -> int32 halves again; object -> string
or category shrinks tens of bytes per cell. On a 10M-row frame these choices
are gigabytes.

## 7. Production Pattern — The Type Contract

```python
TYPE_CONTRACT = {
    "user_id": "Int64",
    "score": "float32",
    "active": "boolean",
    "created": "datetime64[ns, UTC]",
    "split": "category",
}

def apply_contract(df: pd.DataFrame, contract: dict) -> pd.DataFrame:
    """Cast a frame to its declared type contract; fail loudly on mismatch."""
    out = df.copy()
    for col, dtype in contract.items():
        out[col] = out[col].astype(dtype)
    return out
```

The contract is the schema of the dataset — declared once, reviewed in code
review, applied at every intake. This is the pandas side of schema validation
(see 08-mlops data validation).

## Common Mistakes to Avoid

### Mistake 1: `astype(int)` on dirty strings

```python
# WRONG — raises on "12.5" or "abc"
df["n"].astype(int)
# CORRECT — coerce to NaN first
pd.to_numeric(df["n"], errors="coerce")
```

### Mistake 2: Expecting category to be numeric for ML

```python
# WRONG — sklearn sees the category as strings/unknown
model.fit(df[["split"]], y)
# CORRECT — take the codes (or one-hot)
df["split_code"] = df["split"].cat.codes
```

### Mistake 3: Losing ints to float because of NaN

```python
# WRONG — None forces float64
s = pd.Series([1, 2, None])           # float64
# CORRECT — nullable Int64 keeps integers
s = pd.Series([1, 2, None], dtype="Int64")
```

### Mistake 4: Ignoring dtype when measuring memory

```python
# WRONG — object columns dominate the budget and go unnoticed
df.memory_usage()                     # misses deep object payloads
# CORRECT
df.memory_usage(deep=True)
```

## Best Practices

1. Audit dtypes at intake (topic 01) and convert once, early
2. `to_numeric(errors="coerce")` + a missing decision for dirty numbers
3. Parse datetimes with `to_datetime` before any time logic
4. Use nullable dtypes (`Int64`, `boolean`, `string`) for real missingness
5. Use `category` for low-cardinality repeated labels; take `.cat.codes` for ML
6. Choose float32/int32 deliberately when memory is the constraint
7. Encode the type contract as a dict and apply it at every intake

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `astype` | O(n) | full-column cast, new array |
| `to_numeric` | O(n) | parse pass; `errors="coerce"` keeps going |
| `to_datetime` | O(n) | parse pass; `format=` speeds known layouts |
| float64 -> float32 | O(n) | halves numeric memory |
| int64 -> Int64 | O(n) | enables NA at some overhead |
| object -> category | O(n) | factorize; big savings on repeats |
| `memory_usage(deep=True)` | O(payload) | the real budget view |

**At scale:** dtype choice is memory engineering. 10M rows x float64 = 80 MB;
float32 = 40 MB; and 10M object strings can be 500 MB+. The contract decides
whether a dataset fits RAM and how fast the pipeline runs.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| dtype contract | dataset schema enforced at intake (schema validation) |
| category codes | encoding categorical features for sklearn/torch |
| float32 | halving embedding-matrix and feature memory |
| Int64 + NA | keeping IDs integer despite missing values |
| to_datetime | time-based splits and features from log timestamps |
| nullable string | clean text handling with missing values |

**Scale note:** the model serving budget (topic 52 of phase 1) and the dataset
memory budget are the same arithmetic — dtype choice is a cost lever you pull
once at intake and benefit from everywhere.

## Practice Exercises

### Exercise 1: Contract Cast (Easy)
Apply the `TYPE_CONTRACT` above to a small frame and verify each column's
final dtype.

### Exercise 2: Dirty Numeric Parse (Medium)
Given a column with `"12"`, `"3.5"`, `"abc"`, `None`, use `to_numeric` with
coerce, report the NaN count, and fill with the column mean.

### Exercise 3: Memory Audit (Hard)
Build `memory_report(df)` returning per-column bytes with `deep=True`, total
MB, and the top-3 columns to downcast; suggest and apply float32/category
conversions.

## Summary

| Concept | Description |
|---------|-------------|
| dtype families | object, int, float, bool, datetime, category |
| `astype` | explicit cast — raises on impossible conversions |
| `to_numeric` / `to_datetime` | parse strings into real types, `coerce` dirty input |
| nullable dtypes | `Int64`, `boolean`, `string` with `pd.NA` |
| category | compressed codes; take `.cat.codes` for ML |
| memory | dtype choice is the dataset budget |
| type contract | the schema dict applied at every intake |

The dtype is the schema of your data. Decide it once, at intake, in a
reviewed contract — and the whole pipeline inherits the correctness, speed,
and memory profile you chose.

## Quick Reference

| Task | Idiom |
|------|-------|
| Audit dtypes | `df.dtypes` |
| Cast column | `df["c"] = df["c"].astype("float32")` |
| Parse numbers | `pd.to_numeric(s, errors="coerce")` |
| Parse datetimes | `pd.to_datetime(s)` |
| Nullable int | `s.astype("Int64")` |
| Categorical | `df["c"] = df["c"].astype("category")` |
| Ordinal codes | `df["c"].cat.codes` |
| Memory view | `df.memory_usage(deep=True)` |

## Next Steps

Next: **[06-string-methods](06-string-methods-lecture.md)** — the `.str` accessor.
Continues in: **[07-machine-learning — 09 scale](../../../../07-machine-learning/lectures/09-scale-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/basics.html#dtypes
