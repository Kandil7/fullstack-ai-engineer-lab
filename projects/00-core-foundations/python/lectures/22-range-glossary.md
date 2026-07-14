# Python Range Function — Glossary 22

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Range | Generates numeric sequence | `range(5)`, `range(1, 10, 2)` |
| Range Object | Memory-efficient sequence type | `r = range(1000000)` |
| Start | First value (inclusive) | `range(2, 10)` starts at 2 |
| Stop | End value (exclusive) | `range(0, 5)` stops at 4 |
| Step | Increment between values | `range(0, 10, 2)` steps by 2 |
| Negative Step | Decrementing sequence | `range(5, 0, -1)` |
| Slice | Extracting range from sequence | `list[::2]` (every 2nd) |
| List Comprehension | Concise list creation with range | `[x**2 for x in range(10)]` |
| Dict Comprehension | Dict creation with range | `{x: x**2 for x in range(5)}` |
| Set Comprehension | Set creation with range | `{x for x in range(10)}` |
| Generator Expression | Lazy iteration with range | `sum(x for x in range(100))` |
| Index | Position in a sequence | `for i in range(len(list))` |
| Repeat | Execute N times | `for _ in range(5):` |
| Modular Arithmetic | Wrapping with `%` | `range(0, 10)` mod 2 |
| Sequence | Ordered collection | list, tuple, range, string |
| Iterator | Object with `__next__()` | `iter(range(5))` |
| Memory Efficient | Low memory usage | `range(1_000_000)` |
| Exclusive Stop | Stop value not included | `range(5)` → 0,1,2,3,4 |
| Inclusive Start | Start value included | `range(2,5)` → 2,3,4 |
| Step Size | Increment value | `range(0,10,3)` → 0,3,6,9 |
| Zero-based | Starts from 0 | `range(5)` → 0-4 |
| Arithmetic Sequence | Equal spacing between values | 0, 2, 4, 6, 8 |
| Linear Interpolation | Evenly spaced values | `range(start, stop, step)` |
| Sieve | Prime finding algorithm | Sieve of Eratosthenes |

---

## Definitions

### Arithmetic Sequence
**Definition**: A sequence of numbers where the difference between consecutive terms is constant. Range generates arithmetic sequences.

**Example**:
```python
# Arithmetic sequence: 0, 3, 6, 9, 12 (common difference: 3)
seq = list(range(0, 15, 3))
print(seq)  # [0, 3, 6, 9, 12]
```

**Related**: range, step, common difference

---

### Dict Comprehension
**Definition**: A concise syntax for creating dictionaries using `{key: value for item in iterable}`. Often uses range for numeric keys.

**Example**:
```python
# Create mapping of numbers to their squares
squares = {x: x**2 for x in range(10)}
print(squares)  # {0: 0, 1: 1, 2: 4, ...}

# Create mapping with condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

**Related**: list comprehension, set comprehension, range

---

### Exclusive Stop
**Definition**: The stop value in range is not included in the generated sequence. `range(5)` generates 0, 1, 2, 3, 4 (not 5).

**Example**:
```python
# Stop value 5 is NOT included
print(list(range(5)))       # [0, 1, 2, 3, 4]
print(list(range(1, 6)))    # [1, 2, 3, 4, 5]
print(list(range(0, 10, 3)))# [0, 3, 6, 9]
```

**Related**: inclusive start, off-by-one, stop parameter

---

### Generator Expression
**Definition**: A lazy iterator that generates values on demand using `(expression for item in iterable)`. More memory-efficient than list comprehensions for large sequences.

**Example**:
```python
# Sum of squares from 0 to 999999 (memory efficient)
total = sum(x**2 for x in range(1_000_000))
print(total)

# Create generator object
gen = (x**2 for x in range(10))
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 4
```

**Related**: generator, lazy evaluation, memory efficiency, range

---

### Inclusive Start
**Definition**: The start value in range is included in the generated sequence. `range(2, 5)` starts at 2.

**Example**:
```python
# Start value 2 IS included
print(list(range(2, 6)))    # [2, 3, 4, 5]
print(list(range(10, 0, -1)))# [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

**Related**: exclusive stop, start parameter

---

### Index
**Definition**: The position of an element in a sequence. Range is commonly used to generate indices for loop iteration.

**Example**:
```python
items = ["a", "b", "c", "d", "e"]

# Using range for indices
for i in range(len(items)):
    print(f"Index {i}: {items[i]}")

# Better: use enumerate
for i, item in enumerate(items):
    print(f"Index {i}: {item}")
```

**Related**: enumeration, zero-based indexing, range

---

### Iterator
**Definition**: An object with `__iter__()` and `__next__()` methods. Range objects can be converted to iterators for manual iteration.

**Example**:
```python
r = range(5)
it = iter(r)

print(next(it))  # 0
print(next(it))  # 1
print(next(it))  # 2
# StopIteration when exhausted
```

**Related**: `iter()`, `next()`, StopIteration, iterable

---

### Linear Interpolation
**Definition**: Generating evenly spaced values between two points. Range with float step can be used for this.

**Example**:
```python
# 5 evenly spaced values between 0 and 1
start, end, steps = 0, 1, 5
values = [start + i * (end - start) / (steps - 1) for i in range(steps)]
print(values)  # [0.0, 0.25, 0.5, 0.75, 1.0]
```

**Related**: linspace (NumPy), range, even spacing

---

### List Comprehension
**Definition**: A concise syntax for creating lists using `[expression for item in iterable]`. Very commonly used with range.

**Example**:
```python
# Squares
squares = [x**2 for x in range(10)]

# Even numbers
evens = [x for x in range(20) if x % 2 == 0]

# Matrix rows
matrix = [[j for j in range(3)] for i in range(3)]
```

