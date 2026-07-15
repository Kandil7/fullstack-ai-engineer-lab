# Type Hints Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Type Hint | Annotation indicating expected types |
| `typing.Optional` | `Union[X, None]` — value can be X or None |
| `typing.Union` | Value can be one of multiple types |
| `typing.TypeVar` | Generic type variable for parameterized types |
| `typing.Callable` | Annotation for function types |
| `typing.Protocol` | Structural subtyping interface |
| `typing.TypedDict` | Dictionary with specific key/value types |
| `typing.NamedTuple` | Tuple subclass with named fields |
| `typing.NewType` | Creates distinct type from existing type |
| `typing.TypeAlias` | Named alias for complex types |
| `typing.Literal` | Restrict to specific literal values |
| `typing.overload` | Multiple signatures for one function |
| `typing.ParamSpec` | Preserves parameter types in decorators |
| `typing.TYPE_CHECKING` | Import-only for type checkers |
| `typing.Annotated` | Add metadata to types |
| Static Typing | Type checking at analysis time |
| Dynamic Typing | Type checking at runtime |
| Type Safety | Ensuring correct type usage |
| Type Inference | Automatic type detection |
| Structural Subtyping | Type compatibility by interface |
| Nominal Subtyping | Type compatibility by inheritance |
| Covariance | Subtype relationship preserved |
| Contravariance | Subtype relationship reversed |
| `mypy` | Popular Python type checker |
| `pyright` | Fast Python type checker |
| `collections.abc` | Abstract base classes for types |

---

## Detailed Definitions

### `Annotated`

**Definition**: A type hint that adds metadata to a type without changing its runtime behavior. Useful for frameworks that process annotations (FastAPI, Pydantic).

**Example**:
```python
from typing import Annotated

# Add metadata to types
UserId = Annotated[int, "Unique user identifier"]
UserName = Annotated[str, "Min 3 characters"]

def get_user(user_id: UserId) -> dict:
    return {"id": user_id}

# Framework usage (FastAPI)
from fastapi import Query

def search(
    q: Annotated[str, Query(min_length=3)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    pass
```

**Related**: `typing`, Metadata, Framework Integration

---

### `Callable`

**Definition**: A type hint for functions and callables, specifying argument types and return type.

**Example**:
```python
from typing import Callable

# Callable[[ArgTypes], ReturnType]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# No arguments
def create_factory(f: Callable[[], int]) -> Callable[[], int]:
    return f

# Any arguments
def log_call(f: Callable[..., str]) -> Callable[..., str]:
    def wrapper(*args, **kwargs) -> str:
        print(f"Calling {f.__name__}")
        return f(*args, **kwargs)
    return wrapper
```

**Related**: Function Type, Lambda, Higher-Order Functions

---

### Contravariance

**Definition**: A type relationship where a function accepting a supertype can be used where a function accepting a subtype is expected. In Python, function parameter types are contravariant.

**Example**:
```python
from typing import TypeVar, Callable

Animal = TypeVar("Animal")
Dog = TypeVar("Dog", bound=Animal)

# A function that accepts any Animal can be used
# where a function accepting Dog is expected
def handle_animal(func: Callable[[Animal], None]) -> None:
    # This is contravariant: func accepts broader type
    func(Animal())

def handle_dog(dog: Dog) -> None:
    pass

# Contravariance: handle_animal can be used where handle_dog expected
```

**Related**: Covariance, Type Variance, Generic Types

---

### Covariance

**Definition**: A type relationship where a container of a subtype can be used where a container of a supertype is expected. In Python, return types are covariant.

**Example**:
```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)

class Box(Generic[T_co]):
    def __init__(self, item: T_co):
        self.item = item

class Animal: pass
class Dog(Animal): pass

# Box[Dog] can be used where Box[Animal] expected
dog_box: Box[Dog] = Box(Dog())
animal_box: Box[Animal] = dog_box  # OK: covariant

# Return types are covariant
def get_animal() -> Animal:
    return Dog()  # OK: Dog is subtype of Animal
```

**Related**: Contravariance, Type Variance, Generic Types

