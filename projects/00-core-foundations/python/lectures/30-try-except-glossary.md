# Exception Handling Glossary

## Topic 30: Quick Reference Guide

---

## Glossary Terms

### A

#### AttributeError
**Definition:** Raised when an attribute reference or assignment fails.
```python
class MyClass:
    pass

obj = MyClass()
print(obj.nonexistent)  # AttributeError: 'MyClass' has no attribute 'nonexistent'
```
**Related:** `AttributeError`, object attributes, dot notation

---

### B

#### Bare Except
**Definition:** An except clause without specifying an exception type (catches everything).
```python
# BAD PRACTICE - don't do this
try:
    risky_operation()
except:
    print("Error")
```
**Related:** `except Exception`, exception handling best practices

---

### C

#### Catching Exceptions
**Definition:** Using try/except blocks to handle runtime errors gracefully.
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```
**Related:** try/except, exception handling, error handling

#### Context Manager
**Definition:** Object that manages resources with `with` statement (auto-cleanup).
```python
with open("file.txt") as f:
    content = f.read()
# File automatically closed
```
**Related:** `__enter__`, `__exit__`, `with` statement

---

### E

#### Else Clause
**Definition:** Block that executes only if no exception occurred in try block.
```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error!")
else:
    print(f"Success: {result}")
```
**Related:** try/except/else, conditional execution

#### Exception
**Definition:** Base class for most built-in exceptions; runtime error that can be caught.
```python
try:
    risky_operation()
except Exception as e:
    print(f"Caught: {e}")
```
**Related:** BaseException, exception hierarchy, error handling

#### Exception Chaining
**Definition:** Linking exceptions using `raise ... from ...` to preserve original error.
```python
try:
    open("file.txt")
except FileNotFoundError as e:
    raise AppError("Failed") from e
```
**Related:** `__cause__`, `__context__`, `from` keyword

#### Exception Hierarchy
**Definition:** Tree structure of exception classes (BaseException → Exception → ...).
```python
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception
#       ├── ValueError
#       ├── TypeError
#       └── ...
```
**Related:** Inheritance, exception classes, BaseException

---

### F

#### Finally Clause
**Definition:** Block that always executes, whether exception occurred or not.
```python
try:
    f = open("file.txt")
except FileNotFoundError:
    print("Not found")
finally:
    print("Always runs")  # Cleanup code
```
**Related:** Cleanup, resource management, try/finally

---

### I

#### ImportError
**Definition:** Raised when an import statement fails.
```python
import nonexistent_module  # ImportError
```
**Related:** Modules, imports, ModuleNotFoundError

#### IndexError
**Definition:** Raised when sequence index is out of range.
```python
my_list = [1, 2, 3]
print(my_list[10])  # IndexError: list index out of range
```
**Related:** Lists, sequences, indexing

#### Internal Error
**Definition:** Internal Python interpreter error (rarely seen by users).
```python
# Usually indicates a bug in Python itself
```
**Related:** Interpreter errors, CPython bugs

---

### K

#### KeyError
**Definition:** Raised when dictionary key is not found.
```python
my_dict = {"a": 1, "b": 2}
print(my_dict["c"])  # KeyError: 'c'
```
**Related:** Dictionaries, key lookup, `.get()` method

---

### L

#### Lookahead
**Definition:** Asserts what follows matches without consuming text (not exception-related, but used in patterns).
```python
import re
re.findall(r'\d+(?=px)', '10px 20em')  # ['10']
```
**Related:** Regex assertions, lookbehind

---

### M

#### ModuleNotFoundError
**Definition:** Raised when a module cannot be found (subclass of ImportError).
```python
import nonexistent  # ModuleNotFoundError
```
**Related:** ImportError, modules, packages

---

### N

#### NameError
**Definition:** Raised when a name is not defined in current scope.
```python
print(undefined_variable)  # NameError: name 'undefined_variable' is not defined
```
**Related:** Variables, scope, `global`, `local`

---

### O

#### OSError
**Definition:** Raised for system-related errors (I/O, file operations, etc.).
```python
open("/nonexistent/path")  # OSError
```
**Related:** File handling, I/O operations, system errors

---

### P

#### Pass
**Definition:** Statement that does nothing; often used to ignore exceptions.
```python
try:
    risky_operation()
