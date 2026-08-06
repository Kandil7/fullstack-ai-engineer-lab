# 03-libraries/polars — 03: Lazy Evaluation

## Topic Overview

Lazy evaluation is Polars's answer to a hard production question: how do
you run analytics on data that does not fit in memory, without hand-tuning
every pipeline? The answer is a two-phase design. First you *describe* the
work: `scan_csv`/`scan_parquet` open files without reading them, and every
transform — filter, select, join, aggregate — is appended to a `LazyFrame`,
which is just a query plan. Then, when you call `.collect()`, an optimizer
rewrites that plan: it pushes predicates into file scans, drops columns
that nothing downstream needs, and reorders joins before heavy
computations. Only then does execution begin.

The result is that the *same code* you write for a 100KB CSV runs
unchanged on a 50GB Parquet corpus — the file formats change, the data
scale changes, the plan optimizer adapts. This lecture makes the plan
visible: you will read `explain()` output, detect pushdowns, and learn
to debug performance problems at the plan level instead of the CPU level.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the difference between `read_*` (eager) and `scan_*` (lazy)
2. Build a multi-step lazy pipeline and execute it once with `.collect()`
3. Read an optimized query plan and identify FILTER/SELECT/SELECTION nodes
4. Detect predicate pushdown in `explain()` output
5. Detect projection pushdown and compute how many columns a scan reads
6. Use `collect_schema()` to inspect a plan's output without running it
7. Scan a directory of parquet shards as one logical table
8. Explain why lazy pipelines are also faster on in-memory data

## Prerequisites

| Need | Where |
|------|-------|
| Expr and contexts | `02-expressions-lecture.md` |
| DataFrame vs LazyFrame | `01-introduction-lecture.md` |
| Parquet basics | `05-pyarrow-parquet-lecture.md` (parallel topic) |

## 1. scan_* vs read_*: Metadata First

`pl.read_csv(path)` loads the whole file into a DataFrame immediately.
`pl.scan_csv(path)` opens the file, reads its header and row estimate,
and returns a `LazyFrame` — a plan that holds the file path and pending
operations, not the data.

```python
import polars as pl

lf = pl.scan_csv("events.csv")
print(type(lf).__name__)                 # LazyFrame - no data yet
print(lf.collect_schema().names())       # schema from the header only
print(lf.collect().height)               # NOW the file is read
```

```text
LazyFrame
['user', 'split', 'score']
2000
```

The schema and row count are metadata; `collect()` is the boundary where
bytes actually move. For a 50GB corpus, everything before `collect()` is
effectively free.

## 2. Building a Plan: Every Call Appends

Every method on a LazyFrame — `.filter`, `.select`, `.with_columns`,
`.group_by`, `.join` — appends a node to the plan. None of them run
anything. This is why you can assemble an entire ETL as one expression:

```python
import polars as pl

lf = (
    pl.scan_parquet("corpus/")
    .filter(pl.col("split") == "valid")
    .group_by("prompt_type")
    .agg(pl.col("token_count").mean())
    .sort("prompt_type")
)
result = lf.collect()   # one execution pass over the whole plan
print(result.height)
```

```text
3
```

Note that this is the same expression language as eager mode — only the
*execution* differs. The plan is a tree of nodes, and the optimizer's job
is to rewrite that tree before execution.

## 3. explain(): Reading the Optimized Plan

`LazyFrame.explain(optimized=True)` renders the plan the optimizer will
actually run. It is text, so teaching files never print it raw (its
Unicode symbols break cp1252 consoles) — they inspect it with string
checks and print booleans.

```python
import polars as pl

lf = pl.scan_csv("events.csv").filter(pl.col("split") == "valid")
plan = lf.explain(optimized=True)
print("SELECTION" in plan)   # filter pushed into the scan?
print("SELECT" in plan)      # projection node present?
```

```text
True
True
```

The optimized plan for a CSV scan with a filter looks like this
(abbreviated):

```text
SELECT [col("split")]
  simple ...
    Csv SCAN [...]
    PROJECT 2/3 COLUMNS
    SELECTION: col("split") == "valid"
```

