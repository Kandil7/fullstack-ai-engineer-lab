# Advanced Python Lecture 02: Generators and Iterators

## Topic Overview

Generators and iterators are fundamental Python concepts that enable lazy evaluation, memory-efficient data processing, and elegant handling of streams of data. Understanding these concepts is essential for working with large datasets, building data pipelines, and implementing efficient algorithms — skills critical in AI engineering and data science.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the iterator protocol (`__iter__` and `__next__`)
2. Create generator functions using `yield`
3. Build generator expressions for concise lazy evaluation
4. Use `yield from` for delegation
5. Implement infinite sequences and coroutines
6. Compose generators into data pipelines
7. Convert between generators and lists appropriately
8. Handle generator lifecycle and cleanup with `send()`, `throw()`, and `close()`
9. Apply generators to real-world AI engineering patterns
10. Debug generator-related issues

---

## 1. The Iterator Protocol

### What is an Iterator?

An **iterator** is an object that implements two methods:
- `__iter__()`: Returns the iterator object itself
- `__next__()`: Returns the next value or raises `StopIteration`

```python
class CountDown:
    """A manual iterator that counts down from n to 0."""
    
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Usage
for num in CountDown(5):
    print(num)  # 5, 4, 3, 2, 1, 0
```

### Iterable vs Iterator

```python
# Iterable: Has __iter__() that returns an iterator
# Examples: list, dict, str, range, file objects

# Iterator: Has both __iter__() and __next__()
# Examples: enumerate(), map(), filter(), zip()

my_list = [1, 2, 3]  # Iterable
my_iter = iter(my_list)  # Iterator

next(my_iter)  # 1
next(my_iter)  # 2
next(my_iter)  # 3
# next(my_iter)  # StopIteration
```

### The `for` Loop Mechanics

```python
# What happens under the hood:
for item in my_list:
    print(item)

# Is equivalent to:
iterator = iter(my_list)  # Calls my_list.__iter__()
while True:
    try:
        item = next(iterator)  # Calls iterator.__next__()
        print(item)
    except StopIteration:
        break
```

---

## 2. Generator Functions

### Basic Generators

Generators are functions that use `yield` instead of `return`. Each `yield` produces a value and suspends execution.

```python
def count_up(start, end):
    """Generator that yields numbers from start to end."""
    current = start
    while current <= end:
        yield current
        current += 1

# Usage
for num in count_up(1, 5):
    print(num)  # 1, 2, 3, 4, 5

# Or manually:
gen = count_up(1, 3)
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

### How `yield` Works

```python
def simple_generator():
    print("Step 1: Before first yield")
    yield 1
    print("Step 2: After first yield, before second")
    yield 2
    print("Step 3: After second yield, before return")
    yield 3
    print("Step 4: Done")

gen = simple_generator()
print(next(gen))  # Step 1: Before first yield -> 1
print(next(gen))  # Step 2: After first yield -> 2
print(next(gen))  # Step 3: After second yield -> 3
# next(gen)       # Step 4: Done -> StopIteration
```

### Generators vs Lists

```python
import sys

# List: stores all values in memory
squares_list = [x ** 2 for x in range(1000000)]
print(f"List memory: {sys.getsizeof(squares_list):,} bytes")
# ~8 MB

# Generator: produces values on demand
squares_gen = (x ** 2 for x in range(1000000))
print(f"Generator memory: {sys.getsizeof(squares_gen):,} bytes")
# ~200 bytes
```

---

## 3. Generator Expressions

Concise syntax for creating generators, similar to list comprehensions:

```python
# List comprehension (eager evaluation)
squares_list = [x ** 2 for x in range(10)]

# Generator expression (lazy evaluation)
squares_gen = (x ** 2 for x in range(10))

# Using in a for loop
for sq in squares_gen:
    print(sq, end=" ")
# 0 1 4 9 16 25 36 49 64 81

# Passing to functions that accept iterables
total = sum(x ** 2 for x in range(100))
max_val = max(x ** 2 for x in range(100))
```

### Complex Generator Expressions

```python
# Nested generators
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = (num for row in matrix for num in row)
print(list(flat))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Filtered generators
evens = (x for x in range(100) if x % 2 == 0)

# Chained transformations
processed = (x.strip().lower() for x in ["  Hello ", " WORLD ", "  Python  "])
```

---

## 4. `yield from` — Generator Delegation

`yield from` allows a generator to yield values from another generator or iterable:

```python
def inner_generator():
    yield 1
    yield 2
    yield 3

def outer_generator():
    yield "A"
    yield from inner_generator()  # Delegates to inner
    yield "B"

