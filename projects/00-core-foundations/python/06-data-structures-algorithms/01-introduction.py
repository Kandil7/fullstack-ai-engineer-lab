"""
DSA Tutorial 01 - Introduction to Data Structures & Algorithms
==============================================================

Data: Raw facts (numbers, strings, objects)
Data Structure: Organized way to store data
Algorithm: Step-by-step procedure to solve a problem

Why DSA matters:
- Efficient memory usage
- Faster computation
- Real-world problem solving
"""

# =============================================================================
# 1. WHAT IS DATA?
# =============================================================================

# Data comes in different forms
name = "Alice"          # String data
age = 30                # Integer data
scores = [95, 87, 92]  # Collection data
person = {"name": "Bob", "age": 25}  # Structured data

print("=== Types of Data ===")
print(f"String: {name}")
print(f"Integer: {age}")
print(f"List: {scores}")
print(f"Dict: {person}")


# =============================================================================
# 2. WHAT IS A DATA STRUCTURE?
# =============================================================================

# A data structure is a specific way to organize, process, and store data.

# Examples of built-in Python data structures:
# List (Dynamic array)
fruits = ["apple", "banana", "cherry"]

# Tuple (Immutable sequence)
colors = ("red", "green", "blue")

# Dictionary (Key-value pairs)
ages = {"Alice": 30, "Bob": 25, "Charlie": 35}

# Set (Unique elements, unordered)
unique_nums = {1, 2, 3, 3, 4}  # Duplicate 3 is removed

print("\n=== Built-in Data Structures ===")
print(f"List: {fruits}")
print(f"Tuple: {colors}")
print(f"Dict: {ages}")
print(f"Set: {unique_nums}")


# =============================================================================
# 3. WHAT IS AN ALGORITHM?
# =============================================================================

# An algorithm is a finite sequence of well-defined instructions.

# Example: Find the largest number in a list
def find_largest(numbers):
    """Simple algorithm: scan and compare"""
    if not numbers:
        return None
    largest = numbers[0]
    for num in numbers[1:]:
        if num > largest:
            largest = num
    return largest

print("\n=== Algorithm Example ===")
nums = [34, 78, 12, 99, 45]
print(f"Largest in {nums}: {find_largest(nums)}")


# =============================================================================
# 4. TIME COMPLEXITY - Big O Notation
# =============================================================================

# Big O describes how runtime grows with input size.
# We measure the worst case.

# O(1) - Constant time
def get_first(lst):
    """Always takes 1 step regardless of list size"""
    return lst[0]

# O(n) - Linear time
def linear_search(lst, target):
    """Worst case: check every element"""
    for i, val in enumerate(lst):
        if val == target:
            return i
    return -1

# O(n^2) - Quadratic time
def bubble_sort_step(lst):
    """Nested loops = n * n operations"""
    comparisons = 0
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst, comparisons

# O(log n) - Logarithmic time
def binary_search_demo(sorted_lst, target):
    """Halves the search space each step"""
    steps = 0
    low, high = 0, len(sorted_lst) - 1
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if sorted_lst[mid] == target:
            return mid, steps
        elif sorted_lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps

print("\n=== Time Complexity Demo ===")
test_list = list(range(1, 101))

# O(1)
print(f"O(1) get_first: {get_first(test_list)}")

# O(n)
result = linear_search(test_list, 50)
print(f"O(n) linear_search(50): index={result}")

# O(n^2)
sort_result, comps = bubble_sort_step([5, 3, 8, 1, 2])
print(f"O(n^2) bubble_sort comparisons on 5 elements: {comps}")

# O(log n)
idx, steps = binary_search_demo(test_list, 50)
print(f"O(log n) binary_search(50) in 100 elements: {steps} steps")


# =============================================================================
# 5. SPACE COMPLEXITY
# =============================================================================

# Space complexity measures how much memory an algorithm uses.

