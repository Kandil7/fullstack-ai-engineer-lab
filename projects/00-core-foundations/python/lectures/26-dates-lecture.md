# Python Dates — Lecture 26

## Topic Overview

Python's `datetime` module provides classes for manipulating dates, times, and time intervals. It's essential for timestamping, scheduling, time-based calculations, and working with temporal data. The module includes `date`, `time`, `datetime`, `timedelta`, and `timezone` objects.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Create and manipulate date and time objects
- Format dates using strftime and parse with strptime
- Perform date arithmetic with timedelta
- Handle timezones
- Work with timestamps
- Apply date/time to real-world scenarios

---

## Key Concepts

### 1. Creating Date Objects

```python
from datetime import date, time, datetime, timedelta

# Create a date
today = date.today()
print(today)  # 2026-07-05

specific_date = date(2026, 12, 25)
print(specific_date)  # 2026-12-25

# Date attributes
print(today.year)   # 2026
print(today.month)  # 7
print(today.day)    # 5
print(today.weekday())  # 6 (Monday=0, Sunday=6)
```

### 2. Creating Time Objects

```python
from datetime import time

# Create a time
noon = time(12, 0, 0)
print(noon)  # 12:00:00

specific_time = time(14, 30, 45)
print(specific_time)  # 14:30:45

# Time attributes
print(specific_time.hour)    # 14
print(specific_time.minute)  # 30
print(specific_time.second)  # 45
```

### 3. Creating DateTime Objects

```python
from datetime import datetime

# Current datetime
now = datetime.now()
print(now)  # 2026-07-05 14:30:45.123456

# Specific datetime
dt = datetime(2026, 12, 25, 10, 30, 0)
print(dt)  # 2026-12-25 10:30:00

# From timestamp
timestamp = 1672531200  # Unix timestamp
dt_from_ts = datetime.fromtimestamp(timestamp)
print(dt_from_ts)  # 2023-01-01 00:00:00

# Attributes
print(now.year)     # 2026
print(now.month)    # 7
print(now.hour)     # 14
print(now.minute)   # 30
```

### 4. Formatting Dates (strftime)

```python
now = datetime.now()

# Common format codes
print(now.strftime("%Y-%m-%d"))        # 2026-07-05
print(now.strftime("%d/%m/%Y"))        # 05/07/2026
print(now.strftime("%B %d, %Y"))       # July 05, 2026
print(now.strftime("%A, %B %d, %Y"))   # Sunday, July 05, 2026
print(now.strftime("%I:%M %p"))        # 02:30 PM
print(now.strftime("%H:%M:%S"))        # 14:30:45
print(now.strftime("%Y-%m-%d %H:%M"))  # 2026-07-05 14:30
```

### 5. Parsing Dates (strptime)

```python
from datetime import datetime

# Parse string to datetime
date_string = "2026-12-25"
dt = datetime.strptime(date_string, "%Y-%m-%d")
print(dt)  # 2026-12-25 00:00:00

# More complex parsing
date_string = "25/12/2026 10:30 PM"
dt = datetime.strptime(date_string, "%d/%m/%Y %I:%M %p")
print(dt)  # 2026-12-25 22:30:00
```

### 6. Date Arithmetic (timedelta)

```python
from datetime import datetime, timedelta

now = datetime.now()

# Add/subtract days
future = now + timedelta(days=30)
past = now - timedelta(days=30)
print(future.strftime("%Y-%m-%d"))
print(past.strftime("%Y-%m-%d"))

# Add/subtract hours, minutes, seconds
later = now + timedelta(hours=2, minutes=30)
earlier = now - timedelta(hours=1)

# Difference between dates
date1 = datetime(2026, 12, 25)
date2 = datetime(2026, 7, 5)
diff = date1 - date2
print(diff.days)  # 173
print(diff.total_seconds())  # 14947200.0

# Calculate age
birthday = datetime(1990, 5, 15)
age = (datetime.now() - birthday).days // 365
print(f"Age: {age}")
```

### 7. Timezones