---

### `Literal`

**Definition**: A type hint that restricts a value to specific literal values (strings, ints, bools, etc.).

**Example**：
```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode: {mode}")

set_mode("read")   # OK
# set_mode("delete")  # Error: not a valid literal

# Combined with Union
Status = Literal["pending", "approved", "rejected"]

def process(status: Status) -> None:
    match status:
        case "pending": print("Processing...")
        case "approved": print("Approved!")
        case "rejected": print("Rejected")
```

**Related**: Enum, Literal Types, Narrowing

---

### `NamedTuple`

**Definition**: A subclass of `tuple` with named fields and type annotations. Combines tuple's immutability with readability.

**Example**:
```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

# Usage
p = Point(3.0, 4.0)
print(p.x)     # 3.0 (named access)
print(p[0])    # 3.0 (index access)
print(p.y)     # 4.0

# With methods
class Employee(NamedTuple):
    name: str
    salary: float
    
    def annual_salary(self) -> float:
        return self.salary * 12
```

**Related**: `dataclass`, Tuple, Immutable Data

---

### `NewType`

**Definition**: Creates a distinct type from an existing type, providing type safety without runtime overhead. The new type is a callable that returns its argument unchanged.

**Example**:
```python
from typing import NewType

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def get_user(user_id: UserId) -> dict:
    return {"id": user_id}

def process_order(order_id: OrderId) -> None:
    print(f"Order {order_id}")

# Type-safe usage
user_id = UserId(123)
order_id = OrderId(456)

get_user(user_id)    # OK
# get_user(order_id)  # Error: OrderId is not UserId

# Runtime: NewType returns the value unchanged
print(type(user_id))  # <class 'int'>
```

**Related**: Type Safety, Distinct Types, `TypedDict`

---

### `ParamSpec`

**Definition**: A type variable that captures the parameter types of a callable, used for accurately typing decorators that preserve function signatures.

**Example**:
```python
from typing import TypeVar, Callable, ParamSpec

P = ParamSpec("P")  # Captures parameter types
R = TypeVar("R")    # Captures return type

def decorator(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@decorator
def add(a: int, b: int) -> int:
    return a + b

# Type checker knows add takes (int, int) -> int
result = add(3, 5)  # Type: int
```

**Related**: `TypeVar`, Decorator Typing, Function Signatures

---

### `Protocol`

**Definition**: A structural subtyping mechanism that defines an interface without requiring inheritance. Objects are compatible if they have the required methods/attributes.

**Example**:
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Circle"

class Square:
    def draw(self) -> str:
        return "Square"

def render(shape: Drawable) -> None:
    print(shape.draw())

render(Circle())  # OK - structural match
render(Square())  # OK - structural match
# No inheritance needed!
```

**Related**: Structural Subtyping, Duck Typing, ABC

---

### `TypeAlias`

**Definition**: A named alias for a complex type expression, making type annotations more readable and maintainable.

**Example**:
```python
from typing import TypeAlias

# Complex type simplified
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def dot_product(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))

def process_json(data: JSON) -> None:
    # Recursive JSON type
    pass
```

**Related**: Type Comments, Readability, Complex Types

---

### `TypeVar`

**Definition**: A variable representing an unknown type, used for generic functions and classes that work with multiple types.

**Example**:
```python
from typing import TypeVar, Sequence

T = TypeVar("T")  # Any type
Numeric = TypeVar("Numeric", int, float)

def first(items: Sequence[T]) -> T:
    return items[0]

def double(x: Numeric) -> Numeric:
    return x * 2

# Type inference works
result = first([1, 2, 3])     # Type: int
result = first(["a", "b"])   # Type: str
```

**Related**: Generics, Generic Classes, Type Inference

---

### `TypedDict`

**Definition**: A dictionary type with specific key-value types, providing type safety for dictionary-based data structures.

**Example**:
```python
from typing import TypedDict, Required, NotRequired

class UserProfile(TypedDict):
    name: str
    age: int
    email: str
    is_active: bool  # Required by default

