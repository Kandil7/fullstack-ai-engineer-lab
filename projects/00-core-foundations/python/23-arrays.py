"""
W3Schools Python Tutorial - 23: Python Arrays
==============================================
Topics: Creating arrays, accessing, modifying, array methods

Note: Python lists are the standard way to work with arrays.
The array module provides typed arrays for efficiency.

Run: python 23-arrays.py
Reference: https://www.w3schools.com/python/python_arrays.asp
"""

# ============================================================
# Python Lists as Arrays
# ============================================================
# In Python, lists are the most common way to work with arrays.
# They can hold any type of data.

# Example 1: Creating a list (array)
fruits = ["apple", "banana", "cherry", "date"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed: {mixed}")

# Output:
# Fruits: ['apple', 'banana', 'cherry', 'date']
# Numbers: [1, 2, 3, 4, 5]
# Mixed: [1, 'hello', 3.14, True]

# ============================================================
# Accessing Array Items
# ============================================================
# Example 2: Indexing and slicing
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(f"\nFirst: {fruits[0]}")      # apple
print(f"Last: {fruits[-1]}")        # elderberry
print(f"Slice [1:3]: {fruits[1:3]}")  # ['banana', 'cherry']
print(f"Every other: {fruits[::2]}")  # ['apple', 'cherry', 'elderberry']
print(f"Reversed: {fruits[::-1]}")   # ['elderberry', 'date', 'cherry', 'banana', 'apple']

# ============================================================
# Modifying Array Items
# ============================================================
# Example 3: Changing values
numbers = [1, 2, 3, 4, 5]
print(f"\nOriginal: {numbers}")

numbers[0] = 100
print(f"After numbers[0] = 100: {numbers}")

numbers[-1] = 500
print(f"After numbers[-1] = 500: {numbers}")

numbers[1:3] = [20, 30]
print(f"After numbers[1:3] = [20, 30]: {numbers}")

# ============================================================
# Array Methods
# ============================================================
# Example 4: Common array operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(f"\nOriginal: {numbers}")
print(f"Length: {len(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Max: {max(numbers)}")
print(f"Sum: {sum(numbers)}")
print(f"Index of 5: {numbers.index(5)}")
print(f"Count of 1: {numbers.count(1)}")

# ============================================================
# Adding Items
# ============================================================
# Example 5: Different ways to add items
fruits = ["apple", "banana"]
print(f"\nOriginal: {fruits}")

# append() - add to end
fruits.append("cherry")
print(f"After append: {fruits}")

# insert() - add at index
fruits.insert(1, "avocado")
print(f"After insert: {fruits}")

# extend() - add multiple items
fruits.extend(["date", "elderberry"])
print(f"After extend: {fruits}")

# + operator
fruits = fruits + ["fig"]
print(f"After +: {fruits}")

# ============================================================
# Removing Items
# ============================================================
# Example 6: Different ways to remove items
fruits = ["apple", "banana", "cherry", "banana", "date"]
print(f"\nOriginal: {fruits}")

# remove() - remove first occurrence
fruits.remove("banana")
print(f"After remove: {fruits}")

# pop() - remove and return
last = fruits.pop()
print(f"After pop: {fruits}, removed: {last}")

# del - remove by index
del fruits[0]
print(f"After del: {fruits}")

# clear() - remove all
fruits.clear()
print(f"After clear: {fruits}")

# ============================================================
# The array Module (Typed Arrays)
# ============================================================
# Example 7: Using the array module for typed arrays
import array

# Create a typed array (all elements must be same type)
arr = array.array('i', [1, 2, 3, 4, 5])  # 'i' = signed int
print(f"\nTyped array: {arr}")
print(f"Type: {type(arr)}")

# Access and modify like a list
print(f"First: {arr[0]}")
print(f"Last: {arr[-1]}")

# Add items
arr.append(6)
arr.insert(0, 0)
print(f"After append/insert: {arr}")

# Remove items
arr.remove(3)
popped = arr.pop()
print(f"After remove/pop: {arr}")

# ============================================================
# Array Type Codes
# ============================================================
# Example 8: Different array types
print("\n--- Array Type Codes ---")

# 'b' = signed char
bytes_arr = array.array('b', [65, 66, 67])
print(f"Char array: {bytes_arr}")

# 'f' = float
float_arr = array.array('f', [1.1, 2.2, 3.3])
print(f"Float array: {float_arr}")

# 'd' = double
double_arr = array.array('d', [1.1, 2.2, 3.3])
print(f"Double array: {double_arr}")

# 'u' = Unicode character
unicode_arr = array.array('u', ['a', 'b', 'c'])
print(f"Unicode array: {unicode_arr}")

# ============================================================
# NumPy Arrays (Bonus)
# ============================================================
# Example 9: If you have NumPy installed
try:
    import numpy as np
    
    # Create NumPy array
    arr = np.array([1, 2, 3, 4, 5])
    print(f"\nNumPy array: {arr}")
    print(f"Type: {type(arr)}")
    
    # Operations are element-wise
    print(f"Double: {arr * 2}")
    print(f"Squared: {arr ** 2}")
    print(f"Sum: {arr.sum()}")
    print(f"Mean: {arr.mean()}")
    
    # 2D array (matrix)
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\nMatrix:\n{matrix}")
    print(f"Shape: {matrix.shape}")
    
except ImportError:
    print("\nNumPy not installed. Install with: pip install numpy")

# ============================================================
# Practical Examples
# ============================================================
# Example 10: Array operations
print("\n--- Practical Examples ---")

# Find duplicates
numbers = [1, 2, 3, 2, 4, 3, 5, 1]
seen = set()
duplicates = []
for num in numbers:
    if num in seen:
        duplicates.append(num)
    seen.add(num)
print(f"Duplicates: {duplicates}")

# Rotate array
def rotate_right(arr, k):
    """Rotate array k positions to the right."""
    k = k % len(arr)
    return arr[-k:] + arr[:-k]

arr = [1, 2, 3, 4, 5]
rotated = rotate_right(arr, 2)
print(f"Rotated right by 2: {rotated}")

# Find missing number
def find_missing(arr):
    """Find missing number in 1 to n sequence."""
    n = len(arr) + 1
    total = n * (n + 1) // 2
    return total - sum(arr)

arr = [1, 2, 4, 5, 6]
missing = find_missing(arr)
print(f"Missing number: {missing}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Python lists are the standard way to work with arrays")
print("2. Access with index: arr[0], arr[-1]")
print("3. Slice with arr[start:stop:step]")
print("4. Add: append(), insert(), extend()")
print("5. Remove: remove(), pop(), del, clear()")
print("6. array module: typed arrays for efficiency")
print("7. NumPy: powerful array operations (install separately)")
