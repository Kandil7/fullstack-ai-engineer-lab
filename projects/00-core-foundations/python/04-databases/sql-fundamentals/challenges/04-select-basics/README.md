# Challenge 04: select-basics — Projection & Ordering

## 🥉 Bronze — Top-N Leaders (~20 min)

**Task:** Implement `top_n(conn, n)` that returns the `n` models with the
highest `metric`, ordered by metric DESC then name ASC, as `(name, metric)`.

**Signature:**
```python
def top_n(conn: sqlite3.Connection, n: int) -> list[tuple]:
```

**Requirements:**
- Table `models(id PK, name TEXT, epoch INT, metric REAL)` — create if missing
- Tie-break deterministically by name ASC
- Use LIMIT, never Python-side sorting

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| bert 0.9, gpt 0.8, llm 0.7 | `n=2` | `[('bert', 0.9), ('gpt', 0.8)]` |
| Same metrics | `n=1` | lexicographically first name |

---

## 🥈 Silver — Aliased Report (~35 min)

**Task:** Implement `metric_report(conn)` returning, for each distinct
model name, a computed `score = metric * 100` with alias `score`, sorted
by score DESC. Also return the total number of DISTINCT names.

**Signature:**
```python
def metric_report(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Use `AS` aliases; expression in the select list
- DISTINCT applied to names
- Return `{"report": [(name, score)...], "distinct_names": n}`

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| bert 0.9 twice, gpt 0.8 | `report` has 2 rows; `distinct_names == 2` |

---

## 🥇 Gold — Paginator (~45 min)

**Task:** Implement `paginate(conn, page_size, page)` that returns page
`page` (1-indexed) of models ordered by `(metric DESC, name ASC)` using
`LIMIT ? OFFSET ?`, plus the total row count and whether a next page
exists.

**Signature:**
```python
def paginate(conn: sqlite3.Connection, page_size: int, page: int) -> dict:
```

**Requirements:**
- Return `{"rows": [...], "total": n, "has_next": bool}`
- `page=0` or negative -> treat as 1
- OFFSET computed as `(page - 1) * page_size`

**Constraints:** n ≤ 10⁴.

| Setup | Input | Expected |
|-------|-------|----------|
| 5 rows, page_size 2 | `page=3` | 1 row; `has_next == False` |
| 5 rows, page_size 2 | `page=1` | first 2 rows; `has_next == True` |

**Follow-up:** When would keyset pagination beat OFFSET here? (Answer:
deep pages re-read all skipped rows — topic 14 swaps OFFSET for
`WHERE id > last` cursors.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/04-select-basics/test_challenge.py -v
```

## Test File Structure

```
challenges/04-select-basics/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
