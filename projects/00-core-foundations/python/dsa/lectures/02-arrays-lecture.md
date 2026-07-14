# Lecture 02: Arrays

## Topic Overview

Arrays are the most fundamental data structure in computer science. They store elements in contiguous memory locations, enabling constant-time access via indexing. While Python's `list` is technically a dynamic array (resizable), understanding the underlying array concept is critical for mastering all other data structures.

This lecture covers array fundamentals, operations, Python's list internals, and classic array problems.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** how arrays work at the memory level
2. **Implement** core array operations (insert, delete, search, rotate)
3. **Analyze** the time/space complexity of array operations
4. **Use** Python's list methods effectively with awareness of their costs
5. **Solve** classic array problems (two-sum, rotate, reverse, merge)
6. **Apply** techniques like two-pointer and sliding window
7. **Identify** when arrays are the right choice vs. alternatives

---

## Key Concepts

### 1. What Is an Array?

An array is a collection of elements stored at contiguous (adjacent) memory addresses. Each element can be accessed directly using its index.

```
Memory Layout of Array [10, 20, 30, 40, 50]:

Address:  1000   1004   1008   1012   1016
Value:    [10]   [20]   [30]   [40]   [50]
Index:      0      1      2      3      4

Element at index i is at address: base_address + i × element_size
```

**Key properties:**
- **Fixed size** (static arrays) or **dynamic resizing** (dynamic arrays)
- **Random access** — any element in O(1)
- **Homogeneous** — typically stores elements of the same type
- **Zero-indexed** in most languages (including Python)

### 2. Static vs. Dynamic Arrays

```python
# Static array (conceptual — C-style, fixed size)
# In C: int arr[5] = {10, 20, 30, 40, 50};  — cannot resize

# Dynamic array (Python list) — auto-resizes
arr = [10, 20, 30]
arr.append(40)   # Automatically resizes if needed
arr.append(50)   # Python handles memory management
```

#### How Dynamic Arrays Resize

```
Initial capacity: 4
[10, 20, 30, 40] — full!

Append 50:
Step 1: Allocate new array of size 8 (2× capacity)
[_, _, _, _, _, _, _, _]
Step 2: Copy all elements
[10, 20, 30, 40, _, _, _, _]
Step 3: Insert new element
[10, 20, 30, 40, 50, _, _, _]
```

### 3. Array Operations & Complexities

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| Access (by index) | O(1) | Direct memory address calculation |
| Search (unsorted) | O(n) | Must check each element |
| Search (sorted) | O(log n) | Binary search possible |
| Insert at end | O(1) amortized | May trigger resize |
| Insert at beginning | O(n) | Must shift all elements |
| Insert at position | O(n) | Must shift elements after position |
| Delete at end | O(1) | No shifting needed |
| Delete at beginning | O(n) | Must shift all elements |
| Delete at position | O(n) | Must shift elements after position |

### 4. Python List Internals

Python's `list` is implemented as a **dynamic array of pointers** to objects.

```python
import sys

# List stores pointers, not values directly
lst = [1, 2, 3, 4, 5]
print(sys.getsizeof(lst))       # Size of the list object itself
print(sys.getsizeof(lst[0]))    # Size of integer object 1

# Small integer caching
a = 256
b = 256
print(a is b)  # True — Python caches small integers

a = 257
b = 257
print(a is b)  # May be False — different objects in memory
```

**Memory layout of Python list:**
```
list object
├── ob_size: 5          (number of elements)
├── allocated: 8        (capacity — may be larger than ob_size)
└── ob_item: → [ptr0, ptr1, ptr2, ptr3, ptr4, _, _, _]
                 ↓      ↓      ↓      ↓      ↓
               [1]    [2]    [3]    [4]    [5]    (PyObject in heap)
```

### 5. Essential Array Operations in Python

