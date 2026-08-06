# Advanced Python Lecture 05: Type Hints

## Topic Overview

Type hints (also called type annotations) provide optional static type checking in Python, enabling better code documentation, IDE support, and early error detection. Introduced in Python 3.5 (PEP 484) and continuously enhanced, type hints have become essential for large codebases, AI engineering projects, and any code where maintainability and correctness matter.

---

## Learning Objectives

By the end of this lecture, you will be able:

1. Understand the purpose and benefits of type hints
2. Annotate functions, variables, and class attributes
3. Use built-in generic types (`list`, `dict`, `tuple`, `set`)
4. Leverage `typing` module types (`Optional`, `Union`, `Callable`, etc.)
5. Define custom types with `TypeVar`, `NewType`, and `TypeAlias`
6. Use `Protocol` for structural subtyping
7. Apply type hints to async code and decorators
8. Run type checking with `mypy` or `pyright`
9. Handle complex real-world type scenarios
10. Follow type hint best practices

---

## 1. Why Type Hints?

### Benefits

```python
# Without type hints - unclear what this expects/returns
def process(data):
    return data["name"].upper()

# With type hints - clear contract
def process(data: dict[str, str]) -> str:
    return data["name"].upper()

# Benefits:
# 1. Documentation: Self-documenting code
# 2. IDE support: Autocomplete, refactoring, error detection
# 3. Static checking: Catch bugs before runtime
# 4. Better error messages: Clearer function signatures
```

### Type Hints Don't Affect Runtime

```python
# Type hints are ignored at runtime
def greet(name: str) -> str:
    return f"Hello, {name}!"

# This works even though int is not str
greet(42)  # No runtime error!

# Type checkers (mypy) would catch this:
# error: Argument 1 has incompatible type "int"; expected "str"
```

---

## 2. Basic Type Annotations

### Function Annotations

```python
def greet(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def is_valid(email: str) -> bool:
    return "@" in email

def log_message(message: str) -> None:
    """Print a message, returns nothing."""
    print(message)
```

### Variable Annotations

```python
# Variable annotations (Python 3.6+)
name: str = "Alice"
age: int = 30
height: float = 5.9
is_active: bool = True

# Multiple annotations on one line
x: int; y: int; z: int = 1, 2, 3

# Annotated without assignment
result: str
result = compute_something()
```

### Class Attribute Annotations

```python
class User:
    name: str
    age: int
    email: str
    is_active: bool = True  # With default value
    
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email
```

---

## 3. Built-in Generic Types

### Python 3.9+ Syntax (Preferred)

```python
# Collections module types (Python 3.9+)
from collections.abc import Callable, Iterable, Iterator, Sequence

# List
numbers: list[int] = [1, 2, 3]
names: list[str] = ["Alice", "Bob"]

# Dict
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
config: dict[str, list[int]] = {"ports": [8080, 8443]}

# Tuple
point: tuple[int, int] = (10, 20)
mixed: tuple[str, int, bool] = ("Alice", 30, True)
variable_length: tuple[int, ...] = (1, 2, 3, 4, 5)

# Set
unique_ids: set[int] = {1, 2, 3}

# Frozen (immutable) versions
immutable_list: frozenset[int] = frozenset({1, 2, 3})
```

### Legacy `typing` Module (Python 3.5-3.8)

```python
from typing import List, Dict, Tuple, Set, FrozenSet

# Same as above but using typing module
numbers: List[int] = [1, 2, 3]
scores: Dict[str, int] = {"Alice": 95}
point: Tuple[int, int] = (10, 20)
ids: Set[int] = {1, 2, 3}
```

---

## 4. `typing` Module Essentials

### Optional and Union

```python
from typing import Optional, Union

# Optional[X] is equivalent to Union[X, None]
def find_user(user_id: int) -> Optional[dict]:
    """Return user dict or None if not found."""
    if user_id in database:
        return database[user_id]
    return None

# Union[X, Y] - value can be X or Y
def process(value: Union[str, int]) -> str:
    if isinstance(value, int):
        return str(value)
    return value.upper()

# Python 3.10+ pipe syntax
def process_v2(value: str | int) -> str:
    if isinstance(value, int):
        return str(value)
    return value.upper()
```

### Callable

