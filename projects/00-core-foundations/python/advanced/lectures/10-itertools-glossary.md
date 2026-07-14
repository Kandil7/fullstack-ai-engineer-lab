# itertools Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| `itertools` | Module of iterator building blocks |
| `count` | Infinite counter with start and step |
| `cycle` | Infinite cycling through an iterable |
| `repeat` | Repeat a value (finite or infinite) |
| `chain` | Chain multiple iterables into one |
| `chain.from_iterable` | Flatten nested iterables |
| `islice` | Slice an iterator by index |
| `takewhile` | Take elements while condition is true |
| `dropwhile` | Drop elements while condition is true |
| `starmap` | Apply function to unpacked arguments |
| `filterfalse` | Filter where predicate is false |
| `compress` | Filter based on selector iterable |
| `product` | Cartesian product of iterables |
| `permutations` | All ordered arrangements |
| `combinations` | All unordered selections |
| `combinations_with_replacement` | Combinations allowing repeats |
| `tee` | Create independent iterators from one |
| `zip_longest` | Zip with fillvalue for short iterables |
| `groupby` | Group consecutive elements by key |
| `accumulate` | Running accumulation with function |
| Iterator | Object implementing `__iter__` and `__next__` |
| Iterable | Object that can return an iterator |
| Lazy Evaluation | Computing values on demand |
| Short-Circuit | Stopping iteration early |
| Memory-Efficient | Processing without storing all data |
| Pipeline | Chain of iterators for data processing |
| Combinatorics | Mathematical combinations/permutations |
| Cartesian Product | All possible pairings of elements |

---

## Detailed Definitions

### `accumulate`

**Definition**: A function that makes an iterator that returns accumulated sums (or other binary functions) of the input iterable.

**Example**:
```python
from itertools import accumulate
from operator import mul

# Running sum
numbers = [1, 2, 3, 4, 5]
print(list(accumulate(numbers)))
# [1, 3, 6, 10, 15]

# Running product
print(list(accumulate(numbers, mul)))
# [1, 2, 6, 24, 120]

# Running maximum
print(list(accumulate(numbers, max)))
# [1, 2, 3, 4, 5]

# With initial value
print(list(accumulate(numbers, initial=100)))
# [100, 101, 103, 106, 110, 115]
```

**Related**: Running Total, Prefix Sum, Cumulative Operation

---

### `chain`

**Definition**: A function that makes an iterator that returns elements from the first iterable until exhausted, then continues with the next iterable.

**Example**：
```python
from itertools import chain

# Chain multiple iterables
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

combined = list(chain(list1, list2, list3))
print(combined)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Chain from iterable (flatten)
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(chain.from_iterable(nested))
print(flat)  # [1, 2, 3, 4, 5, 6]
```

**Related**: Flattening, Concatenation, `chain.from_iterable`

---

### `chain.from_iterable`

**Definition**: A class method that creates an iterator from a single iterable of iterables, flattening one level of nesting.

**Example**：
```python
from itertools import chain

# Flatten nested lists
nested = [[1, 2], [3, [4, 5]], [6]]
flat = list(chain.from_iterable(nested))
print(flat)  # [1, 2, 3, [4, 5], 6]  # Only one level

# Flatten strings
words = ["hello", "world"]
chars = list(chain.from_iterable(words))
print(chars)  # ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']
```

**Related**: `chain`, Flattening, Nested Iterables

---

### `combinations`

**Definition**: A function that returns all possible combinations of r elements from the input iterable, without repetition.

**Example**：
```python
from itertools import combinations

# All pairs
items = ["A", "B", "C", "D"]
pairs = list(combinations(items, 2))
print(pairs)
# [("A","B"), ("A","C"), ("A","D"), ("B","C"), ("B","D"), ("C","D")]

# Single elements
singles = list(combinations(items, 1))
print(singles)  # [("A",), ("B",), ("C",), ("D",)]

# All elements
all_items = list(combinations(items, 4))
print(all_items)  # [("A","B","C","D")]
```

