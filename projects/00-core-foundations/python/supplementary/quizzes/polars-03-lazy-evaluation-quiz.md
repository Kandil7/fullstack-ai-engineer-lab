# Polars 03 — Lazy Evaluation Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** `pl.scan_csv("data.csv")` returns:

- A) a `LazyFrame` — nothing is read until `collect()`
- B) an eager `DataFrame`
- C) a `Series`
- D) the file contents as text

**E2.** Which call executes a lazy plan?

- A) `lf.collect()`
- B) `lf.lazy()`
- C) `lf.explain()`
- D) `lf.schema`

**E3 (code-output).** What prints?
```python
import polars as pl
lf = pl.DataFrame({"a": [1, 2, 3]}).lazy()
print(lf.select(pl.len()).collect().item())
```

- A) `3`
- B) `1`
- C) `3.0`
- D) `[3]`

**E4.** The `engine="streaming"` argument to `collect()`:

- A) processes data in chunks, bounding memory
- B) speeds up a single-column count by skipping data
- C) writes the result to a file
- D) switches to the pandas engine

**E5 (code-output).** What prints?
```python
import polars as pl
lf = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]}).lazy()
print(lf.columns)
print(lf.select(pl.col("a").sum()).collect().item())
```

- A) `['a', 'b']` `6`
- B) `['a', 'b']` `[6]`
- C) `[]` `6`
- D) `['a']` `6`

**E6.** `lf.explain(optimized=True)`:

- A) returns the (optimized) query plan as text without executing it
- B) executes the query and prints the result
- C) raises unless `collect()` was called first
- D) returns a PNG diagram

---

## Medium

**M1.** A pushed-down filter on a parquet scan appears in the optimized
plan as:

- A) `SELECTION` inside the scan node
- B) a separate `FILTER` node above the scan
- C) a `PROJECT` node
- D) nothing — filters are never visible in plans

**M2 (code-output).** What prints?
```python
import polars as pl
lf = pl.scan_csv("data.csv").filter(pl.col("split") == "valid")
plan = lf.explain(optimized=True)
print("SELECTION" in plan)
print("FILTER" in plan)
```
Assume the CSV scan supports predicate pushdown.

- A) `True` `False`
- B) `False` `True`
- C) `True` `True`
- D) `False` `False`

**M3.** Projection pushdown is visible in the optimized plan as:

- A) `PROJECT n/m COLUMNS` — only the needed columns are read
- B) `SELECTION` — rows are dropped at the scan
- C) `SINK` — the output is written to disk
- D) `AGGREGATE` — grouping happens in the scan

**M4.** Which is lazy end-to-end?

- A) `pl.scan_parquet(dir).filter(...).collect(engine="streaming")`
- B) `pl.read_parquet(dir).filter(...)`
- C) `pl.read_csv("f.csv").select(pl.len())`
- D) `pl.from_pandas(df).mean()`

**M5.** `lf.select(pl.col("a")).collect()` on a frame with columns
`a, b, c` reads:

- A) only column `a` (projection pushdown)
- B) all three columns, then drops `b` and `c`
- C) zero columns
- D) columns in alphabetical order

**M6 (code-output).** What prints?
```python
import polars as pl
lf = pl.DataFrame({"a": [1, 2, 3]}).lazy()
q = lf.filter(pl.col("a") > 1).select(pl.col("a").sum())
print(q.collect().item())
```

- A) `5`
- B) `6`
- C) `3`
- D) `2`

**M7 (code-output).** What prints?
```python
import os
import polars as pl
lf = pl.scan_csv("data.csv").select(pl.len())
lf.sink_parquet("count.parquet", engine="streaming")
print(os.path.exists("count.parquet"))
```

- A) `True`
- B) `False`
- C) `1`
- D) raises `FileNotFoundError`

**M8.** A `LazyFrame` is best described as:

- A) a query graph that defers execution until `collect()`
- B) a smaller, compressed DataFrame
- C) a DataFrame that pages data from disk on demand
- D) a pandas DataFrame with lazy imports

**M9 (code-output).** What prints?
```python
import polars as pl
lf = pl.scan_csv("data.csv")
plan = lf.explain(optimized=True)
print(type(plan).__name__)
```

- A) `str`
- B) `bytes`
- C) `LazyFrame`
- D) `NoneType`

---

## Hard

**H1.** Which statement about the `π` (unicode pi) in Polars plans is
correct?

- A) `explain()` output can contain Unicode glyphs like `π`, which
  crash `print` on a cp1252 Windows terminal — test with `in` checks
  on the plan string, print booleans
- B) plans are pure ASCII by design
- C) Unicode only appears in column names
- D) `explain()` is a no-op unless `collect()` fails

**H2.** A filter on a *DataFrame*-backed lazy query that cannot be
pushed appears in the optimized plan as:

- A) a `FILTER` node (no scan exists to absorb the predicate)
- B) a `SELECTION` inside a fake scan
- C) an `ERROR` node
- D) the filter is silently dropped

**H3.** Given
```python
lf = pl.scan_parquet("shards/")  # 4 parquet shards
```
`lf.collect(engine="streaming")`:

