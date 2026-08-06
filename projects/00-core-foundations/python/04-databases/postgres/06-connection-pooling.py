"""
Postgres — 06: Connection Pooling
==============================================
Topics: why pooling is mandatory, mini-pool implementation, sizing math, PgBouncer,
        pool exhaustion, the serverless pooling problem

Why this matters for AI/backend engineering:
    Postgres caps connections (default 100). Every FastAPI worker x every
    inference replica x a query-heavy feature store blows that budget in
    seconds WITHOUT a pool. Pooling is not an optimization — it is what
    keeps the database alive under load, and pool sizing is the difference
    between 5ms p95 and a queue that melts.

Environment note:
    The pool itself is pure Python (thread-safe, deterministic) and runs
    against sqlite3. The real psycopg_pool section is guarded and skips
    without a server.

Run:      python 06-connection-pooling.py
Verify:   python 06-connection-pooling.py --verify
Reference: https://www.psycopg.org/psycopg3/docs/advanced/pool.html
"""

from __future__ import annotations

import os
import queue
import sqlite3
import sys
import tempfile
import threading
import time
from typing import Any, Callable


# ============================================================
# 1. Why pooling is mandatory
# ============================================================
# Opening a connection costs a TCP round trip + auth + backend process
# spawn (Postgres forks a process per connection!). At 50 req/s that is
# 50 handshakes per second — and at peak, max_connections is exhausted,
# after which NEW queries queue or fail. A pool keeps N connections open
# and hands them out. Rule of thumb sizing:
#   pool_size = peak_concurrency * (query_time / request_time)
# e.g. 200 concurrent users, 10ms query per 100ms request -> 20.

# Example 1: measure the connect-vs-pool difference (sqlite3 as stand-in)
def measure(label: str, work: Callable[[], Any], n: int = 300) -> float:
    """Return wall time in ms for n operations."""
    start = time.perf_counter()
    work()
    return (time.perf_counter() - start) * 1000.0


# ============================================================
# 2. A mini connection pool — acquire / release / timeout
# ============================================================
# The pool keeps a queue of open connections. acquire() waits for a free
# one (bounded by timeout); release() returns it. Sizes are bounded so
# the database never sees more than `max_size` connections — this is
# exactly what psycopg_pool and PgBouncer do, minus the polish.

class MiniPool:
    """Thread-safe bounded pool of sqlite3 connections.

    Complexity: acquire/release O(1) amortized; waits bounded by timeout.
    """

    def __init__(
        self,
        db_path: str,
        max_size: int = 3,
        timeout: float = 0.5,
        connect: Callable[[str], sqlite3.Connection] | None = None,
    ) -> None:
        self._db_path = db_path
        self._max_size = max_size
        self._timeout = timeout
        # check_same_thread=False: sqlite3 connections are pinned to their
        # creating thread by default; a pool hands connections to ANY
        # thread. Real psycopg connections are not thread-pinned, so this
        # matches production behavior. The pool's acquire/release contract
        # still guarantees one holder at a time. WAL + busy_timeout keep
        # concurrent writers from blocking each other for seconds.
        self._connect = connect or self._default_connect
        self._free: queue.Queue[sqlite3.Connection] = queue.Queue()
        self._open_count = 0
        self._lock = threading.Lock()

    @staticmethod
    def _default_connect(db_path: str) -> sqlite3.Connection:
        conn = sqlite3.connect(db_path, check_same_thread=False, timeout=2.0)
        # WAL is a persistent database property — set once at setup, not
        # per connection. busy_timeout makes writers WAIT (bounded) for
        # the lock instead of failing instantly.
        conn.execute("PRAGMA busy_timeout=2000")
        return conn

    def acquire(self) -> sqlite3.Connection:
        """Return a connection, opening one if the pool is not full."""
        try:
            return self._free.get(timeout=self._timeout)
        except queue.Empty:
            with self._lock:
                if self._open_count < self._max_size:
                    self._open_count += 1
                    return self._connect(self._db_path)
            raise TimeoutError(
                f"pool exhausted: {self._max_size} connections in use"
            )

    def release(self, conn: sqlite3.Connection) -> None:
        """Return a connection to the pool for reuse."""
        self._free.put(conn)

    def close(self) -> None:
        """Close every pooled connection."""
        while not self._free.empty():
            self._free.get().close()
        self._open_count = 0


