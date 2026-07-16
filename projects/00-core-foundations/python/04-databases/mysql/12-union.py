"""
W3Schools Python Tutorial - MySQL 12: Union
============================================
Topics: UNION, UNION ALL, combining SELECT results

Run: python 12-union.py
Reference: https://www.w3schools.com/python/python_mysql_join.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create Tables
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create tables for union examples
cursor.execute("""
    CREATE TABLE customers_us (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT
    )
""")

cursor.execute("""
    CREATE TABLE customers_eu (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT
    )
""")

cursor.execute("""
    CREATE TABLE products_a (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL
    )
""")

cursor.execute("""
    CREATE TABLE products_b (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL
    )
""")

# Insert US customers
us_customers = [
    (1, "Alice", "New York"),
    (2, "Bob", "Los Angeles"),
    (3, "Charlie", "Chicago"),
]
cursor.executemany("INSERT INTO customers_us VALUES (?, ?, ?)", us_customers)

# Insert EU customers
eu_customers = [
    (1, "Diana", "London"),
    (2, "Eve", "Paris"),
    (3, "Frank", "Berlin"),
    (4, "Grace", "Madrid"),
]
cursor.executemany("INSERT INTO customers_eu VALUES (?, ?, ?)", eu_customers)

# Insert products A
products_a = [
    (1, "Laptop", 999.99),
    (2, "Mouse", 29.99),
    (3, "Keyboard", 79.99),
]
cursor.executemany("INSERT INTO products_a VALUES (?, ?, ?)", products_a)

# Insert products B (some overlap)
products_b = [
    (1, "Monitor", 449.99),
    (2, "Mouse", 29.99),
    (3, "Headphones", 89.99),
]
cursor.executemany("INSERT INTO products_b VALUES (?, ?, ?)", products_b)
conn.commit()

print("=== Tables Created ===")
for table in ["customers_us", "customers_eu", "products_a", "products_b"]:
    # Table/column identifiers can't be parameterized — only ever interpolate whitelisted literal names, NEVER user input.
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    print(f"{table}: {len(rows)} rows")
print()

# ============================================================
# Section: UNION - Remove Duplicates
# ============================================================

# Example 1: Basic UNION
print("=== UNION (Removes Duplicates) ===")
cursor.execute("""
    SELECT name, city FROM customers_us
    UNION
    SELECT name, city FROM customers_eu
""")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")
print()

# Example 2: UNION with ORDER BY
print("=== UNION with ORDER BY ===")
cursor.execute("""
    SELECT name, city FROM customers_us
    UNION
    SELECT name, city FROM customers_eu
    ORDER BY city
""")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")
print()

# ============================================================
# Section: UNION ALL - Keep Duplicates
# ============================================================

# Example 3: UNION ALL keeps duplicates
print("=== UNION ALL (Keeps Duplicates) ===")
cursor.execute("""
    SELECT name, price FROM products_a
    UNION ALL
    SELECT name, price FROM products_b
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 4: Compare UNION vs UNION ALL
print("=== UNION vs UNION ALL Comparison ===")
cursor.execute("SELECT name FROM products_a UNION SELECT name FROM products_b")
union_result = cursor.fetchall()
print(f"UNION (unique): {len(union_result)} rows")

cursor.execute("SELECT name FROM products_a UNION ALL SELECT name FROM products_b")
union_all_result = cursor.fetchall()
print(f"UNION ALL (all): {len(union_all_result)} rows")
print()

# ============================================================
# Section: UNION with Different Tables
# ============================================================

# Example 5: Union with different column names (uses first query's names)
print("=== UNION with Different Column Names ===")
cursor.execute("""
    SELECT name AS item, price AS cost FROM products_a
    UNION
    SELECT name AS item, price AS cost FROM products_b
    ORDER BY cost DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# ============================================================
# Section: UNION with WHERE
# ============================================================

# Example 6: Filter before union
print("=== UNION with WHERE ===")
cursor.execute("""
    SELECT name, price FROM products_a WHERE price > 50
    UNION
    SELECT name, price FROM products_b WHERE price > 50
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# ============================================================
# Section: UNION with Aggregate Functions
# ============================================================

# Example 7: Union with GROUP BY
print("=== UNION with GROUP BY ===")
cursor.execute("""
    SELECT name, SUM(price) as total_price FROM (
        SELECT name, price FROM products_a
        UNION ALL
        SELECT name, price FROM products_b
    )
    GROUP BY name
    ORDER BY total_price DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:.2f}")
print()

# ============================================================
# Section: UNION ALL for Counting
# ============================================================

# Example 8: Count all products from both tables
print("=== UNION ALL for Counting ===")
cursor.execute("""
    SELECT COUNT(*) as total FROM (
        SELECT name FROM products_a
        UNION ALL
        SELECT name FROM products_b
    )
""")
print(f"  Total products (with duplicates): {cursor.fetchone()[0]}")

cursor.execute("""
    SELECT COUNT(*) as total FROM (
        SELECT name FROM products_a
        UNION
        SELECT name FROM products_b
    )
""")
print(f"  Total products (unique): {cursor.fetchone()[0]}")
print()

# ============================================================
# Section: Practical Example - Combining Data Sources
# ============================================================

# Example 9: Real-world union scenario
print("=== Practical Example: Combined Customer List ===")
cursor.execute("""
    SELECT name, city, 'US' as region FROM customers_us
    UNION ALL
    SELECT name, city, 'EU' as region FROM customers_eu
    ORDER BY region, city
""")
for row in cursor.fetchall():
    print(f"  [{row[2]}] {row[0]} - {row[1]}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 10: Drop tables
tables = ["customers_us", "customers_eu", "products_a", "products_b"]
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
print("1. UNION combines results from multiple SELECT statements")
print("2. UNION removes duplicate rows; UNION ALL keeps all rows")
print("3. Both SELECT statements must have the same number of columns")
print("4. Column types should be compatible across queries")
print("5. ORDER BY applies to the final combined result")
print("6. Use UNION ALL when duplicates don't matter (faster)")
print("7. UNION with GROUP BY can aggregate combined results")
print("8. Practical use: combining data from multiple tables/sources")
print("=" * 60)

# Close connection
conn.close()
