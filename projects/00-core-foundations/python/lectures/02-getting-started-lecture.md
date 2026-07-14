# Python Getting Started - Lecture Notes

## 1. Topic Overview
This lecture covers Python installation, environment setup, and running your first programs. We'll walk through installing Python on different operating systems, setting up an IDE, and understanding how Python executes code.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Install Python on Windows, macOS, and Linux
- Verify Python installation using command line
- Set up a code editor or IDE (VS Code recommended)
- Create and run Python scripts
- Use Python's interactive mode (REPL)
- Understand Python's execution flow

## 3. Key Concepts

### 3.1 Installing Python

**Windows Installation:**
1. Visit https://python.org/downloads
2. Download the latest Python 3.x installer
3. Run the installer
4. **Important**: Check "Add Python to PATH"
5. Click "Install Now"

**macOS Installation:**
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python 3
sudo apt install python3 python3-pip

# Verify installation
python3 --version
```

### 3.2 Verifying Installation

**Command Line Check:**
```bash
# Check Python version
python --version
# or
python3 --version

# Check pip version
pip --version
# or
pip3 --version
```

**Expected Output:**
```
Python 3.12.x
pip 24.x.x
```

### 3.3 IDE Setup (VS Code)

**Recommended Extensions:**
1. Python (Microsoft)
2. Pylance
3. Python Indent
4. Code Runner

**Configuration:**
1. Open VS Code
2. Install Python extension
3. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
4. Choose your Python installation

### 3.4 Running Python Programs

**Interactive Mode (REPL):**
```bash
# Start interactive mode
python

# Or for Python 3 specifically
python3
```

**Script Mode:**
```python
# Save as hello.py
print("Hello, World!")
```

```bash
# Run from command line
python hello.py
```

### 3.5 Python Execution Flow

```
Source Code (.py)
    ↓
Interpreter reads code
    ↓
Compiles to bytecode (.pyc)
    ↓
Python Virtual Machine executes
    ↓
Output/Result
```

## 4. Code Examples

### Example 1: Hello World Program
```python
# hello.py - Your first Python program
print("Hello, World!")
print("Welcome to Python programming!")
```

**Run it:**
```bash
python hello.py
```

**Output:**
```
Hello, World!
Welcome to Python programming!
```

### Example 2: Simple Calculator
```python
# calculator.py
print("Simple Calculator")
print("------------------")

# Get user input
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

# Perform calculations
sum_result = num1 + num2
difference = num1 - num2
product = num1 * num2
quotient = num1 / num2

# Display results
print(f"Sum: {sum_result}")
print(f"Difference: {difference}")
print(f"Product: {product}")
print(f"Quotient: {quotient}")
```

### Example 3: Interactive Mode Examples
```python
# In Python REPL (type these line by line)
>>> print("Hello from REPL")
Hello from REPL

>>> 2 + 2
4

>>> "Hello".upper()
'HELLO'

>>> import math
>>> math.sqrt(16)
4.0
```

### Example 4: Using Variables
```python
# variables.py
name = "Alice"
age = 25
height = 1.65

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height} meters")
```

## 5. Common Mistakes to Avoid

### Mistake 1: Not Adding Python to PATH (Windows)
```bash
# This will fail if Python isn't in PATH
python --version
# 'python' is not recognized as an internal or external command

# Solution: Reinstall Python with "Add to PATH" checked
# Or manually add Python to PATH environment variable
```

### Mistake 2: Using Wrong Python Version
```bash
# Using Python 2 command
python hello.py  # Might use Python 2

# Always use Python 3 explicitly
python3 hello.py
```

### Mistake 3: Indentation in Scripts
```python
# Wrong - mixing tabs and spaces
if True:
	print("Hello")  # Tab
    print("World")  # 4 spaces - IndentationError

# Correct - use consistent 4 spaces
if True:
    print("Hello")
    print("World")
```

### Mistake 4: File Extensions
```python
# Wrong - saving as hello.txt
# Python won't execute .txt files

# Correct - save as hello.py
print("Hello!")
```

## 6. Best Practices

1. **Use Python 3**: Always install the latest Python 3.x
2. **Use Virtual Environments**: Isolate project dependencies
3. **Learn IDE Shortcuts**: Boost productivity
4. **Practice Both Modes**: REPL for testing, scripts for projects
5. **Version Control**: Use Git from the start

## 7. Practice Exercises

### Exercise 1: Installation Verification
Write a program that prints:
- Your Python version
- Your operating system
- Current working directory

### Exercise 2: Personal Information
Create a program that asks for and displays:
- Your name
- Your age
- Your favorite color

### Exercise 3: Unit Converter
Build a program that converts:
- Miles to kilometers
- Pounds to kilograms
- Fahrenheit to Celsius

## 8. Summary

**Key takeaways:**
- Python installation is straightforward across platforms
- Always verify installation with `python --version`
- VS Code with Python extension is recommended for beginners
- Interactive mode (REPL) is great for learning and testing
- Script mode is for actual programs
- Virtual environments are essential for project management

**Next Lecture:** We'll explore Python syntax fundamentals.

---

**Quick Reference:**
- Python Download: https://python.org/downloads
- VS Code: https://code.visualstudio.com
- Python Documentation: https://docs.python.org/3/tutorial/
- Virtual Environments: https://docs.python.org/3/library/venv.html