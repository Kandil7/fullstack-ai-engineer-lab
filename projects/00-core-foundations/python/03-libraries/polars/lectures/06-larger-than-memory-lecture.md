# 03-libraries/polars — 06: Larger Than Memory

## Topic Overview

A 50GB training corpus does not fit in RAM. Yet it must be aggregated,
joined, filtered, and converted to model input — every day, on a normal
server. Polars's answer has three parts, and this lecture covers all
three. First, the **streaming engine**: `collect(engine="streaming")`
executes a lazy plan in bounded-memory batches instead of materializing
the whole frame. Second, **sinks**: `sink_parquet()` writes a plan's
output straight to disk — the "ETL result" never exists in RAM at all.
Third, **shard-at-a-time processing**: the oldest and most robust
pattern, where you loop over files, reduce each to a tiny aggregate, and
merge — peak memory is one shard plus one summary row.

The same code that streams here runs unchanged on a 500GB corpus. What
changes is your understanding of where the bytes go: the plan decides
how much memory the query needs, and you decide whether the output
materializes in RAM or streams to disk.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Execute a lazy plan with the streaming engine and verify it matches eager results
2. Write a plan's output to disk with `sink_parquet` without materializing
3. Build a shard-at-a-time batch loop with bounded memory
4. Join a large lazy frame with a small in-memory table in streaming mode
5. Count corpus rows using metadata instead of loading data
6. Explain when streaming helps and when it does not
7. Choose between collect, streaming collect, and sink for a given output

## Prerequisites

| Need | Where |
|------|-------|
| LazyFrame and plans | `03-lazy-evaluation-lecture.md` |
| Parquet shards and partitioning | `05-pyarrow-parquet-lecture.md` |
| group_by/agg expressions | `02-expressions-lecture.md` |

## 1. The Memory Problem in One Number

A 2M-row frame with three columns is about 60MB — fine for a laptop. The
same shape at 1B rows is 30GB — dead on a 16GB server. The problem is
not the CPU; it is the intermediate frames: filter produces a frame,
group_by produces a frame, join produces a frame. Eager mode keeps them
all alive.

```python
import polars as pl

big = pl.DataFrame({"x": range(2_000_000), "k": [i % 10 for i in range(2_000_000)]})
eager_mem = big.filter(pl.col("k") == 3).select(pl.col("x")).estimated_size()
print(f"{eager_mem / 1e6:.1f} MB materialized")
```

```text
16.0 MB materialized
```

`estimated_size()` measures a frame's in-memory footprint. For a real
corpus the intermediates are gigabytes. The streaming engine exists so
those intermediates never exist.

## 2. The Streaming Engine: collect(engine="streaming")

The streaming engine executes the plan in batches: read a batch of rows,
apply the operators, accumulate the aggregate, free the batch, read the
next. The result is identical to a normal collect — only the peak memory
differs.

```python
import polars as pl

lf = pl.LazyFrame({"k": [i % 10 for i in range(2_000_000)],
                   "v": [float(i) for i in range(2_000_000)]})

streamed = (lf.group_by("k")
              .agg(pl.col("v").sum())
              .collect(engine="streaming"))
eager = (lf.group_by("k")
           .agg(pl.col("v").sum())
           .collect())
print(streamed.equals(eager))
```

```text
True
```

The contract: streaming and eager produce the same numbers; streaming
does it with bounded memory. Use streaming whenever the input or output
might not fit — the code is identical except for the `engine=` argument.

## 3. Sinks: Writing Plans Straight to Disk

`sink_parquet()` consumes a LazyFrame and writes the result to disk
directly. The intermediate DataFrame that `collect()` + `write_parquet()`
would build never exists. This is the write path for "transform 50GB
into 5GB of prepared features".

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
lf = pl.LazyFrame({"k": [i % 4 for i in range(1_000_000)],
                   "v": [float(i) for i in range(1_000_000)]})

out = tmp / "reduced.parquet"
(lf.filter(pl.col("k") == 0)
   .select("v")
   .sink_parquet(out))
print(out.exists(), pl.scan_parquet(out).collect().height)
```

```text
True 250000
```

Filter, project, and write — one pass, no 250k-row frame ever held in
Python memory. Sinks are the streaming engine's sibling: same batching
philosophy, different destination (disk instead of a returned frame).

## 4. Shard-at-a-Time: The Manual Stream

The most portable out-of-core pattern predates Polars: process one file
at a time, reduce each to a tiny summary, merge the summaries. Peak
memory is one shard plus one aggregate row, no matter the corpus size.

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
for shard in range(3):
    pl.DataFrame({"k": [shard % 2] * 100_000,
                  "v": [1.0] * 100_000}).write_parquet(tmp / f"s{shard}.parquet")

totals = {}
for p in sorted(tmp.glob("*.parquet")):
    partial = dict(
        pl.scan_parquet(p).group_by("k").agg(pl.col("v").sum()).collect().rows()
    )
    for key, value in partial.items():
        totals[key] = totals.get(key, 0) + value
print(totals)
```

