"""
W3Schools Python Tutorial - 17: Python If...Else
=================================================
Topics: if, elif, else, shorthand, nested if

Run: python 17-if-else.py
Reference: https://www.w3schools.com/python/python_conditions.asp
"""

# ============================================================
# The if Statement
# ============================================================
# Example 1: Basic if statement
age = 18

if age >= 18:
    print("You are an adult!")
# Output: You are an adult!

# Example 2: if with indentation
temperature = 25
if temperature > 20:
    print("It's warm outside!")
    print("Wear a t-shirt!")
    print("Enjoy the weather!")

# Output:
# It's warm outside!
# Wear a t-shirt!
# Enjoy the weather!

# ============================================================
# The elif Statement
# ============================================================
# Example 3: Multiple conditions with elif
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")
# Output: Score: 75, Grade: C

# ============================================================
# The else Statement
# ============================================================
# Example 4: else catches all other cases
username = "guest"

if username == "admin":
    print("Welcome, Admin!")
elif username == "moderator":
    print("Welcome, Moderator!")
else:
    print(f"Welcome, {username}!")

# Output: Welcome, guest!

# ============================================================
# Short Hand If
# ============================================================
# Example 5: One-line if statement
x = 10
if x > 5: print("x is greater than 5")
# Output: x is greater than 5

# ============================================================
# Short Hand If...Else (Ternary Operator)
# ============================================================
# Example 6: One-line if-else
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age} = {status}")
# Output: Age 20 = adult

# Example 7: Nested ternary (use sparingly!)
x = 10
result = "positive" if x > 0 else "zero" if x == 0 else "negative"
print(f"{x} is {result}")

# ============================================================
# Nested If
# ============================================================
# Example 8: If statements inside if statements
age = 25
has_ticket = True

if age >= 18:
    if has_ticket:
        print("Welcome to the movie!")
    else:
        print("You need a ticket!")
else:
    print("Sorry, you must be 18+")

# Output: Welcome to the movie!

# ============================================================
# Logical Operators in Conditions
# ============================================================
# Example 9: Combining conditions
age = 25
income = 50000
credit_score = 700

# Using 'and'
if age >= 18 and income >= 30000:
    print("Eligible for basic loan")

# Using 'or'
if credit_score >= 750 or income >= 100000:
    print("Eligible for premium loan")

# Using 'not'
if not (age < 18):
    print("You're not a minor")

# Using chained comparisons
temperature = 22
if 20 <= temperature <= 30:
    print(f"Comfortable temperature: {temperature}°C")

# ============================================================
# Practical Examples
# ============================================================
# Example 10: Real-world conditional logic

# Day of week activity
day = "Monday"
if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
elif day == "Friday":
    print("TGIF!")
else:
    print("It's a workday.")

# Price discount
quantity = 15
price_per_unit = 10

if quantity >= 100:
    discount = 0.20  # 20% off
elif quantity >= 50:
    discount = 0.15  # 15% off
elif quantity >= 10:
    discount = 0.10  # 10% off
else:
    discount = 0.0   # No discount

total = quantity * price_per_unit * (1 - discount)
print(f"\nQuantity: {quantity}")
print(f"Discount: {discount * 100}%")
print(f"Total: ${total:.2f}")

# Login check
username = "admin"
password = "secret123"

if username == "admin" and password == "secret123":
    print("\nLogin successful!")
elif username == "admin":
    print("Wrong password!")
elif password == "secret123":
    print("Unknown username!")
else:
    print("Invalid credentials!")

# ============================================================
# match Statement (Python 3.10+)
# ============================================================
# Example 11: Brief preview of match (see 18-match.py for full details)
command = "start"

match command:
    case "start":
        print("\nStarting the system...")
    case "stop":
        print("Stopping the system...")
    case _:
        print("Unknown command!")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. if condition: code executes if True")
print("2. elif condition: check additional conditions")
print("3. else: catch-all for remaining cases")
print("4. Short hand: x = 'yes' if condition else 'no'")
print("5. Nest if statements for complex logic")
print("6. Use and, or, not to combine conditions")
print("7. Python 3.10+: use match for pattern matching")
