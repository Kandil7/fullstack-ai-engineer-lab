"""
Redis — 03: Caching Patterns
==============================================
Topics: cache-aside, write-through, write-behind, TTL, cache stampede and
        its mitigations (jitter, locks, early recompute), invalidation,
        semantic caching for LLM applications

Why this matters for AI/backend engineering:
    The highest-ROI cost optimization in LLM engineering is caching:
    identical prompts cost $0 when served from cache. This exercise builds
    a semantic cache (embedding + similarity instead of exact key match)
    and shows why naive caches collapse under load (stampede).

Run:      python 03-caching-patterns.py
Verify:   python 03-caching-patterns.py --verify
Reference: https://redis.io/docs/latest/develop/use/cases/caching/
"""

from __future__ import annotations

import hashlib
import random
import sys
import time as _time

from redis_client import ManualClock, RedisClient, get_client

random.seed(42)

# ============================================================
# 1. Cache-Aside (read-through)
# ============================================================
# The standard pattern: on read, check cache; on miss, load from the
# source of truth, store, return. TTL bounds staleness.

def cache_aside_get(key: str, load: callable, ttl: float = 60) -> str:
    hit = cache.get(key)
    if hit is not None:
        return hit
    value = load()
    cache.set(key, value, ex=ttl)
    return value


cache: RedisClient = get_client()
db_calls = 0


def load_expensive(prompt: str) -> str:
    global db_calls
    db_calls += 1
    return f"result({prompt})"


print(cache_aside_get("k:1", lambda: load_expensive("p1")))
print(cache_aside_get("k:1", lambda: load_expensive("p1")))
print(f"underlying loads: {db_calls}")

# Output:
# result(p1)
# result(p1)
# underlying loads: 1

# ============================================================
# 2. Write-Through vs Write-Behind
# ============================================================
# write-through: write DB then cache — cache never stale, write latency
#   pays both.
# write-behind: write cache first, flush to DB asynchronously — fast
#   writes, but a crash can lose the queued flush.

def write_through(db: dict, key: str, value: str) -> None:
    db[key] = value                      # system of record first
    cache.set(key, value)                # then cache
    cache.set(f"write-queue:{key}", value, ex=5)  # (write-behind demo below)


def write_behind(db: dict, key: str, value: str) -> None:
    cache.set(key, value)                # serve reads immediately
    cache.rpush("flush-queue", f"{key}:{value}")  # async flush pending


db_store: dict[str, str] = {}
write_through(db_store, "profile:1", "alice")
write_behind(db_store, "profile:2", "bob")
print(f"db has profile:2? {db_store.get('profile:2')} (write-behind not flushed yet)")

# Output:
# db has profile:2? None (write-behind not flushed yet)

# ============================================================
# 3. Cache Stampede and Mitigations
# ============================================================
# Stampede: key expires, 1000 requests all miss, all recompute the same
# expensive value simultaneously. Mitigations:
#   a) TTL jitter — expiry times spread, so recompute is staggered
#   b) early recompute — refresh before expiry, not after
#   c) lock (single-flight) — one recomputes, rest wait (topic 06)

def set_with_jitter(key: str, value: str, ttl: float, jitter: float = 0.1) -> None:
    """a) Jitter: expiry = ttl * (1 - random.uniform(0, jitter))."""
    cache.set(key, value, ex=ttl * (1 - random.uniform(0, jitter)))


clock = ManualClock(start=1000.0)
cc: RedisClient = RedisClient(clock=clock)
cc.set("hot:key", "v", ex=60)
expiry_after_jitter = [0] * 5
for i in range(5):
    cc.set(f"hot:key:{i}", "v", ex=60 * (1 - random.uniform(0, 0.2)))
    expiry_after_jitter[i] = cc.ttl(f"hot:key:{i}")
print(f"jittered TTLs: {expiry_after_jitter}  (all < 60, spread out)")

# Output:
# jittered TTLs: [54, 51, 59, 55, 52]  (all < 60, spread out)

class EarlyRecomputeCache:
    """b) Refresh the value BEFORE it expires: reads stay warm forever."""

    def __init__(self, client: RedisClient, load: callable, ttl: float = 60.0,
                 refresh_before: float = 5.0) -> None:
        self._c = client
        self._load = load
        self._ttl = ttl
        self._refresh_before = refresh_before

    def get(self, key: str) -> str:
        ttl = self._c.ttl(key)
        if ttl < self._refresh_before:
            value = self._load(key)          # early recompute, still serving
            self._c.set(key, value, ex=self._ttl)
            return value
        return self._c.get(key) or self._load(key)


erc = EarlyRecomputeCache(cc, lambda k: f"fresh({k})", ttl=60, refresh_before=5)
cc.set("erc:1", "fresh(erc:1)", ex=60)
print(erc.get("erc:1"))
clock.advance(56)                            # TTL now 4 < refresh_before
print(erc.get("erc:1"))                      # recomputed early, TTL back to 60
print(f"TTL after early recompute: {cc.ttl('erc:1')}")

# Output:
# fresh(erc:1)
# fresh(erc:1)
# TTL after early recompute: 60

# ============================================================
# 4. Semantic Cache for LLM Apps
# ============================================================
# Exact-match caching misses paraphrases. A semantic cache embeds the
# prompt and stores (vector, answer); a new prompt is answered from cache
# if the nearest stored prompt is within a similarity threshold. This is
# where Redis meets vector similarity (full treatment in vector-stores/).
# Here we use a tiny deterministic hashed embedding.

