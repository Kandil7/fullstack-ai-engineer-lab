"""
W3Schools Python Tutorial - MySQL 10: Drop Table
============================================
Topics: DROP TABLE, IF EXISTS, ALTER TABLE basics

Run: python 10-drop-table.py
Reference: https://www.w3schools.com/python/python_mysql_drop_table.asp
"""

# NOTE: This uses sqlite3 as a stand-in for MySQL. The SQL syntax is nearly identical.

import sqlite3

# ============================================================
# Section: Setup
# ============================================================

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# ============================================================
# Section: DROP TABLE
# ============================================================

# Example 1: Create and drop a table
print("=== DROP TABLE ===")
cursor.execute("""
    CREATE TABLE temp_data (
        id INTEGER PRIMARY KEY,
        value TEXT
    )
""")
cursor.execute("INSERT INTO temp_data (value) VALUES ('test')")
conn.commit()

# Verify table exists
cursor.execute("SELECT * FROM temp_data")
print(f"Before DROP: {cursor.fetchall()}")

# Drop the table
cursor.execute("DROP TABLE temp_data")
conn.commit()
print("Table 'temp_data' dropped!")
print()

# ============================================================
# Section: DROP TABLE IF EXISTS
# ============================================================

# Example 2: Safe drop with IF EXISTS
print("=== DROP TABLE IF EXISTS ===")
# This won't throw an error even if table doesn't exist
cursor.execute("DROP TABLE IF EXISTS non_existent_table")
print("Dropped non_existent_table (no error because of IF EXISTS)")
print()

# Example 3: Without IF EXISTS, it would error
print("Without IF EXISTS:")
try:
    cursor.execute("DROP TABLE another_nonexistent")
except sqlite3.OperationalError as e:
    print(f"  Error: {e}")
print()

# ============================================================
# Section: DROP Multiple Tables
# ============================================================

# Example 4: Create and drop multiple tables
print("=== DROP Multiple Tables ===")
tables = ["table_a", "table_b", "table_c"]
for table in tables:
    cursor.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
    cursor.execute(f"INSERT INTO {table} (id) VALUES (1)")
conn.commit()
print(f"Created {len(tables)} tables")

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
conn.commit()
print(f"Dropped {len(tables)} tables")
print()

# ============================================================
# Section: ALTER TABLE - Add Column
# ============================================================

# Example 5: ALTER TABLE ADD COLUMN
print("=== ALTER TABLE - Add Column ===")
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT
    )
""")
cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
conn.commit()

# Add a new column
cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
conn.commit()

cursor.execute("SELECT * FROM users")
print(f"After adding 'phone' column: {cursor.fetchall()}")
print()

# ============================================================
# Section: ALTER TABLE - Drop Column
# ============================================================

# Example 6: ALTER TABLE DROP COLUMN
print("=== ALTER TABLE - Drop Column ===")
cursor.execute("ALTER TABLE users DROP COLUMN email")
conn.commit()

cursor.execute("SELECT * FROM users")
print(f"After dropping 'email' column: {cursor.fetchall()}")
print()

# ============================================================
# Section: ALTER TABLE - Rename Table
# ============================================================

# Example 7: Rename a table
print("=== Rename Table ===")
cursor.execute("ALTER TABLE users RENAME TO customers")
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(f"Tables after rename: {[t[0] for t in cursor.fetchall()]}")
print()

# ============================================================
# Section: ALTER TABLE - Modify Column (sqlite3 limitation)
# ============================================================

# Example 8: In MySQL: ALTER TABLE MODIFY COLUMN
# sqlite3 doesn't support MODIFY COLUMN directly
# Workaround: create new table, copy data, drop old, rename
print("=== Modify Column (Workaround) ===")
print("MySQL: ALTER TABLE users MODIFY COLUMN name VARCHAR(100)")
print("sqlite3: Must recreate table (no direct MODIFY COLUMN)")
print()

# Workaround for sqlite3
cursor.execute("""
    CREATE TABLE users_new (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT
    )
""")
cursor.execute("INSERT INTO users_new SELECT id, name, phone FROM customers")
cursor.execute("DROP TABLE customers")
cursor.execute("ALTER TABLE users_new RENAME TO customers")
conn.commit()

cursor.execute("SELECT * FROM customers")
print(f"After recreation: {cursor.fetchall()}")
print()

# ============================================================
# Section: Check Table Existence
# ============================================================

# Example 9: Check if a table exists before dropping
print("=== Check Table Existence ===")
cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name='customers'
""")
exists = cursor.fetchone()
print(f"Table 'customers' exists: {exists is not None}")

cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name='nonexistent'
""")
exists = cursor.fetchone()
print(f"Table 'nonexistent' exists: {exists is not None}")
print()

# ============================================================
# Section: Cleanup
# ============================================================

# Example 10: Final cleanup
cursor.execute("DROP TABLE IF EXISTS customers")
conn.commit()
print("All tables dropped for cleanup.")
print()

# ============================================================
# Section: Summary
# ============================================================

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("1. DROP TABLE removes a table and all its data permanently")
print("2. Use IF EXISTS to avoid errors when table doesn't exist")
print("3. ALTER TABLE ADD COLUMN adds a new column to a table")
print("4. ALTER TABLE DROP COLUMN removes a column from a table")
print("5. ALTER TABLE RENAME changes a table's name")
print("6. sqlite3 doesn't support MODIFY COLUMN (use workaround)")
print("7. Check sqlite_master to verify table existence")
print("8. DROP TABLE is irreversible — always backup first!")
print("=" * 60)

# Close connection
conn.close()
