# Python OOP Interview Practice

## Overview

Object-Oriented Programming (OOP) is a core paradigm in Python. This guide covers classes, inheritance, polymorphism, encapsulation, magic methods, abstract classes, descriptors, and metaclasses. Master these concepts to demonstrate deep Python knowledge in interviews.

---

## Interview Questions

### Q1: Explain the difference between a class and an instance.

**Answer:**
A class is a blueprint or template that defines the structure and behavior of objects. An instance is a specific object created from a class, with its own state (attributes).

```python
class Dog:
    species = "Canis familiaris"  # Class attribute (shared)
    
    def __init__(self, name, age):
        self.name = name    # Instance attribute (unique)
        self.age = age

# Class - the blueprint
print(Dog.species)  # Canis familiaris

# Instances - specific objects
buddy = Dog("Buddy", 3)
charlie = Dog("Charlie", 5)

print(buddy.name)    # Buddy
print(charlie.name)  # Charlie
print(buddy.species) # Canis familiaris (inherits from class)
```

---

### Q2: What is the purpose of `__init__` and `__new__` methods?

**Answer:**
`__new__` creates the instance (allocates memory), while `__init__` initializes the instance after creation.

```python
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value):
        self.value = value

# __new__ is also used for immutable types
class FrozenList:
    def __new__(cls, items):
        instance = super().__new__(cls)
        instance._items = tuple(items)  # Make immutable
        return instance

s1 = Singleton(1)
s2 = Singleton(2)
print(s1 is s2)      # True - same instance
print(s1.value)      # 2 - last initialization wins
```

---

### Q3: Explain inheritance and its types in Python.

**Answer:**
Python supports single, multiple, and multilevel inheritance. Method Resolution Order (MRO) determines the lookup order.

```python
# Single Inheritance
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof!"

# Multiple Inheritance
class Flyer:
    def fly(self):
        return "Flying"

class Swimmer:
    def swim(self):
        return "Swimming"

class Duck(Animal, Flyer, Swimmer):
    def speak(self):
        return "Quack!"

# Method Resolution Order (MRO)
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Animal'>, <class 'Flyer'>, <class 'Swimmer'>, <class 'object'>)
```

---

### Q4: What is polymorphism and how is it achieved in Python?

**Answer:**
Polymorphism allows objects of different classes to be treated as objects of a common base class. Python achieves this through duck typing.

```python
class Cat:
    def speak(self):
        return "Meow"

class Dog:
    def speak(self):
        return "Woof"

class Duck:
    def speak(self):
        return "Quack"

# Polymorphism in action
def animal_sound(animal):
    print(animal.speak())

# Works with any object that has a speak() method
animals = [Cat(), Dog(), Duck()]
for animal in animals:
    animal_sound(animal)

# Duck typing - "If it walks like a duck and quacks like a duck..."
# We don't care about the actual type
def make_sound(animal):
    return animal.speak()  # Works if animal has speak() method
```

---

### Q5: Explain encapsulation and access modifiers in Python.

**Answer:**
Python uses naming conventions for access control: public, protected (`_`), and private (`__`).

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance          # Public
        self._account_type = "savings"  # Protected (convention)
        self.__pin = 1234               # Private (name mangling)
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def _validate(self, pin):
        """Protected method - convention only"""
        return pin == self.__pin
    
    def __encrypt(self, data):
        """Private method - name mangled"""
        return f"encrypted_{data}"

account = BankAccount(1000)
print(account.balance)        # 1000 - accessible
print(account._account_type)  # savings - accessible (not enforced)
# print(account.__pin)        # AttributeError
print(account._BankAccount__pin)  # 1234 - accessible via name mangling
```

---

### Q6: What are class methods and static methods?

**Answer:**
Class methods receive the class as the first argument. Static methods don't receive any implicit first argument.

```python
class Employee:
    employee_count = 0
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.employee_count += 1
    
    @classmethod
    def from_string(cls, emp_string):
        """Factory method using class method"""
        name, salary = emp_string.split("-")
        return cls(name, float(salary))
    
    @staticmethod
    def is_workday(day):
        """Utility function - no access to class or instance"""
        return day.weekday() < 5
    
    @classmethod
    def get_count(cls):
        return cls.employee_count

