"""
Challenge 01: relational-model — Reference Solution
====================================================
"""

import sqlite3


def create_relational_schema(conn: sqlite3.Connection) -> list[str]:
    """Build the schema: students, courses, enrollments (junction).

    Composite PK on enrollments; FKs to both parents; FK enforcement on.
    """
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    conn.execute("CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT UNIQUE)")
    conn.execute(
        "CREATE TABLE enrollments ("
        "student_id INTEGER REFERENCES students(id),"
        "course_id INTEGER REFERENCES courses(id),"
        "PRIMARY KEY (student_id, course_id))"
    )
    return sorted(
        r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    )


def enforce_keys(conn: sqlite3.Connection) -> dict:
    """Insert samples and prove uniqueness + FK enforcement."""
    conn.execute("PRAGMA foreign_keys = ON")
    result = {"rows": 0, "dup_rejected": False, "orphan_rejected": False}
    conn.executemany("INSERT INTO students (name) VALUES (?)", [("ana",), ("bob",)])
    conn.executemany("INSERT INTO courses (title) VALUES (?)", [("sql",), ("ml",)])

    try:
        conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (1, 1))
    except sqlite3.IntegrityError:
        pass
    result["rows"] = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]

    try:
        conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (1, 1))
    except sqlite3.IntegrityError:
        result["dup_rejected"] = True

    try:
        conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (999, 1))
    except sqlite3.IntegrityError:
        result["orphan_rejected"] = True

    return result


def purge_abandoned_courses(conn: sqlite3.Connection) -> list[str]:
    """Delete courses with no enrollments (NULL-safe)."""
    conn.execute(
        "DELETE FROM courses WHERE NOT EXISTS "
        "(SELECT 1 FROM enrollments e WHERE e.course_id = courses.id)"
    )
    return [
        r[0] for r in conn.execute("SELECT title FROM courses ORDER BY title")
    ]
