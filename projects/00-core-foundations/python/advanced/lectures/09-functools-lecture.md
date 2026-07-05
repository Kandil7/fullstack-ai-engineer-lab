# Advanced Python Lecture 09: functools

## Topic Overview

The `functools` module provides higher-order functions that operate on other functions and callable objects. It offers powerful tools for caching, partial application, wrapping, and reducing — essential utilities for writing clean, efficient, and maintainable Python code. Understanding `functools` is crucial for mastering decorators, optimizing performance, and implementing functional programming patterns.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `functools.partial` to create specialized functions
2. Implement caching with `functools.lru_cache` and `functools.cache`
3. Apply `functools.wraps` to preserve function metadata
4. Use `functools.reduce` for cumulative operations
5. Implement ordering with `functools.total_ordering`
6. Use `functools.singledispatch` for function overloading
7. Apply `functools.cached_property` for lazy computation
8. Use `functools.update_wrapper` for wrapper functions
9. Apply functools in AI engineering patterns
10. Follow best practices for functools usage

---

## 1. `functools.partial`

### Basic Usage

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Partial with positional arguments
def greet(greeting, name):
    return f"{greeting}, {name}!"

say_hello = partial(greet, "Hello")
say_hi = partial(greet, "Hi")

print(say_hello("Alice"))  # "Hello, Alice!"
print(say_hi("Bob"))       # "Hi, Bob!"
```

### Partial in Higher-Order Functions

```python
from functools import partial
from typing import Callable

def apply_operation(func: Callable, value: int, operation: Callable) -> int:
    return operation(func(value))

# Using partial to specialize
double = partial(lambda x: x * 2)
add_ten = partial(lambda x: x + 10)

result = apply_operation(double, 5, add_ten)
print(result)  # 20 (double(5) = 10, then +10 = 20)
```

### Partial for Callbacks

```python
from functools import partial

def log_event(event_type, message, timestamp=None):
    print(f"[{event_type}] {message} at {timestamp}")

# Specialized loggers
log_error = partial(log_event, "ERROR")
log_warning = partial(log_event, "WARNING")
log_info = partial(log_event, "INFO")

log_error("Connection failed", timestamp="2024-01-01 10:00:00")
# [ERROR] Connection failed at 2024-01-01 10:00:00
```

---

## 2. `functools.lru_cache`

### Basic Caching

```python
import functools
import time

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# First call - computes and caches
start = time.perf_counter()
result = fibonacci(100)
elapsed = time.perf_counter() - start
print(f"First call: {result} in {elapsed:.4f}s")

# Second call - cached, instant
start = time.perf_counter()
result = fibonacci(100)
elapsed = time.perf_counter() - start
print(f"Second call: {result} in {elapsed:.6f}s")

# Cache statistics
print(fibonacci.cache_info())
# CacheInfo(hits=99, misses=101, maxsize=128, currsize=101)
```

### Cache Management

```python
import functools

@functools.lru_cache(maxsize=32)
def expensive_computation(n):
    print(f"Computing {n}...")
    return sum(i ** 2 for i in range(n))

# Clear cache
expensive_computation.cache_clear()

# Check cache info
info = expensive_computation.cache_info()
print(f"Cache size: {info.currsize}/{info.maxsize}")

# Decorate existing function
def my_function(x):
    return x * 2

cached_version = functools.lru_cache(maxsize=128)(my_function)
```

---

## 3. `functools.cache` (Python 3.9+)

```python
import functools

@functools.cache  # Unbounded cache (like lru_cache(maxsize=None))
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Same as lru_cache(maxsize=None)
result = fibonacci(100)
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=None, currsize=101)
```

---

## 4. `functools.wraps`

### Preserving Metadata

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

print(greet.__name__)  # "greet" (not "wrapper")
print(greet.__doc__)   # "Greet someone by name."
print(greet.__module__) # "__main__"
```

