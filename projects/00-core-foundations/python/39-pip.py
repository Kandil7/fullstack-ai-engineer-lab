"""
W3Schools Python Tutorial - 39: pip
====================================
Topics: What is pip, install, uninstall, list, show, freeze, requirements.txt, git repos, upgrading

Run: python 39-pip.py
Reference: https://www.w3schools.com/python/python_pip.asp
"""

# ============================================================
# What is pip?
# ============================================================
# pip is the package installer for Python.
# It installs packages from the Python Package Index (PyPI).
# pip is included with Python 3.4+ by default.
# You can install, upgrade, and remove packages.

# ============================================================
# Basic pip commands (run in terminal)
# ============================================================
# Example 1: Installing a package
# pip install requests

# Example 2: Installing a specific version
# pip install requests==2.28.1

# Example 3: Installing with version constraints
# pip install "requests>=2.25,<3.0"

# ============================================================
# Uninstalling packages
# ============================================================
# Example 4: Uninstall a package
# pip uninstall requests

# Example 5: Uninstall without confirmation
# pip uninstall -y requests

# ============================================================
# Listing packages
# ============================================================
# Example 6: List all installed packages
# pip list

# Example 7: List outdated packages
# pip list --outdated

# Example 8: List locally installed packages (not from PyPI)
# pip list --local

# ============================================================
# Package details with pip show
# ============================================================
# Example 9: Show package details
# pip show requests

# Example 10: Show multiple packages
# pip show requests numpy pandas

# Output includes: Name, Version, Summary, Home-page, Author, etc.

# ============================================================
# Freeze and requirements.txt
# ============================================================
# Example 11: Freeze current environment
# pip freeze

# Example 12: Save to requirements.txt
# pip freeze > requirements.txt

# Example 13: Install from requirements.txt
# pip install -r requirements.txt

# Example requirements.txt content:
# requests==2.28.1
# numpy>=1.24.0
# pandas~=2.0.0

# ============================================================
# Installing from Git repositories
# ============================================================
# Example 14: Install from GitHub
# pip install git+https://github.com/user/repo.git

# Example 15: Install specific branch
# pip install git+https://github.com/user/repo.git@branch_name

# Example 16: Install specific commit
# pip install git+https://github.com/user/repo.git@commit_hash

# ============================================================
# Upgrading packages
# ============================================================
# Example 17: Upgrade a package
# pip install --upgrade requests

# Example 18: Upgrade pip itself
# python -m pip install --upgrade pip

# ============================================================
# Useful pip options
# ============================================================
# Example 19: Install with verbose output
# pip install -v requests

# Example 20: Install without dependencies
# pip install --no-deps requests

# Example 21: Install to user directory
# pip install --user requests

# ============================================================
# Practical demonstration (simulated)
# ============================================================
# Example 22: Check if a package is installed
import sys
import subprocess

def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

# Example 23: Show Python and pip info
print("Python version:", sys.version)
print("Python executable:", sys.executable)
print()

# Example 24: List some common packages
common_packages = ['pip', 'setuptools', 'wheel']
print("Checking common packages:")
for pkg in common_packages:
    installed = check_package_installed(pkg)
    status = "installed" if installed else "not installed"
    print(f"  {pkg}: {status}")

print()
print("Note: Most pip commands must be run from terminal, not inside Python.")
print("The examples above show the syntax for reference.")
print()
print("Common workflow:")
print("  1. Create virtual environment: python -m venv myenv")
print("  2. Activate environment: myenv\\Scripts\\activate (Windows)")
print("  3. Install packages: pip install package_name")
print("  4. Save requirements: pip freeze > requirements.txt")
print("  5. Reproduce environment: pip install -r requirements.txt")