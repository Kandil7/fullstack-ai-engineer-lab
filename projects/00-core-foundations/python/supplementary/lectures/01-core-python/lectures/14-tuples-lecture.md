# Python Tuples - Lecture Notes

## 1. Topic Overview
This lecture covers Python tuples in detail. Tuples are ordered, immutable collections similar to lists but cannot be changed after creation. They are used for storing fixed collections of items and as dictionary keys.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Create and initialize tuples
- Access tuple elements using indexing and slicing
- Understand tuple immutability
- Use tuple methods effectively
- Work with named tuples
- Know when to use tuples vs lists

## 3. Key Concepts

### 3.1 Tuple Creation
Tuples are created using parentheses `()` or the `tuple()` constructor.

```python
# Empty tuple
empty_tuple = ()
empty_tuple = tuple()

# Tuple with values
numbers = (1, 2, 3, 4, 5)
fruits = ("apple", "banana", "cherry")
mixed = (1, "hello", 3.14, True)

# Single element tuple (note the comma)
single = (5,)  # This is a tuple
not_tuple = (5)  # This is just an integer!

# From other iterables
chars = tuple("hello")  # ('h', 'e', 'l', 'l', 'o')
```

### 3.2 Tuple Immutability
Tuples cannot be changed after creation.

```python
fruits = ("apple", "banana", "cherry")
# fruits[0] = "date"  # TypeError! Tuples are immutable

# Create new tuple instead
new_fruits = ("date",) + fruits[1:]
```

### 3.3 Tuple Indexing and Slicing
Access elements using indices (0-based).

```python
fruits = ("apple", "banana", "cherry", "date")

# Indexing
print(fruits[0])   # apple
print(fruits[-1])  # date (last element)

# Slicing
print(fruits[0:2])   # ('apple', 'banana')
print(fruits[1:3])   # ('banana', 'cherry')
print(fruits[:2])    # ('apple', 'banana')
print(fruits[2:])    # ('cherry', 'date')
```

### 3.4 Tuple Methods

**Limited methods (because immutable):**
```python
numbers = (1, 2, 3, 2, 4, 2)

# count() - count occurrences
print(numbers.count(2))  # 3

# index() - find index of first occurrence
print(numbers.index(4))  # 4
```

### 3.5 Tuple Operations

**Concatenation and repetition:**
```python
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

# Concatenation
combined = tuple1 + tuple2  # (1, 2, 3, 4, 5, 6)

# Repetition
repeated = tuple1 * 3  # (1, 2, 3, 1, 2, 3, 1, 2, 3)
```

**Membership and length:**
```python
numbers = (1, 2, 3, 4, 5)

print(3 in numbers)      # True
print(6 not in numbers)  # True
print(len(numbers))      # 5
```

### 3.6 Tuple Unpacking
Assign tuple elements to variables.

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

# Star unpacking
first, *middle, last = (1, 2, 3, 4, 5)
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

### 3.7 Named Tuples
Tuples with named fields for better readability.

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

## 4. Code Examples

### Example 1: Basic Tuple Operations
```python
# Create tuple
fruits = ("apple", "banana", "cherry")

# Access elements
print(fruits[0])   # apple
print(fruits[-1])  # cherry

# Slice
print(fruits[0:2])  # ('apple', 'banana')

# Methods
print(fruits.count("apple"))  # 1
print(fruits.index("banana"))  # 1
```

### Example 2: Tuple Unpacking
```python
# Unpacking
person = ("Alice", 25, "Engineer")
name, age, job = person
print(f"{name} is {age} years old and works as {job}")

# Swap variables
x, y = 5, 10
print(f"Before: x={x}, y={y}")
x, y = y, x
print(f"After: x={x}, y={y}")

# Star unpacking
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers
print(f"First: {first}, Middle: {middle}, Last: {last}")
```

### Example 3: Named Tuples
```python
from collections import namedtuple

# Define named tuple
Student = namedtuple('Student', ['name', 'age', 'grade'])

# Create instances
alice = Student("Alice", 20, "A")
bob = Student("Bob", 22, "B")

# Access fields
print(f"{alice.name} got grade {alice.grade}")
print(f"{bob.name} is {bob.age} years old")

# Convert to dictionary
alice_dict = alice._asdict()
print(alice_dict)
```

### Example 4: Tuple as Dictionary Key
```python
# Tuples can be dictionary keys (lists cannot)
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London",
    (35.6762, 139.6503): "Tokyo"
}

# Access using tuple key
print(locations[(51.5074, -0.1278)])  # London
```

## 5. Common Mistakes to Avoid

### Mistake 1: Forgetting the Comma for Single Elements
```python
# Wrong - not a tuple
not_tuple = (5)
print(type(not_tuple))  # <class 'int'>

# Right - use comma
is_tuple = (5,)
print(type(is_tuple))  # <class 'tuple'>
```

### Mistake 2: Trying to Modify Tuples
```python
# Wrong - tuples are immutable
my_tuple = (1, 2, 3)
# my_tuple[0] = 99  # TypeError!

# Right - create new tuple
new_tuple = (99,) + my_tuple[1:]
```

### Mistake 3: Using Tuples When Lists are Needed
```python
# Wrong - using tuple for mutable data
items = ("apple", "banana")  # Can't add/remove items

# Right - use list for mutable data
items = ["apple", "banana"]
items.append("cherry")
```

### Mistake 4: Forgetting Tuple Packing
```python
# This is tuple packing
point = 10, 20  # Parentheses optional
print(type(point))  # <class 'tuple'>

# This is just two separate variables
x = 10
y = 20
```

## 6. Best Practices

1. **Use tuples** for fixed collections of items
2. **Use named tuples** for better readability
3. **Use tuples as dictionary keys** when needed
4. **Prefer tuples** over lists for immutable data
5. **Use tuple unpacking** for multiple assignment
6. **Document** expected tuple structure

## 7. Practice Exercises

### Exercise 1: Tuple Manipulator
Create a program that demonstrates tuple operations (creation, slicing, unpacking).

### Exercise 2: Named Tuple Example
Implement a named tuple for a book (title, author, year) and create a library.

### Exercise 3: Tuple vs List
Compare when to use tuples vs lists with examples.

## 8. Summary

**Key takeaways:**
- Tuples are ordered, immutable collections
- Use parentheses or tuple() to create
- Tuples can be dictionary keys
- Tuple unpacking simplifies multiple assignment
- Named tuples improve readability
- Use tuples for fixed data, lists for mutable data

**Next Lecture:** We'll explore more advanced data structures.

---

**Quick Reference:**
- Tuple Type: https://docs.python.org/3/library/stdtypes.html#tuple
- Named Tuples: https://docs.python.org/3/library/collections.html#collections.namedtuple
- Tuple Unpacking: https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences