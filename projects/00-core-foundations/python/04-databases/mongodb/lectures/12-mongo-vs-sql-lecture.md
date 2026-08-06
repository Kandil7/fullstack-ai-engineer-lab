# Databases — 12: MongoDB vs SQL (The Honest Tradeoff)

## Topic Overview

Every database decision is a tradeoff, and this module would be incomplete
without saying plainly: **most systems in this curriculum belong in a
relational store.** MongoDB wins specific workloads — flexible schemas and
"give me the whole document" reads — and loses others: joins, strict ACID
across documents, and heavy analytics.

This lecture compares the two families on the same domain, turns the
embedding-vs-referencing choice into decision rules, shows where MongoDB's
indexes and transactions actually sit, and gives you a framework for choosing
— including when the honest answer is "Postgres".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Model the same domain relationally and as embedded documents
2. Explain the read-cost difference: 1 document vs N lookups + joins
3. Apply embed-vs-reference decision rules (read-together, bounded, lifecycle)
4. Explain the N+1 read problem in referenced designs
5. Describe MongoDB's index types and the query-shaping cost
6. Explain single-document vs multi-document transaction semantics
7. List the workloads where MongoDB is the wrong tool
8. Recommend a database family from hard requirements

## Prerequisites

| Need | Where |
|---|---|
| Relational modeling and joins | `03-sql-fundamentals/` and `04-postgres/` |
| Documents, queries, aggregation | [01](01-getting-started-lecture.md) through [11](11-aggregation-lecture.md) |
| Index planning | `04-postgres/06-indexes` |

## 1. The Same Domain, Two Models

A blog post with an author and comments. Relational design **normalizes**:
three tables, joined at read time. Document design **embeds**: one document
holds the post, its author object, and its comments array.

```python
# relational: 3 lookups + 2 joins to render one post
relational = {
    "authors": [{"author_id": 1, "name": "sara"}],
    "posts": [{"post_id": 1, "title": "vector search", "author_id": 1}],
    "comments": [{"comment_id": 1, "post_id": 1, "text": "great read"}],
}

# document: 1 lookup returns the whole read shape
embedded = [{
    "_id": 1,
    "title": "vector search",
    "author": {"author_id": 1, "name": "sara"},
    "comments": [{"comment_id": 1, "text": "great read"}],
}]
```

The same answer, two very different read costs — and two very different write
costs when shared data changes.

## 2. Embedding vs Referencing — Decision Rules

Three questions decide it:

| Question | Embed | Reference |
|---|---|---|
| Always read with the parent? | yes | no (queried alone) |
| Bounded size? | yes | no (unbounded growth) |
| Independent lifecycle? | no (dies with parent) | yes (shared, updated alone) |

If all three favor embedding, embed. Otherwise reference. Two canonical
violations: **comments** are unbounded (reference them), and an **author** is
shared across a thousand posts (reference it — embedding means updating every
post when the author renames).

```python
def should_embed(*, read_together, bounded, independent_lifecycle):
    return read_together and bounded and not independent_lifecycle
```

## 3. The Cost of Referencing — N+1 Reads

A referenced design pays extra round trips: reading 50 posts "with author" is
1 query for the list plus 50 author lookups — **51 reads**. The embedded
design is 50 reads, one per document. At API latency per round trip, that
difference is the whole performance story.

```python
def read_count_referenced(n_posts):
    return n_posts + 1  # 1 for the list + 1 author lookup per post

def read_count_embedded(n_posts):
    return n_posts      # author already inside each document
```

The classic fix in SQL is a JOIN (one query); in MongoDB it is embedding — or
denormalizing the author name into each post and accepting update fan-out.

## 4. Schema Flexibility — and Its Cost

MongoDB collections accept documents with different fields. That is a feature
for ingestion — log lines, telemetry, varying AI metadata — and a liability
for application invariants: the database will not stop a document with
`"age": "not-a-number"`. SQL's `ALTER TABLE` and constraints are replaced by
`$jsonSchema` validators and application-layer checks. "No schema" really
means "the schema lives in your code, and it drifts".

## 5. Index Types

Indexes are how MongoDB avoids collection scans — exactly the SQL story:

| Index | Use |
|---|---|
| single-field `{"email": 1}` | equality on one field |
| compound `{"tenant": 1, "created_at": -1}` | multi-field filters |
| multikey | array fields (tags) |
| text | full-text search |
| hashed | shard keys |
| TTL | auto-expire after a timestamp |
| 2dsphere | geospatial |

The cost is shared with SQL too: every index slows writes and burns memory.
Indexes exist for the queries you run, not for decoration.

## 6. Transactions — the Document Boundary

MongoDB guarantees **atomicity per document** — a multi-field update to one
document is atomic. Multi-document transactions exist (replica sets, since
4.0) but are the exception: slower, retry-prone, and often a sign the model
is fighting the workload. If your invariant spans two collections, the
document model is telling you something. Relational databases give you ACID
across rows by default; MongoDB gives you it per document by default, across
documents by opt-in.

## 7. When NOT to Use MongoDB

| Workload | Right answer |
|---|---|
| order systems, ledger, anything ACID-across-rows | SQL |
| heavy joins or cross-entity queries | SQL |
| BI reporting, aggregations over big history | SQL (or a column store) |
| stable schema with migrations | SQL (DDL is a feature) |
| schemaless ingestion, read-whole-document | MongoDB |

The honest discussion: for most of the systems in this curriculum, Postgres is
the correct default and MongoDB is the specialty tool. Choosing MongoDB
because SQL is "boring" is a bug.

## Common Mistakes to Avoid

