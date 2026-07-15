"""
W3Schools Python Tutorial - 16: Python Dictionaries
====================================================
Topics: Creating, accessing, modifying, looping, nested, methods

Run: python 16-dictionaries.py
Reference: https://www.w3schools.com/python/python_dictionaries.asp
"""

# ============================================================
# Creating Dictionaries
# ============================================================
# Example 1: Different ways to create dictionaries
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Using dict() constructor
person2 = dict(name="Bob", age=25, city="London")

# From list of tuples
person3 = dict([("name", "Charlie"), ("age", 35)])

# From zip
keys = ["x", "y", "z"]
values = [10, 20, 30]
coords = dict(zip(keys, values))

# Empty dictionary
empty = {}

print(f"Person: {person}")
print(f"Person2: {person2}")
print(f"Person3: {person3}")
print(f"Coords: {coords}")
print(f"Empty: {empty}")

# Output:
# Person: {'name': 'Alice', 'age': 30, 'city': 'New York'}
# Person2: {'name': 'Bob', 'age': 25, 'city': 'London'}
# Person3: {'name': 'Charlie', 'age': 35}
# Coords: {'x': 10, 'y': 20, 'z': 30}
# Empty: {}

# ============================================================
# Accessing Items
# ============================================================
# Example 2: Accessing dictionary values
person = {"name": "Alice", "age": 30, "city": "New York"}

# Using key
print(f"\nName: {person['name']}")
print(f"Age: {person['age']}")

# Using get() - returns None (or default) if key doesn't exist
print(f"Name: {person.get('name')}")
print(f"Phone: {person.get('phone')}")          # None
print(f"Phone: {person.get('phone', 'N/A')}")   # N/A

# person['phone']  # KeyError: 'phone'

# ============================================================
# Change Items
# ============================================================
# Example 3: Modifying dictionary values
person = {"name": "Alice", "age": 30, "city": "New York"}
print(f"\nOriginal: {person}")

# Change a value
person["age"] = 31
print(f"After person['age'] = 31: {person}")

# Update multiple values
person.update({"city": "Boston", "age": 32})
print(f"After update: {person}")

# ============================================================
# Add Items
# ============================================================
# Example 4: Adding new key-value pairs
person = {"name": "Alice", "age": 30}
print(f"\nOriginal: {person}")

# Add new key
person["email"] = "alice@example.com"
print(f"After adding email: {person}")

# Add using update
person.update({"phone": "555-0123", "address": "123 Main St"})
print(f"After update: {person}")

# setdefault() - add only if key doesn't exist
person.setdefault("name", "Bob")  # Won't change - key exists
person.setdefault("age", 25)      # Won't change - key exists
person.setdefault("country", "USA")  # Will add - key doesn't exist
print(f"After setdefault: {person}")

# ============================================================
# Remove Items
# ============================================================
# Example 5: Removing items from a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "email": "alice@example.com",
    "phone": "555-0123"
}
print(f"\nOriginal: {person}")

# pop() - remove and return value
email = person.pop("email")
print(f"After pop('email'): {person}, removed: {email}")

# pop() with default
phone = person.pop("phone", "N/A")
print(f"After pop('phone'): {person}, removed: {phone}")

# popitem() - remove last inserted item
last = person.popitem()
print(f"After popitem(): {person}, removed: {last}")

# Use list() to snapshot remaining keys before deletion
if "city" in person:
    del person["city"]
print(f"After del: {person}")

# clear() - remove all items
person.clear()
print(f"After clear(): {person}")

# ============================================================
# Loop Dictionaries
# ============================================================
# Example 6: Different ways to loop through a dictionary
person = {"name": "Alice", "age": 30, "city": "New York"}

print("\nMethod 1 - Loop through keys:")
for key in person:
    print(f"  {key}")

print("\nMethod 2 - Loop through values:")
for value in person.values():
    print(f"  {value}")

print("\nMethod 3 - Loop through key-value pairs:")
for key, value in person.items():
    print(f"  {key}: {value}")

print("\nMethod 4 - Using .items():")
for key, value in person.items():
    print(f"  {key} = {value}")

# ============================================================
# Nested Dictionaries
# ============================================================
# Example 7: Dictionaries within dictionaries
students = {
    "student1": {
        "name": "Alice",
        "age": 20,
        "grades": [90, 85, 92]
    },
    "student2": {
        "name": "Bob",
        "age": 22,
        "grades": [80, 75, 88]
    },
    "student3": {
        "name": "Charlie",
        "age": 21,
        "grades": [95, 92, 88]
    }
}

print("\n--- Nested Dictionaries ---")
for student_id, info in students.items():
    avg_grade = sum(info["grades"]) / len(info["grades"])
    print(f"{student_id}: {info['name']}, Age: {info['age']}, Avg: {avg_grade:.1f}")

# Accessing nested values
print(f"\nAlice's first grade: {students['student1']['grades'][0]}")
print(f"Bob's name: {students['student2']['name']}")

# ============================================================
# Dictionary Methods
# ============================================================
# Example 8: Common dictionary methods
person = {"name": "Alice", "age": 30, "city": "New York"}

print(f"\n--- Dictionary Methods ---")
print(f"keys(): {person.keys()}")
print(f"values(): {person.values()}")
print(f"items(): {person.items()}")

# Convert to list
print(f"list(keys()): {list(person.keys())}")
print(f"list(values()): {list(person.values())}")
print(f"list(items()): {list(person.items())}")

# Check if key exists
print(f"'name' in person: {'name' in person}")
print(f"'phone' in person: {'phone' in person}")

# ============================================================
# Dictionary Comprehension
# ============================================================
# Example 9: Dictionary comprehensions
numbers = [1, 2, 3, 4, 5]

# Square each number
squares = {x: x ** 2 for x in numbers}
print(f"\nSquares: {squares}")

# Filter
even_squares = {x: x ** 2 for x in numbers if x % 2 == 0}
print(f"Even squares: {even_squares}")

# From two lists
names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 92]
grade_book = {name: score for name, score in zip(names, scores)}
print(f"Grade book: {grade_book}")

# ============================================================
# Practical Examples
# ============================================================
# Example 10: Real-world dictionary usage

# Counting occurrences
text = "hello world hello python world hello"
words = text.split()
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1
print(f"\nWord count: {word_count}")

# Using collections.Counter (better way)
from collections import Counter
word_count = Counter(words)
print(f"Counter: {dict(word_count)}")

# Merging dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# Method 1: update()
merged = dict1.copy()
merged.update(dict2)
print(f"\nMerged (update): {merged}")

# Method 2: | operator (Python 3.9+)
merged = dict1 | dict2
print(f"Merged (|): {merged}")

# Method 3: ** unpacking
merged = {**dict1, **dict2}
print(f"Merged (**): {merged}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Dictionaries store key-value pairs")
print("2. Access with dict[key] or dict.get(key)")
print("3. Modify with dict[key] = value or update()")
print("4. Remove with pop(), del, clear()")
print("5. Loop with keys(), values(), items()")
print("6. Nested dicts: dict[key1][key2]")
print("7. Dict comprehension: {k: v for k, v in ...}")
