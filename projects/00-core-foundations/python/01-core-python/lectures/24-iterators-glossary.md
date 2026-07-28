# Python Iterators — Glossary 24

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Iterator | Object with `__iter__` and `__next__` | `iter([1,2,3])` |
| Iterable | Object with `__iter__` method | `[1,2,3]`, `"hello"` |
| Iteration | Process of going through elements | `for x in items:` |
| `next()` | Get next value from iterator | `next(iterator)` |
| `iter()` | Get iterator from iterable | `iter(my_list)` |
| StopIteration | Exception when iterator exhausted | Raised by `next()` |
| Generator | Function using `yield` | `def gen(): yield x` |
| Generator Expression | Concise generator syntax | `(x for x in range(10))` |
| Yield | Keyword to produce generator values | `yield value` |
| Lazy Evaluation | Generate values on demand | Memory-efficient |
| Infinite Iterator | Never-ending iterator | `itertools.count()` |
| Finite Iterator | Iterator with defined end | `iter([1,2,3])` |
| Iterator Protocol | `__iter__` and `__next__` methods | Required for iteration |
| Consumable | Can only iterate once | Generator, iterator |
| Reusable | Can iterate multiple times | List, tuple |
| `itertools` | Advanced iteration utilities | `chain`, `islice`, `cycle` |
| Chain | Combine multiple iterables | `chain(list1, list2)` |
| Islice | Slice an iterator | `islice(iter, start, stop)` |
| Cycle | Infinite repetition | `cycle([1, 2, 3])` |
| Accumulate | Running accumulation | `accumulate([1,2,3])` |
| Compress | Filter by selector | `compress(data, selectors)` |
| Filterfalse | Inverse of filter | `filterfalse(pred, iter)` |
| Starmap | Apply function to unpacked args | `starmap(pow, [(2,3), (3,2)])` |
| Tee | Split iterator into copies | `tee(iter, n)` |
| Zip_longest | Zip with fill value | `zip_longest(a, b, fillvalue=0)` |
| Batch | Group items into chunks | Custom generator |

---

## Definitions

### Accumulate
**Definition**: An `itertools` function that returns an iterator producing accumulated sums (or other binary function results) of the input iterable.

**Example**:
```python
from itertools import accumulate

# Running sum
print(list(accumulate([1, 2, 3, 4, 5])))
# [1, 3, 6, 10, 15]

# Running maximum
from operator import mul
print(list(accumulate([3, 1, 4, 1, 5, 9], max)))
# [3, 3, 4, 4, 5, 9]
```

**Related**: `reduce()`, running total, prefix sum

---

### Chain
**Definition**: An `itertools` function that combines multiple iterables into a single continuous iterator.

**Example**:
```python
from itertools import chain

# Chain lists
combined = chain([1, 2], [3, 4], [5, 6])
print(list(combined))  # [1, 2, 3, 4, 5, 6]

# Chain with string
chars = chain("abc", "def")
print(list(chars))  # ['a', 'b', 'c', 'd', 'e', 'f']
```

**Related**: `itertools`, combining iterables, concatenation

---

### Consumable
**Definition**: An iterator or generator that can only be iterated once. After exhaustion, attempting to iterate again produces no values.

**Example**:
```python
# Generator is consumable
gen = (x for x in range(5))
print(list(gen))  # [0, 1, 2, 3, 4]
print(list(gen))  # [] — empty!

# Convert to list to make reusable
gen = (x for x in range(5))
data = list(gen)
print(list(data))  # [0, 1, 2, 3, 4]
print(list(data))  # [0, 1, 2, 3, 4] — works!
```

**Related**: generator, single-pass, reusability

---

### Cycle
**Definition**: An `itertools` function that creates an infinite iterator repeating elements from the input iterable.

**Example**:
```python
from itertools import cycle

colors = cycle(["red", "green", "blue"])
for _ in range(7):
    print(next(colors))  # red, green, blue, red, green, blue, red
```

