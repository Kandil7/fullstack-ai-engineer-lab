"""
MongoDB — 12: MongoDB vs SQL (The Honest Tradeoff)
==============================================
Topics: document vs relational modeling, embedding vs referencing,
        schema flexibility and its cost, index types, transactions,
        when NOT to use MongoDB

Why this matters for AI/backend engineering:
    Every database decision is a tradeoff, and MongoDB's pitch is
    "flexibility + one-document reads". That is genuinely valuable for
    schemaless ingestion and read-with-parent workloads — and genuinely
    wrong for joins, strict ACID across documents, and analytics. This
    exercise makes the tradeoff measurable instead of opinionated.

Run:      python 12-mongo-vs-sql.py
Verify:   python 12-mongo-vs-sql.py --verify
Reference: https://www.mongodb.com/docs/manual/data-modeling/
"""

from __future__ import annotations

import sys

# ============================================================
# 1. The Same Domain, Two Models
# ============================================================
# Domain: blog posts with an author and comments.
#
# RELATIONAL (normalized):
#   posts(post_id, title, author_id) -> authors(author_id, name)
#                                     -> comments(comment_id, post_id, text)
#   Reading a post + comments = 3 queries + 2 joins.
#
# DOCUMENT (embedded):
#   {_id, title, author: {name}, comments: [{text}]}
#   Reading a post + comments = 1 query, 1 document.

# Stand-in relational store: dict of "tables" of rows
relational = {
    "authors": [
        {"author_id": 1, "name": "sara"},
        {"author_id": 2, "name": "omar"},
    ],
    "posts": [
        {"post_id": 1, "title": "vector search", "author_id": 1},
        {"post_id": 2, "title": "prompt caching", "author_id": 2},
    ],
    "comments": [
        {"comment_id": 1, "post_id": 1, "text": "great read"},
        {"comment_id": 2, "post_id": 1, "text": "examples? :)"},
        {"comment_id": 3, "post_id": 2, "text": "nice"},
    ],
}

# Stand-in document store: one collection of documents
embedded = [
    {
        "_id": 1,
        "title": "vector search",
        "author": {"author_id": 1, "name": "sara"},
        "comments": [
            {"comment_id": 1, "text": "great read"},
            {"comment_id": 2, "text": "examples? :)"},
        ],
    },
    {
        "_id": 2,
        "title": "prompt caching",
        "author": {"author_id": 2, "name": "omar"},
        "comments": [{"comment_id": 3, "text": "nice"}],
    },
]


def read_post_relational(post_id: int) -> dict:
    """SQL-style: post, then author lookup, then comments (3 reads)."""
    post = next(p for p in relational["posts"] if p["post_id"] == post_id)
    author = next(a for a in relational["authors"]
                  if a["author_id"] == post["author_id"])
    comments = [c for c in relational["comments"] if c["post_id"] == post_id]
    return {"title": post["title"], "author": author["name"],
            "comments": [c["text"] for c in comments]}


def read_post_embedded(post_id: int) -> dict:
    """MongoDB-style: one document holds everything (1 read)."""
    return next(p for p in embedded if p["_id"] == post_id)


print("relational read (3 lookups):", read_post_relational(1)["title"])
print("embedded read   (1 lookup): ", read_post_embedded(1)["title"])

# Output:
# relational read (3 lookups): vector search
# embedded read   (1 lookup):  vector search

# ============================================================
# 2. Embedding vs Referencing — Decision Rules
# ============================================================
# Embed when:  read together always, bounded size, no independent
#              lifecycle (comments die with the post).
# Reference when: shared data (author across 1000 posts), unbounded
#              growth, or independent updates (author name changes ->
#              embed means updating every post).

def should_embed(*, read_together: bool, bounded: bool,
                 independent_lifecycle: bool) -> bool:
    """Embed only when all three hold."""
    return read_together and bounded and not independent_lifecycle


decisions = [
    ("post + comments", should_embed(read_together=True, bounded=False,
                                     independent_lifecycle=False)),
    ("author embedded in post", should_embed(read_together=True, bounded=True,
                                             independent_lifecycle=True)),
    ("order + line items", should_embed(read_together=True, bounded=True,
                                        independent_lifecycle=False)),
]
for name, embed in decisions:
    print(f"{name}: {'EMBED' if embed else 'REFERENCE'}")

