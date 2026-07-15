# Lecture 14: Bubble Sort

## Learning Objectives

By the end of this lecture, you will be able to:
- Understand the bubble sort algorithm and its mechanics
- Implement bubble sort with optimizations
- Analyze time and space complexity
- Recognize when bubble sort is appropriate (and when it isn't)
- Compare bubble sort with other basic sorting algorithms
- Understand the concept of stability in sorting

---

## 1. Introduction

Bubble sort is the simplest sorting algorithm and often the first one taught in computer science. It works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they're in the wrong order. The pass through the list is repeated until the list is sorted.

**The Core Idea**: Large elements "bubble up" to their correct positions through successive swaps.

**Why Study It**:
- Easiest sorting algorithm to understand and implement
- Excellent for learning algorithm analysis
- Stable sort (preserves relative order of equal elements)
- Useful for nearly sorted data with early termination optimization
- Foundation for understanding more complex sorts

---

## 2. How Bubble Sort Works

### The Algorithm

```
1. Start at the beginning of the array
2. Compare each pair of adjacent elements
3. If they're in the wrong order, swap them
4. After one pass, the largest element is at the end
5. Repeat for the remaining unsorted portion
6. Stop when no swaps occur in a complete pass
```

### Visual Walkthrough

Sorting `[5, 3, 8, 4, 2]`:

```
Pass 1:
[5, 3, 8, 4, 2] → compare 5,3 → swap → [3, 5, 8, 4, 2]
[3, 5, 8, 4, 2] → compare 5,8 → no swap
[3, 5, 8, 4, 2] → compare 8,4 → swap → [3, 5, 4, 8, 2]
[3, 5, 4, 8, 2] → compare 8,2 → swap → [3, 5, 4, 2, 8]
Result: [3, 5, 4, 2, 8] — 8 is in place

Pass 2:
[3, 5, 4, 2, 8] → compare 3,5 → no swap
[3, 5, 4, 2, 8] → compare 5,4 → swap → [3, 4, 5, 2, 8]
[3, 4, 5, 2, 8] → compare 5,2 → swap → [3, 4, 2, 5, 8]
Result: [3, 4, 2, 5, 8] — 5 is in place

Pass 3:
[3, 4, 2, 5, 8] → compare 3,4 → no swap
[3, 4, 2, 5, 8] → compare 4,2 → swap → [3, 2, 4, 5, 8]
Result: [3, 2, 4, 5, 8] — 4 is in place

Pass 4:
[3, 2, 4, 5, 8] → compare 3,2 → swap → [2, 3, 4, 5, 8]
Result: [2, 3, 4, 5, 8] — sorted!
```

---

## 3. Basic Implementation

```python
def bubble_sort_basic(arr):
    """
    Basic bubble sort implementation.
    
    Args:
        arr: List of comparable elements
    
    Returns:
        None (sorts in-place)
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Compare adjacent elements
            if arr[j] > arr[j + 1]:
                # Swap if in wrong order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Example
data = [64, 34, 25, 12, 22, 11, 90]
bubble_sort_basic(data)
print(data)  # Output: [11, 12, 22, 25, 34, 64, 90]
```

**Complexity Analysis**:
- **Time**: O(n²) in all cases — always makes n(n-1)/2 comparisons
- **Space**: O(1) — only uses a temporary variable for swapping

---

## 4. Optimized Bubble Sort

```python
def bubble_sort_optimized(arr):
    """
    Optimized bubble sort with early termination.
    
    Stops early if no swaps occur in a pass (array is sorted).
    
    Time Complexity: O(n²) worst/average, O(n) best
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        swapped = False  # Track if any swaps occurred
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps, array is already sorted
        if not swapped:
            break


# Example with early termination
data = [1, 2, 3, 4, 5]  # Already sorted
bubble_sort_optimized(data)  # Only 1 pass needed
print(data)  # Output: [1, 2, 3, 4, 5]
```

**Optimization Benefits**:
- Best case becomes O(n) for already-sorted arrays
- Reduces unnecessary passes when array becomes sorted early
- No change to worst/average case complexity

---

## 5. Cocktail Shaker Sort (Bidirectional Bubble Sort)

```python
def cocktail_shaker_sort(arr):
    """
    Bidirectional bubble sort (cocktail shaker sort).
    
    Alternates between forward and backward passes.
    Better for elements near the end that need to move to the beginning.
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n = len(arr)
    start = 0
    end = n - 1
    swapped = True
    
    while swapped:
        swapped = False
        
        # Forward pass (like regular bubble sort)
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        
        end -= 1  # Last element is now in place
        
        # Backward pass
        for i in range(end, start, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True
        
        start += 1  # First element is now in place


# Example: small element at the end needs to move far
data = [2, 3, 4, 5, 1]
cocktail_shaker_sort(data)
print(data)  # Output: [1, 2, 3, 4, 5]
```

---

## 6. Common Mistakes and Pitfalls

### Mistake 1: Wrong Inner Loop Bounds

```python
# WRONG: Comparing beyond array bounds
for j in range(0, n):  # BUG: j+1 goes out of bounds
    if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]

# CORRECT: Stop at n - i - 1
for j in range(0, n - i - 1):  # Correct: respects shrinking range
    if arr[j] > arr[j + 1]:
        arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

### Mistake 2: Not Tracking Swaps

```python
# WRONG: Always runs n passes (no early termination)
for i in range(n):
    for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    # No way to detect sorted array

# CORRECT: Track swaps for early termination
for i in range(n):
    swapped = False
    for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            swapped = True
    if not swapped:
        break
```

### Mistake 3: Using `>=` Instead of `>`

```python
# WRONG: Unnecessarily swaps equal elements
if arr[j] >= arr[j + 1]:  # Swaps equal elements (unstable!)
    arr[j], arr[j + 1] = arr[j + 1], arr[j]

# CORRECT: Only swap when strictly greater
if arr[j] > arr[j + 1]:  # Preserves stability
    arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

### Mistake 4: Creating New Arrays Instead of In-Place

```python
# WRONG: Uses O(n) extra space
def bubble_sort_wrong(arr):
    result = arr.copy()  # Unnecessary copy
    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result

# CORRECT: Sort in-place
def bubble_sort_correct(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr  # Return the same list for convenience
```

---

## 7. Stability and Properties

**Stability**: Bubble sort is a stable sorting algorithm. Equal elements maintain their relative order because we only swap when `arr[j] > arr[j+1]` (strictly greater), never when equal.

**In-Place**: Yes, O(1) extra space. Only uses a temporary variable for swapping.

**Adaptive**: The optimized version is adaptive—it runs faster on nearly sorted data.

**Online**: Can sort elements as they are received (though not commonly used this way).

```python
# Stability demonstration
data = [('Alice', 85), ('Bob', 90), ('Charlie', 85), ('David', 90)]

# Sort by score using bubble sort (stable)
bubble_sort_optimized(data, key=lambda x: x[1])

# Result: ('Alice', 85) before ('Charlie', 85) — order preserved
# Result: ('Bob', 90) before ('David', 90) — order preserved
```

---

## 8. Performance Comparison

| Case | Time | Swaps | Passes |
|------|------|-------|--------|
| Best (sorted) | O(n) | 0 | 1 |
| Average | O(n²) | n²/4 | n/2 |
| Worst (reverse) | O(n²) | n(n-1)/2 | n |

**Space Complexity**: O(1) — in-place sorting

**Comparison Count**: Always n(n-1)/2 regardless of input order

**Swap Count**: Varies from 0 (sorted) to n(n-1)/2 (reverse sorted)

---

## 9. When to Use Bubble Sort

**Use Bubble Sort When**:
- Teaching sorting concepts (simplicity is the goal)
- Data is very small (< 20 elements)
- Data is nearly sorted (optimized version excels)
- Stability is required and simplicity matters
- Memory is extremely constrained

**Avoid Bubble Sort When**:
- Performance matters (use quicksort, mergesort, or timsort)
- Data is large (O(n²) is too slow)
- Random data (no advantage over other simple sorts)

```python
# Practical example: Small, nearly sorted dataset
def maintain_sorted_list(new_element, sorted_list):
    """
    Insert element into nearly sorted list.
    Bubble sort is fine here due to early termination.
    """
    sorted_list.append(new_element)
    bubble_sort_optimized(sorted_list)
    return sorted_list
```

---

## 10. Exercises

### Exercise 1: Count Swaps
Modify bubble sort to count the total number of swaps performed.

```python
def bubble_sort_count_swaps(arr):
    """Return (sorted_array, swap_count)."""
    # Your code here
    pass
```

### Exercise 2: Sort in Descending Order
Modify bubble sort to sort in descending order.

```python
def bubble_sort_descending(arr):
    """Sort array in descending order using bubble sort."""
    # Your code here
    pass
```

### Exercise 3: Find Sort Pass
Given an array, determine after which pass it becomes sorted (or -1 if more than n passes needed).

```python
def passes_to_sort(arr):
    """Return the number of passes needed to sort the array."""
    # Your code here
    pass
```

### Exercise 4: Bubble Sort on Linked List
Implement bubble sort for a singly linked list.

```python
def bubble_sort_linked_list(head):
    """Sort a singly linked list using bubble sort."""
    # Your code here
    pass
```

---

## 11. Summary

**Key Takeaways**:
1. Bubble sort is the simplest sorting algorithm with O(n²) time complexity
2. The optimized version with early termination achieves O(n) best case
3. Bubble sort is stable, in-place, and adaptive
4. Suitable for small or nearly sorted datasets; impractical for large ones
5. Understanding bubble sort provides foundation for analyzing other sorts

**Algorithm Properties**:

| Property | Value |
|----------|-------|
| Time (best) | O(n) with optimization |
| Time (average) | O(n²) |
| Time (worst) | O(n²) |
| Space | O(1) |
| Stable | Yes |
| In-place | Yes |
| Adaptive | Yes (optimized) |

**Comparison with Other Simple Sorts**:

| Algorithm | Best | Average | Worst | Stable |
|-----------|------|---------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | Yes |

---

## Next Lecture

In the next lecture, we'll explore **Selection Sort**, another simple O(n²) algorithm that works by repeatedly finding the minimum element and placing it at the beginning.
