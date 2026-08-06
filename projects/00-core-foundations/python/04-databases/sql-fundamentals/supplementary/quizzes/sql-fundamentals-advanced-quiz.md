# SQL Fundamentals — Advanced Quiz (Topics 10-14)

## Topic Overview

Indexes and query plans, transactions, normalization, SQL injection,
and query optimization — the topics that separate functional SQL from
production-grade SQL.

- **Difficulty:** 6 Easy, 9 Medium, 5 Hard
- **Questions:** 20
- **Time:** 30 minutes
- **Passing Score:** 16/20 (80%)

---

## Questions

### Question 1 [Easy] — What does EXPLAIN QUERY PLAN reveal?

A. The query's runtime in milliseconds
B. The engine's execution strategy (SCAN vs SEARCH vs sort)
C. The table's row count
D. The query's syntax errors

**Correct Answer:** B

**Explanation:** EXPLAIN QUERY PLAN shows the chosen strategy — full
scans, index lookups, and sorts. It is not a timer (A), a statistics
report (C), or an error linter (D).

---

### Question 2 [Easy] — A predicate is sargable when...

A. The column appears bare and the value is wrapped
B. The column is wrapped in a function
C. It uses SELECT *
D. It contains a subquery

**Correct Answer:** A

**Explanation:** Sargability means the indexed column is untouched:
`ts >= ?` uses the index; `DATE(ts) = ?` scans. B kills the index; C
and D are unrelated to predicate shape.

---

### Question 3 [Easy] — Which ACID property makes a transfer all-or-
nothing?

A. Atomicity
B. Consistency
C. Isolation
D. Durability

**Correct Answer:** A

**Explanation:** Atomicity guarantees the transaction commits wholly or
not at all — a failed transfer leaves no partial writes. B guards
constraints, C guards concurrency, D guards persistence.

---

### Question 4 [Easy] — What is the 1NF requirement?

A. Every table has a primary key
B. Every cell holds one atomic value; no repeating groups
C. No transitive dependencies
D. All columns are indexed

**Correct Answer:** B

**Explanation:** 1NF forbids CSV-in-a-cell and repeating groups. C is
3NF; A is good practice but not 1NF; D is a performance choice.

---

### Question 5 [Easy] — The #1 defense against SQL injection is:

A. Escaping quotes manually
B. Parameterized queries
C. Shorter table names
D. Stored procedures only

**Correct Answer:** B

**Explanation:** Parameter binding makes values data — they can never
become syntax. Manual escaping is error-prone (A); C is irrelevant; D
helps but does not remove the need for parameters.

---

### Question 6 [Easy] — Keyset pagination is:

A. `LIMIT n OFFSET m`
B. `WHERE id > last_id ORDER BY id LIMIT n`
C. `SELECT * FROM t`
D. `ORDER BY RANDOM()`

**Correct Answer:** B

**Explanation:** Keyset pagination jumps via the primary-key cursor:
O(log n) per page and stable under concurrent writes. A is OFFSET
pagination (O(m) per page); C and D are not pagination at all.

---

### Question 7 [Medium] — Code Output: plan strings

```sql
EXPLAIN QUERY PLAN SELECT * FROM events WHERE ts >= 2500;   -- plan 1
EXPLAIN QUERY PLAN SELECT * FROM events WHERE ts / 1000 >= 2; -- plan 2
```

With an index on ts, what are the plans?

A. SCAN / SCAN
B. SEARCH (index) / SCAN
C. SEARCH / SEARCH
D. SCAN / SEARCH

**Correct Answer:** B

**Explanation:** `ts >= 2500` is sargable — SEARCH. `ts / 1000 >= 2`
wraps the column — the index cannot help, full SCAN. The other
combinations misread one of the two predicates.

---

### Question 8 [Medium] — Composite index `(model, latency, created_at)`:
which column order rule applies?

A. Any order works equally
B. Equality columns first, then range, then sort
C. Sort columns first
D. The widest column first

**Correct Answer:** B

**Explanation:** The index serves `WHERE model = ? AND latency > ?
ORDER BY created_at` only in the equality-then-range-then-sort order.
Other orders break the left-prefix usage. A, C, D are wrong heuristics.

---

### Question 9 [Medium] — A covering index...

A. Stores the whole table twice
B. Holds every column the query needs, so the table is never read
C. Wraps every predicate in a function
D. Is only usable for writes

**Correct Answer:** B

**Explanation:** A covering index contains all projected/filtered
columns — the plan says "USING COVERING INDEX" and the table file is
never touched. A is a misconception; C and D are false.

---

### Question 10 [Medium] — Which dependency violates 3NF?

A. Primary key -> any column
B. Non-key column -> another non-key column
C. Primary key -> non-key column
D. Foreign key -> primary key

**Correct Answer:** B

**Explanation:** A transitive dependency (a -> b -> c with non-key c
depending on non-key b) breaks 3NF. A and C are the normal, allowed
dependencies; D is how relations are wired.

---

### Question 11 [Medium] — Code Output: injection attempt

```python
name = "x' OR '1'='1"
rows = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
```

What happens?

A. Every user row is returned
B. Zero rows are returned — the value is treated as data
C. A syntax error is raised
D. The users table is dropped

**Correct Answer:** B

**Explanation:** The parameter is bound as a value; the quote and OR are
literal characters, matching no username. A is the f-string version;
C and D describe unparameterized behavior that sqlite3's execute()
also blocks.

---

### Question 12 [Medium] — What does ROLLBACK do?

A. Saves the current transaction
B. Discards all changes since BEGIN
C. Commits the transaction
D. Deletes the table

**Correct Answer:** B