# Output:
# post + comments: REFERENCE  (comments are unbounded)
# author embedded in post: REFERENCE  (shared, changes independently)
# order + line items: EMBED  (bounded, read together, same lifecycle)

# ============================================================
# 3. Referencing Cost — the N+1 Read
# ============================================================
# Reference-based reads pay extra round trips: the classic N+1. With
# 50 posts by one author, reading all of them "with author" costs 51
# reads in a pure referenced design (1 for posts + 50 author lookups),
# vs 50 reads with the author embedded.

def read_count_referenced(n_posts: int) -> int:
    return n_posts + 1  # 1 query for the list + 1 per post's author


def read_count_embedded(n_posts: int) -> int:
    return n_posts  # one document per post, author included


print(f"\n50 posts: referenced reads = {read_count_referenced(50)}, "
      f"embedded reads = {read_count_embedded(50)}")

# Output:
# 50 posts: referenced reads = 51, embedded reads = 50

# ============================================================
# 4. Schema Flexibility — and Its Cost
# ============================================================
# MongoDB lets documents in one collection differ. That is a feature
# for ingestion (log lines with varying fields) and a liability for
# application invariants: the database will not stop you from saving
# {"age": "not-a-number"}. SQL's ALTER TABLE is replaced by a
# migration + $jsonSchema validator — the schema moves from the
# database into your code unless you enforce it.

polymorphic = [
    {"_id": 1, "kind": "user", "name": "sara"},
    {"_id": 2, "kind": "product", "name": "laptop", "price": 999.99},
    {"_id": 3, "kind": "user", "name": "omar", "email": "omar@x.com"},
]


def required_fields(doc: dict, required: list) -> bool:
    return all(f in doc for f in required)


print(f"\nall docs have 'kind'? {all(required_fields(d, ['kind']) for d in polymorphic)}")
print(f"all docs have 'price'? {all(required_fields(d, ['price']) for d in polymorphic)}")

# Output:
# all docs have 'kind'? True
# all docs have 'price'? False

# ============================================================
# 5. Index Types — What MongoDB Actually Offers
# ============================================================
# Indexes are how MongoDB avoids collection scans:
#   single-field  : {"email": 1}            equality on one field
#   compound      : {"tenant_id": 1, "created_at": -1}  multi-field
#   multikey      : on an ARRAY field       tags, categories
#   text          : full-text search        titles, bodies
#   hashed        : shard keys, equality only
#   TTL           : auto-delete after expiry  (sessions, logs)
#   2dsphere      : geospatial queries
# The cost: every index slows writes and burns memory. Indexes must
# be chosen for the QUERIES you actually run, exactly like SQL.

def build_index(collection, field):
    """Stand-in: index = {field_value: [doc, ...]}"""
    idx = {}
    for doc in collection:
        if field in doc:
            idx.setdefault(doc[field], []).append(doc)
    return idx


email_index = build_index(polymorphic, "email")
print(f"\nemail index: {sorted(email_index.keys())}")
print(f"lookup 'omar@x.com': {email_index.get('omar@x.com')}")

# Output:
# email index: ['omar@x.com']
# lookup 'omar@x.com': [{'_id': 3, 'kind': 'user', 'name': 'omar', 'email': 'omar@x.com'}]

# ============================================================
# 6. Transactions — Single-Document vs Multi-Document
# ============================================================
# MongoDB guarantees atomicity per DOCUMENT. Multi-document
# transactions exist (replica sets, since 4.0) but are the exception:
# they are slower, need retry logic, and are a sign the model fights
# the workload. The stand-in shows the two semantics.

class MiniTransaction:
    """All-or-nothing over a list of writes: commit or rollback."""

    def __init__(self, collection) -> None:
        self._coll = collection
        self._backup = list(collection)
        self._active = True

    def apply(self, doc) -> None:
        assert self._active, "transaction already finished"
        self._coll.append(doc)

    def commit(self) -> None:
        self._active = False

    def rollback(self) -> None:
        self._coll[:] = self._backup
        self._active = False


tx = MiniTransaction(polymorphic)
tx.apply({"_id": 9, "kind": "log", "level": "info"})
tx.rollback()  # crash before commit -> nothing was written
print(f"\nafter rollback, _id 9 present? {any(d['_id'] == 9 for d in polymorphic)}")

