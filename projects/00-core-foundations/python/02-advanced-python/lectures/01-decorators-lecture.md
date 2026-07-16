# Advanced Python Lecture 01: Decorators

## Topic Overview

Decorators are one of Python's most powerful and elegant features, enabling you to modify or extend the behavior of functions or classes without permanently altering their source code. Rooted in the concept of higher-order functions, decorators provide a clean, readable syntax for wrapping functions with additional functionality — a pattern essential for cross-cutting concerns like logging, authentication, caching, and validation.

This lecture explores decorators from foundational concepts through advanced patterns used in production Python codebases and AI engineering workflows.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand first-class functions and higher-order functions as the foundation of decorators
2. Write basic function decorators using the `@decorator` syntax
3. Create decorators that accept arguments using decorator factories
4. Build class-based decorators
5. Use `functools.wraps` to preserve metadata
6. Implement common real-world decorator patterns (logging, caching, timing, retry)
7. Compose and stack multiple decorators
8. Apply decorators to class methods and static methods
9. Debug decorator-related issues
10. Follow best practices for production decorator design

---

## 1. Foundation: First-Class Functions

In Python, functions are **first-class objects** — they can be assigned to variables, passed as arguments, returned from other functions, and stored in data structures.

```python
# Functions as first-class objects
def greet(name):
    return f"Hello, {name}!"

# Assign to a variable
say_hello = greet
print(say_hello("Alice"))  # "Hello, Alice!"

# Store in a data structure
dispatch = {
    "greet": greet,
    "upper": str.upper,
}

# Pass as an argument
def apply(func, value):
    return func(value)

print(apply(greet, "Bob"))  # "Hello, Bob!"
```

### Higher-Order Functions

A **higher-order function** is a function that either:
- Takes one or more functions as arguments, OR
- Returns a function as its result

```python
# Higher-order function: takes a function as argument
def repeat(func, times):
    def wrapper(*args, **kwargs):
        results = []
        for _ in range(times):
            results.append(func(*args, **kwargs))
        return results
    return wrapper

@repeat
def say_hi():
    return "Hi!"

print(say_hi())  # ['Hi!', 'Hi!', 'Hi!']

# Higher-order function: returns a function
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(5))   # 10
print(triple(5))   # 15
```

---

## 2. Basic Decorators

### The Manual Approach

```python
def my_decorator(func):
    def wrapper():
        print("Something before the function")
        func()
        print("Something after the function")
    return wrapper

def say_hello():
    print("Hello!")

# Manually decorating
say_hello = my_decorator(say_hello)
say_hello()
# Output:
# Something before the function
# Hello!
# Something after the function
```

### The `@decorator` Syntax

Python provides syntactic sugar that makes this cleaner:

```python
def my_decorator(func):
    def wrapper():
        print("Something before the function")
        func()
        print("Something after the function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Equivalent to: say_hello = my_decorator(say_hello)
say_hello()
```

### Preserving Function Metadata with `functools.wraps`

Without `functools.wraps`, the decorated function loses its original metadata:

```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # Preserves func's metadata
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

print(greet.__name__)  # "greet" (not "wrapper")
print(greet.__doc__)   # "Greet someone by name."
```

### Handling Arguments

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers."""
    return a + b

add(3, 5)
# Calling add with (3, 5), {}
# add returned 8
```

---

## 3. Decorators with Arguments (Decorator Factories)

When you need to pass arguments to a decorator itself, you need an extra layer of nesting:

```python
import functools

def repeat(times):
    """Decorator factory that repeats a function call `times` times."""
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
def say_hello(name):
    print(f"Hello, {name}!")
    return name

result = say_hello("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### Real-World Example: Retry Decorator

```python
import functools
import time

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"Attempt {attempt} failed: {e}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Connection refused")
    return {"status": "ok"}
```

---

## 4. Class-Based Decorators

Classes can implement decorators using the `__call__` method:

```python
import functools
import time

class Timer:
    """Class-based decorator that times function execution."""
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.total_time = 0
        self.call_count = 0
    
    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        self.total_time += elapsed
        self.call_count += 1
        
        print(f"{self.func.__name__} took {elapsed:.4f}s "
              f"(avg: {self.total_time / self.call_count:.4f}s)")
        return result
    
    def stats(self):
        """Return timing statistics."""
        return {
            "total_time": self.total_time,
            "call_count": self.call_count,
            "avg_time": self.total_time / self.call_count if self.call_count else 0
        }

@Timer
def slow_function(n):
    time.sleep(n / 10)
    return n

slow_function(1)
slow_function(2)
print(slow_function.stats())
```

### Class Decorator with Arguments

```python
import functools

class RateLimiter:
    """Rate limiter that limits function calls per time window."""
    
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
    
    def __call__(self, func):
        import collections
        calls = collections.deque()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove expired entries
            while calls and calls[0] <= now - self.period:
                calls.popleft()
            
            if len(calls) >= self.max_calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {self.max_calls} calls per {self.period}s"
                )
            
            calls.append(now)
            return func(*args, **kwargs)
        
        wrapper.calls = calls
        return wrapper
```

---

## 5. Decorators for Classes and Methods

### Decorating Classes

```python
import functools

def add_repr(cls):
    """Decorator that adds a __repr__ method to a class."""
    def repr_method(self):
        attrs = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{cls.__name__}({attrs})"
    
    cls.__repr__ = repr_method
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p)  # Point(x=3, y=4)
```

### Decorating Methods

```python
import functools

def log_method(func):
    """Decorator for instance methods."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {type(self).__name__}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

