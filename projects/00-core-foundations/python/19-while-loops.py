"""
W3Schools Python Tutorial - 19: Python While Loops
===================================================
Topics: Basic while, while True, break, continue, else

Run: python 19-while-loops.py
Reference: https://www.w3schools.com/python/python_while_loops.asp
"""

# ============================================================
# Basic While Loop
# ============================================================
# Example 1: Simple while loop
print("--- Basic While Loop ---")
i = 1
while i <= 5:
    print(f"i = {i}")
    i += 1

# Output:
# i = 1
# i = 2
# i = 3
# i = 4
# i = 5

# ============================================================
# Example 2: Counting backwards
# ============================================================
print("\n--- Counting Backwards ---")
count = 5
while count > 0:
    print(f"Countdown: {count}")
    count -= 1
print("Liftoff!")

# Output:
# Countdown: 5
# Countdown: 4
# Countdown: 3
# Countdown: 2
# Countdown: 1
# Liftoff!

# ============================================================
# While Loop with Condition
# ============================================================
# Example 3: Sum numbers until limit
print("\n--- Sum Until Limit ---")
total = 0
num = 1

while total + num <= 20:
    total += num
    print(f"Added {num}, total = {total}")
    num += 1

print(f"Final total: {total}")

# Output:
# Added 1, total = 1
# Added 2, total = 3
# Added 3, total = 6
# Added 4, total = 10
# Added 5, total = 15
# Added 6, total = 21 (stops here)
# Final total: 15

# ============================================================
# while True Loop
# ============================================================
# Example 4: Infinite loop with break
print("\n--- While True with Break ---")
import random

attempts = 0
while True:
    attempts += 1
    number = random.randint(1, 10)
    if number == 7:
        print(f"Found 7 after {attempts} attempts!")
        break
    print(f"Attempt {attempts}: got {number}")

# ============================================================
# break Statement
# ============================================================
# Example 5: Break out of loop
print("\n--- Break Statement ---")
i = 1
while i <= 10:
    if i == 6:
        print(f"Breaking at i = {i}")
        break
    print(f"i = {i}")
    i += 1

# Output:
# i = 1
# i = 2
# i = 3
# i = 4
# i = 5
# Breaking at i = 6

# ============================================================
# continue Statement
# ============================================================
# Example 6: Skip current iteration
print("\n--- Continue Statement ---")
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:  # Skip even numbers
        continue
    print(f"Odd: {i}")

# Output:
# Odd: 1
# Odd: 3
# Odd: 5
# Odd: 7
# Odd: 9

# ============================================================
# else Clause
# ============================================================
# Example 7: While-else (else runs when condition is False)
print("\n--- While-Else ---")
i = 1
while i <= 5:
    print(f"i = {i}")
    i += 1
else:
    print("Loop completed normally!")

# Output:
# i = 1
# i = 2
# i = 3
# i = 4
# i = 5
# Loop completed normally!

# Example 8: Else doesn't run when break is used
print("\n--- Else with Break ---")
i = 1
while i <= 10:
    if i == 6:
        break
    print(f"i = {i}")
    i += 1
else:
    print("This won't print because of break!")

# Output:
# i = 1
# i = 2
# i = 3
# i = 4
# i = 5

# ============================================================
# Practical Examples
# ============================================================
# Example 9: User input simulation (no actual input needed)
print("\n--- Password Validation ---")
correct_password = "secret"
guesses = ["wrong", "wrong", "secret", "wrong"]
guess_index = 0
max_attempts = 3

while guess_index < max_attempts:
    if guess_index < len(guesses):
        guess = guesses[guess_index]
    else:
        guess = "timeout"
    
    if guess == correct_password:
        print(f"Access granted after {guess_index + 1} attempts!")
        break
    
    remaining = max_attempts - guess_index - 1
    if remaining > 0:
        print(f"Wrong password. {remaining} attempts remaining.")
    guess_index += 1
else:
    print("Account locked after too many failed attempts!")

# Output:
# Wrong password. 2 attempts remaining.
# Wrong password. 1 attempts remaining.
# Access granted after 3 attempts!

# Example 10: Simple number guessing game
print("\n--- Number Guessing Game ---")
target = 42
guesses = [20, 50, 35, 45, 42]  # Pre-defined guesses
guess_index = 0

while guess_index < len(guesses):
    guess = guesses[guess_index]
    guess_index += 1
    
    if guess < target:
        print(f"  Guess {guess}: Too low!")
    elif guess > target:
        print(f"  Guess {guess}: Too high!")
    else:
        print(f"  Guess {guess}: Correct! Found in {guess_index} tries!")
        break

# Output:
#   Guess 20: Too low!
#   Guess 50: Too high!
#   Guess 35: Too low!
#   Guess 45: Too high!
#   Guess 42: Correct! Found in 5 tries!

# Example 11: Multiplication table
print("\n--- Multiplication Table (1-5) ---")
i = 1
while i <= 5:
    j = 1
    while j <= 5:
        product = i * j
        print(f"{product:4d}", end="")
        j += 1
    print()  # New line after each row
    i += 1

# Output:
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. while condition: loop while condition is True")
print("2. while True: infinite loop (use break to exit)")
print("3. break: exit the loop immediately")
print("4. continue: skip to the next iteration")
print("5. else: runs when loop condition becomes False")
print("6. Always ensure the loop condition eventually becomes False!")