except Exception:
    pass  # Silently ignores error (bad practice)
```
**Related:** Exception handling, code structure, `...`

#### PermissionError
**Definition:** Raised when trying to access file without proper permissions.
```python
open("/root/file.txt")  # PermissionError (if not root)
```
**Related:** File permissions, access control, OSError

---

### R

#### Raise
**Definition:** Statement to explicitly throw an exception.
```python
def validate(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age
```
**Related:** Exception raising, custom exceptions, `raise from`

#### Re-raising
**Definition:** Re-throwing the current exception to propagate it up the call stack.
```python
try:
    risky_operation()
except SomeError:
    log_error()
    raise  # Re-raises SameError
```
**Related:** Exception propagation, `raise` statement

#### RuntimeError
**Definition:** Generic runtime error not covered by other exception types.
```python
# Often used for conditions detected during runtime
```
**Related:** Exception types, generic exceptions

---

### S

#### SyntaxError
**Definition:** Raised when Python parser encounters syntax error.
```python
if True print("Hello")  # SyntaxError
```
**Related:** Parser, code syntax, compile-time errors

---

### T

#### Try/Except
**Definition:** Block structure for handling exceptions in Python.
```python
try:
    # Risky code
except ExceptionType:
    # Handle error
```
**Related:** Exception handling, error handling, try/except/else/finally

#### TypeError
**Definition:** Raised when operation or function receives wrong type.
```python
"hello" + 5  # TypeError: can only concatenate str to str
```
**Related:** Type checking, type conversion, duck typing

---

### V

#### ValueError
**Definition:** Raised when function receives right type but wrong value.
```python
int("abc")  # ValueError: invalid literal for int()
```
**Related:** Type conversion, input validation, value checking

---

### W

#### Warning
**Definition:** Non-fatal issue signaled to user (not an exception).
```python
import warnings
warnings.warn("Deprecated", DeprecationWarning)
```
**Related:** Deprecation, `warnings` module, non-fatal errors

---

## Quick Reference Table

| Term | Category | Description |
|------|----------|-------------|
| **AttributeError** | Exception | Invalid attribute reference |
| **Bare except** | Pattern | `except:` without exception type |
| **Catch** | Action | Handle an exception |
| **Context Manager** | Pattern | Auto-cleanup with `with` |
| **Custom Exception** | Pattern | User-defined exception class |
| **else** | Clause | Runs on no exception |
| **Exception** | Class | Base exception class |
| **Exception Chaining** | Feature | Link exceptions with `from` |
| **Exception Hierarchy** | Concept | Exception class tree |
| **finally** | Clause | Always executes |
| **ImportError** | Exception | Module import failure |
| **IndexError** | Exception | Index out of range |
| **KeyError** | Exception | Dictionary key not found |
| **ModuleNotFoundError** | Exception | Module not found |
| **NameError** | Exception | Undefined variable |
| **OSError** | Exception | System/I/O error |
| **PermissionError** | Exception | Insufficient permissions |
| **raise** | Statement | Throw exception |
| **Re-raising** | Pattern | Propagate exception |
| **SyntaxError** | Exception | Invalid syntax |
| **Try/Except** | Structure | Exception handling block |
| **TypeError** | Exception | Wrong type received |
| **ValueError** | Exception | Wrong value received |
| **Warning** | Signal | Non-fatal issue |

---

## Exception Patterns

### Pattern 1: Specific Handling
```python
try:
    risky_operation()
except SpecificError as e:
    handle_specific(e)
except AnotherError as e:
    handle_another(e)
```

### Pattern 2: Cleanup
```python
resource = acquire()
try:
    use(resource)
finally:
    release(resource)
```

### Pattern 3: Custom Exception
```python
class AppError(Exception):
    def __init__(self, message, code):
        self.code = code
        super().__init__(message)
```

### Pattern 4: Re-raise with Context
```python
try:
    low_level_operation()
except LowLevelError as e:
    raise HighLevelError("Failed") from e
```
