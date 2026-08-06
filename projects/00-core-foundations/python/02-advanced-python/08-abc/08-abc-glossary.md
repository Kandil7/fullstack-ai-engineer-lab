# Abstract Base Classes (ABCs) Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| ABC | Abstract Base Class defining interfaces |
| `abc.ABC` | Base class for creating abstract classes |
| `@abstractmethod` | Decorator marking required methods |
| `abstractproperty` | Deprecated; use `@property` + `@abstractmethod` |
| `@abstractclassmethod` | Deprecated; use `@classmethod` + `@abstractmethod` |
| `@abstractstaticmethod` | Deprecated; use `@staticmethod` + `@abstractmethod` |
| Virtual Subclass | Class registered without inheriting |
| `register()` | Add virtual subclass to ABC |
| Interface | Contract defining required methods |
| Template Method | Algorithm with abstract steps |
| Plugin Architecture | Extensible system using ABCs |
| Polymorphism | Different implementations of same interface |
| Duck Typing | Type compatibility by interface |
| Structural Subtyping | Type matching by shape |
| Nominal Subtyping | Type matching by inheritance |
| Abstract Method | Method that must be implemented |
| Concrete Method | Method with default implementation |
| `__subclasshook__` | Custom subclass check |
| `isinstance()` | Type checking against ABC |
| `issubclass()` | Class hierarchy checking |

---

## Detailed Definitions

### `ABC`

**Definition**: Abstract Base Class, the base class provided by the `abc` module for creating abstract classes that define interfaces.

**Example**:
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

# Cannot instantiate ABC directly
# animal = Animal()  # TypeError

dog = Dog()
print(dog.speak())  # "Woof!"
```

**Related**: `abstractmethod`, Interface, Abstract Method

---

### `@abstractmethod`

**Definition**: A decorator from `abc` that marks a method as abstract, requiring subclasses to provide an implementation.

**Example**:
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Calculate area. Must be implemented."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter. Must be implemented."""
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

# Missing implementation causes error
# class BadShape(Shape):
#     pass
# shape = BadShape()  # TypeError: Can't instantiate abstract class
```

**Related**: `ABC`, Abstract Method, Interface Contract

---

### Abstract Method

**Definition**: A method defined in an ABC with `@abstractmethod` that has no implementation and must be overridden in subclasses.

**Example**:
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Abstract method - no implementation."""
        pass
    
    @abstractmethod
    def query(self, sql: str) -> list:
        """Abstract method - must be implemented."""
        pass

class PostgresDB(Database):
    def connect(self) -> None:
        print("Connected to PostgreSQL")
    
    def query(self, sql: str) -> list:
        return [{"id": 1}]

class MySQLDB(Database):
    def connect(self) -> None:
        print("Connected to MySQL")
    
    def query(self, sql: str) -> list:
        return [{"id": 2}]
```

**Related**: `@abstractmethod`, Interface, Override

---

### Abstract Property

**Definition**: A property that must be implemented in subclasses, created by combining `@property` with `@abstractmethod`.

**Example**：
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def fuel_type(self) -> str:
        """Must be implemented as a property."""
        pass
    
    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Must be implemented as a property."""
        pass

class ElectricCar(Vehicle):
    @property
    def fuel_type(self) -> str:
        return "Electric"
    
    @property
    def max_speed(self) -> float:
        return 200.0

car = ElectricCar()
print(car.fuel_type)  # "Electric"
print(car.max_speed)  # 200.0
```

**Related**: `@property`, `@abstractmethod`, Property Interface

---

### Abstract Class Method

**Definition**: A class method that must be implemented in subclasses, created by combining `@classmethod` with `@abstractmethod`.

**Example**：
```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, data: dict) -> str:
        """Must be implemented as class method."""
        pass
    
    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> dict:
        """Must be implemented as class method."""
        pass

class JSONSerializer(Serializer):
    @classmethod
    def serialize(cls, data: dict) -> str:
        import json
        return json.dumps(data)
    
    @classmethod
    def deserialize(cls, data: str) -> dict:
        import json
        return json.loads(data)

# Usage
result = JSONSerializer.serialize({"key": "value"})
print(result)  # '{"key": "value"}'
```

**Related**: `@classmethod`, `@abstractmethod`, Factory Method

---

### Abstract Static Method

**Definition**: A static method that must be implemented in subclasses, created by combining `@staticmethod` with `@abstractmethod`.

**Example**：
```python
from abc import ABC, abstractmethod

