# Glossary: Rounding Ufuncs (Lecture 22)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| round() | `np.round(arr, decimals)` | Round to nearest (Banker's) |
| around() | `np.around(arr, decimals)` | Alias for round() |
| floor() | `np.floor(arr)` | Round down to integer |
| ceil() | `np.ceil(arr)` | Round up to integer |
| trunc() | `np.trunc(arr)` | Truncate toward zero |
| fix() | `np.fix(arr)` | Alias for trunc() |
| Decimals | `decimals=-1` | Round to nearest 10, 100 |
| Banker's Rounding | Round half to even | Standard IEEE 754 |
| Data Binning | Round to bins | Group continuous data |

---

## Detailed Definitions

### around()

**Definition:** Alias for `np.round()`. Rounds an array to the given number of decimal places.

**Example:**
```python
import numpy as np

arr = np.array([1.2345, 2.3456, 3.4567])
print(np.around(arr, 2))
# Output: [1.23 2.35 3.46]
```

**Related Terms:** round(), Decimal Places

---

### Banker's Rounding

**Definition:** A rounding strategy where 0.5 values are rounded to the nearest even number. This is the default behavior of `np.round()` and follows IEEE 754 standard.

**Example:**
```python
import numpy as np

# Banker's rounding
print("round(0.5):", np.round(0.5))  # 0.0 (rounds to even)
print("round(1.5):", np.round(1.5))  # 2.0 (rounds to even)
print("round(2.5):", np.round(2.5))  # 2.0 (rounds to even)
print("round(3.5):", np.round(3.5))  # 4.0 (rounds to even)
```

**Related Terms:** round(), IEEE 754

---

### ceil()

**Definition:** Rounds each element up to the nearest integer. Always returns values >= input.

**Example:**
```python
import numpy as np

arr = np.array([1.1, 1.5, 1.9, -1.1, -1.5])
print(np.ceil(arr))
# Output: [ 2.  2.  2. -1. -1.]
```

**Related Terms:** floor(), trunc()

---

### Data Binning

**Definition:** The process of grouping continuous data into discrete bins or intervals. Often achieved through rounding.

**Example:**
```python
import numpy as np

# Round to nearest 5
data = np.array([12, 27, 33, 48, 55])
binned = np.round(data / 5) * 5
print("Binned to 5:", binned)
# Output: [10 25 35 50 55]
```

**Related Terms:** round(), Histogram

---

### Decimal Places

**Definition:** The number of digits after the decimal point to round to. Positive values round to decimals, negative values round to 10s, 100s, etc.

**Example:**
```python
import numpy as np

arr = np.array([1.2345, 2.3456, 3.4567])

print("2 decimals:", np.round(arr, 2))  # [1.23 2.35 3.46]
print("1 decimal:", np.round(arr, 1))   # [1.2 2.3 3.5]

# Negative decimals - round to nearest 10, 100
arr2 = np.array([12, 27, 33, 48, 55])
print("Nearest 10:", np.round(arr2, -1))  # [10 30 30 50 60]
print("Nearest 100:", np.round(arr2, -2))  # [ 0 0 0 0 100]
```

**Related Terms:** round(), Precision

---

### fix()

**Definition:** Alias for `np.trunc()`. Truncates each element toward zero.

**Example:**
```python
import numpy as np

arr = np.array([1.9, 2.1, -3.7, -4.2])
print(np.fix(arr))
# Output: [ 1.  2. -3. -4.]
```

**Related Terms:** trunc(), floor()

---

### floor()

**Definition:** Rounds each element down to the nearest integer. Always returns values <= input. For negative numbers, rounds toward -infinity.

**Example:**
```python
import numpy as np

arr = np.array([1.1, 1.5, 1.9, -1.1, -1.5])
print(np.floor(arr))
# Output: [ 1.  1.  1. -2. -2.]
```

**Related Terms:** ceil(), trunc()

---

### Precision

**Definition:** The degree of exactness in a numerical value. Controlled by the number of decimal places in rounding.

**Example:**
```python
import numpy as np

arr = np.array([1.23456789])

print("High precision:", np.round(arr, 6))
print("Medium precision:", np.round(arr, 3))
print("Low precision:", np.round(arr, 1))
```

**Related Terms:** Decimal Places, Significant Figures

---

### round()

**Definition:** Rounds an array to the given number of decimal places using Banker's rounding (round half to even).

**Example:**
```python
import numpy as np

arr = np.array([1.5, 2.5, 3.5, 4.5])
print(np.round(arr))
# Output: [2. 2. 4. 4.]

print(np.round(arr, 0))  # Same as above
print(np.round(1.234, 2))  # 1.23
```

**Related Terms:** around(), floor(), ceil()

---

### Significant Figures

**Definition:** The number of meaningful digits in a value. Related to but different from decimal places.

**Example:**
```python
import numpy as np

# Round to 3 significant figures
arr = np.array([1234.5678, 0.0012345678])

# Calculate decimals needed for 3 sig figs
decimals = 3 - np.floor(np.log10(np.abs(arr))).astype(int) - 1
result = np.round(arr, decimals)
print("3 sig figs:", result)
```

**Related Terms:** Precision, Decimal Places

---

### Truncation

**Definition:** Removing digits after the decimal point without rounding. Always rounds toward zero.

**Example:**
```python
import numpy as np

arr = np.array([1.9, 2.1, -3.7, -4.2])
print(np.trunc(arr))
# Output: [ 1.  2. -3. -4.]
```

**Related Terms:** floor(), ceil()

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| around() | Alias for round() | `np.around(arr, 2)` |
| Banker's Rounding | Round half to even | `np.round(2.5)` → 2.0 |
| ceil() | Round up | `np.ceil(1.1)` → 2.0 |
| Data Binning | Group into intervals | `np.round(arr/5)*5` |
| Decimal Places | Digits after decimal | `np.round(arr, 2)` |
| fix() | Alias for trunc() | `np.fix(arr)` |
| floor() | Round down | `np.floor(1.9)` → 1.0 |
| Precision | Degree of exactness | 2 decimal places |
| round() | Round to nearest | `np.round(arr, 2)` |
| Significant Figures | Meaningful digits | 3 sig figs |
| Truncation | Remove decimals | `np.trunc(1.9)` → 1.0 |

---

**Back to Lecture:** [22 - Rounding Ufuncs](22-ufunc-rounding-lecture.md)
