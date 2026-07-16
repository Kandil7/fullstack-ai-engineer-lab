# Glossary: Metaclasses

## Quick Reference Table

| Term | Definition | Key Syntax | Purpose |
|------|------------|------------|---------|
| Metaclass | Class that creates classes | `class Meta(type)` | Control class creation |
| type | Default metaclass for all classes | `type(name, bases, ns)` | Class creation |
| __new__ | Create the class | `__new__(mcs, name, bases, ns)` | Class creation hook |
| __init__ | Initialize the class | `__init__(cls, name, bases, ns)` | Class initialization hook |
| __call__ | Create instances | `__call__(cls, *args, **kwargs)` | Instance creation hook |
| Singleton | Pattern ensuring one instance | `metaclass=SingletonMeta` | Single instance |
| Registry | Pattern auto-registering subclasses | `metaclass=RegistryMeta` | Class registration |
| Namespace | Class attribute dictionary | `namespace.keys()` | Class attributes |

---

## Alphabetical Definitions

### __call__

**Definition**: A method in metaclasses that is called when creating instances of the class. It controls how instances are created and can implement patterns like singleton.

**Example**:
```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """Called when creating instances."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.id = id(self)

# __call__ ensures only one instance
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

**Related Terms**: __new__, __init__, instance creation

**Parameters**:
- `cls`: The class being instantiated
- `*args, **kwargs`: Arguments passed to `__init__`

---

### __init__

**Definition**: A method in metaclasses that initializes a class after it has been created by `__new__`. Used to modify or extend the class after creation.

**Example**:
```python
class AutoReprMeta(type):
    def __init__(cls, name, bases, namespace):
        """Called after class is created."""
        super().__init__(name, bases, namespace)
        
        # Add __repr__ if not defined
        if '__repr__' not in namespace:
            fields = [k for k, v in namespace.items() 
                     if not k.startswith('_') and not callable(v)]
            
            def __repr__(self):
                attrs = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
                return f"{name}({attrs})"
            
            cls.__repr__ = __repr__

class Point(metaclass=AutoReprMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p)  # Point(x=3, y=4)
```

**Related Terms**: __new__, class creation, initialization

---

### __new__

**Definition**: A method in metaclasses that creates the class. It's called before `__init__` and is responsible for returning the new class object.

**Example**:
```python
class ValidationMeta(type):
    def __new__(mcs, name, bases, namespace):
        """Create the class with validation."""
        # Validate required attributes
        if bases:  # Skip base classes
            if 'required' not in namespace:
                raise TypeError(f"{name} must define 'required'")
        
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class Base(metaclass=ValidationMeta):
    required = True

class Child(Base):
    required = True  # OK

try:
    class Bad(Base):
        pass  # Missing 'required'
except TypeError as e:
    print(f"Error: {e}")
```

**Related Terms**: __init__, class creation, type

**Key Points**:
- Must return the new class
- Called before `__init__`
- Can modify namespace before class creation

---

### bases

**Definition**: A tuple of base classes (parents) that the new class inherits from. Passed to metaclass `__new__` and `__init__`.

**Example**:
```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating {name} with bases: {bases}")
        return super().__new__(mcs, name, bases, namespace)

class Base1:
    pass

class Base2:
    pass

class Child(Base1, Base2, metaclass=Meta):
    pass
# Output: Creating Child with bases: (<class 'Base1'>, <class 'Base2'>)
```

**Related Terms**: inheritance, MRO, super()

---

### class decorator

**Definition**: A function that modifies a class after creation, providing an alternative to metaclasses for simple class modifications.

**Example**:
```python
def add_repr(cls):
    """Class decorator that adds __repr__."""
    fields = [k for k, v in cls.__dict__.items() 
              if not k.startswith('_') and not callable(v)]
    
    def __repr__(self):
        attrs = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
        return f"{cls.__name__}({attrs})"
    
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p)  # Point(x=3, y=4)
```

**Related Terms**: metaclass, decorator, class modification

**When to Use**:
- Simple class modifications
- No need for inheritance control
- One-time modifications

---

### descriptor

**Definition**: An object that defines `__get__`, `__set__`, or `__delete__` methods to customize attribute access. Properties are implemented as descriptors.

**Example**:
```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Must be positive")
        obj.__dict__[self.name] = value

class Circle:
    radius = Validated()
    
    def __init__(self, r):
        self.radius = r

c = Circle(5)
print(c.radius)  # 5
c.radius = 10    # OK
```

**Related Terms**: property, __get__, __set__, metaclass

---

### factory method

**Definition**: A method that creates and returns objects, often used with metaclass registries to instantiate classes by name.

**Example**:
```python
class RegistryMeta(type):
    _registry = {}
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:
            RegistryMeta._registry[name] = cls
    
    @classmethod
    def create(mcs, class_name, *args, **kwargs):
        """Factory method to create instances by name."""
        if class_name not in mcs._registry:
            raise ValueError(f"Unknown class: {class_name}")
        return mcs._registry[class_name](*args, **kwargs)

class Animal(metaclass=RegistryMeta):
    pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Factory method
dog = RegistryMeta.create("Dog")
cat = RegistryMeta.create("Cat")
print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

