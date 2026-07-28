# Python If/Else Statements — Lecture 17

## Topic Overview

Conditional statements allow your program to make decisions and execute different code paths based on whether conditions evaluate to `True` or `False`. Python uses `if`, `elif` (else if), and `else` keywords to implement branching logic. Unlike many other languages, Python uses **indentation** rather than braces to define code blocks.

Understanding conditionals is fundamental to programming — they're used in virtually every program to control flow, validate input, handle errors, and implement business logic.

---

## Learning Objectives

By the end of this lecture, you will be able:

- Write `if`, `elif`, and `else` statements
- Use comparison and logical operators in conditions
- Implement nested conditionals
- Use ternary expressions for concise conditionals
- Understand truthiness and falsy values in Python
- Apply conditionals to real-world scenarios
- Write clean, readable conditional logic

---

## Key Concepts

### 1. Basic If Statement

```python
# Simple if statement
temperature = 75

if temperature > 70:
    print("It's warm outside!")
    print("Wear sunscreen!")

# Code outside the if block runs regardless
print("Have a nice day!")
```

### 2. If-Else Statement

```python
temperature = 60

if temperature > 70:
    print("It's warm!")
else:
    print("It's cool outside!")

# Only one branch executes — never both
```

### 3. If-Elif-Else Chain

```python
temperature = 75

if temperature >= 90:
    print("It's hot!")
elif temperature >= 70:
    print("It's warm!")       # This executes
elif temperature >= 50:
    print("It's cool!")
elif temperature >= 32:
    print("It's cold!")
else:
    print("It's freezing!")

# Conditions are checked top-to-bottom
# First True condition wins; rest are skipped
```

### 4. Comparison Operators

```python
x = 10
y = 20

# Equal to
print(x == y)    # False

# Not equal to
print(x != y)    # True

# Greater than / Less than
print(x > y)     # False
print(x < y)     # True

# Greater/Less than or equal to
print(x >= 10)   # True
print(x <= 5)    # False

# Chained comparisons (Pythonic!)
print(5 < x < 15)  # True — equivalent to 5 < x and x < 15
print(1 < 2 < 3 < 4)  # True
```

### 5. Logical Operators

```python
age = 25
income = 50000

# and — both conditions must be True
if age >= 18 and income >= 30000:
    print("Loan approved!")

# or — at least one condition must be True
if age < 13 or age > 65:
    print("Discount applies!")

# not — reverses the boolean value
is_student = False
if not is_student:
    print("Full price")

# Combining logical operators
if (age >= 18 and income >= 30000) or not is_student:
    print("Eligible!")
```

### 6. Truthiness and Falsy Values

```python
# Everything in Python has a boolean value

# FALSY values (evaluate to False in conditions)
bool(0)         # False
bool(0.0)       # False
bool("")        # False
bool([])        # False
bool({})        # False
bool(set())     # False
bool(None)      # False
bool(False)     # False

# TRUTHY values (evaluate to True)
bool(1)         # True
bool(-1)        # True
bool("hello")   # True
bool([1, 2])    # True
bool({"a": 1})  # True
bool(object())  # True

# Practical usage
name = ""
if name:          # Empty string is falsy
    print("Hello, " + name)
else:
    print("Name is empty!")

items = []
if not items:     # Empty list is falsy
    print("No items in cart")
```

### 7. Ternary Expression (Conditional Expression)

```python
age = 20

# Traditional way
if age >= 18:
    status = "adult"
else:
    status = "minor"

# Ternary expression (one-liner)
status = "adult" if age >= 18 else "minor"
print(status)  # adult

# Nested ternary (use sparingly)
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(grade)  # B

# Ternary in print statements
print("Even" if 4 % 2 == 0 else "Odd")  # Even
```

### 8. Nested Conditionals

```python
has_ticket = True
is_vip = False
age = 25

if has_ticket:
    if is_vip:
        print("Welcome to VIP lounge!")
    elif age >= 21:
        print("Welcome! You can access the bar.")
    else:
        print("Welcome! Enjoy the show.")
else:
    print("Please purchase a ticket.")

# Flattening with logical operators (often cleaner)
if has_ticket and is_vip:
    print("VIP lounge!")
elif has_ticket and age >= 21:
    print("Show + bar")
elif has_ticket:
    print("Show only")
else:
    print("Buy ticket")
```

### 9. Membership and Identity Tests

```python
# Membership: in / not in
fruits = ["apple", "banana", "cherry"]
if "apple" in fruits:
    print("We have apples!")

if "mango" not in fruits:
    print("No mangoes!")

# Identity: is / is not
value = None
if value is None:
    print("Value is None!")

if value is not None:
    print("Value exists!")

# ALWAYS use 'is' for None checks, not ==
# if value == None:  # Works but not Pythonic
# if value is None:  # Correct and Pythonic
```

### 10. Match Statement (Python 3.10+)

```python
# Structural pattern matching (brief overview — covered in detail in Lecture 18)
command = "quit"

match command:
    case "quit":
        print("Exiting...")
    case "help":
        print("Showing help...")
    case _:
        print(f"Unknown command: {command}")
```

---

## Code Examples

### Example 1: Age Group Classifier

```python
def classify_age(age):
    if age < 0:
        return "Invalid age"
    elif age < 13:
        return "Child"
    elif age < 18:
        return "Teenager"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"

# Test cases
print(classify_age(-5))   # Invalid age
print(classify_age(10))   # Child
print(classify_age(16))   # Teenager
print(classify_age(30))   # Adult
print(classify_age(70))   # Senior
```