**Related**: `permutations`, Combinatorics, Subsets

---

### `combinations_with_replacement`

**Definition**: A function that returns combinations where elements can be repeated.

**Example**：
```python
from itertools import combinations_with_replacement

# With replacement
items = [1, 2, 3]
combs = list(combinations_with_replacement(items, 2))
print(combs)
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]

# Compare with combinations
from itertools import combinations
no_replace = list(combinations(items, 2))
print(no_replace)  # [(1,2), (1,3), (2,3)]  # No (1,1) etc.
```

**Related**: `combinations`, Replacement, Multiset

---

### `compress`

**Definition**: A function that filters elements from data returning only those with a corresponding selector that is true.

**Example**：
```python
from itertools import compress

data = ["A", "B", "C", "D", "E"]
selectors = [1, 0, 1, 0, 1]

result = list(compress(data, selectors))
print(result)  # ["A", "C", "E"]

# With boolean selectors
words = ["hello", "world", "python", "is", "great"]
lengths = [len(w) > 4 for w in words]
filtered = list(compress(words, lengths))
print(filtered)  # ["hello", "world", "python", "great"]
```

**Related**: Filtering, Selector, Masking

---

### `count`

**Definition**: An infinite iterator that generates consecutive numbers starting from a given value with a specified step.

**Example**：
```python
from itertools import count, islice

# Basic counter
counter = count(1)
print(list(islice(counter, 5)))  # [1, 2, 3, 4, 5]

# With step
counter = count(10, 2)
print(list(islice(counter, 5)))  # [10, 12, 14, 16, 18]

# Float step
counter = count(0.5, 0.1)
print(list(islice(counter, 5)))  # [0.5, 0.6, 0.7, 0.8, 0.9]
```

**Related**: `cycle`, `repeat`, Infinite Iterators

---

### `cycle`

**Definition**: An infinite iterator that cycles through the elements of an iterable indefinitely.

**Example**：
```python
from itertools import cycle, islice

# Cycle through values
colors = cycle(["red", "green", "blue"])
print(list(islice(colors, 7)))
# ["red", "green", "blue", "red", "green", "blue", "red"]

# Round-robin
servers = cycle(["s1", "s2", "s3"])
for i in range(6):
    print(f"Request {i} -> {next(servers)}")
# Request 0 -> s1
# Request 1 -> s2
# Request 2 -> s3
# Request 3 -> s1
# ...
```

**Related**: `count`, `repeat`, Infinite Iterators

---

### `dropwhile`

**Definition**: A function that drops elements from the start of an iterable while the predicate is true, then returns the rest.

**Example**：
```python
from itertools import dropwhile

# Drop while less than 5
data = [1, 3, 5, 7, 2, 4, 6]
result = list(dropwhile(lambda x: x < 5, data))
print(result)  # [5, 7, 2, 4, 6]  # Keeps 5 and rest

# Drop leading whitespace
lines = ["  ", "  ", "hello", "world"]
result = list(dropwhile(lambda x: not x.strip(), lines))
print(result)  # ["hello", "world"]
```

**Related**: `takewhile`, Filtering

---

### `filterfalse`

**Definition**: A function that returns an iterator for elements where the predicate returns false.

**Example**：
```python
from itertools import filterfalse

# Keep even numbers (filter out odd)
data = range(10)
evens = list(filterfalse(lambda x: x % 2, data))
print(evens)  # [0, 2, 4, 6, 8]

# Keep odd numbers
odds = list(filterfalse(lambda x: x % 2 == 0, data))
print(odds)  # [1, 3, 5, 7, 9]

# Complement of filter
filtered = list(filter(lambda x: x % 2 == 0, data))
print(filtered)  # [0, 2, 4, 6, 8]  # Same as evens
```

**Related**: `filter`, Filtering, Predicate

