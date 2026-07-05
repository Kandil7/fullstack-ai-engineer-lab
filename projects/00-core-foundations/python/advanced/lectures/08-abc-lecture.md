# Advanced Python Lecture 08: Abstract Base Classes (ABCs)

## Topic Overview

Abstract Base Classes (ABCs) provide a mechanism for defining interfaces and enforcing implementation contracts in Python. Using the `abc` module, you can define abstract methods that subclasses must implement, creating clear contracts for code reuse and polymorphism. ABCs are essential for building extensible frameworks, designing plugin systems, and ensuring consistent interfaces across different implementations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the purpose of abstract base classes
2. Create ABCs using `abc.ABC` and `@abstractmethod`
3. Use abstract properties, class methods, and static methods
4. Implement interface segregation with ABCs
5. Use `@abc.abstractmethod` decorators properly
6. Apply the Template Method pattern with ABCs
7. Create plugin architectures using ABCs
8. Use `register()` for virtual subclasses
9. Apply ABCs to AI engineering patterns
10. Follow best practices for ABC design

---

## 1. Why Abstract Base Classes?

### The Problem

```python
# Without ABCs - no enforcement
class PaymentProcessor:
    def process(self, amount):
        raise NotImplementedError

class StripeProcessor(PaymentProcessor):
    def process(self, amount):
        return f"Charged ${amount} via Stripe"

class PayPalProcessor(PaymentProcessor):
    def process(self, amount):
        return f"Charged ${amount} via PayPal"

# No enforcement - this passes but fails at runtime
class BadProcessor(PaymentProcessor):
    def charge(self, amount):  # Wrong method name!
        return f"Charged ${amount}"

# This creates the object but fails when process() is called
processor = BadProcessor()
# processor.process(100)  # NotImplementedError
```

### The Solution

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> str:
        """Process a payment. Must be implemented by subclasses."""
        pass

class StripeProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"Charged ${amount} via Stripe"

# This fails at instantiation time
class BadProcessor(PaymentProcessor):
    def charge(self, amount: float) -> str:  # Missing process()!
        return f"Charged ${amount}"

# processor = BadProcessor()  # TypeError: Can't instantiate abstract class
```

---

## 2. Basic ABC Usage

### Creating an ABC

```python
from abc import ABC, abstractmethod
from typing import List

class Shape(ABC):
    """Abstract base class for geometric shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass
    
    def describe(self) -> str:
        """Non-abstract method with default implementation."""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Usage
circle = Circle(5)
print(circle.describe())  # "Circle: area=78.54"

rectangle = Rectangle(4, 6)
print(rectangle.describe())  # "Rectangle: area=24.00"
```

---

## 3. Abstract Methods, Properties, and Class Methods

### Abstract Methods

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        pass
    
    @abstractmethod
    def execute(self, query: str) -> list:
        """Execute a query and return results."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass

class PostgresDB(Database):
    def connect(self) -> None:
        print("Connecting to PostgreSQL...")
    
    def execute(self, query: str) -> list:
        print(f"Executing: {query}")
        return [{"id": 1, "name": "Alice"}]
    
    def close(self) -> None:
        print("Closing PostgreSQL connection")
```

### Abstract Properties

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def fuel_type(self) -> str:
        """Return the fuel type."""
        pass
    
    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Return the maximum speed."""
        pass
    
    @abstractmethod
    def start(self) -> None:
        """Start the vehicle."""
        pass

class ElectricCar(Vehicle):
    @property
    def fuel_type(self) -> str:
        return "Electric"
    
    @property
    def max_speed(self) -> float:
        return 200.0
    
    def start(self) -> None:
        print("Electric car started silently")

class GasCar(Vehicle):
    @property
    def fuel_type(self) -> str:
        return "Gasoline"
    
    @property
    def max_speed(self) -> float:
        return 180.0
    
    def start(self) -> None:
        print("Gas car started with engine roar")
```

### Abstract Class Methods and Static Methods

```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, data: dict) -> str:
        """Serialize data to string format."""
        pass
    
    @staticmethod
    @abstractmethod
    def content_type() -> str:
        """Return the content type."""
        pass

class JSONSerializer(Serializer):
    @classmethod
    def serialize(cls, data: dict) -> str:
        import json
        return json.dumps(data)
    
    @staticmethod
    def content_type() -> str:
        return "application/json"

class XMLSerializer(Serializer):
    @classmethod
    def serialize(cls, data: dict) -> str:
        # Simplified XML serialization
        return f"<data>{data}</data>"
    
    @staticmethod
    def content_type() -> str:
        return "application/xml"
```

---

## 4. Multiple Inheritance with ABCs

```python
from abc import ABC, abstractmethod

class Readable(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

class Writable(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass

class Closeable(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

class FileHandler(Readable, Writable, Closeable):
    """Implements multiple interfaces."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self._content = ""
    
    def read(self) -> str:
        return self._content
    
    def write(self, data: str) -> None:
        self._content = data
    
    def close(self) -> None:
        print(f"Closing {self.filename}")

# Usage
handler = FileHandler("test.txt")
handler.write("Hello, World!")
print(handler.read())  # "Hello, World!"
handler.close()
```

