# MongoDB vs SQL — Glossary 12

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| $jsonSchema | Schema | MongoDB validator enforcing field types and required fields |
| 2dsphere | Index | geospatial index for location queries |
| Compound index | Index | index over multiple fields, ordered for filters + sort |
| Document atomicity | Transaction | guarantee that a single document's update is all-or-nothing |
| Embedding (data) | Modeling | storing child data inside the parent document |
| Hash tag / hashed index | Index | index supporting only equality, used for shard keys |
| Index | Performance | structure that avoids a collection scan for a query |
| Multikey index | Index | index on an array field, one entry per element |
| N+1 reads | Modeling | one read per parent plus one per child lookup |
| Normalization | Modeling | splitting data into tables/collections by entity |
| Referencing | Modeling | storing an id link to shared data instead of copying it |
| Relational model | Modeling | tables, rows, keys, and joins with schema enforced |
| Single-field index | Index | index on one field for equality lookups |
| Text index | Index | full-text search over string fields |
| Transaction (multi-doc) | Consistency | opt-in all-or-nothing across several documents |
| TTL index | Index | index that auto-deletes documents after expiry |
| Update fan-out | Modeling | cost of updating copies when shared data changes |

## Detailed Definitions

### $jsonSchema
**Definition**: A MongoDB schema validator that declares required fields and
their BSON types; writes failing validation are rejected.
**Example**:
```python
validator = {
    "required": ["name", "email"],
    "properties": {
        "name": {"bsonType": "string"},
        "email": {"bsonType": "string"},
    },
}
```
```text
# real MongoDB: db.createCollection("users", {"validator": validator})
```
**Complexity**: O(1) per write (validation only).
**Related**: Single-field index, Schema flexibility

### 2dsphere
**Definition**: A geospatial index type that lets queries find documents by
location proximity, `$near` and `$geoWithin`.
**Example**:
```python
# real MongoDB: db.places.createIndex({"location": "2dsphere"})
# query: db.places.find({"location": {"$near": {"$geometry": point}}})
```
```text
# the index is what makes "nearest 10" fast instead of a full scan
```
**Complexity**: O(log n) lookups on the geo index.
**Related**: Index, Multikey index

### Compound index
**Definition**: An index over multiple fields that serves filters on several
fields and can satisfy a sort without a separate step.
**Example**:
```python
# equality fields first, sort field last:
# {"tenant_id": 1, "status": 1, "created_at": -1}
# serves find({"tenant_id": "a", "status": "active"}).sort({"created_at": -1})
```
```text
# field order decides whether the sort is index-backed or a mem sort
```
**Complexity**: O(log n) lookup, extra write cost per insert/update.
**Related**: Index, Single-field index

### Document atomicity
**Definition**: The guarantee that every operation on a single document is
atomic — it either fully applies or not at all, regardless of crashes.
**Example**:
```python
# one $inc + $set + $push on the same document is all-or-nothing
update_one(users, {"_id": 1},
           {"$inc": {"age": 1}, "$push": {"scores": 100}})
```
```text
# across two documents this is NOT atomic by default
```
**Complexity**: O(1) — the document is the transaction unit.
**Related**: Transaction (multi-doc), Embedding (data)

### Embedding (data)
**Definition**: Storing child data (comments, items) inside the parent
document so one read returns the whole aggregate.
**Example**:
```python
post = {
    "_id": 1,
    "title": "vector search",
    "author": {"name": "sara"},
    "comments": [{"text": "great read"}],
}
```
```text
# one lookup returns the full read shape
```
**Complexity**: O(1) read for the aggregate; write cost grows with embedding.
**Related**: Referencing, N+1 reads, Update fan-out

### Hashed index
**Definition**: An index that hashes the field value, supporting only
equality; commonly used for shard keys to spread data evenly.
**Example**:
```python
# real MongoDB: db.coll.createIndex({"user_id": "hashed"})
# supports find({"user_id": 42}) but not ranges
```
```text
# equality-only: no ranges, no sorting via this index
```
**Complexity**: O(1) hash lookup.
**Related**: Index, Single-field index

### Index
**Definition**: A structure that maps field values to documents so queries
avoid scanning the whole collection.
**Example**:
```python
def build_index(collection, field):
    idx = {}
    for doc in collection:
        if field in doc:
            idx.setdefault(doc[field], []).append(doc)
    return idx

email_index = build_index([{"_id": 1, "email": "a@x.com"}], "email")
print(email_index["a@x.com"][0]["_id"])  # -> 1
```
```text
# O(1) lookup instead of a scan; real MongoDB uses B-trees
```
**Complexity**: O(log n) lookup; O(log n) write overhead.
**Related**: Single-field index, Compound index, TTL index

### Multikey index
**Definition**: An index on an array field where each array element gets an
index entry, enabling queries like "document whose tags contain x".
**Example**:
```python
# real MongoDB: db.posts.createIndex({"tags": 1})
# query: db.posts.find({"tags": "ai"})  # matches any element
```
```text
# one document can match via several of its own elements
```
**Complexity**: O(k log n) where k = array length.
**Related**: Index, 2dsphere

### N+1 reads
**Definition**: The read pattern where fetching N parents costs 1 query for
the list plus N queries for each child reference.
**Example**:
```python
def read_count_referenced(n_posts):
    return n_posts + 1  # 1 list + 1 author lookup per post

print(read_count_referenced(50))  # -> 51
```
```text
# embedding removes the +N; joins collapse it to 1 in SQL
```
**Complexity**: O(N) round trips at the API boundary.
**Related**: Referencing, Embedding (data), Normalization

