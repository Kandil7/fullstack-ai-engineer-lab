"""
W3Schools Python Tutorial - 22: Python Range
=============================================
Topics: range() function, start/stop/step, negative step

Run: python 22-range.py
Reference: https://www.w3schools.com/python/python_range.asp
"""

# ============================================================
# The range() Function
# ============================================================
# range() generates a sequence of numbers
# It's commonly used in for loops

# Example 1: Basic range
print("--- Basic Range ---")
for i in range(5):
    print(i, end=" ")
print()

# Output: 0 1 2 3 4

# ============================================================
# range() with start and stop
# ============================================================
# Example 2: Custom start and stop
print("\n--- Range with Start/Stop ---")
for i in range(2, 7):
    print(i, end=" ")
print()

# Output: 2 3 4 5 6

# Example 3: Start at 10, stop at 20
for i in range(10, 21):
    print(i, end=" ")
print()

# Output: 10 11 12 13 14 15 16 17 18 19 20

# ============================================================
# range() with start, stop, and step
# ============================================================
# Example 4: Custom step
print("\n--- Range with Step ---")
for i in range(0, 10, 2):  # Every 2nd number
    print(i, end=" ")
print()

# Output: 0 2 4 6 8

# Example 5: Step of 3
for i in range(0, 20, 3):
    print(i, end=" ")
print()

# Output: 0 3 6 9 12 15 18

# ============================================================
# Negative Step (Counting Backwards)
# ============================================================
# Example 6: Countdown
print("\n--- Countdown ---")
for i in range(10, 0, -1):
    print(i, end=" ")
print()
print("Liftoff!")

# Output:
# 10 9 8 7 6 5 4 3 2 1
# Liftoff!

# Example 7: Negative step with range
for i in range(50, 0, -10):
    print(i, end=" ")
print()

# Output: 50 40 30 20 10

# ============================================================
# Converting range to List
# ============================================================
# Example 8: range() returns a range object, not a list
r = range(5)
print(f"\nType: {type(r)}")
print(f"range(5): {r}")

# Convert to list if needed
numbers = list(range(5))
print(f"list(range(5)): {numbers}")

numbers = list(range(2, 10, 2))
print(f"list(range(2, 10, 2)): {numbers}")

# Output:
# Type: <class 'range'>
# range(5): range(0, 5)
# list(range(5)): [0, 1, 2, 3, 4]
# list(range(2, 10, 2)): [2, 4, 6, 8]

# ============================================================
# Practical Uses of range()
# ============================================================
# Example 9: Common patterns

# Repeat something N times
print("\n--- Repeat 5 times ---")
for _ in range(5):
    print("Hello!")

# Access list by index
print("\n--- Index Access ---")
fruits = ["apple", "banana", "cherry", "date"]
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# Generate numbers for calculation
print("\n--- Sum 1 to 100 ---")
total = sum(range(1, 101))
print(f"Sum of 1-100: {total}")

# Multiplication table
print("\n--- 7x Table ---")
for i in range(1, 11):
    print(f"7 x {i:2d} = {7 * i:2d}")

# ============================================================
# range() Edge Cases
# ============================================================
# Example 10: Empty ranges
print("\n--- Edge Cases ---")
print(f"range(5, 2): {list(range(5, 2))}")    # Empty (start > stop, no negative step)
print(f"range(0): {list(range(0))}")            # Empty
print(f"range(2, 2): {list(range(2, 2))}")      # Empty

# Negative numbers work too
print(f"\nrange(-5, 0): {list(range(-5, 0))}")
print(f"range(-10, 10, 5): {list(range(-10, 10, 5))}")

# Output:
# range(5, 2): []
# range(0): []
# range(2, 2): []

# range(-5, 0): [-5, -4, -3, -2, -1]
# range(-10, 10, 5): [-10, -5, 0, 5]

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. range(stop): 0 to stop-1")
print("2. range(start, stop): start to stop-1")
print("3. range(start, stop, step): custom step size")
print("4. Negative step: counting backwards")
print("5. Returns range object (not list) - convert with list()")
print("6. Commonly used in for loops: for i in range(n)")
