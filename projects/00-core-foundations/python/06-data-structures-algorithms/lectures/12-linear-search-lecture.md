# Lecture 12: Linear Search - Data Structures and Algorithms

## Topic Overview

Linear search is the simplest searching algorithm that sequentially checks each element in a collection until the target is found or the collection is exhausted. While it has O(n) time complexity, it's essential for understanding search fundamentals and is the only option for unsorted data.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement basic linear search
2. Understand sentinel search optimization
3. Apply linear search to 2D arrays and strings
4. Use linear search for finding min/max values
5. Count occurrences and find duplicates
6. Understand interpolation and ternary search variants
7. Compare linear search with other search algorithms

## Key Concepts

### 1. Basic Linear Search

The simplest form of search - check each element sequentially.

```python
def linear_search(arr, target):
    """Search for target in array. Returns index or -1."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Example
arr = [10, 23, 45, 70, 11, 15]
target = 70
result = linear_search(arr, target)
print(f"Found {target} at index {result}")  # Found 70 at index 3
```

**Time Complexity:**
- Best case: O(1) - target is first element
- Average case: O(n/2) ≈ O(n)
- Worst case: O(n) - target is last or not present

**Space Complexity:** O(1)

### 2. Sentinel Linear Search

Optimization that eliminates the boundary check in each iteration.

```python
def sentinel_search(arr, target):
    """Linear search with sentinel - eliminates boundary check"""
    n = len(arr)
    last = arr[n - 1]
    arr[n - 1] = target  # Place sentinel
    
    i = 0
    while arr[i] != target:
        i += 1
    
    arr[n - 1] = rest