---

### `groupby`

**Definition**: A function that groups consecutive elements of an iterable by a key function.

**Example**：
```python
from itertools import groupby

# Group by key
data = [
    {"type": "A", "value": 1},
    {"type": "A", "value": 2},
    {"type": "B", "value": 3},
    {"type": "B", "value": 4},
]

# Must sort first!
data.sort(key=lambda x: x["type"])

for key, group in groupby(data, key=lambda x: x["type"]):
    print(f"Group {key}: {list(group)}")
# Group A: [{'type': 'A', 'value': 1}, {'type': 'A', 'value': 2}]
# Group B: [{'type': 'B', 'value': 3}, {'type': 'B', 'value': 4}]
```

**Related**: Sorting, Key Function, Consecutive Grouping

---

### `islice`

**Definition**: A function that slices an iterator by position, accepting start, stop, and step arguments.

**Example**：
```python
from itertools import islice

# Slice from start
data = range(100)
print(list(islice(data, 5)))  # [0, 1, 2, 3, 4]

# Slice from middle
print(list(islice(data, 5, 10)))  # [5, 6, 7, 8, 9]

# With step
print(list(islice(data, 0, 20, 3)))  # [0, 3, 6, 9, 12, 15, 18]

# Limit infinite iterator
from itertools import count
limited = list(islice(count(1), 10))
print(limited)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

**Related**: Slicing, Iterator Limits

---

### `product`

**Definition**: A function that computes the Cartesian product of input iterables.

**Example**：
```python
from itertools import product

# Two dimensions
colors = ["red", "blue"]
sizes = ["S", "M", "L"]
print(list(product(colors, sizes)))
# [("red","S"), ("red","M"), ("red","L"),
#  ("blue","S"), ("blue","M"), ("blue","L")]

# With repeat (power)
binary = list(product([0, 1], repeat=3))
print(binary)
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1),
#  (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
```

**Related**: Cartesian Product, Combinatorics

---

### `permutations`

**Definition**: A function that returns all possible ordered arrangements of r elements from the input iterable.

**Example**：
```python
from itertools import permutations

# All permutations
items = ["A", "B", "C"]
perms = list(permutations(items))
print(perms)
# [("A","B","C"), ("A","C","B"), ("B","A","C"),
#  ("B","C","A"), ("C","A","B"), ("C","B","A")]

# Permutations of length 2
perms_2 = list(permutations(items, 2))
print(perms_2)
# [("A","B"), ("A","C"), ("B","A"), ("B","C"), ("C","A"), ("C","B")]
```

**Related**: `combinations`, Order Matters, Combinatorics

---

### `repeat`

**Definition**: An iterator that returns the same value repeatedly, either a finite number of times or infinitely.

**Example**：
```python
from itertools import repeat, islice

# Finite repeat
repeated = repeat("hello", 3)
print(list(repeated))  # ["hello", "hello", "hello"]

# Infinite repeat
infinite = repeat("hello")
print(list(islice(infinite, 5)))
# ["hello", "hello", "hello", "hello", "hello"]

# Useful with map
squares = list(map(pow, range(5), repeat(2)))
print(squares)  # [0, 1, 4, 9, 16]
```

**Related**: `count`, `cycle`, Infinite Iterators

---

### `starmap`

**Definition**: A function that applies a function to argument tuples from the iterable.

**Example**：
```python
from itertools import starmap

# Apply to tuples
pairs = [(1, 2), (3, 4), (5, 6)]
products = list(starmap(pow, pairs))
print(products)  # [1, 81, 15625]

# With custom function
def add(a, b):
    return a + b

sums = list(starmap(add, pairs))
print(sums)  # [3, 7, 11]

# Power
powers = list(starmap(pow, [(2, 3), (3, 2), (4, 2)]))
print(powers)  # [8, 9, 16]
```

**Related**: `map`, Function Application, Tuple Unpacking

---

### `takewhile`

**Definition**: A function that returns elements from the start of an iterable while the predicate is true.

**Example**：
```python
from itertools import takewhile

