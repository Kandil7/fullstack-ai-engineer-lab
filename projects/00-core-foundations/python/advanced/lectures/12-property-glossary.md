# Glossary: Properties

## Quick Reference Table

| Term | Definition | Key Syntax | Purpose |
|------|------------|------------|---------|
| Property | Descriptor that manages attribute access | `@property` | Controlled attribute access |
| Getter | Method that returns attribute value | `@property` | Read access |
| Setter | Method that sets attribute value | `@name.setter` | Write access with validation |
| Deleter | Method that deletes attribute | `@name.deleter` | Cleanup/invalidation |
| Computed Property | Property that calculates value dynamically | `@property` | Derived values |
| Cached Property | Property that caches computed result | `@cached_property` | Performance optimization |
| Descriptor | Object defining __get__, __set__, __delete__ | Protocol | Property mechanism |
| Private Attribute | Attribute prefixed with underscore | `self._attr` | Convention for internal use |

---

## Alphabetical Definitions

### Computed Property

**Definition**: A property that calculates its value dynamically from other attributes or data, rather than storing a fixed value.

**Example**:
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def area(self):
        """Computed from width and height."""
        return self.width * self.height
    
    @property
    def perimeter(self):
        """Computed from width and height."""
        return 2 * (self.width + self.height)

r = Rectangle(5, 3)
print(r.area)      # 15 (computed)
print(r.perimeter)  # 16 (computed)
```

**Related Terms**: property, getter, dynamic calculation

**When to Use**:
- Values derived from other attributes
- Formatted representations
- Aggregated calculations

---

### Decorator

**Definition**: In the context of properties, a decorator (`@property`, `@name.setter`, `@name.deleter`) that transforms a method into an attribute-like access pattern.

**Example**:
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property  # Decorator creates getter
    def radius(self):
        return self._radius
    
    @radius.setter  # Decorator creates setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
```

**Related Terms**: property, method decorator, syntactic sugar

**Key Decorators**:
- `@property`: Creates getter method
- `@name.setter`: Creates setter method
- `@name.deleter`: Creates deleter method

---

### Descriptor

**Definition**: An object that defines `__get__`, `__set__`, or `__delete__` methods to customize attribute access. Properties are implemented using descriptors.

**Example**:
```python
class Property:
    """Simplified property descriptor."""
    
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

# Usage
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @Property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value
```

**Related Terms**: property, __get__, __set__, __delete__, data descriptor

**Types**:
- **Data Descriptor**: Defines both `__get__` and `__set__`
- **Non-data Descriptor**: Only defines `__get__`

---

### Getter

**Definition**: A method decorated with `@property` that defines how to retrieve an attribute's value.

**Example**:
```python
class User:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
    
    @property
    def full_name(self):
        """Getter for full name."""
        return f"{self._first_name} {self._last_name}"
    
    @property
    def email(self):
        """Getter for email."""
        return f"{self._first_name.lower()}@example.com"

user = User("John", "Doe")
print(user.full_name)  # John Doe (getter called)
print(user.email)      # john@example.com (getter called)
```

**Related Terms**: property, accessor, read-only

**Characteristics**:
- No parameters (except `self`)
- Returns the attribute value
- Can perform calculations
- Can add caching logic

---

### Private Attribute

**Definition**: An attribute prefixed with a single underscore (`_`) by convention, indicating it's for internal use and should not be accessed directly from outside the class.

**Example**:
```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance  # Private by convention
    
    @property
    def balance(self):
        """Public access to private balance."""
        return self._balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

account = BankAccount("Alice", 1000)
print(account.balance)    # OK (uses property)
print(account._balance)   # Works but discouraged
```

**Related Terms**: encapsulation, name mangling, convention

**Naming Conventions**:
- `_attr`: Protected (convention)
- `__attr`: Name mangling (class-private)
- `__attr__`: Dunder/magic (special methods)

---

### Property

**Definition**: A descriptor that provides a "managed attribute" on a class, allowing controlled access to an underlying attribute using getter, setter, and deleter methods.

