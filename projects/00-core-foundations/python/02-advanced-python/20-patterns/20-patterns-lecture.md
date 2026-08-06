# Lecture 20: Design Patterns

## Topic Overview

Design patterns are reusable solutions to common software design problems. They provide proven approaches to recurring challenges, making code more maintainable, flexible, and understandable. This lecture covers the most commonly used patterns in Python development.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement the Singleton pattern** for single-instance classes
2. **Use the Factory pattern** for flexible object creation
3. **Apply the Observer pattern** for event-driven systems
4. **Utilize the Strategy pattern** for algorithm interchangeability
5. **Implement the Adapter pattern** for interface compatibility
6. **Apply the Decorator pattern** for dynamic behavior addition
7. **Choose the right pattern** for different scenarios

---

## Key Concepts

### 1. Singleton Pattern

Ensure only one instance of a class exists throughout the application.

#### Basic Singleton

```python
class Singleton:
    """Singleton using metaclass."""
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

class DatabaseConnection(Singleton):
    def __init__(self):
        self.connected = True
    
    def query(self, sql):
        return f"Executing: {sql}"

# Only one instance is created
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(f"Same instance: {db1 is db2}")  # True
```

#### Thread-Safe Singleton

```python
import threading

class ThreadSafeSingleton:
    _instances = {}
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
```

---

### 2. Factory Pattern

Create objects without specifying their exact class, delegating instantiation to a factory method.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass
    
    @abstractmethod
    def move(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"
    
    def move(self) -> str:
        return "Runs on 4 legs"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"
    
    def move(self) -> str:
        return "Sneaks quietly"

class Bird(Animal):
    def speak(self) -> str:
        return "Tweet!"
    
    def move(self) -> str:
        return "Flies in the sky"

class AnimalFactory:
    _creators = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
    }
    
    @classmethod
    def register(cls, animal_type: str, creator: type):
        cls._creators[animal_type] = creator
    
    @classmethod
    def create(cls, animal_type: str) -> Animal:
        creator = cls._creators.get(animal_type.lower())
        if not creator:
            raise ValueError(f"Unknown animal type: {animal_type}")
        return creator()

# Usage
for animal_type in ["dog", "cat", "bird"]:
    animal = AnimalFactory.create(animal_type)
    print(f"{animal_type}: {animal.speak()} - {animal.move()}")
```

---

### 3. Observer Pattern

Define a one-to-many dependency between objects so that when one object changes state, all dependents are notified.

```python
from abc import ABC, abstractmethod
from typing import Any, List

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: Any):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event: str, data: Any = None):
        for observer in self._observers:
            observer.update(event, data)

class EventSystem(Subject):
    def __init__(self):
        super().__init__()
        self.events = {}
    
    def emit(self, event: str, data: Any = None):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append({"data": data})
        self.notify(event, data)

class LogObserver(Observer):
    def update(self, event: str, data: Any):
        print(f"[LOG] Event: {event}, Data: {data}")

class AlertObserver(Observer):
    def __init__(self, alert_events):
        self.alert_events = alert_events
    
    def update(self, event: str, data: Any):
        if event in self.alert_events:
            print(f"[ALERT] {event} occurred!")

# Usage
event_system = EventSystem()
log_observer = LogObserver()
alert_observer = AlertObserver(["error", "critical"])

event_system.attach(log_observer)
event_system.attach(alert_observer)

event_system.emit("info", "User logged in")
event_system.emit("error", "Database connection failed")
event_system.emit("critical", "System overload")
```

---

### 4. Strategy Pattern

Define a family of algorithms, encapsulate each one, and make them interchangeable.

```python
from abc import ABC, abstractmethod
from typing import List

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class BubbleSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class InsertionSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    @property
    def strategy(self) -> SortStrategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)

# Usage
data = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {data}")

sorter = Sorter(BubbleSort())
print(f"Bubble Sort: {sorter.sort(data)}")

sorter.strategy = QuickSort()
print(f"Quick Sort: {sorter.sort(data)}")

sorter.strategy = InsertionSort()
print(f"Insertion Sort: {sorter.sort(data)}")
```

---

### 5. Adapter Pattern

Convert the interface of a class into another interface clients expect.

```python
class EuropeanSocket:
    def voltage(self) -> int:
        return 230
    
    def live(self) -> int:
        return 1
    
    def neutral(self) -> int:
        return -1
    
    def earth(self) -> int:
        return 0

class AmericanSocket:
    def voltage(self) -> int:
        return 120
    
    def live(self) -> int:
        return 1
    
    def neutral(self) -> int:
        return -1

class USAdapter:
    def __init__(self, socket: AmericanSocket):
        self._socket = socket
    
    def voltage(self) -> int:
        return self._socket.voltage()
    
    def live(self) -> int:
        return self._socket.live()
    
    def neutral(self) -> int:
        return self._socket.neutral()
    
    def earth(self) -> int:
        return 0  # No earth in American socket