**Related**: `repeat()`, infinite iterator, repetition

---

### Generator
**Definition**: A function that returns an iterator using `yield` statements. Produces values lazily, one at a time, maintaining state between calls.

**Example**:
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

**Related**: `yield`, lazy evaluation, iterator, coroutine

---

### Generator Expression
**Definition**: A concise syntax for creating generators using `(expression for item in iterable if condition)`. Similar to list comprehension but with parentheses.

**Example**:
```python
# Generator expression (lazy)
gen = (x**2 for x in range(1000000))

# List comprehension (eager)
lst = [x**2 for x in range(1000000)]

# Generator uses much less memory
import sys
print(sys.getsizeof(gen))   # ~200 bytes
print(sys.getsizeof(lst))   # ~8 MB
```

**Related**: list comprehension, generator, lazy evaluation

---

### Infinite Iterator
**Definition**: An iterator that produces values indefinitely. Must be manually stopped (e.g., with `break` or `islice`).

**Example**:
```python
from itertools import count, cycle, repeat

# count — infinite counter
counter = count(1)
# Use with islice to limit
from itertools import islice
first_5 = list(islice(counter, 5))  # [1, 2, 3, 4, 5]

# cycle — infinite repetition
cycler = cycle([1, 2, 3])
# Same — use islice
```

**Related**: `itertools.count`, `itertools.cycle`, `itertools.repeat`

---

### Islice
**Definition**: An `itertools` function that slices an iterator, similar to list slicing but for any iterable.

**Example**:
```python
from itertools import islice

# First 5 elements
gen = (x for x in range(100))
first_5 = list(islice(gen, 5))  # [0, 1, 2, 3, 4]

# Elements 2-7
data = iter(range(10))
middle = list(islice(data, 2, 7))  # [2, 3, 4, 5, 6]

# Every 2nd element
evens = list(islice(range(20), 0, None, 2))  # [0, 2, 4, ...]
```

**Related**: `itertools`, slicing, limiting iteration

---

### Iterable
**Definition**: Any object that can be iterated over in a for loop. Has an `__iter__()` method that returns an iterator.

**Example**:
```python
# Lists are iterable
for x in [1, 2, 3]:
    print(x)

# Strings are iterable
for c in "hello":
    print(c)

# Check if iterable
def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
```

**Related**: iterator, `__iter__()`, sequence types

---

### Iterator
**Definition**: An object implementing the iterator protocol: `__iter__()` returns itself, `__next__()` returns the next value or raises StopIteration.

**Example**:
```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current

for num in Counter(5):
    print(num)  # 1, 2, 3, 4, 5
```

**Related**: iterable, `__next__()`, StopIteration, protocol

---

### Iterator Protocol
**Definition**: The set of methods (`__iter__` and `__next__`) that an object must implement to be used as an iterator in Python.

**Example**:
```python
# Protocol requirements:
# 1. __iter__() — returns the iterator object itself
# 2. __next__() — returns next value or raises StopIteration

class MyIterator:
    def __iter__(self):  # Required
        return self
    
    def __next__(self):  # Required
        # Return next value or raise StopIteration
        pass
```

**Related**: iterator, `__iter__()`, `__next__()`, duck typing

---

### Lazy Evaluation
**Definition**: A strategy where expressions are evaluated only when their results are needed. Iterators and generators use lazy evaluation to save memory.

**Example**:
```python
# Eager — all values computed at once
eager = [x**2 for x in range(1000000)]  # All 1M values in memory

# Lazy — values computed on demand
lazy = (x**2 for x in range(1000000))  # ~200 bytes

# Value computed only when requested
for val in lazy:
    if val > 100:
        break  # Only computed values up to ~11
```

**Related**: generator, memory efficiency, on-demand computation

---

### Next
**Definition**: A built-in function that retrieves the next value from an iterator. Raises StopIteration when exhausted (unless a default is provided).

