"""
Redis teaching stand-in (no server required)
==============================================
A small in-memory RedisClient stand-in that mirrors the redis-py API closely
enough to teach real Redis concepts: SET/GET/EXPIRE/INCR, hashes, lists,
sets, sorted sets, pub/sub, MULTI/EXEC pipelines, scripts, and eviction.

Design notes
------------
- Values are stored as native Python types (str/int/float) instead of bytes,
  because the stand-in is a *teaching* device: the concepts transfer to
  redis-py, the byte-decoding noise does not.
- A clock is injectable (`clock=`) so exercises can advance time
  deterministically. Never assert against wall-clock time.
- `get_client()` prefers the stand-in by default so CI is deterministic.
  Set env var REDIS_REAL=1 to use a real redis server when one is reachable;
  it falls back to the stand-in (never crashes).
"""

from __future__ import annotations

import os
import time
from collections import deque
from typing import Any, Callable, Optional


class ManualClock:
    """Deterministic clock: advance() instead of waiting."""

    def __init__(self, start: float = 0.0) -> None:
        self._t: float = start

    def advance(self, seconds: float) -> None:
        self._t += seconds

    def __call__(self) -> float:
        return self._t


class Subscription:
    """A single subscriber's view of one channel."""

    def __init__(self, channel: str) -> None:
        self.channel: str = channel
        self._queue: deque[str] = deque()

    def _deliver(self, message: str) -> None:
        self._queue.append(message)

    def get_message(self) -> Optional[str]:
        """Return the oldest undelivered message, or None if the queue is empty."""
        if not self._queue:
            return None
        return self._queue.popleft()


