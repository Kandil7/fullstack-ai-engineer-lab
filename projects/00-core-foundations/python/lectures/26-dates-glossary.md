# Python Dates — Glossary 26

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Date | Year, month, day object | `date(2026, 12, 25)` |
| Time | Hour, minute, second object | `time(14, 30, 0)` |
| DateTime | Date + time combined | `datetime(2026, 12, 25, 10, 30)` |
| Timedelta | Duration between dates | `timedelta(days=30)` |
| Timestamp | Unix epoch time (float) | `1672531200.0` |
| strftime | Format datetime to string | `dt.strftime("%Y-%m-%d")` |
| strptime | Parse string to datetime | `datetime.strptime(s, fmt)` |
| Timezone | UTC offset information | `timezone.utc`, `timezone(hours=5)` |
| Naive DateTime | No timezone info | `datetime.now()` |
| Aware DateTime | Has timezone info | `datetime.now(timezone.utc)` |
| Epoch | Unix time start (1970-01-01) | `datetime.fromtimestamp(0)` |
| ISO Format | Standard datetime format | `2026-12-25T10:30:00` |
| Calendar | Month/year grid | `calendar.month(2026, 7)` |
| Leap Year | 366-day year | Every 4 years (with exceptions) |
| UTC | Coordinated Universal Time | `timezone.utc` |
| DST | Daylight Saving Time | `tzinfo` objects |
| relativedelta | Precise date arithmetic | `relativedelta(months=3)` |
| Parser | Date string parser | `dateutil.parser.parse()` |
| Weekday | Day of week (0=Monday) | `dt.weekday()` |
| ISO Week | Week number (1-53) | `dt.isocalendar()[1]` |

---

## Definitions

### Aware DateTime
**Definition**: A datetime object that includes timezone information. Can be compared with other aware datetimes and converted between timezones.

**Example**:
```python
from datetime import datetime, timezone, timedelta

# Create aware datetime
aware = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
print(aware.tzinfo)  # UTC

# Convert to different timezone
IST = timezone(timedelta(hours=5, minutes=30))
ist_time = aware.astimezone(IST)
print(ist_time)  # 2026-07-05 17:30:00+05:30
```

**Related**: naive datetime, timezone, UTC, conversion

---

### Calendar
**Definition**: The `calendar` module provides functions for working with calendars, including printing monthly and yearly calendars.

**Example**:
```python
import calendar

# Print July 2026
print(calendar.month(2026, 7))

# Check if leap year
print(calendar.isleap(2024))  # True
print(calendar.isleap(2026))  # False

# Get month with weekday numbers
print(calendar.monthcalendar(2026, 7))
```

**Related**: date, month, year, leap year

---

### Date
**Definition**: An object representing a calendar date (year, month, day). Cannot be modified after creation (immutable).

**Example**:
```python
from datetime import date

# Create date
today = date.today()
christmas = date(2026, 12, 25)

# Access attributes
print(today.year)   # 2026
print(today.month)  # 7
print(today.day)    # 5
print(today.weekday())  # 6 (Sunday)

# Date arithmetic
diff = christmas - today
print(diff.days)  # Days until Christmas
```

**Related**: datetime, time, timedelta, immutable

---

### DateTime
**Definition**: An object combining date and time information. The most commonly used temporal object in Python.

**Example**:
```python
from datetime import datetime

# Current datetime
now = datetime.now()
print(now)  # 2026-07-05 14:30:45.123456

# Specific datetime
dt = datetime(2026, 12, 25, 10, 30, 45)
print(dt)  # 2026-12-25 10:30:45

# From timestamp
dt = datetime.fromtimestamp(1672531200)
```

**Related**: date, time, timestamp, formatting

---

### DST
**Definition**: Daylight Saving Time — seasonal clock adjustment. Handled by timezone objects with appropriate `tzinfo`.