# O(1) space - no extra data structures
def sum_list(nums):
    total = 0
    for n in nums:
        total += n
    return total

# O(n) space - creates new list
def double_list(nums):
    return [n * 2 for n in nums]

# O(n^2) space - creates matrix
def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

print("\n=== Space Complexity Demo ===")
test_nums = [1, 2, 3, 4, 5]
print(f"Sum: {sum_list(test_nums)}  (O(1) space)")
print(f"Doubled: {double_list(test_nums)}  (O(n) space)")
print(f"Identity 3x3: {identity_matrix(3)}  (O(n^2) space)")


# =============================================================================
# 6. COMMON ALGORITHM CATEGORIES
# =============================================================================

# Searching
print("\n=== Searching Algorithms ===")
data = [10, 23, 45, 70, 11, 15]
target = 70

# Linear search
for i, v in enumerate(data):
    if v == target:
        print(f"Linear search found {target} at index {i}")
        break

# Binary search (requires sorted data)
sorted_data = sorted(data)
low, high = 0, len(sorted_data) - 1
while low <= high:
    mid = (low + high) // 2
    if sorted_data[mid] == target:
        print(f"Binary search found {target} at index {mid}")
        break
    elif sorted_data[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

# Sorting
print("\n=== Sorting Algorithms ===")
unsorted = [64, 34, 25, 12, 22, 11, 90]

# Bubble sort
arr = unsorted.copy()
for i in range(len(arr)):
    for j in range(0, len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
print(f"Bubble sort: {arr}")


# =============================================================================
# 7. RECURSION BASICS
# =============================================================================

# A function that calls itself
def factorial(n):
    """Factorial: n! = n * (n-1)! with base case n=1"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """Fibonacci: F(n) = F(n-1) + F(n-2)"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n=== Recursion Basics ===")
print(f"5! = {factorial(5)}")
print(f"Fibonacci(10) = {fibonacci(10)}")


# =============================================================================
# 8. COMPLEXITY COMPARISON TABLE
# =============================================================================

def complexity_table():
    """Visualize how different complexities scale"""
    print("\n=== Complexity Comparison (N = input size) ===")
    print(f"{'N':<8} {'O(1)':<10} {'O(log n)':<12} {'O(n)':<10} {'O(n log n)':<14} {'O(n^2)':<10}")
    print("-" * 65)
    for n in [1, 10, 100, 1000, 10000]:
        import math
        log_n = math.log2(n) if n > 0 else 0
        print(f"{n:<8} {1:<10} {log_n:<12.1f} {n:<10} {n * log_n:<14.1f} {n**2:<10}")

complexity_table()


# =============================================================================
# 9. PRACTICAL EXERCISES
# =============================================================================

print("\n=== Practice Exercises ===")

# Exercise 1: Count occurrences
def count_occurrences(lst, target):
    """O(n) time, O(1) space"""
    count = 0
    for item in lst:
        if item == target:
            count += 1
    return count

test = [1, 2, 3, 2, 4, 2, 5]
print(f"Count of 2 in {test}: {count_occurrences(test, 2)}")

# Exercise 2: Reverse a list in-place
def reverse_in_place(lst):
    """O(n) time, O(1) space - two pointer approach"""
    left, right = 0, len(lst) - 1
    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return lst

nums = [1, 2, 3, 4, 5]
reverse_in_place(nums)
print(f"Reversed in-place: {nums}")

# Exercise 3: Check if palindrome
def is_palindrome(s):
    """O(n) time, O(1) space"""
    s = s.lower().replace(" ", "")
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
print(f"'hello' is palindrome: {is_palindrome('hello')}")


# =============================================================================
# 10. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Introduction to DSA - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Data structures organize data efficiently")
    print("2. Algorithms solve problems step-by-step")
    print("3. Big O notation measures time/space complexity")
    print("4. O(1) < O(log n) < O(n) < O(n log n) < O(n^2)")
    print("5. Choose the right structure for your problem")
