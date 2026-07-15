"""
W3Schools Python Tutorial - 11: Python Booleans
================================================
Topics: True/False, bool() function, evaluation, comparisons

Run: python 11-booleans.py
Reference: https://www.w3schools.com/python/python_booleans.asp
"""

# ============================================================
# Booleans - True and False
# ============================================================
# Example 1: Boolean basics
x = True
y = False

print(f"x = {x}")
print(f"y = {y}")
print(f"type(x) = {type(x)}")

# Output:
# x = True
# y = False
# type(x) = <class 'bool'>

# ============================================================
# The bool() Function
# ============================================================
# Example 2: bool() evaluates truthiness/falsiness
print("\n--- bool() Function ---")

# These evaluate to True:
print(f"bool(1) = {bool(1)}")           # True (non-zero int)
print(f"bool(-1) = {bool(-1)}")         # True (negative int)
print(f"bool(3.14) = {bool(3.14)}")     # True (non-zero float)
print(f"bool('hello') = {bool('hello')}")  # True (non-empty string)
print(f"bool([1,2]) = {bool([1,2])}")   # True (non-empty list)
d = {'a': 1}
print(f"bool(d) = {bool(d)}")  # True (non-empty dict)

# These evaluate to False:
print(f"bool(0) = {bool(0)}")           # False (zero)
print(f"bool(0.0) = {bool(0.0)}")       # False (zero float)
print(f"bool('') = {bool('')}")         # False (empty string)
print(f"bool([]) = {bool([])}")         # False (empty list)
print(f"bool(()) = {bool(())}")         # False (empty tuple)
d = {}
print(f"bool(d) = {bool(d)}")     # False (empty dict)
print(f"bool(set()) = {bool(set())}")   # False (empty set)
print(f"bool(None) = {bool(None)}")     # False (None)

# ============================================================
# Comparison Operators (Return Booleans)
# ============================================================
# Example 3: Comparison operators
print("\n--- Comparison Operators ---")
x = 10
y = 20

print(f"{x} == {y}: {x == y}")   # False - equal
print(f"{x} != {y}: {x != y}")   # True - not equal
print(f"{x} > {y}: {x > y}")     # False - greater than
print(f"{x} < {y}: {x < y}")     # True - less than
print(f"{x} >= {y}: {x >= y}")   # False - greater or equal
print(f"{x} <= {y}: {x <= y}")   # True - less or equal

# Output:
# 10 == 20: False
# 10 != 20: True
# 10 > 20: False
# 10 < 20: True
# 10 >= 20: False
# 10 <= 20: True

# ============================================================
# Logical Operators (and, or, not)
# ============================================================
# Example 4: Logical operators
print("\n--- Logical Operators ---")

x = True
y = False

print(f"True and True: {True and True}")      # True
print(f"True and False: {True and False}")    # False
print(f"False and True: {False and True}")    # False
print(f"False and False: {False and False}")  # False

print(f"True or True: {True or True}")        # True
print(f"True or False: {True or False}")      # True
print(f"False or True: {False or True}")      # True
print(f"False or False: {False or False}")    # False

print(f"not True: {not True}")                # False
print(f"not False: {not False}")              # True

# ============================================================
# Practical Boolean Examples
# ============================================================
# Example 5: Real-world boolean logic
age = 25
has_id = True
is_vip = False

# Access control
can_enter = age >= 18 and has_id
print(f"\nCan enter: {can_enter}")  # True

# Discount eligibility
gets_discount = is_vip or age < 18
print(f"Gets discount: {gets_discount}")  # True (age < 18 is False, but is_vip is False too)

# Wait, let me recalculate:
gets_discount = is_vip or (age < 18)
print(f"Gets discount (corrected): {gets_discount}")  # False

# Better example
student_discount = age < 26 and not is_vip
print(f"Student discount: {student_discount}")  # True

# ============================================================
# Boolean in Conditions
# ============================================================
# Example 6: Using booleans in if statements
is_raining = False
has_umbrella = True

if is_raining:
    print("Take an umbrella!")
else:
    print("No umbrella needed!")

if is_raining and not has_umbrella:
    print("Stay inside!")
elif is_raining and has_umbrella:
    print("You're protected!")
else:
    print("Enjoy the weather!")

# ============================================================
# Boolean Algebra Properties
# ============================================================
# Example 7: Boolean algebra
print("\n--- Boolean Algebra ---")

# De Morgan's Laws
p = True
q = False

print(f"not (p and q) = {not (p and q)}")
print(f"(not p) or (not q) = {(not p) or (not q)}")
# Both should be True (De Morgan's Law)

print(f"not (p or q) = {not (p or q)}")
print(f"(not p) and (not q) = {(not p) and (not q)}")
# Both should be False (De Morgan's Law)

# Double negation
print(f"not not True = {not not True}")    # True
print(f"not not False = {not not False}")  # False

# ============================================================
# Booleans are Subclass of int
# ============================================================
# Example 8: Booleans in math
print(f"\nTrue + True = {True + True}")      # 2
print(f"True * 10 = {True * 10}")           # 10
print(f"False + 5 = {False + 5}")           # 5
print(f"False * 100 = {False * 100}")       # 0
print(f"True == 1: {True == 1}")            # True
print(f"False == 0: {False == 0}")          # True
print(f"True > False: {True > False}")      # True

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Booleans are True or False")
print("2. bool() converts values to boolean (0/empty = False)")
print("3. Comparison operators return booleans (==, !=, >, <, etc.)")
print("4. Logical operators: and, or, not")
print("5. Booleans are subclass of int (True=1, False=0)")
print("6. Truthiness: non-zero, non-empty = True; 0, empty, None = False")
