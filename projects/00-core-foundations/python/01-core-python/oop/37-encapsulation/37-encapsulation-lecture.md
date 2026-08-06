# Encapsulation in Python

## Topic 37: Hiding and Protecting Data

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of encapsulation
2. Implement access control with naming conventions
3. Use properties for controlled access
4. Apply getter/setter patterns
5. Understand Python's approach to privacy
6. Design encapsulated classes

---

## 1. What is Encapsulation?

Encapsulation bundles data (attributes) and methods that operate on that data into a single unit, while **restricting direct access** to some components.

### Why Encapsulate?

- **Data Protection**: Prevent invalid states
- **Controlled Access**: Validate input
- **Abstraction**: Hide implementation details
- **Maintainability**: Change internals without affecting users

### Python's Approach

Python uses naming conventions rather than strict access modifiers.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected (convention)
        self.__secret = "data"  # Name-mangled (pseudo-private)
```

---

## 2. Access Levels in Python

### Public

Accessible from anywhere.

```python
class MyClass:
    def __init__(self):
        self.public = "Anyone can see me"

obj = MyClass()
print(obj.public)  # Works fine
```

### Protected (Single Underscore)

Convention: internal use, not for external access.

```python
class MyClass:
    def __init__(self):
        self._protected = "Internal use"

obj = MyClass()
print(obj._protected)  # Works, but shouldn't be accessed
```

### Private (Double Underscore)

Name mangling: harder (not impossible) to access externally.

```python
class MyClass:
    def __init__(self):
        self.__private = "Really hidden"

obj = MyClass()
# print(obj.__private)  # AttributeError!
print(obj._MyClass__private)  # Works (name mangling)
```

---

## 3. Properties

Controlled access using `@property`.

### Basic Property

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius  # Protected attribute
    
    @property
    def celsius(self):
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Set temperature with validation."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit (read-only)."""
        return self._celsius * 9/5 + 32

# Usage
temp = Temperature(25)
print(temp.celsius)       # 25
print(temp.fahrenheit)    # 77.0

temp.celsius = 100        # Setter with validation
print(temp.fahrenheit)    # 212.0

# temp.fahrenheit = 212  # AttributeError: can't set (read-only)
```

### Computed Properties

```python
class Circle:
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
        """Computed property - calculated on access."""
        import math
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self):
        """Another computed property."""
        import math
        return 2 * math.pi * self._radius

c = Circle(5)
print(c.area)          # 78.53981633974483
print(c.circumference) # 31.41592653589793
```

---

## 4. Getter/Setter Patterns

### Traditional Pattern

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    # Getter
    def get_name(self):
        return self._name
    
    # Setter
    def set_name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
    
    # Getter
    def get_age(self):
        return self._age
    
    # Setter
    def set_age(self, value):
        if not 0 <= value <= 150:
            raise ValueError("Invalid age")
        self._age = value

person = Person("Alice", 30)
print(person.get_name())  # Alice
person.set_age(31)
```

### Property Pattern (Preferred)

```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not 0 <= value <= 150:
            raise ValueError("Invalid age")
        self._age = value

# Clean syntax
person = Person("Alice", 30)
print(person.name)   # Alice
person.age = 31      # Uses setter with validation
```

---

## 5. Read-Only Properties

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
        self._area = None
    
    @property
    def radius(self):
        return self._radius
    
    @property
    def area(self):
        """Read-only computed property."""
        if self._area is None:
            import math
            self._area = math.pi * self._radius ** 2
        return self._area

c = Circle(5)
print(c.area)  # 78.53981633974483
# c.area = 100  # AttributeError: can't set
```

---

## 6. Data Classes with Encapsulation

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    _gpa: float = field(init=False, repr=False)
    
    def __post_init__(self):
        self._gpa = 0.0
    
    @property
    def gpa(self):
        return self._gpa
    
    @gpa.setter
    def gpa(self, value):
        if not 0.0 <= value <= 4.0:
            raise ValueError("GPA must be between 0 and 4")
        self._gpa = value

student = Student("Alice")
student.gpa = 3.8
print(student.gpa)  # 3.8
```

---

## 7. Common Mistakes to Avoid

### 1. Exposing Internal State

```python
# BAD - direct access to internal list
class Team:
    def __init__(self):
        self.members = []  # Public!

# GOOD - controlled access
class Team:
    def __init__(self):
        self._members = []  # Protected
    
    def add_member(self, member):
        self._members.append(member)
    
    @property
    def members(self):
        return self._members.copy()  # Return copy
```

### 2. Not Validating Input

```python
# BAD - no validation
class Person:
    def __init__(self, age):
        self.age = age  # Could be negative!

# GOOD - validate in setter
class Person:
    def __init__(self, age):
        self.age = age  # Uses setter
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
```

---

## 8. Best Practices

1. **Use `_` prefix** for internal attributes
2. **Use `__` prefix** only when name mangling is needed
3. **Use properties** for controlled access
4. **Validate input** in setters
5. **Return copies** of mutable internal state
6. **Document** public API
7. **Don't over-encapsulate** - Python favors simplicity

---

## 9. Practice Exercises

### Exercise 1: Encapsulated Bank Account

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self._owner = owner
        self._balance = balance
        self._transactions = []
    
    @property
    def owner(self):
        return self._owner
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transactions.append(('DEPOSIT', amount))
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(('WITHDRAWAL', amount))
    
    def get_statement(self):
        return self._transactions.copy()

# Test
account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)
print(account.balance)         # 1300
print(account.get_statement()) # [('DEPOSIT', 500), ('WITHDRAWAL', 200)]
```

---

## 10. Summary

| Concept | Key Points |
|---------|------------|
| **Encapsulation** | Bundle data + methods, restrict access |
| **Public** | No underscore - accessible anywhere |
| **Protected** | `_` prefix - internal use |
| **Private** | `__` prefix - name mangling |
| **Properties** | `@property` for controlled access |
| **Validation** | Check input in setters |
| **Read-only** | Property without setter |

---

## Next Steps

- Learn about dataclasses and attrs
- Study descriptor protocol
- Explore metaclasses for advanced encapsulation
