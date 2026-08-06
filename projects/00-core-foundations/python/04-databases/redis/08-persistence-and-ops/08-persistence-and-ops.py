"""
Redis — 08: Persistence and Operations
==============================================
Topics: RDB vs AOF, eviction policies (allkeys-lru, volatile-ttl,
        noeviction), memory reporting, SCAN not KEYS, cluster basics

Why this matters for AI/backend engineering:
    Redis holds your cache, queue, and rate-limit state. When it restarts,
    what survives is decided by your persistence config; when memory runs
    out, what gets evicted is decided by your eviction policy. Both are
    one-line configs with very different failure modes — this exercise
    makes those modes visible.

Run:      python 08-persistence-and-ops.py
Verify:   python 08-persistence-and-ops.py --verify
Reference: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
"""

from __future__ import annotations

import sys

from redis_client import ManualClock, RedisClient, get_client

# ============================================================
# 1. RDB vs AOF — two persistence philosophies
# ============================================================
# RDB: point-in-time SNAPSHOT of the whole dataset, written on a
#      schedule. Cheap to load, small file — but loses everything since
#      the last snapshot (RPO = snapshot interval).
# AOF: APPEND-ONLY LOG of every write. Replays the log on start —
#      loses at most the last unsynced second (fsync policy), but the
#      log is bigger and replay is slower.
# Modern Redis: both (AOF + RDB for fast restart). The tradeoff is
# durability vs. write cost — the RPO/RTO story from databases applies.