class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(value) -> bool:
        """Must be implemented as static method."""
        pass

class EmailValidator(Validator):
    @staticmethod
    def validate(value) -> bool:
        return "@" in value

class NumberValidator(Validator):
    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, (int, float))

print(EmailValidator.validate("test@example.com"))  # True
print(NumberValidator.validate(42))  # True
```

**Related**: `@staticmethod`, `@abstractmethod`, Utility Methods

---

### Concrete Method

**Definition**: A method in an ABC that has a full implementation, providing default behavior that subclasses can use or override.

**Example**：
```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: list) -> list:
        """Must be implemented."""
        pass
    
    def validate(self, data: list) -> bool:
        """Concrete method with default implementation."""
        return len(data) > 0
    
    def log(self, message: str) -> None:
        """Concrete method - logging."""
        print(f"[{self.__class__.__name__}] {message}")

class UserProcessor(DataProcessor):
    def process(self, data: list) -> list:
        self.log(f"Processing {len(data)} users")
        return [{"name": d["name"].upper()} for d in data]

processor = UserProcessor()
print(processor.validate([{"name": "alice"}]))  # True
print(processor.validate([]))  # False
```

**Related**: Abstract Method, Default Implementation, Override

---

### Concrete Class

**Definition**: A class that implements all abstract methods from its ABC parent and can be instantiated.

**Example**：
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):  # Concrete class
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):  # Concrete class
    def speak(self) -> str:
        return "Meow!"

# Can instantiate concrete classes
dog = Dog()
cat = Cat()
print(dog.speak())  # "Woof!"
print(cat.speak())  # "Meow!"
```

**Related**: ABC, Abstract Method, Instantiation

---

### Duck Typing

**Definition**: A programming style where an object's suitability is determined by the presence of certain methods and properties, rather than its type. ABCs can formalize duck typing.

**Example**：
```python
from abc import ABC, abstractmethod

# Formal duck typing with ABC
class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass

# Any class with draw() can be registered
class Circle:
    def draw(self) -> str:
        return "Drawing circle"

# Register as virtual subclass
Drawable.register(Circle)

def render(shape: Drawable) -> None:
    print(shape.draw())

# Works with any registered type
render(Circle())  # "Drawing circle"
```

**Related**: ABC, Virtual Subclass, Structural Subtyping

---

### Interface

**Definition**: A contract specifying the methods and properties that a class must implement. ABCs provide a formal way to define interfaces in Python.

**Example**：
```python
from abc import ABC, abstractmethod

class Repository(ABC):
    """Interface for data access."""
    
    @abstractmethod
    def get(self, id: str) -> dict:
        """Get item by ID."""
        pass
    
    @abstractmethod
    def save(self, item: dict) -> None:
        """Save an item."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete an item by ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> list:
        """List all items."""
        pass

class UserRepo(Repository):
    def __init__(self):
        self.users = {}
    
    def get(self, id: str) -> dict:
        return self.users.get(id)
    
    def save(self, item: dict) -> None:
        self.users[item["id"]] = item
    
    def delete(self, id: str) -> None:
        self.users.pop(id, None)
    
    def list_all(self) -> list:
        return list(self.users.values())
```

**Related**: ABC, Abstract Method, Contract

---

### Nominal Subtyping

**Definition**: Type compatibility determined by explicit inheritance. A subclass is a subtype of its parent class.

**Example**：
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):  # Nominal: Dog IS-A Animal
    def speak(self) -> str:
        return "Woof!"

# Nominal subtyping through inheritance
def animal_sound(animal: Animal) -> str:
    return animal.speak()

dog = Dog()
print(animal_sound(dog))  # Works - Dog is subtype of Animal
```

**Related**: Inheritance, Structural Subtyping, Protocol

---

### Plugin Architecture

**Definition**: A software design pattern where core functionality is extended through plugins that implement a defined interface (often an ABC).

**Example**：
```python
from abc import ABC, abstractmethod
from typing import Dict, Type

class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, context: dict) -> dict:
        pass

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
    
    def register(self, plugin: Plugin) -> None:
        self._plugins[plugin.name] = plugin
    
    def execute(self, name: str, context: dict) -> dict:
        plugin = self._plugins.get(name)
        if plugin is None:
            raise ValueError(f"Plugin {name} not found")
        return plugin.execute(context)

# Implement plugins
class ValidationPlugin(Plugin):
    @property
    def name(self) -> str:
        return "validation"
    
    def execute(self, context: dict) -> dict:
        return {"valid": True}

