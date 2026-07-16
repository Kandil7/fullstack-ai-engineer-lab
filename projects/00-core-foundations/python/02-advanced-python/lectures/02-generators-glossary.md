# Generators and Iterators Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Iterator | Object with `__iter__` and `__next__` methods |
| Iterable | Object that can return an iterator via `__iter__` |
| Generator | Function using `yield` to produce values lazily |
| Generator Expression | Concise `(expr for x in iter)` syntax |
| `yield` | Keyword that produces a value and suspends execution |
| `yield from` | Delegates to a sub-generator |
| `send()` | Sends a value into a generator |
| `throw()` | Raises an exception inside a generator |
| `close()` | Closes a generator, triggering cleanup |
| `StopIteration` | Exception signaling end of iteration |
| Lazy Evaluation | Computing values only when needed |
| Iterator Protocol | The `__iter__`/`__next__` interface |
| Generator Iterator | The iterator object returned by a generator function |
| Coroutine | Generator enhanced with `send()` for bidirectional communication |
| Infinite Sequence | Generator that never raises `StopIteration` |
| Pipeline | Chain of generators for data processing |
| `itertools` | Module with iterator building blocks |
| `itertools.islice` | Slices an iterator without converting to list |
| `itertools.tee` | Creates independent iterators from one source |
| Memory-Efficient | Processing data one item at a time |

---

## Detailed Definitions

### Closed Generator

**Definition**: A generator that has been terminated by calling `close()`, exhausting it, or encountering an unhandled exception. Once closed, it cannot produce more values.

**Example**:
```python
def my_generator():
    try:
        while True:
            yield "data"
    finally:
        print("Cleanup executed")

gen = my_generator()
next(gen)      # "data"
gen.close()    # "Cleanup executed"

# Cannot use gen anymore
try:
    next(gen)
except StopIteration:
    pass  # Generator is exhausted
```

**Related**: `close()`, `finally`, Generator Lifecycle

---

### Coroutine

**Definition**: A generator enhanced with `send()` to accept values, enabling bidirectional communication. Used for producer-consumer patterns and async-like behavior.

**Example**:
```python
def average():
    """Coroutine that computes running average."""
    total = 0.0
    count = 0
    average = None
    
    while True:
        value = yield average
        if value is None:
            break
        total += value
        count += 1
        average = total / count

avg = average()
next(avg)            # Initialize: None
avg.send(10)         # -> 10.0
avg.send(20)         # -> 15.0
avg.send(30)         # -> 20.0
```

**Related**: `send()`, Generator, Bidirectional Communication

---

### `for` Loop Iteration

**Definition**: The mechanism by which Python iterates over an iterable, automatically calling `__iter__()` to get an iterator and `__next__()` to get each value, catching `StopIteration` to end.

**Example**:
```python
# What Python does internally:
for item in iterable:
    process(item)

# Equivalent to:
iterator = iter(iterable)
while True:
    try:
        item = next(iterator)
        process(item)
    except StopIteration:
        break
```

**Related**: Iterator Protocol, `__iter__`, `__next__`, `StopIteration`

---

### Generator Expression

**Definition**: A concise expression syntax for creating generators, similar to list comprehensions but using parentheses `()` instead of brackets `[]`. Produces values lazily.

**Example**:
```python
# List comprehension (eager - all values in memory)
squares_list = [x ** 2 for x in range(1000000)]

# Generator expression (lazy - one value at a time)
squares_gen = (x ** 2 for x in range(1000000))

# Using in function calls (parentheses optional)
total = sum(x ** 2 for x in range(100))
max_val = max(x ** 2 for x in range(100))

# Complex expressions
processed = (x.strip().lower() for x in data if x.strip())
```

**Related**: List Comprehension, Lazy Evaluation, Memory Efficiency

---

### Generator Function

**Definition**: A function containing one or more `yield` keywords. When called, it returns a generator iterator without executing the function body. Execution resumes each time `next()` is called.

**Example**:
```python
def countdown(n):
    """Generator function using yield."""
    print("Starting countdown")
    while n > 0:
        yield n
        n -= 1
    print("Done!")

# Calling returns generator iterator (no code runs yet)
gen = countdown(3)

# Each next() resumes execution
next(gen)  # "Starting countdown" -> 3
next(gen)  # 2
next(gen)  # 1
# next(gen) # "Done!" -> StopIteration
```

**Related**: `yield`, Generator Iterator, Lazy Evaluation

---

### Generator Iterator

**Definition**: The iterator object returned by calling a generator function. It implements the iterator protocol (`__iter__` returns self, `__next__` resumes execution to next `yield`).

