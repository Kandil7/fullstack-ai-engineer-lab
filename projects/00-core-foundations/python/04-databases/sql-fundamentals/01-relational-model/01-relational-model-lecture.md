# SQL Fundamentals — 01: The Relational Model

## Topic Overview

The relational model is the foundation of almost every database you will
touch in production: Postgres, MySQL, SQL Server, and the SQL interfaces
of data warehouses. It was proposed by E. F. Codd in 1970 and its core
bet is simple: represent data as **tables** (relations), manipulate whole
sets of rows with a declarative language (SQL), and let the engine worry
about *how* to find the rows.

SQL is **set-oriented**: you describe *what* you want, not *how* to get
it. That is a genuinely different way of thinking from Python's
row-by-row loops, and it is the single biggest mental shift in this
module. This lecture covers the vocabulary (tables, rows, columns, keys,
relations), the NULL semantics that silently corrupt metrics, and the
bag-vs-set distinction behind `DISTINCT`.

For AI engineers the model matters twice: once because feature stores,
training-data tables, and evaluation result tables are all relational
structures; and again because NULL handling bugs — `WHERE score = NULL`
matching nothing — are a top cause of "the dashboard is empty" and
"accuracy dropped to zero" incidents.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Describe a table as a set of rows with a fixed column structure
2. Explain why a PRIMARY KEY is mandatory for joinable, deduplicatable data
3. Use FOREIGN KEYs to express 1:1, 1:N, and N:M relations
4. Predict the result of any comparison involving NULL (three-valued logic)
5. Write `IS NULL` / `IS NOT NULL` correctly and explain why `= NULL` never matches
6. Distinguish bag semantics (default SELECT) from set semantics (DISTINCT)
7. Recognize when row order is guaranteed (only with ORDER BY)
8. Explain how the relational model maps to feature-store tables

## Prerequisites

| Need | Where |
|---|---|
| Python `sqlite3` basics (connect, execute, fetchall) | `04-databases/mysql/01-getting-started.py` (or any quickstart) |
| Tuple unpacking and list comprehensions | `01-core-python` basics |

---

## 1. Tables, Rows, and Columns

A **table** is a named collection of **rows**, each with the same
**columns**. Think of it as a spreadsheet where every row is one record
and every column is one attribute. The relational model is *typed*: each
column has a declared type, and the engine enforces it.

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (1, "alice", 30))
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (2, "bob", 25))

rows = conn.execute("SELECT id, name, age FROM users").fetchall()
print(rows)
print(f"row count: {len(rows)}, columns per row: {len(rows[0])}")
```

```
[(1, 'alice', 30), (2, 'bob', 25)]
row count: 2, columns per row: 3
```

**Order is not guaranteed** without `ORDER BY`. The engine is free to
return rows in any order — often insertion order for small tables, but
index order, parallel order, or anything else on bigger ones. Code that
depends on "the order it comes back" is code that breaks in production.

## 2. Primary Keys and Uniqueness

The PRIMARY KEY uniquely identifies a row. It gives you three things for
free: **uniqueness** (the engine rejects duplicates), **identity** (a
stable way to reference the row), and **an index** (fast lookups, topic
10).

```python
try:
    conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (1, "evil", 99))
except sqlite3.IntegrityError as exc:
    print(f"duplicate PK rejected: {exc}")
```

```
duplicate PK rejected: UNIQUE constraint failed: users.id
```

Never build a table without a primary key. Without one you cannot
reliably join (which row do we attach the prediction to?), cannot
deduplicate (are these two rows the same record?), and cannot upsert
(topic 03) safely.

## 3. Foreign Keys and Relations

A FOREIGN KEY column references another table's primary key. It
expresses the **relation** between tables and lets the engine enforce
referential integrity: no orphan references.

- **1:1** — one row on each side (user ↔ profile)
- **1:N** — one parent, many children (user → posts)
- **N:M** — many to many, always through a **junction table** (posts ↔ tags)

```python
conn.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id), title TEXT)")
conn.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (1, "hello world"))

try:
    conn.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (999, "orphan"))
except sqlite3.IntegrityError as exc:
    print(f"orphan FK rejected: {exc}")