**Related**: dict comprehension, set comprehension, range

---

### Memory Efficient
**Definition**: Range objects store only start, stop, and step values rather than all generated numbers, making them very memory-efficient even for large sequences.

**Example**:
```python
# Range object — very small memory
r = range(1_000_000)
import sys
print(sys.getsizeof(r))  # ~48 bytes

# List — stores all values
l = list(range(1_000_000))
print(sys.getsizeof(l))  # ~8 MB
```

**Related**: lazy evaluation, generator, range object

---

### Modular Arithmetic
**Definition**: Arithmetic where numbers "wrap around" after reaching a certain value. Often combined with range for cyclical patterns.

**Example**:
```python
# Day of week cycling
for day_num in range(7):
    day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day_num]
    print(day)

# Wrap around with modulo
for i in range(10):
    print(f"{i} mod 3 = {i % 3}")
```

**Related**: modulo operator, cyclical, range

---

### Negative Step
**Definition**: A step value less than zero that generates a decreasing sequence. Used for counting backwards.

**Example**:
```python
# Countdown
print(list(range(5, 0, -1)))  # [5, 4, 3, 2, 1]

# Even numbers descending
print(list(range(10, 0, -2)))  # [10, 8, 6, 4, 2]
```

**Related**: step, countdown, reverse iteration

---

### Range
**Definition**: A built-in Python function that returns a range object representing an arithmetic sequence of integers. Used for numeric iteration.

**Example**:
```python
range(stop)          # 0 to stop-1
range(start, stop)   # start to stop-1
range(start, stop, step)  # with custom increment
```

**Related**: for loop, sequence, iterable, memory efficient

---

### Range Object
**Definition**: The object returned by `range()`. Stores only start, stop, and step values, generating numbers on demand.

**Example**:
```python
r = range(0, 100, 5)
print(type(r))  # <class 'range'>
print(len(r))   # 20
print(25 in r)  # True
print(r.start)  # 0
print(r.stop)   # 100
print(r.step)   # 5
```

**Related**: range, iterator, memory efficient

---

### Repeat
**Definition**: Using range to execute a block of code a specific number of times, typically with `_` as the unused loop variable.

**Example**:
```python
# Repeat 5 times
for _ in range(5):
    print("Hello!")

# Repeat with delay
import time
for i in range(3):
    print(f"Attempt {i + 1}")
    time.sleep(1)
```

**Related**: for loop, underscore variable, iteration

---

### Sequence
**Definition**: An ordered collection of elements that supports indexing, iteration, and membership testing. Range generates integer sequences.

**Example**:
```python
# Range is a sequence type
r = range(5)
print(3 in r)     # True
print(r[2])       # 2
print(len(r))     # 5

# Other sequence types
my_list = [1, 2, 3]  # List
my_tuple = (1, 2, 3)  # Tuple
my_str = "abc"  # String
```

**Related**: list, tuple, string, range, iterable

---

### Set Comprehension
**Definition**: A concise syntax for creating sets using `{expression for item in iterable}`. Used with range to create sets of numbers.

**Example**:
```python
# Set of squares (removes duplicates)
squares = {x**2 for x in range(-5, 6)}
print(squares)  # {0, 1, 4, 9, 16, 25}

# Set of remainders
remainders = {x % 3 for x in range(10)}
print(remainders)  # {0, 1, 2}
```

**Related**: list comprehension, dict comprehension, range

---

### Sieve
**Definition**: An algorithm for finding all prime numbers up to a given limit, commonly implemented using range for iteration.

**Example**:
```python
def sieve(limit):
    """Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(limit + 1) if is_prime[i]]

print(sieve(30))  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

**Related**: primes, algorithm, range, iteration

---

### Slice
**Definition**: Extracting a portion of a sequence using `sequence[start:stop:step]`. Similar to range parameters but applied to existing sequences.

**Example**:
```python
# Slicing a list
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(my_list[::2])   # [0, 2, 4, 6, 8] — every 2nd
print(my_list[1::2])  # [1, 3, 5, 7, 9] — every 2nd starting at 1
print(my_list[::-1])  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] — reversed

# Slicing a string
text = "Hello, World!"
print(text[::2])  # "Hlo ol!"
```

**Related**: range, step, start, stop, indexing

---

### Step
**Definition**: The increment (or decrement if negative) between consecutive values in a range. Default is 1.

**Example**:
```python
# Step of 2
print(list(range(0, 10, 2)))  # [0, 2, 4, 6, 8]

# Step of 3
print(list(range(0, 10, 3)))  # [0, 3, 6, 9]

# Negative step
print(list(range(10, 0, -3)))  # [10, 7, 4, 1]
```

**Related**: start, stop, increment, decrement

---

### Zero-based
**Definition**: Indexing that starts from 0. Python's range starts from 0 by default: `range(n)` generates 0, 1, ..., n-1.

**Example**:
```python
# Zero-based range
print(list(range(5)))  # [0, 1, 2, 3, 4]

# To start from 1
print(list(range(1, 6)))  # [1, 2, 3, 4, 5]
```

**Related**: indexing, off-by-one, start parameter

---

## Code Examples

### Example 1: Generate All Permutations
```python
from itertools import permutations

# Generate permutations using range
nums = list(range(1, 4))
for perm in permutations(nums):
    print(perm)  # (1,2,3), (1,3,2), (2,1,3), ...
```

### Example 2: Matrix Creation
```python
# Create 3x3 identity matrix
identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
print(identity)  # [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
```

---

## Related Concepts

- **NumPy arange**: Similar to range but for floats
- **itertools.count**: Infinite range-like iterator
- **itertools.islice**: Slicing for iterators
- **Generators**: Lazy sequences with yield
- **Comprehensions**: Concise iteration syntax
