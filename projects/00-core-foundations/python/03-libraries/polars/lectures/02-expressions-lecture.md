# 03-libraries/polars — 02: Expressions

## Topic Overview

The expression API is what makes Polars Polars. Almost everything you do
to a table — filtering, computing, aggregating, ranking, joining — is
expressed as an `Expr`: a small, composable recipe that describes a
column operation without touching any data. Expressions only run when a
*context* consumes them. There are four contexts in the core API:
`select` (project columns), `with_columns` (add or replace columns),
`filter` (keep rows), and `group_by().agg()` (aggregate per group).

Because expressions are plain objects, you can build them once and reuse
them, combine them with arithmetic, and — critically — let the query
optimizer see the whole pipeline before anything executes. This is the
single biggest mental shift from pandas: instead of "do this to the
frame", you write "here is the recipe for the column I want", and the
engine figures out the cheapest way to cook it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what an `Expr` is and why it holds no data
2. Distinguish the four contexts: `select`, `with_columns`, `filter`,
   `group_by().agg()`
3. Compose expressions with arithmetic, `.alias()`, and `pl.when/then/otherwise`
4. Combine predicates with `&`, `|`, `~` (and know why `and`/`or` fail)
5. Add multiple derived columns in a single `with_columns` call
6. Aggregate per group with `group_by().agg()` and named outputs
7. Use `.over()` for window-style computations inside `with_columns`
8. Debug the `.alias()` precedence trap

## Prerequisites

| Need | Where |
|------|-------|
| DataFrame construction, schema | `01-introduction-lecture.md` |
| Boolean logic in Python | `01-core-python/lectures/06-booleans-lecture.md` |
| pandas column operations (contrast) | `03-libraries/pandas/lectures/03-dataframes-lecture.md` |

## 1. What an Expr Is: A Recipe, Not a Value

`pl.col("score")` returns an `Expr`. It describes "the column named
score" — it does not fetch it. Arithmetic on expressions builds *new*
expressions; nothing evaluates until a context runs the whole tree.

```python
import polars as pl

expr = (pl.col("score") * 100).alias("score_pct")
print(type(expr).__name__)
print(expr.meta.output_name())
```

```text
Expr
score_pct
```

This has two consequences. First, expressions are reusable: the same
`expr` object can be used in a `select` here and a `with_columns` there.
Second, the optimizer can inspect and rewrite them — a `filter` on
`score > 0.5` is not a black box, it is a tree of known nodes that can be
pushed into a file scan.

## 2. Contexts: Where Expressions Run

An expression defines *what*; a context defines *where and how many rows*.
The same expression means different things in different contexts:

- `select(expr)` — output one column per expression, all rows
- `with_columns(expr)` — keep existing columns, add/replace these
- `filter(expr)` — keep rows where the boolean expression is True
- `group_by(k).agg(expr)` — one output row per group

```python
import polars as pl

df = pl.DataFrame({"user": ["a", "b"], "score": [0.9, 0.4]})

e = pl.col("score").mean()
print(df.select(e).rows())          # scalar aggregate, 1 row
print(df.group_by("user").agg(e).sort("user").rows())
```

```text
[(0.65,)]
[('a', 0.9), ('b', 0.4)]
```

Same expression, different shapes, depending on the context. This
uniformity is the design win: you learn one expression language, and the
context decides the semantics.

## 3. select: The Projection Context

`select()` returns a new frame with exactly the named columns, in the
order given. It may compute columns on the fly. Think of it as the
"columns out" declaration of a pipeline stage.

```python
import polars as pl

df = pl.DataFrame({"user": ["a", "b", "c"], "spend": [10, 20, 30],
                   "score": [0.9, 0.4, 0.7]})

out = df.select(
    pl.col("user"),
    (pl.col("spend") / pl.col("score")).alias("cost_per_point"),
)
print(out.rows())
```

```text
[('a', 11.11111111111111), ('b', 50.0), ('c', 42.857142857142854)]
```

