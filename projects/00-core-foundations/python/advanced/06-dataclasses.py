"""
Dataclasses - Advanced Python Exercises
========================================
Dataclasses provide a decorator and functions to automatically
generate special methods for classes.
"""

from dataclasses import dataclass, field, asdict, astuple, fields, replace
from typing import List, Dict, Optional, ClassVar
from datetime import datetime


# =============================================================================
# 1. Basic Dataclass
# =============================================================================

@dataclass
class Point:
    """Basic dataclass with auto-generated methods."""
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass
class Person:
    """Person with default values and computed property."""
    name: str
    age: int
    email: str
    is_active: bool = True

    @property
    def is_adult(self) -> bool:
        return self.age >= 18


# =============================================================================
# 2. Field Customization
# =============================================================================

@dataclass
class Product:
    """Product with field customizations."""
    name: str
    price: float
    quantity: int = 0
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    sku: str = field(init=False)  # Not in __init__

    def __post_init__(self):
        self.sku = self.name.upper().replace(" ", "-")[:8]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "tags": self.tags,
            "sku": self.sku,
        }


@dataclass(order=True)
class RankedItem:
    """Dataclass with ordering based on rank."""
    rank: int
    name: str = field(compare=False)
    score: float = field(compare=False)


# =============================================================================
# 3. Frozen Dataclass (Immutable)
# =============================================================================

@dataclass(frozen=True)
class Config:
    """Immutable configuration object."""
    host: str
    port: int
    debug: bool = False
    max_connections: int = 100

    def with_debug(self, debug: bool) -> "Config":
        """Return a new Config with debug changed (since frozen)."""
        return replace(self, debug=debug)


@dataclass(frozen=True)
class Vector3D:
    """Immutable 3D vector with operations."""
    x: float
    y: float
    z: float

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


# =============================================================================
# 4. Inheritance
# =============================================================================

@dataclass
class Animal:
    """Base animal class."""
    name: str
    sound: str

    def speak(self) -> str:
        return f"{self.name} says {self.sound}!"


@dataclass
class Dog(Animal):
    """Dog with breed."""
    breed: str
    is_good_boy: bool = True

    def __post_init__(self):
        self.sound = "Woof"


@dataclass
class Cat(Animal):
    """Cat with indoor/outdoor status."""
    indoor: bool = True

    def __post_init__(self):
        self.sound = "Meow"


# =============================================================================
# 5. Serialization
# =============================================================================

@dataclass
class ApiResponse:
    """API response with serialization methods."""
    status: str
    data: Optional[Dict] = None
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def success(cls, data: Dict) -> "ApiResponse":
        return cls(status="success", data=data)

    @classmethod
    def error(cls, errors: List[str]) -> "ApiResponse":
        return cls(status="error", errors=errors)

    def to_json(self) -> str:
        import json
        return json.dumps(asdict(self), default=str)


# =============================================================================
# 6. Slots Dataclass
# =============================================================================

@dataclass(slots=True)
class CompactPoint:
    """Memory-efficient point with __slots__."""
    x: float
    y: float


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DATACLASSES DEMO")
    print("=" * 60)

    # 1. Basic dataclass
    print("\n--- Basic Dataclass ---")
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print(f"  p1 = {p1}")
    print(f"  p2 = {p2}")
    print(f"  Distance: {p1.distance_to(p2):.2f}")
    print(f"  Equal: {p1 == Point(3, 4)}")

    person = Person("Alice", 30, "alice@example.com")
    print(f"  {person.name} is adult: {person.is_adult}")

    # 2. Field customization
    print("\n--- Field Customization ---")
    product = Product("Laptop Pro", 1299.99, quantity=5, tags=["electronics"])
    print(f"  Product: {product.to_dict()}")

    # 3. Frozen dataclass
    print("\n--- Frozen Dataclass ---")
    config = Config("localhost", 8080)
    print(f"  Config: {config}")
    config_debug = config.with_debug(True)
    print(f"  With debug: {config_debug}")
    try:
        config.port = 9090
    except Exception as e:
        print(f"  Cannot modify frozen: {type(e).__name__}")

    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    v3 = v1 + v2
    print(f"  v1 + v2 = {v3}")
    print(f"  Magnitude: {v3.magnitude:.2f}")

    # 4. Inheritance
    print("\n--- Inheritance ---")
    dog = Dog("Buddy", "Woof", "Golden Retriever")
    cat = Cat("Whiskers", "Meow", indoor=True)
    print(f"  {dog.speak()}")
    print(f"  {cat.speak()}")
    print(f"  Dog fields: {[f.name for f in fields(dog)]}")

    # 5. Serialization
    print("\n--- Serialization ---")
    response = ApiResponse.success({"users": 42})
    print(f"  JSON: {response.to_json()[:80]}...")
    error_resp = ApiResponse.error(["Not found", "Unauthorized"])
    print(f"  Error: {error_resp.to_json()[:80]}...")

    # 6. Slots dataclass
    print("\n--- Slots Dataclass ---")
    compact = CompactPoint(1.5, 2.5)
    print(f"  CompactPoint: {compact}")
    print(f"  Has __slots__: {hasattr(CompactPoint, '__slots__')}")

    # 7. asdict and astuple
    print("\n--- Conversion Utilities ---")
    print(f"  asdict: {asdict(person)}")
    print(f"  astuple: {astuple(person)[:3]}")

    print("\n" + "=" * 60)
    print("All dataclass demos complete!")
    print("=" * 60)
