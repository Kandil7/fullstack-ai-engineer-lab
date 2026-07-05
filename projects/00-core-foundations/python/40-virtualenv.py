"""
W3Schools Python Tutorial - 40: Virtual Environments
=====================================================
Topics: venv, virtualenv, creating, activating, deactivating, requirements, managing environments

Run: python 40-virtualenv.py
Reference: https://www.w3schools.com/python/python_pip.asp
"""

# ============================================================
# What are Virtual Environments?
# ============================================================
# Virtual environments are isolated Python environments.
# They allow you to install packages without affecting global Python.
# Each project can have its own dependencies.
# Prevents version conflicts between projects.

# ============================================================
# Creating virtual environments with venv
# ============================================================
# Example 1: Create a virtual environment
# python -m venv myenv

# Example 2: Create with specific Python version
# python3.10 -m venv myenv

# Example 3: Create without pip (minimal)
# python -m venv --without-pip myenv

# ============================================================
# Activating environments
# ============================================================
# Windows (Command Prompt):
# Example 4: Activate in Command Prompt
# myenv\Scripts\activate.bat

# Windows (PowerShell):
# Example 5: Activate in PowerShell
# myenv\Scripts\Activate.ps1

# Linux/macOS:
# Example 6: Activate in bash/zsh
# source myenv/bin/activate

# Example 7: Activate in fish shell
# source myenv/bin/activate.fish

# When activated, you'll see (myenv) in your terminal prompt.

# ============================================================
# Deactivating environments
# ============================================================
# Example 8: Deactivate current environment
# deactivate

# This returns you to the global Python environment.

# ============================================================
# Installing packages in venvs
# ============================================================
# Example 9: Install a package
# pip install requests

# Example 10: Install multiple packages
# pip install numpy pandas matplotlib

# Example 11: Install from requirements.txt
# pip install -r requirements.txt

# ============================================================
# venv module vs virtualenv package
# ============================================================
# venv is built into Python 3.3+ (recommended).
# virtualenv is a third-party package (more features).
# virtualenv supports older Python versions.
# virtualenv is faster for creating environments.
# For most cases, venv is sufficient.

# ============================================================
# Managing requirements in venvs
# ============================================================
# Example 12: Export requirements
# pip freeze > requirements.txt

# Example 13: Install requirements in new environment
# python -m venv newenv
# newenv\Scripts\activate  (Windows)
# pip install -r requirements.txt

# Example 14: Requirements with comments
# Create requirements.txt with:
# # Web framework
# flask==2.3.2
# # Database
# sqlalchemy>=2.0.0

# ============================================================
# Multiple environments workflow
# ============================================================
# Example 15: Different projects, different environments
# Project A: python -m venv projectA-env
# Project B: python -m venv projectB-env
# Each can have different package versions.

# Example 16: Check which environment you're in
# which python  (Linux/macOS)
# where python   (Windows)
# pip list

# ============================================================
# Deleting/cleaning up venvs
# ============================================================
# Example 17: Delete a virtual environment
# Windows: rmdir /s /q myenv
# Linux/macOS: rm -rf myenv

# Just delete the folder - it's self-contained.

# ============================================================
# Using venv in projects
# ============================================================
# Example 18: Project structure
# myproject/
# ├── venv/              # Virtual environment (add to .gitignore)
# ├── src/
# │   └── main.py
# ├── requirements.txt   # Dependencies
# └── README.md

# Example 19: .gitignore for Python projects
# venv/
# .venv/
# env/
# *.pyc
# __pycache__/
# .env

# ============================================================
# Practical demonstration
# ============================================================
# Example 20: Check current environment info
import sys
import os

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Platform:", sys.platform)
print()

# Example 21: Check if we're in a virtual environment
in_venv = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
)

if in_venv:
    print("[+] Currently inside a virtual environment")
    print("  Environment path:", sys.prefix)
else:
    print("[-] Not in a virtual environment (using global Python)")
    print("  Python path:", sys.prefix)

print()

# Example 22: Show how to create and use a venv
print("Quick start guide:")
print("1. Create: python -m venv .venv")
print("2. Activate Windows: .venv\\Scripts\\activate")
print("3. Activate Linux/macOS: source .venv/bin/activate")
print("4. Install: pip install package_name")
print("5. Save: pip freeze > requirements.txt")
print("6. Deactivate: deactivate")
print()

# Example 23: Check for common venv directories
print("Checking for virtual environments in current directory:")
for item in os.listdir('.'):
    if os.path.isdir(item) and item in ['venv', '.venv', 'env', 'myenv']:
        print(f"  Found: {item}/")
        
print()
print("Tip: Always use virtual environments to isolate project dependencies!")