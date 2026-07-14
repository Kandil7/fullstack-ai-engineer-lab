# Decorators Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Decorator | A function that modifies another function's behavior |
| Higher-Order Function | A function that takes or returns functions |
| First-Class Function | A function treated as an object |
| `@` Syntax | Syntactic sugar for decoration |
| `functools.wraps` | Preserves function metadata |
| Decorator Factory | A function that returns a decorator |
| Class-Based Decorator | A class implementing `__call__` |
| Composition | Stacking multiple decorators |
| Wrapper | The inner function in a decorator |
| Closure | A function capturing variables from enclosing scope |
| Memoization | Caching function results |
| `lru_cache` | Built-in least-recently-used cache |
| Monkey Patching | Modifying behavior at runtime |
| Aspect-Oriented Programming | Separating cross-cutting concerns |
| Descriptor | Protocol for managed attribute access |

---

## Detailed Definitions

### Aspect-Oriented Programming (AOP)

**Definition**: A programming paradigm that separates cross-cutting concerns (logging, security, caching) from main business logic, typically implemented via decorators.

**Example**:
```python
# Without AOP: logging mixed with business logic
def process_order(order):
    log.info(f"Processing order {order.id}")
    result = calculate_total(order)
    log.info(f"Order processed: {result}")
    return result

# With AOP: logging separated via decorator
@log_execution
def process_order(order):
    return calculate_total(order)
```

**Related**: Decorator, Cross-Cutting Concern, Separation of Concerns

---

### Class-Based Decorator

**Definition**: A class that implements the `__call__` method, allowing instances to be used as decorators. Useful when you need to maintain state across calls.

**Example**:
```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # say_hello called 1 times; Hello!
say_hello()  # say_hello called 2 times; Hello!
```

**Related**: `__call__`, `functools.update_wrapper`, Instance State

---

### Closure

**Definition**: A function object that remembers values from its enclosing lexical scope even after the outer function has finished executing. Essential for decorators to maintain state.

**Example**:
```python
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
# 'count' persists in the closure
```

**Related**: `nonlocal`, Enclosing Scope, LEGB Rule

---

### Composition

**Definition**: The process of combining multiple decorators on a single function. Decorators are applied bottom-to-top but execute top-to-bottom.

**Example**:
```python
import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}!"

# Applied as: bold(italic(greet))
print(greet("World"))  # <b><i>Hello, World!</i></b>
```

**Related**: Decorator Stacking, Execution Order

---

### Cross-Cutting Concern

**Definition**: A concern that spans multiple modules or layers of an application, such as logging, authentication, or error handling. Decorators are the primary Python mechanism for implementing these.

**Example**:
```python
@require_auth
@rate_limit(calls_per_minute=60)
@log_execution
def api_endpoint(request):
    return process_request(request)
```

**Related**: AOP, Decorator, Middleware

---

### Decorator

**Definition**: A function that takes a function as input and returns a new function with enhanced behavior. The `@decorator_name` syntax provides syntactic sugar for applying decorators.

**Example**:
```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)

slow_function()  # slow_function took 1.0012s
```

**Related**: Higher-Order Function, Wrapper, `functools.wraps`

---

### Decorator Factory

**Definition**: A function that returns a decorator. Used when you need to pass arguments to a decorator itself. Requires three levels of nesting.

**Example**:
```python
import functools

def repeat(times):
    """Decorator factory: returns a decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

**Related**: Decorator, Parameterized Decorator, Factory Pattern

---

### Descriptor Protocol

**Definition**: A protocol that allows objects to customize attribute access. Decorators like `@property`, `@staticmethod`, and `@classmethod` are built on descriptors.

**Example**:
```python
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.attrname = func.__name__
    
    def __set_name__(self, owner, name):
        self.attrname = name
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        value = self.func(instance)
        setattr(instance, self.attrname, value)
        return value

class DataProcessor:
    @CachedProperty
    def processed_data(self):
        print("Computing...")
        return [x ** 2 for x in range(1000)]

processor = DataProcessor()
processor.processed_data  # Computing... [computed value]
processor.processed_data  # [cached, no "Computing..."]
```

**Related**: `@property`, `__get__`, `__set__`, Managed Attributes

---

### First-Class Function

**Definition**: A function in Python that can be treated like any other object — assigned to variables, passed as arguments, returned from functions, and stored in data structures.

**Example**:
```python
def greet(name):
    return f"Hello, {name}!"

# Assigned to variable
my_greet = greet

# Stored in data structure
functions = {"greet": greet, "upper": str.upper}

# Passed as argument
def apply(func, value):
    return func(value)