**Explanation:** ROLLBACK undoes everything since the transaction
started — the "none" half of all-or-nothing. A is COMMIT; C is the
opposite; D confuses transaction control with DDL.

---

### Question 13 [Medium] — What is a savepoint for?

A. Creating a second database
B. Marking a rollback point so only later work can be undone
C. Indexing a transaction
D. Caching query plans

**Correct Answer:** B

**Explanation:** SAVEPOINT marks a position; ROLLBACK TO it undoes only
the work after the marker, keeping earlier work — partial recovery
inside one transaction. The other options are invented roles.

---

### Question 14 [Medium] — Code Output: N+1 query count

A naive loop over 5 parents runs one child query per parent. How many
queries total (including the parent query)?

A. 5
B. 6
C. 10
D. 1

**Correct Answer:** B

**Explanation:** 1 parent query + 5 child queries = 6 — the N+1
problem. A forgets the parent query; C doubles the children; D is the
batched ideal.

---

### Question 15 [Medium] — In a star schema, the fact table holds...

A. Descriptive attributes only
B. Foreign keys to dimensions plus numeric measures
C. Fully normalized dimensions
D. The query cache

**Correct Answer:** B

**Explanation:** Facts are the measured center: FK keys into the
dimensions plus the metrics. A describes dimensions; C describes a
snowflake; D is unrelated.

---

### Question 16 [Hard] — Code Output: leading wildcard

```sql
EXPLAIN QUERY PLAN SELECT * FROM events WHERE name LIKE '%bert';
```

With an index on name, what is the plan?

A. SEARCH USING INDEX name
B. SCAN events
C. SEARCH USING COVERING INDEX
D. USE TEMP B-TREE FOR ORDER BY

**Correct Answer:** B

**Explanation:** A leading wildcard means the match must inspect every
value — the B-tree cannot skip ahead, so the planner SCANs. A and C
assume the index helps; D is a sort artifact, not relevant here.

---

### Question 17 [Hard] — Why is `NOT IN` dangerous with NULLs?

A. It scans the index twice
B. A NULL in the list makes every comparison UNKNOWN — nothing matches
C. It ignores the primary key
D. It disables caching

**Correct Answer:** B

**Explanation:** `x NOT IN (1, NULL)` reduces to NOT (FALSE OR UNKNOWN)
= NOT UNKNOWN = UNKNOWN — the row is dropped. Prefer NOT EXISTS or
LEFT JOIN + IS NULL. A, C, D are false mechanics.

---

### Question 18 [Hard] — Code Output: keyset vs OFFSET plans

```sql
EXPLAIN QUERY PLAN SELECT id FROM t WHERE id > 100 ORDER BY id LIMIT 3;  -- plan 1
EXPLAIN QUERY PLAN SELECT id FROM t ORDER BY id LIMIT 3 OFFSET 100;      -- plan 2
```

What are the plans (t has a primary key on id)?

A. SEARCH rowid / SCAN
B. SCAN / SCAN
C. SEARCH / SEARCH
D. SCAN / SEARCH

**Correct Answer:** A

**Explanation:** Keyset jumps into the B-tree via the primary key
(SEARCH rowid); OFFSET must walk past 100 rows first (SCAN). The other
combinations misread the two techniques.

---

### Question 19 [Hard] — Defense in depth for dynamic ORDER BY input
means:

A. Escaping the input with quotes
B. Mapping input through a whitelist of known column names
C. Using executescript() and hoping
D. Truncating input to 10 characters

**Correct Answer:** B

**Explanation:** Identifiers cannot be parameterized — the only safe
route is a closed whitelist (`{"created": "created_at"}[input]`),
rejecting anything else. A does not help identifiers; C is actively
dangerous; D is security theater.

---

### Question 20 [Hard] — Code Output: batch chunking

Batching 10 parent ids with `batch_size = 3` using IN queries. How
many queries run?

A. 10
B. 4
C. 3
D. 1

**Correct Answer:** B

**Explanation:** ceil(10 / 3) = 4 chunked IN queries — bounded round
trips vs 11 for naive N+1 or 1 if the limit allowed a single list. A
is the per-parent count; C floors; D assumes no chunking needed.

---

## Answer Key

| Q | Difficulty | Answer | Distractor Analysis |
|---|---|---|---|
| 1 | Easy | B | Plans, not timers or stats |
| 2 | Easy | A | Bare column, wrapped value |
| 3 | Easy | A | Atomicity = all-or-nothing |
| 4 | Easy | B | 1NF = atomic cells |
| 5 | Easy | B | Parameters beat escaping |
| 6 | Easy | B | Cursor-based pagination |
| 7 | Medium | B | Sargable SEARCHes; wrapped SCANs |
| 8 | Medium | B | equality -> range -> sort |
| 9 | Medium | B | Covering = table never read |
| 10 | Medium | B | Transitive dependency breaks 3NF |
| 11 | Medium | B | Parameters keep input as data |
| 12 | Medium | B | Rollback undoes since BEGIN |
| 13 | Medium | B | Partial rollback marker |
| 14 | Medium | B | 1 + N = 6 queries |
| 15 | Medium | B | Facts: FKs + measures |
| 16 | Hard | B | Leading wildcard forces SCAN |
| 17 | Hard | B | NULL in NOT IN list = empty result |
| 18 | Hard | A | Keyset SEARCHes rowid; OFFSET SCANs |
| 19 | Hard | B | Whitelist identifiers |
| 20 | Hard | B | ceil(10 / 3) = 4 chunks |

## Scoring Guide

| Score | Verdict |
|---|---|
| 18-20 | SQL fundamentals complete — move to Postgres topics |
| 16-17 | Review plans and optimization (questions 7-9, 16-20) |
| Below 16 | Re-read topics 10-14 lectures, then retake |
