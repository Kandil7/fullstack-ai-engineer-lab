"""
DSA Tutorial 16 - Insertion Sort
==================================

Insertion Sort: Build sorted portion one element at a time.
Like sorting playing cards in your hand.

Time Complexity:
- Best: O(n) - already sorted
- Average: O(n^2)
- Worst: O(n^2) - reverse sorted
Space Complexity: O(1) - in-place
Stable: Yes
"""

# =============================================================================
# 1. BASIC INSERTION SORT
# =============================================================================

def insertion_sort(arr):
    """Basic insertion sort. O(n^2) time, O(1) space"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Shift elements greater than key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

print("=== Basic Insertion Sort ===")
arr = [12, 11, 13, 5, 6]
print(f"Original: {arr}")
print(f"Sorted: {insertion_sort(arr.copy())}")


# =============================================================================
# 2. INSERTION SORT WITH STEPS
# =============================================================================

def insertion_sort_steps(arr):
    """Insertion sort showing each step"""
    arr = arr.copy()
    steps = []

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
        steps.append(f"Insert {key}: {arr.copy()}")

    return arr, steps

print("\n=== Insertion Sort with Steps ===")
arr = [5, 2, 4, 6, 1, 3]
sorted_arr, steps = insertion_sort_steps(arr)
for step in steps:
    print(f"  {step}")
print(f"Final: {sorted_arr}")


# =============================================================================
# 3. BINARY INSERTION SORT
# =============================================================================

def binary_insertion_sort(arr):
    """Use binary search to find insertion position. O(n^2) but fewer comparisons"""
    for i in range(1, len(arr)):
        key = arr[i]

        # Binary search for position
        low, high = 0, i - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] > key:
                high = mid - 1
            else:
                low = mid + 1

        # Shift elements
        for j in range(i - 1, low - 1, -1):
            arr[j + 1] = arr[j]
        arr[low] = key

    return arr

print("\n=== Binary Insertion Sort ===")
arr = [37, 23, 0, 31, 22, 10, 13]
print(f"Original: {arr}")
print(f"Sorted: {binary_insertion_sort(arr.copy())}")


# =============================================================================
# 4. INSERTION SORT DESCENDING
# =============================================================================

def insertion_sort_descending(arr):
    """Sort in descending order"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] < key:  # Changed comparison
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

print("\n=== Descending Insertion Sort ===")
arr = [12, 11, 13, 5, 6]
print(f"Descending: {insertion_sort_descending(arr.copy())}")


# =============================================================================
# 5. COUNTING OPERATIONS
# =============================================================================

def insertion_sort_counted(arr):
    """Insertion sort counting comparisons and shifts"""
    comparisons = 0
    shifts = 0
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break

        arr[j + 1] = key

    return arr, comparisons, shifts

print("\n=== Insertion Sort Statistics ===")
test_cases = [
    [12, 11, 13, 5, 6],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [2, 3, 4, 5, 1],
]

for arr in test_cases:
    sorted_arr, comps, shifts = insertion_sort_counted(arr)
    print(f"{arr}: {comps} comparisons, {shifts} shifts")


# =============================================================================
# 6. SHELL SORT (INSERTION SORT VARIANT)
# =============================================================================

def shell_sort(arr):
    """Shell sort - insertion sort with diminishing gaps. O(n^1.25)"""
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            key = arr[i]
            j = i

            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = key

        gap //= 2

    return arr

print("\n=== Shell Sort ===")
arr = [12, 34, 54, 2, 3, 17, 9, 81]
print(f"Original: {arr}")
print(f"Sorted: {shell_sort(arr.copy())}")


# =============================================================================
# 7. INSERTION SORT ON LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def insertion_sort_linked_list(head):
    """Insertion sort on linked list. O(n^2)"""
    if not head or not head.next:
        return head

    sorted_head = None
    current = head

    while current:
        next_node = current.next
        sorted_head = sorted_insert(sorted_head, current)
        current = next_node

    return sorted_head

