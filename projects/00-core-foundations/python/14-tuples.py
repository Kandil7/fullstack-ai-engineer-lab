"""
W3Schools Python Tutorial - 14: Python Tuples
==============================================
Topics: Creating, accessing, methods, unpacking

Run: python 14-tuples.py
Reference: https://www.w3schools.com/python/python_tuples.asp
"""

# ============================================================
# Creating Tuples
# ============================================================
# Example 1: Different ways to create tuples
fruits = ("apple", "banana", "cherry")
numbers = (1, 2, 3, 4, 5)
mixed = ("hello", 42, 3.14, True)
nested = ((1, 2), (3, 4), (5, 6))
single = ("hello",)  # Note: single item tuple needs trailing comma
not_tuple = ("hello")  # This is just a string!

print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed: {mixed}")
print(f"Nested: {nested}")
print(f"Single item tuple: {single}")
print(f"Not a tuple: {not_tuple}, type: {type(not_tuple).__name__}")

# Output:
# Fruits: ('apple', 'banana', 'cherry')
# Numbers: (1, 2, 3, 4, 5)
# Mixed: ('hello', 42, 3.14, True)
# Nested: ((1, 2), (3, 4), (5, 6))
# Single item tuple: ('hello',)
# Not a tuple: hello, type: str

# ============================================================
# Tuples are IMMUTABLE
# ============================================================
# Example 2: Cannot change tuple items after creation
fruits = ("apple", "banana", "cherry")
# fruits[0] = "avocado"  # TypeError: 'tuple' object does not support item assignment
# del fruits[0]          # TypeError: 'tuple' object doesn't support item deletion

# BUT: you can reassign the entire variable
fruits = ("avocado", "blueberry")
print(f"\nReassigned: {fruits}")

# ============================================================
# Accessing Tuple Items
# ============================================================
# Example 3: Indexing and slicing (same as lists)
fruits = ("apple", "banana", "cherry", "date", "elderberry")
print(f"\nFruits: {fruits}")
print(f"First: {fruits[0]}")      # apple
print(f"Second: {fruits[1]}")     # banana
print(f"Last: {fruits[-1]}")      # elderberry

# Slicing
print(f"First 3: {fruits[:3]}")    # ('apple', 'banana', 'cherry')
print(f"Last 2: {fruits[-2:]}")    # ('date', 'elderberry')
print(f"Middle: {fruits[1:4]}")    # ('banana', 'cherry', 'date')
print(f"Reversed: {fruits[::-1]}")  # ('elderberry', 'date', 'cherry', 'banana', 'apple')

# ============================================================
# Tuple Methods
# ============================================================
# Example 4: Tuple methods (very limited - tuples are immutable!)
numbers = (1, 2, 3, 2, 4, 2, 5)

print(f"\nTuple: {numbers}")
print(f"count(2): {numbers.count(2)}")  # 3 (occurrences of 2)
print(f"index(4): {numbers.index(4)}")  # 4 (index of first 4)

# That's it! Tuples only have count() and index() methods
# because they're immutable and can't be modified

# ============================================================
# Unpacking Tuples
# ============================================================
# Example 5: Unpacking tuple values
coordinates = (10, 20, 30)
x, y, z = coordinates
print(f"\nCoordinates: x={x}, y={y}, z={z}")
# Output: Coordinates: x=10, y=20, z=30

# Example 6: Unpacking with *
first, *rest = (1, 2, 3, 4, 5)
print(f"First: {first}, Rest: {rest}")
# Output: First: 1, Rest: [2, 3, 4, 5]

first, *middle, last = (1, 2, 3, 4, 5)
print(f"First: {first}, Middle: {middle}, Last: {last}")
# Output: First: 1, Middle: [2, 3, 4], Last: 5

# Example 7: Swapping variables using tuple unpacking
a, b = 10, 20
print(f"\nBefore swap: a={a}, b={b}")
a, b = b, a
print(f"After swap: a={a}, b={b}")

# ============================================================
# Tuple vs List
# ============================================================
# Example 8: When to use tuples vs lists
print("\n--- Tuple vs List ---")

# Use TUPLES for:
# - Fixed collections (days of week, coordinates)
# - Dictionary keys (lists can't be keys)
# - Function return values
# - Data that shouldn't change

# Use LISTS for:
# - Collections that will be modified
# - Homogeneous data (same type)
# - When you need list methods

# Example: Tuple as dictionary key
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London",
    (35.6762, 139.6503): "Tokyo"
}

# Can't use a list as a key:
# locations[[40.7128, -74.0060]] = "New York"  # TypeError!

print(f"New York coordinates: {locations[(40.7128, -74.0060)]}")

# ============================================================
# Tuple Operations
# ============================================================
# Example 9: Tuple operations
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

# Concatenation
combined = tuple1 + tuple2
print(f"\nConcatenation: {combined}")

# Repetition
repeated = tuple1 * 3
print(f"Repetition: {repeated}")

# Membership
print(f"2 in tuple1: {2 in tuple1}")
print(f"5 not in tuple1: {5 not in tuple1}")

# Length
print(f"Length: {len(combined)}")

# ============================================================
# Converting Between Lists and Tuples
# ============================================================
# Example 10: Conversion
my_list = [1, 2, 3, 4, 5]
my_tuple = tuple(my_list)
print(f"\nList to tuple: {my_tuple}, type: {type(my_tuple).__name__}")

my_list = list(my_tuple)
print(f"Tuple to list: {my_list}, type: {type(my_list).__name__}")

# ============================================================
# Named Tuples
# ============================================================
# Example 11: Named tuples for cleaner code
from collections import namedtuple

# Create a named tuple type
Point = namedtuple('Point', ['x', 'y'])
Student = namedtuple('Student', 'name age grade')

# Using named tuples
p = Point(10, 20)
print(f"\nPoint: {p}")
print(f"Point x: {p.x}, y: {p.y}")

s = Student("Alice", 90, "A")
print(f"Student: {s}")
print(f"Name: {s.name}, Grade: {s.grade}")

# Named tuples are still tuples
print(f"Is tuple: {isinstance(p, tuple)}")
print(f"Index access: {p[0]}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Tuples are ordered, IMMUTABLE collections")
print("2. Created with parentheses: (1, 2, 3)")
print("3. Only methods: count() and index()")
print("4. Unpack with: a, b, c = (1, 2, 3)")
print("5. Use tuples for fixed data, dict keys, function returns")
print("6. Named tuples add readability: Point(10, 20)")
