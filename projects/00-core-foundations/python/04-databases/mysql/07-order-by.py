"""
W3Schools Python Tutorial - MySQL 07: Order By
============================================
Topics: ORDER BY ASC/DESC, multi-column sort

Run: python 07-order-by.py
Reference: https://www.w3schools.com/python/python_mysql_order_by.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create and Populate Table
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT,
        score REAL
    )
""")

students = [
    (1, "Alice Johnson", 20, "A", 95.5),
    (2, "Bob Smith", 22, "B", 82.3),
    (3, "Charlie Brown", 19, "A", 91.7),
    (4, "Diana Prince", 21, "A", 98.2),
    (5, "Eve Adams", 20, "C", 75.8),
    (6, "Frank Miller", 23, "B", 88.1),
    (7, "Grace Lee", 19, "A", 94.6),
    (8, "Henry Wilson", 21, "C", 72.4),
    (9, "Ivy Chen", 22, "B", 85.9),
    (10, "Jack Ryan", 20, "A", 97.1),
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students)
conn.commit()
print(f"Table 'students' created with {len(students)} rows.")
print()

# ============================================================
# Section: ORDER BY - Default (ASC)
# ============================================================

# Example 1: ORDER BY with default ascending order
print("=== ORDER BY (Default ASC) ===")
cursor.execute("SELECT name, score FROM students ORDER BY score")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# ============================================================
# Section: ORDER BY ASC
# ============================================================

# Example 2: Explicit ascending order
print("=== ORDER BY score ASC ===")
cursor.execute("SELECT name, score FROM students ORDER BY score ASC")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# ============================================================
# Section: ORDER BY DESC
# ============================================================

# Example 3: Descending order
print("=== ORDER BY score DESC ===")
cursor.execute("SELECT name, score FROM students ORDER BY score DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# ============================================================
# Section: ORDER BY with LIMIT
# ============================================================

# Example 4: Top 3 students by score
print("=== Top 3 Students ===")
cursor.execute("SELECT name, score FROM students ORDER BY score DESC LIMIT 3")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  #{i}: {row[0]} ({row[1]})")
print()

# Example 5: Bottom 3 students by score
print("=== Bottom 3 Students ===")
cursor.execute("SELECT name, score FROM students ORDER BY score ASC LIMIT 3")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  #{i}: {row[0]} ({row[1]})")
print()

# ============================================================
# Section: Multi-Column ORDER BY
# ============================================================

# Example 6: Sort by multiple columns
print("=== Multi-Column Sort (grade ASC, score DESC) ===")
cursor.execute("SELECT name, grade, score FROM students ORDER BY grade ASC, score DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: Grade={row[1]}, Score={row[2]}")
print()

# Example 7: Sort with different directions per column
print("=== Mixed Sort Directions ===")
cursor.execute("""
    SELECT name, age, score FROM students
    ORDER BY age ASC, score DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: Age={row[1]}, Score={row[2]}")
print()

# ============================================================
# Section: ORDER BY with WHERE
# ============================================================

# Example 8: Filter and sort
print("=== WHERE + ORDER BY ===")
cursor.execute("""
    SELECT name, grade, score FROM students
    WHERE grade = 'A'
    ORDER BY score DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: Grade={row[1]}, Score={row[2]}")
print()

# ============================================================
# Section: ORDER BY with Aggregate Functions
# ============================================================

# Example 9: Sort by aggregate result
print("=== ORDER BY with COUNT ===")
cursor.execute("""
    SELECT grade, COUNT(*) as student_count
    FROM students
    GROUP BY grade
    ORDER BY student_count DESC
""")
for row in cursor.fetchall():
    print(f"  Grade {row[0]}: {row[1]} students")
print()

# ============================================================
# Section: ORDER BY with Expressions
# ============================================================

# Example 10: Sort by expression
print("=== ORDER BY Expression ===")
cursor.execute("SELECT name, score, score * 1.1 as bonus_score FROM students ORDER BY bonus_score DESC")
for row in cursor.fetchall():
    print(f"  {row[0]}: Score={row[1]}, Bonus={row[2]}")
print()

# ============================================================
# Section: NULL Values in ORDER BY
# ============================================================

# Example 11: NULL values ordering
print("=== NULL Values in ORDER BY ===")
cursor.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        priority INTEGER
    )
""")

cursor.executemany("INSERT INTO items VALUES (?, ?, ?)", [
    (1, "Item A", 3),
    (2, "Item B", None),
    (3, "Item C", 1),
    (4, "Item D", None),
    (5, "Item E", 2),
])
conn.commit()

cursor.execute("SELECT name, priority FROM items ORDER BY priority ASC")
print("  NULLs appear first in ascending order (sqlite3):")
for row in cursor.fetchall():
    print(f"    {row[0]}: priority={row[1]}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS items")
conn.commit()
print("Tables dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. ORDER BY sorts results; default is ascending (ASC)")
print("2. Use DESC for descending order")
print("3. ORDER BY col1 ASC, col2 DESC for multi-column sorting")
print("4. Combine with LIMIT for top/bottom N results")
print("5. Combine with WHERE for filtered sorted results")
print("6. Can sort by expressions (score * 1.1)")
print("7. NULL values sort differently based on database engine")
print("8. ORDER BY with GROUP BY sorts the grouped results")
print("=" * 60)

# Close connection
conn.close()