**Related Terms**: registry, metaclass, instantiation

---

### MRO (Method Resolution Order)

**Definition**: The order in which Python looks up methods in a class hierarchy, defined by the C3 linearization algorithm.

**Example**:
```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

d = D()
print(d.method())  # B (follows MRO)
```

**Related Terms**: inheritance, super(), method lookup

---

### namespace

**Definition**: A dictionary containing the class's attributes and methods during class creation. Passed to metaclass `__new__` and `__init__`.

**Example**:
```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Namespace for {name}:")
        for key, value in namespace.items():
            if not key.startswith('__'):
                print(f"  {key}: {value}")
        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=Meta):
    x = 10
    y = 20
    
    def method(self):
        pass
```

**Related Terms**: class attributes, __dict__, metaclass

**Contents**:
- Class variables
- Methods
- Decorated functions
- `__module__`, `__qualname__`, etc.

---

### Registry

**Definition**: A pattern where a metaclass automatically tracks all subclasses, enabling factory-style instantiation by class name.

**Example**:
```python
class RegistryMeta(type):
    _registry = {}
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:  # Don't register base class
            RegistryMeta._registry[name] = cls
    
    @classmethod
    def get_class(mcs, name):
        return mcs._registry.get(name)

class Plugin(metaclass=RegistryMeta):
    def process(self):
        raise NotImplementedError

class JSONPlugin(Plugin):
    def process(self):
        return "Processing JSON"

class XMLPlugin(Plugin):
    def process(self):
        return "Processing XML"

# Registry access
print(RegistryMeta._registry.keys())
# dict_keys(['JSONPlugin', 'XMLPlugin'])

plugin = RegistryMeta.get_class("JSONPlugin")()
print(plugin.process())  # Processing JSON
```

**Related Terms**: factory, metaclass, plugin system

---

### Singleton

**Definition**: A design pattern that ensures only one instance of a class exists. Can be implemented using metaclasses.

**Example**:
```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True - same instance
```

**Related Terms**: metaclass, __call__, instance management

**Variations**:
- Lazy singleton
- Thread-safe singleton
- Resettable singleton

---

### type

**Definition**: The default metaclass for all Python classes. Can be used to check types or create classes dynamically.

**Example**:
```python
# Checking types
print(type(42))       # <class 'int'>
print(type("hello"))  # <class 'str'>

# Creating classes dynamically
MyClass = type("MyClass", (object,), {
    "x": 10,
    "method": lambda self: self.x
})

obj = MyClass()
print(obj.x)        # 10
print(obj.method()) # 10
```

**Related Terms**: metaclass, isinstance(), class creation

---

## Concept Relationships

```
Metaclasses
├── type (default metaclass)
│   ├── __new__(): Create class
│   ├── __init__(): Initialize class
│   └── __call__(): Create instances
│
├── Custom Metaclasses
│   ├── ValidationMeta
│   ├── SingletonMeta
│   ├── RegistryMeta
│   └── AutoReprMeta
│
├── Related Concepts
│   ├── Descriptors (attribute access)
│   ├── Decorators (simpler alternative)
│   └── Abstract Base Classes (interface enforcement)
│
└── Patterns
    ├── Singleton (one instance)
    ├── Registry (class tracking)
    ├── Factory (object creation)
    └── Validation (constraint enforcement)
```

---

## Metaclass vs Decorator

| Aspect | Metaclass | Decorator |
|--------|-----------|-----------|
| Complexity | High | Low |
| Inheritance control | Yes | No |
| Class creation | Before | After |
| Use case | Complex class behavior | Simple modifications |
| Debugging | Harder | Easier |

---

## When to Use Metaclasses

| Need | Solution |
|------|----------|
| Enforce class constraints | ✅ Metaclass |
| Auto-register subclasses | ✅ Metaclass |
| Singleton pattern | ✅ Metaclass or module |
| Add methods to classes | ⚠️ Consider decorator |
| Simple class modification | ❌ Use decorator |
| Attribute validation | ❌ Use descriptors |

---

## Common Patterns

### 1. Validation Pattern
```python
class ValidationMeta(type):
    def __new__(mcs, name, bases, namespace):
        if bases:
            required = ['validate', 'process']
            for attr in required:
                if attr not in namespace:
                    raise TypeError(f"{name} must implement {attr}")
        return super().__new__(mcs, name, bases, namespace)
```

### 2. Registry Pattern
```python
class RegistryMeta(type):
    _registry = {}
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if bases:
            RegistryMeta._registry[name] = cls
```

### 3. Singleton Pattern
```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

### 4. Auto-Documentation Pattern
```python
class DocMeta(type):
    def __new__(mcs, name, bases, namespace):
        if '__doc__' not in namespace:
            namespace['__doc__'] = f"Auto-generated doc for {name}"
        return super().__new__(mcs, name, bases, namespace)
```

### 5. Method Injection Pattern
```python
class MethodInjectorMeta(type):
    def __new__(mcs, name, bases, namespace):
        def default_method(self):
            return f"Default {name} method"
        
        if 'custom_method' not in namespace:
            namespace['custom_method'] = default_method
        
        return super().__new__(mcs, name, bases, namespace)
```
