# Python Arrays (Lists) — Glossary 23

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| List | Ordered, mutable collection | `[1, 2, 3]` |
| Index | Position of element (0-based) | `lst[0]` |
| Negative Index | Index from end | `lst[-1]` |
| Slice | Extract subsequence | `lst[1:3]` |
| Append | Add element to end | `lst.append(x)` |
| Extend | Add multiple elements | `lst.extend([x, y])` |
| Insert | Add at specific position | `lst.insert(i, x)` |
| Remove | Remove first occurrence | `lst.remove(x)` |
| Pop | Remove and return element | `lst.pop()` |
| Sort | Sort in-place | `lst.sort()` |
| Reverse | Reverse in-place | `lst.reverse()` |
| Copy | Shallow copy | `lst.copy()` |
| Clear | Remove all elements | `lst.clear()` |
| Index | Find element position | `lst.index(x)` |
| Count | Count occurrences | `lst.count(x)` |
| List Comprehension | Concise list creation | `[x for x in range(10)]` |
| Nested List | List containing lists | `[[1, 2], [3, 4]]` |
| Shallow Copy | Copy without deep nesting | `lst.copy()` |
| Deep Copy | Independent copy of all levels | `copy.deepcopy(lst)` |
| Unpacking | Assign multiple variables | `a, b, c = lst` |
| Star Unpacking | Capture remaining elements | `a, *b = lst` |
| Concatenation | Combine lists with `+` | `[1, 2] + [3, 4]` |
| Repetition | Repeat with `*` | `[0] * 5` |
| Membership | Check with `in` | `x in lst` |
| List Array | Typed array (module) | `array.array('i', [1, 2])` |
| Mutability | Can be modified after creation | Lists are mutable |

---

## Definitions

### Append
**Definition**: A method that adds a single element to the end of a list. Modifies the list in-place.

**Example**:
```python
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)  # ['apple', 'banana', 'cherry']

# append adds the element as-is
fruits.append(["date", "elderberry"])
print(fruits)  # ['apple', 'banana', 'cherry', ['date', 'elderberry']]
```

**Related**: `extend()`, `insert()`, adding elements

---

### Clear
**Definition**: A method that removes all elements from a list, leaving it empty.

**Example**:
```python
numbers = [1, 2, 3, 4, 5]
numbers.clear()
print(numbers)  # []
```

**Related**: `remove()`, `pop()`, `del`, empty list

---

### Concatenation
**Definition**: Combining two lists using the `+` operator. Creates a new list containing elements from both.

**Example**:
```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
print(combined)  # [1, 2, 3, 4, 5, 6]

# Also works with extend (in-place)
list1.extend(list2)
```

**Related**: `extend()`, `+` operator, combining lists

---

### Copy
**Definition**: A method that creates a shallow copy of a list. Changes to the copy don't affect the original for top-level elements.

**Example**:
```python
original = [1, 2, 3]
copy_list = original.copy()
copy_list[0] = 99
print(original)  # [1, 2, 3] — unchanged

# Shallow copy — nested objects are shared
original = [[1, 2], [3, 4]]
copy_list = original.copy()
copy_list[0][0] = 99
print(original[0][0])  # 99 — shared reference!
```

**Related**: shallow copy, deep copy, `[:]`, `list()`

---

### Count
**Definition**: A method that returns the number of times a specified element appears in the list.

**Example**:
```python
numbers = [1, 2, 3, 2, 4, 2, 5]
print(numbers.count(2))  # 3
print(numbers.count(6))  # 0
```

**Related**: `index()`, frequency, occurrences

---

### Deep Copy
**Definition**: A complete, independent copy of a list and all nested objects. Changes to the copy don't affect the original at any level.

**Example**:
```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original[0][0])  # 1 — unchanged!
```

**Related**: shallow copy, `copy.deepcopy()`, nested lists

---

### Extend
**Definition**: A method that adds all elements from an iterable to the end of the list. Modifies the list in-place.

**Example**:
```python
fruits = ["apple", "banana"]
fruits.extend(["cherry", "date"])
print(fruits)  # ['apple', 'banana', 'cherry', 'date']

# Unlike append, extend unpacks iterables
fruits.append(["elderberry"])  # Adds list as single element
print(fruits)  # [... ['elderberry']]

fruits.extend(["fig"])  # Adds elements individually
print(fruits)  # [... 'fig']
```

