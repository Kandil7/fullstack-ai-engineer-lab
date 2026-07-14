# Python Functions Interview Practice

## Overview

Functions are first-class objects in Python. This guide covers function basics, arguments, closures, decorators, lambda functions, recursion, and higher-order functions. Master these concepts to write clean, reusable, and efficient Python code.

---

## Interview Questions

### Q1: Explain the difference between arguments and parameters.

**Answer:**
Parameters are variables in function definitions. Arguments are values passed when calling the function.

```python
# name and age are PARAMETERS
def greet(name, age):
    return f"Hello {name}, you are {age}"

# "Alice" and 30 are ARGUMENTS
greeting = greet("Alice", 30)

# Types of arguments
def func(a, b, c=10, *args, **kwargs):
    pass

# Positional arguments
func(1, 2, 3, 4, 5, x=6, y=7)
# a=1, b=2, c=3, args=(4, 5), kwargs={'x': 6, 'y': 7}
```

---

### Q2: What are *args and **kwargs?

**Answer:**
`*args` collects positional arguments into a tuple. `**kwargs` collects keyword arguments into a dictionary.

```python
def flexible(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

flexible(1, 2, 3, name="Alice", age=30)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 30}

# Unpacking in function calls
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))  # 6

config = {"a": 1, "b": 2, "c": 3}
print(add(**config))  # 6

# Combining with regular parameters
def func(a, b, *args, key1=None, **kwargs):
    pass

func(1, 2, 3, 4, key1="value", extra="data")
```

---

### Q3: What is the difference between default mutable and immutable arguments?

**Answer:**
Mutable default arguments are shared across calls, leading to unexpected behavior.

```python
# BAD: Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] - NOT ['b']!

# GOOD: Use None as default
def add_item_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item_safe("a"))  # ['a']
print(add_item_safe("b"))  # ['b'] - Correct!

# Immutable defaults are fine
def greet(name, times=1):
    return f"Hello {name}! " * times
```

---

### Q4: Explain closures and their use cases.

**Answer:**
A closure is a function that remembers variables from its enclosing scope, even after the outer function has returned.

```python
def outer(message):
    def inner():
        print(f"Message: {message}")
    return inner

greeting = outer("Hello")
greeting()  # Message: Hello
# 'message' is remembered even though outer() has finished

# Practical use: counter
def make_counter(start=0):
    count = [start]  # List to allow mutation
    def counter():
        count[0] += 1
        return count[0]
    return counter

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3

# Practical use: multiplier
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

---

### Q5: How do decorators work? Implement a basic decorator.

**Answer:**
Decorators are higher-order functions that modify other functions. They use the `@decorator` syntax.

```python
import functools
import time

# Basic decorator
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

# Decorator with arguments
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return "Success"
```

---

### Q6: Explain lambda functions and their limitations.

**Answer:**
Lambda functions are anonymous, single-expression functions. They're limited to one expression and can't contain statements.

```python
# Lambda syntax
square = lambda x: x ** 2
add = lambda a, b: a + b

print(square(5))  # 25
print(add(3, 4))  # 7

# Common use cases
# 1. Sorting with key
students = [("Alice", 90), ("Bob", 80), ("Charlie", 95)]
students.sort(key=lambda x: x[1], reverse=True)
print(students)  # [('Charlie', 95), ('Alice', 90), ('Bob', 80)]

# 2. With map, filter, reduce
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))

# 3. In dictionary sorting
data = {"b": 2, "a": 1, "c": 3}
sorted_keys = sorted(data.keys(), key=lambda k: data[k])

# Limitations
# - Only single expressions
# - No statements (assert, raise, etc.)
# - No type hints
# - Hard to debug (no name)
```

---

### Q7: What are higher-order functions?

**Answer:**
Higher-order functions take functions as arguments or return functions. Python has built-in ones like `map`, `filter`, `reduce`.

```python
from functools import reduce

# map - apply function to each element
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
print(squared)  # [1, 4, 9, 16, 25]

# filter - keep elements where function returns True
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4]

# reduce - accumulate result
product = reduce(lambda x, y: x * y, nums)
print(product)  # 120

# Custom higher-order function
def apply_to_each(func, iterable):
    return [func(item) for item in iterable]

def create_validator(min_val, max_val):
    def validator(value):
        return min_val <= value <= max_val
    return validator

is_valid_age = create_validator(0, 150)
print(is_valid_age(25))   # True
print(is_valid_age(200))  # False
```

---

### Q8: Explain recursion and its limitations in Python.

**Answer:**
Recursion is when a function calls itself. Python has a default recursion limit of 1000.

```python
import sys