class Pipeline:
    """Batched commands executed atomically via MULTI/EXEC semantics."""

    def __init__(self, client: "RedisClient") -> None:
        self._client = client
        self._commands: list[tuple[str, tuple, dict]] = []

    def _queue(self, name: str, *args: Any, **kwargs: Any) -> "Pipeline":
        self._commands.append((name, args, kwargs))
        return self

    # --- command surface (mirrors RedisClient) ---
    def set(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("set", *a, **k)

    def get(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("get", *a, **k)

    def incr(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("incr", *a, **k)

    def expire(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("expire", *a, **k)

    def delete(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("delete", *a, **k)

    def hset(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("hset", *a, **k)

    def lpush(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("lpush", *a, **k)

    def rpush(self, *a: Any, **k: Any) -> "Pipeline":
        return self._queue("rpush", *a, **k)

    def execute(self) -> list[Any]:
        """Apply all queued commands in order and return their results."""
        self._client.multi()
        results: list[Any] = []
        for name, args, kwargs in self._commands:
            method = getattr(self._client, name)
            results.append(method(*args, **kwargs))
        self._client.exec()
        self._commands = []
        return results


class RedisClient:
    """Dict-based stand-in for a Redis server. Thread-safety is NOT simulated."""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock: Callable[[], float] = clock if clock is not None else time.monotonic
        self._str: dict[str, str] = {}            # string keys -> values
        self._expiry: dict[str, float] = {}       # key -> absolute expiry time
        self._hashes: dict[str, dict[str, str]] = {}
        self._lists: dict[str, list[Any]] = {}
        self._sets: dict[str, set[Any]] = {}
        self._zsets: dict[str, dict[str, float]] = {}
        self._subscribers: dict[str, list[Subscription]] = {}
        self._access: dict[str, int] = {}         # LRU counter for eviction
        self._maxmemory: int = 0
        self._eviction_policy: str = "noeviction"
        self._in_txn: bool = False
        self._txn_queue: list[tuple[str, tuple, dict]] = []
        self._scripts: dict[str, Callable[[RedisClient, list[str], list[Any]], Any]] = {}
        self._clock_counter: int = 0              # tie-breaker for LRU

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _now(self) -> float:
        return self._clock()

    def _purge(self, key: str) -> None:
        if key in self._expiry and self._now() >= self._expiry[key]:
            self._del_key(key)

    def _touch(self, key: str) -> None:
        self._clock_counter += 1
        self._access[key] = self._clock_counter

    def _del_key(self, key: str) -> None:
        for store in (self._str, self._hashes, self._lists, self._sets, self._zsets):
            store.pop(key, None)
        self._expiry.pop(key, None)
        self._access.pop(key, None)

    def _key_kind(self, key: str) -> str:
        self._purge(key)  # EXISTS/TYPE on an expired key must see it gone
        if key in self._str:
            return "string"
        if key in self._hashes:
            return "hash"
        if key in self._lists:
            return "list"
        if key in self._sets:
            return "set"
        if key in self._zsets:
            return "zset"
        return "none"

    def _key_size(self, key: str) -> int:
        kind = self._key_kind(key)
        if kind == "string":
            return len(self._str[key]) + 16
        if kind == "hash":
            return 32 * len(self._hashes[key]) + 16
        if kind == "list":
            return 32 * len(self._lists[key]) + 16
        if kind == "set":
            return 32 * len(self._sets[key]) + 16
        if kind == "zset":
            return 48 * len(self._zsets[key]) + 16
        return 0

    def _enforce_maxmemory(self) -> None:
        """Evict keys until the store fits under maxmemory (0 = unlimited)."""
        if self._maxmemory <= 0:
            return
        used = sum(self._key_size(k) for k in self._str | self._hashes | self._lists
                   | self._sets | self._zsets)
        while used > self._maxmemory and (self._str or self._hashes or self._lists
                                          or self._sets or self._zsets):
            if self._eviction_policy == "noeviction":
                raise MemoryError("OOM command not allowed when used memory > maxmemory")
            if self._eviction_policy == "allkeys-lru":
                victim = min(self._access, key=lambda k: self._access[k])
            elif self._eviction_policy == "volatile-ttl":
                volatile = [k for k in self._expiry if self._key_kind(k) != "none"]
                victim = min(volatile, key=lambda k: self._expiry[k]) if volatile else None
            else:
                victim = None
            if victim is None:
                return
            used -= self._key_size(victim)
            self._del_key(victim)

    # ------------------------------------------------------------------
    # strings
    # ------------------------------------------------------------------
    def set(self, name: str, value: Any, ex: Optional[float] = None,
            nx: bool = False, xx: bool = False) -> bool:
        self._purge(name)  # an expired key must not block NX / satisfy XX
        if nx and name in self._str:
            return False
        if xx and name not in self._str:
            return False
        self._str[name] = str(value)
        if ex is not None:
            self._expiry[name] = self._now() + ex
        else:
            self._expiry.pop(name, None)
        self._touch(name)
        self._enforce_maxmemory()
        return True

    def get(self, name: str) -> Optional[str]:
        self._purge(name)
        if name in self._str:
            self._touch(name)
            return self._str[name]
        return None

    def setnx(self, name: str, value: Any) -> bool:
        return self.set(name, value, nx=True)

    def mset(self, mapping: dict) -> bool:
        for k, v in mapping.items():
            self.set(k, v)
        return True

    def mget(self, *names: str) -> list[Optional[str]]:
        return [self.get(n) for n in names]

    def delete(self, *names: str) -> int:
        count = 0
        for n in names:
            if self._key_kind(n) != "none":
                self._del_key(n)
                count += 1
        return count

    def exists(self, *names: str) -> int:
        return sum(1 for n in names if self._key_kind(n) != "none")

    def expire(self, name: str, seconds: float) -> bool:
        if self._key_kind(name) == "none":
            return False
        self._expiry[name] = self._now() + seconds
        return True

    def ttl(self, name: str) -> int:
        self._purge(name)
        if self._key_kind(name) == "none":
            return -2
        if name not in self._expiry:
            return -1
        return max(0, int(self._expiry[name] - self._now()))

    def persist(self, name: str) -> bool:
        if name in self._expiry:
            del self._expiry[name]
            return True
        return False

    def incr(self, name: str, amount: int = 1) -> int:
        self._purge(name)
        cur = int(self._str.get(name, 0))
        new = cur + amount
        self._str[name] = str(new)
        self._touch(name)
        return new

    def decr(self, name: str, amount: int = 1) -> int:
        return self.incr(name, -amount)

    def append(self, name: str, value: str) -> int:
        self._purge(name)
        cur = self._str.get(name, "")
        self._str[name] = cur + value
        self._touch(name)
        return len(self._str[name])

    def strlen(self, name: str) -> int:
        self._purge(name)
        return len(self._str.get(name, ""))

    # ------------------------------------------------------------------
    # hashes
    # ------------------------------------------------------------------
    def hset(self, name: str, mapping: dict) -> int:
        self._purge(name)
        store = self._hashes.setdefault(name, {})
        before = len(store)
        for k, v in mapping.items():
            store[str(k)] = str(v)
        self._touch(name)
        return len(store) - before

    def hget(self, name: str, key: str) -> Optional[str]:
        self._purge(name)
        return self._hashes.get(name, {}).get(str(key))

    def hgetall(self, name: str) -> dict[str, str]:
        self._purge(name)
        return dict(self._hashes.get(name, {}))

    def hmget(self, name: str, *keys: str) -> list[Optional[str]]:
        return [self.hget(name, k) for k in keys]

    def hdel(self, name: str, *keys: str) -> int:
        self._purge(name)
        store = self._hashes.get(name, {})
        count = 0
        for k in keys:
            if str(k) in store:
                del store[str(k)]
                count += 1
        return count

    def hexists(self, name: str, key: str) -> bool:
        self._purge(name)
        return str(key) in self._hashes.get(name, {})

    def hincrby(self, name: str, key: str, amount: int = 1) -> int:
        self._purge(name)
        store = self._hashes.setdefault(name, {})
        new = int(store.get(str(key), 0)) + amount
        store[str(key)] = str(new)
        return new

    def hkeys(self, name: str) -> list[str]:
        self._purge(name)
        return list(self._hashes.get(name, {}))

    # ------------------------------------------------------------------
    # lists
    # ------------------------------------------------------------------
    def lpush(self, name: str, *values: Any) -> int:
        self._purge(name)
        store = self._lists.setdefault(name, [])
        for v in reversed(values):
            store.insert(0, v)
        self._touch(name)
        return len(store)

    def rpush(self, name: str, *values: Any) -> int:
        self._purge(name)
        store = self._lists.setdefault(name, [])
        store.extend(values)
        self._touch(name)
        return len(store)

    def lpop(self, name: str) -> Optional[Any]:
        self._purge(name)
        store = self._lists.get(name)
        if not store:
            return None
        value = store.pop(0)
        if not store:
            del self._lists[name]
        return value

    def rpop(self, name: str) -> Optional[Any]:
        self._purge(name)
        store = self._lists.get(name)
        if not store:
            return None
        value = store.pop()
        if not store:
            del self._lists[name]
        return value

    def llen(self, name: str) -> int:
        self._purge(name)
        return len(self._lists.get(name, []))

    def lrange(self, name: str, start: int, stop: int) -> list[Any]:
        self._purge(name)
        store = self._lists.get(name, [])
        if stop < 0:
            stop = len(store) + stop
        return store[start:stop + 1]

    def lindex(self, name: str, index: int) -> Optional[Any]:
        self._purge(name)
        store = self._lists.get(name, [])
        try:
            return store[index]
        except IndexError:
            return None

    # ------------------------------------------------------------------
    # sets
    # ------------------------------------------------------------------
    def sadd(self, name: str, *values: Any) -> int:
        self._purge(name)
        store = self._sets.setdefault(name, set())
        before = len(store)
        store.update(values)
        return len(store) - before

    def srem(self, name: str, *values: Any) -> int:
        self._purge(name)
        store = self._sets.get(name)
        if store is None:
            return 0
        count = 0
        for v in values:
            if v in store:
                store.discard(v)
                count += 1
        return count

    def sismember(self, name: str, value: Any) -> bool:
        self._purge(name)
        return value in self._sets.get(name, set())

    def smembers(self, name: str) -> set[Any]:
        self._purge(name)
        return set(self._sets.get(name, set()))

    def scard(self, name: str) -> int:
        self._purge(name)
        return len(self._sets.get(name, set()))

    def sinter(self, *names: str) -> set[Any]:
        if not names:
            return set()
        result = set(self._sets.get(names[0], set()))
        for n in names[1:]:
            self._purge(n)
            result &= self._sets.get(n, set())
        return result

    # ------------------------------------------------------------------
    # sorted sets
    # ------------------------------------------------------------------
    def zadd(self, name: str, mapping: dict[str, float]) -> int:
        self._purge(name)
        store = self._zsets.setdefault(name, {})
        added = 0
        for member, score in mapping.items():
            if member not in store:
                added += 1
            store[member] = float(score)
        return added

    def zincrby(self, name: str, amount: float, member: str) -> float:
        self._purge(name)
        store = self._zsets.setdefault(name, {})
        new = store.get(member, 0.0) + amount
        store[member] = new
        return new

    def zscore(self, name: str, member: str) -> Optional[float]:
        self._purge(name)
        return self._zsets.get(name, {}).get(member)

    def zrank(self, name: str, member: str) -> Optional[int]:
        self._purge(name)
        store = self._zsets.get(name, {})
        if member not in store:
            return None
        return sum(1 for m, s in store.items() if s < store[member] or
                   (s == store[member] and m < member))

    def zrevrank(self, name: str, member: str) -> Optional[int]:
        self._purge(name)
        store = self._zsets.get(name, {})
        if member not in store:
            return None
        return sum(1 for m, s in store.items() if s > store[member] or
                   (s == store[member] and m > member))

    def zrange(self, name: str, start: int, stop: int,
               withscores: bool = False, reverse: bool = False) -> list[Any]:
        self._purge(name)
        store = self._zsets.get(name, {})
        ordered = sorted(store.items(), key=lambda kv: (kv[1], kv[0]),
                         reverse=reverse)
        if stop < 0:
            stop = len(ordered) + stop
        if withscores:
            return [tuple(item) for item in ordered[start:stop + 1]]
        return [m for m, _ in ordered[start:stop + 1]]

    def zrevrange(self, name: str, start: int, stop: int,
                  withscores: bool = False) -> list[Any]:
        return self.zrange(name, start, stop, withscores=withscores, reverse=True)

    def zrangebyscore(self, name: str, min_score: float,
                      max_score: float, withscores: bool = False) -> list[Any]:
        self._purge(name)
        store = self._zsets.get(name, {})
        hits = sorted([(m, s) for m, s in store.items()
                       if min_score <= s <= max_score], key=lambda kv: (kv[1], kv[0]))
        if withscores:
            return [tuple(h) for h in hits]
        return [m for m, _ in hits]

    def zremrangebyscore(self, name: str, min_score: float,
                         max_score: float) -> int:
        """Remove members whose score falls in [min_score, max_score]."""
        self._purge(name)
        store = self._zsets.get(name, {})
        doomed = [m for m, s in store.items() if min_score <= s <= max_score]
        for m in doomed:
            del store[m]
        return len(doomed)

    def zrem(self, name: str, *members: str) -> int:
        self._purge(name)
        store = self._zsets.get(name, {})
        count = 0
        for m in members:
            if m in store:
                del store[m]
                count += 1
        return count

    def zcard(self, name: str) -> int:
        self._purge(name)
        return len(self._zsets.get(name, {}))

    # ------------------------------------------------------------------
    # pub/sub
    # ------------------------------------------------------------------
    def publish(self, channel: str, message: str) -> int:
        subs = self._subscribers.get(channel, [])
        for sub in subs:
            sub._deliver(message)
        return len(subs)

    def subscribe(self, channel: str) -> Subscription:
        sub = Subscription(channel)
        self._subscribers.setdefault(channel, []).append(sub)
        return sub

    def unsubscribe(self, sub: Subscription) -> None:
        subs = self._subscribers.get(sub.channel, [])
        if sub in subs:
            subs.remove(sub)

    # ------------------------------------------------------------------
    # MULTI / EXEC / pipelines / scripts
    # ------------------------------------------------------------------
    def multi(self) -> None:
        self._in_txn = True
        self._txn_queue = []

    def exec(self) -> list[Any]:
        if not self._in_txn:
            raise RuntimeError("EXEC without MULTI")
        queue, self._txn_queue = self._txn_queue, []
        self._in_txn = False
        results: list[Any] = []
        for name, args, kwargs in queue:
            results.append(getattr(self, name)(*args, **kwargs))
        return results

    def discard(self) -> None:
        self._in_txn = False
        self._txn_queue = []

    def _queue_cmd(self, name: str, *args: Any, **kwargs: Any) -> None:
        if self._in_txn:
            self._txn_queue.append((name, args, kwargs))
        else:
            getattr(self, name)(*args, **kwargs)

    def pipeline(self) -> Pipeline:
        return Pipeline(self)

    def register_script(self, name: str, fn: Callable[[RedisClient, list[str], list[Any]], Any]) -> None:
        """Register a named script that runs 'atomically' (single-threaded sim)."""
        self._scripts[name] = fn

    def evalsha(self, name: str, keys: list[str], args: list[Any]) -> Any:
        if name not in self._scripts:
            raise KeyError(f"No script registered: {name}")
        return self._scripts[name](self, keys, args)

    # ------------------------------------------------------------------
    # admin / ops
    # ------------------------------------------------------------------
    def keys(self, pattern: str = "*") -> list[str]:
        all_keys = [k for k in (self._str | self._hashes | self._lists
                                | self._sets | self._zsets)]
        import fnmatch
        return [k for k in sorted(all_keys) if fnmatch.fnmatchcase(k, pattern)]

    def scan(self, cursor: int = 0, match: str = "*", count: int = 10) -> tuple[int, list[str]]:
        """Non-blocking cursor-based scan (simulated: returns one batch per call)."""
        import fnmatch
        all_keys = [k for k in (self._str | self._hashes | self._lists
                                | self._sets | self._zsets)]
        batch = [k for k in sorted(all_keys)[cursor:] if fnmatch.fnmatchcase(k, match)][:count]
        next_cursor = cursor + len(batch)
        if next_cursor >= len(all_keys):
            next_cursor = 0
        return next_cursor, batch

    def dbsize(self) -> int:
        return len(self._str) + len(self._hashes) + len(self._lists) \
            + len(self._sets) + len(self._zsets)

    def flushall(self) -> None:
        self._str.clear()
        self._expiry.clear()
        self._hashes.clear()
        self._lists.clear()
        self._sets.clear()
        self._zsets.clear()
        self._access.clear()

    def set_maxmemory(self, maxmemory: int, policy: str = "noeviction") -> None:
        """Simulate maxmemory + maxmemory-policy. Policies: noeviction,
        allkeys-lru, volatile-ttl."""
        self._maxmemory = maxmemory
        self._eviction_policy = policy


def get_client(clock: Optional[Callable[[], float]] = None) -> RedisClient:
    """Return a client. Stand-in by default (deterministic, no server needed).

    Set REDIS_REAL=1 to attempt a real redis-py client against REDIS_URL
    (default redis://127.0.0.1:6379/0). Falls back to the stand-in if the
    module or a reachable server is missing — never crashes.
    """
    if os.environ.get("REDIS_REAL") == "1":
        try:
            import redis as real_redis  # type: ignore
            from redis.exceptions import RedisError  # type: ignore
            client = real_redis.Redis.from_url(
                os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0"),
                socket_connect_timeout=2, socket_timeout=2,
            )
            client.ping()
            return client  # type: ignore
        except Exception:
            pass
    return RedisClient(clock=clock)