**Example**:
```python
my_iter = iter([10, 20, 30])
print(next(my_iter))      # 10
print(next(my_iter))      # 20
print(next(my_iter))      # 30
# next(my_iter)           # StopIteration

# With default (safe)
val = next(my_iter, None)  # None
print(val)
```

**Related**: `iter()`, StopIteration, iterator, default value

---

### Reusable
**Definition**: An iterable that can be iterated over multiple times without being exhausted. Lists, tuples, and strings are reusable.

**Example**:
```python
# List is reusable
my_list = [1, 2, 3]
print(list(my_list))  # [1, 2, 3]
print(list(my_list))  # [1, 2, 3] — works again!

# Generator is NOT reusable
gen = (x for x in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # [] — empty!
```

**Related**: consumable, iterator, generator, single-pass

---

### Repeat
**Definition**: An `itertools` function that creates an iterator that returns the same value indefinitely or a specified number of times.

**Example**:
```python
from itertools import repeat

# Infinite repeat
rep = repeat("hello")
print(next(rep))  # hello
print(next(rep))  # hello

# Limited repeat
rep = repeat("hello", 3)
print(list(rep))  # ['hello', 'hello', 'hello']
```

**Related**: `cycle()`, `count()`, infinite iterator

---

### Starmap
**Definition**: An `itertools` function that applies a function to arguments from an iterable, unpacking each item as function arguments.

**Example**:
```python
from itertools import starmap

# Apply power function
pairs = [(2, 3), (3, 2), (4, 2)]
results = list(starmap(pow, pairs))
print(results)  # [8, 9, 16]
```

**Related**: `map()`, unpacking, function application

---

### StopIteration
**Definition**: An exception raised by an iterator's `__next__()` method when there are no more values to return.

**Example**:
```python
my_iter = iter([1, 2, 3])
next(my_iter)  # 1
next(my_iter)  # 2
next(my_iter)  # 3
# next(my_iter)  # StopIteration raised

# For loops catch this automatically
for x in [1, 2, 3]:
    print(x)  # No exception handling needed
```

**Related**: `next()`, iterator, for loop, exhaustion

---

### Tee
**Definition**: An `itertools` function that splits one iterator into multiple independent iterators.

**Example**:
```python
from itertools import tee

original = iter([1, 2, 3, 4, 5])
iter1, iter2 = tee(original, 2)

print(list(iter1))  # [1, 2, 3, 4, 5]
print(list(iter2))  # [1, 2, 3, 4, 5] — independent copy
```

**Related**: `itertools`, splitting, independent iteration

---

### Yield
**Definition**: A keyword used in generator functions to produce a value and pause execution. Resumes from where it left off on the next call.

**Example**:
```python
def countdown(n):
    while n > 0:
        yield n  # Produce value and pause
        n -= 1

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

**Related**: generator, coroutine, state preservation

---

### Zip Longest
**Definition**: An `itertools` function that combines iterables like `zip()`, but continues until the longest iterable is exhausted, filling missing values with a specified fillvalue.

**Example**:
```python
from itertools import zip_longest

a = [1, 2, 3]
b = [10, 20]
for x, y in zip_longest(a, b, fillvalue=0):
    print(f"{x}, {y}")
# 1, 10
# 2, 20
# 3, 0
```

**Related**: `zip()`, fill value, padding

---

## Code Examples

### Example 1: Custom Iterator for File Processing
```python
class LineReader:
    """Read file lines lazily."""
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __iter__(self):
        self.file = open(self.filename, 'r')
        return self
    
    def __next__(self):
        line = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration
        return line.strip()
```

### Example 2: Infinite Fibonacci
```python
def fibonacci():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10
from itertools import islice
fib = fibonacci()
first_10 = list(islice(fib, 10))
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## Related Concepts

- **List Comprehension**: Eager evaluation vs. lazy
- **itertools**: Advanced iteration tools
- **Coroutines**: Generators with `send()`
- **Async Iteration**: `async for` and `__aiter__`
- **Context Managers**: `with` statement and `__enter__`/`__exit__`