# Usage
emp1 = Employee("Alice", 50000)
emp2 = Employee.from_string("Bob-60000")  # Factory method
print(Employee.get_count())  # 2

# Static method doesn't need class or instance
from datetime import date
print(Employee.is_workday(date.today()))
```

---

### Q7: Explain the property decorator and its use cases.

**Answer:**
Properties provide a way to implement getters, setters, and deleters with a clean attribute-like syntax.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Getter - accessed like an attribute"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Setter - with validation"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """Deleter"""
        print("Deleting radius")
        del self._radius
    
    @property
    def area(self):
        """Read-only property"""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)      # 5
c.radius = 10        # Setter called
print(c.area)        # 314.159... (read-only)
# c.area = 100       # AttributeError - no setter
```

---

### Q8: What are magic/dunder methods? Give examples.

**Answer:**
Magic methods (double underscore methods) enable operator overloading and special behaviors.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector index out of range")

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)      # (4, 6) - __add__
print(v1 - v2)      # (-2, -2) - __sub__
print(v1 * 3)       # (3, 6) - __mul__
print(v1 == v2)     # False - __eq__
print(len(v1))      # 2 - __len__
print(v1[0])        # 1 - __getitem__
```

---

### Q9: Explain the `__slots__` mechanism.

**Answer:**
`__slots__` restricts attributes and saves memory by preventing `__dict__` creation.

```python
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlotPoint:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

regular = RegularPoint(1, 2)
slot = SlotPoint(1, 2)

# Regular point has __dict__
print(hasattr(regular, '__dict__'))  # True
# print(hasattr(slot, '__dict__'))   # False

# Memory comparison
import sys
print(sys.getsizeof(regular) + sys.getsizeof(regular.__dict__))  # ~400+ bytes
print(sys.getsizeof(slot))  # ~56 bytes

# Slots restrict attribute assignment
slot.z = 3  # AttributeError: 'SlotPoint' object has no attribute 'z'
```

---

### Q10: What are abstract classes and when would you use them?

**Answer:**
Abstract classes cannot be instantiated and define a common interface for subclasses. They're implemented using the `abc` module.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def describe(self):
        """Concrete method - can be inherited as-is"""
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# shape = Shape()  # TypeError: Can't instantiate abstract class
rect = Rectangle(5, 3)
circle = Circle(4)
print(rect.describe())   # Rectangle: area=15.00
print(circle.describe()) # Circle: area=50.27
```

---

### Q11: What is the MRO (Method Resolution Order)?

**Answer:**
MRO determines the order in which Python looks up methods in a class hierarchy, using the C3 linearization algorithm.

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

# Python uses C3 linearization to determine MRO
# It ensures:
# 1. Children come before parents
# 2. Multiple inheritance follows declaration order
# 3. No class appears before its descendants
```

---

### Q12: How do you implement `__hash__` and `__eq__` for custom objects?

**Answer:**
When implementing `__eq__`, you should also implement `__hash__` if objects need to be used in sets or as dictionary keys.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# Usage
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)         # True
print(hash(p1) == hash(p2))  # True

# Can now use in sets and dicts
point_set = {p1, p2, p3}
print(len(point_set))   # 2 (p1 and p2 are equal)

point_dict = {p1: "first"}
print(point_dict[p2])   # "first" (p2 equals p1)
```

---

### Q13: Explain descriptors and their use cases.

**Answer:**
Descriptors are objects that define `__get__`, `__set__`, or `__delete__` methods to customize attribute access.

```python
class Validated:
    def __init__(self, validator):
        self.validator = validator
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        obj.__dict__[self.name] = value

class Person:
    name = Validated(lambda x: isinstance(x, str) and len(x) > 0)
    age = Validated(lambda x: isinstance(x, int) and 0 <= x <= 150)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Usage
p = Person("Alice", 30)
print(p.name)  # Alice

# p = Person("", 30)   # ValueError: Invalid value for name
# p = Person("Alice", 200)  # ValueError: Invalid value for age
```

