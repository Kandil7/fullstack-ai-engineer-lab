"""
W3Schools Python Tutorial - 15: Python Sets
============================================
Topics: Creating, adding, removing, looping, set operations

Run: python 15-sets.py
Reference: https://www.w3schools.com/python/python_sets.asp
"""

# ============================================================
# Creating Sets
# ============================================================
# Example 1: Different ways to create sets
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}
mixed = {"hello", 42, 3.14, True}
empty_set = set()  # {} creates an empty DICT, not a set!

print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed: {mixed}")
print(f"Empty set: {empty_set}")
print(f"{{}} type: {type({}).__name__}")  # dict!

# Output:
# Fruits: {'apple', 'banana', 'cherry'} (order may vary)
# Numbers: {1, 2, 3, 4, 5}
# Mixed: {True, 42, 'hello', 3.14}
# Empty set: set()
# {} type: dict

# ============================================================
# Sets Remove Duplicates
# ============================================================
# Example 2: Sets automatically remove duplicates
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = set(numbers)
print(f"\nOriginal list: {numbers}")
print(f"Unique set: {unique}")
print(f"Unique list: {sorted(unique)}")

# Practical example: find unique visitors
visitors = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice"]
unique_visitors = set(visitors)
print(f"\nAll visitors: {visitors}")
print(f"Unique visitors: {unique_visitors}")
print(f"Count: {len(unique_visitors)}")

# ============================================================
# Accessing Set Items
# ============================================================
# Example 3: Sets CANNOT be accessed by index!
fruits = {"apple", "banana", "cherry"}

# fruits[0]  # TypeError: 'set' object is not subscriptable

# You can check if an item exists
print(f"\n'apple' in fruits: {'apple' in fruits}")
print(f"'grape' in fruits: {'grape' in fruits}")

# Loop through a set
print("Fruits:")
for fruit in fruits:
    print(f"  {fruit}")

# ============================================================
# Add Items
# ============================================================
# Example 4: Adding items to a set
fruits = {"apple", "banana"}
print(f"\nOriginal: {fruits}")

# add() - add single item
fruits.add("cherry")
print(f"After add('cherry'): {fruits}")

# update() - add multiple items
fruits.update(["date", "elderberry"])
print(f"After update([...]): {fruits}")

# update with another set
fruits.update({"fig", "grape"})
print(f"After update(set): {fruits}")

# ============================================================
# Remove Items
# ============================================================
# Example 5: Removing items from a set
fruits = {"apple", "banana", "cherry", "date", "elderberry"}
print(f"\nOriginal: {fruits}")

# remove() - removes item, raises KeyError if not found
fruits.remove("banana")
print(f"After remove('banana'): {fruits}")

# discard() - removes item, no error if not found
fruits.discard("fig")  # No error!
print(f"After discard('fig'): {fruits}")

# pop() - removes and returns a random item
popped = fruits.pop()
print(f"After pop(): {fruits}, removed: {popped}")

# clear() - removes all items
fruits.clear()
print(f"After clear(): {fruits}")

# ============================================================
# Loop Sets
# ============================================================
# Example 6: Different ways to loop through a set
colors = {"red", "green", "blue", "yellow"}

print("\nMethod 1 - for loop:")
for color in colors:
    print(f"  {color}")

print("\nMethod 2 - with enumerate:")
for i, color in enumerate(sorted(colors)):
    print(f"  {i}: {color}")

# ============================================================
# Set Operations
# ============================================================
# Example 7: Set operations (like mathematical sets)
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print(f"\nSet1: {set1}")
print(f"Set2: {set2}")

# Union - all items from both sets
print(f"\nUnion (|): {set1 | set2}")
print(f"union(): {set1.union(set2)}")

# Intersection - items common to both sets
print(f"\nIntersection (&): {set1 & set2}")
print(f"intersection(): {set1.intersection(set2)}")

# Difference - items in set1 but not in set2
print(f"\nDifference (-): {set1 - set2}")
print(f"difference(): {set1.difference(set2)}")

# Symmetric Difference - items in either set, but not both
print(f"\nSymmetric Diff (^): {set1 ^ set2}")
print(f"symmetric_difference(): {set1.symmetric_difference(set2)}")

# ============================================================
# More Set Methods
# ============================================================
# Example 8: Additional set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}
set3 = {1, 2, 3, 4, 5}

print(f"\nSet1: {set1}")
print(f"Set2: {set2}")
print(f"Set3: {set3}")

# Subset - is set1 a subset of set3?
print(f"\n{set1} is subset of {set3}: {set1.issubset(set3)}")
print(f"{set1} <= {set3}: {set1 <= set3}")

# Superset - is set3 a superset of set1?
print(f"{set3} is superset of {set1}: {set3.issuperset(set1)}")
print(f"{set3} >= {set1}: {set3 >= set1}")

# Disjoint - do sets have no common items?
print(f"{set1} is disjoint with {set2}: {set1.isdisjoint(set2)}")

# Update operations (modify the set in-place)
set1 = {1, 2, 3}
set1.intersection_update({2, 3, 4})
print(f"\nintersection_update: {set1}")  # {2, 3}

set1 = {1, 2, 3}
set1.difference_update({2, 3, 4})
print(f"difference_update: {set1}")  # {1}

set1 = {1, 2, 3}
set1.symmetric_difference_update({2, 3, 4})
print(f"symmetric_difference_update: {set1}")  # {1, 4}

# ============================================================
# Practical Examples
# ============================================================
# Example 9: Real-world set usage

# Find common friends
alice_friends = {"Bob", "Charlie", "David", "Eve"}
bob_friends = {"Alice", "Charlie", "Frank", "David"}

common = alice_friends & bob_friends
print(f"\nCommon friends: {common}")

# Find unique friends
only_alice = alice_friends - bob_friends
only_bob = bob_friends - alice_friends
print(f"Only Alice's friends: {only_alice}")
print(f"Only Bob's friends: {only_bob}")

# All friends
all_friends = alice_friends | bob_friends
print(f"All friends: {all_friends}")

# Remove duplicates from a list
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
cleaned = list(set(data))
print(f"\nOriginal: {data}")
print(f"Cleaned: {cleaned}")

# ============================================================
# Frozenset (Immutable Set)
# ============================================================
# Example 10: Frozenset
fs = frozenset([1, 2, 3, 4, 5])
print(f"\nFrozenset: {fs}")
print(f"Type: {type(fs).__name__}")

# Can't modify frozenset
# fs.add(6)  # AttributeError: 'frozenset' object has no attribute 'add'

# Can use frozenset as dictionary key
d = {frozenset([1, 2]): "pair", frozenset([3, 4]): "another pair"}
print(f"Dict with frozenset keys: {d}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Sets are unordered, no duplicates, no indexing")
print("2. Created with {} or set()")
print("3. add() and update() to add items")
print("4. remove(), discard(), pop(), clear() to remove")
print("5. Union: | or union()")
print("6. Intersection: & or intersection()")
print("7. Difference: - or difference()")
print("8. Symmetric Difference: ^ or symmetric_difference()")
print("9. frozenset is an immutable set")