**Related**: `append()`, `+=`, adding multiple elements

---

### Index
**Definition**: A method that returns the index of the first occurrence of a specified element. Raises ValueError if not found.

**Example**:
```python
fruits = ["apple", "banana", "cherry", "banana"]
print(fruits.index("banana"))  # 1
print(fruits.index("banana", 2))  # 3 (start searching from index 2)

# fruits.index("mango")  # ValueError
```

**Related**: `find()` (strings), position, searching

---

### Index
**Definition**: The position of an element in a list. Python uses zero-based indexing.

**Example**:
```python
lst = ["a", "b", "c", "d", "e"]
print(lst[0])   # a (first)
print(lst[2])   # c (third)
print(lst[-1])  # e (last)
print(lst[-2])  # d (second to last)
```

**Related**: zero-based, negative indexing, slicing

---

### Insert
**Definition**: A method that inserts an element at a specified position in the list.

**Example**:
```python
fruits = ["apple", "cherry"]
fruits.insert(1, "banana")
print(fruits)  # ['apple', 'banana', 'cherry']

# Insert at end (same as append)
fruits.insert(len(fruits), "date")
```

**Related**: `append()`, `extend()`, adding elements

---

### List
**Definition**: An ordered, mutable collection that can hold elements of any type. Defined with square brackets `[]` or `list()` constructor.

**Example**:
```python
# Creating lists
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4]]

# From iterable
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
nums = list(range(5))  # [0, 1, 2, 3, 4]
```

**Related**: tuple, set, array, mutable, ordered

---

### List Comprehension
**Definition**: A concise syntax for creating lists using `[expression for item in iterable if condition]`.

**Example**:
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
flat = [x for row in matrix for x in row]

# Transform
upper = [word.upper() for word in ["hello", "world"]]
```

**Related**: generator expression, dict comprehension, set comprehension

---

### List Array
**Definition**: A typed array from Python's `array` module. More memory-efficient than lists for large sequences of the same type, but less flexible.

**Example**:
```python
from array import array

# Create typed array
arr = array('i', [1, 2, 3, 4, 5])  # 'i' = signed int
print(arr)  # array('i', [1, 2, 3, 4, 5])

# arr.append("hello")  # TypeError: integer expected
```

**Related**: NumPy array, typed, memory-efficient

---

### Membership
**Definition**: The operation of checking whether an element exists in a list, using the `in` operator. O(n) time complexity for lists.

**Example**:
```python
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)    # True
print("mango" in fruits)    # False
print("mango" not in fruits) # True
```

**Related**: `in`, `not in`, O(n) complexity

---

### Mutability
**Definition**: The ability to modify a collection after creation. Lists are mutable — you can add, remove, and change elements.

**Example**:
```python
# Lists are mutable
lst = [1, 2, 3]
lst[0] = 99
lst.append(4)
print(lst)  # [99, 2, 3, 4]

# Tuples are immutable
tup = (1, 2, 3)
# tup[0] = 99  # TypeError
```

**Related**: immutable, tuple, modification

---

### Negative Index
**Definition**: Indexing from the end of the list using negative numbers. `-1` is the last element, `-2` is second-to-last, etc.

**Example**:
```python
lst = [10, 20, 30, 40, 50]
print(lst[-1])   # 50
print(lst[-2])   # 40
print(lst[-5])   # 10
```

**Related**: indexing, slicing, zero-based

---

### Nested List
**Definition**: A list that contains other lists as elements, creating a 2D or multi-dimensional structure.

**Example**:
```python
# 2D matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[0][0])  # 1
print(matrix[1][2])  # 6

# Iterating nested lists
for row in matrix:
    for cell in row:
        print(cell, end=" ")
    print()
```

**Related**: 2D array, matrix, nested data structures

---

### Pop
**Definition**: A method that removes and returns an element at a specified index (default: last element).

**Example**:
```python
fruits = ["apple", "banana", "cherry"]
last = fruits.pop()
print(last)    # cherry
print(fruits)  # ['apple', 'banana']

