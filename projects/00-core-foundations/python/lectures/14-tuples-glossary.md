# Python Tuples - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| tuple | Type | Ordered, immutable collection |
| Named Tuple | Type | Tuple with named fields |
| Tuple Unpacking | Operation | Assigning tuple elements to variables |
| Immutability | Property | Cannot be changed after creation |
| Single-element Tuple | Concept | Tuple with one element (needs comma) |
| Tuple Packing | Operation | Creating tuple from values |
| Star Unpacking | Syntax | Using * to capture remaining elements |
| _asdict() | Method | Convert named tuple to dictionary |
| _replace() | Method | Create modified named tuple |
| _fields | Attribute | Get field names of named tuple |

## Detailed Definitions

### C

**Concatenation**
- **Definition**: Joining two tuples using + operator
- **Example**: `(1, 2) + (3, 4)` → `(1, 2, 3, 4)`
- **Related terms**: + Operator, Combine, Tuple
```python
# Tuple concatenation
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined = tuple1 + tuple2
print(combined)  # (1, 2, 3, 4, 5, 6)
```

### I

**Immutability**
- **Definition**: Property that value cannot be changed after creation
- **Example**: Tuples, strings, integers are immutable
- **Related terms**: Mutable, Immutable, Change
```python
# Tuples are immutable
my_tuple = (1, 2, 3)
# my_tuple[0] = 99  # TypeError!

# Create new tuple instead
new_tuple = (99,) + my_tuple[1:]
```

**Index**
- **Definition**: Position of element in tuple (0-based)
- **Example**: `tuple[0]` gets first element
- **Related terms**: Indexing, Slicing, Position
```python
# Indexing
fruits = ("apple", "banana", "cherry")
print(fruits[0])   # apple (first)
print(fruits[-1])  # cherry (last)
```

**Indexing**
- **Definition**: Accessing element by position number
- **Example**: `tuple[0]`, `tuple[-1]`
- **Related terms**: Index, Slice, Position
```python
# Indexing examples
numbers = (10, 20, 30, 40, 50)
print(numbers[0])   # 10
print(numbers[2])   # 30
print(numbers[-1])  # 50
```

### N

**Named Tuple**
- **Definition**: Tuple subclass with named fields
- **Example**: `Point = namedtuple('Point', ['x', 'y'])`
- **Related terms**: namedtuple, Fields, Readability
```python
from collections import namedtuple

# Define named tuple
Point = namedtuple('Point', ['x', 'y'])

# Create instance
p = Point(10, 20)
print(p.x, p.y)  # 10 20

# Access by name or index
print(p[0])      # 10
print(p.x)       # 10
```

### P

**Packing**
- **Definition**: Creating tuple from values
- **Example**: `point = 10, 20` or `point = (10, 20)`
- **Related terms**: Unpacking, Assignment, Tuple
```python
# Tuple packing
point = 10, 20  # Parentheses optional
print(type(point))  # <class 'tuple'>

# Multiple values
person = "Alice", 25, "Engineer"
```

### R

**Repetition**
- **Definition**: Creating tuple with repeated elements using * operator
- **Example**: `(0,) * 5` → `(0, 0, 0, 0, 0)`
- **Related terms**: * Operator, Duplicate, Multiply
```python
# Tuple repetition
zeros = (0,) * 5
print(zeros)  # (0, 0, 0, 0, 0)

pattern = (1, 2) * 3
print(pattern)  # (1, 2, 1, 2, 1, 2)
```

### S

**Slice**
- **Definition**: Extracting sub-tuple using indices
- **Example**: `tuple[1:3]`, `tuple[:2]`, `tuple[::2]`
- **Related terms**: Indexing, Sub-tuple, Range
```python
# Slicing
numbers = (0, 1, 2, 3, 4, 5)
print(numbers[1:3])   # (1, 2)
print(numbers[:3])    # (0, 1, 2)
print(numbers[3:])    # (3, 4, 5)
print(numbers[::2])   # (0, 2, 4)
```

