# Challenge 06: Larger Than Memory

## 🥉 Bronze — Streaming Count (~15 min)

**Task:** Count the rows of a CSV with the streaming engine and return
the count plus whether streaming was requested.

**Signature:**
```python
def streaming_count(path: str) -> dict[str, object]:
```

**Requirements:**
- `pl.scan_csv(path).select(pl.len()).collect(engine="streaming")`
- Return `{"rows": int, "streaming": bool}` (the bool = True, hard-coded
  after the call — this is a self-documenting contract, not a lie)

| Input | Expected |
|-------|----------|
| CSV with 100k rows | `rows == 100000`, `streaming is True` |

**Constraints:** file <= 10^7 rows. Never call `read_csv`.

---

## 🥈 Silver — Chunked Aggregate (~35 min)

**Task:** Aggregate across parquet shards without loading them all at
once: total rows and the mean of one column.

**Signature:**
```python
def chunked_stats(dir_path: str, column: str) -> dict[str, float]:
```

**Requirements:**
- `pl.scan_parquet(dir_path).select(pl.len(), pl.col(column).mean())`
  collected with `engine="streaming"`
- Return `{"rows": float, "mean": float}`

| Input (4 shards × 50k) | Expected |
|-------|----------|
| any seeded shards | `rows == 200000`, mean ≈ 0.5 |

**Constraints:** 2 <= shards <= 16. Only a single scan of the directory
(no per-file loops).

---

## 🥇 Gold — Sink Join Pipeline (~75 min)

**Task:** Join two sharded parquet directories lazily and sink the
result to parquet, proving you never held the full result in memory.

**Signature:**
```python
def sink_join(left_dir: str, right_dir: str, left_key: str, right_key: str, out_path: str) -> int:
```

**Requirements:**
- Left: `id, metric` (2 cols); right: `id, category` (2 cols)
- Lazy join on the keys, then `sink_parquet(out_path, engine="streaming")`
- Return the row count of the written file (`pl.scan_parquet(out_path).collect(engine="streaming").height`)

| Input | Expected |
|-------|----------|
| left 4 shards × 50k, right 50k | row count == 200k |

**Constraints:** keys are unique across each side (1:1 join). The join +
sink must be lazy end-to-end: no `collect()` before the sink.
**Follow-up:** why does sink need `engine="streaming"`? (Answer: without
it the result is collected to RAM before writing — the exact thing the
pattern avoids.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/06-larger-than-memory/test_challenge.py -v
```

## Test File Structure

```
challenges/06-larger-than-memory/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
