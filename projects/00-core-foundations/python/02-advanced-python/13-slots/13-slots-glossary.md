# Glossary: Slots

## Quick Reference Table

| Term | Definition | Key Syntax | Purpose |
|------|------------|------------|---------|
| __slots__ | Class attribute defining allowed instance attributes | `__slots__ = ('x', 'y')` | Memory optimization |
| __dict__ | Dictionary storing instance attributes | `obj.__dict__` | Dynamic attribute storage |
| Data Descriptor | Descriptor with __get__ and __set__ | `@property` | Attribute access control |
| Weak Reference | Reference that doesn't prevent garbage collection | `weakref.ref(obj)` | Memory management |
| Fixed Offset | Memory location for slot attribute | C-level implementation | Fast access |
| Named Tuple | Immutable tuple with named fields | `namedtuple()` | Lightweight alternative |
| Dataclass | Class with auto-generated methods | `@dataclass` | Modern alternative |
| Memory Overhead | Extra memory for object storage | `sys.getsizeof()` | Measurement |

---

## Alphabetical Definitions

### Class Variable

**Definition**: A variable defined inside a class but outside any method, shared by all instances. Class variables are NOT affected by `__slots__`.

**Example**:
```python
class Employee:
    __slots__ = ('name', 'salary')  # Instance slots
    company = "Acme Corp"  # Class variable
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

emp1 = Employee("Alice", 75000)
emp2 = Employee("Bob", 80000)

print(emp1.company)  # Acme Corp
print(emp2.company)  # Acme Corp

emp1.company = "New Corp"  # Creates instance attribute (shadowing)
print(emp2.company)  # Still Acme Corp
```

**Related Terms**: instance variable, class attribute, slot

---

### Data Descriptor

**Definition**: A descriptor that implements both `__get__` and `__set__` methods, taking precedence over instance attributes in attribute lookup.

**Example**:
```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(f"_{self.name}")
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Must be positive")
        obj.__dict__[f"_{self.name}"] = value

class Circle:
    radius = Validated()
    
    def __init__(self, r):
        self.radius = r  # Uses descriptor __set__

c = Circle(5)
print(c.radius)  # Uses descriptor __get__
c.radius = 10    # Uses descriptor __set__
```

**Related Terms**: property, __get__, __set__, attribute lookup

---

### Fixed Offset

**Definition**: A memory offset calculated at class creation time for each slot, allowing direct memory access without dictionary lookup.

**Example**:
```python
import sys

class WithSlots:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class WithoutSlots:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

s = WithSlots(1, 2, 3)
r = WithoutSlots(1, 2, 3)

print(f"With slots: {sys.getsizeof(s)} bytes")
print(f"Without slots: {sys.getsizeof(r)} bytes")
# With slots is smaller because no __dict__
```

**Related Terms**: memory layout, __slots__, performance

---

### __dict__

**Definition**: A dictionary that stores an object's writable attributes. Classes without `__slots__` automatically create `__dict__` for each instance.

**Example**:
```python
class Regular:
    def __init__(self, x):
        self.x = x
        self.y = x * 2

obj = Regular(5)
print(obj.__dict__)  # {'x': 5, 'y': 10}
print(obj.x)         # 5 (from __dict__)

# Adding dynamic attribute
obj.z = 15
print(obj.__dict__)  # {'x': 5, 'y': 10, 'z': 15}
```

**Related Terms**: attribute storage, dynamic attributes, memory overhead

**Memory Cost**:
```python
import sys

class Empty: pass

obj = Empty()
print(f"Empty object: {sys.getsizeof(obj)} bytes")
print(f"Empty __dict__: {sys.getsizeof(obj.__dict__)} bytes")
# __dict__ adds significant memory overhead
```

---

### __slots__

**Definition**: A class attribute that defines the allowed instance attributes, preventing dynamic attribute creation and eliminating the per-instance `__dict__`.

**Example**:
```python
class Point:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x, p.y)  # 1 2

# No __dict__
print(hasattr(p, '__dict__'))  # False

# Cannot add dynamic attributes
try:
    p.z = 3
except AttributeError:
    print("Cannot add z - not in __slots__")
```

