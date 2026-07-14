# Lecture 01: Introduction to Data Structures & Algorithms

## Topic Overview

Data Structures and Algorithms (DSA) form the backbone of computer science and software engineering. A **data structure** is a specialized format for organizing, processing, retrieving, and storing data efficiently. An **algorithm** is a finite sequence of well-defined instructions that solves a specific problem or performs a computation.

Understanding DSA is essential because:
- It determines how efficiently your programs use time and memory
- It enables you to solve complex problems systematically
- It is the foundation for technical interviews at top companies
- It separates competent programmers from excellent ones

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Define** what data structures and algorithms are and why they matter
2. **Classify** data structures into linear and non-linear categories
3. **Explain** Big-O notation and analyze time/space complexity
4. **Differentiate** between best, average, and worst-case scenarios
5. **Measure** algorithmic complexity using counting techniques
6. **Apply** complexity analysis to choose the right data structure
7. **Implement** basic Python data structure operations
8. **Identify** common complexity patterns in everyday code

---

## Key Concepts

### 1. What Are Data Structures?

A data structure is a way of organizing data in memory so that it can be used efficiently. Different data structures are suited to different kinds of applications, and some are highly specialized for specific tasks.

**Example in everyday life:**
- A **library catalog** organizes books so you can find one quickly (hash table analogy)
- A **stack of plates** — you add and remove from the top (stack analogy)
- A **family tree** — hierarchical relationships (tree analogy)
- A **subway map** — stations connected by lines (graph analogy)

```python
# Python provides built-in data structures:
# Lists, Tuples, Sets, Dictionaries

# List (dynamic array)
fruits = ["apple", "banana", "cherry"]

# Tuple (immutable sequence)
coordinates = (10.0, 20.0)

# Set (unordered, unique elements)
unique_ids = {101, 102, 103}

# Dictionary (key-value pairs)
student = {"name": "Alice", "age": 22, "gpa": 3.8}
```

### 2. What Are Algorithms?

An algorithm is a step-by-step procedure for solving a problem. Good algorithms have these properties:

| Property       | Description                                      |
|----------------|--------------------------------------------------|
| **Finiteness** | Must terminate after a finite number of steps     |
| **Definiteness**| Each step must be precisely defined               |
| **Input**      | Zero or more inputs                               |
| **Output**     | One or more outputs                               |
| **Effectiveness**| Steps must be basic enough to be carried out      |

```python
# Simple algorithm: Find the maximum in a list
def find_maximum(numbers):
    """Algorithm to find the maximum value in a list."""
    if not numbers:                    # Handle edge case
        return None
    
    max_value = numbers[0]             # Step 1: Assume first is max
    for num in numbers[1:]:            # Step 2: Compare each element
        if num > max_value:            # Step 3: Update if larger
            max_value = num
    return max_value                   # Step 4: Return result

# Time complexity: O(n) — we examine each element once
print(find_maximum([3, 7, 2, 9, 1]))  # Output: 9
```

### 3. Classification of Data Structures

```
Data Structures
├── Linear
│   ├── Array
│   ├── Linked List
│   ├── Stack
│   ├── Queue
│   └── Hash Table (sometimes classified as non-linear)
│
├── Non-Linear
│   ├── Tree
│   │   ├── Binary Tree
│   │   ├── Binary Search Tree
│   │   ├── AVL Tree
│   │   ├── Red-Black Tree
│   │   └── Heap
│   └── Graph
│       ├── Directed / Undirected
│       ├── Weighted / Unweighted
│       └── Cyclic / Acyclic
│
└── Abstract Data Types (ADTs)
    ├── List
    ├── Stack
    ├── Queue
    ├── Map / Dictionary
    └── Set
```

**Key Distinction:** A data structure is a concrete implementation; an ADT is an abstract specification. A "stack" is an ADT (LIFO behavior), while "array-based stack" or "linked-list stack" are data structures.

### 4. Big-O Notation

Big-O notation describes the upper bound of an algorithm's growth rate. It tells us how the runtime or space requirements grow as the input size grows.

#### Common Complexity Classes (Best to Worst)

| Big-O          | Name            | Example                        | Input Size 10⁶ |
|----------------|-----------------|--------------------------------|-----------------|
| O(1)           | Constant        | Array index access             | 1 operation     |
| O(log n)       | Logarithmic     | Binary search                  | ~20 operations  |
| O(n)           | Linear          | Simple search                  | 10⁶ operations  |
| O(n log n)     | Linearithmic    | Merge sort                     | ~2×10⁷ ops     |
| O(n²)          | Quadratic       | Bubble sort                    | 10¹² operations |
| O(n³)          | Cubic           | Matrix multiplication          | 10¹⁸ operations |
| O(2ⁿ)          | Exponential     | Subset enumeration             | ∞               |
| O(n!)          | Factorial       | Permutation generation         | ∞               |

