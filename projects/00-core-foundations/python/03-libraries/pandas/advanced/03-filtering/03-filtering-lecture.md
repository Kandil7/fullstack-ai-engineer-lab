# 03-libraries/pandas (advanced) — 03: Filtering — Query Techniques

## Topic Overview

Filtering is selection by *condition*: keep the rows that satisfy a rule. The
tools build on each other: boolean masks (fastest, most explicit), `.query()`
(readable compound conditions), `.isin`/`.between` (set and range membership),
and `.filter()` (name-based column/row filtering). The hidden distinction that
matters most is *filtering by values* (masks) vs *filtering by names*
(`df.filter`).

For AI engineers filtering is the data-governance layer: keeping only
high-confidence predictions, dropping out-of-distribution rows, selecting
eval subsets by document id, and applying user permissions to rows. Filtering
decisions ARE model decisions — the data you exclude shapes the model you get.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build compound masks with `&`, `|`, `~` and parentheses
2. Write readable filters with `.query()`
3. Use `.isin()`, `.between()`, `.str.contains()`, `.str.startswith()`
4. Filter by column names with `.filter()`
5. Use `df.drop_duplicates()` with subset and keep rules
6. Explain mask-vs-name filtering and pick the right tool
7. Build reusable filter functions for dataset governance

## Prerequisites

| Need | Where |
|------|-------|
| Selection basics | `02-indexing-selection-lecture.md` |
| String methods | `06-string-methods-lecture.md` |
| Boolean logic | `11-booleans.py` (core) |

## 1. Compound Masks — The Grammar

```python
import pandas as pd

df = pd.DataFrame({
    "doc": ["a", "b", "c", "d"],
    "score": [0.2, 0.8, 0.6, 0.9],
    "split": ["train", "train", "val", "test"],
})

# AND, OR, NOT — each comparison parenthesized
df[(df["score"] > 0.5) & (df["split"] != "test")]
df[(df["score"] > 0.5) | (df["doc"] == "a")]
df[~df["doc"].isin(["b", "d"])]
```

The grammar is fixed: `&`/`|`/`~` are element-wise and bind tighter than `>`,
so every comparison needs parentheses. There is no "and" for Series.

## 2. `.query()` — Conditions as Strings

```python
df.query("score > 0.5 and split != 'test'")
df.query("score > 0.7 or doc == 'a'")
df.query("split in ['val', 'test']")
```

`.query()` reads top-to-bottom like SQL WHERE. It supports `and`, `or`, `not`,
`in`, `==`, comparisons, and even `@` for Python variables:

```python
threshold = 0.6
df.query("score > @threshold")     # @ pulls the Python variable in
```

Use `.query()` when a filter is long or will be read by others; use raw masks
when you need the mask Series itself later (e.g. to reuse or to set values).

## 3. Set and Range Membership

```python
df[df["doc"].isin(["a", "c"])]                 # set membership
df[df["score"].between(0.5, 0.8, inclusive="both")]
df[df["doc"].str.contains("^[ab]", regex=True)]  # regex on strings
df[df["doc"].str.startswith("a")]              # prefix filter
```

`.str` methods are vectorized string ops (see topic 06). Note `.str.contains`
defaults to regex — pass `regex=False` for literal substring search.

## 4. Filtering by Name — `df.filter`

```python
df.filter(items=["score", "split"])            # by exact names
df.filter(like="sco")                           # substring match
df.filter(regex="^s")                           # regex on names
```

This is *name* filtering (columns/rows by label), not value filtering — the
two families solve different problems and are easy to confuse.

## 5. `drop_duplicates` — Dedup with Rules

```python
df.drop_duplicates(subset=["doc"])              # keep first per doc
df.drop_duplicates(subset=["doc"], keep="last")
df.drop_duplicates(subset=["doc"], keep=False)  # drop ALL duplicates
```

`keep=False` is the interesting one for data hygiene: it removes every row
with a duplicated key, leaving only singletons — the right move when duplicates
are suspicious rather than benign.

## 6. Production Pattern — Governed Subset Builder

```python
def select_inference_subset(
    df: pd.DataFrame,
    *,
    min_score: float = 0.7,
    allowed_splits: tuple[str, ...] = ("val", "test"),
    max_rows: int = 10_000,
) -> pd.DataFrame:
    """Deterministic, reusable subsetting for evaluation runs."""
    mask = (
        (df["score"] >= min_score)
        & (df["split"].isin(allowed_splits))
    )
    return df.loc[mask].head(max_rows).copy()
```

