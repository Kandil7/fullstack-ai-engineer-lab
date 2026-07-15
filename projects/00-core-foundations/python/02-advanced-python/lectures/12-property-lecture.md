# Lecture 12: Properties

## Topic Overview

Properties provide a Pythonic way to manage attribute access on classes. They allow you to define methods that are accessed like attributes, enabling controlled access to private data with getters, setters, and computed values.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement property getters** for controlled attribute access
2. **Create property setters** with validation logic
3. **Build computed properties** that derive values from other attributes
4. **Use property caching** for expensive computations
5. **Apply property deletion** for cache invalidation
6. **Understand the property descriptor protocol**
7. **Choose between properties and regular methods**

---

## Key Concepts

### 1. Basic Property

Properties use decorators to define getter, setter, and deleter methods that are accessed like attributes.

#### Simple Property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius  # Use setter for validation
    
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
    
    @property
    def area(self):
        """Computed property - area."""
        return 3.14159 * self._radius ** 2

# Usage
c = Circle(5)
print(c.radius)    # 5 (getter)
print(c.area)      # 78.53975 (computed)
c.radius = 10      # setter (validated)
print(c.area)      # 314.159
```

#### Read-Only Property

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance
    
    @property
    def balance(self):
        """Read-only property - no setter defined."""
        return self._balance

account = BankAccount(1000)
print(account.balance)  # 1000

try:
    account.balance = 2000  # AttributeError
except AttributeError as e:
    print(f"Error: {e}")  # can't set attribute
```

---

### 2. Property with Validation

Properties are ideal for enforcing validation rules on attribute access.

#### Temperature Example

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = None
        self.celsius = celsius  # Use setter for validation
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self):
        return self._celsius + 273.15

# Usage
t = Temperature(100)
print(f"{t.celsius}°C = {t.fahrenheit}°F = {t.kelvin}K")
# 100°C = 212.0°F = 373.15K

t.fahrenheit = 32  # Converts to celsius automatically
print(f"{t.celsius}°C")  # 0.0°C
```

#### User Input Validation

```python
class User:
    def __init__(self, name, email, age):
        self.name = name  # Uses setter
        self.email = email
        self.age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        self._name = value.strip().title()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value.lower()
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

# Usage
user = User("alice", "Alice@Example.COM", 25)
print(f"{user.name}, {user.email}, {user.age}")
# Alice, alice@example.com, 25
```

---

### 3. Computed Properties

Computed properties calculate their value dynamically from other attributes.

#### Financial Example

```python
class Product:
    def __init__(self, name, price, quantity, discount=0):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.discount = discount
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    
    @property
    def discount_amount(self):
        return self.subtotal * (self.discount / 100)
    
    @property
    def total(self):
        return self.subtotal - self.discount_amount
    
    @property
    def margin(self):
        if self.price == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100

# Usage
product = Product("Widget", 10.00, 5, 10)
print(f"Subtotal: ${product.subtotal}")      # $50.00
print(f"Discount: ${product.discount_amount}") # $5.00
print(f"Total: ${product.total}")            # $45.00
```

---

### 4. Property with Caching

Cache expensive computations using properties to avoid redundant calculations.

#### Manual Caching

```python
class DataAnalyzer:
    def __init__(self, data):
        self._data = data
        self._sorted_cache = None
        self._stats_cache = None
    
    @property
    def sorted_data(self):
        """Sort data only once."""
        if self._sorted_cache is None:
            print("Sorting data (first access)...")
            self._sorted_cache = sorted(self._data)
        return self._sorted_cache
    
    @property
    def statistics(self):
        """Compute statistics only once."""
        if self._stats_cache is None:
            print("Computing statistics (first access)...")
            self._stats_cache = {
                "count": len(self._data),
                "min": min(self._data),
                "max": max(self._data),
                "mean": sum(self._data) / len(self._data),
            }
        return self._stats_cache
    
    def invalidate_cache(self):
        """Clear all cached values."""
        self._sorted_cache = None
        self._stats_cache = None

# Usage
analyzer = DataAnalyzer([3, 1, 4, 1, 5, 9, 2, 6])
print(analyzer.sorted_data)  # Computes
print(analyzer.sorted_data)  # Uses cache
print(analyzer.statistics)   # Computes
```

#### Using functools.cached_property

```python
from functools import cached_property
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @cached_property
    def area(self):
        """Automatically cached after first access."""
        print("Computing area...")
        return math.pi * self.radius ** 2
    
    @cached_property
    def circumference(self):
        print("Computing circumference...")
        return 2 * math.pi * self.radius

# Usage
c = Circle(5)
print(c.area)  # Computes
print(c.area)  # Uses cache (no print)
```

---

### 5. Property with Deletion

Properties can define deleter methods to handle attribute cleanup.

#### Cache Invalidation Pattern

```python
class CachedData:
    def __init__(self, data):
        self._data = data
        self._cache = {}
    
    @property
    def processed(self):
        if "processed" not in self._cache:
            print("Processing data...")
            self._cache["processed"] = [x * 2 for x in self._data]
        return self._cache["processed"]
    
    @processed.deleter
    def processed(self):
        print("Clearing processed cache")
        self._cache.pop("processed", None)

