# PostgreSQL Cheat Sheet

## DDL (Data Definition Language)

### Creating Tables
```sql
-- Basic table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table with constraints
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total DECIMAL(10, 2) CHECK (total >= 0),
    status VARCHAR(20) DEFAULT 'pending'
);
```

### Altering Tables
```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users RENAME TO customers;
```

---

## DML (Data Manipulation Language)

### Inserting Data
```sql
INSERT INTO users (email, name) VALUES ('john@example.com', 'John Doe');

-- Multiple rows
INSERT INTO users (email, name) VALUES
    ('jane@example.com', 'Jane Smith'),
    ('bob@example.com', 'Bob Wilson');

-- Upsert
INSERT INTO users (email, name) VALUES ('john@example.com', 'John Updated')
ON CONFLICT (email) 
DO UPDATE SET name = EXCLUDED.name;
```

### Updating Data
```sql
UPDATE users SET name = 'John Smith' WHERE id = 1;

UPDATE users 
SET name = 'Updated Name', updated_at = CURRENT_TIMESTAMP
WHERE id = 1
RETURNING *;
```

### Deleting Data
```sql
DELETE FROM users WHERE id = 1;

DELETE FROM users 
WHERE created_at < '2023-01-01'
RETURNING *;
```

---

## Joins

### Inner Join
```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### Left Join
```sql
SELECT u.name, COALESCE(SUM(o.total), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### Full Outer Join
```sql
SELECT u.name, o.total
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;
```

---

## Indexes

### Creating Indexes
```sql
-- B-tree index (default)
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index
CREATE INDEX idx_orders_pending ON orders(created_at) 
WHERE status = 'pending';

-- GIN index for full-text search
CREATE INDEX idx_posts_content_gin ON posts 
USING gin(to_tsvector('english', content));
```

### Managing Indexes
```sql
SELECT * FROM pg_indexes WHERE tablename = 'users';
DROP INDEX IF EXISTS idx_users_email;
REINDEX INDEX idx_users_email;
```

---

## EXPLAIN (Query Analysis)

### Basic Usage
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT * FROM users WHERE email = 'test@example.com';
```

### Reading Output
```
Seq Scan on users  (cost=0.00..1.02 rows=1 width=64)
  Filter: (email = 'test@example.com'::text)
  Rows Removed by Filter: 999

-- cost: estimated startup/total cost
-- rows: estimated number of rows
-- actual time: real execution time
```

---

## Connection Pooling

### Application Connection Strings
```python
# Python (psycopg2)
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="user",
    password="pass"
)
```

### Connection Management
```sql
-- Show current connections
SELECT * FROM pg_stat_activity;

-- Kill idle connections
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' 
AND query_start < NOW() - INTERVAL '1 hour';
```

---

## Transactions

### Basic Transactions
```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- or ROLLBACK;
```

### Isolation Levels
```sql
BEGIN ISOLATION LEVEL READ COMMITTED;    -- Default
BEGIN ISOLATION LEVEL REPEATABLE READ;  -- Consistent reads
BEGIN ISOLATION LEVEL SERIALIZABLE;     -- Strictest
```

### Optimistic Locking
```sql
UPDATE products 
SET stock = stock - 1, version = version + 1
WHERE id = 1 AND version = 5;

-- If affected_rows = 0, someone else modified it
```

---

## Useful Functions

### String Functions
```sql
CONCAT('Hello', ' ', 'World')  -- 'Hello World'
LENGTH('Hello')  -- 5
UPPER('hello')  -- 'HELLO'
LOWER('HELLO')  -- 'hello'
TRIM('  hello  ')  -- 'hello'
REPLACE('Hello World', 'World', 'PostgreSQL')  -- 'Hello PostgreSQL'
```

### Date/Time Functions
```sql
NOW()  -- Current timestamp
CURRENT_DATE  -- Current date
EXTRACT(YEAR FROM NOW())  -- 2024
AGE(NOW(), '2000-01-01')  -- Interval
DATE_TRUNC('day', NOW())  -- Truncate to day
```

### Aggregate Functions
```sql
COUNT(*)  -- Count rows
COUNT(DISTINCT email)  -- Count unique
SUM(amount)  -- Sum
AVG(amount)  -- Average
MIN(amount), MAX(amount)  -- Min/Max
```

### JSON Functions
```sql
SELECT data->>'name' FROM json_table;
SELECT data->'address'->>'city' FROM json_table;
SELECT json_agg(json_build_object('id', id, 'name', name)) FROM users;
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `\dt` | List tables |
| `\d table_name` | Describe table |
| `\di` | List indexes |
| `\du` | List users |
| `\l` | List databases |
| `\c dbname` | Connect to database |
| `\q` | Quit psql |

---

*Last updated: Phase 0*
