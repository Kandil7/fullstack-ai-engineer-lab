# SQL Fundamentals — Queries Quiz (Topics 01-08)

## Topic Overview

Covers the relational model, DDL/DML, SELECT basics, advanced
filtering, aggregation, joins, and subqueries/CTEs. All questions run
against SQLite semantics.

- **Difficulty:** 6 Easy, 9 Medium, 5 Hard
- **Questions:** 20
- **Time:** 25 minutes
- **Passing Score:** 16/20 (80%)

---

## Questions

### Question 1 [Easy] — Which construct uniquely identifies a row?

A. A UNIQUE constraint
B. A primary key
C. A foreign key
D. A CHECK constraint

**Correct Answer:** B

**Explanation:** The primary key uniquely identifies each row (UNIQUE +
NOT NULL semantics plus an automatic index). A UNIQUE constraint
prevents duplicates but allows NULLs and does not carry the "identity"
role. A foreign key references other rows; a CHECK is a row-level rule.

---

### Question 2 [Easy] — Code Output: duplicates in SELECT

```sql
CREATE TABLE t (v TEXT);
INSERT INTO t (v) VALUES ('a');
INSERT INTO t (v) VALUES ('a');
SELECT v FROM t;
```

What does the SELECT return?

A. One row `('a')` — duplicates are removed automatically
B. Two rows `('a', 'a')`
C. Zero rows — duplicates cause an IntegrityError
D. `('a',)` plus a warning

**Correct Answer:** B

**Explanation:** A plain SELECT returns a **bag** (multiset) —
duplicates survive. Only `SELECT DISTINCT` converts the result to a
set. Options A, C, and D are distractors: no dedup happens, no error is
raised, and the driver never warns about duplicates.

---

### Question 3 [Easy] — Code Output: NULL comparison

```sql
SELECT NULL = NULL;
```

What is the result?

A. `1` (true)
B. `0` (false)
C. `NULL` (unknown)
D. An error

**Correct Answer:** C

**Explanation:** In three-valued logic, any comparison with NULL yields
UNKNOWN — NULL is not equal to anything, not even to itself. That is
why NULL is tested with `IS NULL`, never `= NULL`. A and B assume
two-valued logic; D confuses NULL semantics with a syntax error.

---

### Question 4 [Easy] — Which is the only correct NULL test?

A. `col = NULL`
B. `col <> NULL`
C. `col IS NULL`
D. `col == NULL`

**Correct Answer:** C

**Explanation:** `IS NULL` / `IS NOT NULL` are the only correct tests.
Both `= NULL` and `<> NULL` evaluate to UNKNOWN, so WHERE drops every
row. D is Python syntax, not SQL at all.

---

### Question 5 [Easy] — Default ORDER BY direction?

A. Ascending
B. Descending
C. Undefined
D. Depends on the column type

**Correct Answer:** A

**Explanation:** ORDER BY defaults to ASC; DESC must be written
explicitly. C is wrong — the order is well defined; D is wrong — the
direction never depends on the type.

---

### Question 6 [Easy] — Code Output: COUNT variants

```sql
CREATE TABLE u (tag TEXT);
INSERT INTO u (tag) VALUES (NULL), ('a'), ('a');
SELECT COUNT(*), COUNT(tag), COUNT(DISTINCT tag) FROM u;
```

What is the result?

A. `(3, 3, 1)`
B. `(3, 2, 1)`
C. `(2, 2, 2)`
D. `(3, 2, 2)`

**Correct Answer:** B

**Explanation:** `COUNT(*)` counts rows including NULLs (3).
`COUNT(tag)` counts non-NULL values (2). `COUNT(DISTINCT tag)` counts
distinct non-NULL values (1). A counts the NULL in COUNT(tag); C and D
miscount DISTINCT or the NULL.

---

### Question 7 [Medium] — Code Output: GROUP BY + HAVING

```sql
CREATE TABLE sales (region TEXT, amt REAL);
INSERT INTO sales VALUES ('east', 10), ('east', 5), ('west', 30);
SELECT region, COUNT(*) AS n FROM sales GROUP BY region HAVING COUNT(*) >= 2;
```

What is returned?

A. `[('east', 2), ('west', 1)]`
B. `[('east', 2)]`
C. `[('east', 5), ('west', 30)]`
D. `[('east', 2), ('west', 2)]`

**Correct Answer:** B

**Explanation:** HAVING filters **groups** after aggregation — only
'east' has 2+ rows. A shows the pre-filter group list; C shows raw
values instead of counts; D invents a west count of 2.

---

### Question 8 [Medium] — WHERE vs HAVING: which statement is true?

