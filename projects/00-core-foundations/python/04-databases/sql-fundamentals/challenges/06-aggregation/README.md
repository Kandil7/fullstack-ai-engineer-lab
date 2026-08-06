# Challenge 06: aggregation — GROUP BY, HAVING, Reports

## 🥉 Bronze — Group Totals (~20 min)

**Task:** Implement `group_totals(conn)` returning per-`model` rows:
`COUNT(*)` as `runs`, `SUM(metric)` as `total`, `AVG(metric)` as `avg`,
ordered by `avg` DESC.

**Signature:**
```python
def group_totals(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- Group in SQL; no Python aggregation
- Table `runs(id PK, model TEXT, metric REAL)` — create if missing
- Return `(model, runs, total, avg)` tuples

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| bert 0.9, bert 0.8, gpt 0.7 | `[('bert', 2, 1.7, 0.85), ('gpt', 1, 0.7, 0.7)]` |

---

## 🥈 Silver — HAVING Filter (~35 min)

**Task:** Implement `having_filter(conn, min_runs, min_avg)` returning
models with at least `min_runs` runs AND average metric at least
`min_avg` — the run count in HAVING, the average in HAVING too.

**Signature:**
```python
def having_filter(conn: sqlite3.Connection, min_runs: int, min_avg: float) -> list[tuple]:
```

**Requirements:**
- Both conditions after aggregation (HAVING), not in WHERE
- Return `(model, runs, avg)` sorted by avg DESC

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| bert 2 runs avg 0.85; gpt 3 runs avg 0.6 | `(2, 0.7)` | `[('bert', 2, 0.85)]` |

---

## 🥇 Gold — Two-Level Report (~50 min)

**Task:** Implement `aggregate_report(conn)` producing a per-model
report with `COUNT(DISTINCT experiment)`, `COUNT(*)`, `MAX(metric)`,
plus a global `WHERE` filter applied BEFORE grouping: only runs with
`metric >= 0.5` participate.

**Signature:**
```python
def aggregate_report(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- WHERE filters pre-group; HAVING (if used) filters post-group
- Return `{"rows": [(model, experiments, runs, best)...], "global_avg": float}`
- `global_avg` = AVG over ALL rows (filtered), one scalar subquery

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| bert exp1 0.9, bert exp1 0.1, bert exp2 0.8, gpt exp1 0.6 | `bert` counts 2 experiments, 2 runs (0.1 filtered out); `global_avg == 0.6` |

**Follow-up:** Why does the `0.1` row disappear from bert's run count
but still affect nothing in HAVING? (Answer: WHERE removes it before
grouping — GROUP BY never sees it.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/06-aggregation/test_challenge.py -v
```

## Test File Structure

```
challenges/06-aggregation/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
