# Python Lists - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| list | Type | Ordered, mutable collection |
| Index | Concept | Position of element in list |
| Slice | Operation | Extracting sub-list |
| List Comprehension | Syntax | Concise list creation |
| append() | Method | Add element to end |
| insert() | Method | Add element at index |
| remove() | Method | Remove first occurrence |
| pop() | Method | Remove and return element |
| sort() | Method | Sort list in place |
| Nested List | Concept | List containing lists |

## Detailed Definitions

### A

**append()**
- **Definition**: Method to add element to end of list
- **Example**: `list.append(4)` adds 4 to end
- **Related terms**: insert(), extend(), Add
```python
# append() method
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)  # ['apple', 'banana', 'cherry']

# append another list (adds as single element)
fruits.append(["date", "elderberry"])
print(fruits)  # ['apple', 'banana', 'cherry', ['date', 'elderberry']]
```

### C

**Concatenation**
- **Definition**: Joining two lists using + operator
- **Example**: `[1, 2] + [3, 4]` → `[1, 2, 3, 4]`
- **Related terms**: + Operator, extend(), Combine
```python
# List concatenation
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
print(combined)  # [1, 2, 3, 4, 5, 6]
```

**copy()**
- **Definition**: Method to create shallow copy of list
- **Example**: `new_list = old_list.copy()`
- **Related terms**: Shallow Copy, Deep Copy, Reference
```python
# copy() method
original = [1, 2, 3]
copied = original.copy()
copied[0] = 99
print(original)  # [1, 2, 3] (unchanged)
print(copied)    # [99, 2, 3]
```

### D

**Deep Copy**
- **Definition**: Creating independent copy of list and all nested objects
- **Example**: `copy.deepcopy(list)`
- **Related terms**: Shallow Copy, Nested List, Reference
```python
import copy

# Deep copy
original = [[1, 2], [3, 4]]
deep_copied = copy.deepcopy(original)
deep_copied[0][0] = 99
print(original)  # [[1, 2], [3, 4]] (unchanged)
```

**del**
- **Definition**: Statement to delete elements by index or slice
- **Example**: `del list[0]`, `del list[1:3]`
- **Related terms**: remove(), pop(), Delete
```python
# del statement
fruits = ["apple", "banana", "cherry"]
del fruits[0]  # Delete first element
print(fruits)  # ['banana', 'cherry']

del fruits[0:2]  # Delete slice
print(fruits)  # []
```

### E

**enumerate()**
- **Definition**: Function to get index and value while iterating
- **Example**: `for i, val in enumerate(list)`
- **Related terms**: Iteration, Index, Loop
```python
# enumerate() function
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry
```

**extend()**
- **Definition**: Method to add multiple elements to list
- **Example**: `list.extend([4, 5, 6])`
- **Related terms**: append(), Add, Multiple Elements
```python
# extend() method
fruits = ["apple", "banana"]
fruits.extend(["cherry", "date"])
print(fruits)  # ['apple', 'banana', 'cherry', 'date']
```

### I

**Index**
- **Definition**: Position of element in list (0-based)
- **Example**: `list[0]` gets first element
- **Related terms**: Indexing, Slicing, Position
```python
# Indexing
fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple (first)
print(fruits[-1])  # cherry (last)
```

**Indexing**
- **Definition**: Accessing element by position number
- **Example**: `list[0]`, `list[-1]`
- **Related terms**: Index, Slice, Position
```python
# Indexing examples
numbers = [10, 20, 30, 40, 50]
print(numbers[0])   # 10
print(numbers[2])   # 30
print(numbers[-1])  # 50
```

**insert()**
- **Definition**: Method to add element at specific index
- **Example**: `list.insert(1, "value")`
- **Related terms**: append(), Add, Index
```python
# insert() method
fruits = ["apple", "cherry"]
fruits.insert(1, "banana")
print(fruits)  # ['apple', 'banana', 'cherry']
```

### L

**List**
- **Definition**: Ordered, mutable collection of elements
- **Example**: `[1, 2, 3]`, `["a", "b"]`
- **Related terms**: Mutable, Ordered, Collection
```python
# List creation
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

# List operations
numbers.append(6)
numbers.remove(1)
print(numbers)
```

**List Comprehension**
- **Definition**: Concise syntax for creating lists
- **Example**: `[x**2 for x in range(10)]`
- **Related terms**: Comprehension, Concise, Pythonic
```python
# List comprehension
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### M

**Mutable**
- **Definition**: Can be changed after creation
- **Example**: Lists are mutable, tuples are not
- **Related terms**: Immutable, Change, Modify
```python
# Lists are mutable
fruits = ["apple", "banana"]
fruits[0] = "cherry"  # Works!
print(fruits)  # ['cherry', 'banana']
```

### N

**Nested List**
- **Definition**: List containing other lists
- **Example**: `[[1, 2], [3, 4]]`
- **Related terms**: 2D List, Matrix, Multi-dimensional
```python
# Nested list (matrix)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access elements
print(matrix[0][0])  # 1
print(matrix[1][2])  # 6
```

### P

**pop()**
- **Definition**: Method to remove and return element
- **Example**: `list.pop()` returns last element, `list.pop(0)` returns first
- **Related terms**: remove(), Delete, Return
```python
# pop() method
fruits = ["apple", "banana", "cherry"]
last = fruits.pop()
print(last)    # cherry
print(fruits)  # ['apple', 'banana']

