"""
Challenge 12: normalization — Reference Solution
=================================================
"""

import sqlite3


def split_csv_column(conn: sqlite3.Connection) -> list[tuple]:
    """1NF: one atomic tag per row."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, email TEXT, tags_csv TEXT)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS contact_tags (contact_id INTEGER, tag TEXT)")
    rows = []
    for cid, tags in conn.execute("SELECT id, tags_csv FROM contacts"):
        for tag in tags.split(","):
            tag = tag.strip()
            if tag:
                rows.append((cid, tag))
    conn.executemany(
        "INSERT INTO contact_tags (contact_id, tag) VALUES (?, ?)", rows)
    return [tuple(r) for r in conn.execute(
        "SELECT contact_id, tag FROM contact_tags ORDER BY contact_id, tag")]


def split_departments(conn: sqlite3.Connection) -> dict:
    """3NF: departments table owns the transitive dependency."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS employees ("
        "id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT, dept_location TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS departments (dept_name TEXT PRIMARY KEY, location TEXT)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS employees_normalized ("
        "id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT REFERENCES departments(dept_name))")

    depts = sorted({(d, loc) for _, _, d, loc in
                    conn.execute("SELECT * FROM employees")}, key=lambda x: x[0])
    conn.executemany(
        "INSERT INTO departments (dept_name, location) VALUES (?, ?)", depts)
    conn.execute(
        "INSERT INTO employees_normalized (name, dept_name) "
        "SELECT name, dept_name FROM employees")

    return {
        "departments": conn.execute("SELECT COUNT(*) FROM departments").fetchone()[0],
        "employees": conn.execute("SELECT COUNT(*) FROM employees_normalized").fetchone()[0],
        "locations": [r[0] for r in conn.execute(
            "SELECT DISTINCT location FROM departments ORDER BY location")],
    }


def build_star_schema(conn: sqlite3.Connection) -> dict:
    """Dimensions with surrogate keys + fact table joined from them."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS events_log (date TEXT, user TEXT, product TEXT, amount REAL)")
    conn.execute("CREATE TABLE dim_date (date_key INTEGER PRIMARY KEY, date TEXT UNIQUE)")
    conn.execute("CREATE TABLE dim_user (user_key INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.execute("CREATE TABLE dim_product (product_key INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.execute(
        "CREATE TABLE fact_sales ("
        "date_key INTEGER REFERENCES dim_date(date_key),"
        "user_key INTEGER REFERENCES dim_user(user_key),"
        "product_key INTEGER REFERENCES dim_product(product_key),"
        "amount REAL)")

    conn.execute("INSERT INTO dim_date (date) SELECT DISTINCT date FROM events_log")
    conn.execute("INSERT INTO dim_user (name) SELECT DISTINCT user FROM events_log")
    conn.execute("INSERT INTO dim_product (name) SELECT DISTINCT product FROM events_log")
    conn.execute(
        "INSERT INTO fact_sales (date_key, user_key, product_key, amount) "
        "SELECT d.date_key, u.user_key, p.product_key, e.amount "
        "FROM events_log e "
        "JOIN dim_date d ON d.date = e.date "
        "JOIN dim_user u ON u.name = e.user "
        "JOIN dim_product p ON p.name = e.product")

    reconstructed = [tuple(r) for r in conn.execute(
        "SELECT d.date, u.name, p.name, f.amount "
        "FROM fact_sales f "
        "JOIN dim_date d ON d.date_key = f.date_key "
        "JOIN dim_user u ON u.user_key = f.user_key "
        "JOIN dim_product p ON p.product_key = f.product_key ORDER BY f.amount")]
    return {
        "facts": conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0],
        "dims": {
            "date": conn.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0],
            "user": conn.execute("SELECT COUNT(*) FROM dim_user").fetchone()[0],
            "product": conn.execute("SELECT COUNT(*) FROM dim_product").fetchone()[0],
        },
        "reconstructed": reconstructed,
    }