---

### Q14: What are metaclasses?

**Answer:**
Metaclasses are classes whose instances are classes. They control how classes are created.

```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

# Both variables reference the same instance
db1 = Database()
db2 = Database()
print(db1 is db2)  # True

# Another example - auto-registration
class PluginMeta(type):
    plugins = {}
    
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "Plugin":
            PluginMeta.plugins[name] = cls

class Plugin(metaclass=PluginMeta):
    pass

class Logger(Plugin):
    pass

class Auth(Plugin):
    pass

print(PluginMeta.plugins)  # {'Logger': <class 'Logger'>, 'Auth': <class 'Auth'>}
```

---

### Q15: Explain composition vs inheritance.

**Answer:**
Composition builds complex objects by combining simpler ones (has-a relationship), while inheritance creates specialized versions (is-a relationship).

```python
# Inheritance approach
class Engine:
    def start(self):
        return "Engine started"

class Car(Engine):  # Car IS-A Engine? Not really...
    pass

# Composition approach (preferred)
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Car HAS-A Engine
    
    def start(self):
        return self.engine.start()

# More complex example
class Wheels:
    def __init__(self, count):
        self.count = count

class GPS:
    def __init__(self):
        self.location = None
    
    def locate(self):
        return "Locating..."

class ModernCar:
    def __init__(self):
        self.engine = Engine()
        self.wheels = Wheels(4)
        self.gps = GPS()
    
    def start(self):
        self.gps.locate()
        return self.engine.start()
```

---

## Coding Challenges

### Challenge 1: Implement a Stack Class

**Problem:** Create a Stack class with push, pop, peek, and is_empty methods.

**Solution:**
```python
class Stack:
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def __len__(self):
        return len(self._items)
    
    def __repr__(self):
        return f"Stack({self._items})"

# Test
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.peek())   # 3
print(stack.pop())    # 3
print(stack.pop())    # 2
print(len(stack))     # 1
```

---

### Challenge 2: Implement a Queue with Deque

**Problem:** Create a Queue class using collections.deque with enqueue, dequeue, and size methods.

**Solution:**
```python
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item):
        self._items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[0]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def __repr__(self):
        return f"Queue({list(self._items)})"

# Test
queue = Queue()
queue.enqueue("first")
queue.enqueue("second")
queue.enqueue("third")
print(queue.dequeue())  # first
print(queue.peek())     # second
print(queue.size())     # 2
```

---

### Challenge 3: Implement a Linked List

**Problem:** Create a singly linked list with append, delete, and search operations.

**Solution:**
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def delete(self, data):
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        return False
    
    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes) if nodes else "Empty"

# Test
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(ll)           # 1 -> 2 -> 3
ll.delete(2)
print(ll)           # 1 -> 3
print(ll.search(3)) # True
```

---

### Challenge 4: Implement a Binary Tree

**Problem:** Create a binary search tree with insert, search, and traversal methods.

**Solution:**
```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

# Test
bst = BST()
for val in [5, 3, 7, 1, 4, 6, 8]:
    bst.insert(val)

print(bst.inorder())   # [1, 3, 4, 5, 6, 7, 8]
print(bst.search(4))   # True
print(bst.search(9))   # False
```

---

### Challenge 5: Implement a LRU Cache

**Problem:** Create an LRU (Least Recently Used) cache using OrderedDict.

**Solution:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def __repr__(self):
        return f"LRUCache({dict(self.cache)})"

# Test
cache = LRUCache(3)
cache.put(1, "one")
cache.put(2, "two")
cache.put(3, "three")
print(cache.get(1))    # one
cache.put(4, "four")   # Evicts key 2
print(cache.get(2))    # -1 (not found)
```

---

### Challenge 6: Implement an Iterator Class

**Problem:** Create a custom iterator for Fibonacci sequence.