Note the parentheses around the division: `.alias()` binds tighter than
`/`, so `pl.col("spend") / pl.col("score").alias("x")` would alias only
`score` and name the output column after `spend`. This precedence trap
is the most common beginner bug in the whole API.

## 4. with_columns: The Transform Context

`with_columns()` keeps every existing column and adds or overwrites the
named ones. This is feature engineering: one call, many derived columns,
all vectorized.

```python
import polars as pl

df = pl.DataFrame({"score": [0.9, 0.4, 0.7, 0.2], "spend": [10, 20, 30, 40]})

w = df.with_columns(
    (pl.col("spend") / 100).alias("spend_norm"),
    pl.col("score").rank(descending=True).alias("score_rank"),
    pl.when(pl.col("score") >= 0.5)
    .then(pl.lit("high"))
    .otherwise(pl.lit("low"))
    .alias("band"),
)
print(w.columns)
print(w["band"].to_list())
```

```text
['score', 'spend', 'spend_norm', 'score_rank', 'band']
['high', 'low', 'high', 'low']
```

Three features in one pass: normalization, ranking, and a binned label.
`pl.when(...).then(...).otherwise(...)` is the vectorized if/else — it
replaces both pandas `np.where` and any Python loop.

## 5. filter: The Row Context

`filter()` keeps rows where the predicate expression is True. Predicates
combine with `&` (and), `|` (or), and `~` (not) — and *must* be wrapped
in parentheses because expression operators bind differently than Python
boolean keywords.

```python
import polars as pl

df = pl.DataFrame({"user": ["a", "b", "c", "a"],
                   "score": [0.9, 0.4, 0.7, 0.2],
                   "spend": [10, 20, 30, 40]})

kept = df.filter((pl.col("score") >= 0.5) & (pl.col("spend") >= 15))
print(kept.rows())
```

```text
[('c', 0.7, 30)]
```

`and`/`or` fail with `ValueError` because Python evaluates them on the
truthiness of the `Expr` object, which is deliberately undefined. The
rule is mechanical: every comparison in parentheses, joined with `&`,
`|`, `~`.

## 6. group_by + agg: The Aggregation Context

`group_by("key")` splits the frame; `.agg(...)` applies one or more
reduction expressions per group; the result is one row per group. This
is split-apply-combine where "apply" is a vectorized expression, never a
Python function per group.

```python
import polars as pl

df = pl.DataFrame({"user": ["a", "b", "c", "a"],
                   "score": [0.9, 0.4, 0.7, 0.2],
                   "spend": [10, 20, 30, 40]})

g = df.group_by("user").agg(
    pl.col("score").mean().alias("avg_score"),
    pl.col("spend").sum().alias("total_spend"),
    pl.len().alias("n_events"),
).sort("user")
print(g.rows())
```

```text
[('a', 0.55, 50, 2), ('b', 0.4, 20, 1), ('c', 0.7, 30, 1)]
```

`pl.len()` counts rows per group — the polars equivalent of
`size()`. Multiple aggregates in one `.agg()` share a single group pass;
there is no reason to group twice.

## 7. Window Computations: .over() Inside with_columns

Sometimes you need an aggregate *aligned back to the rows* — "each row's
rank within its user", "each row's spend share of its user's total".
That is what `.over()` does: compute the aggregate per group, then map
the result back onto every row of the group.

```python
import polars as pl

df = pl.DataFrame({"user": ["a", "b", "c", "a"],
                   "score": [0.9, 0.4, 0.7, 0.2],
                   "spend": [10, 20, 30, 40]})

w = df.with_columns(
    pl.col("spend").rank().over("user").alias("spend_rank_in_user"),
    (pl.col("spend") / pl.col("spend").sum().over("user")).alias("spend_share"),
)
print(w.sort("user", "spend").rows())
```

```text
[('a', 0.9, 10, 1.0, 0.2), ('a', 0.2, 40, 2.0, 0.8),
 ('b', 0.4, 20, 1.0, 1.0), ('c', 0.7, 30, 1.0, 1.0)]
```

