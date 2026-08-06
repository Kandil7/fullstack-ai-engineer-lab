# Python For Loops — Glossary 20

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| For Loop | Iterates over an iterable | `for x in items:` |
| Iterable | Object that can be iterated over | list, tuple, str, range, dict |
| Iterator | Object with `__next__()` method | `iter(my_list)` |
| Range | Generates numeric sequence | `range(5)`, `range(1, 10, 2)` |
| Enumerate | Adds counter to iterable | `enumerate(items, start=1)` |
| Zip | Parallel iteration over iterables | `zip(list1, list2)` |
| Break | Exits the loop immediately | `break` |
| Continue | Skips to next iteration | `continue` |
| Else | Runs when loop completes normally | `for...else:` |
| List Comprehension | Concise loop alternative | `[x for x in items]` |
| Unpacking | Extracting values from iterable | `for a, b in pairs:` |
| Nested Loop | Loop inside another loop | `for...for...` |
| StopIteration | Exception signaling iterator end | Raised by `next()` |
| Iterable Protocol | `__iter__()` and `__next__()` | Iterator interface |
| For-Else | Else clause with for loop | `for x in...else:` |
| Loop Target | Variable receiving each element | `for item in list:` |
| Generator | Lazy iterator with `yield` | `def gen(): yield x` |
| Star Unpacking | Capture remaining items | `for first, *rest:` |
| Dict Items | View of key-value pairs | `.items()` |
| Dict Keys | View of dictionary keys | `.keys()` |
| Dict Values | View of dictionary values | `.values()` |

---

## Definitions

### Break
**Definition**: A statement that immediately exits the innermost for loop. Code after the loop (or the else clause) continues execution.

**Example**:
```python
for num in range(100):
    if num == 5:
        print(f"Found 5!")
        break
    print(num)
# Prints 0, 1, 2, 3, 4, then "Found 5!"
```

**Related**: `continue`, loop control, `else` clause

---

### Continue
**Definition**: A statement that skips the remaining code in the current iteration and moves to the next element.

**Example**:
```python
for num in range(10):
    if num % 2 == 0:
        continue
    print(num)
# Prints: 1, 3, 5, 7, 9 (skips even numbers)
```

**Related**: `break`, iteration, skip

---

### Dict Items
**Definition**: A method returning a view object of a dictionary's key-value pairs as tuples, used for iterating over both keys and values.

**Example**:
```python
person = {"name": "Alice", "age": 30}
for key, value in person.items():
    print(f"{key}: {value}")

# Convert to list of tuples
pairs = list(person.items())
print(pairs)  # [('name', 'Alice'), ('age', 30)]
```

**Related**: `keys()`, `values()`, dictionary iteration

---

### Dict Keys
**Definition**: A method returning a view object of all dictionary keys, commonly used for iteration.

**Example**:
```python
d = {"a": 1, "b": 2, "c": 3}
for key in d.keys():  # or just: for key in d:
    print(key)
```

**Related**: `values()`, `items()`, dictionary

---

### Dict Values
**Definition**: A method returning a view object of all dictionary values.

**Example**:
```python
d = {"a": 1, "b": 2, "c": 3}
for value in d.values():
    print(value)  # 1, 2, 3
```

**Related**: `keys()`, `items()`, dictionary

---

### Else
**Definition**: An optional clause on a for loop that executes when the loop completes all iterations without hitting a `break`.

**Example**:
```python
# Search with for-else
primes = [2, 3, 5, 7, 11]
for p in primes:
    if p == 4:
        print("Found 4!")
        break
else:
    print("4 not found!")  # Printed

for p in primes:
    if p == 5:
        print("Found 5!")
        break
else:
    print("5 not found!")  # NOT printed
```

**Related**: `break`, search pattern, loop completion

---

### For Loop
**Definition**: A control flow statement that iterates over each element in an iterable object, executing the loop body once per element.

**Example**:
```python
# For loop over list
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)

# For loop with range
for i in range(5):
    print(i)
```

**Related**: iterable, iterator, `range()`, loop body

---

### For-Else
**Definition**: A for loop with an optional else clause that runs when the loop exhausts all items without a break. Useful for search patterns.

**Example**:
```python
def find_in_list(items, target):
    for item in items:
        if item == target:
            return True
    else:
        return False  # Loop completed without finding target

print(find_in_list([1, 2, 3], 2))  # True
print(find_in_list([1, 2, 3], 5))  # False
```

**Related**: `break`, search, `else` clause

---

### Generator
**Definition**: A function that returns an iterator using `yield` instead of `return`. Produces values lazily, one at a time, saving memory for large sequences.

**Example**:
```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

**Related**: iterator, `yield`, lazy evaluation, memory efficiency

---

### Iterable Protocol
**Definition**: The Python protocol that defines how objects can be iterated. Requires an `__iter__()` method that returns an iterator.

**Example**:
```python
# Any object with __iter__() is iterable
class Counter:
    def __init__(self, max_val):
        self.max_val = max_val
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max_val:
            raise StopIteration
        self.current += 1
        return self.current