def sorted_insert(head, node):
    """Insert node into sorted linked list"""
    if not head or node.data <= head.data:
        node.next = head
        return node

    current = head
    while current.next and current.next.data < node.data:
        current = current.next

    node.next = current.next
    current.next = node
    return head

def linked_list_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

print("\n=== Insertion Sort on Linked List ===")
values = [12, 11, 13, 5, 6]
head = Node(values[0])
current = head
for val in values[1:]:
    current.next = Node(val)
    current = current.next

head = insertion_sort_linked_list(head)
print(f"Sorted: {linked_list_to_list(head)}")


# =============================================================================
# 8. INSERTION SORT FOR 2D ARRAY
# =============================================================================

def insertion_sort_2d(matrix):
    """Sort each row of a 2D array"""
    for row in matrix:
        insertion_sort(row)
    return matrix

print("\n=== Insertion Sort 2D Array ===")
matrix = [
    [5, 2, 8],
    [1, 9, 3],
    [7, 4, 6]
]
print("Before:")
for row in matrix:
    print(f"  {row}")

insertion_sort_2d(matrix)
print("After (each row sorted):")
for row in matrix:
    print(f"  {row}")


# =============================================================================
# 9. PARTIAL INSERTION SORT
# =============================================================================

def partial_insertion_sort(arr, k):
    """Sort only the first k elements. O(k^2)"""
    for i in range(1, min(k, len(arr))):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

print("\n=== Partial Insertion Sort ===")
arr = [5, 3, 8, 1, 9, 2, 7, 4, 6]
print(f"Original: {arr}")
print(f"Sort first 4: {partial_insertion_sort(arr.copy(), 4)}")


# =============================================================================
# 10. INSERTION SORT PERFORMANCE
# =============================================================================

def analyze_insertion_sort():
    """Analyze insertion sort on different inputs"""
    import time
    import random

    print("\n=== Insertion Sort Analysis ===")
    sizes = [100, 500, 1000]

    for size in sizes:
        # Random
        arr = list(range(size))
        random.shuffle(arr)
        start = time.time()
        insertion_sort(arr.copy())
        random_time = time.time() - start

        # Nearly sorted (10% random)
        arr = list(range(size))
        for _ in range(size // 10):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        start = time.time()
        insertion_sort(arr.copy())
        nearly_time = time.time() - start

        # Reverse sorted
        arr = list(range(size, 0, -1))
        start = time.time()
        insertion_sort(arr.copy())
        reverse_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  Random:       {random_time*1000:.2f}ms")
        print(f"  Nearly sorted: {nearly_time*1000:.2f}ms")
        print(f"  Reverse:      {reverse_time*1000:.2f}ms")

analyze_insertion_sort()


# =============================================================================
# 11. PRACTICAL APPLICATIONS
# =============================================================================

print("\n=== Practical Applications ===")

# Sort while maintaining relative order
def stable_sort_custom(arr, key_func):
    """Stable insertion sort with custom key"""
    for i in range(1, len(arr)):
        key = arr[i]
        key_val = key_func(key)
        j = i - 1

        while j >= 0 and key_func(arr[j]) > key_val:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

# Sort tuples by second element
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 92)]
print(f"Students: {students}")
sorted_students = stable_sort_custom(students.copy(), lambda x: x[1])
print(f"Sorted by grade: {sorted_students}")

# Insert into sorted list
def insert_into_sorted(sorted_arr, value):
    """Insert value while maintaining sorted order"""
    i = len(sorted_arr) - 1
    sorted_arr.append(None)

    while i >= 0 and sorted_arr[i] > value:
        sorted_arr[i + 1] = sorted_arr[i]
        i -= 1

    sorted_arr[i + 1] = value
    return sorted_arr

sorted_list = [1, 3, 5, 7, 9]
print(f"\nInsert 4 into {sorted_list}: {insert_into_sorted(sorted_list.copy(), 4)}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Insertion Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Insertion sort is efficient for small/nearly sorted data")
    print("2. O(n) best case for already sorted arrays")
    print("3. Stable sort - maintains relative order")
    print("4. In-place with O(1) space")
    print("5. Shell sort improves performance with gap-based insertion")
