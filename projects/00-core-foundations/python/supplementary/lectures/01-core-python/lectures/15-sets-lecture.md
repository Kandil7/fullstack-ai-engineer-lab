# Python Sets — Lecture 15

## Topic Overview

A **set** is an unordered collection of unique elements. Sets are mutable, meaning you can add or remove items after creation, but the elements themselves must be immutable (hashable). Sets are optimized for membership testing, deduplication, and mathematical set operations like union, intersection, and difference.

Sets are defined using curly braces `{}` or the `set()` constructor. An empty set **must** be created with `set()` — using `{}` creates an empty dictionary instead.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Understand the difference between sets, lists, and tuples
- Create sets using different methods
- Add and remove elements from sets
- Perform set operations: union, intersection, difference, symmetric difference
- Use set comprehensions
- Understand when to use sets vs. other collections
- Apply sets to real-world deduplication and membership testing scenarios

---

## Key Concepts

### 1. What Makes Sets Special?

Sets enforce **uniqueness** — no duplicate elements allowed. This makes them ideal for:
- Removing duplicates from data
- Fast membership testing (`O(1)` average lookup)
- Mathematical operations between collections

```python
# Lists allow duplicates
my_list = [1, 2, 2, 3, 3, 3]
print(my_list)  # [1, 2, 2, 3, 3, 3]

# Sets eliminate duplicates automatically
my_set = {1, 2, 2, 3, 3, 3}
print(my_set)   # {1, 2, 3}
```

### 2. Creating Sets

```python
# Using curly braces
fruits = {"apple", "banana", "cherry"}
print(type(fruits))  # <class 'set'>

# Using the set() constructor
numbers = set([1, 2, 3, 4, 5])
print(numbers)  # {1, 2, 3, 4, 5}

# From a string (each character becomes an element)
chars = set("hello")
print(chars)  # {'h', 'e', 'l', 'o'}  — duplicates removed

# Empty set — MUST use set(), not {}
empty_set = set()     # This is an empty set
empty_dict = {}       # This is an empty dictionary!

# IMPORTANT: {1, 2, 3} is a set, but {} is a dictionary
```

### 3. Set Properties

- **Unordered**: Elements have no defined index position
- **Unqiue**: No duplicate elements
- **Mutable**: You can add/remove elements
- **Elements must be immutable**: Numbers, strings, tuples can be in sets; lists and dictionaries cannot

```python
# Immutable elements are allowed
valid_set = {1, "hello", (2, 3)}

# Mutable elements cause errors
# invalid_set = {1, [2, 3]}       # TypeError: unhashable type: 'list'
# invalid_set = {1, {"a": 1}}     # TypeError: unhashable type: 'dict'
```

### 4. Adding and Removing Elements

```python
fruits = {"apple", "banana"}

# add() — adds a single element
fruits.add("cherry")
print(fruits)  # {'apple', 'banana', 'cherry'}

# add() does nothing if element already exists (no error)
fruits.add("apple")
print(fruits)  # {'apple', 'banana', 'cherry'} — unchanged

# remove() — removes element, raises KeyError if not found
fruits.remove("banana")
print(fruits)  # {'apple', 'cherry'}

# fruits.remove("mango")  # KeyError: 'mango'

# discard() — removes element, does nothing if not found (no error)
fruits.discard("mango")  # No error!
print(fruits)  # {'apple', 'cherry'}

# pop() — removes and returns an arbitrary element
popped = fruits.pop()
print(popped)   # 'apple' (or 'cherry' — order is arbitrary)
print(fruits)   # {'cherry'}

# clear() — removes all elements
fruits.clear()
print(fruits)   # set()
```

### 5. Set Operations (Mathematical)

```python
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Union — all elements from both sets
print(a | b)           # {1, 2, 3, 4, 5, 6, 7, 8}
print(a.union(b))      # {1, 2, 3, 4, 5, 6, 7, 8}

# Intersection — elements common to both sets
print(a & b)                  # {4, 5}
print(a.intersection(b))      # {4, 5}

# Difference — elements in a but not in b
print(a - b)                  # {1, 2, 3}
print(a.difference(b))        # {1, 2, 3}

# Symmetric Difference — elements in either set, but not both
print(a ^ b)                          # {1, 2, 3, 6, 7, 8}
print(a.symmetric_difference(b))      # {1, 2, 3, 6, 7, 8}
```

### 6. Subset and Superset

```python
a = {1, 2}
b = {1, 2, 3, 4}
c = {5, 6}

# issubset — is a a subset of b?
print(a.issubset(b))      # True — all elements of a are in b
print(a <= b)             # True (same as issubset)

# issuperset — is b a superset of a?
print(b.issuperset(a))    # True — b contains all elements of a
print(b >= a)             # True (same as issuperset)

# isdisjoint — do sets have NO common elements?
print(a.isdisjoint(c))    # True — no overlap
print(a.isdisjoint(b))    # False — they share 1 and 2
```

### 7. Set Comprehensions

```python
# Create a set of squares from 0 to 9
squares = {x**2 for x in range(10)}
print(squares)  # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}

# Filter: set of even numbers from 0 to 19
evens = {x for x in range(20) if x % 2 == 0}
print(evens)  # {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}

# Transform: lowercase first letters from a list of names
names = ["Alice", "Bob", "Alice", "Charlie", "Bob"]
first_letters = {name[0].lower() for name in names}
print(first_letters)  # {'a', 'b', 'c'}
```

### 8. Frozen Sets — Immutable Sets

