# Enums Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| `Enum` | Base class for creating enumerations |
| `IntEnum` | Enum with integer values, comparable to ints |
| `StrEnum` | Enum with string values (Python 3.11+) |
| `Flag` | Enum supporting bitwise operations |
| `IntFlag` | Flag with integer values |
| `auto()` | Automatic value assignment |
| Enum Member | A named constant in an enumeration |
| `.name` | The string name of an enum member |
| `.value` | The value of an enum member |
| `.member` | Access the enum class from a member |
| Functional API | Create enums dynamically with `Enum()` |
| Bitwise OR | `\|` operator for combining Flag members |
| Bitwise AND | `&` operator for checking Flag membership |
| State Machine | Enum representing valid states |
| Serialization | Converting enums to/from other types |
| JSON | Common serialization format for enums |
| Pattern Matching | Using enums in `match` statements |
| Docstring | Documentation for enum members |

---

## Detailed Definitions

### `auto()`

**Definition**: A function that automatically assigns the next available value to an enum member. Works with integers by default, but can be customized.

**Example**:
```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()    # 1
    GREEN = auto()  # 2
    BLUE = auto()   # 3

# Custom auto with __init__
class Format(Enum):
    def __init__(self, mime_type):
        self.mime_type = mime_type
    
    JSON = auto(), "application/json"
    XML = auto(), "application/xml"
    CSV = auto(), "text/csv"

print(Format.JSON.mime_type)  # "application/json"
```

**Related**: `Enum`, Value Assignment

---

### Bitwise AND

**Definition**: The `&` operator used to check if a Flag enum member contains specific flags.

**Example**:
```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

perms = Permission.READ | Permission.WRITE

# Check if READ is set
print(bool(perms & Permission.READ))   # True
print(bool(perms & Permission.EXECUTE))  # False

# Intersection
both = Permission.READ & Permission.READ  # Permission.READ
```

**Related**: Bitwise OR, Flag, Permission Checking

---

### Bitwise OR

**Definition**: The `|` operator used to combine Flag enum members into composite values.

**Example**：
```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()    # 1
    WRITE = auto()   # 2
    EXECUTE = auto() # 4

# Combine flags
read_write = Permission.READ | Permission.WRITE
print(read_write)  # Permission.READ|WRITE

# All permissions
all_perms = Permission.READ | Permission.WRITE | Permission.EXECUTE
print(all_perms)  # Permission.READ|WRITE|EXECUTE

# Iterate combined flags
for perm in read_write:
    print(perm.name)  # "READ", "WRITE"
```

**Related**: Bitwise AND, Flag, Combining Flags

---

### `.name`

**Definition**: A read-only attribute of an enum member that returns its string name.

**Example**:
```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED.name)  # "RED"
print(Color.GREEN.name)  # "GREEN"

# Useful for logging
for color in Color:
    print(f"Color: {color.name}")
```

**Related**: `.value`, Enum Member, String Representation

---

### `.value`

**Definition**: A read-only attribute of an enum member that returns its assigned value.

**Example**:
```python
from enum import Enum, auto

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = auto()

print(Status.ACTIVE.value)   # "active"
print(Status.PENDING.value)  # 1

# Comparison with values
print(Status.ACTIVE.value == "active")  # True
```

**Related**: `.name`, Enum Member, Value Comparison

---

### `.member`

**Definition**: A property that returns the enum class itself when accessed from an instance. Useful for type checking.

**Example**:
```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Access enum class from member
print(Color.RED.__class__)  # <enum 'Color'>
print(type(Color.RED))      # <enum 'Color'>

# Member iteration
for member in Color:
    print(f"{member.name}: {member.value}")
```

**Related**: `.name`, `.value`, Type Checking

---

### Bitwise Operations

**Definition**: Operations (`|`, `&`, `^`, `~`) supported by `Flag` and `IntFlag` enums for combining and checking flags.

**Example**:
```python
from enum import IntFlag, auto

class FileMode(IntFlag):
    READ = auto()    # 1
    WRITE = auto()   # 2
    EXECUTE = auto() # 4

# OR: combine
rw = FileMode.READ | FileMode.WRITE
print(oct(rw))  # 0o3

# AND: check
print(bool(rw & FileMode.READ))    # True
print(bool(rw & FileMode.EXECUTE))  # False

# XOR: toggle
toggled = rw ^ FileMode.READ
print(toggled)  # FileMode.WRITE

# NOT: invert
inverted = ~FileMode.READ
print(inverted)  # FileMode.WRITE|EXECUTE
```

