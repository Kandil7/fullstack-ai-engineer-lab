# Lecture 14: Metaclasses

## Topic Overview

Metaclasses are the "classes of classes" in Python. Just as a class defines how instances behave, a metaclass defines how classes behave. Metaclasses allow you to intercept class creation, modify class attributes, enforce constraints, and implement advanced patterns like singletons and registries.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand the type() function** and its role in class creation
2. **Create custom metaclasses** using `__new__` and `__init__`
3. **Implement common patterns** like singleton, registry, and validation
4. **Distinguish between __new__ and __init__** in metaclasses
5. **Know when to use metaclasses** vs decorators or other approaches
6. **Debug metaclass conflicts** and inheritance issues

---

## Key Concepts

### 1. type() Function

`type()` is both a function to check types and the default metaclass for all Python classes.

#### Checking Types

```python
# Check type of an object
print(type(42))        # <class 'int'>
print(type("hello"))   # <class 'str'>
print(type([]))        # <class 'list'>

# Check if objects are instances
print(isinstance(42, int))  # True
print(isinstance("hello", str))  # True
```

#### Creating Classes Dynamically

```python
# type(name, bases, namespace)
# name: class name (string)
# bases: tuple of base classes
# namespace: dict of class attributes

# Create class with type()
MyClass = type("MyClass", (object,), {
    "greet": lambda self: "Hello!",
    "class_var": 42
})

obj = MyClass()
print(obj.greet())      # Hello!
print(obj.class_var)    # 42
print(MyClass.__name__) # MyClass
```

#### Equivalent Definitions

```python
# These are equivalent:

# Using class statement
class MyClass:
    class_var = 42
    
    def greet(self):
        return "Hello!"

# Using type()
MyClass = type("MyClass", (object,), {
    "class_var": 42,
    "greet": lambda self: "Hello!"
})

# Both produce the same class
```

---

### 2. Custom Metaclass

Create custom metaclasses by subclassing `type` and overriding `__new__` or `__init__`.

#### Basic Metaclass

```python
class ValidationMeta(type):
    """Metaclass that validates class attributes."""
    
    def __new__(mcs, name, bases, namespace):
        # Skip for base classes
        if bases:
            # Check for required attributes
            if 'required_attr' not in namespace:
                raise TypeError(f"Class {name} must define 'required_attr'")
        
        return super().__new__(mcs, name, bases, namespace)

# Using the metaclass
class BaseAPI(metaclass=ValidationMeta):
    required_attr = True

class UserAPI(BaseAPI):
    required_attr = True
    def get_user(self, id):
        return {"id": id, "name": "Alice"}

# This fails - missing required_attr
try:
    class BadAPI(BaseAPI):
        pass
except TypeError as e:
    print(f"Error: {e}")
```

#### Metaclass Parameters

```python
class DebugMeta(type):
    """Metaclass that logs class creation."""
    
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        print(f"  Bases: {bases}")
        print(f"  Attributes: {list(namespace.keys())}")
        
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        print(f"Initialized: {name}")

class MyClass(metaclass=DebugMeta):
    x = 10
    def method(self):
        pass
```

---

### 3. Singleton Metaclass

Implement the singleton pattern using a metaclass to ensure only one instance exists.

```python
class SingletonMeta(type):
    """Metaclass implementing singleton pattern."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection_id = id(self)
    
    def query(self, sql):
        return f"Executing: {sql}"

# Only one instance is created
db1 = Database()
db2 = Database()

print(f"Same instance: {db1 is db2}")  # True
print(f"db1 ID: {db1.connection_id}")
print(f"db2 ID: {db2.connection_id}")
print(f"Same ID: {db1.connection_id == db2.connection_id}")  # True
```

#### Thread-Safe Singleton

```python
import threading

class ThreadSafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=ThreadSafeSingletonMeta):
    def __init__(self):
        self.settings = {}
```

---

### 4. Class Registry Metaclass

Automatically register subclasses for factory pattern implementation.

