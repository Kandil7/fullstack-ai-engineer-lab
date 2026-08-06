# Challenge 05: PyArrow & Parquet

## 🥉 Bronze — Zstd Writer (~15 min)

**Task:** Write a Polars frame to Parquet with zstd compression and
report the on-disk size.

**Signature:**
```python
def write_zstd_parquet(df: pl.DataFrame, path: str) -> int:
```

**Requirements:**
- `df.write_parquet(path, compression="zstd")`
- Return `os.path.getsize(path)` (bytes)

| Input | Expected |
|-------|----------|
| 50k-row frame (int + float + string cols) | bytes on disk > 0 |

**Constraints:** n <= 10^6. File must actually be zstd — the test
verifies via `parquet_file.metadata` through PyArrow.

---

## 🥈 Silver — Compression Wins (~35 min)

**Task:** Compare a CSV export vs a zstd Parquet export of the same
frame and return both sizes.

**Signature:**
```python
def compression_compare(df: pl.DataFrame, csv_path: str, pq_path: str) -> dict[str, int]:
```

**Requirements:**
- Write the CSV (default), then the Parquet with zstd
- Return `{"csv_bytes": ..., "parquet_bytes": ...}`

| Input | Expected |
|-------|----------|
| 50k-row seeded frame | `parquet_bytes` strictly < `csv_bytes` |

**Constraints:** n <= 10^6. The comparison must hold for a frame with a
repetitive string column (that is what makes compression effective).

---

## 🥇 Gold — Zero-Copy Round Trip (~75 min)

**Task:** Prove the zero-copy read path: write a frame, read it back,
and show that a numeric column is served from the arrow buffer without
a copy.

**Signature:**
```python
def roundtrip_zero_copy(df: pl.DataFrame, path: str) -> dict[str, object]:
```

**Requirements:**
- Write Parquet (zstd), read back with `scan_parquet(...).collect()`
- Extract one numeric column via `pl.col(...).to_numpy(allow_copy=False)`
- Return `{"match": bool, "zero_copy": bool}` where `match` = exact
  equality with the source column and `zero_copy` = the to_numpy call
  succeeded without raising

| Input | Expected |
|-------|----------|
| 100k-row frame with a float `score` column | `match` True, `zero_copy` True |

**Constraints:** n <= 10^6. Use the new `allow_copy=False` keyword
(`zero_copy_only` is deprecated in Polars 1.4x+).
**Follow-up:** why does this fail for string columns? (Answer: the Arrow
string layout is not a contiguous buffer of Python str, so a copy is
unavoidable — Polars raises RuntimeError instead of silently copying.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/05-pyarrow-parquet/test_challenge.py -v
```

## Test File Structure

```
challenges/05-pyarrow-parquet/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
