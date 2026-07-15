# Python Iterators — Lecture 24

## Topic Overview

An **iterator** is an object that implements the iterator protocol, consisting of `__iter__()` and `__next__()` methods. Iterators enable **lazy evaluation** — generating values one at a time instead of storing everything in memory. This is fundamental to how Python processes sequences, files, and data streams.

Understanding iterators is key to writing efficient, memory-friendly Python code and is the foundation for generators, comprehensions, and the `itertools` module.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Understand the iterator protocol (`__iter__` and `__next__`)
- Create custom iterators using classes
- Use the `iter()` and `built-in next()` functions
- Implement generators as iterator factories
- Understand lazy evaluation and its benefits
- Use `itertools` for advanced iteration patterns
- Apply iterators to real-world scenarios

---

## Key Concepts

### 1. The Iterator Protocol

```python
# Every iterable has an __iter__() method that returns an iterator
# Every iterator has a __next__() method that returns the next value

my_list = [1, 2, 3]

# Get iterator from iterable
my_iter = iter(my_list)

# Get values one at a time
print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3
# next(my_iter)  # StopIteration exception
```

### 2. Custom Iterator Class

```python
class CountDown:
    """Custom iterator that counts down from n to 1."""
    
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self  # Iterator returns itself
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration  # Signal end of iteration
        value = self.current
        self.current -= 1
        return value

# Usage
for num in CountDown(5):
    print(num)  # 5, 4, 3, 2, 1
```

### 3. Iterables vs. Iterators

```python
# Iterable: has __iter__() method, can be iterated over
# Examples: list, tuple, str, dict, set, range

# Iterator: has both __iter__() and __next__() methods
# Created by calling iter() on an iterable

my_list = [1, 2, 3]  # Iterable (has __iter__)
my_iter = iter(my_list)  # Iterator (has __next__)

print(type(my_list))   # <class 'list'>
print(type(my_iter))   # <class 'list_iterator'>

# An iterator IS an iterable (returns itself)
print(my_iter.__iter__() is my_iter)  # True
```

### 4. Generators (Simplified Iterators)

```python
# Generator function — uses yield instead of return
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Using generator
for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# Generator is an iterator
gen = countdown(3)
print(next(gen))  # 3
print(next(gen))  # 2
print(next(gen))  # 1
# next(gen)  # StopIteration
```

### 5. Generator Expressions

```python
# List comprehension — stores all values in memory
squares_list = [x**2 for x in range(1000000)]

# Generator expression — produces values lazily
squares_gen = (x**2 for x in range(1000000))

# Generator uses much less memory
import sys
print(sys.getsizeof(squares_list))  # ~8 MB
print(sys.getsizeof(squares_gen))   # ~200 bytes

# Can only iterate once!
for val in squares_gen:
    pass
# Second iteration yields nothing
for val in squares_gen:
    print(val)  # Nothing printed!
```

### 6. Infinite Iterators

```python
from itertools import count, cycle, repeat

# count — infinite counter
counter = count(10)
for _ in range(5):
    print(next(counter))  # 10, 11, 12, 13, 14

# cycle — infinite repetition
colors = cycle(["red", "green", "blue"])
for _ in range(7):
    print(next(colors))  # red, green, blue, red, green, blue, red

# repeat — repeat a value
repeater = repeat("hello", 3)
for val in repeater:
    print(val)  # hello, hello, hello
```

### 7. Itertools Module

```python
from itertools import chain, islice, takewhile, dropwhile, accumulate

# chain — combine iterables
combined = chain([1, 2], [3, 4], [5, 6])
print(list(combined))  # [1, 2, 3, 4, 5, 6]

# islice — slice an iterator
from itertools import islice
gen = (x for x in range(100))
first_five = list(islice(gen, 5))
print(first_five)  # [0, 1, 2, 3, 4]

# accumulate — running total
from itertools import accumulate
totals = list(accumulate([1, 2, 3, 4, 5]))
print(totals)  # [1, 3, 6, 10, 15]

# takewhile / dropwhile
from itertools import takewhile, dropwhile
small = list(takewhile(lambda x: x < 5, [1, 3, 5, 2, 7]))
print(small)  # [1, 3]
```

### 8. Iterating with enumerate and zip

```python
# enumerate — adds counter to iterator
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# zip — combine multiple iterators
names = ["Alice", "Bob"]
scores = [85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip_longest — fill missing values
from itertools import zip_longest
a = [1, 2, 3]
b = [10, 20]
for x, y in zip_longest(a, b, fillvalue=0):
    print(f"{x}, {y}")
```