### Without `functools.wraps`

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring."""
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

print(greet.__name__)  # "wrapper" - lost original name!
print(greet.__doc__)   # "Wrapper docstring." - lost original docstring!
```

---

## 5. `functools.reduce`

### Basic Reduction

```python
from functools import reduce

# Sum a list
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 15

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, lst: acc + lst, nested, [])
print(flat)  # [1, 2, 3, 4, 5, 6]
```

### Reduce with Initial Value

```python
from functools import reduce

# Multiply with initial value
numbers = [1, 2, 3, 4]
product = reduce(lambda acc, x: acc * x, numbers, 1)
print(product)  # 24

# Build dictionary
pairs = [("a", 1), ("b", 2), ("c", 3)]
result = reduce(lambda d, pair: {**d, pair[0]: pair[1]}, pairs, {})
print(result)  # {"a": 1, "b": 2, "c": 3}
```

### Practical Examples

```python
from functools import reduce
from typing import Callable, Any

def compose(*functions: Callable) -> Callable:
    """Compose multiple functions into one."""
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), functions)

# Usage
def add_one(x): return x + 1
def double(x): return x * 2
def square(x): return x ** 2

composed = compose(square, double, add_one)
print(composed(3))  # square(double(add_one(3))) = square(double(4)) = square(8) = 64
```

---

## 6. `functools.total_ordering`

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

# Only need __eq__ and __lt__
# total_ordering adds: __le__, __gt__, __ge__

alice = Student("Alice", 95)
bob = Student("Bob", 87)

print(alice > bob)    # True
print(alice >= bob)   # True
print(alice <= bob)   # False
print(alice < bob)    # False
print(alice == bob)   # False
print(alice != bob)   # True
```

---

## 7. `functools.singledispatch`

```python
from functools import singledispatch

@singledispatch
def process(value):
    raise NotImplementedError(f"Cannot process {type(value)}")

@process.register(int)
def process_int(value):
    return value * 2

@process.register(str)
def process_str(value):
    return value.upper()

@process.register(list)
def process_list(value):
    return [process(item) for item in value]

# Usage
print(process(5))        # 10
print(process("hello")) # "HELLO"
print(process([1, "two", 3]))  # [2, "TWO", 6]
```

### SingleDispatch with Type Hints

```python
from functools import singledispatch
from typing import Union

@singledispatch
def serialize(value) -> str:
    raise TypeError(f"Cannot serialize {type(value)}")

@serialize.register
def _(value: int) -> str:
    return f"INT:{value}"

@serialize.register
def _(value: str) -> str:
    return f"STR:{value}"

@serialize.register
def _(value: dict) -> str:
    return f"DICT:{value}"

print(serialize(42))      # "INT:42"
print(serialize("hello")) # "STR:hello"
print(serialize({"a": 1})) # "DICT:{'a': 1}"
```

---

## 8. `functools.cached_property`

```python
from functools import cached_property
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @cached_property
    def area(self):
        """Computed once, then cached."""
        print("Computing area...")
        return math.pi * self.radius ** 2
    
    @cached_property
    def circumference(self):
        print("Computing circumference...")
        return 2 * math.pi * self.radius

c = Circle(5)
print(c.area)           # "Computing area..." -> 78.54
print(c.area)           # 78.54 (cached, no computation)
print(c.circumference)  # "Computing circumference..." -> 31.42
print(c.circumference)  # 31.42 (cached)

# Cache is instance-specific
c2 = Circle(10)
print(c2.area)  # "Computing area..." -> 314.16
```

### Cached Property with Invalidation

```python
from functools import cached_property

class DataProcessor:
    def __init__(self, data):
        self._data = data
        self._dirty = True
    
    @cached_property
    def processed_data(self):
        print("Processing data...")
        self._dirty = False
        return [x ** 2 for x in self._data]
    
    def invalidate(self):
        """Manually invalidate cache."""
        if "processed_data" in self.__dict__:
            del self.__dict__["processed_data"]
        self._dirty = True

processor = DataProcessor([1, 2, 3])
print(processor.processed_data)  # [1, 4, 9]
processor.invalidate()
print(processor.processed_data)  # Re-computes
```

---

## 9. `functools.update_wrapper`

```python
import functools

def my_wrapper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Copy metadata from func to wrapper
    functools.update_wrapper(wrapper, func)
    return wrapper

# Equivalent to @functools.wraps
@my_wrapper
def greet(name):
    return f"Hello, {name}!"

print(greet.__name__)  # "greet"
```

---

## 10. `functools.partialmethod`

```python
from functools import partialmethod

class Cell:
    def __init__(self):
        self._alive = False
    
    def set_state(self, state):
        self._alive = state
    
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

cell = Cell()
cell.set_alive()
print(cell._alive)  # True

cell.set_dead()
print(cell._alive)  # False
```

---

## 11. functools in AI Engineering

### Cached Model Predictions

```python
import functools
from typing import Hashable

def cached_prediction(model_name: str):
    """Decorator that caches model predictions."""
    def decorator(func):
        @functools.lru_cache(maxsize=1000)
        def wrapper(input_hash: Hashable):
            return func(input_hash)
        
        wrapper.cache_info = functools.wraps(func)(wrapper).cache_info
        return wrapper
    return decorator

@cached_prediction("gpt-4")
def predict(text_hash: int):
    # Expensive API call or model inference
    return f"Prediction for {text_hash}"
```

### Partial for Configuration

```python
from functools import partial

def train_model(data, model, learning_rate, epochs):
    print(f"Training {model} for {epochs} epochs at lr={learning_rate}")
    return {"model": model, "epochs": epochs}

# Specialized trainers
train_bert = partial(train_model, model="bert", learning_rate=2e-5, epochs=10)
train_gpt = partial(train_model, model="gpt", learning_rate=1e-5, epochs=5)

train_bert(data)  # Uses bert config
train_gpt(data)   # Uses gpt config
```

### Reduce for Pipeline

```python
from functools import reduce

def pipeline(*steps):
    """Create a data processing pipeline."""
    def process(data):
        return reduce(lambda d, step: step(d), steps, data)
    return process

# Define steps
def validate(data):
    return [d for d in data if d.get("valid")]

def transform(data):
    return [{**d, "processed": True} for d in data]

def aggregate(data):
    return {"count": len(data), "items": data}

# Create pipeline
process = pipeline(validate, transform, aggregate)
result = process([{"valid": True}, {"valid": False}, {"valid": True}])
print(result)  # {'count': 2, 'items': [...]}
```

---

## 12. Best Practices

1. **Use `lru_cache`** for expensive computations with hashable arguments
2. **Use `cache`** (3.9+) for unbounded caching
3. **Always use `functools.wraps`** in decorators
4. **Use `partial`** to create specialized functions from general ones
5. **Use `reduce`** for cumulative operations (but consider readability)
6. **Use `total_ordering`** to reduce comparison method boilerplate
7. **Use `singledispatch`** for type-based function overloading
8. **Use `cached_property`** for expensive computed properties
9. **Clear caches** when data changes
10. **Profile before caching** — overhead may not always be worth it

---

## 13. Practice Exercises

### Exercise 1: Partial Application
Create specialized functions using `partial`:

```python
def log(level, module, message):
    print(f"[{level}] {module}: {message}")

# Create specialized loggers
log_error = ...  # Partial for ERROR level
log_auth = ...   # Partial for auth module
```

### Exercise 2: LRU Cache with TTL
Implement a custom cache decorator with time-to-live:

```python
def ttl_cache(ttl_seconds=300):
    # Cache entries expire after ttl_seconds
    pass
```

### Exercise 3: Compose Function
Implement function composition using `reduce`:

```python
def compose(*funcs):
    # Return a function that applies all funcs right-to-left
    pass
```

### Exercise 4: Singledispatch Serializer
Create a type-based serializer:

```python
@singledispatch
def serialize(value):
    pass

# Support: int, str, list, dict, datetime
```

---

## 14. Summary

| Function | Description |
|----------|-------------|
| **`partial`** | Create specialized functions with preset arguments |
| **`lru_cache`** | Cache with least-recently-used eviction |
| **`cache`** | Unbounded cache (Python 3.9+) |
| **`wraps`** | Preserve function metadata in decorators |
| **`update_wrapper`** | Copy metadata between functions |
| **`reduce`** | Cumulative operation on iterable |
| **`total_ordering`** | Auto-generate comparison methods |
| **`singledispatch`** | Type-based function overloading |
| **`cached_property`** | Lazy computed property with caching |
| **`partialmethod`** | Partial for methods |

The `functools` module is a cornerstone of Python's functional programming capabilities. Mastering these tools enables writing more concise, efficient, and maintainable code — essential for AI engineering workflows where performance and clarity are paramount.

---

## Next Steps

In the final lecture, we'll explore **itertools**, which complements `functools` with powerful iterator utilities.