**Solution:**
```python
class FibonacciIterator:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value

# Test
fib = FibonacciIterator(10)
print(list(fib))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Or use it in a for loop
for num in FibonacciIterator(5):
    print(num, end=" ")  # 0 1 1 2 3
```

---

### Challenge 7: Implement a Context Manager

**Problem:** Create a context manager for file handling with automatic cleanup.

**Solution:**
```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        return False  # Don't suppress exceptions

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")

# Alternative using contextlib
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    file = open(filename, mode)
    try:
        yield file
    finally:
        file.close()

with file_manager("test.txt", "r") as f:
    print(f.read())
```

---

### Challenge 8: Implement a Descriptor-Based Validation System

**Problem:** Create descriptors for type validation and range checking.

**Solution:**
```python
class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        obj.__dict__[self.name] = value

class Range:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not self.min_val <= value <= self.max_val:
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        obj.__dict__[self.name] = value

class Student:
    name = Typed(str)
    age = Range(0, 150)
    gpa = Range(0.0, 4.0)
    
    def __init__(self, name, age, gpa):
        self.name = name
        self.age = age
        self.gpa = gpa

# Usage
s = Student("Alice", 20, 3.8)
print(s.name, s.age, s.gpa)
# s = Student(123, 20, 3.8)  # TypeError: name must be str
# s = Student("Alice", 200, 3.8)  # ValueError: age must be between 0 and 150
```

---

## Common Follow-up Questions

1. **"When should you use inheritance vs composition?"**
   - Use inheritance for true "is-a" relationships (Dog IS-A Animal)
   - Use composition for "has-a" relationships (Car HAS-A Engine)
   - Favor composition for flexibility and loose coupling

2. **"What is the diamond problem and how does Python handle it?"**
   - Diamond problem occurs with multiple inheritance when a class inherits from two classes that have a common base
   - Python uses C3 linearization (MRO) to determine method lookup order

3. **"When would you use a metaclass?"**
   - For validation, registration, or modification of classes at creation time
   - Examples: Singleton pattern, ORM frameworks, plugin systems
   - Often overkill - decorators or class methods can achieve similar results

4. **"What is the difference between `__str__` and `__repr__`?"**
   - `__str__` returns user-friendly string representation
   - `__repr__` returns developer-friendly unambiguous representation
   - Always implement `__repr__`; `__str__` falls back to `__repr__` if not defined

5. **"How do you handle multiple inheritance safely?"**
   - Use mixins for adding functionality
   - Ensure classes have clear responsibilities
   - Use `super()` consistently
   - Be aware of MRO and potential conflicts

---

## Tips for Answering

1. **Know the "why"** - Explain why OOP is useful, not just how to implement it
2. **Discuss trade-offs** - Inheritance creates coupling; composition is more flexible
3. **Show practical examples** - Use real-world analogies (Animal, Shape, etc.)
4. **Understand Python's approach** - Python uses duck typing; interfaces are implicit
5. **Mention PEP standards** - PEP 8, PEP 3119 (abstract classes)
6. **Be familiar with real-world usage** - Django uses models, metaclasses in ORMs
7. **Practice explaining MRO** - This is a common interview topic
8. **Know when NOT to use OOP** - Sometimes functions are simpler
9. **Discuss testing** - How OOP affects testability (mocking, dependency injection)
10. **Stay current** - Python 3.10+ has match statements, structural pattern matching

---

## Key Concepts to Review

| Concept | Key Points |
|---------|-----------|
| Classes | Blueprints for objects, instance vs class attributes |
| Inheritance | Code reuse, is-a relationship, MRO |
| Polymorphism | Duck typing, interface flexibility |
| Encapsulation | Name mangling, conventions, properties |
| Magic Methods | Operator overloading, special behaviors |
| Abstract Classes | Interface definition, ABC module |
| Descriptors | Custom attribute access, validation |
| Metaclasses | Class creation control, advanced patterns |
| Composition | Has-a relationship, flexibility |

---

*Master these concepts to confidently handle OOP questions in any Python interview. Practice explaining them clearly and with examples!*