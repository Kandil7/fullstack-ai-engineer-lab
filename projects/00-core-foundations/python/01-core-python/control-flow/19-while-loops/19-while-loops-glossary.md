# Python While Loops — Glossary 19

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| While Loop | Repeats while condition is True | `while x > 0:` |
| Condition | Expression evaluated each iteration | `while count < 10:` |
| Break | Exits the loop immediately | `break` |
| Continue | Skips to next iteration | `continue` |
| Else | Runs when loop completes normally | `while...else:` |
| Infinite Loop | Loop that never terminates | `while True:` |
| Counter | Variable tracking iterations | `i = 0; while i < n:` |
| Sentinel | Value that signals loop termination | `while input() != "quit":` |
| Nested While | While loop inside another while | `while...while...` |
| Loop Variable | Variable modified in the loop | `count += 1` |
| Off-By-One | Common boundary error | `i <= n` vs `i < n` |
| Guard Clause | Early exit condition in loop | `if not valid: continue` |
| Iteration | Single execution of loop body | — |
| Body | Indented block executed each iteration | — |
| Termination | Loop ending condition | — |
| Timeout | Maximum execution time safety | — |
| Loop-and-a-Half | while True with break in middle | — |
| Mid-Loop Break | break inside conditional in loop | — |
| Accumulator | Variable that accumulates results | `total += x` |
| Tracer | Debug print inside loop | — |

---

## Definitions

### Accumulator
**Definition**: A variable that collects or sums values during loop execution. Initialized before the loop and updated each iteration.

**Example**:
```python
total = 0
i = 1
while i <= 100:
    total += i
    i += 1
print(f"Sum: {total}")  # Sum: 5050
```

**Related**: loop variable, aggregation, running total

---

### Body
**Definition**: The indented block of code that executes each time the while loop runs. Contains the statements to be repeated.

**Example**:
```python
# This is the body:
while x > 0:
    print(x)    # body line 1
    x -= 1      # body line 2
    x *= 2      # body line 3
```

**Related**: indentation, loop, block

---

### Break
**Definition**: A statement that immediately exits the innermost loop. Any remaining code in the loop body is skipped, and the while-else else clause is NOT executed.

**Example**:
```python
while True:
    number = int(input("Enter a positive number: "))
    if number < 0:
        print("Negative! Exiting...")
        break
    print(f"You entered: {number}")
```

**Related**: `continue`, loop exit, `else` clause

---

### Condition
**Definition**: An expression evaluated at the start of each loop iteration. If `True`, the loop body executes. If `False`, the loop ends.

**Example**:
```python
# Condition: x > 0
x = 5
while x > 0:
    print(x)
    x -= 1
```

**Related**: boolean, expression, truthiness, termination

---

### Continue
**Definition**: A statement that skips the remaining code in the current iteration and jumps back to evaluate the loop condition again.

**Example**:
```python
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
# Output: 1, 3, 5, 7, 9
```

**Related**: `break`, skip iteration, loop control

---

### Counter
**Definition**: A variable that tracks how many times the loop has executed. Typically incremented each iteration.

**Example**:
```python
count = 0
while count < 5:
    print(f"Iteration {count + 1}")
    count += 1
```

**Related**: loop variable, iteration, increment

---

### Else
**Definition**: An optional clause on a while loop that executes only if the loop completes normally (condition becomes `False`) without hitting a `break`.

**Example**:
```python
# Without break — else runs
i = 1
while i <= 5:
    print(i)
    i += 1
else:
    print("Loop completed!")  # Printed

# With break — else skipped
i = 1
while i <= 5:
    if i == 3:
        break
    i += 1
else:
    print("Loop completed!")  # NOT printed
```

**Related**: `break`, normal completion, loop control

---

### Guard Clause
**Definition**: An early `continue` or `break` that handles edge cases before the main logic, reducing nesting.

**Example**:
```python
i = 0
while i < len(data):
    # Guard clause
    if data[i] is None:
        i += 1
        continue
    
    # Main logic (less nested)
    process(data[i])
    i += 1
```

**Related**: early continue, flattening, readability

---

### Infinite Loop
**Definition**: A while loop whose condition never becomes `False`, causing it to run forever. Sometimes intentional (with `break`), sometimes a bug.

**Example**:
```python
# Intentional infinite loop
while True:
    user_input = input("Enter command: ")
    if user_input == "quit":
        break

# Unintentional (bug!)
# x = 1
# while x > 0:
#     x += 1  # x grows forever, never < 0
```