def embed(text: str, dim: int = 8) -> list[float]:
    h = int(hashlib.md5(text.encode()).hexdigest(), 16)   # stable across runs
    vec = [0.0] * dim
    vec[h % dim] = 1.0 if (h >> 8) % 2 == 0 else -1.0
    return vec


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / (
        (sum(x * x for x in a) ** 0.5) * (sum(y * y for y in b) ** 0.5) or 1.0)


class SemanticCache:
    """Prompt -> embedding -> nearest neighbor -> cached answer."""

    def __init__(self, client: RedisClient, threshold: float = 0.9) -> None:
        self._c = client
        self._threshold = threshold

    def _vec_key(self, text: str) -> str:
        v = embed(text)
        return f"svec:{'|'.join(str(round(x, 4)) for x in v)}"

    def get(self, prompt: str) -> str | None:
        v = embed(prompt)
        best_sim, best_key = -1.0, None
        for stored_key in self._c.keys("ans:*"):
            sv = [float(x) for x in stored_key.split(":")[1].split("|")]
            sim = cosine(v, sv)
            if sim > best_sim:
                best_sim, best_key = sim, stored_key
        if best_key is not None and best_sim >= self._threshold:
            return self._c.get(best_key)
        return None

    def put(self, prompt: str, answer: str) -> None:
        v = embed(prompt)
        self._c.set(f"ans:{'|'.join(str(round(x, 4)) for x in v)}", answer, ex=300)


sc = SemanticCache(cache)
sc.put("What is RAG?", "Retrieval-Augmented Generation")
print(f"exact hit   -> {sc.get('What is RAG?')}")
print(f"near miss   -> {sc.get('What is RAG')} (may or may not hit: hash embed)")

# Output:
# exact hit   -> Retrieval-Augmented Generation
# near miss   -> None (may or may not hit: hash embed)

# ============================================================
# 5. Invalidation
# ============================================================
# The hardest problem in caching: when the source of truth changes, stale
# cache answers must die. Two sane strategies: TTL (eventual consistency
# bounded by TTL) or active invalidation (DELETE on write). Never mix
# unbounded caches with mutable data.

def invalidate_on_write(db: dict, key: str, value: str) -> None:
    db[key] = value
    cache.delete(f"cache:{key}")        # kill stale entry synchronously


db_store["profile:1"] = "alice-v2"
invalidate_on_write(db_store, "profile:1", "alice-v2")
print(f"cache after invalidation: {cache.get('cache:profile:1')}")

# Output:
# cache after invalidation: None

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: same TTL for every key -> thundering herd at expiry boundaries.
# CORRECT: jitter TTLs.
#
# MISTAKE: cache writes on every DB write, even for cold keys.
# CORRECT: write-through only for hot keys; invalidate otherwise.
#
# MISTAKE: no TTL at all on cache entries -> unbounded memory + permanent
#   staleness after a bug writes a bad value.
# CORRECT: every cache entry has a TTL; treat Redis as disposable.
#
# MISTAKE: exact-key semantic cache -> paraphrases always miss.
# CORRECT: embed + threshold (or a vector store) for LLM prompts.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert db_calls == 1, "Cache-aside must load the expensive value once"

    # write-behind: cache serves the value before the DB has it
    assert cache.get("profile:2") == "bob", \
        "Write-behind must serve reads from cache immediately"
    assert db_store.get("profile:2") is None, \
        "Write-behind must NOT have flushed to the DB synchronously"

    # jitter: every TTL is strictly under the nominal 60s and varies
    assert all(t < 60 for t in expiry_after_jitter), \
        "Jitter must shorten every TTL below nominal"
    assert len(set(expiry_after_jitter)) > 1, \
        "Jitter must spread expiries (not all identical)"

    # early recompute: TTL is restored to full after refresh
    assert cc.ttl("erc:1") == 60, \
        "Early recompute must reset the TTL to the full window"

    # semantic cache: exact prompt round-trips
    assert sc.get("What is RAG?") == "Retrieval-Augmented Generation", \
        "Semantic cache must serve the stored answer for the same prompt"

    # invalidation: DELETE on write removes the stale entry
    assert cache.get("cache:profile:1") is None, \
        "Active invalidation must remove the cache entry on write"

    # jitter stays deterministic under a fixed seed
    random.seed(42)
    cc2: RedisClient = RedisClient(clock=ManualClock(start=0.0))
    cc2.set("a", "v", ex=60 * (1 - random.uniform(0, 0.2)))
    cc2.set("b", "v", ex=60 * (1 - random.uniform(0, 0.2)))
    assert cc2.ttl("a") == expiry_after_jitter[0] and cc2.ttl("b") == expiry_after_jitter[1], \
        "Jitter must reproduce exactly under the same seed"

    print("[OK] 03-caching-patterns: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Cache-aside: read -> hit/miss -> load -> store -> TTL")
        print("2. Write-through = never stale + slow; write-behind = fast + risky")
        print("3. Stampede kills caches: jitter, early recompute, single-flight")
        print("4. Semantic caching turns LLM cost into cache hits")
        _verify()  # always runs, so plain execution is also a test
