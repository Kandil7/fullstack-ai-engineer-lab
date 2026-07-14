"""
W3Schools Python Tutorial - MySQL 06: Where Clause
============================================
Topics: WHERE with all operators (=, <>, >, <, LIKE, IN, BETWEEN), AND/OR, NULL

Run: python 06-where.py
Reference: https://www.w3schools.com/python/python_mysql_where.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup - Create and Populate Table
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        quantity INTEGER,
        in_stock INTEGER DEFAULT 1
    )
""")

products = [
    (1, "Laptop", "Electronics", 999.99, 50, 1),
    (2, "Mouse", "Electronics", 29.99, 200, 1),
    (3, "Desk", "Furniture", 299.99, 30, 1),
    (4, "Chair", "Furniture", 199.99, 0, 0),
    (5, "Keyboard", "Electronics", 79.99, 150, 1),
    (6, "Monitor", "Electronics", 449.99, 75, 1),
    (7, "Bookshelf", "Furniture", 149.99, 25, 1),
    (8, "Headphones", "Electronics", 89.99, None, 1),
    (9, "Webcam", "Electronics", 59.99, 100, 1),
    (10, "Desk Lamp", "Furniture", 39.99, 80, 1),
]

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", products)
conn.commit()
print(f"Table 'products' created with {len(products)} rows.")
print()

# ============================================================
# Section: Comparison Operators
# ============================================================

# Example 1: Equal (=)
print("=== Equal Operator (=) ===")
cursor.execute("SELECT name, price FROM products WHERE price = 29.99")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 2: Not Equal (<> or !=)
print("=== Not Equal Operator (<>) ===")
cursor.execute("SELECT name, category FROM products WHERE category <> 'Electronics'")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print()

# Example 3: Greater Than (>)
print("=== Greater Than (>) ===")
cursor.execute("SELECT name, price FROM products WHERE price > 500")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 4: Less Than (<)
print("=== Less Than (<) ===")
cursor.execute("SELECT name, price FROM products WHERE price < 100")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 5: Greater Than or Equal (>=) and Less Than or Equal (<=)
print("=== Greater/Less Than or Equal ===")
cursor.execute("SELECT name, price FROM products WHERE price >= 200 AND price <= 500")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# ============================================================
# Section: LIKE Operator
# ============================================================

# Example 6: LIKE with % wildcard (matches any sequence of characters)
print("=== LIKE with % wildcard ===")
cursor.execute("SELECT name FROM products WHERE name LIKE '%o%'")
print("  Products with 'o' in name:")
for row in cursor.fetchall():
    print(f"    {row[0]}")
print()

# Example 7: LIKE with _ wildcard (matches single character)
print("=== LIKE with _ wildcard ===")
cursor.execute("SELECT name FROM products WHERE name LIKE '_e%'")
print("  Products where 2nd letter is 'e':")
for row in cursor.fetchall():
    print(f"    {row[0]}")
print()

# Example 8: LIKE with pattern
print("=== LIKE patterns ===")
cursor.execute("SELECT name FROM products WHERE name LIKE 'L%'")
print("  Products starting with 'L':")
for row in cursor.fetchall():
    print(f"    {row[0]}")
print()

# ============================================================
# Section: IN Operator
# ============================================================

# Example 9: IN - match any value in a list
print("=== IN Operator ===")
cursor.execute("SELECT name, price FROM products WHERE price IN (29.99, 79.99, 89.99)")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 10: NOT IN - exclude values in a list
print("=== NOT IN Operator ===")
cursor.execute("SELECT name, category FROM products WHERE category NOT IN ('Electronics', 'Furniture')")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
print("(No results if all categories are Electronics or Furniture)")
print()

# ============================================================
# Section: BETWEEN Operator
# ============================================================

# Example 11: BETWEEN - range query (inclusive)
print("=== BETWEEN Operator ===")
cursor.execute("SELECT name, price FROM products WHERE price BETWEEN 50 AND 100")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# Example 12: NOT BETWEEN
print("=== NOT BETWEEN Operator ===")
cursor.execute("SELECT name, price FROM products WHERE price NOT BETWEEN 50 AND 100")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}")
print()

# ============================================================
# Section: AND / OR Operators
# ============================================================

# Example 13: AND - both conditions must be true
print("=== AND Operator ===")
cursor.execute("SELECT name, price, quantity FROM products WHERE price > 100 AND quantity > 50")
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]}, qty={row[2]}")
print()

# Example 14: OR - either condition can be true
print("=== OR Operator ===")
cursor.execute("SELECT name, category, price FROM products WHERE category = 'Furniture' OR price < 50")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}): ${row[2]}")
print()

# Example 15: Combining AND and OR with parentheses
print("=== AND + OR with Parentheses ===")
cursor.execute("""
    SELECT name, price, category FROM products
    WHERE (category = 'Electronics' OR category = 'Furniture')
    AND price > 200
""")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[2]}): ${row[1]}")
print()

# ============================================================
# Section: NULL Handling
# ============================================================

# Example 16: IS NULL - check for NULL values
print("=== IS NULL ===")
cursor.execute("SELECT name, quantity FROM products WHERE quantity IS NULL")
for row in cursor.fetchall():
    print(f"  {row[0]}: quantity is NULL")
print()

# Example 17: IS NOT NULL - check for non-NULL values
print("=== IS NOT NULL ===")
cursor.execute("SELECT name, quantity FROM products WHERE quantity IS NOT NULL")
for row in cursor.fetchall():
    print(f"  {row[0]}: quantity={row[1]}")
print()

# Example 18: NULL in comparisons returns NULL (not True or False)
print("=== NULL in Comparisons ===")
cursor.execute("SELECT name, quantity FROM products WHERE quantity = NULL")
result = cursor.fetchall()
print(f"  WHERE quantity = NULL returns: {result} (empty — NULL comparisons use IS NULL)")
print()

# ============================================================
# Section: Cleanup
# ============================================================

cursor.execute("DROP TABLE IF EXISTS products")
conn.commit()
print("Table dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. Comparison: =, <>, !=, >, <, >=, <=")
print("2. LIKE: % matches any sequence, _ matches single character")
print("3. IN: match any value in a list; NOT IN: exclude list values")
print("4. BETWEEN: range query inclusive on both ends")
print("5. AND/OR: combine conditions; use parentheses for precedence")
print("6. NULL: use IS NULL / IS NOT NULL (not = or <>)")
print("7. NULL comparisons always return NULL, never True/False")
print("8. Parameterized queries (?) work with all operators")
print("=" * 60)

# Close connection
conn.close()