# Take while less than 5
data = [1, 3, 5, 7, 2, 4, 6]
taken = list(takewhile(lambda x: x < 5, data))
print(taken)  # [1, 3]

# Take while non-empty
words = ["hello", "world", "", "python"]
taken = list(takewhile(lambda x: x, words))
print(taken)  # ["hello", "world"]
```

**Related**: `dropwhile`, Filtering

---

### `tee`

**Definition**: A function that creates multiple independent iterators from a single iterator.

**Example**：
```python
from itertools import tee

# Create independent copies
original = range(5)
iter1, iter2, iter3 = tee(original, 3)

print(list(iter1))  # [0, 1, 2, 3, 4]
print(list(iter2))  # [0, 1, 2, 3, 4]
print(list(iter3))  # [0, 1, 2, 3, 4]

# Each is independent
print(list(iter1))  # [0, 1, 2, 3, 4]
print(list(iter2))  # [0, 1, 2, 3, 4]  # Same data, not exhausted
```

**Related**: Iterator Copying, Memory Warning

---

### `zip_longest`

**Definition**: A function that zips iterables, filling missing values with a specified fillvalue.

**Example**：
```python
from itertools import zip_longest

# Different lengths
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87]

zipped = list(zip_longest(names, scores, fillvalue="N/A"))
print(zipped)
# [("Alice", 95), ("Bob", 87), ("Charlie", "N/A")]

# Default fillvalue is None
zipped = list(zip_longest(names, scores))
print(zipped)
# [("Alice", 95), ("Bob", 87), ("Charlie", None)]
```

**Related**: `zip`, Filling Missing Values

---

### Accumulator

**Definition**: A pattern where values are cumulatively combined (summed, multiplied, etc.) as an iterator progresses. Implemented by `accumulate`.

**Example**：
```python
from itertools import accumulate

# Running sum accumulator
numbers = [1, 2, 3, 4, 5]
running_sum = list(accumulate(numbers))
print(running_sum)  # [1, 3, 6, 10, 15]

# Running max accumulator
running_max = list(accumulate(numbers, max))
print(running_max)  # [1, 2, 3, 4, 5]

# Running product accumulator
from operator import mul
running_prod = list(accumulate(numbers, mul))
print(running_prod)  # [1, 2, 6, 24, 120]
```

**Related**: `accumulate`, Prefix Sum, Running Total

---

### Combinatorics

**Definition**: A branch of mathematics dealing with combinations, permutations, and arrangements of elements. `itertools` provides functions for these operations.

**Example**：
```python
from itertools import combinations, permutations, product

# Combinations (order doesn't matter)
items = [1, 2, 3, 4]
print(list(combinations(items, 2)))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# Permutations (order matters)
print(list(permutations(items, 2)))
# [(1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,1), (3,2), (3,4), (4,1), (4,2), (4,3)]

# Cartesian product
print(list(product([1, 2], [3, 4])))
# [(1,3), (1,4), (2,3), (2,4)]
```

**Related**: `combinations`, `permutations`, `product`

---

### Iterator

**Definition**: An object implementing `__iter__` and `__next__` methods, producing values one at a time. `itertools` functions return iterators.

**Example**：
```python
# itertools returns iterators
from itertools import count, islice

counter = count(1)
print(type(counter))  # <class 'itertools.count'>

# Convert to list if needed
numbers = list(islice(counter, 5))
print(numbers)  # [1, 2, 3, 4, 5]

# Or iterate with next()
counter = count(1)
print(next(counter))  # 1
print(next(counter))  # 2
```

**Related**: Iterator Protocol, Lazy Evaluation

---

### Lazy Evaluation

**Definition**: A strategy where values are computed only when needed. `itertools` functions return iterators that compute values on demand.

**Example**：
```python
from itertools import islice, count

