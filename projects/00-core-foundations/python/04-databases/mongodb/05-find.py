"""
W3Schools Python Tutorial - MongoDB 05: Find Documents
==============================================
Topics: find() for all, find() with query, find_one(), querying nested fields, projection

Run: python 05-find.py
Reference: https://www.w3schools.com/python/python_mongodb_find.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

users = [
    {"_id": 1, "name": "Alice", "age": 25, "email": "alice@mail.com", "city": "New York", "active": True},
    {"_id": 2, "name": "Bob", "age": 30, "email": "bob@mail.com", "city": "Boston", "active": True},
    {"_id": 3, "name": "Charlie", "age": 35, "email": "charlie@mail.com", "city": "New York", "active": False},
    {"_id": 4, "name": "Diana", "age": 28, "email": "diana@mail.com", "city": "Chicago", "active": True},
    {"_id": 5, "name": "Eve", "age": 32, "email": "eve@mail.com", "city": "Boston", "active": True}
]

# ============================================================
# Find All Documents
# ============================================================

# Example 1: Find all documents
# MongoDB equivalent: db.users.find()

def find_all(collection):
    """Return all documents in a collection"""
    return collection

all_users = find_all(users)
print("All users:", len(all_users))
for user in all_users:
    print(f"  {user['name']}")

# ============================================================
# Find with Query
# ============================================================

# Example 2: Find documents matching a condition
# MongoDB equivalent: db.users.find({"age": 25})

def find(collection, query):
    """Find documents matching the query"""
    results = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if key not in doc or doc[key] != value:
                match = False
                break
        if match:
            results.append(doc)
    return results

age_25 = find(users, {"age": 25})
print("\nUsers with age 25:", age_25)

# Example 3: Find by city
new_york_users = find(users, {"city": "New York"})
print("\nUsers in New York:", len(new_york_users))
for user in new_york_users:
    print(f"  {user['name']}")

# ============================================================
# Find One Document
# ============================================================

# Example 4: Find first matching document
# MongoDB equivalent: db.users.find_one({"name": "Bob"})

def find_one(collection, query):
    """Find the first document matching the query"""
    for doc in collection:
        match = True
        for key, value in query.items():
            if key not in doc or doc[key] != value:
                match = False
                break
        if match:
            return doc
    return None

bob = find_one(users, {"name": "Bob"})
print("\nFind one (Bob):", bob)

# Example 5: Find one with no match
not_found = find_one(users, {"name": "Zack"})
print("Find one (Zack):", not_found)

# ============================================================
# Querying Nested Fields
# ============================================================

# Example 6: Query nested documents
orders = [
    {"_id": 1, "customer": "Alice", "items": [{"name": "Laptop", "price": 999}, {"name": "Mouse", "price": 29}]},
    {"_id": 2, "customer": "Bob", "items": [{"name": "Keyboard", "price": 79}]},
    {"_id": 3, "customer": "Charlie", "items": [{"name": "Monitor", "price": 399}, {"name": "Webcam", "price": 89}]}
]

def find_nested(collection, query):
    """Find documents with nested field queries"""
    results = []
    for doc in collection:
        match = True
        for path, value in query.items():
            keys = path.split(".")
            current = doc
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    match = False
                    break
            if match and current != value:
                match = False
        if match:
            results.append(doc)
    return results

# MongoDB equivalent:
# db.orders.find({"items.name": "Laptop"})

laptop_orders = find_nested(orders, {"items.name": "Laptop"})
print("\nOrders with Laptop:", len(laptop_orders))

# ============================================================
# Projection - Select Specific Fields
# ============================================================

# Example 7: Projection - include specific fields
# MongoDB equivalent: db.users.find({}, {"name": 1, "email": 1})

def find_projection(collection, query, projection):
    """Find documents with field projection"""
    results = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if key not in doc or doc[key] != value:
                match = False
                break
        
        if match:
            if projection:
                # Determine mode from non-_id fields (MongoDB forbids mixing
                # inclusion and exclusion, except for _id which can be excluded
                # in either mode).
                modes = [v for field, v in projection.items() if field != "_id"]
                is_exclusion = any(v == 0 for v in modes)

                if is_exclusion:
                    # Exclusion: copy the whole document, drop listed fields.
                    projected = dict(doc)
                    for field, exclude in projection.items():
                        if exclude == 0:
                            projected.pop(field, None)
                else:
                    # Inclusion: keep only the listed fields.
                    projected = {}
                    for field, include in projection.items():
                        if include == 1 and field in doc:
                            projected[field] = doc[field]
                    # _id is included by default unless explicitly excluded.
                    if projection.get("_id") != 0:
                        projected["_id"] = doc["_id"]
                results.append(projected)
            else:
                results.append(doc)

    return results

# Include only name and email
name_email = find_projection(users, {}, {"name": 1, "email": 1})
print("\nProjection (name, email):")
for user in name_email:
    print(f"  {user}")

# Example 8: Exclude specific fields (all other fields are returned)
# MongoDB equivalent: db.users.find({}, {"password": 0, "_id": 0})

no_password_users = find_projection(users, {}, {"password": 0, "_id": 0})
print("\nUsers without password (all other fields kept):")
for user in no_password_users:
    print(f"  {user}")

# ============================================================
# Query Operators (Basic)
# ============================================================

# Example 9: Greater than, less than queries
def find_gt(collection, field, value):
    """Find documents where field > value"""
    return [doc for doc in collection if field in doc and doc[field] > value]

def find_lt(collection, field, value):
    """Find documents where field < value"""
    return [doc for doc in collection if field in doc and doc[field] < value]

# MongoDB equivalent:
# db.users.find({"age": {"$gt": 25}})
# db.users.find({"age": {"$lt": 30}})

older_than_25 = find_gt(users, "age", 25)
print("\nUsers older than 25:")
for user in older_than_25:
    print(f"  {user['name']}: {user['age']}")

younger_than_30 = find_lt(users, "age", 30)
print("\nUsers younger than 30:")
for user in younger_than_30:
    print(f"  {user['name']}: {user['age']}")

# ============================================================
# Count Documents
# ============================================================

# Example 10: Count matching documents
# MongoDB equivalent: db.users.count_documents({"active": True})

def count_documents(collection, query=None):
    """Count documents matching query"""
    if query is None:
        return len(collection)
    count = 0
    for doc in collection:
        match = True
        for key, value in query.items():
            if key not in doc or doc[key] != value:
                match = False
                break
        if match:
            count += 1
    return count

print("\nTotal users:", count_documents(users))
print("Active users:", count_documents(users, {"active": True}))
print("NY users:", count_documents(users, {"city": "New York"}))

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Finding Documents")
print("=" * 60)
print("""
1. find() returns all documents matching a query
2. find_one() returns the first matching document
3. Query with {field: value} to match exact values
4. Use dot notation for nested fields: {"address.city": "NY"}
5. Projection controls which fields are returned
6. {field: 1} includes a field, {field: 0} excludes it
7. _id is included by default unless explicitly excluded
8. Comparison operators: $gt, $lt, $gte, $lte, $ne
9. count_documents() counts matching documents
10. find() with empty query returns all documents
""")
