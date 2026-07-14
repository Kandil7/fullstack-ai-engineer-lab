# Python Modules — Lecture 25

## Topic Overview

**Modules** are Python files containing functions, classes, and variables that can be imported and reused in other programs. They're essential for organizing code, promoting reusability, and avoiding naming conflicts. Python comes with a rich standard library of modules and supports third-party packages via pip.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Create and import custom modules
- Understand different import styles
- Use the standard library modules
- Organize code into packages
- Understand the module search path
- Use `if __name__ == "__main__"`
- Apply best practices for module organization

---

## Key Concepts

### 1. Creating a Module

```python
# mymodule.py — a simple module
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

def add(a, b):
    """Add two numbers."""
    return a + b

PI = 3.14159

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return PI * self.radius ** 2
```

### 2. Importing Modules

```python
# Import entire module
import math
print(math.sqrt(16))  # 4.0

# Import specific items
from math import sqrt, pi
print(sqrt(16))  # 4.0
print(pi)  # 3.14159...

# Import with alias
import numpy as np
from datetime import datetime as dt

# Import everything (avoid in production!)
from math import *
```

### 3. The __name__ Variable

```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

# Only runs when file is executed directly
if __name__ == "__main__":
    print(greet("World"))  # Only runs when python mymodule.py
    # Doesn't run when imported by another file
```

### 4. Standard Library Modules

```python
# math — mathematical functions
import math
print(math.sqrt(25))     # 5.0
print(math.ceil(4.3))    # 5
print(math.floor(4.7))   # 4
print(math.pi)           # 3.14159...

# datetime — date and time
from datetime import datetime, date, timedelta
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
tomorrow = date.today() + timedelta(days=1)

# random — random number generation
import random
print(random.randint(1, 10))      # Random int 1-10
print(random.choice(["a", "b"]))  # Random element
print(random.random())            # Float 0.0-1.0

# os — operating system interface
import os
print(os.getcwd())              # Current directory
print(os.listdir("."))          # List files
os.makedirs("new_dir", exist_ok=True)

# json — JSON encoding/decoding
import json
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data)
parsed = json.loads(json_str)

# re — regular expressions
import re
pattern = r"\d+"
numbers = re.findall(pattern, "abc123def456")
print(numbers)  # ['123', '456']
```

### 5. Packages

```python
# Directory structure:
# mypackage/
#     __init__.py
#     module1.py
#     module2.py
#     subpackage/
#         __init__.py
#         module3.py

# __init__.py makes a directory a package
# mypackage/__init__.py
def init():
    print("Package initialized")

# Importing from packages
from mypackage import module1
from mypackage.module2 import function
from mypackage.subpackage import module3
```

### 6. Module Search Path

```python
import sys

# Where Python looks for modules
print(sys.path)

# Add custom path
sys.path.append("/my/custom/path")

# Module search order:
# 1. Current directory
# 2. PYTHONPATH environment variable
# 3. Default directories (standard library)
# 4. Site-packages (third-party)
```

### 7. Package Management with pip

```bash
# Install packages
pip install requests
pip install numpy==1.24.0  # Specific version

# List installed packages
pip list

# Show package info
pip show requests

# Install from requirements.txt
pip install -r requirements.txt

# Freeze current environment
pip freeze > requirements.txt
```

---

## Code Examples

### Example 1: Utility Module

```python
# utils.py
"""Common utility functions."""

def flatten(nested_list):
    """Flatten a nested list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def chunk(lst, size):
    """Split list into chunks."""
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def unique(lst):
    """Remove duplicates preserving order."""
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

if __name__ == "__main__":
    # Test functions
    print(flatten([1, [2, 3], [4, [5, 6]]]))
    print(chunk([1, 2, 3, 4, 5], 2))
    print(unique([1, 2, 2, 3, 1, 4]))
```

### Example 2: Configuration Module

```python
# config.py
"""Application configuration."""

import os

class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    API_KEY = os.getenv("API_KEY", "")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

def get_config():
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
```

### Example 3: Package Structure

```
mypackage/
    __init__.py          # Package initialization
    core.py              # Core functionality
    utils.py             # Utility functions
    models/
        __init__.py
        user.py
        product.py
    api/
        __init__.py
        endpoints.py
        serializers.py
```

```python
# mypackage/__init__.py
from .core import main_function
from .models.user import User
from .models.product import Product

__version__ = "1.0.0"
__all__ = ["main_function", "User", "Product"]
```

---

## Common Mistakes to Avoid

### Mistake 1: Circular Imports
```python
# a.py
# from b import function_b  # May cause circular import

# b.py
# from a import function_a  # Circular!

# SOLUTION: Use lazy imports or restructure code
def function_a():
    from b import function_b  # Import inside function
    return function_b()
```

### Mistake 2: Star Imports
```python
# WRONG — pollutes namespace, hard to track
from math import *
from random import *

# CORRECT — explicit imports
from math import sqrt, pi
from random import randint, choice
```

### Mistake 3: Running Module Code on Import
```python
# WRONG — runs when imported!
print("Loading module...")
main()

# CORRECT — use __name__ guard
if __name__ == "__main__":
    main()
```

---

## Best Practices

1. **Use explicit imports** — avoid `from module import *`
2. **Use `if __name__ == "__main__"`** for test code
3. **Organize imports**: stdlib → third-party → local
4. **Use packages** for related modules
5. **Write docstrings** for modules
6. **Use `requirements.txt`** to track dependencies
7. **Avoid circular imports** — restructure if needed
8. **Use virtual environments** for project isolation

---

## Practice Exercises

### Exercise 1: Math Utilities Module
Create a module with functions for factorial, gcd, and prime checking.

### Exercise 2: String Utilities Module
Create a module with functions for capitalize_words, snake_to_camel, and truncate.

### Exercise 3: Import a Module
Import the `collections` module and use `Counter` to count word frequencies in a sentence.

---

## Summary

- **Modules** are `.py` files containing reusable code
- **Import styles**: `import module`, `from module import func`, `import module as alias`
- **`__name__`** prevents code from running on import
- **Packages** are directories with `__init__.py`
- **Standard library** includes math, datetime, random, os, json, re
- **pip** manages third-party packages
- **`requirements.txt`** tracks dependencies
- **Virtual environments** isolate project dependencies