- A) streams shard by shard, keeping only partial results in memory
- B) loads all 4 shards fully, then processes
- C) fails — a directory scan cannot be streamed
- D) returns a single shard

**H4.** What is the practical contract of the lazy API for a
larger-than-memory pipeline?

- A) the engine can push filtering/projection into scans and stream
  the rest — peak memory is bounded by chunk size, not dataset size
- B) laziness only defers execution; memory use is identical to eager
- C) lazy queries are always faster, regardless of workload
- D) streaming requires rewriting the query in SQL

**H5 (code-output).** What prints?
```python
import polars as pl
lf = pl.DataFrame({"a": [1, 2, 3, 4]}).lazy()
filtered = lf.filter(pl.col("a") % 2 == 0)
plan = filtered.explain(optimized=True)
print("FILTER" in plan)
print(filtered.select(pl.len()).collect().item())
```

- A) `True` `2`
- B) `False` `2`
- C) `True` `4`
- D) `False` `4`

---

## Answer Key

**E1 — A.** `scan_*` functions return a `LazyFrame`; the actual file
I/O happens at `collect()`.
*Distractors:* B is `read_csv`/`read_parquet`; C is a single column;
D is text parsing, not a frame.

**E2 — A.** `collect()` executes the deferred plan and returns an
eager DataFrame.
*Distractors:* B creates laziness; C explains without running; D reads
the schema metadata.

**E3 — A.** `.lazy()` wraps the eager frame; `pl.len()` = 3 rows;
`.item()` extracts the scalar.
*Distractors:* B is the column count; C is the float coercion; D is
the frame cell without `.item()`.

**E4 — A.** The streaming engine processes chunks, keeping memory
bounded — the core larger-than-memory mechanism.
*Distractors:* B confuses it with predicate pushdown; C is
`sink_parquet`; D is false — both engines are native Polars.

**E5 — A.** `lf.columns` is metadata, available without execution:
`['a', 'b']`; the sum executes at collect: 6.
*Distractors:* B forgets `.item()`; C wrongly empties columns; D
drops `b`.

**E6 — A.** `explain` returns the plan as text — metadata only, no
data read.
*Distractors:* B is `collect`; C is false (explain works before
collect); D is false (text, not a diagram).

**M1 — A.** Pushed predicates show as `SELECTION` inside the scan —
the scan reads only matching rows.
*Distractors:* B is the non-pushable case; C is projection; D is
false — plans show optimizations.

**M2 — A.** For a CSV scan, the predicate becomes a `SELECTION` inside
the scan; there is no separate `FILTER` node.
*Distractors:* B/C invert the node types; D would mean no pushdown at
all.

**M3 — A.** `PROJECT n/m COLUMNS` in the plan proves only n of m
columns are read — projection pushdown.
*Distractors:* B is predicate pushdown; C is sinking; D is grouping.

**M4 — A.** scan → lazy ops → streaming collect is the full lazy
pipeline.
*Distractors:* B/C/D start with eager reads or end without lazy
execution.

**M5 — A.** The optimizer pushes the projection into the scan — only
`a` is read.
*Distractors:* B is the naive eager behavior; C/D are nonsense.

**M6 — A.** Filter keeps 2 and 3; sum = 5.
*Distractors:* B is the sum without filtering; C is the count; D is
the first kept value.

**M7 — A.** `sink_parquet` writes the lazy result to disk — the file
exists afterward. It is not an alias for collect-then-write; it is the
streaming write path.
*Distractors:* B is the anti-pattern; C/D are false.

**M8 — A.** A LazyFrame is a query graph; execution is deferred to
`collect()`.
*Distractors:* B/C are memory-layout myths; D is about imports, not
execution.

**M9 — A.** `explain()` returns a plain `str` — which is why `"SELECTION"
in plan` string checks work.
*Distractors:* B would need bytes; C is what you call explain on; D is
false.

**H1 — A.** Optimized plans can contain Unicode (e.g., `π` in
descriptions), which crashes `print` on cp1252; the lab pattern is
`"SELECTION" in plan` and printing booleans only.
*Distractors:* B is false (verified in the lab); C confuses data with
plan text; D is false.

**H2 — A.** Without a scan to absorb the predicate, the optimizer
emits a real `FILTER` node — the pushability determines the node type.
*Distractors:* B is scan-specific; C/D are false.

**H3 — A.** Directory scans stream shard by shard — the streaming
engine's whole point for larger-than-memory data.
*Distractors:* B is eager behavior; C is false (verified: shard dirs
stream fine); D is false.

**H4 — A.** Pushdowns + streaming bound peak memory by chunk size —
the practical contract of lazy evaluation.
*Distractors:* B is false (memory behavior differs); C is false
(lazy can be slower for tiny in-memory data); D is false.

**H5 — A.** On an in-memory DataFrame-backed lazy query, the filter
cannot push into a scan → a `FILTER` node exists; the filtered count
is 2 (rows 2 and 4).
*Distractors:* B inverts the node presence; C/D get the count wrong.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 03](03-libraries/polars/lectures/03-lazy-evaluation-lecture.md) ·
[Glossary 03](03-libraries/polars/lectures/03-lazy-evaluation-glossary.md) ·
[Challenge 03](03-libraries/polars/challenges/03-lazy-evaluation/README.md)
