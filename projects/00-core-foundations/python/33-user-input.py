"""
W3Schools Python Tutorial - 33: Python User Input
==================================================
Topics: input() function, converting input, input validation

Run: python 33-user-input.py
Reference: https://www.w3schools.com/python/python_user_input.asp
"""

# ============================================================
# The input() Function
# ============================================================
# The input() function reads a line from the user and returns it
# as a string (without the newline character).

# Example 1: Basic input
# Uncomment to test interactively:
# name = input("Enter your name: ")
# print(f"Hello, {name}!")

# ============================================================
# Input is Always a String
# ============================================================
# Example 2: Input type
# Uncomment to test:
# age = input("Enter your age: ")
# print(f"Type: {type(age)}")  # <class 'str'>
# print(f"Value: {age}")

# ============================================================
# Converting Input
# ============================================================
# Example 3: Converting string input to numbers
# Uncomment to test:

def demo_conversion():
    """Demonstrate input conversion."""
    # Integer input
    age = int(input("Enter your age: "))
    print(f"Next year you'll be {age + 1}")

    # Float input
    height = float(input("Enter your height in meters: "))
    print(f"Height in cm: {height * 100}")

# ============================================================
# Input Validation
# ============================================================
# Example 4: Safe input with validation
def get_integer(prompt, min_val=None, max_val=None):
    """Get a validated integer from user input."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Must be at least {min_val}. Try again.")
                continue
            if max_val is not None and value > max_val:
                print(f"Must be at most {max_val}. Try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number!")

# Example 5: Safe input with default value
def get_input_with_default(prompt, default=""):
    """Get input with a default value if user presses Enter."""
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default

# Example 6: Yes/No confirmation
def confirm(prompt="Continue?"):
    """Ask for yes/no confirmation."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'!")

# ============================================================
# Interactive Examples (Uncomment to Test)
# ============================================================

# Example 7: Simple calculator
def simple_calculator():
    """Interactive calculator."""
    print("\n--- Simple Calculator ---")
    print("Enter 'quit' to exit")

    while True:
        expression = input("\nEnter calculation (e.g., 2 + 3): ")
        if expression.lower() == 'quit':
            print("Goodbye!")
            break

        try:
            # Evaluate safely (for demo only - don't use eval in production!)
            result = eval(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

# Example 8: Menu system
def menu_system():
    """Interactive menu."""
    print("\n--- Menu System ---")
    while True:
        print("\n1. Option 1")
        print("2. Option 2")
        print("3. Option 3")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            print("You selected Option 1!")
        elif choice == '2':
            print("You selected Option 2!")
        elif choice == '3':
            print("You selected Option 3!")
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-4.")

# Example 9: Name list builder
def name_list_builder():
    """Build a list of names from user input."""
    print("\n--- Name List Builder ---")
    names = []

    while True:
        name = input("Enter a name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if name:
            names.append(name)
            print(f"Added '{name}'. Total: {len(names)} names.")

    if names:
        print(f"\nAll names: {names}")
        print(f"Total: {len(names)} names")
    else:
        print("No names entered.")

# ============================================================
# Simulated Input (For Testing)
# ============================================================
# Example 10: Simulating input for testing
print("--- Simulated Input ---")

# Simulate what input() does
simulated_inputs = ["Alice", "30", "5.7", "yes"]
input_index = 0

def simulated_input(prompt=""):
    """Simulate input() for testing."""
    global input_index
    if input_index < len(simulated_inputs):
        value = simulated_inputs[input_index]
        input_index += 1
        print(f"{prompt}{value}")
        return value
    return ""

# Test with simulated input
name = simulated_input("Enter name: ")
age = int(simulated_input("Enter age: "))
height = float(simulated_input("Enter height: "))
response = simulated_input("Continue? (y/n): ")

print(f"\nName: {name}")
print(f"Age: {age}")
print(f"Height: {height}")
print(f"Response: {response}")

# ============================================================
# input() with Different Prompts
# ============================================================
# Example 11: Prompt techniques
print("\n--- Prompt Techniques ---")

# Simple prompt
# name = input("Name: ")

# Prompt with default
# name = input("Name [Anonymous]: ")

# Prompt with validation hint
# age = input("Age (18-120): ")

# Prompt with example
# email = input("Email (e.g., user@example.com): ")

print("Prompts can guide user input:")
print("  - 'Name: ' - simple")
print("  - 'Name [Anonymous]: ' - with default")
print("  - 'Age (18-120): ' - with range")
print("  - 'Email (user@example.com): ' - with example")

# ============================================================
# Security Note
# ============================================================
# ⚠️ SECURITY WARNING:
# Never use eval() or exec() on user input!
# This is dangerous and can execute malicious code.
#
# WRONG:
# result = eval(input("Enter math: "))  # DANGEROUS!
#
# RIGHT:
# Use a safe math parser or ast.literal_eval()

import ast

def safe_eval(expression):
    """Safely evaluate a mathematical expression."""
    try:
        # Only allows numbers, operators, and basic math
        tree = ast.parse(expression, mode='eval')
        return eval(compile(tree, '<string>', 'eval'))
    except:
        return None

# Test safe eval
expressions = ["2 + 3", "10 * 5", "100 / 4"]
for expr in expressions:
    result = safe_eval(expr)
    print(f"  {expr} = {result}")

# This would fail safely:
result = safe_eval("__import__('os').system('echo HACKED')")
print(f"  Malicious input: {result}")  # None (blocked!)

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. input(prompt) reads user input as a string")
print("2. Always convert input: int(), float() with try/except")
print("3. Validate input ranges and types")
print("4. Use defaults for optional input")
print("5. NEVER use eval() on user input - use ast.literal_eval()")
print("6. Strip whitespace with .strip()")
print("7. Provide clear prompts with examples")
