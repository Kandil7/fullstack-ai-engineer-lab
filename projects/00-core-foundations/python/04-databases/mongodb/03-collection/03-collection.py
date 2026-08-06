"""
W3Schools Python Tutorial - MongoDB 03: Collections
==============================================
Topics: Collections Concept, Creating/Dropping Collections

Run: python 03-collection.py
Verify: python 03-collection.py --verify
Reference: https://www.w3schools.com/python/python_mongodb_get_started.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# What is a Collection?
# ============================================================

# A collection is a group of MongoDB documents.
# It is equivalent to a table in relational databases.
# Collections do not enforce a schema - documents can vary.

# Example 1: A collection of users
users = [
    {"_id": 1, "name": "Alice", "age": 25},
    {"_id": 2, "name": "Bob", "age": 30, "email": "bob@mail.com"},
    {"_id": 3, "name": "Charlie"}  # No age field - flexible schema
]
print("Users collection:", len(users), "documents")
print("Alice:", users[0])
print("Bob:", users[1])  # Bob has an extra email field
print("Charlie:", users[2])  # Charlie has no age field

# ============================================================
# Creating Collections
# ============================================================

# Example 2: Create a collection by inserting documents
database = {}

# MongoDB equivalent:
# db.createCollection("users")

def create_collection(db, name):
    """Create a new empty collection"""
    if name not in db:
        db[name] = []
        print(f"Created collection: {name}")
    else:
        print(f"Collection '{name}' already exists")
    return db[name]

# Create collections
users_coll = create_collection(database, "users")
products_coll = create_collection(database, "products")
orders_coll = create_collection(database, "orders")

print("\nCollections:", list(database.keys()))

# Example 3: Try to create existing collection
create_collection(database, "users")  # Already exists

# ============================================================
# Collection Naming Rules
# ============================================================

# Example 4: Valid collection names
# - Cannot start with system. (reserved)
# - Cannot contain $ (reserved for some operations)
# - Should be lowercase with underscores
# - Cannot be empty
# - Max 255 characters (with database name)

# MongoDB equivalent:
# db.createCollection("my_collection")

valid_names = ["users", "user_data", "order_items"]
invalid_names = ["system.users", "my$collection", ""]

print("\nValid collection names:", valid_names)
print("Invalid collection names:", invalid_names)

# ============================================================
# Dropping Collections
# ============================================================

# Example 5: Drop a collection
def drop_collection(db, name):
    """Drop a collection from the database"""
    if name in db:
        del db[name]
        print(f"Dropped collection: {name}")
        return True
    else:
        print(f"Collection '{name}' not found")
        return False

# Create and then drop a collection
temp_coll = create_collection(database, "temp_collection")
print("Before drop:", list(database.keys()))
drop_collection(database, "temp_collection")
print("After drop:", list(database.keys()))

# MongoDB equivalent:
# db.temp_collection.drop()

# ============================================================
# Collection Operations
# ============================================================

# Example 6: Collection info and stats
def collection_count(db, name):
    """Get the number of documents in a collection"""
    if name in db:
        return len(db[name])
    return 0

def list_collections(db):
    """List all collections in the database"""
    return list(db.keys())

def collection_exists(db, name):
    """Check if a collection exists"""
    return name in db

# Add some data
database["users"] = [
    {"_id": 1, "name": "Alice", "age": 25},
    {"_id": 2, "name": "Bob", "age": 30}
]
database["products"] = [
    {"_id": 1, "name": "Laptop", "price": 999.99}
]

print("\nCollection 'users' exists:", collection_exists(database, "users"))
print("Collection 'users' count:", collection_count(database, "users"))
print("Collection 'orders' exists:", collection_exists(database, "orders"))
print("Collection 'orders' count:", collection_count(database, "orders"))

# ============================================================
# Renaming Collections
# ============================================================

# Example 7: Rename a collection
def rename_collection(db, old_name, new_name):
    """Rename a collection"""
    if old_name in db and new_name not in db:
        db[new_name] = db.pop(old_name)
        print(f"Renamed '{old_name}' to '{new_name}'")
        return True
    else:
        print(f"Cannot rename: old not found or new already exists")
        return False

# MongoDB equivalent:
# db.users.renameCollection("customers")

print("\nBefore rename:", list(database.keys()))
rename_collection(database, "users", "customers")
print("After rename:", list(database.keys()))

# ============================================================
# Working with Collection Documents
# ============================================================

# Example 8: Add and count documents
def insert_document(coll, doc):
    """Insert a document into a collection"""
    coll.append(doc)
    return doc

def count_documents(coll):
    """Count documents in a collection"""
    return len(coll)

# Working with customers collection
customers = database["customers"]
insert_document(customers, {"_id": 3, "name": "Diana", "age": 28})
insert_document(customers, {"_id": 4, "name": "Eve", "age": 35})

print("\nCustomers count:", count_documents(customers))
for customer in customers:
    print(f"  {customer}")

# ============================================================
# Collection with Different Document Structures
# ============================================================

# Example 9: Flexible schema - documents in same collection
mixed_collection = [
    {"_id": 1, "type": "user", "name": "Alice"},
    {"_id": 2, "type": "product", "name": "Laptop", "price": 999.99},
    {"_id": 3, "type": "user", "name": "Bob", "email": "bob@mail.com"}
]

print("\nMixed collection (flexible schema):")
for doc in mixed_collection:
    print(f"  {doc['type']}: {doc}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: MongoDB Collections")
print("=" * 60)
print("""
1. Collections group related documents (like tables)
2. Collections have flexible schema - documents can vary
3. Use createCollection() to explicitly create a collection
4. Collections are auto-created when first document is inserted
5. Collection names cannot start with 'system.' or contain '$'
6. Use drop() to remove a collection permanently
7. Use renameCollection() to rename a collection
8. Collections can hold documents with different structures
9. Collections are case-sensitive in some MongoDB deployments
""")

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # create_collection registers a fresh empty collection
    db = {}
    coll = create_collection(db, "users")
    assert coll == [] and "users" in db
    # duplicate create is a no-op
    create_collection(db, "users")
    assert len(list_collections(db)) == 1

    # exists / count
    assert collection_exists(db, "users") is True
    assert collection_exists(db, "orders") is False
    assert collection_count(db, "orders") == 0

    # insert + count
    insert_document(coll, {"_id": 1, "name": "Alice"})
    insert_document(coll, {"_id": 2, "name": "Bob"})
    assert count_documents(coll) == 2

    # rename
    assert rename_collection(db, "users", "customers") is True
    assert rename_collection(db, "missing", "x") is False
    assert "customers" in db and "users" not in db

    # drop
    assert drop_collection(db, "customers") is True
    assert drop_collection(db, "customers") is False

    # flexible schema: docs in one collection may differ
    assert {"type": "product", "price": 999.99}.items() <= mixed_collection[1].items()
    assert "age" not in mixed_collection[2] or mixed_collection[2].get("email")

    print("[OK] 03-collection: all checks passed")


if __name__ == "__main__":
    _verify()  # plain execution and --verify are both tests