```python
from datetime import datetime, timezone, timedelta

# UTC
utc_now = datetime.now(timezone.utc)
print(utc_now)

# Create timezone
EST = timezone(timedelta(hours=-5))
PST = timezone(timedelta(hours=-8))
IST = timezone(timedelta(hours=5, minutes=30))

# Convert between timezones
est_time = datetime.now(EST)
ist_time = est_time.astimezone(IST)
print(f"EST: {est_time}")
print(f"IST: {ist_time}")
```

### 8. Working with Timestamps

```python
from datetime import datetime

# Current timestamp
now = datetime.now()
timestamp = now.timestamp()
print(timestamp)  # Unix timestamp (float)

# Convert timestamp to datetime
dt = datetime.fromtimestamp(1672531200)
print(dt)

# Convert to timestamp and back
dt = datetime(2026, 7, 5, 12, 0, 0)
ts = dt.timestamp()
dt_back = datetime.fromtimestamp(ts)
print(dt_back)
```

---

## Code Examples

### Example 1: Age Calculator

```python
from datetime import date

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

birthday = date(1990, 5, 15)
print(f"Age: {calculate_age(birthday)} years")
```

### Example 2: Days Until Event

```python
from datetime import date

def days_until(target_date):
    today = date.today()
    delta = target_date - today
    return max(delta.days, 0)

christmas = date(2026, 12, 25)
print(f"Days until Christmas: {days_until(christmas)}")
```

### Example 3: Business Days Calculator

```python
from datetime import date, timedelta

def business_days(start, end):
    """Count business days between two dates."""
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Monday-Friday
            days += 1
        current += timedelta(days=1)
    return days

start = date(2026, 7, 1)
end = date(2026, 7, 31)
print(f"Business days in July 2026: {business_days(start, end)}")
```

### Example 4: Date Range Generator

```python
from datetime import date, timedelta

def date_range(start, end, step_days=1):
    """Generate dates in a range."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=step_days)

for d in date_range(date(2026, 7, 1), date(2026, 7, 10), 3):
    print(d)  # 2026-07-01, 2026-07-04, 2026-07-07, 2026-07-10
```

---

## Common Mistakes to Avoid

### Mistake 1: Mutable Default Arguments
```python
# WRONG
def add_days(dt, days=timedelta(days=1)):
    return dt + days  # timedelta created once!

# CORRECT
def add_days(dt, days=1):
    return dt + timedelta(days=days)
```

### Mistake 2: Comparing Naive and Aware Datetimes
```python
from datetime import datetime, timezone

# WRONG — mixing naive and aware
naive = datetime.now()
aware = datetime.now(timezone.utc)
# naive == aware  # TypeError

# CORRECT — both aware
utc = datetime.now(timezone.utc)
eastern = utc.astimezone(timezone(timedelta(hours=-5)))
print(utc == eastern)  # True (same instant)
```

### Mistake 3: Month/Day Order
```python
# WRONG — ambiguous order
dt = datetime(2026, 25, 12)  # ValueError!

# CORRECT — year, month, day
dt = datetime(2026, 12, 25)  # OK
```

---

## Best Practices

1. **Use `datetime` over `date`** when time matters
2. **Use timezone-aware datetimes** for production code
3. **Store timestamps** in UTC, convert for display
4. **Use `timedelta`** for date arithmetic
5. **Use `strftime`/`strptime`** for formatting/parsing
6. **Be careful with month/day order** — always `year, month, day`
7. **Use `date.today()`** for current date
8. **Use `datetime.now(timezone.utc)`** for current UTC time

---

## Practice Exercises

### Exercise 1: Birthday Calculator
Write a function that calculates a person's age in years, months, and days.

### Exercise 2: Calendar Generator
Write a function that prints a monthly calendar for a given year and month.

### Exercise 3: Flight Duration
Write a function that calculates flight duration given departure and arrival datetimes (with timezones).

---

## Summary

- **`date`**: Year, month, day
- **`time`**: Hour, minute, second
- **`datetime`**: Date + time
- **`timedelta`**: Duration/difference
- **`strftime()`**: Format datetime to string
- **`strptime()`**: Parse string to datetime
- **Timezones**: Use `timezone.utc` and `astimezone()`
- **Timestamps**: `datetime.timestamp()` and `fromtimestamp()`
- **Date arithmetic**: Add/subtract `timedelta` objects
