# Challenge 01: Core vs ORM — Bulk Metrics Loader

## 🥉 Bronze — Bulk Insert (~15 min)

**Task:** Implement `bulk_insert_metrics(conn, rows)` which bulk-loads metric rows
through the Core layer and returns how many rows were written.

**Signature:**
```python
def bulk_insert_metrics(conn, rows: list[dict]) -> int:
```

**Requirements:**
- Use `metrics_table.insert()` with an executemany-style parameter list
- Return the number of rows inserted
- Do NOT commit (the caller owns the transaction)

| Input | Expected |
|---|---|
| `[{"model": "bert", "metric": "f1", "value": 89}]` | `1` |
| `[]` | `0` |

**Constraints:** n ≤ 10⁵ rows. Any correct approach passes.

---

## 🥈 Silver — Threshold Query (~35 min)

**Task:** Implement `query_above(conn, threshold)` which returns rows whose value
is strictly above a threshold, ordered by value descending.

**Signature:**
```python
def query_above(conn, threshold: float) -> list[tuple[int, str, float]]:
```

**Requirements:**
- Use `text()` with a `:threshold` bound parameter — never f-string values
- Return `(id, metric, value)` tuples

| Input | Expected |
|---|---|
| threshold `90` over rows `[(1,'f1',89),(2,'acc',95)]` | `[(2,'acc',95)]` |

**Constraints:** n ≤ 10⁶ rows — the query must run in the database, not in Python.

---

## 🥇 Gold — Table-Bounded Loader (~75 min)

**Task:** Implement `safe_upsert_metrics(conn, rows, batch_size)` which inserts
metrics in bounded batches of `batch_size` rows each, so a 1M-row load never
materializes a giant single statement. Return total rows written.

**Signature:**
```python
def safe_upsert_metrics(conn, rows: list[dict], batch_size: int = 500) -> int:
```

**Requirements:**
- Insert in chunks of `batch_size`; every chunk committed
- Must be single-pass over `rows` (no full copies)
- Handle `rows` larger than `batch_size` correctly

| Input | Expected |
|---|---|
| 10 rows, batch_size 3 | `10` |

**Constraints:** 10⁷ rows, memory ≤ 50 MB. Must be single-pass.

**Follow-up:** what breaks first at 10⁹ rows? (Answer: the parameter list itself —
sqlite has a ~999-parameter default limit per statement; real loaders chunk.)

---

## Running

```bash
pytest challenges/01-core-vs-orm/test_challenge.py -v
```

## Test File Structure

```
challenges/01-core-vs-orm/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
