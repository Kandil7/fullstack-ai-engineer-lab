"""
Slots - Advanced Python Exercises
==================================
__slots__ provides memory optimization by preventing dynamic
attribute creation and reducing memory overhead.
"""

import sys
from typing import List


# =============================================================================
# 1. Basic __slots__
# =============================================================================

class PointRegular:
    """Regular class without __slots__."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class PointSlots:
    """Class with __slots__ for memory efficiency."""
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# =============================================================================
# 2. Memory Comparison
# =============================================================================

def demo_memory_comparison():
    """Compare memory usage with and without __slots__."""
    regular = PointRegular(1, 2)
    slotted = PointSlots(1, 2)

    print(f"  Regular class size: {sys.getsizeof(regular)} bytes")
    print(f"  Slotted class size: {sys.getsizeof(slotted)} bytes")

    # Compare __dict__
    print(f"  Regular has __dict__: {hasattr(regular, '__dict__')}")
    print(f"  Slotted has __dict__: {hasattr(slotted, '__dict__')}")

    # Cannot add dynamic attributes to slotted class
    try:
        slotted.z = 3
    except AttributeError as e:
        print(f"  Cannot add attribute: {e}")

    # Can add to regular class
    regular.z = 3
    print(f"  Regular can add: regular.z = {regular.z}")


# =============================================================================
# 3. Memory with Large Objects
# =============================================================================

class UserRegular:
    """Regular user class."""
    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age


class UserSlots:
    """User class with __slots__."""
    __slots__ = ('id', 'name', 'email', 'age')

    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age


def demo_large_objects():
    """Compare memory with many objects."""
    n = 10000

    regular_users = [UserRegular(i, f"user{i}", f"user{i}@email.com", 25) for i in range(n)]
    slotted_users = [UserSlots(i, f"user{i}", f"user{i}@email.com", 25) for i in range(n)]

    regular_memory = sum(sys.getsizeof(u) for u in regular_users)
    slotted_memory = sum(sys.getsizeof(u) for u in slotted_users)

    print(f"  {n} regular users: ~{regular_memory:,} bytes")
    print(f"  {n} slotted users: ~{slotted_memory:,} bytes")
    print(f"  Savings: ~{regular_memory - slotted_memory:,} bytes")


# =============================================================================
# 4. __slots__ with Inheritance
# =============================================================================

class Base:
    """Base class with __slots__."""
    __slots__ = ('id',)


class Child(Base):
    """Child class adding more slots."""
    __slots__ = ('name', 'value')

    def __init__(self, id: int, name: str, value: float):
        self.id = id
        self.name = name
        self.value = value


def demo_inheritance():
    """Demonstrate __slots__ with inheritance."""
    obj = Child(1, "test", 3.14)
    print(f"  Child slots: {obj.id}, {obj.name}, {obj.value}")
    print(f"  Base slots accessible: {obj.id}")
    print(f"  Combined slots: {Base.__slots__ + Child.__slots__}")

    # Check memory
    print(f"  Child size: {sys.getsizeof(obj)} bytes")


# =============================================================================
# 5. __slots__ with Properties
# =============================================================================

class Circle:
    """Circle using __slots__ with property."""
    __slots__ = ('_radius',)

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2


# =============================================================================
# 6. Performance Benchmark
# =============================================================================

def benchmark_class(cls, n: int = 100000):
    """Benchmark object creation and attribute access."""
    import time

    start = time.perf_counter()
    objects = [cls(i, f"item{i}") for i in range(n)]
    creation_time = time.perf_counter() - start

    start = time.perf_counter()
    total = sum(obj.x for obj in objects)
    access_time = time.perf_counter() - start

    return creation_time, access_time


class ItemRegular:
    def __init__(self, x: int, name: str):
        self.x = x
        self.name = name


class ItemSlots:
    __slots__ = ('x', 'name')

    def __init__(self, x: int, name: str):
        self.x = x
        self.name = name


def demo_benchmark():
    """Compare performance of regular vs slotted classes."""
    n = 100000

    reg_create, reg_access = benchmark_class(ItemRegular, n)
    slot_create, slot_access = benchmark_class(ItemSlots, n)

    print(f"  Regular - Create: {reg_create:.4f}s, Access: {reg_access:.4f}s")
    print(f"  Slots   - Create: {slot_create:.4f}s, Access: {slot_access:.4f}s")
    print(f"  Speedup - Create: {reg_create/slot_create:.2f}x, Access: {reg_access/slot_access:.2f}x")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SLOTS DEMO")
    print("=" * 60)

    # 1. Basic comparison
    print("\n--- Basic __slots__ ---")
    demo_memory_comparison()

    # 2. Large objects
    print("\n--- Large Object Memory ---")
    demo_large_objects()

    # 3. Inheritance
    print("\n--- __slots__ with Inheritance ---")
    demo_inheritance()

    # 4. Properties with slots
    print("\n--- __slots__ with Properties ---")
    c = Circle(5)
    print(f"  Radius: {c.radius}")
    print(f"  Area: {c.area:.2f}")
    c.radius = 10
    print(f"  New area: {c.area:.2f}")

    # 5. Benchmark
    print("\n--- Performance Benchmark ---")
    demo_benchmark()

    # 6. Key differences summary
    print("\n--- Key Differences ---")
    print("  1. Memory: __slots__ uses less memory per instance")
    print("  2. Speed: Attribute access is slightly faster")
    print("  3. Restriction: Cannot add dynamic attributes")
    print("  4. Inheritance: Child classes need their own __slots__")
    print("  5. Trade-off: Less flexible but more efficient")

    print("\n" + "=" * 60)
    print("All slots demos complete!")
    print("=" * 60)
