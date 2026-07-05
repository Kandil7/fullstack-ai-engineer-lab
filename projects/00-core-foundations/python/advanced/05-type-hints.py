"""
Type Hints - Advanced Python Exercises
=======================================
Type hints improve code clarity, enable static analysis,
and provide better IDE support.
"""

from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any, Callable,
    TypeVar, Generic, Protocol, Literal, Final, TypeAlias
)
from dataclasses import dataclass


# =============================================================================
# 1. Basic Type Hints
# =============================================================================

def greet(name: str) -> str:
    """Simple function with type hints."""
    return f"Hello, {name}!"


def calculate(a: float, b: float, operation: str = "add") -> float:
    """Calculator with type hints."""
    operations = {"add": a + b, "sub": a - b, "mul": a * b, "div": a / b}
    return operations.get(operation, 0.0)


def process_items(items: List[str], uppercase: bool = False) -> Dict[str, int]:
    """Process a list of items into a dictionary."""
    result = {}
    for item in items:
        key = item.upper() if uppercase else item
        result[key] = len(item)
    return result


# =============================================================================
# 2. Complex Types
# =============================================================================

def merge_dicts(
    dict1: Dict[str, Any],
    dict2: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge two dictionaries."""
    return {**dict1, **dict2}


def find_duplicates(items: List[int]) -> Set[int]:
    """Find duplicate items in a list."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates


def flexible_input(data: Union[str, int, float]) -> str:
    """Accept multiple types with Union."""
    if isinstance(data, str):
        return f"String: {data}"
    elif isinstance(data, int):
        return f"Integer: {data}"
    return f"Float: {data}"


# =============================================================================
# 3. TypeVar and Generics
# =============================================================================

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Stack(Generic[T]):
    """Generic stack implementation."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Pair(Generic[K, V]):
    """Generic key-value pair."""

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"Pair({self.key!r}, {self.value!r})"


# =============================================================================
# 4. Protocol and Structural Typing
# =============================================================================

class Drawable(Protocol):
    """Protocol for anything that can be drawn."""
    def draw(self) -> str: ...


class Circle:
    def draw(self) -> str:
        return "Drawing a circle"


class Square:
    def draw(self) -> str:
        return "Drawing a square"


def draw_shape(shape: Drawable) -> str:
    """Accept any object with a draw method (structural typing)."""
    return shape.draw()


# =============================================================================
# 5. Literal and Final Types
# =============================================================================

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    """Only accept specific string literals."""
    return f"Mode set to: {mode}"


MAX_RETRIES: Final = 3
TypeAlias = TypeAlias
Vector: TypeAlias = List[float]


def scale_vector(vector: Vector, factor: float) -> Vector:
    """Scale a vector by a factor."""
    return [v * factor for v in vector]


# =============================================================================
# 6. Callable and Function Types
# =============================================================================

def apply_operation(
    values: List[float],
    operation: Callable[[float], float]
) -> List[float]:
    """Apply a function to each value."""
    return [operation(v) for v in values]


def create_multiplier(factor: float) -> Callable[[float], float]:
    """Create a multiplier function."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier


# =============================================================================
# 7. Class Annotations
# =============================================================================

@dataclass
class User:
    """User class with full type annotations."""
    name: str
    email: str
    age: int
    is_active: bool = True
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "is_active": self.is_active,
            "tags": self.tags,
        }


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TYPE HINTS DEMO")
    print("=" * 60)

    # 1. Basic hints
    print("\n--- Basic Type Hints ---")
    print(f"  {greet('World')}")
    print(f"  {calculate(10, 3, 'add')}")
    print(f"  {calculate(10, 3, 'mul')}")
    result = process_items(["apple", "banana", "cherry"], uppercase=True)
    print(f"  {result}")

    # 2. Complex types
    print("\n--- Complex Types ---")
    merged = merge_dicts({"a": 1}, {"b": 2})
    print(f"  Merged: {merged}")
    dupes = find_duplicates([1, 2, 3, 2, 4, 3, 5])
    print(f"  Duplicates: {dupes}")
    print(f"  {flexible_input(42)}")
    print(f"  {flexible_input('hello')}")
    print(f"  {flexible_input(3.14)}")

    # 3. Generics
    print("\n--- Generic Stack ---")
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    print(f"  Stack size: {len(int_stack)}")
    print(f"  Pop: {int_stack.pop()}")
    print(f"  Peek: {int_stack.peek()}")

    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"  String stack: {str_stack.pop()}")

    # 4. Protocol
    print("\n--- Protocol (Structural Typing) ---")
    print(f"  {draw_shape(Circle())}")
    print(f"  {draw_shape(Square())}")

    # 5. Literal and Final
    print("\n--- Literal and Final ---")
    print(f"  {set_mode('read')}")
    print(f"  MAX_RETRIES = {MAX_RETRIES}")
    scaled = scale_vector([1.0, 2.0, 3.0], 2.5)
    print(f"  Scaled vector: {scaled}")

    # 6. Callable
    print("\n--- Callable Types ---")
    doubled = apply_operation([1, 2, 3, 4], lambda x: x * 2)
    print(f"  Doubled: {doubled}")
    triple = create_multiplier(3)
    print(f"  Triple(5) = {triple(5)}")

    # 7. Dataclass with annotations
    print("\n--- Dataclass Annotations ---")
    user = User("Alice", "alice@example.com", 30, tags=["admin", "user"])
    print(f"  User: {user.to_dict()}")

    print("\n" + "=" * 60)
    print("All type hint demos complete!")
    print("=" * 60)
