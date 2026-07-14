# Python Modules — Glossary 25

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Module | Python file with reusable code | `import math` |
| Package | Directory of modules with `__init__.py` | `import mypackage` |
| Import | Load module/function into namespace | `from math import sqrt` |
| Import Alias | Rename module on import | `import numpy as np` |
| `__name__` | Module's name variable | `if __name__ == "__main__":` |
| `__init__.py` | Package initializer file | Empty or with imports |
| Standard Library | Built-in Python modules | `math`, `datetime`, `os` |
| pip | Package installer | `pip install requests` |
| requirements.txt | Dependency file | `pip install -r requirements.txt` |
| Virtual Env | Isolated Python environment | `python -m venv env` |
| Site-packages | Third-party package directory | `pip show requests` |
| Module Search Path | `sys.path` lookup order | Current → PYTHONPATH → default |
| Star Import | Import everything | `from math import *` |
| Lazy Import | Import inside function | `def f(): import module` |
| Circular Import | Mutual import dependency | A imports B, B imports A |
| Namespace | Module's symbol table | Functions, classes, variables |
| Docstring | Module-level documentation | `"""Module description"""` |
| `__all__` | Exported names list | `__all__ = ["func1", "func2"]` |
| Entry Point | Module's main execution | `if __name__ == "__main__"` |
| PYTHONPATH | Env var for module search | Extra directories to search |

---

## Definitions

### Circular Import
**Definition**: A situation where two or more modules import each other, either directly or indirectly, potentially causing import errors or unexpected behavior.

**Example**:
```python
# a.py
from b import func_b
def func_a():
    return func_b()

# b.py
from a import func_a  # Circular!
def func_b():
    return func_a()

# SOLUTION: Lazy import
def func_a():
    from b import func_b  # Import inside function
    return func_b()
```

**Related**: lazy import, module dependency, restructuring

---

### Import
**Definition**: A statement that loads a module or specific names from a module into the current namespace.

**Example**:
```python
# Import entire module
import math

# Import specific names
from math import sqrt, pi

# Import with alias
import datetime as dt

# Import all (avoid)
from math import *
```

**Related**: module, namespace, alias, from...import

---

### Import Alias
**Definition**: A renamed reference to a module or function when importing, using the `as` keyword.

**Example**:
```python
import numpy as np           # Common alias
import pandas as pd          # Common alias
from datetime import datetime as dt

print(np.array([1, 2, 3]))
print(dt.now())
```

**Related**: import, convention, numpy, pandas

---

### Lazy Import
**Definition**: Importing a module inside a function or method rather than at the top of the file. Used to avoid circular imports or reduce startup time.

**Example**:
```python
def process_data():
    import pandas as pd  # Only imported when function is called
    df = pd.read_csv("data.csv")
    return df
```

**Related**: circular import, performance, conditional import

---

### Module
**Definition**: A `.py` file containing Python definitions and statements. Functions, classes, and variables defined in a module can be imported and reused.

**Example**:
```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159

class Circle:
    def __init__(self, radius):
        self.radius = radius
```

**Related**: package, import, namespace, `__name__`

---

### Module Search Path
**Definition**: The ordered list of directories Python searches when importing a module. Stored in `sys.path`.

**Example**:
```python
import sys
print(sys.path)
# ['', '/usr/lib/python3.x', '/usr/lib/python3.x/lib-dynload', ...]

# Add custom path
sys.path.insert(0, "/my/modules")
```

**Related**: `sys.path`, PYTHONPATH, site-packages, import

---

### Namespace
**Definition**: A container mapping names to objects. Each module has its own namespace, preventing naming conflicts.

**Example**:
```python
# math namespace contains sqrt, pi, etc.
import math
print(math.sqrt)  # <built-in function sqrt>

# Separate namespace
import random
print(random.sqrt)  # AttributeError — not in random namespace
```

**Related**: scope, module, import, naming conflicts

---

### Package
**Definition**: A directory containing Python modules and an `__init__.py` file that makes it importable as a module.

**Example**:
```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

```python
from mypackage import module1
from mypackage.subpackage import module3
```

**Related**: `__init__.py`, module, directory, namespace package

---

### PYTHONPATH
**Definition**: An environment variable specifying additional directories to search for modules, added to `sys.path`.

**Example**:
```bash
# Linux/Mac
export PYTHONPATH="/my/modules:$PYTHONPATH"

