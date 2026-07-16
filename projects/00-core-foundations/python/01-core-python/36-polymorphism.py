"""
W3Schools Python Tutorial - 36: Python Polymorphism
====================================================
Topics: Polymorphism concept, duck typing, method overriding

Run: python 36-polymorphism.py
Reference: https://www.w3schools.com/python/python_polymorphism.asp
"""

# ============================================================
# What is Polymorphism?
# ============================================================
# Polymorphism means "many forms". It allows objects of different
# classes to be treated as objects of a common parent class.
# The same method can behave differently for different classes.

# ============================================================
# Polymorphism in Practice
# ============================================================
# Example 1: Different classes, same method name
print("--- Polymorphism in Practice ---")

class Cat:
    def speak(self):
        return "Meow!"
    
    def __str__(self):
        return "Cat"

class Dog:
    def speak(self):
        return "Woof!"
    
    def __str__(self):
        return "Dog"

class Duck:
    def speak(self):
        return "Quack!"
    
    def __str__(self):
        return "Duck"

# Polymorphic function
def animal_sound(animal):
    """Works with any object that has a speak() method."""
    print(f"{animal}: {animal.speak()}")

# Create different animals
animals = [Cat(), Dog(), Duck()]

# Same function, different behavior
for animal in animals:
    animal_sound(animal)

# Output:
# Cat: Meow!
# Dog: Woof!
# Duck: Quack!

# ============================================================
# Polymorphism with Inheritance
# ============================================================
# Example 2: Polymorphism through inheritance
print("\n--- Polymorphism with Inheritance ---")

class Shape:
    def __init__(self, name):
        self.name = name
    
    def area(self):
        raise NotImplementedError("Subclass must implement area()")
    
    def describe(self):
        return f"{self.name}: Area = {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__("Triangle")
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

# Polymorphic function
def print_shape_info(shape):
    """Works with any Shape subclass."""
    print(f"  {shape.describe()}")

# Create different shapes
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 8)
]

print("\nShape Information:")
for shape in shapes:
    print_shape_info(shape)

# Output:
# Shape Information:
#   Circle: Area = 78.54
#   Rectangle: Area = 24.00
#   Triangle: Area = 12.00

# ============================================================
# Duck Typing
# ============================================================
# Example 3: "If it walks like a duck and quacks like a duck..."
print("\n--- Duck Typing ---")

class English:
    def greet(self):
        return "Hello!"

class Spanish:
    def greet(self):
        return "¡Hola!"

class French:
    def greet(self):
        return "Bonjour!"

def say_hello(language):
    """Works with any object that has a greet() method."""
    return language.greet()

# All different classes, same method, works perfectly
languages = [English(), Spanish(), French()]
for lang in languages:
    print(f"  {type(lang).__name__}: {say_hello(lang)}")

# Output:
#   English: Hello!
#   Spanish: ¡Hola!
#   French: Bonjour!

# ============================================================
# Polymorphism Built-in Functions
# ============================================================
# Example 4: len() is polymorphic
print("\n--- Built-in Polymorphism ---")

# len() works with different types
print(f"len('Hello'): {len('Hello')}")          # String
print(f"len([1,2,3]): {len([1,2,3])}")         # List
d = {1: 2, 3: 4}
print(f"len(d): {len(d)}") # Dict
print(f"len((1,2,3)): {len((1,2,3))}")         # Tuple

# + operator is polymorphic
print(f"\n5 + 3 = {5 + 3}")           # Integer addition
print(f"'Hello' + ' ' + 'World' = {'Hello' + ' ' + 'World'}")  # String concatenation
print(f"[1,2] + [3,4] = {[1,2] + [3,4]}")  # List concatenation

# print() works with anything
print(f"\nprint(42): ", end="")
print(42)
print(f"print('hello'): ", end="")
print("hello")
print(f"print([1,2,3]): ", end="")
print([1,2,3])

# ============================================================
# Abstract Base Classes
# ============================================================
# Example 5: Enforcing polymorphism with ABC
print("\n--- Abstract Base Classes ---")

from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        """Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def fuel_type(self):
        pass

class Car(Vehicle):
    def start(self):
        return "Car engine started"
    
    def stop(self):
        return "Car engine stopped"
    
    def fuel_type(self):
        return "Gasoline"

class ElectricCar(Vehicle):
    def start(self):
        return "Electric motor engaged"
    
    def stop(self):
        return "Electric motor disengaged"
    
    def fuel_type(self):
        return "Electricity"

# This would fail - can't instantiate abstract class:
# vehicle = Vehicle()  # TypeError

# Must implement all abstract methods:
class BrokenCar(Vehicle):
    pass  # Missing required methods

# broken = BrokenCar()  # TypeError: Can't instantiate abstract class

# Working classes
car = Car()
ev = ElectricCar()

def start_vehicle(vehicle):
    print(f"  {vehicle.start()}")
    print(f"  Fuel: {vehicle.fuel_type()}")

print("Starting vehicles:")
start_vehicle(car)
print()
start_vehicle(ev)

# ============================================================
# Practical Example
# ============================================================
# Example 6: Real-world polymorphism
print("\n--- Practical Example: Payment Processing ---")

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
    
    @abstractmethod
    def refund(self, amount):
        pass
    
    @abstractmethod
    def name(self):
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        return f"Charged ${amount:.2f} to card ending in {self.card_number[-4:]}"
    
    def refund(self, amount):
        return f"Refunded ${amount:.2f} to card ending in {self.card_number[-4:]}"
    
    def name(self):
        return "Credit Card"

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        return f"Paid ${amount:.2f} via PayPal ({self.email})"
    
    def refund(self, amount):
        return f"Refunded ${amount:.2f} to PayPal ({self.email})"
    
    def name(self):
        return "PayPal"

class CryptoWallet(PaymentMethod):
    def __init__(self, address):
        self.address = address
    
    def pay(self, amount):
        return f"Sent ${amount:.2f} from wallet {self.address[:8]}..."
    
    def refund(self, amount):
        return f"Returned ${amount:.2f} to wallet {self.address[:8]}..."
    
    def name(self):
        return "Crypto Wallet"

# Process payments polymorphically
payment_methods = [
    CreditCard("1234567890123456"),
    PayPal("user@example.com"),
    CryptoWallet("0x1234567890abcdef1234567890abcdef")
]

amount = 99.99
print(f"\nProcessing ${amount:.2f} payment:")
for method in payment_methods:
    print(f"  {method.name()}: {method.pay(amount)}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Polymorphism: same interface, different implementations")
print("2. Duck typing: if it has the method, it works")
print("3. Method overriding: child redefines parent method")
print("4. Built-in functions (len, print) are polymorphic")
print("5. ABC: enforce method implementation in subclasses")
print("6. Polymorphism enables flexible, extensible code")
print("7. Common in frameworks: same function, different behaviors")