```python
# O(1) — Constant Time
def get_first元素(lst):
    return lst[0]  # No matter the size, this is one operation

# O(n) — Linear Time
def linear_search(lst, target):
    for item in lst:          # Loops through all n elements
        if item == target:
            return True
    return False

# O(n²) — Quadratic Time
def bubble_sort(lst):
    n = len(lst)
    for i in range(n):              # n iterations
        for j in range(n - 1):      # n iterations each
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

# O(log n) — Logarithmic Time
def binary_search(sorted_lst, target):
    low, high = 0, len(sorted_lst) - 1
    while low <= high:              # Halves search space each time
        mid = (low + high) // 2
        if sorted_lst[mid] == target:
            return mid
        elif sorted_lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

### 5. Time Complexity Analysis

#### How to Count Operations

```python
# Example 1: Single loop — O(n)
def example_1(n):
    count = 0
    for i in range(n):       # Runs n times
        count += 1            # Constant time operation
    return count              # Total: O(n)

# Example 2: Nested loops — O(n²)
def example_2(n):
    count = 0
    for i in range(n):       # Outer: n times
        for j in range(n):   # Inner: n times
            count += 1        # Total: n × n = n²
    return count

# Example 3: Sequential operations — Add complexities
def example_3(n):
    # Block A: O(n)
    for i in range(n):
        print(i)
    
    # Block B: O(n²)
    for i in range(n):
        for j in range(n):
            print(i, j)
    
    # Total: O(n) + O(n²) = O(n²)  (dominant term wins)

# Example 4: Independent loops — Take the maximum
def example_4(n):
    # Block A: O(n)
    for i in range(n):
        print(i)
    
    # Block B: O(n³)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                print(i, j, k)
    
    # Total: max(O(n), O(n³)) = O(n³)
```

#### Rules for Simplifying Big-O

1. **Drop constants:** O(2n) → O(n), O(n²/2) → O(n²)
2. **Drop lower-order terms:** O(n² + n) → O(n²)
3. **Different inputs = different variables:** O(a + b), not O(n)
4. **Sequential code:** Take the maximum of all blocks
5. **Nested code:** Multiply the complexities

### 6. Space Complexity

Space complexity measures how much memory an algorithm uses relative to input size.

```python
# O(1) Space — Constant extra space
def sum_list(lst):
    total = 0              # One variable, regardless of input size
    for num in lst:
        total += num
    return total

# O(n) Space — Linear extra space
def create_copy(lst):
    copy = []              # Creates a new list of size n
    for num in lst:
        copy.append(num)
    return copy

# O(n) Space — Recursive call stack
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # n recursive calls on the stack
```

### 7. Best, Average, and Worst Case

```python
# Linear Search Analysis
def linear_search_analysis(lst, target):
    """
    Best case:  Target is first element     → O(1)
    Worst case: Target is last or absent     → O(n)
    Average case: Target is somewhere middle  → O(n/2) = O(n)
    """
    for i, item in enumerate(lst):
        if item == target:
            return i
    return -1

# Binary Search Analysis
def binary_search_analysis(lst, target):
    """
    Best case:  Target is at midpoint       → O(1)
    Worst case: Target not found             → O(log n)
    Average case: ~log n comparisons         → O(log n)
    """
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

### 8. Amortized Analysis

Some operations are occasionally expensive but cheap on average. Dynamic array resizing is the classic example.

```python
# Python list append — Amortized O(1)
"""
When a Python list (backed by a C array) runs out of capacity:
1. A new, larger array is allocated (typically 2x the old size)
2. All elements are copied over
3. The old array is freed

Individual append: O(1) usually, O(n) during resize
Amortized append: O(1) — because resize happens rarely enough
"""

# Demonstration of amortized behavior
import sys

lst = []
prev_size = sys.getsizeof(lst)

for i in range(64):
    lst.append(i)
    new_size = sys.getsizeof(lst)
    if new_size != prev_size:
        print(f"Size changed at i={i}: {prev_size} → {new_size} bytes")
        prev_size = new_size
```

---

## Complete Code Examples

```python
"""
Complete Example: Analyzing Multiple Algorithms
"""

import time
import random

def measure_time(func, *args, iterations=10):
    """Measure average execution time of a function."""
    total = 0
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        total += (end - start)
    return total / iterations

# === Algorithm 1: Finding duplicate pairs — O(n²) ===
def find_duplicates_quadratic(lst):
    """Find all pairs of duplicates. O(n²) time, O(1) space."""
    duplicates = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                duplicates.append((lst[i], lst[j]))
    return duplicates

# === Algorithm 2: Finding duplicates with a set — O(n) ===
def find_duplicates_linear(lst):
    """Find all pairs of duplicates. O(n) time, O(n) space."""
    seen = {}
    duplicates = []
    for item in lst:
        if item in seen:
            duplicates.append((item, item))
        else:
            seen[item] = True
    return duplicates

# Compare performance
sizes = [100, 500, 1000, 2000]
print("Size | O(n²) time    | O(n) time     | Speedup")
print("-" * 55)

for size in sizes:
    data = [random.randint(0, size // 2) for _ in range(size)]
    
    t_quadratic = measure_time(find_duplicates_quadratic, data, iterations=5)
    t_linear = measure_time(find_duplicates_linear, data, iterations=5)
    speedup = t_quadratic / t_linear if t_linear > 0 else float('inf')
    
    print(f"{size:5d} | {t_quadratic:11.6f}s | {t_linear:11.6f}s | {speedup:.1f}x")
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing Big-O with Exact Runtime
```python
# WRONG: "O(100n) is worse than O(n²)"
# RIGHT: Drop constants — O(100n) = O(n), which is BETTER than O(n²)
```

### Mistake 2: Ignoring Input Size
```python
# WRONG: "O(n²) is always bad"
# For n=10, O(n²)=100 operations — perfectly fine!
# Big-O tells you how it SCALES, not whether it's fast for your case.
```

### Mistake 3: Forgetting About Space
```python
# A function can be O(n) time but O(n²) space
def create_pairs_matrix(lst):
    """Time: O(n²), Space: O(n²) — stores n×n matrix"""
    matrix = []
    for i in lst:
        row = []
        for j in lst:
            row.append((i, j))
        matrix.append(row)
    return matrix
```

### Mistake 4: Miscounting Nested Loops
```python
# This is O(n), NOT O(n²):
for i in range(n):
    for j in range(10):  # Fixed constant, not n!
        print(i, j)

# This IS O(n²):
for i in range(n):
    for j in range(i):  # j grows with i → n(n-1)/2
        print(i, j)
```

### Mistake 5: Assuming Python Operations Are Free
```python
# "in" on a list is O(n), not O(1)!
if target in large_list:  # Scans the entire list
    pass

# "in" on a set is O(1) average
if target in large_set:   # Hash lookup
    pass
```

---

## Best Practices

1. **Always analyze before optimizing.** Profile first, optimize second.
2. **Choose the right data structure for the job.** Don't use a list where a set would be faster.
3. **Understand the trade-offs.** O(n) time with O(n) space vs. O(n²) time with O(1) space — which is better depends on constraints.
4. **Use Python's built-in data structures.** They are implemented in C and highly optimized.
5. **Write clear code first, then optimize.** Premature optimization is the root of all evil.
6. **Test with realistic data sizes.** An O(n²) algorithm may be faster for small n.
7. **Know your common patterns.** Two-pointer, sliding window, divide-and-conquer, etc.

---

## Practice Exercises

### Exercise 1: Complexity Identification
For each snippet, determine the time and space complexity:

```python
# Snippet A
def mystery_a(n):
    for i in range(n):
        for j in range(n, 0, -1):
            print(i + j)

# Snippet B
def mystery_b(n):
    i = n
    while i > 1:
        i = i // 2
        print(i)

# Snippet C
def mystery_c(lst):
    result = []
    for item in lst:
        if item not in result:  # result is a list
            result.append(item)
    return result
```

### Exercise 2: Complexity Comparison
You have two algorithms for the same problem:
- Algorithm A: O(n²) time, O(1) space
- Algorithm B: O(n log n) time, O(n) space

For which input sizes would you prefer Algorithm A? Why?

### Exercise 3: Improve This Code
```python
def has_common_element(list1, list2):
    """Check if two lists have any common element."""
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                return True
    return False
# Current: O(n²) — Can you make it O(n)?
```

---

## Summary

| Concept               | Key Takeaway                                            |
|-----------------------|---------------------------------------------------------|
| **Data Structure**    | A way to organize data for efficient access             |
| **Algorithm**         | A step-by-step procedure to solve a problem             |
| **Big-O Notation**    | Describes how runtime grows with input size             |
| **Time Complexity**   | How many operations an algorithm performs                |
| **Space Complexity**  | How much memory an algorithm uses                       |
| **Best/Worst/Average**| Different scenarios for the same algorithm              |
| **Amortized**         | Average performance over a sequence of operations       |

**Key Insight:** The goal of DSA is not to memorize algorithms but to understand the *thinking patterns* that let you solve new problems efficiently.

**Next Lecture:** We dive into Arrays — the most fundamental data structure, and explore how Python implements lists under the hood.
