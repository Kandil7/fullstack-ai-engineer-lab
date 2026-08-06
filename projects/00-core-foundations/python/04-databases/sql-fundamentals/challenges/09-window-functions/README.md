# Challenge 09: window-functions — Rankings, Deltas, Frames

## 🥉 Bronze — Partitioned Ranks (~20 min)

**Task:** Implement `rank_rows(conn)` adding, per model, `ROW_NUMBER()`,
`RANK()`, and `DENSE_RANK()` over metric DESC to a `runs(model, metric)`
table.

**Signature:**
```python
def rank_rows(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- All three ranking functions in one query with `PARTITION BY model`
- Return `(model, metric, rn, rank, dense)` ordered by model, rn

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| bert: 0.9, 0.9, 0.8 | bert rows: `(0.9,1,1,1),(0.9,2,1,1),(0.8,3,3,2)` |

---

## 🥈 Silver — LAG Deltas (~35 min)

**Task:** Implement `lag_delta(conn)` returning for each run its
improvement over the previous run of the SAME model (metric -
LAG(metric)), with the first run's delta as NULL.

**Signature:**
```python
def lag_delta(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- `LAG(metric, 1) OVER (PARTITION BY model ORDER BY run_ts)` — the
  window ORDER BY uses a `run_ts` column
- Return `(model, run_ts, metric, delta)` ordered by model, run_ts

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| bert: 0.8 then 0.9; gpt: 0.7 | `(bert,2,0.9,0.1)`, `(gpt,...)` delta NULL |

---

## 🥇 Gold — Frames & Running Totals (~50 min)

**Task:** Implement `frames_report(conn)` computing per model:
`running_total` = SUM over `ROWS BETWEEN UNBOUNDED PRECEDING AND
CURRENT ROW`, and `moving_avg` = AVG over `ROWS BETWEEN 2 PRECEDING AND
CURRENT ROW` (3-run window), ordered by model, run_ts.

**Signature:**
```python
def frames_report(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- Both frame variants in one query
- Moving average uses fewer rows near the start of each partition
- Return `(model, run_ts, metric, running_total, moving_avg)` ordered
  by model, run_ts

**Constraints:** n ≤ 10⁴; ≤ 10 runs per model.

| Setup | Expected |
|-------|----------|
| bert: 1.0, 2.0, 3.0, 4.0 | running totals 1,3,6,10; moving avgs 1.0,1.5,2.0,3.0 |

**Follow-up:** Why does the 4th moving average use only 3 rows while the
1st uses 1? (Answer: the frame is bounded by the partition start — the
window can't reach before it.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/09-window-functions/test_challenge.py -v
```

## Test File Structure

```
challenges/09-window-functions/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
