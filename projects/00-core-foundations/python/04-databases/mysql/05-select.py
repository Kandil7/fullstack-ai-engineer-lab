"""
W3Schools Python Tutorial - MySQL 05: Select Data
============================================
Topics: SELECT *, SELECT columns, fetchone/fetchall/fetchmany

Run: python 05-select.py
Reference: https://www.w3schools.com/python/python_mysql_select.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create and Populate Table
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL,
        hire_date TEXT
    )
""")

employees = [
    (1, "Alice Johnson", "Engineering", 85000, "2022-01-15"),
    (2, "Bob Smith", "Marketing", 65000, "2021-06-20"),
    (3, "Charlie Brown", "Engineering", 92000, "2020-03-10"),
    (4, "Diana Prince", "Sales", 72000, "2023-02-01"),
    (5, "Eve Adams", "Marketing", 68000, "2022-08-15"),
    (6, "Frank Miller", "Engineering", 95000, "2019-11-30"),
    (7, "Grace Lee", "Sales", 70000, "2021-04-25"),
    (8, "Henry Wilson", "HR", 60000, "2020-09-10"),
]

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)
conn.commit()
print(f"Table 'employees' created with {len(employees)} rows.")
print()

# ============================================================
# Section: SELECT * - All Columns
# ============================================================

# Example 1: Select all columns
print("=== SELECT * (All Columns) ===")
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
for row in rows:
    print(f"  {row}")
print()

# ============================================================
# Section: SELECT Specific Columns
# ============================================================

# Example 2: Select specific columns
print("=== SELECT Specific Columns ===")
cursor.execute("SELECT name, department FROM employees")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")
print()

# Example 3: Select with alias
print("=== Column Aliases ===")
cursor.execute("SELECT name AS employee_name, salary AS annual_salary FROM employees")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:,.2f}")
print()

# ============================================================
# Section: fetchone - Get Single Row
# ============================================================

# Example 4: fetchone returns one row at a time
print("=== fetchone() ===")
cursor.execute("SELECT * FROM employees")
first = cursor.fetchone()
print(f"  First row: {first}")
second = cursor.fetchone()
print(f"  Second row: {second}")
print()

# Example 5: fetchone with no more rows returns None
cursor.execute("SELECT * FROM employees WHERE id = 999")
result = cursor.fetchone()
print(f"  Query with no results: {result}")
print()

# ============================================================
# Section: fetchall - Get All Rows
# ============================================================

# Example 6: fetchall returns all rows as a list
print("=== fetchall() ===")
cursor.execute("SELECT name, department FROM employees")
all_rows = cursor.fetchall()
print(f"  Total rows returned: {len(all_rows)}")
for row in all_rows:
    print(f"  {row}")
print()

# ============================================================
# Section: fetchmany - Get N Rows
# ============================================================

# Example 7: fetchmany returns specified number of rows
print("=== fetchmany(3) ===")
cursor.execute("SELECT * FROM employees")
batch = cursor.fetchmany(3)
print(f"  Got {len(batch)} rows:")
for row in batch:
    print(f"  {row}")
print()

# Example 8: fetchmany continues from where fetchone left off
print("=== fetchmany continues from cursor position ===")
cursor.execute("SELECT * FROM employees")
cursor.fetchone()  # Skip first row
batch = cursor.fetchmany(2)  # Get next 2 rows
print(f"  After fetchone + fetchmany(2), got {len(batch)} rows:")
for row in batch:
    print(f"  {row}")
print()

# ============================================================
# Section: COUNT and Aggregates
# ============================================================

# Example 9: COUNT(*) - Total number of rows
print("=== COUNT and Aggregates ===")
cursor.execute("SELECT COUNT(*) FROM employees")
print(f"  Total employees: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM employees WHERE department = 'Engineering'")
print(f"  Engineering employees: {cursor.fetchone()[0]}")

cursor.execute("SELECT AVG(salary) FROM employees")
print(f"  Average salary: ${cursor.fetchone()[0]:,.2f}")

cursor.execute("SELECT MAX(salary) FROM employees")
print(f"  Highest salary: ${cursor.fetchone()[0]:,.2f}")

cursor.execute("SELECT MIN(salary) FROM employees")
print(f"  Lowest salary: ${cursor.fetchone()[0]:,.2f}")
print()

# ============================================================
# Section: DISTINCT
# ============================================================

# Example 10: DISTINCT removes duplicates
print("=== DISTINCT ===")
cursor.execute("SELECT DISTINCT department FROM employees")
departments = cursor.fetchall()
print(f"  Unique departments: {[d[0] for d in departments]}")
print()

# ============================================================
# Section: LIMIT
# ============================================================

# Example 11: LIMIT restricts number of rows returned
print("=== LIMIT ===")
cursor.execute("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3")
top_earners = cursor.fetchall()
print("  Top 3 earners:")
for row in top_earners:
    print(f"    {row[0]}: ${row[1]:,.2f}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

cursor.execute("DROP TABLE IF EXISTS employees")
conn.commit()
print("Table dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. SELECT * returns all columns; SELECT col1, col2 returns specific ones")
print("2. Use AS to create column aliases for output")
print("3. fetchone() returns one row; returns None when no more rows")
print("4. fetchall() returns all rows as a list of tuples")
print("5. fetchmany(n) returns up to n rows, continuing from cursor position")
print("6. COUNT, AVG, MAX, MIN are aggregate functions for statistics")
print("7. DISTINCT removes duplicate values from results")
print("8. LIMIT restricts the number of rows returned")
print("=" * 60)

# Close connection
conn.close()
