# Inner Classes Glossary

## Topic 41: Quick Reference Guide

---

## Glossary Terms

### B

#### Builder Pattern
**Definition:** Using inner class to construct complex objects step by step.
```python
class QueryBuilder:
    class Condition:
        def __init__(self, field, value):
            self.field = field
            self.value = value
    
    def where(self, field, value):
        self._conditions.append(self.Condition(field, value))
        return self  # Fluent interface
```
**Related:** Fluent interface, factory, inner class

---

### C

#### Closure
**Definition:** Inner function/class capturing variables from enclosing scope.
```python
class Outer:
    def __init__(self):
        self.data = [1, 2, 3]
    
    class Iterator:
        def __init__(self, data):
            self.data = data  # Captured from outer
```
**Related:** Enclosing scope, variable capture

#### Composition
**Definition:** Building classes using other classes as components.
```python
class Car:
    class Engine:  # Inner class (composition)
        def start(self):
            return "Vroom!"
    
    def __init__(self):
        self.engine = self.Engine()
```
**Related:** Inner class, "has-a" relationship

---

### D

#### Data Container
**Definition:** Inner class that holds related data together.
```python
class Config:
    class Database:
        def __init__(self):
            self.host = "localhost"
            self.port = 5432
    
    def __init__(self):
        self.db = self.Database()
```
**Related:** Struct, record, grouping

---

### F

#### Factory
**Definition:** Inner class or method that creates objects.
```python
class LoggerFactory:
    class FileLogger:
        def __init__(self, path):
            self.path = path
    
    @staticmethod
    def create(log_type):
        if log_type == "file":
            return LoggerFactory.FileLogger("app.log")
```
**Related:** Factory pattern, creation pattern

---

### I

#### Inner Class
**Definition:** Class defined inside another class.
```python
class Outer:
    class Inner:
        pass
```
**Related:** Nested class, nested type

#### Iterator Pattern
**Definition:** Using inner class to implement iteration.
```python
class Collection:
    class Iterator:
        def __init__(self, items):
            self.items = items
            self.index = 0
        
        def __next__(self):
            if self.index >= len(self.items):
                raise StopIteration
            item = self.items[self.index]
            self.index += 1
            return item
```
**Related:** `__iter__`, `__next__`, iterable

---

### N

#### Nested Class
**Definition:** Another term for inner class.
```python
class Outer:
    class Nested:  # Same as inner class
        pass
```
**Related:** Inner class, encapsulation

---

### S

#### State Machine
**Definition:** Using inner classes to represent states.
```python
class TrafficLight:
    class State:
        pass
    
    class Red(State):
        def next(self, light):
            light._state = light.Green()
    
    class Green(State):
        def next(self, light):
            light._state = light.Yellow()
```
**Related:** State pattern, FSM, transitions

---

## Quick Reference Table

| Term | Concept | Description |
|------|---------|-------------|
| **Inner class** | Pattern | Class inside class |
| **Nested class** | Synonym | Same as inner class |
| **Closure** | Pattern | Capturing outer scope |
| **Builder** | Pattern | Step-by-step construction |
| **Factory** | Pattern | Object creation |
| **State machine** | Pattern | State transitions |
| **Iterator** | Pattern | Custom iteration |
| **Data container** | Pattern | Related data grouping |
| **Composition** | Concept | "Has-a" relationship |
| **Encapsulation** | Concept | Hiding details |

---

## Inner Class Patterns

### Pattern 1: Helper Class
```python
class Outer:
    class Helper:
        def assist(self):
            return "Assisting..."
```

### Pattern 2: Data Holder
```python
class Config:
    class Settings:
        def __init__(self):
            self.key = "value"
```

### Pattern 3: Iterator
```python
class Collection:
    class Iterator:
        def __next__(self):
            raise StopIteration
```

### Pattern 4: State
```python
class Machine:
    class State:
        def next(self, machine):
            pass
```

### Pattern 5: Builder
```python
class Query:
    class Builder:
        def build(self):
            return "query"
```

---

## When to Use Inner Classes

| Use Case | Example |
|----------|---------|
| **Logically related** | `University.Department` |
| **Encapsulation** | `Car.Engine` (hidden) |
| **Iterator** | `Collection.Iterator` |
| **Builder** | `QueryBuilder.Condition` |
| **State** | `TrafficLight.Red/Green/Yellow` |
| **Factory** | `LoggerFactory.FileLogger` |

---

## Access Patterns

### From Outer to Inner
```python
class Outer:
    class Inner:
        pass
    
    def create(self):
        return self.Inner()  # Direct access
```

### From Inner to Outer
```python
class Outer:
    class Inner:
        def __init__(self, outer):
            self.outer = outer  # Store reference
    
    def method(self):
        return self.Inner(self)
```
