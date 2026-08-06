# Lecture 19: Logging

## Topic Overview

The `logging` module provides a flexible event logging system for applications. It allows you to track events during software execution, which is essential for debugging, monitoring, and auditing. Unlike print statements, logging provides severity levels, output routing, and formatting options.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Configure logging** with basic setup
2. **Use different log levels** appropriately
3. **Create custom formatters** for log output
4. **Add multiple handlers** (console, file, etc.)
5. **Understand logger hierarchy** and propagation
6. **Build application loggers** for production use
7. **Log exceptions** with traceback information

---

## Key Concepts

### 1. Basic Logging

Start logging with simple configuration.

```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

---

### 2. Logging Levels

Different levels indicate message severity.

```python
import logging

# Set level on logger
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log at different levels
logger.debug("Debug: Detailed information for diagnosing")
logger.info("Info: Confirmation that things are working")
logger.warning("Warning: Something unexpected happened")
logger.error("Error: The software failed to perform a function")
logger.critical("Critical: Program may be unable to continue")
```

#### Level Hierarchy

```
CRITICAL (40)
    ↓
ERROR (30)
    ↓
WARNING (20)
    ↓
INFO (10)
    ↓
DEBUG (0)
```

---

### 3. Custom Formatter

Create detailed log formats.

```python
import logging

logger = logging.getLogger("custom_format")
logger.setLevel(logging.DEBUG)

# Detailed format
detailed_formatter = logging.Formatter(
    fmt='%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

handler = logging.StreamHandler()
handler.setFormatter(detailed_formatter)
logger.addHandler(handler)

def my_function():
    logger.info("Inside my_function")
    logger.debug("Debugging my_function")

my_function()
```

#### Format Variables

| Variable | Description |
|----------|-------------|
| `%(asctime)s` | Time of log message |
| `%(name)s` | Logger name |
| `%(levelname)s` | Log level |
| `%(message)s` | Log message |
| `%(funcName)s` | Function name |
| `%(lineno)d` | Line number |
| `%(filename)s` | File name |

---

### 4. Multiple Handlers

Send logs to different destinations.

```python
import logging
import tempfile
import os

logger = logging.getLogger("multi_handler")
logger.setLevel(logging.DEBUG)

# Console handler (INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)

# File handler (DEBUG and above)
temp_file = tempfile.mktemp(suffix=".log")
file_handler = logging.FileHandler(temp_file)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# This goes to both console and file
logger.info("Info message - console and file")
logger.debug("Debug message - file only")

# Clean up
logger.removeHandler(console_handler)
logger.removeHandler(file_handler)
file_handler.close()
os.remove(temp_file)
```

---

### 5. Logger Hierarchy

Loggers form a hierarchy with parent-child relationships.

```python
import logging

# Parent logger
parent_logger = logging.getLogger("app")
parent_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(message)s'))
parent_logger.addHandler(handler)

# Child loggers
db_logger = logging.getLogger("app.database")
api_logger = logging.getLogger("app.api")

parent_logger.info("Parent message")
db_logger.info("Database message")  # Propagates to parent
api_logger.info("API message")  # Propagates to parent
```

#### Propagation

```python
import logging

# Disable propagation
child_logger = logging.getLogger("app.child")
child_logger.propagation = False
child_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
child_logger.addHandler(handler)

# Parent logger
parent_logger = logging.getLogger("app")

# This only goes to child's handler
child_logger.info("Child message - no propagation")
```

---

### 6. Application Logger

Build a reusable logger for applications.

```python
import logging
from typing import Optional

class ApplicationLogger:
    """Reusable application logger setup."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def _setup_handlers(self, log_file: Optional[str]):
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        self.logger.addHandler(console)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(file_handler)
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def error(self, msg: str, exc_info: bool = False):
        self.logger.error(msg, exc_info=exc_info)
    
    def debug(self, msg: str):
        self.logger.debug(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)

# Usage
app_log = ApplicationLogger("myapp", log_file="app.log")
app_log.info("Application started")
app_log.debug("Loading configuration")
app_log.warning("Configuration not found")
app_log.error("Failed to connect to database")
```

---

### 7. Exception Logging

Log exceptions with full traceback.

```python
import logging

logger = logging.getLogger("exception_demo")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)

def risky_operation():
    try:
        result = 1 / 0
    except Exception:
        logger.exception("Error in risky_operation")  # Includes traceback
        raise

try:
    risky_operation()
except Exception:
    pass
```

---

## Common Mistakes to Avoid

### 1. Using print Instead of logging

```python
# BAD
print("Starting process...")
print(f"Error: {e}")

# GOOD
logger.info("Starting process...")
logger.error(f"Error: {e}")
```

### 2. Not Configuring Logging

```python
# BAD - no output
logger = logging.getLogger("myapp")
logger.info("This won't appear")

# GOOD - configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")
logger.info("This will appear")
```

### 3. Adding Handlers Multiple Times

```python
# BAD - duplicate messages
def setup_logger():
    logger = logging.getLogger("myapp")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger

# GOOD - check for existing handlers
def setup_logger():
    logger = logging.getLogger("myapp")
    if not logger.handlers:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger
```

---

## Best Practices

### 1. Use Appropriate Levels

```python
logger.debug("Variable value: %s", variable)  # Development
logger.info("User logged in: %s", username)   # Normal operations
logger.warning("Disk space low: %s%%", space) # Potential issues
logger.error("Failed to send email: %s", e)   # Errors
logger.critical("Database connection lost")    # Critical failures
```

### 2. Use Lazy Formatting

```python
# BAD - string formatting even if log level disabled
logger.debug("User %s performed action %s" % (user, action))

# GOOD - lazy formatting
logger.debug("User %s performed action %s", user, action)
```

### 3. Include Context

```python
# BAD
logger.error("Error occurred")

# GOOD
logger.error("Failed to process order %s for user %s", order_id, user_id)
```

---

## Practice Exercises

### Exercise 1: Configure Logging
```python
"""
Configure logging with:
- Console handler (INFO level)
- File handler (DEBUG level)
- Custom format with timestamp
"""
# Your code here
```

### Exercise 2: Application Logger
```python
"""
Create an ApplicationLogger class that:
- Accepts app name and optional log file
- Prevents duplicate handlers
- Provides info(), error(), debug() methods
"""
# Your code here
```

### Exercise 3: Exception Logger
```python
"""
Create a decorator that:
- Catches exceptions
- Logs them with traceback
- Re-raises the exception
"""
# Your code here
```

---

## Summary

### Logging Levels

| Level | Value | When to Use |
|-------|-------|-------------|
| DEBUG | 10 | Detailed diagnostic information |
| INFO | 15 | General operational information |
| WARNING | 20 | Unexpected but recoverable |
| ERROR | 30 | Serious problem |
| CRITICAL | 50 | Program may not continue |

### Key Components

| Component | Purpose |
|-----------|---------|
| Logger | Interface for logging |
| Handler | Directs log output |
| Formatter | Formats log messages |
| Filter | Filters log messages |

### Key Takeaways

1. **Use appropriate log levels** for different situations
2. **Configure logging early** in application startup
3. **Use lazy formatting** for performance
4. **Include context** in log messages
5. **Log exceptions** with traceback
6. **Prevent duplicate handlers**

---

## Further Reading

- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
