# Challenge 07: joins — INNER, LEFT, Self, Fan-out

## 🥉 Bronze — Inner Join Pairs (~20 min)

**Task:** Implement `inner_join_pairs(conn)` joining `users(id, name)`
and `posts(id, user_id, title)` and returning `(user_name, post_title)`
for every written post, sorted by user name then post title.

**Signature:**
```python
def inner_join_pairs(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- Explicit INNER JOIN syntax with ON
- Create both tables if missing
- Users with no posts must NOT appear

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| ana: 2 posts, bob: 0 posts | 2 rows; bob absent |

---

## 🥈 Silver — Left Join + Nulls (~35 min)

**Task:** Implement `left_join_with_nulls(conn)` returning every user
with their post count, plus `inactive_names`: users with no posts,
detected via `LEFT JOIN ... WHERE p.id IS NULL`.

**Signature:**
```python
def left_join_with_nulls(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- LEFT JOIN keeps all users; `WHERE p.id IS NULL` finds unmatched
- Return `{"counts": [(name, n)...], "inactive_names": [...]}` — counts
  sorted by name

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| ana: 2 posts, bob: 0 | `counts == [('ana', 2), ('bob', 0)]`, `inactive_names == ['bob']` |

---

## 🥇 Gold — Self-Join Report (~50 min)

**Task:** Implement `self_join_report(conn)` over `employees(id, name,
mgr_id)` producing `(employee, manager_or_'ROOT', report_depth)`
where depth 0 = root (no manager), 1 = direct report, 2 = second level,
using a self LEFT JOIN. Return also `distinct_teams`: for each manager,
the DISTINCT number of direct reports — must correct for fan-out.

**Signature:**
```python
def self_join_report(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Self-join with AS aliases (`e`, `m`)
- Depth: `CASE WHEN e.mgr_id IS NULL THEN 0 ELSE 1 END` for level 1;
  for level 2, use a second LEFT JOIN `mm`
- `distinct_teams`: `[(manager, COUNT(DISTINCT e.id))...]` sorted

**Constraints:** n ≤ 10⁴.

| Setup | Expected |
|-------|----------|
| ana(root), bob->ana, cam->ana, dave->bob | 4 report rows; `distinct_teams == [('ana', 2), ('bob', 1)]` |

**Follow-up:** Why COUNT(DISTINCT e.id) instead of COUNT(*)? (Answer:
the self-join fans out manager rows once per report; DISTINCT collapses
the duplicates.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/07-joins/test_challenge.py -v
```

## Test File Structure

```
challenges/07-joins/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