### Example 2: FizzBuzz

```python
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz(15)
```

### Example 3: Login Validator

```python
def validate_login(username, password):
    if not username:
        return "Username is required"
    if len(username) < 3:
        return "Username must be at least 3 characters"
    if not password:
        return "Password is required"
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase letter"
    if not any(c.isdigit() for c in password):
        return "Password must contain a digit"
    return "Valid!"

print(validate_login("ab", "short"))       # Username must be at least 3 characters
print(validate_login("alice", "password")) # Password must contain a digit
print(validate_login("alice", "Pass1234")) # Valid!
```

### Example 4: Discount Calculator

```python
def calculate_discount(total, is_member, day_of_week):
    discount = 0
    
    # Base discount for members
    if is_member:
        discount += 0.10  # 10% member discount
    
    # Day-specific discounts
    if day_of_week == "Tuesday":
        discount += 0.05  # 5% Tuesday special
    elif day_of_week == "Wednesday":
        discount += 0.15  # 15% Wednesday deal
    
    # High-value purchase bonus
    if total >= 100:
        discount += 0.05  # 5% big spender
    
    # Cap discount at 30%
    discount = min(discount, 0.30)
    
    final = total * (1 - discount)
    return final, discount

final_price, applied_discount = calculate_discount(150, True, "Wednesday")
print(f"Original: $150, Discount: {applied_discount*100}%, Final: ${final_price:.2f}")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using `=` Instead of `==`
```python
# WRONG — assignment, not comparison
if x = 5:    # SyntaxError!

# CORRECT
if x == 5:
    print("x is 5")
```

### Mistake 2: Mutable Default in Conditions
```python
# WRONG — truthiness checks on objects
class Empty:
    def __bool__(self):
        return False

# Pythonic — explicit checks
if len(my_list) > 0:    # or simply: if my_list:
    process(my_list)
```

### Mistake 3: Deeply Nested Ifs
```python
# WRONG — deeply nested
if condition1:
    if condition2:
        if condition3:
            do_something()

# BETTER — flatten with early returns or combined conditions
if not condition1:
    return
if not condition2:
    return
if not condition3:
    return
do_something()
```

### Mistake 4: Chained Comparisons Misuse
```python
# This works in Python:
if 1 < x < 10:  # Pythonic!
    print("x is between 1 and 10")

# In many other languages, this doesn't work as expected
# Python chains: (1 < x) and (x < 10)
```

### Mistake 5: Comparing with `True`/`False`
```python
# WRONG — verbose and unpythonic
if is_valid == True:
    process()

if is_valid == False:
    reject()

# CORRECT — Pythonic
if is_valid:
    process()

if not is_valid:
    reject()
```

---

## Best Practices

1. **Use early returns** to flatten nested conditionals
2. **Chain comparisons** `1 < x < 10` instead of `x > 1 and x < 10`
3. **Use `is` for None checks**, not `==`
4. **Keep conditions simple** — extract complex conditions into well-named variables
5. **Use truthiness** — `if my_list:` instead of `if len(my_list) > 0:`
6. **Avoid comparing booleans** with `==` — use `if is_valid:` not `if is_valid == True:`
7. **Use ternary expressions** for simple assignments, not complex logic
8. **Match statement** for complex pattern matching (Python 3.10+)
9. **Docstrings** to explain WHY, not WHAT the condition checks

---

## Practice Exercises

### Exercise 1: Grade Calculator
Write a function that takes a numeric score (0-100) and returns the letter grade (A, B, C, D, F) with + or - modifiers.

```python
def get_grade(score):
    # Your code here
    pass

# Expected: "A-", "B+", etc.
print(get_grade(92))   # A-
print(get_grade(85))   # B+
print(get_grade(73))   # C
```

### Exercise 2: BMI Calculator
Write a function that calculates BMI and returns a category: "Underweight", "Normal weight", "Overweight", "Obese".

```python
def bmi_category(weight_kg, height_m):
    # Your code here
    pass

# Expected: "Normal weight"
print(bmi_category(70, 1.75))
```

### Exercise 3: Leap Year Checker
Write a function that determines if a year is a leap year.

```python
def is_leap_year(year):
    # Your code here
    pass

# Expected: True
print(is_leap_year(2024))
print(is_leap_year(1900))  # False
print(is_leap_year(2000))  # True
```

### Exercise 4: Traffic Light
Write a function that takes a traffic light color and returns the action ("Stop", "Slow down", "Go").

```python
def traffic_action(color):
    # Your code here
    pass

# Expected: "Stop"
print(traffic_action("red"))
print(traffic_action("yellow"))
print(traffic_action("green"))
```

---

## Summary

- **`if`** executes code when condition is True
- **`elif`** adds alternative conditions (checked top-to-bottom)
- **`else`** catches everything not covered by previous conditions
- **Comparison operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical operators**: `and`, `or`, `not`
- **Membership**: `in`, `not in`
- **Identity**: `is`, `is not` (use `is None` for None checks)
- **Ternary**: `value_if_true if condition else value_if_false`
- **Truthiness**: empty collections, `None`, `0`, `""` are falsy
- **Chained comparisons**: `1 < x < 10` is Pythonic and clean
- **Match statement** (Python 3.10+) for pattern matching
