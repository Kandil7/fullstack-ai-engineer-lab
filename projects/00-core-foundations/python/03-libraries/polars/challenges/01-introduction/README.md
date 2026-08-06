# Challenge 01: Polars Introduction

## 🥉 Bronze — Typed Feature Frame (~15 min)

**Task:** Build a feature DataFrame from raw column dicts with an explicit
schema. Raw strings arrive as text and must become the right Arrow dtypes.

**Signature:**
```python
def build_features_frame(raw: dict[str, list]) -> pl.DataFrame:
```

**Requirements:**
- DataFrame must have columns: `sample_id` (Int64), `score` (Float64),
  `split` (String)
- Force the dtypes explicitly with `.cast()` — construction infers, and
  strict mode refuses to reinterpret `"1"` as an int at build time
- Return a `pl.DataFrame`

| Input | Expected |
|-------|----------|
| `{"sample_id": ["1", "2"], "score": [0.9, 0.4], "split": ["a", "b"]}` | frame with schema `Int64, Float64, String` |

**Constraints:** n <= 10^3 rows. Any correct approach passes.

---

## 🥈 Silver — Column Stats via Expressions (~35 min)

**Task:** Compute per-column statistics for every numeric column using
Polars expressions — no Python loops, no `apply`.

**Signature:**
```python
def column_stats(df: pl.DataFrame) -> dict[str, tuple[float, float, float]]:
```

**Requirements:**
- Return `{col: (mean, min, max)}` for every numeric column (Int/Float)
- Skip non-numeric columns entirely
- Must be vectorized: no `for` loops over rows, no `.apply()`

| Input | Expected |
|-------|----------|
| `pl.DataFrame({"a": [1.0, 2.0, 3.0], "s": ["x", "y", "z"]})` | `{"a": (2.0, 1.0, 3.0)}` |

**Constraints:** n <= 10^6. A per-element Python loop will be flagged.

---

## 🥇 Gold — Memory Footprint Estimator (~75 min)

**Task:** Estimate the in-memory footprint (in bytes) of a frame's numeric
columns using Arrow dtype widths — the number you consult before deciding
eager vs streaming.

**Signature:**
```python
def estimate_numeric_bytes(df: pl.DataFrame) -> int:
```

**Requirements:**
- Sum `row_count * dtype_width` over numeric columns only
- Dtype widths: Int8/8, Int16/16, Int32/32, Int64/64, UInt variants same,
  Float32/32, Float64/64
- Ignore strings, booleans, nulls, and other non-numeric types
- Must be a single pass over the schema — no Python loops over rows

| Input | Expected |
|-------|----------|
| 1_000_000 rows of Int64 | `8_000_000` |
| 500_000 rows of Float32 + 500_000 rows of Int16 | `2_000_000 + 1_000_000 = 3_000_000` |

**Constraints:** n <= 10^7. Must stay O(columns), not O(rows).
**Follow-up:** why does `estimated_size()` differ from your sum? (Answer:
it adds per-column overhead, string offsets, and validity bitmaps.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/01-introduction/test_challenge.py -v
```

## Test File Structure

```
challenges/01-introduction/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