**Example**:
```python
def make_gen():
    yield 1
    yield 2

gen_iter = make_gen()  # This IS the generator iterator
print(type(gen_iter))  # <class 'generator'>

# It's also an iterator
print(iter(gen_iter) is gen_iter)  # True
print(next(gen_iter))  # 1
print(next(gen_iter))  # 2
```

**Related**: Generator Function, Iterator Protocol

---

### Infinite Sequence

**Definition**: A generator that produces values indefinitely without raising `StopIteration`. Must be consumed with care (using `islice`, `take`, or conditionals).

**Example**:
```python
def fibonacci():
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice

# Take first 10 values
first_10 = list(islice(fibonacci(), 10))
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Take values until condition
def take_until(gen, condition):
    for value in gen:
        if not condition(value):
            return
        yield value

under_100 = list(take_until(fibonacci(), lambda x: x < 100))
print(under_100)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

**Related**: `islice`, `take_until`, Lazy Evaluation

---

### Iterable

**Definition**: Any object that can return an iterator via its `__iter__()` method. Includes lists, tuples, strings, dicts, sets, generators, and file objects.

**Example**:
```python
class MyIterable:
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        return iter(self.data)

my_list = MyIterable([1, 2, 3])
for item in my_list:
    print(item)  # 1, 2, 3

# Built-in iterables
for char in "hello":      # str
    print(char)

for key in {"a": 1}:     # dict
    print(key)
```

**Related**: Iterator, `__iter__`, `for` Loop

---

### Iterator

**Definition**: An object implementing both `__iter__()` (returns self) and `__next__()` (returns next value or raises `StopIteration`). Supports one-pass sequential access.

**Example**:
```python
class Counter:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

counter = Counter(1, 5)
print(list(counter))  # [1, 2, 3, 4]
print(list(counter))  # [] — exhausted!
```

**Related**: Iterator Protocol, `__iter__`, `__next__`, `StopIteration`

---

### Iterator Protocol

**Definition**: The Python interface requiring `__iter__()` (returns the iterator) and `__next__()` (returns next value or raises `StopIteration`). Any object implementing this protocol can be used in `for` loops.

**Example**:
```python
class Fibonacci:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value

# Works with for loop, list(), next(), etc.
fib = Fibonacci(5)
print(list(fib))  # [0, 1, 1, 2, 3]
```

**Related**: Iterator, `__iter__`, `__next__`, `StopIteration`

---

### `itertools.islice`

**Definition**: A function from `itertools` that slices an iterator by index, returning an iterator of selected elements. Unlike list slicing, it doesn't require creating the full list.

**Example**:
```python
from itertools import islice

def infinite_count(start=0):
    while True:
        yield start
        start += 1

# Take first 5 from infinite generator
first_5 = list(islice(infinite_count(), 5))
print(first_5)  # [0, 1, 2, 3, 4]

# Slice from index 2 to 5
sliced = list(islice(infinite_count(10), 2, 5))
print(sliced)  # [12, 13, 14]

# With step
stepped = list(islice(infinite_count(), 0, 20, 3))
print(stepped)  # [0, 3, 6, 9, 12, 15, 18]
```

**Related**: `itertools`, Slicing, Infinite Sequences

---

### `itertools.tee`

**Definition**: Creates multiple independent iterators from a single iterator, allowing multiple passes over the same data without re-executing the source.

**Example**:
```python
from itertools import tee

def expensive_generator():
    print("Generating...")
    for i in range(5):
        yield i * 2

# Without tee: second pass gets empty generator
gen = expensive_generator()
first_pass = list(gen)   # "Generating..." -> [0, 2, 4, 6, 8]
second_pass = list(gen)  # [] — exhausted

# With tee: independent iterators
gen1, gen2 = tee(expensive_generator())
first_pass = list(gen1)   # "Generating..." -> [0, 2, 4, 6, 8]
second_pass = list(gen2)  # [0, 2, 4, 6, 8] — same data
```

**Related**: `itertools`, Iterator Copying, Memory Warning

---

### Lazy Evaluation

**Definition**: A strategy where expressions are evaluated only when their values are needed. Generators implement lazy evaluation by producing one value at a time.

**Example**:
```python
# Eager: all values computed immediately
eager = [x ** 2 for x in range(10_000_000)]  # Takes time, uses memory

# Lazy: values computed on demand
lazy = (x ** 2 for x in range(10_000_000))   # Instant, minimal memory

