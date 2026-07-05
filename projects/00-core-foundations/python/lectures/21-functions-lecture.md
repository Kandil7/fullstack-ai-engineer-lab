# Python Functions — Lecture 21

## Topic Overview

**Functions** are reusable blocks of code that perform a specific task. They are fundamental to writing clean, maintainable, and DRY (Don't Repeat Yourself) code. Functions in Python are first-class objects — they can be assigned to variables, passed as arguments, and returned from other functions.

This lecture covers function definition, parameters, return values, scope, closures, decorators, and advanced function patterns.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Define and call functions with parameters and return values
- Use default arguments, keyword arguments, and *args/**kwargs
- Understand variable scope (local, enclosing, global, builtin)
- Implement closures and decorators
- Use lambda functions for simple operations
- Apply best practices for function design

---

## Key Concepts

### 1. Defining and Calling Functions

```python
# Basic function definition
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)  # Hello, Alice!

# Functions without return value return None
def say_hello():
    print("Hello!")

result = say_hello()
print(result)  # None
```

### 2. Parameters and Arguments

```python
# Positional arguments
def add(a, b):
    return a + b

print(add(3, 5))  # 8

# Keyword arguments
print(add(b=5, a=3))  # 8

# Default arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Alice", "Hi"))        # Hi, Alice!
```

### 3. *args and **kwargs

```python
# *args — variable positional arguments (tuple)
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs — variable keyword arguments (dict)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")

# Combined
def complex_func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

complex_func(1, 2, 3, 4, x=5, y=6)
```

### 4. Return Values

```python
# Single return value
def square(x):
    return x ** 2

# Multiple return values (returns tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")

# Early return
def divide(a, b):
    if b == 0:
        return None  # Early return
    return a / b

# Returning different types based on condition
def process(data, mode="summary"):
    if mode == "summary":
        return sum(data) / len(data)
    elif mode == "all":
        return data
    return None
```

### 5. Variable Scope

```python
# Local scope
def my_func():
    x = 10  # Local variable
    print(x)

my_func()
# print(x)  # NameError: x is not defined

# Global scope
greeting = "Hello"  # Global variable

def use_global():
    global greeting
    greeting = "Hi"

# Enclosing scope (closures)
def outer():
    x = "outer"
    def inner():
        print(x)  # Accesses enclosing scope
    inner()

# LEGB Rule: Local → Enclosing → Global → Builtin
```

### 6. Lambda Functions

```python
# Lambda — anonymous function
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda with multiple arguments
add = lambda a, b: a + b
print(add(3, 5))  # 8

# Lambda in sorting
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda s: s[1], reverse=True)
print(students)  # [('Bob', 92), ('Alice', 85), ('Charlie', 78)]

# Lambda with filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]
```

### 7. Closures

```python
# A closure captures variables from enclosing scope
def multiplier(factor):
    def multiply(x):
        return x * factor  # 'factor' is captured
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Practical: counter
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

### 8. Decorators

```python
import time

# Basic decorator
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"

slow_function()  # Prints timing info

# Decorator with arguments
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()  # Prints "Hello!" 3 times
```

### 9. Docstrings and Type Hints

```python
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
    
    Returns:
        BMI value (weight / height^2)
    
    Raises:
        ValueError: If height is zero or negative
    """
    if height_m <= 0:
        raise ValueError("Height must be positive")
    return weight_kg / (height_m ** 2)

# Access docstring
print(calculate_bmi.__doc__)
```

---

## Code Examples

### Example 1: Function Composition

```python
def compose(*functions):
    """Compose multiple functions into one."""
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed

# Usage
double = lambda x: x * 2
add_one = lambda x: x + 1
square = lambda x: x ** 2

transform = compose(square, double, add_one)
print(transform(3))  # square(double(add_one(3))) = square(double(4)) = square(8) = 64
```

### Example 2: Memoization Decorator

```python
def memoize(func):
    """Cache function results."""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # Computed instantly!
```

### Example 3: Retry Decorator

```python
import time

def retry(max_attempts=3, delay=1):
    """Retry a function on failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"
```

### Example 4: Higher-Order Functions

```python
def apply_operation(func, *numbers):
    """Apply a function to a list of numbers."""
    return func(*numbers)

# Using with different operations
result1 = apply_operation(sum, 1, 2, 3, 4, 5)
result2 = apply_operation(max, 10, 20, 30)
result3 = apply_operation(min, 5, 3, 8, 1)

print(result1)  # 15
print(result2)  # 30
print(result3)  # 1
```

---

## Common Mistakes to Avoid

### Mistake 1: Mutable Default Arguments
```python
# WRONG — default list is shared across calls!
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] — unexpected!

# CORRECT
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Mistake 2: Not Returning Values
```python
# WRONG — forgets to return
def square(x):
    x ** 2  # Computed but not returned!

result = square(5)
print(result)  # None

# CORRECT
def square(x):
    return x ** 2
```

### Mistake 3: Shadowing Built-ins
```python
# WRONG — shadowing built-in functions
def list(items):  # Shadows built-in list!
    return items

# CORRECT
def process_items(items):
    return items
```

### Mistake 4: Global Variables
```python
# WRONG — modifying global without declaration
count = 0
def increment():
    global count
    count += 1

# BETTER — pass and return
def increment(count):
    return count + 1
```

---

## Best Practices

1. **Single Responsibility** — each function does one thing well
2. **Use descriptive names** — `calculate_average()` not `calc()`
3. **Keep functions small** — if >20 lines, consider splitting
4. **Use default arguments** for optional parameters
5. **Avoid mutable defaults** — use `None` instead
6. **Add docstrings** and type hints for clarity
7. **Use early returns** to reduce nesting
8. **Prefer pure functions** when possible (no side effects)
9. **Use decorators** for cross-cutting concerns (logging, timing)
10. **Test functions** in isolation

---

## Practice Exercises

### Exercise 1: Function Pipeline
Write a function that chains multiple transformations on a list.

```python
def pipeline(data, *functions):
    # Your code here
    pass

# Expected: [4, 16, 36]
print(pipeline([1, 2, 3], lambda x: x*2, lambda x: x**2))
```

### Exercise 2: Curry Function
Implement a curry function that transforms `f(a, b, c)` into `f(a)(b)(c)`.

```python
def curry(func):
    # Your code here
    pass

add = curry(lambda a, b, c: a + b + c)
print(add(1)(2)(3))  # 6
```

### Exercise 3: Rate Limiter
Create a decorator that limits function calls to N per minute.

```python
def rate_limit(calls_per_minute):
    # Your code here
    pass

@rate_limit(5)
def api_call():
    print("API called")
```

---

## Summary

- **Functions** are reusable code blocks with parameters and return values
- **Parameters**: positional, keyword, default, `*args`, `**kwargs`
- **Return**: single value, multiple values (tuple), or `None`
- **Scope**: Local → Enclosing → Global → Builtin (LEGB)
- **Closures** capture enclosing scope variables
- **Decorators** modify function behavior using `@decorator` syntax
- **Lambda** creates anonymous one-line functions
- **Docstrings** and **type hints** improve documentation
- **Mutable defaults** are shared — always use `None`!
