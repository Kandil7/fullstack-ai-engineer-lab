"""
DSA Tutorial 17 - Quick Sort
=============================

Quick Sort: Divide and conquer - partition around a pivot.
Elements smaller than pivot go left, larger go right.

Time Complexity:
- Best: O(n log n)
- Average: O(n log n)
- Worst: O(n^2) - poor pivot choice
Space Complexity: O(log n) - recursive stack
Stable: No (default)
"""

# =============================================================================
# 1. BASIC QUICK SORT
# =============================================================================

def quick_sort(arr):
    """Basic quick sort. O(n log n) average"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

print("=== Basic Quick Sort ===")
arr = [3, 6, 8, 10, 1, 2, 1]
print(f"Original: {arr}")
print(f"Sorted: {quick_sort(arr)}")


# =============================================================================
# 2. IN-PLACE QUICK SORT
# =============================================================================

def quick_sort_inplace(arr, low=0, high=None):
    """In-place quick sort using Lomuto partition"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

    return arr

def partition(arr, low, high):
    """Lomuto partition scheme"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

print("\n=== In-Place Quick Sort ===")
arr = [10, 7, 8, 9, 1, 5]
print(f"Original: {arr}")
print(f"Sorted: {quick_sort_inplace(arr.copy())}")


# =============================================================================
# 3. HOARE PARTITION
# =============================================================================

def quick_sort_hoare(arr, low=0, high=None):
    """Quick sort with Hoare partition - more efficient"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = hoare_partition(arr, low, high)
        quick_sort_hoare(arr, low, pivot_idx)
        quick_sort_hoare(arr, pivot_idx + 1, high)

    return arr

def hoare_partition(arr, low, high):
    """Hoare partition scheme - fewer swaps"""
    pivot = arr[low]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]

print("\n=== Hoare Partition ===")
arr = [10, 7, 8, 9, 1, 5]
print(f"Sorted: {quick_sort_hoare(arr.copy())}")


# =============================================================================
# 4. THREE-WAY QUICK SORT (DUPLICATES)
# =============================================================================

def quick_sort_three_way(arr, low=0, high=None):
    """Three-way partition for arrays with many duplicates"""
    if high is None:
        high = len(arr) - 1

    if low >= high:
        return

    lt, gt = low, high
    pivot = arr[low]
    i = low

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1

    quick_sort_three_way(arr, low, lt - 1)
    quick_sort_three_way(arr, gt + 1, high)

    return arr

print("\n=== Three-Way Quick Sort ===")
arr = [4, 9, 4, 4, 1, 9, 4, 4, 9, 4, 4, 1, 4]
print(f"Original: {arr}")
print(f"Sorted: {quick_sort_three_way(arr.copy())}")


# =============================================================================
# 5. RANDOMIZED QUICK SORT
# =============================================================================

import random

