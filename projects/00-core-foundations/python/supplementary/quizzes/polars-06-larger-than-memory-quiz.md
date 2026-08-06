# Polars 06 — Larger Than Memory Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** The streaming engine (`collect(engine="streaming")`):

- A) processes the query in chunks, bounding peak memory
- B) loads everything into RAM, then processes
- C) only works for CSV files
- D) runs the query on a remote cluster

**E2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [2, None, 1]})
print(df.sort("a")["a"].to_list())
```

- A) `[None, 1, 2]`
- B) `[1, 2, None]`
- C) `[2, None, 1]`
- D) `[None, 2, 1]`

**E3.** `sink_parquet(path, engine="streaming")`:

- A) writes the lazy result to parquet without holding it in memory
- B) collects to RAM and then writes
- C) only writes a schema
- D) requires a database connection

**E4.** Which call returns the number of rows of a lazy query without
materializing data columns?

- A) `lf.select(pl.len()).collect(engine="streaming")`
- B) `lf.collect()` then `len()`
- C) `lf.columns`
- D) `lf.explain()`

**E5 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [2, None, 1]})
print(df.select(pl.col("a").null_count()).item())
```

- A) `1`
- B) `2`
- C) `0`
- D) `None`

**E6.** A 2M-row dataset split into 4 parquet shards of 500k rows each
is best read with:

- A) `pl.scan_parquet("shards/")` — one scan of the directory
- B) four separate `read_parquet` calls merged by hand
- C) `pl.read_csv` on each shard
- D) pandas `concat` of the shards

---

## Medium

**M1 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [2, None, 1]})
print(df.sort("a", nulls_last=True)["a"].to_list())
```

- A) `[1, 2, None]`
- B) `[None, 1, 2]`
- C) `[2, 1, None]`
- D) `[None, 2, 1]`

**M2.** The default null placement in `sort()` is:

- A) nulls first
- B) nulls last
- C) nulls are dropped
- D) nulls raise an error

**M3.** Which piece of the pipeline actually keeps memory bounded?

- A) the streaming engine folding partial results chunk by chunk
- B) `collect()` with `engine="eager"`
- C) reading the CSV twice
- D) writing to a temp file first

**M4 (code-output).** What prints?
```python
import polars as pl
lf = pl.scan_csv("events.csv")   # 100k rows, columns id, metric
print(lf.select(pl.len()).collect(engine="streaming").item())
```

- A) `100000`
- B) `2`
- C) `100000.0`
- D) `2.0`

**M5 (code-output).** What prints?
```python
import os
import polars as pl
lf = pl.scan_parquet("left/")
rf = pl.scan_parquet("right/")
lf.join(rf, on="id").sink_parquet("joined.parquet", engine="streaming")
print(os.path.exists("joined.parquet"))
```

- A) `True`
- B) `False`
- C) `None`
- D) raises `InvalidOperationError`

**M6.** Which of these is TRUE about streaming aggregates?

- A) `len`, `sum`, `mean` over a scan stream correctly
- B) streaming cannot count rows
- C) streaming requires a sorted input
- D) streaming only works on a single column

**M7 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"tier": [None] * 3 + ["free", "pro"]})
print(df.group_by("tier").len().sort("tier").rows())
```

- A) `[(None, 3), ('free', 1), ('pro', 1)]`
- B) `[('free', 1), ('pro', 1), (None, 3)]`
- C) `[('free', 1), ('pro', 1)]`
- D) `[(None, 3), ('pro', 1), ('free', 1)]`

**M8.** `pl.scan_parquet("shards/")` on 4 shards streams the data:

- A) shard by shard, aggregating partials as it goes
- B) only after loading all shards into one frame
- C) into memory and then re-partitions
- D) alphabetically by filename only

**M9.** The purpose of `engine="streaming"` on `sink_parquet` is:

- A) to avoid collecting the whole result in RAM before writing
- B) to make the file smaller
- C) to sort the output
- D) it is the default for all writes

---

## Hard

**H1.** Why is `df.select(pl.len()).collect()` over a huge CSV
memory-cheap even without streaming?

- A) the optimizer can count rows with a single scan and no materialized
  data columns — but streaming still bounds it further
- B) `len` never touches the file
- C) CSV files store row counts in the header
- D) Polars caches the answer after the first read

**H2.** A 2M-row dataset processed eagerly needs ~2M×row_size RAM;
streaming needs approximately:

- A) a few chunks × chunk size (partial results only)
- B) the same as eager (streaming is only about I/O)
- C) zero memory — streaming touches the disk directly
- D) the size of one shard + the output (but only when sorted)

