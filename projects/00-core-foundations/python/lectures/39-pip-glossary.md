# pip Glossary

## Topic 39: Quick Reference Guide

---

## Glossary Terms

### D

#### Dependency
**Definition:** Package required by another package to function.
```bash
# requests depends on urllib3, etc.
pip install requests  # Installs dependencies too
```
**Related:** Requirements, sub-dependency

---

### F

#### Freeze
**Definition:** Command to output installed packages in requirements format.
```bash
pip freeze > requirements.txt
# Output: requests==2.28.0
```
**Related:** requirements.txt, version pinning

---

### I

#### Install
**Definition:** Add a package to Python environment.
```bash
pip install requests
```
**Related:** Uninstall, upgrade

---

### P

#### Package
**Definition:** Reusable Python module distributed via PyPI.
```bash
pip install package_name
```
**Related:** PyPI, module, library

#### PyPI (Python Package Index)
**Definition:** Official repository for Python packages.
```bash
# Visit https://pypi.org
pip install requests  # From PyPI
```
**Related:** Package, repository, index

---

### R

#### Requirements File
**Definition:** Text file listing packages and versions.
```text
# requirements.txt
requests==2.28.0
flask>=2.0.0
```
**Related:** `pip freeze`, `pip install -r`

---

### U

#### Uninstall
**Definition:** Remove a package from Python environment.
```bash
pip uninstall requests
```
**Related:** Install, remove

#### Upgrade
**Definition:** Update package to newer version.
```bash
pip install --upgrade requests
```
**Related:** Install, update

---

## Quick Reference Table

| Term | Command/Concept | Description |
|------|-----------------|-------------|
| **pip** | `pip` | Package installer |
| **PyPI** | pypi.org | Package repository |
| **install** | `pip install pkg` | Add package |
| **uninstall** | `pip uninstall pkg` | Remove package |
| **upgrade** | `pip install --upgrade pkg` | Update package |
| **freeze** | `pip freeze` | List packages |
| **list** | `pip list` | Show installed |
| **show** | `pip show pkg` | Package info |
| **requirements** | `requirements.txt` | Dependency file |
| **--user** | `pip install --user pkg` | User-level install |
| **-r** | `pip install -r file` | From requirements |
| **==** | `pkg==1.0` | Exact version |
| **>=** | `pkg>=1.0` | Minimum version |
| **~=** | `pkg~=1.0` | Compatible release |

---

## Common Commands

### Package Management
```bash
pip install requests              # Install
pip install requests==2.28.0      # Specific version
pip install --upgrade requests    # Upgrade
pip uninstall requests            # Remove
pip show requests                 # Info
```

### Listing
```bash
pip list                         # All packages
pip list --outdated              # Need update
pip freeze                       # For requirements
```

### Requirements
```bash
pip freeze > requirements.txt    # Create
pip install -r requirements.txt  # Install
```

---

## Version Specifiers

| Symbol | Name | Example | Meaning |
|--------|------|---------|---------|
| `==` | Exact | `==1.0` | Exactly this version |
| `>=` | Greater or equal | `>=1.0` | 1.0 or higher |
| `<=` | Less or equal | `<=2.0` | 2.0 or lower |
| `!=` | Not equal | `!=1.5` | Any except 1.5 |
| `~=` | Compatible | `~=1.4` | >=1.4, <2.0 |
| `===` | Arbitrary | `===1.0` | Exactly this string |

---

## Troubleshooting

### Permission Error
```bash
# Solution 1: Use --user
pip install --user requests

# Solution 2: Use virtual environment
python -m venv myenv
```

### Slow Download
```bash
# Use mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

### Version Conflict
```bash
# Check installed versions
pip list | grep package_name

# Force reinstall
pip install --force-reinstall requests
```