# Only computes what's needed
first_5 = list(islice(lazy, 5))  # Only computes 5 values
```

**Related**: Generator Expression, Memory Efficiency, Short-Circuit Evaluation

---

### Memory-Efficient Processing

**Definition**: Processing data one item at a time rather than loading everything into memory. Generators enable this through lazy evaluation.

**Example**:
```python
import sys

# Memory-inefficient: 8+ MB for 1M integers
squares_list = [x ** 2 for x in range(1_000_000)]
print(f"List: {sys.getsizeof(squares_list):,} bytes")

# Memory-efficient: ~200 bytes regardless of size
squares_gen = (x ** 2 for x in range(1_000_000))
print(f"Generator: {sys.getsizeof(squares_gen):,} bytes")

# Process large file line by line
def process_file(filename):
    with open(filename) as f:
        for line in f:  # File objects are iterators
            yield process_line(line)
```

**Related**: Lazy Evaluation, Generator, File Processing

---

### Pipeline

**Definition**: A sequence of generator functions where each stage processes data and yields results to the next stage, enabling modular and efficient data processing.

**Example**:
```python
def read_data(source):
    for item in source:
        yield item

def validate(items):
    for item in items:
        if is_valid(item):
            yield item

def transform(items):
    for item in items:
        yield process(item)

def aggregate(items):
    total = 0
    count = 0
    for item in items:
        total += item
        count += 1
    return total / count

# Pipeline: data flows through stages
raw = range(1000)
result = aggregate(transform(validate(read_data(raw))))
```

**Related**: Generator Composition, Data Processing, Streaming

---

### `StopIteration`

**Definition**: A built-in exception raised by `__next__()` to signal that the iterator has no more values. Catches by `for` loops to terminate iteration.

**Example**:
```python
my_iter = iter([1, 2, 3])
print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3

try:
    next(my_iter)  # Raises StopIteration
except StopIteration:
    print("No more items")

# Custom iterator
class OneShot:
    def __iter__(self):
        return self
    def __next__(self):
        raise StopIteration

list(OneShot())  # []
```

**Related**: Iterator Protocol, `next()`, `for` Loop Termination

---

### `throw()`

**Definition**: A generator method that raises an exception inside the generator at the point of the last `yield`. Used for error injection and cooperative cancellation.

**Example**：
```python
def resilient_generator():
    try:
        while True:
            try:
                value = yield
                print(f"Processing: {value}")
            except ValueError as e:
                print(f"Handling error: {e}")
            except GeneratorExit:
                print("Generator closed")
                return

gen = resilient_generator()
next(gen)
gen.send("hello")      # Processing: hello
gen.throw(ValueError, "bad input")  # Handling error: bad input
gen.send("world")      # Processing: world
gen.close()            # Generator closed
```

**Related**: `send()`, `close()`, Exception Handling

---

### `yield`

**Definition**: A keyword that produces a value from a generator function and suspends execution. When `next()` is called again, execution resumes after the `yield`.

**Example**:
```python
def simple():
    print("Before yield 1")
    yield 1
    print("Between yields")
    yield 2
    print("After yield 2")

gen = simple()
print(next(gen))
# Output: "Before yield 1" -> 1
print(next(gen))
# Output: "Between yields" -> 2
```

**Related**: Generator Function, `yield from`, Generator Iterator

---

### `yield from`

**Definition**: A syntax for delegating part of a generator's operations to another generator or iterable, simplifying nested generators and enabling sub-generators to receive sent values and return values.

**Example**:
```python
def generator():
    yield "before"
    yield from [1, 2, 3]     # Delegates to list iterator
    yield from inner_gen()    # Delegates to sub-generator
    yield "after"

def inner_gen():
    yield "inner1"
    yield "inner2"

print(list(generator()))
# ["before", 1, 2, 3, "inner1", "inner2", "after"]
```

**Related**: Generator Delegation, Sub-Generator, `send()` Forwarding

---

### Zip Generator

**Definition**: The `zip()` function returns a lazy iterator that aggregates elements from multiple iterables, producing tuples until the shortest iterable is exhausted.

**Example**:
```python
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
grades = ["A", "B+", "A-"]

# Lazy - produces tuples on demand
zipped = zip(names, scores, grades)
print(type(zipped))  # <class 'zip'>
print(list(zipped))  # [("Alice", 95, "A"), ("Bob", 87, "B+"), ...]

# Useful in generator pipelines
def combine_data(names, scores):
    for name, score in zip(names, scores):
        yield {"name": name, "score": score}
```

**Related**: `zip()`, Iterator, Lazy Evaluation, Tuple Packing

---
