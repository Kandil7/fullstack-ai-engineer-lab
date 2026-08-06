"""
Logging - Advanced Python Exercises
====================================
The logging module provides flexible event logging for applications
with configurable levels, handlers, and formatters.
"""

import logging
import sys
from typing import Optional
from datetime import datetime


# =============================================================================
# 1. Basic Logging
# =============================================================================

def demo_basic_logging():
    """Demonstrate basic logging setup."""
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


# =============================================================================
# 2. Logging Levels
# =============================================================================

def demo_logging_levels():
    """Demonstrate different logging levels."""
    logger = logging.getLogger("levels_demo")
    logger.setLevel(logging.DEBUG)

    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(levelname)-8s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Log at different levels
    logger.debug("Debug: Detailed information for diagnosing")
    logger.info("Info: Confirmation that things are working")
    logger.warning("Warning: Something unexpected happened")
    logger.error("Error: The software failed to perform a function")
    logger.critical("Critical: Program may be unable to continue")

    logger.removeHandler(handler)


# =============================================================================
# 3. Custom Formatter
# =============================================================================

def demo_custom_formatter():
    """Demonstrate custom log formatting."""
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
    logger.removeHandler(handler)


# =============================================================================
# 4. Multiple Handlers
# =============================================================================

def demo_multiple_handlers():
    """Demonstrate using multiple handlers."""
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


# =============================================================================
# 5. Logger Hierarchy
# =============================================================================

def demo_logger_hierarchy():
    """Demonstrate logger hierarchy and propagation."""
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
    db_logger.info("Database message")
    api_logger.info("API message")

    parent_logger.removeHandler(handler)


# =============================================================================
# 6. Practical Application Logger
# =============================================================================

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


def demo_application_logger():
    """Demonstrate practical application logging."""
    import tempfile

    temp_file = tempfile.mktemp(suffix=".log")
    app_log = ApplicationLogger("myapp", log_file=temp_file)

    app_log.info("Application started")
    app_log.debug("Loading configuration")
    app_log.warning("Configuration file not found, using defaults")
    app_log.error("Failed to connect to database")

    try:
        1 / 0
    except Exception as e:
        app_log.error(f"Exception occurred: {e}", exc_info=True)

    app_log.info("Application finished")

    # Clean up - close handlers BEFORE removing the file.
    # On Windows an open FileHandler holds the file open (WinError 32).
    # Iterate over a copy: removeHandler mutates the list while iterating.
    for h in list(app_log.logger.handlers):
        h.close()
        app_log.logger.removeHandler(h)

    import os
    if os.path.exists(temp_file):
        os.remove(temp_file)


# =============================================================================
# 7. Exception Logging
# =============================================================================

def demo_exception_logging():
    """Demonstrate logging exceptions with traceback."""
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

    logger.removeHandler(handler)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LOGGING DEMO")
    print("=" * 60)

    # Reset logging for clean demo
    logging.root.handlers.clear()

    print("\n--- Basic Logging ---")
    demo_basic_logging()

    print("\n--- Logging Levels ---")
    logging.root.handlers.clear()
    demo_logging_levels()

    print("\n--- Custom Formatter ---")
    logging.root.handlers.clear()
    demo_custom_formatter()

    print("\n--- Multiple Handlers ---")
    logging.root.handlers.clear()
    demo_multiple_handlers()

    print("\n--- Logger Hierarchy ---")
    logging.root.handlers.clear()
    demo_logger_hierarchy()

    print("\n--- Application Logger ---")
    logging.root.handlers.clear()
    demo_application_logger()

    print("\n--- Exception Logging ---")
    logging.root.handlers.clear()
    demo_exception_logging()

    print("\n" + "=" * 60)
    print("All logging demos complete!")
    print("=" * 60)
