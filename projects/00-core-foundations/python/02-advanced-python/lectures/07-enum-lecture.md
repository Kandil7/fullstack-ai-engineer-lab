# Advanced Python Lecture 07: Enums

## Topic Overview

Enums (Enumerations) provide a way to define a set of named constants that are distinct and self-documenting. Python's `enum` module (introduced in Python 3.4) offers multiple enum types for different use cases, from simple constant groups to complex state machines. Enums improve code readability, prevent invalid values, and enable pattern matching — essential for building robust, maintainable systems.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create basic enums using `enum.Enum`
2. Use different enum types (`IntEnum`, `Flag`, `IntFlag`)
3. Define auto-values with `auto()`
4. Implement custom methods on enums
5. Use enums for state machines and status codes
6. Combine enums with dataclasses
7. Apply enums to AI engineering patterns
8. Convert between enums and other types
9. Follow best practices for enum design
10. Handle common enum pitfalls

---

## 1. Basic Enums

### Creating Enums

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Access members
print(Color.RED)           # Color.RED
print(Color.RED.name)      # "RED"
print(Color.RED.value)     # 1

# Comparison
print(Color.RED == Color.RED)    # True
print(Color.RED == Color.BLUE)   # False

# Membership check
print(Color.RED in Color)  # True
```

### Enum Iteration

```python
from enum import Enum

class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

# Iterate over members
for direction in Direction:
    print(f"{direction.name} = {direction.value}")

# Get member by name
print(Direction["NORTH"])  # Direction.NORTH

# Get member by value
print(Direction["N"])      # Direction.NORTH

# List all members
print(list(Direction))
# [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
```

---

## 2. Enum Types

### `IntEnum` — Numeric Enums

```python
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Can be used as integers
print(Priority.HIGH > Priority.LOW)   # True
print(Priority.HIGH + 10)             # 13
print(sorted([Priority.CRITICAL, Priority.LOW]))
# [Priority.LOW, Priority.CRITICAL]

# Useful for comparisons
def process(priority: int) -> str:
    if priority >= Priority.HIGH:
        return "Urgent"
    return "Normal"

print(process(Priority.CRITICAL))  # "Urgent"
print(process(Priority.LOW))       # "Normal"
```

### `StrEnum` — String Enums (Python 3.11+)

```python
from enum import StrEnum

classHttpStatus(StrEnum):
    OK = "200"
    NOT_FOUND = "404"
    SERVER_ERROR = "500"

# Can be used as strings
print(f"Status: {HttpStatus.OK}")  # "Status: 200"
print(HttpStatus.OK.upper())       # "200"

# JSON serialization
import json
print(json.dumps({"status": HttpStatus.OK}))
# {"status": "200"}
```

### `Flag` and `IntFlag` — Bitwise Enums

```python
from enum import Flag, IntFlag

class Permission(Flag):
    READ = 1
    WRITE = 2
    EXECUTE = 4
    ALL = READ | WRITE | EXECUTE

# Bitwise operations
read_write = Permission.READ | Permission.WRITE
print(read_write)  # Permission.READ|WRITE

# Check membership
print(Permission.READ in read_write)   # True
print(Permission.EXECUTE in read_write)  # False

# Iteration over combined flags
for perm in read_write:
    print(perm.name)  # "READ", "WRITE"

# IntFlag allows integer operations
class FileMode(IntFlag):
    OWNER_READ = 0o400
    OWNER_WRITE = 0o200
    GROUP_READ = 0o040
    OTHER_READ = 0o004

mode = FileMode.OWNER_READ | FileMode.OWNER_WRITE
print(oct(mode))  # 0o600
```

---

## 3. Auto Values

```python
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()    # 1
    RUNNING = auto()    # 2
    COMPLETED = auto()  # 3
    FAILED = auto()     # 4

print(Status.PENDING.value)  # 1
print(Status.RUNNING.value)  # 2

# Custom auto with __init__
class Color(Enum):
    def __init__(self, rgb):
        self.rgb = rgb
    
    RED = auto(), (255, 0, 0)
    GREEN = auto(), (0, 255, 0)
    BLUE = auto(), (0, 0, 255)

print(Color.RED.rgb)  # (255, 0, 0)
print(Color.RED.value)  # 1 (auto-assigned)
```

---

## 4. Custom Methods on Enums

```python
from enum import Enum
import math

