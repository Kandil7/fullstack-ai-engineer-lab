# Virtual Environments Glossary

## Topic 40: Quick Reference Guide

---

## Glossary Terms

### A

#### Activate
**Definition:** Enable a virtual environment for use.
```bash
# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
```
**Related:** Deactivate, environment

---

### D

#### Deactivate
**Definition:** Disable current virtual environment.
```bash
deactivate
```
**Related:** Activate, exit environment

---

### E

#### Environment
**Definition:** Isolated Python installation with own packages.
```bash
python -m venv myenv  # Create environment
```
**Related:** Virtual environment, venv, isolation

#### Environment Variable
**Definition:** System-level configuration values.
```bash
# Check Python in PATH
echo %PATH%  # Windows
echo $PATH   # macOS/Linux
```
**Related:** PATH, system configuration

---

### I

#### Isolation
**Definition:** Separating project dependencies from system Python.
```bash
# Each project has its own venv
# No conflicts between projects
```
**Related:** Virtual environment, dependency management

---

### P

#### PATH
**Definition:** System variable for executable locations.
```bash
# Where Python is found
which python  # Shows PATH location
```
**Related:** Environment variable, executable

#### Project Dependencies
**Definition:** External packages a project requires.
```bash
# Listed in requirements.txt
pip install -r requirements.txt
```
**Related:** requirements.txt, packages

---

### R

#### Requirements File
**Definition:** Text file listing package dependencies.
```text
# requirements.txt
requests==2.28.0
flask>=2.0.0
```
**Related:** `pip freeze`, dependency file

---

### V

#### venv
**Definition:** Python standard library module for virtual environments.
```bash
python -m venv myenv
```
**Related:** Virtual environment, isolation

#### Virtual Environment
**Definition:** Self-contained Python + packages directory.
```bash
python -m venv .venv
source .venv/bin/activate  # Activate
```
**Related:** Isolation, venv, packages

---

## Quick Reference Table

| Term | Command/Concept | Description |
|------|-----------------|-------------|
| **venv** | `python -m venv name` | Create environment |
| **activate** | `source name/bin/activate` | Enable environment |
| **deactivate** | `deactivate` | Disable environment |
| **freeze** | `pip freeze > req.txt` | Save dependencies |
| **install -r** | `pip install -r req.txt` | Install from file |
| **isolation** | Concept | Separate dependencies |
| **PATH** | System variable | Executable locations |
| **requirements.txt** | File | Dependency list |
| **.venv** | Directory name | Common venv name |
| **site-packages** | Directory | Installed packages |

---

## Virtual Environment Workflow

### Create
```bash
python -m venv .venv
```

### Activate
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Work
```bash
pip install requests
pip freeze > requirements.txt
python script.py
```

### Deactivate
```bash
deactivate
```

### Recreate
```bash
python -m venv .venv
pip install -r requirements.txt
```

---

## Common Environment Tools

| Tool | Type | Command |
|------|------|---------|
| **venv** | Standard lib | `python -m venv` |
| **virtualenv** | Third-party | `virtualenv` |
| **Poetry** | Dependency mgr | `poetry new` |
| **Pipenv** | Dependency mgr | `pipenv install` |
| **conda** | Package manager | `conda create` |

---

## Troubleshooting

### "python" not found
```bash
# Use python3
python3 -m venv .venv

# Or check version
python --version
python3 --version
```

### Permission errors
```bash
# Use virtual environment (not system)
python -m venv .venv
```

### Forgot to activate
```bash
# Use full path
.venv\Scripts\python.exe script.py
```
