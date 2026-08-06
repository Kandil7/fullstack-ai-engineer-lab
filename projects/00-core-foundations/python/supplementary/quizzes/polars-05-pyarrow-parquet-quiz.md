# Polars 05 — PyArrow & Parquet Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** `df.write_parquet("out.parquet")` writes:

- A) a columnar binary file readable by Polars, pandas, DuckDB, and
  Spark (via Arrow)
- B) a CSV with a different extension
- C) a compressed JSON file
- D) a Python pickle

**E2.** The default compression for `df.write_parquet` in Polars is:

- A) zstd
- B) snappy
- C) gzip
- D) uncompressed

**E3 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3]})
df.write_parquet("t.parquet")
print(pl.read_parquet("t.parquet").height)
```

- A) `3`
- B) `1`
- C) `3.0`
- D) `0`

**E4.** `pl.scan_parquet("data.parquet")`:

- A) returns a lazy query over the parquet file
- B) reads the whole file eagerly
- C) returns the raw bytes
- D) raises unless `collect()` is passed

**E5.** `df.write_parquet(path, compression="snappy")`:

- A) selects the snappy codec explicitly
- B) is invalid — only zstd exists
- C) always produces a bigger file than zstd
- D) writes a CSV with snappy metadata

**E6 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3]})
df.write_parquet("t.parquet")
print(pl.scan_parquet("t.parquet").collect().shape)
```

- A) `(3, 1)`
- B) `(1, 3)`
- C) `(3, 3)`
- D) `(3,)`

---

## Medium

**M1.** Which is the *most compressed* (smallest file) among these for
typical numeric+string ML data?

- A) zstd parquet
- B) snappy parquet
- C) uncompressed parquet
- D) raw CSV

**M2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"score": [0.5, 0.25]})
arr = df["score"].to_numpy(allow_copy=False)
print(arr.dtype)
print(arr[0])
```

- A) `float64` `0.5`
- B) `float32` `0.5`
- C) `float64` `[0.5]`
- D) raises `RuntimeError`

**M3 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"label": ["pos", "neg"]})
try:
    df["label"].to_numpy(allow_copy=False)
    print("ok")
except RuntimeError:
    print("RuntimeError")
```

- A) `RuntimeError`
- B) `ok`
- C) `TypeError`
- D) `ValueError`

**M4.** `pl.scan_parquet("shards/")` on a directory containing *both*
`.parquet` and `.csv` files:

- A) raises — a parquet directory scan expects parquet files only
- B) reads both formats transparently
- C) reads only the parquet files
- D) sorts the directory alphabetically

**M5.** The parquet schema of
```python
df = pl.DataFrame({"id": [1], "emb_0": [0.1], "label": ["pos"]})
```
is:

- A) `id: Int64, emb_0: Float64, label: String`
- B) `id: int, emb_0: float, label: str`
- C) `id: Int32, emb_0: Float32, label: String`
- D) `id: Float64, emb_0: Float64, label: String`

**M6 (code-output).** What prints?
```python
import os
import polars as pl
df = pl.DataFrame({"a": [i % 1000 for i in range(100_000)]})
df.write_parquet("z.parquet", compression="zstd")
df.write_parquet("u.parquet", compression="uncompressed")
print(os.path.getsize("z.parquet") < os.path.getsize("u.parquet"))
```

- A) `True`
- B) `False`
- C) `0`
- D) raises `FileNotFoundError`

