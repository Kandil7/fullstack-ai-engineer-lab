"""
Itertools - Advanced Python Exercises
======================================
itertools provides iterator building blocks for efficient looping
and combinatorics.
"""

from itertools import (
    chain, product, permutations, combinations, combinations_with_replacement,
    groupby, islice, takewhile, dropwhile, count, cycle, repeat,
    starmap, zip_longest, tee, filterfalse
)
from typing import List, Tuple


# =============================================================================
# 1. Infinite Iterators
# =============================================================================

def demo_infinite():
    """Demonstrate infinite iterators."""
    # count - count from start
    counter = count(start=10, step=2)
    first_5 = list(islice(counter, 5))
    print(f"  count(10, 2): {first_5}")

    # cycle - cycle through iterable
    colors = cycle(["red", "green", "blue"])
    first_6 = [next(colors) for _ in range(6)]
    print(f"  cycle(['red', 'green', 'blue']): {first_6}")

    # repeat - repeat a value
    repeated = list(repeat("hello", 4))
    print(f"  repeat('hello', 4): {repeated}")


# =============================================================================
# 2. Terminating Iterators
# =============================================================================

def demo_terminating():
    """Demonstrate terminating iterators."""
    # chain - chain iterables together
    nums = chain([1, 2, 3], [4, 5, 6], [7, 8])
    print(f"  chain: {list(nums)}")

    # chain.from_iterable
    nested = [[1, 2], [3, 4], [5]]
    flat = list(chain.from_iterable(nested))
    print(f"  chain.from_iterable: {flat}")

    # islice - slice an iterator
    data = range(100)
    sliced = list(islice(data, 5, 15, 2))
    print(f"  islice(range(100), 5, 15, 2): {sliced}")

    # takewhile / dropwhile
    numbers = [1, 3, 5, 2, 4, 6, 1]
    less_than_5 = list(takewhile(lambda x: x < 5, numbers))
    from_5 = list(dropwhile(lambda x: x < 5, numbers))
    print(f"  takewhile(<5): {less_than_5}")
    print(f"  dropwhile(<5): {from_5}")


# =============================================================================
# 3. Combinatoric Iterators
# =============================================================================

def demo_combinatorics():
    """Demonstrate combinatoric iterators."""
    items = ["A", "B", "C"]

    # product - Cartesian product
    prods = list(product(items, repeat=2))
    print(f"  product(repeat=2): {prods}")

    # permutations - ordered arrangements
    perms = list(permutations(items, 2))
    print(f"  permutations(2): {perms}")

    # combinations - unordered selections
    combos = list(combinations(items, 2))
    print(f"  combinations(2): {combos}")

    # combinations_with_replacement
    combos_r = list(combinations_with_replacement(items, 2))
    print(f"  combinations_with_replacement(2): {combos_r}")


# =============================================================================
# 4. groupby - Group Consecutive Elements
# =============================================================================

def demo_groupby():
    """Demonstrate groupby for grouping data."""
    # Group sorted data
    data = [
        {"type": "fruit", "name": "apple"},
        {"type": "fruit", "name": "banana"},
        {"type": "vegetable", "name": "carrot"},
        {"type": "vegetable", "name": "daikon"},
        {"type": "fruit", "name": "cherry"},
    ]

    # Must sort by key first!
    data.sort(key=lambda x: x["type"])

    print("  Grouped by type:")
    for key, group in groupby(data, key=lambda x: x["type"]):
        items = [item["name"] for item in group]
        print(f"    {key}: {items}")

    # Group numbers by parity
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    for key, group in groupby(numbers, key=lambda x: x % 2):
        print(f"    {'odd' if key else 'even'}: {list(group)}")


# =============================================================================
# 5. starmap and zip_longest
# =============================================================================

def demo_starmap_zip():
    """Demonstrate starmap and zip_longest."""
    # starmap - apply function to argument tuples
    pairs = [(2, 3), (4, 5), (6, 7)]
    powers = list(starmap(lambda a, b: a ** b, pairs))
    print(f"  starmap(power): {powers}")

    # zip_longest - zip with fill value
    names = ["Alice", "Bob", "Charlie"]
    scores = [95, 87]
    zipped = list(zip_longest(names, scores, fillvalue="N/A"))
    print(f"  zip_longest: {zipped}")


# =============================================================================
# 6. filterfalse and partition
# =============================================================================

def demo_filter_partition():
    """Demonstrate filterfalse and custom partition."""
    numbers = range(10)

    # filterfalse - complement of filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    odds = list(filterfalse(lambda x: x % 2 == 0, numbers))
    print(f"  filter (evens): {evens}")
    print(f"  filterfalse (odds): {odds}")

    # Custom partition using filterfalse
    def partition(pred, iterable):
        """Partition iterable into two based on predicate."""
        t1, t2 = tee(iterable)
        return filter(pred, t1), filterfalse(pred, t2)

    positives, negatives = partition(lambda x: x > 0, [-3, -2, -1, 0, 1, 2, 3])
    print(f"  partition positives: {list(positives)}")
    print(f"  partition negatives: {list(negatives)}")


# =============================================================================
# 7. Practical Examples
# =============================================================================

def flatten(nested_list: list) -> list:
    """Flatten a nested list using chain."""
    return list(chain.from_iterable(nested_list))


def roundrobin(*iterables):
    """Round-robin iteration through multiple iterables."""
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next_func in nexts:
                yield next_func()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def sliding_window(iterable, n):
    """Sliding window of size n."""
    it = iter(iterable)
    window = list(islice(it, n))
    if len(window) == n:
        yield tuple(window)
    for item in it:
        window = window[1:] + [item]
        yield tuple(window)


def demo_practical():
    """Practical itertools examples."""
    # Flatten
    nested = [[1, 2], [3, [4, 5]], [6]]
    # Note: chain.from_iterable only handles one level
    print(f"  flatten: {flatten([[1, 2], [3, 4], [5]])}")

    # Round-robin
    result = list(roundrobin("ABC", "123", "xyz"))
    print(f"  roundrobin: {result}")

    # Sliding window
    data = [1, 2, 3, 4, 5, 6]
    windows = list(sliding_window(data, 3))
    print(f"  sliding_window(3): {windows}")

    # Combinations for passwords
    chars = "abc"
    all_2_char = ["".join(c) for c in combinations(chars, 2)]
    print(f"  2-char combinations: {all_2_char}")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ITERTOOLS DEMO")
    print("=" * 60)

    print("\n--- Infinite Iterators ---")
    demo_infinite()

    print("\n--- Terminating Iterators ---")
    demo_terminating()

    print("\n--- Combinatorics ---")
    demo_combinatorics()

    print("\n--- groupby ---")
    demo_groupby()

    print("\n--- starmap and zip_longest ---")
    demo_starmap_zip()

    print("\n--- filterfalse and partition ---")
    demo_filter_partition()

    print("\n--- Practical Examples ---")
    demo_practical()

    print("\n" + "=" * 60)
    print("All itertools demos complete!")
    print("=" * 60)
