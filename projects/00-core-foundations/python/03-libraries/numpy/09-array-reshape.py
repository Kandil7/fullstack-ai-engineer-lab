"""
Array Reshape
W3Schools: https://www.w3schools.com/python/numpy_array_reshape.asp

Changing the shape of arrays without changing their data.
"""

import numpy as np

# ============================================================
# Example 1: Basic Reshape
# reshape() returns a new array with specified shape.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
print("Original:", arr)
print("Shape:", arr.shape)  # (12,)

# Reshape to 3 rows, 4 columns
arr_3x4 = arr.reshape(3, 4)
print("\nReshaped to 3x4:\n", arr_3x4)
print("Shape:", arr_3x4.shape)  # (3, 4)

# Reshape to 4 rows, 3 columns
arr_4x3 = arr.reshape(4, 3)
print("\nReshaped to 4x3:\n", arr_4x3)
print("Shape:", arr_4x3.shape)  # (4, 3)

# Reshape to 2x2x3 (3D)
arr_3d = arr.reshape(2, 2, 3)
print("\nReshaped to 2x2x3:\n", arr_3d)
print("Shape:", arr_3d.shape)  # (2, 2, 3)
# Output:
# Original: [ 1  2  3  4  5  6  7  8  9 10 11 12]
# Shape: (12,)
#
# Reshaped to 3x4:
#  [[ 1  2  3  4]
#   [ 5  6  7  8]
#   [ 9 10 11 12]]
# Shape: (3, 4)

# ============================================================
# Example 2: Reshape with -1
# -1 lets NumPy auto-calculate that dimension.
# ============================================================

arr = np.arange(24)
print("\nOriginal:", arr)
print("Shape:", arr.shape)  # (24,)

# Calculate columns automatically
arr_auto = arr.reshape(6, -1)
print("\nReshape(6, -1):", arr_auto.shape)  # (6, 4)

# Calculate rows automatically
arr_auto2 = arr.reshape(-1, 8)
print("Reshape(-1, 8):", arr_auto2.shape)  # (3, 8)

# Flatten with -1
arr_flat = arr.reshape(-1)
print("Reshape(-1,):", arr_flat.shape)  # (24,)

# 3D with -1
arr_3d = arr.reshape(2, 3, -1)
print("Reshape(2, 3, -1):", arr_3d.shape)  # (2, 3, 4)

# Two -1 dimensions is not allowed
try:
    arr.reshape(-1, -1)
except ValueError as e:
    print("\nError with two -1s:", e)
# Output:
# Original: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23]
# Shape: (24,)
#
# Reshape(6, -1): (6, 4)
# Reshape(-1, 8): (3, 8)
# Reshape(-1,): (24,)
# Reshape(2, 3, -1): (2, 3, 4)

# ============================================================
# Example 3: Flatten and Ravel
# Flatten always returns a copy; ravel returns a view when possible.
# ============================================================

arr = np.array([[1, 2, 3], [4, 5, 6]])
print("\nOriginal:\n", arr)
print("Shape:", arr.shape)  # (2, 3)

# flatten() - returns a copy
flat = arr.flatten()
print("\nFlattened:", flat)  # [1 2 3 4 5 6]
print("Shape:", flat.shape)  # (6,)

# ravel() - returns a view when possible
ravel = arr.ravel()
print("Raveled:", ravel)    # [1 2 3 4 5 6]
print("Shape:", ravel.shape)  # (6,)

# Test: flatten is a copy, ravel is a view
flat[0] = 999
print("\nAfter flat[0]=999:")
print("Original:\n", arr)  # UNCHANGED

ravel[0] = 888
print("After ravel[0]=888:")
print("Original:\n", arr)  # CHANGED!
# Output:
# Original:
#  [[1 2 3]
#   [4 5 6]]
# Shape: (2, 3)
#
# Flattened: [1 2 3 4 5 6]
# Shape: (6,)
#
# After flat[0]=999:
# Original:
#  [[1 2 3]
#   [4 5 6]]
# After ravel[0]=888:
# Original:
#  [[888   2   3]
#   [  4   5   6]]

# ============================================================
# Example 4: Resize
# resize changes shape, repeating data if necessary.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])
print("\nOriginal:", arr)
print("Shape:", arr.shape)  # (5,)

# np.resize - changes size, repeats data if needed
resized = np.resize(arr, (3, 4))
print("\nResized to (3,4):\n", resized)
print("Shape:", resized.shape)  # (3, 4)
# Data is repeated to fill the new shape

# Method resize - modifies in place
arr2 = np.array([1, 2, 3])
arr2.resize(2, 3)
print("\nMethod resize to (2,3):\n", arr2)
# Output:
# Original: [1 2 3 4 5]
# Shape: (5,)
#
# Resized to (3,4):
#  [[1 2 3 4]
#   [5 1 2 3]
#   [4 5 1 2]]
# Shape: (3, 4)

# ============================================================
# Example 5: Squeeze and Expand_dims
# Add or remove dimensions of size 1.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])
print("\nOriginal shape:", arr.shape)  # (5,)

# expand_dims - add a new dimension
arr_row = np.expand_dims(arr, axis=0)
print("expand_dims(axis=0):", arr_row.shape)  # (1, 5)

arr_col = np.expand_dims(arr, axis=1)
print("expand_dims(axis=1):", arr_col.shape)  # (5, 1)

# squeeze - remove dimensions of size 1
arr_3d = np.array([[[1, 2, 3, 4, 5]]])
print("\n3D array shape:", arr_3d.shape)  # (1, 1, 5)

squeezed = arr_3d.squeeze()
print("Squeezed:", squeezed.shape)  # (5,)

# Squeeze specific axis
arr_2d = np.array([[[1, 2, 3]], [[4, 5, 6]]])
print("\nBefore squeeze:", arr_2d.shape)  # (2, 1, 3)
squeezed = arr_2d.squeeze(axis=1)
print("After squeeze(axis=1):", squeezed.shape)  # (2, 3)
# Output:
# Original shape: (5,)
# expand_dims(axis=0): (1, 5)
# expand_dims(axis=1): (5, 1)
#
# 3D array shape: (1, 1, 5)
# Squeezed: (5,)
#
# Before squeeze: (2, 1, 3)
# After squeeze(axis=1): (2, 3)
