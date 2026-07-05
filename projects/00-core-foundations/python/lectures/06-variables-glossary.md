# Python Variables - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Variable | Concept | Named container for storing data |
| Assignment | Operation | Storing a value in a variable |
| Dynamic Typing | Feature | Variables can change type at runtime |
| Scope | Concept | Where a variable is accessible |
| Local Variable | Scope | Variable inside a function |
| Global Variable | Scope | Variable accessible throughout program |
| Constant | Convention | Variable that shouldn't change |
| Identifier | Syntax | Name given to variables, functions, classes |
| Keyword | Syntax | Reserved word with special meaning |
| snake_case | Convention | Naming style with underscores |

## Detailed Definitions

### A

**Assignment**
- **Definition**: Storing a value in a variable using = operator
- **Example**: `x = 10`, `name = "Alice"`
- **Related terms**: Variable, Value, Operator
```python
# Basic assignment
x = 10
name = "Alice"
is_active = True

# Multiple assignment
a, b, c = 1, 2, 3
```

### C

**Constant**
- **Definition**: Variable that shouldn't change during execution
- **Example**: `MAX_SIZE = 100`, `PI = 3.14159`
- **Related terms**: Variable, Convention, UPPER_SNAKE_CASE
```python
# Constants (convention - not enforced by Python)
MAX_RETRY = 3
PI = 3.14159
API_URL = "https://api.example.com"
```

### D

**Declaration**
- **Definition**: Creating a variable (implicit in Python)
- **Example**: First assignment creates the variable
- **Related terms**: Assignment, Dynamic Typing
```python
# Python doesn't require explicit declaration
x = 10  # Creates and assigns in one step
# No need for: int x = 10; (like in C/Java)
```

**Dynamic Typing**
- **Definition**: Variables can change type during execution
- **Example**: `x = 10` then `x = "hello"`
- **Related terms**: Static Typing, Type Inference, Duck Typing
```python
# Dynamic typing example
x = 10          # int
print(type(x))  # <class 'int'>

x = "hello"     # str
print(type(x))  # <class 'str'>
```

### G

**Global Variable**
- **Definition**: Variable accessible throughout entire program
- **Example**: Variable defined outside all functions
- **Related terms**: Local Variable, Scope, Global Keyword
```python
# Global variable
global_var = "I'm global"

def my_function():
    print(global_var)  # Can access global

my_function()
print(global_var)  # Can access global
```

### I

**Identifier**
- **Definition**: Name given to variables, functions, classes
- **Example**: `user_name`, `calculate_total`, `MyClass`
- **Related terms**: Variable, Function, Class Name
```python
# Valid identifiers
user_name = "Alice"
def calculate_total():
    pass
class UserAccount:
    pass
```

**Initialization**
- **Definition**: Giving a variable its first value
- **Example**: `x = 10` (initializes x to 10)
- **Related terms**: Assignment, Default Value
```python
# Initialization
x = 10          # Initialize with value
name = "Alice"  # Initialize with string
is_active = True  # Initialize with boolean
```

### K

**Keyword**
- **Definition**: Reserved word with special meaning in Python
- **Example**: `if`, `else`, `for`, `while`, `def`, `class`
- **Related terms**: Reserved Word, Identifier, Syntax Error
```python
# List of Python keywords
import keyword
print(keyword.kwlist)
# ['False', 'None', 'True', 'and', 'as', ...]

# Cannot use as variable names
class = "Math"  # SyntaxError!
```

### L

**Local Variable**
- **Definition**: Variable defined inside a function
- **Example**: Variable created within function scope
- **Related terms**: Global Variable, Scope, Function
```python
def my_function():
    local_var = "I'm local"  # Local variable
    print(local_var)  # Accessible here

my_function()
# print(local_var)  # Error! Not accessible here
```

### N

**Naming Convention**
- **Definition**: Standardized rules for naming identifiers
- **Example**: snake_case, PascalCase, UPPER_SNAKE_CASE
- **Related terms**: PEP 8, Identifier, Convention
```python
# Variable naming conventions
user_name = "Alice"      # snake_case for variables
def calculate_total():   # snake_case for functions
    pass
class UserAccount:       # PascalCase for classes
    pass
MAX_SIZE = 100           # UPPER_SNAKE_CASE for constants
```

### O

**Object**
- **Definition**: Everything in Python is an object
- **Example**: Numbers, strings, lists, functions
- **Related terms**: Variable, Reference, Instance
```python
# Everything is an object
x = 10
print(type(x))  # <class 'int'>
print(id(x))    # Memory address

name = "Hello"
print(type(name))  # <class 'str'>
print(id(name))    # Memory address
```

### P

**PEP 8**
- **Definition**: Official Python style guide
- **Example**: Naming conventions, indentation rules
- **Related terms**: Style Guide, Convention, Readability
```python
# PEP 8 variable naming rules
# - snake_case for variables and functions
# - PascalCase for classes
# - UPPER_SNAKE_CASE for constants
# - Avoid single letters except loop counters
# - Use descriptive names
```

### R

