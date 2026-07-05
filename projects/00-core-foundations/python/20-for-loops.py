"""
W3Schools Python Tutorial - 20: Python For Loops
=================================================
Topics: range, lists, strings, break, continue, else, nested

Run: python 20-for-loops.py
Reference: https://www.w3schools.com/python/python_for_loops.asp
"""

# ============================================================
# For Loop with range()
# ============================================================
# Example 1: Basic for loop with range
print("--- For Loop with range() ---")
for i in range(5):
    print(f"i = {i}")

# Output:
# i = 0
# i = 1
# i = 2
# i = 3
# i = 4

# ============================================================
# For Loop with List
# ============================================================
# Example 2: Looping through a list
print("\n--- For Loop with List ---")
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")

# Output:
# I like apple
# I like banana
# I like cherry

# ============================================================
# For Loop with String
# ============================================================
# Example 3: Looping through a string
print("\n--- For Loop with String ---")
for letter in "Python":
    print(letter, end=" ")
print()

# Output: P y t h o n

# ============================================================
# break Statement
# ============================================================
# Example 4: Break out of loop
print("\n--- Break Statement ---")
for i in range(10):
    if i == 5:
        print(f"\nBreaking at {i}!")
        break
    print(i, end=" ")
print()

# Output: 0 1 2 3 4
# Breaking at 5!

# ============================================================
# continue Statement
# ============================================================
# Example 5: Skip current iteration
print("\n--- Continue Statement ---")
for i in range(10):
    if i % 2 == 0:  # Skip even numbers
        continue
    print(i, end=" ")
print()

# Output: 1 3 5 7 9

# ============================================================
# else Clause
# ============================================================
# Example 6: For-else (else runs when loop completes normally)
print("\n--- For-Else ---")
for i in range(5):
    print(i, end=" ")
else:
    print("\nLoop completed!")

# Output:
# 0 1 2 3 4
# Loop completed!

# Example 7: Else doesn't run with break
print("\n--- For-Else with Break ---")
for i in range(10):
    if i == 5:
        break
    print(i, end=" ")
else:
    print("This won't print!")

# Output: 0 1 2 3 4

# ============================================================
# Nested Loops
# ============================================================
# Example 8: Inner loop runs completely for each outer iteration
print("\n--- Nested Loops ---")
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()  # New line

# Output:
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# (2,0) (2,1) (2,2)

# ============================================================
# Looping with enumerate()
# ============================================================
# Example 9: Get index and value
print("\n--- Enumerate ---")
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Output:
# 0: apple
# 1: banana
# 2: cherry

# With custom start
print("\nWith start=1:")
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")

# Output:
# 1: apple
# 2: banana
# 3: cherry

# ============================================================
# Looping with zip()
# ============================================================
# Example 10: Loop through multiple lists
print("\n--- Zip ---")
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["New York", "London", "Paris"]

for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}, {city}")

# Output:
# Alice, 25, New York
# Bob, 30, London
# Charlie, 35, Paris

# ============================================================
# Loop Techniques
# ============================================================
# Example 11: Useful loop patterns
print("\n--- Loop Techniques ---")

# reversed()
print("Reversed range:")
for i in reversed(range(5)):
    print(i, end=" ")
print()

# sorted()
print("Sorted fruits:")
for fruit in sorted(["cherry", "apple", "banana"]):
    print(fruit, end=" ")
print()

# Loop with step
print("Step 2:")
for i in range(0, 10, 2):
    print(i, end=" ")
print()

# Negative step (countdown)
print("Countdown:")
for i in range(5, 0, -1):
    print(i, end=" ")
print()

# ============================================================
# Practical Examples
# ============================================================
# Example 12: FizzBuzz
print("\n--- FizzBuzz ---")
for i in range(1, 21):
    if i % 15 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")
print()

# Output: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz

# Example 13: Matrix multiplication
print("\n--- Matrix Multiplication ---")
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
result = [[0, 0], [0, 0]]

for i in range(2):
    for j in range(2):
        for k in range(2):
            result[i][j] += A[i][k] * B[k][j]

print("Result:")
for row in result:
    print(row)

# Output:
# [19, 22]
# [43, 50]

# Example 14: Flatten nested list
print("\n--- Flatten Nested List ---")
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = []
for sublist in nested:
    for item in sublist:
        flat.append(item)
print(f"Flattened: {flat}")

# Output: Flattened: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. for item in iterable: loop through each item")
print("2. range(n): generates numbers 0 to n-1")
print("3. range(start, stop, step): customizable range")
print("4. break: exit loop; continue: skip iteration")
print("5. else: runs when loop completes (not with break)")
print("6. enumerate(): get index and value")
print("7. zip(): loop through multiple iterables")
print("8. Nested loops: inner loop runs fully per outer iteration")