### Normalization
**Definition**: Designing the schema so each fact is stored once, connected
by ids — the relational default.
**Example**:
```python
# authors, posts, comments as separate tables linked by author_id/post_id
relational = {
    "authors": [{"author_id": 1, "name": "sara"}],
    "posts": [{"post_id": 1, "author_id": 1}],
    "comments": [{"comment_id": 1, "post_id": 1}],
}
```
```text
# updates touch one row; reads pay joins
```
**Complexity**: reads cost joins; writes stay small and single-source.
**Related**: Relational model, Referencing, Update fan-out

### Referencing
**Definition**: Storing an id to shared data instead of copying it, so a
change to the referenced entity updates everywhere at once.
**Example**:
```python
# post stores author_id, not the author's name
post = {"_id": 1, "title": "vector search", "author_id": 1}
# author renamed? update one authors row, all posts stay correct
```
```text
# the cost: reading the aggregate needs the extra lookup
```
**Complexity**: extra read per reference; O(1) update for shared data.
**Related**: Embedding (data), N+1 reads, Normalization

### Relational model
**Definition**: Data organized into tables of rows with enforced schema,
keys, and joins — Postgres's model.
**Example**:
```python
# one row per entity, foreign keys between tables
posts = [{"post_id": 1, "title": "vector search", "author_id": 1}]
authors = [{"author_id": 1, "name": "sara"}]
# join = match author_id across tables
```
```text
# schema enforced by the database; DDL migrations are explicit
```
**Complexity**: joins cost per query; constraints free per write.
**Related**: Normalization, Transaction (multi-doc), Referencing

### Single-field index
**Definition**: An index on exactly one field, serving equality lookups and
simple sorts.
**Example**:
```python
# real MongoDB: db.users.createIndex({"email": 1})
# query: db.users.find({"email": "a@x.com"})  # index-backed
```
```text
# the baseline index; compound covers multi-field queries
```
**Complexity**: O(log n) lookup.
**Related**: Index, Compound index, Hashed index

### Text index
**Definition**: An index supporting full-text search over string fields,
with stemming and tokenization.
**Example**:
```python
# real MongoDB: db.articles.createIndex({"title": "text", "body": "text"})
# query: db.articles.find({"$text": {"$search": "vector index"}})
```
```text
# not a replacement for dedicated search engines at scale
```
**Complexity**: tokenization at write; O(terms) query cost.
**Related**: Index, Multikey index

### Transaction (multi-doc)
**Definition**: MongoDB's opt-in all-or-nothing guarantee across several
documents, available on replica sets since 4.0.
**Example**:
```python
# session = client.start_session()
# with session.start_transaction():
#     orders.insert_one(order, session=session)
#     inventory.update_one({...}, {"$inc": {"stock": -1}}, session=session)
```
```text
# slower than single-doc ops; needs retry logic under contention
```
**Complexity**: higher latency and coordination cost per operation.
**Related**: Document atomicity, Relational model

### TTL index
**Definition**: An index on a date field that makes MongoDB delete documents
automatically after the configured seconds.
**Example**:
```python
# real MongoDB: db.sessions.createIndex({"created_at": 1},
#                                        {"expireAfterSeconds": 1800})
```
```text
# the document disappears ~1800s after its created_at timestamp
```
**Complexity**: background sweeper; O(1) per expired document.
**Related**: Index, Single-field index

### Update fan-out
**Definition**: The write cost of a denormalized design: changing shared data
requires updating every copy that embeds it.
**Example**:
```python
# author name embedded in 1000 posts:
# rename -> 1000 updates. Referenced -> 1 update.
```
```text
# the exact trade for embedding shared data
```
**Complexity**: O(copies) writes per change of the shared entity.
**Related**: Embedding (data), Referencing, Normalization

## Key Concepts Summary

### Modeling choice
- Embed children with the parent when read together, bounded, same lifecycle
- Reference shared or unbounded data; the N+1 read is the price of referencing
- Normalized (SQL) = single source of truth, joins at read; embedded = whole
  read shape, fan-out at write

### Indexes
- Single-field for equality; compound for filters + sort; multikey for arrays
- Text for search, hashed for shard keys, TTL for expiry, 2dsphere for geo
- Every index slows writes — build for the queries you actually run

### Consistency
- Per-document atomicity is the default guarantee
- Multi-document transactions exist but cost; model to avoid needing them
- SQL gives cross-row ACID by default — the honest advantage

### When to choose
- MongoDB: flexible schema, read-whole-document workloads, schemaless ingestion
- SQL: joins, cross-entity invariants, analytics, stable schemas, most OLTP

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Embedding — ___
2. N+1 reads — ___
3. Compound index — ___
4. Document atomicity — ___
5. Update fan-out — ___
6. TTL index — ___
7. Normalization — ___
8. Multi-doc transaction — ___

a) Extra lookup per referenced child when reading parents
b) Storing child data inside the parent document
c) Opt-in all-or-nothing across several documents
d) Index on several fields for filters plus sort
e) Cost of updating every copy of shared data
f) Index that auto-deletes documents after a timestamp
g) Single-document writes are all-or-nothing
h) Storing each fact once, linked by ids

**Answers:** 1-b, 2-a, 3-d, 4-g, 5-e, 6-f, 7-h, 8-c