**Reference**
- **Definition**: How variables point to objects in memory
- **Example**: `x = 10` (x references the integer object)
- **Related terms**: Object, Memory, Assignment
```python
# Variables reference objects
x = 10
y = x  # Both reference same object

x = 20  # x now references new object
print(y)  # 10 (still references old object)
```

**Reassignment**
- **Definition**: Changing the value of an existing variable
- **Example**: `x = 10` then `x = 20`
- **Related terms**: Assignment, Dynamic Typing
```python
# Reassignment
x = 10
print(x)  # 10

x = 20  # Reassign
print(x)  # 20
```

### S

**Scope**
- **Definition**: Where a variable is accessible in code
- **Example**: Local (inside function), Global (outside)
- **Related terms**: Local Variable, Global Variable, LEGB Rule
```python
# Variable scope
x = "global"  # Global scope

def outer():
    y = "outer"  # Enclosing scope
    
    def inner():
        z = "local"  # Local scope
        print(x, y, z)  # Can access all
    
    inner()

outer()
```

**Static Typing**
- **Definition**: Variable type must be declared and checked at compile time
- **Example**: Java, C++, TypeScript
- **Related terms**: Dynamic Typing, Type System
```java
// Static typing example (Java)
int x = 5;      // Must declare type
String s = "hi"; // Must declare type
// x = "hello"; // Compile error!
```

**Subscript**
- **Definition**: Accessing elements in a sequence
- **Example**: `my_list[0]`, `my_dict["key"]`
- **Related terms**: Index, Sequence, Dictionary
```python
# Subscript examples
my_list = [10, 20, 30]
print(my_list[0])  # 10

my_dict = {"name": "Alice", "age": 25}
print(my_dict["name"])  # Alice
```

### T

**Type**
- **Definition**: Classification of data (int, str, float, etc.)
- **Example**: `type(x)` returns the type of x
- **Related terms**: Data Type, Dynamic Typing, Type Inference
```python
# Different types
x = 10          # int
y = 3.14        # float
z = "hello"     # str
w = True        # bool
a = [1, 2, 3]   # list

print(type(x))  # <class 'int'>
print(type(y))  # <class 'float'>
```

**Type Inference**
- **Definition**: Python automatically determining variable type
- **Example**: `x = 10` → Python knows x is int
- **Related terms**: Dynamic Typing, Type System
```python
# Type inference in action
x = 10          # int (inferred)
y = 3.14        # float (inferred)
z = "hello"     # str (inferred)
print(type(x))  # <class 'int'>
```

### U

**Unpacking**
- **Definition**: Assigning multiple variables at once
- **Example**: `x, y, z = 1, 2, 3`
- **Related terms**: Multiple Assignment, Tuple Unpacking
```python
# Unpacking examples
coordinates = (10, 20)
x, y = coordinates
print(x, y)  # 10 20

# Swap using unpacking
x, y = 5, 10
x, y = y, x  # Now x=10, y=5
```

### V

**Variable**
- **Definition**: Named container for storing data
- **Example**: `name = "Alice"`, `age = 25`
- **Related terms**: Assignment, Value, Reference
```python
# Variable examples
name = "Alice"      # String variable
age = 25            # Integer variable
height = 1.65       # Float variable
is_student = True   # Boolean variable
```

### W

**Writable**
- **Definition**: Whether a variable can be changed
- **Example**: Regular variables are writable, constants aren't (by convention)
- **Related terms**: Reassignment, Constant, Immutable
```python
# Writable variables
x = 10
x = 20  # Can reassign

# Immutable objects (content can't change)
my_tuple = (1, 2, 3)
# my_tuple[0] = 5  # Error! Tuples are immutable
```

## Key Concepts Summary

### Variable Naming Rules
| Rule | Valid | Invalid |
|------|-------|---------|
| Start with letter or _ | `name`, `_count` | `2count` |
| Can contain letters, numbers, _ | `user_name`, `count2` | `user-name` |
| Case-sensitive | `name` ≠ `Name` | - |
| Can't be keywords | `if`, `for`, `while` | - |

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_name` |
| Functions | snake_case | `calculate_total()` |
| Classes | PascalCase | `UserAccount` |
| Constants | UPPER_SNAKE_CASE | `MAX_SIZE` |
| Modules | snake_case | `my_module.py` |

### Variable Scope
| Scope | Location | Access |
|-------|----------|--------|
| Local | Inside function | Function only |
| Enclosing | Nested functions | Enclosing function |
| Global | Module level | Entire module |
| Built-in | Python built-ins | Everywhere |

### Dynamic Typing Benefits
- **Flexibility**: Variables can change type
- **Rapid prototyping**: No type declarations needed
- **Simpler code**: Less boilerplate

### Dynamic Typing Risks
- **Runtime errors**: Type errors caught at runtime
- **Less clarity**: Type not explicit
- **Performance**: Type checking at runtime

## Practice Terms

Match these terms to their definitions:
1. Variable - ?
2. Dynamic Typing - ?
3. Scope - ?
4. Global Variable - ?
5. Constant - ?

**Answers:**
1. Named container for storing data
2. Variables can change type at runtime
3. Where a variable is accessible in code
4. Variable accessible throughout entire program
5. Variable that shouldn't change (convention)