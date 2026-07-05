"""
W3Schools Python Tutorial - MySQL 11: Joins
============================================
Topics: INNER JOIN, LEFT JOIN, creating related tables

Run: python 11-join.py
Reference: https://www.w3schools.com/python/python_mysql_join.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create Related Tables
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create customers table
cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT
    )
""")

# Create orders table with foreign key
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT NOT NULL,
        amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

# Insert customers
customers = [
    (1, "Alice", "New York"),
    (2, "Bob", "Los Angeles"),
    (3, "Charlie", "Chicago"),
    (4, "Diana", "Houston"),
    (5, "Eve", "Phoenix"),
]
cursor.executemany("INSERT INTO customers VALUES (?, ?, ?)", customers)

# Insert orders
orders = [
    (1, 1, "Laptop", 999.99),
    (2, 1, "Mouse", 29.99),
    (3, 2, "Keyboard", 79.99),
    (4, 3, "Monitor", 449.99),
    (5, 3, "Headphones", 89.99),
    (6, 3, "Webcam", 59.99),
]
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
conn.commit()

print("=== Tables Created ===")
cursor.execute("SELECT * FROM customers")
print("Customers:")
for row in cursor.fetchall():
    print(f"  {row}")

cursor.execute("SELECT * FROM orders")
print("\nOrders:")
for row in cursor.fetchall():
    print(f"  {row}")
print()

# ============================================================
# Section: INNER JOIN
# ============================================================

# Example 1: Basic INNER JOIN
print("=== INNER JOIN ===")
cursor.execute("""
    SELECT customers.name, orders.product, orders.amount
    FROM customers
    INNER JOIN orders ON customers.id = orders.customer_id
""")
for row in cursor.fetchall():
    print(f"  {row[0]} bought {row[1]} for ${row[2]}")
print()

# Example 2: INNER JOIN with aliases
print("=== INNER JOIN with Aliases ===")
cursor.execute("""
    SELECT c.name, o.product, o.amount
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} (${row[2]})")
print()

# ============================================================
# Section: LEFT JOIN
# ============================================================

# Example 3: LEFT JOIN includes all left table rows
print("=== LEFT JOIN ===")
cursor.execute("""
    SELECT c.name, o.product, o.amount
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
""")
for row in cursor.fetchall():
    product = row[1] if row[1] else "No orders"
    amount = f"${row[2]}" if row[2] else "N/A"
    print(f"  {row[0]}: {product} ({amount})")
print()

# Example 4: Find customers with no orders
print("=== Customers with No Orders ===")
cursor.execute("""
    SELECT c.name
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    WHERE o.id IS NULL
""")
for row in cursor.fetchall():
    print(f"  {row[0]} has no orders")
print()

# ============================================================
# Section: RIGHT JOIN (workaround in sqlite3)
# ============================================================

# Example 5: sqlite3 doesn't support RIGHT JOIN directly
# Workaround: use LEFT JOIN with tables swapped
print("=== RIGHT JOIN Workaround ===")
print("sqlite3 doesn't support RIGHT JOIN directly.")
print("Workaround: LEFT JOIN with tables in reverse order")
print()

# Simulated RIGHT JOIN
cursor.execute("""
    SELECT c.name, o.product
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.id
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# ============================================================
# Section: JOIN with WHERE
# ============================================================

# Example 6: Filter after join
print("=== JOIN with WHERE ===")
cursor.execute("""
    SELECT c.name, c.city, o.product, o.amount
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
    WHERE o.amount > 100
""")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}): {row[2]} - ${row[3]}")
print()

# ============================================================
# Section: JOIN with ORDER BY
# ============================================================

# Example 7: Sort joined results
print("=== JOIN with ORDER BY ===")
cursor.execute("""
    SELECT c.name, o.product, o.amount
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
    ORDER BY o.amount DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} (${row[2]})")
print()

# ============================================================
# Section: Multiple JOINs
# ============================================================

# Example 8: Joining multiple tables
print("=== Multiple JOINs ===")

# Create products table
cursor.execute("""
    CREATE TABLE product_info (
        product_name TEXT PRIMARY KEY,
        category TEXT,
        stock INTEGER
    )
""")

product_info = [
    ("Laptop", "Electronics", 50),
    ("Mouse", "Electronics", 200),
    ("Keyboard", "Electronics", 150),
    ("Monitor", "Electronics", 75),
    ("Headphones", "Electronics", 100),
    ("Webcam", "Electronics", 80),
]
cursor.executemany("INSERT INTO product_info VALUES (?, ?, ?)", product_info)
conn.commit()

cursor.execute("""
    SELECT c.name, o.product, p.category, o.amount
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
    INNER JOIN product_info p ON o.product = p.product_name
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} ({row[2]}) - ${row[3]}")
print()

# ============================================================
# Section: Aggregate with JOIN
# ============================================================

# Example 9: Summarize joined data
print("=== Aggregate with JOIN ===")
cursor.execute("""
    SELECT c.name, COUNT(o.id) as order_count, SUM(o.amount) as total_spent
    FROM customers c
    INNER JOIN orders o ON c.id = o.customer_id
    GROUP BY c.name
    ORDER BY total_spent DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} orders, ${row[2]:.2f} total")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 10: Drop all tables
tables = ["customers", "orders", "product_info"]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
conn.commit()
print("All tables dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. INNER JOIN returns only matching rows from both tables")
print("2. LEFT JOIN returns all rows from left table, matching from right")
print("3. RIGHT JOIN: sqlite3 workaround is LEFT JOIN with swapped tables")
print("4. Use aliases (c, o, p) for cleaner JOIN queries")
print("5. JOIN with WHERE filters results after joining")
print("6. Multiple JOINs combine 3+ tables in one query")
print("7. Use GROUP BY with JOIN for aggregate summaries")
print("8. Foreign keys define relationships between tables")
print("=" * 60)

# Close connection
conn.close()
