# Advanced Python Lecture 10: itertools

## Topic Overview

The `itertools` module provides a collection of fast, memory-efficient tools for working with iterators. These building blocks enable elegant solutions for combinatorial problems, data processing pipelines, and efficient iteration patterns. Mastering `itertools` is essential for writing Pythonic code that handles large datasets, generates sequences, and processes data streams efficiently.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use infinite iterators (`count`, `cycle`, `repeat`)
2. Apply terminating iterators (`chain`, `islice`, `starmap`)
3. Generate combinatorial iterators (`product`, `permutations`, `combinations`)
4. Implementtee, zip_longest, and groupby
5. Build efficient data pipelines with itertools
6. Handle infinite sequences safely
7. Apply itertools to AI engineering patterns
8. Combine itertools with generators
9. Follow itertools best practices
10. Debug itertools-related issues

---

## 1. Infinite Iterators

### `count`

```python
from itertools import count, islice

# Infinite counter
counter = count(start=10, step=2)
print(list(islice(counter, 5)))  # [10, 12, 14, 16, 18]

# With float step
float_counter = count(0.5, 0.1)
print(list(islice(float_counter, 5)))  # [0.5, 0.6, 0.7, 0.8, 0.9]
```

### `cycle`

```python
from itertools import cycle, islice

# Infinite cycling
colors = cycle(["red", "green", "blue"])
print(list(islice(colors, 7)))
# ["red", "green", "blue", "red", "green", "blue", "red"]

# Round-robin assignment
servers = cycle(["server1", "server2", "server3"])
for request in range(6):
    server = next(servers)
    print(f"Request {request} -> {server}")
```

### `repeat`

```python
from itertools import repeat

# Repeat a value
repeated = repeat("hello", 3)  # Finite: 3 repetitions
print(list(repeated))  # ["hello", "hello", "hello"]

# Infinite repeat (no second argument)
infinite = repeat("hello")
print(list(islice(infinite, 5)))  # ["hello", "hello", "hello", "hello", "hello"]

# Useful with map
squares = list(map(pow, range(5), repeat(2)))
print(squares)  # [0, 1, 4, 9, 16]
```

---

## 2. Terminating Iterators

### `chain`

```python
from itertools import chain

# Chain multiple iterables
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

combined = list(chain(list1, list2, list3))
print(combined)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Chain from iterable (flatten nested)
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(chain.from_iterable(nested))
print(flat)  # [1, 2, 3, 4, 5, 6]
```

### `islice`

```python
from itertools import islice

# Slice an iterator
data = range(100)
sliced = list(islice(data, 5, 10))
print(sliced)  # [5, 6, 7, 8, 9]

# With step
stepped = list(islice(data, 0, 20, 3))
print(stepped)  # [0, 3, 6, 9, 12, 15, 18]

# Limit infinite iterator
from itertools import count
limited = list(islice(count(1), 10))
print(limited)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### `takewhile` and `dropwhile`

```python
from itertools import takewhile, dropwhile

# Take while condition is true
data = [1, 3, 5, 7, 2, 4, 6]
taken = list(takewhile(lambda x: x < 6, data))
print(taken)  # [1, 3, 5]

# Drop while condition is true
dropped = list(dropwhile(lambda x: x < 6, data))
print(dropped)  # [7, 2, 4, 6] - keeps 7 and rest
```

### `starmap`

```python
from itertools import starmap

# Apply function to unpacked arguments
pairs = [(1, 2), (3, 4), (5, 6)]
products = list(starmap(pow, pairs))
print(products)  # [1, 81, 15625]

# With custom function
def add(a, b):
    return a + b

sums = list(starmap(add, pairs))
print(sums)  # [3, 7, 11]
```

### `filterfalse`

```python
from itertools import filterfalse

# Filter out items where predicate is true
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers (filter out odd)
evens = list(filterfalse(lambda x: x % 2, data))
print(evens)  # [2, 4, 6, 8, 10]

# Keep only odd numbers
odds = list(filterfalse(lambda x: x % 2 == 0, data))
print(odds)  # [1, 3, 5, 7, 9]
```

### `compress`

```python
from itertools import compress

# Filter based on selectors
data = ["A", "B", "C", "D", "E"]
selectors = [1, 0, 1, 0, 1]

