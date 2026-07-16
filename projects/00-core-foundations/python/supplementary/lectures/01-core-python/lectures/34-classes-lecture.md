# Classes in Python

## Topic 34: Object-Oriented Programming Fundamentals

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of classes and objects
2. Create classes with attributes and methods
3. Use the `__init__` constructor method
4. Implement instance methods and class methods
5. Work with special methods (dunder methods)
6. Apply OOP principles in real-world scenarios

---

## 1. What Are Classes?

Classes are **blueprints** for creating objects. They define properties (attributes) and behaviors (methods).

### Classes vs Objects

```python
# Class = Blueprint
class Car:
    pass

# Object = Instance of a class
my_car = Car()
your_car = Car()

print(type(my_car))  # <class '__main__.Car'>
```

### Why Use Classes?

- **Organization**: Group related data and functions
- **Reusability**: Create multiple objects from one definition
- **Abstraction**: Hide complexity behind simple interfaces
- **Encapsulation**: Keep data and methods together

---

## 2. Creating Classes

### Basic Class

```python
class Dog:
    """A class representing a dog."""
    
    pass

# Create instances
buddy = Dog()
max_dog = Dog()

print(buddy)  # <__main__.Dog object at 0x...>
```

### Class with Attributes

```python
class Dog:
    """A class representing a dog."""
    
    species = "Canis familiaris"  # Class attribute
    
    def __init__(self, name, age):
        """Initialize dog attributes."""
        self.name = name      # Instance attribute
        self.age = age

# Create instances
buddy = Dog("Buddy", 5)
max_dog = Dog("Max", 3)

print(buddy.name)    # Buddy
print(buddy.species) # Canis familiaris
```

---

## 3. The `__init__` Constructor

The `__init__` method runs when you create a new object.

```python
class Person:
    def __init__(self, name, age, email=None):
        """Initialize person with name and age."""
        self.name = name
        self.age = age
        self.email = email
    
    def greet(self):
        """Return greeting message."""
        return f"Hi, I'm {self.name}!"

# Usage
person = Person("Alice", 30, "alice@example.com")
print(person.greet())  # Hi, I'm Alice!
```

### Constructor Best Practices

```python
class Product:
    def __init__(self, name, price, quantity=0):
        """
        Initialize a product.
        
        Args:
            name: Product name
            price: Product price (must be positive)
            quantity: Available quantity (default: 0)
        """
        # Validation
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        self.name = name
        self.price = price
        self.quantity = quantity
```

---

## 4. Instance Methods

Methods that operate on a specific instance (use `self`).

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        """Add money to account."""
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """Remove money from account."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def get_balance(self):
        """Return current balance."""
        return self.balance

# Usage
account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())  # 1500
account.withdraw(200)
print(account.get_balance())  # 1300
```

---

## 5. Class vs Instance Attributes

### Class Attributes

Shared by all instances of the class.

```python
class Employee:
    company = "Tech Corp"  # Class attribute
    employee_count = 0
    
    def __init__(self, name):
        self.name = name  # Instance attribute
        Employee.employee_count += 1

emp1 = Employee("Alice")
emp2 = Employee("Bob")

print(emp1.company)       # Tech Corp
print(Employee.company)   # Tech Corp
print(Employee.employee_count)  # 2
```

### Instance Attributes

Unique to each instance.

```python
class Dog:
    species = "Dog"  # Class attribute
    
    def __init__(self, name, breed):
        self.name = name      # Instance attribute
        self.breed = breed    # Instance attribute

buddy = Dog("Buddy", "Golden Retriever")
max_dog = Dog("Max", "German Shepherd")

print(buddy.name)     # Buddy
print(buddy.breed)    # Golden Retriever
print(max_dog.name)   # Max
```

---

## 6. Special Methods (Dunder Methods)

Magic methods that define built-in behavior.

### Common Special Methods

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        """Developer-friendly string representation."""
        return f"Point({self.x}, {self.y})"
    
    def __str__(self):
        """User-friendly string representation."""
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        """Equality comparison."""
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        """Add two points."""
        return Point(self.x + other.x, self.y + other.y)
    
    def __len__(self):
        """Return length (for demonstration)."""
        return int((self.x**2 + self.y**2) ** 0.5)

# Usage
p1 = Point(1, 2)
p2 = Point(3, 4)

print(repr(p1))      # Point(1, 2)
print(str(p1))       # (1, 2)
print(p1 == Point(1, 2))  # True
p3 = p1 + p2
print(p3)            # (4, 6)
```

### More Special Methods

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __abs__(self):
        """Absolute value (magnitude)."""
        return (self.x**2 + self.y**2) ** 0.5
    
    def __bool__(self):
        """Boolean conversion."""
        return self.x != 0 or self.y != 0
    
    def __contains__(self, item):
        """Membership test."""
        return item == self.x or item == self.y
    
    def __getitem__(self, index):
        """Index access."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector index out of range")
    
    def __iter__(self):
        """Iteration."""
        yield self.x
        yield self.y

v = Vector(3, 4)
print(abs(v))        # 5.0
print(bool(v))       # True
print(3 in v)        # True
print(v[0])          # 3
print(list(v))       # [3, 4]
```

---

## 7. Properties

Controlled access to attributes using `@property`.

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
        """Set temperature in Celsius."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit."""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature in Fahrenheit."""
        self.celsius = (value - 32) * 5/9

# Usage
temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0

temp.fahrenheit = 32
print(temp.celsius)      # 0.0
```

---

## 8. Common Mistakes to Avoid

### 1. Forgetting `self`

```python
class Dog:
    def __init__(name):  # Missing self!
        self.name = name
    
    def bark():  # Missing self!
        return "Woof!"
```

### 2. Mutable Default Arguments

```python
# BAD - shared default
class Queue:
    def __init__(self, items=[]):
        self.items = items

# GOOD - use None
class Queue:
    def __init__(self, items=None):
        self.items = items if items is not None else []
```

### 3. Confusing Class and Instance Attributes

```python
class Dog:
    tricks = []  # Class attribute - shared!
    
    def __init__(self, name):
        self.name = name
        self.tricks = []  # Instance attribute - unique!
```

---

## 9. Best Practices

1. **Use `__init__`** for initialization
2. **Use `__repr__`** for debugging
3. **Use `__str__`** for user output
4. **Validate input** in constructors
5. **Keep methods focused** on single responsibility
6. **Use properties** for controlled access
7. **Document** classes and methods
8. **Follow PEP 8** naming conventions

---

## 10. Practice Exercises

### Exercise 1: Bank Account

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
        self._transactions = []
    
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
        return "\n".join(f"{t[0]}: ${t[1]:.2f}" for t in self._transactions)

# Test
account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)
print(account.balance)      # 1300
print(account.get_statement())
```

---

## 11. Summary

| Concept | Key Points |
|---------|------------|
| **Class** | Blueprint for objects |
| **Object** | Instance of a class |
| **__init__** | Constructor method |
| **self** | Reference to instance |
| **Instance methods** | Operate on instance data |
| **Class attributes** | Shared by all instances |
| **Special methods** | Define built-in behavior |
| **Properties** | Controlled attribute access |

---

## Next Steps

- Learn about inheritance and composition
- Study design patterns
- Explore abstract base classes
