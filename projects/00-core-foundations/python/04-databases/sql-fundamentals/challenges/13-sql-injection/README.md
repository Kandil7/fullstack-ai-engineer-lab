# Challenge 13: sql-injection — Defensive Query Writing

## 🥉 Bronze — Parameterized Login (~20 min)

**Task:** Implement `safe_login(conn, username)` that fetches the user
row `(id, username, role)` with a parameterized query. A malicious
input like `"admin' OR '1'='1"` must return `None`.

**Signature:**
```python
def safe_login(conn: sqlite3.Connection, username: str) -> tuple | None:
```

**Requirements:**
- Use `?` placeholders — never string building
- Table `users(id PK, username TEXT UNIQUE, role TEXT)` — create if missing
- Return the tuple or `None`

**Constraints:** n ≤ 10³.

| Input | Expected |
|-------|----------|
| `"admin"` | `(1, 'admin', 'owner')` |
| `"admin' OR '1'='1"` | `None` |

---

## 🥈 Silver — Identifier Whitelist (~35 min)

**Task:** Implement `safe_sort(conn, column_name, ascending)` that sorts
`models(name, metric)` by a column chosen ONLY from the whitelist
`{"name": "name", "metric": "metric"}` — unknown names raise
`ValueError`.

**Signature:**
```python
def safe_sort(conn: sqlite3.Connection, column_name: str, ascending: bool) -> list[tuple]:
```

**Requirements:**
- Map the input through the whitelist; never concatenate it into SQL
- `ascending=True` -> ASC, else DESC
- Return `(name, metric)` rows

**Constraints:** n ≤ 10³.

| Input | Expected |
|-------|----------|
| `("metric", False)` | rows ordered metric DESC |
| `("metric; DROP TABLE models; --", False)` | `ValueError` raised |

---

## 🥇 Gold — Defense in Depth (~50 min)

**Task:** Implement `secure_search(conn, term, limit)` that searches
models by `name LIKE ?` (parameterized) with a validated integer limit
(1-100, else default 10) and returns `(name, metric)` rows, plus a
probe that proves stacked statements cannot execute.

**Signature:**
```python
def secure_search(conn: sqlite3.Connection, term: str, limit: int) -> dict:
```

**Requirements:**
- Term bound via `%`-pattern parameter: `name LIKE ?` with
  `f"%{term}%"` — the term itself stays a parameter
- Limit coerced to int; out-of-range -> 10
- Return `{"rows": [...], "probe_ok": bool}` where `probe_ok` is True
  when a stacked-statement attempt (`"x'; DELETE FROM models; --"`)
  does NOT delete rows

**Constraints:** n ≤ 10³.

| Input | Expected |
|-------|----------|
| `("bert", 5)` | matching rows |
| `("bert'; DELETE FROM models; --", 5)` | `probe_ok == True`, rows intact |

**Follow-up:** What does the `probe_ok` test actually prove? (Answer:
the driver refuses multi-statement strings — but rely on parameters,
never on that refusal as your only defense.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/13-sql-injection/test_challenge.py -v
```

## Test File Structure

```
challenges/13-sql-injection/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
