"""
W3Schools Python Tutorial - MongoDB 07: Sort Documents
==============================================
Topics: sort() Ascending/Descending, Sorting by Multiple Fields

Run: python 07-sort.py
Reference: https://www.w3schools.com/python/python_mongodb_sort.asp
"""

# NOTE: This uses Python dicts as stand-ins for MongoDB documents.
# The syntax mirrors MongoDB operations.

# ============================================================
# Sample Data
# ============================================================

users = [
    {"_id": 1, "name": "Alice", "age": 25, "city": "New York", "salary": 75000},
    {"_id": 2, "name": "Bob", "age": 30, "city": "Boston", "salary": 85000},
    {"_id": 3, "name": "Charlie", "age": 35, "city": "New York", "salary": 95000},
    {"_id": 4, "name": "Diana", "age": 28, "city": "Chicago", "salary": 70000},
    {"_id": 5, "name": "Eve", "age": 32, "city": "Boston", "salary": 90000},
    {"_id": 6, "name": "Frank", "age": 45, "city": "Chicago", "salary": 110000}
]

# ============================================================
# Sort Ascending
# ============================================================

# Example 1: Sort by name ascending
# MongoDB equivalent: db.users.find().sort("name", 1)

def sort_ascending(collection, field):
    """Sort collection by field in ascending order"""
    return sorted(collection, key=lambda x: x.get(field, 0))

sorted_by_name = sort_ascending(users, "name")
print("Sorted by name (ascending):")
for user in sorted_by_name:
    print(f"  {user['name']}: age {user['age']}")

# Example 2: Sort by age ascending
sorted_by_age = sort_ascending(users, "age")
print("\nSorted by age (ascending):")
for user in sorted_by_age:
    print(f"  {user['name']}: age {user['age']}")

# ============================================================
# Sort Descending
# ============================================================

# Example 3: Sort by age descending
# MongoDB equivalent: db.users.find().sort("age", -1)

def sort_descending(collection, field):
    """Sort collection by field in descending order"""
    return sorted(collection, key=lambda x: x.get(field, 0), reverse=True)

sorted_by_age_desc = sort_descending(users, "age")
print("\nSorted by age (descending):")
for user in sorted_by_age_desc:
    print(f"  {user['name']}: age {user['age']}")

# Example 4: Sort by salary descending (highest first)
sorted_by_salary = sort_descending(users, "salary")
print("\nSorted by salary (highest first):")
for user in sorted_by_salary:
    print(f"  {user['name']}: ${user['salary']:,}")

# ============================================================
# Sort Function with Direction
# ============================================================

# Example 5: Sort with explicit direction
# MongoDB equivalent: db.users.find().sort("age", 1)  // 1 = ASC, -1 = DESC

def sort_by(collection, field, direction=1):
    """Sort collection by field with direction (1=ASC, -1=DESC)"""
    reverse = (direction == -1)
    return sorted(collection, key=lambda x: x.get(field, 0), reverse=reverse)

# ASC = 1
ascending = sort_by(users, "name", 1)
print("\nName ASC (1):")
for user in ascending:
    print(f"  {user['name']}")

# DESC = -1
descending = sort_by(users, "name", -1)
print("\nName DESC (-1):")
for user in descending:
    print(f"  {user['name']}")

# ============================================================
# Sort by Multiple Fields
# ============================================================

# Example 6: Sort by city then by age
# MongoDB equivalent: db.users.find().sort([("city", 1), ("age", 1)])

def sort_multiple(collection, sort_keys):
    """Sort by multiple fields
    sort_keys: list of (field, direction) tuples
    """
    def sort_key(doc):
        keys = []
        for field, direction in sort_keys:
            val = doc.get(field, 0)
            if direction == -1:
                # For descending, negate numeric values or reverse strings
                if isinstance(val, (int, float)):
                    val = -val
                else:
                    val = tuple([-ord(c) for c in str(val)])
            keys.append(val)
        return tuple(keys)
    
    return sorted(collection, key=sort_key)

