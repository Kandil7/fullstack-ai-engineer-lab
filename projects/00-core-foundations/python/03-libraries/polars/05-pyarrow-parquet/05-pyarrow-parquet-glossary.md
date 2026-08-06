# PyArrow and Parquet — Glossary 05

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| Arrow Table | Type | Columnar typed memory table; the interchange format |
| pa.table() | Function | Builds an Arrow Table from arrays/columns |
| pl.from_arrow() | Function | Wraps an Arrow Table as a Polars frame (zero-copy) |
| to_arrow() | Method | Converts a Polars frame to an Arrow Table |
| to_numpy() | Method | Converts a Series to a NumPy array |
| allow_copy=False | Option | Demands a zero-copy view; raises if impossible |
| np.shares_memory | Function | Proves two arrays share a buffer |
| Parquet | Format | Columnar disk format: compression + statistics |
| compression | Concept | Per-column codecs: none, snappy, zstd |
| zstd | Codec | Strongest default compression (slower writes) |
| snappy | Codec | Middle compression, fast writes |
| partition_by | Option | Hive-style `key=value/` directory layout |
| hive partitioning | Concept | `label=neg/` directories read by all engines |
| row-group statistics | Concept | Per-chunk min/max enabling row-group skipping |
| pq.write_table | Function | pyarrow parquet writer |
| scan_parquet(dir) | Function | Lazy read of all shards in a directory |
| CSV | Format | Text format: no schema, no compression, no stats |
| dictionary encoding | Concept | Parquet's low-cardinality string compression |

## Detailed Definitions

### Arrow Table
**Definition**: A columnar, typed collection of arrays with an explicit
schema — the in-memory interchange object of the Arrow ecosystem.
**Example**:
```python
import pyarrow as pa
t = pa.table({"id": pa.array([1, 2]), "ok": pa.array([True, False])})
print(t.num_rows, t.num_columns)
```
```text
2 2
```
**Complexity**: O(n) to build.
**Related**: pa.table(), pl.from_arrow()

### pa.table()
**Definition**: PyArrow's constructor taking a dict of column name to
array/sequence; infers types and produces a Table.
**Related**: Arrow Table, to_arrow()

### pl.from_arrow()
**Definition**: Wraps an Arrow Table as a Polars DataFrame sharing the
same buffers — no conversion, O(1).
**Example**:
```python
import pyarrow as pa
import polars as pl
t = pa.table({"x": pa.array([1.0, 2.0])})
df = pl.from_arrow(t)
print(df.shape)
```
```text
(2, 1)
```
**Complexity**: O(1) wrap.
**Related**: Arrow Table, zero-copy

### to_arrow()
**Definition**: The Polars DataFrame method returning an Arrow Table
view of the same data.
**Related**: pl.from_arrow(), Arrow Table

### to_numpy()
**Definition**: Converts a Series to a NumPy array. With
`allow_copy=False` it must be a view or raises.
**Example**:
```python
import polars as pl
import numpy as np
s = pl.Series("v", [1.0, 2.0])
a = s.to_numpy(allow_copy=False)
print(np.shares_memory(s.to_numpy(), a))
```
```text
True
```
**Complexity**: O(1) view or O(n) copy.
**Related**: allow_copy=False, np.shares_memory

### allow_copy=False
**Definition**: The to_numpy option demanding zero-copy semantics.
Raises RuntimeError for dtypes that cannot be viewed (strings).
**Related**: to_numpy(), zero-copy

### np.shares_memory
**Definition**: The verification tool for zero-copy claims: True means
two arrays reference the same underlying buffer.
**Related**: allow_copy=False, zero-copy

### Parquet
**Definition**: The columnar disk format: per-column compression,
embedded schema, and row-group statistics. The default dataset format
of the AI stack.
**Related**: CSV, hive partitioning

### compression
**Definition**: Per-column encoding of a parquet file. Choices trade
size against write CPU: none, snappy, zstd.
**Related**: zstd, snappy

### zstd
**Definition**: The compression codec with the best size ratio at
moderate CPU cost; the default for read-heavy datasets.
**Related**: compression, snappy

### snappy
**Definition**: The fast middle-ground codec; larger files than zstd
but cheaper writes.
**Related**: compression, zstd

### partition_by
**Definition**: The write option producing hive-style directories —
one `key=value/` directory per distinct value.
**Example**:
```python
import polars as pl
from pathlib import Path
import tempfile

out = Path(tempfile.mkdtemp()) / "part"
pl.DataFrame({"k": ["a", "b"], "v": [1, 2]}).write_parquet(out, partition_by="k")
print(sorted(p.name for p in out.iterdir()))
```
```text
['k=a', 'k=b']
```
**Related**: hive partitioning, scan_parquet(dir)

### hive partitioning
**Definition**: The `key=value/` directory convention shared by Polars,
DuckDB, and Spark; filters on partition columns prune whole files.
**Related**: partition_by, row-group statistics

### row-group statistics
**Definition**: Min/max metadata per parquet row group; a pushed
predicate can skip groups whose stats exclude a match.
**Related**: hive partitioning, scan_parquet(dir)

### pq.write_table
**Definition**: The pyarrow function writing an Arrow Table to parquet
with codec options — the file-writing side of the ecosystem.
**Related**: Arrow Table, compression

### scan_parquet(dir)
**Definition**: Lazy reader over one file or a whole directory of
shards; rejects directories mixing file extensions.
**Related**: hive partitioning, row-group statistics

### CSV
**Definition**: The text format: no schema, no compression, no
statistics. The same data as parquet is typically 2-4x larger before
any pruning.
**Related**: Parquet, compression

### dictionary encoding
**Definition**: Parquet's treatment of low-cardinality strings: store
the vocabulary once, reference by index — often the biggest single
saving on label columns.
**Related**: compression, Parquet

## Key Concepts Summary

### The Two Formats
- Arrow: columnar typed memory, shared zero-copy across tools
- Parquet: columnar typed disk, compressed, with statistics

### Zero-Copy Rules
- Numeric dtypes can be viewed: `to_numpy(allow_copy=False)`
- Strings must copy: RuntimeError when a view is demanded
- Prove it with `np.shares_memory`, never by reading code

### Dataset Layout
- zstd < snappy < none in file size, always
- Partition by the columns you filter on
- Directory scans read shards as one logical table

## Practice Terms

Match each term to its definition (answers at the bottom).

1. zstd — ___
2. partition_by — ___
3. allow_copy=False — ___
4. row-group statistics — ___
5. pl.from_arrow() — ___

A. Demands a zero-copy numpy view, raising if impossible
B. Wraps an Arrow Table as a Polars frame without copying
C. Codec with the best size ratio for read-heavy datasets
D. Min/max metadata enabling row-group skipping
E. Write option creating key=value/ directories

**Answers:** 1-C, 2-E, 3-A, 4-D, 5-B
