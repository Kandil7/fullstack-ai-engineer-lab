"""
W3Schools Python Tutorial - 35: Python Inheritance
===================================================
Topics: Parent/child classes, super(), method overriding

Run: python 35-inheritance.py
Reference: https://www.w3schools.com/python/python_inheritance.asp
"""

# ============================================================
# What is Inheritance?
# ============================================================
# Inheritance allows a class (child) to inherit attributes and
# methods from another class (parent). This promotes code reuse.

# ============================================================
# Parent and Child Classes
# ============================================================
# Example 1: Basic inheritance
print("--- Basic Inheritance ---")

class Animal:
    """Parent class: Animal"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def speak(self):
        """Default speak method."""
        return f"{self.name} makes a sound"
    
    def describe(self):
        return f"{self.name} is a {self.species}"

class Dog(Animal):
    """Child class: Dog inherits from Animal"""
    
    def __init__(self, name, breed):
        super().__init__(name, species="Dog")  # Call parent constructor
        self.breed = breed  # New attribute
    
    def speak(self):
        """Override parent's speak method."""
        return f"{self.name} says Woof!"
    
    def fetch(self):
        """New method specific to Dog."""
        return f"{self.name} fetches the ball!"

class Cat(Animal):
    """Child class: Cat inherits from Animal"""
    
    def __init__(self, name, color):
        super().__init__(name, species="Cat")
        self.color = color
    
    def speak(self):
        return f"{self.name} says Meow!"
    
    def purr(self):
        return f"{self.name} purrs..."

# Create instances
dog = Dog("Rex", "German Shepherd")
cat = Cat("Whiskers", "Orange")

print(f"Dog: {dog.describe()}")
print(f"Dog speaks: {dog.speak()}")
print(f"Dog fetches: {dog.fetch()}")

print(f"\nCat: {cat.describe()}")
print(f"Cat speaks: {cat.speak()}")
print(f"Cat purrs: {cat.purr()}")

# Output:
# Dog: Rex is a Dog
# Dog speaks: Rex says Woof!
# Dog fetches: Rex fetches the ball!
# 
# Cat: Whiskers is a Cat
# Cat speaks: Whiskers says Meow!
# Cat purrs: Whiskers purrs...

# ============================================================
# The super() Function
# ============================================================
# Example 2: Using super() to call parent methods
print("\n--- super() Function ---")

class Shape:
    def __init__(self, color="red"):
        self.color = color
    
    def describe(self):
        return f"A {self.color} shape"

class Circle(Shape):
    def __init__(self, radius, color="blue"):
        super().__init__(color)  # Call parent's __init__
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def describe(self):
        # Extend parent's describe
        base = super().describe()  # Call parent's describe
        return f"{base} with radius {self.radius}"

circle = Circle(5, "green")
print(f"Circle: {circle.describe()}")
print(f"Area: {circle.area():.2f}")

# Output:
# Circle: A green shape with radius 5
# Area: 78.54

# ============================================================
# Method Overriding
# ============================================================
# Example 3: Overriding parent methods
print("\n--- Method Overriding ---")

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False
    
    def start(self):
        self.is_running = True
        return f"{self.make} {self.model} started"
    
    def stop(self):
        self.is_running = False
        return f"{self.make} {self.model} stopped"
    
    def describe(self):
        return f"{self.year} {self.make} {self.model}"

class ElectricCar(Vehicle):
    def __init__(self, make, model, year, battery_size):
        super().__init__(make, model, year)
        self.battery_size = battery_size
        self.charge_level = 100
    
    def start(self):
        """Override to add battery check."""
        if self.charge_level < 10:
            return "Battery too low! Please charge first."
        return super().start()
    
    def charge(self):
        """New method for electric cars."""
        self.charge_level = 100
        return f"Battery charged to {self.charge_level}%"
    
    def describe(self):
        """Override to include battery info."""
        base = super().describe()
        return f"{base} (Battery: {self.charge_level}%)"