# Usage
manager = PluginManager()
manager.register(ValidationPlugin())
result = manager.execute("validation", {"data": [1, 2, 3]})
print(result)  # {"valid": True}
```

**Related**: ABC, Extensibility, Registry Pattern

---

### Polymorphism

**Definition**: The ability to use a single interface to represent different underlying forms (data types or classes). ABCs enable polymorphism by defining common interfaces.

**Example**：
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2

# Polymorphic function
def total_area(shapes: list[Shape]) -> float:
    return sum(shape.area() for shape in shapes)

# Works with any Shape implementation
shapes = [Circle(5), Square(4), Circle(3)]
print(total_area(shapes))  # Same interface, different implementations
```

**Related**: ABC, Interface, Override

---

### `register()`

**Definition**: A method on ABC that registers a class as a virtual subclass without inheritance, enabling `isinstance()` and `issubclass()` checks.

**Example**：
```python
from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

class User:
    """Third-party class - can't modify to inherit from Serializable."""
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def to_dict(self) -> dict:
        return {"name": self.name, "age": self.age}

# Register without inheritance
Serializable.register(User)

# Now passes isinstance check
user = User("Alice", 30)
print(isinstance(user, Serializable))  # True
print(issubclass(User, Serializable))  # True

# Can use in type hints
def process(item: Serializable) -> dict:
    return item.to_dict()

print(process(user))  # {'name': 'Alice', 'age': 30}
```

**Related**: Virtual Subclass, Duck Typing, Third-Party Integration

---

### Structural Subtyping

**Definition**: Type compatibility determined by the structure (methods/attributes) of types rather than explicit inheritance. Python's `Protocol` provides this.

**Example**：
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Circle"

class Square:
    def draw(self) -> str:
        return "Square"

# Structural - no inheritance needed
def render(shape: Drawable) -> None:
    print(shape.draw())

render(Circle())  # Works - has draw()
render(Square())  # Works - has draw()

# isinstance works with runtime_checkable
print(isinstance(Circle(), Drawable))  # True
```

**Related**: `Protocol`, Duck Typing, ABC

---

### `__subclasshook__`

**Definition**: A class method on ABC that allows customizing subclass checks, enabling structural matching without inheritance.

**Example**：
```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Drawable:
            # Check if C has draw method
            if any("draw" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

class Circle:
    def draw(self) -> str:
        return "Circle"

# Structural check without register()
print(issubclass(Circle, Drawable))  # True
```

**Related**: Structural Subtyping, Custom Checks

---

### Template Method

**Definition**: A design pattern where an ABC defines the algorithm skeleton with abstract steps, and subclasses implement the steps.

**Example**：
```python
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    def run(self, data):
        """Template method - defines the algorithm."""
        validated = self.validate(data)
        transformed = self.transform(validated)
        return self.store(transformed)
    
    @abstractmethod
    def validate(self, data):
        pass
    
    @abstractmethod
    def transform(self, data):
        pass
    
    @abstractmethod
    def store(self, data):
        pass

class UserPipeline(DataPipeline):
    def validate(self, data):
        return [d for d in data if "email" in d]
    
    def transform(self, data):
        return [{**d, "email": d["email"].lower()} for d in data]
    
    def store(self, data):
        print(f"Storing {len(data)} users")
        return data

pipeline = UserPipeline()
result = pipeline.run([{"email": "TEST@X.COM"}, {"name": "NoEmail"}])
# Stores 1 user
```

**Related**: ABC, Algorithm Structure, Hook Methods

---

### Virtual Subclass

**Definition**: A class that is recognized as a subclass of an ABC through `register()` without actually inheriting from it.

**Example**：
```python
from abc import ABC, abstractmethod

class Flyer(ABC):
    @abstractmethod
    def fly(self) -> str:
        pass

class Bird:
    def fly(self) -> str:
        return "Flying with wings"

class Airplane:
    def fly(self) -> str:
        return "Flying with engines"

# Register without inheritance
Flyer.register(Bird)
Flyer.register(Airplane)

# isinstance works
print(isinstance(Bird(), Flyer))  # True
print(isinstance(Airplane(), Flyer))  # True

# Type hints work
def launch(flyer: Flyer) -> None:
    print(flyer.fly())

launch(Bird())   # Works
launch(Airplane())  # Works
```

**Related**: `register()`, Duck Typing, Structural Typing

---