```python
# === CREATION ===
arr1 = [1, 2, 3, 4, 5]            # List literal
arr2 = list(range(10))             # [0, 1, 2, ..., 9]
arr3 = [0] * 10                    # [0, 0, 0, ..., 0] (10 zeros)
arr4 = [[0] * 3 for _ in range(3)] # 3×3 zero matrix

# === ACCESS & MODIFICATION ===
arr = [10, 20, 30, 40, 50]
print(arr[0])      # 10 — O(1)
print(arr[-1])     # 50 — O(1) — last element
arr[2] = 99        # [10, 20, 99, 40, 50] — O(1)

# === INSERTION ===
arr.append(60)          # End: O(1) amortized
arr.insert(0, 5)        # Beginning: O(n) — shifts everything
arr.insert(3, 35)       # Middle: O(n) — shifts after index 3

# === DELETION ===
arr.pop()               # End: O(1)
arr.pop(0)              # Beginning: O(n) — shifts everything
arr.remove(35)          # By value: O(n) — search + shift

# === SEARCHING ===
arr = [10, 20, 30, 40, 50]
print(30 in arr)        # O(n) — linear search
print(arr.index(30))    # O(n) — returns first index of value
print(arr.count(20))    # O(n) — counts occurrences

# === SLICING ===
sub = arr[1:4]          # [20, 30, 40] — O(k) where k is slice size
sub = arr[::2]          # [10, 30, 50] — every other element
sub = arr[::-1]         # [50, 40, 30, 20, 10] — reversed copy

# === SORTING ===
arr = [3, 1, 4, 1, 5, 9]
arr.sort()              # In-place sort: O(n log n)
arr.sort(reverse=True)  # Descending sort
sorted_arr = sorted(arr)  # Returns new sorted list: O(n log n)
```

---

## Complete Code Examples

### Example 1: Two Sum Problem

```python
"""
Given an array of integers and a target, find two numbers that add up to the target.

Approach 1: Brute Force — O(n²) time, O(1) space
Approach 2: Hash Map — O(n) time, O(n) space
"""
def two_sum_brute(nums, target):
    """Brute force: check every pair."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

def two_sum_hashmap(nums, target):
    """Hash map: O(n) time by complement lookup."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
nums = [2, 7, 11, 15]
target = 9
print(two_sum_brute(nums, target))     # [0, 1]
print(two_sum_hashmap(nums, target))   # [0, 1]
```

### Example 2: Rotate Array

```python
"""
Rotate an array to the right by k steps.
Example: [1,2,3,4,5,6,7] rotated by 3 → [5,6,7,1,2,3,4]

Approach 1: Extra array — O(n) time, O(n) space
Approach 2: In-place reversal — O(n) time, O(1) space
"""

def rotate_extra_array(nums, k):
    """Use an extra array to place each element correctly."""
    n = len(nums)
    rotated = [0] * n
    for i in range(n):
        rotated[(i + k) % n] = nums[i]
    return rotated

def rotate_inplace(nums, k):
    """Reverse technique — O(1) space."""
    n = len(nums)
    k = k % n  # Handle k > n
    
    def reverse(arr, start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
    
    # Step 1: Reverse entire array
    reverse(nums, 0, n - 1)
    # Step 2: Reverse first k elements
    reverse(nums, 0, k - 1)
    # Step 3: Reverse remaining elements
    reverse(nums, k, n - 1)

# Test
nums = [1, 2, 3, 4, 5, 6, 7]
rotate_inplace(nums, 3)
print(nums)  # [5, 6, 7, 1, 2, 3, 4]
```

### Example 3: Sliding Window — Max Sum Subarray

```python
"""
Find the maximum sum of a contiguous subarray of size k.

Approach 1: Brute force — O(n×k) time
Approach 2: Sliding window — O(n) time, O(1) space
"""

def max_sum_subarray_brute(arr, k):
    """Check every possible window of size k."""
    max_sum = float('-inf')
    for i in range(len(arr) - k + 1):
        window_sum = sum(arr[i:i+k])  # O(k) each time
        max_sum = max(max_sum, window_sum)
    return max_sum

def max_sum_subarray_sliding(arr, k):
    """Sliding window — remove left element, add right element."""
    # Compute first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# Test
arr = [2, 1, 5, 1, 3, 2]
k = 3
print(max_sum_subarray_sliding(arr, k))  # 9 (subarray [5, 1, 3])
```

### Example 4: Two-Pointer Technique

```python
"""
Find two numbers in a SORTED array that sum to a target.
Returns their indices (1-based).

Two-Pointer: O(n) time, O(1) space
"""

def two_sum_sorted(arr, target):
    """Two pointers: one from start, one from end."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left + 1, right + 1]  # 1-based
        elif current_sum < target:
            left += 1    # Need larger sum → move left pointer right
        else:
            right -= 1   # Need smaller sum → move right pointer left
    
    return []

# Test
arr = [1, 2, 3, 4, 6]
target = 6
print(two_sum_sorted(arr, target))  # [1, 3] → arr[0]+arr[2] = 1+5 = 6
```

### Example 5: Dutch National Flag (3-Way Partition)