# Example 2: pool serves 12 pieces of work with only 3 connections
fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)
try:
    # WAL once, schema once — the pool then only serves INSERTs
    setup = sqlite3.connect(db_path)
    setup.execute("PRAGMA journal_mode=WAL")
    setup.execute("CREATE TABLE work (id INTEGER PRIMARY KEY, v INTEGER)")
    setup.commit()
    setup.close()

    pool = MiniPool(db_path, max_size=3, timeout=2.0)
    results: list[int] = []
    lock = threading.Lock()


    def do_work(i: int) -> None:
        """Run one 'query' through the pool."""
        conn = pool.acquire()
        try:
            conn.execute("INSERT INTO work (v) VALUES (?)", (i,))
            conn.commit()
            with lock:
                results.append(i)
        finally:
            pool.release(conn)   # ALWAYS release — even on error


    threads = [threading.Thread(target=do_work, args=(i,)) for i in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"2. pool(max_size=3) served {len(results)} requests with only 3 connections")
    pool.close()
    print()

    # ============================================================
    # 3. Pool exhaustion — what happens when demand exceeds size
    # ============================================================
    # When all connections are busy, acquire() waits. If it waits longer
    # than `timeout`, the request FAILS — that is the failure mode to design
    # for: retry, shed load, or grow the pool (up to what the server allows).

    # Example 3: exhaustion demo — hold all 3, ask for a 4th
    pool2 = MiniPool(db_path, max_size=3, timeout=0.2)
    held: list[sqlite3.Connection] = [pool2.acquire() for _ in range(3)]
    try:
        pool2.acquire()   # 4th request -> must time out
        exhausted = False
    except TimeoutError:
        exhausted = True
    print(f"3. 4th request with pool of 3 and timeout 0.2s -> TimeoutError: {exhausted}")
    for c in held:
        pool2.release(c)
    pool2.close()
    print()
finally:
    try:
        os.remove(db_path)   # Windows: only after every connection is closed
    except OSError:
        pass

# ============================================================
# 4. Sizing math — the formula, worked
# ============================================================
# C = concurrency * (query_time / request_time). Too small -> queueing;
# too big -> server max_connections blowup. And remember: if you run
# N app replicas, multiply by N. 50 replicas x 20 each = 1000 -> beyond
# default Postgres -> PgBouncer territory.

# Example 4: worked example
def pool_size(concurrency: int, query_ms: float, request_ms: float) -> int:
    """Little's-law-style pool sizing (rounded up)."""
    size = concurrency * (query_ms / request_ms)
    return max(1, int(size) + (1 if size % 1 else 0))


print("4. sizing: 200 concurrent, 10ms query / 100ms request ->", end=" ")
print(pool_size(200, 10.0, 100.0), "connections")
print("   50 replicas x 20 ->", 50 * pool_size(200, 10.0, 100.0),
      "-> needs PgBouncer or per-replica pools")
print()

# ============================================================
# 5. PgBouncer — pooling OUTSIDE the app
# ============================================================
# PgBouncer sits between apps and Postgres and multiplexes thousands of
# client sessions onto a few real connections. Transaction pooling
# (default): a backend connection is held only for one transaction —
# perfect for HTTP services. Session pooling: held for the whole
# session — required for prepared statements and cursors. The price of
# transaction pooling: no session state, no long transactions.

# Example 5: multiplexing math
print("=== 5. PgBouncer ===")
print("   3000 app connections -> PgBouncer -> 50 real Postgres connections")
print("   transaction pooling: backend held only during one transaction")
print("   session pooling:     backend held for the whole session")
print()

# ============================================================
# 6. Serverless pooling — the cold-start trap
# ============================================================
# Serverless functions scale to 1000s of instances; each one opening its
# own pool means 1000s of connections and, after idle, hundreds of pools
# reconnecting at once (connection storm). Options: PgBouncer in front,
# or serverless-aware pools (psycopg_pool can run with min_size=0 and
# close connections when idle). Lambda-style compute plus Postgres is
# exactly where pooling architecture is decided BEFORE the incident.

# Example 6: the storm — many instances, all reconnect at once
print("=== 6. Serverless ===")
print("   100 idle functions wake up -> 100 simultaneous pool warmups")
print("   -> connection storm; solution: PgBouncer + min_size=0")
print()