first = fruits.pop(0)
print(first)   # apple
print(fruits)  # ['banana']
```

### R

**remove()**
- **Definition**: Method to remove first occurrence of value
- **Example**: `list.remove("value")`
- **Related terms**: pop(), del, Delete
```python
# remove() method
fruits = ["apple", "banana", "cherry", "banana"]
fruits.remove("banana")  # Removes first occurrence
print(fruits)  # ['apple', 'cherry', 'banana']
```

**Repetition**
- **Definition**: Creating list with repeated elements using * operator
- **Example**: `[0] * 5` → `[0, 0, 0, 0, 0]`
- **Related terms**: * Operator, Duplicate, Multiply
```python
# List repetition
zeros = [0] * 5
print(zeros)  # [0, 0, 0, 0, 0]

pattern = [1, 2] * 3
print(pattern)  # [1, 2, 1, 2, 1, 2]
```

### S

**Shallow Copy**
- **Definition**: Creating copy that references same nested objects
- **Example**: `list.copy()`, `list[:]`, `list(list)`
- **Related terms**: Deep Copy, Reference, Nested
```python
# Shallow copy
original = [[1, 2], [3, 4]]
shallow = original.copy()
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] - Modified!
```

**Slice**
- **Definition**: Extracting sub-list using indices
- **Example**: `list[1:3]`, `list[:2]`, `list[::2]`
- **Related terms**: Indexing, Sub-list, Range
```python
# Slicing
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:3])   # [1, 2]
print(numbers[:3])    # [0, 1, 2]
print(numbers[3:])    # [3, 4, 5]
print(numbers[::2])   # [0, 2, 4]
```

**sort()**
- **Definition**: Method to sort list in place
- **Example**: `list.sort()`, `list.sort(reverse=True)`
- **Related terms**: sorted(), Order, Ascending
```python
# sort() method
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Descending order
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]
```

**sorted()**
- **Definition**: Function to return new sorted list
- **Example**: `new_list = sorted(old_list)`
- **Related terms**: sort(), Order, New List
```python
# sorted() function
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)
print(original)    # [3, 1, 4, 1, 5] (unchanged)
print(sorted_list) # [1, 1, 3, 4, 5]
```

### T

**Tuple**
- **Definition**: Ordered, immutable collection
- **Example**: `(1, 2, 3)`
- **Related terms**: Immutable, List, Ordered
```python
# Tuple vs List
my_list = [1, 2, 3]    # Mutable
my_tuple = (1, 2, 3)   # Immutable

my_list[0] = 99   # Works
# my_tuple[0] = 99  # TypeError!
```

## Key Concepts Summary

### List Operations
| Operation | Example | Result |
|-----------|---------|--------|
| Create | `[1, 2, 3]` | `[1, 2, 3]` |
| Index | `[1, 2, 3][0]` | `1` |
| Slice | `[1, 2, 3][0:2]` | `[1, 2]` |
| Concat | `[1, 2] + [3, 4]` | `[1, 2, 3, 4]` |
| Repeat | `[1, 2] * 3` | `[1, 2, 1, 2, 1, 2]` |
| Length | `len([1, 2, 3])` | `3` |
| Membership | `2 in [1, 2, 3]` | `True` |

### List Methods
| Method | Description | Example |
|--------|-------------|---------|
| append(x) | Add x to end | `[1, 2].append(3)` → `[1, 2, 3]` |
| insert(i, x) | Insert x at index i | `[1, 3].insert(1, 2)` → `[1, 2, 3]` |
| extend(iter) | Add multiple elements | `[1].extend([2, 3])` → `[1, 2, 3]` |
| remove(x) | Remove first x | `[1, 2, 1].remove(1)` → `[2, 1]` |
| pop(i) | Remove and return i | `[1, 2, 3].pop()` → returns 3 |
| sort() | Sort in place | `[3, 1, 2].sort()` → `[1, 2, 3]` |
| reverse() | Reverse in place | `[1, 2, 3].reverse()` → `[3, 2, 1]` |
| copy() | Shallow copy | `[1, 2].copy()` → `[1, 2]` |
| index(x) | Find index of x | `[1, 2, 3].index(2)` → `1` |
| count(x) | Count occurrences | `[1, 1, 2].count(1)` → `2` |

### List Comprehension Patterns
| Pattern | Example | Result |
|---------|---------|--------|
| Basic | `[x**2 for x in range(5)]` | `[0, 1, 4, 9, 16]` |
| With condition | `[x for x in range(10) if x%2==0]` | `[0, 2, 4, 6, 8]` |
| With function | `[x.upper() for x in ['a','b']]` | `['A', 'B']` |
| Nested | `[[i*j for j in range(3)] for i in range(3)]` | `[[0,0,0],[0,1,2],[0,2,4]]` |

### Common Patterns
```python
# Initialize empty list
my_list = []

# Add elements
my_list.append(1)
my_list.extend([2, 3])

# Iterate with index
for i, val in enumerate(my_list):
    print(f"{i}: {val}")

# Filter with comprehension
evens = [x for x in my_list if x % 2 == 0]

# Sort
my_list.sort()
```

## Practice Terms

Match these terms to their definitions:
1. list - ?
2. append() - ?
3. list comprehension - ?
4. slice - ?
5. sort() - ?

**Answers:**
1. Ordered, mutable collection
2. Add element to end of list
3. Concise list creation syntax
4. Extracting sub-list using indices
5. Sort list in place