result = list(compress(data, selectors))
print(result)  # ["A", "C", "E"]

# Useful for conditional filtering
words = ["hello", "world", "python", "is", "great"]
keep = [True, False, True, False, True]
filtered = list(compress(words, keep))
print(filtered)  # ["hello", "python", "great"]
```

---

## 3. Combinatorial Iterators

### `product`

```python
from itertools import product

# Cartesian product
colors = ["red", "blue"]
sizes = ["S", "M", "L"]

combinations = list(product(colors, sizes))
print(combinations)
# [("red", "S"), ("red", "M"), ("red", "L"),
#  ("blue", "S"), ("blue", "M"), ("blue", "L")]

# With repeat (power)
binary = list(product([0, 1], repeat=3))
print(binary)
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1),
#  (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
```

### `permutations`

```python
from itertools import permutations

# All permutations
items = ["A", "B", "C"]
perms = list(permutations(items))
print(perms)
# [("A","B","C"), ("A","C","B"), ("B","A","C"),
#  ("B","C","A"), ("C","A","B"), ("C","B","A")]

# Permutations of length r
perms_2 = list(permutations(items, 2))
print(perms_2)
# [("A","B"), ("A","C"), ("B","A"), ("B","C"), ("C","A"), ("C","B")]
```

### `combinations`

```python
from itertools import combinations

# All combinations
items = ["A", "B", "C", "D"]
combs = list(combinations(items, 2))
print(combs)
# [("A","B"), ("A","C"), ("A","D"), ("B","C"), ("B","D"), ("C","D")]

# Combinations with replacement
combs_r = list(combinations_with_replacement([1, 2, 3], 2))
print(combs_r)
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]
```

---

## 4. Combinatorial Functions

### `tee`

```python
from itertools import tee

# Create multiple independent iterators
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

### `zip_longest`

```python
from itertools import zip_longest

# Zip with different lengths (fills with fillvalue)
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87]

zipped = list(zip_longest(names, scores, fillvalue="N/A"))
print(zipped)
# [("Alice", 95), ("Bob", 87), ("Charlie", "N/A")]

# Without fillvalue (default None)
zipped = list(zip_longest(names, scores))
print(zipped)
# [("Alice", 95), ("Bob", 87), ("Charlie", None)]
```

### `groupby`

```python
from itertools import groupby

# Group consecutive elements
data = [
    {"type": "A", "value": 1},
    {"type": "A", "value": 2},
    {"type": "B", "value": 3},
    {"type": "B", "value": 4},
    {"type": "A", "value": 5},
]

# Must be sorted by key first!
data.sort(key=lambda x: x["type"])

for key, group in groupby(data, key=lambda x: x["type"]):
    print(f"Group {key}: {list(group)}")
# Group A: [{'type': 'A', 'value': 1}, {'type': 'A', 'value': 2}]
# Group B: [{'type': 'B', 'value': 3}, {'type': 'B', 'value': 4}]
# Group A: [{'type': 'A', 'value': 5}]  # New group!
```

### `accumulate`

```python
from itertools import accumulate

# Running sum
numbers = [1, 2, 3, 4, 5]
running_sum = list(accumulate(numbers))
print(running_sum)  # [1, 3, 6, 10, 15]

# Running product
from operator import mul
running_prod = list(accumulate(numbers, mul))
print(running_prod)  # [1, 2, 6, 24, 120]

# Running maximum
running_max = list(accumulate(numbers, max))
print(running_max)  # [1, 2, 3, 4, 5]

# With initial value
from operator import add
running_sum = list(accumulate(numbers, add, initial=100))
print(running_sum)  # [100, 101, 103, 106, 110, 115]
```

---

## 5. Data Processing Pipelines

```python
from itertools import chain, filterfalse, starmap

def read_chunks(source):
    """Simulate reading data in chunks."""
    for chunk in source:
        yield chunk

def filter_valid(data):
    """Filter out invalid entries."""
    for item in data:
        if item.get("valid", False):
            yield item

def transform(data):
    """Transform data."""
    for item in data:
        yield {
            "id": item["id"],
            "name": item["name"].upper(),
            "score": item["score"] * 100
        }

def aggregate(data):
    """Aggregate results."""
    total = 0
    count = 0
    for item in data:
        total += item["score"]
        count += 1
    return {"total": total, "count": count, "average": total / count if count else 0}

# Compose pipeline
raw_data = [
    {"id": 1, "name": "alice", "score": 0.9, "valid": True},
    {"id": 2, "name": "bob", "score": 0.7, "valid": False},
    {"id": 3, "name": "charlie", "score": 0.85, "valid": True},
]

pipeline = aggregate(transform(filter_valid(read_chunks(raw_data))))
result = pipeline
print(result)  # {'total': 175.0, 'count': 2, 'average': 87.5}
```

