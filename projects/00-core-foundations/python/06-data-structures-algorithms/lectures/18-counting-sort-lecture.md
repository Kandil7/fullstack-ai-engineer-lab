# Lecture 18: Counting Sort

> A non-comparison-based sorting algorithm that counts occurrences of each element

## Learning Objectives

By the end of this lecture, you will be able to:
1. Understand the counting sort algorithm and its mechanics
2. Implement counting sort from scratch
3. Analyze time and space complexity
4. Know when counting sort is optimal versus when to use other algorithms
5. Handle edge cases like negative numbers and large ranges

## Key Concepts

### What is Counting Sort?

Counting sort is a non-comparison-based sorting algorithm that works by counting the occurrences of each distinct element in the input array. It then uses these counts to determine the positions of elements in the sorted output array.

**Key Insight:** Instead of comparing elements to each other, counting sort uses arithmetic to determine positions, achieving O(n + k) time complexity where k is the range of input values.

### Core Principle

1. **Count Phase:** Count how many times each value appears
2. **Cumulative Count:** Transform counts to cumulative positions
3. **Place Phase:** Place each element in its correct position

### Why Counting Sort?

- **Speed:** O(n + k) time complexity
- **Simplicity:** Easy to understand and implement
- **Stability:** Maintains relative order of equal elements
- **Predictable:** Performance depends on value range, not input order

### Limitations

- **Range Dependent:** Performance degrades when k >> n
- **Integer Keys Only:** Works with integer (or integer-mapped) keys
- **Space:** Requires O(k) extra space for counting array

## Algorithm Walkthrough

### Step 1: Find Range
Determine the minimum and maximum values to establish the range.

### Step 2: Initialize Count Array
Create an array of zeros with size equal to the range.

### Step 3: Count Occurrences
For each element in input, increment the corresponding count.

### Step 4: Compute Cumulative Counts
Transform counts into cumulative sums (prefix sums).

### Step 5: Build Output Array
Place elements in their correct positions using cumulative counts.

### Step 6: Copy to Original
Copy the sorted output back to the original array.

## Code Examples

### Basic Counting Sort

```python
def counting_sort(arr):
    """
    Basic counting sort for non-negative integers.
    
    Time Complexity: O(n + k) where k is the range of input
    Space Complexity: O(n + k) for output and count arrays
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    # Find range of input
    max_val = max(arr)
    
    # Initialize count array
    count = [0] * (max_val + 1)
    
    # Count occurrences
    for num in arr:
        count[num] += 1
    
    # Build sorted array
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])
    
    return sorted_arr

# Example usage
arr = [4, 2, 2, 8, 3, 3, 1]
print("Original array:", arr)
sorted_arr = counting_sort(arr)
print("Sorted array:", sorted_arr)
```

### In-Place Counting Sort

```python
def counting_sort_inplace(arr):
    """
    In-place counting sort that modifies the original array.
    
    Uses cumulative counts to place elements directly.
    
    Args:
        arr: List of non-negative integers to sort (modified in-place)
    """
    if not arr:
        return
    
    max_val = max(arr)
    
    # Count occurrences
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    
    # Compute cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output array (traverse backwards for stability)
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    
    # Copy back to original array
    for i in range(len(arr)):
        arr[i] = output[i]

# Example usage
arr = [4, 2, 2, 8, 3, 3, 1]
print("Original array:", arr)
counting_sort_inplace(arr)
print("Sorted array:", arr)
```

### Counting Sort with Negative Numbers

```python
def counting_sort_with_negatives(arr):
    """
    Counting sort that handles negative numbers.
    
    Shifts all values to non-negative range before sorting.
    
    Args:
        arr: List of integers (including negatives) to sort
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    # Shift range to start from 0
    shift = -min_val
    range_size = max_val - min_val + 1
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num + shift] += 1
    
    # Build sorted array
    sorted_arr = []
    for i in range(range_size):
        sorted_arr.extend([i - shift] * count[i])
    
    return sorted_arr

# Example usage
arr = [-5, -1, -3, 2, 4, -2, 1, 0]
print("Original array:", arr)
sorted_arr = counting_sort_with_negatives(arr)
print("Sorted array:", sorted_arr)
```

### Counting Sort for Objects

```python
def counting_sort_by_key(arr, key_func):
    """
    Counting sort for objects using a key function.
    
    Sorts objects based on integer keys extracted by key_func.
    
    Args:
        arr: List of objects to sort
        key_func: Function that extracts integer key from object
    
    Returns:
        Sorted list of objects
    """
    if not arr:
        return arr
    
    # Find range of keys
    keys = [key_func(item) for item in arr]
    min_key = min(keys)
    max_key = max(keys)
    
    # Count occurrences of each key
    count = [0] * (max_key - min_key + 1)
    for key in keys:
        count[key - min_key] += 1
    
    # Compute cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output (traverse backwards for stability)
    output = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        key = key_func(arr[i])
        output[count[key - min_key] - 1] = arr[i]
        count[key - min_key] -= 1
    
    return output

# Example usage: Sort students by age
students = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 22},
    {"name": "Charlie", "age": 25},
    {"name": "Diana", "age": 21}
]

print("Original students:")
for s in students:
    print(f"  {s['name']}: {s['age']}")

sorted_students = counting_sort_by_key(students, lambda x: x["age"])

print("\nSorted by age:")
for s in sorted_students:
    print(f"  {s['name']}: {s['age']}")
```

### Counting Sort with Range Specification