```python
# frozenset is an immutable version of set
fs = frozenset([1, 2, 3, 4])
print(type(fs))  # <class 'frozenset'>

# fs.add(5)  # AttributeError: 'frozenset' object has no attribute 'add'

# Frozensets can be used as dictionary keys or set elements
nested = {frozenset([1, 2]), frozenset([3, 4])}
print(nested)  # {frozenset({1, 2}), frozenset({3, 4})}

# All set operations work on frozensets (returning frozensets)
a = frozenset([1, 2, 3])
b = frozenset([3, 4, 5])
print(a | b)  # frozenset({1, 2, 3, 4, 5})
```

---

## Code Examples

### Example 1: Removing Duplicates While Preserving Order

```python
# Problem: Remove duplicates but keep the original order
original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
seen = set()
result = []

for item in original:
    if item not in seen:
        seen.add(item)
        result.append(item)

print(result)  # [3, 1, 4, 5, 9, 2, 6]
```

### Example 2: Finding Common Interests

```python
alice_interests = {"python", "machine learning", "cooking", "hiking"}
bob_interests = {"python", "data science", "hiking", "photography"}
charlie_interests = {"cooking", "hiking", "travel", "photography"}

# All three share
all_share = alice_interests & bob_interests & charlie_interests
print(f"All share: {all_share}")  # {'hiking'}

# Alice and Bob share
ab_share = alice_interests & bob_interests
print(f"Alice & Bob share: {ab_share}")  # {'python', 'hiking'}

# Unique to Alice
alice_only = alice_interests - bob_interests - charlie_interests
print(f"Only Alice: {alice_only}")  # {'machine learning'}
```

### Example 3: Fast Membership Testing

```python
# Sets are O(1) for lookups vs O(n) for lists
large_list = list(range(1_000_000))
large_set = set(range(1_000_000))

import time

# List lookup
start = time.time()
999_999 in large_list
list_time = time.time() - start

# Set lookup
start = time.time()
999_999 in large_set
set_time = time.time() - start

print(f"List: {list_time:.6f}s, Set: {set_time:.6f}s")
# Set is typically 100-1000x faster for large collections
```

### Example 4: Data Validation with Sets

```python
valid_colors = {"red", "green", "blue", "yellow"}
user_input = "Red"

# Case-insensitive validation
if user_input.lower() in valid_colors:
    print(f"Valid color: {user_input}")
else:
    print(f"Invalid color: {user_input}")
```

---

## Common Mistakes to Avoid

### Mistake 1: Creating an Empty Set
```python
# WRONG — this creates a dictionary
my_set = {}
print(type(my_set))  # <class 'dict'>

# CORRECT
my_set = set()
print(type(my_set))  # <class 'set'>
```

### Mistake 2: Using `in` on Sets Thinking They're Ordered
```python
s = {3, 1, 4, 1, 5, 9}
# You can't do s[0] — sets don't support indexing
# s[0]  # TypeError: 'set' object is not subscriptable
```

### Mistake 3: Modifying a Set While Iterating
```python
# WRONG — may cause RuntimeError
s = {1, 2, 3, 4, 5}
# for item in s:
#     if item % 2 == 0:
#         s.remove(item)  # RuntimeError!

# CORRECT — iterate over a copy
s = {1, 2, 3, 4, 5}
for item in s.copy():
    if item % 2 == 0:
        s.remove(item)
print(s)  # {1, 3, 5}
```

### Mistake 4: Adding Mutable Elements
```python
# WRONG
# my_set = {[1, 2, 3]}  # TypeError

# CORRECT — use tuples instead
my_set = {(1, 2, 3)}
```

---

## Best Practices

1. **Use sets for membership testing** — they're much faster than lists for `in` operations
2. **Use sets for deduplication** — `list(set(my_list))` is the quickest way to remove duplicates
3. **Use `discard()` over `remove()`** when you're unsure if the element exists
4. **Use set operations** instead of manual loops for comparing collections
5. **Use frozensets** when you need an immutable set (e.g., as dictionary keys)
6. **Convert to list if you need indexing** — sets don't support `[]` access
7. **Use set comprehensions** for concise creation of sets from iterables

---

## Practice Exercises

### Exercise 1: Unique Words
Write a function that takes a sentence and returns a set of unique words (case-insensitive).

```python
def unique_words(sentence):
    # Your code here
    pass

# Expected: {"hello", "world"}
print(unique_words("Hello hello world World"))
```

### Exercise 2: Set Calculator
Write a function that takes two sets and an operation string ("union", "intersection", "difference", "symmetric_difference") and returns the result.

```python
def set_operation(set_a, set_b, operation):
    # Your code here
    pass

# Expected: {1, 2, 3, 4, 5}
print(set_operation({1, 2, 3}, {3, 4, 5}, "union"))
```

### Exercise 3: Find Missing Numbers
Given two sets of numbers from 1-10, find the numbers missing from each set.

```python
def missing_numbers(set_a, set_b):
    full = set(range(1, 11))
    # Your code here — return (missing from A, missing from B)
    pass
```

### Exercise 4: Password Validator
Check if a password meets these criteria using set operations:
- At least 8 characters
- Contains at least one uppercase, one lowercase, one digit, and one special character

```python
def validate_password(password):
    # Your code here
    pass
```

---

## Summary

- **Sets** are unordered collections of unique, immutable elements
- Created with `{1, 2, 3}` or `set([1, 2, 3])` — empty set needs `set()`
- **Key operations**: `add()`, `remove()`, `discard()`, `pop()`, `clear()`
- **Set math**: `union(|)`, `intersection(&)`, `difference(-)`, `symmetric_difference(^)`
- **Subset/Superset**: `issubset()`, `issuperset()`, `isdisjoint()`
- **Frozen sets** are immutable sets that can be used as dictionary keys
- Sets have **O(1) average** lookup time — much faster than lists for membership testing
- Use **set comprehensions** `{x for x in iterable if condition}` for concise creation