# Basic recursion - factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Fibonacci (inefficient without memoization)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# With memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_memo(n):
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

# Tail recursion (Python doesn't optimize it)
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)

# Check recursion limit
print(sys.getrecursionlimit())  # 1000
sys.setrecursionlimit(2000)     # Increase if needed

# Convert recursion to iteration
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

---

### Q9: What is function overloading in Python?

**Answer:**
Python doesn't support traditional overloading but provides alternatives.

```python
# Using default arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Using *args and type checking
def add(*args):
    if len(args) == 2:
        return args[0] + args[1]
    elif len(args) == 3:
        return args[0] + args[1] + args[2]
    raise ValueError("Invalid number of arguments")

# Using functools.singledispatch (Python 3.4+)
from functools import singledispatch

@singledispatch
def process(value):
    raise TypeError(f"Cannot process {type(value)}")

@process.register(int)
def _(value):
    return value * 2

@process.register(str)
def _(value):
    return value.upper()

@process.register(list)
def _(value):
    return [process(item) for item in value]

print(process(5))          # 10
print(process("hello"))    # HELLO
print(process([1, "a"]))   # [2, 'A']
```

---

### Q10: Explain function annotations and type hints.

**Answer:**
Type hints document expected types without enforcing them (use mypy for enforcement).

```python
from typing import List, Dict, Optional, Union, Tuple

# Basic annotations
def greet(name: str, times: int = 1) -> str:
    return f"Hello {name}! " * times

# Complex types
def process_items(
    items: List[int],
    config: Dict[str, Union[int, str]],
    callback: Optional[callable] = None
) -> Tuple[List[int], int]:
    result = [x * 2 for x in items]
    if callback:
        result = callback(result)
    return result, len(result)

# New syntax (Python 3.9+)
def merge(
    dict1: dict[str, int],
    dict2: dict[str, int]
) -> dict[str, int]:
    return {**dict1, **dict2}

# Using TypeVar for generics
from typing import TypeVar, Sequence

T = TypeVar('T')

def first(items: Sequence[T]) -> T:
    return items[0]

# Type checking with mypy
# $ mypy script.py
```

---

### Q11: What are pure functions and side effects?

**Answer:**
Pure functions always return the same output for the same input and don't modify external state. Side effects include modifying globals, I/O operations, etc.

```python
# Pure function
def add(a: int, b: int) -> int:
    return a + b

# Function with side effects
total = 0
def add_to_total(value):
    global total
    total += value  # Modifies external state
    return total

# Avoiding side effects
def calculate_discount(price: float, discount: float) -> float:
    return price * (1 - discount)

# Instead of
class ShoppingCart:
    def __init__(self):
        self.total = 0
    
    def add_item(self, price):
        self.total += price  # Side effect: modifies state
```

---

### Q12: Explain the nonlocal keyword.

**Answer:**
`nonlocal` allows modifying variables in the enclosing (but not global) scope.

```python
def outer():
    count = 0
    
    def inner():
        nonlocal count
        count += 1
        return count
    
    return inner

counter = outer()
print(counter())  # 1
print(counter())  # 2

# Without nonlocal, this would fail
def outer_bad():
    count = 0
    
    def inner_bad():
        # count += 1  # UnboundLocalError
        count = count + 1  # Creates local variable
        return count
    
    return inner_bad

# Practical example: running average
def make_averager():
    values = []
    
    def averager(new_value):
        values.append(new_value)
        return sum(values) / len(values)
    
    return averager

avg = make_averager()
print(avg(10))  # 10.0
print(avg(20))  # 15.0
print(avg(30))  # 20.0
```

---

### Q13: How do you create function aliases and partial functions?

**Answer:**
Functions are first-class objects, so you can assign them to variables and create partials.

```python
from functools import partial

# Function alias
def greet(name):
    return f"Hello, {name}!"

hello = greet  # Alias
print(hello("Alice"))

# Partial functions
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Partial with built-in functions
from operator import mul

double = partial(mul, 2)
print(double(5))  # 10

# Practical example
def connect(host, port, protocol):
    return f"Connecting to {protocol}://{host}:{port}"

http_connect = partial(connect, protocol="http")
print(http_connect("localhost", 8080))  # http://localhost:8080
```

---

### Q14: Explain generator functions and expressions.

**Answer:**
Generators produce values lazily using `yield` instead of `return`. They're memory-efficient for large sequences.

