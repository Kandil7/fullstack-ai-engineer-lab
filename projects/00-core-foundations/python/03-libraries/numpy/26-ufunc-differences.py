"""
Ufunc Differences
W3Schools: https://www.w3schools.com/python/numpy_ufunc_differences.asp

Difference operations on arrays (discrete calculus).
"""

import numpy as np

# ============================================================
# Example 1: Basic Difference
# diff() calculates n[i+1] - n[i].
# ============================================================

arr = np.array([10, 15, 25, 40, 60])

# First order difference
print("Original:", arr)
print("diff():", np.diff(arr))  # [ 5 10 15 20]
# Output:
# Original: [10 15 25 40 60]
# diff(): [ 5 10 15 20]

# Second order difference (diff of diff)
print("diff(2):", np.diff(arr, n=2))  # [5 5 5]

# Verify: second diff is constant for quadratic sequence
arr2 = np.array([1, 4, 9, 16, 25])  # n^2
print("\nn^2 sequence:", arr2)
print("First diff:", np.diff(arr2))    # [3 5 7 9]
print("Second diff:", np.diff(arr2, n=2))  # [2 2 2]
# Output:
# diff(2): [5 5 5]

# ============================================================
# Example 2: Differences Along Axis
# Calculate differences in 2D arrays.
# ============================================================

arr2d = np.array([[1, 2, 3, 4],
                   [5, 7, 9, 11],
                   [10, 14, 18, 22]])

print("\n2D Array:\n", arr2d)

# Diff along rows (axis=1)
print("\nDiff axis=1 (columns):\n", np.diff(arr2d, axis=1))
# [[1 1 1]
#  [2 2 2]
#  [4 4 4]]

# Diff along columns (axis=0)
print("\nDiff axis=0 (rows):\n", np.diff(arr2d, axis=0))
# [[4 5 6 7]
#  [5 7 9 11]]

# Second order diff
print("\nSecond diff axis=1:\n", np.diff(arr2d, n=2, axis=1))
# [[0 0]
#  [0 0]
#  [0 0]]
# Output:
# Diff axis=1 (columns):
#  [[1 1 1]
#   [2 2 2]
#   [4 4 4]]

# ============================================================
# Example 3: Differences with Prepend/Append
# Control start and end values.
# ============================================================

arr = np.array([10, 20, 35, 55, 80])

# Basic diff
print("\nOriginal:", arr)
print("diff():", np.diff(arr))  # [10 15 20 25]

# Prepend a value to diff
diff_with_start = np.diff(arr, prepend=0)
print("diff(prepend=0):", diff_with_start)  # [10 10 15 20 25]

# Append a value
diff_with_end = np.diff(arr, append=100)
print("diff(append=100):", diff_with_end)  # [10 15 20 25 20]

# Both prepend and append
diff_both = np.diff(arr, prepend=0, append=100)
print("diff(prepend=0, append=100):", diff_both)

# Practical: reconstruct array from diff
original = np.array([10, 20, 35, 55, 80])
diffs = np.diff(original)
reconstructed = np.concatenate([[original[0]], np.cumsum(diffs)])
print("\nOriginal:", original)
print("Diff:", diffs)
print("Reconstructed:", reconstructed)
print("Match:", np.array_equal(original, reconstructed))
# Output:
# Original: [10 20 35 55 80]
# diff(): [10 15 20 25]
# diff(prepend=0): [10 10 15 20 25]

# ============================================================
# Example 4: Practical Applications
# Use cases for diff().
# ============================================================

# Velocity from position
time = np.array([0, 1, 2, 3, 4, 5])  # seconds
position = np.array([0, 5, 20, 45, 80, 125])  # meters

velocity = np.diff(position) / np.diff(time)
print("\nPosition:", position)
print("Velocity (m/s):", velocity)  # [5 15 25 35 45]

# Acceleration from velocity
acceleration = np.diff(velocity) / np.diff(time[:-1])
print("Acceleration (m/s^2):", acceleration)  # [10 10 10 10]

# Daily price changes
prices = np.array([100, 102, 101, 105, 103, 108])
changes = np.diff(prices)
percent_changes = np.diff(prices) / prices[:-1] * 100
print("\nPrices:", prices)
print("Changes:", changes)
print("Percent changes:", percent_changes.round(2))
# Output:
# Position: [  0   5  20  45  80 125]
# Velocity (m/s): [ 5 15 25 35 45]

# ============================================================
# Example 5: Edge Detection with diff
# Detecting changes in data.
# ============================================================

# Step function
signal = np.array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0])
print("\nSignal:", signal)
print("diff:", np.diff(signal))
# [0 0 1 0 0 0 -1 0 0 1 0 -1 0]

# Find transitions
diff_signal = np.diff(signal)
rise_edges = np.where(diff_signal == 1)[0] + 1
fall_edges = np.where(diff_signal == -1)[0] + 1
print("Rise edges at:", rise_edges)  # [3 10]
print("Fall edges at:", fall_edges)  # [7 12]

# Cumulative sum to reconstruct
print("\nCumulative sum:", np.concatenate([[0], np.cumsum(diff_signal)]))
# [0 0 0 1 1 1 1 0 0 0 1 1 0 0]

# Detect monotonic increase
data = np.array([1, 2, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6])
diffs = np.diff(data)
is_increasing = np.all(diffs > 0)
print(f"\nData: {data}")
print(f"Is monotonically increasing: {is_increasing}")
# Output:
# Signal: [0 0 0 1 1 1 1 0 0 0 1 1 0 0]
# Rise edges at: [ 3 10]
# Fall edges at: [ 7 12]
