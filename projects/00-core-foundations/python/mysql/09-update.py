"""
W3Schools Python Tutorial - MySQL 09: Update Data
============================================
Topics: UPDATE SET, WHERE clause, updating multiple columns

Run: python 09-update.py
Reference: https://www.w3schools.com/python/python_mysql_update.asp
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
        status TEXT DEFAULT 'active'
    )
""")

employees = [
    (1, "Alice Johnson", "Engineering", 85000, "active"),
    (2, "Bob Smith", "Marketing", 65000, "active"),
    (3, "Charlie Brown", "Engineering", 92000, "active"),
    (4, "Diana Prince", "Sales", 72000, "active"),
    (5, "Eve Adams", "Marketing", 68000, "inactive"),
    (6, "Frank Miller", "Engineering", 95000, "active"),
]

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)
conn.commit()
print(f"Table 'employees' created with {len(employees)} rows.")
print()

def show_employees(label=""):
    if label:
        print(f"--- {label} ---")
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        print(f"  {row}")
    print()

show_employees("Initial data")

# ============================================================
# Section: UPDATE Single Column
# ============================================================

# Example 1: Update one column for a specific row
print("=== UPDATE Single Column ===")
cursor.execute("UPDATE employees SET salary = 90000 WHERE id = 1")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After updating Alice's salary")

# ============================================================
# Section: UPDATE Multiple Columns
# ============================================================

# Example 2: Update multiple columns at once
print("=== UPDATE Multiple Columns ===")
cursor.execute("UPDATE employees SET department = 'Management', salary = 100000 WHERE id = 3")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After promoting Charlie")

# ============================================================
# Section: UPDATE with WHERE Condition
# ============================================================

# Example 3: Update by name
print("=== UPDATE by Name ===")
cursor.execute("UPDATE employees SET status = 'active' WHERE name = 'Eve Adams'")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After reactivating Eve")

# Example 4: Update with comparison
print("=== UPDATE with Comparison ===")
cursor.execute("UPDATE employees SET salary = salary * 1.10 WHERE salary < 70000")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After 10% raise for salaries under 70k")

# ============================================================
# Section: UPDATE with Expression
# ============================================================

# Example 5: Update using expressions
print("=== UPDATE with Expression ===")
cursor.execute("UPDATE employees SET salary = salary + 5000 WHERE department = 'Engineering'")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After $5k raise for Engineering")

# ============================================================
# Section: UPDATE with CASE
# ============================================================

# Example 6: Conditional update with CASE
print("=== UPDATE with CASE ===")
cursor.execute("""
    UPDATE employees SET status = CASE
        WHEN salary >= 90000 THEN 'senior'
        WHEN salary >= 70000 THEN 'mid-level'
        ELSE 'junior'
    END
""")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After setting status based on salary")

# ============================================================
# Section: WARNING - UPDATE Without WHERE
# ============================================================

# Example 7: WARNING - no WHERE updates ALL rows!
print("=== WARNING: UPDATE Without WHERE ===")
print("UPDATE employees SET status = 'active'  -- CHANGES EVERY ROW!")
print("Always use WHERE unless you truly want to update all rows!")
print()

# ============================================================
# Section: UPDATE with NULL
# ============================================================

# Example 8: Set column to NULL
print("=== UPDATE to NULL ===")
cursor.execute("UPDATE employees SET department = NULL WHERE id = 5")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")
show_employees("After setting Eve's department to NULL")

# ============================================================
# Section: UPDATE and Verify
# ============================================================

# Example 9: Verify update with rowcount
print("=== Verify Updates ===")
cursor.execute("UPDATE employees SET salary = 110000 WHERE name = 'Frank Miller'")
conn.commit()
print(f"Rows updated: {cursor.rowcount}")

cursor.execute("SELECT name, salary FROM employees WHERE name = 'Frank Miller'")
row = cursor.fetchone()
print(f"Frank's new salary: ${row[1]:,.2f}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 10: Drop table
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
print("1. UPDATE table SET col = value WHERE condition")
print("2. Update multiple columns: SET col1 = v1, col2 = v2")
print("3. Use WHERE to target specific rows")
print("4. Use expressions: SET salary = salary * 1.10")
print("5. Use CASE for conditional updates")
print("6. Set columns to NULL with SET col = NULL")
print("7. cursor.rowcount shows how many rows were updated")
print("8. WARNING: Without WHERE, UPDATE changes ALL rows!")
print("=" * 60)

# Close connection
conn.close()