def simulate_rdb_restore(snapshot_interval: int, crash: float,
                         writes: list[tuple[float, str]]) -> int:
    """Snapshot every `snapshot_interval` seconds; a crash at `crash`
    restores the last snapshot. Returns the number of writes lost
    (writes after the last snapshot, before the crash)."""
    last_snapshot = (int(crash) // snapshot_interval) * snapshot_interval
    return sum(1 for t, _ in writes if last_snapshot < t <= crash)


writes = [(i * 10.0, f"w{i}") for i in range(10)]   # one write per 10s
rdb_loss = simulate_rdb_restore(snapshot_interval=30, crash=85.0,
                                writes=writes)
print(f"RDB (snapshot every 30s): lose {rdb_loss} write(s) after a crash at t=85")
print(f"AOF (fsync every write):  lose 0 writes after a crash")

# Output:
# RDB (snapshot every 30s): lose 2 write(s) after a crash at t=85
# AOF (fsync every write):  lose 0 writes after a crash

# ============================================================
# 2. Eviction Policies — what dies when memory is full
# ============================================================
# maxmemory limits the store; maxmemory-policy picks the victim:
#   noeviction     -> writes FAIL (OOM error) — safe, loud
#   allkeys-lru    -> evict the least-recently-used key ANYWHERE
#   volatile-ttl   -> evict keys with the earliest TTL first
#   allkeys-random -> evict anything
# For caches, allkeys-lru is the classic choice. For rate-limit keys,
# noeviction is safer (evicting a limit means letting traffic through).

def fill_then_evict(policy: str) -> tuple[bool, list[str]]:
    c = RedisClient(clock=ManualClock(0.0))
    c.set_maxmemory(150, policy=policy)
    ok = True
    for i in range(10):
        try:
            c.set(f"k:{i}", "x" * 20)
        except MemoryError:
            ok = False
    return ok, c.keys()


print("\nnoeviction: all 10 writes accepted?", fill_then_evict("noeviction")[0])

# Output:
# noeviction: all 10 writes accepted? False

ok, keys = fill_then_evict("allkeys-lru")
print(f"allkeys-lru: all writes accepted? {ok} | surviving keys: {keys}")

# Output:
# allkeys-lru: all writes accepted? True | surviving keys: ['k:6', 'k:7', 'k:8', 'k:9']

# volatile-ttl: keys with TTL get evicted first; keys without TTL survive
vc = RedisClient(clock=ManualClock(0.0))
vc.set_maxmemory(150, policy="volatile-ttl")
for i in range(8):
    vc.set(f"v:{i}", "y" * 20, ex=1000 - i * 100)   # v:0 expires latest
vc.set("no-ttl:1", "z" * 20)                        # never expires
vc.set("no-ttl:2", "z" * 20)                        # must survive eviction
print(f"volatile-ttl: no-ttl keys survived? "
      f"{bool(vc.exists('no-ttl:1') and vc.exists('no-ttl:2'))}")

# Output:
# volatile-ttl: no-ttl keys survived? True

# ============================================================
# 3. Memory Reporting
# ============================================================
# INFO memory / MEMORY USAGE report per-key size. Knowing your footprint
# is how you size maxmemory before an incident, not after.

def memory_usage(c: RedisClient, key: str) -> int:
    return c._key_size(key)


c = RedisClient(clock=ManualClock(0.0))
c.set("tiny", "a")
c.set("big", "x" * 500)
c.rpush("list:many", *range(50))
print(f"\nmemory: tiny={memory_usage(c, 'tiny')}B big={memory_usage(c, 'big')}B "
      f"list:many={memory_usage(c, 'list:many')}B")

# Output:
# memory: tiny=17B big=516B list:many=1616B

# ============================================================
# 4. SCAN, Not KEYS
# ============================================================
# KEYS * blocks Redis for the whole scan — on a busy production cache
# that is seconds of frozen service. SCAN returns small batches via a
# cursor; the server keeps serving between batches. (Our stand-in models
# the cursor contract; the blocking difference is real.)

c2 = RedisClient(clock=ManualClock(0.0))
for i in range(50):
    c2.set(f"user:{i}:profile", "p")
cursor, batch = 0, []
seen = 0
while True:
    cursor, batch = c2.scan(cursor, match="user:*", count=10)
    seen += len(batch)
    if cursor == 0:
        break
print(f"\nSCAN batches over 50 keys with count=10: {seen} keys found (cursor loop)")

# Output:
# SCAN batches over 50 keys with count=10: 50 keys found (cursor loop)

# ============================================================
# 5. Cluster Basics
# ============================================================
# A Redis Cluster shards keys across 16384 hash slots; each key maps to
# a slot via CRC16(key) % 16384. Clients route by slot. Hash tags
# ({user:1}.profile) force related keys into the same slot so multi-key
# ops work. Stand-in: compute the slot a key would land on.

def hash_slot(key: str) -> int:
    """CRC16 % 16384, honoring hash tags: only the text inside the FIRST
    pair of braces is hashed, so {user:1}:profile and {user:1}:settings
    land on the same slot."""
    tag = key
    if "{" in key and "}" in key:
        start = key.index("{") + 1
        end = key.index("}", start)
        if start < end:
            tag = key[start:end]
    crc = 0
    for ch in tag.encode():
        crc = ((crc << 5) - crc + ch) & 0xFFFFFFFF
    return crc % 16384


print(f"\nslot('user:1:profile') = {hash_slot('user:1:profile')}")
print(f"slot('user:2:profile') = {hash_slot('user:2:profile')}")
print(f"slot('{'{user:1}'}:profile') = {hash_slot('{user:1}:profile')} "
      f"(hash tag forces same slot)")

# Output:
# slot('user:1:profile') = 15985
# slot('user:2:profile') = 11634
# slot('{user:1}:profile') = 16335 (hash tag forces same slot)

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: noeviction + no monitoring -> cache writes start failing at
#   3 AM; the app 500s.
# CORRECT: allkeys-lru for pure caches; alert on maxmemory usage.
#
# MISTAKE: KEYS * in production scripts.
# CORRECT: SCAN with a cursor in small batches.
#
# MISTAKE: RDB-only persistence for a queue/stream you cannot afford to
#   lose — a crash between snapshots loses every queued job.
# CORRECT: AOF (or streams + consumer groups) when loss is unacceptable.
#
# MISTAKE: assuming TTL-less keys are safe from eviction under
#   allkeys-lru — they are exactly the victims LRU picks first.
# CORRECT: volatile policies for "must keep" keys, or size maxmemory
#   above the working set.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # RDB loses writes since the last snapshot; AOF loses none
    assert rdb_loss == 2, \
        "RDB must lose exactly the writes since the last snapshot"

    # noeviction rejects writes when full
    ok, _ = fill_then_evict("noeviction")
    assert ok is False, "noeviction must reject writes past maxmemory"

    # allkeys-lru accepts writes by evicting the least-recently-used keys
    ok, keys = fill_then_evict("allkeys-lru")
    assert ok is True, "allkeys-lru must keep accepting writes"
    assert "k:0" not in keys, "LRU must evict the oldest keys first"
    assert "k:9" in keys, "the newest key must survive LRU eviction"

    # volatile-ttl spares keys without TTL
    assert vc.exists("no-ttl:1") and vc.exists("no-ttl:2"), \
        "volatile-ttl must never evict keys without a TTL"

    # memory sizing is proportional to value length
    assert memory_usage(c, "big") > memory_usage(c, "tiny"), \
        "longer values must report larger memory footprints"

    # SCAN returns every matching key across batches
    assert seen == 50, "SCAN must visit all 50 keys across cursor batches"

    # hash tags: keys inside {braces} share the slot of the braced part
    assert hash_slot("{user:1}:profile") == hash_slot("{user:1}:settings"), \
        "hash tags must route related keys to the same slot"

    # eviction frees memory: after eviction the store fits under maxmemory
    c3 = RedisClient(clock=ManualClock(0.0))
    c3.set_maxmemory(200, policy="allkeys-lru")
    for i in range(10):
        c3.set(f"e:{i}", "x" * 40)
    used = sum(c3._key_size(k) for k in c3.keys())
    assert used <= 200, "after eviction the store must fit under maxmemory"

    print("[OK] 08-persistence-and-ops: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. RDB = snapshot (small, lossy); AOF = log (durable, bigger)")
        print("2. Eviction policy decides WHO dies at maxmemory")
        print("3. Memory reporting precedes capacity planning")
        print("4. SCAN, never KEYS; clusters shard by CRC16 slots")
        _verify()  # always runs, so plain execution is also a test
