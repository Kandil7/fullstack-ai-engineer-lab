# Encapsulation Glossary

## Topic 37: Quick Reference Guide

---

## Glossary Terms

### A

#### Access Control
**Definition:** Restricting access to object components.
```python
class MyClass:
    def __init__(self):
        self.public = "anyone"
        self._protected = "internal"
        self.__private = "hidden"
```
**Related:** Public, protected, private, encapsulation

---

### E

#### Encapsulation
**Definition:** Bundling data and methods, restricting direct access.
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Encapsulated
    
    @property
    def balance(self):
        return self._balance
```
**Related:** Abstraction, information hiding, data protection

---

### G

#### Getter
**Definition:** Method/property to retrieve attribute value.
```python
class Person:
    @property
    def name(self):
        return self._name  # Getter
```
**Related:** Setter, property, accessor

---

### I

#### Information Hiding
**Definition:** Concealing implementation details from users.
```python
class Calculator:
    def add(self, a, b):
        return self._internal_add(a, b)  # Hidden implementation
    
    def _internal_add(self, a, b):
        return a + b
```
**Related:** Encapsulation, abstraction

---

### M

#### Name Mangling
**Definition:** Python mechanism for `__` prefix (adds class name).
```python
class MyClass:
    def __init__(self):
        self.__private = "hidden"

obj = MyClass()
# obj.__private  # AttributeError
obj._MyClass__private  # Works (mangled name)
```
**Related:** Private, `__` prefix, encapsulation

---

### P

#### Private
**Definition:** Attributes with `__` prefix (name-mangled).
```python
class MyClass:
    def __init__(self):
        self.__secret = "hidden"
    
    def get_secret(self):
        return self.__secret  # Access via method
```
**Related:** Name mangling, protected, encapsulation

#### Property
**Definition:** Controlled attribute access using decorators.
```python
class Temperature:
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value
```
**Related:** Getter, setter, `@property`

#### Protected
**Definition:** Attributes with `_` prefix (convention only).
```python
class MyClass:
    def __init__(self):
        self._internal = "for class use"
```
**Related:** Private, public, convention

#### Public
**Definition:** Attributes with no underscore (accessible anywhere).
```python
class MyClass:
    def __init__(self):
        self.anyone = "accessible"
```
**Related:** Protected, private

---

### S

#### Setter
**Definition:** Method/property to set attribute value with validation.
```python
class Person:
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Invalid age")
        self._age = value
```
**Related:** Getter, property, mutator

---

## Quick Reference Table

| Term | Syntax | Description |
|------|--------|-------------|
| **Public** | `self.name` | No underscore, full access |
| **Protected** | `self._name` | Single underscore, internal use |
| **Private** | `self.__name` | Double underscore, name-mangled |
| **Getter** | `@property` | Get attribute value |
| **Setter** | `@prop.setter` | Set with validation |
| **Read-only** | `@property` only | No setter defined |
| **Name mangling** | `__attr` → `_Class__attr` | Python's privacy mechanism |

---

## Encapsulation Patterns

### Pattern 1: Property with Validation
```python
class Person:
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Invalid age")
        self._age = value
```

### Pattern 2: Read-Only Property
```python
class Circle:
    @property
    def area(self):
        return math.pi * self._radius ** 2
```

### Pattern 3: Protected with Copy
```python
class Team:
    @property
    def members(self):
        return self._members.copy()  # Return copy
```

### Pattern 4: Validation in Constructor
```python
class Student:
    def __init__(self, gpa):
        self.gpa = gpa  # Uses setter
    
    @gpa.setter
    def gpa(self, value):
        if not 0 <= value <= 4:
            raise ValueError("Invalid GPA")
        self._gpa = value
```

---

## Access Levels

| Level | Syntax | Access | Use Case |
|-------|--------|--------|----------|
| **Public** | `x` | Anywhere | User-facing API |
| **Protected** | `_x` | Class + subclasses | Internal implementation |
| **Private** | `__x` | Class only | Name collision prevention |

---

## Property Decorators

| Decorator | Purpose | Example |
|-----------|---------|---------|
| `@property` | Getter | `obj.attr` |
| `@attr.setter` | Setter | `obj.attr = value` |
| `@attr.deleter` | Deleter | `del obj.attr` |

```python
class Example:
    @property
    def value(self):
        """Getter."""
        return self._value
    
    @value.setter
    def value(self, val):
        """Setter."""
        self._value = val
    
    @value.deleter
    def value(self):
        """Deleter."""
        del self._value
```
