# functools Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| `functools` | Module for higher-order functions on callables |
| `partial` | Create specialized function with preset arguments |
| `partialmethod` | Partial for class methods |
| `lru_cache` | Least-recently-used cache decorator |
| `cache` | Unbounded cache decorator (Python 3.9+) |
| `wraps` | Preserve function metadata in decorators |
| `update_wrapper` | Copy metadata from one function to another |
| `reduce` | Cumulative function application on iterable |
| `total_ordering` | Auto-generate comparison methods |
| `singledispatch` | Type-based function overloading |
| `cached_property` | Lazy computed property with caching |
| `CacheInfo` | Named tuple with cache statistics |
| Function Composition | Combining functions into one |
| Memoization | Caching function results |
| Higher-Order Function | Function that takes/returns functions |
| Partial Application | Fixing some function arguments |
| LRU Eviction | Removing least recently used items |
| Cache Invalidation | Clearing expired cached values |
| Decorator | Function that modifies other functions |
| Wrapper | Inner function in a decorator |

---

## Detailed Definitions

### Cache Invalidation

**Definition**: The process of removing stale or expired entries from a cache. With `lru_cache`, use `cache_clear()` to manually invalidate.

**Example**:
```python
import functools

@functools.lru_cache(maxsize=128)
def compute(x):
    return x ** 2

compute(5)  # Cached
compute.cache_clear()  # Invalidate all entries
compute(5)  # Re-computes
```

**Related**: `lru_cache`, `cache_clear()`, Cache Management

---

### `cache_clear()`

**Definition**: A method on `lru_cache`-wrapped functions that removes all cached entries.

**Example**：
```python
import functools

@functools.lru_cache
def expensive(n):
    print(f"Computing {n}")
    return sum(range(n))

expensive(1000)  # "Computing 1000"
expensive(1000)  # (cached, no print)

expensive.cache_clear()
expensive(1000)  # "Computing 1000" (re-computed)
```

**Related**: `lru_cache`, Cache Management, Invalidation

---

### `cache_info()`

**Definition**: A method on `lru_cache`-wrapped functions that returns cache statistics as a `CacheInfo` named tuple.

**Example**:
```python
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(10)
info = fibonacci.cache_info()
print(info)
# CacheInfo(hits=8, misses=11, maxsize=128, currsize=11)

print(f"Hits: {info.hits}, Misses: {info.misses}")
```

**Related**: `lru_cache`, `CacheInfo`, Performance Monitoring

---

### `CacheInfo`

**Definition**: A named tuple returned by `cache_info()` containing cache statistics: `hits`, `misses`, `maxsize`, and `currsize`.

**Example**：
```python
import functools

@functools.lru_cache(maxsize=100)
def process(x):
    return x * 2

process(1)
process(2)
process(1)  # Cache hit

info = process.cache_info()
print(info.hits)     # 1
print(info.misses)   # 2
print(info.maxsize)  # 100
print(info.currsize) # 2
```

**Related**: `cache_info()`, `lru_cache`, Statistics

---

### Function Composition

**Definition**: Combining multiple functions into a single function where the output of one becomes the input of the next.

**Example**：
```python
from functools import reduce

def compose(*functions):
    """Compose functions right-to-left."""
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), functions)

def add_one(x): return x + 1
def double(x): return x * 2
def square(x): return x ** 2

# square(double(add_one(x)))
transform = compose(square, double, add_one)
print(transform(3))  # square(double(add_one(3))) = square(double(4)) = square(8) = 64
```

**Related**: `reduce`, Higher-Order Functions, Pipelines

---

### Decorator

**Definition**: A higher-order function that wraps another function to extend its behavior. `functools.wraps` preserves metadata in decorators.

**Example**：
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
    time.sleep(0.1)

slow_function()  # "slow_function took 0.1012s"
```

**Related**: `functools.wraps`, Higher-Order Function

---

### Higher-Order Function

**Definition**: A function that takes one or more functions as arguments, or returns a function as a result. `functools` provides many higher-order functions.

**Example**：
```python
from functools import partial

def apply(func, value):
    return func(value)

