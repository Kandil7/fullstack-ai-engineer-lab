# Python Getting Started - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Python | Language | High-level programming language |
| pip | Tool | Package installer for Python |
| venv | Tool | Python's built-in virtual environment module |
| virtualenv | Tool | Third-party virtual environment creator |
| conda | Tool | Package and environment management system |
| VS Code | IDE | Visual Studio Code editor |
| PyCharm | IDE | Python-focused IDE by JetBrains |
| REPL | Tool | Read-Eval-Print Loop interactive shell |
| IDLE | IDE | Python's default development environment |
| PATH | System | Environment variable for executable locations |

## Detailed Definitions

### A

**Activation Script**
- **Definition**: Script that modifies shell environment for virtual environment
- **Example**: `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (Unix)
- **Related terms**: Virtual Environment, Shell Environment, Deactivation
```bash
# Windows activation
myenv\Scripts\activate

# macOS/Linux activation
source myenv/bin/activate

# Deactivation
deactivate
```

### B

**Bytecode Compilation**
- **Definition**: Process of translating Python source to intermediate code
- **Example**: `.py` files become `.pyc` files in `__pycache__`
- **Related terms**: Interpreter, Compilation, Module Cache
```python
# Python automatically compiles to bytecode
import py_compile
py_compile.compile('script.py')

# Bytecode files appear in __pycache__/
# script.cpython-312.pyc
```

### C

**Command Line**
- **Definition**: Text-based interface for interacting with operating system
- **Example**: Terminal, Command Prompt, PowerShell
- **Related terms**: Shell, Terminal, CLI
```bash
# Windows Command Prompt
python --version

# macOS/Linux Terminal
python3 --version
```

**Configuration File**
- **Definition**: File containing settings for applications or projects
- **Example**: `.vscode/settings.json`, `requirements.txt`
- **Related terms**: Settings, Environment Variables, Config
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.pylintEnabled": true
}
```

### D

**Dependency**
- **Definition**: External package required by your project
- **Example**: `requests` library for HTTP requests
- **Related terms**: Package, Requirements, Virtual Environment
```python
# requirements.txt
requests==2.31.0
flask==3.0.0
pandas==2.1.0
```

**Deactivation**
- **Definition**: Process of exiting virtual environment
- **Example**: `deactivate` command
- **Related terms**: Virtual Environment, Activation
```bash
# Deactivate current virtual environment
deactivate
# Returns to global Python environment
```

### E

**Environment Variable**
- **Definition**: Dynamic-named value stored in operating system
- **Example**: `PATH`, `PYTHONPATH`, `VIRTUAL_ENV`
- **Related terms**: PATH, Configuration, System Settings
```bash
# Check environment variables
echo $PATH  # Unix/macOS
echo %PATH%  # Windows

# Set environment variable (temporary)
export MY_VAR="value"  # Unix/macOS
set MY_VAR="value"  # Windows
```

**Executable**
- **Definition**: File that can be run as a program
- **Example**: `python.exe`, `pip.exe`, `code.exe`
- **Related terms**: Binary, Command, Script
```bash
# Find Python executable
which python  # Unix/macOS
where python  # Windows
```

### I

**IDE (Integrated Development Environment)**
- **Definition**: Software for comprehensive programming facilities
- **Example**: VS Code, PyCharm, IntelliJ IDEA
- **Related terms**: Text Editor, Debugger, Terminal
```python
# IDE features:
# - Code editing with syntax highlighting
# - Auto-completion
# - Debugging tools
# - Version control integration
# - Package management
```

**Interpreter Path**
- **Definition**: Location of Python executable on system
- **Example**: `/usr/bin/python3`, `C:\Python312\python.exe`
- **Related terms**: PATH, Executable, Installation
```python
# Find Python interpreter path
import sys
print(sys.executable)
# Output: /usr/bin/python3 or C:\Python312\python.exe
```

### L

**Library**
- **Definition**: Collection of pre-written code modules
- **Example**: `math`, `os`, `requests`
- **Related terms**: Module, Package, Framework
```python
# Standard library modules
import math
import os
import sys
import datetime

# Third-party library
import requests
```

**Local Installation**
- **Definition**: Python installed for current user only
- **Example**: User-level Python installation
- **Related terms**: System Installation, Virtual Environment
```bash
# Install packages locally
pip install --user package_name

# Check local packages
pip list --user
```

### M

**Module**
- **Definition**: Single Python file containing code
- **Example**: `math.py`, `random.py`, custom modules
- **Related terms**: Package, Library, Import
```python
# Import entire module
import math
print(math.pi)

# Import specific function
from math import sqrt
print(sqrt(16))

# Import with alias
import numpy as np
```

### P

**Package**
- **Definition**: Directory containing multiple modules
- **Example**: `numpy`, `pandas`, `flask`
- **Related terms**: Module, Library, PyPI
```
package_name/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

**Package Manager**
- **Definition**: Tool for installing, updating, and removing packages
- **Example**: pip, conda, poetry
- **Related terms**: pip, PyPI, Dependency Management
```bash
# pip commands
pip install package_name
pip uninstall package_name
pip install --upgrade package_name
pip list  # Show installed packages
```

**PATH**
- **Definition**: Environment variable listing executable directories
- **Example**: Contains directories like `/usr/bin`, `C:\Python312`
- **Related terms**: Environment Variable, Executable, Installation
```bash
# View PATH
echo $PATH  # Unix/macOS
echo %PATH%  # Windows

