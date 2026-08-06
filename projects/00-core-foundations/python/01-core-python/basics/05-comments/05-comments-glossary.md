# Python Comments - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Comment | Syntax | Text ignored by Python interpreter |
| Docstring | Documentation | String literal as first statement in module/class/function |
| PEP 257 | Standard | Python docstring conventions |
| PEP 8 | Standard | Python style guide (includes comment rules) |
| Module Docstring | Documentation | Documentation for entire module |
| Class Docstring | Documentation | Documentation for class |
| Function Docstring | Documentation | Documentation for function |
| Inline Comment | Comment | Comment on same line as code |
| Block Comment | Comment | Group of comment lines explaining code |
| Documentation | Concept | Human-readable explanation of code |

## Detailed Definitions

### B

**Block Comment**
- **Definition**: Group of comment lines explaining a code section
- **Example**: Multiple `#` lines before a function
- **Related terms**: Inline Comment, Documentation, PEP 8
```python
# Block comment explaining the function
# This function processes user data
# It validates input and returns cleaned data
def process_user_data(data):
    pass
```

### D

**Docstring**
- **Definition**: String literal as first statement in module/class/function
- **Example**: `"""Greet a person."""`
- **Related terms**: Documentation, PEP 257, Help System
```python
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}!"

# Access docstring
print(greet.__doc__)  # Greet a person by name.
help(greet)  # Shows formatted documentation
```

**Docstring Convention**
- **Definition**: Standardized format for writing docstrings
- **Example**: Summary line, blank line, extended description
- **Related terms**: PEP 257, Google Style, NumPy Style
```python
def function(param1, param2):
    """
    Summary line.
    
    Extended description.
    
    Args:
        param1: Description.
        param2: Description.
    
    Returns:
        Description of return value.
    
    Raises:
        ValueError: When error occurs.
    """
    pass
```

### I

**Inline Comment**
- **Definition**: Comment on same line as code
- **Example**: `x = 10  # Initial value`
- **Related terms**: Block Comment, PEP 8, Spacing
```python
# Inline comments (2+ spaces before #)
x = 10  # Initial value
y = 20  # Default multiplier
```

### M

**Module Docstring**
- **Definition**: Documentation for entire Python module
- **Example**: First statement in `.py` file
- **Related terms**: Docstring, Module, Documentation
```python
"""
calculator.py - A simple calculator module.

This module provides basic arithmetic operations.
"""

def add(a, b):
    """Return sum of a and b."""
    return a + b
```

### P

**PEP (Python Enhancement Proposal)**
- **Definition**: Design documents for Python improvements
- **Example**: PEP 8, PEP 257
- **Related terms**: Standard, Convention, RFC
- **Website**: https://peps.python.org

**PEP 8**
- **Definition**: Official Python style guide
- **Example**: Comment formatting rules
- **Related terms**: Style Guide, Convention, Readability
```python
# PEP 8 comment rules
# - Block comments: # followed by space
# - Inline comments: 2+ spaces before #
# - Don't use docstrings for non-public code
```

**PEP 257**
- **Definition**: Python docstring conventions
- **Example**: Docstring format and content guidelines
- **Related terms**: Docstring, Documentation, Convention
```python
# PEP 257 recommendations
# - Use triple double quotes
# - One-line docstrings for simple functions
# - Multi-line docstrings for complex functions
# - Include summary, description, args, returns
```

### R

**Readability**
- **Definition**: How easy code is to understand
- **Example**: Clear comments, meaningful names
- **Related terms**: Documentation, PEP 8, Maintenance
```python
# Good readability
def calculate_average(numbers):
    """Calculate arithmetic mean of numbers."""
    if not numbers:
        raise ValueError("Empty list")
    return sum(numbers) / len(numbers)
```

### W

**Why vs What**
- **Definition**: Principle that comments should explain why, not what
- **Example**: Explain reasoning, not code mechanics
- **Related terms**: Documentation, Best Practices
```python
# Bad - explains what
x = x + 1  # Increment x

# Good - explains why
x = x + 1  # Offset for 1-based indexing
```

## Key Concepts Summary

### Comment Types
| Type | Syntax | Use Case |
|------|--------|----------|
| Single-line | `# comment` | Quick notes |
| Multi-line | `# line1\n# line2` | Longer explanations |
| Docstring | `"""..."""` | Official documentation |
| Inline | `code  # comment` | Brief clarifications |

### Docstring Formats
| Format | Style | Example |
|--------|-------|---------|
| Google | Google Style | `Args:`, `Returns:` |
| NumPy | NumPy Style | `Parameters\n----------` |
| Sphinx | Sphinx Style | `:param name:`, `:returns:` |
| reST | reStructuredText | Standard Python docs |

### When to Comment
| Good | Bad |
|------|-----|
| Explain why | Explain what |
| Document algorithms | Restate code |
| Note workarounds | Comment obvious code |
| Clarify business rules | Leave outdated comments |

### Documentation Hierarchy
1. **Module docstring**: Overall module purpose
2. **Class docstring**: Class description and usage
3. **Function docstring**: Function behavior and parameters
4. **Inline comments**: Brief clarifications

## Practice Terms

Match these terms to their definitions:
1. Docstring - ?
2. PEP 257 - ?
3. Block comment - ?
4. Inline comment - ?
5. Why vs What - ?

**Answers:**
1. String literal as first statement in module/class/function
2. Python docstring conventions
3. Group of comment lines explaining code
4. Comment on same line as code
5. Principle that comments should explain why, not what