def validate_positive(func):
    """Decorator that validates first argument is positive."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args and args[0] <= 0:
            raise ValueError(f"Expected positive value, got {args[0]}")
        return func(*args, **kwargs)
    return wrapper

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    @log_method
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    @validate_positive
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance
```

### Built-in Method Decorators

```python
class MyClass:
    @staticmethod
    def static_method():
        """No access to class or instance."""
        return "static"
    
    @classmethod
    def class_method(cls):
        """Access to class, not instance."""
        return f"class method of {cls.__name__}"
    
    @property
    def value(self):
        """Getter for a property."""
        return self._value
    
    @value.setter
    def value(self, val):
        """Setter for a property."""
        if val < 0:
            raise ValueError("Value cannot be negative")
        self._value = val
```

---

## 6. Common Decorator Patterns

### Caching / Memoization

```python
import functools

# Simple cache
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Custom cache with TTL
def ttl_cache(maxsize=128, ttl=300):
    """Cache with time-to-live expiration."""
    import time
    
    def decorator(func):
        cache = {}
        timestamps = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            
            # Check if cached and not expired
            if args in cache and (now - timestamps[args]) < ttl:
                return cache[args]
            
            result = func(*args)
            cache[args] = result
            timestamps[args] = now
            
            # Evict if over capacity
            if len(cache) > maxsize:
                oldest = min(timestamps, key=timestamps.get)
                del cache[oldest]
                del timestamps[oldest]
            
            return result
        
        wrapper.cache_clear = lambda: (cache.clear(), timestamps.clear())
        return wrapper
    return decorator

@ttl_cache(ttl=60)
def get_user(user_id):
    """Fetch user with 60-second cache."""
    print(f"Fetching user {user_id} from database...")
    return {"id": user_id, "name": "Alice"}
```

### Logging Decorator

```python
import functools
import logging
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)

def log_execution(
    level: str = "INFO",
    include_args: bool = True,
    include_result: bool = False
):
    """Configurable logging decorator."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            log_func = getattr(logger, level.lower())
            
            func_name = func.__name__
            if include_args:
                log_msg = f"Entering {func_name} | args={args}, kwargs={kwargs}"
            else:
                log_msg = f"Entering {func_name}"
            
            log_func(log_msg)
            start = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                
                if include_result:
                    log_msg = f"Exiting {func_name} | result={result} | {elapsed:.4f}s"
                else:
                    log_msg = f"Exiting {func_name} | {elapsed:.4f}s"
                
                log_func(log_msg)
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                logger.error(
                    f"Error in {func_name}: {e} | {elapsed:.4f}s"
                )
                raise
        
        return wrapper
    return decorator
```

### Validation Decorator

```python
import functools