```python
class RegistryMeta(type):
    """Metaclass that registers subclasses."""
    
    _registry = {}
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:  # Don't register base class
            RegistryMeta._registry[name] = cls
    
    @classmethod
    def get_registry(mcs):
        return dict(mcs._registry)
    
    @classmethod
    def create_instance(mcs, class_name, *args, **kwargs):
        if class_name not in RegistryMeta._registry:
            raise ValueError(f"Unknown class: {class_name}")
        return RegistryMeta._registry[class_name](*args, **kwargs)

class Serializer(metaclass=RegistryMeta):
    def serialize(self, data):
        raise NotImplementedError

class JSONSerializer(Serializer):
    def serialize(self, data):
        import json
        return json.dumps(data)

class XMLSerializer(Serializer):
    def serialize(self, data):
        return f"<data>{data}</data>"

class CSVSerializer(Serializer):
    def serialize(self, data):
        if isinstance(data, dict):
            return ",".join(str(v) for v in data.values())
        return str(data)

# Registry automatically populated
print(f"Registry: {list(RegistryMeta.get_registry().keys())}")
# ['JSONSerializer', 'XMLSerializer', 'CSVSerializer']

# Factory method
json_ser = RegistryMeta.create_instance("JSONSerializer")
data = {"name": "Alice", "age": 30}
print(f"JSON: {json_ser.serialize(data)}")
```

---

### 5. Auto-Representation Metaclass

Automatically add `__repr__` to classes.

```python
class ReprMeta(type):
    """Metaclass that adds __repr__ to classes."""
    
    def __new__(mcs, name, bases, namespace):
        fields = [
            k for k, v in namespace.items()
            if not k.startswith('_') and not callable(v)
        ]
        
        def __repr__(self):
            attrs = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
            return f"{name}({attrs})"
        
        namespace['__repr__'] = __repr__
        return super().__new__(mcs, name, bases, namespace)

class Point(metaclass=ReprMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Person(metaclass=ReprMeta):
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Point(3, 4)
person = Person("Bob", 25)
print(p)      # Point(x=3, y=4)
print(person) # Person(name='Bob', age=25)
```

---

### 6. __new__ vs __init__

Understanding the difference between `__new__` and `__init__` in metaclasses.

```python
class DemoMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"\n__new__ called for {name}")
        print(f"  mcs: {mcs}")
        print(f"  name: {name}")
        print(f"  bases: {bases}")
        
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"  Created class: {cls}")
        
        return cls
    
    def __init__(cls, name, bases, namespace):
        print(f"\n__init__ called for {name}")
        print(f"  cls: {cls}")
        
        # Initialize the class
        super().__init__(name, bases, namespace)

class MyClass(metaclass=DemoMeta):
    x = 10
```

#### Key Differences

| Aspect | `__new__` | `__init__` |
|--------|-----------|------------|
| Purpose | Create the class | Initialize the class |
| Called on | Metaclass (type) | Class (cls) |
| Returns | New class | None |
| Parameters | `mcs, name, bases, namespace` | `cls, name, bases, namespace` |
| Use case | Modify class creation | Modify class after creation |

---

### 7. Practical Examples

#### Method Logging

```python
class LoggingMeta(type):
    """Add logging to all methods."""
    
    def __new__(mcs, name, bases, namespace):
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                original = value
                
                def wrapper(*args, _original=original, _name=key, **kwargs):
                    print(f"  Calling {name}.{_name}")
                    return _original(*args, **kwargs)
                
                namespace[key] = wrapper
        
        return super().__new__(mcs, name, bases, namespace)

class API(metaclass=LoggingMeta):
    def get_user(self, id):
        return {"id": id}
    
    def create_user(self, data):
        return data

api = API()
api.get_user(1)    # Logs: Calling API.get_user
api.create_user({}) # Logs: Calling API.create_user
```

#### Attribute Validation

```python
class TypeCheckMeta(type):
    """Validate type annotations."""
    
    def __new__(mcs, name, bases, namespace):
        annotations = namespace.get('__annotations__', {})
        
        for attr_name, expected_type in annotations.items():
            if attr_name.startswith('_'):
                continue
            
            original_init = namespace.get('__init__')
            
            if original_init:
                def new_init(self, *args, _orig=original_init, _ann=annotations, **kwargs):
                    _orig(self, *args, **kwargs)
                    for attr, expected in _ann.items():
                        if not attr.startswith('_') and hasattr(self, attr):
                            value = getattr(self, attr)
                            if not isinstance(value, expected):
                                raise TypeError(
                                    f"{attr} must be {expected.__name__}, "
                                    f"got {type(value).__name__}"
                                )
                
                namespace['__init__'] = new_init
        
        return super().__new__(mcs, name, bases, namespace)

class User(metaclass=TypeCheckMeta):
    name: str
    age: int
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 25)  # OK
try:
    user = User("Alice", "twenty-five")  # TypeError
except TypeError as e:
    print(f"Error: {e}")
```

