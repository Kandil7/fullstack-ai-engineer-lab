"""
Postgres — 05: Transactions and MVCC
==============================================
Topics: MVCC, snapshot isolation, SERIALIZABLE and retry loops, SELECT FOR UPDATE,
        advisory locks, bloat and VACUUM

Why this matters for AI/backend engineering:
    A feature store that assigns ids, a job queue that claims work items,
    an experiment ledger that must not double-count: all of them are
    concurrency problems hiding behind innocent UPDATEs. MVCC is why
    readers never block writers in Postgres — and why your "safe"
    read-modify-write is NOT safe without the right isolation level and
    a retry loop.

Environment note:
    sqlite3 gives real BEGIN/COMMIT/ROLLBACK, savepoints, locked-busy
    errors and a measurable VACUUM (bloat) demo. Snapshot isolation and
    SERIALIZABLE retry are demonstrated with WAL mode + busy_timeout and
    the guarded real-Postgres section.

Run:      python 05-transactions-mvcc.py
Verify:   python 05-transactions-mvcc.py --verify
Reference: https://www.postgresql.org/docs/current/mvcc.html
"""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import threading
import time
from typing import Callable


# ============================================================
# 1. ACID in one breath — BEGIN, COMMIT, ROLLBACK
# ============================================================
# A transaction groups statements so they all apply or none do. In
# sqlite3 (like Postgres), BEGIN starts one; COMMIT makes it visible;
# ROLLBACK undoes it. In-memory sqlite3 defaults to autocommit per
# statement, so wrap multi-step work explicitly.

# Example 1: rollback undoes the whole batch
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE evals (id INTEGER PRIMARY KEY, metric TEXT, value REAL)")
try:
    with conn:                                # commit on success
        conn.execute("INSERT INTO evals (metric, value) VALUES (?, ?)", ("acc", 0.91))
        conn.execute("INSERT INTO evals (metric, value) VALUES (?, ?)", ("f1", 0.87))
    with conn:
        conn.execute("INSERT INTO evals (metric, value) VALUES (?, ?)", ("bad", 1.0))
        raise RuntimeError("abort mid-batch") # -> rollback
except RuntimeError:
    pass
rows = conn.execute("SELECT metric FROM evals ORDER BY metric").fetchall()
print(f"1. committed: {[r[0] for r in rows]}  (the aborted batch is gone)")
print()

# ============================================================
# 2. Savepoints — roll back PART of a transaction
# ============================================================
# Postgres: SAVEPOINT sp; ...; ROLLBACK TO sp; ...; RELEASE sp. sqlite3
# supports the same syntax. Use savepoints for checkpoints inside a long
# batch — e.g. per-batch ingestion of 10k rows where a bad row must not
# kill the whole load.

# Example 2: partial rollback keeps the good rows
conn.execute("CREATE TABLE ingest (id INTEGER PRIMARY KEY, batch TEXT)")
with conn:
    conn.execute("SAVEPOINT batch_1")
    conn.execute("INSERT INTO ingest (batch) VALUES (?)", ("row-1",))
    conn.execute("INSERT INTO ingest (batch) VALUES (?)", ("row-2",))
    conn.execute("ROLLBACK TO batch_1")       # undo batch_1 only
    conn.execute("INSERT INTO ingest (batch) VALUES (?)", ("row-3",))
count = conn.execute("SELECT COUNT(*) FROM ingest").fetchone()[0]
print(f"2. rows after partial rollback: {count} (row-1/row-2 undone)")
print()

# ============================================================
# 3. MVCC — readers don't block writers
# ============================================================
# Postgres MVCC: every transaction sees a SNAPSHOT of committed data as
# of its start; writers create new row versions instead of overwriting,
# so a reader never waits for a writer. sqlite3 reproduces this with WAL
# mode: the reader keeps reading the snapshot while another connection
# writes. (In-memory :memory: cannot share across connections — use a
# temp FILE database.)