---

## 5. Template Method Pattern

```python
from abc import ABC, abstractmethod
from typing import List

class DataProcessor(ABC):
    """Template method pattern with ABC."""
    
    def process(self, data: List[dict]) -> List[dict]:
        """Template method - defines the processing pipeline."""
        validated = self.validate(data)
        transformed = self.transform(validated)
        filtered = self.filter(transformed)
        return self.store(filtered)
    
    @abstractmethod
    def validate(self, data: List[dict]) -> List[dict]:
        """Validate data. Must be implemented."""
        pass
    
    @abstractmethod
    def transform(self, data: List[dict]) -> List[dict]:
        """Transform data. Must be implemented."""
        pass
    
    def filter(self, data: List[dict]) -> List[dict]:
        """Default filtering - can be overridden."""
        return data
    
    @abstractmethod
    def store(self, data: List[dict]) -> List[dict]:
        """Store processed data. Must be implemented."""
        pass

class UserDataProcessor(DataProcessor):
    def validate(self, data: List[dict]) -> List[dict]:
        return [d for d in data if "email" in d]
    
    def transform(self, data: List[dict]) -> List[dict]:
        return [{**d, "email": d["email"].lower()} for d in data]
    
    def filter(self, data: List[dict]) -> List[dict]:
        return [d for d in data if d.get("active", True)]
    
    def store(self, data: List[dict]) -> List[dict]:
        print(f"Storing {len(data)} users")
        return data

# Usage
processor = UserDataProcessor()
data = [
    {"name": "Alice", "email": "ALICE@test.com", "active": True},
    {"name": "Bob", "active": False},
    {"name": "Charlie", "email": "charlie@test.com", "active": True},
]
result = processor.process(data)
# Stores 2 users (Bob filtered out by active, Bob filtered out by missing email)
```

---

## 6. Plugin Architecture with ABCs

```python
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional

class Plugin(ABC):
    """Base class for all plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @abstractmethod
    def execute(self, context: dict) -> dict:
        """Execute the plugin logic."""
        pass
    
    def __repr__(self) -> str:
        return f"<{self.name} v{self.version}>"

class PluginRegistry:
    """Registry for managing plugins."""
    
    _plugins: Dict[str, Type[Plugin]] = {}
    
    @classmethod
    def register(cls, plugin_class: Type[Plugin]) -> Type[Plugin]:
        """Register a plugin class."""
        cls._plugins[plugin_class.name] = plugin_class
        return plugin_class
    
    @classmethod
    def get(cls, name: str) -> Optional[Type[Plugin]]:
        """Get a plugin by name."""
        return cls._plugins.get(name)
    
    @classmethod
    def list_plugins(cls) -> list:
        """List all registered plugins."""
        return list(cls._plugins.keys())
    
    @classmethod
    def create(cls, name: str, **kwargs) -> Plugin:
        """Create a plugin instance."""
        plugin_class = cls.get(name)
        if plugin_class is None:
            raise ValueError(f"Plugin {name} not found")
        return plugin_class(**kwargs)

# Define plugins
@PluginRegistry.register
class DataValidationPlugin(Plugin):
    name = "data_validation"
    version = "1.0.0"
    
    def execute(self, context: dict) -> dict:
        data = context.get("data", [])
        valid = [d for d in data if d.get("valid", False)]
        return {"valid_data": valid, "count": len(valid)}

@PluginRegistry.register
class DataTransformPlugin(Plugin):
    name = "data_transform"
    version = "1.0.0"
    
    def execute(self, context: dict) -> dict:
        data = context.get("data", [])
        transformed = [{k: v.upper() if isinstance(v, str) else v 
                       for k, v in d.items()} for d in data]
        return {"transformed_data": transformed}

# Usage
print(PluginRegistry.list_plugins())  # ["data_validation", "data_transform"]

plugin = PluginRegistry.create("data_validation")
result = plugin.execute({"data": [{"valid": True}, {"valid": False}]})
print(result)  # {'valid_data': [{'valid': True}], 'count': 1}
```

---

## 7. ABCs in AI Engineering

