"""
W3Schools Python Tutorial - 41: Inner/Nested Classes
=====================================================
Topics: Defining inner classes, accessing outer/inner, use cases, encapsulation, best practices

Run: python 41-inner-classes.py
Reference: https://www.w3schools.com/python/python_classes.asp
"""

# ============================================================
# What are Inner/Nested Classes?
# ============================================================
# Inner classes are classes defined inside another class.
# They help organize code logically and improve encapsulation.
# The inner class is part of the outer class's namespace.

# ============================================================
# Defining Inner Classes
# ============================================================
# Example 1: Basic inner class
class Outer:
    """Outer class with an inner class."""

    def __init__(self, name):
        self.name = name
        self.inner = self.Inner()

    class Inner:
        """Inner class definition."""

        def __init__(self):
            self.value = 42

        def show(self):
            print(f"Inner class value: {self.value}")

# Example 2: Create instances
outer = Outer("OuterObject")
outer.inner.show()

# ============================================================
# Accessing Outer Class from Inner Class
# ============================================================
# Example 3: Inner class accessing outer class attributes
class School:
    """School class with nested Student class."""

    def __init__(self, name):
        self.name = name
        self.students = []

    class Student:
        """Student is a nested class of School."""

        def __init__(self, school, student_name):
            self.school = school
            self.student_name = student_name

        def display(self):
            print(f"Student {self.student_name} attends {self.school.name}")

    def add_student(self, student_name):
        student = self.Student(self, student_name)
        self.students.append(student)
        return student

# Example 4: Use the nested class
my_school = School("Python Academy")
student1 = my_school.add_student("Alice")
student2 = my_school.add_student("Bob")
student1.display()
student2.display()

# ============================================================
# Accessing Inner Class from Outer Class
# ============================================================
# Example 5: Outer class using inner class
class Computer:
    """Computer class with nested CPU class."""

    def __init__(self, brand):
        self.brand = brand
        self.cpu = self.CPU()

    class CPU:
        """CPU is a component of Computer."""

        def __init__(self):
            self.cores = 8
            self.speed = "3.5 GHz"

        def info(self):
            return f"CPU: {self.cores} cores @ {self.speed}"

    def specs(self):
        print(f"Computer: {self.brand}")
        print(f"  {self.cpu.info()}")

# Example 6: Access inner class from outer
my_computer = Computer("Dell")
my_computer.specs()

# ============================================================
# Inner Class Use Cases: Iterators
# ============================================================
# Example 7: Iterator pattern with inner class
class NumberRange:
    """Iterable number range with inner iterator class."""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    class Iterator:
        """Inner iterator class."""

        def __init__(self, start, end):
            self.current = start
            self.end = end

        def __iter__(self):
            return self

        def __next__(self):
            if self.current >= self.end:
                raise StopIteration
            value = self.current
            self.current += 1
            return value

    def __iter__(self):
        return self.Iterator(self.start, self.end)

# Example 8: Use the iterator
print("\nNumber range iterator:")
for num in NumberRange(1, 6):
    print(num, end=" ")
print()

# ============================================================
# Inner Class Use Cases: Builders
# ============================================================
# Example 9: Builder pattern with inner class
class QueryBuilder:
    """SQL query builder with inner builder class."""

    def __init__(self, table):
        self.table = table
        self.builder = self.Builder(table)

    class Builder:
        """Inner builder class for constructing queries."""

        def __init__(self, table):
            self.table = table
            self.conditions = []
            self.fields = ["*"]

        def select(self, *fields):
            self.fields = fields
            return self

        def where(self, condition):
            self.conditions.append(condition)
            return self

        def build(self):
            query = f"SELECT {', '.join(self.fields)} FROM {self.table}"
            if self.conditions:
                query += " WHERE " + " AND ".join(self.conditions)
            return query

# Example 10: Use the builder
query = QueryBuilder("users")
sql = query.builder.select("name", "email").where("age > 18").where("active = 1").build()
print(f"\nBuilt query: {sql}")

# ============================================================
# Best Practices
# ============================================================
# 1. Use inner classes for tightly coupled components
# 2. Keep inner classes small and focused
# 3. Provide clear access methods from outer class
# 4. Use inner classes for implementation details
# 5. Document the relationship between outer and inner classes
# 6. Consider if a module-level class would be simpler
# 7. Inner classes can access outer class attributes via instance

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("Inner/nested classes are powerful for:")
print("  - Organizing related code")
print("  - Implementing design patterns (Iterator, Builder)")
print("  - Encapsulating implementation details")
print("  - Creating tightly coupled components")
print("Key takeaways:")
print("  - Inner classes are defined inside other classes")
print("  - They can access outer class attributes via instance reference")
print("  - Use inner classes when coupling is tight; modules when independent")
print("=" * 60)