**Related**: Flag, IntFlag, Permission Systems

---

### Enum Member

**Definition**: A named constant within an enumeration class, created by assigning a value to a class attribute.

**Example**:
```python
from enum import Enum, auto

class Planet(Enum):
    MERCURY = auto()
    VENUS = auto()
    EARTH = auto()
    MARS = auto()

# Access member
earth = Planet.EARTH
print(earth)        # Planet.EARTH
print(earth.name)   # "EARTH"
print(earth.value)  # 3

# Members are singletons
print(Planet.EARTH is Planet.EARTH)  # True
```

**Related**: `.name`, `.value`, Enum Class

---

### Enum Iteration

**Definition**: The ability to loop over all members of an enum class, which preserves definition order.

**Example**：
```python
from enum import Enum

class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

# Iterate all members
for season in Season:
    print(f"{season.name}: {season.value}")

# Membership test
print("spring" in [s.value for s in Season])  # True
print(Season.SPRING in Season)  # True

# Get length
print(len(Season))  # 4
```

**Related**: Enum Class, Membership Testing

---

### Functional API

**Definition**: A way to create enums dynamically using `Enum()` constructor instead of class syntax.

**Example**:
```python
from enum import Enum

# Basic functional API
Color = Enum("Color", ["RED", "GREEN", "BLUE"])
print(Color.RED)  # Color.RED

# With explicit values
Animal = Enum("Animal", {"CAT": "meow", "DOG": "woof"})
print(Animal.CAT.value)  # "meow"

# With auto
Status = Enum("Status", "PENDING RUNNING COMPLETED FAILED")
print(Status.PENDING.value)  # 1
```

**Related**: Dynamic Enums, Runtime Creation

---

### Flag

**Definition**: An enum type where members can be combined using bitwise operations. Members represent individual flags that can be OR'd together.

**Example**：
```python
from enum import Flag, auto

class Feature(Flag):
    DARK_MODE = auto()
    NOTIFICATIONS = auto()
    SYNC = auto()
    ANALYTICS = auto()

# Single flags
print(Feature.DARK_MODE)  # Feature.DARK_MODE

# Combined flags
user_prefs = Feature.DARK_MODE | Feature.SYNC
print(user_prefs)  # Feature.DARK_MODE|SYNC

# Check membership
print(Feature.DARK_MODE in user_prefs)  # True
print(Feature.ANALYTICS in user_prefs)  # False

# Iterate over combined flags
for flag in user_prefs:
    print(flag.name)  # "DARK_MODE", "SYNC"
```

**Related**: IntFlag, Bitwise Operations, Permission Systems

---

### Functional API

**Definition**: See "Functional API". Using `Enum()` constructor to create enums dynamically.

**Example**：
```python
from enum import Enum

# Create from list
Size = Enum("Size", ["SMALL", "MEDIUM", "LARGE"])
print(Size.MEDIUM)  # Size.MEDIUM

# Create from dict
Weekday = Enum("Weekday", {
    "MONDAY": 0,
    "TUESDAY": 1,
    "WEDNESDAY": 2
})
print(Weekday.MONDAY.value)  # 0
```

**Related**: Dynamic Enums, Runtime Creation

---

### IntEnum

**Definition**: An enum type where members are also integers, allowing direct numeric comparisons and operations.

**Example**：
```python
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Numeric operations
print(Priority.HIGH + 10)  # 13
print(Priority.HIGH > Priority.LOW)  # True

# Use as integer
def process(priority: int) -> str:
    if priority >= Priority.HIGH:
        return "Urgent"
    return "Normal"

print(process(Priority.CRITICAL))  # "Urgent"
print(4)  # 4
```

**Related**: Enum, Integer Comparison

---

### JSON Serialization

**Definition**: Converting enum members to/from JSON format, requiring explicit handling since enums aren't natively JSON serializable.

**Example**:
```python
from enum import Enum
import json

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Custom serializer
def enum_serializer(obj):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Cannot serialize {type(obj)}")

# Serialize
data = {"status": Status.ACTIVE}
json_str = json.dumps(data, default=enum_serializer)
print(json_str)  # {"status": "active"}

# Deserialize
data = json.loads(json_str)
status = Status(data["status"])
print(status)  # Status.ACTIVE
```

**Related**: Serialization, API Integration, Custom Encoder

---

### Pattern Matching