class APIResponse(TypedDict, total=False):
    data: dict
    error: str
    status: int  # All optional with total=False

# Usage
user: UserProfile = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "is_active": True
}
```

**Related**: `NamedTuple`, Dictionary Type Safety, JSON

---

### `TYPE_CHECKING`

**Definition**: A boolean constant that's `False` at runtime but `True` during type checking. Used to import types only needed for annotations.

**Example**:
```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from my_module import MyClass  # Only imported during type checking

def process(obj: "MyClass") -> None:
    # String annotation (forward reference)
    pass

# Runtime: no import error even if my_module isn't installed
# Type checking: mypy sees the import and validates types
```

**Related**: Forward References, Circular Imports, Lazy Imports

---

### `overload`

**Definition**: A decorator that allows defining multiple type signatures for a single function, enabling precise type inference for different argument patterns.

**Example**:
```python
from typing import overload

@overload
def process(value: int) -> int: ...

@overload
def process(value: str) -> str: ...

@overload
def process(value: list) -> list: ...

def process(value: int | str | list) -> int | str | list:
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    else:
        return [process(v) for v in value]

# Type checker uses overloads
result = process(5)          # Type: int
result = process("hello")   # Type: str
result = process([1, 2])    # Type: list
```

**Related**: Function Overloading, Union Types, Type Narrowing

---

### Structural Subtyping

**Definition**: Type compatibility based on the structure (methods/attributes) of types rather than explicit inheritance. Python's `Protocol` enables this.

**Example**:
```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict: ...

class User:
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self) -> dict:
        return {"name": self.name}

class Product:
    def __init__(self, title: str):
        self.title = title
    
    def to_dict(self) -> dict:
        return {"title": self.title}

def save(item: Serializable) -> None:
    data = item.to_dict()
    database.save(data)

# Both work - structural match, no inheritance needed
save(User("Alice"))
save(Product("Widget"))
```

**Related**: `Protocol`, Duck Typing, Nominal Subtyping

---

### Nominal Subtyping

**Definition**: Type compatibility based on explicit inheritance hierarchy. A subclass is a subtype of its parent class.

**Example**:
```python
class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

def pet(animal: Animal) -> None:
    print(animal.speak())

# Nominal: Dog is subtype of Animal through inheritance
pet(Dog())   # OK
pet(Cat())   # OK
```

**Related**: Inheritance, `Protocol`, Liskov Substitution

---

### `collections.abc`

**Definition**: Module containing abstract base classes for container types, providing type hints for common collection interfaces.

**Example**:
```python
from collections.abc import (
    Callable, Iterable, Iterator, Sequence,
    Mapping, MutableMapping, Set, MutableSet
)

def process(items: Iterable[int]) -> list[int]:
    return [x * 2 for x in items]

def merge(
    base: MutableMapping[str, int],
    updates: Mapping[str, int]
) -> None:
    base.update(updates)

# Works with any compatible type
process([1, 2, 3])           # list
process((1, 2, 3))           # tuple
process(range(10))            # range
```

**Related**: ABC, Type Hints, Collections

---

### Type Variance

**Definition**: The relationship between types when substituting subtype for supertype. Covariance preserves direction, contravariance reverses it.

**Example**:
```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)    # Covariant
T_contra = TypeVar("T_contra", contravariant=True)  # Contravariant

class Producer(Generic[T_co]):
    def get(self) -> T_co: ...

class Consumer(Generic[T_contra]):
    def put(self, item: T_contra) -> None: ...
```

**Related**: Covariance, Contravariance, Generic Types

---

### Type Safety

**Definition**: The degree to which type information prevents type-related errors at compile time (type checking) rather than runtime.

**Example**:
```python
# Unsafe (dynamic typing)
def add(a, b):
    return a + b

add(1, 2)       # OK
add("a", "b")   # OK
add(1, "2")     # Runtime error!

# Type-safe (static typing)
def add_safe(a: int, b: int) -> int:
    return a + b

add_safe(1, 2)      # OK
# add_safe("a", "b")  # Type error caught by mypy
```

**Related**: Type Hints, `mypy`, Static Checking

---
