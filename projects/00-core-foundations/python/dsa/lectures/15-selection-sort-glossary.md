# Glossary: Selection Sort (Lecture 15)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Selection Sort | Find minimum, swap to front | O(n²) with O(n) swaps |
| Minimum Finding | Scan unsorted portion for smallest | `min_idx = i` loop |
| Swap | Exchange element at current position with minimum | At most n-1 swaps |
| Unsorted Portion | Elements from current index to end | Shrinks by 1 each pass |
| Sorted Portion | Elements from start to current index | Grows by 1 each pass |
| Invariant | Minimum of unsorted is placed at boundary | After pass i, first i are sorted |
| Not Stable | Equal elements may change relative order | Swap disrupts order |
| Write-Optimal | Minimizes total data movement | O(n) swaps vs O(n²) |
| Bidirectional | Find both min and max per pass | Halves number of passes |
| Comparison Count | Always n(n-1)/2 regardless of input | Not adaptive |

---

## Alphabetical Definitions

### B
**Best Case**: O(n²) time. Unlike bubble sort, selection sort always scans the entire unsorted portion. Even on sorted data, it performs all comparisons.

**Bidirectional Selection Sort**: A variant that finds both the minimum and maximum in each pass. Places minimum at the start and maximum at the end, reducing the number of passes by half.

### C
**Comparison Count**: Always exactly n(n-1)/2 comparisons. Selection sort is deterministic in its comparison count regardless of input ordering.

**Consecutive Selection**: The process of selecting the minimum from successive subarrays. Each selection reduces the unsorted portion by one element.

### D
**Descending Order**: Sorting from largest to smallest. Achieved by finding the maximum instead of the minimum in each pass.

**Displacement**: The distance an element needs to move from its original position to its sorted position. Selection sort can move elements far in a single swap, but this disrupts stability.

### E
**Exchange Sort**: Not the same as selection sort. Exchange sort swaps elements whenever they're out of order (like bubble sort), while selection sort finds the minimum first and swaps once.

### F
**Finding Minimum**: The core operation of selection sort. A linear scan of the unsorted portion identifies the smallest element, which is then swapped to its correct position.

### I
**In-Place Sorting**: Selection sort uses O(1) extra space. It only needs a temporary variable for swapping and an index variable for tracking the minimum.

**Inner Loop**: The loop that scans the unsorted portion to find the minimum. Runs from i+1 to n-1 on each pass, performing one comparison per iteration.

### L
**Linear Scan**: The method used to find the minimum in each pass. The unsorted portion is scanned from left to right, comparing each element with the current minimum.

### M
**Minimum Element**: The smallest value in the unsorted portion. Finding this is the "selection" in selection sort. It's placed at the beginning of the unsorted portion.

**Monotonic Invariant**: After pass i, the first i elements are the i smallest elements in sorted order. This invariant is maintained throughout the algorithm.

### N
**Non-Adaptive**: Selection sort performs the same operations regardless of input order. It always makes n(n-1)/2 comparisons, even on sorted data.

**Not Stable**: Selection sort is not a stable sorting algorithm. Swapping distant elements can change the relative order of equal elements.

### O
**One Swap Per Pass**: The key advantage of selection sort. Each pass makes at most one swap, regardless of how many elements are out of order.

**Outer Loop**: Controls the number of passes. Runs n-1 times (the last element is automatically in place after n-1 selections).

### P
**Pass**: One complete scan of the unsorted portion to find the minimum, followed by one swap. After pass i, the i-th smallest element is in its correct position.

**Placement**: The process of putting the selected minimum into its correct position. Each placement is done via a single swap operation.

### S
**Selection**: The act of choosing the minimum (or maximum) element from the unsorted portion. This is the defining characteristic of selection sort.

**Stability**: Selection sort is NOT stable. Equal elements may change their relative order due to long-distance swaps. Use insertion sort or merge sort if stability is needed.

**Swap Count**: At most n-1 swaps for an array of n elements. This is the minimum among comparison-based sorts, making selection sort write-optimal.

### T
**Total Swaps**: At most n-1 for an array of n elements. This is O(n) swaps, much better than bubble sort's O(n²) swaps in the worst case.

**Two-Phase Algorithm**: Selection sort has two phases in each pass: (1) finding the minimum, (2) swapping it into place. The finding phase is O(n), the swap is O(1).

---

## Code Examples

```python
# Basic Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Selection Sort Descending
def selection_sort_desc(arr):
    n = len(arr)
    for i in range(n - 1):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j] > arr[max_idx]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

# Count Operations
def selection_sort_counting(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comparisons, swaps
```

---

## Related Terms

- **Bubble Sort** → O(n²) sort with O(n²) swaps; stable
- **Insertion Sort** → O(n²) sort; stable and adaptive
- **Quicksort** → O(n log n) average sort using partitioning
- **Merge Sort** → O(n log n) stable sort
- **Heap Sort** → Selection sort variant using a heap for O(n log n)
- **Stability** → Property lost by selection sort
- **Inversion Count** → Number of out-of-order pairs; selection sort doesn't use this
- **Write-Optimal** → Minimizing total data movement
- **Stable Selection Sort** → Variant using insertion instead of swapping
- **Bidirectional Selection** → Find both min and max per pass

---

## Complexity Summary

| Metric | Value |
|--------|-------|
| Best Time | O(n²) |
| Average Time | O(n²) |
| Worst Time | O(n²) |
| Space | O(1) |
| Comparisons | Always n(n-1)/2 |
| Swaps (worst) | n-1 |
| Swaps (best) | 0 |
| Stable | No |
| Adaptive | No |
| Online | Yes (but not practical) |

---

## Key Takeaways

1. Selection sort finds the minimum and swaps it to the front in O(n²) time
2. It performs only O(n) swaps — the minimum among comparison sorts
3. Selection sort is NOT stable — equal elements may change order
4. Use when write operations are expensive or simplicity is paramount
5. Not adaptive — always performs the same work regardless of input order
