# Challenge 01: relational-model — Tables, Keys & NULL

## 🥉 Bronze — Relational Schema Builder (~20 min)

**Task:** Implement `create_relational_schema(conn)` that builds a
students/courses/enrollments schema: `students(id PK, name NOT NULL)`,
`courses(id PK, title UNIQUE)`, and `enrollments(student_id, course_id)`
as a junction table with a composite PK and FKs to both parents.

**Signature:**
```python
def create_relational_schema(conn: sqlite3.Connection) -> list[str]:
```

**Requirements:**
- Return the sorted list of table names
- Composite primary key on `enrollments(student_id, course_id)`
- Foreign keys on both junction columns
- Turn on `PRAGMA foreign_keys` at the start

**Constraints:** n ≤ 10³. Any correct approach passes.

| Table | Expectation |
|-------|-------------|
| `students` | PK `id`, `name` NOT NULL |
| `courses` | PK `id`, UNIQUE `title` |
| `enrollments` | PK `(student_id, course_id)`, FKs to both |

---

## 🥈 Silver — Key Enforcement (~30 min)

**Task:** Implement `enforce_keys(conn)` that inserts sample rows and
returns a summary proving the keys work: how many rows landed, whether
duplicate enrollment was rejected, whether an orphan enrollment was
rejected.

**Signature:**
```python
def enforce_keys(conn: sqlite3.Connection) -> dict:
```

**Requirements:**
- Insert 2 students, 2 courses, one valid enrollment
- Try inserting the same enrollment twice -> must be rejected
- Try inserting an enrollment with `student_id = 999` -> must be rejected
- Return `{"rows": n, "dup_rejected": bool, "orphan_rejected": bool}`

**Constraints:** n ≤ 10³. Must use `PRAGMA foreign_keys = ON`.

| Scenario | Expected |
|----------|----------|
| Valid data | `rows == 5`, both flags `True` |
| Missing tables | Function raises no exception; still returns a dict |

---

## 🥇 Gold — NULL-Aware Cleanup (~45 min)

**Task:** Implement `purge_abandoned_courses(conn)` that deletes courses
no student is enrolled in, then returns the remaining course titles
sorted. A course with NULL or zero enrollments counts as abandoned.

**Signature:**
```python
def purge_abandoned_courses(conn: sqlite3.Connection) -> list[str]:
```

**Requirements:**
- Use a `NOT EXISTS` anti-join (or LEFT JOIN + IS NULL)
- Never use `NOT IN` with the enrollments subquery — a NULL course_id
  there would match nothing (three-valued logic trap)
- Return sorted remaining titles

**Constraints:** n ≤ 10³. One query per phase.

| Setup | Expected |
|-------|----------|
| Courses `c1`(enrolled), `c2`(no enrollments), `c3`(NULL row) | Returns `['c1']`; `c2`, `c3` deleted |

**Follow-up:** Why is `NOT IN (SELECT course_id FROM enrollments)` unsafe
here? (Answer: if any `course_id` is NULL, NOT IN matches no rows — the
classic three-valued-logic footgun.)

---

## Running

```bash
python -m pytest 04-databases/sql-fundamentals/challenges/01-relational-model/test_challenge.py -v
```

## Test File Structure

```
challenges/01-relational-model/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