list(outer_generator())  # ["A", 1, 2, 3, "B"]
```

### Practical Use: Flattening Nested Structures

```python
def flatten(nested):
    """Recursively flatten nested iterables."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3, [4, 5]], [6, [7, [8, [9]]]]]
print(list(flatten(nested)))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### `yield from` with Return Values

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value
    return total  # Final result

def delegator():
    result = yield from accumulator()
    print(f"Final total: {result}")

gen = delegator()
next(gen)        # Initialize
gen.send(10)     # total=10
gen.send(20)     # total=30
gen.send(30)     # total=60
gen.send(None)   # StopIteration, prints "Final total: 60"
```

---

## 5. Generator Methods: `send()`, `throw()`, `close()`

### `send()` — Sending Values into Generators

```python
def chatbot():
    """Simple chatbot generator using send()."""
    response = yield "Hello! How can I help?"
    while True:
        if response == "quit":
            yield "Goodbye!"
            return
        response = yield f"You said: {response}. Tell me more."

bot = chatbot()
print(next(bot))        # "Hello! How can I help?"
print(bot.send("Hi"))   # "You said: Hi. Tell me more."
print(bot.send("Python")) # "You said: Python. Tell me more."
print(bot.send("quit")) # "Goodbye!"
```

### `throw()` — Raising Exceptions Inside Generators

```python
def safe_generator():
    try:
        while True:
            value = yield
            print(f"Received: {value}")
    except ValueError:
        print("Caught ValueError!")
    finally:
        print("Generator cleaned up")

gen = safe_generator()
next(gen)              # Initialize
gen.send("hello")     # Received: hello
gen.throw(ValueError)  # Caught ValueError! -> Generator cleaned up
```

### `close()` — Closing Generators

```python
def resource_generator():
    print("Opening resource")
    try:
        while True:
            yield "resource data"
    finally:
        print("Closing resource")

gen = resource_generator()
next(gen)    # "Opening resource"
gen.close()  # "Closing resource"
```

---

## 6. Infinite Generators

```python
def count_from(start=0, step=1):
    """Infinite counter."""
    current = start
    while True:
        yield current
        current += step

def fibonacci():
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def cycle(iterable):
    """Infinite cycling through an iterable."""
    while True:
        yield from iterable

# Usage with itertools.islice
from itertools import islice

first_10_fibs = list(islice(fibonacci(), 10))
print(first_10_fibs)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

first_10_count = list(islice(count_from(1), 10))
print(first_10_count)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

---

## 7. Composing Generators into Data Pipelines

```python
def read_data(source):
    """Stage 1: Read raw data."""
    for item in source:
        yield item

def filter_valid(data):
    """Stage 2: Filter invalid entries."""
    for item in data:
        if item.get("valid", False):
            yield item

def transform(data):
    """Stage 3: Transform data."""
    for item in data:
        item["name"] = item["name"].upper()
        item["score"] *= 100
        yield item

def aggregate(data):
    """Stage 4: Aggregate results."""
    total = 0
    count = 0
    for item in data:
        total += item["score"]
        count += 1
    yield {"total": total, "count": count, "average": total / count if count else 0}

# Compose the pipeline
raw_data = [
    {"name": "alice", "score": 0.9, "valid": True},
    {"name": "bob", "score": 0.7, "valid": False},  # Filtered out
    {"name": "charlie", "score": 0.85, "valid": True},
]

pipeline = aggregate(transform(filter_valid(read_data(raw_data))))
result = next(pipeline)
print(result)  # {'total': 175.0, 'count': 2, 'average': 87.5}
```

### Pipeline with `itertools`

```python
import itertools

def pipeline_with_itertools(data):
    """Use itertools for common pipeline operations."""
    return itertools.starmap(
        lambda x: {"name": x["name"].upper(), "score": x["score"] * 100},
        filter(lambda x: x["valid"], data)
    )
```

---

## 8. Generators in AI Engineering

### Lazy Data Loading

```python
def load_chunks(file_path, chunk_size=1024):
    """Load file in chunks for memory efficiency."""
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def process_large_file(file_path):
    """Process a large file without loading it all into memory."""
    for chunk in load_chunks(file_path, chunk_size=4096):
        # Process each chunk
        yield process_chunk(chunk)
```

### Token Stream Processing

```python
def tokenize_stream(text_stream):
    """Tokenize a stream of text chunks."""
    buffer = ""
    for text in text_stream:
        buffer += text
        while " " in buffer:
            token, buffer = buffer.split(" ", 1)
            yield token
    if buffer:
        yield buffer

# Usage
text_chunks = ["Hello world", " this is", " a test"]
tokens = tokenize_stream(text_chunks)
print(list(tokens))  # ["Hello", "world", "this", "is", "a", "test"]
```

### Batch Generator for Training

```python
def batch_generator(data, batch_size=32):
    """Generate batches for model training."""
    import random
    shuffled = list(data)
    random.shuffle(shuffled)
    
    for i in range(0, len(shuffled), batch_size):
        batch = shuffled[i:i + batch_size]
        inputs = [item["input"] for item in batch]
        targets = [item["target"] for item in batch]
        yield inputs, targets

def infinite_batches(data, batch_size=32):
    """Infinite batch generator for training loops."""
    while True:
        yield from batch_generator(data, batch_size)
```

---

## 9. Common Mistakes to Avoid

### Mistake 1: Consuming a Generator Twice

```python
# Generators are single-use!
def generate_numbers():
    yield 1
    yield 2
    yield 3

gen = generate_numbers()
print(list(gen))  # [1, 2, 3]
print(list(gen))  # [] — Empty! Generator exhausted

# Solution: Use itertools.tee() or create a new generator
from itertools import tee

gen1, gen2 = tee(generate_numbers())
print(list(gen1))  # [1, 2, 3]
print(list(gen2))  # [1, 2, 3]
```

### Mistake 2: Forgetting Generator is Lazy

```python
# This creates a generator that does NOTHING until iterated
def process():
    for i in range(10):
        print(f"Processing {i}")
        yield i

# Nothing prints here!
gen = process()

# NOW it processes
list(gen)
```

### Mistake 3: Holding References in Long-Lived Generators

```python
# BAD: Keeps entire dataset in memory via reference
def bad_generator(data):
    for item in data:
        yield transform(item)
    # 'data' reference held until generator is garbage collected

# BETTER: Process and release
def good_generator(data):
    for item in data:
        result = transform(item)
        del item  # Release reference
        yield result
```

---

## 10. Best Practices

1. **Use generators for large datasets** to avoid memory overhead
2. **Prefer generator expressions** for simple transformations
3. **Use `yield from`** for delegation instead of manual loops
4. **Don't reuse generators** — create new ones when needed
5. **Use `itertools.islice`** to limit infinite generators
6. **Add `close()` cleanup** in `finally` blocks for resource management
7. **Document yield behavior** in docstrings
8. **Use `send()`** for coroutine-like patterns
9. **Test generators** by converting to lists in tests
10. **Consider `collections.deque`** when you need to peek without consuming

---

## 11. Practice Exercises

### Exercise 1: Range Generator
Implement a `frange(start, stop, step)` generator that works like `range()` but supports float steps:

```python
for x in frange(0.0, 1.0, 0.1):
    print(f"{x:.1f}", end=" ")
# 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
```

### Exercise 2: Window Generator
Create a `sliding_window(iterable, size)` generator that yields windows:

```python
list(sliding_window([1, 2, 3, 4, 5], 3))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

### Exercise 3: Pipeline Generator
Build a log file parser using generator pipeline:
1. `read_lines(file)` — yields lines
2. `filter_errors(lines)` — yields only error lines
3. `parse_timestamp(lines)` — extracts timestamps
4. `aggregate_by_minute(timestamps)` — groups by minute

### Exercise 4: Coroutine with `send()`
Create a `running_average()` generator that computes the running average:

```python
avg = running_average()
next(avg)          # Initialize
avg.send(10)       # -> 10.0
avg.send(20)       # -> 15.0
avg.send(30)       # -> 20.0
```

---

## 12. Summary

| Concept | Description |
|---------|-------------|
| **Iterator Protocol** | `__iter__` + `__next__` methods |
| **Generator Function** | Function with `yield` keyword |
| **Generator Expression** | `(expr for x in iterable)` syntax |
| **`yield from`** | Delegate to sub-generator |
| **`send()`** | Send values into generator |
| **`throw()`** | Raise exceptions in generator |
| **`close()`** | Close generator with cleanup |
| **Infinite Generators** | `while True: yield` patterns |
| **Pipeline Pattern** | Compose generators for data processing |
| **Memory Efficiency** | Lazy evaluation, one item at a time |

Generators are indispensable for building efficient, scalable Python applications. They enable processing datasets larger than memory, building composable data pipelines, and implementing elegant control flow patterns — all essential skills for AI engineers working with data-intensive applications.

---

## Next Steps

In the next lecture, we'll explore **Context Managers**, which provide elegant resource management using the `with` statement.
