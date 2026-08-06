# Lazy Evaluation — Glossary 03

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| collect() | Method | Executes a lazy plan, returning a DataFrame |
| collect_schema() | Method | Output schema of a plan without executing it |
| engine="streaming" | Option | Executes a plan in bounded-memory batches |
| explain() | Method | Renders the plan as text for inspection |
| FILTER node | Plan | A predicate applied after the scan (not pushed) |
| LazyFrame | Type | A query plan; data only after collect() |
| partition pruning | Concept | Skipping whole files via partition column filters |
| predicate pushdown | Concept | Moving a filter into the file scan |
| PROJECT n/m COLUMNS | Plan | Scan reads n of m columns (projection trim) |
| projection pushdown | Concept | Dropping unread columns from the scan |
| read_csv() | Function | Eager CSV reader; loads everything now |
| row-group statistics | Concept | Parquet min/max metadata enabling row-group skipping |
| scan_csv() | Function | Lazy CSV opener: schema + estimate, no data |
| scan_parquet() | Function | Lazy parquet opener; directory scans all shards |
| SELECTION | Plan | Plan line proving a predicate was pushed to the scan |
| sink_parquet() | Method | Writes a lazy plan's output directly to disk |
| optimized plan | Concept | The rewritten plan the engine will actually run |

## Detailed Definitions

### collect()
**Definition**: The LazyFrame method that executes the optimized plan
and returns an eager DataFrame. The boundary where bytes actually move.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"a": [1, 2, 3]}).filter(pl.col("a") > 1)
print(lf.collect().rows())
```
```text
[(2,), (3,)]
```
**Related**: LazyFrame, explain()

### collect_schema()
**Definition**: Resolves the output schema of a lazy plan without
executing it — a cheap compile check for pipelines.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"a": [1], "b": ["x"]}).select("a")
print(lf.collect_schema().names())
```
```text
['a']
```
**Related**: LazyFrame, explain()

### engine="streaming"
**Definition**: The collect option that executes the plan in
bounded-memory batches instead of materializing intermediates.
**Related**: collect(), sink_parquet()

### explain()
**Definition**: Renders the plan (logical or optimized) as text. Read
bottom-up: scan at the bottom, final projection at the top.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"a": [1, 2]}).filter(pl.col("a") > 1)
print("FILTER" in lf.explain(optimized=True))
```
```text
True
```
**Related**: optimized plan, collect()

### FILTER node
**Definition**: A plan node applying a predicate after the scan —
present when the filter could not be pushed into the source. Seeing one
above a scan is a hint the predicate depends on computed columns.
**Related**: SELECTION, predicate pushdown

### LazyFrame
**Definition**: A query plan built by scan_* or .lazy(): file
references plus pending transformations. Executes at collect() or a sink.
**Example**:
```python
import polars as pl
lf = pl.scan_csv("data.csv")
print(type(lf).__name__)
```
```text
LazyFrame
```
**Related**: collect(), scan_csv()

### partition pruning
**Definition**: Skipping entire files because a filter targets the
partition column (e.g., `label=neg/` files when filtering `label ==
"neg"`).
**Related**: predicate pushdown, row-group statistics

### predicate pushdown
**Definition**: The optimizer moving WHERE conditions into the scan, so
rows are filtered at read time. Visible as `SELECTION` in the plan.
**Related**: SELECTION, filter

### PROJECT n/m COLUMNS
**Definition**: A plan line stating the scan reads n of m columns — the
proof of projection pushdown.
**Related**: projection pushdown, explain()

### projection pushdown
**Definition**: Dropping columns from the scan because nothing
downstream uses them. For Parquet, whole column chunks are skipped.
**Related**: PROJECT n/m COLUMNS, explain()

### read_csv()
**Definition**: The eager CSV reader: loads the entire file into a
DataFrame immediately. The counterpart of scan_csv().
**Related**: scan_csv(), LazyFrame

### row-group statistics
**Definition**: Per-chunk min/max metadata stored in Parquet, used to
skip row groups that cannot match a pushed predicate.
**Related**: predicate pushdown, partition pruning

### scan_csv()
**Definition**: Opens a CSV as a LazyFrame: reads the header and row
estimate, holds the file path, reads no data until collect().
**Related**: read_csv(), LazyFrame

### scan_parquet()
**Definition**: Lazy parquet reader. Accepts a single file or a
directory (all shards as one logical table). Rejects directories mixing
file extensions.
**Related**: LazyFrame, partition pruning

### SELECTION
**Definition**: The plan line inside a scan block showing the pushed
predicate, e.g. `SELECTION: col("split") == "valid"`.
**Related**: predicate pushdown, explain()

### sink_parquet()
**Definition**: A LazyFrame method writing the plan's output directly to
disk, batch by batch — no intermediate DataFrame in RAM.
**Example**:
```python
import polars as pl
from pathlib import Path
import tempfile

out = Path(tempfile.mkdtemp()) / "r.parquet"
pl.LazyFrame({"a": [1, 2]}).sink_parquet(out)
print(out.exists())
```
```text
True
```
**Related**: engine="streaming", collect()

### optimized plan
**Definition**: The plan after the optimizer's rewrites — pushdowns
applied, columns trimmed, joins reordered. What `explain(optimized=True)`
shows and what actually executes.
**Related**: explain(), predicate pushdown

## Key Concepts Summary

### The Plan Lifecycle
- scan_* opens metadata only; LazyFrame holds the plan
- Every transform appends a node; nothing runs
- collect() executes the optimized plan once

### What the Optimizer Does
- Predicate pushdown: filters into the scan (SELECTION)
- Projection pushdown: only needed columns read (PROJECT n/m)
- Partition pruning: whole files skipped via partition filters

### Reading a Plan
- Read bottom-up: scan first, final projection last
- SELECTION at the scan means the filter was pushed
- A FILTER node above the scan means it was not

## Practice Terms

Match each term to its definition (answers at the bottom).

1. scan_csv() — ___
2. SELECTION — ___
3. PROJECT 2/3 COLUMNS — ___
4. collect_schema() — ___
5. engine="streaming" — ___

A. Plan line proving a predicate was pushed into the scan
B. Plan line proving only 2 of 3 columns are read
C. Metadata-first lazy opener; no data until collect()
D. Schema of a plan's output without executing it
E. Bounded-memory execution of a plan

**Answers:** 1-C, 2-A, 3-B, 4-D, 5-E