---

## Code Examples

### Example 1: Fibonacci Iterator

```python
class Fibonacci:
    """Generate Fibonacci numbers indefinitely."""
    
    def __init__(self):
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value

# Get first 10 Fibonacci numbers
fib = Fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Example 2: File Line Iterator

```python
def read_lines(filename, chunk_size=1024):
    """Read file line by line (memory efficient)."""
    with open(filename, 'r') as f:
        for line in f:  # File object is an iterator
            yield line.strip()

# Usage
for line in read_lines("large_file.txt"):
    process(line)
```

### Example 3: Batch Iterator

```python
def batch(iterable, n):
    """Split iterable into batches of size n."""
    iterator = iter(iterable)
    while True:
        batch_items = list(islice(iterator, n))
        if not batch_items:
            break
        yield batch_items

# Usage
data = range(25)
for batch_num, batch_items in enumerate(batch(data, 10)):
    print(f"Batch {batch_num}: {list(batch_items)}")
# Batch 0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Batch 1: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# Batch 2: [20, 21, 22, 23, 24]
```

### Example 4: Window Iterator

```python
def window(iterable, size=3):
    """Sliding window over an iterable."""
    it = iter(iterable)
    win = []
    for _ in range(size):
        try:
            win.append(next(it))
        except StopIteration:
            return
    yield tuple(win)
    
    for item in it:
        win = win[1:] + [item]
        yield tuple(win)

# Usage
data = [1, 2, 3, 4, 5, 6]
for w in window(data, 3):
    print(w)  # (1,2,3), (2,3,4), (3,4,5), (4,5,6)
```

---

## Common Mistakes to Avoid

### Mistake 1: Reusing Exhausted Iterator
```python
# WRONG — iterator is exhausted after first loop
gen = (x for x in range(5))
for val in gen:
    print(val)  # 0, 1, 2, 3, 4
for val in gen:
    print(val)  # Nothing! Iterator is empty

# CORRECT — recreate or use list
gen = (x for x in range(5))
data = list(gen)  # Convert to list if needed multiple times
```

### Mistake 2: Not Handling StopIteration
```python
# WRONG — bare next() can raise StopIteration
# val = next(my_iterator)  # May raise StopIteration

# CORRECT — provide default
val = next(my_iterator, None)  # Returns None if exhausted
```

### Mistake 3: Converting Large Iterators to Lists
```python
# WRONG — defeats the purpose of iterators
big_data = (x for x in range(10_000_000))
all_data = list(big_data)  # Uses lots of memory!

# CORRECT — iterate lazily
for val in big_data:
    process(val)
```

---

## Best Practices

1. **Use generators** for large datasets to save memory
2. **Use `next(iterator, default)`** to avoid StopIteration
3. **Don't reuse exhausted iterators** — recreate them
4. **Use `itertools`** for common iteration patterns
5. **Prefer lazy evaluation** when processing large files/streams
6. **Use `chain()`** to combine iterables efficiently
7. **Use `islice()`** for slicing iterators
8. **Understand that for loops** automatically handle StopIteration

---

## Practice Exercises

### Exercise 1: Custom Range Iterator
Implement your own range function using an iterator class.

```python
class MyRange:
    # Your code here
    pass

for i in MyRange(1, 10, 2):
    print(i)  # 1, 3, 5, 7, 9
```

### Exercise 2: Chunk Iterator
Write an iterator that yields chunks of a given size from an iterable.

```python
def chunks(iterable, size):
    # Your code here
    pass

for chunk in chunks(range(10), 3):
    print(chunk)  # [0,1,2], [3,4,5], [6,7,8], [9]
```

### Exercise 3: Flatten Iterator
Write an iterator that flattens nested iterables.

```python
def flatten(nested):
    # Your code here
    pass

for item in flatten([1, [2, 3], [4, [5, 6]]]):
    print(item)  # 1, 2, 3, 4, 5, 6
```

---

## Summary

- **Iterators** implement `__iter__()` and `__next__()` methods
- **Iterables** have `__iter__()` and return an iterator
- **`iter()`** converts iterable to iterator
- **`next()`** gets next value (raises StopIteration when done)
- **Generators** are simplified iterators using `yield`
- **Lazy evaluation** generates values on demand
- **`itertools`** provides powerful iteration utilities
- **Generators are exhausted** after one pass
- **For loops** automatically handle StopIteration