# Usage
data = CachedData([1, 2, 3])
print(data.processed)  # Computes
del data.processed     # Clears cache
print(data.processed)  # Recomputes
```

#### Resource Cleanup Pattern

```python
class DatabaseConnection:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._connection = None
    
    @property
    def connection(self):
        if self._connection is None:
            print(f"Connecting to {self._host}:{self._port}...")
            self._connection = f"Connection({self._host}:{self._port})"
        return self._connection
    
    @connection.deleter
    def connection(self):
        if self._connection is not None:
            print("Closing connection...")
            self._connection = None

# Usage
db = DatabaseConnection("localhost", 5432)
print(db.connection)  # Connects
del db.connection     # Closes
print(db.connection)  # Reconnects
```

---

### 6. Property Inheritance

Properties work correctly with inheritance.

```python
class Animal:
    def __init__(self, name, sound):
        self._name = name
        self._sound = sound
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return f"{self.name} says {self._sound}"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self._breed = breed
    
    @property
    def breed(self):
        return self._breed
    
    @property
    def description(self):
        # Override parent property
        return f"{self.name} ({self.breed}) says {self._sound}"

# Usage
dog = Dog("Rex", "German Shepherd")
print(dog.name)         # Rex (inherited getter)
print(dog.breed)        # German Shepherd (new getter)
print(dog.description)  # Rex (German Shepherd) says Woof (overridden)
```

---

## Common Mistakes to Avoid

### 1. Forgetting to Use Setter in __init__

```python
class BadCircle:
    def __init__(self, radius):
        self.radius = radius  # Calls setter
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

# WRONG - bypasses validation
class BadCircle2:
    def __init__(self, radius):
        self._radius = radius  # Direct assignment, no validation!

c = BadCircle2(-5)  # No error, but invalid state
```

### 2. Circular Property Calls

```python
class Bad:
    @property
    def value(self):
        return self.value  # Infinite recursion!

# CORRECT
class Good:
    @property
    def value(self):
        return self._value
```

### 3. Not Handling None Values

```python
class Bad:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        # Might fail if value is None
        self._value = value.upper()

# CORRECT
class Good:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value is not None:
            self._value = value.upper()
        else:
            self._value = None
```

---

## Best Practices

### 1. Use Properties for Validation

```python
class Config:
    @property
    def timeout(self):
        return self._timeout
    
    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Timeout must be numeric")
        if value <= 0:
            raise ValueError("Timeout must be positive")
        self._timeout = value
```

### 2. Cache Expensive Computations

```python
class DataProcessor:
    @cached_property
    def expensive_computation(self):
        # Only computed once, then cached
        return sum(x ** 2 for x in range(1000000))
```

### 3. Document Property Behavior

```python
class User:
    @property
    def email(self):
        """Get user email.
        
        Returns:
            str: Lowercase email address
            
        Note:
            Email is automatically lowercased on set
        """
        return self._email
```

### 4. Consider Using @property vs Methods

```python
# GOOD - simple computed value
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"

# BAD - method when no arguments needed
def get_full_name(self):
    return f"{self.first_name} {self.last_name}"

# GOOD - method when arguments needed
def calculate_tax(self, rate):
    return self.income * rate
```

---

## Practice Exercises

### Exercise 1: Email Validator
```python
class Email:
    """
    Implement Email class with properties that:
    - Validate email format
    - Auto-lowercase on set
    - Provide username and domain properties
    """
    def __init__(self, address):
        # Your code here
        pass
```

### Exercise 2: Cached Calculator
```python
class Calculator:
    """
    Implement Calculator with cached properties for:
    - factorial(n)
    - fibonacci(n)
    - prime_check(n)
    """
    def __init__(self, n):
        # Your code here
        pass
```

### Exercise 3: Configuration Manager
```python
class Config:
    """
    Implement Config with validated properties for:
    - host (non-empty string)
    - port (1-65535)
    - debug (boolean)
    - timeout (positive number)
    """
    def __init__(self, host, port, debug=False, timeout=30):
        # Your code here
        pass
```

---

## Summary

### Property Decorators

| Decorator | Purpose | Example |
|-----------|---------|---------|
| `@property` | Define getter | `@property def name(self): return self._name` |
| `@name.setter` | Define setter | `@name.setter def name(self, value): ...` |
| `@name.deleter` | Define deleter | `@name.deleter def name(self): ...` |

### When to Use Properties

| Use Case | Example |
|----------|---------|
| Validation | `@radius.setter` checks for negative values |
| Computed values | `@property def area(self): return π * r²` |
| Caching | `@cached_property def expensive(self): ...` |
| Read-only access | `@property def balance(self): return self._balance` |
| Encapsulation | Hide internal implementation details |

### Key Takeaways

1. **Properties provide controlled access** to attributes
2. **Use setters for validation** and data integrity
3. **Computed properties derive values** from other attributes
4. **Cache expensive computations** with `@cached_property`
5. **Properties work with inheritance** and can be overridden
6. **Choose properties over methods** when no arguments are needed

---

## Further Reading

- [Python property documentation](https://docs.python.org/3/library/functions.html#property)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [functools.cached_property](https://docs.python.org/3/library/functools.html#functools.cached_property)
