# Glossary: Linear Search (Lecture 12)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Linear Search | Sequential search through each element | `for item in arr` |
| Brute Force Search | Checking every possible option | O(n) full scan |
| Sentinel Search | Optimized linear search with a guard value | Reduce comparisons |
| Sequential Access | Reading elements one after another | Array traversal |
| Best Case | Target found at first position | O(1) |
| Worst Case | Target at last position or absent | O(n) |
| Average Case | Target somewhere in the middle | O(n/2) |
| Search Key | The value being sought | Target element |
| Match | Element equals search key | Found condition |
| Not Found | Element not present in collection | Return -1 or None |

---

## Alphabetical Definitions

### B
**Best Case**: The scenario where the target element is found at the very first position. Requires only 1 comparison, giving O(1) time complexity regardless of input size.

### C
**Comparison**: The fundamental operation of linear search—checking whether the current element equals the target. Each comparison is O(1), but up to n may be needed.

**Comparison Count**: The total number of element-to-target comparisons performed. Linear search averages n/2 comparisons for successful searches.

**Sequential Search**: Another name for linear search. Emphasizes that elements are accessed in sequence, one after another, without random access.

### D
**Duplicate Handling**: Linear search can find all occurrences or just the first. The search continues until explicitly stopped or the array ends.

### F
**First Occurrence**: Linear search naturally finds the first match when scanning left to right. To find later occurrences, continue past the first match.

**Forward Scan**: Searching from index 0 to n-1. A reverse scan goes from n-1 to 0 and is equally valid for basic linear search.

### G
**Guard Value (Sentinel)**: A special value placed at the end of the array to eliminate the bounds check in each iteration. Converts two comparisons per element to one.

### L
**Linear Time**: O(n) complexity where work grows proportionally with input size. Linear search is inherently linear because it may need to check every element.

**List Traversal**: The process of visiting each element in a list. Linear search is a traversal-based algorithm that stops early when the target is found.

### M
**Midpoint**: Not used in linear search (unlike binary search). Linear search checks every element sequentially regardless of value ordering.

### N
**Near-Miss Search**: A search where the target is close to the end or absent entirely. This is the worst case for linear search, requiring n comparisons.

**No-Op Early Termination**: Linear search has no early termination for absent targets—it must check every element before concluding the target is missing.

### O
**Ordered vs Unordered**: Linear search works on both ordered and unordered collections. Unlike binary search, no sorting requirement exists.

### S
**Sentinel Linear Search**: A variation that places the target at the end of the array as a sentinel. Removes the need to check `i < n` on each iteration, reducing comparisons by ~50%.

**Sequential Scan**: Processing elements in order from first to last. Each element is visited at most once during a single pass.

**Sublinear Early Exit**: For successful searches where the target is near the start, linear search can terminate in far fewer than n steps. This is its advantage over algorithms with fixed O(n log n) work.

### T
**Time Complexity**: O(n) worst case and average case for linear search. O(1) best case when the target is the first element.

---

## Code Examples

```python
# Basic Linear Search
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Sentinel Linear Search
def sentinel_search(arr, target):
    n = len(arr)
    last = arr[n - 1]
    arr[n - 1] = target  # Place sentinel
    i = 0
    while arr[i] != target:
        i += 1
    arr[n - 1] = last    # Restore original
    if i < n - 1 or arr[n - 1] == target:
        return i
    return -1

# Linear Search in Linked List
def search_linked_list(head, target):
    current = head
    index = 0
    while current:
        if current.data == target:
            return index
        current = current.next
        index += 1
    return -1

# Count Occurrences
def count_occurrences(arr, target):
    count = 0
    for item in arr:
        if item == target:
            count += 1
    return count
```

---

## Related Terms

- **Binary Search** → efficient alternative when array is sorted
- **Interpolation Search** → improvement over binary search for uniformly distributed data
- **Hash Table** → O(1) average lookup but requires extra space
- **Linked List Search** → linear search is the only option (no random access)
- **Array Traversal** → the foundation underlying linear search
- **Sentinel Pattern** → optimization technique to reduce loop overhead
- **Brute Force** → general strategy that linear search exemplifies
- **Search Algorithm** → broad category; linear search is the simplest member
- **Early Termination** → stopping as soon as the target is found
- **Sequential Access** → access pattern required by linear search

---

## Complexity Summary

| Scenario | Time | Space | Comparisons |
|----------|------|-------|-------------|
| Best (found first) | O(1) | O(1) | 1 |
| Average (found) | O(n/2) | O(1) | n/2 |
| Worst (not found) | O(n) | O(1) | n |
| All occurrences | O(n) | O(1) | n |
| Sentinel variant | O(n) | O(1) | n |

---

## Key Takeaways

1. Linear search is the simplest search algorithm with O(n) complexity
2. Works on both sorted and unsorted collections
3. Sentinel optimization reduces comparisons per iteration
4. Best for small datasets, unsorted data, or linked lists
5. Always consider binary search when data is sorted
