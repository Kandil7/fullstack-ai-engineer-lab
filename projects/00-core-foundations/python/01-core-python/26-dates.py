"""
W3Schools Python Tutorial - 26: Python Dates
=============================================
Topics: datetime module, current date/time, formatting, timedelta

Run: python 26-dates.py
Reference: https://www.w3schools.com/python/python_date.asp
"""

# ============================================================
# The datetime Module
# ============================================================
# Python has a built-in module for working with dates and times.

from datetime import datetime, date, time, timedelta

# ============================================================
# Current Date and Time
# ============================================================
# Example 1: Getting current date and time
print("--- Current Date and Time ---")

now = datetime.now()
print(f"datetime.now(): {now}")

today = date.today()
print(f"date.today(): {today}")

current_time = datetime.now().time()
print(f"datetime.now().time(): {current_time}")

# Output:
# datetime.now(): 2024-01-15 14:30:45.123456
# date.today(): 2024-01-15
# datetime.now().time(): 14:30:45.123456

# ============================================================
# Creating Date Objects
# ============================================================
# Example 2: Creating specific dates
print("\n--- Creating Dates ---")

# From year, month, day
birthday = date(1990, 6, 15)
print(f"Birthday: {birthday}")

# From datetime
dt = datetime(2024, 12, 25, 10, 30, 0)
print(f"Christmas: {dt}")

# From string (parsing)
date_string = "2024-01-15"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
print(f"Parsed: {parsed_date}")

# ============================================================
# Accessing Date Components
# ============================================================
# Example 3: Getting individual components
now = datetime.now()

print(f"\n--- Date Components ---")
print(f"Year: {now.year}")
print(f"Month: {now.month}")
print(f"Day: {now.day}")
print(f"Hour: {now.hour}")
print(f"Minute: {now.minute}")
print(f"Second: {now.second}")
print(f"Microsecond: {now.microsecond}")
print(f"Weekday: {now.weekday()}")  # 0=Monday, 6=Sunday
print(f"Iso weekday: {now.isoweekday()}")  # 1=Monday, 7=Sunday

# ============================================================
# Formatting Dates (strftime)
# ============================================================
# Example 4: Format date to string
now = datetime.now()

print(f"\n--- Formatting Dates ---")
print(f"Default: {now}")
print(f"ISO format: {now.isoformat()}")
print(f"Year-Month-Day: {now.strftime('%Y-%m-%d')}")
print(f"Day/Month/Year: {now.strftime('%d/%m/%Y')}")
print(f"Time: {now.strftime('%H:%M:%S')}")
print(f"DateTime: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Day name: {now.strftime('%A')}")
print(f"Month name: {now.strftime('%B')}")
print(f"12-hour time: {now.strftime('%I:%M %p')}")

# Output:
# Default: 2024-01-15 14:30:45.123456
# ISO format: 2024-01-15T14:30:45.123456
# Year-Month-Day: 2024-01-15
# Day/Month/Year: 15/01/2024
# Time: 14:30:45
# DateTime: 2024-01-15 14:30:45
# Day name: Monday
# Month name: January
# 12-hour time: 02:30 PM

# ============================================================
# Format Codes Reference
# ============================================================
# Example 5: Common format codes
print("\n--- Format Codes ---")
dt = datetime(2024, 3, 15, 14, 30, 45)

# Year
print(f"%Y (4-digit year): {dt.strftime('%Y')}")
print(f"%y (2-digit year): {dt.strftime('%y')}")

# Month
print(f"%m (month number): {dt.strftime('%m')}")
print(f"%B (month name): {dt.strftime('%B')}")
print(f"%b (abbreviated): {dt.strftime('%b')}")

# Day
print(f"%d (day): {dt.strftime('%d')}")
print(f"%A (day name): {dt.strftime('%A')}")
print(f"%a (abbreviated): {dt.strftime('%a')}")

# Time
print(f"%H (24-hour): {dt.strftime('%H')}")
print(f"%I (12-hour): {dt.strftime('%I')}")
print(f"%M (minute): {dt.strftime('%M')}")
print(f"%S (second): {dt.strftime('%S')}")
print(f"%p (AM/PM): {dt.strftime('%p')}")

# ============================================================
# Parsing Dates (strptime)
# ============================================================
# Example 6: Parse string to date
print("\n--- Parsing Dates ---")

date_string = "2024-01-15"
date_obj = datetime.strptime(date_string, "%Y-%m-%d")
print(f"Parsed '{date_string}': {date_obj}")

time_string = "14:30:45"
time_obj = datetime.strptime(time_string, "%H:%M:%S")
print(f"Parsed '{time_string}': {time_obj}")

datetime_string = "15/01/2024 14:30:45"
dt_obj = datetime.strptime(datetime_string, "%d/%m/%Y %H:%M:%S")
print(f"Parsed '{datetime_string}': {dt_obj}")

# ============================================================
# timedelta - Date Arithmetic
# ============================================================
# Example 7: Working with time differences
print("\n--- timedelta ---")

today = date.today()
print(f"Today: {today}")

# Add days
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)
next_month = today + timedelta(days=30)

print(f"Tomorrow: {tomorrow}")
print(f"Next week: {next_week}")
print(f"In 30 days: {next_month}")

# Subtract days
last_week = today - timedelta(weeks=1)
print(f"Last week: {last_week}")

# Date difference
birthday = date(1990, 6, 15)
age = today - birthday
print(f"\nDays since birthday: {age.days}")
print(f"Years (approx): {age.days // 365}")
print(f"Hours (approx): {age.days * 24}")

# Time difference
dt1 = datetime(2024, 1, 15, 10, 0, 0)
dt2 = datetime(2024, 1, 15, 14, 30, 0)
diff = dt2 - dt1
print(f"\nTime difference: {diff}")
print(f"Total seconds: {diff.total_seconds()}")

# ============================================================
# Practical Examples
# ============================================================
# Example 8: Real-world date operations
print("\n--- Practical Examples ---")

# Age calculator
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

birthday = date(1990, 6, 15)
print(f"Age: {calculate_age(birthday)} years")

# Days until Christmas
def days_until_christmas():
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    return (christmas - today).days

print(f"Days until Christmas: {days_until_christmas()}")

# Week number
today = date.today()
print(f"Week number: {today.isocalendar()[1]}")

# Is leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print(f"2024 is leap year: {is_leap_year(2024)}")
print(f"2023 is leap year: {is_leap_year(2023)}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. from datetime import datetime, date, time, timedelta")
print("2. datetime.now(): current date and time")
print("3. date.today(): current date only")
print("4. strftime(): format date to string")
print("5. strptime(): parse string to date")
print("6. timedelta(): date arithmetic (add/subtract days)")
print("7. Date comparison: date1 < date2")
print("8. Date difference: date1 - date2 returns timedelta")
