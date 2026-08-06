"""
Array Shape
W3Schools: https://www.w3schools.com/python/numpy_array_shape.asp

Understanding and inspecting array shapes and dimensions.
"""

import numpy as np

# ============================================================
# Example 1: Array Shape Attribute
# shape returns a tuple representing array dimensions.
# ============================================================

# 1D array
arr1d = np.array([1, 2, 3, 4, 5])
print("1D shape:", arr1d.shape)     # (5,)
print("ndim:", arr1d.ndim)         # 1
print("size:", arr1d.size)         # 5

# 2D array (3 rows, 4 columns)
arr2d = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])
print("\n2D shape:", arr2d.shape)   # (3, 4)
print("ndim:", arr2d.ndim)         # 2
print("rows:", arr2d.shape[0])     # 3
print("cols:", arr2d.shape[1])     # 4

# 3D array
arr3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print("\n3D shape:", arr3d.shape)   # (2, 2, 2)
print("ndim:", arr3d.ndim)         # 3
# Output:
# 1D shape: (5,)
# ndim: 1
# size: 5
#
# 2D shape: (3, 4)
# ndim: 2
# rows: 3
# cols: 4
#
# 3D shape: (2, 2, 2)
# ndim: 3

# ============================================================
# Example 2: Reshape Arrays
# Change array shape without changing data.
# ============================================================

arr = np.arange(12)
print("\nOriginal:", arr)
print("Shape:", arr.shape)  # (12,)

# Reshape to 3x4
arr_3x4 = arr.reshape(3, 4)
print("\nReshaped to 3x4:\n", arr_3x4)
print("Shape:", arr_3x4.shape)  # (3, 4)

# Reshape to 4x3
arr_4x3 = arr.reshape(4, 3)
print("\nReshaped to 4x3:\n", arr_4x3)
print("Shape:", arr_4x3.shape)  # (4, 3)

# Reshape to 2x2x3
arr_3d = arr.reshape(2, 2, 3)
print("\nReshaped to 2x2x3:\n", arr_3d)
print("Shape:", arr_3d.shape)  # (2, 2, 3)

# Flatten to 1D
arr_flat = arr_3x4.flatten()
print("\nFlattened:", arr_flat)
print("Shape:", arr_flat.shape)  # (12,)
# Output:
# Original: [ 0  1  2  3  4  5  6  7  8  9 10 11]
# Shape: (12,)
#
# Reshaped to 3x4:
#  [[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]
# Shape: (3, 4)

# ============================================================
# Example 3: Reshape with Unknown Dimension
# Use -1 to let NumPy calculate the dimension.
# ============================================================

arr = np.arange(12)

# Let NumPy figure out number of rows
arr_unknown = arr.reshape(-1, 4)
print("\nReshape(-1, 4):", arr_unknown.shape)  # (3, 4)

# Let NumPy figure out number of columns
arr_unknown2 = arr.reshape(3, -1)
print("Reshape(3, -1):", arr_unknown2.shape)  # (3, 4)

# 1D with -1
arr_unknown3 = arr.reshape(-1)
print("Reshape(-1,):", arr_unknown3.shape)  # (12,)

# 3D with -1
arr_unknown4 = arr.reshape(2, -1, 3)
print("Reshape(2, -1, 3):", arr_unknown4.shape)  # (2, 2, 3)

# ravel returns a flattened view
arr_ravel = arr.ravel()
print("\nRavel:", arr_ravel)
print("Shape:", arr_ravel.shape)  # (12,)
# Output:
# Reshape(-1, 4): (3, 4)
# Reshape(3, -1): (3, 4)
# Reshape(-1,): (12,)
# Reshape(2, -1, 3): (2, 2, 3)

# ============================================================
# Example 4: Transpose (Swapping Dimensions)
# Transpose reverses the order of dimensions.
# ============================================================

arr = np.array([[1, 2, 3], [4, 5, 6]])
print("\nOriginal:\n", arr)
print("Shape:", arr.shape)  # (2, 3)

# Transpose
arr_t = arr.T
print("\nTransposed:\n", arr_t)
print("Shape:", arr_t.shape)  # (3, 2)

# Using np.transpose
arr_t2 = np.transpose(arr)
print("\nnp.transpose:", arr_t2.shape)  # (3, 2)

# 3D transpose
arr3d = np.arange(24).reshape(2, 3, 4)
print("\n3D shape:", arr3d.shape)          # (2, 3, 4)
print("3D transposed:", arr3d.T.shape)     # (4, 3, 2)
print("3D transpose:", np.transpose(arr3d, (1, 0, 2)).shape)  # (3, 2, 4)
# Output:
# Original:
#  [[1 2 3]
#   [4 5 6]]
# Shape: (2, 3)
#
# Transposed:
#  [[1 4]
#   [2 5]
#   [3 6]]
# Shape: (3, 2)

# ============================================================
# Example 5: Shape Manipulation Functions
# Various functions to reshape and manipulate array dimensions.
# ============================================================

arr = np.arange(24)

# resize - changes shape, repeats data if needed
resized = np.resize(arr, (4, 6))
print("\nResized (4x6):\n", resized)
print("Shape:", resized.shape)  # (4, 6)

# Expand dimensions
arr_1d = np.array([1, 2, 3])
print("\n1D shape:", arr_1d.shape)  # (3,)

arr_row = np.expand_dims(arr_1d, axis=0)
print("As row:", arr_row.shape)    # (1, 3)

arr_col = np.expand_dims(arr_1d, axis=1)
print("As col:", arr_col.shape)    # (3, 1)

# Squeeze - removes size-1 dimensions
arr_squeeze = np.array([[[1, 2, 3]]])
print("\nBefore squeeze:", arr_squeeze.shape)  # (1, 1, 3)
arr_squeezed = arr_squeeze.squeeze()
print("After squeeze:", arr_squeezed.shape)   # (3,)

# Column stack and row stack
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("\nColumn stack:", np.column_stack((a, b)).shape)  # (3, 2)
print("Row stack:", np.vstack((a, b)).shape)             # (2, 3)