# ============================================================
# 7. Real psycopg_pool (guarded — skips when no server)
# ============================================================
def pg_demo() -> None:
    """Real ConnectionPool against Postgres; [skip] when unavailable."""
    dsn = os.environ.get(
        "PGDSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    try:
        import psycopg
        from psycopg_pool import ConnectionPool
    except ImportError:
        print("[skip] psycopg/psycopg_pool not installed — pip install 'psycopg[binary]' 'psycopg-pool'")
        return
    try:
        with ConnectionPool(
            dsn, min_size=1, max_size=4, open=False, timeout=2
        ) as pool:
            pool.wait(timeout=2.0)
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT count(*) FROM pg_stat_activity")
                    print("7. psycopg_pool: min=1 max=4, active backends seen:", cur.fetchone()[0])
    except Exception as exc:  # noqa: BLE001
        print(
            "[skip] real Postgres demo: %s -- requires a Postgres server "
            "(install: docker compose up -d postgres)" % exc
        )


pg_demo()
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: opening a new connection per request -> handshake storm and
#   max_connections exhaustion; CORRECT: pool, sized with the formula
#
# MISTAKE: acquiring from the pool and never releasing (leak) -> pool
#   dries up silently; CORRECT: try/finally release, or with-block
#
# MISTAKE: pool.max_size x replicas > server max_connections -> mass
#   failures; CORRECT: size the pool per replica + PgBouncer if needed
#
# MISTAKE: infinite pool -> now Postgres is the queue; CORRECT: bounded
#   pool + timeout + load shedding + retries
#
# MISTAKE: session pooling when transaction pooling suffices -> fewer
#   real connections multiplexed; CORRECT: PgBouncer transaction mode
#   for stateless HTTP workloads

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        os.remove(db_path)
    except OSError:
        pass

    # 1. Pool serves more requests than it has connections
    setup = sqlite3.connect(db_path)
    setup.execute("PRAGMA journal_mode=WAL")
    setup.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER)")
    setup.commit()
    setup.close()
    pool = MiniPool(db_path, max_size=2, timeout=2.0)
    try:
        done: list[int] = []
        def worker(i: int) -> None:
            conn = pool.acquire()
            try:
                conn.execute("INSERT INTO t (v) VALUES (?)", (i,))
                conn.commit()
                done.append(i)
            finally:
                pool.release(conn)
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(done) == 6, "pool must serve all 6 requests"
        assert pool._open_count <= 2, "pool must never open more than max_size"
    finally:
        pool.close()

    # 2. Exhaustion raises TimeoutError instead of hanging
    pool2 = MiniPool(db_path, max_size=1, timeout=0.1)
    try:
        held = pool2.acquire()
        try:
            try:
                pool2.acquire()
                raised = False
            except TimeoutError:
                raised = True
            assert raised, "exhausted pool must raise TimeoutError"
        finally:
            pool2.release(held)
    finally:
        pool2.close()

    # 3. Sizing formula matches the worked examples
    assert pool_size(200, 10.0, 100.0) == 20, "sizing formula must give 20"
    assert pool_size(100, 100.0, 100.0) == 100, "1:1 ratio keeps concurrency"
    assert pool_size(0, 10.0, 100.0) == 1, "sizing must floor at 1"

    # 4. Release returns the connection for reuse (acquire gets it back)
    pool3 = MiniPool(db_path, max_size=1)
    try:
        c1 = pool3.acquire()
        pool3.release(c1)
        c2 = pool3.acquire()
        assert c1 is c2, "released connection must be reusable"
        pool3.release(c2)
    finally:
        pool3.close()

    # 5. close() leaves no open pooled connections
    pool4 = MiniPool(db_path, max_size=2)
    try:
        c = pool4.acquire()
        pool4.release(c)
        pool4.close()
        assert pool4._open_count == 0, "close must drop the open count"
    finally:
        try:
            os.remove(db_path)
        except OSError:
            pass

    print("[OK] 06-connection-pooling: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Pools reuse connections; Postgres caps them at max_connections")
        print("2. Bounded acquire/release with timeout is the core contract")
        print("3. Exhaustion surfaces as TimeoutError - design for it")
        print("4. Size = concurrency x (query/request) ; multiply by replicas")
        print("5. PgBouncer multiplexes; serverless needs min_size=0 pools")
        _verify()          # always runs, so plain execution is also a test
