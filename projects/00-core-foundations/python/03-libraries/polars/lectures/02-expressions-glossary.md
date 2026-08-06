# Expressions — Glossary 02

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| .agg() | Method | Applies reduction expressions per group in group_by |
| .alias() | Method | Names an expression's output column |
| & / | / ~ | Operator | Expression boolean combinators (and / or / not) |
| .filter() | Method | Row context: keeps rows where the predicate is True |
| group_by() | Method | Splits the frame by key values for aggregation |
| .over() | Method | Window computation: aggregate mapped back to rows |
| pl.col() | Function | References a column by name as an expression |
| pl.len() | Function | Row count expression, useful inside .agg() |
| pl.lit() | Function | Wraps a Python scalar as an expression |
| pl.map_batches | Function | Applies a Python function to whole batches |
| pl.when/then/otherwise | Function | Vectorized if/else expression builder |
| select | Context | Projection: output only the named expressions |
| .rank() | Method | Ordinal ranking of column values |
| Expr | Type | Lazy recipe for a column operation; holds no data |
| context | Concept | The place an expression runs (select, filter, ...) |
| predicate | Concept | Boolean expression selecting rows |
| window | Concept | Aggregate computed per group, aligned back to rows |
| with_columns | Context | Transform: keep all columns, add/replace named ones |
| fill_null | Method | Replaces null values with a given value |

## Detailed Definitions

### .agg()
**Definition**: The method that applies one or more reduction
expressions per group after `group_by`. Reductions collapse many rows to
one value (sum, mean, count, first).
**Example**:
```python
import polars as pl
df = pl.DataFrame({"k": ["a", "a", "b"], "v": [1, 2, 3]})
print(df.group_by("k").agg(pl.col("v").sum().alias("total")).sort("k").rows())
```
```text
[('a', 3), ('b', 3)]
```
**Complexity**: O(n log g) with a hash grouping.
**Related**: group_by(), pl.len()

### .alias()
**Definition**: Names the output column of an expression. Binds to the
immediate expression it is called on — parenthesize compound arithmetic
before aliasing.
**Example**:
```python
import polars as pl
e = (pl.col("a") * 2).alias("double")
print(e.meta.output_name())
```
```text
double
```
**Related**: Expr, select

### & | ~
**Definition**: The boolean combinators for predicates. `&` is and, `|`
is or, `~` is not. Python's `and`/`or` cannot be used on expressions.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3]})
print(df.filter((pl.col("a") > 1) & (pl.col("a") < 3)).rows())
```
```text
[(2,)]
```
**Related**: predicate, filter

### .filter()
**Definition**: The row context. Keeps rows where the predicate
expression evaluates True. Equivalent to pandas boolean masking.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3, 4]})
print(df.filter(pl.col("a") % 2 == 0).rows())
```
```text
[(2,), (4,)]
```
**Complexity**: O(n).
**Related**: predicate, select

### group_by()
**Definition**: Splits a frame by key column values; usually followed by
`.agg(...)` to compute per-group reductions. Polars' split-apply-combine
without apply().
**Related**: .agg(), .over()

### .over()
**Definition**: Window computation. Aggregates per group, then maps the
result back onto every row of the group — pandas `transform` equivalent.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"k": ["a", "a", "b"], "v": [10, 20, 30]})
out = df.with_columns((pl.col("v") / pl.col("v").sum().over("k")).alias("share"))
print(out.rows())
```
```text
[('a', 10, 0.3333333333333333), ('a', 20, 0.6666666666666666), ('b', 30, 1.0)]
```
**Complexity**: O(n log g).
**Related**: group_by(), with_columns

### pl.col()
**Definition**: References a column by name, producing an expression.
The standard way to write expressions instead of using strings.
**Example**:
```python
import polars as pl
e = pl.col("score") > 0.5
print(type(e).__name__)
```
```text
Expr
```
**Related**: Expr, pl.lit()

### pl.len()
**Definition**: Counts rows in the current context — per group inside
`.agg()`, or total rows in `select()`.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"k": ["a", "a", "b"]})
print(df.group_by("k").agg(pl.len()).sort("k").rows())
```
```text
[('a', 2), ('b', 1)]
```
**Related**: .agg(), group_by()

