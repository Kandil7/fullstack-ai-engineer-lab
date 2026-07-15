"""
Enum - Advanced Python Exercises
=================================
Enums provide a set of symbolic names bound to unique values.
They are useful for defining constants and states.
"""

from enum import Enum, auto, unique, IntEnum, Flag, IntFlag
from typing import Optional


# =============================================================================
# 1. Basic Enum
# =============================================================================

class Color(Enum):
    """Basic color enumeration."""
    RED = 1
    GREEN = 2
    BLUE = 3


class Direction(Enum):
    """Cardinal directions."""
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


# =============================================================================
# 2. Auto Values
# =============================================================================

class Status(Enum):
    """Status with auto-generated values."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class Priority(IntEnum):
    """Integer enum for comparison operations."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# =============================================================================
# 3. Functional API
# =============================================================================

Animal = Enum("Animal", ["CAT", "DOG", "BIRD", "FISH"])
Month = Enum("Month", {
    "JANUARY": 1, "FEBRUARY": 2, "MARCH": 3,
    "APRIL": 4, "MAY": 5, "JUNE": 6,
})


# =============================================================================
# 4. String Enum with Methods
# =============================================================================

class HttpStatus(Enum):
    """HTTP status codes with descriptions."""
    OK = (200, "Success")
    NOT_FOUND = (404, "Resource not found")
    UNAUTHORIZED = (401, "Authentication required")
    SERVER_ERROR = (500, "Internal server error")

    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    @classmethod
    def from_code(cls, code: int) -> Optional["HttpStatus"]:
        """Find status by code."""
        for status in cls:
            if status.code == code:
                return status
        return None

    def is_success(self) -> bool:
        return 200 <= self.code < 300

    def is_client_error(self) -> bool:
        return 400 <= self.code < 500


# =============================================================================
# 5. Flag Enums
# =============================================================================

class Permission(Flag):
    """File system permissions."""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ALL = READ | WRITE | EXECUTE


class LogLevel(IntFlag):
    """Logging levels that can be combined."""
    DEBUG = 1
    INFO = 2
    WARNING = 4
    ERROR = 8
    CRITICAL = 16
    STANDARD = INFO | WARNING | ERROR | CRITICAL


# =============================================================================
# 6. Enum with Methods
# =============================================================================

class HttpMethod(Enum):
    """HTTP methods with metadata."""
    GET = ("safe", True, False)
    POST = ("unsafe", False, True)
    PUT = ("unsafe", False, True)
    DELETE = ("unsafe", False, False)
    PATCH = ("unsafe", False, True)

    def __init__(self, safety: str, idempotent: bool, has_body: bool):
        self.safety = safety
        self.idempotent = idempotent
        self.has_body = has_body

    def description(self) -> str:
        return (
            f"{self.name}: {self.safety}, "
            f"{'idempotent' if self.idempotent else 'not idempotent'}, "
            f"{'has body' if self.has_body else 'no body'}"
        )


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ENUM DEMO")
    print("=" * 60)

    # 1. Basic enum
    print("\n--- Basic Enum ---")
    print(f"  Color.RED = {Color.RED}")
    print(f"  Color.RED.value = {Color.RED.value}")
    print(f"  Color.RED.name = {Color.RED.name}")
    print(f"  Direction.NORTH.value = {Direction.NORTH.value}")

    # 2. Iteration and membership
    print("\n--- Iteration ---")
    for color in Color:
        print(f"  {color.name} = {color.value}")

    print(f"  'RED' in Color.names: {'RED' in Color.__members__}")
    print(f"  Color(1) = {Color(1)}")

    # 3. Auto values
    print("\n--- Auto Values ---")
    for status in Status:
        print(f"  {status.name} = {status.value}")

    # 4. IntEnum comparison
    print("\n--- IntEnum Comparison ---")
    print(f"  Priority.HIGH > Priority.MEDIUM: {Priority.HIGH > Priority.MEDIUM}")
    print(f"  Priority.CRITICAL >= 4: {Priority.CRITICAL >= 4}")

    # 5. Functional API
    print("\n--- Functional API ---")
    print(f"  Animal.CAT = {Animal.CAT}")
    print(f"  Month.MARCH = {Month.MARCH.value}")

    # 6. String Enum with methods
    print("\n--- HTTP Status Enum ---")
    status = HttpStatus.from_code(404)
    print(f"  Status 404: {status.name} - {status.description}")
    print(f"  Is success: {status.is_success()}")
    print(f"  Is client error: {status.is_client_error()}")
    print(f"  HTTP 200 is success: {HttpStatus.OK.is_success()}")

    # 7. Flag enums
    print("\n--- Flag Enums ---")
    perm = Permission.READ | Permission.WRITE
    print(f"  READ | WRITE = {perm}")
    print(f"  Has READ: {Permission.READ in perm}")
    print(f"  Has EXECUTE: {Permission.EXECUTE in perm}")
    print(f"  ALL includes WRITE: {Permission.WRITE in Permission.ALL}")

    # 8. LogLevel combination
    print("\n--- Log Level Flags ---")
    print(f"  STANDARD = {LogLevel.STANDARD}")
    print(f"  DEBUG | ERROR = {LogLevel.DEBUG | LogLevel.ERROR}")

    # 9. HTTP Method metadata
    print("\n--- HTTP Methods ---")
    for method in HttpMethod:
        print(f"  {method.description()}")

    print("\n" + "=" * 60)
    print("All enum demos complete!")
    print("=" * 60)
