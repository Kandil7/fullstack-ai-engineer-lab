# 03-libraries/polars — 05: PyArrow and Parquet

## Topic Overview

Two formats carry the modern data stack: Arrow is the *memory* format,
and Parquet is the *disk* format. Arrow is columnar, typed, and
zero-copy-shareable: a table built by PyArrow can be consumed by Polars,
pandas, DuckDB, and PyTorch without conversion, because they all speak
the same buffer layout. Parquet is Arrow's disk twin: columnar files with
per-column compression, embedded schema, and row-group statistics that
let readers skip data they don't need.

For AI engineers this pair is the answer to "how do we store and load the
training corpus?" — and the answer is never CSV. This lecture covers the
Arrow table model, Polars/PyArrow interop, Parquet compression and
partitioning, the zero-copy bridge to NumPy, and an honest size
comparison that shows why Parquet beats CSV on every axis that matters.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build an Arrow Table and describe its schema
2. Convert between PyArrow, Polars, and NumPy with zero copies
3. Write Parquet with different compression codecs and compare sizes
4. Write and read hive-partitioned parquet datasets
5. Detect zero-copy behavior with `np.shares_memory`
6. Explain which dtypes copy and which don't when converting to NumPy
7. List the concrete reasons Parquet replaces CSV for datasets

## Prerequisites

| Need | Where |
|------|-------|
| Polars DataFrames | `01-introduction-lecture.md` |
| Lazy scanning of parquet | `03-lazy-evaluation-lecture.md` |
| numpy arrays and dtypes | `03-libraries/numpy/lectures/01-array-creating-lecture.md` |

## 1. What an Arrow Table Is

An Arrow `Table` is a columnar collection of typed arrays with an
explicit schema. It is the interchange object: PyArrow builds it, Polars
wraps it, parquet serializes it, DuckDB queries it.

```python
import pyarrow as pa
import polars as pl
import numpy as np

rng = np.random.default_rng(42)
table = pa.table({
    "id": pa.array(np.arange(5)),
    "score": pa.array(rng.normal(size=5)),
    "label": pa.array(["pos", "neg", "pos", "neg", "pos"]),
})
print(table.schema)
```

```text
id: int64
score: double
label: string
```

Every field is an Arrow type (`int64`, `double`, `string`) — the same
types Polars reports in `df.schema`. The table knows its own contract;
that contract is what makes round-trips lossless.

## 2. The Zero-Copy Bridge: Arrow -> Polars -> NumPy

`pl.from_arrow(table)` wraps the Arrow buffers without copying. From
there, `df["col"].to_numpy(allow_copy=False)` hands a column to NumPy as
a view when the dtype allows it. `np.shares_memory()` proves no copy
happened.

```python
import pyarrow as pa
import polars as pl
import numpy as np

table = pa.table({"score": pa.array([0.9, 0.4, 0.7])})
df = pl.from_arrow(table)
arr = df["score"].to_numpy(allow_copy=False)
print(np.shares_memory(df["score"].to_numpy(), arr))
```

```text
True
```

The same bytes serve as an Arrow array, a Polars Series, and a NumPy
array. That is why the "pandas -> polars -> torch" pipeline can be one
allocation: the data moves as pointers, not copies.

## 3. When Zero-Copy Is Impossible

Zero-copy works for fixed-width dtypes: ints, floats, booleans, dates.
Strings do not — a Python `str` object cannot wrap an Arrow string
buffer, so conversion builds new objects and raises when you demand a
no-copy view.

```python
import polars as pl

s = pl.Series("label", ["pos", "neg"])
try:
    s.to_numpy(allow_copy=False)
except RuntimeError as e:
    print(type(e).__name__)
```

```text
RuntimeError
```

The practical rule: keep strings in Arrow/Polars and convert only numeric
columns to NumPy. For a feature matrix this costs nothing — embeddings
and scalars are all numerics anyway.

## 4. Parquet: Columnar Layout on Disk

Parquet stores each column as its own compressed chunk, plus row-group
statistics (min/max per chunk). Readers use the layout twice: they read
only requested columns, and they skip row groups whose statistics prove
no rows can match the filter. Compression is per-column, which is why
the same file can carry zstd for floats and dictionary encoding for
low-cardinality strings.

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
df = pl.DataFrame({
    "id": range(100_000),
    "emb": pl.Series(range(100_000)).cast(pl.Float64) / 1000.0,
    "label": ["pos" if i % 2 else "neg" for i in range(100_000)],
})

sizes = {}
for name, kwargs in (("none", {"compression": None}),
                     ("snappy", {"compression": "snappy"}),
                     ("zstd", {"compression": "zstd"})):
    p = tmp / f"data-{name}.parquet"
    df.write_parquet(p, **kwargs)
    sizes[name] = p.stat().st_size