```python
# Generator function
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num, end=" ")  # 1 2 3 4 5

# Generator expression
squares = (x**2 for x in range(1000000))
print(sum(squares))  # Memory efficient

# Generator pipeline
def read_large_file(path):
    with open(path, 'r') as f:
        for line in f:
            yield line.strip()

def filter_lines(lines, pattern):
    for line in lines:
        if pattern in line:
            yield line

# Chain of generators
lines = read_large_file("large.txt")
matches = filter_lines(lines, "error")
for match in matches:
    print(match)

# yield from - delegating to sub-generator
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
```

---

### Q15: What are function scopes and the LEGB rule?

**Answer:**
Python follows LEGB: Local, Enclosing, Global, Built-in scopes.

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)      # local
    
    inner()
    print(x)          # enclosing

outer()
print(x)              # global

# Built-in scope
print = lambda x: x  # Shadows built-in
# Don't do this! Use a different name

# Built-in functions
import builtins
print(dir(builtins))  # List all built-ins

# Global keyword
def modify_global():
    global x
    x = "modified"

# nonlocal keyword
def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = "modified"
    inner()
    print(x)  # modified
```

---

## Coding Challenges

### Challenge 1: Implement Memoization Decorator

**Problem:** Create a decorator that caches function results.

**Solution:**
```python
import functools

def memoize(func):
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    wrapper.cache = cache
    wrapper.cache_info = lambda: {"size": len(cache)}
    wrapper.cache_clear = lambda: cache.clear()
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test
print(fibonacci(50))  # Fast!
print(fibonacci.cache_info())

# Alternative using lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)
```

---

### Challenge 2: Implement a Retry Decorator

**Problem:** Create a decorator that retries failed function calls.

**Solution:**
```python
import functools
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1, exceptions=(ValueError, ConnectionError))
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("API unavailable")
    return "Success!"

# Test
try:
    result = unreliable_api_call()
    print(result)
except ConnectionError as e:
    print(f"Failed after retries: {e}")
```

---

### Challenge 3: Implement a Function Timer

**Problem:** Create a decorator that measures and logs function execution time.

**Solution:**
```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        
        # Format duration
        if duration < 0.001:
            formatted = f"{duration * 1000000:.2f}µs"
        elif duration < 1:
            formatted = f"{duration * 1000:.2f}ms"
        else:
            formatted = f"{duration:.2f}s"
        
        print(f"{func.__name__} took {formatted}")
        return result
    
    wrapper.timings = []
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)
    return "Done"

# Test
slow_function()

# More advanced: accumulate timings
def timer_stats(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        if not hasattr(wrapper, 'stats'):
            wrapper.stats = {'count': 0, 'total': 0, 'min': float('inf'), 'max': 0}
        
        wrapper.stats['count'] += 1
        wrapper.stats['total'] += duration
        wrapper.stats['min'] = min(wrapper.stats['min'], duration)
        wrapper.stats['max'] = max(wrapper.stats['max'], duration)
        
        return result
    return wrapper
```

---

### Challenge 4: Implement a Throttle Decorator

**Problem:** Create a decorator that limits function calls to once every N seconds.

**Solution:**
```python
import functools
import time

def throttle(interval):
    def decorator(func):
        last_called = [0]
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= interval:
                last_called[0] = now
                return func(*args, **kwargs)
            else:
                print(f"Throttled: {func.__name__} called too soon")
                return None
        return wrapper
    return decorator

@throttle(interval=1)
def api_call():
    print("API called")
    return "response"

# Test
api_call()  # API called
time.sleep(0.5)
api_call()  # Throttled: api_call called too soon
time.sleep(1)
api_call()  # API called
```

---

### Challenge 5: Implement a Function Pipeline

**Problem:** Create a function that chains multiple functions together.

**Solution:**
```python
def pipeline(*functions):
    def wrapper(value):
        result = value
        for func in functions:
            result = func(result)
        return result
    return wrapper

# Alternative with reduce
from functools import reduce

def pipeline_reduce(*functions):
    def wrapper(value):
        return reduce(lambda v, f: f(v), functions, value)
    return wrapper

# Test
def double(x):
    return x * 2

def add_one(x):
    return x + 1

def square(x):
    return x ** 2

transform = pipeline(double, add_one, square)
print(transform(3))  # (3 * 2 + 1)^2 = 49

# Practical example: data processing
clean_text = pipeline(
    str.strip,
    str.lower,
    lambda s: s.replace("-", " "),
    str.title
)
print(clean_text("  hello-world  "))  # "Hello World"
```

---

### Challenge 6: Implement a Debounce Decorator

**Problem:** Create a decorator that delays execution until calls stop for N seconds.

**Solution:**
```python
import functools
import time
import threading

def debounce(interval):
    def decorator(func):
        timer = None
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timer
            
            if timer is not None:
                timer.cancel()
            
            def call_func():
                func(*args, **kwargs)
            
            timer = threading.Timer(interval, call_func)
            timer.start()
        
        wrapper.cancel = lambda: timer.cancel() if timer else None
        return wrapper
    return decorator

@debounce(interval=0.5)
def search(query):
    print(f"Searching for: {query}")

# Test
search("a")
search("ap")
search("app")
search("appl")
# Only executes once after 0.5s of no calls
```

---

### Challenge 7: Implement a Cache with TTL

**Problem:** Create a memoization decorator with time-to-live expiration.

**Solution:**
```python
import functools
import time

def memoize_with_ttl(ttl_seconds):
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return result
            
            result = func(*args)
            cache[args] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {
            "size": len(cache),
            "entries": list(cache.keys())
        }
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=5)
def expensive_calculation(n):
    print(f"Computing {n}...")
    return n ** 2

