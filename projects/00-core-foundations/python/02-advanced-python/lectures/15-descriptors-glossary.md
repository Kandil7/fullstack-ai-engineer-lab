# Glossary: Descriptors

## Quick Reference Table

| Term | Definition | Key Methods | Purpose |
|------|------------|-------------|---------|
| Descriptor | Object defining attribute access | `__get__`, `__set__`, `__delete__` | Customize attribute behavior |
| Data Descriptor | Has `__get__` and `__set__`/`__delete__` | Both methods | Priority over instance attrs |
| Non-Data Descriptor | Only has `__get__` | `__get__` only | Can be overridden |
| __set_name__ | Called when descriptor is created | `__set_name__(owner, name)` | Get attribute name |
| Property | Built-in descriptor | `@property` | Managed attributes |
| Validator | Descriptor that validates | Custom `__set__` | Data integrity |
| Cached Descriptor | Caches computed values | Custom `__get__` | Performance |
| Computed Attribute | Calculates value dynamically | Custom `__get__` | Derived values |

---

## Alphabetical Definitions

### __delete__

**Definition**: A method in the descriptor protocol that is called when an attribute is deleted using the `del` statement.

**Example**:
```python
class Cached:
    def __init__(self, func):
        self.func = func
        self.name = None
        self.cache_attr = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.cache_attr = f"_cached_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.cache_attr):
            setattr(obj, self.cache_attr, self.func(obj))
        return getattr(obj, self.cache_attr)
    
    def __delete__(self, obj):
        """Clear the cached value."""
        if hasattr(obj, self.cache_attr):
            delattr(obj, self.cache_attr)

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @Cached
    def result(self):
        print("Computing...")
        return sum(self.data)

proc = DataProcessor([1, 2, 3])
print(proc.result)  # "Computing..." then 6
del proc.result     # Clears cache
print(proc.result)  # "Computing..." again
```

**Related Terms**: __get__, __set__, cache invalidation

---

### __get__

**Definition**: A method in the descriptor protocol that is called when an attribute is accessed (read). Returns the attribute value.

**Example**:
```python
class UpperCase:
    def __init__(self, func):
        self.func = func
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Class access
        value = self.func(obj)
        return value.upper() if isinstance(value, str) else value

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    @UpperCase
    def title_upper(self):
        return self.title

doc = Document("hello world", "content")
print(doc.title_upper)  # HELLO WORLD
print(Document.title_upper)  # <UpperCase object>
```

**Related Terms**: __set__, __delete__, attribute access

**Parameters**:
- `self`: The descriptor instance
- `obj`: The instance being accessed (None if class access)
- `objtype`: The class being accessed

---

### __set__

**Definition**: A method in the descriptor protocol that is called when an attribute is assigned a value. Used for validation or transformation.

**Example**:
```python
class Validated:
    def __init__(self, validator, error_msg="Invalid"):
        self.validator = validator
        self.error_msg = error_msg
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        """Validate before setting."""
        if not self.validator(value):
            raise ValueError(f"{self.name}: {self.error_msg}")
        obj.__dict__[self.name] = value

class PositiveNumber(Validated):
    def __init__(self):
        super().__init__(
            lambda x: isinstance(x, (int, float)) and x > 0,
            "must be positive"
        )

class Product:
    price = PositiveNumber()
    
    def __init__(self, price):
        self.price = price

p = Product(100)    # OK
p.price = 50        # OK
try:
    p.price = -10   # ValueError
except ValueError as e:
    print(e)  # price: must be positive
```

**Related Terms**: __get__, __delete__, validation

---

### __set_name__

**Definition**: A method in the descriptor protocol that is called when the descriptor is assigned to a class attribute. It provides the attribute name automatically.

**Example**:
```python
class Tracked:
    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name
        print(f"Descriptor created: {owner.__name__}.{name}")
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"Accessing {self.name}")
        return obj.__dict__.get(self.name)

class MyClass:
    x = Tracked()  # "Descriptor created: MyClass.x"
    y = Tracked()  # "Descriptor created: MyClass.y"

obj = MyClass()
obj.x  # "Accessing x"
```

**Related Terms**: descriptor, __get__, __set__

**When Called**: At class creation time, not at instance creation.

---

### caching descriptor

**Definition**: A descriptor that computes a value once and caches it for subsequent accesses, improving performance for expensive calculations.

**Example**:
```python
class CachedResult:
    def __init__(self, func):
        self.func = func
        self.name = None
        self.cache_attr = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.cache_attr = f"_cached_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, self.cache_attr):
            print(f"Computing {self.name}...")
            setattr(obj, self.cache_attr, self.func(obj))
        return getattr(obj, self.cache_attr)

class DataAnalysis:
    def __init__(self, data):
        self.data = data
    
    @CachedResult
    def mean(self):
        return sum(self.data) / len(self.data)
    
    @CachedResult
    def variance(self):
        m = self.mean  # Uses cached value
        return sum((x - m) ** 2 for x in self.data) / len(self.data)

analysis = DataAnalysis([1, 2, 3, 4, 5])
print(analysis.mean)      # "Computing mean..." then 3.0
print(analysis.mean)      # 3.0 (cached)
print(analysis.variance)  # "Computing variance..." then 2.0
```

**Related Terms**: descriptor, __get__, memoization

---

### computed attribute

**Definition**: A descriptor that calculates its value dynamically from other attributes, rather than storing a fixed value.

