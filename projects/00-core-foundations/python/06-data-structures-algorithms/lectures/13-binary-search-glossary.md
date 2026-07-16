# Glossary: Binary Search (Lecture 13)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Binary Search | Divide-and-conquer search on sorted data | O(log n) lookup |
| Midpoint | Element at center of current search range | `mid = (L+R)//2` |
| Search Space | The portion of the array currently being examined | Shrinks by half each step |
| Sorted Array | Prerequisite for binary search correctness | `[1,3,5,7,9]` |
| Iterative Approach | Using a while loop instead of recursion | O(1) space |
| Recursive Approach | Function calls itself with narrower bounds | O(log n) space |
| Invariant | Property that holds true at every iteration | `target in arr[L..R]` |
| Boundary Condition | Rules for when to stop or continue searching | `left <= right` |
| First Occurrence | Leftmost index of a duplicate target | Uses `right = mid - 1` |
| Last Occurrence | Rightmost index of a duplicate target | Uses `left = mid + 1` |

---

## Alphabetical Definitions

### B
**Best Case**: O(1) — the target is found at the midpoint on the first comparison. Binary search checks the middle first, so this is the fastest possible outcome.

**Boundary Condition**: The rule controlling when the search terminates. For standard binary search, this is `left <= right`. Changing to `<` (exclusive) or `>` changes what the algorithm finds.

**Binary Search Tree (BST)**: A tree data structure where left children are less than the parent and right children are greater. Supports O(log n) average-case search, similar to binary search on arrays.

### D
**Divide and Conquer**: The algorithmic strategy of breaking a problem into smaller subproblems, solving each recursively, and combining results. Binary search exemplifies this by halving the search space each step.

**Duplicate Elements**: When multiple elements equal the target. Standard binary search finds an arbitrary occurrence. Modified versions find the first or last occurrence.

### I
**Integer Overflow**: In languages like C/Java, `(left + right)` can overflow for very large arrays. Python handles big integers natively, but the pattern `left + (right - left) // 2` is safer across languages.

**Invariant**: A condition that remains true throughout algorithm execution. For binary search: "if the target exists, it's within `arr[left..right]`." Verifying invariants helps prove correctness.

**Iterative Binary Search**: Uses a while loop with explicit pointers. Preferred for production code due to O(1) space and no recursion overhead.

### L
**Lower Bound**: The smallest index where the target could be. `bisect_left` in Python finds this. Returns the first position where target could be inserted while maintaining sort order.

**Logarithmic Time**: O(log n) complexity. Binary search reduces the problem size by half each iteration. Searching 1,000,000 elements takes only ~20 comparisons.

### M
**Midpoint Calculation**: `mid = left + (right - left) // 2`. The floor division ensures integer results. This formula avoids overflow and always produces a valid index within bounds.

**Monotonic Function**: A function that is entirely non-increasing or non-decreasing. Binary search works on any monotonic predicate, not just sorted arrays. This enables solving many non-obvious problems.

### N
**No Duplicates Assumption**: Standard binary search implementations assume no duplicates or don't care which match is returned. When duplicates matter, use first/last occurrence variants.

### O
**One-Sided Binary Search**: A variant where only one boundary is updated. Used when you know which direction to search (e.g., finding a peak in an array).

### P
**Predicate Function**: A function returning True/False. Binary search can find the boundary where a predicate changes from False to True, generalizing beyond simple value searches.

### R
**Recursive Binary Search**: Calls itself with updated bounds. Cleaner code but uses O(log n) stack space. Risk of stack overflow for extremely large inputs (rare in practice).

**Right Upper Bound**: `bisect_right` finds the insertion point after any existing entries of the target. Returns `first index where arr[index] > target`.

### S
**Search Space**: The portion of the array being examined. Initially the entire array, it shrinks by half with each comparison until empty or the target is found.

**Sentinel Pattern**: Not typically used with binary search (unlike linear search) because random access eliminates the need for sequential scanning optimizations.

**Sorted Array**: A prerequisite for binary search. Elements must be in non-decreasing order. Without this guarantee, binary search produces incorrect results.

**Standard Binary Search**: The basic version that returns any index where the target is found, or -1 if absent. Uses `left <= right` as the loop condition.

### T
**Target**: The value being searched for. Must be comparable to elements in the array (same type or compatible ordering).

**Two-Pointer Technique**: Binary search uses two pointers (left and right) that converge toward each other. This is a specific application of the broader two-pointer pattern.

### U
**Upper Bound**: The largest index where the target could be. `bisect_right` returns this. Used to find the last occurrence of a target or count elements less than a value.

---

## Code Examples

```python
# Standard Binary Search (Iterative)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# First Occurrence (Lower Bound)
def find_first(arr, target):
    left, right = 0, len(arr) - 1
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

# Last Occurrence (Upper Bound)
def find_last(arr, target):
    left, right = 0, len(arr) - 1
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

# Python bisect Module
import bisect
arr = [1, 3, 3, 3, 5, 7]
bisect.bisect_left(arr, 3)   # Returns 1 (first 3)
bisect.bisect_right(arr, 3)  # Returns 4 (after last 3)
```

---

## Related Terms

- **Linear Search** → simpler but O(n); no sorting required
- **Interpolation Search** → O(log log n) average for uniform data
- **Ternary Search** → divides into thirds; rarely better than binary
- **Binary Search Tree** → tree-based equivalent of binary search
- **Divide and Conquer** → the strategy binary search exemplifies
- **Two Pointers** → related technique using converging indices
- **Bisect Module** → Python's optimized binary search library
- **Rotated Array Search** → advanced binary search application
- **Monotonic Predicate** → generalizes binary search beyond sorted arrays
- **Meet in the Middle** → advanced technique building on binary search ideas

---

## Complexity Deep Dive

| Operation | Iterative | Recursive |
|-----------|-----------|-----------|
| Time (best) | O(1) | O(1) |
| Time (avg) | O(log n) | O(log n) |
| Time (worst) | O(log n) | O(log n) |
| Space | O(1) | O(log n) |
| Comparisons per step | 1-3 | 1-3 |
| Total comparisons | ≤ 2·log₂(n) + 1 | ≤ 2·log₂(n) + 1 |

**Concrete Example**: Searching 1 billion elements
- Linear search: up to 1,000,000,000 comparisons
- Binary search: at most ~60 comparisons (2·30 + 1)

---

## Key Takeaways

1. Binary search requires sorted data and achieves O(log n) performance
2. The `<=` vs `<` boundary condition is critical and error-prone
3. First/last occurrence variants handle duplicates by adjusting boundary updates
4. Python's `bisect` module provides production-ready implementations
5. Many problems can be reframed as binary search on a monotonic predicate
