"""
W3Schools Python Tutorial - MongoDB 01: Getting Started
==============================================
Topics: What is MongoDB, Document Model vs Relational, PyMongo Concept, CRUD Overview

Run: python 01-getting-started.py
Verify: python 01-getting-started.py --verify
Reference: https://www.w3schools.com/python/python_mongodb_get_started.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# What is MongoDB?
# ============================================================

# MongoDB is a NoSQL document database that stores data in flexible,
# JSON-like documents instead of rows and columns.
#
# Key differences from relational databases:
# - MongoDB stores documents (dicts), not rows
# - Documents are grouped in collections, not tables
# - Schema is flexible - documents can have different fields
# - Data is stored as BSON (Binary JSON)

# Example 1: Relational vs Document Model
# Relational (SQL):
# | id | name  | age | email           |
# |----|-------|-----|-----------------|
# | 1  | Alice | 25  | alice@mail.com  |
#
# MongoDB:
# {
#     "_id": 1,
#     "name": "Alice",
#     "age": 25,
#     "email": "alice@mail.com"
# }

# ============================================================
# Document Model Basics
# ============================================================

# Example 2: A simple MongoDB document
user_document = {
    "_id": 1,
    "name": "Alice",
    "age": 25,
    "email": "alice@mail.com",
    "is_active": True
}
print("Simple document:", user_document)

# Example 3: Nested document
nested_document = {
    "_id": 2,
    "name": "Bob",
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62704"
    },
    "hobbies": ["reading", "coding", "hiking"]
}
print("Nested document:", nested_document)

# ============================================================
# Collections and Documents
# ============================================================

# In MongoDB, collections hold documents (like tables hold rows).
# A collection is a group of related documents.

# Example 4: A collection of users
users_collection = [
    {"_id": 1, "name": "Alice", "age": 25},
    {"_id": 2, "name": "Bob", "age": 30},
    {"_id": 3, "name": "Charlie", "age": 35}
]
print("\nUsers collection:")
for user in users_collection:
    print(f"  {user['name']} (age {user['age']})")

# ============================================================
# CRUD Operations Overview
# ============================================================

# CRUD = Create, Read, Update, Delete
# These are the four basic operations for any database.

# Example 5: CRUD overview with dicts
# CREATE - Adding a new document
new_user = {"_id": 4, "name": "Diana", "age": 28}
users_collection.append(new_user)
print("\nAfter CREATE:", users_collection[-1])

# READ - Retrieving a document
found_user = next((u for u in users_collection if u["_id"] == 2), None)
print("READ (Bob):", found_user)

# UPDATE - Modifying a document
for user in users_collection:
    if user["_id"] == 1:
        user["age"] = 26
        break
print("UPDATE (Alice):", users_collection[0])

# DELETE - Removing a document
users_collection = [u for u in users_collection if u["_id"] != 3]
print("DELETE (Charlie removed):", len(users_collection), "users remain")

# ============================================================
# PyMongo Concept
# ============================================================

# PyMongo is the official MongoDB driver for Python.
# Installation: pip install pymongo
# Import: from pymongo import MongoClient

# Example 6: PyMongo connection concept (NOT actual code)
# from pymongo import MongoClient
# client = MongoClient("mongodb://localhost:27017/")
# db = client["mydb"]
# collection = db["users"]

# MongoDB equivalent operations:
# db.users.insert_one({"name": "Alice", "age": 25})
# db.users.find({"age": {"$gt": 25}})

# ============================================================
# Database and Collection Setup
# ============================================================

# Example 7: Simulating a database
database = {
    "users": [
        {"_id": 1, "name": "Alice", "age": 25},
        {"_id": 2, "name": "Bob", "age": 30},
    ],
    "products": [
        {"_id": 1, "name": "Laptop", "price": 999.99},
        {"_id": 2, "name": "Mouse", "price": 29.99},
    ]
}

print("\nDatabase collections:", list(database.keys()))
print("Users count:", len(database["users"]))
print("Products count:", len(database["products"]))

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: MongoDB Getting Started")
print("=" * 60)
print("""
1. MongoDB is a NoSQL document database
2. Documents are JSON-like dicts with key-value pairs
3. Collections group related documents (like tables)
4. Documents can have nested structures and arrays
5. CRUD operations: Create, Read, Update, Delete
6. PyMongo is the official Python driver for MongoDB
7. MongoDB stores data as BSON (Binary JSON)
8. Schema is flexible - documents can vary in structure
""")

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Document model: nested docs and arrays are first-class
    assert nested_document["address"]["city"] == "Springfield"
    assert nested_document["hobbies"] == ["reading", "coding", "hiking"]

    # CRUD on a fresh collection
    coll = [
        {"_id": 1, "name": "Alice", "age": 25},
        {"_id": 2, "name": "Bob", "age": 30},
    ]
    # CREATE appends
    coll.append({"_id": 3, "name": "Carol", "age": 27})
    assert len(coll) == 3
    # READ finds by _id
    assert next(u for u in coll if u["_id"] == 2)["name"] == "Bob"
    # UPDATE mutates the matched document
    for u in coll:
        if u["_id"] == 1:
            u["age"] = 26
    assert coll[0]["age"] == 26
    # DELETE removes the document
    coll = [u for u in coll if u["_id"] != 3]
    assert len(coll) == 2

    # Database shape: collections hold lists of documents
    assert set(database.keys()) == {"users", "products"}
    assert len(database["users"]) == 2 and len(database["products"]) == 2

    print("[OK] 01-getting-started: all checks passed")


if __name__ == "__main__":
    _verify()  # plain execution and --verify are both tests