```python
"""
Sort an array of 0s, 1s, and 2s in a single pass.
Dutch National Flag problem — O(n) time, O(1) space.

Uses three pointers:
- low: boundary for 0s (everything before low is 0)
- mid: current element being examined
- high: boundary for 2s (everything after high is 2)
"""

def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # Don't increment mid — swapped element needs checking

# Test
arr = [2, 0, 2, 1, 1, 0]
sort_colors(arr)
print(arr)  # [0, 0, 1, 1, 2, 2]
```

---

## Common Mistakes to Avoid

### Mistake 1: Off-by-One Errors
```python
# WRONG: Missing the last element
for i in range(len(arr) - 1):  # Stops at len-2!
    print(arr[i])

# RIGHT: Include all elements
for i in range(len(arr)):
    print(arr[i])

# Or more Pythonic:
for item in arr:
    print(item)
```

### Mistake 2: Modifying a List While Iterating
```python
# WRONG: Skipping elements
lst = [1, 2, 3, 4, 5]
for item in lst:
    if item % 2 == 0:
        lst.remove(item)  # Dangerous! Skips elements

# RIGHT: Use list comprehension
lst = [item for item in lst if item % 2 != 0]

# Or iterate over a copy
for item in lst[:]:  # lst[:] creates a shallow copy
    if item % 2 == 0:
        lst.remove(item)
```

### Mistake 3: Confusing `is` with `==`
```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True — same values
print(a is b)   # False — different objects in memory

# For checking None:
x = None
print(x is None)     # Correct
print(x == None)     # Works but not Pythonic
```

### Mistake 4: Using `in` for Sorted Arrays
```python
# WRONG: Linear search on sorted array — O(n)
if target in sorted_arr:
    pass

# RIGHT: Binary search — O(log n)
import bisect
idx = bisect.bisect_left(sorted_arr, target)
if idx < len(sorted_arr) and sorted_arr[idx] == target:
    pass
```

### Mistake 5: Creating Unnecessary Copies
```python
# WRONG: O(n) extra space for no reason
result = list(arr)  # Copies entire list
result.sort()

# RIGHT: Sort in-place if you don't need original
arr.sort()  # O(1) extra space
```

---

## Best Practices

1. **Use slicing for subarrays:** `arr[start:end]` is clean and efficient
2. **Prefer list comprehensions** over manual loops for filtering/transformation
3. **Use `enumerate()`** when you need both index and value
4. **Use `bisect` module** for sorted array operations
5. **Preallocate when size is known:** `[0] * n` is faster than repeated `append()`
6. **Avoid inserting/deleting at the beginning** — O(n) due to shifting
7. **Use `collections.deque`** when you need frequent insert/delete at both ends

---

## Practice Exercises

### Exercise 1: Remove Duplicates from Sorted Array
```python
def remove_duplicates(nums):
    """
    Remove duplicates in-place, return new length.
    Input: [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
    """
    # Your solution here — O(n) time, O(1) space
    pass
```

### Exercise 2: Merge Two Sorted Arrays
```python
def merge_sorted(arr1, arr2):
    """
    Merge two sorted arrays into one sorted array.
    Input: [1,3,5], [2,4,6]
    Output: [1,2,3,4,5,6]
    """
    # Your solution here — O(n+m) time
    pass
```

### Exercise 3: Best Time to Buy and Sell Stock
```python
def max_profit(prices):
    """
    Find the maximum profit from buying and selling once.
    Input: [7,1,5,3,6,4]
    Output: 5 (buy at 1, sell at 6)
    """
    # Your solution here — O(n) time, O(1) space
    pass
```

### Exercise 4: Container With Most Water
```python
def max_area(height):
    """
    Find two lines that together with the x-axis form a container
    holding the most water.
    Input: [1,8,6,2,5,4,8,3,7]
    Output: 49
    """
    # Your solution here — O(n) time using two pointers
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Array** | Contiguous memory, O(1) random access |
| **Dynamic Array** | Auto-resizing (amortized O(1) append) |
| **Insert/Delete** | O(n) at arbitrary positions due to shifting |
| **Two-Pointer** | O(n) for sorted array problems |
| **Sliding Window** | O(n) for contiguous subarray problems |
| **Python List** | Dynamic array of pointers — flexible but has overhead |

**Key Insight:** Arrays are simple but powerful. Mastering array manipulation techniques (two-pointer, sliding window, sorting) unlocks solutions to hundreds of interview problems.

**Next Lecture:** Stacks — a LIFO data structure built on arrays with powerful applications in expression parsing and backtracking.
