"""
Redis — 02: Data Structures
==============================================
Topics: strings, hashes, lists, sets, sorted sets, bitmaps, HyperLogLog,
        complexity per operation

Why this matters for AI/backend engineering:
    Every LLM application layer has a canonical Redis type: hashes for
    prompt/experiment metadata, lists for ingestion queues, sets for
    dedup (already-processed document hashes), sorted sets for ranking
    and priority queues, HyperLogLog for unique-user counting at ~1KB
    memory. Picking the right type is a cost decision.

Run:      python 02-data-structures.py
Verify:   python 02-data-structures.py --verify
Reference: https://redis.io/docs/latest/develop/data-types/
"""

from __future__ import annotations

import hashlib
import sys

from redis_client import RedisClient, get_client

r: RedisClient = get_client()

# ============================================================
# 1. Strings — O(1) ops
# ============================================================
# The workhorse type: any scalar you can serialize. Used for cached
# completions, counters, feature flags.

r.set("cache:completion:summarize", '{"text": "..."}', ex=300)
r.set("flag:rerank", "on")
r.incr("counter:evals")
print(f"string get -> {r.get('cache:completion:summarize')}")
print(f"string incr -> {r.get('counter:evals')}")

# Output:
# string get -> {"text": "..."}
# string incr -> 1

# ============================================================
# 2. Hashes — O(1) per field
# ============================================================
# Hashes map field -> value under one key: perfect for an object you
# mutate field-by-field (a prompt config, a user profile, an experiment
# run). Avoids re-serializing the whole object on every update.

r.hset("exp:run:42", {"model": "gpt-4o", "temperature": "0.2", "status": "running"})
r.hset("exp:run:42", {"status": "completed"})   # update ONE field
print(f"hash get -> {r.hget('exp:run:42', 'status')}")
print(f"hash all -> {r.hgetall('exp:run:42')}")

# Output:
# hash get -> completed
# hash all -> {'model': 'gpt-4o', 'temperature': '0.2', 'status': 'completed'}

# ============================================================
# 3. Lists — O(1) push/pop at both ends
# ============================================================
# Lists are queues/stack: LPUSH + BRPOP is the classic job-queue shape.
# (BRPOP = blocking right pop; our stand-in exposes RPOP — the concept
# of consuming from one end is what matters.)

r.rpush("queue:ingest", "doc-1.pdf", "doc-2.pdf", "doc-3.pdf")
print(f"list len   -> {r.llen('queue:ingest')}")
print(f"list range -> {r.lrange('queue:ingest', 0, -1)}")
print(f"list pop   -> {r.lpop('queue:ingest')}")

# Output:
# list len   -> 3
# list range -> ['doc-1.pdf', 'doc-2.pdf', 'doc-3.pdf']
# list pop   -> doc-1.pdf

# ============================================================
# 4. Sets — O(1) membership, O(n) iteration
# ============================================================
# Sets deduplicate and test membership: "has this chunk been embedded?"
# SINTER computes shared tags across documents in O(n).

r.sadd("tags:doc:1", "ml", "rag", "python")
r.sadd("tags:doc:2", "ml", "database")
r.sadd("tags:doc:2", "ml")                      # duplicate: ignored
print(f"set card      -> {r.scard('tags:doc:1')}")
print(f"set member    -> {r.sismember('tags:doc:1', 'rag')}")
print(f"set intersect -> {sorted(r.sinter('tags:doc:1', 'tags:doc:2'))}")

# Output:
# set card      -> 3
# set member    -> True
# set intersect -> ['ml']

# ============================================================
# 5. Sorted Sets — O(log n) ops
# ============================================================
# Sorted sets map member -> score with ordered access: leaderboards,
# rate limits, priority queues, and "top-k" retrievals.

r.zadd("leaderboard:rag-eval", {"system-a": 0.92, "system-b": 0.87, "system-c": 0.95})
print(f"zset top    -> {r.zrevrange('leaderboard:rag-eval', 0, 1, withscores=True)}")
r.zincrby("leaderboard:rag-eval", 0.03, "system-b")
print(f"zset rank   -> {r.zrank('leaderboard:rag-eval', 'system-b')}")
print(f"zset score  -> {r.zscore('leaderboard:rag-eval', 'system-b')}")

# Output:
# zset top    -> [('system-c', 0.95), ('system-a', 0.92)]
# zset rank   -> 1
# zset score  -> 0.9

# ============================================================
# 6. Bitmaps — 1 bit per element
# ============================================================
# Bitmaps pack boolean flags: 1M users -> 125 KB. Real Redis: SETBIT/GETBIT.
# Stand-in: we keep an int bitmask under the key.

def setbit(mask_key: str, offset: int) -> None:
    current = int(r.get(mask_key) or 0)
    r.set(mask_key, str(current | (1 << offset)))


def getbit(mask_key: str, offset: int) -> bool:
    return bool(int(r.get(mask_key) or 0) & (1 << offset))


