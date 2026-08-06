"""
DSA Tutorial 14 - Bubble Sort
==============================

Bubble Sort: Repeatedly swap adjacent elements if they're in wrong order.
Largest element "bubbles up" to the end in each pass.

Time Complexity:
- Best: O(n) - already sorted (with optimization)
- Average: O(n^2)
- Worst: O(n^2)
Space Complexity: O(1) - in-place
Stable: Yes
"""

# =============================================================================
# 1. BASIC BUBBLE SORT
# =============================================================================

def bubble_sort(arr):
    """Basic bubble sort. O(n^2) time, O(1) space"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print("=== Basic Bubble Sort ===")
arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")
print(f"Sorted: {bubble_sort(arr.copy())}")


# =============================================================================
# 2. OPTIMIZED BUBBLE SORT
# =============================================================================

def bubble_sort_optimized(arr):
    """Bubble sort with early termination. O(n) best case"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # Already sorted
    return arr

print("\n=== Optimized Bubble Sort ===")
arr = [1, 2, 3, 4, 5]  # Already sorted
print(f"Already sorted: {bubble_sort_optimized(arr.copy())}")

arr = [5, 1, 4, 2, 8]
print(f"Random: {bubble_sort_optimized(arr.copy())}")


# =============================================================================
# 3. BUBBLE SORT WITH STEP TRACKING
# =============================================================================

def bubble_sort_steps(arr):
    """Bubble sort showing each step"""
    n = len(arr)
    steps = []
    arr = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append(f"Swap {arr[j+1]} and {arr[j]}: {arr.copy()}")
        if not swapped:
            break

    return arr, steps

print("\n=== Bubble Sort with Steps ===")
arr = [5, 3, 8, 1, 2]
sorted_arr, steps = bubble_sort_steps(arr)
print(f"Original: {arr}")
for step in steps:
    print(f"  {step}")
print(f"Final: {sorted_arr}")


# =============================================================================
# 4. COUNTING COMPARISONS AND SWAPS
# =============================================================================

def bubble_sort_counted(arr):
    """Bubble sort counting comparisons and swaps"""
    n = len(arr)
    comparisons = 0
    swaps = 0
    arr = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return arr, comparisons, swaps

print("\n=== Bubble Sort Statistics ===")
test_cases = [
    [64, 34, 25, 12, 22, 11, 90],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 4, 1, 5, 9, 2, 6]
]

for arr in test_cases:
    sorted_arr, comps, swaps = bubble_sort_counted(arr)
    print(f"{arr}: {comps} comparisons, {swaps} swaps")


# =============================================================================
# 5. BUBBLE SORT DESCENDING
# =============================================================================

def bubble_sort_descending(arr):
    """Sort in descending order"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:  # Changed comparison
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

print("\n=== Descending Bubble Sort ===")
arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Descending: {bubble_sort_descending(arr.copy())}")


# =============================================================================
# 6. BUBBLE SORT ON LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def bubble_sort_linked_list(head):
    """Bubble sort on linked list. O(n^2)"""
    if not head:
        return head

    swapped = True
    while swapped:
        swapped = False
        current = head
        while current.next:
            if current.data > current.next.data:
                current.data, current.next.data = current.next.data, current.data
                swapped = True
            current = current.next

    return head

def linked_list_to_list(head):
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

print("\n=== Bubble Sort on Linked List ===")
values = [64, 34, 25, 12, 22]
head = Node(values[0])
current = head
for val in values[1:]:
    current.next = Node(val)
    current = current.next

head = bubble_sort_linked_list(head)
print(f"Sorted linked list: {linked_list_to_list(head)}")


# =============================================================================
# 7. COCKTAIL SHAKER SORT (BIDIRECTIONAL)
# =============================================================================

def cocktail_shaker_sort(arr):
    """Bidirectional bubble sort - sorts from both ends"""
    n = len(arr)
    start, end = 0, n - 1
    swapped = True

    while swapped:
        swapped = False

        # Forward pass
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        end -= 1

        # Backward pass
        for i in range(end, start, -1):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]
                swapped = True
        start += 1

    return arr

print("\n=== Cocktail Shaker Sort ===")
arr = [5, 1, 4, 2, 8, 0, 2]
print(f"Original: {arr}")
print(f"Sorted: {cocktail_shaker_sort(arr.copy())}")


# =============================================================================
# 8. COMB SORT
# =============================================================================

def comb_sort(arr):
    """Improved bubble sort using gap. O(n^2/2^p)"""
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True

        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False

    return arr

print("\n=== Comb Sort ===")
arr = [8, 4, 1, 56, 3, -44, 23, -6, 28, 0]
print(f"Original: {arr}")
print(f"Sorted: {comb_sort(arr.copy())}")


# =============================================================================
# 9. ODD-EVEN SORT
# =============================================================================

def odd_even_sort(arr):
    """Parallel-friendly variant of bubble sort"""
    n = len(arr)
    sorted_flag = False

    while not sorted_flag:
        sorted_flag = True

        # Odd phase
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False

        # Even phase
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False

    return arr

print("\n=== Odd-Even Sort ===")
arr = [5, 3, 8, 1, 9, 2, 7]
print(f"Original: {arr}")
print(f"Sorted: {odd_even_sort(arr.copy())}")


# =============================================================================
# 10. PERFORMANCE COMPARISON
# =============================================================================

def compare_bubble_variants():
    """Compare different bubble sort variants"""
    import time
    import random

    print("\n=== Performance Comparison ===")
    sizes = [100, 500, 1000]

    for size in sizes:
        arr = list(range(size))
        random.shuffle(arr)

        # Basic
        test = arr.copy()
        start = time.time()
        bubble_sort(test)
        basic_time = time.time() - start

        # Optimized
        test = arr.copy()
        start = time.time()
        bubble_sort_optimized(test)
        opt_time = time.time() - start

        # Cocktail
        test = arr.copy()
        start = time.time()
        cocktail_shaker_sort(test)
        cocktail_time = time.time() - start

        # Comb
        test = arr.copy()
        start = time.time()
        comb_sort(test)
        comb_time = time.time() - start

        print(f"\nn={size}:")
        print(f"  Basic:    {basic_time*1000:.2f}ms")
        print(f"  Optimized: {opt_time*1000:.2f}ms")
        print(f"  Cocktail: {cocktail_time*1000:.2f}ms")
        print(f"  Comb:     {comb_time*1000:.2f}ms")

compare_bubble_variants()


# =============================================================================
# 11. PRACTICAL EXAMPLES
# =============================================================================

print("\n=== Practical Examples ===")

# Sort student grades
def sort_grades(students):
    """Sort students by grade using bubble sort"""
    n = len(students)
    for i in range(n):
        for j in range(0, n - i - 1):
            if students[j][1] > students[j + 1][1]:
                students[j], students[j + 1] = students[j + 1], students[j]
    return students

students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 95)]
print(f"Students before: {students}")
print(f"Students after:  {sort_grades(students)}")

# Sort strings
def bubble_sort_strings(arr):
    """Sort strings lexicographically"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

words = ["banana", "apple", "cherry", "date"]
print(f"\nWords before: {words}")
print(f"Words after:  {bubble_sort_strings(words.copy())}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Bubble Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Bubble sort is simple but O(n^2)")
    print("2. Optimization: stop if no swaps in a pass")
    print("3. Stable sort - maintains relative order")
    print("4. In-place - O(1) extra space")
    print("5. Use only for small or nearly sorted datasets")