# Example 3: WAL reader sees its snapshot while a writer commits
fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)
try:
    a = sqlite3.connect(db_path)
    b = sqlite3.connect(db_path)
    a.execute("PRAGMA journal_mode=WAL")
    a.execute("CREATE TABLE stats (k TEXT PRIMARY KEY, v INTEGER)")
    a.execute("INSERT INTO stats VALUES ('rows', 0)")
    a.commit()
    # reader B opens a read transaction (snapshot)
    b.execute("BEGIN")
    before = b.execute("SELECT v FROM stats WHERE k = 'rows'").fetchone()[0]
    # writer A commits a change — B's snapshot does not move
    a.execute("UPDATE stats SET v = 100 WHERE k = 'rows'")
    a.commit()
    after_snapshot = b.execute("SELECT v FROM stats WHERE k = 'rows'").fetchone()[0]
    b.execute("COMMIT")
    after_commit = b.execute("SELECT v FROM stats WHERE k = 'rows'").fetchone()[0]
    print(f"3. MVCC snapshot: before={before}, during txn={after_snapshot}, after commit={after_commit}")
finally:
    a.close()
    b.close()
    os.remove(db_path)  # Windows: only after both connections are closed
print()

# ============================================================
# 4. Lost updates — why read-modify-write needs care
# ============================================================
# Two transactions both read v=0, both add 1, both write v=1: one update
# is lost. Postgres' READ COMMITTED default does NOT stop this; the
# fixes are SELECT ... FOR UPDATE (lock the row) or SERIALIZABLE +
# retry. sqlite3 demonstrates the failure with two writers and
# busy_timeout, then the retry loop that production code needs.

# Example 4: retry loop for a contended update (busy -> retry)
def update_with_retry(
    db_path: str, key: str, max_attempts: int = 12
) -> int:
    """Increment key inside a transaction, retrying on 'database is locked'.

    WAL mode + a busy timeout makes writers WAIT instead of failing
    instantly; the retry loop is the backstop for the residual
    SQLITE_BUSY that even WAL can produce under heavy contention.
    """
    for attempt in range(1, max_attempts + 1):
        conn = sqlite3.connect(db_path, timeout=0.5)
        conn.execute("PRAGMA busy_timeout=500")
        try:
            conn.execute("BEGIN IMMEDIATE")
            v = conn.execute("SELECT v FROM stats WHERE k = ?", (key,)).fetchone()[0]
            conn.execute("UPDATE stats SET v = ? WHERE k = ?", (v + 1, key))
            conn.execute("COMMIT")
            return v + 1
        except sqlite3.OperationalError:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.OperationalError:
                pass
            time.sleep(0.01)  # back off before retrying
        finally:
            conn.close()
    raise RuntimeError(f"could not update {key} after {max_attempts} attempts")


fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)
try:
    base = sqlite3.connect(db_path)
    base.execute("CREATE TABLE stats (k TEXT PRIMARY KEY, v INTEGER)")
    base.execute("INSERT INTO stats VALUES ('counter', 0)")
    base.commit()
    base.close()
    # WAL: concurrent writers serialize with busy-wait instead of failing
    tune = sqlite3.connect(db_path)
    tune.execute("PRAGMA journal_mode=WAL")
    tune.execute("CREATE TABLE IF NOT EXISTS stats (k TEXT PRIMARY KEY, v INTEGER)")
    tune.close()
    # Two threads hammering the same row — retries make it converge
    results: list[int] = []
    def worker() -> None:
        results.append(update_with_retry(db_path, "counter"))
    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    final = sqlite3.connect(db_path)
    try:
        v = final.execute("SELECT v FROM stats WHERE k = 'counter'").fetchone()[0]
    finally:
        final.close()
    print(f"4. 4 contended increments, final counter = {v} (no lost update)")
finally:
    try:
        os.remove(db_path)
    except OSError:
        pass  # Windows: file may still be open briefly
print()

# ============================================================
# 5. Advisory locks and SELECT FOR UPDATE (real Postgres SQL)
# ============================================================
# SELECT ... FOR UPDATE locks the matched ROWS until commit — the tool
# for claim-job / claim-slot patterns. pg_advisory_lock(key) locks a
# bigint APPLICATION-level key — the tool for "only one worker runs
# this reindex" without touching table rows. The real SQL lives in the
# guarded section; the pattern here is the API shape.

# Example 5: single-writer gate in pure Python (advisory-lock shape)
_gate = threading.Lock()
def exclusive_reindex() -> str:
    """One worker at a time — advisory lock analog (pg_advisory_lock)."""
    if not _gate.acquire(blocking=False):
        return "skipped: another worker holds the lock"
    try:
        return "reindexed"
    finally:
        _gate.release()


print(f"5. advisory-lock shape: {exclusive_reindex()}")
print()