# Test
print(expensive_calculation(5))  # Computes
print(expensive_calculation(5))  # Cached
time.sleep(6)
print(expensive_calculation(5))  # Computes again
```

---

### Challenge 8: Implement Function Composition

**Problem:** Create a compose function that combines multiple functions right-to-left.

**Solution:**
```python
from functools import reduce

def compose(*functions):
    def wrapper(value):
        return reduce(lambda v, f: f(v), reversed(functions), value)
    return wrapper

# Pipe (left-to-right)
def pipe(*functions):
    def wrapper(value):
        return reduce(lambda v, f: f(v), functions, value)
    return wrapper

# Test
def add_one(x):
    return x + 1

def double(x):
    return x * 2

def square(x):
    return x ** 2

# Compose: right to left
transform = compose(square, double, add_one)
print(transform(3))  # square(double(add_one(3))) = square(double(4)) = square(8) = 64

# Pipe: left to right
transform_pipe = pipe(add_one, double, square)
print(transform_pipe(3))  # square(double(add_one(3))) = 64

# Practical example
clean_email = compose(
    str.lower,
    str.strip,
    lambda email: email.split("@")[0]
)
print(clean_email("  Alice@Example.com  "))  # "alice"
```

---

## Common Follow-up Questions

1. **"When would you use a lambda vs a regular function?"**
   - Lambda: short, simple, one-time use (sorting keys, callbacks)
   - Regular function: complex logic, reusable, needs docstring

2. **"How do decorators affect function performance?"**
   - Add slight overhead due to wrapper function
   - Can improve performance if caching or throttling
   - Profile before optimizing

3. **"Explain the difference between `return` and `yield`"**
   - `return` sends a value and exits the function
   - `yield` produces a value but pauses execution, maintaining state

4. **"When would you use recursion vs iteration?"**
   - Recursion: naturally recursive problems (trees, divide-and-conquer)
   - Iteration: simple loops, performance-critical code, deep recursion

5. **"How do you handle functions with many parameters?"**
   - Use dataclasses or named tuples
   - Configuration objects
   - Builder pattern
   - **kwargs with validation

---

## Tips for Answering

1. **Understand first-class functions** - Functions are objects; they can be passed around
2. **Know the closures mechanism** - How variables are captured from enclosing scope
3. **Practice decorators** - Both simple and parameterized versions
4. **Be aware of mutable default pitfalls** - Common interview gotcha
5. **Understand scope rules** - LEGB, global, nonlocal
6. **Know built-in functions** - map, filter, reduce, zip, enumerate
7. **Practice type hints** - Modern Python best practice
8. **Understand generators** - yield, yield from, generator expressions
9. **Be familiar with functools** - partial, lru_cache, wraps
10. **Think about testability** - Pure functions are easier to test

---

## Key Concepts to Review

| Concept | Key Points |
|---------|-----------|
| Arguments | Positional, keyword, *args, **kwargs |
| Default Arguments | Avoid mutable defaults (use None) |
| Closures | Remember enclosing scope variables |
| Decorators | Higher-order functions, @syntax |
| Lambda | Anonymous, single-expression, limited |
| Recursion | Self-calling, needs base case, depth limit |
| Generators | yield, lazy evaluation, memory efficient |
| Higher-Order | Functions as arguments/returns |
| Scope | LEGB rule, global, nonlocal |
| Type Hints | Documentation, static analysis |

---

*Functions are the building blocks of Python programs. Master these concepts to write clean, efficient, and maintainable code!*