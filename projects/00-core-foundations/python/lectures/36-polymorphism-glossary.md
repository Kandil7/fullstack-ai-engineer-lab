# Polymorphism Glossary

## Topic 36: Quick Reference Guide

---

## Glossary Terms

### D

#### Duck Typing
**Definition:** Python's approach where object type is determined by methods/attributes, not class.
```python
class Duck:
    def speak(self):
        return "Quack!"

class Person:
    def speak(self):
        return "Hello!"

def make_speak(thing):
    print(thing.speak())  # Works with both!

make_speak(Duck())    # Quack!
make_speak(Person())  # Hello!
```
**Related:** Polymorphism, type checking, protocols

---

### O

#### Operator Overloading
**Definition:** Defining custom behavior for operators using special methods.
```python
class Vector:
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```
**Related:** Dunder methods, special methods, `__add__`, `__eq__`

#### Overriding
**Definition:** Child class providing its own implementation of parent method.
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):  # Overrides Animal.speak
        return "Woof!"
```
**Related:** Inheritance, method replacement, polymorphism

---

### P

#### Polymorphism
**Definition:** Objects can be treated as instances of parent class; same interface, different behavior.
```python
def make_sound(animal):
    print(animal.speak())  # Different behavior per animal type

make_sound(Dog())   # Woof!
make_sound(Cat())   # Meow!
```
**Related:** Inheritance, duck typing, overriding

#### Protocol
**Definition:** Structural subtyping - defines required methods/attributes.
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...
```
**Related:** Duck typing, structural subtyping, typing

---

### S

#### Structural Subtyping
**Definition:** Type compatibility based on structure (methods/attrs), not inheritance.
```python
# No inheritance needed
class Circle:
    def draw(self):
        print("Drawing circle")

def draw_shape(shape: Drawable):  # Just needs draw()
    shape.draw()

draw_shape(Circle())  # Works!
```
**Related:** Duck typing, protocols, nominal subtyping

---

## Quick Reference Table

| Term | Concept | Description |
|------|---------|-------------|
| **Polymorphism** | OOP | Many forms of objects |
| **Duck Typing** | Python | Type by behavior, not class |
| **Overriding** | Inheritance | Replace parent method |
| **Operator Overloading** | Special methods | Custom operator behavior |
| **Protocol** | Typing | Structural interface |
| **Abstract class** | Interface | Enforces contract |
| **__add__** | Operator | Addition behavior |
| **__eq__** | Operator | Equality behavior |
| **__lt__** | Operator | Less-than behavior |
| **__len__** | Operator | Length behavior |
| **__str__** | Operator | String conversion |
| **__repr__** | Operator | Debug string |

---

## Operator Overloading Methods

| Method | Operator | Description |
|--------|----------|-------------|
| `__add__` | `+` | Addition |
| `__sub__` | `-` | Subtraction |
| `__mul__` | `*` | Multiplication |
| `__truediv__` | `/` | Division |
| `__floordiv__` | `//` | Floor division |
| `__mod__` | `%` | Modulo |
| `__pow__` | `**` | Power |
| `__eq__` | `==` | Equality |
| `__ne__` | `!=` | Not equal |
| `__lt__` | `<` | Less than |
| `__le__` | `<=` | Less or equal |
| `__gt__` | `>` | Greater than |
| `__ge__` | `>=` | Greater or equal |
| `__contains__` | `in` | Membership test |
| `__len__` | `len()` | Length |
| `__getitem__` | `[]` | Index access |
| `__setitem__` | `[] =` | Index assignment |
| `__iter__` | `for` | Iteration |
| `__call__` | `()` | Function call |

---

## Polymorphism Patterns

### Pattern 1: Method Overriding
```python
class Base:
    def method(self):
        return "Base"

class Child(Base):
    def method(self):  # Override
        return "Child"
```

### Pattern 2: Duck Typing
```python
def process(thing):
    return thing.method()  # Just needs method()
```

### Pattern 3: Abstract Interface
```python
from abc import ABC, abstractmethod

class Interface(ABC):
    @abstractmethod
    def method(self):
        pass
```

### Pattern 4: Operator Overloading
```python
class MyClass:
    def __add__(self, other):
        return MyClass(...)
```

### Pattern 5: Protocol
```python
from typing import Protocol

class MyProtocol(Protocol):
    def required_method(self) -> str: ...
```
