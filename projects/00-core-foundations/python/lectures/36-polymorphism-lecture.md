# Polymorphism in Python

## Topic 36: Many Forms of Objects

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of polymorphism
2. Implement method overriding for polymorphic behavior
3. Use duck typing in Python
4. Apply operator overloading
5. Create flexible, reusable code
6. Design polymorphic interfaces

---

## 1. What is Polymorphism?

Polymorphism means "many forms" - objects can be treated as instances of their parent class or as instances of their own class.

### Key Idea

The same method call can produce different behavior depending on the object type.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Duck:
    def speak(self):
        return "Quack!"

# Polymorphism in action
animals = [Dog(), Cat(), Duck()]

for animal in animals:
    print(animal.speak())  # Same method, different results

# Output:
# Woof!
# Meow!
# Quack!
```

---

## 2. Method Overriding

Child classes provide their own implementation of parent methods.

```python
class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")
    
    def describe(self):
        return f"{self.__class__.__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):  # Override parent method
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):  # Override parent method
        return self.width * self.height

# Same code works for all shapes
shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(shape.describe())
```

---

## 3. Duck Typing

"If it walks like a duck and quacks like a duck, it's a duck."

Python doesn't check type - it checks for method/attribute presence.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Duck:
    def speak(self):
        return "Quack!"

class NonAnimal:
    def speak(self):
        return "I'm not an animal but I can speak!"

# Python doesn't care about the class type
def make_it_speak(thing):
    print(thing.speak())  # Just needs a speak() method

make_it_speak(Dog())      # Woof!
make_it_speak(Cat())      # Meow!
make_it_speak(Duck())     # Quack!
make_it_speak(NonAnimal())  # I'm not an animal but I can speak!
```

### Duck Typing with Protocols

```python
from typing import Protocol

class Speakable(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "Woof!"

def announce(animal: Speakable) -> None:
    print(animal.speak())

announce(Dog())  # Works because Dog has speak()
```

---

## 4. Operator Overloading

Define how operators work with your objects using special methods.

### Arithmetic Operators

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)    # Vector(4, 6)
print(v1 - v2)    # Vector(-2, -2)
print(v1 * 3)     # Vector(3, 6)
```

### Comparison Operators

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    
    def __le__(self, other):
        return self.grade <= other.grade
    
    def __gt__(self, other):
        return self.grade > other.grade
    
    def __repr__(self):
        return f"{self.name}: {self.grade}"

alice = Student("Alice", 95)
bob = Student("Bob", 85)

print(alice == bob)   # False
print(alice > bob)    # True
print(alice >= bob)   # True

# Can now sort!
students = [bob, alice]
print(sorted(students))  # [Bob: 85, Alice: 95]
```

### String Operators

```python
class Text:
    def __init__(self, content):
        self.content = content
    
    def __str__(self):
        return self.content
    
    def __add__(self, other):
        return Text(self.content + " " + other.content)
    
    def __mul__(self, times):
        return Text(self.content * times)
    
    def __contains__(self, item):
        return item in self.content

t1 = Text("Hello")
t2 = Text("World")

print(t1 + t2)        # Hello World
print(t1 * 3)         # HelloHelloHello
print("ell" in t1)    # True
```

---

## 5. Polymorphic Functions

Functions that work with multiple types.

```python
def total_length(items):
    """Calculate total length of items."""
    return sum(len(item) for item in items)

# Works with strings
print(total_length(["hello", "world"]))  # 10

# Works with lists
print(total_length([[1, 2], [3, 4, 5]]))  # 5

# Works with any iterable with length
```

### Built-in Polymorphism

```python
# len() works with any object that implements __len__
print(len("hello"))      # 5 (string)
print(len([1, 2, 3]))    # 3 (list)
print(len({"a": 1}))     # 1 (dict)

# + operator is polymorphic
print(1 + 2)             # 3 (addition)
print("a" + "b")         # ab (concatenation)
print([1] + [2])         # [1, 2] (list concatenation)
```

---

## 6. Abstract Polymorphic Interfaces

Define contracts that all implementations must follow.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount):
        pass
    
    @abstractmethod
    def refund(self, amount):
        pass
    
    @abstractmethod
    def get_balance(self):
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self):
        self.balance = 0
    
    def charge(self, amount):
        self.balance += amount
        return f"Charged ${amount} to credit card"
    
    def refund(self, amount):
        self.balance -= amount
        return f"Refunded ${amount} to credit card"
    
    def get_balance(self):
        return self.balance

class PayPalProcessor(PaymentProcessor):
    def __init__(self):
        self.balance = 0
    
    def charge(self, amount):
        self.balance += amount
        return f"Charged ${amount} via PayPal"
    
    def refund(self, amount):
        self.balance -= amount
        return f"Refunded ${amount} via PayPal"
    
    def get_balance(self):
        return self.balance

# Polymorphic function
def process_payment(processor: PaymentProcessor, amount: float):
    print(processor.charge(amount))

# Works with any PaymentProcessor
cc = CreditCardProcessor()
paypal = PayPalProcessor()

process_payment(cc, 100)     # Charged $100 to credit card
process_payment(paypal, 50)  # Charged $50 via PayPal
```

---

## 7. Common Mistakes to Avoid

### 1. Type Checking Instead of Duck Typing

```python
# BAD - explicit type checking
def make_speak(animal):
    if isinstance(animal, Dog):
        return animal.speak()
    elif isinstance(animal, Cat):
        return animal.speak()
    else:
        raise TypeError("Not an animal")

# GOOD - duck typing
def make_speak(animal):
    return animal.speak()
```

### 2. Not Implementing Required Methods

```python
# BAD - missing method
class Incomplete(Shape):
    pass  # area() not implemented!

# GOOD - implement all abstract methods
class Complete(Shape):
    def area(self):
        return 0  # Even if just returning default
```

---

## 8. Best Practices

1. **Use duck typing** - don't check types explicitly
2. **Implement `__repr__`** and `__str__` for debugging
3. **Use abstract classes** to define interfaces
4. **Override comparison operators** for sorting
5. **Make operators consistent** (e.g., if `+` works, `+=` should too)
6. **Document** expected methods/attributes
7. **Use Protocols** for structural subtyping

---

## 9. Practice Exercises

### Exercise 1: Custom Container

```python
class UniqueList:
    """List that only allows unique elements."""
    
    def __init__(self):
        self._items = []
    
    def append(self, item):
        if item not in self._items:
            self._items.append(item)
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __contains__(self, item):
        return item in self._items
    
    def __iter__(self):
        return iter(self._items)
    
    def __repr__(self):
        return f"UniqueList({self._items})"

# Test
ul = UniqueList()
ul.append(1)
ul.append(2)
ul.append(1)  # Ignored (duplicate)
print(ul)        # UniqueList([1, 2])
print(len(ul))   # 2
print(1 in ul)   # True
```

---

## 10. Summary

| Concept | Key Points |
|---------|------------|
| **Polymorphism** | Same interface, different behavior |
| **Method overriding** | Child replaces parent method |
| **Duck typing** | Check behavior, not type |
| **Operator overloading** | Define operator behavior |
| **Abstract classes** | Enforce interface contracts |
| **Protocols** | Structural subtyping |

---

## Next Steps

- Learn about design patterns using polymorphism
- Study protocol-based programming
- Explore functional programming concepts
