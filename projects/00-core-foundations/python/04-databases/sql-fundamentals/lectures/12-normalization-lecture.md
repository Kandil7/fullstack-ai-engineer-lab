# SQL Fundamentals — 12: Normalization

## Topic Overview

Normalization is the discipline of deciding **where each fact lives**.
Unnormalized schemas duplicate facts until an update must touch many rows and
silently corrupts when it misses one. The normal forms are a vocabulary for
that discipline: 1NF (atomic cells), 2NF (no partial dependencies), 3NF (no
transitive dependencies). The goal is not perfect forms — it is knowing
exactly when the schema stores one fact in one place, and knowing how to
break that rule **deliberately** when reads demand it (star schemas, feature
stores, denormalized reporting copies).

The senior judgment this topic builds: normal forms tell you where the 
update anomalies are; denormalization tells you where they are worth paying
for throughput.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the update anomalies that normalization prevents.
2. Identify 1NF violations (non-atomic cells).
3. Identify 2NF violations (partial dependencies on composite keys).
4. Identify 3NF violations (transitive dependencies).
5. Normalize a schema to 3NF with one fact per table.
6. Reassemble normalized data with joins.
7. Decide when deliberate denormalization is correct.
8. Choose surrogate vs natural keys.

## Prerequisites

| Need | Where |
|---|---|
| Keys and relations | `01-relational-model-lecture.md` |
| Joins | `07-joins-lecture.md` |
| DDL | `02-ddl-schema-lecture.md` |

---

## 1. The unnormalized problems

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE orders_bad (
        order_id INTEGER PRIMARY KEY,
        customer TEXT, customer_city TEXT,
        items TEXT
    )
""")
conn.executemany("INSERT INTO orders_bad (order_id, customer, customer_city, items) VALUES (?, ?, ?, ?)",
                 [(1, "ada", "london", "gpu,cpu"), (2, "ada", "london", "ram"), (3, "bob", "paris", "gpu")])
```

```
# items holds a LIST -> not atomic (1NF violation)
# customer_city repeats per order -> transitive dependency (3NF violation)
```

Three symptom families follow: **update** (change ada's city: touch N rows),
**insert** (can't record an item without an order), **delete** (deleting the
order deletes the item).

## 2. 1NF — atomic cells

1NF requires each cell to hold one value. The comma-separated `items` column
breaks it; the fix is a child table with one row per (order, item) pair.

```python
conn.execute("""
    CREATE TABLE order_items (
        order_id INTEGER, item TEXT,
        PRIMARY KEY (order_id, item)
    )
""")
conn.executemany("INSERT INTO order_items (order_id, item) VALUES (?, ?)",
                 [(1, "gpu"), (1, "cpu"), (2, "ram"), (3, "gpu")])
print(conn.execute("SELECT DISTINCT order_id FROM order_items WHERE item = 'gpu'").fetchall())
```

```
[(1,), (3,)]
```

Now "which orders contain gpu" is a query, not a string parse.

## 3. 2NF — no partial dependencies

2NF applies to composite keys: every non-key column must depend on the *whole*
key. If `item_price` depends on `item` alone inside `(order_id, item)`, that is
a partial dependency — price repeats per order and updates fan out.

```python
conn.execute("CREATE TABLE items (item TEXT PRIMARY KEY, price INTEGER)")
conn.executemany("INSERT INTO items (item, price) VALUES (?, ?)",
                 [("gpu", 1000), ("cpu", 300), ("ram", 100)])
```

```
# price lives once in items; order_items references it
```

## 4. 3NF — no transitive dependencies

3NF: no non-key column depends on another non-key column. In `orders_bad`,
`customer_city` depends on `customer`, which is not the key — a transitive
dependency. The fix: customers table.

```python
conn.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
conn.executemany("INSERT INTO customers (id, name, city) VALUES (?, ?, ?)",
                 [(1, "ada", "london"), (2, "bob", "paris")])
conn.execute("CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER)")
```

```
# update ada's city once -> every order sees it (no fan-out)
```

## 5. The normalized query — joins reassemble views

```python
rows = conn.execute("""
    SELECT o.order_id, c.name, c.city
    FROM orders o JOIN customers c ON c.id = o.customer_id
    ORDER BY o.order_id