Read it bottom-up: the CSV scan happens, the projection trims columns,
the selection filters rows *during* the scan — and only the surviving
rows ever reach the `SELECT` node. A `FILTER` node appears only when a
predicate *cannot* be pushed down (for example, filters on computed
columns that don't exist at scan time).

## 4. Predicate Pushdown: Filtering at the Source

Predicate pushdown moves `WHERE` conditions as close to the data as
possible. For CSV it becomes a read-time row filter. For Parquet it is
far more powerful: Parquet stores per-row-group statistics, so a pushed
`label == "neg"` can skip whole row groups — sometimes without reading
any data column at all.

```python
import polars as pl

lf = pl.scan_parquet("part/").filter(pl.col("label") == "neg")
plan = lf.explain(optimized=True)
print("SELECTION" in plan)
```

```text
True
```

The plan line `SELECTION: col("label") == "neg"` inside the scan block is
the proof. When you see a `FILTER` node *above* the scan instead, ask why
the predicate wasn't pushed — usually the predicate depends on a column
computed after the scan (a `with_columns` step), which makes the plan
honest about the extra work.

## 5. Projection Pushdown: Reading Only What You Need

Projection pushdown drops columns that nothing downstream uses. The plan
line `PROJECT 2/3 COLUMNS` says the scan reads 2 of 3 columns; the third
never leaves disk. For Parquet, whole column chunks are skipped.

```python
import polars as pl

lf = pl.scan_parquet("part/").select("score")
plan = lf.explain(optimized=True)
for line in plan.splitlines():
    if "PROJECT" in line and "COLUMNS" in line:
        print(line.strip())
```

```text
PROJECT 1/3 COLUMNS
```

The payoff compounds: with predicate *and* projection pushdown, a query
that logically touches 50GB can physically read a few hundred MB — the
rows that match, and only the columns the report needs. This is the
whole argument for columnar formats.

## 6. collect(): The Execution Boundary

`.collect()` runs the optimized plan and returns a plain DataFrame.
Everything before it is free; everything after it is materialized. The
eager/lazy boundary is where memory is spent, so it is also where you
decide:

- `.collect()` — materialize into RAM (fine when output is small)
- `.collect(engine="streaming")` — execute in bounded-memory batches
- `.sink_parquet(path)` — write the plan's output straight to disk

```python
import polars as pl

lf = pl.scan_csv("events.csv").filter(pl.col("split") == "valid")
small = lf.collect()                       # small output: fine
print(small.height)
```

```text
500
```

The rule: never collect a plan whose *output* is huge unless you need the
whole frame in RAM. The optimizer already minimized what the scan reads;
the collect decides what the result holds.

## 7. collect_schema(): The Plan's Output Contract

`collect_schema()` resolves the output schema of a lazy plan without
executing it. It is the cheapest possible way to check that a pipeline
produces the columns you expect — a poor-man's compile check that runs
even before touching file data.

```python
import polars as pl

lf = pl.scan_csv("events.csv").select(
    (pl.col("score") * 100).alias("score_pct"),
    pl.col("split"),
)
print(lf.collect_schema().names())
print(lf.collect_schema()["score_pct"])
```

```text
['score_pct', 'split']
Float64
```

Type errors surface here instead of mid-run: if a pipeline concatenates
an Int64 and a String, `collect_schema()` raises before any file is read.
CI should run `collect_schema()` on every critical pipeline.

## 8. Scanning a Directory: The Corpus Pattern

`pl.scan_parquet(dir)` reads every parquet file in a directory as one
logical table — the layout real corpora use, with one shard per file and
optional hive-style `key=value/` subdirectories. A filter on a partition
column prunes entire files.

```python
import polars as pl

corpus = pl.scan_parquet("corpus/")              # all shards
print(corpus.select(pl.len()).collect(engine="streaming")[0, 0])

chat = corpus.filter(pl.col("prompt_type") == "chat")
print(chat.collect_schema().names())             # never reads full data
```

```text
2000000
['user', 'token_count', 'prompt_type']
```

One caveat: a directory scan refuses mixed extensions. A directory
containing `events.csv` and `events.parquet` raises
`InvalidOperationError`; keep parquet shards in their own directory or
use an explicit glob.

## Common Mistakes to Avoid

### Mistake 1: Collecting Before Filtering
```
# WRONG — the whole corpus lands in RAM, then you filter
big = pl.scan_parquet("corpus/").collect()
small = big.filter(pl.col("split") == "valid")
# CORRECT — filter stays in the plan and is pushed into the scan
small = pl.scan_parquet("corpus/").filter(pl.col("split") == "valid").collect()
```

### Mistake 2: Indexing a LazyFrame Like a DataFrame
```
# WRONG — LazyFrames are not subscriptable
pl.scan_csv(p)["score"]
# CORRECT — select on the plan, or collect first
pl.scan_csv(p).select("score").collect()
```

### Mistake 3: Scanning a Mixed-Extension Directory
```
# WRONG — InvalidOperationError: paths with different file extensions
pl.scan_parquet("data_dir/")    # data_dir contains a .csv too
# CORRECT — parquet-only directory, or a glob
pl.scan_parquet("data_dir/*.parquet")
```

### Mistake 4: Trusting explain() Output You Never Read
```
# WRONG — "it's slow" with no plan inspection; FILTER above the scan
# CORRECT — read the plan bottom-up; hunt for SELECTION/PROJECT at the scan
plan = lf.explain(optimized=True)
```

### Mistake 5: Treating Lazy as a Performance Guarantee
```
# WRONG — lazy plans can still be bad (e.g., filter after a cross join)
# CORRECT — lazy gives the optimizer a chance; verify with explain()
```

## Best Practices

1. Scan everything that might exceed RAM; read only scratch files
2. Write filters and selects BEFORE collects so pushdown can act
3. Read `explain(optimized=True)` bottom-up when debugging slowness
4. Run `collect_schema()` in CI as a compile check on pipelines
5. Keep parquet shards in their own directory for directory scans
6. Prefer `.collect(engine="streaming")` for large outputs
7. Use `.sink_parquet()` for large transformed outputs
8. Print booleans about the plan, never the raw plan, on Windows
9. Verify determinism: the same plan must give the same result twice
10. Profile the plan before the CPU — pushdown gaps are the usual cause

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `scan_csv` / `scan_parquet` | O(metadata) | O(1) | — (read_* loads everything) |
| `explain(optimized=True)` | O(plan size) | O(plan size) | — |
| `collect_schema()` | O(plan size) | O(1) | — (no data read) |
| predicate pushdown | O(n_skipped) | O(1) | filters on partition columns (skip files) |
| projection pushdown | O(columns read) | O(columns read) | select fewer columns |
| `collect()` | O(plan) | O(output) | stream or sink large outputs |

The dominant cost is I/O, and the optimizer's currency is bytes avoided:
a pushed predicate can skip whole row groups; a trimmed projection can
skip whole columns. Both are visible in the plan before a single byte is
read.

## AI Engineering Relevance

**Where this shows up:** dataset ETL and evaluation pipelines. Training
corpora live in partitioned parquet; every epoch's data-loading job is a
lazy plan that must touch only the rows and columns the model needs.

| Concept here | Used for |
|--------------|----------|
| `scan_parquet(dir)` | loading a sharded training corpus |
| predicate pushdown | reading only the split/class you train on |
| projection pushdown | loading only feature columns, never labels' raw text |
| `collect_schema()` | CI gate: feature schema must not drift |
| streaming collect | computing corpus statistics on 50GB without OOM |

**Scale note:** at 10GB the pushdown savings are "nice"; at 1TB they are
the difference between a 2-hour job and a 2-minute job. Partition your
corpus by the columns you filter on, and the optimizer does the rest.

## Practice Exercises

### Exercise 1: Scan vs Read (Difficulty: Easy)
Write `scan_metadata(path)` returning `(columns, row_count)` using only a
scan (no `read_csv`). Assert the column names match the CSV header.

### Exercise 2: Plan Inspection (Difficulty: Easy)
For `lf = scan_csv(p).filter(...).select(...)`, write a function returning
`True` iff the optimized plan contains a SELECT node and a SELECTION line.

### Exercise 3: Pushdown Detection (Difficulty: Medium)
Write `has_predicate_pushdown(lf)` returning `"SELECTION" in explain()`.
Assert True for a parquet filter on a plain column.

### Exercise 4: Projection Counting (Difficulty: Medium)
Write `projected_columns(lf)` parsing `PROJECT n/m COLUMNS`. Assert that
selecting one column from a three-column table reads exactly 1 of 3.

### Exercise 5: Directory Corpus (Difficulty: Hard)
Write `scan_corpus(dir)` over 3 shards and assert the lazy count equals
the sum of per-shard heights without ever calling `read_parquet`.

## Summary

| Concept | Description |
|---------|-------------|
| LazyFrame | A query plan; appends transforms, executes at collect |
| scan_* | Open metadata only; the default for big files |
| explain() | The optimized plan as text — read it bottom-up |
| SELECTION | Plan line proving a predicate was pushed into the scan |
| PROJECT n/m COLUMNS | Plan line proving column trimming at the scan |
| collect_schema() | Output schema without executing |
| collect(engine="streaming") | Bounded-memory execution |

Lazy evaluation converts "write code that happens to work" into "describe
a pipeline and let an optimizer minimize the bytes it touches". The plan
is inspectable, the pushdowns are provable, and the same expressions work
at every scale. Next we translate everything so far into a pandas
engineer's vocabulary.

## Quick Reference

| Task | Idiom |
|------|-------|
| Lazy read CSV | `pl.scan_csv(path)` |
| Lazy read Parquet | `pl.scan_parquet(path)` |
| Execute plan | `lf.collect()` |
| Stream execution | `lf.collect(engine="streaming")` |
| Schema without data | `lf.collect_schema()` |
| Optimized plan text | `lf.explain(optimized=True)` |
| Scan a shard dir | `pl.scan_parquet("corpus/")` |
| Write plan to disk | `lf.sink_parquet(path)` |
| Convert eager | `df.lazy()` |

## Next Steps

Next: **[04 pandas Comparison](04-pandas-comparison-lecture.md)** — the
migration table: same idioms, side by side, with measurements.
Continues in: **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**
Official docs: https://docs.pola.rs/user-guide/lazy/using/