**Example**:
```python
from datetime import datetime, timezone, timedelta

# UTC offset changes with DST
# In practice, use pytz or zoneinfo for proper DST handling
import zoneinfo
ny_tz = zoneinfo.ZoneInfo("America/New_York")
dt = datetime(2026, 7, 5, 12, 0, tzinfo=ny_tz)
print(dt)  # Handles DST automatically
```

**Related**: timezone, UTC, clock adjustment

---

### Epoch
**Definition**: The starting point for Unix time: January 1, 1970, 00:00:00 UTC. Timestamps are seconds since this epoch.

**Example**:
```python
from datetime import datetime

# Epoch start
epoch = datetime(1970, 1, 1)
print(epoch.timestamp())  # 0.0

# Current timestamp
now = datetime.now()
print(now.timestamp())  # Seconds since epoch
```

**Related**: timestamp, Unix time, fromtimestamp

---

### ISO Format
**Definition**: A standardized datetime format: `YYYY-MM-DDTHH:MM:SS`. Widely used for data interchange.

**Example**:
```python
from datetime import datetime

dt = datetime(2026, 12, 25, 10, 30, 45)

# ISO format string
iso_str = dt.isoformat()
print(iso_str)  # 2026-12-25T10:30:45

# Parse ISO format
dt_back = datetime.fromisoformat(iso_str)
print(dt_back)  # 2026-12-25 10:30:45
```

**Related**: strftime, strptime, formatting, standard

---

### Leap Year
**Definition**: A year with 366 days (February has 29 days). Occurs every 4 years, except years divisible by 100 but not 400.

**Example**:
```python
import calendar

# Check leap year
print(calendar.isleap(2024))  # True (divisible by 4)
print(calendar.isleap(2026))  # False
print(calendar.isleap(1900))  # False (divisible by 100, not 400)
print(calendar.isleap(2000))  # True (divisible by 400)
```

**Related**: calendar, February, 366 days

---

### Naive DateTime
**Definition**: A datetime object without timezone information. Cannot be safely compared with aware datetimes.

**Example**:
```python
from datetime import datetime

# Naive datetime (no timezone)
naive = datetime.now()
print(naive.tzinfo)  # None

# Cannot compare with aware
from datetime import timezone
aware = datetime.now(timezone.utc)
# naive == aware  # TypeError
```

**Related**: aware datetime, timezone, comparison

---

### Parser
**Definition**: A function that converts a string representation of a date/time into a datetime object. Python's `strptime` and third-party `dateutil.parser`.

**Example**:
```python
from datetime import datetime

# Using strptime
dt = datetime.strptime("25/12/2026 10:30", "%d/%m/%Y %H:%M")

# Using dateutil (more flexible)
from dateutil import parser
dt = parser.parse("December 25, 2026 10:30 AM")
```

**Related**: strptime, dateutil, parsing

---

### strftime
**Definition**: A method that formats a datetime object into a string using format codes.

**Example**:
```python
from datetime import datetime

dt = datetime(2026, 7, 5, 14, 30, 45)

print(dt.strftime("%Y-%m-%d"))        # 2026-07-05
print(dt.strftime("%d/%m/%Y"))        # 05/07/2026
print(dt.strftime("%B %d, %Y"))       # July 05, 2026
print(dt.strftime("%I:%M %p"))        # 02:30 PM
print(dt.strftime("%A, %B %d %Y"))    # Sunday, July 05 2026
```

**Related**: strptime, format codes, string conversion

---

### strptime
**Definition**: A function that parses a string into a datetime object using format codes.

**Example**:
```python
from datetime import datetime

dt = datetime.strptime("2026-12-25", "%Y-%m-%d")
print(dt)  # 2026-12-25 00:00:00

dt = datetime.strptime("25/12/2026 10:30 PM", "%d/%m/%Y %I:%M %p")
print(dt)  # 2026-12-25 22:30:00
```

**Related**: strftime, parsing, format codes

---

### Time
**Definition**: An object representing a time of day (hour, minute, second, microsecond). Used independently or as part of a datetime.

