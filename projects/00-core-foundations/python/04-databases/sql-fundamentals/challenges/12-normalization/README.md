# Challenge 12: normalization — 1NF, 3NF, Star Schema

## 🥉 Bronze — 1NF Split (~20 min)

**Task:** Implement `split_csv_column(conn)` that migrates a
`contacts(id, email, tags_csv)` table (tags like `'ml,db,sql'`) into a
normalized `contact_tags(contact_id, tag)` table with one row per tag
and returns the tag rows sorted.

**Signature:**
```python
def split_csv_column(conn: sqlite3.Connection) -> list[tuple]:
```

**Requirements:**
- Parse the CSV in SQL or Python — one atomic value per cell in the new
  table
- Create `contact_tags` if missing; insert one row per (contact, tag)
- Return `[(contact_id, tag)...]` sorted by contact_id, tag

**Constraints:** n ≤ 10⁴ rows.

| Setup | Expected |
|-------|----------|
| `(1, 'ml,db')`, `(2, 'sql')` | `[(1,'db'),(1,'ml'),(2,'sql')]` |

---

## 🥈 Silver — 3NF Split (~35 min)

**Task:** Implement `split_departments(conn)` on
`employees(id, name, dept_name, dept_location)`: create a normalized
`departments(dept_name PK, location)` and a `employees_normalized`
referencing it by name; return counts proving every location lives in
exactly one department row.

**Signature:**
```python
def split_departments(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Transitive dependency `dept_name -> dept_location` removed
- Insert distinct departments; foreign key from employees to departments
- Return `{"departments": n, "employees": n, "locations": [...]}`

**Constraints:** n ≤ 10⁴ rows.

| Setup | Expected |
|-------|----------|
| ana/eng/floor1, bob/eng/floor1, cam/ml/floor2 | `departments == 2`, `employees == 3`, `locations == ['floor1','floor2']` |

---

## 🥇 Gold — Star Schema Build (~50 min)

**Task:** Implement `build_star_schema(conn)` from a denormalized
`events_log(date TEXT, user TEXT, product TEXT, amount REAL)` into
`dim_date`, `dim_user`, `dim_product`, and `fact_sales(date_key,
user_key, product_key, amount)` with FKs. Return a join report
reconstructing the original rows plus the fact count.

**Signature:**
```python
def build_star_schema(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Four CREATE TABLEs; dimensions get surrogate integer keys
- INSERT INTO fact SELECT from dims via joins
- Return `{"facts": n, "dims": {"date": n, "user": n, "product": n},
  "reconstructed": [(date, user, product, amount)...]}`

**Constraints:** n ≤ 10⁴ log rows.

| Setup | Expected |
|-------|----------|
| 3 log rows, 2 distinct users | `facts == 3`, `dims.user == 2`, reconstructed equals the log |

**Follow-up:** Why surrogate keys in the fact table? (Answer: stable
engine-generated ids — the natural text values live in the dimensions
and can change without rewriting the facts.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/12-normalization/test_challenge.py -v
```

## Test File Structure

```
challenges/12-normalization/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