# partial is a higher-order function
double = partial(lambda x: x * 2)
print(apply(double, 5))  # 10

# reduce is a higher-order function
from functools import reduce
total = reduce(lambda a, b: a + b, [1, 2, 3, 4])
print(total)  # 10
```

**Related**: `partial`, `reduce`, Functional Programming

---

### LRU Eviction

**Definition**: Least Recently Used eviction — a cache strategy that removes the least recently accessed entries when the cache is full.

**Example**：
```python
import functools

@functools.lru_cache(maxsize=3)
def process(x):
    return x * 2

process(1)  # Cache: {1: 2}
process(2)  # Cache: {1: 2, 2: 4}
process(3)  # Cache: {1: 2, 2: 4, 3: 6}
process(4)  # Evicts 1, Cache: {2: 4, 3: 6, 4: 8}
process(1)  # Cache miss - re-computes
```

**Related**: `lru_cache`, Cache Management, Eviction Policy

---

### `lru_cache`

**Definition**: A decorator that caches function results with least-recently-used eviction. Optional `maxsize` parameter limits cache size.

**Example**：
```python
import functools

@functools.lru_cache(maxsize=256)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without cache: O(2^n) time
# With cache: O(n) time
print(fibonacci(100))  # Instant result

# Cache with unlimited size
@functools.lru_cache(maxsize=None)
def unlimited_cache(x):
    return x ** 2
```

**Related**: `cache`, Memoization, Cache Management

---

### `cache`

**Definition**: A decorator (Python 3.9+) providing unbounded caching, equivalent to `lru_cache(maxsize=None)`.

**Example**：
```python
import functools

@functools.cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# No size limit
print(fibonacci(1000))  # Works with large values

# Same interface as lru_cache
print(fibonacci.cache_info())
fibonacci.cache_clear()
```

**Related**: `lru_cache`, Memoization, Unbounded Cache

---

### Memoization

**Definition**: An optimization technique caching function results based on arguments, avoiding redundant computation. Implemented by `lru_cache` and `cache`.

**Example**：
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

# Built-in memoization
@functools.lru_cache
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)
```

**Related**: `lru_cache`, `cache`, Performance Optimization

---

### `partial`

**Definition**: A function that creates a new function with some arguments pre-filled, reducing the number of arguments needed at call time.

**Example**：
```python
from functools import partial

def greet(greeting, name):
    return f"{greeting}, {name}!"

# Create specialized functions
say_hello = partial(greet, "Hello")
say_hi = partial(greet, "Hi")

print(say_hello("Alice"))  # "Hello, Alice!"
print(say_hi("Bob"))       # "Hi, Bob!"

# With keyword arguments
def connect(host, port, database):
    return f"Connecting to {host}:{port}/{database}"

connect_db = partial(connect, database="mydb")
print(connect_db("localhost", 5432))  # "Connecting to localhost:5432/mydb"
```

**Related**: Partial Application, Currying, Function Specialization

---

### `partialmethod`

**Definition**: Like `partial`, but for class methods. Creates a new method with some arguments pre-filled.

**Example**：
```python
from functools import partialmethod

class Cell:
    def __init__(self):
        self._state = False
    
    def set_state(self, state):
        self._state = state
    
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

cell = Cell()
cell.set_alive()
print(cell._state)  # True

cell.set_dead()
print(cell._state)  # False
```

**Related**: `partial`, Class Methods, Method Specialization

---

### `reduce`

**Definition**: A function that cumulatively applies a function to an iterable, reducing it to a single value.

**Example**：
```python
from functools import reduce

# Sum
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)
print(total)  # 15

# Product
product = reduce(lambda a, b: a * b, numbers)
print(product)  # 120

# With initial value
total = reduce(lambda a, b: a + b, numbers, 100)
print(total)  # 115
```

**Related**: Function Composition, Accumulation, Iterable Processing

---

### `singledispatch`

**Definition**: A decorator that implements function overloading based on the type of the first argument.

**Example**：
```python
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

print(process(5))        # 10
print(process("hello")) # "HELLO"
print(process([1, "two", 3]))  # [2, "TWO", 6]
```

