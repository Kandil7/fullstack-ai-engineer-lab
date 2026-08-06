# SQL Fundamentals — 13: SQL Injection

## Topic Overview

SQL injection is what happens when untrusted text is merged into SQL text:
the input stops being a *value* and becomes *code*. Every endpoint that
builds queries with string interpolation (`f"..."`, `%s % ...`, `+`) is
exploitable, and the payload need not come from a browser — agent tool
arguments, imported CSV rows, and prompt-injected instructions are all
inputs. The fix is boring and absolute: **separate data from code**. Bind
values as parameters, whitelist identifiers, run with least privilege, and
never assume an ORM makes raw text safe.

The mental model: SQL injection and prompt injection are the same failure —
untrusted data interpreted as instructions. Learn the SQL version and you
already understand the shape of the AI one.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why string interpolation is never acceptable for SQL values.
2. Write and exploit the classic `' OR '1'='1' --` bypass to see the risk.
3. Parameterize values with `?` placeholders in every driver.
4. Handle identifiers (tables/columns) via whitelists, never binding.
5. Apply least privilege so a breach cannot escalate.
6. Identify where ORMs hide raw-text escape hatches.

## Prerequisites

| Need | Where |
|---|---|
| SELECT / WHERE | `02-select-where-lecture.md` |
| INSERT/UPDATE/DELETE | `03-insert-update-delete-lecture.md` |

---

## 1. The primitive — interpolation

```python
sql = f"SELECT * FROM users WHERE username = '{username}'"
conn.execute(sql).fetchall()
```

With `username = "ada"` this is a normal query. With
`username = "' OR '1'='1' --"` the assembled text is:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --'
```

`'1'='1'` is always true, so every row matches; `--` comments out the
trailing quote. One input, whole table leaked. There is no "safe" subset of
interpolation — this pattern is the vulnerability itself.

## 2. The fix — parameters

```python
sql = "SELECT * FROM users WHERE username = ?"
conn.execute(sql, (username,)).fetchall()
```

The statement and the values travel separately. The engine parses the
statement once, then *binds* values as data — a payload is stored or
compared literally, never executed. Every Python driver has this:
`?` (sqlite3, MySQL), `%s` (psycopg), `:name` (named), and query builders.

## 3. Values vs identifiers

`?` binds values only. Table and column names are identifiers — they change
how the statement is *parsed*, so no binding can make them safe. The correct
pattern is a **whitelist**:

```python
ALLOWED = {"id", "username", "role"}
if column not in ALLOWED:
    raise ValueError(f"column {column!r} not allowed")