apply(greet, "World")  # "Hello, World!"
```

**Related**: Higher-Order Function, Callable, First-Class Object

---

### `functools.lru_cache`

**Definition**: A built-in decorator that caches function results based on arguments, using a least-recently-used eviction policy. Essential for performance optimization.

**Example**:
```python
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)  # Instant result due to caching
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)
```

**Related**: Memoization, Cache, Performance Optimization

---

### `functools.update_wrapper`

**Definition**: A function that copies metadata from the wrapped function to the wrapper. `functools.wraps` is a shortcut for this function.

**Example**:
```python
import functools

def my_decorator(func):
    wrapper = lambda *args, **kwargs: func(*args, **kwargs)
    functools.update_wrapper(wrapper, func)
    return wrapper

# Equivalent to:
def my_decorator_v2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

**Related**: `functools.wraps`, Metadata Preservation

---

### `functools.wraps`

**Definition**: A decorator that copies the metadata (`__name__`, `__doc__`, `__module__`, `__wrapped__`, etc.) from the original function to the wrapper function.

**Example**:
```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring (ignored if wraps is used)."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)  # "greet" (not "wrapper")
print(greet.__doc__)   # "Greet someone."
print(greet.__wrapped__)  # Original unwrapped function
```

**Related**: `functools.update_wrapper`, Metadata, `__wrapped__`

---

### Higher-Order Function

**Definition**: A function that either takes one or more functions as arguments, or returns a function as its result. Decorators are higher-order functions.

**Example**:
```python
# Takes a function as argument
def apply_to_list(func, items):
    return [func(item) for item in items]

# Returns a function
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
apply_to_list(double, [1, 2, 3])  # [2, 4, 6]
```

**Related**: First-Class Function, Decorator, Functional Programming

---

### `lru_cache`

**Definition**: See `functools.lru_cache`. A decorator that provides memoization with automatic eviction of least-recently-used entries.

**Example**:
```python
from functools import lru_cache

@lru_cache(maxsize=256)
def expensive_computation(n):
    # Simulate expensive work
    return sum(i ** 2 for i in range(n))

result = expensive_computation(1000)
# Second call is instant
result = expensive_computation(1000)
```

**Related**: `functools.lru_cache`, Memoization, Caching

---

### Memoization

**Definition**: An optimization technique where function results are cached based on input arguments, avoiding redundant computation.

**Example**:
```python
import functools

# Manual memoization
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

# Built-in memoization
@functools.lru_cache
def fibonacci(n):
    return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)
```

**Related**: `lru_cache`, Caching, Performance Optimization

---

### Monkey Patching

**Definition**: Dynamically modifying classes, modules, or objects at runtime to alter behavior. Decorators can be seen as a structured form of monkey patching.

**Example**:
```python
# Monkey patching (fragile)
original_print = print
def patched_print(*args, **kwargs):
    original_print("[PATCHED]", *args, **kwargs)
print = patched_print

# Decorator approach (safer)
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

**Related**: Runtime Modification, Dynamic Behavior, Decorator

---

### `nonlocal`

**Definition**: A keyword that allows a nested function to modify a variable in its enclosing (but not global) scope. Essential for closures used in decorators.

**Example**:
```python
def make_counter():
    count = 0
    
    def counter():
        nonlocal count  # Without this, UnboundLocalError
        count += 1
        return count
    
    return counter

counter = make_counter()
counter()  # 1
counter()  # 2
```

**Related**: Closure, Enclosing Scope, Nested Functions

---

### Parameterized Decorator

**Definition**: A decorator that accepts arguments, implemented using a decorator factory (extra layer of nesting).

**Example**:
```python
import functools

def validate_range(min_val=None, max_val=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if min_val is not None and result < min_val:
                raise ValueError(f"Result {result} below minimum {min_val}")
            if max_val is not None and result > max_val:
                raise ValueError(f"Result {result} above maximum {max_val}")
            return result
        return wrapper
    return decorator

@validate_range(min_val=0, max_val=100)
def calculate_score(answers):
    return sum(answers) / len(answers) * 100
```

**Related**: Decorator Factory, `@decorator(arg)` Syntax

---

### Wrapper

**Definition**: The inner function returned by a decorator that surrounds the original function with additional behavior.

**Example**:
```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # <-- This is the wrapper
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

**Related**: Decorator, Closure, `functools.wraps`

---

### `__call__`

**Definition**: A special method that makes an instance of a class callable like a function. Used in class-based decorators.

**Example**:
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
print(callable(double))  # True
```

**Related**: Callable Protocol, Class-Based Decorator, Magic Methods

---

### `__wrapped__`

**Definition**: An attribute set by `functools.wraps` that points to the original unwrapped function, allowing access to the pre-decorated version.

**Example**:
```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    return f"Hello, {name}!"

# Access original function
print(greet.__wrapped__("World"))  # "Hello, World!"
```

**Related**: `functools.wraps`, Metadata, Unwrapping

---