class Laptop:
    def __init__(self, socket):
        self._socket = socket
    
    def charge(self) -> str:
        return f"Charging at {self._socket.voltage()}V"

# Usage
european = EuropeanSocket()
american = AmericanSocket()
adapter = USAdapter(american)

laptop1 = Laptop(european)
laptop2 = Laptop(adapter)

print(f"European socket: {laptop1.charge()}")
print(f"American socket (adapted): {laptop2.charge()}")
```

---

### 6. Decorator Pattern (Class-based)

Dynamically add responsibilities to objects without modifying their class.

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

class AddExclamation(TextDecorator):
    def process(self, text: str) -> str:
        return self._processor.process(text) + "!"

# Usage
text = "  Hello World  "
print(f"Original: '{text}'")

processor = PlainText()
print(f"Plain: '{processor.process(text)}'")

processor = UpperCase(PlainText())
print(f"Upper: '{processor.process(text)}'")

processor = TrimSpaces(UpperCase(PlainText()))
print(f"Trim+Upper: '{processor.process(text)}'")

processor = AddExclamation(TrimSpaces(UpperCase(PlainText())))
print(f"Trim+Upper+Excl: '{processor.process(text)}'")
```

---

## Common Mistakes to Avoid

### 1. Overusing Singleton

```python
# BAD - making everything a singleton
class UserService(Singleton):
    pass

# GOOD - only when truly needed
class DatabaseConnection(Singleton):
    pass
```

### 2. Not Using Interfaces

```python
# BAD - no interface
class Dog:
    def speak(self):
        return "Woof"

# GOOD - use ABC
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof"
```

### 3. Tight Coupling

```python
# BAD - tightly coupled
class ConcreteObserver:
    def update(self, data):
        print(data)

# GOOD - use abstract base class
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass
```

---

## Best Practices

### 1. Prefer Composition Over Inheritance

```python
# BAD - inheritance
class SmartList(list):
    def custom_method(self):
        pass

# GOOD - composition
class SmartList:
    def __init__(self):
        self._list = []
    
    def append(self, item):
        self._list.append(item)
```

### 2. Program to Interface

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, id):
        pass
    
    @abstractmethod
    def save(self, entity):
        pass

# Can swap implementations
class SQLRepository(Repository):
    def get(self, id):
        pass
    
    def save(self, entity):
        pass

class MongoRepository(Repository):
    def get(self, id):
        pass
    
    def save(self, entity):
        pass
```

### 3. Keep Patterns Simple

```python
# BAD - complex factory
class ComplexFactory:
    def create(self, type, *args, **kwargs):
        if type == "a":
            return A(*args, **kwargs)
        elif type == "b":
            return B(*args, **kwargs)
        # ... 50 more elifs

# GOOD - simple factory with registry
class Factory:
    _creators = {}
    
    @classmethod
    def register(cls, type, creator):
        cls._creators[type] = creator
    
    @classmethod
    def create(cls, type):
        return cls._creators[type]()
```

---

## Practice Exercises

### Exercise 1: Observer Pattern
```python
"""
Implement an Observer pattern for a news agency:
- NewsAgency (Subject)
- NewsChannel (Observer)
- SportsChannel, WeatherChannel (Concrete Observers)
"""
# Your code here
```

### Exercise 2: Strategy Pattern
```python
"""
Implement a Strategy pattern for compression:
- CompressionStrategy interface
- ZIP, RAR, GZIP strategies
- Compressor context class
"""
# Your code here
```

### Exercise 3: Factory Pattern
```python
"""
Implement a Factory pattern for UI elements:
- Button, TextBox, CheckBox
- WindowsFactory, MacFactory
- UIFactory interface
"""
# Your code here
```

---

## Summary

### Pattern Categories

| Pattern | Type | Purpose |
|---------|------|---------|
| Singleton | Creational | One instance |
| Factory | Creational | Object creation |
| Observer | Behavioral | Event notification |
| Strategy | Behavioral | Algorithm interchange |
| Adapter | Structural | Interface compatibility |
| Decorator | Structural | Dynamic behavior |

### When to Use Each Pattern

| Pattern | Use Case |
|---------|----------|
| Singleton | Database connections, config |
| Factory | Creating different object types |
| Observer | Event systems, notifications |
| Strategy | Different algorithms |
| Adapter | Integrating incompatible interfaces |
| Decorator | Adding features without inheritance |

### Key Takeaways

1. **Singleton**: Use sparingly, for true single-instance needs
2. **Factory**: Decouple creation from usage
3. **Observer**: Build event-driven systems
4. **Strategy**: Make algorithms interchangeable
5. **Adapter**: Integrate incompatible interfaces
6. **Decorator**: Add features dynamically

---

## Further Reading

- [Python design patterns](https://python-patterns.guide/)
- [Gang of Four patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru](https://refactoring.guru/design-patterns)