### pl.lit()
**Definition**: Wraps a Python scalar into an expression, for constants
inside when/then or arithmetic.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2]})
print(df.with_columns(pl.lit("fixed").alias("tag")).rows())
```
```text
[(1, 'fixed'), (2, 'fixed')]
```
**Related**: pl.col(), pl.when/then/otherwise

### pl.map_batches
**Definition**: Applies a Python function to whole batches of a column,
preserving vectorization at the boundary. The escape hatch when a
function cannot be expressed natively.
**Related**: Expr, pl.when/then/otherwise

### pl.when/then/otherwise
**Definition**: The vectorized if/else. `pl.when(pred).then(a).otherwise(b)`
evaluates the predicate elementwise and picks per row.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"score": [0.9, 0.4, 0.7]})
band = df.with_columns(
    pl.when(pl.col("score") >= 0.5).then(pl.lit("high")).otherwise(pl.lit("low")).alias("band")
)
print(band["band"].to_list())
```
```text
['high', 'low', 'high']
```
**Related**: pl.lit(), predicate

### select
**Definition**: Projection context. Returns a frame with exactly the
named expressions, in order — computed or existing columns.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2], "b": [10, 20]})
print(df.select((pl.col("b") / pl.col("a")).alias("ratio")).rows())
```
```text
[(10.0,), (10.0,)]
```
**Related**: with_columns, Expr

### .rank()
**Definition**: Ordinal ranking of values, ascending by default
(smallest value -> rank 1). Pass `descending=True` for the reverse.
**Example**:
```python
import polars as pl
s = pl.Series("v", [0.9, 0.4, 0.7])
print(s.rank().to_list())
```
```text
[3.0, 1.0, 2.0]
```
**Related**: .over(), Expr

### Expr
**Definition**: A lazy, composable recipe for a column operation. Holds
no data; evaluates only inside a context.
**Related**: pl.col(), context

### context
**Definition**: The place an expression runs and the shape its result
takes: select (projection), with_columns (transform), filter (rows),
group_by.agg (per group).
**Related**: select, filter, group_by()

### predicate
**Definition**: A boolean expression over a row used by `filter` to
decide row survival.
**Related**: filter, & | ~

### window
**Definition**: An aggregate computed per group and aligned back to the
original rows via `.over()`, enabling per-row features that depend on
group context.
**Related**: .over(), group_by()

### with_columns
**Definition**: Transform context. Keeps every existing column and adds
or overwrites the named expressions — the workhorse of feature
engineering.
**Related**: select, .alias()

### fill_null
**Definition**: Replaces null values in a column with a given scalar or
strategy expression.
**Example**:
```python
import polars as pl
s = pl.Series("x", [1.0, None, 3.0])
print(s.fill_null(0.0).to_list())
```
```text
[1.0, 0.0, 3.0]
```
**Related**: Expr, with_columns

## Key Concepts Summary

### Expression Nature
- An Expr is a recipe, not a value; it holds no data
- Arithmetic and methods compose expressions into trees
- The optimizer can inspect and rewrite expression trees

### The Four Contexts
- select: choose and compute output columns
- with_columns: keep all columns, add/replace some
- filter: keep rows matching a predicate
- group_by().agg(): one output row per group

### Combinators and Traps
- Predicates join with & | ~ and full parentheses
- .alias() binds tightly — parenthesize compound expressions
- rank() defaults to ascending; say descending=True when needed

## Practice Terms

Match each term to its definition (answers at the bottom).

1. pl.when/then/otherwise — ___
2. .over() — ___
3. select — ___
4. pl.len() — ___
5. predicate — ___

A. Window aggregate mapped back to each row of its group
B. Row-count expression, used inside .agg()
C. Vectorized if/else expression builder
D. Boolean expression deciding which rows survive a filter
E. Projection context returning only the named columns

**Answers:** 1-C, 2-A, 3-E, 4-B, 5-D