```text
{0: 100000.0, 1: 200000.0}
```

Each iteration reads one shard, aggregates it to a single number per
group, and discards the frame. This pattern works even without the
streaming engine — which is why it is the fallback for exotic formats.

## 5. Out-of-Core Joins: Big Left, Small Right

A join needs one side's keys in a hash table. When the *small* side
fits in memory (a user table, a label map, a tokenizer vocab) and the
big side does not, Polars streams the big side through and looks up the
small side — no hash table for the big table, no materialized join
buffer.

```python
import polars as pl

big = pl.LazyFrame({"user": [i % 1000 for i in range(2_000_000)],
                    "token_count": [100] * 2_000_000})
meta = pl.DataFrame({"user": [0, 1, 2], "tier": ["free", "pro", "pro"]})

joined = (big.select("user", "token_count")
             .join(meta.lazy(), on="user", how="left")
             .collect(engine="streaming"))
print(joined.height, joined.columns)
print(joined["tier"].null_count())   # users 3..999 not in meta
```

```text
2000000 ['user', 'token_count', 'tier']
1994000
```

The big side streams in batches; only the 3-row metadata table lives in
memory. The nulls are honest: 1994000 rows reference users absent from
the metadata — the join *did* stream, and the result says so.

## 6. Metadata-First Queries: Counting Without Loading

Some questions never need the data. `select(pl.len())` on a lazy scan
counts rows from parquet metadata (or with a cheap streaming pass) —
the query "how big is my corpus" must not load the corpus.

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
for shard in range(4):
    pl.DataFrame({"x": range(500_000)}).write_parquet(tmp / f"s{shard}.parquet")

corpus = pl.scan_parquet(tmp)
count = corpus.select(pl.len()).collect(engine="streaming")[0, 0]
print(count)
```

```text
2000000
```

`[0, 0]` on the collected single-cell frame extracts the integer without
building a Python list. The scan still opens the files, but the payload
stays on disk.

## 7. When Streaming Does Not Help

Streaming is not a magic switch. It does not help when:

- the **output** must be a full in-RAM frame anyway (then you are bound
  by the output size);
- the pipeline is a single tiny frame (the batching overhead dominates);
- the bottleneck is a single operator that needs the whole input (a full
  sort, a global median) — some operators degrade to spilling or fall
  back to non-streaming.

The honest diagnostic is `explain()` plus `estimated_size()`: if the
output is small and the operators are aggregations, stream. If you need
a full sorted frame in RAM, no engine argument saves you.

## Common Mistakes to Avoid

### Mistake 1: Collecting Before Filtering "To Be Safe"
```
# WRONG — the whole corpus lands in RAM before any work
big = pl.scan_parquet("corpus/").collect()
small = big.filter(...)
# CORRECT — keep the pipeline lazy, collect the small result
small = pl.scan_parquet("corpus/").filter(...).collect(engine="streaming")
```

### Mistake 2: Looping Over Rows to Process a Big File
```
# WRONG — O(n) Python dispatches; slower than the disk I/O
for row in big_df.iter_rows():
    ...
# CORRECT — vectorized expressions; loop over FILES, not rows
```

### Mistake 3: Calling sink_parquet on an Eager DataFrame
```
# WRONG — AttributeError: sink is a LazyFrame method
pl.DataFrame(...).sink_parquet(p)
# CORRECT — sink lives on the plan
pl.DataFrame(...).lazy().sink_parquet(p)
```

### Mistake 4: Assuming Streaming = Faster
```
# WRONG — streaming is about memory, not speed; it can be slower
# CORRECT — use it for big inputs/outputs; use eager for small data
```

### Mistake 5: Ignoring Nulls After Streaming Joins
```
# WRONG — assuming every big-side key matched
tier_counts = joined.group_by("tier").agg(pl.len()).sort("tier")
# CORRECT — nulls sort FIRST in Polars; use nulls_last=True when reading
tier_counts = joined.group_by("tier").agg(pl.len()).sort("tier", nulls_last=True)
```

## Best Practices

1. Default to `collect(engine="streaming")` for anything non-trivial
2. Use `sink_parquet` for large transformed outputs
3. Loop over shards, never over rows
4. Keep the join's small side in memory; stream the big side
5. Answer size questions with `pl.len()` on the lazy scan
6. Check `estimated_size()` before deciding eager vs streaming
7. Read the plan first: a streaming run of a bad plan is still bad
8. Sort with `nulls_last=True` when reading join results
9. Verify streaming == eager equivalence on a sample
10. Clean up temp corpora with context managers or `finally`

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `collect(engine="streaming")` | O(plan) | O(batch) | eager when output fits easily |
| `sink_parquet` | O(plan) | O(batch) | collect+write when output is small |
| shard loop | O(n) total | O(shard) | streaming collect (single pass) |
| big-left streamed join | O(n + m) | O(m) | — (m = small side) |
| `select(pl.len())` | O(metadata) | O(1) | — |

Memory is the currency: every pattern in this lecture trades a bounded
memory footprint for slightly more engineering or engine overhead. The
right choice is the smallest footprint that still meets the runtime
budget — and the answer changes with data size, not with preference.

## AI Engineering Relevance

**Where this shows up:** training data ETL and eval pipelines. A 50GB
corpus is processed every night: split stats, deduplication summaries,
token-count aggregates, feature joins — all of them streaming jobs.

| Concept here | Used for |
|--------------|----------|
| streaming collect | corpus statistics without OOM |
| sink_parquet | nightly feature prep: big in, smaller out |
| shard loops | custom per-shard transforms (dedup, hashing) |
| big-left joins | enriching corpora with in-memory metadata |
| metadata counts | dataset size reporting in CI |

**Scale note:** between 10GB and 1TB, the difference between an eager
`read_csv` pipeline and a streaming `scan_parquet` pipeline is the
difference between a job that OOMs and a job that finishes. At 1TB+,
streaming is not an optimization — it is the only option.

## Practice Exercises

### Exercise 1: Streaming Equivalence (Difficulty: Easy)
Run the same `group_by().agg(sum)` eagerly and with
`engine="streaming"` on 1M rows; assert `equals()` is True.

### Exercise 2: Sink Check (Difficulty: Easy)
Sink a filtered+projected lazy plan to parquet; assert the file exists
and its row count is less than the input count.

### Exercise 3: Shard Loop (Difficulty: Medium)
Build 4 shards, aggregate per shard in a loop, merge totals; assert the
merged result equals a single streaming collect.

### Exercise 4: Streaming Join (Difficulty: Medium)
Join a 2M-row lazy frame with a 3-row metadata frame in streaming mode;
assert height is preserved and unknown users get nulls.

### Exercise 5: Memory-Aware Decision (Difficulty: Hard)
Write `choose_mode(lf, output_estimate)` returning `"eager"`,
`"streaming"`, or `"sink"` given the estimated output size vs a budget;
assert each branch for a crafted frame.

## Summary

| Concept | Description |
|---------|-------------|
| Streaming engine | Bounded-memory execution of a lazy plan |
| Sinks | Writing a plan's output to disk, no intermediate frame |
| Shard loop | File-at-a-time reduce-and-merge, max portability |
| Big-left streamed join | Small side in memory, big side streams |
| Metadata queries | Counts and schemas without loading data |
| `estimated_size()` | Deciding eager vs streaming from numbers |

Larger-than-memory data is not an exception in AI work; it is the
default. The patterns here — streaming, sinking, sharding, smart joins —
are the same three ideas at every scale: don't materialize what you can
stream, don't read what you can skip, and keep the plan visible so the
optimizer can help.

## Quick Reference

| Task | Idiom |
|------|-------|
| Stream a plan | `lf.collect(engine="streaming")` |
| Write plan to disk | `lf.sink_parquet(path)` |
| Frame footprint | `df.estimated_size()` |
| Count rows lazily | `lf.select(pl.len()).collect(engine="streaming")[0, 0]` |
| Shard loop | `for p in sorted(dir.glob("*.parquet")): ...` |
| Big-left streamed join | `big.lazy().join(small.lazy(), on="k", how="left").collect(engine="streaming")` |
| Nulls-aware sort | `df.sort("tier", nulls_last=True)` |
| Batch limit | `df.iter_slices(n=100_000)` (in-RAM batching) |

## Next Steps

Next: continue into **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**,
where these pipelines feed models.
Review: **[01 Introduction](01-introduction-lecture.md)** for the memory
model that makes all of this fast.
Official docs: https://docs.pola.rs/user-guide/concepts/streaming/
