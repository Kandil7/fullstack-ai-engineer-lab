"""
Abstract Base Classes (ABC) - Advanced Python Exercises
========================================================
ABCs define interfaces and enforce implementation requirements
for subclasses.
"""

from abc import ABC, abstractmethod, abstractproperty
from typing import List, Optional
from dataclasses import dataclass


# =============================================================================
# 1. Basic Abstract Class
# =============================================================================

class Shape(ABC):
    """Abstract base class for shapes."""

    def __init__(self, color: str = "black"):
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

    def describe(self) -> str:
        """Concrete method - available to all subclasses."""
        return (
            f"{self.__class__.__name__} (color={self.color}, "
            f"area={self.area():.2f}, perimeter={self.perimeter():.2f})"
        )


class Circle(Shape):
    """Circle implementation."""

    def __init__(self, radius: float, color: str = "red"):
        super().__init__(color)
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    """Rectangle implementation."""

    def __init__(self, width: float, height: float, color: str = "blue"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Triangle implementation using Heron's formula."""

    def __init__(self, a: float, b: float, c: float, color: str = "green"):
        super().__init__(color)
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# =============================================================================
# 2. Plugin System
# =============================================================================

class Plugin(ABC):
    """Abstract plugin interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @abstractmethod
    def execute(self, data: dict) -> dict:
        """Execute the plugin."""
        pass

    def __repr__(self) -> str:
        return f"<Plugin: {self.name}>"


class ValidationPlugin(Plugin):
    """Validates data fields."""

    @property
    def name(self) -> str:
        return "validation"

    def execute(self, data: dict) -> dict:
        errors = []
        if "email" in data and "@" not in data.get("email", ""):
            errors.append("Invalid email")
        if "age" in data and not isinstance(data.get("age"), int):
            errors.append("Age must be integer")
        return {"valid": len(errors) == 0, "errors": errors}


class TransformPlugin(Plugin):
    """Transforms data fields."""

    @property
    def name(self) -> str:
        return "transform"

    def execute(self, data: dict) -> dict:
        return {k: str(v).upper() if isinstance(v, str) else v for k, v in data.items()}


class PluginManager:
    """Manages and executes plugins."""

    def __init__(self):
        self._plugins: List[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        self._plugins.append(plugin)

    def execute_all(self, data: dict) -> dict:
        result = {"original": data, "results": {}}
        for plugin in self._plugins:
            result["results"][plugin.name] = plugin.execute(data)
        return result


# =============================================================================
# 3. Abstract Collection
# =============================================================================

class AbstractCollection(ABC):
    """Abstract collection interface."""

    @abstractmethod
    def add(self, item) -> None: pass

    @abstractmethod
    def remove(self, item) -> bool: pass

    @abstractmethod
    def contains(self, item) -> bool: pass

    @abstractmethod
    def size(self) -> int: pass

    @abstractmethod
    def is_empty(self) -> bool: pass

    def __len__(self) -> int:
        return self.size()

    def __bool__(self) -> bool:
        return not self.is_empty()


class UniqueList(AbstractCollection):
    """A list that only contains unique items."""

    def __init__(self):
        self._items: list = []

    def add(self, item) -> None:
        if not self.contains(item):
            self._items.append(item)

    def remove(self, item) -> bool:
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def contains(self, item) -> bool:
        return item in self._items

    def size(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __repr__(self) -> str:
        return f"UniqueList({self._items})"


# =============================================================================
# 4. Mixin Pattern
# =============================================================================

class Printable(ABC):
    """Mixin for printable objects."""

    @abstractmethod
    def to_string(self) -> str: pass

    def print(self) -> None:
        print(f"  {self.to_string()}")


class Comparable(ABC):
    """Mixin for comparable objects."""

    @abstractmethod
    def value(self) -> float: pass

    def __lt__(self, other) -> bool:
        return self.value() < other.value()

    def __eq__(self, other) -> bool:
        return self.value() == other.value()

    def __gt__(self, other) -> bool:
        return self.value() > other.value()


@dataclass
class Temperature(Comparable, Printable):
    """Temperature that is both printable and comparable."""
    celsius: float

    def value(self) -> float:
        return self.celsius

    def to_string(self) -> str:
        return f"{self.celsius}°C ({self.celsius * 9/5 + 32:.1f}°F)"

    def to_fahrenheit(self) -> float:
        return self.celsius * 9/5 + 32


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ABC DEMO")
    print("=" * 60)

    # 1. Basic abstract class
    print("\n--- Shape Hierarchy ---")
    shapes = [
        Circle(5, "red"),
        Rectangle(4, 6, "blue"),
        Triangle(3, 4, 5, "green"),
    ]
    for shape in shapes:
        print(f"  {shape.describe()}")

    # 2. Cannot instantiate abstract class
    print("\n--- Abstract Class Protection ---")
    try:
        shape = Shape("yellow")
    except TypeError as e:
        print(f"  Cannot instantiate: {e}")

    # 3. Plugin system
    print("\n--- Plugin System ---")
    manager = PluginManager()
    manager.register(ValidationPlugin())
    manager.register(TransformPlugin())

    data = {"email": "user@example.com", "age": 25, "name": "alice"}
    result = manager.execute_all(data)
    print(f"  Data: {result['original']}")
    for plugin_name, plugin_result in result["results"].items():
        print(f"  {plugin_name}: {plugin_result}")

    # 4. Abstract collection
    print("\n--- Unique Collection ---")
    collection = UniqueList()
    for item in [1, 2, 3, 2, 4, 1, 5]:
        collection.add(item)
    print(f"  Collection: {collection}")
    print(f"  Size: {len(collection)}")
    print(f"  Contains 3: {collection.contains(3)}")
    collection.remove(3)
    print(f"  After remove(3): {collection}")

    # 5. Mixin pattern
    print("\n--- Mixin Pattern ---")
    temps = [Temperature(100), Temperature(0), Temperature(37)]
    for t in temps:
        t.print()
    temps.sort()
    print(f"  Sorted: {[t.to_string() for t in temps]}")

    print("\n" + "=" * 60)
    print("All ABC demos complete!")
    print("=" * 60)
