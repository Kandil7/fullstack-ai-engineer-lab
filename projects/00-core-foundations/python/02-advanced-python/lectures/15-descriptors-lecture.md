# Lecture 15: Descriptors

## Topic Overview

Descriptors are the underlying mechanism behind Python's properties, methods, classmethods, and staticmethods. A descriptor is any object that defines `__get__`, `__set__`, or `__delete__` methods, allowing you to customize attribute access on classes. Understanding descriptors gives you deep control over Python's object model.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Understand the descriptor protocol** (`__get__`, `__set__`, `__delete__`)
2. **Create custom descriptors** for validation and computed attributes
3. **Distinguish between data and non-data descriptors**
4. **Use `__set_name__`** for automatic attribute naming
5. **Build practical descriptor examples** (validation, caching, type checking)
6. **Understand how properties work** under the hood

---

## Key Concepts

### 1. The Descriptor Protocol

Descriptors implement methods that are called when attribute access occurs.

#### Basic Descriptor

```python
class SimpleDescriptor:
    def __get__(self, obj, objtype=None):
        """Called when attribute is accessed."""
        if obj is None:
            return self  # Accessed on class
        return f"Getting value from {obj}"
    
    def __set__(self, obj, value):
        """Called when attribute is set."""
        print(f"Setting value: {value}")
    
    def __delete__(self, obj):
        """Called when attribute is deleted."""
        print("Deleting attribute")

class MyClass:
    attr = SimpleDescriptor()

obj = MyClass()
print(obj.attr)      # Getting value from <__main__.MyClass object>
obj.attr = "hello"   # Setting value: hello
del obj.attr         # Deleting attribute
```

#### Understanding the Parameters

```python
class Descriptive:
    def __get__(self, obj, objtype=None):
        print(f"self: {self}")           # The descriptor instance
        print(f"obj: {obj}")             # Instance being accessed (None if class)
        print(f"objtype: {objtype}")     # Class being accessed
        return "value"
    
    def __set__(self, obj, value):
        print(f"Setting on {obj}: {value}")

class Example:
    x = Descriptive()

# Access on instance
obj = Example()
obj.x  # obj is the instance

# Access on class
Example.x  # obj is None, objtype is Example
```

---

### 2. Validation Descriptor

Create descriptors that validate values before allowing assignment.

#### Basic Validation

```python
class Validated:
    """Descriptor that validates values."""
    
    def __init__(self, validator, error_msg="Invalid value"):
        self.validator = validator
        self.error_msg = error_msg
        self.name = None
    
    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to a class attribute."""
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.name}: {self.error_msg}")
        obj.__dict__[self.name] = value

class PositiveNumber(Validated):
    def __init__(self):
        super().__init__(
            lambda x: isinstance(x, (int, float)) and x > 0,
            "must be a positive number"
        )

class NonEmptyString(Validated):
    def __init__(self):
        super().__init__(
            lambda x: isinstance(x, str) and len(x) > 0,
            "must be a non-empty string"
        )
```

#### Practical Example

```python
class Product:
    name = NonEmptyString()
    price = PositiveNumber()
    quantity = PositiveNumber()
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __repr__(self):
        return f"Product({self.name!r}, ${self.price}, qty={self.quantity})"

# Valid product
p = Product("Laptop", 999.99, 10)
print(p)  # Product('Laptop', $999.99, qty=10)

# Invalid product
try:
    bad = Product("", -100, 5)
except ValueError as e:
    print(f"Error: {e}")  # name: must be a non-empty string
```

---

### 3. Type-Checked Descriptor

Enforce type constraints on attribute assignment.

```python
class Typed:
    """Descriptor that enforces type checking."""
    
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

class Employee:
    name = Typed(str)
    age = Typed(int)
    salary = Typed(float)
    
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

# Valid assignment
emp = Employee("Alice", 30, 75000.0)
print(f"{emp.name}, age {emp.age}")

# Invalid assignment
try:
    emp.age = "thirty"  # TypeError
except TypeError as e:
    print(f"Error: {e}")
```

---

### 4. Computed Attribute Descriptor

Create descriptors that compute values dynamically.

```python
class ComputedAttribute:
    """Descriptor that computes value from other attributes."""
    
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
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    @ComputedAttribute
    def tax_rate(self):
        if self.salary > 100000:
            return 0.35
        elif self.salary > 50000:
            return 0.25
        return 0.15
    
    @ComputedAttribute
    def annual_tax(self):
        return self.salary * self.tax_rate

emp = Employee("Alice", 75000)
print(f"Tax rate: {emp.tax_rate}")   # 0.25
print(f"Annual tax: ${emp.annual_tax:,.2f}")  # $18,750.00
```

---

### 5. Caching Descriptor

Cache expensive computations to avoid redundant calculations.

```python
class CachedResult:
    """Descriptor that caches computed results."""
    
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
        if hasattr(obj, self.cache_attr):
            delattr(obj, self.cache_attr)

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @CachedResult
    def expensive_computation(self):
        """This only runs once, then result is cached."""
        print("Computing...")
        return sum(x ** 2 for x in self.data)

proc = DataProcessor(range(1000))
print(proc.expensive_computation)  # "Computing..." then result
print(proc.expensive_computation)  # Uses cache (no "Computing...")
del proc.expensive_computation      # Clears cache
print(proc.expensive_computation)  # "Computing..." again
```

---

### 6. Data vs Non-Data Descriptors

Understanding the difference affects attribute lookup priority.

#### Data Descriptor (has __set__ or __delete__)

