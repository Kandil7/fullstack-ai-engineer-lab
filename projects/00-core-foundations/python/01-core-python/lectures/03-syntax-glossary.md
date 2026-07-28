# Python Syntax Fundamentals - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Indentation | Syntax | Whitespace used to define code blocks |
| Statement | Syntax | Instruction that Python can execute |
| Expression | Syntax | Combination of values and operators |
| Comment | Syntax | Text ignored by Python interpreter |
| PEP 8 | Standard | Python's official style guide |
| snake_case | Convention | Naming style with underscores |
| PascalCase | Convention | Naming style with capital letters |
| Constant | Concept | Value that shouldn't change |
| Reserved Word | Syntax | Word with special meaning in Python |
| Line Continuation | Syntax | Breaking long lines across multiple lines |

## Detailed Definitions

### B

**Block**
- **Definition**: Group of statements under a control structure
- **Example**: Code under `if`, `for`, `while`, functions
- **Related terms**: Indentation, Scope, Suite
```python
# Code block under if
if True:
    # This is a block
    print("Statement 1")
    print("Statement 2")
# Block ends here
```

**Blank Line**
- **Definition**: Empty line used to separate logical sections
- **Example**: Between functions, classes, or code sections
- **Related terms**: Whitespace, Readability, PEP 8
```python
def function1():
    pass

# Blank line separates functions
def function2():
    pass


# Two blank lines between top-level definitions
class MyClass:
    pass
```

### C

**Colon (:)**
- **Definition**: Punctuation marking start of indented block
- **Example**: After `if`, `for`, `while`, `def`, `class`
- **Related terms**: Indentation, Block, Suite
```python
if condition:    # Colon required
    do_something()

def function():  # Colon required
    do_something()
```

**Comment**
- **Definition**: Text ignored by Python interpreter
- **Example**: `# This is a comment`
- **Related terms**: Docstring, Documentation, PEP 8
```python
# Single-line comment

"""
Multi-line comment
using docstrings
"""

x = 10  # Inline comment
```

**Compound Statement**
- **Definition**: Statement containing other statements
- **Example**: `if`, `for`, `while`, `def`, `class`
- **Related terms**: Simple Statement, Block, Suite
```python
# Compound statements
if condition:
    do_something()  # Contains simple statement

for item in list:
    process(item)  # Contains simple statement
```

### D

**Docstring**
- **Definition**: String literal as first statement in module/class/function
- **Example**: `"""Documentation string"""`
- **Related terms**: Comment, Documentation, Help
```python
def my_function():
    """This is a docstring."""
    pass

class MyClass:
    """Class documentation."""
    pass

module = """
Module documentation.
"""
```

### E

**Expression**
- **Definition**: Combination of values, variables, and operators
- **Example**: `2 + 3`, `x > 5`, `"hello".upper()`
- **Related terms**: Statement, Operator, Value
```python
# Expressions
2 + 3          # Arithmetic
"hello" * 3    # String repetition
x > 5          # Comparison
True and False # Boolean
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

**Indentation**
- **Definition**: Whitespace at beginning of line defining code blocks
- **Example**: 4 spaces (standard) or tabs
- **Related terms**: Block, Suite, PEP 8
```python
# Proper indentation
if True:
    print("4 spaces")  # Indented block
    print("4 spaces")  # Same level

print("No indentation")  # Outside block
```

### K

**Keyword**
- **Definition**: Reserved word with special meaning in Python
- **Example**: `if`, `else`, `for`, `while`, `def`, `class`
- **Related terms**: Reserved Word, Identifier, Syntax
```python
# Python keywords
import keyword
print(keyword.kwlist)
# ['False', 'None', 'True', 'and', 'as', 'assert', ...]
```

### L

**Line Continuation**
- **Definition**: Breaking long line across multiple lines
- **Example**: Using parentheses or backslash
- **Related terms**: Implicit Continuation, Explicit Continuation
```python
# Implicit continuation (recommended)
total = (10 +
         20 +
         30)

# Explicit continuation (backslash)
total = 10 + \
        20 + \
        30
```

### N

**Naming Convention**
- **Definition**: Rules for naming variables, functions, classes
- **Example**: snake_case, PascalCase, UPPER_SNAKE_CASE
- **Related terms**: PEP 8, Identifier, Convention
```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total():
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_SIZE = 100
```

### O

**Operator**
- **Definition**: Symbol that performs operation on values
- **Example**: `+`, `-`, `*`, `/`, `=`, `==`
- **Related terms**: Expression, Operand, Precedence
```python
# Arithmetic operators
result = 10 + 5