**Example**:
```python
from datetime import time

t = time(14, 30, 45)
print(t.hour)    # 14
print(t.minute)  # 30
print(t.second)  # 45

# Time without date
noon = time(12, 0, 0)
print(noon)  # 12:00:00
```

**Related**: date, datetime, hour, minute, second

---

### timedelta
**Definition**: An object representing a duration or difference between two dates/times. Supports addition and subtraction with dates.

**Example**:
```python
from datetime import datetime, timedelta

now = datetime.now()

# Create timedelta
week = timedelta(days=7)
hours = timedelta(hours=2, minutes=30)

# Add to datetime
future = now + week
past = now - hours

# Difference between dates
d1 = datetime(2026, 12, 25)
d2 = datetime(2026, 7, 5)
diff = d1 - d2
print(diff.days)  # 173
```

**Related**: date arithmetic, duration, addition

---

### Timestamp
**Definition**: A floating-point number representing seconds since the Unix epoch (January 1, 1970). Used for storing and comparing points in time.

**Example**:
```python
from datetime import datetime

# Current timestamp
now = datetime.now()
ts = now.timestamp()
print(ts)  # 1751723445.123456

# Convert timestamp to datetime
dt = datetime.fromtimestamp(ts)
print(dt)  # 2026-07-05 14:30:45.123456

# Specific timestamp
dt = datetime.fromtimestamp(1672531200)
print(dt)  # 2023-01-01 00:00:00
```

**Related**: epoch, Unix time, fromtimestamp

---

### Timezone
**Definition**: Information about the offset from UTC. Timezone-aware datetimes can be converted between timezones.

**Example**:
```python
from datetime import datetime, timezone, timedelta

# UTC
utc = datetime.now(timezone.utc)

# Create timezone
EST = timezone(timedelta(hours=-5))
IST = timezone(timedelta(hours=5, minutes=30))

# Convert
est_time = utc.astimezone(EST)
ist_time = utc.astimezone(IST)

print(f"UTC: {utc}")
print(f"EST: {est_time}")
print(f"IST: {ist_time}")
```

**Related**: UTC, conversion, aware datetime, DST

---

### UTC
**Definition**: Coordinated Universal Time — the primary time standard by which the world regulates clocks. All other timezones are offsets from UTC.

**Example**:
```python
from datetime import datetime, timezone

# Current UTC time
utc_now = datetime.now(timezone.utc)
print(utc_now)

# Convert local to UTC
local = datetime.now()
utc = local.astimezone(timezone.utc)
```

**Related**: timezone, epoch, global time

---

### Weekday
**Definition**: The day of the week as an integer (Monday=0, Sunday=6) or name.

**Example**:
```python
from datetime import date

d = date(2026, 7, 5)  # Sunday
print(d.weekday())      # 6
print(d.isoweekday())   # 7 (Monday=1, Sunday=7)

# Day name
import calendar
day_name = calendar.day_name[d.weekday()]
print(day_name)  # Sunday
```

**Related**: date, day of week, calendar

---

## Code Examples

### Example 1: Business Days Between Dates
```python
from datetime import date, timedelta

def business_days(start, end):
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days

start = date(2026, 7, 1)
end = date(2026, 7, 31)
print(f"Business days: {business_days(start, end)}")
```

### Example 2: Age Calculator
```python
from datetime import date

def age_details(birthdate):
    today = date.today()
    years = today.year - birthdate.year
    months = today.month - birthdate.month
    days = today.day - birthdate.day
    
    if days < 0:
        months -= 1
        days += 30
    if months < 0:
        years -= 1
        months += 12
    
    return years, months, days

bd = date(1990, 5, 15)
y, m, d = age_details(bd)
print(f"Age: {y} years, {m} months, {d} days")
```

---

## Related Concepts

- **dateutil**: Third-party library for flexible parsing
- **pytz**: Timezone definitions (legacy)
- **zoneinfo**: Standard library timezone support (Python 3.9+)
- **Arrow**: Human-friendly datetime library
- **Pandas**: DatetimeIndex for time series
- **Cron**: Scheduled tasks
