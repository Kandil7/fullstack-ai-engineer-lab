"""
W3Schools Python Tutorial - 18: Python Match
=============================================
Topics: match statement, patterns, wildcards (Python 3.10+)

Run: python 18-match.py
Reference: https://www.w3schools.com/python/python_match.asp
"""

import sys

# ============================================================
# The match Statement (Python 3.10+)
# ============================================================
# The match statement is used for pattern matching.
# It's similar to switch/case in other languages but more powerful.

if sys.version_info < (3, 10):
    print("This script requires Python 3.10 or newer!")
    print(f"Current version: {sys.version}")
    sys.exit(0)

# ============================================================
# Basic match
# ============================================================
# Example 1: Simple value matching
day = "Monday"

match day:
    case "Monday":
        print("Start of the work week")
    case "Friday":
        print("Almost the weekend!")
    case "Saturday" | "Sunday":
        print("It's the weekend!")
    case _:
        print("Regular weekday")

# Output: Start of the work week

# ============================================================
# Matching with Conditions (Guards)
# ============================================================
# Example 2: Using guards for complex conditions
score = 85

match score:
    case s if s >= 90:
        grade = "A"
    case s if s >= 80:
        grade = "B"
    case s if s >= 70:
        grade = "C"
    case s if s >= 60:
        grade = "D"
    case _:
        grade = "F"

print(f"\nScore {score} = Grade {grade}")
# Output: Score 85 = Grade B

# ============================================================
# Matching Structures
# ============================================================
# Example 3: Matching with tuples
point = (1, 0)

match point:
    case (0, 0):
        print("\nPoint is at the origin")
    case (x, 0):
        print(f"Point is on the x-axis at x={x}")
    case (0, y):
        print(f"Point is on the y-axis at y={y}")
    case (x, y):
        print(f"Point is at ({x}, {y})")

# Output: Point is on the x-axis at x=1

# ============================================================
# Matching with Lists
# ============================================================
# Example 4: Pattern matching with lists
command = ["move", "right", "10"]

match command:
    case ["quit"]:
        print("\nQuitting...")
    case ["move", direction, steps]:
        print(f"Moving {steps} steps {direction}")
    case ["attack", target]:
        print(f"Attacking {target}")
    case _:
        print("Unknown command")

# Output: Moving 10 steps right

# ============================================================
# Matching with Dictionaries
# ============================================================
# Example 5: Pattern matching with dictionaries
user = {"name": "Alice", "role": "admin", "active": True}

match user:
    case {"role": "admin", "active": True}:
        print(f"\nWelcome, active admin {user['name']}!")
    case {"role": "admin", "active": False}:
        print(f"Admin {user['name']} is inactive")
    case {"role": "user"}:
        print(f"Regular user: {user['name']}")
    case _:
        print("Unknown user type")

# Output: Welcome, active admin Alice!

# ============================================================
# Matching with Classes
# ============================================================
# Example 6: Pattern matching with class instances
class Shape:
    pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

def describe_shape(shape):
    match shape:
        case Circle(radius=r):
            return f"Circle with radius {r}"
        case Rectangle(width=w, height=h):
            return f"Rectangle {w}x{h}"
        case Triangle(base=b, height=h):
            return f"Triangle with base {b} and height {h}"
        case _:
            return "Unknown shape"

shapes = [Circle(5), Rectangle(10, 20), Triangle(8, 12)]
print("\n--- Shapes ---")
for shape in shapes:
    print(f"  {describe_shape(shape)}")

# Output:
#   Circle with radius 5
#   Rectangle 10x20
#   Triangle with base 8 and height 12

# ============================================================
# Wildcard Pattern
# ============================================================
# Example 7: The _ wildcard catches everything
status_code = 404

match status_code:
    case 200:
        print(f"\n{status_code}: OK")
    case 301:
        print(f"{status_code}: Moved Permanently")
    case 404:
        print(f"{status_code}: Not Found")
    case 500:
        print(f"{status_code}: Internal Server Error")
    case code if 400 <= code < 500:
        print(f"{code}: Client Error")
    case code if 500 <= code < 600:
        print(f"{code}: Server Error")
    case _:
        print(f"{status_code}: Unknown status")

# Output: 404: Not Found

# ============================================================
# OR Patterns (|)
# ============================================================
# Example 8: Multiple patterns with |
http_method = "PUT"

match http_method:
    case "GET":
        print(f"\n{http_method}: Read resource")
    case "POST" | "PUT" | "PATCH":
        print(f"{http_method}: Create or update resource")
    case "DELETE":
        print(f"{http_method}: Delete resource")
    case _:
        print(f"{http_method}: Unknown method")

# Output: PUT: Create or update resource

# ============================================================
# Capture Patterns
# ============================================================
# Example 9: Capturing values
data = {"type": "error", "message": "Disk full", "code": 507}

match data:
    case {"type": "error", "message": msg, "code": code}:
        print(f"\nError {code}: {msg}")
    case {"type": "info", "message": msg}:
        print(f"Info: {msg}")
    case _:
        print("Unknown data format")

# Output: Error 507: Disk full

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. match statement: pattern matching (Python 3.10+)")
print("2. case value: match specific values")
print("3. case _: wildcard/catch-all pattern")
print("4. case p1 | p2: OR patterns")
print("5. case pattern if guard: conditional matching")
print("6. Can match tuples, lists, dicts, and classes")
print("7. More powerful than traditional switch/case")