# Comparison operators
is_greater = 10 > 5

# Assignment operators
x = 10
```

### P

**PEP (Python Enhancement Proposal)**
- **Definition**: Design documents for Python improvements
- **Example**: PEP 8 (Style Guide), PEP 20 (Zen of Python)
- **Related terms**: Standard, Convention, RFC
- **Website**: https://peps.python.org

**PEP 8**
- **Definition**: Official Python style guide
- **Example**: Indentation, naming, line length rules
- **Related terms**: Style Guide, Convention, Readability
```python
# PEP 8 recommendations
# - 4 spaces indentation
# - 79 character line limit
# - snake_case for variables/functions
# - PascalCase for classes
# - UPPER_SNAKE_CASE for constants
```

### R

**Reserved Word**
- **Definition**: Word with special meaning that can't be used as identifier
- **Example**: `if`, `else`, `for`, `while`, `def`, `class`
- **Related terms**: Keyword, Identifier, Syntax Error
```python
# Cannot use reserved words as identifiers
class = "Math"  # SyntaxError!
for = 5         # SyntaxError!

# Use descriptive alternatives
subject = "Math"
count = 5
```

### S

**Simple Statement**
- **Definition**: Single line of code
- **Example**: Assignment, function call, return statement
- **Related terms**: Compound Statement, Expression, Statement
```python
# Simple statements
x = 10
print("Hello")
return result
```

**Suite**
- **Definition**: Block of statements under compound statement
- **Example**: Indented code after `if`, `for`, `while`
- **Related terms**: Block, Indentation, Compound Statement
```python
if condition:  # Suite starts after colon
    statement1  # Part of suite
    statement2  # Part of suite
# Suite ends when indentation returns to previous level
```

### T

**Tab**
- **Definition**: Whitespace character (avoid in Python)
- **Example**: `\t` character
- **Related terms**: Indentation, Spaces, PEP 8
```python
# WRONG - mixing tabs and spaces
if True:
	print("Tab")      # Tab character
    print("Space")  # 4 spaces - IndentationError!

# CORRECT - use only spaces
if True:
    print("4 spaces")
    print("4 spaces")
```

### V

**Variable**
- **Definition**: Named storage for data
- **Example**: `x = 10`, `name = "Alice"`
- **Related terms**: Identifier, Assignment, Value
```python
# Variable assignment
x = 10
name = "Alice"
is_active = True
```

### W

**Whitespace**
- **Definition**: Spaces, tabs, newlines in code
- **Example**: Indentation, line breaks, spaces around operators
- **Related terms**: Indentation, Readability, PEP 8
```python
# Whitespace for readability
x = 10 + 5      # Spaces around operators
y = x * 2       # Consistent indentation

# Function with proper whitespace
def calculate(a, b):
    """Calculate sum."""
    return a + b
```

## Key Concepts Summary

### Indentation Rules
- **4 spaces** = standard indentation (PEP 8)
- **Never mix** tabs and spaces
- **Consistent** indentation throughout code block
- **Nested blocks** add another level of indentation

### Statement vs Expression
| Aspect | Statement | Expression |
|--------|-----------|------------|
| Purpose | Performs action | Produces value |
| Example | `x = 10` | `10 + 5` |
| Returns | None | Result value |
| Used in | Top level | Inside statements |

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_name` |
| Functions | snake_case | `calculate_total()` |
| Classes | PascalCase | `UserAccount` |
| Constants | UPPER_SNAKE_CASE | `MAX_SIZE` |
| Modules | snake_case | `my_module.py` |

### Line Structure Rules
1. **One statement per line** (recommended)
2. **Semicolons** separate multiple statements (allowed)
3. **Parentheses** for implicit line continuation
4. **Backslash** for explicit line continuation (avoid)

## Practice Terms

Match these terms to their definitions:
1. Indentation - ?
2. Statement - ?
3. Expression - ?
4. PEP 8 - ?
5. Keyword - ?

**Answers:**
1. Whitespace defining code blocks
2. Instruction Python can execute
3. Combination of values and operators
4. Python's official style guide
5. Reserved word with special meaning