```python
def counting_sort_with_range(arr, min_val, max_val):
    """
    Counting sort with specified range.
    
    Useful when range is known beforehand.
    
    Args:
        arr: List of integers to sort
        min_val: Minimum expected value
        max_val: Maximum expected value
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    # Validate range
    if min_val > max_val:
        raise ValueError("min_val must be <= max_val")
    
    # Initialize count array
    range_size = max_val - min_val + 1
    count = [0] * range_size
    
    # Count occurrences
    for num in arr:
        if num < min_val or num > max_val:
            raise ValueError(f"Element {num} out of range [{min_val}, {max_val}]")
        count[num - min_val] += 1
    
    # Build sorted array
    sorted_arr = []
    for i in range(range_size):
        sorted_arr.extend([i + min_val] * count[i])
    
    return sorted_arr

# Example usage
arr = [15, 12, 18, 14, 16, 13, 17, 19]
sorted_arr = counting_sort_with_range(arr, 10, 20)
print("Sorted array:", sorted_arr)
```

### Optimized Counting Sort

```python
def counting_sort_optimized(arr):
    """
    Optimized counting sort with multiple improvements.
    
    1. Uses array indexing instead of extend for better performance
    2. Handles empty and single-element arrays
    3. Skips counting if array is already sorted
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    
    # Handle edge cases
    if n <= 1:
        return arr[:]
    
    # Check if already sorted
    is_sorted = all(arr[i] <= arr[i + 1] for i in range(n - 1))
    if is_sorted:
        return arr[:]
    
    max_val = max(arr)
    
    # Count occurrences
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    
    # Build output array
    output = [0] * n
    index = 0
    for i in range(len(count)):
        for _ in range(count[i]):
            output[index] = i
            index += 1
    
    return output

# Example usage
arr = [6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2]
print("Original array:", arr)
sorted_arr = counting_sort_optimized(arr)
print("Sorted array:", sorted_arr)
```

## Common Mistakes

### Mistake 1: Not Handling Empty Arrays
```python
# WRONG: Will crash on empty array
def counting_sort_wrong(arr):
    max_val = max(arr)  # ValueError: max() arg is an empty sequence
    count = [0] * (max_val + 1)
    # ...

# CORRECT: Check for empty array
def counting_sort_correct(arr):
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    # ...
```

### Mistake 2: Off-by-One in Count Array
```python
# WRONG: Size max_val instead of max_val + 1
count = [0] * max_val  # IndexError when max_val appears

# CORRECT: Include max_val in range
count = [0] * (max_val + 1)
```

### Mistake 3: Not Using Cumulative Counts
```python
# WRONG: Placing elements without cumulative counts
for num in arr:
    output[count[num]] = num  # Overwrites previous elements
    count[num] += 1

# CORRECT: Compute cumulative counts first
for i in range(1, len(count)):
    count[i] += count[i - 1]
```

### Mistake 4: Not Preserving Stability
```python
# WRONG: Forward traversal breaks stability
for i in range(len(arr)):
    output[count[arr[i]] - 1] = arr[i]
    count[arr[i]] -= 1

# CORRECT: Backward traversal preserves stability
for i in range(len(arr) - 1, -1, -1):
    output[count[arr[i]] - 1] = arr[i]
    count[arr[i]] -= 1
```

## Best Practices

1. **Validate Input:** Check for empty arrays and invalid values
2. **Choose Right Algorithm:** Use counting sort when k (range) is small relative to n
3. **Preserve Stability:** Use backward traversal when stability is needed
4. **Handle Edge Cases:** Single element, already sorted, all same values
5. **Optimize Memory:** Reuse arrays when sorting multiple times
6. **Document Assumptions:** Clearly state input requirements (non-negative integers)
7. **Test Thoroughly:** Include edge cases and performance tests

## Complexity Analysis

| Case | Time | Space | Notes |
|------|------|-------|-------|
| Best | O(n + k) | O(n + k) | Range k is small |
| Average | O(n + k) | O(n + k) | Typical performance |
| Worst | O(n + k) | O(n + k) | Range k is large |

- **n** = number of elements
- **k** = range of input values (max - min + 1)

**When to use counting sort:**
- k = O(n) or smaller
- Input consists of integers
- Stability is important
- Range is known or bounded

**When NOT to use counting sort:**
- k >> n (large range, few elements)
- Input contains floating-point numbers
- Memory is severely constrained

## Exercises

### Exercise 1: Count Frequencies
**Problem:** Given an array, count the frequency of each element using counting sort logic.

**Expected Time Complexity:** O(n + k)

### Exercise 2: Sort Characters
**Problem:** Implement counting sort for lowercase English characters.

### Exercise 3: Range Query
**Problem:** After sorting, find how many elements fall in a given range [L, R].

### Exercise 4: Stability Test
**Problem:** Create a test that verifies counting sort is stable.

### Exercise 5: Performance Comparison
**Problem:** Compare counting sort with quick sort on arrays with small ranges.

## Summary

Counting sort is a powerful non-comparison-based sorting algorithm that achieves O(n + k) time complexity. Key takeaways:

- **Best for:** Integer keys with small range relative to input size
- **Time complexity:** O(n + k) where k is the range
- **Space complexity:** O(n + k) for output and count arrays
- **Stability:** Yes, when implemented correctly
- **Limitation:** Not suitable for large ranges or non-integer data

Understanding counting sort provides insight into non-comparison sorting and is a building block for radix sort.

## Next Steps

- **Lecture 19:** Radix Sort (uses counting sort as subroutine)
- **Practice:** Implement counting sort for various use cases
- **Explore:** Bucket sort and other distribution-based sorts
