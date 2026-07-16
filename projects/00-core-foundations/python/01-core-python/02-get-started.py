"""
W3Schools Python Tutorial - 02: Get Started
============================================
Topics: Installing Python, running Python in terminal, running Python files

Run: python 02-get-started.py
Reference: https://www.w3schools.com/python/python_getting_started.asp
"""

# ============================================================
# Installing Python
# ============================================================
# Step 1: Download Python from https://www.python.org/downloads/
# Step 2: Run the installer - CHECK "Add Python to PATH"
# Step 3: Verify installation by opening a terminal and typing:
#         python --version
#         or: python3 --version

import sys
print(f"Python version: {sys.version}")
print(f"Executable path: {sys.executable}")
# Output: Python version: 3.x.x and the path to your python executable

# ============================================================
# Running Python in the Terminal
# ============================================================
# You can run Python code directly in the terminal (interactive mode):
#
# $ python
# >>> print("Hello from terminal!")
# Hello from terminal!
# >>> exit()
#
# Or use the short form:
# $ python -c "print('Hello inline!')"

# This script demonstrates running a .py file:
print("\nThis script is running as a .py file!")
print("You ran it with: python 02-get-started.py")

# ============================================================
# Running Python Files
# ============================================================
# There are three main ways to run Python:
#
# 1. Interactive mode (REPL):
#    $ python
#    >>> print("Hello")
#    Hello
#
# 2. Script mode (run a file):
#    $ python my_script.py
#
# 3. Inline execution:
#    $ python -c "print('inline')"
#
# 4. From an IDE:
#    VS Code, PyCharm, etc. have built-in run buttons

print("\nWays to run Python:")
print("1. Interactive mode: python  (then type commands)")
print("2. Script mode: python script.py")
print("3. Inline: python -c \"print('hello')\"")
print("4. IDE: Click the Run button")

# ============================================================
# The Python Command Line
# ============================================================
# When running python without arguments, you enter the REPL:
# - REPL stands for Read-Eval-Print-Loop
# - Each line you type is read, evaluated, and the result printed
# - Type 'exit()' or 'quit()' to leave

# Demonstrating that this file IS running in Python:
if sys.version_info >= (3, 6):
    print(f"\nPython {sys.version_info.major}.{sys.version_info.minor} detected - great!")
else:
    print("\nPlease upgrade to Python 3.6 or newer for f-strings!")

# ============================================================
# Example: Your first Python calculation
# ============================================================
print("\n--- Python as a Calculator ---")
print(f"10 + 5 = {10 + 5}")       # Output: 10 + 5 = 15
print(f"10 - 5 = {10 - 5}")       # Output: 10 - 5 = 5
print(f"10 * 5 = {10 * 5}")       # Output: 10 * 5 = 50
print(f"10 / 5 = {10 / 5}")       # Output: 10 / 5 = 2.0
print(f"10 ** 2 = {10 ** 2}")     # Output: 10 ** 2 = 100

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Download Python from python.org")
print("2. Always check 'Add Python to PATH' during installation")
print("3. Verify with: python --version")
print("4. Run files with: python filename.py")
print("5. Use interactive mode for quick testing")