**Related**: Function Overloading, Type Dispatch

---

### `singledispatchmethod`

**Definition**: A version of `singledispatch` for instance methods, dispatching on the type of the second argument (self is first).

**Example**：
```python
from functools import singledispatchmethod

class Processor:
    @singledispatchmethod
    def process(self, value):
        raise TypeError(f"Cannot process {type(value)}")
    
    @process.register(int)
    def _(self, value):
        return value * 2
    
    @process.register(str)
    def _(self, value):
        return value.upper()

p = Processor()
print(p.process(5))      # 10
print(p.process("hello"))  # "HELLO"
```

**Related**: `singledispatch`, Method Dispatch

---

### `total_ordering`

**Definition**: A class decorator that auto-generates missing comparison methods (`__lt__`, `__le__`, `__gt__`, `__ge__`) from `__eq__` and one other comparison method.

**Example**：
```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade

alice = Student("Alice", 95)
bob = Student("Bob", 87)

# All comparisons work
print(alice > bob)    # True
print(alice >= bob)   # True
print(alice <= bob)   # False
print(alice < bob)    # False
```

**Related**: Comparison Operators, `__lt__`, `__eq__`

---

### `update_wrapper`

**Definition**: A function that copies metadata from one function to another, used as a building block for `functools.wraps`.

**Example**：
```python
import functools

def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Equivalent to @functools.wraps
    functools.update_wrapper(wrapper, func)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)  # "greet"
print(greet.__doc__)   # "Greet someone."
```

**Related**: `functools.wraps`, Metadata Preservation

---

### `wraps`

**Definition**: A decorator that copies the metadata (`__name__`, `__doc__`, `__module__`, `__wrapped__`, etc.) from the original function to the wrapper function.

**Example**：
```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring (ignored)."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

print(greet.__name__)      # "greet" (preserved)
print(greet.__doc__)       # "Greet someone by name." (preserved)
print(greet.__wrapped__)   # Original unwrapped function
```

**Related**: `update_wrapper`, Decorator, Metadata

---

### Wrapper

**Definition**: The inner function returned by a decorator that surrounds the original function with additional behavior.

**Example**：
```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # <-- This is the wrapper
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
    time.sleep(0.1)

slow_function()  # wrapper executes, calls func
```

**Related**: Decorator, `functools.wraps`, Closure

---

### `cached_property`

**Definition**: A descriptor that converts a method into a lazy property, computing the value once and caching it as an instance attribute.

**Example**：
```python
from functools import cached_property

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    @cached_property
    def statistics(self):
        """Compute once, cache forever."""
        print("Computing statistics...")
        return {
            "mean": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data),
        }

analyzer = DataAnalyzer([1, 2, 3, 4, 5])
print(analyzer.statistics)  # "Computing statistics..." -> dict
print(analyzer.statistics)  # Cached, no computation
```

**Related**: Property, Lazy Evaluation, Caching

---

### `partial` Application

**Definition**: The process of fixing some arguments of a function, producing a new function with smaller arity. `functools.partial` implements this.

**Example**：
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Partial application
square = partial(power, exponent=2)  # Fixes exponent
cube = partial(power, exponent=3)

print(square(5))  # 25 (5**2)
print(cube(5))    # 125 (5**3)

# Partial with multiple arguments
def log(level, module, message):
    print(f"[{level}] {module}: {message}")

log_error = partial(log, level="ERROR", module="auth")
log_error("Failed login")  # "[ERROR] auth: Failed login"
```

**Related**: `partial`, Currying, Function Specialization

---

### Performance Optimization

**Definition**: Using `functools` tools like `lru_cache` and `cached_property` to reduce computation time by avoiding redundant work.

**Example**：
```python
import functools

# Without cache: O(2^n) for naive fibonacci
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Now O(n) with cache
fibonacci(100)  # Instant

# Profile impact
import time
start = time.perf_counter()
fibonacci(200)
elapsed = time.perf_counter() - start
print(f"fibonacci(200): {elapsed:.6f}s")
```

**Related**: `lru_cache`, `cache`, Memoization

---