def randomized_quick_sort(arr, low=0, high=None):
    """Quick sort with random pivot selection"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = randomized_partition(arr, low, high)
        randomized_quick_sort(arr, low, pivot_idx - 1)
        randomized_quick_sort(arr, pivot_idx + 1, high)

    return arr

def randomized_partition(arr, low, high):
    """Random pivot selection"""
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return partition(arr, low, high)

print("\n=== Randomized Quick Sort ===")
arr = [10, 7, 8, 9, 1, 5]
print(f"Sorted: {randomized_quick_sort(arr.copy())}")


# =============================================================================
# 6. QUICK SORT WITH MEDIAN-OF-THREE
# =============================================================================

def median_of_three(arr, low, high):
    """Select median of first, middle, last as pivot"""
    mid = (low + high) // 2

    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]

    # Place median at high-1
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    return arr[high - 1]

def quick_sort_median(arr, low=0, high=None):
    """Quick sort with median-of-three pivot"""
    if high is None:
        high = len(arr) - 1

    if low + 2 <= high:
        pivot = median_of_three(arr, low, high)
        i = low
        j = high - 1

        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            j -= 1
            while arr[j] > pivot:
                j -= 1
            if i < j:
                arr[i], arr[j] = arr[j], arr[i]
            else:
                break

        arr[i], arr[high - 1] = arr[high - 1], arr[i]

        quick_sort_median(arr, low, i - 1)
        quick_sort_median(arr, i + 1, high)
    elif low < high:
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]

    return arr

print("\n=== Median-of-Three Quick Sort ===")
arr = [10, 7, 8, 9, 1, 5]
print(f"Sorted: {quick_sort_median(arr.copy())}")


# =============================================================================
# 7. QUICK SELECT (KTH SMALLEST)
# =============================================================================

def quick_select(arr, k):
    """Find kth smallest element. O(n) average"""
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k <= len(left):
        return quick_select(left, k)
    elif k <= len(left) + len(middle):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(middle))

print("\n=== Quick Select ===")
arr = [3, 2, 1, 5, 6, 4]
print(f"Array: {arr}")
for k in range(1, len(arr) + 1):
    print(f"  {k}th smallest: {quick_select(arr, k)}")


# =============================================================================
# 8. QUICK SORT ON LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def quick_sort_linked_list(head):
    """Quick sort on linked list"""
    if not head or not head.next:
        return head

    # Find tail
    tail = head
    while tail.next:
        tail = tail.next

    return _quick_sort_ll(head, tail)

def _quick_sort_ll(head, tail):
    if not head or head == tail:
        return head

    if head.next == tail:
        if head.data > tail.data:
            head.data, tail.data = tail.data, head.data
        return head

    pivot = head.data
    left_dummy = Node(0)
    right_dummy = Node(0)
    equal_dummy = Node(0)

    left, right, equal = left_dummy, right_dummy, equal_dummy
    current = head

    while current:
        next_node = current.next
        current.next = None

        if current.data < pivot:
            left.next = current
            left = left.next
        elif current.data > pivot:
            right.next = current
            right = right.next
        else:
            equal.next = current
            equal = equal.next

        current = next_node

    left_dummy.next = _quick_sort_ll(left_dummy.next, left)
    equal.next = _quick_sort_ll(equal.next, equal)

    left_tail = left_dummy.next
    if left_tail:
        while left_tail.next:
            left_tail = left_tail.next
        left_tail.next = equal_dummy.next
    else:
        left_dummy.next = equal_dummy.next

    equal_tail = equal_dummy.next
    if equal_tail:
        while equal_tail.next:
            equal_tail = equal_tail.next
        equal_tail.next = _quick_sort_ll(right_dummy.next, right)
    else:
        left_tail.next = _quick_sort_ll(right_dummy.next, right)

    return left_dummy.next


# =============================================================================
# 9. COUNTING COMPARISONS
# =============================================================================

def quick_sort_counted(arr):
    """Quick sort counting comparisons"""
    comparisons = [0]

    def _sort(arr, low, high):
        if low < high:
            pivot_idx = partition_counted(arr, low, high)
            _sort(arr, low, pivot_idx - 1)
            _sort(arr, pivot_idx + 1, high)

    def partition_counted(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparisons[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _sort(arr, 0, len(arr) - 1)
    return arr, comparisons[0]

print("\n=== Quick Sort Comparisons ===")
test_cases = [
    [3, 6, 8, 10, 1, 2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
]

for arr in test_cases:
    _, comps = quick_sort_counted(arr.copy())
    print(f"{arr}: {comps} comparisons")


# =============================================================================
# 10. QUICK SORT VARIANTS COMPARISON
# =============================================================================

def compare_quick_sort_variants():
    """Compare different quick sort implementations"""
    import time

    print("\n=== Quick Sort Variants Comparison ===")
    sizes = [1000, 5000, 10000]

    for size in sizes:
        arr = list(range(size))
        random.shuffle(arr)

        # Basic
        test = arr.copy()
        start = time.time()
        quick_sort_inplace(test)
        basic_time = time.time() - start

        # Hoare
        test = arr.copy()
        start = time.time()
        quick_sort_hoare(test)
        hoare_time = time.time() - start

        # Three-way
        test = arr.copy()
        start = time.time()
        quick_sort_three_way(test)
        three_way_time = time.time() - start

        # Randomized
        test = arr.copy()
        start = time.time()
        randomized_quick_sort(test)
        random_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  Basic (Lomuto):  {basic_time*1000:.2f}ms")
        print(f"  Hoare:           {hoare_time*1000:.2f}ms")
        print(f"  Three-way:       {three_way_time*1000:.2f}ms")
        print(f"  Randomized:      {random_time*1000:.2f}ms")

compare_quick_sort_variants()


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Quick Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Quick sort is O(n log n) average, O(n^2) worst")
    print("2. In-place with O(log n) stack space")
    print("3. Randomized/median-of-three avoids worst case")
    print("4. Three-way partition handles duplicates efficiently")
    print("5. Quick select finds kth element in O(n) average")