A. Both filter rows before grouping
B. WHERE filters rows before grouping; HAVING filters groups after
C. HAVING can reference any column of the base table
D. WHERE can reference aggregate results

**Correct Answer:** B

**Explanation:** WHERE removes rows pre-group (less work for the
engine); HAVING filters post-aggregation and may reference aggregates.
C is wrong — HAVING references groups; D is wrong — WHERE cannot see
aggregate results.

---

### Question 9 [Medium] — Code Output: LEFT JOIN padding

```sql
CREATE TABLE a (id INT, v TEXT);
CREATE TABLE b (aid INT, w TEXT);
INSERT INTO a VALUES (1, 'x'), (2, 'y');
INSERT INTO b VALUES (1, 'p');
SELECT a.v, b.w FROM a LEFT JOIN b ON a.id = b.aid;
```

What is returned?

A. `[('x', 'p')]`
B. `[('x', 'p'), ('y', None)]`
C. `[('x', 'p'), ('y', '')]`
D. `[('x', 'p'), ('y', 'y')]`

**Correct Answer:** B

**Explanation:** LEFT JOIN keeps all left rows; the unmatched right
side is padded with NULL — never an empty string. A is an INNER JOIN
result; C confuses NULL with ''; D is nonsense.

---

### Question 10 [Medium] — What does a junction table do?

A. Adds a CHECK constraint between two tables
B. Expresses an N:M relation with two foreign keys
C. Stores default values for joins
D. Replaces primary keys in large databases

**Correct Answer:** B

**Explanation:** An N:M relation always passes through a junction table
holding both foreign keys (often as a composite primary key). A, C, and
D describe constraints, defaults, and an invented role.

---

### Question 11 [Medium] — Code Output: LIKE patterns

```sql
SELECT name FROM models WHERE name LIKE 'bert%';
```

Given names `bert`, `bert_v2`, `gpt`, what is returned?

A. `['bert', 'bert_v2']`
B. `['bert']`
C. `['bert_v2']`
D. `['bert', 'bert_v2', 'gpt']`

**Correct Answer:** A

**Explanation:** `%` matches any run of characters (including none), so
'bert' and 'bert_v2' both match; 'gpt' does not. B and C drop a valid
match; D includes a non-matching name.

---

### Question 12 [Medium] — Code Output: OFFSET pagination

```sql
SELECT id FROM t ORDER BY id LIMIT 2 OFFSET 1;
```

Given ids 1-4, what is returned?

A. `[1, 2]`
B. `[2, 3]`
C. `[1, 3]`
D. `[3, 4]`

**Correct Answer:** B

**Explanation:** OFFSET 1 skips the first row, LIMIT 2 takes the next
two: ids 2 and 3. A is the no-OFFSET result; C jumps rows; D is OFFSET
2.

---

### Question 13 [Medium] — Upsert: what does `excluded` refer to?

```sql
INSERT INTO m (name, epoch) VALUES (?, ?)
ON CONFLICT(name) DO UPDATE SET epoch = excluded.epoch;
```

A. The row that was rejected before the conflict
B. The values that were about to be inserted
C. Rows excluded by the WHERE clause
D. The old row's values

**Correct Answer:** B

**Explanation:** `excluded` is SQLite's alias for the would-be inserted
row — the new values win. A and D confuse it with the existing row; C
is unrelated to upserts.

---

### Question 14 [Medium] — Code Output: NOT EXISTS anti-join

