# Lecture 13: Slots

## Topic Overview

`__slots__` is a Python mechanism for memory optimization that prevents dynamic attribute creation and reduces memory overhead per instance. By restricting attributes to a predefined list, slots eliminate the `__dict__` dictionary from instances, resulting in faster attribute access and lower memory usage.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand how __slots__ works** at the memory level
2. **Compare memory usage** with and without slots
3. **Implement __slots__** correctly in classes
4. **Handle inheritance** with slots
5. **Combine slots with properties**
6. **Benchmark performance** differences
7. **Know when to use slots** and when to avoid them

---

## Key Concepts

### 1. Basic __slots__

Slots restrict instance attributes to a predefined set, preventing dynamic attribute creation.

#### Simple Example

```python
class PointRegular:
    """Regular class without __slots__."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    """Class with __slots__ for memory efficiency."""
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Regular class
regular = PointRegular(1, 2)
regular.z = 3  # Works - can add dynamic attributes
print(regular.z)  # 3

# Slotted class
slotted = PointSlots(1, 2)
try:
    slotted.z = 3  # AttributeError - cannot add dynamic attributes
except AttributeError as e:
    print(f"Error: {e}")  # 'PointSlots' object has no attribute 'z'
```

#### Key Differences

```python
import sys

regular = PointRegular(1, 2)
slotted = PointSlots(1, 2)

# Regular class has __dict__
print(f"Regular has __dict__: {hasattr(regular, '__dict__')}")
print(f"Regular __dict__: {regular.__dict__}")

# Slotted class has no __dict__
print(f"Slotted has __dict__: {hasattr(slotted, '__dict__')}")
print(f"Slotted __slots__: {PointSlots.__slots__}")

# Memory comparison
print(f"Regular size: {sys.getsizeof(regular)} bytes")
print(f"Slotted size: {sys.getsizeof(slotted)} bytes")
```

---

### 2. Memory Comparison

Slots significantly reduce memory usage, especially with many instances.

#### Single Instance Comparison

```python
import sys

class UserRegular:
    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

class UserSlots:
    __slots__ = ('id', 'name', 'email', 'age')
    
    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

regular = UserRegular(1, "Alice", "alice@email.com", 25)
slotted = UserSlots(1, "Alice", "alice@email.com", 25)

print(f"Regular: {sys.getsizeof(regular)} bytes")
print(f"Slotted: {sys.getsizeof(slotted)} bytes")
```

#### Large Scale Comparison

```python
import sys

def compare_memory(n=10000):
    regular_users = [
        UserRegular(i, f"user{i}", f"user{i}@email.com", 25)
        for i in range(n)
    ]
    slotted_users = [
        UserSlots(i, f"user{i}", f"user{i}@email.com", 25)
        for i in range(n)
    ]
    
    # Measure total memory
    regular_memory = sum(sys.getsizeof(u) for u in regular_users)
    slotted_memory = sum(sys.getsizeof(u) for u in slotted_users)
    
    # Measure __dict__ memory for regular users
    dict_memory = sum(sys.getsizeof(u.__dict__) for u in regular_users[:100])
    
    print(f"Regular users: ~{regular_memory:,} bytes")
    print(f"Slotted users: ~{slotted_memory:,} bytes")
    print(f"Savings: ~{regular_memory - slotted_memory:,} bytes")
    print(f"Regular __dict__ sample: ~{dict_memory:,} bytes")
    
    return regular_memory, slotted_memory

regular, slotted = compare_memory(10000)
print(f"Memory reduction: {(1 - slotted/regular)*100:.1f}%")
```

---

### 3. __slots__ with Inheritance

Handling inheritance with slots requires careful planning.

#### Basic Inheritance

```python
class Base:
    __slots__ = ('id',)
    
    def __init__(self, id):
        self.id = id

class Child(Base):
    __slots__ = ('name', 'value')  # Additional slots
    
    def __init__(self, id, name, value):
        super().__init__(id)
        self.name = name
        self.value = value

child = Child(1, "test", 3.14)
print(f"Child: id={child.id}, name={child.name}, value={child.value}")
print(f"Base slots: {Base.__slots__}")
print(f"Child slots: {Child.__slots__}")
print(f"Combined: {Base.__slots__ + Child.__slots__}")
```