**H3 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"user_id": [0, 1, 2, 3], "tier": ["free", "pro", "pro", "free"]})
print(df.filter(pl.col("user_id") < 4).group_by("tier").len().sort("tier").rows())
```

- A) `[('free', 2), ('pro', 2)]`
- B) `[('free', 1), ('pro', 2), ('free', 1)]`
- C) `[(0, 1), (1, 1), (2, 1), (3, 1)]`
- D) `[('pro', 2), ('free', 2)]`

**H4.** Which describes the memory profile of
`lf.join(rf).sink_parquet(..., engine="streaming")`?

- A) join partials are produced chunk by chunk and written out —
  neither input nor output ever exists fully in RAM
- B) the join result is fully materialized, then streamed out
- C) inputs are streamed but the output is held in RAM
- D) streaming forces a hash join that needs the whole right side in
  RAM (correct for joins on non-unique keys)

**H5.** When would you *not* use streaming?

- A) tiny in-memory frames where eager is simpler and faster
- B) 10 GB parquet shards
- C) row counts over huge CSVs
- D) joins of sharded directories

---

## Answer Key

**E1 — A.** Streaming processes chunk by chunk; peak memory is bounded
by chunk size, not dataset size.
*Distractors:* B is eager; C is false; D is a cluster engine.

**E2 — A.** Polars `sort()` puts nulls **first** by default.
*Distractors:* B is `nulls_last=True`; C is the original order; D is
a partial sort.

**E3 — A.** Sink streams the result to disk — never materializes the
full output in RAM.
*Distractors:* B is the anti-pattern; C/D are false.

**E4 — A.** `select(pl.len())` touches only the row count; streaming
keeps it bounded.
*Distractors:* B materializes everything; C is metadata; D explains
without executing.

**E5 — A.** One null in the column → `null_count()` = 1.
*Distractors:* B counts non-nulls; C counts a full column; D is the
wrong type.

**E6 — A.** One `scan_parquet` of the directory handles all shards.
*Distractors:* B is manual; C is the wrong format; D re-imports
pandas.

**M1 — A.** `nulls_last=True` moves nulls to the end: [1, 2, None].
*Distractors:* B is the default; C/D are wrong orders.

**M2 — A.** Polars puts nulls first by default (verified:
`[None, 1, 2]`).
*Distractors:* B is the explicit option; C/D are false.

**M3 — A.** The streaming engine folds partial results chunk by
chunk — that is the mechanism.
*Distractors:* B is eager (no bound); C/D are workarounds, not
mechanisms.

**M4 — A.** The row count of the CSV is 100000; `.item()` extracts it.
*Distractors:* B is the column count; C/D are float coercions.

**M5 — A.** Lazy join + sink writes the output file — the canonical
larger-than-memory join pattern (verified).
*Distractors:* B is false (streaming joins work); C/D are false.

**M6 — A.** Aggregate expressions stream correctly over scans.
*Distractors:* B is false (len streams); C/D are false.

**M7 — A.** `group_by("tier").len()` counts nulls as their own group:
(None, 3), then free/pro sorted with nulls first.
*Distractors:* B/C drop or reorder the null group; D is the
nulls-last order.

**M8 — A.** Directory scans stream shard by shard, aggregating
partials.
*Distractors:* B/C are eager myths; D is about ordering, not
execution.

**M9 — A.** Streaming sink avoids materializing the result in RAM
before writing.
*Distractors:* B/C are false; D is false (sink needs the streaming
engine explicitly for this benefit).

**H1 — A.** `len` can be answered by a single counting scan with no
column materialization; streaming bounds it further for multi-step
plans.
*Distractors:* B is false; C is false; D is false.

**H2 — A.** Streaming holds a few chunks plus small partial
aggregates — bounded, not proportional to dataset size.
*Distractors:* B is false; C is false (memory is still used, just
bounded); D invents conditions.

**H3 — A.** Group by tier: free = users 0 and 3 → 2; pro = users 1
and 2 → 2; sorted: `[('free', 2), ('pro', 2)]`.
*Distractors:* B is an ungrouped row list; C groups by user_id; D is
the unsorted order.

**H4 — A.** Streaming join+sink produces and writes partials
incrementally — bounded memory end to end.
*Distractors:* B/C describe partial materialization; D is true for
some join algorithms (build-side buffering), but the streaming sink
still bounds the *output* — the pattern remains the right default.

**H5 — A.** For tiny frames, eager is simpler and often faster —
streaming adds no value below memory pressure.
*Distractors:* B/C/D are exactly where streaming shines.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 06](03-libraries/polars/lectures/06-larger-than-memory-lecture.md) ·
[Glossary 06](03-libraries/polars/lectures/06-larger-than-memory-glossary.md) ·
[Challenge 06](03-libraries/polars/challenges/06-larger-than-memory/README.md)
