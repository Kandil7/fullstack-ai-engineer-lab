"""
W3Schools Python Tutorial - MongoDB 09: Delete Documents
==============================================
Topics: delete_one(), delete_many(), Deleting with Filters

Run: python 09-delete.py
Verify: python 09-delete.py --verify
Reference: https://www.w3schools.com/python/python_mongodb_delete.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

users = [
    {"_id": 1, "name": "Alice", "age": 25, "city": "New York", "status": "active"},
    {"_id": 2, "name": "Bob", "age": 30, "city": "Boston", "status": "active"},
    {"_id": 3, "name": "Charlie", "age": 35, "city": "New York", "status": "inactive"},
    {"_id": 4, "name": "Diana", "age": 28, "city": "Chicago", "status": "active"},
    {"_id": 5, "name": "Eve", "age": 32, "city": "Boston", "status": "inactive"},
    {"_id": 6, "name": "Frank", "age": 45, "city": "Chicago", "status": "active"}
]

# ============================================================
# Delete One Document
# ============================================================

# Example 1: Delete one document by _id
# MongoDB equivalent: db.users.delete_one({"_id": 1})

def delete_one_by_id(collection, doc_id):
    """Delete one document by its _id"""
    for i, doc in enumerate(collection):
        if doc["_id"] == doc_id:
            deleted = collection.pop(i)
            return {"deleted_count": 1, "deleted": deleted}
    return {"deleted_count": 0, "deleted": None}

# Make a copy for demonstration
users_copy = users.copy()
users_copy = list(users_copy)  # Deep copy for safety

# Actually, let's work with a fresh copy each time
def reset_users():
    return [
        {"_id": 1, "name": "Alice", "age": 25, "city": "New York", "status": "active"},
        {"_id": 2, "name": "Bob", "age": 30, "city": "Boston", "status": "active"},
        {"_id": 3, "name": "Charlie", "age": 35, "city": "New York", "status": "inactive"},
        {"_id": 4, "name": "Diana", "age": 28, "city": "Chicago", "status": "active"},
        {"_id": 5, "name": "Eve", "age": 32, "city": "Boston", "status": "inactive"},
        {"_id": 6, "name": "Frank", "age": 45, "city": "Chicago", "status": "active"}
    ]

users = reset_users()
result = delete_one_by_id(users, 3)
print("Delete one by _id=3:", result)
print("Remaining users:", len(users))

# ============================================================
# Delete One by Query
# ============================================================

# Example 2: Delete first matching document
# MongoDB equivalent: db.users.delete_one({"name": "Bob"})

def delete_one_by_query(collection, query):
    """Delete the first document matching the query"""
    for i, doc in enumerate(collection):
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        if match:
            deleted = collection.pop(i)
            return {"deleted_count": 1, "deleted": deleted}
    return {"deleted_count": 0, "deleted": None}

users = reset_users()
result = delete_one_by_query(users, {"name": "Bob"})
print("\nDelete one (name=Bob):", result)
print("Remaining users:", [u["name"] for u in users])

# ============================================================
# Delete Many Documents
# ============================================================

# Example 3: Delete all matching documents
# MongoDB equivalent: db.users.delete_many({"status": "inactive"})

def delete_many_by_query(collection, query):
    """Delete all documents matching the query"""
    deleted = []
    remaining = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        if match:
            deleted.append(doc)
        else:
            remaining.append(doc)
    
    # Replace collection contents
    collection.clear()
    collection.extend(remaining)
    
    return {"deleted_count": len(deleted), "deleted": deleted}

users = reset_users()
result = delete_many_by_query(users, {"status": "inactive"})
print("\nDelete many (status=inactive):")
print(f"  Deleted: {result['deleted_count']} documents")
print(f"  Remaining: {len(users)} users")
for user in users:
    print(f"    {user['name']}: {user['status']}")

# ============================================================
# Delete with Comparison Operators
# ============================================================

# Example 4: Delete users younger than 30
# MongoDB equivalent: db.users.delete_many({"age": {"$lt": 30}})

def delete_many_with_operator(collection, field, operator, value):
    """Delete documents using comparison operators"""
    deleted = []
    remaining = []
    
    for doc in collection:
        doc_val = doc.get(field)
        should_delete = False
        
        if operator == "$lt" and doc_val < value:
            should_delete = True
        elif operator == "$lte" and doc_val <= value:
            should_delete = True
        elif operator == "$gt" and doc_val > value:
            should_delete = True
        elif operator == "$gte" and doc_val >= value:
            should_delete = True
        elif operator == "$ne" and doc_val != value:
            should_delete = True
        
        if should_delete:
            deleted.append(doc)
        else:
            remaining.append(doc)
    
    collection.clear()
    collection.extend(remaining)
    
    return {"deleted_count": len(deleted), "deleted": deleted}

users = reset_users()
result = delete_many_with_operator(users, "age", "$lt", 30)
print("\nDelete users younger than 30:")
print(f"  Deleted: {result['deleted_count']}")
for user in users:
    print(f"    {user['name']}: age {user['age']}")

# ============================================================
# Delete with $in Operator
# ============================================================

# Example 5: Delete users in specific cities
# MongoDB equivalent: db.users.delete_many({"city": {"$in": ["New York", "Chicago"]}})

def delete_many_in(collection, field, values):
    """Delete documents where field is in values list"""
    deleted = []
    remaining = []
    
    for doc in collection:
        if doc.get(field) in values:
            deleted.append(doc)
        else:
            remaining.append(doc)
    
    collection.clear()
    collection.extend(remaining)
    
    return {"deleted_count": len(deleted), "deleted": deleted}

users = reset_users()
result = delete_many_in(users, "city", ["New York", "Chicago"])
print("\nDelete users in NY or Chicago:")
print(f"  Deleted: {result['deleted_count']}")
for user in users:
    print(f"    {user['name']}: {user['city']}")

# ============================================================
# Delete All Documents
# ============================================================

# Example 6: Delete all documents in a collection
# MongoDB equivalent: db.users.delete_many({})

def delete_all(collection):
    """Delete all documents from a collection"""
    count = len(collection)
    collection.clear()
    return {"deleted_count": count}

users = reset_users()
result = delete_all(users)
print("\nDelete all:", result)
print("Remaining:", len(users), "users")

# ============================================================
# Delete with Complex Queries
# ============================================================

# Example 7: Delete with AND conditions
# MongoDB equivalent:
# db.users.delete_many({"$and": [{"status": "active"}, {"age": {"$gt": 30}}]})

def delete_many_complex(collection, conditions):
    """Delete documents matching complex conditions"""
    deleted = []
    remaining = []
    
    for doc in collection:
        should_delete = True
        for condition in conditions:
            field = list(condition.keys())[0]
            value = condition[field]
            
            if isinstance(value, dict):
                for op, val in value.items():
                    doc_val = doc.get(field)
                    if op == "$gt" and not (doc_val > val):
                        should_delete = False
                    elif op == "$lt" and not (doc_val < val):
                        should_delete = False
                    elif op == "$ne" and not (doc_val != val):
                        should_delete = False
            else:
                if doc.get(field) != value:
                    should_delete = False
        
        if should_delete:
            deleted.append(doc)
        else:
            remaining.append(doc)
    
    collection.clear()
    collection.extend(remaining)
    
    return {"deleted_count": len(deleted), "deleted": deleted}

users = reset_users()
result = delete_many_complex(users, [
    {"status": "active"},
    {"age": {"$gt": 30}}
])
print("\nDelete active users older than 30:")
print(f"  Deleted: {result['deleted_count']}")
for user in users:
    print(f"    {user['name']}: age {user['age']}, {user['status']}")

# ============================================================
# Return Value
# ============================================================

# Example 8: Delete returns deleted document
users = reset_users()
result = delete_one_by_query(users, {"name": "Alice"})
print("\nDelete with return value:")
print(f"  Deleted count: {result['deleted_count']}")
print(f"  Deleted document: {result['deleted']}")

# ============================================================
# Practical Examples
# ============================================================

# Example 9: Soft delete vs hard delete
users = reset_users()

def soft_delete_one(collection, doc_id):
    """Soft delete - mark as deleted instead of removing"""
    for doc in collection:
        if doc["_id"] == doc_id:
            doc["deleted"] = True
            doc["deleted_at"] = "2024-01-15"
            return {"deleted_count": 1, "deleted": doc}
    return {"deleted_count": 0}

result = soft_delete_one(users, 2)
print("\nSoft delete (Bob):")
print(f"  Result: {result}")
print("  Bob still in collection:", any(u["name"] == "Bob" for u in users))
print("  Bob marked deleted:", result["deleted"].get("deleted"))

# Example 10: Delete with confirmation
def delete_with_confirm(collection, query, confirm=False):
    """Delete with optional confirmation"""
    count = len([doc for doc in collection if all(doc.get(k) == v for k, v in query.items())])
    
    if not confirm:
        print(f"  Would delete {count} documents. Pass confirm=True to proceed.")
        return {"deleted_count": 0}
    
    return delete_many_by_query(collection, query)

users = reset_users()
print("\nDelete without confirmation:")
delete_with_confirm(users, {"status": "inactive"}, confirm=False)

print("\nDelete with confirmation:")
result = delete_with_confirm(users, {"status": "inactive"}, confirm=True)
print(f"  Deleted: {result['deleted_count']}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Deleting Documents")
print("=" * 60)
print("""
1. delete_one() removes the first matching document
2. delete_many() removes all matching documents
3. delete_one({}) deletes the first document in collection
4. delete_many({}) deletes ALL documents (use with caution!)
5. Returns {deletedCount: N} with number of deleted docs
6. Use comparison operators for complex filters
7. Consider soft delete for audit trails
8. Always validate queries before delete_many()
9. Back up data before bulk delete operations
""")

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # delete one by _id
    u1 = reset_users()
    r1 = delete_one_by_id(u1, 3)
    assert r1["deleted_count"] == 1 and len(u1) == 5
    assert delete_one_by_id(u1, 999)["deleted_count"] == 0

    # delete one by query
    u2 = reset_users()
    r2 = delete_one_by_query(u2, {"name": "Bob"})
    assert r2["deleted_count"] == 1 and "Bob" not in [d["name"] for d in u2]

    # delete many by query
    u3 = reset_users()
    r3 = delete_many_by_query(u3, {"status": "inactive"})
    assert r3["deleted_count"] == 2 and len(u3) == 4

    # delete with comparison operator
    u4 = reset_users()
    r4 = delete_many_with_operator(u4, "age", "$lt", 30)
    assert r4["deleted_count"] == 2  # Alice(25), Diana(28)
    assert all(d["age"] >= 30 for d in u4)

    # delete with $in
    u5 = reset_users()
    r5 = delete_many_in(u5, "city", ["New York", "Chicago"])
    assert r5["deleted_count"] == 4  # Alice, Charlie, Diana, Frank

    # delete all
    u6 = reset_users()
    assert delete_all(u6)["deleted_count"] == 6 and len(u6) == 0

    # complex AND conditions: active AND age > 30 -> Frank only
    # (Eve is inactive in this dataset)
    u7 = reset_users()
    r7 = delete_many_complex(u7, [{"status": "active"}, {"age": {"$gt": 30}}])
    assert r7["deleted_count"] == 1  # Frank(45, active)
    assert all(d["status"] == "inactive" or d["age"] <= 30 for d in u7)

    # soft delete: document remains, marked deleted
    u8 = reset_users()
    soft_delete_one(u8, 2)
    assert any(d["_id"] == 2 and d.get("deleted") for d in u8)

    # confirmation guard
    u9 = reset_users()
    assert delete_with_confirm(u9, {"status": "inactive"}, confirm=False)["deleted_count"] == 0
    assert len(u9) == 6
    assert delete_with_confirm(u9, {"status": "inactive"}, confirm=True)["deleted_count"] == 2

    print("[OK] 09-delete: all checks passed")


if __name__ == "__main__":
    _verify()  # plain execution and --verify are both tests