**Related Terms**: memory optimization, attribute restriction, __dict__

**Syntax Options**:
```python
# Tuple (immutable)
__slots__ = ('x', 'y')

# List (also works)
__slots__ = ['x', 'y']

# Single attribute
__slots__ = ('x',)
```

---

### Inheritance

**Definition**: In the context of slots, inheritance requires that each class in the hierarchy defines its own `__slots__` for its specific attributes.

**Example**:
```python
class Animal:
    __slots__ = ('species',)
    
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    __slots__ = ('breed',)
    
    def __init__(self, breed):
        super().__init__("Canine")
        self.breed = breed

class GuideDog(Dog):
    __slots__ = ('handler',)
    
    def __init__(self, breed, handler):
        super().__init__(breed)
        self.handler = handler

# All slots are accessible
gd = GuideDog("Labrador", "John")
print(gd.species)   # Canine
print(gd.breed)     # Labrador
print(gd.handler)   # John

# Combined slots
print(Animal.__slots__)  # ('species',)
print(Dog.__slots__)     # ('breed',)
print(GuideDog.__slots__) # ('handler',)
```

**Related Terms**: MRO, parent class, child class

---

### Memory Overhead

**Definition**: The extra memory required to store an object beyond its actual data. Slots reduce this overhead by eliminating `__dict__`.

**Example**:
```python
import sys

class Regular:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Slotted:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

r = Regular(1, 2)
s = Slotted(1, 2)

print(f"Regular overhead: {sys.getsizeof(r)} bytes")
print(f"Slotted overhead: {sys.getsizeof(s)} bytes")
print(f"Savings per instance: {sys.getsizeof(r) - sys.getsizeof(s)} bytes")

# For 1 million instances:
n = 1_000_000
savings = (sys.getsizeof(r) - sys.getsizeof(s)) * n
print(f"Savings for {n:,} instances: ~{savings:,} bytes")
```

**Related Terms**: memory optimization, __dict__, performance

---

### Named Tuple

**Definition**: A tuple subclass with named fields, providing a lightweight immutable alternative to classes with slots.

**Example**:
```python
from collections import namedtuple
import sys

# Named tuple
PointNT = namedtuple('Point', ['x', 'y'])

# Slots class
class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

nt = PointNT(1, 2)
sl = PointSlots(1, 2)

print(f"Named tuple: {sys.getsizeof(nt)} bytes")
print(f"Slots class: {sys.getsizeof(sl)} bytes")

# Named tuple is immutable
try:
    nt.x = 3
except AttributeError:
    print("Named tuple is immutable")

# Slots class is mutable
sl.x = 3
print(f"Slots mutable: {sl.x}")
```

**Related Terms**: tuple, immutable, lightweight, slots

**When to Use**:
- Use namedtuple for immutable records
- Use slots for mutable objects with many instances

---

### Object Pool

**Definition**: A design pattern that reuses objects instead of creating new ones, often combined with slots for memory efficiency.

**Example**:
```python
class PooledObject:
    __slots__ = ('_in_use', '_data')
    
    def __init__(self):
        self._in_use = False
        self._data = None
    
    def acquire(self, data):
        if self._in_use:
            raise RuntimeError("Object already in use")
        self._in_use = True
        self._data = data
        return self
    
    def release(self):
        self._in_use = False
        self._data = None

class ObjectPool:
    def __init__(self, size):
        self._pool = [PooledObject() for _ in range(size)]
        self._available = list(range(size))
    
    def acquire(self, data):
        if not self._available:
            raise RuntimeError("Pool exhausted")
        idx = self._available.pop()
        return self._pool[idx].acquire(data)
    
    def release(self, obj):
        idx = self._pool.index(obj)
        obj.release()
        self._available.append(idx)

pool = ObjectPool(3)
obj1 = pool.acquire("data1")
print(obj1._data)  # data1
pool.release(obj1)
```

**Related Terms**: memory management, reuse, slots