post_rows = conn.execute(
    "SELECT p.title FROM posts p JOIN users u ON p.user_id = u.id WHERE u.name = ?",
    ("alice",),
).fetchall()
print(f"alice's posts: {post_rows}")
```

```
orphan FK rejected: FOREIGN KEY constraint failed
alice's posts: [('hello world',)]
```

**sqlite caveat:** foreign keys are OFF by default. You must run
`PRAGMA foreign_keys = ON` on *every connection*, before any DML. In
Postgres and MySQL they are on by default. Always write code that
assumes FKs are enforced.

## 4. NULL Semantics — NULL is not a value

NULL means **unknown / missing** — not zero, not an empty string, not
"false". The killer rule: any comparison with NULL yields NULL (UNKNOWN),
which is falsy in a WHERE clause. Therefore `x = NULL` never matches —
not even `NULL = NULL`.

```python
print(f"NULL = NULL:  {conn.execute('SELECT NULL = NULL').fetchone()[0]}")
print(f"NULL IS NULL: {conn.execute('SELECT NULL IS NULL').fetchone()[0]}")
print(f"1 = NULL:     {conn.execute('SELECT 1 = NULL').fetchone()[0]}")
print(f"NULL OR TRUE: {conn.execute('SELECT NULL OR TRUE').fetchone()[0]}")
```

```
NULL = NULL:  None
NULL IS NULL: 1
1 = NULL:     None
NULL OR TRUE: 1
```

`NULL OR TRUE` is TRUE because TRUE wins in three-valued logic. This
matters in compound filters: one NULL in the wrong place silently drops
rows. The only correct tests are `IS NULL` and `IS NOT NULL`.

```python
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, NULL)", (5, "erin"))
print(conn.execute("SELECT name FROM users WHERE age = ?", (None,)).fetchall())
print(conn.execute("SELECT name FROM users WHERE age IS NULL").fetchall())
```

```
[]
[('erin',)]
```

## 5. Set Thinking — bags vs sets

SELECT returns a **bag** (multiset): duplicates survive. `DISTINCT`
converts the bag into a **set** by collapsing duplicates across the
whole projected row. Thinking "which rows satisfy this predicate?" rather
than "for each row, do..." is the SQL mindset.

```python
conn.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (6, "alice", 30))
names = conn.execute("SELECT name FROM users").fetchall()
print([n[0] for n in names])
names = conn.execute("SELECT DISTINCT name FROM users").fetchall()
print([n[0] for n in names])
```

```
['alice', 'bob', 'erin', 'alice']
['alice', 'bob', 'erin']
```

## Common Mistakes to Avoid

### Mistake 1: Comparing to NULL with `=`

```python
# WRONG - matches nothing, silently, no error
#   WHERE age = NULL
# CORRECT - NULLs are only found with IS NULL
#   WHERE age IS NULL
#   WHERE age IS NOT NULL
```

### Mistake 2: Assuming SELECT order is meaningful

```python
# WRONG - order is whatever the engine feels like
#   SELECT name FROM users
# CORRECT - order only exists with ORDER BY
#   SELECT name FROM users ORDER BY id ASC
```

### Mistake 3: Skipping the primary key

```python
# WRONG - no identity: cannot join, dedupe, or upsert
#   CREATE TABLE log (msg TEXT)
# CORRECT
#   CREATE TABLE log (id INTEGER PRIMARY KEY, msg TEXT)
```

### Mistake 4: Forgetting FKs are off in sqlite

```python
# WRONG - FK silently does nothing
#   conn.execute("CREATE TABLE child (pid REFERENCES parent(id))")
# CORRECT - before ANY DML on EVERY connection
#   conn.execute("PRAGMA foreign_keys = ON")
```

### Mistake 5: Treating NULL as a value in application code

```python
# WRONG - None == None is True in Python, NULL = NULL is UNKNOWN in SQL
#   if user.age is None: ...   # fine in Python
#   WHERE age = NULL           # broken in SQL
```

## Best Practices

1. Give every table a surrogate INTEGER PRIMARY KEY (topic 12).
2. Enable `PRAGMA foreign_keys = ON` on every sqlite connection.
3. Always add `ORDER BY` when the consumer cares about row order.
4. Use `IS NULL` / `IS NOT NULL` exclusively for NULL tests.
5. Parameterize every query — values are data, never code (topic 13).
6. Use junction tables for every N:M relation.
7. Choose FK actions (`ON DELETE CASCADE` / `SET NULL`) deliberately.
8. `SELECT DISTINCT` only when you need the set — it costs a sort/hash.
9. Model "unknown" as NULL, not as 0 or `''` — they mean different things.
10. Write queries as whole-set descriptions, not row-by-row loops.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Equality lookup on PK | O(log n) | O(1) | B-tree index (automatic for PK) |
| Full table scan (no index) | O(n) | O(1) | index the filtered column |
| `DISTINCT` | O(n log n) sort or O(n) hash | O(n) | skip it when duplicates are fine |
| N:M resolution via junction | O(log n) per hop | O(1) | — (this is the point) |

## AI Engineering Relevance

**Where this shows up:** feature stores, training-data tables,
evaluation-result tables, vector-store metadata.

| Concept here | Used for |
|---|---|
| PRIMARY KEY | one row per entity/embedding — the key for upserts |
| FK + relations | linking predictions to ground truth, runs to metrics |
| NULL semantics | "abstained" predictions, missing features, sparse labels |
| Set thinking | deduplicating training rows, cohort membership queries |

**Scale note:** at 1M rows, a missing primary key or a NULL-comparison
bug costs hours of debugging and corrupted aggregates. At 100M rows the
NULL semantics decide whether your feature-join produces 99M or 60M rows
— silently.

## Practice Exercises

### Exercise 1: Build the vocabulary  (Difficulty: Easy)

Create a `users` table with an INTEGER PRIMARY KEY, insert three users,
and fetch them back. Confirm `len(row)` per row equals the column count.

### Exercise 2: NULL probe  (Difficulty: Easy)

Insert a row with `age = NULL`. Write queries that prove `age = NULL`
matches nothing while `age IS NULL` matches it. Try `NULL OR FALSE` and
`NULL AND FALSE` and record the results.

### Exercise 3: Relation types  (Difficulty: Medium)

Create `users`, `posts`, and a `post_tags` junction with `tags`. Insert
one user, two posts, two tags. Write the query that returns each post
with its tags. Which relation type does each table express?

### Exercise 4: Bag vs set  (Difficulty: Medium)

Insert a duplicate name into users. Show that plain SELECT returns it
twice and `SELECT DISTINCT` returns it once. Then explain what
`SELECT DISTINCT name, age` deduplicates on.

### Exercise 5: FK enforcement probe  (Difficulty: Medium)

With `PRAGMA foreign_keys = ON`, attempt to insert a post whose
`user_id` does not exist. Verify the IntegrityError. Then repeat with
the pragma OFF and observe the difference — the orphan is accepted.

### Exercise 6: NULL in evaluation data  (Difficulty: Hard)

Design a `predictions` table where `confidence` may be NULL (model
abstained). Write the query that counts abstained predictions, and
explain why `COUNT(confidence)` differs from `COUNT(*)`.

## Summary

| Concept | Description |
|---|---|
| Table | a set of rows with a fixed column structure |
| Primary key | enforced unique identity for every row |
| Foreign key | enforced reference expressing a relation |
| NULL | UNKNOWN — never equal to anything, found only with IS NULL |
| Bag vs set | default SELECT keeps duplicates; DISTINCT removes them |
| Order | never guaranteed without ORDER BY |

The relational model gives you structure (types, keys), integrity
(FKs), and a set-oriented language. Three rules carry the whole module:
keys are non-negotiable, NULL is never a value, and row order is never
free. Everything after this lecture — joins, aggregation, transactions,
optimization — builds on these three.

## Quick Reference

| Task | Idiom |
|---|---|
| Find NULLs | `WHERE col IS NULL` |
| Reject NULLs | `WHERE col IS NOT NULL` |
| Deduplicate rows | `SELECT DISTINCT col FROM t` |
| Enforce FK (sqlite) | `PRAGMA foreign_keys = ON` (per connection) |
| Express N:M | junction table with composite PK |

## Next Steps

Next: **[02 — DDL and Schema](02-ddl-schema-lecture.md)** — how to define
the tables, types, and constraints you just learned to read.

Continues in: **[Phase 9 — ML/MLOps](../../../09-ml-mlops/README.md)** —
feature stores and training-data pipelines are relational-model thinking
at production scale.

Official docs: https://www.sqlite.org/lang_table.html ,
https://www.sqlite.org/nulls.html
