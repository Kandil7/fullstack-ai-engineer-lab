"""
W3Schools Python Tutorial - 13: Python Lists
=============================================
Topics: Creating, accessing, slicing, modifying, methods, comprehension

Run: python 13-lists.py
Reference: https://www.w3schools.com/python/python_lists.asp
"""

# ============================================================
# Creating Lists
# ============================================================
# Example 1: Different ways to create lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]
empty = []

print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed: {mixed}")
print(f"Nested: {nested}")
print(f"Empty: {empty}")

# Output:
# Fruits: ['apple', 'banana', 'cherry']
# Numbers: [1, 2, 3, 4, 5]
# Mixed: ['hello', 42, 3.14, True, None]
# Nested: [[1, 2], [3, 4], [5, 6]]
# Empty: []

# ============================================================
# Accessing Items
# ============================================================
# Example 2: Indexing (0-based)
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
print(f"\nFruits: {fruits}")
print(f"First: {fruits[0]}")      # apple
print(f"Second: {fruits[1]}")     # banana
print(f"Last: {fruits[-1]}")      # elderberry
print(f"Third from end: {fruits[-3]}")  # cherry

# ============================================================
# Slicing
# ============================================================
# Example 3: List slicing [start:stop:step]
print(f"\nFull list: {fruits}")
print(f"First 3: {fruits[:3]}")          # ['apple', 'banana', 'cherry']
print(f"Last 2: {fruits[-2:]}")          # ['date', 'elderberry']
print(f"Middle: {fruits[1:4]}")          # ['banana', 'cherry', 'date']
print(f"Every other: {fruits[::2]}")     # ['apple', 'cherry', 'elderberry']
print(f"Reversed: {fruits[::-1]}")       # ['elderberry', 'date', 'cherry', 'banana', 'apple']

# ============================================================
# Modify Items
# ============================================================
# Example 4: Changing list items
fruits = ["apple", "banana", "cherry"]
print(f"\nOriginal: {fruits}")

fruits[0] = "avocado"
print(f"After fruits[0] = 'avocado': {fruits}")

fruits[-1] = "coconut"
print(f"After fruits[-1] = 'coconut': {fruits}")

# Change a range
fruits[1:3] = ["blueberry", "cranberry"]
print(f"After fruits[1:3] = [...]: {fruits}")

# ============================================================
# Add Items
# ============================================================
# Example 5: Adding items to a list
fruits = ["apple", "banana"]
print(f"\nOriginal: {fruits}")

# append() - add to end
fruits.append("cherry")
print(f"After append('cherry'): {fruits}")

# insert() - add at specific index
fruits.insert(1, "avocado")
print(f"After insert(1, 'avocado'): {fruits}")

# extend() - add multiple items
fruits.extend(["date", "elderberry"])
print(f"After extend([...]): {fruits}")

# + operator
fruits = fruits + ["fig"]
print(f"After + ['fig']: {fruits}")

# * operator (repetition)
zeros = [0] * 5
print(f"[0] * 5 = {zeros}")

# ============================================================
# Remove Items
# ============================================================
# Example 6: Removing items from a list
fruits = ["apple", "banana", "cherry", "banana", "date"]
print(f"\nOriginal: {fruits}")

# remove() - remove first occurrence
fruits.remove("banana")
print(f"After remove('banana'): {fruits}")

# pop() - remove and return item
last = fruits.pop()
print(f"After pop(): {fruits}, removed: {last}")

first = fruits.pop(0)
print(f"After pop(0): {fruits}, removed: {first}")

# del - remove by index or slice
del fruits[0]
print(f"After del fruits[0]: {fruits}")

# clear() - remove all items
fruits.clear()
print(f"After clear(): {fruits}")

# ============================================================
# Loop Lists
# ============================================================
# Example 7: Different ways to loop through a list
fruits = ["apple", "banana", "cherry"]

# Method 1: for loop (most common)
print("\nMethod 1 - for loop:")
for fruit in fruits:
    print(f"  {fruit}")

# Method 2: for loop with index
print("\nMethod 2 - for loop with range:")
for i in range(len(fruits)):
    print(f"  {i}: {fruits[i]}")