# Add to PATH (Unix/macOS - add to .bashrc or .zshrc)
export PATH="/path/to/python:$PATH"
```

**pip**
- **Definition**: Package installer for Python
- **Example**: `pip install requests`
- **Related terms**: PyPI, Package Manager, Virtual Environment
```bash
# Install package
pip install requests

# Install specific version
pip install requests==2.31.0

# Install from requirements file
pip install -r requirements.txt

# Show installed packages
pip list
```

**PyPI (Python Package Index)**
- **Definition**: Official repository for Python packages
- **Example**: https://pypi.org
- **Related terms**: pip, Package, Repository
- **Stats**: 400,000+ packages available

**Python Launcher**
- **Definition**: Utility for managing Python versions on Windows
- **Example**: `py` command, `py -3.12`
- **Related terms**: Python Version, Windows Installation
```bash
# Windows Python Launcher
py --version  # Check version
py -3.12 script.py  # Run with specific version
py -3.12 -m pip install package  # Install with specific version
```

### Q

**Quick Start**
- **Definition**: Minimal steps to begin using a technology
- **Example**: Install Python → Write code → Run script
- **Related terms**: Installation, Setup, Tutorial
```bash
# Python Quick Start
# 1. Install Python
# 2. Verify: python --version
# 3. Create file: hello.py
# 4. Run: python hello.py
```

### R

**REPL (Read-Eval-Print Loop)**
- **Definition**: Interactive programming environment
- **Example**: Python's interactive shell
- **Related terms**: Interactive Mode, Interpreter
```python
# Start REPL
python

# REPL operations
>>> 2 + 2
4
>>> "hello".upper()
'HELLO'
>>> exit()  # Exit REPL
```

**Requirements File**
- **Definition**: Text file listing project dependencies
- **Example**: `requirements.txt`
- **Related terms**: Dependency, pip, Virtual Environment
```text
# requirements.txt
requests==2.31.0
flask==3.0.0
python-dotenv==1.0.0
```

### S

**Script Mode**
- **Definition**: Running Python code from saved files
- **Example**: `python script.py`
- **Related terms**: Interactive Mode, File Execution
```python
# Save as script.py
def main():
    print("Running in script mode")

if __name__ == "__main__":
    main()
```

**Shell**
- **Definition**: Command-line interface for operating system
- **Example**: Bash, Zsh, PowerShell, Command Prompt
- **Related terms**: Terminal, Command Line, CLI
```bash
# Common shell commands
ls  # List files (Unix/macOS)
dir  # List files (Windows)
cd  # Change directory
pwd  # Print working directory
```

**System Installation**
- **Definition**: Python installed for all users
- **Example**: System-wide Python installation
- **Related terms**: Local Installation, Virtual Environment
```bash
# System-wide installation (Linux)
sudo apt install python3

# Check system Python
which python3
```

### T

**Terminal**
- **Definition**: Text-based interface for system interaction
- **Example**: Terminal.app, Windows Terminal, GNOME Terminal
- **Related terms**: Command Line, Shell, CLI
```bash
# Open terminal
# macOS: Cmd+Space → "Terminal"
# Windows: Win+R → "cmd" or "powershell"
# Linux: Ctrl+Alt+T
```

**Third-party Package**
- **Definition**: Package not part of Python's standard library
- **Example**: `requests`, `flask`, `pandas`
- **Related terms**: PyPI, pip, Package Manager
```bash
# Install third-party packages
pip install requests
pip install flask
pip install pandas
```

### V

**Version Control**
- **Definition**: System for tracking code changes over time
- **Example**: Git, GitHub, GitLab
- **Related terms**: Git, Repository, Commit
```bash
# Initialize Git repository
git init

# Basic Git commands
git add .
git commit -m "Initial commit"
git push origin main
```

**Virtual Environment**
- **Definition**: Isolated Python environment for project dependencies
- **Example**: `venv`, `virtualenv`, `conda`
- **Related terms**: pip, Dependency Management, Activation
```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate

# Activate (macOS/Linux)
source myenv/bin/activate

# Deactivate
deactivate
```

## Key Concepts Summary

### Installation Checklist
- [ ] Python 3.8+ installed
- [ ] pip installed and working
- [ ] PATH configured correctly
- [ ] IDE installed (VS Code recommended)
- [ ] Python extension installed in IDE
- [ ] Virtual environment tool ready

### Development Workflow
1. **Install Python** → System-wide or user-level
2. **Create Project** → Directory for your code
3. **Create Virtual Environment** → Isolate dependencies
4. **Activate Environment** → Enter isolated environment
5. **Install Packages** → `pip install package_name`
6. **Write Code** → Create `.py` files
7. **Run Code** → `python script.py`
8. **Version Control** → Git for tracking changes

### Common Commands Reference
```bash
# Python commands
python --version
python -c "print('Hello')"
python -m venv myenv

# pip commands
pip install package
pip uninstall package
pip list
pip freeze > requirements.txt
pip install -r requirements.txt

# Virtual environment
python -m venv myenv
source myenv/bin/activate  # Unix/macOS
myenv\Scripts\activate     # Windows
deactivate
```

## Practice Terms

Match these terms to their definitions:
1. venv - ?
2. pip - ?
3. REPL - ?
4. PATH - ?
5. Requirements file - ?

**Answers:**
1. Python's built-in virtual environment module
2. Package installer for Python
3. Read-Eval-Print Loop interactive shell
4. Environment variable for executable locations
5. Text file listing project dependencies