**Definition**: Using enums in Python 3.10+ `match` statements for clean conditional logic.

**Example**：
```python
from enum import Enum

class Command(Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"

def handle_command(cmd: Command):
    match cmd:
        case Command.START:
            print("Starting...")
        case Command.STOP:
            print("Stopping...")
        case Command.PAUSE:
            print("Pausing...")
        case Command.RESUME:
            print("Resuming...")

handle_command(Command.START)  # "Starting..."
```

**Related**: Match Statement, Control Flow

---

### State Machine

**Definition**: A system that can be in exactly one state at a time, with transitions between states governed by rules. Enums are ideal for defining states.

**Example**：
```python
from enum import Enum, auto

class OrderState(Enum):
    CREATED = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    
    @property
    def is_terminal(self):
        return self in {OrderState.DELIVERED, OrderState.CANCELLED}
    
    @property
    def next_states(self):
        transitions = {
            OrderState.CREATED: {OrderState.PAID, OrderState.CANCELLED},
            OrderState.PAID: {OrderState.SHIPPED},
            OrderState.SHIPPED: {OrderState.DELIVERED},
            OrderState.DELIVERED: set(),
            OrderState.CANCELLED: set(),
        }
        return transitions[self]

class Order:
    def __init__(self):
        self.state = OrderState.CREATED
    
    def transition(self, new_state):
        if new_state not in self.state.next_states:
            raise ValueError(f"Invalid transition: {self.state} -> {new_state}")
        self.state = new_state

order = Order()
order.transition(OrderState.PAID)
order.transition(OrderState.SHIPPED)
print(order.state)  # OrderState.SHIPPED
```

**Related**: Enum, Transitions, Valid States

---

### Serialization

**Definition**: The process of converting enum members to a storable/transmittable format (strings, numbers, JSON).

**Example**：
```python
from enum import Enum
import json

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# To string
color_str = Color.RED.name  # "RED"

# To value
color_val = Color.RED.value  # 1

# To dict
color_dict = {c.name: c.value for c in Color}
print(color_dict)  # {"RED": 1, "GREEN": 2, "BLUE": 3}

# JSON with custom encoder
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

data = {"color": Color.RED}
print(json.dumps(data, cls=EnumEncoder))  # {"color": 1}
```

**Related**: JSON, API, Data Persistence

---

### StrEnum

**Definition**: An enum type (Python 3.11+) where members are also strings, useful for JSON and string-based operations.

**Example**：
```python
from enum import StrEnum

classHttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

# String operations
print(HttpMethod.GET.upper())  # "GET"
print(f"Method: {HttpMethod.POST}")  # "Method: POST"

# JSON serialization (native)
import json
print(json.dumps({"method": HttpMethod.GET}))  # {"method": "GET"}

# Comparison with strings
print(HttpMethod.GET == "GET")  # True
```

**Related**: Enum, String Operations, JSON

---

### Docstring

**Definition**: Documentation string for enum classes or individual members, explaining the purpose and usage.

**Example**：
```python
from enum import Enum

class LogLevel(Enum):
    """Logging levels for application output."""
    
    DEBUG = "DEBUG"
    """Detailed debug information for developers."""
    
    INFO = "INFO"
    """General information about system operation."""
    
    WARNING = "WARNING"
    """Potential issues that don't prevent operation."""
    
    ERROR = "ERROR"
    """Serious problems that affect functionality."""

# Access docstrings
print(LogLevel.__doc__)  # "Logging levels..."
print(LogLevel.DEBUG.__doc__)  # "Detailed debug..."
```

**Related**: Documentation, Code Clarity

---

### `.value`

**Definition**: See ".value". The attribute returning the enum member's assigned value.

**Example**：
```python
from enum import Enum, auto

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = auto()

print(Status.ACTIVE.value)    # "active"
print(Status.PENDING.value)   # 1

# Use in comparisons
if Status.ACTIVE.value == "active":
    print("Active status")
```

**Related**: `.name`, Value Access

---

### `__contains__`

**Definition**: A method that enables the `in` operator for checking enum membership.

**Example**：
```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Membership test
print(Color.RED in Color)  # True
print(1 in Color)  # True (checks values)

# With Flag
from enum import Flag, auto

class Permission(Flag):
    READ = auto()
    WRITE = auto()

perms = Permission.READ | Permission.WRITE
print(Permission.READ in perms)  # True
```

**Related**: Membership Testing, `in` Operator

---