### Model Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AIModel(ABC):
    """Abstract interface for AI models."""
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def input_shape(self) -> tuple:
        pass
    
    @property
    @abstractmethod
    def output_shape(self) -> tuple:
        pass
    
    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """Make a prediction."""
        pass
    
    @abstractmethod
    def train(self, training_data: Any, labels: Any, **kwargs) -> Dict[str, float]:
        """Train the model."""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Save model to disk."""
        pass
    
    @classmethod
    @abstractmethod
    def load(cls, path: str) -> "AIModel":
        """Load model from disk."""
        pass

class ImageClassifier(AIModel):
    def __init__(self, num_classes: int = 10):
        self.num_classes = num_classes
    
    @property
    def model_name(self) -> str:
        return "ImageClassifier"
    
    @property
    def input_shape(self) -> tuple:
        return (224, 224, 3)
    
    @property
    def output_shape(self) -> tuple:
        return (self.num_classes,)
    
    def predict(self, input_data):
        return [0.1] * self.num_classes
    
    def train(self, training_data, labels, epochs=10, lr=0.001):
        return {"loss": 0.5, "accuracy": 0.85}
    
    def save(self, path):
        print(f"Saving to {path}")
    
    @classmethod
    def load(cls, path):
        return cls()
```

### Data Pipeline Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Generator

class DataSource(ABC):
    @abstractmethod
    def read(self) -> Generator[Any, None, None]:
        """Yield data items."""
        pass
    
    @abstractmethod
    def validate(self, item: Any) -> bool:
        """Validate a single item."""
        pass

class DataTransformer(ABC):
    @abstractmethod
    def transform(self, item: Any) -> Any:
        """Transform a single item."""
        pass

class DataSink(ABC):
    @abstractmethod
    def write(self, item: Any) -> None:
        """Write a single item."""
        pass
    
    @abstractmethod
    def flush(self) -> None:
        """Flush pending writes."""
        pass

class Pipeline:
    def __init__(
        self,
        source: DataSource,
        transformers: list[DataTransformer],
        sink: DataSink
    ):
        self.source = source
        self.transformers = transformers
        self.sink = sink
    
    def run(self) -> int:
        """Execute the pipeline. Returns count of processed items."""
        count = 0
        for item in self.source.read():
            if not self.source.validate(item):
                continue
            
            for transformer in self.transformers:
                item = transformer.transform(item)
            
            self.sink.write(item)
            count += 1
        
        self.sink.flush()
        return count
```

---

## 8. `register()` for Virtual Subclasses

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass

class Circle:
    """Not inheriting from Drawable but registered as virtual subclass."""
    def draw(self) -> str:
        return "Drawing circle"

# Register as virtual subclass
Drawable.register(Circle)

# Now Circle is considered a subclass of Drawable
print(issubclass(Circle, Drawable))  # True

# Can use isinstance
c = Circle()
print(isinstance(c, Drawable))  # True

# Type checking works
def render(shape: Drawable) -> None:
    print(shape.draw())

render(c)  # Works!
```

---

## 9. Best Practices

1. **Use ABCs for interfaces** — define contracts for implementations
2. **Keep ABCs focused** — one responsibility per abstract class
3. **Use `@abstractmethod`** for required methods
4. **Provide default implementations** for optional methods
5. **Use abstract properties** for required attributes
6. **Document abstract methods** clearly
7. **Don't over-abstract** — not every class needs to be an ABC
8. **Consider Protocol** for structural subtyping
9. **Use `register()`** for third-party class integration
10. **Test implementations** against the ABC contract

---

## 10. Practice Exercises

### Exercise 1: Storage Interface
Create an abstract `Storage` class with implementations:

```python
class Storage(ABC):
    @abstractmethod
    def get(self, key: str) -> Any: ...
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...
    
    @abstractmethod
    def delete(self, key: str) -> None: ...

class MemoryStorage(Storage): ...
class RedisStorage(Storage): ...
class FileStorage(Storage): ...
```

### Exercise 2: Plugin System
Design a plugin architecture for data processing:

```python
class Processor(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def process(self, data: list) -> list: ...
```

### Exercise 3: Model Trainer
Create an abstract trainer interface:

```python
class Trainer(ABC):
    @abstractmethod
    def train(self, model, data) -> dict: ...
    
    @abstractmethod
    def evaluate(self, model, data) -> dict: ...
    
    @abstractmethod
    def save_checkpoint(self, path) -> None: ...
```

### Exercise 4: Observer Pattern
Implement an Observer pattern using ABCs:

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: Any) -> None: ...

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None: ...
    
    @abstractmethod
    def detach(self, observer: Observer) -> None: ...
    
    @abstractmethod
    def notify(self, event: str, data: Any) -> None: ...
```

---

## 11. Summary

| Concept | Description |
|---------|-------------|
| **`ABC`** | Base class for abstract classes |
| **`@abstractmethod`** | Decorator marking required methods |
| **Abstract Property** | Required property attribute |
| **Abstract Class Method** | Required class method |
| **Abstract Static Method** | Required static method |
| **Template Method** | Algorithm skeleton with abstract steps |
| **Plugin Architecture** | Extensible system using ABCs |
| **`register()`** | Add virtual subclasses |
| **Interface Segregation** | Small, focused ABCs |
| **Multiple Inheritance** | Combine multiple ABCs |

ABCs are fundamental for designing extensible, maintainable Python systems. They enforce contracts, enable polymorphism, and support clean architecture patterns — essential for building robust AI engineering frameworks and plugin systems.

---

## Next Steps

In the next lecture, we'll explore **functools**, which provides powerful function tools that complement ABCs and decorators.