**Related**: `while True`, `break`, termination

---

### Iteration
**Definition**: A single execution of the loop body. Each time the condition is checked and found `True`, one iteration occurs.

**Example**:
```python
# 3 iterations
x = 3
while x > 0:
    print(x)  # Iteration body
    x -= 1
# Iteration 1: prints 3
# Iteration 2: prints 2
# Iteration 3: prints 1
```

**Related**: loop, body, repetition

---

### Loop-and-a-Half
**Definition**: A pattern using `while True` with `break` in the middle. Avoids duplicating the condition check and is useful for input loops.

**Example**:
```python
# Loop-and-a-half pattern
while True:
    data = input("Enter data (or 'quit'): ")
    if data == "quit":
        break
    process(data)
```

**Related**: `while True`, `break`, input validation

---

### Loop Variable
**Definition**: A variable that controls the loop's execution, typically modified each iteration to eventually make the condition `False`.

**Example**:
```python
i = 0           # initialized
while i < 10:   # checked
    print(i)
    i += 1      # modified
```

**Related**: counter, condition, increment

---

### Nested While
**Definition**: A while loop placed inside another while loop. Each inner loop runs to completion for each iteration of the outer loop.

**Example**:
```python
i = 1
while i <= 3:
    j = 1
    while j <= 3:
        print(f"({i}, {j})", end=" ")
        j += 1
    print()
    i += 1
# (1, 1) (1, 2) (1, 3)
# (2, 1) (2, 2) (2, 3)
# (3, 1) (3, 2) (3, 3)
```

**Related**: loops, 2D iteration, matrix traversal

---

### Off-By-One
**Definition**: A common boundary error where the loop runs one too many or one too few times. Caused by incorrect use of `<` vs `<=`.

**Example**:
```python
# Runs 5 times (0,1,2,3,4) — off by one if you want 1-5
i = 0
while i < 5:
    print(i)
    i += 1

# Runs 5 times (1,2,3,4,5) — correct for 1-5
i = 1
while i <= 5:
    print(i)
    i += 1
```

**Related**: boundary, `<` vs `<=`, indexing

---

### Sentinel
**Definition**: A special value that signals the end of input or loop termination. The loop continues until the sentinel value is encountered.

**Example**:
```python
# Sentinel value: -1
total = 0
while True:
    number = float(input("Enter number (-1 to quit): "))
    if number == -1:
        break
    total += number
print(f"Total: {total}")
```

**Related**: sentinel value, loop termination, input

---

### Termination
**Definition**: The event of a loop ending. Occurs when the condition becomes `False` or `break` is executed.

**Example**:
```python
# Termination by condition
x = 5
while x > 0:
    x -= 1
# Terminated when x == 0

# Termination by break
while True:
    if condition:
        break  # Terminated by break
```

**Related**: condition, `break`, infinite loop

---

### Timeout
**Definition**: A safety mechanism that forces a loop to terminate after a maximum execution time, preventing infinite loops in production code.

**Example**:
```python
import time

start = time.time()
timeout = 5  # seconds

while True:
    if time.time() - start > timeout:
        print("Timeout!")
        break
    # Do work...
```

**Related**: infinite loop, safety, production code

---

### Tracer
**Definition**: A debugging technique where you print variables inside a loop to understand its behavior and identify issues.

**Example**:
```python
x = 10
while x > 0:
    print(f"DEBUG: x = {x}")  # Tracer
    x -= 2
# Use this to see: 10, 8, 6, 4, 2, 0
```

**Related**: debugging, print, debugging technique

---

## Code Examples

### Example 1: Reverse a Number
```python
def reverse_number(n):
    reversed_num = 0
    while n > 0:
        digit = n % 10
        reversed_num = reversed_num * 10 + digit
        n //= 10
    return reversed_num

print(reverse_number(12345))  # 54321
```

### Example 2: Greatest Common Divisor
```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print(gcd(48, 18))  # 6
```

### Example 3: Power Calculation
```python
def power(base, exponent):
    result = 1
    while exponent > 0:
        result *= base
        exponent -= 1
    return result

print(power(2, 10))  # 1024
```

---

## Related Concepts

- **For Loops**: When iteration count is known
- **Recursion**: Alternative to loops using function calls
- **Generators**: Lazy iteration with `yield`
- **Iterator Protocol**: `__iter__` and `__next__` methods
- **Loop Optimization**: Reducing iterations, early termination
