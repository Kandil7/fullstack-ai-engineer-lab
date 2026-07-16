# Glossary: Insertion Sort (Lecture 16)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Insertion Sort | Build sorted portion by inserting elements | O(n) best, O(n²) worst |
| Key | Element being inserted | `key = arr[i]` |
| Sorted Portion | Left part of array, always sorted | Grows by 1 each step |
| Shifting | Moving larger elements right to make room | `arr[j+1] = arr[j]` |
| Stable Sort | Preserves order of equal elements | No equal-element reordering |
| Adaptive Sort | O(n) on nearly sorted data | Early termination |
| Online Sort | Can sort as data arrives | Insert new elements incrementally |
| Binary Insertion | Use binary search for insertion point | Reduces comparisons |
| Sentinel | Minimum at position 0 to eliminate bounds check | Removes `j >= 0` test |
| Card Sort Analogy | Like sorting playing cards in hand | Intuitive mental model |

---

## Alphabetical Definitions

### A
**Adaptive Algorithm**: An algorithm that takes advantage of existing order. Insertion sort is adaptive—it runs in O(n) on already-sorted data because no shifts are needed.

**Array Shift**: Moving elements one position to the right to make room for insertion. Each shift is O(1), but up to n-1 shifts may be needed per element.

### B
**Best Case**: O(n) for insertion sort. Occurs when the array is already sorted. Each element is compared once with its predecessor and no shifts occur.

**Binary Insertion Sort**: A variant that uses binary search to find the insertion point. Reduces comparisons from O(n) to O(log n) per element but shifts remain O(n).

**Boundary Check**: The `j >= 0` condition in the inner loop. Prevents accessing negative indices. Can be eliminated with a sentinel.

### C
**Card Sort Analogy**: Insertion sort mimics sorting playing cards in your hand. You pick up each card and insert it into the correct position among the cards already sorted.

**Comparison Count**: Ranges from n-1 (best case) to n(n-1)/2 (worst case). Binary insertion sort reduces this to O(n log n) but doesn't improve shift count.

### D
**Descending Order**: Sorting from largest to smallest. Achieved by changing the comparison from `arr[j] > key` to `arr[j] < key`.

### E
**Element Insertion**: The core operation—placing a new element into its correct position within the sorted portion. This involves shifting and then inserting.

### H
**Hybrid Algorithm Foundation**: Insertion sort is used as a subroutine in Timsort, introsort, and other hybrid algorithms for small subarrays.

### I
**In-Place Sorting**: Insertion sort uses O(1) extra space. Only a temporary variable for the key is needed.

**Inner Loop**: The loop that shifts elements to make room for the key. Runs from i-1 down to the insertion point.

**Insertion Point**: The position where the key should be placed. Found by shifting elements greater than the key to the right.

**Insertion Sort**: A simple sorting algorithm that builds the sorted array one element at a time by inserting each element into its correct position.

### L
**Linear Search for Insertion**: Standard insertion sort finds the insertion point by linear scan. Takes O(n) comparisons per element in the worst case.

### M
**Minimum at Start (Sentinel)**: An optimization where the minimum element is placed at position 0 as a sentinel. Eliminates the bounds check in the inner loop.

### N
**Nearly Sorted Data**: Data with only a few elements out of place. Insertion sort excels here with O(n) performance because few shifts are needed.

**No Extra Space**: Insertion sort is in-place, requiring only O(1) auxiliary space for the key variable.

### O
**Online Sorting**: Insertion sort can process elements as they arrive. Each new element is inserted into the correct position in the already-sorted portion.

**O(n) Best Case**: Insertion sort is the only O(n²) algorithm with O(n) best case. This makes it ideal for nearly sorted or small datasets.

### P
**Pass**: Processing one element—finding its insertion point and inserting it. After pass i, the first i+1 elements are sorted.

**Partial Sort**: After each pass, the left portion is sorted. This invariant is maintained throughout the algorithm.

### S
**Sentinel Optimization**: Placing the minimum element at position 0 removes the `j >= 0` bounds check. Reduces inner loop overhead.

**Shifting**: Moving elements rightward to create space for the key. The number of shifts equals the number of inversions involving the current element.

**Small Array Optimization**: Insertion sort outperforms divide-and-conquer sorts on small arrays (< 50 elements) due to lower overhead.

**Stable Sorting Algorithm**: Insertion sort preserves the relative order of equal elements. It only shifts when `arr[j] > key` (strictly greater).

### T
**Time Complexity**: O(n²) worst and average case. O(n) best case when data is already sorted.

**Timsort Integration**: Python's built-in Timsort uses insertion sort for small runs (< 64 elements). This combines insertion sort's efficiency on small data with merge sort's efficiency on large data.

---

## Code Examples

```python
# Basic Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Binary Insertion Sort
def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i
        while left < right:
            mid = (left + right) // 2
            if arr[mid] <= key:
                left = mid + 1
            else:
                right = mid
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        arr[left] = key
    return arr

# Sentinel Version
def insertion_sort_sentinel(arr):
    # Find and place minimum at position 0
    min_idx = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
    arr[0], arr[min_idx] = arr[min_idx], arr[0]
    
    # Insertion sort without bounds check
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

---

## Related Terms

- **Bubble Sort** → O(n²) sort; stable, adaptive, but more swaps
- **Selection Sort** → O(n²) sort; fewer swaps but not stable
- **Shell Sort** → Generalized insertion sort with gap sequences
- **Timsort** → Python's sort; uses insertion sort for small runs
- **Merge Sort** → O(n log n) stable sort; uses insertion for small subarrays
- **Introsort** → Hybrid quicksort/insertion sort
- **Stability** → Property preserved by insertion sort
- **Online Algorithm** → Can process elements as they arrive
- **Nearly Sorted Data** → Insertion sort's specialty
- **Sentinel Pattern** → Optimization to eliminate bounds checks

---

## Complexity Summary

| Metric | Value |
|--------|-------|
| Best Time | O(n) — already sorted |
| Average Time | O(n²) |
| Worst Time | O(n²) — reverse sorted |
| Space | O(1) |
| Comparisons (best) | n-1 |
| Comparisons (worst) | n(n-1)/2 |
| Shifts (best) | 0 |
| Shifts (worst) | n(n-1)/2 |
| Stable | Yes |
| Adaptive | Yes |
| Online | Yes |

---

## Key Takeaways

1. Insertion sort builds sorted array by inserting each element into position
2. O(n) best case makes it ideal for nearly sorted or small data
3. Stable, in-place, adaptive, and online
4. Foundation for hybrid algorithms like Timsort
5. Best among O(n²) sorts for practical use on small datasets