# Sort by city ASC, then age ASC
multi_sort = sort_multiple(users, [("city", 1), ("age", 1)])
print("\nSort by city then age (ASC/ASC):")
for user in multi_sort:
    print(f"  {user['city']}: {user['name']} (age {user['age']})")

# Example 7: Sort by city ASC, then salary DESC
multi_sort2 = sort_multiple(users, [("city", 1), ("salary", -1)])
print("\nSort by city ASC, salary DESC:")
for user in multi_sort2:
    print(f"  {user['city']}: {user['name']} (${user['salary']:,})")

# ============================================================
# Sort with Queries
# ============================================================

# Example 8: Filter then sort
# MongoDB equivalent:
# db.users.find({"city": "New York"}).sort("age", 1)

def find_and_sort(collection, query, sort_field, direction=1):
    """Find documents matching query, then sort"""
    # First filter
    results = []
    for doc in collection:
        match = True
        for key, value in query.items():
            if doc.get(key) != value:
                match = False
                break
        if match:
            results.append(doc)
    
    # Then sort
    reverse = (direction == -1)
    return sorted(results, key=lambda x: x.get(sort_field, 0), reverse=reverse)

# New York users sorted by age
ny_sorted = find_and_sort(users, {"city": "New York"}, "age")
print("\nNew York users sorted by age:")
for user in ny_sorted:
    print(f"  {user['name']}: age {user['age']}")

# ============================================================
# Sorting with None/Missing Values
# ============================================================

# Example 9: Handle missing fields in sort
users_with_missing = [
    {"_id": 1, "name": "Alice", "age": 25},
    {"_id": 2, "name": "Bob"},  # No age
    {"_id": 3, "name": "Charlie", "age": 35},
    {"_id": 4, "name": "Diana"}  # No age
]

def sort_safe(collection, field, direction=1, default=None):
    """Sort with safe handling of missing values"""
    def sort_key(doc):
        val = doc.get(field, default)
        if val is None:
            return (1, "")  # Put None values at end
        if direction == -1 and isinstance(val, (int, float)):
            return (0, -val)
        return (0, val)
    
    return sorted(collection, key=sort_key)

sorted_safe = sort_safe(users_with_missing, "age", 1)
print("\nSort with missing values:")
for user in sorted_safe:
    age = user.get("age", "N/A")
    print(f"  {user['name']}: age {age}")

# ============================================================
# Practical Examples
# ============================================================

# Example 10: Top N highest salaries
def top_n(collection, field, n, direction=-1):
    """Get top N documents by field"""
    sorted_coll = sort_by(collection, field, direction)
    return sorted_coll[:n]

top_3_salary = top_n(users, "salary", 3)
print("\nTop 3 highest salaries:")
for i, user in enumerate(top_3_salary, 1):
    print(f"  {i}. {user['name']}: ${user['salary']:,}")

# Example 11: Sort and limit
def sort_and_limit(collection, sort_field, limit, direction=-1):
    """Sort and return limited results"""
    sorted_coll = sort_by(collection, sort_field, direction)
    return sorted_coll[:limit]

oldest_2 = sort_and_limit(users, "age", 2, -1)
print("\n2 oldest users:")
for user in oldest_2:
    print(f"  {user['name']}: age {user['age']}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY: Sorting Documents")
print("=" * 60)
print("""
1. sort("field", 1) sorts ascending (A-Z, 0-9)
2. sort("field", -1) sorts descending (Z-A, 9-0)
3. sort([("field1", 1), ("field2", -1)]) sorts by multiple fields
4. Sorting is stable - equal elements maintain order
5. Use sort with find() for filtered + sorted results
6. Handle missing fields with default values
7. Combine sort with limit() for top-N queries
8. Common patterns: sort by date, price, name, or custom field
""")