A single function encodes the evaluation governance rules — reviewers read one
expression, and the same rules apply to every experiment.

## Common Mistakes to Avoid

### Mistake 1: Unparenthesized comparisons

```python
# WRONG — & binds tighter than >, misparsed
df[df.a > 1 & df.b < 2]
# CORRECT
df[(df.a > 1) & (df.b < 2)]
```

### Mistake 2: `and`/`or` on Series

```python
# WRONG — ValueError: ambiguous truth value
df[(df.a > 1) and (df.b < 2)]
# CORRECT
df[(df.a > 1) & (df.b < 2)]
```

### Mistake 3: `.str.contains` without regex=False for literals

```python
# WRONG — "a.b" treated as regex (a + any char + b)
df[df.col.str.contains("a.b")]
# CORRECT — literal substring
df[df.col.str.contains("a.b", regex=False)]
```

### Mistake 4: Value filtering vs name filtering confusion

```python
# WRONG — .filter selects by NAME, not by value
df.filter(like="score")
# CORRECT for values
df[df["score"] > 0.5]
```

## Best Practices

1. Masks for explicit, reusable conditions; `.query()` for readable chains
2. Always parenthesize comparisons in compound masks
3. `regex=False` for literal `.str.contains` searches
4. `keep=False` in `drop_duplicates` when duplicates are suspect
5. Encode governance rules in named filter functions
6. Prefer `.isin`/`.between` over long OR chains

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| boolean mask | O(n) | vectorized comparison |
| `.query()` | O(n) | parse once + vectorized eval |
| `.isin()` | O(n) | hashed set lookup |
| `.between()` | O(n) | two comparisons |
| `.str.contains` | O(n x len) | vectorized regex |
| `drop_duplicates` | O(n) | hashing; keeps first/last/none |
| `.filter()` | O(columns) | metadata-level |

**At scale:** masks and query are single O(n) passes — fine to 10M rows. The
expensive parts are the copies they produce and regex on long strings; filter
on cheap columns first and drop unneeded columns before heavy regex.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| masks | confidence thresholds on model outputs |
| `.isin` | doc allow-lists for eval subsets |
| `.query` | readable experiment-filter DSL |
| `drop_duplicates(keep=False)` | cleaning scraped training data |
| regex filters | dropping PII or out-of-scope rows |
| governed subsets | reproducible evaluation sets |

**Scale note:** eval subsets are governance artifacts — they must be
deterministic and reviewable. Encoding them as named functions (not scattered
masks) means the same rows are used by every experiment and reviewer.

## Practice Exercises

### Exercise 1: Confidence Filter (Easy)
Given `df` with `score` and `split`, select rows with `score >= 0.8` on
`"test"` using a single compound mask.

### Exercise 2: Query DSL (Medium)
Rewrite the same filter with `.query()` and `@threshold`, then confirm both
produce identical frames (compare `equals()`).

### Exercise 3: Hygiene Pipeline (Hard)
Write `dedupe_scraped(df, key_col)` that removes rows whose key appears more
than once AND contains the substring `"spam"` in the text, returning a clean
frame with a report of how many rows were dropped.

## Summary

| Concept | Description |
|---------|-------------|
| compound masks | `&`/`\|`/`~` with parenthesized comparisons |
| `.query()` | SQL-like string conditions, `@var` for Python values |
| `.isin` / `.between` | set and range membership |
| `.str.contains` | vectorized regex/literal string filters |
| `.filter()` | selection BY NAME, not by value |
| `drop_duplicates` | keep first/last/none per key |
| governed subsets | filtering rules as named, reusable functions |

Filtering is the governance layer of data work. Get the grammar right once —
parentheses, element-wise operators, name-vs-value — and the pipeline
decisions become readable, reviewable, and reproducible.

## Quick Reference

| Task | Idiom |
|------|-------|
| AND mask | `df[(a) & (b)]` |
| OR mask | `df[(a) \| (b)]` |
| NOT mask | `df[~mask]` |
| SQL-like | `df.query("a > 1 and b in ['x','y']")` |
| Python var in query | `df.query("a > @threshold")` |
| In set | `df[df.c.isin(s)]` |
| Range | `df[df.c.between(lo, hi)]` |
| Literal substring | `df[df.c.str.contains("x", regex=False)]` |

## Next Steps

Next: **[04-missing-data](04-missing-data-lecture.md)** — the empty-value problem.
Continues in: **[07-machine-learning — 04 clean data](../../../../07-machine-learning/lectures/04-clean-data-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing
