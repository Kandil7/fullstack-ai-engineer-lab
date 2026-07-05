"""
DSA Tutorial 15 - Selection Sort
==================================

Selection Sort: Find minimum element, swap with first unsorted position.
Repeat for remaining unsorted portion.

Time Complexity: O(n^2) always
Space Complexity: O(1) - in-place
Stable: No (default implementation)
"""

# =============================================================================
# 1. BASIC SELECTION SORT
# =============================================================================

def selection_sort(arr):
    """Basic selection sort. O(n^2) time, O(1) space"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print("=== Basic Selection Sort ===")
arr = [64, 25, 12, 22, 11]
print(f"Original: {arr}")
print(f"Sorted: {selection_sort(arr.copy())}")


# =============================================================================
# 2. SELECTION SORT WITH STEPS
# =============================================================================

def selection_sort_steps(arr):
    """Selection sort showing each step"""
    n = len(arr)
    steps = []
    arr = arr.copy()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append(f"Pass {i+1}: Swap {arr[min_idx]} and {arr[i]}: {arr.copy()}")
        else:
            steps.append(f"Pass {i+1}: {arr[i]} already in place: {arr.copy()}")

    return arr, steps

print("\n=== Selection Sort with Steps ===")
arr = [29, 10, 14, 37, 13]
sorted_arr, steps = selection_sort_steps(arr)
for step in steps:
    print(f"  {step}")
print(f"Final: {sorted_arr}")


# =============================================================================
# 3. SELECTION SORT DESCENDING
# =============================================================================

def selection_sort_descending(arr):
    """Sort in descending order"""
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j] > arr[max_idx]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    return arr

print("\n=== Descending Selection Sort ===")
arr = [64, 25, 12, 22, 11]
print(f"Descending: {selection_sort_descending(arr.copy())}")


# =============================================================================
# 4. COUNTING OPERATIONS
# =============================================================================

def selection_sort_counted(arr):
    """Selection sort counting comparisons and swaps"""
    n = len(arr)
    comparisons = 0
    swaps = 0
    arr = arr.copy()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    return arr, comparisons, swaps

print("\n=== Selection Sort Statistics ===")
test_cases = [
    [64, 25, 12, 22, 11],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
]

for arr in test_cases:
    sorted_arr, comps, swaps = selection_sort_counted(arr)
    print(f"{arr}: {comps} comparisons, {swaps} swaps")


# =============================================================================
# 5. SELECTION SORT ON LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def selection_sort_linked_list(head):
    """Selection sort on linked list. O(n^2)"""
    if not head:
        return head

    current = head
    while current:
        min_node = current
        search = current.next

        while search:
            if search.data < min_node.data:
                min_node = search
            search = search.next

        if min_node != current:
            current.data, min_node.data = min_node.data, current.data

        current = current.next

    return head

def linked_list_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

print("\n=== Selection Sort on Linked List ===")
values = [64, 25, 12, 22, 11]
head = Node(values[0])
current = head
for val in values[1:]:
    current.next = Node(val)
    current = current.next

head = selection_sort_linked_list(head)
print(f"Sorted: {linked_list_to_list(head)}")


# =============================================================================
# 6. STABLE SELECTION SORT
# =============================================================================

def selection_sort_stable(arr):
    """Stable selection sort using insertion"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Insert min element at correct position (stable)
        key = arr[min_idx]
        while min_idx > i:
            arr[min_idx] = arr[min_idx - 1]
            min_idx -= 1
        arr[i] = key

    return arr

print("\n=== Stable Selection Sort ===")
# Using tuples to demonstrate stability
arr = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e')]
print(f"Before: {arr}")
sorted_arr = selection_sort_stable(arr.copy())
print(f"After:  {sorted_arr}")


# =============================================================================
# 7. DOUBLE SELECTION SORT
# =============================================================================

def double_selection_sort(arr):
    """Find both min and max in each pass"""
    n = len(arr)
    left = 0
    right = n - 1

    while left < right:
        min_idx = left
        max_idx = right

        for i in range(left, right + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            if arr[i] > arr[max_idx]:
                max_idx = i

        # Place minimum at left
        arr[left], arr[min_idx] = arr[min_idx], arr[left]

        # If maximum was at left, it got swapped
        if max_idx == left:
            max_idx = min_idx

        # Place maximum at right
        arr[right], arr[max_idx] = arr[max_idx], arr[right]

        left += 1
        right -= 1

    return arr

print("\n=== Double Selection Sort ===")
arr = [64, 25, 12, 22, 11, 90, 45]
print(f"Original: {arr}")
print(f"Sorted: {double_selection_sort(arr.copy())}")


# =============================================================================
# 8. SELECTION SORT FOR STRINGS
# =============================================================================

def selection_sort_strings(arr):
    """Sort strings lexicographically"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print("\n=== Selection Sort Strings ===")
words = ["banana", "apple", "cherry", "date", "elderberry"]
print(f"Before: {words}")
print(f"After:  {selection_sort_strings(words.copy())}")


# =============================================================================
# 9. SELECTION SORT PERFORMANCE
# =============================================================================

def compare_with_other_sorts():
    """Compare selection sort with bubble and insertion sort"""
    import time
    import random

    def bubble_sort(arr):
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

    def insertion_sort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    print("\n=== Sort Comparison ===")
    sizes = [100, 500, 1000]

    for size in sizes:
        arr = list(range(size))
        random.shuffle(arr)

        # Selection
        test = arr.copy()
        start = time.time()
        selection_sort(test)
        sel_time = time.time() - start

        # Bubble
        test = arr.copy()
        start = time.time()
        bubble_sort(test)
        bub_time = time.time() - start

        # Insertion
        test = arr.copy()
        start = time.time()
        insertion_sort(test)
        ins_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  Selection: {sel_time*1000:.2f}ms")
        print(f"  Bubble:    {bub_time*1000:.2f}ms")
        print(f"  Insertion: {ins_time*1000:.2f}ms")

compare_with_other_sorts()


# =============================================================================
# 10. CYCLIC SORT (OPTIMIZED FOR 1-N)
# =============================================================================

def cyclic_sort(arr):
    """Optimized for arrays containing 1 to N. O(n) time, O(1) space"""
    i = 0
    while i < len(arr):
        correct_idx = arr[i] - 1
        if arr[i] != arr[correct_idx]:
            arr[i], arr[correct_idx] = arr[correct_idx], arr[i]
        else:
            i += 1
    return arr

print("\n=== Cyclic Sort (1-N) ===")
arr = [3, 1, 5, 2, 4]
print(f"Before: {arr}")
print(f"After:  {cyclic_sort(arr.copy())}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Selection Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Selection sort always does O(n^2) comparisons")
    print("2. Only O(n) swaps - minimum among O(n^2) sorts")
    print("3. Not stable by default (use stable variant if needed)")
    print("4. In-place sorting with O(1) space")
    print("5. Good when write operations are expensive")