# Output:
# after rollback, _id 9 present? False

# ============================================================
# 7. When NOT to Use MongoDB
# ============================================================
# The honest answer: most OLTP systems with cross-entity invariants
# belong in a relational store. MongoDB wins when the read shape is
# "give me this whole document" and the schema is genuinely unstable.

def recommend_db(*, heavy_joins: bool, strict_acid: bool,
                 flexible_schema: bool, analytics: bool) -> str:
    """Pick a database family from the workload's hard requirements."""
    if heavy_joins or strict_acid or analytics:
        return "SQL (Postgres)"
    if flexible_schema:
        return "MongoDB"
    return "SQL (Postgres)"  # default: relational for stable schemas


cases = [
    ("order system (ACID, joins)", dict(heavy_joins=True, strict_acid=True,
                                        flexible_schema=False, analytics=False)),
    ("log ingestion (varying fields)", dict(heavy_joins=False, strict_acid=False,
                                            flexible_schema=True, analytics=False)),
    ("bi reporting (aggregations)", dict(heavy_joins=True, strict_acid=False,
                                         flexible_schema=False, analytics=True)),
    ("content app, read-by-id", dict(heavy_joins=False, strict_acid=False,
                                     flexible_schema=False, analytics=False)),
]
for name, req in cases:
    print(f"{name}: {recommend_db(**req)}")

# Output:
# order system (ACID, joins): SQL (Postgres)
# log ingestion (varying fields): MongoDB
# bi reporting (aggregations): SQL (Postgres)
# content app, read-by-id: SQL (Postgres)

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: embedding shared data (author, category) -> update fan-out.
# CORRECT: reference shared data; embed only what dies with the parent.
#
# MISTAKE: assuming MongoDB gives ACID across documents for free.
# CORRECT: multi-doc transactions exist but cost; model per-document.
#
# MISTAKE: no indexes on hot query fields -> collection scans.
# CORRECT: index by the queries; compound for multi-field filters.
#
# MISTAKE: "no schema" as an excuse to skip validation.
# CORRECT: $jsonSchema validators + app-level invariants.
#
# MISTAKE: choosing MongoDB because SQL is "boring".
# CORRECT: choose by join/ACID/analytics needs; Mongo for flexible,
#          read-with-parent workloads.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # both models answer the same question
    assert read_post_relational(1)["title"] == "vector search"
    assert read_post_embedded(1)["title"] == "vector search"

    # embedded read returns the full graph in one document
    assert read_post_embedded(1)["author"]["name"] == "sara"
    assert len(read_post_embedded(1)["comments"]) == 2

    # embedding decision rules
    assert decisions[0][1] is False, "unbounded comments must be referenced"
    assert decisions[1][1] is False, "shared author must be referenced"
    assert decisions[2][1] is True, "bounded same-lifecycle data embeds"

    # referencing costs extra reads (N+1)
    assert read_count_referenced(50) == 51
    assert read_count_embedded(50) == 50
    assert read_count_referenced(50) > read_count_embedded(50)

    # schema flexibility: missing fields are allowed
    assert all(required_fields(d, ["kind"]) for d in polymorphic)
    assert not all(required_fields(d, ["price"]) for d in polymorphic)

    # index lookup works for present values, misses for absent ones
    email_index = build_index(polymorphic, "email")
    assert len(email_index.get("omar@x.com", [])) == 1
    assert "nobody@x.com" not in email_index

    # transactions: rollback restores the pre-transaction state
    snap = list(polymorphic)
    tx2 = MiniTransaction(polymorphic)
    tx2.apply({"_id": 99, "kind": "log"})
    tx2.rollback()
    assert all(d["_id"] != 99 for d in polymorphic)
    assert polymorphic == snap, "rollback must restore the collection"

    # honest recommendations
    assert recommend_db(heavy_joins=True, strict_acid=True,
                        flexible_schema=False, analytics=False) == "SQL (Postgres)"
    assert recommend_db(heavy_joins=False, strict_acid=False,
                        flexible_schema=True, analytics=False) == "MongoDB"
    assert recommend_db(heavy_joins=True, strict_acid=False,
                        flexible_schema=False, analytics=True) == "SQL (Postgres)"

    print("[OK] 12-mongo-vs-sql: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        _verify()  # plain execution is also a test