print(sizes["none"] > sizes["snappy"] > sizes["zstd"])
```

```text
True
```

The order is stable across versions: no compression is largest, snappy
is a middle ground, zstd wins on size (at some CPU cost). For datasets
that are read far more often than written, zstd is the default choice.

## 5. Partitioning: Hive-Style Directories

`write_parquet(dir, partition_by="label")` writes one file per partition
value into `label=value/` subdirectories — the layout Polars, DuckDB,
and Spark read natively. A filter on the partition column prunes whole
files.

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
df = pl.DataFrame({"id": range(6),
                   "label": ["pos", "neg", "pos", "neg", "pos", "neg"]})
df.write_parquet(tmp / "part", partition_by="label")
print(sorted(p.name for p in (tmp / "part").iterdir()))
```

```text
['label=neg', 'label=pos']
```

Reading restores the partition column automatically:

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
pl.DataFrame({"id": range(4), "label": ["pos", "neg", "pos", "neg"]}) \
  .write_parquet(tmp / "part", partition_by="label")

neg = (pl.scan_parquet(tmp / "part")
       .filter(pl.col("label") == "neg").collect())
print(neg.height)
```

```text
2
```

The scan pushed the filter into file selection: only `label=neg` was
opened. Partition by the columns you filter on — it is the cheapest
"index" a dataset can have.

## 6. CSV vs Parquet: The Size Case

CSV stores text: no schema, no compression, no statistics. The same
table as CSV is typically 2-4x larger than zstd Parquet, and every read
re-parses text. Parquet carries the schema, compresses, and skips data
via statistics.

```python
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
df = pl.DataFrame({"id": range(100_000),
                   "emb": pl.Series(range(100_000)).cast(pl.Float64) / 1000.0,
                   "label": ["pos" if i % 2 else "neg" for i in range(100_000)]})

csv_size = (df.write_csv(tmp / "d.csv"), (tmp / "d.csv").stat().st_size)[1]
df.write_parquet(tmp / "d.parquet", compression="zstd")
pq_size = (tmp / "d.parquet").stat().st_size
print(f"csv={csv_size}, parquet={pq_size}, ratio={csv_size / pq_size:.2f}")
```

```text
csv=4242970, parquet=1269870, ratio=3.34
```

That 3.3x is before any column pruning or row-group skipping — pure
encoding. Add those, and the effective gap grows to 10-100x on real
queries.

## 7. The Full Loop: Arrow -> Parquet -> Polars -> Arrow

The whole ecosystem is one round-trip: build in Arrow, store as Parquet,
read in Polars, hand back to Arrow. Nothing is lost and nothing is
converted by hand.

```python
import pyarrow as pa
import pyarrow.parquet as pq
import polars as pl
from pathlib import Path
import tempfile

tmp = Path(tempfile.mkdtemp())
table = pa.table({"id": pa.array([1, 2, 3]),
                  "score": pa.array([0.9, 0.4, 0.7])})
pq.write_table(table, tmp / "t.parquet", compression="zstd")