def validate_types(*type_args, **type_kwargs):
    """Validate function argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Validate positional arguments
            for i, (arg, expected) in enumerate(zip(args, type_args)):
                if not isinstance(arg, expected):
                    raise TypeError(
                        f"Argument {i} of {func.__name__} must be {expected.__name__}, "
                        f"got {type(arg).__name__}"
                    )
            
            # Validate keyword arguments
            for key, expected in type_kwargs.items():
                if key in kwargs:
                    arg = kwargs[key]
                    if not isinstance(arg, expected):
                        raise TypeError(
                            f"Argument '{key}' of {func.__name__} must be "
                            f"{expected.__name__}, got {type(arg).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(int, str, debug=bool)
def process_data(user_id, name, debug=False):
    return f"Processing {name} (id={user_id})"
```

---

## 7. Decorator Composition and Stacking

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

def underline(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper

@bold
@italic
@underline
def greet(name):
    return f"Hello, {name}!"

# Decorators applied bottom-to-top, executed top-to-bottom
# greet = bold(italic(underline(greet)))
print(greet("World"))
# Output: <b><i><u>Hello, World!</u></i></b>
```

### Conditional Decorator Application

```python
import functools

def conditional_decorator(condition, decorator):
    """Apply decorator only if condition is True."""
    def wrapper(func):
        if condition:
            return decorator(func)
        return func
    return wrapper

DEBUG = True

@conditional_decorator(DEBUG, my_decorator)
def debug_only_function():
    pass
```

---

## 8. Common Mistakes to Avoid

### Mistake 1: Forgetting `functools.wraps`

```python
# BAD: Loses function metadata
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# GOOD: Preserves metadata
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Mistake 2: Mutable Default Arguments in Decorators

```python
# BAD: Shared mutable state between calls
def bad_decorator(func):
    results = []  # Shared across all decorated functions
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        results.append(result)  # Accumulates forever
        return result
    return wrapper

# GOOD: Fresh state per decorator instance
def good_decorator(func):
    def wrapper(*args, **kwargs):
        results = []  # Fresh per call
        result = func(*args, **kwargs)
        results.append(result)
        return result
    return wrapper
```

### Mistake 3: Not Handling Exceptions Properly

```python
# BAD: Swallows exceptions silently
def bad_catch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:  # Catches EVERYTHING including SystemExit
            return None
    return wrapper

# GOOD: Specific exception handling with re-raise
def good_catch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"ValueError in {func.__name__}: {e}")
            raise  # Re-raise after logging
    return wrapper
```

### Mistake 4: Decorator Order Confusion

```python
# Order matters! Applied bottom-to-top
@decorator_a
@decorator_b
@decorator_c
def func():
    pass

# Equivalent to: func = decorator_a(decorator_b(decorator_c(func)))
```

---

## 9. Best Practices

1. **Always use `functools.wraps`** to preserve function metadata
2. **Keep decorators simple** — avoid complex logic that's hard to debug
3. **Document your decorators** with clear docstrings
4. **Use type hints** in decorator signatures for IDE support
5. **Prefer function decorators** over class decorators for simple cases
6. **Use class decorators** when you need to maintain state
7. **Test decorators independently** before applying to functions
8. **Consider `functools.partial`** for simple parameter binding before resorting to decorators
9. **Profile performance** — decorators add overhead, be mindful in hot paths
10. **Avoid side effects** in decorator definitions (keep them pure when possible)

---

## 10. Practice Exercises

### Exercise 1: Basic Decorator
Write a `@debug` decorator that prints the function name, arguments, and return value:

```python
@debug
def add(a, b):
    return a + b

# Expected output:
# Calling add(3, 5)
# add returned 8
```

### Exercise 2: Decorator Factory
Create a `@retry(max_attempts=3, delay=1)` decorator that retries failed function calls:

```python
@retry(max_attempts=3, delay=1)
def unstable_function():
    import random
    if random.random() < 0.5:
        raise ConnectionError("Network error")
    return "Success"
```

### Exercise 3: Class-Based Decorator
Build a `@singleton` decorator that ensures only one instance of a class is created:

```python
@singleton
class Database:
    def __init__(self):
        print("Connecting to database...")

db1 = Database()  # "Connecting to database..."
db2 = Database()  # No output - returns same instance
assert db1 is db2
```

### Exercise 4: Composed Decorators
Create `@timer` and `@log` decorators and compose them:

```python
@timer
@log
def process_data(data):
    return [x ** 2 for x in data]
```

### Exercise 5: Method Decorator
Write a `@validate` decorator that validates method arguments against a schema:

```python
class User:
    @validate(name=str, age=int, email=str)
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

user = User("Alice", 30, "alice@example.com")  # OK
user = User("Alice", "thirty", "alice@example.com")  # TypeError
```

---

## 11. Summary

| Concept | Description |
|---------|-------------|
| **First-class functions** | Functions can be passed as arguments, returned, and assigned |
| **Higher-order functions** | Functions that take/return other functions |
| **`@decorator` syntax** | Syntactic sugar for `func = decorator(func)` |
| **Decorator factory** | A function that returns a decorator (for parameterized decorators) |
| **`functools.wraps`** | Preserves original function metadata through decoration |
| **Class-based decorator** | Uses `__call__` to make instances callable |
| **Composition** | Multiple decorators stack bottom-to-top |
| **Common patterns** | Caching, logging, timing, retry, validation, rate limiting |

Decorators are a fundamental tool in Python that enable clean, reusable, and maintainable code. Master them to write more Pythonic and expressive programs, especially in AI engineering workflows where cross-cutting concerns like logging, caching, and error handling are pervasive.

---

## Next Steps

In the next lecture, we'll explore **Generators and Iterators**, which build on the same higher-order function concepts to enable lazy evaluation and memory-efficient data processing.
