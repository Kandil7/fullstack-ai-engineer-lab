# Glossary: Bubble Sort (Lecture 14)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Bubble Sort | Adjacent comparison sort | Swap if out of order |
| Bubble Up | Large elements move toward end | 90 moves to last position |
| Pass | One complete traversal of unsorted portion | Reduces unsorted by 1 |
| Swap | Exchange two adjacent elements | `a, b = b, a` |
| Stable Sort | Preserves order of equal elements | No equal-element reordering |
| In-Place Sort | Uses O(1) extra memory | No auxiliary array needed |
| Adaptive Sort | Runs faster on nearly sorted data | O(n) best case |
| Cocktail Sort | Bidirectional bubble sort | Forward + backward passes |
| Early Termination | Stop when no swaps occur | Detects sorted array |
| Comparison Sort | Sorts by comparing pairs | O(n log n) lower bound |

---

## Alphabetical Definitions

### A
**Adaptive Algorithm**: An algorithm that takes advantage of existing order in input data. Optimized bubble sort is adaptive—it runs in O(n) on nearly sorted data because early termination detects when sorting is complete.

**Adjacent Comparison**: The fundamental operation of bubble sort—comparing two elements that are next to each other. Only adjacent elements are ever compared, which is why it's called "bubble" sort.

### B
**Best Case**: O(n) for optimized bubble sort. Occurs when the array is already sorted. The algorithm makes one pass with no swaps and terminates immediately.

**Bubble**: The process where larger elements move toward their correct position at the end of the array. Each pass "bubbles" the largest unsorted element to its final position.

**Bubble Up**: The visual metaphor for how large elements gradually move rightward through successive swaps, like bubbles rising in water.

### C
**Comparison-Based Sort**: A sorting algorithm that determines order by comparing elements. Bubble sort is comparison-based, and all comparison sorts have an O(n log n) lower bound (bubble sort doesn't achieve this).

**Cocktail Shaker Sort**: A bidirectional variant of bubble sort that alternates forward and backward passes. Better for elements that need to move long distances (e.g., a small element at the end).

**Consecutive Pair**: Two elements at adjacent indices (i and i+1). Bubble sort only ever examines consecutive pairs, making it simple but limiting its efficiency.

### D
**Descending Order**: Sorting from largest to smallest. Achieved in bubble sort by changing the comparison from `>` to `<`.

**Divide and Conquer**: Not used by bubble sort. Bubble sort is an iterative comparison-based algorithm, unlike quicksort or mergesort which use divide-and-conquer.

### E
**Exchange Sort**: Another name for bubble sort (or its close relatives). Emphasizes that sorting is done by exchanging pairs of elements.

**Extra Space**: Bubble sort requires O(1) extra space—only a temporary variable for swapping. This makes it an in-place sorting algorithm.

### I
**In-Place Sorting**: An algorithm that sorts without requiring significant extra memory. Bubble sort uses only O(1) auxiliary space for the swap operation.

**Inner Loop**: The loop that performs adjacent comparisons and swaps. Runs from index 0 to n-i-1, where i is the current pass number.

**Insertion**: Not directly related to bubble sort, but insertion sort is a related algorithm that builds the sorted array one element at a time (rather than bubbling large elements to the end).

### L
**Last Pass**: The final pass of bubble sort where zero swaps occur (in the optimized version). This confirms the array is sorted and triggers early termination.

**Linear Scan**: One complete traversal of the unsorted portion of the array. Each pass of bubble sort is a linear scan.

### N
**Near-Sorted Data**: Data that is almost sorted with only a few elements out of place. Optimized bubble sort handles this efficiently due to early termination.

**No-Swap Condition**: The condition that triggers early termination—when a complete pass produces zero swaps, the array is sorted. This reduces best-case time to O(n).

### O
**Outer Loop**: Controls the number of passes. Runs n times in the worst case, but the optimized version exits early when sorted.

**O(n²) Complexity**: The worst and average case time complexity of bubble sort. Quadratic time makes it impractical for large datasets.

### P
**Pass**: One complete traversal of the unsorted portion of the array, comparing and swapping adjacent elements. After pass i, the i-th largest element is in its correct position.

**Partially Sorted**: A state where some elements are in their correct positions but others aren't. Bubble sort makes progress on partially sorted data with each pass.

### S
**Stable Sorting Algorithm**: A sorting algorithm that preserves the relative order of elements with equal keys. Bubble sort is stable because it only swaps when `arr[j] > arr[j+1]` (strictly greater).

**Stuttering Pass**: An optimization where the last swap position in each pass marks the new boundary for the next pass, since nothing after it needs swapping.

**Swapped Flag**: A boolean variable tracking whether any swaps occurred during a pass. When false, the array is sorted and bubble sort can terminate early.

### T
**Time Complexity**: O(n²) for bubble sort in worst and average cases. O(n) best case with optimization on already-sorted data.

**Total Comparisons**: Always n(n-1)/2 regardless of input order. Bubble sort always compares every adjacent pair in every pass.

**Total Swaps**: Ranges from 0 (already sorted) to n(n-1)/2 (reverse sorted). The number of swaps equals the number of inversions in the array.

---

## Code Examples

```python
# Basic Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Optimized with Early Termination
def bubble_sort_optimized(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Count Inversions (related to swap count)
def count_inversions(arr):
    """Number of swaps needed equals number of inversions."""
    inversions = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

# Stable Sort Demonstration
def bubble_sort_stable(data, key):
    n = len(data)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if key(data[j]) > key(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data
```

---

## Related Terms

- **Selection Sort** → O(n²) sort that selects minimum and swaps to front
- **Insertion Sort** → O(n²) sort that builds sorted portion incrementally
- **Quicksort** → O(n log n) average sort using partitioning
- **Merge Sort** → O(n log n) stable sort using divide-and-conquer
- **Tim Sort** → Python's built-in sort; hybrid of merge sort and insertion sort
- **Stability** → Property of preserving equal-element order
- **Inversion Count** → Number of out-of-order pairs; equals swap count for bubble sort
- **Adaptive Algorithm** → Takes advantage of existing order in input
- **Cocktail Shaker Sort** → Bidirectional bubble sort variant
- **Gnome Sort** → Similar to bubble sort but swaps with previous elements

---

## Complexity Summary

| Metric | Value |
|--------|-------|
| Best Time | O(n) — already sorted |
| Average Time | O(n²) |
| Worst Time | O(n²) — reverse sorted |
| Space | O(1) — in-place |
| Comparisons | Always n(n-1)/2 |
| Swaps (best) | 0 |
| Swaps (worst) | n(n-1)/2 |
| Stable | Yes |
| Adaptive | Yes (optimized) |
| Online | Yes |

---

## Key Takeaways

1. Bubble sort is the simplest sorting algorithm with O(n²) complexity
2. Optimized version with early termination achieves O(n) best case
3. Bubble sort is stable, in-place, and adaptive
4. Use only for small datasets or educational purposes
5. The number of swaps equals the number of inversions in the array