---

### Property

**Definition**: A descriptor that provides a managed attribute interface, commonly used with slots to add validation while maintaining memory efficiency.

**Example**:
```python
import math

class Circle:
    __slots__ = ('_radius',)
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.area)  # 78.539...

c.radius = 10
print(c.area)  # 314.159...

# Still has no __dict__
print(hasattr(c, '__dict__'))  # False
```

**Related Terms**: descriptor, getter, setter, validation

---

### Weak Reference

**Definition**: A reference that doesn't prevent garbage collection of the referenced object. Requires `__weakref__` slot when using slots.

**Example**:
```python
import weakref

class Bad:
    __slots__ = ('x',)
    def __init__(self, x):
        self.x = x

class Good:
    __slots__ = ('x', '__weakref__')
    def __init__(self, x):
        self.x = x

# Bad - no __weakref__
try:
    obj = Bad(1)
    ref = weakref.ref(obj)
except TypeError as e:
    print(f"Error: {e}")

# Good - has __weakref__
obj = Good(1)
ref = weakref.ref(obj)
print(f"Reference valid: {ref() is not None}")
print(f"Referent: {ref().x}")
```

**Related Terms**: garbage collection, memory management, __weakref__

---

## Concept Relationships

```
Slots
├── Memory Optimization
│   ├── Eliminates __dict__
│   ├── Fixed attribute offsets
│   └── Reduced memory per instance
│
├── Attribute Access
│   ├── Direct memory access (faster)
│   ├── No dynamic attribute creation
│   └── AttributeError for undefined attributes
│
├── Inheritance
│   ├── Each class defines own slots
│   ├── Parent slots accessible
│   └── Child cannot add parent's slots
│
├── Related Concepts
│   ├── Properties (can combine)
│   ├── Weak References (need __weakref__)
│   └── Named Tuples (alternative)
│
└── Trade-offs
    ├── ✅ Less memory
    ├── ✅ Faster access
    ├── ✅ Prevents typos
    ├── ❌ Less flexible
    ├── ❌ No dynamic attributes
    └── ❌ More complex inheritance
```

---

## When to Use Slots

| Scenario | Use Slots? | Why |
|----------|------------|-----|
| Many instances (1000+) | ✅ Yes | Memory savings compound |
| Few instances | ❌ No | Overhead not worth it |
| Dynamic attributes needed | ❌ No | Slots prevent this |
| Memory constrained | ✅ Yes | Reduces footprint |
| Performance critical | ✅ Yes | Faster attribute access |
| Need weak references | ⚠️ Maybe | Include `__weakref__` |
| Simple data holder | ⚠️ Maybe | Consider namedtuple |

---

## Memory Comparison

| Type | Memory (approx) | Notes |
|------|-----------------|-------|
| Regular class instance | 48+ bytes | Includes __dict__ pointer |
| __dict__ (empty) | 64 bytes | Dictionary overhead |
| __dict__ (with attrs) | 120+ bytes | Grows with attributes |
| Slot instance | 16-32 bytes | No __dict__ |
| Named tuple | 48-64 bytes | Tuple overhead |

---

## Common Patterns

### 1. Data Class Pattern
```python
class Point:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
```

### 2. Entity Pattern
```python
class User:
    __slots__ = ('id', 'name', 'email', '_active')
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self._active = True
```

### 3. Component Pattern (Game Engine)
```python
class Position:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

class Velocity:
    __slots__ = ('dx', 'dy', 'dz')
    def __init__(self, dx=0, dy=0, dz=0):
        self.dx, self.dy, self.dz = dx, dy, dz
```

### 4. Cache Entry Pattern
```python
class CacheEntry:
    __slots__ = ('key', 'value', '_expiry', '_hits')
    def __init__(self, key, value, expiry):
        self.key = key
        self.value = value
        self._expiry = expiry
        self._hits = 0
```

### 5. Node Pattern (Linked List)
```python
class Node:
    __slots__ = ('data', 'next')
    def __init__(self, data):
        self.data = data
        self.next = None
```
