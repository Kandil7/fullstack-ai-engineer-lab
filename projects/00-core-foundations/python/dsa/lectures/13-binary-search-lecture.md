# Lecture 13: Binary Search

## Learning Objectives

By the end of this lecture, you will be able to:
- Understand the divide-and-conquer principle behind binary search
- Implement iterative and recursive binary search
- Analyze time and space complexity of binary search
- Recognize when binary search is applicable versus linear search
- Handle edge cases in binary search implementations
- Apply binary search to solve real-world problems

---

## 1. Introduction

Binary search is one of the most powerful and fundamental search algorithms. While linear search examines every element, binary search repeatedly divides the search space in half, achieving logarithmic time complexity. This makes it exponentially faster than linear search for large datasets.

**The Core Idea**: If the data is sorted, you can eliminate half the remaining possibilities with each comparison.

**Why It Matters**:
- Searching 1 billion elements takes only ~30 comparisons
- Foundation for many advanced algorithms
- Demonstrates the power of divide-and-conquer thinking
- Required knowledge for virtually every technical interview

---

## 2. The Divide-and-Conquer Principle

Binary search operates on a simple principle:

```
1. Compare the target with the middle element
2. If equal: found it
3. If target < middle: search the left half
4. If target > middle: search the right half
5. Repeat until found or search space is empty
```

**Visual Example**: Searching for 7 in sorted array [1, 3, 5, 7, 9, 11, 13]

```
Step 1: [1, 3, 5, 7, 9, 11, 13]
         L        M        R
         mid = 5, target = 7, 7 > 5 → search right

Step 2:              [7, 9, 11, 13]
                     L     M     R
                     mid = 9, target = 7, 7 < 9 → search left

Step 3:              [7]
                     L=M=R
                     mid = 7, found!
```

**Key Requirement**: Data MUST be sorted. Binary search on unsorted data produces incorrect results.

---

## 3. Iterative Implementation

```python
def binary_search_iterative(arr, target):
    """
    Iterative binary search implementation.
    
    Args:
        arr: Sorted list of comparable elements
        target: Element to find
    
    Returns:
        Index of target if found, -1 otherwise
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # Avoids potential integer overflow in other languages
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Target not found


# Example usage
sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 67, 91]
print(binary_search_iterative(sorted_array, 23))  # Output: 5
print(binary_search_iterative(sorted_array, 50))  # Output: -1
```

**Complexity Analysis**:
- **Time**: O(log n) — each iteration halves the search space
- **Space**: O(1) — only a few variables for pointers

---

## 4. Recursive Implementation

```python
def binary_search_recursive(arr, target, left=0, right=None):
    """
    Recursive binary search implementation.
    
    Args:
        arr: Sorted list of comparable elements
        target: Element to find
        left: Left boundary index
        right: Right boundary index
    
    Returns:
        Index of target if found, -1 otherwise
    
    Time Complexity: O(log n)
    Space Complexity: O(log n) — due to recursion stack
    """
    if right is None:
        right = len(arr) - 1
    
    # Base case: search space exhausted
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


# Example usage
sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 67, 91]
print(binary_search_recursive(sorted_array, 23))  # Output: 5
```

**Trade-offs**:
- Recursive version is cleaner and more readable
- Iterative version is more memory-efficient
- Recursive version risks stack overflow for very large arrays
- In Python, iterative is generally preferred for production code

---

## 5. Common Variants

### Finding First Occurrence

```python
def find_first_occurrence(arr, target):
    """Find the leftmost occurrence of target."""
    left = 0
    right = len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


# Example with duplicates
arr = [1, 2, 2, 2, 3, 4, 5]
print(find_first_occurrence(arr, 2))  # Output: 1 (first 2)
```

### Finding Last Occurrence

```python
def find_last_occurrence(arr, target):
    """Find the rightmost occurrence of target."""
    left = 0
    right = len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


# Example
arr = [1, 2, 2, 2, 3, 4, 5]
print(find_last_occurrence(arr, 2))  # Output: 3 (last 2)
```

### Finding Insertion Point

```python
def find_insertion_point(arr, target):
    """
    Find where target should be inserted to maintain sorted order.
    Returns the index of the first element greater than target.
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid - 1
    
    return left


# Example
arr = [1, 3, 5, 7, 9]
print(find_insertion_point(arr, 6))  # Output: 3 (insert before index 3)
```

---

## 6. Common Mistakes and Pitfalls

### Mistake 1: Off-by-One Errors