```python
from typing import Callable

# Callable[[ArgTypes], ReturnType]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Callable with no arguments
def create_factory(func: Callable[[], int]) -> Callable[[], int]:
    return func

# Callable with any arguments
def log_call(func: Callable[..., str]) -> Callable[..., str]:
    def wrapper(*args, **kwargs) -> str:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### TypeVar — Generic Functions

```python
from typing import TypeVar, Sequence

T = TypeVar("T")  # Any type
Number = TypeVar("Number", int, float)  # Restricted type var

def first(items: Sequence[T]) -> T:
    """Return the first item of a sequence."""
    return items[0]

# Type is inferred correctly
result = first([1, 2, 3])  # Type: int
result = first(["a", "b"])  # Type: str

def double(x: Number) -> Number:
    return x * 2

double(5)      # OK: int
double(3.14)   # OK: float
# double("hi")  # Error: str not in (int, float)
```

### TypeVar with Bounds

```python
from typing import TypeVar

# Bound: T must be a subclass of Comparable
Comparable = TypeVar("Comparable", bound="ComparableClass")

def largest(items: list[Comparable]) -> Comparable:
    return max(items)

# Constrained: T must be exactly one of these types
Numeric = TypeVar("Numeric", int, float, complex)

def sum_values(values: list[Numeric]) -> Numeric:
    return sum(values)
```

---

## 5. Advanced Type Patterns

### Literal Types

```python
from typing import Literal

# Restrict to specific literal values
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode: {mode}")

set_mode("read")  # OK
# set_mode("delete")  # Error

# Combined with Union
Status = Literal["pending", "approved", "rejected"]

def process_status(status: Status) -> None:
    match status:
        case "pending":
            print("Processing...")
        case "approved":
            print("Approved!")
        case "rejected":
            print("Rejected")
```

### TypedDict — Structured Dictionaries

```python
from typing import TypedDict

class UserProfile(TypedDict):
    name: str
    age: int
    email: str
    is_active: bool

def create_user(name: str, age: int, email: str) -> UserProfile:
    return {
        "name": name,
        "age": age,
        "email": email,
        "is_active": True
    }

user = create_user("Alice", 30, "alice@example.com")
user["name"]  # Typed as str
user["age"]   # Typed as int
```

### NamedTuple

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    
    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

point = Point(3.0, 4.0)
print(point.x)  # 3.0
print(point[0])  # Also works (tuple indexing)
```

### NewType

```python
from typing import NewType

# Create distinct types for type safety
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def get_user(user_id: UserId) -> dict:
    return {"id": user_id}

# Type checker ensures correct usage
user_id = UserId(123)
order_id = OrderId(456)

get_user(user_id)   # OK
# get_user(order_id)  # Error: OrderId is not UserId
```

### TypeAlias

```python
from typing import TypeAlias

# Python 3.10+ TypeAlias
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]

def dot_product(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(x * y for x, y in zip(row, col)) 
             for col in zip(*b)] 
            for row in a]
```

---

## 6. Protocol — Structural Subtyping

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

def render(shape: Drawable) -> None:
    """Accepts any object with a draw() method."""
    print(shape.draw())

render(Circle())  # OK - Circle has draw()
render(Square())  # OK - Square has draw()

# Structural: doesn't need explicit inheritance
# Duck typing with type safety
```

### Protocol with Multiple Methods

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> None: ...

class ReadWriteFile:
    def read(self) -> str:
        return "file content"
    
    def write(self, data: str) -> None:
        print(f"Writing: {data}")

def copy_data(source: Readable, dest: Writable) -> None:
    data = source.read()
    dest.write(data)

copy_data(ReadWriteFile(), ReadWriteFile())
```

---

## 7. Type Hints with Decorators

```python
import functools
from typing import TypeVar, Callable, ParamSpec

P = ParamSpec("P")  # Preserves parameter types
R = TypeVar("R")    # Preserves return type

# Decorator that preserves function signature
def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

# Type checker knows add takes (int, int) -> int
result = add(3, 5)  # Type: int
# add("a", "b")  # Type error caught!
```

### Overloads

