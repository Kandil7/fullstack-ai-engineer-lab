# Glossary: Introduction to Data Structures & Algorithms

> Quick reference for all terms introduced in Lecture 01.

---

## A

### Abstract Data Type (ADT)
- **Definition:** A theoretical model that specifies the behavior (operations and their semantics) of a data type without specifying the implementation.
- **Example:** A "Stack" ADT defines push/pop/peek operations with LIFO behavior, but doesn't say whether to use arrays or linked lists.
- **Related:** Data Structure, Interface, Encapsulation

```python
# Stack ADT — abstract specification
class StackADT:
    def push(self, item): ...   # Add to top
    def pop(self): ...          # Remove from top
    def peek(self): ...         # View top without removing
    def is_empty(self): ...     # Check if empty
```

### Algorithm
- **Definition:** A finite, well-defined sequence of instructions that solves a class of problems or performs a computation.
- **Example:** Binary search, merge sort, Dijkstra's shortest path.
- **Related:** Complexity, Big-O Notation, Procedure

```python
# Algorithm: Linear Search
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### Amortized Analysis
- **Definition:** Analyzing the average time per operation over a worst-case sequence of operations, rather than a single operation.
- **Example:** Python list `append()` is O(1) amortized — occasionally O(n) when resizing, but the average over many appends is O(1).
- **Related:** Average Case, Worst Case, Dynamic Array

```python
# Amortized O(1): occasional resize is "paid for" by many cheap appends
lst = []
for i in range(1000):
    lst.append(i)  # Most calls O(1), a few O(n), average O(1)
```

### Array
- **Definition:** A collection of elements stored at contiguous memory locations, accessible by index.
- **Example:** `[10, 20, 30, 40, 50]` — element at index 2 is 30.
- **Related:** Index, Contiguous Memory, Dynamic Array

```python
arr = [1, 2, 3, 4, 5]
print(arr[0])   # O(1) access — first element
print(arr[3])   # O(1) access — fourth element
```

---

## B

### Base Case
- **Definition:** The condition in a recursive function that stops the recursion, preventing infinite calls.
- **Example:** In factorial: `if n <= 1: return 1`
- **Related:** Recursion, Recursive Case, Stack Overflow

```python
def factorial(n):
    if n <= 1:          # Base case — stops recursion
        return 1
    return n * factorial(n - 1)  # Recursive case
```

### Best Case
- **Definition:** The scenario where an algorithm performs the minimum number of operations.
- **Example:** Binary search finding the target on the first check — O(1).
- **Related:** Worst Case, Average Case, Lower Bound

### Big-O Notation
- **Definition:** Mathematical notation describing the upper bound of an algorithm's growth rate as input size approaches infinity.
- **Example:** O(n), O(n²), O(log n), O(1).
- **Related:** Big-Theta, Big-Omega, Complexity Class

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

---

## C

### Constant Time — O(1)
- **Definition:** An operation that completes in the same amount of time regardless of input size.
- **Example:** Accessing an array element by index, pushing to a stack.
- **Related:** Big-O Notation, Time Complexity

```python
def get_first(lst):
    return lst[0]  # Always one operation, regardless of list size
```

### Contiguous Memory
- **Definition:** Memory layout where elements are stored in adjacent memory addresses.
- **Example:** C arrays and Python lists (backed by C arrays) use contiguous memory.
- **Related:** Array, Cache Locality, Pointer

---

## D

### Data Structure
- **Definition:** A concrete implementation of an ADT — the actual way data is organized, stored, and accessed in memory.
- **Example:** Python `list` is a data structure implementing the List ADT.
- **Related:** ADT, Implementation, Memory Layout

### Divide and Conquer
- **Definition:** An algorithm paradigm that breaks a problem into smaller subproblems, solves each recursively, and combines the results.
- **Example:** Merge sort, quicksort, binary search.
- **Related:** Recursion, Recurrence Relation, Merge Sort

```python
# Divide and Conquer: find max in unsorted list
def find_max(lst):
    if len(lst) == 1:          # Base case
        return lst[0]
    mid = len(lst) // 2        # Divide
    left_max = find_max(lst[:mid])
    right_max = find_max(lst[mid:])
    return max(left_max, right_max)  # Combine
```

---

## E

### Efficiency
- **Definition:** A measure of how well an algorithm uses resources (time and space) to solve a problem.
- **Example:** An O(n log n) sorting algorithm is more efficient than O(n²) for large inputs.
- **Related:** Time Complexity, Space Complexity, Optimization

---

## H

### Hash Table
- **Definition:** A data structure that maps keys to values using a hash function for O(1) average-time lookup, insertion, and deletion.
- **Example:** Python `dict` and `set` are hash table implementations.
- **Related:** Hash Function, Collision, Bucket

```python
# Hash table in action
lookup = {"alice": 90, "bob": 85}
print(lookup["alice"])  # O(1) average — hash("alice") → index → value
```

---

## I

### Immutable
- **Definition:** A value that cannot be changed after creation.
- **Example:** Python tuples, strings, and frozensets are immutable.
- **Related:** Mutable, Hashability, Tuple

```python
t = (1, 2, 3)
# t[0] = 5  # TypeError — tuples are immutable
```

### Index
- **Definition:** A numerical position used to access elements in a sequential data structure.
- **Example:** In `[10, 20, 30]`, index 0 → 10, index 1 → 20.
- **Related:** Array, Zero-Based Indexing, Key

---

## L

### Linear Data Structure
- **Definition:** A data structure where elements are arranged sequentially, and each element has at most one predecessor and one successor.
- **Example:** Array, linked list, stack, queue.
- **Related:** Non-Linear Data Structure, Sequential Access

### Logarithmic Time — O(log n)
- **Definition:** An algorithm that halves the search space with each step.
- **Example:** Binary search on a sorted array.
- **Related:** Binary Search, Divide and Conquer

```python
# O(log n): each step halves the problem
def log_example(n):
    while n > 1:
        n = n // 2  # Halving → log₂(n) steps total
```

---

## M

### Memory Complexity
- **Definition:** See Space Complexity.

### Mutable
- **Definition:** A value that can be changed after creation without creating a new object.
- **Example:** Python lists, dictionaries, and sets are mutable.
- **Related:** Immutable, In-Place Modification

```python
lst = [1, 2, 3]
lst[0] = 99  # OK — lists are mutable
```

---

## N

### Non-Linear Data Structure
- **Definition:** A data structure where elements may have multiple predecessors and/or successors.
- **Example:** Trees, graphs, heaps.
- **Related:** Linear Data Structure, Hierarchical

---

## P

### Polynomial Time
- **Definition:** An algorithm whose running time is bounded by a polynomial in the input size (O(n^k) for some constant k).
- **Example:** O(n), O(n²), O(n³) are all polynomial.
- **Related:** P Complexity Class, Exponential Time

---

## Q

### Quadratic Time — O(n²)
- **Definition:** An algorithm whose runtime grows proportionally to the square of the input size.
- **Example:** Bubble sort, selection sort, checking all pairs.
- **Related:** Nested Loops, Cubic Time

```python
# O(n²): nested loop over same input
def quadratic_example(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
```

---

## R

### Recursion
- **Definition:** A technique where a function calls itself with a smaller input until reaching a base case.
- **Example:** Factorial, Fibonacci, tree traversals.
- **Related:** Base Case, Recursive Case, Call Stack, Stack Overflow

```python
def fibonacci(n):
    if n <= 1:           # Base case
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Recursive case
```

---

## S

### Sequential Access
- **Definition:** Accessing elements one after another in order, starting from the first element.
- **Example:** Reading a linked list requires sequential access; arrays allow random access.
- **Related:** Random Access, Linked List, Iterator

### Space Complexity
- **Definition:** The amount of working memory (RAM) an algorithm needs relative to input size.
- **Example:** An algorithm using a temporary array of size n has O(n) space complexity.
- **Related:** Time Complexity, Auxiliary Space, In-Place

```python
# O(1) space — only uses a fixed number of variables
def in_place_reverse(lst):
    left, right = 0, len(lst) - 1
    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
```

### Stack
- **Definition:** A LIFO (Last In, First Out) data structure — elements are added and removed from the same end.
- **Example:** Undo button in text editors, function call stack.
- **Related:** Queue, Push, Pop, Peek

### Sublinear Time
- **Definition:** An algorithm that runs in less than O(n) time — it does not examine all inputs.
- **Example:** Binary search: O(log n).
- **Related:** Linear Time, Logarithmic Time

---

## T

### Time Complexity
- **Definition:** A measure of the number of operations an algorithm performs as a function of input size.
- **Example:** O(n) means operations grow linearly with input.
- **Related:** Space Complexity, Big-O Notation

---

## W

### Worst Case
- **Definition:** The scenario where an algorithm performs the maximum number of operations.
- **Example:** Linear search when the target is the last element or absent — O(n).
- **Related:** Best Case, Average Case, Upper Bound

---

## Quick Reference Table

| Term | Definition | Big-O | Python Example |
|------|-----------|-------|----------------|
| Constant | Fixed time regardless of size | O(1) | `lst[0]`, `d[key]` |
| Logarithmic | Halves problem each step | O(log n) | Binary search |
| Linear | Processes each element once | O(n) | `for x in lst` |
| Linearithmic | n × log n | O(n log n) | Merge sort |
| Quadratic | Nested loop over n | O(n²) | Bubble sort |
| Cubic | Triple nested loop | O(n³) | Naive matrix multiply |
| Exponential | Doubles with each addition | O(2ⁿ) | Subset enumeration |
| Factorial | All permutations | O(n!) | Brute-force TSP |

| Data Structure | Access | Search | Insert | Delete | Space |
|---------------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* | O(n) |
| Hash Table | — | O(1)† | O(1)† | O(1)† | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |

*At known position; †Average case