#### Multi-Level Inheritance

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

guide = GuideDog("Labrador", "John")
print(f"Species: {guide.species}")
print(f"Breed: {guide.breed}")
print(f"Handler: {guide.handler}")
print(f"Animal slots: {Animal.__slots__}")
print(f"Dog slots: {Dog.__slots__}")
print(f"GuideDog slots: {GuideDog.__slots__}")
```

#### Common Mistake: Parent Without Slots

```python
class Parent:
    # No __slots__ defined
    pass

class Child(Parent):
    __slots__ = ('name',)
    
    def __init__(self, name):
        self.name = name

child = Child("test")
print(f"Child has __dict__: {hasattr(child, '__dict__')}")
# True - parent without slots means child still has __dict__
```

---

### 4. __slots__ with Properties

Slots and properties work together seamlessly.

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
    
    @property
    def circumference(self):
        return 2 * math.pi * self._radius

c = Circle(5)
print(f"Radius: {c.radius}")
print(f"Area: {c.area:.2f}")
print(f"Circumference: {c.circumference:.2f}")

c.radius = 10
print(f"New area: {c.area:.2f}")

try:
    c.radius = -5  # Validates via setter
except ValueError as e:
    print(f"Error: {e}")

# Verify no __dict__
print(f"Has __dict__: {hasattr(c, '__dict__')}")
print(f"Slots: {Circle.__slots__}")
```

---

### 5. Performance Benchmark

Slots provide faster attribute access in addition to memory savings.

```python
import time
import sys

class ItemRegular:
    def __init__(self, x, name):
        self.x = x
        self.name = name

class ItemSlots:
    __slots__ = ('x', 'name')
    
    def __init__(self, x, name):
        self.x = x
        self.name = name

def benchmark_class(cls, n=100000):
    """Benchmark object creation and attribute access."""
    # Creation time
    start = time.perf_counter()
    objects = [cls(i, f"item{i}") for i in range(n)]
    creation_time = time.perf_counter() - start
    
    # Access time
    start = time.perf_counter()
    total = sum(obj.x for obj in objects)
    access_time = time.perf_counter() - start
    
    return creation_time, access_time

# Run benchmarks
n = 100000
reg_create, reg_access = benchmark_class(ItemRegular, n)
slot_create, slot_access = benchmark_class(ItemSlots, n)

print(f"Regular - Create: {reg_create:.4f}s, Access: {reg_access:.4f}s")
print(f"Slots   - Create: {slot_create:.4f}s, Access: {slot_access:.4f}s")
print(f"Speedup - Create: {reg_create/slot_create:.2f}x, Access: {reg_access/slot_access:.2f}x")
```

---

### 6. __slots__ with Class Variables

Slots can work with class variables and methods.

```python
class Employee:
    __slots__ = ('name', 'salary', '_bonus')
    
    # Class variable (not in slots)
    company = "Acme Corp"
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        self._bonus = 0
    
    @property
    def total_compensation(self):
        return self.salary + self._bonus
    
    def set_bonus(self, amount):
        if amount < 0:
            raise ValueError("Bonus cannot be negative")
        self._bonus = amount
    
    def __repr__(self):
        return f"Employee({self.name!r}, ${self.salary:,})"

emp = Employee("Alice", 75000)
print(f"Company: {emp.company}")  # Class variable
print(f"Name: {emp.name}")        # Instance slot
print(f"Salary: ${emp.salary:,}") # Instance slot
emp.set_bonus(10000)
print(f"Total: ${emp.total_compensation:,}")

# Verify no __dict__
print(f"Has __dict__: {hasattr(emp, '__dict__')}")
print(f"Slots: {Employee.__slots__}")
print(f"Company in slots: {'company' in Employee.__slots__}")
```

---

## Common Mistakes to Avoid

### 1. Forgetting to Include All Attributes

```python
class Bad:
    __slots__ = ('x',)  # Only x is allowed
    
    def __init__(self, x, y):
        self.x = x
        self.y = y  # AttributeError!

# CORRECT
class Good:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### 2. Mixing Slots and __dict__

```python
class Base:
    __slots__ = ('x',)
    
