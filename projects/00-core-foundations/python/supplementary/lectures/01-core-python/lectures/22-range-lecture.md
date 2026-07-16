# Python Range Function — Lecture 22

## Topic Overview

The `range()` function generates a sequence of numbers, commonly used for looping a specific number of times in for loops. It returns a **range object** — a memory-efficient sequence that generates numbers on demand rather than storing them all in memory.

Range is essential for numeric iteration, indexing loops, and creating sequences of numbers.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Use `range()` with one, two, and three arguments
- Understand range objects vs. lists
- Use range with negative steps
- Apply range in common patterns
- Understand when to use range vs. other iteration methods

---

## Key Concepts

### 1. Basic Range Usage

```python
# range(stop) — generates 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) — generates start to stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step) — with increment
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
```

### 2. Range Object vs. List

```python
# Range object — memory efficient
r = range(1000000)
print(type(r))  # <class 'range'>
print(len(r))   # 1000000
# r takes very little memory (just stores start, stop, step)

# Converting to list uses more memory
my_list = list(range(1000000))
# my_list stores all 1,000,000 integers in memory

# Check membership efficiently
print(5 in r)      # True — O(1)
print(5 in my_list) # True — O(n)
```

### 3. Negative Step

```python
# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1

# Reverse range
for i in range(10, 0, -2):
    print(i)  # 10, 8, 6, 4, 2
```

### 4. Common Patterns

```python
# Repeat N times
for _ in range(5):
    print("Hello!")

# Iterate with index
fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# Better: use enumerate
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# Create list of numbers
numbers = list(range(1, 11))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Even numbers
evens = list(range(0, 20, 2))  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Odd numbers
odds = list(range(1, 20, 2))  # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

# Powers of 2
powers = [2**i for i in range(10)]  # [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
```

### 5. Range Attributes

```python
r = range(2, 20, 3)
print(r.start)  # 2
print(r.stop)   # 20
print(r.step)   # 3

# Index and count
r = range(0, 10, 2)
print(r.index(6))  # 3 (index of value 6)
print(r.count(6))  # 1 (how many times 6 appears)
```

### 6. Range with Comprehensions

```python
# List comprehension with range
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Dict comprehension
square_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension
square_set = {x**2 for x in range(-5, 6)}
# {0, 1, 4, 9, 16, 25}

# Generator expression
sum_of_squares = sum(x**2 for x in range(100))
```

### 7. Range vs. Other Iteration

```python
# When to use range:
# 1. When you need the index
for i in range(len(items)):
    process(items[i], i)

# 2. When you need numeric sequences
for i in range(1, 101):
    print(i)

# 3. When you need to repeat
for _ in range(3):
    do_something()

# When NOT to use range (iterate directly):
for item in items:      # Better than range(len(items))
    process(item)

for char in "hello":    # Better than range(len("hello"))
    print(char)
```

---

## Code Examples

### Example 1: Generate Multiplication Table

```python
def multiplication_table(n, size=10):
    """Generate an n x n multiplication table."""
    table = []
    for i in range(1, size + 1):
        row = [i * j for j in range(1, size + 1)]
        table.append(row)
    return table

table = multiplication_table(5)
for row in table:
    print([f"{x:3d}" for x in row])
```

### Example 2: Sieve of Eratosthenes

```python
def sieve_of_eratosthenes(limit):
    """Find all primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(limit + 1) if is_prime[i]]

primes = sieve_of_eratosthenes(50)
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

### Example 3: Linear Interpolation

```python
def interpolate(start, end, steps):
    """Generate evenly spaced values between start and end."""
    step = (end - start) / (steps - 1)
    return [start + i * step for i in range(steps)]

# Generate 5 values between 0 and 1
values = interpolate(0, 1, 5)
print(values)  # [0.0, 0.25, 0.5, 0.75, 1.0]
```

### Example 4: Caesar Cipher with Range

```python
def caesar_cipher(text, shift):
    """Encrypt text using Caesar cipher."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Use modular arithmetic with range
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)

print(caesar_cipher("Hello, World!", 3))  # Khoor, Zruog!
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting range is Exclusive
```python
# WRONG — misses last value
for i in range(1, 5):
    print(i)  # 1, 2, 3, 4 (not 5!)

# CORRECT — use stop + 1
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5
```

### Mistake 2: Using Range Unnecessarily
```python
# WRONG — range with len is often unneeded
for i in range(len(my_list)):
    item = my_list[i]

# CORRECT — iterate directly
for item in my_list:
    process(item)
```

### Mistake 3: Large Range in Memory
```python
# This is fine — range is memory efficient
for i in range(1_000_000):
    process(i)

# Don't convert large ranges to lists
# my_list = list(range(1_000_000))  # Uses lots of memory!
```

---

## Best Practices

1. **Use range** for numeric iteration and counting
2. **Iterate directly** over collections when possible
3. **Use `_`** for unused loop variables: `for _ in range(5):`
4. **Remember range is exclusive** at the stop value
5. **Use step parameter** for non-sequential iteration
6. **Prefer enumerate** over `range(len(...))`
7. **Don't convert large ranges** to lists

---

## Practice Exercises

### Exercise 1: Sum of Range
Write a function that sums all numbers in a range.

```python
def sum_range(start, stop, step=1):
    # Your code here
    pass

# Expected: 55
print(sum_range(1, 11))
print(sum_range(0, 10, 2))  # 0+2+4+6+8 = 20
```

### Exercise 2: Generate Prime Range
Write a function that returns all primes in a given range.

```python
def primes_in_range(start, end):
    # Your code here
    pass

# Expected: [2, 3, 5, 7, 11, 13, 17, 19, 23]
print(primes_in_range(2, 25))
```

### Exercise 3: Fibonacci Range
Generate the first N Fibonacci numbers using range.

```python
def fibonacci_range(n):
    # Your code here
    pass

# Expected: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print(fibonacci_range(10))
```

---

## Summary

- **`range(stop)`** generates 0 to stop-1
- **`range(start, stop)`** generates start to stop-1
- **`range(start, stop, step)`** with custom increment
- **Range objects** are memory-efficient (not lists!)
- **Negative step** for counting backwards
- **Range is exclusive** at the stop value
- **Use for loops** and **comprehensions** with range
- **Don't convert large ranges** to lists
