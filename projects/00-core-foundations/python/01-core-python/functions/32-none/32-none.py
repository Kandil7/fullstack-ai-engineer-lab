"""
W3Schools Python Tutorial - 32: Python None
============================================
Topics: None value, checking for None, None in functions

Run: python 32-none.py
Reference: https://www.w3schools.com/python/python_ref_none.asp
"""

# ============================================================
# What is None?
# ============================================================
# None is a special constant in Python that represents the absence
# of a value or a null value. It's an object of its own type (NoneType).

# Example 1: Basic None
print("--- None Basics ---")

x = None
print(f"x = {x}")
print(f"type(x) = {type(x)}")
print(f"x is None: {x is None}")
print(f"x is not None: {x is not None}")

# Output:
# x = None
# type(x) = <class 'NoneType'>
# x is None: True
# x is not None: False

# ============================================================
# Checking for None
# ============================================================
# Example 2: Different ways to check for None
print("\n--- Checking for None ---")

value = None

# Using 'is' (recommended)
if value is None:
    print("value is None (using is)")

# Using 'is not'
if value is not None:
    print("This won't print")
else:
    print("value is not not None (double negative)")

# Using == (works but not recommended)
if value == None:
    print("value == None (using ==)")

# ⚠️ Use 'is' instead of '==' for None comparison!
# 'is' checks identity (same object), '==' checks equality
# For None, both work, but 'is' is the Pythonic way.

# ============================================================
# None in Boolean Context
# ============================================================
# Example 3: None is falsy
print("\n--- None in Boolean Context ---")

x = None
print(f"bool(None) = {bool(None)}")       # False
print(f"if None: {bool(None)}")            # False

# None vs False vs 0 vs "" vs []
print(f"None is falsy: {not None}")
print(f"False is falsy: {not False}")
print(f"0 is falsy: {not 0}")
print(f"'' is falsy: {not ''}")
print(f"[] is falsy: {not []}")

# All of these are falsy, but they're different!
print(f"\nNone == False: {None == False}")  # False
print(f"None == 0: {None == 0}")           # False
print(f"None == '': {None == ''}")         # False

# ============================================================
# None as Default Parameter
# ============================================================
# Example 4: Using None as default
print("\n--- None as Default ---")

def greet(name=None):
    if name is None:
        return "Hello, Stranger!"
    return f"Hello, {name}!"

print(greet())         # Hello, Stranger!
print(greet("Alice"))  # Hello, Alice!

# ⚠️ Common mistake: mutable default arguments
# WRONG:
def append_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - OOPS! Same list!

# CORRECT:
def append_to_list_fixed(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list

print(append_to_list_fixed(1))  # [1]
print(append_to_list_fixed(2))  # [2] - Correct!

# ============================================================
# None in Functions
# ============================================================
# Example 5: Functions returning None
print("\n--- None in Functions ---")

# Functions without return statement return None
def say_hello():
    print("Hello!")

result = say_hello()
print(f"Return value: {result}")
print(f"Is None: {result is None}")

# print() function returns None
result = print("This prints but returns None")
print(f"print() returns: {result}")

# append() returns None
my_list = [1, 2, 3]
result = my_list.append(4)
print(f"append() returns: {result}")
print(f"List: {my_list}")

# ============================================================
# Optional Values Pattern
# ============================================================
# Example 6: Using None for optional values
print("\n--- Optional Values Pattern ---")

def create_user(name, email, phone=None):
    """Create a user with optional phone number."""
    user = {"name": name, "email": email}
    if phone is not None:
        user["phone"] = phone
    return user

user1 = create_user("Alice", "alice@example.com", "555-0123")
user2 = create_user("Bob", "bob@example.com")

print(f"User 1: {user1}")
print(f"User 2: {user2}")

# Output:
# User 1: {'name': 'Alice', 'email': 'alice@example.com', 'phone': '555-0123'}
# User 2: {'name': 'Bob', 'email': 'bob@example.com'}

# ============================================================
# None in Data Structures
# ============================================================
# Example 7: None in lists and dictionaries
print("\n--- None in Data Structures ---")

# None in list
data = [1, 2, None, 4, None, 6]
print(f"Original: {data}")

# Filter out None values
filtered = [x for x in data if x is not None]
print(f"Filtered: {filtered}")

# Count None values
none_count = data.count(None)
print(f"None count: {none_count}")

# None in dictionary
user = {"name": "Alice", "email": None, "phone": "555-0123"}
print(f"User: {user}")

# Check for None values
for key, value in user.items():
    if value is None:
        print(f"  {key}: (not provided)")
    else:
        print(f"  {key}: {value}")

# ============================================================
# None vs Empty Values
# ============================================================
# Example 8: None vs empty
print("\n--- None vs Empty ---")

empty_string = ""
empty_list = []
empty_dict = {}
none_value = None

print(f"empty_string: {bool(empty_string)}")    # False
print(f"empty_list: {bool(empty_list)}")        # False
print(f"empty_dict: {bool(empty_dict)}")        # False
print(f"none_value: {bool(none_value)}")        # False

# But they're different!
print(f"\nempty_string is None: {empty_string is None}")  # False
print(f"empty_list is None: {empty_list is None}")        # False
print(f"empty_dict is None: {empty_dict is None}")        # False

# None means "no value", empty means "value exists but is empty"

# ============================================================
# Practical Examples
# ============================================================
# Example 9: Real-world None usage
print("\n--- Practical Examples ---")

# Find function
def find_first(numbers, target):
    """Find first occurrence of target, return None if not found."""
    for num in numbers:
        if num == target:
            return num
    return None

result = find_first([1, 2, 3, 4, 5], 3)
print(f"Found 3: {result}")

result = find_first([1, 2, 3, 4, 5], 6)
print(f"Found 6: {result}")

# Dictionary get with None
config = {"host": "localhost", "port": 5432}
debug_mode = config.get("debug")  # Returns None if key doesn't exist
print(f"Debug mode: {debug_mode}")

# Chain of operations
def get_user_email(user):
    """Safely get user email."""
    if user is None:
        return None
    return user.get("email")

user = {"name": "Alice", "email": "alice@example.com"}
email = get_user_email(user)
print(f"Email: {email}")

email = get_user_email(None)
print(f"Email (None user): {email}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. None represents absence of value (null)")
print("2. Use 'is None' or 'is not None' to check (not '==')")
print("3. None is falsy in boolean context")
print("4. Functions return None if no explicit return")
print("5. Use None as default parameter (not mutable objects!)")
print("6. None != empty: None means no value, '' means empty string")
print("7. Common pattern: return None for 'not found'")