**Example**:
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get the radius."""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set the radius with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """Delete the radius."""
        del self._radius

c = Circle(5)
print(c.radius)   # 5 (getter)
c.radius = 10     # setter called
del c.radius      # deleter called
```

**Related Terms**: descriptor, getter, setter, deleter, managed attribute

**Protocol Methods**:
- `__get__(self, obj, objtype=None)`: Return attribute value
- `__set__(self, obj, value)`: Set attribute value
- `__delete__(self, obj)`: Delete attribute
- `__set_name__(self, owner, name)`: Called when descriptor is created

---

### Setter

**Definition**: A method decorated with `@name.setter` that defines how to set an attribute's value, typically including validation logic.

**Example**:
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = None
        self.celsius = celsius  # Uses setter
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set temperature with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be numeric")
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

t = Temperature(100)
t.celsius = 37.5      # OK
t.celsius = -300      # ValueError
t.celsius = "hot"     # TypeError
```

**Related Terms**: property, validation, mutator

**Best Practices**:
- Always use setter in `__init__` to ensure validation
- Perform validation before assignment
- Raise descriptive exceptions for invalid values

---

### Cached Property

**Definition**: A property that computes its value only once and caches the result for subsequent accesses, improving performance for expensive calculations.

**Example**:
```python
from functools import cached_property
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @cached_property
    def area(self):
        """Expensive calculation, cached after first access."""
        print("Computing area...")
        return math.pi * self.radius ** 2

c = Circle(5)
print(c.area)  # "Computing area..." then 78.54
print(c.area)  # 78.54 (no computation)
```

**Related Terms**: property, caching, performance, memoization

**Implementation Options**:
1. `functools.cached_property` (Python 3.8+)
2. Manual caching with `_cache` attribute
3. Custom `cached_property` decorator

---

### Computed Attribute

**Definition**: An attribute whose value is calculated dynamically from other data, rather than stored as a fixed value.

**Example**:
```python
class Employee:
    def __init__(self, name, hourly_rate, hours_worked):
        self.name = name
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    
    @property
    def gross_pay(self):
        """Computed: hourly_rate * hours_worked"""
        return self.hourly_rate * self.hours_worked
    
    @property
    def tax(self):
        """Computed: 20% of gross pay"""
        return self.gross_pay * 0.20
    
    @property
    def net_pay(self):
        """Computed: gross_pay - tax"""
        return self.gross_pay - self.tax

emp = Employee("Alice", 25, 40)
print(emp.gross_pay)  # 1000 (computed)
print(emp.tax)        # 200 (computed)
print(emp.net_pay)    # 800 (computed)
```

**Related Terms**: property, derived value, calculation

---

## Concept Relationships

```
Properties
├── Descriptors (underlying mechanism)
│   ├── __get__() - getter
│   ├── __set__() - setter
│   └── __delete__() - deleter
│
├── Decorators (syntax)
│   ├── @property - defines getter
│   ├── @name.setter - defines setter
│   └── @name.deleter - defines deleter
│
├── Patterns
│   ├── Computed Properties
│   │   └── Calculate values dynamically
│   ├── Cached Properties
│   │   └── Cache expensive computations
│   ├── Validated Properties
│   │   └── Enforce constraints on values
│   └── Read-only Properties
│       └── No setter defined
│
└── Related Concepts
    ├── Encapsulation
    ├── Data Validation
    └── Performance Optimization
```

---

## When to Use Properties

| Use Case | Example | Why |
|----------|---------|-----|
| Validation | `@radius.setter` checks negative | Enforce constraints |
| Computed values | `@property def area(self)` | Derive from other data |
| Caching | `@cached_property` | Avoid redundant computation |
| Read-only access | `@property def balance(self)` | Protect internal state |
| Legacy interface | Same API, different implementation | Maintain compatibility |
| Logging/Debugging | Track attribute access | Monitor usage |

---

## Property vs Method

| Scenario | Use Property | Use Method |
|----------|--------------|------------|
| No arguments needed | `@property def name(self)` | |
| Simple computation | `@property def full_name(self)` | |
| Arguments required | | `def calculate_tax(self, rate)` |
| Side effects | | `def send_email(self)` |
| Unclear cost | | `def expensive_operation(self)` |
| Changing state | | `def reset(self)` |

---

## Common Patterns

### 1. Validation Pattern
```python
@property
def age(self):
    return self._age

@age.setter
def age(self, value):
    if not isinstance(value, int):
        raise TypeError("Age must be integer")
    if value < 0 or value > 150:
        raise ValueError("Age must be 0-150")
    self._age = value
```

### 2. Computed Value Pattern
```python
@property
def total_price(self):
    return self.price * self.quantity * (1 - self.discount)
```

### 3. Caching Pattern
```python
@cached_property
def expensive_computation(self):
    # Heavy calculation here
    return result
```

### 4. Read-Only Pattern
```python
@property
def id(self):
    return self._id
# No setter - read-only
```

### 5. Delegated Access Pattern
```python
@property
def name(self):
    return self._user.name

@name.setter
def name(self, value):
    self._user.name = value
```
