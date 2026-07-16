# User Input in Python

## Topic 33: Getting Data from Users

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use the `input()` function to get user input
2. Convert input strings to appropriate data types
3. Validate user input
4. Create interactive programs
5. Handle input errors gracefully
6. Build command-line interfaces

---

## 1. The `input()` Function

The `input()` function reads a line of text from the user.

### Basic Usage

```python
# Simple input
name = input("Enter your name: ")
print(f"Hello, {name}!")

# The input is always a string
age = input("Enter your age: ")
print(type(age))  # <class 'str'>
```

### With Prompt

```python
# The prompt is displayed to the user
response = input("What is your favorite color? ")
print(f"You chose: {response}")
```

---

## 2. Converting Input Types

### String to Number

```python
# Integer input
age = int(input("Enter your age: "))

# Float input
height = float(input("Enter your height in meters: "))

# Math operations work after conversion
age_next_year = age + 1
print(f"Next year you'll be {age_next_year}")
```

### Multiple Values

```python
# Using split()
numbers = input("Enter three numbers: ").split()
print(numbers)  # ['1', '2', '3']

# Convert to integers
numbers = [int(x) for x in input("Enter three numbers: ").split()]

# Map approach
a, b, c = map(int, input("Enter three numbers: ").split())
```

---

## 3. Input Validation

### Basic Validation

```python
# Validate integer input
while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 150:
            break
        else:
            print("Please enter a valid age (0-150)")
    except ValueError:
        print("Please enter a number!")

print(f"Your age: {age}")
```

### Confirmation Input

```python
def confirm(message):
    """Get yes/no confirmation from user."""
    while True:
        response = input(f"{message} (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'")

# Usage
if confirm("Do you want to continue?"):
    print("Continuing...")
else:
    print("Cancelled.")
```

---

## 4. Menu Systems

### Simple Menu

```python
def show_menu():
    print("\n=== Menu ===")
    print("1. Option A")
    print("2. Option B")
    print("3. Option C")
    print("4. Exit")
    print("============")

while True:
    show_menu()
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        print("Option A selected")
    elif choice == '2':
        print("Option B selected")
    elif choice == '3':
        print("Option C selected")
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")
```

---

## 5. Password Input

```python
import getpass

# getpass hides input (no echo)
password = getpass.getpass("Enter password: ")
print("Password entered (hidden from view)")

# Or use input with note
password = input("Enter password (will be visible): ")
```

---

## 6. Command-Line Arguments

### Using sys.argv

```python
import sys

# sys.argv is a list of command-line arguments
print(f"Script name: {sys.argv[0]}")
print(f"Arguments: {sys.argv[1:]}")

# Example: python script.py arg1 arg2
# sys.argv = ['script.py', 'arg1', 'arg2']
```

### Using argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('numbers', type=int, nargs='+',
                    help='numbers to sum')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='enable verbose output')

args = parser.parse_args()

total = sum(args.numbers)
if args.verbose:
    print(f"Sum of {args.numbers} = {total}")
else:
    print(total)
```

---

## 7. Input Patterns

### Required Field

```python
def get_required(prompt):
    """Get required input from user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required!")

name = get_required("Enter your name: ")
```

### Default Value

```python
# Show default in prompt
default_port = 8080
port_input = input(f"Port [{default_port}]: ").strip()
port = int(port_input) if port_input else default_port
```

### Choice Selection

```python
def get_choice(options, prompt="Select: "):
    """Get validated choice from user."""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Enter 1-{len(options)}")
        except ValueError:
            print("Enter a number!")

color = get_choice(["Red", "Green", "Blue"])
```

---

## 8. Common Mistakes to Avoid

### 1. Not Converting Input

```python
# BAD - input is always string
age = input("Enter age: ")
next_age = age + 1  # TypeError!

# GOOD - convert first
age = int(input("Enter age: "))
next_age = age + 1
```

### 2. No Error Handling

```python
# BAD - crashes on invalid input
age = int(input("Enter age: "))

# GOOD - handle errors
try:
    age = int(input("Enter age: "))
except ValueError:
    print("Invalid number!")
```

### 3. Not Validating Range

```python
# BAD - accepts any number
age = int(input("Enter age: "))

# GOOD - validate range
age = int(input("Enter age: "))
if age < 0 or age > 150:
    print("Invalid age!")
```

---

## 9. Best Practices

1. **Always convert** input to appropriate type
2. **Validate input** before processing
3. **Use loops** to re-prompt on invalid input
4. **Provide clear prompts** telling users what to enter
5. **Show default values** when applicable
6. **Use `getpass`** for sensitive input
7. **Handle `KeyboardInterrupt** for clean exit
8. **Strip whitespace** from input

---

## 10. Practice Exercises

### Exercise 1: Age Calculator

```python
from datetime import datetime

def get_valid_date():
    """Get a valid date from user."""
    while True:
        try:
            date_str = input("Enter date (YYYY-MM-DD): ")
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD")

def calculate_age():
    """Calculate age from birthdate."""
    birth_date = get_valid_date()
    today = datetime.now()
    
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

age = calculate_age()
print(f"You are approximately {age} years old!")
```

### Exercise 2: Calculator

```python
def calculator():
    """Simple calculator with user input."""
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("First number (or 'q' to quit): "))
        except ValueError:
            choice = input("Quit? (y/n): ").lower()
            if choice == 'y':
                break
            continue
        
        op = input("Operation (+, -, *, /): ")
        num2 = float(input("Second number: "))
        
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                print("Cannot divide by zero!")
                continue
            result = num1 / num2
        else:
            print("Invalid operation!")
            continue
        
        print(f"Result: {result}")

calculator()
```

---

## 11. Summary

| Concept | Key Points |
|---------|------------|
| **input()** | Reads string from user |
| **Type conversion** | `int()`, `float()` for numbers |
| **Validation** | Check input before processing |
| **getpass()** | Hidden input (passwords) |
| **sys.argv** | Command-line arguments |
| **argparse** | Argument parsing library |

---

## Next Steps

- Learn about GUI input (tkinter, PyQt)
- Explore web form input handling
- Study async input patterns