class Child(Base):
    __slots__ = ('y',)  # No __dict__ slot
    
# If you need both:
class Flexible:
    __slots__ = ('x', '__dict__')  # Explicitly include __dict__
```

### 3. Inheritance Without Parent Slots

```python
class Parent:
    # No __slots__
    pass

class Child(Parent):
    __slots__ = ('y',)  # Won't help - parent has __dict__
    
child = Child()
child.x = 1  # Works because Parent has __dict__
child.y = 2
print(f"Has __dict__: {hasattr(child, '__dict__')}")  # True
```

### 4. Using Weak References with Slots

```python
import weakref

class Bad:
    __slots__ = ('x',)
    
    def __init__(self, x):
        self.x = x

# This fails:
try:
    obj = Bad(1)
    ref = weakref.ref(obj)
except TypeError as e:
    print(f"Error: {e}")  # Cannot create weak reference

# CORRECT - include __weakref__
class Good:
    __slots__ = ('x', '__weakref__')
    
    def __init__(self, x):
        self.x = x

obj = Good(1)
ref = weakref.ref(obj)
print(f"Reference works: {ref() is not None}")
```

---

## Best Practices

### 1. Use Slots for Data Classes with Many Instances

```python
# GOOD - many instances
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

points = [Point(i, i*2) for i in range(100000)]

# BAD - few instances, dynamic attributes needed
class Config:
    def __init__(self):
        self.settings = {}
    
    def __setattr__(self, name, value):
        self.settings[name] = value
```

### 2. Document Slot Constraints

```python
class User:
    """User with limited attributes for memory efficiency.
    
    Attributes (slots):
        id (int): User identifier
        name (str): User name
        email (str): User email
    
    Note: Cannot add dynamic attributes.
    """
    __slots__ = ('id', 'name', 'email')
    
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
```

### 3. Consider Alternatives

```python
# Alternative 1: Named tuple (immutable)
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

# Alternative 2: Dataclass with slots (Python 3.10+)
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float
```

---

## Practice Exercises

### Exercise 1: Memory Comparison
```python
"""
Create a script that compares memory usage of:
1. Regular class vs slots class (1000 instances)
2. Named tuple vs slots class
3. Dataclass vs slots class
"""
# Your code here
```

### Exercise 2: Slotted Product
```python
"""
Implement a Product class with __slots__ that includes:
- name, price, quantity (slots)
- Properties for total_value, discount_price
- Validation in setters
"""
class Product:
    # Your code here
    pass
```

### Exercise 3: Performance Benchmark
```python
"""
Benchmark and compare:
1. Object creation time
2. Attribute access time
3. Iteration time
Regular vs Slotted classes with 100000 instances
"""
# Your code here
```

---

## Summary

### Key Features of __slots__

| Feature | Description |
|---------|-------------|
| Memory reduction | Eliminates `__dict__` per instance |
| Faster access | Fixed attribute offsets |
| Restriction | Prevents dynamic attribute creation |
| Inheritance | Child classes need own `__slots__` |

### When to Use Slots

| Use Case | Recommendation |
|----------|----------------|
| Many instances (1000+) | ✅ Use slots |
| Few instances | ❌ Skip slots |
| Dynamic attributes needed | ❌ Use regular classes |
| Memory constrained | ✅ Use slots |
| Performance critical | ✅ Use slots |
| Need weak references | ⚠️ Include `__weakref__` |

### Key Takeaways

1. **Slots reduce memory** by eliminating `__dict__`
2. **Slots speed up access** with fixed attribute offsets
3. **Slots prevent dynamic attributes** for safety
4. **Inheritance requires care** - parent must have slots
5. **Consider alternatives** like namedtuple and dataclasses
6. **Not always worth it** - benchmark first

---

## Further Reading

- [Python __slots__ documentation](https://docs.python.org/3/reference/datamodel.html#slots)
- [Memory optimization guide](https://wiki.python.org/moin/UsingSlots)
- [Dataclasses with slots](https://docs.python.org/3/library/dataclasses.html)
