"""
DSA Tutorial 20 - Merge Sort
==============================

Merge Sort: Divide and conquer - split array, sort halves, merge.
Guaranteed O(n log n) time but uses extra space.

Time Complexity: O(n log n) always
Space Complexity: O(n)
Stable: Yes
When to use: When stable sort is needed, linked lists
"""

# =============================================================================
# 1. BASIC MERGE SORT
# =============================================================================

def merge_sort(arr):
    """Basic merge sort. O(n log n) time, O(n) space"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

print("=== Basic Merge Sort ===")
arr = [38, 27, 43, 3, 9, 82, 10]
print(f"Original: {arr}")
print(f"Sorted: {merge_sort(arr)}")


# =============================================================================
# 2. IN-PLACE MERGE SORT
# =============================================================================

def merge_sort_inplace(arr, low=0, high=None):
    """In-place merge sort using O(1) extra space"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        mid = (low + high) // 2
        merge_sort_inplace(arr, low, mid)
        merge_sort_inplace(arr, mid + 1, high)
        merge_inplace(arr, low, mid, high)

    return arr

def merge_inplace(arr, low, mid, high):
    """Merge without extra space (gap method)"""
    gap = (high - low + 1) // 2 + (high - low + 1) % 2

    while gap > 0:
        for i in range(low, high - gap + 1):
            j = i + gap
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]

        if gap <= 1:
            break
        gap = (gap + 1) // 2

print("\n=== In-Place Merge Sort ===")
arr = [38, 27, 43, 3, 9, 82, 10]
print(f"Sorted: {merge_sort_inplace(arr.copy())}")


# =============================================================================
# 3. MERGE SORT WITH STEPS
# =============================================================================

def merge_sort_steps(arr):
    """Merge sort showing each merge step"""
    steps = []

    def _merge_sort(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])

        merged = merge(left, right)
        steps.append(f"Merge {left} + {right} = {merged}")
        return merged

    result = _merge_sort(arr)
    return result, steps

print("\n=== Merge Sort with Steps ===")
arr = [38, 27, 43, 3, 9]
sorted_arr, steps = merge_sort_steps(arr)
for step in steps:
    print(f"  {step}")
print(f"Final: {sorted_arr}")


# =============================================================================
# 4. BOTTOM-UP MERGE SORT
# =============================================================================

def merge_sort_bottom_up(arr):
    """Iterative merge sort - no recursion"""
    n = len(arr)
    size = 1

    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(start + size - 1, n - 1)
            end = min(start + 2 * size - 1, n - 1)

            if mid < end:
                left = arr[start:mid + 1]
                right = arr[mid + 1:end + 1]
                merged = merge(left, right)
                arr[start:start + len(merged)] = merged

        size *= 2

    return arr

print("\n=== Bottom-Up Merge Sort ===")
arr = [38, 27, 43, 3, 9, 82, 10]
print(f"Sorted: {merge_sort_bottom_up(arr.copy())}")


# =============================================================================
# 5. MERGE SORT DESCENDING
# =============================================================================

def merge_sort_descending(arr):
    """Sort in descending order"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_descending(arr[:mid])
    right = merge_sort_descending(arr[mid:])

    return merge_desc(left, right)

def merge_desc(left, right):
    """Merge two arrays in descending order"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

print("\n=== Descending Merge Sort ===")
arr = [38, 27, 43, 3, 9, 82, 10]
print(f"Descending: {merge_sort_descending(arr)}")


# =============================================================================
# 6. MERGE SORT ON LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def merge_sort_linked_list(head):
    """Merge sort on linked list. O(n log n)"""
    if not head or not head.next:
        return head

    # Split list
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(mid)

    return merge_linked_lists(left, right)

def merge_linked_lists(l1, l2):
    """Merge two sorted linked lists"""
    dummy = Node(0)
    current = dummy

    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next

def linked_list_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

print("\n=== Merge Sort Linked List ===")
values = [38, 27, 43, 3, 9]
head = Node(values[0])
current = head
for val in values[1:]:
    current.next = Node(val)
    current = current.next

head = merge_sort_linked_list(head)
print(f"Sorted: {linked_list_to_list(head)}")


# =============================================================================
# 7. COUNTING INVERSIONS
# =============================================================================

def count_inversions(arr):
    """Count inversions using merge sort. O(n log n)"""
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    merged, split_inv = merge_count(left, right)

    return merged, left_inv + right_inv + split_inv

def merge_count(left, right):
    """Merge and count split inversions"""
    result = []
    inversions = 0
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result, inversions

print("\n=== Count Inversions ===")
arr = [2, 4, 1, 3, 5]
sorted_arr, inversions = count_inversions(arr)
print(f"Array: {arr}")
print(f"Inversions: {inversions}")
print(f"Sorted: {sorted_arr}")


# =============================================================================
# 8. EXTERNAL MERGE SORT (LARGE FILES)
# =============================================================================

def external_merge_sort(files, chunk_size=3):
    """Simulate external merge sort for large data"""
    import heapq

    # Create sorted chunks
    chunks = []
    for i in range(0, len(files), chunk_size):
        chunk = sorted(files[i:i + chunk_size])
        chunks.append(iter(chunk))

    # Merge chunks using heap
    result = list(heapq.merge(*chunks))
    return result

print("\n=== External Merge Sort ===")
data = [38, 27, 43, 3, 9, 82, 10, 15, 28, 41]
print(f"Original: {data}")
print(f"Sorted: {external_merge_sort(data)}")


# =============================================================================
# 9. MERGE K SORTED ARRAYS
# =============================================================================

def merge_k_sorted(arrays):
    """Merge k sorted arrays. O(N log k)"""
    import heapq

    result = []
    min_heap = []

    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))

    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)

        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))

    return result

print("\n=== Merge K Sorted Arrays ===")
arrays = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
print(f"Arrays: {arrays}")
print(f"Merged: {merge_k_sorted(arrays)}")


# =============================================================================
# 10. MERGE SORT PERFORMANCE
# =============================================================================

def analyze_merge_sort():
    """Analyze merge sort performance"""
    import time
    import random

    print("\n=== Merge Sort Performance ===")
    sizes = [1000, 5000, 10000, 50000]

    for size in sizes:
        arr = list(range(size))
        random.shuffle(arr)

        # Top-down
        test = arr.copy()
        start = time.time()
        merge_sort(test)
        top_time = time.time() - start

        # Bottom-up
        test = arr.copy()
        start = time.time()
        merge_sort_bottom_up(test)
        bottom_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  Top-down:  {top_time*1000:.2f}ms")
        print(f"  Bottom-up: {bottom_time*1000:.2f}ms")

analyze_merge_sort()


# =============================================================================
# 11. PRACTICAL APPLICATIONS
# =============================================================================

print("\n=== Practical Applications ===")

# Sort custom objects
def merge_sort_by_key(arr, key_func):
    """Merge sort with custom key"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_by_key(arr[:mid], key_func)
    right = merge_sort_by_key(arr[mid:], key_func)

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 85)]
print(f"Students: {students}")
sorted_students = merge_sort_by_key(students, lambda x: x[1])
print(f"Sorted by grade: {sorted_students}")

# Find median using merge sort
def find_median(arr):
    """Find median using merge sort"""
    sorted_arr = merge_sort(arr)
    n = len(sorted_arr)
    if n % 2 == 1:
        return sorted_arr[n // 2]
    else:
        return (sorted_arr[n // 2 - 1] + sorted_arr[n // 2]) / 2

arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nArray: {arr}")
print(f"Median: {find_median(arr)}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Merge Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Merge sort guarantees O(n log n) in all cases")
    print("2. Stable sort - maintains relative order")
    print("3. Requires O(n) extra space")
    print("4. Excellent for linked lists (no random access needed)")
    print("5. Used in: external sorting, inversion counting, Tim Sort")