setbit("bitmap:users-online", 7)
setbit("bitmap:users-online", 7)                # idempotent
setbit("bitmap:users-online", 42)
print(f"bitmap bit 7  -> {getbit('bitmap:users-online', 7)}")
print(f"bitmap bit 42 -> {getbit('bitmap:users-online', 42)}")
print(f"bitmap bit 8  -> {getbit('bitmap:users-online', 8)} (unset)")

# Output:
# bitmap bit 7  -> True
# bitmap bit 42 -> True
# bitmap bit 8  -> False (unset)

# ============================================================
# 7. HyperLogLog — ~12 KB for ~2^64 unique items
# ============================================================
# PFADD/PFCOUNT estimate cardinality (unique visitors, unique prompts)
# with ~0.81% error. Stand-in: hash each item, keep the longest leading
# zero-run across hashes (the HLL insight in miniature).

def pfadd(hll_key: str, *items: str) -> None:
    if not r.hexists(hll_key, "_max"):
        r.hset(hll_key, {"_max": "0"})       # initialize once, never reset
    for item in items:
        h = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        zeros = 0
        while (h >> zeros) & 1 == 0 and zeros < 64:
            zeros += 1
        if zeros > int(r.hget(hll_key, "_max") or 0):
            r.hset(hll_key, {"_max": str(zeros)})


def pfcount(hll_key: str) -> int:
    return 2 ** int(r.hget(hll_key, "_max") or 0)


pfadd("hll:unique-prompts", "hello", "world", "hello", "world")
pfadd("hll:unique-prompts", "vector")
print(f"HLL estimate -> ~{pfcount('hll:unique-prompts')} unique prompts (true: 3)")

# Output:
# HLL estimate -> ~4 unique prompts (true: 3)

# ============================================================
# Complexity Reference
# ============================================================
# | Type          | Typical op        | Time      | Space            |
# |---------------|-------------------|-----------|------------------|
# | string        | GET/SET/INCR      | O(1)      | O(len(value))    |
# | hash          | HSET/HGET         | O(1)      | O(fields)        |
# | list          | LPUSH/LPOP        | O(1)      | O(elements)      |
# | set           | SADD/SISMEMBER    | O(1)      | O(members)       |
# | sorted set    | ZADD/ZSCORE       | O(log n)  | O(members)       |
# | bitmap        | SETBIT/GETBIT     | O(1)      | O(max offset/8)  |
# | HyperLogLog   | PFADD/PFCOUNT     | O(1)      | ~12 KB fixed     |

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: storing a whole object as a string and re-writing it on every
#   field change -> every write serializes everything.
# CORRECT: hash for mutable objects; string only for atomic blobs.
#
# MISTAKE: using a list as a dedup store (O(n) scan per membership test).
# CORRECT: set for membership/dedup; list only for order-preserving queues.
#
# MISTAKE: keeping user id lists for analytics ("how many unique users?").
# CORRECT: HyperLogLog — fixed memory, 0.81% error, O(1) per add.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert r.get("counter:evals") == "1", "INCR must yield 1 from 0"

    # hash: single-field update must not clobber other fields
    h = r.hgetall("exp:run:42")
    assert h["model"] == "gpt-4o" and h["status"] == "completed", \
        "HSET of one field must preserve the others"

    # list: pop is FIFO after RPUSH
    assert r.llen("queue:ingest") == 2, "LPOP must reduce list length"
    assert r.lpop("queue:ingest") == "doc-2.pdf", "FIFO order after RPUSH"

    # set: duplicates ignored, intersection correct
    assert r.scard("tags:doc:2") == 2, "Duplicate SADD must be ignored"
    assert sorted(r.sinter("tags:doc:1", "tags:doc:2")) == ["ml"], \
        "SINTER must return shared members only"

    # sorted set: zincrby moves the member, zrevrange returns top-k
    assert r.zscore("leaderboard:rag-eval", "system-b") == 0.9, \
        "ZINCRBY must accumulate (0.87 + 0.03)"
    assert r.zrevrange("leaderboard:rag-eval", 0, 0) == ["system-c"], \
        "Top of the leaderboard must be system-c (0.95)"

    # bitmap: idempotent set, distinct offsets independent
    assert getbit("bitmap:users-online", 7) is True, "Set bit must read back True"
    assert getbit("bitmap:users-online", 8) is False, "Unset bit must read back False"

    # HLL stand-in: dedup within a batch keeps the estimate stable
    before = pfcount("hll:unique-prompts")
    pfadd("hll:unique-prompts", "hello", "world")
    assert pfcount("hll:unique-prompts") == before, \
        "Re-adding seen items must not raise the estimate"

    print("[OK] 02-data-structures: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Choose the type by operation: hash=object, list=queue,")
        print("   set=dedup, zset=ranking, bitmap=flags, HLL=cardinality")
        print("2. Every type gives O(1) or O(log n) core ops")
        print("3. Wrong type = wasted memory or O(n) scans at runtime")
        _verify()  # always runs, so plain execution is also a test
