# Inner Classes (Nested Classes) in Python

## Topic 41: Classes Within Classes

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what inner classes are and why they exist
2. Define and use nested classes
3. Access outer class attributes from inner classes
4. Implement practical patterns with inner classes
5. Apply inner classes in real-world scenarios

---

## 1. What are Inner Classes?

Inner classes (nested classes) are classes defined **inside another class**.

### Basic Syntax

```python
class Outer:
    class Inner:
        def __init__(self, value):
            self.value = value
    
    def create_inner(self):
        return self.Inner(42)

# Usage
outer = Outer()
inner = outer.create_inner()
print(inner.value)  # 42
```

### Why Use Inner Classes?

- **Logical grouping**: Related classes together
- **Encapsulation**: Hide implementation details
- **Helper classes**: Support outer class functionality
- **Builder pattern**: Construct complex objects
- **Iterators**: Custom iteration behavior

---

## 2. Basic Inner Classes

```python
class University:
    def __init__(self, name):
        self.name = name
        self.departments = []
    
    class Department:
        def __init__(self, name, head):
            self.name = name
            self.head = head
        
        def __repr__(self):
            return f"Dept: {self.name} (Head: {self.head})"
    
    def add_department(self, name, head):
        dept = self.Department(name, head)
        self.departments.append(dept)
        return dept

# Usage
uni = University("MIT")
cs = uni.add_department("Computer Science", "Dr. Smith")
physics = uni.add_department("Physics", "Dr. Jones")

print(uni.departments)
# [Dept: Computer Science (Head: Dr. Smith), Dept: Physics (Head: Dr. Jones)]
```

---

## 3. Accessing Outer Class from Inner Class

### Using Outer Class Name

```python
class Outer:
    def __init__(self):
        self.outer_attr = "Outer value"
    
    class Inner:
        def __init__(self, outer_instance):
            self.outer = outer_instance  # Store reference
        
        def access_outer(self):
            return self.outer.outer_attr

# Usage
outer = Outer()
inner = outer.Inner(outer)  # Pass outer instance
print(inner.access_outer())  # Outer value
```

### Using Closure

```python
class Outer:
    def __init__(self):
        self.data = [1, 2, 3, 4, 5]
    
    class Iterator:
        def __init__(self, data):
            self.data = data
            self.index = 0
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.index >= len(self.data):
                raise StopIteration
            value = self.data[self.index]
            self.index += 1
            return value
    
    def __iter__(self):
        return self.Iterator(self.data)

# Usage
outer = Outer()
for item in outer:
    print(item)  # 1, 2, 3, 4, 5
```

---

## 4. Practical Patterns

### Builder Pattern

```python
class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self._conditions = []
        self._order = None
        self._limit = None
    
    class Condition:
        def __init__(self, field, operator, value):
            self.field = field
            self.operator = operator
            self.value = value
        
        def __str__(self):
            return f"{self.field} {self.operator} {self.value}"
    
    def where(self, field, operator, value):
        self._conditions.append(self.Condition(field, operator, value))
        return self
    
    def order_by(self, field, desc=False):
        self._order = f"{field} {'DESC' if desc else 'ASC'}"
        return self
    
    def limit(self, count):
        self._limit = count
        return self
    
    def build(self):
        query = f"SELECT * FROM {self.table}"
        if self._conditions:
            conditions = " AND ".join(str(c) for c in self._conditions)
            query += f" WHERE {conditions}"
        if self._order:
            query += f" ORDER BY {self._order}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Usage
query = (QueryBuilder("users")
    .where("age", ">", 18)
    .where("status", "=", "active")
    .order_by("name")
    .limit(10)
    .build())

print(query)
# SELECT * FROM users WHERE age > 18 AND status = active ORDER BY name ASC LIMIT 10
```

### State Machine

