# Python While Loops — Lecture 19

## Topic Overview

A **while loop** repeatedly executes a block of code as long as a condition remains `True`. It's ideal when you don't know in advance how many iterations you need — for example, waiting for user input, processing data until a condition is met, or implementing game loops.

While loops can run indefinitely if the condition never becomes `False`, so careful control of the loop variable is essential.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Write while loops with proper termination conditions
- Use break, continue, and else clauses with while loops
- Implement counter-controlled and sentinel-controlled loops
- Avoid infinite loops
- Use while loops for input validation
- Understand when to use while vs. for loops
- Apply while loops to real-world scenarios

---

## Key Concepts

### 1. Basic While Loop

```python
# Simple while loop
count = 1
while count <= 5:
    print(f"Count: {count}")
    count += 1  # CRITICAL: must update the condition variable!

# Output:
# Count: 1
# Count: 2
# Count: 3
# Count: 4
# Count: 5
```

### 2. While Loop with Condition

```python
# Loop until a condition is met
password = ""
while password != "secret":
    password = input("Enter password: ")
print("Access granted!")
```

### 3. Counter-Controlled Loop

```python
# Use a counter to control iterations
i = 0
total = 0
while i < 10:
    total += i
    i += 1
print(f"Sum: {total}")  # Sum: 45
```

### 4. Sentinel-Controlled Loop

```python
# Loop until a sentinel value is entered
total = 0
while True:
    number = float(input("Enter a number (negative to quit): "))
    if number < 0:
        break
    total += number
print(f"Total: {total}")
```

### 5. Break Statement

```python
# Exit the loop immediately
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        print("Goodbye!")
        break
    print(f"You entered: {user_input}")
```

### 6. Continue Statement

```python
# Skip the rest of the current iteration
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
i = 0
while i < len(numbers):
    if numbers[i] % 2 == 0:
        i += 1
        continue  # Skip even numbers
    print(numbers[i])
    i += 1
# Output: 1, 3, 5, 7, 9
```

### 7. While-Else

```python
# else clause runs when loop condition becomes False (no break)
i = 1
while i <= 5:
    if i == 3:
        break
    print(i)
    i += 1
else:
    print("Loop completed normally!")  # NOT printed because of break

# Without break
i = 1
while i <= 5:
    print(i)
    i += 1
else:
    print("Loop completed normally!")  # Printed!
```

### 8. Infinite Loop with Exit

```python
# Common pattern: infinite loop with break
while True:
    print("Menu:")
    print("1. Play")
    print("2. Settings")
    print("3. Quit")
    choice = input("Select: ")
    
    if choice == "1":
        print("Starting game...")
    elif choice == "2":
        print("Opening settings...")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")
```

### 9. Nested While Loops

```python
# Multiplication table
i = 1
while i <= 5:
    j = 1
    while j <= 5:
        print(f"{i*j:4d}", end="")
        j += 1
    print()  # New line
    i += 1

# Output:
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25
```

---

## Code Examples

### Example 1: Number Guessing Game

```python
import random

def guessing_game():
    target = random.randint(1, 100)
    attempts = 0
    
    while True:
        guess = int(input("Guess a number (1-100): "))
        attempts += 1
        
        if guess < target:
            print("Too low!")
        elif guess > target:
            print("Too high!")
        else:
            print(f"Correct! You got it in {attempts} attempts!")
            break

guessing_game()
```

### Example 2: Input Validation

```python
def get_valid_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if 0 <= age <= 150:
                return age
            print("Age must be between 0 and 150!")
        except ValueError:
            print("Please enter a valid number!")

age = get_valid_age()
print(f"Your age: {age}")
```

### Example 3: FizzBuzz with While

```python
def fizzbuzz_while(n):
    i = 1
    while i <= n:
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
        i += 1

fizzbuzz_while(15)
```

### Example 4: Collatz Conjecture

```python
def collatz(n):
    """Generate Collatz sequence until reaching 1."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

print(collatz(6))  # [6, 3, 10, 5, 16, 8, 4, 2, 1]
```

### Example 5: Prime Checker

```python
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:  # Only check up to sqrt(n)
        if n % i == 0:
            return False
        i += 1
    return True

primes = []
n = 2
while len(primes) < 20:  # Find first 20 primes
    if is_prime(n):
        primes.append(n)
    n += 1
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
```

---

## Common Mistakes to Avoid

### Mistake 1: Infinite Loop
```python
# WRONG — no way to exit!
# while True:
#     print("Running forever...")

# WRONG — condition never changes
# x = 1
# while x > 0:
#     print(x)
#     x += 1  # x keeps growing, never < 0

# CORRECT — ensure condition eventually becomes False
x = 5
while x > 0:
    print(x)
    x -= 1
```

### Mistake 2: Off-By-One Error
```python
# WRONG — misses last value
i = 0
while i < 5:
    print(i)
    i += 1
# Prints 0, 1, 2, 3, 4 (misses 5)

# CORRECT — include the boundary
i = 1
while i <= 5:
    print(i)
    i += 1
# Prints 1, 2, 3, 4, 5
```

### Mistake 3: Forgetting to Update Counter
```python
# WRONG — infinite loop!
count = 1
while count <= 5:
    print(count)
    # count += 1  # FORGOT THIS!

# CORRECT
count = 1
while count <= 5:
    print(count)
    count += 1
```

### Mistake 4: Modifying Collection While Iterating
```python
# WRONG
items = [1, 2, 3, 4, 5]
i = 0
while i < len(items):
    if items[i] % 2 == 0:
        items.pop(i)  # Skips elements after removal!
    i += 1

# CORRECT — iterate over a copy
items = [1, 2, 3, 4, 5]
i = 0
while i < len(items):
    if items[i] % 2 == 0:
        items.pop(i)
    else:
        i += 1  # Only increment if not removing
```

---

## Best Practices

1. **Always ensure the loop can terminate** — update the condition variable
2. **Use `while True` with `break`** for input loops and menus
3. **Prefer `for` loops** when you know the number of iterations
4. **Use `else` clause** to detect normal completion vs. break
5. **Add timeout/safety** for potentially infinite loops
6. **Use meaningful variable names** for loop counters
7. **Consider `for` loop with `range()`** instead of while for counting

---

## Practice Exercises

### Exercise 1: Digit Sum
Write a function that sums the digits of a number using a while loop.

```python
def digit_sum(n):
    # Your code here
    pass

# Expected: 15 (1 + 2 + 3 + 4 + 5)
print(digit_sum(12345))
```

### Exercise 2: Fibonacci Generator
Write a function that generates Fibonacci numbers up to n.

```python
def fibonacci(n):
    # Your code here — use while loop
    pass

# Expected: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print(fibonacci(40))
```

### Exercise 3: Binary Search
Implement binary search using a while loop.

```python
def binary_search(sorted_list, target):
    # Your code here
    pass

# Expected: 3
print(binary_search([1, 2, 3, 4, 5, 6, 7], 4))
```

### Exercise 4: ATM Simulator
Write an ATM simulator that keeps asking for commands until user types "exit".

```python
def atm_simulator():
    balance = 1000
    # Your code here — while loop with menu
    pass
```

---

## Summary

- **While loops** repeat as long as condition is `True`
- **Always update** the loop variable to avoid infinite loops
- **`break`** exits the loop immediately
- **`continue`** skips to the next iteration
- **`else`** runs when loop completes without `break`
- Use `while True` with `break` for input validation loops
- Use **for loops** when you know the iteration count
- **Nested while loops** for 2D iteration patterns
