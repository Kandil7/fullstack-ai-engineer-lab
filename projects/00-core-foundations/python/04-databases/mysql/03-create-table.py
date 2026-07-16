"""
W3Schools Python Tutorial - MySQL 03: Create Table
============================================
Topics: Column types, constraints, PRIMARY KEY, AUTO_INCREMENT concept, NOT NULL

Run: python 03-create-table.py
Reference: https://www.w3schools.com/python/python_mysql_create_table.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Basic CREATE TABLE
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Example 1: Simple table creation
cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT
    )
""")
print("Table 'customers' created successfully!")
print()

# Example 2: Insert and verify
cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
conn.commit()
cursor.execute("SELECT * FROM customers")
print("Data in customers:", cursor.fetchall())
print()

# ============================================================
# Section: PRIMARY KEY
# ============================================================

# Example 3: PRIMARY KEY ensures unique identification
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product TEXT NOT NULL,
        amount REAL NOT NULL
    )
""")
print("Table 'orders' with PRIMARY KEY created!")
print()

# Example 4: PRIMARY KEY auto-increments in sqlite3
# In MySQL: AUTO_INCREMENT keyword
# In sqlite3: INTEGER PRIMARY KEY auto-increments
cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Laptop', 999.99)")
cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Mouse', 29.99)")
cursor.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Keyboard', 79.99)")
conn.commit()
cursor.execute("SELECT * FROM orders")
for row in cursor.fetchall():
    print(f"  Order: id={row[0]}, customer={row[1]}, product={row[2]}, amount={row[3]}")
print()

# ============================================================
# Section: NOT NULL Constraint
# ============================================================

# Example 5: NOT NULL prevents NULL values
print("=== NOT NULL Constraint ===")
try:
    cursor.execute("INSERT INTO customers (name, email) VALUES (NULL, 'test@example.com')")
except sqlite3.IntegrityError as e:
    print(f"Error inserting NULL name: {e}")
print()

# Example 6: NOT NULL with multiple columns
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT
    )
""")
print("Table 'products' with multiple NOT NULL columns created!")
print()

# ============================================================
# Section: DEFAULT Values
# ============================================================

# Example 7: DEFAULT provides a value when none is specified
cursor.execute("""
    CREATE TABLE settings (
        id INTEGER PRIMARY KEY,
        theme TEXT DEFAULT 'light',
        language TEXT DEFAULT 'en',
        notifications INTEGER DEFAULT 1
    )
""")

# Insert without specifying defaults
cursor.execute("INSERT INTO settings (id) VALUES (1)")
conn.commit()

cursor.execute("SELECT * FROM settings")
row = cursor.fetchone()
print(f"Settings with defaults: theme={row[1]}, lang={row[2]}, notify={row[3]}")
print()

# ============================================================
# Section: UNIQUE Constraint
# ============================================================

# Example 8: UNIQUE ensures no duplicate values
cursor.execute("""
    CREATE TABLE usernames (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("INSERT INTO usernames (username, email) VALUES ('john_doe', 'john@example.com')")
conn.commit()

try:
    cursor.execute("INSERT INTO usernames (username, email) VALUES ('john_doe', 'other@example.com')")
except sqlite3.IntegrityError as e:
    print(f"UNIQUE constraint violation: {e}")
print()

# ============================================================
# Section: CHECK Constraint
# ============================================================

# Example 9: CHECK ensures values meet a condition
cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER CHECK(age >= 18 AND age <= 120),
        salary REAL CHECK(salary > 0)
    )
""")

cursor.execute("INSERT INTO employees (name, age, salary) VALUES ('John', 30, 50000)")
conn.commit()

try:
    cursor.execute("INSERT INTO employees (name, age, salary) VALUES ('Young', 15, 50000)")
except sqlite3.IntegrityError as e:
    print(f"CHECK constraint violation (age): {e}")

try:
    cursor.execute("INSERT INTO employees (name, age, salary) VALUES ('Poor', 25, -100)")
except sqlite3.IntegrityError as e:
    print(f"CHECK constraint violation (salary): {e}")
print()

# ============================================================
# Section: AUTO_INCREMENT Concept
# ============================================================

# Example 10: AUTO_INCREMENT in MySQL vs INTEGER PRIMARY KEY in sqlite3
print("=== AUTO_INCREMENT Concept ===")
print("MySQL:    id INTEGER PRIMARY KEY AUTO_INCREMENT")
print("sqlite3:  id INTEGER PRIMARY KEY  (auto-increments)")
print()

cursor.execute("""
    CREATE TABLE logs (
        id INTEGER PRIMARY KEY,
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

for i in range(5):
    cursor.execute("INSERT INTO logs (message) VALUES (?)", (f"Log entry {i+1}",))
conn.commit()

cursor.execute("SELECT * FROM logs")
for row in cursor.fetchall():
    print(f"  Log #{row[0]}: {row[1]}")
print()

# ============================================================
# Section: Composite PRIMARY KEY
# ============================================================

# Example 11: Primary key with multiple columns
cursor.execute("""
    CREATE TABLE enrollment (
        student_id INTEGER,
        course_id INTEGER,
        enrollment_date TEXT,
        PRIMARY KEY (student_id, course_id)
    )
""")

cursor.execute("INSERT INTO enrollment VALUES (1, 101, '2024-01-15')")
cursor.execute("INSERT INTO enrollment VALUES (1, 102, '2024-01-15')")
conn.commit()

try:
    # This fails because (1, 101) already exists
    cursor.execute("INSERT INTO enrollment VALUES (1, 101, '2024-02-01')")
except sqlite3.IntegrityError as e:
    print(f"Composite PK violation: {e}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 12: Drop all created tables
tables_to_drop = ["customers", "orders", "products", "settings", "usernames", "employees", "logs", "enrollment"]
for table in tables_to_drop:
    # Table/column identifiers can't be parameterized — only ever interpolate whitelisted literal names, NEVER user input.
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
print("1. PRIMARY KEY uniquely identifies each row in a table")
print("2. NOT NULL prevents NULL values in a column")
print("3. DEFAULT provides a value when none is specified")
print("4. UNIQUE ensures all values in a column are different")
print("5. CHECK validates that values meet a condition")
print("6. AUTO_INCREMENT (MySQL) / INTEGER PRIMARY KEY (sqlite3)")
print("7. Composite PRIMARY KEY uses multiple columns")
print("8. All constraints enforce data integrity at the database level")
print("=" * 60)

# Close connection
conn.close()