User "a" has two events: the first gets spend-rank 1 and a 0.2 share of
the user's total, the second rank 2 and 0.8. In pandas this needs
`groupby().transform()`; here it is one expression inside
`with_columns`, and it stays part of the optimizer-visible plan.

## 8. Reusing and Composing Expressions

Because expressions are objects, build a library of them: a module-level
`FEATURES` list that a pipeline selects every run. This is the feature
pipeline as configuration — the same expressions serve train and serve.

```python
import polars as pl

FEATURES = [
    pl.col("score").fill_null(0.0).alias("score_filled"),
    (pl.col("spend") / (pl.col("spend").sum().over("user") + 1.0)).alias("share"),
    pl.when(pl.col("score") >= 0.5).then(pl.lit(1)).otherwise(pl.lit(0)).alias("high"),
]

def build_features(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(FEATURES)

df = pl.DataFrame({"user": ["a", "a"], "score": [0.9, None], "spend": [10, 20]})
print(build_features(df).rows())
```

```text
[('a', 0.9, 0.3333333333333333, 1), ('a', None, 0.6666666666666666, 0)]
```

Note `fill_null(0.0)` kept the null in the source column — the *copy* in
`score_filled` is what got filled. Composition like this is how
production feature code stays readable: the recipe list is the spec.

## Common Mistakes to Avoid

### Mistake 1: .alias() on the Wrong Operand
```
# WRONG — alias binds to pl.col("score") because . binds tighter than /
pl.col("spend") / pl.col("score").alias("ratio")
# CORRECT — alias the whole expression
(pl.col("spend") / pl.col("score")).alias("ratio")
```

### Mistake 2: Python and/or on Expressions
```
# WRONG — ValueError: truth value of an Expr is ambiguous
df.filter(pl.col("a") > 1 and pl.col("b") < 2)
# CORRECT — parenthesized comparisons joined with & |
df.filter((pl.col("a") > 1) & (pl.col("b") < 2))
```

### Mistake 3: Forgetting select Drops Columns
```
# WRONG — surprising: the frame now has ONLY column a
result = df.select(pl.col("a"))
# CORRECT — use with_columns to keep the rest
result = df.with_columns(pl.col("a").alias("a_renamed"))
```

### Mistake 4: Python Functions Inside Expressions
```
# WRONG — per-element Python dispatch, slow and non-optimizable
df.select(pl.col("x").apply(my_py_fn))
# CORRECT — native expressions, or pl.map_batches for real batch functions
df.select((pl.col("x") * 2).alias("double"))
```

### Mistake 5: Expecting rank() to Default to Descending
```
# WRONG — rank() is ascending by default: smallest value -> rank 1
df.with_columns(pl.col("score").rank())
# CORRECT — say what you mean
df.with_columns(pl.col("score").rank(descending=True))
```

## Best Practices

1. Parenthesize every arithmetic expression before `.alias()`
2. Combine predicates with `&`/`|`/`~`, never `and`/`or`
3. Put multiple derived columns in one `with_columns` call — one pass
4. Name aggregates explicitly with `.alias()`; don't rely on defaults
5. Use `pl.when(...).then(...).otherwise(...)` instead of `np.where`
6. Prefer `.over()` for group-aligned features over join-then-merge
7. Build reusable expression lists for train/serve parity
8. Use `pl.len()` inside `.agg()` instead of counting a column
9. Test expression output with `.rows()`/`.to_list()` (ASCII-safe)
10. When a Python function is unavoidable, wrap it with `pl.map_batches`

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `select(expr)` | O(n) per expr | O(output cols) | select only needed columns |
| `with_columns(3 exprs)` | O(3n) one pass | O(n) extra | batch columns in one call |
| `filter(pred)` | O(n) | O(matched) | push predicate into scan |
| `group_by(k).agg(...)` | O(n log g) hash | O(g) | fewer aggregates per pass |
| `expr.over("k")` | O(n log g) | O(n) | — (window semantics needed) |

