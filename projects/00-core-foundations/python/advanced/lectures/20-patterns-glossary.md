# Glossary: Design Patterns

## Quick Reference Table

| Term | Definition | Type | Purpose |
|------|------------|------|---------|
| Singleton | One instance only | Creational | Single instance guarantee |
| Factory | Object creation abstraction | Creational | Decouple creation |
| Observer | One-to-many dependency | Behavioral | Event notification |
| Strategy | Algorithm interchangeability | Behavioral | Swap algorithms |
| Adapter | Interface compatibility | Structural | Interface conversion |
| Decorator | Dynamic behavior addition | Structural | Add responsibilities |
| Abstract Class | Interface definition | Structural | Define contracts |
| Subject | Observable object | Behavioral | Notify observers |
| Observer | Subscriber to events | Behavioral | Receive notifications |
| Concrete Class | Implementation class | Creational | Provide implementation |

---

## Alphabetical Definitions

### Abstract Class

**Definition**: A class that cannot be instantiated and defines an interface for other classes. Used to establish contracts that concrete classes must implement.

**Example**:
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius

# shape = Shape()  # TypeError: Can't instantiate abstract class
circle = Circle(5)
print(f"Area: {circle.area():.2f}")
```

**Related Terms**: Interface, concrete class, ABC

---

### Adapter

**Definition**: A structural pattern that converts the interface of one class into another interface clients expect, allowing incompatible classes to work together.

**Example**:
```python
class EuropeanSocket:
    def voltage(self):
        return 230

class AmericanSocket:
    def voltage(self):
        return 120

class USAdapter:
    def __init__(self, socket):
        self._socket = socket
    
    def voltage(self):
        return self._socket.voltage()
    
    def earth(self):
        return 0

class Laptop:
    def __init__(self, socket):
        self._socket = socket
    
    def charge(self):
        return f"Charging at {self._socket.voltage()}V"

# Usage
european = EuropeanSocket()
american = AmericanSocket()
adapter = USAdapter(american)

laptop1 = Laptop(european)
laptop2 = Laptop(adapter)

print(laptop1.charge())  # Charging at 230V
print(laptop2.charge())  # Charging at 120V
```

**Related Terms**: Interface, compatibility, wrapper

---

### Concrete Class

**Definition**: A class that provides implementations for all abstract methods defined in its parent abstract class. Can be instantiated.

**Example**:
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

# animal = Animal()  # Can't instantiate abstract
dog = Dog()  # Can instantiate concrete
cat = Cat()

print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

**Related Terms**: Abstract class, implementation, instantiation

---

### Creational Pattern

**Definition**: Design patterns that deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

**Examples**: Singleton, Factory, Abstract Factory, Builder, Prototype

**Related Terms**: Factory, Singleton, Builder

---

### Decorator Pattern

**Definition**: A structural pattern that allows adding new behaviors to objects dynamically by wrapping them in decorator objects.

**Example**:
```python
from abc import ABC, abstractmethod

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str:
        pass

class PlainText(TextProcessor):
    def process(self, text: str) -> str:
        return text

class TextDecorator(TextProcessor):
    def __init__(self, processor: TextProcessor):
        self._processor = processor
    
    def process(self, text: str) -> str:
        return self._processor.process(text)

class UpperCase(TextDecorator):
    def process(self, text: str) -> str:
        return self._processor.process(text).upper()

class TrimSpaces(TextDecorator):
    def process(self, text: str) -> str:
        return self._processor.process(text).strip()

# Usage
processor = TrimSpaces(UpperCase(PlainText()))
result = processor.process("  hello world  ")
print(result)  # HELLO WORLD
```

**Related Terms**: Wrapper, composition, dynamic behavior

---

### Factory Pattern

**Definition**: A creational pattern that provides an interface for creating objects without specifying their concrete classes.

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

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

class AnimalFactory:
    _creators = {
        "dog": Dog,
        "cat": Cat,
    }
    
    @classmethod
    def create(cls, animal_type: str) -> Animal:
        creator = cls._creators.get(animal_type.lower())
        if not creator:
            raise ValueError(f"Unknown animal type: {animal_type}")
        return creator()

# Usage
dog = AnimalFactory.create("dog")
cat = AnimalFactory.create("cat")
print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

**Related Terms**: Abstract Factory, Creator, Product

---

### Observer Pattern

**Definition**: A behavioral pattern that defines a one-to-many dependency between objects, so that when one object changes state, all its dependents are notified automatically.

**Example**:
```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data):
        pass

class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event: str, data):
        for observer in self._observers:
            observer.update(event, data)

