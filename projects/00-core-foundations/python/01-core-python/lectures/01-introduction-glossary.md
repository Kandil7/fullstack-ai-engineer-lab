# Python Introduction - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Python | Language | High-level, interpreted programming language |
| Interpreter | Tool | Executes Python code line by line |
| Compiler | Tool | Translates entire code to machine code before execution |
| PEP | Standard | Python Enhancement Proposal for language improvements |
| PEP 8 | Standard | Style guide for Python code |
| PyPI | Repository | Python Package Index with 400K+ packages |
| IDE | Tool | Integrated Development Environment for coding |
| REPL | Tool | Read-Eval-Print Loop for interactive coding |
| Virtual Environment | Tool | Isolated Python environment for projects |
| pip | Tool | Package installer for Python |

## Detailed Definitions

### B

**Bytecode**
- **Definition**: Intermediate code that Python compiles to before interpretation
- **Example**: Python compiles `.py` files to `.pyc` bytecode files
- **Related terms**: Interpreter, Compilation, Module
```python
# Python automatically compiles to bytecode
import py_compile
py_compile.compile('my_script.py')  # Creates my_script.pyc
```

### C

**Compiled Language**
- **Definition**: Language that translates entire code to machine code before execution
- **Example**: C, C++, Rust, Go
- **Related terms**: Interpreter, High-level Language, Bytecode
```c
// Compiled language example (C)
#include <stdio.h>
int main() {
    printf("Hello, World!");
    return 0;
}
// Must compile: gcc hello.c -o hello
// Then run: ./hello
```

**CPython**
- **Definition**: Reference implementation of Python in C
- **Example**: The standard Python you download from python.org
- **Related terms**: Python Implementation, Jython, PyPy, Cython
```python
# Check your Python implementation
import sys
print(sys.implementation.name)  # Output: cpython
```

### D

**Dynamic Typing**
- **Definition**: Variable types determined at runtime, not compile time
- **Example**: `x = 5` (int) then `x = "hello"` (str) - same variable
- **Related terms**: Static Typing, Type Inference, Duck Typing
```python
# Dynamic typing in action
x = 10          # x is an integer
print(type(x))  # <class 'int'>

x = "hello"     # Now x is a string
print(type(x))  # <class 'str'>
```

### H

**High-level Language**
- **Definition**: Language abstracting hardware details, closer to human language
- **Example**: Python, JavaScript, Ruby
- **Related terms**: Low-level Language, Assembly, Machine Code
- **Why important**: Easier to read, write, and maintain

### I

**IDE (Integrated Development Environment)**
- **Definition**: Software application for comprehensive coding facilities
- **Example**: VS Code, PyCharm, IntelliJ IDEA
- **Related terms**: Text Editor, Debugger, Terminal
- **Features**: Code editing, debugging, version control, package management

**Interpreter**
- **Definition**: Program that executes code line by line
- **Example**: Python interpreter, Node.js
- **Related terms**: Compiler, Bytecode, REPL
```python
# Python interpreter executes line by line
print("Line 1")  # Executes immediately
print("Line 2")  # Then this executes
```

**Interactive Mode**
- **Definition**: Python mode where code executes immediately after typing
- **Example**: Python REPL (Read-Eval-Print Loop)
- **Related terms**: Script Mode, REPL
```python
>>> # Interactive mode starts with >>>
>>> 2 + 2
4
>>> print("Hello")
Hello
>>> exit()  # Exit interactive mode
```

### L

**Library**
- **Definition**: Collection of pre-written code for specific tasks
- **Example**: `math`, `os`, `datetime` are Python standard libraries
- **Related terms**: Module, Package, Framework
```python
# Using standard library modules
import math
print(math.sqrt(16))  # 4.0

import datetime
print(datetime.date.today())
```

**Low-level Language**
- **Definition**: Language close to machine code, less abstracted
- **Example**: Assembly, Machine Code
- **Related terms**: High-level Language, C, Hardware
- **Use cases**: System programming, embedded systems

### M

**Module**
- **Definition**: Single Python file containing code (functions, classes, variables)
- **Example**: `math.py`, `random.py`
- **Related terms**: Package, Library, Import
```python
# Importing a module
import math
from random import randint

print(math.pi)
print(randint(1, 10))
```

### P

**Package**
- **Definition**: Collection of related modules in a directory
- **Example**: `numpy`, `pandas`, `flask`
- **Related terms**: Module, Library, PyPI
```
my_package/
    __init__.py
    module1.py
    module2.py
```

