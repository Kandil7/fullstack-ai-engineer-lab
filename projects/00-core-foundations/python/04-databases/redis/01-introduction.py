"""
Redis — 01: Introduction
==============================================
Topics: key-value data structures, redis-py, connection pooling,
        when Redis is the WRONG tool

Why this matters for AI/backend engineering:
    Redis is the default in-memory layer in LLM applications: semantic
    caches, rate-limit counters, job queues, and session stores all sit on
    it. Knowing what it is — and what it is NOT — decides whether your
    service costs $0.10 or $10 per request.

Run:      python 01-introduction.py
Verify:   python 01-introduction.py --verify
Reference: https://redis.io/docs/latest/develop/get-started/
"""

from __future__ import annotations

import sys

from redis_client import RedisClient, get_client

# ============================================================
# 1. Key-Value Model
# ============================================================
# Redis stores STRINGS (plus richer types we meet next lesson) under flat
# keys. Keys are conventionally namespaced with colons: "cache:llm:prompt".
# Lookup by key is O(1) — that is the whole point of an in-memory store.

client: RedisClient = get_client()

# Example 1: SET / GET round trip
client.set("cache:llm:prompt", "What is a vector database?")
value = client.get("cache:llm:prompt")
print(f"GET -> {value}")

# Output:
# GET -> What is a vector database?

# Example 2: INCR as an atomic counter (O(1))
client.set("stats:requests", 0)
for _ in range(3):
    client.incr("stats:requests")
print(f"Request counter -> {client.get('stats:requests')}")

# Output:
# Request counter -> 3

# ============================================================
# 2. Why In-Memory? Latency vs Persistence
# ============================================================
# Redis keeps data in RAM: sub-millisecond reads, but persistence is a
# deliberate design choice (RDB snapshots / AOF log — topic 08). It is a
# cache and a coordination layer, NOT the system of record.

# Example 3: TTL — a key that expires (time is simulated, deterministic)
from redis_client import ManualClock

clock = ManualClock(start=100.0)
ttl_client: RedisClient = RedisClient(clock=clock)
ttl_client.set("session:user-7", "opaque-token", ex=60)
print(f"TTL right after SET -> {ttl_client.ttl('session:user-7')}s")
clock.advance(61)
print(f"TTL after 61s       -> {ttl_client.ttl('session:user-7')} (key gone)")

# Output:
# TTL right after SET -> 60s
# TTL after 61s       -> -2 (key gone)

# ============================================================
# 3. redis-py Connection Patterns
# ============================================================
# In production you use a connection POOL (reuse sockets, one client
# object per process), never a new connection per request. Our stand-in
# models the client API; the pool lesson is about process hygiene.

def cached_get(key: str, miss: callable) -> str:
    """Cache-aside read: hit returns fast, miss computes and stores."""
    hit = ttl_client.get(key)
    if hit is not None:
        return hit
    fresh = miss()
    ttl_client.set(key, fresh, ex=30)
    return fresh


calls: list[str] = []


def expensive_llm_call(prompt: str) -> str:
    """Stand-in for a real LLM completion (network + tokens = $)."""
    calls.append(prompt)
    return f"answer-for-{prompt}"


first = cached_get("q:1", lambda: expensive_llm_call("hello"))
second = cached_get("q:1", lambda: expensive_llm_call("hello"))
print(f"\nFirst  -> {first}")
print(f"Second -> {second} (served from cache)")
print(f"LLM calls made: {len(calls)} (should be 1)")

# Output:
# First  -> answer-for-hello
# Second -> answer-for-hello (served from cache)
# LLM calls made: 1 (should be 1)

# ============================================================
# 4. When Redis Is the WRONG Tool
# ============================================================
# Redis is not: a relational store (no joins/ad-hoc queries), a durable
# system of record (snapshots can be lost), a huge-data warehouse (RAM is
# the most expensive storage class), or an analytics engine. Use Postgres
# for facts, Redis for speed.

WRONG_USE = """
WRONG: storing the entire customer ledger in Redis because it is fast.
CORRECT: Postgres owns the ledger; Redis caches hot reads and queues jobs.

Choose Redis when:
  - the working set fits in RAM (say < 30 GB)
  - reads vastly outnumber writes
  - you need O(1) operations with sub-ms latency
  - you need coordination primitives (locks, rate limits, pub/sub)
Choose a database when:
  - you query by anything other than the key
  - you need ACID transactions over multiple rows
  - data must survive a restart without loss
"""

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unbounded cache keys — every user query is unique, cache grows
#   forever, memory fills, Redis evicts everything.
# CORRECT: hash/normalize keys + TTL on every entry (topic 03).
#
# MISTAKE: one connection per request — socket churn dominates latency.
# CORRECT: one pooled client per process.
#
# MISTAKE: using Redis as the system of record for money.
# CORRECT: Redis speeds up reads; the database stays authoritative.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert client.get("stats:requests") == "3", \
        "INCR must produce 3 after three increments"

    assert ttl_client.ttl("session:user-7") == -2, \
        "Key must be gone after its TTL elapses (expired -> -2)"

    # cache-aside: second read must not re-run the expensive call
    assert len(calls) == 1, \
        "Cache-aside must serve the second read from cache"

    # SET with nx=True must not overwrite an existing key
    assert ttl_client.set("nx:demo", "a", nx=True) is True, \
        "SET NX on a fresh key must succeed"
    assert ttl_client.set("nx:demo", "b", nx=True) is False, \
        "SET NX on an existing key must be rejected"
    assert ttl_client.get("nx:demo") == "a", \
        "SET NX must not overwrite the original value"

    # TTL semantics: -1 means no expiry, positive means remaining seconds
    ttl_client.set("ttl:demo", "v")
    assert ttl_client.ttl("ttl:demo") == -1, \
        "Keys set without EX must report TTL -1 (no expiry)"

    # value round-trip preserves strings
    assert client.get("cache:llm:prompt") == "What is a vector database?", \
        "GET must return exactly what SET stored"

    print("[OK] 01-introduction: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Redis is an in-memory key-value store with O(1) ops")
        print("2. TTL makes keys expire; use it for every cache entry")
        print("3. Cache-aside turns repeated LLM calls into one call + hits")
        print("4. Redis complements, never replaces, your database")
        _verify()  # always runs, so plain execution is also a test
