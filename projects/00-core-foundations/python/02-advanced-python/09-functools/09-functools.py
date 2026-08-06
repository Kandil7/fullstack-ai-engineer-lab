"""
Functools - Advanced Python Exercises
======================================
functools provides higher-order functions and operations
on callable objects.
"""

from functools import reduce, partial, lru_cache, total_ordering, wraps, cached_property
from typing import Callable, Any
import time


# =============================================================================
# 1. reduce() - Apply Function Cumulatively
# =============================================================================

def demo_reduce():
    """Demonstrate functools.reduce."""
    # Sum of squares
    numbers = [1, 2, 3, 4, 5]
    sum_of_squares = reduce(lambda acc, x: acc + x ** 2, numbers, 0)
    print(f"  Sum of squares: {sum_of_squares}")

    # Find maximum
    maximum = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"  Maximum: {maximum}")

    # Flatten nested list
    nested = [[1, 2], [3, 4], [5, 6]]
    flat = reduce(lambda acc, lst: acc + lst, nested, [])
    print(f"  Flattened: {flat}")

    # String concatenation
    words = ["Python", "is", "awesome"]
    sentence = reduce(lambda a, b: f"{a} {b}", words)
    print(f"  Sentence: {sentence}")


# =============================================================================
# 2. partial() - Partial Function Application
# =============================================================================

def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent."""
    return base ** exponent


def demo_partial():
    """Demonstrate functools.partial."""
    # Create specialized functions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    print(f"  square(5) = {square(5)}")
    print(f"  cube(3) = {cube(3)}")

    # Partial with multiple arguments
    def multiply(a, b, c):
        return a * b * c

    double_and_triple = partial(multiply, 2, c=3)
    print(f"  double_and_triple(5) = {double_and_triple(5)}")

    # Using partial with map
    numbers = [1, 2, 3, 4, 5]
    doubled = list(map(partial(power, exponent=2), numbers))
    print(f"  Doubled: {doubled}")


# =============================================================================
# 3. lru_cache() - Memoization
# =============================================================================

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number with caching."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@lru_cache(maxsize=32)
def expensive_computation(x: int, y: int) -> int:
    """Simulate expensive computation."""
    time.sleep(0.001)  # Small delay to simulate work
    return x ** y


def demo_lru_cache():
    """Demonstrate lru_cache memoization."""
    # Fibonacci with caching
    start = time.perf_counter()
    result = fibonacci(30)
    elapsed = time.perf_counter() - start
    print(f"  fib(30) = {result} (cached: {elapsed:.4f}s)")

    # Cache info
    info = fibonacci.cache_info()
    print(f"  Cache info: hits={info.hits}, misses={info.misses}, currsize={info.currsize}")

    # Expensive computation
    start = time.perf_counter()
    expensive_computation(2, 10)
    first_time = time.perf_counter() - start

    start = time.perf_counter()
    expensive_computation(2, 10)
    second_time = time.perf_counter() - start

    print(f"  First call: {first_time:.4f}s")
    print(f"  Second call (cached): {second_time:.6f}s")


# =============================================================================
# 4. total_ordering - Comparison Decorator
# =============================================================================

@total_ordering
class Temperature:
    """Temperature class with automatic comparison methods."""

    def __init__(self, celsius: float):
        self.celsius = celsius

    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius

    def __lt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius

    def __repr__(self):
        return f"Temperature({self.celsius}°C)"


def demo_total_ordering():
    """Demonstrate total_ordering decorator."""
    t1 = Temperature(20)
    t2 = Temperature(30)
    t3 = Temperature(20)

    print(f"  {t1} == {t3}: {t1 == t3}")
    print(f"  {t1} < {t2}: {t1 < t2}")
    print(f"  {t1} <= {t3}: {t1 <= t3}")
    print(f"  {t2} > {t1}: {t2 > t1}")
    print(f"  {t2} >= {t1}: {t2 >= t1}")

    temps = [Temperature(30), Temperature(10), Temperature(20)]
    temps.sort()
    print(f"  Sorted: {temps}")


# =============================================================================
# 5. wraps() - Preserve Function Metadata
# =============================================================================

def log_execution(func: Callable) -> Callable:
    """Decorator that logs function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result}")
        return result
    return wrapper


def demo_wraps():
    """Demonstrate wraps decorator."""
    @log_execution
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    print(f"  Function name: {add.__name__}")
    print(f"  Function doc: {add.__doc__}")
    result = add(3, 5)


# =============================================================================
# 6. cached_property - Cached Instance Attribute
# =============================================================================

class DataProcessor:
    """Example using cached_property."""

    def __init__(self, data: list):
        self._data = data

    @cached_property
    def statistics(self) -> dict:
        """Compute statistics once and cache."""
        print("  Computing statistics...")
        return {
            "count": len(self._data),
            "sum": sum(self._data),
            "mean": sum(self._data) / len(self._data),
            "min": min(self._data),
            "max": max(self._data),
        }


def demo_cached_property():
    """Demonstrate cached_property."""
    processor = DataProcessor([1, 2, 3, 4, 5])

    print("  First access:")
    stats = processor.statistics
    print(f"  Stats: {stats}")

    print("  Second access (cached):")
    stats = processor.statistics  # No "Computing..." message
    print(f"  Stats: {stats}")


# =============================================================================
# 7. Function Composition
# =============================================================================

def compose(*functions: Callable) -> Callable:
    """Compose multiple functions into one."""
    def composed(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


def demo_composition():
    """Demonstrate function composition."""
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    square = lambda x: x ** 2

    # Compose: square(add_one(double(x)))
    transform = compose(square, add_one, double)
    result = transform(3)  # square(add_one(double(3))) = square(add_one(6)) = square(7) = 49
    print(f"  compose(square, add_one, double)(3) = {result}")

    # String processing pipeline
    clean = lambda s: s.strip()
    lower = lambda s: s.lower()
    replace_spaces = lambda s: s.replace(" ", "_")

    process_text = compose(replace_spaces, lower, clean)
    result = process_text("  Hello World  ")
    print(f"  process_text('  Hello World  ') = {result}")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FUNCTOOLS DEMO")
    print("=" * 60)

    print("\n--- reduce() ---")
    demo_reduce()

    print("\n--- partial() ---")
    demo_partial()

    print("\n--- lru_cache() ---")
    demo_lru_cache()

    print("\n--- total_ordering ---")
    demo_total_ordering()

    print("\n--- wraps() ---")
    demo_wraps()

    print("\n--- cached_property ---")
    demo_cached_property()

    print("\n--- Function Composition ---")
    demo_composition()

    print("\n" + "=" * 60)
    print("All functools demos complete!")
    print("=" * 60)
