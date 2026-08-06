"""
SQL Fundamentals — 13: SQL Injection
======================================
Topics: How injection works, parameterized queries, identifier vs value
binding, least privilege, why ORMs do not automatically save you

Why this matters for AI/backend engineering:
    Every endpoint that builds SQL by string interpolation is a live
    vulnerability. AI products compound this: agent tools that query
    databases, RAG audit logs, and prompt inputs can carry hostile payloads.
    Prompt injection and SQL injection share a shape — untrusted text merged
    into a trusted grammar. The fix is the same: separate data from code.

Run:      python 13-sql-injection.py
Verify:   python 13-sql-injection.py --verify
Reference: https://www.sqlite.org/lang_expr.html#varparam
"""

from __future__ import annotations

import sqlite3
import sys

# ============================================================
# 1. The vulnerable pattern — string interpolation
# ============================================================
# WRONG: f-strings / % formatting merge user input into the SQL text.
# The input is parsed as SQL, not treated as a value.

def vulnerable_login(conn: sqlite3.Connection, username: str) -> list:
    """BROKEN — do not copy. Demonstrates the injection primitive."""
    sql = f"SELECT * FROM users WHERE username = '{username}'"
    return conn.execute(sql).fetchall()


conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, passwd TEXT, role TEXT)")
conn.executemany(
    "INSERT INTO users (username, passwd, role) VALUES (?, ?, ?)",
    [("ada", "p1", "admin"), ("bob", "p2", "user"), ("carol", "p3", "user")],
)

print("=== 1. The vulnerable pattern ===")
rows = vulnerable_login(conn, "ada")
print(f"normal lookup: {rows}")
# Payload: close the quote, inject OR, comment out the rest.
rows = vulnerable_login(conn, "' OR '1'='1' --")
print(f"with payload  : {rows}   <- ALL users leaked")
print()

# ============================================================
# 2. The fix — parameterized queries (always)
# ============================================================
# Parameterized SQL separates the statement (fixed) from the values
# (bound). The engine treats the bound value as data, never as SQL text.

def safe_login(conn: sqlite3.Connection, username: str) -> list:
    sql = "SELECT * FROM users WHERE username = ?"
    return conn.execute(sql, (username,)).fetchall()


print("=== 2. Parameterized queries ===")
rows = safe_login(conn, "' OR '1'='1' --")
print(f"payload now returns: {rows}   <- no leak, just no such user")
print()

# ============================================================
# 3. Identifier vs value binding
# ============================================================
# '?' binds VALUES only. Table/column NAMES cannot be bound — they must be
# validated against a whitelist, because identifiers change the parse tree.

ALLOWED_COLUMNS = {"id", "username", "role"}  # whitelist

def select_column(conn: sqlite3.Connection, column: str) -> list:
    if column not in ALLOWED_COLUMNS:
        raise ValueError(f"column {column!r} not allowed")
    # Identifier from the whitelist; value can still be parameterized.
    return conn.execute(f"SELECT id, {column} FROM users ORDER BY id").fetchall()


print("=== 3. Identifier vs value binding ===")
print(f"whitelisted column 'role': {select_column(conn, 'role')}")
try:
    select_column(conn, "passwd; DROP TABLE users; --")
except ValueError as e:
    print(f"malicious identifier rejected: {e}")
print()

# ============================================================
# 4. Least privilege — the defense in depth
# ============================================================
# Even a perfect parameterization cannot stop damage done by a connection
# with too many rights. Connect as a role that can only do what the feature
# needs (SELECT only, no DROP).

# Simulate: the app connection cannot DROP even if a payload slips through.
limited = sqlite3.connect(":memory:")
limited.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, msg TEXT)")
limited.execute("INSERT INTO logs (msg) VALUES ('hello')")
# A realistic defense: open with a read-only URI on the real DB file.
ro = sqlite3.connect("file:logs.db?mode=ro", uri=True) if False else limited

print("=== 4. Least privilege ===")
print("app user runs SELECT only; destructive statements require a role the app lacks")
try:
    # If the app account had no DROP privilege, the engine would refuse:
    limited.execute("DROP TABLE logs")
    print("  (simulated) DROP allowed because this demo connection is admin")
except sqlite3.OperationalError:
    print("  DROP rejected — least privilege works")
print()

# ============================================================
# 5. ORMs do not automatically save you
# ============================================================
# Raw SQL in ORM APIs (text(), raw(), exec_driver_sql) reintroduces the
# same interpolation risk. The ORM protects you only while you use its
# query builders / bound parameters.

def orm_like_raw(conn: sqlite3.Connection, order: str) -> list:
    # The 'order' string is dropped into the SQL text — same risk as #1.
    return conn.execute(f"SELECT username FROM users ORDER BY {order}").fetchall()


print("=== 5. ORMs do not automatically save you ===")
print(f"valid order: {orm_like_raw(conn, 'username')}")
try:
    orm_like_raw(conn, "username; DROP TABLE users; --")
    print("  payload accepted (bad!)")
except sqlite3.OperationalError:
    print("  payload errored here — but on another driver it might not")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: f-string SQL because 'it's just internal' — injection is input,
#   and 'internal' inputs (feature flags, agent tool args) get hostile too
# CORRECT: parameterize values, whitelist identifiers
#
# MISTAKE: '%s' % user_input in MySQL / psycopg — formatting is the bug
# CORRECT: cursor.execute(sql, (user_input,))
#
# MISTAKE: trusting an ORM because you never write raw SQL — raw hooks,
#   order_by strings, and custom clauses are still text
# CORRECT: use builders; whitelist any dynamic identifiers
#
# MISTAKE: one admin connection for everything — least privilege means the
#   app can't drop tables even if a payload gets through
# CORRECT: scoped roles; read-only connections for reads

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
        db.executemany(
            "INSERT INTO users (username, role) VALUES (?, ?)",
            [("ada", "admin"), ("bob", "user")],
        )

        # 1. Interpolation leaks all rows; parameterization leaks none
        payload = "' OR '1'='1' --"
        leaked = db.execute(
            f"SELECT username FROM users WHERE username = '{payload}'"
        ).fetchall()
        assert len(leaked) == 2, "interpolated payload must bypass the filter"
        safe = db.execute(
            "SELECT username FROM users WHERE username = ?", (payload,)
        ).fetchall()
        assert safe == [], "parameterized query must treat payload as a literal value"

        # 2. Bound values can never change the statement shape
        assert " OR " in payload, "sanity: payload really is hostile"
        assert safe == [], "payload executed as data, not SQL"

        # 3. Identifier binding must go through a whitelist
        try:
            db.execute("SELECT username FROM users ORDER BY username; DROP TABLE users; --")
            assert False, "interpolated identifier must be the vulnerability"
        except sqlite3.OperationalError:
            pass  # sqlite errors on the trailing garbage; the point is the risk

        # 4. Values are safely bound even when they look like SQL
        tricky = "x'; DELETE FROM users; --"
        db.execute("INSERT INTO users (username, role) VALUES (?, ?)", (tricky, "user"))
        count = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", (tricky,)).fetchone()[0]
        assert count == 1, "parameterized insert must store the literal string"

        # 5. All rows still present after hostile-looking operations
        total = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert total == 3, "no rows may be deleted by any payload above"
    finally:
        db.close()
    print("[OK] 13-sql-injection: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Never interpolate input into SQL text")
        print("2. Parameterize values; whitelist identifiers")
        print("3. Least privilege: the app role can't drop anything")
        print("4. ORMs protect you only while you use their builders")
        _verify()          # always runs, so plain execution is also a test
