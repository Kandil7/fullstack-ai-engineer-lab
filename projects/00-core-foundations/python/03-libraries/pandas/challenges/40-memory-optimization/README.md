# Challenge 40: Memory Optimization

The cheapest optimization in the data stack: same values, 50-90% less RAM.
This challenge builds the audit, the dtype pass, and the streamed read — and
pins the memory savings with assertions, not vibes.

## 🥉 Bronze — Honest Measurement (~15 min)

**Task:** Implement `measure_deep(frame)`, returning the total
`memory_usage(deep=True)` of the frame as an `int`. This is the only honest
number for columns containing strings.

**Signature:**
```python
def measure_deep(frame: pd.DataFrame) -> int:
```

| Input | Expected |
|---|---|
| `{"a": [1, 2, 3]}` | int64: `3 * 8 + overhead` — use `frame.memory_usage(deep=True).sum()` |
| `{"s": ["x", "y", "z"]}` | strictly greater than `3 * 8` (string payloads) |

**Constraints:** `n <= 10^3`. Any correct approach passes.

---

## 🥈 Silver — The Optimization Pass (~35 min)

**Task:** Implement `optimize_dtypes(frame)` returning a **new** frame where
every column is right-sized: integer columns downcast
(`pd.to_numeric(..., downcast="integer")`), float columns downcast to
`float32`, low-cardinality object columns (`nunique() / len < 0.1`)
converted to `category`. Values must be preserved: ints exactly, floats
within `1e-6`.

**Signature:**
```python
def optimize_dtypes(frame: pd.DataFrame) -> pd.DataFrame:
```

| Input (100k rows) | Expected |
|---|---|
| `user_id` ints in `[0, 1_000_000)` | dtype `int32` (not int64) |
| `score` floats in `[0, 1)` | dtype `float32` |
| `tier` from 3 strings | dtype `category` |
| total deep memory | `< 35%` of the original |

**Constraints:** `n = 10^5`. The memory guard measures AFTER the call —
materializing a full `float64` copy of the frame will fail the budget.

---

## 🥇 Gold — Streamed Mean Under a Memory Ceiling (~75 min)

**Task:** Implement `streamed_mean(csv_text, col, chunksize)` returning the
mean of a column from a CSV **string** without ever loading the whole file:
use `pd.read_csv(io.StringIO(csv_text), chunksize=...)` and accumulate
per-chunk `sum`/`count`. The mean must equal the full-frame mean exactly.

**Signature:**
```python
def streamed_mean(csv_text: str, col: str, chunksize: int) -> float:
```

| Input | Expected |
|---|---|
| 3-row CSV, `"y"`, chunksize 1 | same as `df["y"].mean()` |
| 1000-row CSV, `"y"`, chunksize 250 | same as full-frame mean |
| empty column | `nan` (0/0), no crash |

**Constraints:** 10^6-row CSV (~27 MB text). The tests run `tracemalloc`
around the call with a **130 MB peak ceiling** (measured: chunked read peaks
~109 MB, a full `pd.read_csv` materialization peaks ~141 MB) — a solution
that loads the whole file blows the ceiling; a chunked reader passes.

**Follow-up:** what breaks if you also need the **median**? (Answer: medians
do not stream — you must either keep all values, use an online quantile
estimator, or accept an approximation.)

---

## Running

```bash
pytest challenges/40-memory-optimization/test_challenge.py -v
```

## Test File Structure

```
challenges/40-memory-optimization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