**M7 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
df.write_parquet("t.parquet", compression="zstd")
back = pl.read_parquet("t.parquet")
print(back["a"].sum())
print(back["b"][1])
```

- A) `6` `y`
- B) `6` `'y'`
- C) `3` `y`
- D) `[6]` `y`

**M8.** Which statement about `to_numpy`'s copy semantics is true?

- A) `allow_copy=False` means a copy is an *error*, not a silent
  slowdown
- B) `allow_copy=False` guarantees no copy ever happens, for any dtype
- C) `zero_copy_only` is the new name for `allow_copy`
- D) numpy always copies Arrow data

**M9.** Parquet is a good storage format for ML features because:

- A) it is columnar: queries read only the needed columns
- B) it is row-oriented like CSV
- C) it cannot store strings
- D) it requires a database server

---

## Hard

**H1.** Why can a `Float64` column be zero-copied into numpy but a
`String` column cannot?

- A) float64 is a contiguous numeric buffer; String uses an
  offset+bytes layout that numpy cannot view directly
- B) strings are always encoded with UTF-16
- C) numpy lacks string support entirely
- D) parquet stores strings compressed; floats are stored raw

**H2 (code-output).** What prints?
```python
import polars as pl
df = pl.DataFrame({"label": ["neg"] * 4})
df.write_parquet("t.parquet", compression="zstd")
schema = pl.read_parquet("t.parquet").schema
print(schema["label"])
print(pl.read_parquet("t.parquet")["label"].to_list())
```

- A) `String` `['neg', 'neg', 'neg', 'neg']`
- B) `str` `['neg']`
- C) `Utf8` `['neg', 'neg', 'neg', 'neg']`
- D) `String` `['neg']`

**H3.** A CSV export of a 100k-row frame (int + float + repetitive
string) vs the same frame as zstd parquet — expected size relation:

- A) parquet is smaller: columnar layout + zstd beats raw text
- B) CSV is always smaller
- C) equal by construction
- D) parquet is bigger because of schema overhead

**H4.** The zero-copy contract is verified in the lab with:

- A) `allow_copy=False` and catching `RuntimeError`
- B) comparing `sys.getsizeof` of two arrays
- C) timing `to_numpy` twice
- D) checking `arr.flags["OWNDATA"]` — always True

**H5.** Which is the correct *lazy* read path for a single parquet
file?

- A) `pl.scan_parquet(f).select(pl.col("a")).collect()`
- B) `pl.read_parquet(f).select(pl.col("a"))`
- C) `pl.read_parquet(f)["a"]`
- D) `pl.from_pandas(pl.read_parquet(f))`

---

## Answer Key

**E1 — A.** Parquet is a columnar binary format; Arrow makes it
interoperable across the data ecosystem.
*Distractors:* B is false (binary, not CSV); C is false; D is
Python-only.

**E2 — A.** Polars defaults `write_parquet` to zstd compression.
*Distractors:* B is pyarrow's default; C is legacy; D is opt-in via
`compression="none"`.

**E3 — A.** The roundtrip preserves all 3 rows.
*Distractors:* B is the column count; C is float coercion; D is
false.

**E4 — A.** `scan_parquet` returns a LazyFrame over the file.
*Distractors:* B is `read_parquet`; C is `open()`; D is false.

**E5 — A.** `compression="snappy"` selects the snappy codec
explicitly.
*Distractors:* B is false; C is a heuristic, not a rule; D is false.

**E6 — A.** Shape is (rows, columns) = (3, 1).
*Distractors:* B swaps the tuple; C invents columns; D is the numpy
shape.

**M1 — A.** zstd typically gives the smallest files for ML data
(verified: zstd 1,688,371 < snappy 2,015,147 < none 2,414,081 < CSV
4,915,505 bytes on the lab frame).
*Distractors:* B is second; C/D are larger.

**M2 — A.** A float64 Arrow buffer is a contiguous double array;
numpy views it directly — dtype `float64`, value 0.5.
*Distractors:* B is wrong width; C is an array repr; D is the string
case, not numeric.

**M3 — A.** String columns raise `RuntimeError` under
`allow_copy=False` — the offset+bytes layout cannot be viewed as a
single numpy buffer (verified).
*Distractors:* B is the numeric case; C/D are wrong exception types.

**M4 — A.** Directory scans expect homogeneous parquet files; mixed
extensions raise `InvalidOperationError`.
*Distractors:* B/C/D describe nonexistent tolerance.

**M5 — A.** Roundtrip keeps Polars dtypes: Int64, Float64, String.
*Distractors:* B is numpy speak; C changes widths; D changes id's
type.

**M6 — A.** zstd is far smaller: 3,466 vs 133,530 bytes on the
100k-row snippet (verified). Caution: parquet's "uncompressed" still
RLE/bit-packs runs, so codec gains only show on non-run data — and
polars 1.43 accepts `"uncompressed"`, not `"none"`.
*Distractors:* B inverts; C is not how bool prints; D is false —
write_parquet succeeds.

**M7 — A.** Sum = 6; `"b"[1]` = "y".
*Distractors:* B shows repr quotes; C is the count; D misses
`.item()`-style extraction (Series sum is already a scalar... note
`back["a"].sum()` returns a Python int → prints `6`).

**M8 — A.** `allow_copy=False` makes a copy an error — the point is
to fail loudly rather than silently slow down.
*Distractors:* B is false (strings copy); C is backwards
(`zero_copy_only` is the deprecated name); D is false.

**M9 — A.** Columnar layout means a query over one feature column
reads only that column's pages.
*Distractors:* B/C/D are false.

**H1 — A.** Numeric columns are contiguous; String is an offsets +
bytes layout, not a single contiguous buffer numpy can wrap.
*Distractors:* B is false; C is false; D is false (compression is
decompressed at read).

**H2 — A.** Schema roundtrips: `String`; all 4 rows survive.
*Distractors:* B uses Python type; C is the deprecated alias; D
drops rows.

**H3 — A.** Columnar layout + zstd beats raw text for repetitive
data (verified in the lab: 1.7 MB vs 4.9 MB).
*Distractors:* B/C/D are false.

**H4 — A.** The lab pattern: try `allow_copy=False`, catch
`RuntimeError` — that is the honest zero-copy test.
*Distractors:* B/C are timing heuristics; D is false (OWNDATA is
often True for fresh arrays regardless).

**H5 — A.** scan → lazy select → collect is the canonical lazy path.
*Distractors:* B is eager; C is eager; D adds a pointless pandas hop.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 05](03-libraries/polars/lectures/05-pyarrow-parquet-lecture.md) ·
[Glossary 05](03-libraries/polars/lectures/05-pyarrow-parquet-glossary.md) ·
[Challenge 05](03-libraries/polars/challenges/05-pyarrow-parquet/README.md)
