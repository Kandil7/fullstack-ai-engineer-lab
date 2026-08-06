"""
W3Schools Python Tutorial - MongoDB 02: Databases
==============================================
Topics: Databases Concept, Creating/Using Databases, Collection Concept

Run: python 02-databases.py
Verify: python 02-databases.py --verify
Reference: https://www.w3schools.com/python/python_mongodb_get_started.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# What is a MongoDB Database?
# ============================================================

# A MongoDB database holds collections of documents.
# MongoDB creates databases lazily - they exist only when data is added.

# Example 1: Creating a database structure
database = {}
print("Empty database:", database)

# Example 2: Adding a collection to a database
database["users"] = []
print("Database after adding users collection:", list(database.keys()))

# MongoDB equivalent:
# use mydb  // switches to mydb (creates if doesn't exist)
# show dbs   // lists all databases

# ============================================================
# Creating Databases
# ============================================================

# Example 3: Creating multiple databases
databases = {
    "school": {
        "students": [
            {"_id": 1, "name": "Alice", "grade": "A"},
            {"_id": 2, "name": "Bob", "grade": "B"}
        ],
        "teachers": [
            {"_id": 1, "name": "Mr. Smith", "subject": "Math"},
            {"_id": 2, "name": "Ms. Jones", "subject": "Science"}
        ]
    },
    "store": {
        "products": [
            {"_id": 1, "name": "Laptop", "price": 999.99},
            {"_id": 2, "name": "Mouse", "price": 29.99}
        ],
        "orders": [
            {"_id": 1, "customer": "Alice", "total": 1029.98}
        ]
    }
}

print("\nAvailable databases:", list(databases.keys()))

# Example 4: Accessing a specific database
school_db = databases["school"]
print("School database collections:", list(school_db.keys()))
print("Students:", len(school_db["students"]))
print("Teachers:", len(school_db["teachers"]))

# ============================================================
# Using Databases
# ============================================================

# Example 5: Database operations
def list_databases(dbs):
    """List all databases"""
    print("Databases:", list(dbs.keys()))

def create_database(dbs, name):
    """Create a new database"""
    dbs[name] = {}
    print(f"Created database: {name}")

def drop_database(dbs, name):
    """Drop a database"""
    if name in dbs:
        del dbs[name]
        print(f"Dropped database: {name}")
    else:
        print(f"Database {name} not found")

# MongoDB equivalent:
# show dbs
# db.dropDatabase()

list_databases(databases)
create_database(databases, "analytics")
list_databases(databases)
drop_database(databases, "analytics")
list_databases(databases)

# ============================================================
# Collection Concept
# ============================================================

# Collections are groups of documents in a database.
# They are similar to tables in relational databases.

# Example 6: Working with collections
school_db = databases["school"]

# Add a new collection
school_db["courses"] = [
    {"_id": 1, "name": "Python 101", "credits": 3},
    {"_id": 2, "name": "Data Science", "credits": 4}
]

print("\nSchool collections:", list(school_db.keys()))

# Example 7: Collection operations
def list_collections(db):
    """List all collections in a database"""
    return list(db.keys())

def create_collection(db, name):
    """Create a new collection"""
    db[name] = []
    print(f"Created collection: {name}")

def drop_collection(db, name):
    """Drop a collection"""
    if name in db:
        del db[name]
        print(f"Dropped collection: {name}")

print("Collections:", list_collections(school_db))
create_collection(school_db, "grades")
print("Collections after create:", list_collections(school_db))
drop_collection(school_db, "grades")
print("Collections after drop:", list_collections(school_db))

# ============================================================
# Database Naming Rules
# ============================================================

# Example 8: Valid database names
# - Cannot contain: . $ / \ or null character
# - Should be lowercase
# - Max 64 characters
# - Case-sensitive in some systems

# MongoDB equivalent:
# db.getCollectionNames()

valid_names = ["mydb", "user_data", "analytics_db"]
invalid_names = ["my.db", "my$db", ""]

print("\nValid database names:", valid_names)
print("Invalid database names:", invalid_names)

# ============================================================
# Using Database and Collection
# ============================================================

# Example 9: Complete workflow
def use_database(dbs, name):
    """Switch to a database (create if not exists)"""
    if name not in dbs:
        dbs[name] = {}
        print(f"Created and switched to database: {name}")
    else:
        print(f"Switched to database: {name}")
    return dbs[name]

def use_collection(db, name):
    """Switch to a collection (create if not exists)"""
    if name not in db:
        db[name] = []
        print(f"Created and switched to collection: {name}")
    else:
        print(f"Switched to collection: {name}")
    return db[name]

# Workflow: use database, use collection, insert document
db = use_database(databases, "inventory")
collection = use_collection(db, "items")
collection.append({"_id": 1, "name": "Widget", "quantity": 100})
print(f"Inserted into {db}: {collection}")

# ============================================================
# Show Databases and Collections
# ============================================================

# Example 10: List all databases and their collections
print("\n" + "=" * 40)
print("All Databases and Collections")
print("=" * 40)

for db_name, db_contents in databases.items():
    print(f"\nDatabase: {db_name}")
    for coll_name, docs in db_contents.items():
        print(f"  Collection: {coll_name} ({len(docs)} documents)")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: MongoDB Databases")
print("=" * 60)
print("""
1. A database holds collections of documents
2. MongoDB creates databases lazily (when data is added)
3. Collections are like tables in relational databases
4. Use show dbs to list all databases
5. Use db.collectionName to access a collection
6. Database names cannot contain . $ / \ or null
7. Collections are created automatically when documents are inserted
8. Use db.dropDatabase() to remove a database
""")

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # create/drop database
    dbs = {}
    create_database(dbs, "analytics")
    assert "analytics" in dbs
    drop_database(dbs, "analytics")
    assert "analytics" not in dbs
    drop_database(dbs, "missing")  # no-op, must not raise

    # create/drop collections (rename lives in the collection lecture)
    db = {}
    create_collection(db, "users")
    assert list_collections(db) == ["users"]
    create_collection(db, "users")  # duplicate is a no-op
    assert len(list_collections(db)) == 1
    drop_collection(db, "users")
    assert list_collections(db) == []

    # use_database / use_collection lazily create
    dbs2 = {}
    inv = use_database(dbs2, "inventory")
    items = use_collection(inv, "items")
    items.append({"_id": 1, "name": "Widget", "quantity": 100})
    assert dbs2["inventory"]["items"][0]["name"] == "Widget"

    # multi-database model (the demo additionally created "inventory")
    assert {"school", "store"} <= set(databases.keys())
    assert len(databases["school"]["students"]) == 2
    assert databases["inventory"]["items"][0]["name"] == "Widget"

    print("[OK] 02-databases: all checks passed")


if __name__ == "__main__":
    _verify()  # plain execution and --verify are both tests
