# Python OOP Quiz

## Topic Overview
This quiz covers Object-Oriented Programming (OOP) concepts in Python including classes and objects, inheritance, polymorphism, encapsulation, and magic methods. Test your understanding of OOP principles and their implementation in Python.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the correct way to define a class in Python?**

A) `class MyClass {}`  
B) `class MyClass:`  
C) `def class MyClass`  
D) `new class MyClass`  

**Difficulty:** Easy  

---

### Question 2
**What does the `__init__` method do?**

A) Initializes the class variables  
B) Creates a new object instance  
C) Destroys the object  
D) Returns the class name  

**Difficulty:** Easy  

---

### Question 3
**What is the output of this code?**
```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says Woof!"

my_dog = Dog("Buddy")
print(my_dog.bark())
```

A) Buddy says Woof!  
B) Dog says Woof!  
C) Error  
D) my_dog says Woof!  

**Difficulty:** Easy  

---

### Question 4
**What is inheritance in Python?**

A) Creating objects from classes  
B) A class acquiring properties and methods from another class  
C) Defining multiple classes  
D) Destroying objects  

**Difficulty:** Easy  

---

### Question 5
**What is the output of this code?**
```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

dog = Dog()
print(dog.speak())
```

A) Some sound  
B) Woof!  
C) Error  
D) None  

**Difficulty:** Medium  

---

### Question 6
**What is polymorphism in Python?**

A) Having multiple constructors  
B) The ability of different classes to be treated as instances of the same class through inheritance  
C) Creating objects of different types  
D) Multiple inheritance  

**Difficulty:** Medium  

---

### Question 7
**What is encapsulation?**

A) Hiding internal implementation details and providing a public interface  
B) Creating multiple objects  
C) Inheriting from multiple classes  
D) Defining magic methods  

**Difficulty:** Medium  

---

### Question 8
**What is the output of this code?**
```python
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    
    def get_name(self):
        return self.__name

p = Person("Alice", 25)
print(p.__name)
```

A) Alice  
B) Error  
C) None  
D) person__name  

**Difficulty:** Hard  

---

### Question 9
**What is the correct way to call a parent class method in Python?**

A) `super().method()`  
B) `parent.method()`  
C) `self.parent.method()`  
D) `base.method()`  

**Difficulty:** Medium  

---

### Question 10
**What is the output of this code?**
```python
class Base:
    def __init__(self):
        print("Base init")

class Child(Base):
    def __init__(self):
        super().__init__()
        print("Child init")

c = Child()
```

A) Child init  
B) Base init  
C) Base init Child init  
D) Child init Base init  

**Difficulty:** Medium  

---

### Question 11
**What is the purpose of the `self` parameter?**

A) It's a keyword for creating instances  
B) It refers to the current instance of the class  
C) It's used for inheritance  
D) It's optional in all methods  

**Difficulty:** Easy  

---

### Question 12
**What is the output of this code?**
```python
class Counter:
    count = 0
    
    def __init__(self):
        Counter.count += 1

c1 = Counter()
c2 = Counter()
c3 = Counter()
print(Counter.count)
```

A) 1  
B) 3  
C) Error  
D) 0  

**Difficulty:** Medium  

---

### Question 13
**What is the purpose of the `__str__` method?**

A) To convert an object to a string for printing  
B) To initialize the object  
C) To compare two objects  
D) To create a copy of the object  

**Difficulty:** Easy  

---

### Question 14
**What is the output of this code?**
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print(v3)
```

A) (4, 6)  
B) (1, 2, 3, 4)  
C) Error  
D) (3, 4)  

**Difficulty:** Hard  

---

### Question 15
**What is the difference between a class variable and an instance variable?**

A) Class variables are shared across all instances, instance variables are unique to each instance  
B) Class variables are faster than instance variables  
C) Instance variables are shared, class variables are unique  
D) There is no difference  

**Difficulty:** Medium  

---

### Question 16
**What is the output of this code?**
```python
class MathOperations:
    @staticmethod
    def add(a, b):
        return a + b

print(MathOperations.add(5, 3))
```

A) 8  
B) Error  
C) None  
D) (5, 3)  

**Difficulty:** Medium  

---

### Question 17
**What is the purpose of the `__repr__` method?**

A) To return a string representation for debugging  
B) To initialize the object  
C) To compare objects  
D) To destroy the object  

**Difficulty:** Easy  

---

### Question 18
**What is the output of this code?**
```python
class A:
    def show(self):
        return "A"

class B(A):
    def show(self):
        return "B"

class C(B):
    pass

c = C()
print(c.show())
```

A) A  
B) B  
C) C  
D) Error  

**Difficulty:** Medium  

---

### Question 19
**What is the difference between `__str__` and `__repr__`?**

A) They are identical  
B) `__str__` is for end users, `__repr__` is for developers/debugging  
C) `__repr__` is for end users, `__str__` is for debugging  
D) `__str__` is required, `__repr__` is optional  

**Difficulty:** Medium  

---

### Question 20
**What is the output of this code?**
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)
```

A) True  
B) False  
C) Error  
D) None  

**Difficulty:** Hard  

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You have a strong grasp of OOP concepts.
- 14-17: Good job! Review the concepts you missed.
- 10-13: Fair. Consider revisiting OOP fundamentals.
- Below 10: Keep practicing! Review the OOP material.

---

## Answer Key

1. **B) `class MyClass:`** - Python class definitions end with a colon, not curly braces.

2. **B) Creates a new object instance** - `__init__` is the constructor method that initializes a newly created object.

3. **A) Buddy says Woof!** - The `bark` method uses the instance's `name` attribute, which is "Buddy".

4. **B) A class acquiring properties and methods from another class** - Inheritance allows a child class to reuse code from a parent class.

5. **B) Woof!** - The `speak` method is overridden in the `Dog` class, demonstrating polymorphism.

6. **B) The ability of different classes to be treated as instances of the same class through inheritance** - Polymorphism allows objects of different classes to be used interchangeably.

7. **A) Hiding internal implementation details and providing a public interface** - Encapsulation restricts direct access to some components and provides public methods.

8. **B) Error** - `__name` is a private attribute (name mangling), so it can't be accessed directly from outside the class.

9. **A) `super().method()`** - `super()` returns a proxy object that delegates method calls to the parent class.

10. **C) Base init Child init** - `super().__init__()` calls the parent's `__init__` first, then the child's code runs.

11. **B) It refers to the current instance of the class** - `self` is a reference to the current object instance.

12. **B) 3** - `Counter.count` is a class variable that increments each time an instance is created.

13. **A) To convert an object to a string for printing** - `__str__` is called by `print()` and `str()` to get a human-readable string.

14. **A) (4, 6)** - The `__add__` method allows adding two Vector objects, resulting in element-wise addition.

15. **A) Class variables are shared across all instances, instance variables are unique to each instance** - Class variables belong to the class, instance variables belong to each object.

16. **A) 8** - `@staticmethod` defines a method that doesn't need access to the class or instance.

17. **A) To return a string representation for debugging** - `__repr__` is meant to be unambiguous and useful for debugging.

18. **B) B** - Method resolution order (MRO) follows: C → B → A. Since `B` defines `show`, that's what gets called.

19. **B) `__str__` is for end users, `__repr__` is for developers/debugging** - `__str__` should return a readable description, `__repr__` should return an unambiguous representation.

20. **A) True** - The Singleton pattern ensures only one instance exists. Both `s1` and `s2` point to the same object.

---

*Quiz completed! How did you score?* 🎯