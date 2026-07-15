# pip - Python Package Installer

## Topic 39: Managing Python Packages

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what pip is and why it matters
2. Install, upgrade, and remove packages
3. Search for packages on PyPI
4. Use requirements files
5. Manage package versions
6. Handle common pip issues

---

## 1. What is pip?

**pip** stands for "Pip Installs Packages" - the standard package manager for Python.

### Why Use pip?

- **Install libraries** from PyPI (Python Package Index)
- **Manage dependencies** for your projects
- **Version control** for packages
- **Virtual environment** support

---

## 2. Basic pip Commands

### Installing Packages

```bash
# Install latest version
pip install requests

# Install specific version
pip install requests==2.28.0

# Install minimum version
pip install requests>=2.25.0

# Install from requirements file
pip install -r requirements.txt
```

### Upgrading Packages

```bash
# Upgrade to latest version
pip install --upgrade requests

# Upgrade pip itself
pip install --upgrade pip
```

### Removing Packages

```bash
# Uninstall a package
pip uninstall requests

# Uninstall multiple
pip uninstall requests flask
```

---

## 3. Searching for Packages

```bash
# Search PyPI
pip search requests

# Better alternative: visit https://pypi.org
```

### Viewing Package Info

```bash
# Show package details
pip show requests

# Output:
# Name: requests
# Version: 2.28.0
# Summary: Python HTTP for Humans.
# ...
```

---

## 4. Listing Packages

```bash
# List installed packages
pip list

# List outdated packages
pip list --outdated

# List specific format
pip list --format=columns
pip list --format=json
```

---

## 5. Requirements Files

### Creating Requirements

```bash
# Save current packages
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Requirements File Format

```text
# requirements.txt
requests==2.28.0
flask>=2.0.0
numpy~=1.21.0
pandas
```

### Version Specifiers

| Specifier | Meaning | Example |
|-----------|---------|---------|
| `==` | Exact version | `requests==2.28.0` |
| `>=` | Minimum version | `requests>=2.25.0` |
| `<=` | Maximum version | `requests<=3.0.0` |
| `!=` | Exclude version | `requests!=2.27.0` |
| `~=` | Compatible release | `requests~=2.28.0` |

---

## 6. Virtual Environments

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

### pip in Virtual Environments

```bash
# Install packages in venv
pip install requests

# Save requirements
pip freeze > requirements.txt

# Exit venv
deactivate
```

---

## 7. Common pip Issues

### Permission Errors

```bash
# BAD - might cause permission issues
pip install requests

# GOOD - use --user flag
pip install --user requests

# Or use virtual environment (best practice)
python -m venv myenv
```

### Slow Downloads

```bash
# Use mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ requests

# Or configure in pip.conf
```

### Network Errors

```bash
# Retry with timeout
pip install --timeout 60 requests

# Use proxy
pip install --proxy http://proxy:8080 requests
```

---

## 8. Best Practices

1. **Use virtual environments** for each project
2. **Freeze requirements** with `pip freeze > requirements.txt`
3. **Pin versions** for reproducibility
4. **Use `--user`** if not using venv
5. **Update pip** regularly
6. **Check PyPI** for package info
7. **Use `pip show`** before installing

---

## 9. Practice Exercises

### Exercise 1: Setup Project

```bash
# 1. Create virtual environment
python -m venv project_env

# 2. Activate
# Windows:
project_env\Scripts\activate
# macOS/Linux:
source project_env/bin/activate

# 3. Install packages
pip install requests flask pytest

# 4. Save requirements
pip freeze > requirements.txt

# 5. Verify
cat requirements.txt
```

### Exercise 2: Install from Requirements

```bash
# Create requirements.txt
echo "requests>=2.28.0" > requirements.txt
echo "flask>=2.0.0" >> requirements.txt

# Install
pip install -r requirements.txt

# Verify
pip list
```

---

## 10. Summary

| Command | Description |
|---------|-------------|
| `pip install pkg` | Install package |
| `pip install pkg==1.0` | Install specific version |
| `pip install --upgrade pkg` | Upgrade package |
| `pip uninstall pkg` | Remove package |
| `pip list` | List installed packages |
| `pip show pkg` | Show package info |
| `pip freeze` | List packages (for requirements) |
| `pip install -r file.txt` | Install from requirements |

---

## Next Steps

- Learn about Poetry or Pipenv for advanced dependency management
- Explore publishing your own packages to PyPI
- Study dependency locking strategies