The optimizer combines expressions in a context into fewer kernel passes
when it can; your job is to give it whole pipelines, not fragments. A
`with_columns` with five expressions is one pass; five separate
`with_columns` calls may be five.

## AI Engineering Relevance

**Where this shows up:** feature stores and training pipelines. Every
derived feature — normalization, rank, binned label, share-of-group — is
an expression, and the same expressions must run identically at training
and at serving time.

| Concept here | Used for |
|--------------|----------|
| `with_columns` + `.alias()` | building the feature matrix from raw events |
| `pl.when/then/otherwise` | discretizing continuous scores into buckets |
| `rank().over()` | position-based features (e.g., "2nd query this session") |
| `group_by().agg()` | per-user or per-item aggregates for tabular models |
| reusable `FEATURES` list | train/serve parity, feature registry |

**Scale note:** at 100M rows the difference between an expression pipeline
and a loop-based pipeline is hours. Expressions also keep the plan small:
a feature list of 20 expressions compiles to a handful of kernels, which
is what lets streaming and lazy execution stay fast.

## Practice Exercises

### Exercise 1: Projection (Difficulty: Easy)
Write `select_demo(df)` returning only `user` and
`cost_per_point = spend / score` (aliased with correct parentheses).
Assert the output has exactly two columns.

### Exercise 2: Compound Filter (Difficulty: Easy)
Write `filter_demo(df)` keeping rows with `score >= 0.5` AND `spend >= 15`.
Assert the exact surviving rows.

### Exercise 3: Feature Batch (Difficulty: Medium)
In one `with_columns`, add `spend_norm`, `score_rank` (descending), and a
`band` column via `when/then/otherwise`. Assert all three columns exist
and their exact values.

### Exercise 4: Grouped Aggregates (Difficulty: Medium)
Write `groupby_demo(df)` computing per-user `avg_score`, `total_spend`,
and `n_events` (`pl.len()`). Assert the per-group values.

### Exercise 5: Window Features (Difficulty: Hard)
Add `spend_rank_in_user` via `rank().over("user")` and `spend_share` via
`spend / sum().over("user")`. Assert that for a user with two events the
shares sum to 1.0.

## Summary

| Concept | Description |
|---------|-------------|
| Expr | A lazy recipe for a column operation; holds no data |
| select | Projection context: output columns |
| with_columns | Transform context: add/replace columns |
| filter | Row context: keep rows matching a predicate |
| group_by().agg() | Aggregation context: one row per group |
| `.over()` | Window computation aligned back to rows |
| `pl.when/then/otherwise` | Vectorized if/else |
| `&` `|` `~` | Expression boolean combinators (not `and`/`or`) |

Expressions are the vocabulary of Polars. Every later topic — lazy
optimization, pandas migration, Parquet I/O, streaming — is built on
this one idea: describe the transformation, let the engine execute it.
The next topic shows what happens when the description covers a whole
pipeline: the optimizer gets to work.

## Quick Reference

| Task | Idiom |
|------|-------|
| Reference a column | `pl.col("score")` |
| New column | `with_columns((pl.col("a") * 2).alias("b"))` |
| Filter rows | `df.filter((pl.col("a") > 1) & (pl.col("b") == 2))` |
| If/else vectorized | `pl.when(c).then(v).otherwise(w)` |
| Per-group aggregate | `df.group_by("k").agg(pl.col("v").mean())` |
| Row count per group | `pl.len()` inside `.agg()` |
| Rank within group | `pl.col("v").rank().over("k")` |
| Share of group | `pl.col("v") / pl.col("v").sum().over("k")` |
| Null fill | `pl.col("v").fill_null(0.0)` |
| Output name | `expr.alias("name")` — parenthesize the whole expr |

## Next Steps

Next: **[03 Lazy Evaluation](03-lazy-evaluation-lecture.md)** — how the
optimizer exploits whole pipelines of expressions.
Continues in: **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**
Official docs: https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/