class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    
    def area(self, *dimensions):
        if self == Shape.CIRCLE:
            radius = dimensions[0]
            return math.pi * radius ** 2
        elif self == Shape.SQUARE:
            side = dimensions[0]
            return side ** 2
        elif self == Shape.TRIANGLE:
            base, height = dimensions
            return 0.5 * base * height
    
    @property
    def emoji(self):
        emojis = {
            "circle": "⭕",
            "square": "⬜",
            "triangle": "🔺"
        }
        return emojis[self.value]

# Usage
print(Shape.CIRCLE.area(5))       # 78.54
print(Shape.SQUARE.area(4))       # 16.0
print(Shape.CIRCLE.emoji)         # "⭕"
```

### Functional API

```python
from enum import Enum

# Create enum dynamically
Animal = Enum("Animal", ["CAT", "DOG", "BIRD"])

print(Animal.CAT)  # Animal.CAT
print(Animal.CAT.value)  # 1

# With custom values
Animal = Enum("Animal", {"CAT": "meow", "DOG": "woof", "BIRD": "tweet"})
print(Animal.CAT.value)  # "meow"
```

---

## 5. Enums in State Machines

```python
from enum import Enum, auto

class OrderState(Enum):
    CREATED = auto()
    PAYMENT_PENDING = auto()
    PAID = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    
    @property
    def is_terminal(self):
        return self in (OrderState.DELIVERED, OrderState.CANCELLED)
    
    @property
    def can_transition_to(self):
        transitions = {
            OrderState.CREATED: [OrderState.PAYMENT_PENDING, OrderState.CANCELLED],
            OrderState.PAYMENT_PENDING: [OrderState.PAID, OrderState.CANCELLED],
            OrderState.PAID: [OrderState.PROCESSING],
            OrderState.PROCESSING: [OrderState.SHIPPED],
            OrderState.SHIPPED: [OrderState.DELIVERED],
            OrderState.DELIVERED: [],
            OrderState.CANCELLED: [],
        }
        return transitions.get(self, [])

class Order:
    def __init__(self):
        self.state = OrderState.CREATED
    
    def transition(self, new_state):
        if new_state not in self.state.can_transition_to:
            raise ValueError(
                f"Cannot transition from {self.state} to {new_state}"
            )
        self.state = new_state

# Usage
order = Order()
order.transition(OrderState.PAYMENT_PENDING)
order.transition(OrderState.PAID)
order.transition(OrderState.PROCESSING)
print(order.state)  # OrderState.PROCESSING
```

---

## 6. Enums with Dataclasses

```python
from dataclasses import dataclass, field
from enum import Enum, auto

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

@dataclass
class LogEntry:
    message: str
    level: LogLevel
    timestamp: str = ""
    metadata: dict = field(default_factory=dict)

@dataclass
class Logger:
    name: str
    min_level: LogLevel = LogLevel.INFO
    entries: list[LogEntry] = field(default_factory=list)
    
    def log(self, level: LogLevel, message: str, **metadata):
        if level.value >= self.min_level.value:
            entry = LogEntry(
                message=message,
                level=level,
                metadata=metadata
            )
            self.entries.append(entry)

# Usage
logger = Logger("app", min_level=LogLevel.WARNING)
logger.log(LogLevel.DEBUG, "Debug message")    # Ignored
logger.log(LogLevel.WARNING, "Something happened")
logger.log(LogLevel.ERROR, "Critical failure")

for entry in logger.entries:
    print(f"[{entry.level.name}] {entry.message}")
# [WARNING] Something happened
# [ERROR] Critical failure
```

---

## 7. Enums in AI Engineering

### Model Types and Tasks

```python
from enum import Enum, auto

class ModelType(Enum):
    TRANSFORMER = auto()
    CNN = auto()
    RNN = auto()
    GAN = auto()
    VAE = auto()

class TaskType(Enum):
    CLASSIFICATION = auto()
    REGRESSION = auto()
    GENERATION = auto()
    EXTRACTION = auto()
    TRANSLATION = auto()

class TrainingStatus(Enum):
    NOT_STARTED = auto()
    LOADING_DATA = auto()
    PREPROCESSING = auto()
    TRAINING = auto()
    EVALUATING = auto()
    COMPLETED = auto()
    FAILED = auto()
    
    @property
    def progress_percentage(self):
        stages = list(TrainingStatus)
        index = stages.index(self)
        return int((index / (len(stages) - 1)) * 100)

