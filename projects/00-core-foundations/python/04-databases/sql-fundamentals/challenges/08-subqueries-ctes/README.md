# Challenge 08: subqueries-ctes — Scalar, Anti-Join, Recursion

## 🥉 Bronze — Scalar Subquery (~20 min)

**Task:** Implement `scalar_report(conn)` returning each customer with
their total spend, plus a global `avg_spend` column computed once by a
scalar subquery in the select list.

**Signature:**
```python
def scalar_report(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- One scalar subquery for the global average — no Python computation
- Tables: `customers(id, name)`, `orders(customer_id, amount)` — create if missing
- Return `{"rows": [(name, spend)...], "avg_spend": float}`

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| ana 10+20, bob 30 | `rows == [('bob',30),('ana',30)]` (order by spend DESC), `avg_spend == 20` |

---

## 🥈 Silver — NOT EXISTS Anti-Join (~35 min)

**Task:** Implement `anti_join(conn)` returning customers with NO
orders, using `NOT EXISTS`, and the same result using `LEFT JOIN +
IS NULL`, verifying both produce identical lists.

**Signature:**
```python
def anti_join(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Both methods must agree (NULL-safe)
- Return `{"not_exists": [...], "left_join": [...], "identical": bool}`

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| ana 1 order, bob 0, cam 0 | both lists `['bob','cam']`, `identical == True` |

---

## 🥇 Gold — Recursive Date Spine (~50 min)

**Task:** Implement `recursive_spine(conn, start, end)` that generates
every calendar day between two ISO dates (inclusive) with
`WITH RECURSIVE`, then joins a `events(date TEXT)` table to produce a
zero-filled daily count — days without events show 0.

**Signature:**
```python
def recursive_spine(conn: sqlite3.Connection, start: str, end: str) -> list[tuple]:
```

**Requirements:**
- Recursive CTE: seed = `start`; recursive term = `date(d, '+1 day')`
  with `WHERE d < end` for termination
- Left join events; `COALESCE(COUNT(...), 0)`
- Return `(day, count)` ascending

**Constraints:** span ≤ 400 days (keeps recursion bounded).

| Setup | Input | Expected |
|-------|-------|----------|
| events on 2026-08-01, 2026-08-03 | `('2026-08-01','2026-08-03')` | `[('2026-08-01',1),('2026-08-02',0),('2026-08-03',1)]` |

**Follow-up:** What happens without the `WHERE d < end` guard?
(Answer: infinite recursion — the CTE never terminates.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/08-subqueries-ctes/test_challenge.py -v
```

## Test File Structure

```
challenges/08-subqueries-ctes/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
