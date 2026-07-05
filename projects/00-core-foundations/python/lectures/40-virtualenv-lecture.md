# Virtual Environments in Python

## Topic 40: Isolating Python Projects

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand why virtual environments matter
2. Create and activate virtual environments
3. Manage packages within environments
4. Use requirements files for reproducibility
5. Work with multiple Python versions
6. Apply best practices for project isolation

---

## 1. What is a Virtual Environment?

A **self-contained directory** containing a Python installation and packages, separate from the system Python.

### Why Use Virtual Environments?

- **Isolation**: Each project has its own dependencies
- **No conflicts**: Different projects can use different package versions
- **Reproducibility**: Easy to recreate environments
- **Clean system**: Don't pollute global Python

### The Problem Without Virtual Environments

```bash
# Project A needs requests==2.25.0
pip install requests==2.25.0

# Project B needs requests==2.28.0
pip install requests==2.28.0  # Overwrites! Project A breaks!
```

---

## 2. Creating Virtual Environments

### Using `venv` (Standard Library)

```bash
# Create virtual environment
python -m venv myenv

# Create with specific Python version
python3.10 -m venv myenv

# Create with site-packages access
python -m venv --system-site-packages myenv
```

### Directory Structure

```
myenv/
├── Include/
├── Lib/
│   └── site-packages/
├── Scripts/          # Windows
│   ├── activate
│   ├── pip.exe
│   └── python.exe
└── pyvenv.cfg
```

---

## 3. Activating Virtual Environments

### Windows

```bash
# Command Prompt
myenv\Scripts\activate

# PowerShell
myenv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source myenv/bin/activate
```

### Verify Activation

```bash
# After activation, (myenv) appears in prompt
(myenv) C:\Projects\myproject>

# Check Python location
which python  # macOS/Linux
where python  # Windows
# Should show path inside myenv/
```

---

## 4. Working in Virtual Environments

### Installing Packages

```bash
# Activate environment first
(myenv) $ pip install requests flask

# Check installed packages
(myenv) $ pip list

# Save to requirements.txt
(myenv) $ pip freeze > requirements.txt
```

### Deactivating

```bash
(myenv) $ deactivate
$
```

---

## 5. Requirements Files

### Creating Requirements

```bash
# Save current environment
(myenv) $ pip freeze > requirements.txt
```

### Example requirements.txt

```text
certifi==2022.12.7
charset-normalizer==3.1.0
Flask==2.2.2
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
requests==2.28.1
urllib3==1.26.14
Werkzeug==2.2.2
```

### Recreating Environment

```bash
# Create new environment
python -m venv newenv

# Activate
newenv\Scripts\activate  # Windows
source newenv/bin/activate  # macOS/Linux

# Install from requirements
pip install -r requirements.txt
```

---

## 6. Managing Multiple Environments

### Project Structure

```
projects/
├── project_a/
│   ├── venv/
│   ├── requirements.txt
│   └── ...
├── project_b/
│   ├── env/
│   ├── requirements.txt
│   └── ...
```

### Switching Projects

```bash
# Work on Project A
cd projects/project_a
venv\Scripts\activate  # Windows
# ... work on Project A ...
deactivate

# Work on Project B
cd projects/project_b
source venv/bin/activate  # macOS/Linux
# ... work on Project B ...
deactivate
```

---

## 7. Alternative Tools

### virtualenv (Third-party)

```bash
# Install
pip install virtualenv

# Create environment
virtualenv myenv

# Create with specific Python
virtualenv --python=python3.10 myenv
```

### Poetry

```bash
# Install
pip install poetry

# Create project
poetry new myproject

# Add dependency
poetry add requests

# Install all dependencies
poetry install
```

### Pipenv

```bash
# Install
pip install pipenv

# Create environment and install
pipenv install requests

# Activate shell
pipenv shell
```

---

## 8. Common Issues and Solutions

### Issue: "python" not found

```bash
# Use python3 explicitly
python3 -m venv myenv

# Or check Python installation
python --version
python3 --version
```

### Issue: Permission errors

```bash
# Use --user flag (not recommended for venvs)
# Better: use virtual environment properly
```

### Issue: Forgetting to activate

```bash
# Always activate before working!
myenv\Scripts\activate

# Or use full path to venv Python
myenv\Scripts\python.exe script.py
```

### Issue: Gitignore

Add to `.gitignore`:
```
venv/
env/
myenv/
*.pyc
__pycache__/
```

---

## 9. Best Practices

1. **Always use virtual environments** for projects
2. **Name environments** consistently (`.venv`, `venv`, `env`)
3. **Commit requirements.txt** to version control
4. **Don't commit** the environment folder
5. **Document** Python version in README
6. **Use `.gitignore`** for environment files
7. **Create fresh environments** for new projects

---

## 10. Practice Exercises

### Exercise 1: Create Project Environment

```bash
# 1. Create project directory
mkdir myproject
cd myproject

# 2. Create virtual environment
python -m venv .venv

# 3. Activate (Windows)
.venv\Scripts\activate

# 4. Install packages
pip install requests flask pytest

# 5. Save requirements
pip freeze > requirements.txt

# 6. Verify
cat requirements.txt
```

### Exercise 2: Recreate Environment

```bash
# 1. Create new environment
python -m venv .venv-new

# 2. Activate
.venv-new\Scripts\activate

# 3. Install from requirements
pip install -r requirements.txt

# 4. Verify same packages
pip list
```

---

## 11. Summary

| Concept | Key Points |
|---------|------------|
| **Virtual environment** | Isolated Python + packages |
| **venv** | Standard library module |
| **activate** | Enable environment |
| **deactivate** | Disable environment |
| **freeze** | Save package list |
| **requirements.txt** | Dependency file |
| **Isolation** | Prevents conflicts |

---

## Next Steps

- Learn about Poetry for modern dependency management
- Explore Docker for full environment isolation
- Study CI/CD with virtual environments