### Mistake 1: Embedding shared data
```
# WRONG — author lives in 1000 posts; renaming updates all of them
# CORRECT — reference shared data; embed only same-lifecycle children
```

### Mistake 2: Assuming cross-document ACID
```
# WRONG — two collections updated "at once" can split on a crash
# CORRECT — model per-document; use transactions only when unavoidable
```

### Mistake 3: No indexes on hot query fields
```
# WRONG — every find() is a collection scan under load
# CORRECT — index by the queries; compound for multi-field filters
```

### Mistake 4: "No schema" as an excuse to skip validation
```
# WRONG — bad data enters and every downstream query pays for it
# CORRECT — $jsonSchema validators + app-level invariants
```

### Mistake 5: MongoDB for a join-heavy OLTP system
```
# WRONG — 5 lookups per request where one JOIN would do
# CORRECT — SQL; reach for MongoDB when the read shape is a document
```

## Best Practices

1. Start from the read shape: "give me this whole document" points to MongoDB.
2. Embed children, reference shared parents — decide by lifecycle, not size alone.
3. Denormalize deliberately; document the update fan-out when you do.
4. Enforce schema at the boundary ($jsonSchema + app validation).
5. Index by query patterns; measure with `explain()` before and after.
6. Prefer single-document atomicity; multi-document transactions are the exception.
7. Count round trips: if a "simple" read needs N+1 lookups, re-model.
8. Keep audit/migration needs in mind — flexibility now is drift later.
9. Use SQL for joins, analytics, and cross-entity invariants; say it out loud.
10. Revisit the choice when the schema stabilizes — migration cost grows with time.

## Complexity and Cost

| Operation | SQL (normalized) | MongoDB (embedded) |
|---|---|---|
| Read one aggregate | JOIN across tables | 1 document read |
| Write shared data | 1 row update | update fan-out (denormalized) |
| Cross-entity invariant | transaction, by default | multi-doc transaction, opt-in |
| Schema change | `ALTER TABLE` + migration | no-op at DB; app drift |
| Analytics | mature SQL engines | aggregation framework, heavier |

The real cost is not queries — it is **which failures become possible**. SQL
fails loudly on constraint violations; MongoDB accepts the data and lets your
code fail later. Choose by which failure you can afford.

## AI Engineering Relevance

**Where this shows up:** AI applications mix both families — document stores
for flexible metadata and eval records, relational stores for users, billing,
and anything with invariants.

| Concept here | Used for |
|---|---|
| Flexible documents | ingestion of heterogeneous AI metadata (model, provider, params) |
| Embedding vs referencing | storing chunks alongside doc metadata vs linking to a relational core |
| Per-document atomicity | single-vector insert + metadata update in one document |
| TTL indexes | expiring stale eval records and feature caches |
| Honest tradeoff | Postgres + pgvector often beats Mongo + vector store for small systems |

**Scale note:** the phase's own vector-stores module demonstrates the pattern —
a document database stores the *metadata* around vectors, while the vector
index itself lives elsewhere. Knowing which store owns which truth is the
architecture skill; this lecture is where that habit starts.

## Practice Exercises

### Exercise 1: Model both ways (Difficulty: Easy)
Model a shopping order (customer, items, totals) relationally and as one
embedded document; count the reads each needs to render the order page.

### Exercise 2: Decision rules (Difficulty: Easy)
Classify five pairs (post+comments, author+posts, order+items, user+sessions,
product+reviews) as embed or reference, and justify each with the three rules.

### Exercise 3: N+1 measurement (Difficulty: Medium)
Given 200 posts each with a referenced author, compute total reads for
rendering all posts with author names; compare against the embedded design.

### Exercise 4: Index planning (Difficulty: Medium)
For `find({"tenant": "a", "status": "active"})` plus a sort by `created_at`,
choose the compound index and justify the field order.

### Exercise 5: Recommendation engine (Difficulty: Hard)
Given requirements (joins? ACID? flexible schema? analytics?), write
`recommend_db(...)` and defend it for five realistic workloads, including one
where MongoDB is wrong and one where it is right.

## Summary

| Concept | Description |
|---|---|
| Normalized vs embedded | 3 tables + joins vs 1 document |
| Embed rules | read-together, bounded, same lifecycle |
| N+1 | referencing costs extra reads per parent |
| Flexibility cost | invariants move into your code |
| Index types | single, compound, multikey, text, TTL, hashed |
| Transactions | atomic per document; multi-doc is opt-in |
| When not | joins, ACID-across-rows, analytics, stable schemas |

MongoDB is not "SQL but easier" — it is a different trade, and the honest
engineer picks by workload. This lecture is the capstone: after 11 topics of
documents, queries, and pipelines, you now know when *not* to use them.

## Quick Reference

| Decision | Idiom |
|---|---|
| Embed? | read-together AND bounded AND same lifecycle |
| Reference? | shared, queried alone, or unbounded |
| Read cost | embedded: 1 doc; referenced: 1 + N |
| Schema guard | `$jsonSchema` + app validation |
| Index | compound: filter fields then sort field |
| Transaction | per-document by default; multi-doc opt-in |
| Recommendation | joins/ACID/analytics -> SQL; flexible + whole-doc -> MongoDB |

## Next Steps

Next: **[Redis 01 — Introduction](../redis/01-introduction-lecture.md)** —
or continue into **[Vector Stores 01](../vector-stores/01-vector-search-fundamentals-lecture.md)** —
the database family built for embeddings.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
where these stores serve real endpoints.

Official docs: [mongodb.com/docs/manual/data-modeling/](https://www.mongodb.com/docs/manual/data-modeling/)