```python
# WRONG: Using < instead of <=
def binary_search_wrong(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left < right:  # BUG: misses case when left == right
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# CORRECT: Use <=
def binary_search_correct(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:  # Correct: includes single element case
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Mistake 2: Not Updating Boundaries Correctly

```python
# WRONG: Using mid instead of mid + 1 / mid - 1
# This causes infinite loops when target not found

# CORRECT: Always use mid + 1 or mid - 1
if arr[mid] < target:
    left = mid + 1  # Not left = mid
else:
    right = mid - 1  # Not right = mid
```

### Mistake 3: Integer Overflow (Less Relevant in Python)

```python
# POTENTIAL ISSUE in other languages:
mid = (left + right) // 2  # Could overflow

# SAFER (works in all languages):
mid = left + (right - left) // 2
```

### Mistake 4: Forgetting Array Must Be Sorted

```python
# WRONG: Using binary search on unsorted array
unsorted = [3, 1, 4, 1, 5, 9, 2, 6]
result = binary_search_iterative(unsorted, 5)  # Undefined behavior

# CORRECT: Sort first or use linear search
unsorted.sort()
result = binary_search_iterative(unsorted, 5)  # Now valid
```

---

## 7. Applications

### Searching in Rotated Sorted Array

```python
def search_rotated(arr, target):
    """Search in a rotated sorted array."""
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        
        # Left half is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# Example
rotated = [4, 5, 6, 7, 0, 1, 2]
print(search_rotated(rotated, 0))  # Output: 4
```

### Finding Peak Element

```python
def find_peak(arr):
    """Find a peak element (greater than neighbors)."""
    left = 0
    right = len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left


# Example
arr = [1, 3, 5, 4, 2]
print(find_peak(arr))  # Output: 2 (index of value 5)
```

---

## 8. Best Practices

1. **Always use `<=` in the while condition** for standard binary search
2. **Use `left + (right - left) // 2`** to avoid overflow in other languages
3. **Clearly define what `left` and `right` represent** (inclusive vs exclusive)
4. **Consider using built-in functions** like `bisect` in Python
5. **Test edge cases**: empty array, single element, target at boundaries
6. **Document the invariant**: what is true about `left` and `right` at each step?

```python
# Python's built-in bisect module
import bisect

arr = [1, 3, 5, 7, 9]

# Find insertion point
idx = bisect.bisect_left(arr, 5)   # Returns 2
idx = bisect.bisect_right(arr, 5)  # Returns 3

# Check if element exists
pos = bisect.bisect_left(arr, 5)
if pos < len(arr) and arr[pos] == 5:
    print("Found!")
```

---

## 9. Exercises

### Exercise 1: Implement Binary Search
Write an iterative binary search that returns the index of the target or -1 if not found.

### Exercise 2: Find Boundary
Given a sorted boolean array (False followed by True), find the index of the first True.

```python
def find_boundary(arr):
    """Find index of first True in [False, False, ..., True, True]."""
    # Your code here
    pass
```

### Exercise 3: Search Range
Given a sorted array and a target, return the range [first, last] of the target's occurrences.

```python
def search_range(arr, target):
    """Return [first_occurrence, last_occurrence] or [-1, -1]."""
    # Your code here
    pass
```

### Exercise 4: Minimum in Rotated Array
Find the minimum element in a rotated sorted array with no duplicates.

```python
def find_min_rotated(arr):
    """Find minimum in rotated sorted array."""
    # Your code here
    pass
```

---

## 10. Summary

**Key Takeaways**:
1. Binary search requires sorted data and achieves O(log n) time complexity
2. Iterative version is O(1) space; recursive is O(log n) space
3. Off-by-one errors are the most common bugs—be careful with boundary conditions
4. Many problems can be transformed into binary search problems
5. Python's `bisect` module provides optimized binary search utilities

**When to Use Binary Search**:
- Data is sorted (or can be sorted)
- Need O(log n) search performance
- Problem can be framed as "find the first/last X" or "find the boundary"
- Need to search a monotonic function

**When NOT to Use**:
- Data is unsorted and cannot be sorted efficiently
- Data structure doesn't support random access (e.g., linked list)
- Need to search by multiple criteria simultaneously

**Complexity Comparison**:

| Algorithm | Time | Space | Prerequisite |
|-----------|------|-------|--------------|
| Linear Search | O(n) | O(1) | None |
| Binary Search | O(log n) | O(1) | Sorted array |
| Hash Lookup | O(1) avg | O(n) | Hash table |
| Binary Search Tree | O(log n) avg | O(n) | BST structure |

---

## Next Lecture

In the next lecture, we'll explore **Bubble Sort**, the first sorting algorithm we'll study. Understanding binary search's requirement for sorted data motivates the need for efficient sorting algorithms.
