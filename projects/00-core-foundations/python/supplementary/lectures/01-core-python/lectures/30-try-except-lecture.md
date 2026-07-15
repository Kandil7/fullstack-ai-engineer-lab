# Exception Handling with Try/Except in Python

## Topic 30: Handling Errors Gracefully

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what exceptions are and why they occur
2. Use try/except blocks to handle errors
3. Catch specific exceptions vs. general exceptions
4. Use else and finally clauses
5. Create and raise custom exceptions
6. Implement proper error handling strategies

---

## 1. What Are Exceptions?

Exceptions are **runtime errors** that occur during program execution. Without proper handling, they crash your program.

### Types of Errors

```python
# Syntax Error - caught before execution
if True print("Hello")  # SyntaxError: invalid syntax

# Runtime Exception - occurs during execution
result = 10 / 0           # ZeroDivisionError
print(undefined_var)      # NameError
my_list = [1, 2, 3]
print(my_list[10])        # IndexError
```

### Common Built-in Exceptions

| Exception | Description |
|-----------|-------------|
| `ValueError` | Wrong value type |
| `TypeError` | Wrong argument type |
| `IndexError` | Index out of range |
| `KeyError` | Dictionary key not found |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Division by zero |
| `AttributeError` | Invalid attribute reference |
| `ImportError` | Module import fails |
| `StopIteration` | Iterator exhausted |

---

## 2. Basic Try/Except

### Syntax

```python
try:
    # Code that might raise an exception
    risky_code()
except ExceptionType:
    # Code to handle the exception
    handle_error()
```

### Simple Example

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Output: Cannot divide by zero!
# Program continues running
```

### Handling Multiple Exceptions

```python
try:
    num = int(input("Enter a number: "))
    result = 10 / num
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Different messages for different errors
```

---

## 3. Exception Information

### Accessing Error Details

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print(f"Error args: {e.args}")

# Output:
# Error type: ZeroDivisionError
# Error message: division by zero
# Error args: ('division by zero',)
```

### Using sys.exc_info()

```python
import sys

try:
    result = 10 / 0
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"Type: {exc_type}")
    print(f"Value: {exc_value}")
    print(f"Traceback: {exc_traceback}")
```

---

## 4. Catching Multiple Exceptions

### Multiple Except Blocks

```python
try:
    # Risky operations
    value = int(input("Enter number: "))
    result = 100 / value
    my_list = [1, 2, 3]
    print(my_list[10])
except ValueError:
    print("Invalid input - not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except IndexError:
    print("Index out of range")
```

### Combined Exception Handling

```python
try:
    value = int(input("Enter number: "))
    result = 100 / value
except (ValueError, ZeroDivisionError) as e:
    print(f"Input error: {e}")
    # Handles both ValueError and ZeroDivisionError the same way
```

### Catching All Exceptions (Not Recommended)

```python
try:
    risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
    # Catches almost all exceptions
```

---

## 5. Else and Finally

### The `else` Clause

Runs if **no exception** occurred in the try block.

```python
try:
    num = int(input("Enter a number: "))
    result = 100 / num
except ValueError:
    print("Invalid input!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
else:
    # Only runs if no exception
    print(f"Result: {result}")
    print("Calculation successful!")
```

### The `finally` Clause

**Always runs**, whether exception occurred or not. Used for cleanup.

```python
file = None
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    # Always executes
    if file:
        file.close()
        print("File closed.")
```

### Complete Try/Except/Else/Finally

```python
try:
    print("Attempting operation...")
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero!")
else:
    print(f"Success! Result = {result}")
finally:
    print("Cleanup complete.")

# Output:
# Attempting operation...
# Success! Result = 5.0
# Cleanup complete.
```

---

## 6. Raising Exceptions

### Using `raise`

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

try:
    result = divide(10, 0)
except ZeroDivisionError as e:
    print(e)  # Cannot divide by zero!
```

### Re-raising Exceptions

```python
try:
    risky_operation()
except SomeError:
    print("Logging error...")
    raise  # Re-raises the same exception
```

### Raising Different Exceptions

```python
def process_age(age):
    try:
        age = int(age)
    except ValueError:
        raise ValueError("Age must be a number") from None
    
    if age < 0 or age > 150:
        raise ValueError(f"Invalid age: {age}")
    
    return age
