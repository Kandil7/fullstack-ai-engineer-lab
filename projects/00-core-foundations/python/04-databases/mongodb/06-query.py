"""
W3Schools Python Tutorial - MongoDB 06: Query Operators
==============================================
Topics: Comparison Operators ($eq, $ne, $gt, $lt), Logical Operators ($and, $or), $in, $regex

Run: python 06-query.py
Reference: https://www.w3schools.com/python/python_mongodb_query.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

users = [
    {"_id": 1, "name": "Alice", "age": 25, "email": "alice@mail.com", "city": "New York", "status": "active"},
    {"_id": 2, "name": "Bob", "age": 30, "email": "bob@mail.com", "city": "Boston", "status": "active"},
    {"_id": 3, "name": "Charlie", "age": 35, "email": "charlie@mail.com", "city": "New York", "status": "inactive"},
    {"_id": 4, "name": "Diana", "age": 28, "email": "diana@mail.com", "city": "Chicago", "status": "active"},
    {"_id": 5, "name": "Eve", "age": 32, "email": "eve@mail.com", "city": "Boston", "status": "active"},
    {"_id": 6, "name": "Frank", "age": 45, "email": "frank@mail.com", "city": "Chicago", "status": "inactive"}
]

# ============================================================
# Comparison Operators
# ============================================================

# Example 1: $eq - Equal to
# MongoDB equivalent: db.users.find({"age": {"$eq": 25}})

def query_eq(collection, field, value):
    """Find documents where field == value"""
    return [doc for doc in collection if doc.get(field) == value]

print("Users with age $eq 25:")
for user in query_eq(users, "age", 25):
    print(f"  {user['name']}: {user['age']}")

# Example 2: $ne - Not equal to
# MongoDB equivalent: db.users.find({"status": {"$ne": "active"}})

def query_ne(collection, field, value):
    """Find documents where field != value"""
    return [doc for doc in collection if doc.get(field) != value]

print("\nInactive users ($ne active):")
for user in query_ne(users, "status", "active"):
    print(f"  {user['name']}: {user['status']}")

# Example 3: $gt - Greater than
# MongoDB equivalent: db.users.find({"age": {"$gt": 30}})

def query_gt(collection, field, value):
    """Find documents where field > value"""
    return [doc for doc in collection if doc.get(field, 0) > value]

print("\nUsers older than 30 ($gt):")
for user in query_gt(users, "age", 30):
    print(f"  {user['name']}: {user['age']}")

# Example 4: $gte - Greater than or equal
# MongoDB equivalent: db.users.find({"age": {"$gte": 30}})

def query_gte(collection, field, value):
    """Find documents where field >= value"""
    return [doc for doc in collection if doc.get(field, 0) >= value]

print("\nUsers age >= 30 ($gte):")
for user in query_gte(users, "age", 30):
    print(f"  {user['name']}: {user['age']}")

# Example 5: $lt - Less than
# MongoDB equivalent: db.users.find({"age": {"$lt": 30}})

def query_lt(collection, field, value):
    """Find documents where field < value"""
    return [doc for doc in collection if doc.get(field, 0) < value]

print("\nUsers younger than 30 ($lt):")
for user in query_lt(users, "age", 30):
    print(f"  {user['name']}: {user['age']}")

# Example 6: $lte - Less than or equal
# MongoDB equivalent: db.users.find({"age": {"$lte": 25}})

def query_lte(collection, field, value):
    """Find documents where field <= value"""
    return [doc for doc in collection if doc.get(field, 0) <= value]

print("\nUsers age <= 25 ($lte):")
for user in query_lte(users, "age", 25):
    print(f"  {user['name']}: {user['age']}")

# ============================================================
# Logical Operators
# ============================================================

# Example 7: $and - Both conditions must be true
# MongoDB equivalent: db.users.find({"$and": [{"age": {"$gt": 25}}, {"city": "Boston"}]})

def query_and(collection, conditions):
    """Find documents matching ALL conditions"""
    results = []
    for doc in collection:
        match = True
        for condition in conditions:
            field = list(condition.keys())[0]
            op = list(condition[field].keys())[0]
            value = condition[field][op]
            
            if op == "$gt" and not (doc.get(field, 0) > value):
                match = False
            elif op == "$lt" and not (doc.get(field, 0) < value):
                match = False
            elif op == "$eq" and not (doc.get(field) == value):
                match = False
            elif op == "$ne" and not (doc.get(field) != value):
                match = False
        
        if match:
            results.append(doc)
    return results

# Users older than 25 AND in Boston
and_result = query_and(users, [
    {"age": {"$gt": 25}},
    {"city": "Boston"}
])
print("\n$and (age > 25 AND city = Boston):")
for user in and_result:
    print(f"  {user['name']}: age {user['age']}, {user['city']}")

# Example 8: $or - At least one condition must be true
# MongoDB equivalent: db.users.find({"$or": [{"city": "New York"}, {"city": "Boston"}]})

def query_or(collection, conditions):
    """Find documents matching ANY condition"""
    results = []
    for doc in collection:
        for condition in conditions:
            field = list(condition.keys())[0]
            value = condition[field]
            if doc.get(field) == value:
                results.append(doc)
                break
    return results

# Users in New York OR Boston
or_result = query_or(users, [
    {"city": "New York"},
    {"city": "Boston"}
])
print("\n$or (city = NY OR city = Boston):")
for user in or_result:
    print(f"  {user['name']}: {user['city']}")

# ============================================================
# $in Operator
# ============================================================

# Example 9: $in - Match any value in array
# MongoDB equivalent: db.users.find({"city": {"$in": ["New York", "Chicago"]}})

def query_in(collection, field, values):
    """Find documents where field is in values list"""
    return [doc for doc in collection if doc.get(field) in values]

# Users in New York or Chicago
in_result = query_in(users, "city", ["New York", "Chicago"])
print("\n$in (city in [NY, Chicago]):")
for user in in_result:
    print(f"  {user['name']}: {user['city']}")

# Example 10: $nin - Not in array
# MongoDB equivalent: db.users.find({"city": {"$nin": ["New York"]}})

def query_nin(collection, field, values):
    """Find documents where field is NOT in values list"""
    return [doc for doc in collection if doc.get(field) not in values]

# Users NOT in New York
nin_result = query_nin(users, "city", ["New York"])
print("\n$nin (city NOT in [NY]):")
for user in nin_result:
    print(f"  {user['name']}: {user['city']}")

# ============================================================
# $regex Operator
# ============================================================

# Example 11: $regex - Regular expression matching
# MongoDB equivalent: db.users.find({"email": {"$regex": "mail.com"}})

import re

def query_regex(collection, field, pattern):
    """Find documents matching regex pattern"""
    return [doc for doc in collection if re.search(pattern, str(doc.get(field, "")))]

# Users with email matching pattern
regex_result = query_regex(users, "email", r"@mail\.com")
print("\n$regex (email matches @mail.com):")
for user in regex_result:
    print(f"  {user['name']}: {user['email']}")

# Example 12: Name starts with 'A' or 'B'
name_regex = query_regex(users, "name", r"^[AB]")
print("\n$regex (name starts with A or B):")
for user in name_regex:
    print(f"  {user['name']}")

# ============================================================
# Combined Queries
# ============================================================

# Example 13: Complex query - Multiple operators
# MongoDB equivalent:
# db.users.find({
#     "$and": [
#         {"age": {"$gte": 28}},
#         {"age": {"$lte": 35}},
#         {"status": "active"}
#     ]
# })

def complex_query(collection, query):
    """Execute a complex query with multiple conditions"""
    results = []
    for doc in collection:
        match = True
        for key, condition in query.items():
            if key == "$and":
                for cond in condition:
                    field = list(cond.keys())[0]
                    op = list(cond[field].keys())[0]
                    value = cond[field][op]
                    
                    doc_val = doc.get(field)
                    if op == "$gte" and not (doc_val >= value):
                        match = False
                    elif op == "$lte" and not (doc_val <= value):
                        match = False
            elif key == "$or":
                or_match = False
                for cond in condition:
                    field = list(cond.keys())[0]
                    value = cond[field]
                    if doc.get(field) == value:
                        or_match = True
                        break
                if not or_match:
                    match = False
            elif key not in doc:
                match = False
            elif isinstance(condition, dict):
                for op, value in condition.items():
                    if op == "$gt" and not (doc[key] > value):
                        match = False
                    elif op == "$lt" and not (doc[key] < value):
                        match = False
                    elif op == "$in" and doc[key] not in value:
                        match = False
            elif doc[key] != condition:
                match = False
        
        if match:
            results.append(doc)
    return results

# Active users aged 28-35
complex_result = complex_query(users, {
    "$and": [
        {"age": {"$gte": 28}},
        {"age": {"$lte": 35}}
    ],
    "status": "active"
})

print("\nComplex query (active, age 28-35):")
for user in complex_result:
    print(f"  {user['name']}: age {user['age']}, {user['status']}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Query Operators")
print("=" * 60)
print("""
1. $eq - Equal to (default, can omit)
2. $ne - Not equal to
3. $gt - Greater than
4. $gte - Greater than or equal to
5. $lt - Less than
6. $lte - Less than or equal to
7. $and - All conditions must match
8. $or - At least one condition must match
9. $in - Match any value in an array
10. $nin - Match no value in an array
11. $regex - Regular expression pattern matching
12. Queries can be combined for complex filters
""")