---

## 6. itertools in AI Engineering

### Batch Processing

```python
from itertools import islice, chain

def batched(iterable, batch_size):
    """Batch data into chunks."""
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch

# Usage
data = range(1000)
for batch in batched(data, 32):
    process_batch(batch)
```

### Parallel Processing Preparation

```python
from itertools import islice
import multiprocessing

def process_item(item):
    """Process a single item."""
    return item ** 2

def parallel_process(data, num_workers=4):
    """Prepare data for parallel processing."""
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(process_item, data)
    return results

# Chunk data for parallel processing
data = range(1000)
chunk_size = len(data) // 4
chunks = [
    list(islice(data, i * chunk_size, (i + 1) * chunk_size))
    for i in range(4)
]
```

### Feature Engineering

```python
from itertools import combinations, product

def generate_features(data):
    """Generate feature combinations."""
    # Feature pairs
    features = list(combinations(data.columns, 2))
    
    # Feature interactions
    interactions = list(product(data.columns, repeat=2))
    
    return features, interactions

# Generate polynomial features
def polynomial_features(degree, n_features):
    """Generate polynomial feature indices."""
    from itertools import combinations_with_replacement
    features = []
    for d in range(1, degree + 1):
        features.extend(combinations_with_replacement(range(n_features), d))
    return features
```

---

## 7. Best Practices

1. **Use `islice`** to limit infinite iterators
2. **Use `chain.from_iterable`** to flatten nested iterables
3. **Sort before `groupby`** — it groups consecutive elements
4. **Use `product`** for Cartesian products instead of nested loops
5. **Use `tee`** carefully — memory usage grows with number of copies
6. **Prefer `itertools`** over manual loops for clarity
7. **Combine with generators** for memory-efficient pipelines
8. **Use `accumulate`** for running totals/operations
9. **Profile performance** — itertools is fast but overhead matters
10. **Document complex chains** for maintainability

---

## 8. Practice Exercises

### Exercise 1: Window Iterator
Create a sliding window using itertools:

```python
def sliding_window(iterable, size):
    # Use itertools to create windows
    pass

list(sliding_window([1, 2, 3, 4, 5], 3))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

### Exercise 2: Round Robin
Implement round-robin scheduling:

```python
def round_robin(*iterables):
    # Cycle through iterables evenly
    pass

list(round_robin("ABC", "123", "xyz"))
# ["A", "1", "x", "B", "2", "y", "C", "3", "z"]
```

### Exercise 3: Combinations with Constraints
Generate valid combinations:

```python
def valid_passwords(length, min_digits=1):
    # Generate all valid passwords of given length
    pass
```

### Exercise 4: Data Pipeline
Build a data pipeline using itertools:

```python
def pipeline(data):
    # chain, filter, transform, aggregate
    pass
```

---

## 9. Summary

| Category | Functions |
|----------|-----------|
| **Infinite** | `count`, `cycle`, `repeat` |
| **Terminating** | `chain`, `islice`, `takewhile`, `dropwhile`, `starmap`, `filterfalse`, `compress` |
| **Combinatorial** | `product`, `permutations`, `combinations`, `combinations_with_replacement` |
| **Combinatorics** | `tee`, `zip_longest`, `groupby`, `accumulate` |
| **Terminating (Aggregate)** | `all`, `any`, `max`, `min`, `sum` (from built-ins) |

The `itertools` module provides fast, memory-efficient building blocks for iterator-based algorithms. Mastering these tools enables writing elegant, performant Python code for data processing, combinatorial problems, and AI engineering workflows.

---

## Next Steps

Congratulations on completing the Advanced Python lecture series! You now have a solid foundation in decorators, generators, context managers, async/await, type hints, dataclasses, enums, ABCs, functools, and itertools. Apply these concepts to build robust, maintainable Python applications in your AI engineering journey.
