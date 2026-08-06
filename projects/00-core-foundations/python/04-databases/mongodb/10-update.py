"""
W3Schools Python Tutorial - MongoDB 10: Update Documents
==============================================
Topics: update_one(), update_many(), $set, $unset, $inc, $push, upsert

Run: python 10-update.py
Verify: python 10-update.py --verify
Reference: https://www.w3schools.com/python/python_mongodb_update.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

def reset_users():
    return [
        {"_id": 1, "name": "Alice", "age": 25, "email": "alice@mail.com", "status": "active", "scores": [85, 90]},
        {"_id": 2, "name": "Bob", "age": 30, "email": "bob@mail.com", "status": "active", "scores": [78, 82]},
        {"_id": 3, "name": "Charlie", "age": 35, "email": "charlie@mail.com", "status": "inactive", "scores": [92, 88]},
        {"_id": 4, "name": "Diana", "age": 28, "email": "diana@mail.com", "status": "active", "scores": [95, 91]}
    ]

users = reset_users()

# ============================================================
# Update One Document
# ============================================================

# Example 1: Update a single field with $set
# MongoDB equivalent: db.users.update_one({"name": "Alice"}, {"$set": {"age": 26}})

def update_one(collection, query, update_doc):
    """Update the first document matching the query"""
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        
        if match:
            for field, value in update_doc.items():
                if field == "$set":
                    for k, v in value.items():
                        doc[k] = v
                elif field == "$unset":
                    for k in value:
                        doc.pop(k, None)
                elif field == "$inc":
                    for k, v in value.items():
                        doc[k] = doc.get(k, 0) + v
                elif field == "$push":
                    for k, v in value.items():
                        if k in doc and isinstance(doc[k], list):
                            doc[k].append(v)
            return {"modified_count": 1, "doc": doc}
    
    return {"modified_count": 0, "doc": None}

# Update Alice's age
users = reset_users()
result = update_one(users, {"name": "Alice"}, {"$set": {"age": 26}})
print("Update Alice's age:", result)
print("Alice now:", users[0])

# ============================================================
# $set Operator
# ============================================================

# Example 2: Update multiple fields
# MongoDB equivalent: db.users.update_one({"name": "Bob"}, {"$set": {"age": 31, "email": "bob_new@mail.com"}})

users = reset_users()
result = update_one(users, {"name": "Bob"}, {"$set": {"age": 31, "email": "bob_new@mail.com"}})
print("\nUpdate Bob (age + email):", result["modified_count"], "modified")
print("Bob now:", users[1])

# ============================================================
# $unset Operator
# ============================================================

# Example 3: Remove a field
# MongoDB equivalent: db.users.update_one({"name": "Charlie"}, {"$unset": {"email": ""}})

users = reset_users()
result = update_one(users, {"name": "Charlie"}, {"$unset": {"email": ""}})
print("\nRemove Charlie's email:", result["modified_count"], "modified")
print("Charlie now:", users[2])

# ============================================================
# $inc Operator
# ============================================================

# Example 4: Increment a field
# MongoDB equivalent: db.users.update_one({"name": "Alice"}, {"$inc": {"age": 1}})

users = reset_users()
result = update_one(users, {"name": "Alice"}, {"$inc": {"age": 1}})
print("\nIncrement Alice's age:", result["modified_count"], "modified")
print("Alice now:", users[0])

# Example 5: Decrement (negative increment)
users = reset_users()
result = update_one(users, {"name": "Bob"}, {"$inc": {"age": -2}})
print("\nDecrement Bob's age:", result["modified_count"], "modified")
print("Bob now:", users[1])

# ============================================================
# $push Operator
# ============================================================

# Example 6: Add to array
# MongoDB equivalent: db.users.update_one({"name": "Alice"}, {"$push": {"scores": 95}})

users = reset_users()
result = update_one(users, {"name": "Alice"}, {"$push": {"scores": 95}})
print("\nPush to Alice's scores:", result["modified_count"], "modified")
print("Alice's scores:", users[0]["scores"])

# ============================================================
# Update Many Documents
# ============================================================

# Example 7: Update all matching documents
# MongoDB equivalent: db.users.update_many({"status": "active"}, {"$set": {"verified": true}})

def update_many(collection, query, update_doc):
    """Update all documents matching the query"""
    modified_count = 0
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        
        if match:
            for field, value in update_doc.items():
                if field == "$set":
                    for k, v in value.items():
                        doc[k] = v
                elif field == "$unset":
                    for k in value:
                        doc.pop(k, None)
                elif field == "$inc":
                    for k, v in value.items():
                        doc[k] = doc.get(k, 0) + v
                elif field == "$push":
                    for k, v in value.items():
                        if k in doc and isinstance(doc[k], list):
                            doc[k].append(v)
            modified_count += 1
    
    return {"modified_count": modified_count}

# Set all active users as verified
users = reset_users()
result = update_many(users, {"status": "active"}, {"$set": {"verified": True}})
print("\nSet verified for all active users:", result["modified_count"], "modified")
for user in users:
    print(f"  {user['name']}: verified={user.get('verified', False)}")

# ============================================================
# Upsert
# ============================================================

# Example 8: Update or insert (upsert)
# MongoDB equivalent:
# db.users.update_one({"name": "Eve"}, {"$set": {"age": 28}}, {"upsert": true})

def upsert_one(collection, query, update_doc):
    """Update first match, or insert if no match found"""
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        
        if match:
            for field, value in update_doc.items():
                if field == "$set":
                    for k, v in value.items():
                        doc[k] = v
            return {"modified_count": 1, "upserted": None}
    
    # No match found - insert new document
    new_doc = {}
    for key, value in query.items():
        new_doc[key] = value
    for field, value in update_doc.items():
        if field == "$set":
            new_doc.update(value)
    
    new_doc["_id"] = max([d["_id"] for d in collection], default=0) + 1
    collection.append(new_doc)
    return {"modified_count": 0, "upserted": new_doc["_id"]}

# Eve doesn't exist - should insert
users = reset_users()
result = upsert_one(users, {"name": "Eve"}, {"$set": {"age": 28, "status": "active"}})
print("\nUpsert Eve (insert):", result)
print("Users count:", len(users))

# Eve exists - should update
result = upsert_one(users, {"name": "Eve"}, {"$set": {"age": 29}})
print("\nUpsert Eve (update):", result)

# ============================================================
# Update with Nested Fields
# ============================================================

# Example 9: Update nested document fields
# MongoDB equivalent: db.users.update_one({"name": "Alice"}, {"$set": {"address.city": "LA"}})

users_with_address = [
    {"_id": 1, "name": "Alice", "address": {"city": "New York", "zip": "10001"}},
    {"_id": 2, "name": "Bob", "address": {"city": "Boston", "zip": "02101"}}
]

def update_nested(collection, query, field_path, value):
    """Update a nested field using dot notation"""
    for doc in collection:
        match = True
        for key, val in query.items():
            if doc.get(key) != val:
                match = False
                break
        
        if match:
            keys = field_path.split(".")
            current = doc
            for key in keys[:-1]:
                current = current[key]
            current[keys[-1]] = value
            return {"modified_count": 1}
    
    return {"modified_count": 0}

result = update_nested(users_with_address, {"name": "Alice"}, "address.city", "Los Angeles")
print("\nUpdate nested field:", result)
print("Alice's address:", users_with_address[0]["address"])

# ============================================================
# Atomic Operations
# ============================================================

# Example 10: Multiple atomic operations
# MongoDB equivalent:
# db.users.update_one({"name": "Alice"}, {
#     "$inc": {"age": 1},
#     "$set": {"status": "active"},
#     "$push": {"scores": 100}
# })

users = reset_users()
result = update_one(users, {"name": "Alice"}, {
    "$inc": {"age": 1},
    "$set": {"status": "active"},
    "$push": {"scores": 100}
})
print("\nMultiple operations on Alice:", result)
print("Alice:", users[0])

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Updating Documents")
print("=" * 60)
print("""
1. update_one() updates the first matching document
2. update_many() updates all matching documents
3. $set - Set or update field values
4. $unset - Remove fields from documents
5. $inc - Increment or decrement numeric fields
6. $push - Add items to array fields
7. upsert=True creates document if no match found
8. Use dot notation for nested fields: {"address.city": "NY"}
9. Multiple update operators can be combined
10. Updates are atomic within a single document
""")

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # $set single and multi-field
    u1 = reset_users()
    assert update_one(u1, {"name": "Alice"}, {"$set": {"age": 26}})["modified_count"] == 1
    assert u1[0]["age"] == 26
    assert update_one(u1, {"name": "Bob"}, {"$set": {"age": 31, "email": "bob_new@mail.com"}})["modified_count"] == 1
    assert u1[1]["email"] == "bob_new@mail.com"

    # $unset removes a field
    u2 = reset_users()
    update_one(u2, {"name": "Charlie"}, {"$unset": {"email": ""}})
    assert "email" not in u2[2]

    # $inc increments and decrements
    u3 = reset_users()
    update_one(u3, {"name": "Alice"}, {"$inc": {"age": 1}})
    assert u3[0]["age"] == 26
    update_one(u3, {"name": "Bob"}, {"$inc": {"age": -2}})
    assert u3[1]["age"] == 28

    # $push appends to an array
    u4 = reset_users()
    update_one(u4, {"name": "Alice"}, {"$push": {"scores": 95}})
    assert u4[0]["scores"] == [85, 90, 95]

    # update_many touches every match
    u5 = reset_users()
    assert update_many(u5, {"status": "active"}, {"$set": {"verified": True}})["modified_count"] == 3
    assert all(d.get("verified") for d in u5 if d["status"] == "active")

    # upsert: insert when missing, update when present
    u6 = reset_users()
    r_ins = upsert_one(u6, {"name": "Eve"}, {"$set": {"age": 28, "status": "active"}})
    assert r_ins["upserted"] is not None and len(u6) == 5
    r_upd = upsert_one(u6, {"name": "Eve"}, {"$set": {"age": 29}})
    assert r_upd["modified_count"] == 1 and next(d for d in u6 if d["name"] == "Eve")["age"] == 29

    # nested field update via dot notation
    assert update_nested(users_with_address, {"name": "Alice"}, "address.city", "Los Angeles")["modified_count"] == 1
    assert users_with_address[0]["address"]["city"] == "Los Angeles"

    # combined operators in one update
    u7 = reset_users()
    update_one(u7, {"name": "Alice"}, {"$inc": {"age": 1}, "$set": {"status": "active"}, "$push": {"scores": 100}})
    assert u7[0]["age"] == 26 and u7[0]["scores"] == [85, 90, 100]

    print("[OK] 10-update: all checks passed")


if __name__ == "__main__":
    _verify()  # plain execution and --verify are both tests
