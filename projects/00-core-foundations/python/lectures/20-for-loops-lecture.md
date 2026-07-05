# Python For Loops — Lecture 20

## Topic Overview

A **for loop** iterates over a sequence (list, tuple, string, range, dictionary, or any iterable) and executes a block of code for each element. Unlike while loops, for loops are ideal when you know **how many times** to iterate or when you want to process each item in a collection.

Python's for loop uses the **iterator protocol** — it calls `__iter__()` on the object and repeatedly calls `__next__()` until `StopIteration` is raised.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Write for loops over different iterables
- Use `range()` for numeric sequences
- Use `enumerate()` for index-element pairs
- Use `zip()` to iterate multiple sequences in parallel
- Implement nested for loops
- Use break, continue, and else with for loops
- Understand list comprehensions as concise for loops
- Apply for loops to real-world scenarios

---

## Key Concepts

### 1. Basic For Loop

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

### 2. For Loop with Range

```python
# range(stop) — 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) — start to stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step) — with increment
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### 3. Iterating Over Strings

```python
# Strings are iterable — each character is an element
for char in "Python":
    print(char, end=" ")
# P y t h o n
```

### 4. Iterating Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Iterate over keys (default)
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### 5. Enumerate — Index and Value

```python
fruits = ["apple", "banana", "cherry"]

# Without enumerate (manual index)
i = 0
for fruit in fruits:
    print(f"{i}: {fruit}")
    i += 1

# With enumerate (Pythonic!)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Custom start index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
```

### 6. Zip — Parallel Iteration

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
grades = ["B", "A", "C"]

# Iterate over multiple sequences
for name, score, grade in zip(names, scores, grades):
    print(f"{name}: {score} ({grade})")

# Zip stops at shortest sequence
a = [1, 2, 3]
b = [10, 20]
for x, y in zip(a, b):
    print(f"{x} + {y}")
# 1 + 10
# 2 + 20
# (3 is skipped)
```

### 7. Break, Continue, and Else

```python
# Break — exit loop early
for num in range(10):
    if num == 5:
        break
    print(num)  # 0, 1, 2, 3, 4

# Continue — skip current iteration
for num in range(10):
    if num % 2 == 0:
        continue
    print(num)  # 1, 3, 5, 7, 9

# Else — runs when loop completes normally (no break)
for num in range(5):
    print(num)
else:
    print("Loop completed!")  # Printed

# With break — else not executed
for num in range(5):
    if num == 3:
        break
    print(num)
else:
    print("Completed!")  # NOT printed
```

### 8. Nested For Loops

```python
# Multiplication table
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4d}", end="")
    print()

# Output:
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25
```

### 9. For-Else Pattern

```python
# Search with for-else
def find_item(items, target):
    for item in items:
        if item == target:
            print(f"Found {target}!")
            break
    else:
        print(f"{target} not found")

find_item([1, 2, 3, 4], 3)  # Found 3!
find_item([1, 2, 3, 4], 5)  # 5 not found
```

### 10. Unpacking in For Loops

```python
# Unpack tuples
points = [(0, 0), (1, 2), (3, 4)]
for x, y in points:
    print(f"({x}, {y})")

# Unpack nested structures
data = [
    {"name": "Alice", "scores": [85, 90]},
    {"name": "Bob", "scores": [78, 82]}
]
for person in data:
    name = person["name"]
    avg = sum(person["scores"]) / len(person["scores"])
    print(f"{name}: {avg:.1f}")
```

---

## Code Examples

### Example 1: Find Largest Element

```python
def find_largest(numbers):
    if not numbers:
        return None
    
    largest = numbers[0]
    for num in numbers[1:]:
        if num > largest:
            largest = num
    return largest

print(find_largest([3, 1, 4, 1, 5, 9, 2, 6]))  # 9
```

### Example 2: Matrix Transpose

```python
def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(matrix[i][j])
        result.append(new_row)
    
    return result

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
print(transpose(matrix))
# [[1, 4], [2, 5], [3, 6]]
```

### Example 3: Flatten Nested List

```python
def flatten(nested_list):
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat

print(flatten([1, [2, 3], [4, [5, 6]]]))  # [1, 2, 3, 4, 5, 6]
```

### Example 4: Word Frequency Counter

```python
def word_freq(text):
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

text = "the cat sat on the mat the cat ate the rat"
result = word_freq(text)
# {'the': 4, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1, 'ate': 1, 'rat': 1}
```

---

## Common Mistakes to Avoid

### Mistake 1: Modifying List During Iteration
```python
# WRONG
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Skips elements!

# CORRECT — iterate over copy or use list comprehension
items = [1, 2, 3, 4, 5]
items = [item for item in items if item % 2 != 0]
```

### Mistake 2: Using Range with List Length
```python
# WRONG — using range unnecessarily
for i in range(len(my_list)):
    item = my_list[i]

# CORRECT — iterate directly
for item in my_list:
    process(item)
```

### Mistake 3: Shadowing Built-in Names
```python
# WRONG — shadowing built-in `list`
list = [1, 2, 3]
for list in items:  # Now 'list' is the loop variable!
    print(list)

# CORRECT — use descriptive names
my_list = [1, 2, 3]
for item in my_list:
    print(item)
```

### Mistake 4: Not Using Enumerate
```python
# WRONG — manual index management
i = 0
for item in items:
    print(f"{i}: {item}")
    i += 1

# CORRECT — use enumerate
for i, item in enumerate(items):
    print(f"{i}: {item}")
```

---

## Best Practices

1. **Iterate directly** over collections, not indices
2. **Use `enumerate()`** when you need both index and value
3. **Use `zip()`** for parallel iteration
4. **Use `for-else`** for search patterns
5. **Prefer list comprehensions** for simple transformations
6. **Avoid shadowing** built-in names like `list`, `dict`, `type`
7. **Use `_` for unused loop variables**: `for _ in range(5):`
8. **Use meaningful variable names** for loop targets

---

## Practice Exercises

### Exercise 1: Sum of Digits
Write a function that sums the digits of a number using a for loop.

```python
def sum_digits(n):
    # Your code here
    pass

# Expected: 15 (1 + 2 + 3 + 4 + 5)
print(sum_digits(12345))
```

### Exercise 2: Palindrome Checker
Write a function that checks if a string is a palindrome using a for loop.

```python
def is_palindrome(s):
    # Your code here
    pass

# Expected: True
print(is_palindrome("racecar"))
print(is_palindrome("hello"))
```

### Exercise 3: Matrix Multiplication
Write a function that multiplies two 2x2 matrices.

```python
def multiply_matrices(a, b):
    # Your code here — nested for loops
    pass

a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
# Expected: [[19, 22], [43, 50]]
print(multiply_matrices(a, b))
```

### Exercise 4: Caesar Cipher
Write a function that encrypts a string using Caesar cipher (shift letters by n positions).

```python
def caesar_encrypt(text, shift):
    # Your code here
    pass

# Expected: "Khoor"
print(caesar_encrypt("Hello", 3))
```

---

## Summary

- **For loops** iterate over sequences: lists, tuples, strings, ranges, dicts
- **`range()`** generates numeric sequences
- **`enumerate()`** provides index-value pairs
- **`zip()`** enables parallel iteration over multiple sequences
- **Break** exits the loop; **continue** skips to next iteration
- **Else** runs when loop completes without break
- **Nested for loops** for 2D iteration
- **List comprehensions** are concise for loop alternatives
- **For-else** pattern for search algorithms
