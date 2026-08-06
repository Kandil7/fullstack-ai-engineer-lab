# Larger Than Memory — Glossary 06

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| streaming engine | Execution | Bounded-memory execution of a lazy plan |
| collect(engine="streaming") | Method | Run a plan in batches instead of materializing |
| sink_parquet() | Method | Write a plan's output to disk, no intermediate frame |
| shard | Concept | One file of a multi-file corpus |
| shard loop | Pattern | File-at-a-time reduce-and-merge processing |
| out-of-core | Concept | Processing data larger than available RAM |
| big-left join | Pattern | Large lazy frame joined with a small in-memory table |
| metadata query | Pattern | Counts/schemas answered without loading data |
| estimated_size() | Method | In-memory footprint of a frame in bytes |
| iter_slices() | Method | Yields in-RAM batches of a DataFrame |
| nulls_last | Option | Sort nulls after values (`sort("c", nulls_last=True)`) |
| spill | Concept | Streaming operator falling back to disk for whole-input ops |
| batch | Concept | The unit of rows processed at once by the streaming engine |
| reduce-and-merge | Pattern | Aggregate per shard, then merge partial aggregates |
| corpus | Concept | The full collection of data files a pipeline reads |

## Detailed Definitions

### streaming engine
**Definition**: The execution mode that processes a lazy plan in
bounded-memory batches: read batch, apply operators, accumulate, free,
repeat. Same results as eager, lower peak memory.
**Related**: collect(engine="streaming"), batch

### collect(engine="streaming")
**Definition**: The collect call that engages the streaming engine.
The code is otherwise identical to a plain collect.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"k": [1, 2, 3]})
print(lf.group_by("k").agg(pl.len()).collect(engine="streaming").height)
```
```text
3
```
**Related**: streaming engine, sink_parquet()

### sink_parquet()
**Definition**: A LazyFrame method writing the plan's output directly to
disk in batches — the "write side" of streaming.
**Example**:
```python
import polars as pl
from pathlib import Path
import tempfile

out = Path(tempfile.mkdtemp()) / "r.parquet"
pl.LazyFrame({"a": [1, 2]}).sink_parquet(out)
print(out.stat().st_size > 0)
```
```text
True
```
**Related**: collect(engine="streaming"), out-of-core

### shard
**Definition**: One file of a multi-file dataset. Corpora are split into
shards so each can be processed independently and in parallel.
**Related**: shard loop, corpus

### shard loop
**Definition**: The pattern of iterating over shard files, reducing each
to a tiny aggregate, and merging — peak memory is one shard plus one
summary row.
**Related**: shard, reduce-and-merge

### out-of-core
**Definition**: Processing data larger than available RAM by streaming,
batching, or file-level iteration rather than materializing.
**Related**: streaming engine, sink_parquet()

### big-left join
**Definition**: A join where the large side streams through while the
small side (metadata, label maps) lives in memory as the hash table.
**Related**: streaming engine, shard loop

### metadata query
**Definition**: A question answered from parquet metadata or a cheap
streaming pass — e.g., row counts via `select(pl.len())` — without
loading the data.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"x": range(1000)})
print(lf.select(pl.len()).collect(engine="streaming")[0, 0])
```
```text
1000
```
**Related**: out-of-core, estimated_size()

### estimated_size()
**Definition**: Returns a frame's estimated in-memory size in bytes;
the number that decides eager vs streaming.
**Related**: metadata query, streaming engine

### iter_slices()
**Definition**: Yields in-RAM batches of a DataFrame (`n=` rows each) —
the in-memory batching tool when the frame already fits but you want
chunked processing.
**Related**: batch, shard loop

### nulls_last
**Definition**: Sort option placing nulls after all values. Polars sorts
nulls FIRST by default — a common surprise when reading join results.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"t": [None, "b", "a"]})
print(df.sort("t", nulls_last=True)["t"].to_list())
```
```text
['a', 'b', None]
```
**Related**: big-left join, out-of-core

### spill
**Definition**: A streaming operator's fallback when it needs the whole
input (full sort, global median): data moves to disk and back. Some
plans degrade this way; the plan text tells you.
**Related**: streaming engine, batch

### batch
**Definition**: The unit of rows the streaming engine processes at a
time. Aggregates accumulate per batch and merge at the end.
**Related**: streaming engine, spill

### reduce-and-merge
**Definition**: The algorithmic shape of shard loops: reduce each shard
to a small summary, then merge the summaries into the final result.
**Related**: shard loop, corpus

### corpus
**Definition**: The full collection of data files a pipeline reads as
one logical dataset — typically sharded parquet.
**Related**: shard, shard loop

## Key Concepts Summary

### Three Out-of-Core Tools
- Streaming engine: `collect(engine="streaming")` for bounded RAM
- Sinks: `sink_parquet()` writes plans to disk directly
- Shard loops: file-at-a-time reduce-and-merge, most portable

### Join Strategy
- Small side in memory as the hash table
- Big side streams through in batches
- Expect nulls for unmatched big-side keys; sort with nulls_last

### Decision Discipline
- Measure with `estimated_size()` before choosing a mode
- Streaming is about memory, not speed
- Metadata queries (pl.len()) never load payload data

## Practice Terms

Match each term to its definition (answers at the bottom).

1. sink_parquet() — ___
2. shard loop — ___
3. big-left join — ___
4. estimated_size() — ___
5. spill — ___

A. Writing a plan's output to disk without an intermediate frame
B. Large frame streams through a small in-memory hash table
C. File-at-a-time reduce-and-merge processing
D. Frame footprint in bytes; the eager-vs-streaming decision input
E. Streaming fallback to disk for whole-input operators

**Answers:** 1-A, 2-C, 3-B, 4-D, 5-E