---

## Common Mistakes to Avoid

### 1. Forgetting to Return from __new__

```python
class BadMeta(type):
    def __new__(mcs, name, bases, namespace):
        # WRONG - forgot to return
        super().__new__(mcs, name, bases, namespace)

# This fails
try:
    class Bad(metaclass=BadMeta):
        pass
except TypeError as e:
    print(f"Error: {e}")

# CORRECT
class GoodMeta(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)
```

### 2. Not Calling super().__init__

```python
class BadInitMeta(type):
    def __init__(cls, name, bases, namespace):
        # WRONG - didn't call super
        pass  # Missing: super().__init__(name, bases, namespace)

# CORRECT
class GoodInitMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
```

### 3. Metaclass Conflict

```python
class MetaA(type):
    pass

class MetaB(type):
    pass

# Can't use two different metaclasses
try:
    class Bad(metaclass=MetaA, metaclass=MetaB):
        pass
except TypeError as e:
    print(f"Error: {e}")

# Solution: Create a combined metaclass
class CombinedMeta(MetaA, MetaB):
    pass
```

---

## Best Practices

### 1. Use Metaclasses Sparingly

```python
# GOOD - simple validation
class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, obj, value):
        # validation logic
        obj.__dict__[self.name] = value

# OVERKILL - metaclass for simple validation
class ValidationMeta(type):
    pass  # Use descriptors instead
```

### 2. Document Metaclass Behavior

```python
class RegistryMeta(type):
    """Metaclass that auto-registers subclasses.
    
    Classes using this metaclass are automatically added to
    a registry for factory-style instantiation.
    
    Example:
        class MySerializer(metaclass=RegistryMeta):
            pass
        
        # MySerializer is now in RegistryMeta._registry
    """
    pass
```

### 3. Consider Alternatives

| Need | Solution |
|------|----------|
| Simple validation | Descriptors |
| Class decoration | Class decorators |
| Single instance | Module-level instance |
| Method modification | Function decorators |
| Complex class creation | Metaclasses |

---

## Practice Exercises

### Exercise 1: Validation Metaclass
```python
"""
Create a metaclass that:
1. Validates all methods have docstrings
2. Adds __str__ method if not present
3. Logs class creation
"""
class DocstringMeta(type):
    # Your code here
    pass
```

### Exercise 2: Registry Pattern
```python
"""
Create a Plugin metaclass that:
1. Registers all plugin classes
2. Provides a get_plugin() factory method
3. Validates plugins have a 'process' method
"""
class PluginMeta(type):
    # Your code here
    pass
```

### Exercise 3: Singleton with Reset
```python
"""
Create a singleton metaclass that:
1. Ensures only one instance
2. Provides a reset() class method
3. Is thread-safe
"""
class ResettableSingletonMeta(type):
    # Your code here
    pass
```

---

## Summary

### Metaclass Protocol

| Method | Purpose | Parameters |
|--------|---------|------------|
| `__new__` | Create the class | `mcs, name, bases, namespace` |
| `__init__` | Initialize the class | `cls, name, bases, namespace` |
| `__call__` | Create instances | `cls, *args, **kwargs` |

### Common Patterns

| Pattern | Use Case |
|---------|----------|
| Singleton | Ensure single instance |
| Registry | Auto-register subclasses |
| Validation | Enforce class constraints |
| Auto-repr | Add __repr__ automatically |
| Method logging | Track method calls |

### Key Takeaways

1. **Metaclasses control class creation**, not instance creation
2. **`type()` is the default metaclass** for all classes
3. **Use `__new__` to modify class creation**
4. **Use `__init__` to modify class after creation**
5. **Consider alternatives** like descriptors and decorators first
6. **Document metaclass behavior** clearly

---

## Further Reading

- [Python data model - Metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)
- [PEP 3119 - Abstract Base Classes](https://www.python.org/dev/peps/pep-3119/)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