first = fruits.pop(0)
print(first)   # apple
print(fruits)  # ['banana']
```

**Related**: `remove()`, `del`, `append()`, `insert()`

---

### Remove
**Definition**: A method that removes the first occurrence of a specified element. Raises ValueError if not found.

**Example**:
```python
numbers = [1, 2, 3, 2, 4]
numbers.remove(2)
print(numbers)  # [1, 3, 2, 4] — only first 2 removed

# numbers.remove(5)  # ValueError: list.remove(x): x not in list
```

**Related**: `pop()`, `del`, `clear()`

---

### Repetition
**Definition**: Creating a list by repeating another list using the `*` operator.

**Example**:
```python
zeros = [0] * 5  # [0, 0, 0, 0, 0]
ones = [1] * 3   # [1, 1, 1]

# WARNING: nested list repetition shares references!
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] — all rows changed!
```

**Related**: `*` operator, concatenation, shared references

---

### Reverse
**Definition**: A method that reverses the elements of a list in-place. Or use slicing `[::-1]` to create a reversed copy.

**Example**:
```python
# In-place reverse
lst = [1, 2, 3, 4, 5]
lst.reverse()
print(lst)  # [5, 4, 3, 2, 1]

# New reversed list (doesn't modify original)
original = [1, 2, 3, 4, 5]
reversed_list = original[::-1]
print(original)    # [1, 2, 3, 4, 5] — unchanged
print(reversed_list)  # [5, 4, 3, 2, 1]
```

**Related**: slicing, `[::-1]`, in-place modification

---

### Shallow Copy
**Definition**: A copy of a list where nested objects are referenced, not copied. Changes to nested objects in the copy affect the original.

**Example**:
```python
# Shallow copy methods
original = [1, 2, 3]
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

# All are shallow copies
copy1[0] = 99
print(original)  # [1, 2, 3] — independent for top-level
```

**Related**: deep copy, `copy()`, `[:]`, `list()`

---

### Slice
**Definition**: A portion of a list extracted using `lst[start:stop:step]`. Returns a new list.

**Example**:
```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(lst[2:5])    # [2, 3, 4]
print(lst[:3])     # [0, 1, 2]
print(lst[7:])     # [7, 8, 9]
print(lst[::2])    # [0, 2, 4, 6, 8]
print(lst[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

**Related**: indexing, start, stop, step, subsequence

---

### Sort
**Definition**: A method that sorts the list in-place. Can use a custom key function and reverse flag.

**Example**:
```python
# Simple sort
numbers = [3, 1, 4, 1, 5, 9]
numbers.sort()
print(numbers)  # [1, 1, 3, 4, 5, 9]

# Descending
numbers.sort(reverse=True)
print(numbers)  # [9, 5, 4, 3, 1, 1]

# With key
words = ["banana", "apple", "cherry"]
words.sort(key=len)
print(words)  # ['apple', 'banana', 'cherry']
```

**Related**: `sorted()`, key function, stable sort

---

### Star Unpacking
**Definition**: Using `*` in assignment to capture remaining elements of a list into a new list.

**Example**:
```python
# Capture first and rest
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

# Capture first, last, and middle
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

**Related**: unpacking, `*args`, multiple assignment

---

### Unpacking
**Definition**: Assigning multiple variables from a list in a single statement.

**Example**:
```python
# Basic unpacking
a, b, c = [1, 2, 3]
print(a, b, c)  # 1 2 3

# Swap variables
a, b = b, a

# Ignore values with _
first, _, third = [1, 2, 3]
```

**Related**: multiple assignment, swap, star unpacking

---

## Code Examples

### Example 1: Rotate List
```python
def rotate(lst, n):
    """Rotate list n positions to the right."""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[-n:] + lst[:-n]

print(rotate([1, 2, 3, 4, 5], 2))  # [4, 5, 1, 2, 3]
```

### Example 2: Find Duplicates
```python
def find_duplicates(lst):
    """Find all duplicate elements."""
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # [2, 3]
```

---

## Related Concepts

- **Tuple**: Immutable alternative to lists
- **Set**: Unordered, unique elements
- **Array module**: Typed arrays
- **NumPy arrays**: Efficient numerical arrays
- **Deque**: Double-ended queue for efficient appends/pops
- **Generators**: Lazy sequences