# Method 3: enumerate()
print("\nMethod 3 - enumerate:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# Method 4: while loop
print("\nMethod 4 - while loop:")
i = 0
while i < len(fruits):
    print(f"  {fruits[i]}")
    i += 1

# ============================================================
# List Comprehension
# ============================================================
# Example 8: List comprehension - concise way to create lists
numbers = [1, 2, 3, 4, 5]

# Basic comprehension
squares = [x ** 2 for x in numbers]
print(f"\nSquares: {squares}")  # [1, 4, 9, 16, 25]

# With condition
evens = [x for x in numbers if x % 2 == 0]
print(f"Evens: {evens}")  # [2, 4]

# With transformation
upper_fruits = [f.upper() for f in ["apple", "banana", "cherry"]]
print(f"Uppercase: {upper_fruits}")  # ['APPLE', 'BANANA', 'CHERRY']

# Nested comprehension
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"Matrix: {matrix}")  # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Filter and transform
words = ["hello", "world", "python", "hi"]
long_words = [w.upper() for w in words if len(w) > 3]
print(f"Long words (upper): {long_words}")  # ['HELLO', 'WORLD', 'PYTHON']

# ============================================================
# Sort Lists
# ============================================================
# Example 9: Sorting
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nOriginal: {numbers}")

# sort() - sorts in place
numbers.sort()
print(f"After sort(): {numbers}")

numbers.sort(reverse=True)
print(f"After sort(reverse=True): {numbers}")

# sorted() - returns new sorted list
original = [3, 1, 4, 1, 5, 9, 2, 6]
new_sorted = sorted(original)
print(f"Original: {original}")
print(f"sorted(): {new_sorted}")

# Sort with key
words = ["banana", "apple", "cherry", "date"]
words.sort(key=len)
print(f"By length: {words}")  # ['date', 'apple', 'banana', 'cherry']

# Sort complex data
students = [("Alice", 90), ("Bob", 80), ("Charlie", 95)]
students.sort(key=lambda x: x[1], reverse=True)
print(f"Students by grade: {students}")

# ============================================================
# Copy Lists
# ============================================================
# Example 10: Copying (important - assignment doesn't copy!)
original = [1, 2, 3, 4, 5]

# WRONG - this just creates a reference!
reference = original
reference[0] = 999
print(f"\nOriginal after 'copy': {original}")  # [999, 2, 3, 4, 5] - OOPS!

# CORRECT - ways to copy
original = [1, 2, 3, 4, 5]
copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]

copy1[0] = 999
print(f"Original: {original}")   # [1, 2, 3, 4, 5] - unchanged!
print(f"Copy1: {copy1}")         # [999, 2, 3, 4, 5]

# Deep copy for nested lists
import copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
deep[0][0] = 999
print(f"\nOriginal nested: {nested}")  # [[1, 2], [3, 4]] - unchanged!
print(f"Deep copy: {deep}")            # [[999, 2], [3, 4]]

# ============================================================
# Join Lists
# ============================================================
# Example 11: Joining lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Using +
combined = list1 + list2
print(f"\nlist1 + list2 = {combined}")

# Using extend()
list1.extend(list2)
print(f"After extend: {list1}")

# Using unpacking (*)
combined = [*list1, *list2]
print(f"Unpacking: {combined}")

# ============================================================
# List Methods
# ============================================================
# Example 12: Complete list of list methods
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(f"\n--- List Methods ---")
print(f"list: {numbers}")
print(f"count(1): {numbers.count(1)}")      # 2
print(f"index(5): {numbers.index(5)}")      # 4

# ============================================================
# Useful List Functions
# ============================================================
# Example 13: Built-in functions with lists
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(f"\nlen: {len(numbers)}")
print(f"min: {min(numbers)}")
print(f"max: {max(numbers)}")
print(f"sum: {sum(numbers)}")
print(f"sorted: {sorted(numbers)}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Lists are ordered, mutable, allow duplicates")
print("2. Access with index: list[0], list[-1]")
print("3. Slice with list[start:stop:step]")
print("4. Add: append(), insert(), extend()")
print("5. Remove: remove(), pop(), del, clear()")
print("6. Comprehensions: [x for x in list if condition]")
print("7. Sort: sort() in-place, sorted() returns new list")
print("8. ALWAYS copy with .copy() not assignment (=)")
