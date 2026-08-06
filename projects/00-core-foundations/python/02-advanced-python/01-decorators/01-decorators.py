"""
Decorators - Advanced Python Exercises
======================================
Decorators are functions that modify other functions or classes.
They are a powerful tool for code reuse and separation of concerns.
"""

import functools
import time
from typing import Any, Callable


# =============================================================================
# 1. Basic Decorators
# =============================================================================

def timer(func: Callable) -> Callable:
    """Measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] executed in {elapsed:.6f}s")
        return result
    return wrapper


def log_calls(func: Callable) -> Callable:
    """Log function calls with arguments."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join([repr(a) for a in args])
        kwargs_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"  Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result
    return wrapper


# =============================================================================
# 2. Decorators with Arguments
# =============================================================================

def retry(max_attempts: int = 3, delay: float = 0.1):
    """Retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def cache(max_size: int = 128):
    """Simple memoization decorator with max size."""
    def decorator(func: Callable) -> Callable:
        cache_dict: dict = {}
        cache_order: list = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in cache_dict:
                return cache_dict[args]
            result = func(*args)
            if len(cache_dict) >= max_size:
                oldest = cache_order.pop(0)
                del cache_dict[oldest]
            cache_dict[args] = result
            cache_order.append(args)
            return result
        wrapper.cache_info = lambda: {"size": len(cache_dict), "max_size": max_size}
        wrapper.cache_clear = lambda: (cache_dict.clear(), cache_order.clear())
        return wrapper
    return decorator


# =============================================================================
# 3. Class Decorators
# =============================================================================

def singleton(cls):
    """Make a class a singleton."""
    instances = {}
    @functools.wraps(cls, updated=[])
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def add_repr(cls):
    """Add __repr__ to a class."""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls


# =============================================================================
# 4. Stacking Decorators
# =============================================================================

def bold(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper


def italic(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"*{func(*args, **kwargs)}*"
    return wrapper


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DECORATORS DEMO")
    print("=" * 60)

    # 1. Basic decorator
    print("\n--- Basic Decorators ---")

    @timer
    @log_calls
    def slow_add(a: int, b: int) -> int:
        time.sleep(0.01)
        return a + b

    result = slow_add(3, 5)
    print(f"  Result: {result}")
    print(f"  Function name preserved: {slow_add.__name__}")

    # 2. Decorators with arguments
    print("\n--- Retry Decorator ---")

    counter = {"value": 0}

    @retry(max_attempts=3, delay=0.01)
    def flaky_function():
        counter["value"] += 1
        if counter["value"] < 3:
            raise ValueError("Not ready yet")
        return "Success!"

    result = flaky_function()
    print(f"  Result: {result}")

    # 3. Cache decorator
    print("\n--- Cache Decorator ---")

    call_count = {"n": 0}

    @cache(max_size=10)
    def fibonacci(n: int) -> int:
        call_count["n"] += 1
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(f"  fib(10) = {fibonacci(10)}")
    print(f"  Actual calls: {call_count['n']} (with caching)")
    print(f"  Cache info: {fibonacci.cache_info()}")

    # 4. Singleton decorator
    print("\n--- Singleton Decorator ---")

    @singleton
    class DatabaseConnection:
        def __init__(self):
            self.id = id(self)

    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"  Same instance: {db1 is db2}")
    print(f"  db1.id == db2.id: {db1.id == db2.id}")

    # 5. Stacked decorators
    print("\n--- Stacked Decorators ---")

    @bold
    @italic
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(f"  {greet('World')}")

    # 6. Add repr decorator
    print("\n--- Class Decorator (add_repr) ---")

    @add_repr
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Point(3, 4)
    print(f"  {p}")

    print("\n" + "=" * 60)
    print("All decorator demos complete!")
    print("=" * 60)