```python
from typing import overload

@overload
def process(value: int) -> int: ...

@overload
def process(value: str) -> str: ...

def process(value: int | str) -> int | str:
    if isinstance(value, int):
        return value * 2
    return value.upper()

# Type checker uses overloads to determine return type
result = process(5)      # Type: int
result = process("hi")  # Type: str
```

---

## 8. Type Checking with mypy/pyright

### Setup

```bash
# Install type checker
pip install mypy

# Run on file
mypy script.py

# Run on project
mypy src/
```

### mypy Configuration

```ini
# mypy.ini or setup.cfg
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
check_untyped_defs = True

# Per-module overrides
[mypy-tests.*]
ignore_errors = True
```

### Common mypy Errors

```python
# Error: Missing return type
def add(a, b):  # Error: Function is missing a return type annotation
    return a + b

# Error: Incompatible types
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet(42)  # Error: Argument 1 has incompatible type "int"; expected "str"

# Error: Missing type annotation
def process(data):  # Error: Function is missing a type annotation
    return data
```

---

## 9. Type Hints in AI Engineering

```python
from typing import Optional, Union, Protocol
import numpy as np

# Type aliases for ML
Tensor = np.ndarray
Vector = np.ndarray

class Model(Protocol):
    def predict(self, X: Tensor) -> Tensor: ...

def train_model(
    model: Model,
    X_train: Tensor,
    y_train: Tensor,
    epochs: int = 100,
    learning_rate: float = 0.001,
    validation_split: float = 0.2,
    callbacks: Optional[list] = None,
) -> dict[str, float]:
    """Train a model and return metrics."""
    history = {"loss": [], "accuracy": []}
    # Training logic...
    return history

def predict_batch(
    model: Model,
    data: Tensor,
    batch_size: int = 32,
    verbose: bool = False,
) -> Tensor:
    """Make predictions in batches."""
    predictions = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        pred = model.predict(batch)
        predictions.append(pred)
    return np.concatenate(predictions)
```

---

## 10. Best Practices

1. **Start with function signatures** — annotate return types and parameters
2. **Use built-in types** (`list`, `dict`) for Python 3.9+
3. **Use `Optional` for nullable values** instead of `Union[X, None]`
4. **Annotate class attributes** for clarity
5. **Use `TypeVar` for generic functions** that work with multiple types
6. **Use `Protocol` for duck typing** with type safety
7. **Run type checkers** in CI/CD pipelines
8. **Don't over-annotate** — skip obvious types like `self`
9. **Use `TYPE_CHECKING`** for import-only types
10. **Keep annotations up to date** — they're documentation

---

## 11. Practice Exercises

### Exercise 1: Annotate a Function
Add type hints to this function:

```python
def merge_dicts(dict1, dict2, override=True):
    # Add type hints here
    pass
```

### Exercise 2: Generic Function
Create a generic `filter_by_type` function:

```python
T = TypeVar("T")

def filter_by_type(items, target_type):
    # Should return list of items matching target_type
    pass
```

### Exercise 3: Protocol Definition
Define a `Serializable` protocol:

```python
class Serializable(Protocol):
    def to_json(self) -> str: ...
    @classmethod
    def from_json(cls, data: str) -> "Serializable": ...
```

### Exercise 4: TypedDict
Create a `ModelConfig` TypedDict with appropriate fields for ML model configuration.

### Exercise 5: Type-Safe Decorator
Create a decorator that preserves function signatures using `ParamSpec`.

---

## 12. Summary

| Concept | Description |
|---------|-------------|
| **Function Annotations** | `def func(x: int) -> str:` |
| **Variable Annotations** | `x: int = 5` |
| **`Optional[X]`** | `Union[X, None]` |
| **`Union[X, Y]`** | Value is X or Y |
| **`Callable`** | Function type annotation |
| **`TypeVar`** | Generic type variable |
| **`TypedDict`** | Structured dictionary type |
| **`Protocol`** | Structural subtyping |
| **`NewType`** | Distinct type wrappers |
| **`mypy`/`pyright`** | Static type checkers |

Type hints are a powerful tool for writing maintainable, well-documented Python code. They catch errors early, improve IDE support, and make code self-documenting — essential qualities for AI engineering projects that evolve rapidly and involve multiple contributors.

---

## Next Steps

In the next lecture, we'll explore **Dataclasses**, which combine type hints with automatic method generation for cleaner class definitions.
