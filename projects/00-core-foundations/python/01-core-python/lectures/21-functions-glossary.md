# Python Functions — Glossary 21

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Function | Reusable block of code | `def greet(name):` |
| Parameter | Variable in function definition | `def f(x):` |
| Argument | Value passed to function | `f(5)` |
| Return | Send value back from function | `return x + 1` |
| Default Argument | Parameter with default value | `def f(x=10):` |
| Keyword Argument | Argument passed by name | `f(name="Alice")` |
| Positional Argument | Argument passed by position | `f(5, 10)` |
| *args | Variable positional arguments | `def f(*args):` |
| **kwargs | Variable keyword arguments | `def f(**kwargs):` |
| Lambda | Anonymous one-line function | `lambda x: x + 1` |
| Closure | Function capturing enclosing scope | `def outer(): def inner():` |
| Decorator | Function modifying another function | `@timer` |
| Scope | Variable visibility region | local, enclosing, global |
| LEGB | Scope resolution order | Local→Enclosing→Global→Builtin |
| Docstring | Function documentation string | `"""Description"""` |
| Type Hint | Variable type annotation | `def f(x: int) -> str:` |
| Pure Function | No side effects, same input → same output | `def add(a, b): return a + b` |
| Higher-Order | Function that takes/returns functions | `map(func, iterable)` |
| Callback | Function passed as argument | `def on_click(callback):` |
| Generator | Function using `yield` | `def gen(): yield x` |
| Memoize | Cache function results | `@lru_cache` |

---

## Definitions

### *args
**Definition**: A parameter that collects extra positional arguments into a tuple. Allows a function to accept any number of positional arguments.

**Example**:
```python
def sum_all(*args):
    """Sum any number of arguments."""
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3))      # 6
print(sum_all(1, 2, 3, 4, 5)) # 15
```

**Related**: `**kwargs`, tuple, variable arguments

---

### **kwargs
**Definition**: A parameter that collects extra keyword arguments into a dictionary. Allows a function to accept any number of keyword arguments.

**Example**:
```python
def print_info(**kwargs):
    """Print all keyword arguments."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
# name: Alice
# age: 30
# city: NYC
```

**Related**: `*args`, dictionary, keyword arguments

---

### Callback
**Definition**: A function passed as an argument to another function, to be called ("called back") at a later time or when an event occurs.

**Example**:
```python
def on_click(callback):
    """Simulate button click."""
    print("Button clicked!")
    callback()

def handle_click():
    print("Click handled!")

on_click(handle_click)
```

**Related**: event handler, higher-order function, function as argument

---

### Closure
**Definition**: A function that captures and remembers variables from its enclosing scope, even after the enclosing function has finished executing.

**Example**:
```python
def counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = counter(10)
print(c())  # 11
print(c())  # 12
```

**Related**: enclosing scope, `nonlocal`, factory function

---

### Decorator
**Definition**: A function that takes another function and returns a modified version, adding behavior before/after. Applied with `@decorator` syntax.

**Example**:
```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow():
    import time
    time.sleep(1)

slow()  # Prints timing
```

**Related**: closure, higher-order function, `@` syntax

---

### Default Argument
**Definition**: A parameter that has a default value used when the argument is not provided by the caller.

**Example**:
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Alice", "Hi"))    # Hi, Alice!
```

**Mutable default warning**: Don't use mutable defaults like `[]` or `{}` — use `None` instead.

**Related**: keyword argument, optional parameter

---

### Docstring
**Definition**: A string literal that serves as documentation for a function, class, or module. Placed as the first statement and accessible via `__doc__`.

**Example**:
```python
def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    return a + b

print(add.__doc__)
```

**Related**: documentation, `__doc__`, help()

---

### Function
**Definition**: A reusable block of code that performs a specific task, defined with `def`. Can accept parameters and return values.

**Example**:
```python
def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

**Related**: def, parameter, return, scope

---

### Generator
**Definition**: A function that returns an iterator using `yield`, producing values lazily one at a time instead of returning all at once.

**Example**:
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

**Related**: `yield`, iterator, lazy evaluation, memory efficiency

---