```sql
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

Given ana (1 order), bob (0 orders), what is returned?

A. `['ana']`
B. `['bob']`
C. `['ana', 'bob']`
D. `[]`

**Correct Answer:** B

**Explanation:** NOT EXISTS is true when the subquery finds nothing —
only customers WITHOUT orders survive. A returns customers WITH orders;
C returns everyone; D inverts the logic.

---

### Question 15 [Medium] — Composite index: what does the engine
enforce on `PRIMARY KEY (a, b)`?

A. Only `a` must be unique
B. The pair `(a, b)` must be unique
C. Both `a` and `b` must each be unique
D. Nothing — composite keys are advisory

**Correct Answer:** B

**Explanation:** The composite key guarantees the **combination** is
unique; each column may repeat. C demands per-column uniqueness, which
is stronger; A and D misstate the guarantee.

---

### Question 16 [Hard] — Code Output: three-valued logic

```sql
SELECT COUNT(*) FROM t
WHERE (col = 1 OR col = 2) AND col IS NOT NULL;
```

Given values `1, 2, 3, NULL`, what is the count?

A. 4
B. 3
C. 2
D. 0

**Correct Answer:** C

**Explanation:** Only 1 and 2 satisfy `col = 1 OR col = 2`; NULL fails
both comparisons (UNKNOWN) and 3 fails the OR — the AND with
`IS NOT NULL` adds nothing for the non-NULL rows. A counts the NULL
too; B counts 1, 2, 3; D ignores the OR entirely.

---

### Question 17 [Hard] — Code Output: correlated subquery cost

```sql
SELECT name FROM products p
WHERE price > (SELECT AVG(price) FROM products);
```

How many times does the subquery execute?

A. Once — it is uncorrelated and hoisted
B. Once per product row
C. Never — the query fails
D. Twice — once per aggregate

**Correct Answer:** A

**Explanation:** The subquery does not reference the outer row, so it
is uncorrelated and evaluated once. Correlated subqueries (B) re-run
per outer row. C and D are false.

---

### Question 18 [Hard] — Code Output: LEFT JOIN + COUNT

```sql
SELECT u.name, COUNT(p.id) FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id;
```

Given ana with 2 posts, bob with 0, what is returned?

A. `[('ana', 2), ('bob', 0)]`
B. `[('ana', 2)]`
C. `[('ana', 2), ('bob', 1)]`
D. `[('ana', 3)]`

**Correct Answer:** A

**Explanation:** The LEFT JOIN produces `('bob', NULL)`; `COUNT(p.id)`
skips NULLs, so bob's count is 0. B drops bob (INNER JOIN behavior);
C counts the NULL as 1 (`COUNT(*)` behavior); D double-counts.

---

### Question 19 [Hard] — Code Output: recursive CTE

```sql
WITH RECURSIVE cnt(x) AS (
  SELECT 1
  UNION ALL
  SELECT x + 1 FROM cnt WHERE x < 3
)
SELECT x FROM cnt;
```

What is returned?

A. `[1, 2, 3]`
B. `[1, 2]`
C. `[3, 2, 1]`
D. `[1, 2, 3, 4]`

**Correct Answer:** A

**Explanation:** Seed 1; recursion adds 2, then 3; the guard `x < 3`
stops before 4. B stops too early; C reverses; D misses the
termination guard.

---

### Question 20 [Hard] — Why does `NOT IN (SELECT id FROM t)` match
nothing when `t.id` contains a NULL?

A. NULL ids are filtered by DISTINCT
B. `x NOT IN (1, NULL)` is UNKNOWN for every x — WHERE drops UNKNOWN
C. NOT IN cannot read NULLs from an index
D. SQLite disables NOT IN with NULLs as a safety feature

**Correct Answer:** B

**Explanation:** `NOT IN` is `NOT (x = v1 OR x = v2 OR ...)`; comparing
x with NULL yields UNKNOWN, making the whole OR UNKNOWN-or-TRUE, never
FALSE — so no row passes. This is the classic reason to prefer
NOT EXISTS or LEFT JOIN + IS NULL. A, C, D are invented mechanics.

---

## Answer Key

| Q | Difficulty | Answer | Distractor Analysis |
|---|---|---|---|
| 1 | Easy | B | UNIQUE allows NULLs; FK/CHECK serve other roles |
| 2 | Easy | B | SELECT returns a bag; no dedup, no error |
| 3 | Easy | C | NULL = NULL is UNKNOWN, not TRUE/FALSE |
| 4 | Easy | C | = and <> with NULL are always UNKNOWN |
| 5 | Easy | A | ASC is the default; DESC explicit |
| 6 | Easy | B | COUNT(*) counts rows; COUNT(col) skips NULLs |
| 7 | Medium | B | HAVING filters groups; east is the only 2-row group |
| 8 | Medium | B | WHERE pre-group; HAVING post-group |
| 9 | Medium | B | LEFT pads with NULL, never '' |
| 10 | Medium | B | Junction = two FKs for N:M |
| 11 | Medium | A | % matches zero or more characters |
| 12 | Medium | B | OFFSET skips, LIMIT takes |
| 13 | Medium | B | excluded = would-be inserted values |
| 14 | Medium | B | NOT EXISTS finds rows WITHOUT matches |
| 15 | Medium | B | Composite uniqueness is per-pair |
| 16 | Hard | C | NULL comparisons are UNKNOWN; OR/AND per Kleene tables |
| 17 | Hard | A | Uncorrelated subqueries run once |
| 18 | Hard | A | COUNT(col) skips the NULL-padded row |
| 19 | Hard | A | Seed + UNION ALL + guard |
| 20 | Hard | B | NOT IN + NULL list = empty result |

## Scoring Guide

| Score | Verdict |
|---|---|
| 18-20 | Ready for the advanced quiz |
| 16-17 | Review questions 7-15 |
| Below 16 | Re-read topics 01-08 lectures, then retake |
