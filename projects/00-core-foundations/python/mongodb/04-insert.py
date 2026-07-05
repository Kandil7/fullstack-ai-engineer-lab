"""
W3Schools Python Tutorial - MongoDB 04: Insert Documents
==============================================
Topics: insert_one, insert_many, _id Field, Automatic IDs, Inserting Documents

Run: python 04-insert.py
Reference: https://www.w3schools.com/python/python_mongodb_insert.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Insert One Document
# ============================================================

# Example 1: Insert a single document
users = []
next_id = 1

def insert_one(collection, document):
    """Insert one document into a collection"""
    global next_id
    if "_id" not in document:
        document["_id"] = next_id
        next_id += 1
    collection.append(document)
    return document["_id"]

# MongoDB equivalent:
# db.users.insert_one({"name": "Alice", "age": 25})

doc_id = insert_one(users, {"name": "Alice", "age": 25, "email": "alice@mail.com"})
print("Inserted document with _id:", doc_id)
print("Users:", users)

# Example 2: Insert with explicit _id
doc_id = insert_one(users, {"_id": 100, "name": "Bob", "age": 30})
print("\nInserted with explicit _id:", doc_id)
print("Users:", users)

# ============================================================
# The _id Field
# ============================================================

# Every MongoDB document must have an _id field.
# If you don't provide one, MongoDB auto-generates an ObjectId.

# Example 3: _id is required
# MongoDB equivalent:
# { "_id": ObjectId("..."), "name": "Charlie" }

# Example 4: Custom _id values
users = []
insert_one(users, {"_id": "user001", "name": "Alice"})
insert_one(users, {"_id": "user002", "name": "Bob"})
insert_one(users, {"_id": 1001, "name": "Charlie"})

print("\nUsers with custom _ids:")
for user in users:
    print(f"  _id={user['_id']}, name={user['name']}")

# ============================================================
# Insert Many Documents
# ============================================================

# Example 5: Insert multiple documents at once
def insert_many(collection, documents):
    """Insert multiple documents into a collection"""
    global next_id
    ids = []
    for doc in documents:
        if "_id" not in doc:
            doc["_id"] = next_id
            next_id += 1
        collection.append(doc)
        ids.append(doc["_id"])
    return ids

# MongoDB equivalent:
# db.users.insert_many([
#     {"name": "David", "age": 28},
#     {"name": "Eve", "age": 32},
#     {"name": "Frank", "age": 45}
# ])

users = []
new_ids = insert_many(users, [
    {"name": "David", "age": 28, "city": "Boston"},
    {"name": "Eve", "age": 32, "city": "New York"},
    {"name": "Frank", "age": 45, "city": "Chicago"}
])

print("\nInserted IDs:", new_ids)
print("Users:", users)

# ============================================================
# Insert with Nested Documents
# ============================================================

# Example 6: Insert documents with nested structures
products = []

insert_many(products, [
    {
        "name": "Laptop",
        "price": 999.99,
        "specs": {
            "ram": "16GB",
            "storage": "512GB SSD",
            "cpu": "Intel i7"
        },
        "tags": ["electronics", "computers"]
    },
    {
        "name": "Mouse",
        "price": 29.99,
        "specs": {
            "type": "wireless",
            "dpi": 1600
        },
        "tags": ["electronics", "accessories"]
    }
])

print("\nProducts with nested docs:")
for product in products:
    print(f"  {product['name']}: ${product['price']}")
    print(f"    Specs: {product['specs']}")

# ============================================================
# Insert with Arrays
# ============================================================

# Example 7: Documents with array fields
students = []

insert_many(students, [
    {
        "name": "Alice",
        "courses": ["Math", "Science", "English"],
        "grades": [95, 88, 92]
    },
    {
        "name": "Bob",
        "courses": ["Math", "History"],
        "grades": [78, 85]
    }
])

print("\nStudents with arrays:")
for student in students:
    print(f"  {student['name']}: {len(student['courses'])} courses")
    print(f"    Courses: {student['courses']}")
    print(f"    Grades: {student['grades']}")

# ============================================================
# Insert with Date Fields
# ============================================================

# Example 8: Documents with timestamps
from datetime import datetime

orders = []

insert_many(orders, [
    {
        "customer": "Alice",
        "items": ["Laptop", "Mouse"],
        "total": 1029.98,
        "created_at": datetime.now().isoformat()
    },
    {
        "customer": "Bob",
        "items": ["Keyboard"],
        "total": 79.99,
        "created_at": datetime.now().isoformat()
    }
])

print("\nOrders with timestamps:")
for order in orders:
    print(f"  {order['customer']}: ${order['total']} at {order['created_at']}")

# ============================================================
# Insert with Validation
# ============================================================

# Example 9: Validate before insert
def insert_with_validation(collection, document, required_fields):
    """Insert document only if required fields are present"""
    for field in required_fields:
        if field not in document:
            print(f"Validation failed: missing '{field}'")
            return None
    
    if "_id" not in document:
        document["_id"] = next_id
        # increment next_id here in real code
    
    collection.append(document)
    return document.get("_id")

# MongoDB equivalent:
# db.createCollection("users", {
#     validator: { $jsonSchema: {
#         required: ["name", "email"],
#         properties: {
#             name: { bsonType: "string" },
#             email: { bsonType: "string" }
#         }
#     }}
# })

validated_users = []
result = insert_with_validation(validated_users, 
    {"name": "Grace", "email": "grace@mail.com"}, 
    ["name", "email"])
print("\nValid insert result:", result)

result = insert_with_validation(validated_users, 
    {"name": "Hank"},  # Missing email
    ["name", "email"])
print("Invalid insert result:", result)

# ============================================================
# Bulk Insert Performance
# ============================================================

# Example 10: Bulk insert comparison
import time

def bulk_insert_simple(collection, count):
    """Insert documents one by one"""
    for i in range(count):
        collection.append({"_id": i, "value": f"item_{i}"})

def bulk_insert_batch(collection, count):
    """Insert documents as a batch"""
    docs = [{"_id": i, "value": f"item_{i}"} for i in range(count)]
    collection.extend(docs)

# Compare performance
collection1 = []
collection2 = []

start = time.time()
bulk_insert_simple(collection1, 10000)
simple_time = time.time() - start

start = time.time()
bulk_insert_batch(collection2, 10000)
batch_time = time.time() - start

print(f"\nBulk insert performance (10000 docs):")
print(f"  One by one: {simple_time:.4f}s")
print(f"  Batch: {batch_time:.4f}s")
print(f"  Speedup: {simple_time/batch_time:.2f}x")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Inserting Documents")
print("=" * 60)
print("""
1. insert_one() adds a single document to a collection
2. insert_many() adds multiple documents at once
3. Every document must have an _id field (auto-generated if omitted)
4. _id can be any type: ObjectId, string, integer, etc.
5. Documents can contain nested objects and arrays
6. MongoDB is schema-flexible - documents can have different fields
7. Batch inserts are faster than individual inserts
8. Validate required fields before inserting
9. Use timestamps for audit trails
10. insert_many() returns a list of inserted _id values
""")