### Higher-Order Function
**Definition**: A function that takes other functions as arguments, or returns a function as its result. Examples: `map()`, `filter()`, `sorted()`.

**Example**:
```python
# Takes function as argument
def apply_twice(func, x):
    return func(func(x))

print(apply_twice(lambda x: x * 2, 3))  # 12

# Returns function
def multiplier(factor):
    return lambda x: x * factor

double = multiplier(2)
print(double(5))  # 10
```

**Related**: lambda, map, filter, function as first-class object

---

### LEGB
**Definition**: The scope resolution order in Python: Local → Enclosing → Global → Built-in. Python looks for variables in this order.

**Example**:
```python
x = "global"          # Global

def outer():
    x = "enclosing"    # Enclosing
    
    def inner():
        x = "local"    # Local
        print(x)       # "local"
    
    inner()

outer()
```

**Related**: scope, local, enclosing, global, builtin

---

### Lambda
**Definition**: An anonymous one-line function defined with `lambda` keyword. Can have any number of arguments but only one expression.

**Example**:
```python
# Simple lambda
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda with multiple args
add = lambda a, b: a + b

# Lambda in sorting
students = [("Alice", 85), ("Bob", 92)]
students.sort(key=lambda s: s[1], reverse=True)

# Lambda with map/filter
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
```

**Related**: anonymous function, map, filter, one-liner

---

### Memoize
**Definition**: A technique (often implemented as a decorator) that caches function results to avoid redundant computation.

**Example**:
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # Instant!
```

**Related**: caching, `lru_cache`, performance optimization

---

### Pure Function
**Definition**: A function that always returns the same output for the same input and produces no side effects (no modifying external state).

**Example**:
```python
# Pure function
def add(a, b):
    return a + b

# Impure function (has side effect)
total = 0
def add_to_total(x):
    global total
    total += x  # Modifies external state
```

**Related**: side effects, functional programming, testability

---

### Scope
**Definition**: The region of code where a variable is accessible. Python has four scope levels: local, enclosing, global, and builtin.

**Example**:
```python
# Global scope
x = 10

def func():
    # Local scope
    y = 20
    print(x)  # Can access global
    print(y)  # Can access local

func()
# print(y)  # Error: y is local
```

**Related**: LEGB, local, enclosing, global, builtin, `global`, `nonlocal`

---

### Type Hint
**Definition**: Annotations indicating the expected types of function parameters and return values. Improves code readability and enables static type checking.

**Example**:
```python
def greet(name: str, times: int = 1) -> str:
    """Greet someone multiple times."""
    return (f"Hello, {name}! " * times).strip()

# Type hints don't enforce types at runtime
print(greet("Alice"))        # Hello, Alice!
print(greet("Bob", 3))      # Hello, Bob! Hello, Bob! Hello, Bob!
```

**Related**: annotation, mypy, type checking, documentation

---

## Code Examples

### Example 1: Function Factory
```python
def create_multiplier(factor):
    """Create a multiplier function."""
    def multiplier(x):
        return x * factor
    return multiplier

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

### Example 2: Compose Functions
```python
def compose(*funcs):
    """Compose multiple functions."""
    def composed(x):
        result = x
        for f in reversed(funcs):
            result = f(result)
        return result
    return composed

add_one = lambda x: x + 1
double = lambda x: x * 2
square = lambda x: x ** 2

transform = compose(square, double, add_one)
print(transform(3))  # square(double(add_one(3))) = 64
```

### Example 3: Once Function
```python
def once(func):
    """Call function only once, cache result."""
    called = False
    result = None
    def wrapper(*args, **kwargs):
        nonlocal called, result
        if not called:
            called = True
            result = func(*args, **kwargs)
        return result
    return wrapper

@once
def expensive_calculation():
    print("Computing...")
    return 42

print(expensive_calculation())  # Computing... 42
print(expensive_calculation())  # 42 (no computation)
```

---

## Related Concepts

- **First-Class Functions**: Functions as objects (assign, pass, return)
- **Functional Programming**: map, filter, reduce, composition
- **Closures**: Capturing enclosing scope
- **Decorators**: Function transformation
- **Generators**: Lazy iteration with yield
- **Recursion**: Function calling itself
- **Callbacks**: Functions passed as arguments