**PEP (Python Enhancement Proposal)**
- **Definition**: Design documents for Python improvements
- **Example**: PEP 8 (Style Guide), PEP 20 (Zen of Python)
- **Related terms**: Python Enhancement, RFC, Standard
- **Website**: https://peps.python.org

**pip**
- **Definition**: Package installer for Python
- **Example**: `pip install requests`
- **Related terms**: PyPI, Virtual Environment, Package
```bash
# Common pip commands
pip install package_name
pip uninstall package_name
pip list  # Show installed packages
```

**PyPI (Python Package Index)**
- **Definition**: Official repository for Python packages
- **Example**: https://pypi.org
- **Related terms**: pip, Package, Repository
- **Stats**: 400,000+ packages available

**Python Implementation**
- **Definition**: Specific version/variant of Python
- **Example**: CPython, PyPy, Jython, IronPython
- **Related terms**: CPython, PyPy, Jython
```python
# Different Python implementations
import platform
print(platform.python_implementation())  # CPython
```

### R

**REPL (Read-Eval-Print Loop)**
- **Definition**: Interactive programming environment
- **Example**: Python's interactive shell
- **Related terms**: Interactive Mode, Interpreter
```python
# REPL is the interactive mode
>>> 2 + 2
4
>>> "hello".upper()
'HELLO'
```

### S

**Script Mode**
- **Definition**: Writing Python code in a file (.py) and executing it
- **Example**: `python my_script.py`
- **Related terms**: Interactive Mode, File Execution
```python
# script.py
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
```

**Standard Library**
- **Definition**: Python's built-in collection of modules
- **Example**: `os`, `sys`, `math`, `datetime`
- **Related terms**: Module, Package, Third-party Library
```python
# Using standard library
import os
import sys
import math

# os for file operations
print(os.getcwd())

# sys for system-specific parameters
print(sys.version)

# math for mathematical functions
print(math.pi)
```

**Static Typing**
- **Definition**: Variable types must be declared and checked at compile time
- **Example**: Java, C++, TypeScript
- **Related terms**: Dynamic Typing, Type System, Type Safety
```java
// Static typing example (Java)
int x = 5;      // Must declare type
String s = "hi"; // Must declare type
// x = "hello"; // Compile error!
```

### T

**Third-party Library**
- **Definition**: Libraries developed outside Python's standard library
- **Example**: `requests`, `flask`, `pandas`
- **Related terms**: PyPI, pip, Package
```bash
# Installing third-party libraries
pip install requests
pip install flask
pip install pandas
```

**Type Inference**
- **Definition**: Python automatically determining variable type
- **Example**: `x = 10` → Python knows x is int
- **Related terms**: Dynamic Typing, Type System
```python
# Python infers types automatically
x = 10          # int
y = 3.14        # float
z = "hello"     # str
print(type(x))  # <class 'int'>
```

### V

**Virtual Environment**
- **Definition**: Isolated Python environment for specific projects
- **Example**: `venv`, `virtualenv`, `conda`
- **Related terms**: Dependency Management, Package Isolation
```bash
# Creating a virtual environment
python -m venv myenv

# Activating (Windows)
myenv\Scripts\activate

# Activating (macOS/Linux)
source myenv/bin/activate
```

### Z

**Zen of Python**
- **Definition**: Collection of 19 guiding principles for Python
- **Example**: "Beautiful is better than ugly"
- **Related terms**: PEP 20, Python Philosophy
```python
# See the Zen of Python
import this
```

## Key Concepts Summary

### Python Development Tools
1. **Interpreter**: Executes Python code
2. **pip**: Installs packages
3. **PyPI**: Repository of packages
4. **IDE**: Development environment
5. **Virtual Environment**: Project isolation

### Python Philosophy
1. **Readability**: Code is read more than written
2. **Simplicity**: Simple is better than complex
3. **Explicit**: Explicit is better than implicit
4. **Community**: Strong ecosystem and support

### Installation Checklist
- [ ] Python 3.8+ installed
- [ ] pip installed (usually with Python)
- [ ] IDE configured (VS Code, PyCharm)
- [ ] Virtual environment tool ready
- [ ] Terminal/command line accessible

## Practice Terms

Match these terms to their definitions:
1. PEP - ?
2. PyPI - ?
3. pip - ?
4. REPL - ?
5. Virtual Environment - ?

**Answers:**
1. Python Enhancement Proposal
2. Python Package Index
3. Package installer
4. Read-Eval-Print Loop
5. Isolated Python environment