**Example**:
```python
class ComputedAttribute:
    def __init__(self, func):
        self.func = func
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)

class Employee:
    def __init__(self, hourly_rate, hours):
        self.hourly_rate = hourly_rate
        self.hours = hours
    
    @ComputedAttribute
    def gross_pay(self):
        return self.hourly_rate * self.hours
    
    @ComputedAttribute
    def tax(self):
        return self.gross_pay * 0.2  # Uses computed attribute

emp = Employee(25, 40)
print(f"Gross pay: ${emp.gross_pay}")  # $1000
print(f"Tax: ${emp.tax}")              # $200
```

**Related Terms**: descriptor, property, derived value

---

### data descriptor

**Definition**: A descriptor that implements both `__get__` and `__set__` (or `__delete__`). Data descriptors take priority over instance attributes in attribute lookup.

**Example**:
```python
class DataDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return f"From descriptor: {obj.__dict__.get(self.name)}"
    
    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class Example:
    attr = DataDescriptor()

obj = Example()
obj.attr = "instance value"
print(obj.attr)  # "From descriptor: instance value" (descriptor wins)
```

**Related Terms**: non-data descriptor, attribute lookup, priority

**Priority**: Data descriptors > Instance attributes > Non-data descriptors

---

### descriptor

**Definition**: An object that defines `__get__`, `__set__`, or `__delete__` methods to customize attribute access on classes. The mechanism behind properties, methods, classmethods, and staticmethods.

**Example**:
```python
class MyDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return "descriptor value"
    
    def __set__(self, obj, value):
        print(f"Setting: {value}")
    
    def __delete__(self, obj):
        print("Deleting")

class MyClass:
    attr = MyDescriptor()

obj = MyClass()
print(obj.attr)   # "descriptor value"
obj.attr = "new"  # "Setting: new"
del obj.attr      # "Deleting"
```

**Related Terms**: __get__, __set__, __delete__, property

---

### non-data descriptor

**Definition**: A descriptor that only implements `__get__`. Non-data descriptors can be overridden by instance attributes, unlike data descriptors.

**Example**:
```python
class NonDataDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return f"From non-data descriptor: {self.name}"

class Example:
    attr = NonDataDescriptor()

obj = Example()
print(obj.attr)  # "From non-data descriptor: attr"

obj.attr = "instance value"  # Instance attribute
print(obj.attr)  # "instance value" (instance wins)
```

**Related Terms**: data descriptor, attribute lookup, priority

**Priority**: Loses to instance attributes

---

### property

**Definition**: A built-in descriptor that provides a simple way to define getter, setter, and deleter methods for attribute access.

**Example**:
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Getter."""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Setter with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.radius)   # 5 (getter)
c.radius = 10     # setter
print(c.radius)   # 10
```

**Related Terms**: descriptor, getter, setter, deleter

---

### type checker

**Definition**: A descriptor that validates the type of values assigned to an attribute.

**Example**:
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class User:
    name = Typed(str)
    age = Typed(int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 25)
try:
    user.age = "twenty-five"  # TypeError
except TypeError as e:
    print(e)
```

**Related Terms**: descriptor, validation, type safety

---

## Concept Relationships

```
Descriptors
├── Protocol Methods
│   ├── __get__() - read access
│   ├── __set__() - write access
│   ├── __delete__() - delete access
│   └── __set_name__() - get attribute name
│
├── Types
│   ├── Data Descriptors
│   │   ├── Has __get__ and __set__/__delete__
│   │   └── Priority over instance attributes
│   └── Non-Data Descriptors
│       └── Only has __get__
│
├── Built-in Descriptors
│   ├── property()
│   ├── classmethod()
│   ├── staticmethod()
│   └── function (methods)
│
└── Patterns
    ├── Validation
    ├── Type Checking
    ├── Caching
    ├── Computed Attributes
    └── Logging/Debugging
```

---

## Data vs Non-Data Descriptor

| Aspect | Data Descriptor | Non-Data Descriptor |
|--------|-----------------|---------------------|
| Methods | `__get__` + `__set__`/`__delete__` | `__get__` only |
| Priority | Wins over instance attrs | Loses to instance attrs |
| Example | `property()` | `staticmethod()` |
| Use case | Managed attributes | Method lookup |

---

## When to Use Descriptors

| Use Case | Example | Solution |
|----------|---------|----------|
| Validation | Check value before set | `Validated` descriptor |
| Type checking | Enforce type constraints | `Typed` descriptor |
| Caching | Cache expensive results | `CachedResult` descriptor |
| Computed values | Calculate dynamically | `ComputedAttribute` descriptor |
| Logging | Track attribute access | `Logged` descriptor |
| Delegation | Forward to another object | `Delegated` descriptor |

---

## Common Patterns

### 1. Validation Pattern
```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, obj, value):
        if not self.is_valid(value):
            raise ValueError(f"Invalid {self.name}: {value}")
        obj.__dict__[self.name] = value
```

### 2. Type Checking Pattern
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type.__name__}")
        obj.__dict__[self.name] = value
```

### 3. Caching Pattern
```python
class Cached:
    def __get__(self, obj, objtype=None):
        if not hasattr(obj, '_cache'):
            obj._cache = {}
        if self.name not in obj._cache:
            obj._cache[self.name] = self.func(obj)
        return obj._cache[self.name]
```

### 4. Computed Pattern
```python
class Computed:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)
```

### 5. Logging Pattern
```python
class Logged:
    def __get__(self, obj, objtype=None):
        print(f"Getting {self.name}")
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        print(f"Setting {self.name} = {value}")
        obj.__dict__[self.name] = value
```
