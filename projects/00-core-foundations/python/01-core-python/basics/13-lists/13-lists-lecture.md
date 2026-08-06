# Python Lists - Lecture Notes

## 1. Topic Overview
This lecture covers Python lists in detail. Lists are ordered, mutable collections that can hold multiple items. They are one of the most versatile data structures in Python, used for storing and manipulating sequences of data.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Create and initialize lists
- Access list elements using indexing and slicing
- Modify lists (add, remove, sort elements)
- Use list methods effectively
- Understand list comprehensions
- Work with nested lists

## 3. Key Concepts

### 3.1 List Creation
Lists are created using square brackets `[]` or the `list()` constructor.

```python
# Empty list
empty_list = []
empty_list = list()

# List with values
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]

# From other iterables
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
```

### 3.2 List Indexing and Slicing
Access elements using indices (0-based).

```python
fruits = ["apple", "banana", "cherry", "date"]

# Indexing
print(fruits[0])   # apple
print(fruits[-1])  # date (last element)

# Slicing
print(fruits[0:2])   # ['apple', 'banana']
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:2])    # ['apple', 'banana']
print(fruits[2:])    # ['cherry', 'date']
```

### 3.3 List Modification

**Adding elements:**
```python
fruits = ["apple", "banana"]

# append() - add to end
fruits.append("cherry")

# insert() - add at index
fruits.insert(1, "blueberry")

# extend() - add multiple elements
fruits.extend(["date", "elderberry"])

# concatenation
fruits = fruits + ["fig"]
```

**Removing elements:**
```python
fruits = ["apple", "banana", "cherry", "banana"]

# remove() - remove first occurrence
fruits.remove("banana")

# pop() - remove and return element
last = fruits.pop()

# del - remove by index
del fruits[0]

# clear() - remove all elements
fruits.clear()
```

### 3.4 List Methods

**Common methods:**
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sorting
numbers.sort()  # Sort in place
sorted_numbers = sorted(numbers)  # Return new sorted list

# Reversing
numbers.reverse()

# Counting
print(numbers.count(1))  # 2

# Finding index
print(numbers.index(5))  # 4

# Copying
copy = numbers.copy()
```

### 3.5 List Comprehensions
Concise way to create lists.

```python
# Basic syntax
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# With function
upper_fruits = [fruit.upper() for fruit in fruits]

# Nested lists
matrix = [[i*j for j in range(3)] for i in range(3)]
```

### 3.6 List Operations

**Concatenation and repetition:**
```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Concatenation
combined = list1 + list2  # [1, 2, 3, 4, 5, 6]

# Repetition
repeated = list1 * 3  # [1, 2, 3, 1, 2, 3, 1, 2, 3]
```

**Membership and length:**
```python
numbers = [1, 2, 3, 4, 5]

print(3 in numbers)      # True
print(6 not in numbers)  # True
print(len(numbers))      # 5
```

## 4. Code Examples

### Example 1: Basic List Operations
```python
# Create list
fruits = ["apple", "banana", "cherry"]

# Add elements
fruits.append("date")
fruits.insert(1, "blueberry")

# Remove elements
fruits.remove("banana")
last = fruits.pop()

# Display
print(fruits)
print(f"Popped: {last}")
```

### Example 2: List Comprehensions
```python
# Squares of numbers 1-10
squares = [x**2 for x in range(1, 11)]
print(squares)

# Filter even numbers
numbers = range(20)
evens = [x for x in numbers if x % 2 == 0]
print(evens)

# Transform strings
words = ["hello", "world", "python"]
upper_words = [word.upper() for word in words]
print(upper_words)
```

### Example 3: Sorting and Searching
```python
# Sorting
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Original: {numbers}")

numbers.sort()
print(f"Sorted: {numbers}")

numbers.reverse()
print(f"Reversed: {numbers}")

# Finding elements
print(f"Index of 5: {numbers.index(5)}")
print(f"Count of 1: {numbers.count(1)}")
```

### Example 4: Nested Lists
```python
# Matrix (2D list)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access elements
print(matrix[0][0])  # 1
print(matrix[1][2])  # 6

# Iterate through matrix
for row in matrix:
    for item in row:
        print(item, end=" ")
    print()
```

## 5. Common Mistakes to Avoid

### Mistake 1: Modifying List During Iteration
```python
# Wrong - modifying during iteration
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Bug!

# Right - iterate over copy
for num in numbers[:]:
    if num % 2 == 0:
        numbers.remove(num)
```

### Mistake 2: Shallow vs Deep Copy
```python
# Shallow copy - references same objects
list1 = [[1, 2], [3, 4]]
list2 = list1.copy()
list2[0][0] = 99
print(list1)  # [[99, 2], [3, 4]] - Modified!

# Deep copy - independent objects
import copy
list1 = [[1, 2], [3, 4]]
list2 = copy.deepcopy(list1)
list2[0][0] = 99
print(list1)  # [[1, 2], [3, 4]] - Unchanged
```

### Mistake 3: Not Using List Comprehensions
```python
# Non-Pythonic
squares = []
for x in range(10):
    squares.append(x**2)

# Pythonic
squares = [x**2 for x in range(10)]
```

### Mistake 4: Forgetting List is Mutable
```python
# List is mutable
original = [1, 2, 3]
modified = original
modified[0] = 99
print(original)  # [99, 2, 3] - Both point to same list!

# Use copy if you want independence
modified = original.copy()
```

## 6. Best Practices

1. **Use list comprehensions** for concise list creation
2. **Prefer append()** over concatenation for adding elements
3. **Use slice assignment** for bulk updates
4. **Consider collections.deque** for frequent insertions/deletions
5. **Use enumerate()** for index-value pairs
6. **Document** expected list contents

## 7. Practice Exercises

### Exercise 1: List Manipulator
Create a program that can add, remove, sort, and search in a list.

### Exercise 2: List Comprehensions
Write list comprehensions to:
- Generate first 20 Fibonacci numbers
- Filter words longer than 5 characters
- Create multiplication table

### Exercise 3: Matrix Operations
Implement basic matrix operations (addition, multiplication) using nested lists.

## 8. Summary

**Key takeaways:**
- Lists are ordered, mutable collections
- Use indexing and slicing to access elements
- List methods provide powerful manipulation
- List comprehensions are concise and Pythonic
- Be careful with shallow copies
- Lists are versatile for many use cases

**Next Lecture:** We'll explore tuples.

---

**Quick Reference:**
- List Type: https://docs.python.org/3/library/stdtypes.html#list
- List Methods: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
- List Comprehensions: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions