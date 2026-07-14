# Glossary: Arrays

> Quick reference for all terms introduced in Lecture 02.

---

## A

### Access Time
- **Definition:** The time required to retrieve an element from a data structure.
- **Example:** Array access by index is O(1) — constant time.
- **Related:** Random Access, Sequential Access

```python
arr = [10, 20, 30]
print(arr[1])  # O(1) access — direct index lookup
```

### Amortized Analysis
- **Definition:** Average time per operation over a sequence of operations, accounting for occasional expensive operations.
- **Example:** `list.append()` is O(1) amortized — occasionally O(n) when the internal array resizes.
- **Related:** Dynamic Array, Resize

### Append
- **Definition:** Adding an element to the end of an array/list.
- **Time Complexity:** O(1) amortized for dynamic arrays.
- **Related:** Insert, Push

```python
lst = [1, 2, 3]
lst.append(4)  # [1, 2, 3, 4]
```

---

## B

### Binary Search
- **Definition:** A search algorithm that finds the position of a target in a sorted array by repeatedly dividing the search interval in half.
- **Time Complexity:** O(log n)
- **Related:** Sorted Array, Divide and Conquer, bisect

```python
import bisect

def binary_search(arr, target):
    idx = bisect.bisect_left(arr, target)
    return idx if idx < len(arr) and arr[idx] == target else -1
```

### Boundary
- **Definition:** The start and end positions of a sliding window or subarray.
- **Example:** In sliding window, the boundary is defined by `left` and `right` pointers.
- **Related:** Sliding Window, Two-Pointer

---

## C

### Contiguous Memory
- **Definition:** Elements stored in adjacent memory addresses, enabling O(1) access via index arithmetic.
- **Example:** `[10, 20, 30]` — element at address `base + i * size`.
- **Related:** Array, Cache Locality, Pointer

### Cursor
- **Definition:** A pointer or index tracking the current position during iteration or traversal.
- **Example:** In binary search, `low` and `high` are cursors defining the search range.
- **Related:** Pointer, Index, Two-Pointer

```python
# Binary search with cursors
low, high = 0, len(arr) - 1
while low <= high:
    mid = (low + high) // 2
    # ... adjust low or high
```

---

## D

### Dynamic Array
- **Definition:** A resizable array that automatically grows (and sometimes shrinks) as elements are added or removed.
- **Example:** Python `list`, Java `ArrayList`, C++ `std::vector`.
- **Related:** Static Array, Resize, Amortized

```python
# Python list is a dynamic array
lst = []
for i in range(100):
    lst.append(i)  # Internally resizes as needed
```

### Dutch National Flag
- **Definition:** A three-way partitioning algorithm that sorts an array of three distinct values in a single pass.
- **Example:** Sorting `[0, 1, 2, 0, 1, 2]` into `[0, 0, 1, 1, 2, 2]`.
- **Related:** Three-Way Partition, Quick Sort

```python
def dutch_flag_sort(arr):
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1; mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
```

---

## E

### Element
- **Definition:** A single value or object stored in a data structure.
- **Example:** In `[10, 20, 30]`, `20` is an element at index 1.
- **Related:** Index, Value, Item

---

## I

### Index
- **Definition:** The position of an element in an array, typically starting from 0.
- **Example:** In `["a", "b", "c"]`, index 0 → "a", index 2 → "c".
- **Related:** Zero-Based Indexing, Key

```python
arr = ["apple", "banana", "cherry"]
print(arr[0])  # "apple" — index 0
print(arr[-1]) # "cherry" — negative index from end
```

### In-Place
- **Definition:** An algorithm that uses O(1) extra space, modifying the input directly.
- **Example:** Reversing an array using two pointers is in-place.
- **Related:** Space Complexity, Two-Pointer

```python
# In-place reversal
def reverse_inplace(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1; right -= 1
```

### Insert
- **Definition:** Adding an element at a specific position in an array.
- **Time Complexity:** O(n) worst case (shifting elements).
- **Related:** Append, Push, Delete

```python
arr = [1, 2, 4, 5]
arr.insert(2, 3)  # [1, 2, 3, 4, 5] — O(n) due to shifting
```

---

## L

### Linear Search
- **Definition:** Sequentially checking each element until the target is found or the end is reached.
- **Time Complexity:** O(n)
- **Related:** Binary Search, Search

```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

---

## M

### Merge
- **Definition:** Combining two or more sorted arrays/sequences into one sorted sequence.
- **Time Complexity:** O(n + m) for two arrays of sizes n and m.
- **Related:** Merge Sort, Two-Pointer

```python
def merge_sorted(arr1, arr2):
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i]); i += 1
        else:
            result.append(arr2[j]); j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

---

## P

### Preallocate
- **Definition:** Allocating memory for a known number of elements before filling the array, avoiding repeated resizing.
- **Example:** `arr = [0] * n` instead of repeated `append()`.
- **Related:** Dynamic Array, Resize

```python
# Preallocate — faster for known size
n = 1000
arr = [0] * n  # Single allocation

# vs. repeated append (causes multiple resizes)
arr = []
for i in range(n):
    arr.append(i)  # Multiple allocations during resize
```

---

## R

### Random Access
- **Definition:** The ability to access any element directly in O(1) time using its index.
- **Example:** `arr[5]` directly accesses the 6th element.
- **Related:** Sequential Access, Array, Index

### Resize
- **Definition:** Allocating a new, larger (or smaller) backing array and copying elements when capacity is exceeded.
- **Example:** Python list doubles capacity when full.
- **Related:** Dynamic Array, Amortized, Capacity

```
Capacity growth strategy (Python):
[0] → [0, 0] → [0, 0, 0, 0] → [0, 0, 0, 0, 0, 0, 0, 0]
Size:  1          4                 8
```

---

## S

### Sliding Window
- **Definition:** A technique using two pointers to maintain a "window" over a contiguous section of an array.
- **Example:** Finding the maximum sum subarray of size k.
- **Related:** Two-Pointer, Subarray, Window Size

```python
def sliding_window_max_sum(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Slide: add right, remove left
        max_sum = max(max_sum, window_sum)
    return max_sum
```

### Static Array
- **Definition:** An array with a fixed size determined at creation time, which cannot be resized.
- **Example:** C arrays: `int arr[5];`
- **Related:** Dynamic Array, Fixed Size

### Subarray
- **Definition:** A contiguous sequence of elements within an array.
- **Example:** In `[1, 2, 3, 4, 5]`, `[2, 3, 4]` is a subarray (indices 1-3).
- **Note:** Subarray must be contiguous; a non-contiguous subset is a "subsequence."
- **Related:** Subsequence, Sliding Window, Window

```python
arr = [1, 2, 3, 4, 5]
# Subarrays: [1], [1,2], [1,2,3], [2], [2,3], [3,4,5], etc.
# Subsequences: [1,3,5], [2,4] — non-contiguous OK
```

### Subsequence
- **Definition:** A sequence derived from an array by deleting some or no elements without changing the order.
- **Example:** In `[1, 2, 3, 4, 5]`, `[1, 3, 5]` is a subsequence.
- **Related:** Subarray, Contiguous

---

## T

### Two-Pointer
- **Definition:** A technique using two indices that move toward each other (or in the same direction) to solve problems in O(n) time.
- **Example:** Finding a pair sum in a sorted array, removing duplicates in-place.
- **Related:** Sliding Window, Binary Search

```python
def two_pointer_pair_sum(arr, target):
    """Find pair with given sum in sorted array."""
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
```

---

## Z

### Zero-Based Indexing
- **Definition:** Numbering array indices starting from 0 instead of 1.
- **Example:** `[10, 20, 30]` — index 0 is 10, index 2 is 30.
- **Related:** Index, Array

---

## Quick Reference Table

| Term | Definition | Complexity | Example |
|------|-----------|-----------|---------|
| Access | Retrieve element by index | O(1) | `arr[3]` |
| Search (unsorted) | Find element in unsorted array | O(n) | `30 in arr` |
| Search (sorted) | Find element in sorted array | O(log n) | Binary search |
| Insert (end) | Add element to end | O(1)* | `arr.append(x)` |
| Insert (beginning) | Add element to start | O(n) | `arr.insert(0, x)` |
| Delete (end) | Remove last element | O(1) | `arr.pop()` |
| Delete (beginning) | Remove first element | O(n) | `arr.pop(0)` |
| Two-Pointer | Scan from both ends | O(n) | Pair sum in sorted array |
| Sliding Window | Maintain window over subarray | O(n) | Max sum subarray |
| Binary Search | Halve search space | O(log n) | Search in sorted array |

*Amortized