```python
class TrafficLight:
    def __init__(self):
        self._state = self.Red()
    
    class State:
        def next(self, light):
            raise NotImplementedError
        
        def __str__(self):
            return self.__class__.__name__
    
    class Red(State):
        def next(self, light):
            light._state = light.Green()
    
    class Green(State):
        def next(self, light):
            light._state = light.Yellow()
    
    class Yellow(State):
        def next(self, light):
            light._state = light.Red()
    
    def next(self):
        self._state.next(self)
    
    @property
    def current(self):
        return str(self._state)

# Usage
light = TrafficLight()
print(light.current)  # Red
light.next()
print(light.current)  # Green
light.next()
print(light.current)  # Yellow
light.next()
print(light.current)  # Red
```

---

## 5. Inner Classes with Inheritance

```python
class Vehicle:
    class Engine:
        def __init__(self, horsepower):
            self.horsepower = horsepower
        
        def start(self):
            return f"Engine started ({self.horsepower} HP)"
    
    def __init__(self, make, horsepower):
        self.make = make
        self.engine = self.Engine(horsepower)

class ElectricVehicle(Vehicle):
    class Engine(Vehicle.Engine):  # Override inner class
        def start(self):
            return f"Silent electric motor ({self.horsepower} HP)"

# Usage
car = Vehicle("Toyota", 200)
print(car.engine.start())  # Engine started (200 HP)

tesla = ElectricVehicle("Tesla", 450)
print(tesla.engine.start())  # Silent electric motor (450 HP)
```

---

## 6. Common Use Cases

### Data Container

```python
class Config:
    class Database:
        def __init__(self):
            self.host = "localhost"
            self.port = 5432
            self.name = "mydb"
    
    class Cache:
        def __init__(self):
            self.enabled = True
            self.ttl = 300
    
    def __init__(self):
        self.database = self.Database()
        self.cache = self.Cache()

# Usage
config = Config()
print(config.database.host)  # localhost
print(config.cache.enabled)  # True
```

### Factory

```python
class LoggerFactory:
    class FileLogger:
        def __init__(self, filename):
            self.filename = filename
        
        def log(self, message):
            with open(self.filename, 'a') as f:
                f.write(f"{message}\n")
    
    class ConsoleLogger:
        def log(self, message):
            print(f"LOG: {message}")
    
    @staticmethod
    def create(log_type, **kwargs):
        if log_type == "file":
            return LoggerFactory.FileLogger(**kwargs)
        elif log_type == "console":
            return LoggerFactory.ConsoleLogger()
        raise ValueError(f"Unknown type: {log_type}")

# Usage
file_logger = LoggerFactory.create("file", filename="app.log")
console_logger = LoggerFactory.create("console")
```

---

## 7. Common Mistakes to Avoid

### 1. Forgetting to Pass Outer Instance

```python
class Outer:
    class Inner:
        def __init__(self):
            self.value = 42  # No access to outer!
```

### 2. Overusing Inner Classes

```python
# BAD - too nested
class A:
    class B:
        class C:
            class D:
                pass

# GOOD - flatten when too deep
class A:
    pass

class B:
    pass
```

---

## 8. Best Practices

1. **Use inner classes** for logically related components
2. **Keep nesting shallow** (1-2 levels max)
3. **Document** the relationship between classes
4. **Use inner classes** for iterators and builders
5. **Consider composition** over deep nesting
6. **Name clearly** - inner class name should indicate purpose

---

## 9. Practice Exercises

### Exercise 1: Linked List

```python
class LinkedList:
    def __init__(self):
        self.head = None
    
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def append(self, data):
        if not self.head:
            self.head = self.Node(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = self.Node(data)
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

# Usage
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(list(ll))  # [1, 2, 3]
```

---

## 10. Summary

| Concept | Key Points |
|---------|------------|
| **Inner class** | Class defined inside another class |
| **Logical grouping** | Related classes together |
| **Encapsulation** | Hide implementation details |
| **Patterns** | Builder, state machine, iterator |
| **Access outer** | Pass outer instance or use closure |
| **Keep shallow** | 1-2 levels max |

---

## Next Steps

- Learn about closures and function factories
- Study design patterns using inner classes
- Explore metaclasses for advanced patterns