@dataclass
class ModelConfig:
    model_type: ModelType
    task: TaskType
    status: TrainingStatus = TrainingStatus.NOT_STARTED
    hyperparameters: dict = field(default_factory=dict)
    
    def start_training(self):
        self.status = TrainingStatus.LOADING_DATA
    
    def update_status(self, new_status: TrainingStatus):
        print(f"Status: {self.status.name} -> {new_status.name}")
        self.status = new_status

# Usage
config = ModelConfig(
    model_type=ModelType.TRANSFORMER,
    task=TaskType.GENERATION,
    hyperparameters={"lr": 0.001, "epochs": 100}
)

config.start_training()
config.update_status(TrainingStatus.TRAINING)
print(f"Progress: {config.status.progress_percentage}%")
```

### API Response Codes

```python
from enum import IntEnum

class APIStatus(IntEnum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    RATE_LIMITED = 429
    SERVER_ERROR = 500

@dataclass
class APIResponse:
    status: APIStatus
    data: Any = None
    error: Optional[str] = None
    
    @property
    def is_success(self):
        return 200 <= self.status < 300
    
    @property
    def is_client_error(self):
        return 400 <= self.status < 500
    
    @property
    def is_server_error(self):
        return 500 <= self.status < 600

# Usage
response = APIResponse(status=APIStatus.SUCCESS, data={"users": []})
print(response.is_success)  # True
print(f"Status code: {response.status.value}")  # 200
```

---

## 8. Converting Between Enums

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Enum to value
value = Color.RED.value  # 1
name = Color.RED.name    # "RED"

# Value to Enum
color = Color(1)  # Color.RED
color = Color["RED"]  # Color.RED

# To dictionary
color_dict = {c.name: c.value for c in Color}
print(color_dict)  # {"RED": 1, "GREEN": 2, "BLUE": 3}

# List of values
values = [c.value for c in Color]
print(values)  # [1, 2, 3]

# JSON serialization
import json

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Custom serializer
def enum_serializer(obj):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

print(json.dumps({"status": Status.ACTIVE}, default=enum_serializer))
# {"status": "active"}
```

---

## 9. Best Practices

1. **Use `auto()`** for simple sequential values
2. **Prefer `Enum`** over class constants for related values
3. **Use `IntEnum`** when numeric comparison is needed
4. **Use `Flag`/`IntFlag`** for combinable options
5. **Add docstrings** to document enum purpose
6. **Keep enums small** and focused
7. **Use meaningful names** that describe the value's purpose
8. **Don't use enums** for unrelated constants
9. **Handle serialization** explicitly for JSON/APIs
10. **Consider `StrEnum`** (3.11+) for string-valued enums

---

## 10. Practice Exercises

### Exercise 1: Status Codes
Create an `HttpStatus` enum with appropriate methods:

```python
class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500
    
    @property
    def message(self):
        # Return human-readable message
        pass
    
    @property
    def is_error(self):
        pass
```

### Exercise 2: State Machine
Build a `TrafficLight` state machine with valid transitions:

```python
class TrafficLight(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    # Define valid transitions and timing
```

### Exercise 3: Permission Flags
Create a `Permission` flag enum with helper methods:

```python
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ADMIN = auto()
    
    def describe(self):
        # Return human-readable description
        pass
```

### Exercise 4: Data Pipeline Status
Create enums for a data pipeline with status tracking:

```python
class PipelineStage(Enum):
    EXTRACT = auto()
    TRANSFORM = auto()
    LOAD = auto()
    VALIDATE = auto()

class PipelineStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
```

---

## 11. Summary

| Concept | Description |
|---------|-------------|
| **`Enum`** | Basic enumeration type |
| **`IntEnum`** | Enum with integer values (comparable) |
| **`StrEnum`** | Enum with string values (3.11+) |
| **`Flag`/`IntFlag`** | Bitwise combinable enums |
| **`auto()`** | Automatic sequential values |
| **Custom methods** | Add behavior to enum members |
| **State machines** | Enums for valid states and transitions |
| **Iteration** | Enum members are iterable |
| **Lookup** | By name (`Enum["NAME"]`) or value (`Enum(value)`) |
| **Serialization** | Explicit conversion needed |

Enums are essential for writing clean, type-safe Python code. They prevent invalid values, make code self-documenting, and enable powerful patterns like state machines — all critical for building reliable AI engineering systems.

---

## Next Steps

In the next lecture, we'll explore **Abstract Base Classes (ABCs)**, which define interfaces that enums can implement.