**Star Unpacking**
- **Definition**: Using * to capture remaining elements in unpacking
- **Example**: `first, *rest = (1, 2, 3, 4)`
- **Related terms**: Unpacking, Iterable Unpacking
```python
# Star unpacking
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# Only first and rest
first, *rest = numbers
print(first)  # 1
print(rest)   # [2, 3, 4, 5]
```

### T

**Tuple**
- **Definition**: Ordered, immutable collection
- **Example**: `(1, 2, 3)`, `("a", "b")`
- **Related terms**: Immutable, Ordered, Collection
```python
# Tuple creation
numbers = (1, 2, 3, 4, 5)
fruits = ("apple", "banana", "cherry")
mixed = (1, "hello", 3.14, True)

# Single element tuple
single = (5,)  # Note the comma
```

**Tuple Method**
- **Definition**: Limited methods available for tuples
- **Example**: `count()`, `index()`
- **Related terms**: Method, Function, Immutable
```python
# Tuple methods
numbers = (1, 2, 3, 2, 4, 2)

# count() - count occurrences
print(numbers.count(2))  # 3

# index() - find index of first occurrence
print(numbers.index(4))  # 4
```

### U

**Unpacking**
- **Definition**: Assigning tuple elements to variables
- **Example**: `x, y = (10, 20)`
- **Related terms**: Packing, Assignment, Multiple Variables
```python
# Basic unpacking
coordinates = (10, 20)
x, y = coordinates
print(x, y)  # 10 20

# Multiple assignment
a, b, c = (1, 2, 3)
print(a, b, c)  # 1 2 3

# Swap variables
x, y = 5, 10
x, y = y, x
print(x, y)  # 10 5
```

## Key Concepts Summary

### Tuple vs List
| Feature | Tuple | List |
|---------|-------|------|
| Syntax | `(1, 2, 3)` | `[1, 2, 3]` |
| Mutability | Immutable | Mutable |
| Methods | count(), index() | Many more |
| Dict Key | Yes | No |
| Performance | Faster | Slower |
| Use Case | Fixed data | Mutable data |

### Tuple Operations
| Operation | Example | Result |
|-----------|---------|--------|
| Create | `(1, 2, 3)` | `(1, 2, 3)` |
| Index | `(1, 2, 3)[0]` | `1` |
| Slice | `(1, 2, 3)[0:2]` | `(1, 2)` |
| Concat | `(1, 2) + (3, 4)` | `(1, 2, 3, 4)` |
| Repeat | `(1, 2) * 3` | `(1, 2, 1, 2, 1, 2)` |
| Length | `len((1, 2, 3))` | `3` |
| Membership | `2 in (1, 2, 3)` | `True` |

### Tuple Methods
| Method | Description | Example |
|--------|-------------|---------|
| count(x) | Count occurrences | `(1,2,2).count(2)` → `2` |
| index(x) | Find index of x | `(1,2,3).index(2)` → `1` |

### Named Tuple Pattern
```python
from collections import namedtuple

# Define
Point = namedtuple('Point', ['x', 'y'])
Student = namedtuple('Student', 'name age grade')

# Create
p = Point(10, 20)
s = Student("Alice", 20, "A")

# Access
print(p.x, p.y)
print(s.name, s.grade)

# Convert to dict
d = p._asdict()

# Create modified version
p2 = p._replace(x=50)
```

### When to Use Tuples
| Use Case | Why Tuple |
|----------|-----------|
| Fixed collections | Immutability prevents changes |
| Dictionary keys | Hashable, can be keys |
| Multiple return values | Functions can return tuples |
| Unpacking | Clean multiple assignment |
| Performance | Faster than lists |
| Data integrity | Cannot be accidentally modified |

## Practice Terms

Match these terms to their definitions:
1. tuple - ?
2. immutable - ?
3. named tuple - ?
4. unpacking - ?
5. packing - ?

**Answers:**
1. Ordered, immutable collection
2. Cannot be changed after creation
3. Tuple with named fields
4. Assigning tuple elements to variables
5. Creating tuple from values