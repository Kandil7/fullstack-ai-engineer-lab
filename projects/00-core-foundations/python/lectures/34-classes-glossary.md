# Classes Glossary

## Topic 34: Quick Reference Guide

---

## Glossary Terms

### A

#### Attribute
**Definition:** Variable belonging to an object or class.
```python
class Dog:
    def __init__(self, name):
        self.name = name  # Instance attribute

buddy = Dog("Buddy")
print(buddy.name)  # Access attribute
```
**Related:** Instance attribute, class attribute, property

---

### C

#### Class
**Definition:** Blueprint for creating objects with shared attributes and methods.
```python
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

my_car = Car("Toyota", "Camry")
```
**Related:** Object, instance, blueprint

#### Class Attribute
**Definition:** Attribute shared by all instances of a class.
```python
class Dog:
    species = "Canis familiaris"  # Class attribute

buddy = Dog()
max_dog = Dog()
print(buddy.species)  # Canis familiaris
```
**Related:** Instance attribute, shared state

#### Constructor
**Definition:** Method that initializes a new object (`__init__`).
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```
**Related:** `__init__`, initialization, instantiation

---

### D

#### Dunder Method
**Definition:** "Double underscore" magic methods (e.g., `__init__`, `__str__`).
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
```
**Related:** Magic methods, special methods, operator overloading

---

### I

#### Instance
**Definition:** A specific object created from a class.
```python
class Dog:
    pass

buddy = Dog()  # Instance of Dog
max_dog = Dog()  # Another instance
```
**Related:** Class, object, instantiation

#### Instance Attribute
**Definition:** Attribute unique to each instance.
```python
class Dog:
    def __init__(self, name):
        self.name = name  # Instance attribute

buddy = Dog("Buddy")
max_dog = Dog("Max")
print(buddy.name)  # Buddy
print(max_dog.name)  # Max
```
**Related:** Class attribute, `self`

#### Instance Method
**Definition:** Method that operates on instance data (uses `self`).
```python
class Calculator:
    def __init__(self, value):
        self.value = value
    
    def add(self, x):  # Instance method
        self.value += x
        return self
```
**Related:** `self`, methods, behavior

---

### M

#### Method
**Definition:** Function defined inside a class.
```python
class Dog:
    def bark(self):  # Method
        return "Woof!"
```
**Related:** Function, behavior, `self`

---

### O

#### Object
**Definition:** Instance of a class; combination of data and methods.
```python
class Dog:
    pass

buddy = Dog()  # Object
print(type(buddy))  # <class '__main__.Dog'>
```
**Related:** Class, instance, instantiation

---

### P

#### Property
**Definition:** Controlled attribute access using decorators.
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value
```
**Related:** Getter, setter, encapsulation, `@property`

---

### S

#### Self
**Definition:** Reference to the current instance in methods.
```python
class Dog:
    def __init__(self, name):
        self.name = name  # self refers to this instance
    
    def bark(self):
        return f"{self.name} says Woof!"
```
**Related:** Instance, methods, `__init__`

#### Special Method
**Definition:** Dunder method that defines built-in behavior.
```python
class Point:
    def __repr__(self):  # Special method
        return f"Point(...)"
    
    def __eq__(self, other):  # Special method
        return self.x == other.x
```
**Related:** Dunder, magic methods, operator overloading

---

## Quick Reference Table

| Term | Syntax/Example | Description |
|------|----------------|-------------|
| **Class** | `class MyClass:` | Define a class |
| **Object** | `obj = MyClass()` | Create instance |
| **__init__** | `def __init__(self, ...)` | Constructor |
| **self** | `self.name` | Reference to instance |
| **Class attribute** | `MyClass.attr = value` | Shared attribute |
| **Instance attribute** | `self.attr = value` | Instance-specific |
| **Method** | `def method(self):` | Function in class |
| **Property** | `@property` | Controlled access |
| **__str__** | `str(obj)` | User string |
| **__repr__** | `repr(obj)` | Debug string |
| **__eq__** | `obj1 == obj2` | Equality |
| **__add__** | `obj1 + obj2` | Addition |

---

## OOP Concepts

### Encapsulation
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected
    
    @property
    def balance(self):
        return self._balance  # Read-only access
```

### Abstraction
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

### Inheritance
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"
```

### Polymorphism
```python
def make_sound(animal):
    print(animal.speak())  # Works with any Animal

make_sound(Dog())   # Woof!
make_sound(Cat())   # Meow!
```
