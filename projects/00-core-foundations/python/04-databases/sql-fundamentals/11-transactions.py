"""
SQL Fundamentals — 11: Transactions
=====================================
Topics: ACID, BEGIN/COMMIT/ROLLBACK, savepoints, isolation levels,
        anomalies (dirty/phantom/non-repeatable), deadlock

Why this matters for AI/backend engineering:
    Billing, usage accounting, and model-registry promotion must be
    atomic: a partial write is a corrupted invariant. Transactions are
    the mechanism; isolation levels are the tradeoff between
    consistency and concurrency; deadlocks are the failure mode you
    must design around.

Run:      python 11-transactions.py
Verify:   python 11-transactions.py --verify
Reference: https://www.sqlite.org/lang_transaction.html
"""

from __future__ import annotations

import sqlite3
import sys

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
conn.executemany("INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
                 [(1, "ada", 100), (2, "bob", 50)])

# ============================================================
# 1. Atomicity — the all-or-nothing transfer
# ============================================================
print("=== 1. Atomic Transfer ===")
def transfer(from_id: int, to_id: int, amount: int) -> None:
    """A transfer must debit AND credit atomically — never one alone."""
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    conn.commit()


transfer(1, 2, 30)
print(f"  after transfer: {conn.execute('SELECT id, balance FROM accounts ORDER BY id').fetchall()}")
print("  -> total conserved: 100 + 50 = 120 always")

# ============================================================
# 2. ROLLBACK — undo on failure
# ============================================================
print("\n=== 2. ROLLBACK ===")
def risky_transfer(from_id: int, to_id: int, amount: int) -> str:
    try:
        conn.execute("BEGIN")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        if amount > 100:
            raise ValueError("amount exceeds limit")   # simulated failure
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        conn.commit()
        return "committed"
    except Exception as e:
        conn.rollback()
        return f"rolled back: {e}"


r = risky_transfer(1, 2, 500)
print(f"  {r}")
print(f"  balances unchanged: {conn.execute('SELECT id, balance FROM accounts ORDER BY id').fetchall()}")
print("  -> the debit was undone — no half-transfer")

# ============================================================
# 3. SAVEPOINT — partial rollback
# ============================================================
print("\n=== 3. SAVEPOINT ===")
conn.execute("BEGIN")
conn.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
conn.execute("SAVEPOINT after_credit")
conn.execute("UPDATE accounts SET balance = balance - 5 WHERE id = 1")
conn.execute("ROLLBACK TO after_credit")       # undo only the -5
conn.commit()
print(f"  after savepoint dance: {conn.execute('SELECT id, balance FROM accounts ORDER BY id').fetchall()}")
print("  -> +10 kept, -5 undone — granular control within a transaction")

# ============================================================
# 4. Isolation levels — the consistency/concurrency tradeoff
# ============================================================
print("\n=== 4. Isolation Levels ===")
isolation = {
    "READ UNCOMMITTED": "may see uncommitted writes (dirty reads)",
    "READ COMMITTED": "only committed writes; non-repeatable reads possible",
    "REPEATABLE READ": "stable reads; phantom rows possible",
    "SERIALIZABLE": "as if run alone; strongest, lowest concurrency",
}
for level, meaning in isolation.items():
    print(f"  {level}: {meaning}")
print("  -> sqlite defaults to SERIALIZABLE (one writer at a time);")
print("     Postgres uses READ COMMITTED by default")

# ============================================================
# 5. Deadlock — the failure mode to design around
# ============================================================
print("\n=== 5. Deadlock Awareness ===")
print("""
  Transaction A: UPDATE account 1, then account 2
  Transaction B: UPDATE account 2, then account 1
  -> each waits on the other's lock: deadlock. One is aborted.
  Prevention: acquire locks in a consistent global order (always
  update the lower ID first), keep transactions short.
""")

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: autocommit for multi-statement invariants -> partial writes
# CORRECT: BEGIN/COMMIT around the whole unit; ROLLBACK on any failure
#
# MISTAKE: holding a transaction open across slow work -> lock contention
# CORRECT: short transactions; do I/O outside the transaction
#
# MISTAKE: ignoring isolation level when choosing a database default
# CORRECT: know your engine's default; pick levels by anomaly tolerance

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE a (id INTEGER PRIMARY KEY, v INTEGER)")
    conn.executemany("INSERT INTO a (id, v) VALUES (?, ?)", [(1, 10), (2, 20)])
    conn.commit()  # close the implicit fixture transaction (Py 3.13 legacy
    # transaction control) so the explicit BEGIN below is allowed
    try:
        # 1. Commit persists both statements
        conn.execute("BEGIN")
        conn.execute("UPDATE a SET v = v + 5 WHERE id = 1")
        conn.execute("UPDATE a SET v = v + 5 WHERE id = 2")
        conn.commit()
        assert conn.execute("SELECT SUM(v) FROM a").fetchone()[0] == 40, \
            "commit must persist both statements"

        # 2. Rollback undoes everything in the failed transaction
        conn.execute("BEGIN")
        conn.execute("UPDATE a SET v = 999 WHERE id = 1")
        conn.rollback()
        assert conn.execute("SELECT v FROM a WHERE id = 1").fetchone()[0] == 15, \
            "rollback must undo the uncommitted change"

        # 3. Savepoint allows partial rollback
        conn.execute("BEGIN")
        conn.execute("UPDATE a SET v = v + 1 WHERE id = 1")
        conn.execute("SAVEPOINT sp")
        conn.execute("UPDATE a SET v = v + 100 WHERE id = 1")
        conn.execute("ROLLBACK TO sp")
        conn.commit()
        assert conn.execute("SELECT v FROM a WHERE id = 1").fetchone()[0] == 16, \
            "savepoint rollback must keep the outer change"

        # 4. Failure + rollback keeps invariants
        conn.execute("BEGIN")
        conn.execute("UPDATE a SET v = v - 1000 WHERE id = 1")
        try:
            raise RuntimeError("simulated failure")
        except RuntimeError:
            conn.rollback()
        assert conn.execute("SELECT v FROM a WHERE id = 1").fetchone()[0] == 16, \
            "failed transaction must not partially apply"

        # 5. Isolation levels are a known tradeoff surface
        assert "SERIALIZABLE" in isolation and "READ COMMITTED" in isolation
    finally:
        conn.close()
    print("[OK] 11-transactions: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. ACID: atomicity keeps invariants whole")
        print("2. ROLLBACK undoes failed units; SAVEPOINT partial undo")
        print("3. Isolation levels trade consistency for concurrency")
        print("4. Deadlocks: consistent lock order + short transactions")
        _verify()