```

Dynamic ORDER BY, dynamic table selection, and dynamic sort direction are
the classic identifier-injection spots. Whitelist or die.

## 4. Least privilege — defense in depth

A perfect query API is not enough if the connection can do damage. The app
database role should be able to do exactly what the feature does — typically
`SELECT/INSERT/UPDATE/DELETE` on specific tables, and **no `DROP`, no
`GRANT`, no `CREATE`**. Then even a successful injection (via a missed raw
text path, a second-order payload, or a compromised library) cannot escalate.
Defense in depth: parameters prevent the bug; least privilege caps the blast
radius when one slips through.

## 5. ORMs — helpful, not magical

```python
# Text-based escape hatches reintroduce the risk:
Model.objects.raw(f"... {user_input} ...")
session.execute(text(f"... {user_input} ..."))
```

ORMs protect you while you use their query builders. The moment you pass
strings into `raw()`, `text()`, `exec_driver_sql`, or interpolate into
`order_by`, you are back in section 1. Treat every raw-text API as a
security boundary that requires the same whitelist/parameter discipline.

## Common Mistakes to Avoid

### Mistake 1: f-string SQL, even for "internal" tools

```python
# WRONG - agent tool args are untrusted input
# CORRECT - bind every value; whitelist every identifier
```

### Mistake 2: Formatting with % before calling the driver

```python
# WRONG - sql % (user_input,) is exactly the vulnerability
# CORRECT - cursor.execute(sql, (user_input,))
```

### Mistake 3: Dynamic ORDER BY via interpolation

```python
# WRONG - f"... ORDER BY {column}"
# CORRECT - validate against a whitelist first
```

### Mistake 4: One admin connection for everything

```python
# WRONG - app connects as owner; a leak is a full compromise
# CORRECT - scoped roles; read-only connections for reads
```

### Mistake 5: Trusting the ORM because "we never write SQL"

```python
# WRONG - raw()/text() paths exist in every ORM
# CORRECT - treat raw SQL hooks as boundaries; audit them
```

## Best Practices

1. Parameterize every value — no exceptions, no "internal" carve-outs.
2. Never build SQL text from input; if you must, whitelist identifiers.
3. Connect with the least privilege the feature needs.
4. Keep raw-text ORM hooks out of the codebase or behind one audited helper.
5. Use read-only connections for read-only features.
6. Escape hatch rule: any function building SQL text must be reviewed as a
   security boundary.
7. Apply the same principle to prompt construction — it is the same class
   of bug in LLM systems.

## Complexity and Cost

| Concern | Cost | Cheaper alternative |
|---|---|---|
| Parameterization | none (one arg tuple) | — |
| Identifier whitelist | none (small set lookup) | — |
| Least-privilege setup | one-time schema/role work | — |
| Breach remediation | unbounded | prevent + scope |

Security here is effectively free at runtime; the cost is discipline, not
compute.

## AI Engineering Relevance

**Where this shows up:** agent tools that query databases, RAG audit logs,
data pipelines ingesting untrusted rows, and any LLM feature that turns
user text into SQL (text-to-SQL is a giant injection surface).

| Concept here | Used for |
|---|---|
| Data/code separation | prompt construction with untrusted text |
| Whitelisting | constraining agent tool arguments |
| Least privilege | scoping what a compromised agent can do |
| Parameterized queries | executing agent-generated SQL safely |

**Scale note:** a text-to-SQL agent that interpolates model output into SQL
is an injection-by-design system. The production pattern: constrain the
generator to a fixed tool contract, validate with a whitelist, and run on a
read-only, row-limited connection.

## Practice Exercises

### Exercise 1: Exploit it  (Difficulty: Easy)
Write the `' OR '1'='1' --` payload against an interpolated query; show every
row leaks. Assert the leak.

### Exercise 2: Fix it  (Difficulty: Easy)
Rewrite with parameters; assert the payload returns no rows.

### Exercise 3: Identifier whitelist  (Difficulty: Medium)
Implement dynamic ORDER BY with a whitelist; assert a malicious identifier
raises before touching the database.

### Exercise 4: Least privilege  (Difficulty: Medium)
Model two roles (app vs admin); show which statements the app role can run.
Assert the app role cannot drop tables.

### Exercise 5: ORM raw-text audit  (Difficulty: Hard)
Find the raw-text paths of your framework of choice (`text()`, `raw()`);
build a single audited wrapper that forbids interpolation and asserts it in
tests.

### Exercise 6: Second-order injection  (Difficulty: Hard)
A row is inserted containing a payload, then read back and interpolated into
a later query. Show the delayed exploit and fix it with parameters at the
second step. Assert both stages.

## Summary

| Concept | Description |
|---|---|
| Interpolation | merging input into SQL text = the vulnerability |
| Parameterization | binding values as data, never as code |
| Identifier binding | impossible to parameterize; use whitelists |
| Least privilege | capping blast radius if a bug slips through |
| ORM raws | escape hatches that need the same discipline |

Injection is not a database quirk — it is the general failure of treating
untrusted data as trusted grammar. SQL today, prompts tomorrow; the fix is
the same separation.

## Quick Reference

| Task | Idiom |
|---|---|
| Bind a value (sqlite/MySQL) | `execute(sql, (v,))` with `?` |
| Bind a value (Postgres) | `execute(sql, (v,))` with `%s` |
| Dynamic identifier | whitelist set + explicit check |
| Read-only connection | `sqlite3.connect('file:x?mode=ro', uri=True)` |
| Test the boundary | payloads as fixtures, `--verify` asserts |

## Next Steps

Next: **[14 — Query Optimization](14-query-optimization-lecture.md)** — plans,
indexes, and why `SELECT *` is an anti-pattern.

Continues in: **[04-databases — Postgres 07 Query Tuning](../../04-databases/postgres/lectures/07-query-tuning-lecture.md)** — EXPLAIN ANALYZE in a real engine.

Official docs: https://owasp.org/www-community/attacks/SQL_Injection
