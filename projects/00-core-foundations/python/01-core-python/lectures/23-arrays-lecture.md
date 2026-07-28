# Python Arrays (Lists) — Lecture 23

## Topic Overview

In Python, the term "array" most commonly refers to **lists** — ordered, mutable collections that can hold elements of any type. While Python has a built-in `array` module for typed arrays and NumPy provides powerful array operations, **lists** are the go-to data structure for most Python programming.

Lists are one of the most versatile data structures in Python, supporting indexing, slicing, iteration, and a rich set of methods for manipulation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Create and initialize lists in different ways
- Access elements using indexing and slicing
- Modify lists using various methods
- Understand list memory and performance characteristics
- Use list comprehensions for concise operations
- Implement common list algorithms
- Know when to use lists vs. other data structures

---

## Key Concepts

### 1. Creating Lists

```python
# Empty list
empty = []
empty = list()

# List with values
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]

# From other iterables
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
nums = list(range(5))  # [0, 1, 2, 3, 4]
```

### 2. Accessing Elements (Indexing)

```python
fruits = ["apple", "banana", "cherry", "date"]

# Positive indexing (0-based)
print(fruits[0])    # apple
print(fruits[2])    # cherry

# Negative indexing
print(fruits[-1])   # date (last)
print(fruits[-2])   # cherry (second to last)

# Out of range raises IndexError
# print(fruits[10])  # IndexError: list index out of range
```

### 3. Slicing

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slice [start:stop]
print(numbers[2:5])    # [2, 3, 4]

# From start
print(numbers[:5])     # [0, 1, 2, 3, 4]

# To end
print(numbers[5:])     # [5, 6, 7, 8, 9]

# With step
print(numbers[::2])    # [0, 2, 4, 6, 8]
print(numbers[1::2])   # [1, 3, 5, 7, 9]

# Reverse
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# Copy
copy = numbers[:]
```

### 4. Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]

# Change element
fruits[0] = "avocado"
print(fruits)  # ['avocado', 'banana', 'cherry']

# Slice assignment
fruits[1:3] = ["blueberry", "cranberry", "dragonfruit"]
print(fruits)  # ['avocado', 'blueberry', 'cranberry', 'dragonfruit', None]

# Insert
fruits.insert(1, "banana")
print(fruits)  # ['avocado', 'banana', 'blueberry', ...]

# Append
fruits.append("elderberry")

# Extend
fruits.extend(["fig", "grape"])

# Remove
fruits.remove("banana")  # Remove first occurrence
popped = fruits.pop()    # Remove and return last
del fruits[0]            # Remove by index
```

### 5. List Methods

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort
numbers.sort()           # In-place sort
numbers.sort(reverse=True)  # Descending

# Sorted (returns new list)
sorted_nums = sorted(numbers)

# Reverse (in-place)
numbers.reverse()

# Find
index = numbers.index(5)      # Index of first occurrence
count = numbers.count(1)      # Count occurrences

# Copy
copy = numbers.copy()

# Clear
numbers.clear()
```

### 6. List Comprehensions

```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
matrix = [[j for j in range(3)] for i in range(3)]

# Transform
words = ["hello", "world"]
upper = [word.upper() for word in words]

# Flatten
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sublist in nested for x in sublist]
```

### 7. Common List Operations

```python
# Concatenation
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2

# Repetition
zeros = [0] * 5  # [0, 0, 0, 0, 0]

# Membership
print(3 in list1)  # True
print(7 not in list1)  # True

# Length
print(len(list1))  # 3

# Min/Max/Sum
print(min(list1))  # 1
print(max(list1))  # 3
print(sum(list1))  # 6

# Unpacking
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5
```

---

## Code Examples

### Example 1: Remove Duplicates (Preserve Order)

```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

print(remove_duplicates([1, 2, 2, 3, 1, 4, 3, 5]))  # [1, 2, 3, 4, 5]
```

### Example 2: Rotate List

```python
def rotate(lst, n):
    """Rotate list by n positions."""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[-n:] + lst[:-n]

print(rotate([1, 2, 3, 4, 5], 2))  # [4, 5, 1, 2, 3]
print(rotate([1, 2, 3, 4, 5], -1))  # [2, 3, 4, 5, 1]
```

### Example 3: Flatten Nested List

```python
def flatten(nested):
    """Recursively flatten nested lists."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, 3], [4, [5, 6]]]))  # [1, 2, 3, 4, 5, 6]
```

### Example 4: Matrix Transpose

```python
def transpose(matrix):
    """Transpose a matrix."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
print(transpose(matrix))  # [[1, 4], [2, 5], [3, 6]]
```

### Example 5: Two Sum Problem

```python
def two_sum(nums, target):
    """Find indices of two numbers that sum to target."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

---

## Common Mistakes to Avoid

### Mistake 1: Modifying List While Iterating
```python
# WRONG
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Skips elements!

# CORRECT — use list comprehension
items = [item for item in items if item % 2 != 0]
```

### Mistake 2: Shallow Copy Issues
```python
# WRONG — nested lists share references
original = [[1, 2], [3, 4]]
copy = original.copy()
copy[0][0] = 99
print(original[0][0])  # 99 — original modified!

# CORRECT — deep copy
import copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original[0][0])  # 1 — original unchanged
```

### Mistake 3: Using `*` for Nested Lists
```python
# WRONG — creates shared references
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — all rows changed!

# CORRECT — use comprehension
matrix = [[0] * 3 for _ in range(3)]
matrix[0][0] = 1
print(matrix)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] — only first row
```

---

## Best Practices

1. **Use list comprehensions** for concise transformations
2. **Use `append()`** for adding single items, `extend()` for multiple
3. **Use `in` operator** for membership testing (O(n) — consider sets for large data)
4. **Use slicing** for copying and subsetting
5. **Use `sorted()`** when you need a new list
6. **Use `enumerate()`** for index-value pairs
7. **Use unpacking** for elegant assignment
8. **Consider `collections.deque`** for frequent insert/delete at ends

---

## Practice Exercises

### Exercise 1: Merge Sorted Lists
Write a function that merges two sorted lists into one sorted list.

```python
def merge_sorted(list1, list2):
    # Your code here
    pass

# Expected: [1, 2, 3, 4, 5, 6]
print(merge_sorted([1, 3, 5], [2, 4, 6]))
```

### Exercise 2: Find Duplicates
Write a function that finds all duplicate elements in a list.

```python
def find_duplicates(lst):
    # Your code here
    pass

# Expected: [2, 3]
print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))
```

### Exercise 3: Matrix Rotate 90°
Write a function that rotates a matrix 90 degrees clockwise.

```python
def rotate_90(matrix):
    # Your code here
    pass

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
# Expected: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
print(rotate_90(matrix))
```

---

## Summary

- **Lists** are ordered, mutable, heterogeneous collections
- **Indexing**: `lst[0]`, `lst[-1]`
- **Slicing**: `lst[start:stop:step]`
- **Methods**: `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `sort()`, `reverse()`
- **Comprehensions**: `[x for x in iterable if condition]`
- **Operations**: `+` (concat), `*` (repeat), `in`, `len()`, `min()`, `max()`, `sum()`
- **Unpacking**: `first, *rest = lst`
- **Use `deepcopy`** for nested lists
- **Avoid modifying** while iterating
