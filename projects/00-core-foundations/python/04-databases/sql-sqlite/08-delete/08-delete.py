"""
W3Schools Python Tutorial - MySQL 08: Delete Data
============================================
Topics: DELETE FROM, WHERE clause, caution about deleting all rows

Run: python 08-delete.py
Reference: https://www.w3schools.com/python/python_mysql_delete.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create and Populate Table
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer TEXT NOT NULL,
        product TEXT NOT NULL,
        amount REAL,
        status TEXT DEFAULT 'pending'
    )
""")

orders = [
    (1, "Alice", "Laptop", 999.99, "completed"),
    (2, "Bob", "Mouse", 29.99, "pending"),
    (3, "Charlie", "Keyboard", 79.99, "completed"),
    (4, "Diana", "Monitor", 449.99, "cancelled"),
    (5, "Eve", "Headphones", 89.99, "pending"),
    (6, "Frank", "Desk", 299.99, "completed"),
    (7, "Grace", "Chair", 199.99, "pending"),
    (8, "Henry", "Webcam", 59.99, "cancelled"),
]

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
conn.commit()
print(f"Table 'orders' created with {len(orders)} rows.")
print()

def show_orders(label=""):
    if label:
        print(f"--- {label} ---")
    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        print(f"  {row}")
    print()

show_orders("Initial data")

# ============================================================
# Section: DELETE with WHERE
# ============================================================

# Example 1: Delete specific row by ID
print("=== DELETE with WHERE (by ID) ===")
cursor.execute("DELETE FROM orders WHERE id = 4")
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting id=4")

# ============================================================
# Section: DELETE with Condition
# ============================================================

# Example 2: Delete by status
print("=== DELETE with WHERE (by status) ===")
cursor.execute("DELETE FROM orders WHERE status = 'cancelled'")
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting cancelled orders")

# Example 3: Delete with comparison
print("=== DELETE with comparison ===")
cursor.execute("DELETE FROM orders WHERE amount < 100")
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting orders under $100")

# ============================================================
# Section: DELETE with Multiple Conditions
# ============================================================

# Example 4: DELETE with AND
print("=== DELETE with AND ===")
cursor.execute("DELETE FROM orders WHERE customer = 'Bob' AND status = 'pending'")
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting Bob's pending orders")

# Example 5: DELETE with OR
print("=== DELETE with OR ===")
cursor.execute("DELETE FROM orders WHERE customer = 'Grace' OR customer = 'Henry'")
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting Grace and Henry")

# ============================================================
# Section: DELETE with LIMIT
# ============================================================

# Example 6: Delete limited rows
print("=== DELETE with LIMIT ===")
# Recreate for this example
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer TEXT NOT NULL,
        product TEXT NOT NULL,
        amount REAL,
        status TEXT DEFAULT 'pending'
    )
""")
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", [
    (1, "Alice", "Laptop", 999.99, "completed"),
    (2, "Bob", "Mouse", 29.99, "pending"),
    (3, "Charlie", "Keyboard", 79.99, "completed"),
    (4, "Diana", "Monitor", 449.99, "pending"),
    (5, "Eve", "Headphones", 89.99, "pending"),
])
conn.commit()

# MySQL supports: DELETE FROM orders WHERE status = 'pending' LIMIT 2
# sqlite3 rejects DELETE ... LIMIT, so use a portable subquery form:
cursor.execute(
    "DELETE FROM orders WHERE id IN "
    "(SELECT id FROM orders WHERE status = 'pending' LIMIT 2)"
)
conn.commit()
print(f"Deleted rows: {cursor.rowcount}")
show_orders("After deleting 2 pending orders")
print("NOTE: MySQL allows DELETE ... LIMIT directly;")
print("      the portable subquery form works on both MySQL and sqlite3.")
print()

# ============================================================
# Section: WARNING - DELETE All Rows
# ============================================================

# Example 7: DELETE without WHERE deletes ALL rows!
print("=== WARNING: DELETE ALL ROWS ===")
print("DELETE FROM orders  -- THIS DELETES EVERYTHING!")
print("Always use WHERE unless you truly want all rows deleted!")
print()

# Example 8: TRUNCATE equivalent
print("=== TRUNCATE Equivalent ===")
print("MySQL: TRUNCATE TABLE orders  (faster, resets auto_increment)")
print("sqlite3: DELETE FROM orders; or DROP + CREATE")
print()

# ============================================================
# Section: DELETE and Verify
# ============================================================

# Example 9: Verify deletion with rowcount
print("=== Verify Deletion ===")
cursor.execute("DELETE FROM orders WHERE id = 1")
conn.commit()
print(f"Rows deleted: {cursor.rowcount}")

cursor.execute("SELECT COUNT(*) FROM orders")
remaining = cursor.fetchone()[0]
print(f"Remaining rows: {remaining}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 10: Drop table
cursor.execute("DROP TABLE IF EXISTS orders")
conn.commit()
print("Table dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. DELETE FROM table WHERE condition removes matching rows")
print("2. Always use WHERE to avoid deleting all rows accidentally")
print("3. cursor.rowcount shows how many rows were deleted")
print("4. Use AND/OR for complex deletion conditions")
print("5. DELETE with LIMIT removes only a specified number of rows")
print("6. TRUNCATE is faster than DELETE for removing all rows (MySQL)")
print("7. DELETE is logged and can be rolled back; TRUNCATE cannot")
print("8. Always commit after DELETE to save changes")
print("=" * 60)

# Close connection
conn.close()
