"""
W3Schools Python Tutorial - 34: Python Classes/Objects
======================================================
Topics: Creating classes, __init__, self, properties, methods

Run: python 34-classes.py
Reference: https://www.w3schools.com/python/python_classes.asp
"""

# ============================================================
# What is a Class?
# ============================================================
# A class is a blueprint for creating objects.
# Objects are instances of classes.
# Classes bundle data (attributes) and functions (methods).

# ============================================================
# Creating a Class
# ============================================================
# Example 1: Basic class
class Dog:
    """A simple Dog class."""
    
    # Class attribute (shared by all instances)
    species = "Canis familiaris"
    
    # Initializer (constructor)
    def __init__(self, name, age):
        """Initialize the dog with name and age."""
        self.name = name    # Instance attribute
        self.age = age      # Instance attribute
    
    # Instance method
    def bark(self):
        """Return the dog's bark."""
        return f"{self.name} says Woof!"
    
    def description(self):
        """Return a description of the dog."""
        return f"{self.name} is {self.age} years old"

# Creating objects (instances)
dog1 = Dog("Rex", 5)
dog2 = Dog("Buddy", 3)

print(f"Dog 1: {dog1.name}, Age: {dog1.age}")
print(f"Dog 2: {dog2.name}, Age: {dog2.age}")
print(f"Species: {dog1.species}")
print(f"{dog1.bark()}")
print(f"{dog2.description()}")

# Output:
# Dog 1: Rex, Age: 5
# Dog 2: Buddy, Age: 3
# Species: Canis familiaris
# Rex says Woof!
# Buddy is 3 years old

# ============================================================
# The __init__ Method
# ============================================================
# Example 2: Customizing initialization
print("\n--- __init__ Method ---")

class Person:
    def __init__(self, name, age, email=None):
        """Initialize person with name, age, and optional email."""
        self.name = name
        self.age = age
        self.email = email
        self.is_adult = age >= 18
    
    def introduce(self):
        """Return introduction string."""
        intro = f"I'm {self.name}, {self.age} years old."
        if self.email:
            intro += f" Email: {self.email}"
        return intro

person1 = Person("Alice", 30, "alice@example.com")
person2 = Person("Bob", 25)

print(person1.introduce())
print(person2.introduce())

# Output:
# I'm Alice, 30 years old. Email: alice@example.com
# I'm Bob, 25 years old.

# ============================================================
# The self Parameter
# ============================================================
# Example 3: Understanding self
print("\n--- self Parameter ---")

class Calculator:
    def __init__(self, value=0):
        """Initialize calculator with starting value."""
        self.value = value  # self refers to the instance
        print(f"Created calculator with value: {self.value}")
    
    def add(self, amount):
        """Add amount to value."""
        self.value += amount  # Modify the instance's value
        return self  # Return self for method chaining
    
    def subtract(self, amount):
        """Subtract amount from value."""
        self.value -= amount
        return self
    
    def result(self):
        """Return current value."""
        return self.value

# Method chaining
calc = Calculator(10)
calc.add(5).subtract(3).add(7)
print(f"Final result: {calc.result()}")

# Output:
# Created calculator with value: 10
# Final result: 19

# ============================================================
# Class Attributes vs Instance Attributes
# ============================================================
# Example 4: Different types of attributes
print("\n--- Attribute Types ---")

class Employee:
    # Class attribute (shared by all employees)
    company = "Tech Corp"
    employee_count = 0
    
    def __init__(self, name, position, salary):
        # Instance attributes (unique to each employee)
        self.name = name
        self.position = position
        self.salary = salary
        Employee.employee_count += 1  # Update class attribute
    
    def describe(self):
        return f"{self.name} - {self.position} at {self.company}"

emp1 = Employee("Alice", "Engineer", 95000)
emp2 = Employee("Bob", "Designer", 85000)

print(f"Employee 1: {emp1.describe()}")
print(f"Employee 2: {emp2.describe()}")
print(f"Total employees: {Employee.employee_count}")

# Modify class attribute
Employee.company = "New Tech Corp"
print(f"\nAfter company change:")
print(f"Employee 1 company: {emp1.company}")
print(f"Employee 2 company: {emp2.company}")

# Output:
# Employee 1: Alice - Engineer at Tech Corp
# Employee 2: Bob - Designer at Tech Corp
# Total employees: 2
# 
# After company change:
# Employee 1 company: New Tech Corp
# Employee 2 company: New Tech Corp

# ============================================================
# Properties (Getters and Setters)
# ============================================================
# Example 5: Using @property decorator
print("\n--- Properties ---")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # Private attribute (convention)
    
    @property
    def balance(self):
        """Getter for balance."""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """Setter for balance with validation."""
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value
    
    def deposit(self, amount):
        """Deposit money."""
        if amount <= 0:
            raise ValueError("Deposit must be positive!")
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        """Withdraw money."""
        if amount > self._balance:
            raise ValueError("Insufficient funds!")
        self._balance -= amount
        return self._balance

account = BankAccount("Alice", 1000)
print(f"Initial balance: ${account.balance}")

account.deposit(500)
print(f"After deposit: ${account.balance}")

account.withdraw(200)
print(f"After withdrawal: ${account.balance}")

# account.balance = -100  # ValueError: Balance cannot be negative!

# ============================================================
# Special Methods (Magic Methods)
# ============================================================
# Example 6: Dunder methods
print("\n--- Special Methods ---")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """String representation for print()."""
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        """Developer representation."""
        return f"Vector(x={self.x}, y={self.y})"
    
    def __add__(self, other):
        """Add two vectors."""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        """Check equality."""
        return self.x == other.x and self.y == other.y
    
    def __len__(self):
        """Return length (magnitude)."""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1: {v1}")
print(f"v2: {v2}")
print(f"v1 + v2: {v1 + v2}")
print(f"v1 == v2: {v1 == v2}")
print(f"|v1|: {len(v1)}")

# ============================================================
# Practical Example
# ============================================================
# Example 7: Real-world class
print("\n--- Practical Example: Todo List ---")

class TodoList:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task, priority="medium"):
        """Add a task to the list."""
        self.tasks.append({"task": task, "priority": priority, "done": False})
    
    def complete_task(self, index):
        """Mark a task as done."""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = True
    
    def remove_task(self, index):
        """Remove a task."""
        if 0 <= index < len(self.tasks):
            return self.tasks.pop(index)
    
    def show_tasks(self):
        """Display all tasks."""
        print(f"\n{self.name}:")
        for i, task in enumerate(self.tasks):
            status = "X" if task["done"] else " "
            print(f"  {i + 1}. [{status}] {task['task']} ({task['priority']})")
    
    def summary(self):
        """Return task summary."""
        done = sum(1 for t in self.tasks if t["done"])
        return f"{done}/{len(self.tasks)} tasks completed"

# Usage
todo = TodoList("My Project")
todo.add_task("Design database", "high")
todo.add_task("Write API code", "high")
todo.add_task("Create tests", "medium")
todo.add_task("Write documentation", "low")

todo.show_tasks()
todo.complete_task(0)
todo.complete_task(1)
print(f"\n{todo.summary()}")
todo.show_tasks()

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. class ClassName: defines a new class")
print("2. __init__(self): constructor method")
print("3. self refers to the current instance")
print("4. Instance attributes: self.name = name")
print("5. Class attributes: shared by all instances")
print("6. @property: getter/setter for controlled access")
print("7. Special methods: __str__, __add__, __eq__, etc.")
print("8. Methods define object behavior")