for num in Counter(5):
    print(num)  # 1, 2, 3, 4, 5
```

**Related**: `__iter__()`, `__next__()`, iterator, StopIteration

---

### Iterable
**Definition**: Any object that can be iterated over in a for loop. Includes lists, tuples, strings, dictionaries, sets, ranges, and generators.

**Example**:
```python
# Lists are iterable
for item in [1, 2, 3]:
    print(item)

# Strings are iterable
for char in "hello":
    print(char)

# Ranges are iterable
for i in range(5):
    print(i)
```

**Related**: iterator, `__iter__()`, sequence types

---

### Iterator
**Definition**: An object that implements the iterator protocol: `__iter__()` returns itself, and `__next__()` returns the next value or raises `StopIteration`.

**Example**:
```python
my_list = [1, 2, 3]
my_iter = iter(my_list)  # Get iterator

print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3
# next(my_iter)  # StopIteration
```

**Related**: `iter()`, `next()`, StopIteration, iterable

---

### List Comprehension
**Definition**: A concise syntax for creating lists using the pattern `[expression for item in iterable if condition]`. Equivalent to a for loop that builds a list.

**Example**:
```python
# For loop approach
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension (concise)
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
```

**Related**: dict comprehension, set comprehension, generator expression

---

### Loop Target
**Definition**: The variable that receives each element from the iterable during each iteration of the for loop.

**Example**:
```python
# 'fruit' is the loop target
for fruit in ["apple", "banana"]:
    print(fruit)

# Multiple targets (unpacking)
for x, y in [(1, 2), (3, 4)]:
    print(f"{x}, {y}")
```

**Related**: loop variable, unpacking, iteration

---

### Nested Loop
**Definition**: A for loop placed inside another for loop. The inner loop completes all iterations for each iteration of the outer loop.

**Example**:
```python
# 2D matrix traversal
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for cell in row:
        print(cell, end=" ")
    print()
```

**Related**: loops, 2D iteration, matrix

---

### Range
**Definition**: A built-in function that generates a sequence of numbers. Returns a range object that is memory-efficient for iteration.

**Example**:
```python
range(5)       # 0, 1, 2, 3, 4
range(1, 6)    # 1, 2, 3, 4, 5
range(0, 10, 2)# 0, 2, 4, 6, 8
range(5, 0, -1)# 5, 4, 3, 2, 1
```

**Related**: for loop, numeric sequence, indexing

---

### Star Unpacking
**Definition**: Using `*` in a for loop target to capture remaining elements of a sequence into a list.

**Example**:
```python
# Capture first and rest
items = [1, 2, 3, 4, 5]
first, *rest = items
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

# In for loop
for first, *middle, last in [[1, 2, 3], [4, 5, 6]]:
    print(f"First: {first}, Middle: {middle}, Last: {last}")
```

**Related**: unpacking, *args, sequence destructuring

---

### StopIteration
**Definition**: An exception raised by an iterator's `__next__()` method when there are no more elements to return. Signals the end of iteration.

**Example**:
```python
my_iter = iter([1, 2, 3])
print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3
# next(my_iter)  # Raises StopIteration

# For loops handle this automatically
for x in [1, 2, 3]:
    print(x)  # No StopIteration needed
```

**Related**: iterator, `next()`, iterable protocol

---

### Unpacking
**Definition**: Assigning multiple variables from an iterable in a single statement. Used in for loops to destructure tuples or lists.

**Example**:
```python
# Tuple unpacking
pairs = [(1, "a"), (2, "b"), (3, "c")]
for num, letter in pairs:
    print(f"{num}: {letter}")

# Nested unpacking
data = [(1, (2, 3)), (4, (5, 6))]
for a, (b, c) in data:
    print(f"{a}, {b}, {c}")
```

**Related**: tuple, multiple assignment, loop target

---

### Zip
**Definition**: A built-in function that iterates over multiple iterables in parallel, stopping at the shortest one. Returns tuples of corresponding elements.

**Example**:
```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# With dict
gradebook = dict(zip(names, scores))
print(gradebook)  # {'Alice': 85, 'Bob': 92, 'Charlie': 78}
```

**Related**: `enumerate()`, parallel iteration, dictionary creation

---

## Code Examples

### Example 1: Find Common Elements
```python
def common_elements(list1, list2):
    result = []
    for item in list1:
        if item in list2 and item not in result:
            result.append(item)
    return result

print(common_elements([1, 2, 3, 4], [3, 4, 5, 6]))  # [3, 4]
```

### Example 2: Matrix Operations
```python
def add_matrices(a, b):
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j] + b[i][j])
        result.append(row)
    return result

a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
print(add_matrices(a, b))  # [[6, 8], [10, 12]]
```

---

## Related Concepts

- **While Loops**: When iteration count is unknown
- **Itertools**: Advanced iteration tools (`chain`, `product`, `combinations`)
- **Generator Expressions**: `(x for x in range(10))` — lazy version
- **Async For**: `async for` for asynchronous iteration
- **Comprehensions**: Concise loop alternatives