tesla = ElectricCar("Tesla", "Model 3", 2024, 75)
print(f"Car: {tesla.describe()}")
print(f"Start: {tesla.start()}")
print(f"Charge: {tesla.charge()}")

# Output:
# Car: 2024 Tesla Model 3 (Battery: 100%)
# Start: 2024 Tesla Model 3 started
# Charge: Battery charged to 100%

# ============================================================
# isinstance() and issubclass()
# ============================================================
# Example 4: Type checking
print("\n--- Type Checking ---")

dog = Dog("Rex", "Shepherd")
cat = Cat("Whiskers", "Gray")

print(f"dog is Animal: {isinstance(dog, Animal)}")    # True
print(f"dog is Dog: {isinstance(dog, Dog)}")          # True
print(f"dog is Cat: {isinstance(dog, Cat)}")          # False

print(f"Dog is subclass of Animal: {issubclass(Dog, Animal)}")  # True
print(f"Cat is subclass of Animal: {issubclass(Cat, Animal)}")  # True
print(f"Animal is subclass of Dog: {issubclass(Animal, Dog)}")  # False

# ============================================================
# Multiple Inheritance
# ============================================================
# Example 5: Inheriting from multiple classes
print("\n--- Multiple Inheritance ---")

class Flyable:
    def fly(self):
        return f"{self.name} is flying!"
    
    def land(self):
        return f"{self.name} has landed"

class Swimmable:
    def swim(self):
        return f"{self.name} is swimming!"
    
    def dive(self):
        return f"{self.name} is diving!"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name, species="Duck")
    
    def speak(self):
        return f"{self.name} says Quack!"

duck = Duck("Donald")
print(f"Duck: {duck.describe()}")
print(f"Speak: {duck.speak()}")
print(f"Fly: {duck.fly()}")
print(f"Swim: {duck.swim()}")

# Output:
# Duck: Donald is a Duck
# Speak: Donald says Quack!
# Fly: Donald is flying!
# Swim: Donald is swimming!

# ============================================================
# Practical Example
# ============================================================
# Example 6: Real-world inheritance
print("\n--- Practical Example: Employee Hierarchy ---")

class Employee:
    def __init__(self, name, employee_id, base_salary):
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary
    
    def calculate_pay(self):
        return self.base_salary
    
    def describe(self):
        return f"{self.name} (ID: {self.employee_id})"

class Manager(Employee):
    def __init__(self, name, employee_id, base_salary, team_size):
        super().__init__(name, employee_id, base_salary)
        self.team_size = team_size
    
    def calculate_pay(self):
        """Managers get bonus based on team size."""
        bonus = self.team_size * 1000
        return self.base_salary + bonus
    
    def describe(self):
        base = super().describe()
        return f"{base} - Manager (Team: {self.team_size})"

class Developer(Employee):
    def __init__(self, name, employee_id, base_salary, skills):
        super().__init__(name, employee_id, base_salary)
        self.skills = skills
    
    def calculate_pay(self):
        """Developers get bonus per skill."""
        bonus = len(self.skills) * 500
        return self.base_salary + bonus
    
    def describe(self):
        base = super().describe()
        return f"{base} - Developer (Skills: {', '.join(self.skills)})"

# Create employees
employees = [
    Manager("Alice", "M001", 120000, 5),
    Developer("Bob", "D001", 100000, ["Python", "JavaScript", "SQL"]),
    Developer("Charlie", "D002", 95000, ["Python", "Go"]),
]

print("\nEmployee Summary:")
for emp in employees:
    pay = emp.calculate_pay()
    print(f"  {emp.describe()} - Pay: ${pay:,.2f}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. class Child(Parent): inherits from parent class")
print("2. super().__init__(): call parent constructor")
print("3. super().method(): call parent method")
print("4. Override methods by redefining in child class")
print("5. isinstance(obj, Class): check object type")
print("6. issubclass(Child, Parent): check class hierarchy")
print("7. Multiple inheritance: class Child(Parent1, Parent2)")
print("8. MRO (Method Resolution Order): defines lookup order")
