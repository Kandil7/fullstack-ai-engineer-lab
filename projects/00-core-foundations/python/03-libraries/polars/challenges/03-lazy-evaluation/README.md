# Challenge 03: Polars Lazy Evaluation

## 🥉 Bronze — Count Without Loading (~15 min)

**Task:** Count the rows of a CSV file without ever materializing its
data into RAM.

**Signature:**
```python
def lazy_count(path: str) -> int:
```

**Requirements:**
- Use `pl.scan_csv` (never `read_csv`)
- Count via `select(pl.len())`, executed with the streaming engine
- Return a plain `int`

| Input | Expected |
|-------|----------|
| CSV with 1,000 rows + header | `1000` |

**Constraints:** file <= 10^5 rows. Must be lazy end-to-end.

---

## 🥈 Silver — Prove the Pushdown (~35 min)

**Task:** Return whether a filter on a lazy parquet scan is pushed into
the scan itself (visible as `SELECTION` in the optimized plan).

**Signature:**
```python
def predicate_pushed(path: str, column: str, value: str) -> bool:
```

**Requirements:**
- Build `pl.scan_parquet(path).filter(pl.col(column) == value)`
- Inspect `explain(optimized=True)`; return `"SELECTION" in plan`
- Never print the raw plan

| Input | Expected |
|-------|----------|
| parquet with a `split` column, filter `split == "valid"` | `True` |

**Constraints:** must call `explain`, not `collect`.

---

## 🥇 Gold — Pushdown Report (~75 min)

**Task:** Execute a lazy filter + projection and report *which columns
the scan actually read*, proving projection pushdown.

**Signature:**
```python
def project_and_filter(path: str, keep: list[str], column: str, value: str) -> tuple[pl.DataFrame, int]:
```

**Requirements:**
- Scan the parquet file, filter `column == value`, keep only `keep` columns
- Return `(result_frame, columns_read)` where `columns_read` is parsed
  from the plan line `PROJECT n/m COLUMNS`
- The result must contain only the kept columns and matching rows

| Input (4-column file) | Expected |
|-------|----------|
| `keep=["score"]`, filter on `split` | `columns_read == 1` |

**Constraints:** file has 4 columns, n <= 10^6 rows. Must be lazy
end-to-end (single `collect(engine="streaming")`).
**Follow-up:** why would `columns_read` be larger than `len(keep)`?
(Answer: the filter predicate needs the `column` it filters on, so that
column is also read even if it is not kept.)

---

## Running

```bash
python -m pytest 03-libraries/polars/challenges/03-lazy-evaluation/test_challenge.py -v
```

## Test File Structure

```
challenges/03-lazy-evaluation/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
