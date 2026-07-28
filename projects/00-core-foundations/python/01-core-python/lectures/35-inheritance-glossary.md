# Inheritance Glossary

## Topic 35: Quick Reference Guide

---

## Glossary Terms

### A

#### Abstract Base Class (ABC)
**Definition:** Class that cannot be instantiated; defines interface for subclasses.
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```
**Related:** Abstract method, interface, contract

#### Abstract Method
**Definition:** Method that must be implemented by subclasses.
```python
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass  # No implementation
```
**Related:** `@abstractmethod`, abstract base class

---

### B

#### Base Class
**Definition:** Parent class that other classes inherit from.
```python
class Animal:  # Base class
    pass

class Dog(Animal):  # Child class
    pass
```
**Related:** Parent class, superclass

---

### C

#### Child Class
**Definition:** Class that inherits from another class.
```python
class Animal:
    pass

class Dog(Animal):  # Dog is child of Animal
    pass
```
**Related:** Derived class, subclass, inheritance

#### Composition
**Definition:** Building classes using other classes as components ("has-a").
```python
class Car:
    def __init__(self, engine):
        self.engine = engine  # Car HAS-A Engine
```
**Related:** Inheritance, "has-a" relationship

---

### D

#### Derived Class
**Definition:** Another term for child class.
```python
class Base:
    pass

class Derived(Base):  # Derived inherits from Base
    pass
```
**Related:** Child class, subclass

---

### I

#### Inheritance
**Definition:** Mechanism where a class inherits attributes/methods from parent.
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):
        return "Woof!"
```
**Related:** Parent, child, super(), overriding

#### isinstance()
**Definition:** Check if object is instance of a class (or its subclasses).
```python
dog = Dog()
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True (inheritance)
```
**Related:** Type checking, inheritance, issubclass()

#### issubclass()
**Definition:** Check if class is subclass of another class.
```python
print(issubclass(Dog, Animal))  # True
print(issubclass(Animal, Dog))  # False
```
**Related:** Inheritance, type checking

---

### M

#### Method Resolution Order (MRO)
**Definition:** Order in which Python searches for methods in inheritance chain.
```python
class D(B, C):
    pass

print(D.mro())  # Shows resolution order
```
**Related:** Multiple inheritance, super(), C3 linearization

#### Mixin
**Definition:** Class providing methods to add functionality without inheritance hierarchy.
```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class User(JsonMixin):
    def __init__(self, name):
        self.name = name
```
**Related:** Multiple inheritance, composition

#### Multiple Inheritance
**Definition:** Class inheriting from more than one parent class.
```python
class Flyer:
    def fly(self):
        pass

class Swimmer:
    def swim(self):
        pass

class Duck(Flyer, Swimmer):  # Multiple inheritance
    pass
```
**Related:** MRO, diamond problem, mixins

---

### O

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
**Related:** Polymorphism, method replacement

---

### P

#### Parent Class
**Definition:** Class that other classes inherit from (also base/super class).
```python
class Animal:  # Parent class
    pass

class Dog(Animal):  # Child class
    pass
```
**Related:** Base class, superclass, inheritance

---

### S

#### Superclass
**Definition:** Another term for parent class.
```python
class Animal:  # Superclass
    pass

class Dog(Animal):  # Subclass
    pass
```
**Related:** Parent class, base class

#### super()
**Definition:** Function that calls methods from parent class.
```python
class Child(Parent):
    def __init__(self):
        super().__init__()  # Call Parent.__init__
```
**Related:** Parent class, method calling, `__init__`

---

## Quick Reference Table

| Term | Syntax/Example | Description |
|------|----------------|-------------|
| **Inheritance** | `class Child(Parent):` | Child inherits from Parent |
| **super()** | `super().__init__()` | Call parent constructor |
| **Override** | `def method(self):` in child | Replace parent method |
| **ABC** | `class X(ABC):` | Abstract base class |
| **@abstractmethod** | `@abstractmethod` | Force implementation |
| **isinstance()** | `isinstance(obj, Class)` | Check object type |
| **issubclass()** | `issubclass(A, B)` | Check class hierarchy |
| **MRO** | `Class.mro()` | Method resolution order |
| **Mixin** | `class Mixin:` | Add functionality |
| **Multiple** | `class C(A, B):` | Inherit from multiple |

---

## Inheritance Patterns

### Pattern 1: Simple Inheritance
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"
```

### Pattern 2: With super()
```python
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
```

### Pattern 3: Abstract Interface
```python
from abc import ABC, abstractmethod

class Interface(ABC):
    @abstractmethod
    def method(self):
        pass
```

### Pattern 4: Mixin
```python
class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

class MyClass(JsonMixin, OtherBase):
    pass
```

---

## "Is-a" vs "Has-a"

| Relationship | Type | Example |
|--------------|------|---------|
| Dog **is an** Animal | Inheritance | `class Dog(Animal)` |
| Car **has an** Engine | Composition | `self.engine = Engine()` |
| Square **is a** Shape | Inheritance | `class Square(Shape)` |
| Person **has a** Phone | Composition | `self.phone = Phone()` |
