"""
Copy vs View
W3Schools: https://www.w3schools.com/python/numpy_copy_vs_view.asp

Understanding the difference between copies and views of arrays.
"""

import numpy as np

# ============================================================
# Example 1: Array View
# A view is a reference to the original array's data.
# Changes to the view affect the original.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])
view = arr.view()

print("Original:", arr)      # [1 2 3 4 5]
print("View:", view)         # [1 2 3 4 5]
print("Same data?", arr.ctypes.data == view.ctypes.data)  # True

# Modify the view
view[0] = 100
print("\nAfter view[0]=100:")
print("Original:", arr)      # [100   2   3   4   5]  (CHANGED!)
print("View:", view)         # [100   2   3   4   5]

# Modify the original
arr[1] = 200
print("\nAfter arr[1]=200:")
print("Original:", arr)      # [100 200   3   4   5]
print("View:", view)         # [100 200   3   4   5]  (CHANGED!)
# Output:
# Original: [1 2 3 4 5]
# View: [1 2 3 4 5]
# Same data? True
#
# After view[0]=100:
# Original: [100   2   3   4   5]
# View: [100   2   3   4   5]
#
# After arr[1]=200:
# Original: [100 200   3   4   5]
# View: [100 200   3   4   5]

# ============================================================
# Example 2: Array Copy
# A copy is an independent array with its own data.
# Changes to the copy do NOT affect the original.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])
copy_arr = arr.copy()

print("\nOriginal:", arr)      # [1 2 3 4 5]
print("Copy:", copy_arr)      # [1 2 3 4 5]
print("Same data?", arr.ctypes.data == copy_arr.ctypes.data)  # False

# Modify the copy
copy_arr[0] = 100
print("\nAfter copy_arr[0]=100:")
print("Original:", arr)      # [1 2 3 4 5]  (UNCHANGED!)
print("Copy:", copy_arr)     # [100   2   3   4   5]

# Modify the original
arr[1] = 200
print("\nAfter arr[1]=200:")
print("Original:", arr)      # [100 200   3   4   5]
print("Copy:", copy_arr)     # [100   2   3   4   5]  (UNCHANGED!)
# Output:
# Original: [1 2 3 4 5]
# Copy: [1 2 3 4 5]
# Same data? False
#
# After copy_arr[0]=100:
# Original: [1 2 3 4 5]
# Copy: [100   2   3   4   5]
#
# After arr[1]=200:
# Original: [100 200   3   4   5]
# Copy: [100   2   3   4   5]

# ============================================================
# Example 3: View from Slicing
# Slicing creates a view, not a copy.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# Slice creates a view
slice_view = arr[2:6]
print("\nOriginal:", arr)          # [1 2 3 4 5 6 7 8]
print("Slice view:", slice_view)  # [3 4 5 6]

# Check if it's a view
print("Is view?", slice_view.base is arr)  # True

# Modify the slice
slice_view[0] = 999
print("\nAfter slice_view[0]=999:")
print("Original:", arr)          # [  1   2 999   4   5   6   7   8]
print("Slice view:", slice_view)  # [999   4   5   6]
# Output:
# Original: [1 2 3 4 5 6 7 8]
# Slice view: [3 4 5 6]
# Is view? True
#
# After slice_view[0]=999:
# Original: [  1   2 999   4   5   6   7   8]
# Slice view: [999   4   5   6]

# ============================================================
# Example 4: Copy vs View with reshape
# reshape() may return a view or copy depending on memory layout.
# ============================================================

arr = np.arange(12)
print("\nOriginal:", arr)
print("Shape:", arr.shape)  # (12,)

# reshape returns a view when possible
reshaped = arr.reshape(3, 4)
print("\nReshaped:\n", reshaped)
print("Is view?", reshaped.base is arr)  # True

# Modify reshape view
reshaped[0, 0] = 999
print("After reshaped[0,0]=999:")
print("Original:", arr)  # Original is modified!

# Use copy() to avoid this
arr2 = np.arange(12)
reshaped2 = arr2.reshape(3, 4).copy()
reshaped2[0, 0] = 888
print("\nAfter copy reshape modification:")
print("Original arr2:", arr2)  # arr2 is NOT modified
# Output:
# Original: [ 0  1  2  3  4  5  6  7  8  9 10 11]
# Shape: (12,)
#
# Reshaped:
#  [[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]
# Is view? True
#
# After reshaped[0,0]=999:
# Original: [999   1   2   3   4   5   6   7   8   9  10  11]
#
# After copy reshape modification:
# Original arr2: [ 0  1  2  3  4  5  6  7  8  9 10 11]

# ============================================================
# Example 5: Checking Copy vs View
# Use .base attribute to check if array is a view.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# View
view = arr.view()
print("\nView.base is arr:", view.base is arr)  # True
print("View.base:", view.base)  # [1 2 3 4 5]

# Copy
copy_arr = arr.copy()
print("Copy.base is arr:", copy_arr.base is arr)  # False
print("Copy.base:", copy_arr.base)  # None

# Slicing view
slice_view = arr[1:4]
print("Slice.base is arr:", slice_view.base is arr)  # True

# np.array() with copy=False
arr2 = np.array(arr, copy=False)
print("\nnp.array(copy=False) view:", arr2.base is arr)  # True

# Using nditer (creates views)
for x in np.nditer(arr):
    pass  # x is a view