back = pl.read_parquet(tmp / "t.parquet")
print(back.to_arrow().schema)
```

```text
id: int64
score: double
```

This is the load path of a training pipeline: dataset builders emit
Parquet; loaders read it into Arrow; Polars does the feature work; the
final columns go to NumPy/Torch as views.

## Common Mistakes to Avoid

### Mistake 1: Converting Through pandas for No Reason
```
# WRONG — copies twice, then copies again
arrow_table.to_pandas().to_numpy()
# CORRECT — zero-copy path when the dtype allows
pl.from_arrow(table)["score"].to_numpy(allow_copy=False)
```

### Mistake 2: Assuming Zero-Copy for Strings
```
# WRONG — RuntimeError: string columns cannot be viewed without copy
df["label"].to_numpy(allow_copy=False)
# CORRECT — keep strings in Arrow/Polars; convert only numerics
```

### Mistake 3: Treating Compressed CSV as a Dataset
```
# WRONG — zip has no schema, no statistics, no column pruning
data.csv.zip
# CORRECT — write parquet once with a real codec
df.write_parquet("data.parquet", compression="zstd")
```

### Mistake 4: Forgetting Partitioning on Filtered Columns
```
# WRONG — one big file, every query reads everything
df.write_parquet("all.parquet")
# CORRECT — partition by the filter column
df.write_parquet("corpus/", partition_by="label")
```

### Mistake 5: Mixing CSV and Parquet in One Directory
```
# WRONG — scan_parquet(dir) raises on mixed extensions
# CORRECT — parquet-only directories, or explicit globs
```

## Best Practices

1. Build datasets as Arrow Tables or Polars frames, store as Parquet
2. Use zstd by default; snappy when write speed matters more
3. Partition by the columns your queries filter on
4. Convert numerics to NumPy with `allow_copy=False`; keep strings native
5. Verify zero-copy claims with `np.shares_memory`, never by reading code
6. Prefer directory scans for corpora; keep shard dirs homogeneous
7. Pin schemas explicitly when writing Parquet (types travel with data)
8. Check `sizes["zstd"] < sizes["snappy"]` in verification, not exact bytes
9. Round-trip test: write -> read -> compare schema and row count
10. For huge datasets, stream: `scan_parquet(...).sink_parquet(...)`

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `pa.table(dict)` | O(n) | O(n) | build columns as arrays first |
| `pl.from_arrow(t)` | O(1) | O(1) | zero-copy wrap |
| `to_numpy(allow_copy=False)` | O(1) or O(n) | O(1) or O(n) | numeric dtypes only |
| `write_parquet(zstd)` | O(n) | O(n) disk | snappy when write-bound |
| `partition_by="k"` | O(n) | O(n) disk | fewer, larger partitions |
| directory scan + filter | O(matched) | O(matched) | partition pruning |

Disk size is the dominant cost for datasets, and Parquet attacks it
twice: per-column compression and row-group skipping. Memory cost is
attacked by zero-copy: the same buffers flow from file to model.

## AI Engineering Relevance

**Where this shows up:** dataset engineering. HuggingFace datasets,
feature stores, and eval corpora all speak Parquet; Arrow is the load
path into Polars, DuckDB, and PyTorch.

| Concept here | Used for |
|--------------|----------|
| Arrow Table schema | typed feature contracts before training |
| zero-copy to NumPy | feeding embedding columns to model code |
| zstd Parquet | 3-10x smaller corpora, faster transfers |
| partition_by label/split | reading only the split you train on |
| directory scans | sharded 50GB corpora as one logical table |

**Scale note:** at 1TB, CSV is not "inefficient", it is *unusable*: 3TB
of storage, no pruning, no schema. Parquet with zstd and partitioning
turns the same corpus into a few hundred GB with filtered reads — the
difference between a dataset and a liability.

## Practice Exercises

### Exercise 1: Arrow Build (Difficulty: Easy)
Build a `pa.Table` with an int64, a float64, and a string column; assert
`num_rows` and the field types.

### Exercise 2: Zero-Copy Check (Difficulty: Easy)
Convert an Arrow numeric column through Polars to NumPy with
`allow_copy=False`; assert `np.shares_memory(...)` is True.

### Exercise 3: Compression Order (Difficulty: Medium)
Write the same frame with `compression=None`, `snappy`, and `zstd`;
assert the byte sizes strictly decrease in that order.

### Exercise 4: Partition Round-Trip (Difficulty: Medium)
Write a frame partitioned by `label`, then read it back with a filter on
`label`; assert the partition columns are restored and counts sum to the
original height.

### Exercise 5: CSV vs Parquet Report (Difficulty: Hard)
Write a function returning `(csv_bytes, parquet_bytes)` for the same
frame; assert parquet is smaller AND return the ratio for the demo
output.

## Summary

| Concept | Description |
|---------|-------------|
| Arrow Table | Columnar typed memory; the interchange format |
| Parquet | Columnar disk format: compression + statistics |
| Zero-copy | `pl.from_arrow` + `to_numpy(allow_copy=False)` share buffers |
| zstd / snappy / none | Compression ladder; zstd smallest, none largest |
| Hive partitioning | `label=value/` directories; filters prune files |
| CSV vs Parquet | 2-4x size gap before pruning; schema + stats on top |

Arrow and Parquet are the substrate beneath Polars: the memory layout
that makes columnar work fast and the disk layout that makes corpora
manageable. With zero-copy interop and partitioned reads, the pipeline
from raw events to model input becomes one typed, pruned data flow.

## Quick Reference

| Task | Idiom |
|------|-------|
| Build Arrow table | `pa.table({"a": pa.array(...)})` |
| Arrow -> Polars | `pl.from_arrow(table)` |
| Polars -> Arrow | `df.to_arrow()` |
| Column to numpy view | `df["a"].to_numpy(allow_copy=False)` |
| Write parquet | `df.write_parquet(p, compression="zstd")` |
| Partitioned write | `df.write_parquet(dir, partition_by="k")` |
| Scan directory | `pl.scan_parquet(dir)` |
| pyarrow write | `pq.write_table(table, p, compression="zstd")` |
| File size | `Path(p).stat().st_size` |

## Next Steps

Next: **[06 Larger Than Memory](06-larger-than-memory-lecture.md)** —
streaming, sinks, and out-of-core joins on the data you just stored.
Continues in: **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**
Official docs: https://arrow.apache.org/docs/python/parquet.html