```

---

## 7. Custom Exceptions

### Creating Exception Classes

```python
class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds."""
    
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        message = f"Cannot withdraw ${amount}. Balance: ${balance}"
        super().__init__(message)

class InvalidEmailError(Exception):
    """Raised when email format is invalid."""
    pass

# Using custom exceptions
def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    new_balance = withdraw(100, 150)
except InsufficientFundsError as e:
    print(e)  # Cannot withdraw $150. Balance: $100
```

### Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for application."""
    pass

class ValidationError(AppError):
    """Validation specific errors."""
    pass

class DatabaseError(AppError):
    """Database related errors."""
    pass

class ConnectionError(DatabaseError):
    """Connection failures."""
    pass
```

---

## 8. Exception Chaining

### Using `from` Keyword

```python
class DatabaseError(Exception):
    pass

def connect_db():
    try:
        import psycopg2
        return psycopg2.connect("dbname=test")
    except ImportError as e:
        raise DatabaseError("Database driver not installed") from e

try:
    connect_db()
except DatabaseError as e:
    print(f"Error: {e}")
    print(f"Original cause: {e.__cause__}")
```

---

## 9. Context Managers and Exceptions

### Using `with` Statement

```python
# File handling with automatic cleanup
try:
    with open("data.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found!")
# File automatically closed even if exception occurs
```

### Custom Context Manager

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Acquiring resource")
    try:
        yield "resource"
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        print("Releasing resource")

with managed_resource() as res:
    print(f"Using {res}")
```

---

## 10. Common Mistakes to Avoid

### 1. Bare Except

```python
# BAD - catches everything including KeyboardInterrupt
try:
    risky_operation()
except:
    print("Error occurred")

# GOOD - catch specific exceptions
try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")
```

### 2. Catching Too Broadly

```python
# BAD - hides specific errors
try:
    result = complex_operation()
except Exception:
    log_error()

# GOOD - handle specific cases
try:
    result = complex_operation()
except ValueError as e:
    handle_value_error(e)
except TypeError as e:
    handle_type_error(e)
```

### 3. Swallowing Exceptions

```python
# BAD - silent failure
try:
    important_operation()
except Exception:
    pass

# GOOD - at least log it
try:
    important_operation()
except Exception as e:
    logging.error(f"Operation failed: {e}")
```

### 4. Not Using Finally for Cleanup

```python
# BAD - resource may leak
try:
    file = open("data.txt")
    process(file)
except Error:
    handle_error()

# GOOD - use finally
file = None
try:
    file = open("data.txt")
    process(file)
except Error:
    handle_error()
finally:
    if file:
        file.close()
```

---

## 11. Best Practices

1. **Be specific** - Catch the most specific exception possible
2. **Use finally** for cleanup code that must run
3. **Use else** for code that should run only on success
4. **Don't catch and ignore** - At least log the error
5. **Create custom exceptions** for your application domain
6. **Use context managers** (`with` statements) for resource management
7. **Include helpful error messages** when raising exceptions
8. **Document exceptions** in docstrings

---

## 12. Practice Exercises

### Exercise 1: Safe Division Calculator

```python
def safe_divide(a, b):
    """Divide a by b with error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Division by zero"
    except TypeError:
        return "Error: Invalid types"
    else:
        return result

# Test
print(safe_divide(10, 2))      # 5.0
print(safe_divide(10, 0))      # Error: Division by zero
print(safe_divide("10", 2))    # Error: Invalid types
```

### Exercise 2: Safe File Reader

```python
def safe_read_file(filename):
    """Read file contents safely."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return f"Error: {filename} not found"
    except PermissionError:
        return f"Error: No permission to read {filename}"
    except Exception as e:
        return f"Error: {e}"
    else:
        return content

# Test
print(safe_read_file("existing.txt"))
print(safe_read_file("nonexistent.txt"))
```

### Exercise 3: Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base application exception."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} {resource_id} not found")

def validate_user(data):
    if 'email' not in data:
        raise ValidationError('email', 'Required')
    if '@' not in data.get('email', ''):
        raise ValidationError('email', 'Invalid format')
    return True

try:
    validate_user({})
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## 13. Summary

| Concept | Key Points |
|---------|------------|
| **try/except** | Catch and handle exceptions |
| **Specific exceptions** | Catch what you expect |
| **else** | Code that runs on success |
| **finally** | Cleanup code that always runs |
| **raise** | Explicitly raise exceptions |
| **Custom exceptions** | Domain-specific error types |
| **Exception chaining** | Link related exceptions |
| **Context managers** | Automatic resource cleanup |

---

## Next Steps

- Learn about logging for production error handling
- Explore exception handling in async code
- Study exception handling patterns in frameworks
