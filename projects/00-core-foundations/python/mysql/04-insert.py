"""
W3Schools Python Tutorial - MySQL 04: Insert Data
============================================
Topics: INSERT single/multiple, parameterized queries, executemany, lastrowid

Run: python 04-insert.py
Reference: https://www.w3schools.com/python/python_mysql_insert.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        age INTEGER,
        grade TEXT
    )
""")
print("Table 'students' created for INSERT examples.")
print()

# ============================================================
# Section: Single Row INSERT
# ============================================================

# Example 1: Basic INSERT with specific columns
cursor.execute(
    "INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
    ("Alice Johnson", "alice@example.com", 20, "A")
)
conn.commit()
print(f"Inserted Alice. Rows affected: {cursor.rowcount}")
print()

# Example 2: INSERT without specifying columns (must provide all values)
cursor.execute(
    "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
    (2, "Bob Smith", "bob@example.com", 22, "B")
)
conn.commit()
print(f"Inserted Bob. Rows affected: {cursor.rowcount}")
print()

# Example 3: INSERT with NULL values
cursor.execute(
    "INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
    ("Charlie Brown", None, 21, "C")
)
conn.commit()
print(f"Inserted Charlie with NULL email. Rows affected: {cursor.rowcount}")
print()

# ============================================================
# Section: Parameterized Queries
# ============================================================

# Example 4: Why use parameterized queries?
# WRONG: String concatenation (SQL injection risk!)
# cursor.execute("INSERT INTO students (name) VALUES ('" + user_input + "')")

# RIGHT: Parameterized queries (safe from SQL injection)
print("=== Parameterized Queries ===")
print("Always use ? placeholders, never string concatenation!")
print()

# Example 5: Multiple parameter formats
name = "Diana Prince"
email = "diana@example.com"
age = 25
grade = "A"

# Tuple parameters (most common)
cursor.execute(
    "INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
    (name, email, age, grade)
)
conn.commit()
print(f"Inserted Diana using tuple parameters.")
print()

# ============================================================
# Section: executemany for Bulk INSERT
# ============================================================

# Example 6: Insert multiple rows at once
students_data = [
    ("Eve Adams", "eve@example.com", 19, "B"),
    ("Frank Miller", "frank@example.com", 23, "A"),
    ("Grace Lee", "grace@example.com", 20, "C"),
    ("Henry Wilson", "henry@example.com", 21, "B"),
    ("Ivy Chen", "ivy@example.com", 22, "A"),
]

cursor.executemany(
    "INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
    students_data
)
conn.commit()
print(f"Inserted {len(students_data)} students using executemany.")
print(f"Rows affected: {cursor.rowcount}")
print()

# ============================================================
# Section: Getting Last Inserted Row ID
# ============================================================

# Example 7: lastrowid gets the last inserted row's ID
cursor.execute(
    "INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
    ("Jack Ryan", "jack@example.com", 24, "A")
)
conn.commit()
last_id = cursor.lastrowid
print(f"Last inserted row ID: {last_id}")
print()

# Example 8: Getting multiple lastrowid values
cursor.execute("INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
               ("Kate Bishop", "kate@example.com", 20, "B"))
id1 = cursor.lastrowid
cursor.execute("INSERT INTO students (name, email, age, grade) VALUES (?, ?, ?, ?)",
               ("Leo Messi", "leo@example.com", 22, "A"))
id2 = cursor.lastrowid
conn.commit()
print(f"Inserted Kate (ID={id1}) and Leo (ID={id2})")
print()

# ============================================================
# Section: INSERT with Defaults
# ============================================================

# Example 9: Let columns use default values
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        status TEXT DEFAULT 'pending'
    )
""")

# Only specify product — quantity and status use defaults
cursor.execute("INSERT INTO orders (product) VALUES (?)", ("Laptop",))
conn.commit()

cursor.execute("SELECT * FROM orders")
row = cursor.fetchone()
print(f"Order with defaults: product={row[1]}, qty={row[2]}, status={row[3]}")
print()

# ============================================================
# Section: INSERT Or Replace
# ============================================================

# Example 10: INSERT OR REPLACE (REPLACE in MySQL)
cursor.execute("""
    CREATE TABLE config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
""")

cursor.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("theme", "dark"))
conn.commit()
print("Inserted: theme=dark")

# This replaces the existing row
cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ("theme", "light"))
conn.commit()
print("Replaced: theme=light")

cursor.execute("SELECT * FROM config")
print(f"Current config: {cursor.fetchall()}")
print()

# ============================================================
# Section: Verifying Inserted Data
# ============================================================

# Example 11: Verify all inserted rows
print("=== All Students in Database ===")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(f"  ID={row[0]}, Name={row[1]}, Email={row[2]}, Age={row[3]}, Grade={row[4]}")
print(f"\nTotal students: {cursor.execute('SELECT COUNT(*) FROM students').fetchone()[0]}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 12: Drop tables
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS config")
conn.commit()
print("Tables dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. Use INSERT INTO table (cols) VALUES (?, ?, ?) for single rows")
print("2. Always use parameterized queries (?) to prevent SQL injection")
print("3. Use executemany() for bulk inserts with list of tuples")
print("4. cursor.lastrowid gets the ID of the last inserted row")
print("5. cursor.rowcount shows how many rows were affected")
print("6. Use DEFAULT values for columns not specified in INSERT")
print("7. INSERT OR REPLACE updates existing rows with same PRIMARY KEY")
print("8. Commit after INSERT to save changes permanently")
print("=" * 60)

# Close connection
conn.close()