# Windows
set PYTHONPATH=C:\my\modules;%PYTHONPATH%
```

**Related**: `sys.path`, module search, environment variable

---

### Requirements.txt
**Definition**: A text file listing all Python package dependencies for a project. Used with pip to install dependencies.

**Example**:
```
# requirements.txt
requests==2.28.0
numpy>=1.24.0
pandas~=1.5.0
flask
```

```bash
pip install -r requirements.txt
```

**Related**: pip, dependencies, virtual environment

---

### Site-packages
**Definition**: The directory where pip installs third-party packages. Part of the module search path.

**Example**:
```bash
# Find site-packages
python -c "import site; print(site.getsitepackages())"

# Install location
pip install requests  # Installed to site-packages/requests/
```

**Related**: pip, third-party, import, sys.path

---

### Star Import
**Definition**: Importing all public names from a module using `from module import *`. Generally discouraged due to namespace pollution.

**Example**:
```python
# BAD — namespace pollution
from math import *
from random import *

# GOOD — explicit imports
from math import sqrt, pi
from random import randint, choice
```

**Related**: namespace pollution, explicit imports, best practices

---

### Virtual Environment
**Definition**: An isolated Python environment with its own packages and dependencies, preventing conflicts between projects.

**Example**:
```bash
# Create virtual environment
python -m venv myenv

# Activate (Linux/Mac)
source myenv/bin/activate

# Activate (Windows)
myenv\Scripts\activate

# Install packages
pip install requests

# Deactivate
deactivate
```

**Related**: venv, pip, dependencies, isolation

---

### __all__
**Definition**: A list of names that should be exported when `from module import *` is used. Controls what gets imported with star imports.

**Example**:
```python
# mymodule.py
__all__ = ["public_func", "PublicClass"]

def public_func():
    pass

def _private_func():  # Not exported
    pass

class PublicClass:
    pass
```

**Related**: star import, namespace, public API

---

### __init__.py
**Definition**: A Python file in a directory that makes it a package. Can be empty or contain initialization code and imports.

**Example**:
```python
# mypackage/__init__.py
from .module1 import Class1
from .module2 import function2

__version__ = "1.0.0"
__all__ = ["Class1", "function2"]
```

**Related**: package, module, import, namespace

---

### __name__
**Definition**: A special variable containing the name of the current module. Equals `"__main__"` when the file is executed directly.

**Example**:
```python
# mymodule.py
def main():
    print("Running directly!")

if __name__ == "__main__":
    main()  # Only runs when executed, not imported

# When imported:
# import mymodule — main() NOT called
# When executed:
# python mymodule.py — main() IS called
```

**Related**: entry point, main guard, module execution

---

### Docstring
**Definition**: A string literal at the beginning of a module, class, or function that provides documentation. Accessible via `__doc__`.

**Example**:
```python
"""My Module.

This module provides utility functions for data processing.
"""

def process(data):
    """Process the input data.
    
    Args:
        data: Input data to process
    
    Returns:
        Processed data
    """
    pass
```

**Related**: documentation, `__doc__`, help()

---

### Entry Point
**Definition**: The starting point of a program's execution. In Python modules, typically indicated by `if __name__ == "__main__":`.

**Example**:
```python
# app.py
def main():
    print("Application started")
    # ... application logic

if __name__ == "__main__":
    main()
```

**Related**: `__name__`, main guard, script execution

---

### Standard Library
**Definition**: Python's built-in collection of modules that come with every Python installation. Includes math, datetime, os, json, re, and many more.

**Example**:
```python
import math
import datetime
import os
import json
import re
import collections
import itertools
```

**Related**: built-in, third-party, pip, modules

---

## Code Examples

### Example 1: Custom Module
```python
# math_utils.py
"""Custom math utilities module."""

def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    print(factorial(5))  # 120
    print(is_prime(17))  # True
```

### Example 2: Package Structure
```
dataflow/
    __init__.py
    extract.py
    transform.py
    load.py
    utils/
        __init__.py
        validators.py
        formatters.py
```

---

## Related Concepts

- **Libraries vs. Packages**: A library is a collection of packages
- **Modules vs. Packages**: A package is a directory of modules
- **Namespaces**: Python's mechanism for avoiding naming conflicts
- **Duck Typing**: Modules imported by behavior, not type
- **Meta Path Finders**: Advanced module finding mechanism