```python
class DataDescriptor:
    """Data descriptor takes priority over instance attributes."""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(f"_{self.name}", "from data descriptor")
    
    def __set__(self, obj, value):
        obj.__dict__[f"_{self.name}"] = value

class Example:
    data = DataDescriptor()

obj = Example()
obj.data = "instance value"  # Goes to descriptor __set__
print(obj.data)  # "from data descriptor" (descriptor wins)
```

#### Non-Data Descriptor (only __get__)

```python
class NonDataDescriptor:
    """Non-data descriptor can be overridden by instance attributes."""
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return f"from non-data descriptor: {self.name}"

class Example:
    non_data = NonDataDescriptor()

obj = Example()
print(obj.non_data)  # "from non-data descriptor: non_data"

obj.non_data = "instance value"  # Instance attribute
print(obj.non_data)  # "instance value" (instance wins)
```

#### Priority Rules

| Descriptor Type | Instance Attribute | Priority |
|----------------|-------------------|----------|
| Data descriptor | Yes | Descriptor wins |
| Non-data descriptor | Yes | Instance wins |
| No descriptor | Yes | Instance wins |

---

### 7. Practical Example Classes

#### Product with Validation

```python
class Product:
    name = NonEmptyString()
    price = PositiveNumber()
    quantity = PositiveNumber()
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @CachedResult
    def total_value(self):
        """Expensive computation - cached."""
        print(f"Computing total value for {self.name}...")
        return self.price * self.quantity
    
    def __repr__(self):
        return f"Product({self.name!r}, ${self.price}, qty={self.quantity})"

product = Product("Laptop", 999.99, 10)
print(f"Total value: ${product.total_value():,.2f}")
print(f"Total value (cached): ${product.total_value():,.2f}")
```

#### Employee with Typed Attributes

```python
class Employee:
    name = Typed(str)
    age = Typed(int)
    salary = Typed(float)
    
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
    
    @ComputedAttribute
    def tax_rate(self):
        if self.salary > 100000:
            return 0.35
        elif self.salary > 50000:
            return 0.25
        return 0.15
    
    @ComputedAttribute
    def annual_tax(self):
        return self.salary * self.tax_rate

emp = Employee("Alice", 30, 75000)
print(f"Employee: {emp.name}, age {emp.age}")
print(f"Tax rate: {emp.tax_rate:.0%}")
print(f"Annual tax: ${emp.annual_tax:,.2f}")
```

---

## Common Mistakes to Avoid

### 1. Forgetting __set_name__

```python
class Bad:
    def __get__(self, obj, objtype=None):
        # self.name is None - error!
        return obj.__dict__.get(self.name)

# CORRECT
class Good:
    def __set_name__(self, owner, name):
        self.name = name  # Now we know the attribute name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
```

### 2. Not Handling Class Access

```python
class Bad:
    def __get__(self, obj, objtype=None):
        # Fails when accessed on class: obj is None
        return obj.__dict__['attr']

# CORRECT
class Good:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Return descriptor itself
        return obj.__dict__.get('attr')
```

### 3. Infinite Recursion

```python
class Bad:
    def __get__(self, obj, objtype=None):
        return self.attr  # Recursive call!

# CORRECT - use __dict__ directly
class Good:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get('_value')
```

---

## Best Practices

### 1. Always Use __set_name__

```python
class Validated:
    def __set_name__(self, owner, name):
        self.name = name  # Automatic attribute name
```

### 2. Handle Class-Level Access

```python
def __get__(self, obj, objtype=None):
    if obj is None:
        return self  # Class access
    return obj.__dict__.get(self.name)  # Instance access
```

### 3. Store Values in Instance __dict__

```python
def __set__(self, obj, value):
    obj.__dict__[self.name] = value  # Direct dict access
```

---

## Practice Exercises

### Exercise 1: Range Validator
```python
class Range:
    """
    Create a descriptor that validates values are within a range.
    Usage: age = Range(min_val=0, max_val=150)
    """
    def __init__(self, min_val, max_val):
        # Your code here
        pass
```

### Exercise 2: Unit Converter
```python
class UnitConverter:
    """
    Create a descriptor that automatically converts units.
    Usage: 
        celsius = UnitConverter('celsius')
        fahrenheit = UnitConverter('fahrenheit')
    """
    def __init__(self, unit):
        # Your code here
        pass
```

### Exercise 3: Observable Attribute
```python
class Observable:
    """
    Create a descriptor that notifies when attribute changes.
    Usage: name = Observable(callback=on_change)
    """
    def __init__(self, callback=None):
        # Your code here
        pass
```

---

## Summary

### Descriptor Protocol Methods

| Method | Purpose | Parameters |
|--------|---------|------------|
| `__get__(self, obj, objtype)` | Return attribute value | obj: instance, objtype: class |
| `__set__(self, obj, value)` | Set attribute value | obj: instance, value: new value |
| `__delete__(self, obj)` | Delete attribute | obj: instance |
| `__set_name__(self, owner, name)` | Get attribute name | owner: class, name: attribute name |

### Descriptor Types

| Type | Methods | Priority |
|------|---------|----------|
| Data descriptor | `__get__` + `__set__`/`__delete__` | Wins over instance attributes |
| Non-data descriptor | Only `__get__` | Loses to instance attributes |

### Key Takeaways

1. **Descriptors are the mechanism** behind properties, methods, classmethods
2. **`__set_name__`** automatically provides the attribute name
3. **Data descriptors** take priority over instance attributes
4. **Non-data descriptors** can be overridden by instance attributes
5. **Use descriptors** for reusable attribute behavior
6. **Store values** in `obj.__dict__` to avoid recursion

---

## Further Reading

- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Python data model - Descriptors](https://docs.python.org/3/reference/datamodel.html#descriptors)
- [PEP 252 - Making Types Look More Like Classes](https://www.python.org/dev/peps/pep-252/)
