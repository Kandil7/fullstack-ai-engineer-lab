# Inheritance in Python

## Topic 35: Building Class Hierarchies

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of inheritance
2. Create child classes from parent classes
3. Use the `super()` function
4. Implement method overriding
5. Work with multiple inheritance
6. Apply inheritance in real-world scenarios

---

## 1. What is Inheritance?

Inheritance allows a class to **inherit attributes and methods** from another class.

### Benefits of Inheritance

- **Code Reuse**: Share common functionality
- **Hierarchy**: Model real-world relationships
- **Polymorphism**: Treat objects uniformly
- **Maintainability**: Changes in parent affect children

### Parent and Child Classes

```python
# Parent (base) class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "..."

# Child (derived) class
class Dog(Animal):
    def speak(self):
        return "Woof!"

# Usage
dog = Dog("Buddy")
print(dog.name)      # Buddy (inherited from Animal)
print(dog.speak())   # Woof! (overridden in Dog)
```

---

## 2. Basic Inheritance

### Simple Example

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def describe(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        super().__init__(make, model, year)
        self.doors = doors
    
    def describe(self):
        base = super().describe()
        return f"{base} with {self.doors} doors"

# Usage
car = Car("Toyota", "Camry", 2024, 4)
print(car.describe())  # 2024 Toyota Camry with 4 doors
```

### Checking Inheritance

```python
print(isinstance(car, Car))      # True
print(isinstance(car, Vehicle))  # True
print(issubclass(Car, Vehicle))  # True
print(issubclass(Vehicle, Car))  # False
```

---

## 3. The `super()` Function

Calls methods from the parent class.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hi, I'm {self.name}"

class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)  # Call parent constructor
        self.school = school
    
    def greet(self):
        parent_greeting = super().greet()  # Call parent method
        return f"{parent_greeting} and I attend {self.school}"

student = Student("Alice", 20, "MIT")
print(student.greet())  # Hi, I'm Alice and I attend MIT
```

---

## 4. Method Overriding

Child classes can override parent methods.

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subclass must implement speak()")
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

class Dog(Animal):
    def speak(self):
        return "Woof!"
    
    def fetch(self, item):
        return f"{self.name} fetches the {item}"

class Cat(Animal):
    def speak(self):
        return "Meow!"
    
    def purr(self):
        return f"{self.name} purrs..."

# Polymorphism in action
animals = [Dog("Buddy"), Cat("Whiskers")]
for animal in animals:
    print(f"{animal}: {animal.speak()}")
# Dog: Buddy: Woof!
# Cat: Whiskers: Meow!
```

---

## 5. Multiple Inheritance

A class can inherit from multiple parents.

```python
class Swimmer:
    def swim(self):
        return "Swimming..."

class Flyer:
    def fly(self):
        return "Flying..."

class Duck(Animal, Swimmer, Flyer):
    def speak(self):
        return "Quack!"

# Duck inherits from Animal, Swimmer, and Flyer
duck = Duck("Donald")
print(duck.speak())   # Quack!
print(duck.swim())    # Swimming...
print(duck.fly())     # Flying...
```

### Method Resolution Order (MRO)

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

d = D()
print(d.method())  # B (follows MRO)
print(D.mro())     # Shows resolution order
```

---

## 6. Abstract Base Classes

Define interfaces that child classes must implement.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate area of shape."""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate perimeter of shape."""
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Usage
circle = Circle(5)
rect = Rectangle(4, 6)

shapes = [circle, rect]
for shape in shapes:
    print(f"{shape.__class__.__name__}: area={shape.area():.2f}")
```

---

## 7. Inheritance Patterns

### Template Method Pattern

```python
class DataProcessor(ABC):
    def process(self):
        """Template method."""
        self.load()
        self.transform()
        self.save()
    
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def transform(self):
        pass
    
    @abstractmethod
    def save(self):
        pass

class CSVProcessor(DataProcessor):
    def load(self):
        print("Loading CSV...")
    
    def transform(self):
        print("Transforming CSV data...")
    
    def save(self):
        print("Saving CSV...")
```

### Composition vs Inheritance

```python
# Inheritance: "is-a" relationship
class ElectricCar(Car):
    pass  # ElectricCar IS A Car

# Composition: "has-a" relationship
class ElectricCar:
    def __init__(self, engine):
        self.engine = engine  # ElectricCar HAS AN Engine
```

---

## 8. Common Mistakes to Avoid

### 1. Forgetting to Call super()

```python
class Child(Parent):
    def __init__(self, name, value):
        # BAD - Parent.__init__ not called
        self.value = value
    
    def __init__(self, name, value):
        # GOOD - Call super()
        super().__init__(name)
        self.value = value
```

### 2. Overusing Inheritance

```python
# BAD - Inheritance when composition is better
class Stack(list):  # Stack is-a list
    pass

# GOOD - Composition
class Stack:
    def __init__(self):
        self._items = []  # Stack has-a list
```

### 3. Not Using Abstract Classes

```python
# BAD - No enforcement
class Shape:
    def area(self):
        raise NotImplementedError

# GOOD - Abstract base class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

---

## 9. Best Practices

1. **Use inheritance** for "is-a" relationships
2. **Use composition** for "has-a" relationships
3. **Call `super()`** in constructors
4. **Use abstract classes** to enforce interfaces
5. **Keep hierarchies shallow** (2-3 levels max)
6. **Document** inheritance relationships
7. **Use `isinstance()`** sparingly
8. **Follow Liskov Substitution Principle**

---

## 10. Practice Exercises

### Exercise 1: Employee Hierarchy

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
    
    @abstractmethod
    def calculate_pay(self):
        pass
    
    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class HourlyEmployee(Employee):
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        super().__init__(name, employee_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    
    def calculate_pay(self):
        return self.hourly_rate * self.hours_worked

class SalariedEmployee(Employee):
    def __init__(self, name, employee_id, annual_salary):
        super().__init__(name, employee_id)
        self.annual_salary = annual_salary
    
    def calculate_pay(self):
        return self.annual_salary / 12

# Usage
hourly = HourlyEmployee("Alice", "E001", 25, 40)
salaried = SalariedEmployee("Bob", "E002", 60000)

print(f"{hourly}: ${hourly.calculate_pay():.2f}")
print(f"{salaried}: ${salaried.calculate_pay():.2f}")
```

---

## 11. Summary

| Concept | Key Points |
|---------|------------|
| **Inheritance** | Child inherits from parent |
| **super()** | Call parent methods |
| **Method overriding** | Child replaces parent method |
| **Multiple inheritance** | Inherit from multiple parents |
| **MRO** | Method resolution order |
| **Abstract classes** | Enforce interface contracts |

---

## Next Steps

- Learn about mixins and multiple inheritance patterns
- Study design patterns using inheritance
- Explore composition over inheritance