""").fetchall()
print(rows)
```

```
[(1, 'ada', 'london'), (2, 'ada', 'london'), (3, 'bob', 'paris')]
```

The same report the denormalized table produced directly — now from
single-fact tables. The price of normalization is the join; the reward is no
update anomalies.

## 6. When to denormalize — deliberately

- **Star schema**: a central fact table joined to dimension tables, designed
  for fast aggregation. Denormalization *is* the design.
- **Feature stores / caches**: duplicated data for latency, refreshed by an
  owning pipeline.
- **Read-heavy reporting**: a nightly denormalized copy replaces 10-way joins.

The rule: denormalize **deliberately**, with a named refresh owner and a
documented staleness policy — never as an accident of a lazy schema.

## 7. Surrogate vs natural keys

- **Natural key**: real-world value (email, ISBN) — meaningful, but mutable
  and often wide.
- **Surrogate key**: auto-increment or UUID — stable, small, meaningless.

```python
# surrogate PK
CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT UNIQUE)
```

The pattern: surrogate PK for joins, `UNIQUE` constraint on the natural key
for identity. Emails change; the join key should not.

## Common Mistakes to Avoid

### Mistake 1: Comma-separated lists in a column

```sql
-- WRONG - items = 'gpu,cpu' is not atomic
-- CORRECT - order_items (order_id, item) rows
```

### Mistake 2: Repeating customer data per order

```sql
-- WRONG - customer_city on every order; update fans out
-- CORRECT - customers table; orders reference the id
```

### Mistake 3: Over-normalizing hot read paths

```sql
-- WRONG - every dashboard query joins 10 tables
-- CORRECT - deliberate denormalization (star schema) with an owner
```

### Mistake 4: Natural keys as primary keys

```sql
-- WRONG - PRIMARY KEY (email): mutability and width problems
-- CORRECT - surrogate id + UNIQUE(email)
```

### Mistake 5: Denormalizing without an owner

```sql
-- WRONG - duplicated columns with nobody refreshing them
-- CORRECT - named pipeline, documented staleness, monitored freshness
```

## Best Practices

1. One fact per table — the core of normalization.
2. Child tables for multi-valued attributes (1NF).
3. Separate tables for facts that depend on part of a key (2NF).
4. Separate tables for facts depending on other facts (3NF).
5. Reassemble with joins; keep join keys indexed.
6. Denormalize deliberately for read-heavy paths with a refresh owner.
7. Surrogate PKs; unique constraints on natural keys.
8. Document the denormalization decision and its staleness.
9. Migrate in steps; test update anomalies before and after.
10. Know your engine's conventions (Postgres: identity columns).

## Complexity and Cost

| Design | Read cost | Write cost | Anomaly risk |
|---|---|---|---|
| Unnormalized | fast (no joins) | fast | high — updates fan out |
| 3NF | joins | minimal writes | none |
| Star schema | fast aggregations | ETL refresh | managed (dimensions) |
| Feature store | fast lookups | pipeline refresh | managed staleness |

Normalization trades read joins for write safety; denormalization trades write
safety for read speed. The decision is the tradeoff, made consciously.

## AI Engineering Relevance

**Where this shows up:** eval stores (predictions x models x datasets),
feature stores (entity-feature freshness), and metadata catalogs.

| Concept here | Used for |
|---|---|
| 3NF | eval facts stored once per (model, dataset) |
| Star schema | analytics cubes over prediction metrics |
| Surrogate keys | stable joins for entities that may rename |
| Denormalization | cached feature tables refreshed by pipelines |
| Update anomalies | avoiding corrupted eval aggregations |

**Scale note:** feature stores are the canonical AI denormalization — entity
features duplicated for lookup speed, with point-in-time correctness owned by
the pipeline. Normalization knowledge is what makes those designs safe instead
of accidental.

## Practice Exercises

### Exercise 1: Spot 1NF  (Difficulty: Easy)
Given a table with a list column, assert why it violates 1NF and produce the
atomic form.

### Exercise 2: Spot 2NF  (Difficulty: Easy)
Given a composite-key table with a column depending on part of the key, split
it and assert the price update affects one row.

### Exercise 3: Spot 3NF  (Difficulty: Medium)
Given a transitive dependency, normalize to 3NF and assert a city update
reflects in all orders.

### Exercise 4: Normalize to 3NF  (Difficulty: Medium)
Normalize a full orders/customers/items schema and assert the join report
matches the original denormalized one.

### Exercise 5: Star schema  (Difficulty: Hard)
Build a fact + dimensions design; assert aggregation speed/shape and explain
the deliberate denormalization.

### Exercise 6: Key choice  (Difficulty: Hard)
Design a table where the natural key mutates; assert the surrogate approach
survives the change while the natural-key PK breaks.

## Summary

| Concept | Description |
|---|---|
| 1NF | atomic cells; child tables for multi-values |
| 2NF | no partial dependencies on composite keys |
| 3NF | no transitive dependencies on non-keys |
| Joins | reassemble normalized views |
| Denormalization | deliberate for reads, with an owner |
| Surrogate keys | stable PKs + unique natural keys |

Normalization is schema hygiene: one fact in one place. Denormalization is
schema economics: paying for speed where the reads demand it. The skill is
knowing which you are doing at any moment.

## Quick Reference

| Task | Idiom |
|---|---|
| Atomic cells | child table `(parent_id, value)` |
| Kill partial dep | separate table per dependent fact |
| Kill transitive dep | table per non-key dependency |
| Reassemble | `JOIN` on surrogate keys |
| Denormalize | star schema / cached copy with refresh owner |
| Keys | surrogate PK + `UNIQUE` natural key |

## Next Steps

Next: **[13 — SQL Injection](13-sql-injection-lecture.md)** — the attack your schema
design must survive.

Continues in: **[04-databases — SQLAlchemy Models](../../04-databases/sqlalchemy/lectures/02-declarative-models-lecture.md)** — normalization expressed as ORM models.

Official docs: https://en.wikipedia.org/wiki/Database_normalization