# Eager: all values in memory
eager_list = list(range(1_000_000))  # ~8 MB

# Lazy: one value at a time
lazy_iter = count(1)  # ~200 bytes
first_100 = list(islice(lazy_iter, 100))  # Only computes 100

# Pipeline of lazy operations
from itertools import filterfalse
data = range(1_000_000)
evens = filterfalse(lambda x: x % 2, data)  # Still lazy!
limited = islice(evens, 10)  # Still lazy!
result = list(limited)  # NOW computes 10 values
```

**Related**: Memory Efficiency, Iterator, Short-Circuit Evaluation

---

### Memory-Efficient Processing

**Definition**: Processing data one item at a time without loading everything into memory. `itertools` enables this through lazy evaluation.

**Example**：
```python
from itertools import islice, chain

# Process large file line by line
def process_large_file(filename, chunk_size=1000):
    with open(filename) as f:
        while True:
            chunk = list(islice(f, chunk_size))
            if not chunk:
                break
            process(chunk)

# Chain multiple files
def process_multiple_files(*filenames):
    for filename in filenames:
        with open(filename) as f:
            yield from f
```

**Related**: Lazy Evaluation, Streaming, File Processing

---

### Pipeline

**Definition**: A sequence of iterator operations where data flows through stages, each transforming or filtering the data.

**Example**：
```python
from itertools import chain, filterfalse, starmap

def read_data(source):
    for item in source:
        yield item

def validate(items):
    for item in items:
        if item.get("valid"):
            yield item

def transform(items):
    for item in items:
        yield {
            "name": item["name"].upper(),
            "score": item["score"] * 100
        }

def aggregate(items):
    total = 0
    count = 0
    for item in items:
        total += item["score"]
        count += 1
    return {"total": total, "count": count, "avg": total / count}

# Compose pipeline
pipeline = aggregate(transform(validate(read_data(data))))
result = pipeline()
```

**Related**: Iterator Composition, Data Processing

---

### `product` (Cartesian Product)

**Definition**: See "product". Computes all possible combinations of elements from input iterables.

**Example**：
```python
from itertools import product

# Days of week and times
days = ["Mon", "Tue", "Wed"]
times = ["9am", "12pm", "3pm"]
schedule = list(product(days, times))
print(schedule)
# [('Mon','9am'), ('Mon','12pm'), ('Mon','3pm'),
#  ('Tue','9am'), ('Tue','12pm'), ('Tue','3pm'),
#  ('Wed','9am'), ('Wed','12pm'), ('Wed','3pm')]
```

**Related**: Combinatorics, All Pairings

---

### `groupby`

**Definition**: See "groupby". Groups consecutive elements with the same key.

**Example**：
```python
from itertools import groupby

# Group numbers by parity
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sorted_nums = sorted(numbers, key=lambda x: x % 2)

for key, group in groupby(sorted_nums, key=lambda x: x % 2):
    print(f"{'Even' if key == 0 else 'Odd'}: {list(group)}")
# Even: [2, 4, 6, 8, 10]
# Odd: [1, 3, 5, 7, 9]
```

**Related**: Sorting, Key Function

---

### Infinite Iterator

**Definition**: An iterator that never raises `StopIteration`, producing values indefinitely. Must be consumed with care (using `islice`, `takewhile`, etc.).

**Example**：
```python
from itertools import count, cycle, repeat, islice

# Infinite counter
counter = count(1)
first_5 = list(islice(counter, 5))  # [1, 2, 3, 4, 5]

# Infinite cycling
colors = cycle(["R", "G", "B"])
first_6 = list(islice(colors, 6))  # ['R', 'G', 'B', 'R', 'G', 'B']

# Infinite repeat
ones = repeat(1)
first_5 = list(islice(ones, 5))  # [1, 1, 1, 1, 1]
```

**Related**: `count`, `cycle`, `repeat`, `islice`

---