class EventSystem(Subject):
    def emit(self, event: str, data):
        self.notify(event, data)

class LogObserver(Observer):
    def update(self, event: str, data):
        print(f"[LOG] {event}: {data}")

# Usage
system = EventSystem()
logger = LogObserver()
system.attach(logger)
system.emit("user_login", {"user": "Alice"})
```

**Related Terms**: Subject, Event, notification, pub-sub

---

### Pattern

**Definition**: A general, reusable solution to a commonly occurring problem within a given context in software design.

**Types**:
- **Creational**: Object creation (Singleton, Factory)
- **Structural**: Object composition (Adapter, Decorator)
- **Behavioral**: Object communication (Observer, Strategy)

**Related Terms**: Design, solution, best practice

---

### Singleton Pattern

**Definition**: A creational pattern that ensures a class has only one instance and provides a global point of access to it.

**Example**:
```python
class Singleton:
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

class DatabaseConnection(Singleton):
    def __init__(self):
        self.connected = True

# Usage
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True - same instance
```

**Related Terms**: Instance, global access, one instance

---

### Strategy Pattern

**Definition**: A behavioral pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable.

**Example**:
```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data.copy()
        for i in range(len(arr)):
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

# Usage
data = [64, 34, 25, 12, 22, 11, 90]
sorter = Sorter(BubbleSort())
print(f"Bubble: {sorter.sort(data)}")

sorter.set_strategy(QuickSort())
print(f"Quick: {sorter.sort(data)}")
```

**Related Terms**: Algorithm, interchangeability, context

---

### Structural Pattern

**Definition**: Design patterns that deal with object composition, creating relationships between objects to form larger structures.

**Examples**: Adapter, Decorator, Facade, Proxy

**Related Terms**: Adapter, Decorator, composition

---

### Subject

**Definition**: The object that maintains a list of observers and notifies them of state changes in the Observer pattern.

**Example**:
```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class Observer:
    def update(self, state):
        print(f"Observer received: {state}")
```

**Related Terms**: Observer, notification, state

---

## Concept Relationships

```
Design Patterns
├── Creational Patterns
│   ├── Singleton (one instance)
│   ├── Factory (object creation)
│   ├── Abstract Factory (families)
│   ├── Builder (complex objects)
│   └── Prototype (cloning)
│
├── Structural Patterns
│   ├── Adapter (interface conversion)
│   ├── Decorator (dynamic behavior)
│   ├── Facade (simplified interface)
│   └── Proxy (controlled access)
│
└── Behavioral Patterns
    ├── Observer (event notification)
    ├── Strategy (algorithm swap)
    ├── Command (encapsulated action)
    └── Iterator (sequential access)
```

---

## When to Use Each Pattern

| Pattern | Use Case |
|---------|----------|
| Singleton | Database, config, logger |
| Factory | Creating different object types |
| Observer | Event systems, notifications |
| Strategy | Different algorithms |
| Adapter | Integrating incompatible APIs |
| Decorator | Adding features without inheritance |

---

## Common Patterns

### 1. Singleton Pattern
```python
class Singleton:
    _instances = {}
    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
```

### 2. Factory Pattern
```python
class Factory:
    _creators = {}
    @classmethod
    def register(cls, type, creator):
        cls._creators[type] = creator
    @classmethod
    def create(cls, type):
        return cls._creators[type]()
```

### 3. Observer Pattern
```python
class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, observer):
        self._observers.append(observer)
    def notify(self, event, data):
        for obs in self._observers:
            obs.update(event, data)
```

### 4. Strategy Pattern
```python
class Context:
    def __init__(self, strategy):
        self._strategy = strategy
    def execute(self, data):
        return self._strategy.execute(data)
```

### 5. Adapter Pattern
```python
class Adapter:
    def __init__(self, adaptee):
        self._adaptee = adaptee
    def target_method(self):
        return self._adaptee.different_method()
```

---

## Pattern Selection Guide

```
Need to ensure only one instance?
└── Yes → Singleton

Need to create different object types?
└── Yes → Factory

Need to notify multiple objects of changes?
└── Yes → Observer

Need to swap algorithms at runtime?
└── Yes → Strategy

Need to make incompatible interfaces work together?
└── Yes → Adapter

Need to add responsibilities dynamically?
└── Yes → Decorator
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God Object | Too many responsibilities | Single Responsibility |
| Singleton Abuse | Global state everywhere | Use sparingly |
| Tight Coupling | Hard to change | Use interfaces |
| Over-Engineering | Unnecessary complexity | Keep it simple |