# ============================================================
# 6. Bloat and VACUUM — dead row versions cost you
# ============================================================
# MVCC leaves DEAD row versions around; bloat grows the table file.
# Postgres VACUUM reclaims space (and autovacuum does it for you).
# sqlite3 VACUUM does the same; we measure the file size shrinking.

# Example 6: measure bloat, then VACUUM it away
fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)
try:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE big (id INTEGER PRIMARY KEY, payload TEXT)")
    conn.executemany(
        "INSERT INTO big (payload) VALUES (?)",
        [("x" * 200,) for _ in range(2000)],
    )
    conn.commit()
    size_before = os.path.getsize(db_path)
    # delete 90% — the file does not shrink (dead space stays)
    conn.execute("DELETE FROM big WHERE id > 200")
    conn.commit()
    size_deleted = os.path.getsize(db_path)
    conn.execute("VACUUM")
    size_vacuumed = os.path.getsize(db_path)
    print(f"6. file: after insert={size_before}B, after delete={size_deleted}B, after VACUUM={size_vacuumed}B")
    print("   VACUUM reclaimed:", size_deleted - size_vacuumed, "bytes")
    conn.close()
    os.remove(db_path)
except OSError:
    pass  # cleanup raced on Windows; the demo already printed
print()

# ============================================================
# 7. Real Postgres transactions (guarded — skips when no server)
# ============================================================
def pg_demo() -> None:
    """SERIALIZABLE + retry, SELECT FOR UPDATE, advisory lock; [skip] when down."""
    dsn = os.environ.get(
        "PGDSN", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    try:
        import psycopg
    except ImportError:
        print("[skip] psycopg not installed — pip install 'psycopg[binary]'")
        return
    try:
        with psycopg.connect(dsn, connect_timeout=1) as pg:
            with pg.cursor() as cur:
                cur.execute("CREATE TEMP TABLE counters (k text primary key, v int)")
                cur.execute("INSERT INTO counters VALUES (%s, %s)", ("c", 0))
                pg.commit()
                # SERIALIZABLE with retry loop on serialization_failure (40001)
                for attempt in range(3):
                    try:
                        cur.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
                        cur.execute("SELECT v FROM counters WHERE k = %s", ("c",))
                        v = cur.fetchone()[0]
                        cur.execute("UPDATE counters SET v = %s WHERE k = %s", (v + 1, "c"))
                        pg.commit()
                        break
                    except psycopg.errors.SerializationFailure:
                        pg.rollback()  # 40001 — retry the whole transaction
                else:
                    raise RuntimeError("serializable retries exhausted")
                # SELECT FOR UPDATE — row lock for claim patterns
                cur.execute("BEGIN")
                cur.execute("SELECT v FROM counters WHERE k = %s FOR UPDATE", ("c",))
                cur.execute("UPDATE counters SET v = v + 1 WHERE k = %s", ("c",))
                pg.commit()
                # Advisory lock — single-worker gate, no rows touched
                cur.execute("SELECT pg_try_advisory_lock(%s)", (42,))
                print("7. real Postgres: serializable+retry ok, FOR UPDATE ok,",
                      "advisory lock acquired:", cur.fetchone()[0] is True)
                cur.execute("SELECT pg_advisory_unlock(%s)", (42,))
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
# MISTAKE: read-then-write without FOR UPDATE at READ COMMITTED -> lost
#   update; CORRECT: SELECT ... FOR UPDATE or SERIALIZABLE + retry
#
# MISTAKE: no retry loop around SERIALIZABLE -> random 40001 failures in
#   prod; CORRECT: catch serialization_failure, rollback, back off, retry
#
# MISTAKE: holding a transaction open across a network call -> minutes of
#   locks; CORRECT: short transactions; do I/O outside the transaction
#
# MISTAKE: never VACUUMing (or no autovacuum) -> table bloat; CORRECT:
#   autovacuum + monitoring; VACUUM FULL for aggressive shrink
#
# MISTAKE: catching ALL errors and retrying -> retrying real bugs forever;
#   CORRECT: retry only 40001/40P01 (serialization/deadlock)

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. ROLLBACK undoes the aborted batch
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("CREATE TABLE e (id INTEGER PRIMARY KEY, m TEXT)")
        try:
            with conn:
                conn.execute("INSERT INTO e (m) VALUES ('a')")
                raise RuntimeError("abort")
        except RuntimeError:
            pass
        assert conn.execute("SELECT COUNT(*) FROM e").fetchone()[0] == 0, \
            "rollback must undo the batch"

        # 2. Savepoints roll back only their own work
        with conn:
            conn.execute("SAVEPOINT sp1")
            conn.execute("INSERT INTO e (m) VALUES ('x')")
            conn.execute("ROLLBACK TO sp1")
            conn.execute("INSERT INTO e (m) VALUES ('y')")
        rows = [r[0] for r in conn.execute("SELECT m FROM e ORDER BY m").fetchall()]
        assert rows == ["y"], "ROLLBACK TO must discard only the savepoint work"
    finally:
        conn.close()

    # 3. WAL snapshot: a reader inside a transaction sees pre-commit state
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        a = sqlite3.connect(db_path)
        b = sqlite3.connect(db_path)
        a.execute("PRAGMA journal_mode=WAL")
        a.execute("CREATE TABLE s (k TEXT PRIMARY KEY, v INTEGER)")
        a.execute("INSERT INTO s VALUES ('k', 1)")
        a.commit()
        b.execute("BEGIN")
        before = b.execute("SELECT v FROM s WHERE k = 'k'").fetchone()[0]
        a.execute("UPDATE s SET v = 2 WHERE k = 'k'")
        a.commit()
        during = b.execute("SELECT v FROM s WHERE k = 'k'").fetchone()[0]
        b.execute("COMMIT")
        after = b.execute("SELECT v FROM s WHERE k = 'k'").fetchone()[0]
        assert (before, during, after) == (1, 1, 2), \
            "WAL snapshot must freeze the read view until COMMIT"
        a.close()
        b.close()
    finally:
        try:
            os.remove(db_path)
        except OSError:
            pass

    # 4. Retry loop converges under contention (no lost update)
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        base = sqlite3.connect(db_path)
        base.execute("CREATE TABLE stats (k TEXT PRIMARY KEY, v INTEGER)")
        base.execute("INSERT INTO stats VALUES ('counter', 0)")
        base.commit()
        base.close()
        tune = sqlite3.connect(db_path)
        tune.execute("PRAGMA journal_mode=WAL")
        tune.close()
        results: list[int] = []
        def worker() -> None:
            results.append(update_with_retry(db_path, "counter"))
        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        final = sqlite3.connect(db_path)
        try:
            v = final.execute("SELECT v FROM stats WHERE k = 'counter'").fetchone()[0]
        finally:
            final.close()
        assert v == 4, f"4 increments must land, got {v}"
        assert sorted(results) == [1, 2, 3, 4], "increments must be unique"
    finally:
        try:
            os.remove(db_path)
        except OSError:
            pass

    # 5. VACUUM measurably shrinks the file after mass DELETE
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE b (id INTEGER PRIMARY KEY, payload TEXT)")
        conn.executemany(
            "INSERT INTO b (payload) VALUES (?)", [("y" * 200,) for _ in range(1500)]
        )
        conn.commit()
        size_insert = os.path.getsize(db_path)
        conn.execute("DELETE FROM b WHERE id > 150")
        conn.commit()
        size_deleted = os.path.getsize(db_path)
        conn.execute("VACUUM")
        size_vacuumed = os.path.getsize(db_path)
        assert size_deleted >= size_insert, "file must not shrink on DELETE alone"
        assert size_vacuumed < size_deleted, "VACUUM must reclaim dead space"
        conn.close()
    finally:
        try:
            os.remove(db_path)
        except OSError:
            pass

    # 6. Advisory-lock shape: second caller is refused, not blocked
    assert exclusive_reindex() == "reindexed", "first worker must run"
    _gate.acquire(blocking=False)
    try:
        assert exclusive_reindex().startswith("skipped"), \
            "second worker must be refused while the lock is held"
    finally:
        _gate.release()

    print("[OK] 05-transactions-mvcc: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. BEGIN/COMMIT/ROLLBACK make a batch atomic")
        print("2. Savepoints allow partial rollback")
        print("3. MVCC snapshots let readers ignore writers")
        print("4. Read-modify-write needs FOR UPDATE or SERIALIZABLE + retry")
        print("5. Dead row versions bloat files; VACUUM reclaims")
        _verify()          # always runs, so plain execution is also a test
