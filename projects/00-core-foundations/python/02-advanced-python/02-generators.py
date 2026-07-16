"""
Generators - Advanced Python Exercises
======================================
Generators are lazy iterators that yield values one at a time,
enabling efficient memory usage for large sequences.
"""

import sys
from typing import Iterator, Generator, Optional


# =============================================================================
# 1. Basic Generator Functions
# =============================================================================

def countdown(n: int) -> Generator[int, None, None]:
    """Count down from n to 1."""
    print(f"  Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("  Liftoff!")


def fibonacci_infinite() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_large_file(filepath: str) -> Generator[str, None, None]:
    """Read a file line by line without loading all into memory."""
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


# =============================================================================
# 2. Generator with send()
# =============================================================================

def accumulator() -> Generator[int, None, None]:
    """Accumulate values sent to it."""
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value


def coroutine_example():
    """Demonstrate send() to communicate with generator."""
    gen = accumulator()
    next(gen)  # Prime the generator
    print(f"  After prime: {gen.send(10)}")
    print(f"  After send(20): {gen.send(20)}")
    print(f"  After send(30): {gen.send(30)}")


# =============================================================================
# 3. Generator Expressions
# =============================================================================

def generator_vs_list():
    """Compare memory usage of generators vs lists."""
    # List comprehension - stores all values in memory
    list_comp = [x ** 2 for x in range(1000000)]
    print(f"  List size: {sys.getsizeof(list_comp):,} bytes")

    # Generator expression - stores only the generator object
    gen_exp = (x ** 2 for x in range(1000000))
    print(f"  Generator size: {sys.getsizeof(gen_exp)} bytes")


# =============================================================================
# 4. Generator Pipelines
# =============================================================================

def read_data() -> Generator[str, None, None]:
    """Stage 1: Read raw data."""
    data = ["1,apple,5", "2,banana,3", "3,cherry,8", "4,date,2", "5,elderberry,7"]
    for item in data:
        yield item


def parse_data(data: Generator) -> Generator[dict, None, None]:
    """Stage 2: Parse CSV-like data."""
    for line in data:
        parts = line.split(",")
        yield {"id": int(parts[0]), "name": parts[1], "value": int(parts[2])}


def filter_data(data: Generator, min_value: int = 3) -> Generator[dict, None, None]:
    """Stage 3: Filter by minimum value."""
    for item in data:
        if item["value"] >= min_value:
            yield item


def transform_data(data: Generator) -> Generator[dict, None, None]:
    """Stage 4: Add computed fields."""
    for item in data:
        item["label"] = f"{item['name'].upper()} ({item['value']})"
        yield item


# =============================================================================
# 5. Infinite Sequences
# =============================================================================

def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """Infinite counter starting from a value."""
    n = start
    while True:
        yield n
        n += step


def take(n: int, iterable: Iterator) -> list:
    """Take first n items from an iterable."""
    result = []
    for i, item in enumerate(iterable):
        if i >= n:
            break
        result.append(item)
    return result


def window(iterable: Iterator, size: int) -> Generator[list, None, None]:
    """Sliding window over an iterable."""
    window_list = []
    for item in iterable:
        window_list.append(item)
        if len(window_list) == size:
            yield window_list[:]
            window_list.pop(0)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATORS DEMO")
    print("=" * 60)

    # 1. Basic generators
    print("\n--- Countdown Generator ---")
    for num in countdown(5):
        print(f"  {num}...")

    print("\n--- Fibonacci (first 10) ---")
    fib = fibonacci_infinite()
    first_10 = take(10, fib)
    print(f"  {first_10}")

    # 2. send() demo
    print("\n--- Generator with send() ---")
    coroutine_example()

    # 3. Memory comparison
    print("\n--- Generator vs List (memory) ---")
    generator_vs_list()

    # 4. Generator pipeline
    print("\n--- Generator Pipeline ---")
    pipeline = transform_data(
        filter_data(
            parse_data(read_data()),
            min_value=4
        )
    )
    for item in pipeline:
        print(f"  {item['label']}")

    # 5. Infinite sequences
    print("\n--- Infinite Counter (first 8) ---")
    counter = infinite_counter(start=100, step=5)
    print(f"  {take(8, counter)}")

    # 6. Sliding window
    print("\n--- Sliding Window ---")
    nums = iter([1, 2, 3, 4, 5, 6, 7])
    for w in window(nums, 3):
        print(f"  {w}")

    print("\n" + "=" * 60)
    print("All generator demos complete!")
    print("=" * 60)
