# Lecture 20: Creating Custom Ufuncs in NumPy

## Topic Overview

While NumPy provides many built-in ufuncs, sometimes you need to create your own custom universal functions. NumPy offers `np.frompyfunc()` to convert Python functions into ufuncs, enabling element-wise operations on arrays using your custom logic. This lecture covers how to create custom ufuncs, apply them to arrays, and work with string operations.

Custom ufuncs are particularly useful when you need specialized calculations that aren't available in NumPy's built-in functions, such as custom business logic, domain-specific calculations, or complex conditional transformations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create custom ufuncs using `np.frompyfunc()`
2. Convert Python functions to work element-wise on arrays
3. Create ufuncs with multiple input and output parameters
4. Apply custom ufuncs to string arrays
5. Handle dtype conversion when using custom ufuncs
6. Create practical data transformation functions
7. Apply custom ufuncs to real-world scenarios
8. Understand the limitations and considerations of custom ufuncs
9. Combine custom ufuncs with built-in NumPy functions
10. Optimize custom ufunc performance

---

## Key Concepts

### 1. frompyfunc() — Create ufunc from Python Function

`np.frompyfunc()` converts any Python function into a ufunc that operates element-wise on arrays.

```python
import numpy as np

# Simple function
def add_ten(x):
    return x + 10

# Create ufunc
add_ten_ufunc = np.frompyfunc(add_ten, 1, 1)

arr = np.array([1, 2, 3, 4, 5])
result = add_ten_ufunc(arr)
print("add_ten:", result)  # [11 12 13 14 15]
print("Type:", result.dtype)  # object
```

**Parameters:**
- `func`: Python function to convert
- `nin`: Number of input parameters
- `nout`: Number of output values

### 2. frompyfunc with Multiple Inputs

```python
import numpy as np

def add_multiply(x, y, multiplier):
    return (x + y) * multiplier

# Create ufunc (3 inputs, 1 output)
add_mult = np.frompyfunc(add_multiply, 3, 1)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = add_mult(arr1, arr2, 2)
print("add_multiply:", result.astype(int))  # [10 14 18]
```

### 3. Custom Math Functions

```python
import numpy as np

# Custom square
def square(x):
    return x ** 2

square_ufunc = np.frompyfunc(square, 1, 1)
arr = np.array([1, 2, 3, 4, 5])
print("Square:", square_ufunc(arr).astype(int))  # [ 1  4  9 16 25]

# Custom percentage
def percentage(x, total):
    return (x / total) * 100

pct_ufunc = np.frompyfunc(percentage, 2, 1)
scores = np.array([85, 92, 78, 95, 88])
total = 100
print("Percentages:", pct_ufunc(scores, total).astype(float))
# Output: [85. 92. 78. 95. 88.]

# Custom clamp
def clamp(x, min_val, max_val):
    return max(min_val, min(x, max_val))

clamp_ufunc = np.frompyfunc(clamp, 3, 1)
arr = np.array([-5, 10, 25, 50, 100])
print("Clamped [0,50]:", clamp_ufunc(arr, 0, 50).astype(int))
# Output: [ 0 10 25 50 50]
```

### 4. String Operations

```python
import numpy as np

arr = np.array(["hello", "world", "numpy", "python"])

# String operations
print("\nUpper:", np.char.upper(arr))
print("Lower:", np.char.lower(arr))
print("Title:", np.char.title(arr))
print("Strip:", np.char.strip(arr))

# String operations with custom function
def add_prefix(x):
    return "num_" + x

prefix_ufunc = np.frompyfunc(add_prefix, 1, 1)
print("\nWith prefix:", prefix_ufunc(arr))
# Output: ['num_hello' 'num_world' 'num_numpy' 'num_python']
```

### 5. Data Transformation Examples

```python
import numpy as np

# Temperature conversion
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temp_convert = np.frompyfunc(celsius_to_fahrenheit, 1, 1)

temps_c = np.array([0, 20, 37, 100])
temps_f = temp_convert(temps_c).astype(float)
print("\nCelsius:", temps_c)
print("Fahrenheit:", temps_f.round(2))

# Grade calculator
def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

grade_ufunc = np.frompyfunc(calculate_grade, 1, 1)
scores = np.array([95, 82, 74, 66, 55])
grades = grade_ufunc(scores)
print("\nScores:", scores)
print("Grades:", grades)

# BMI calculator
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

bmi_ufunc = np.frompyfunc(calculate_bmi, 2, 1)
weights = np.array([70, 85, 60])
heights = np.array([1.75, 1.80, 1.65])
bmi = bmi_ufunc(weights, heights).astype(float)
print("\nBMI:", bmi.round(2))
print("BMI categories:", np.where(bmi < 18.5, "Underweight",
       np.where(bmi < 25, "Normal",
       np.where(bmi < 30, "Overweight", "Obese"))))
```

---

## Code Examples with Explanations

### Example 1: Basic Custom Ufunc

```python
import numpy as np

# Define custom function
def circle_area(radius):
    return np.pi * radius ** 2

# Create ufunc
area_ufunc = np.frompyfunc(circle_area, 1, 1)

# Apply to array
radii = np.array([1, 2, 3, 4, 5])
areas = area_ufunc(radii).astype(float)

print("Radii:", radii)
print("Areas:", areas.round(2))
# Output:
# Radii: [1 2 3 4 5]
# Areas: [ 3.14 12.57 28.27 50.27 78.54]
```

### Example 2: Multi-Input Custom Ufunc

```python
import numpy as np

# Calculate distance between two points
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Create ufunc
distance_ufunc = np.frompyfunc(distance, 4, 1)

# Calculate distances
x1 = np.array([0, 1, 2])
y1 = np.array([0, 1, 2])
x2 = np.array([3, 4, 5])
y2 = np.array([3, 4, 5])

distances = distance_ufunc(x1, y1, x2, y2).astype(float)
print("Distances:", distances.round(2))
# Output: Distances: [4.24 4.24 4.24]
```

### Example 3: Custom Ufunc with Conditional Logic

```python
import numpy as np

# Custom function with complex logic
def categorize(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Average"
    else:
        return "Poor"

# Create ufunc
categorize_ufunc = np.frompyfunc(categorize, 1, 1)

# Apply to scores
scores = np.array([95, 82, 68, 55, 90, 76, 88])
categories = categorize_ufunc(scores)

print("Scores:", scores)
print("Categories:", categories)
# Output:
# Scores: [95 82 68 55 90 76 88]
# Categories: ['Excellent' 'Good' 'Average' 'Poor' 'Excellent' 'Good' 'Good']
```

### Example 4: String Manipulation Ufunc

```python
import numpy as np

# Custom string transformation
def format_name(first, last):
    return f"{last.upper()}, {first.title()}"

# Create ufunc
format_ufunc = np.frompyfunc(format_name, 2, 1)

# Apply to name arrays
first_names = np.array(["john", "jane", "bob", "alice"])
last_names = np.array(["doe", "smith", "brown", "johnson"])

formatted = format_ufunc(first_names, last_names)
print("Formatted names:", formatted)
# Output: ['Doe, John' 'Smith, Jane' 'Brown, Bob' 'Johnson, Alice']
```

### Example 5: Practical Data Transformation

```python
import numpy as np

# Tax calculator with brackets
def calculate_tax(income):
    if income <= 10000:
        return income * 0.10
    elif income <= 40000:
        return 10000 * 0.10 + (income - 10000) * 0.12
    elif income <= 85000:
        return 10000 * 0.10 + 30000 * 0.12 + (income - 40000) * 0.22
    else:
        return 10000 * 0.10 + 30000 * 0.12 + 45000 * 0.22 + (income - 85000) * 0.24

# Create ufunc
tax_ufunc = np.frompyfunc(calculate_tax, 1, 1)

# Calculate taxes
incomes = np.array([5000, 15000, 50000, 100000])
taxes = tax_ufunc(incomes).astype(float)

print("Incomes:", incomes)
print("Taxes:", taxes.round(2))
print("Effective rates:", (taxes / incomes * 100).round(1))
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting dtype Conversion

```python
import numpy as np

def add_one(x):
    return x + 1

# WRONG - Result is object dtype
ufunc = np.frompyfunc(add_one, 1, 1)
result = ufunc(np.array([1, 2, 3]))
print(result.dtype)  # object

# CORRECT - Convert to proper dtype
result = ufunc(np.array([1, 2, 3])).astype(int)
print(result.dtype)  # int64
```

### Mistake 2: Not Handling NaN/None Values

```python
import numpy as np

def safe_divide(x, y):
    if y == 0:
        return np.nan
    return x / y

# Handle edge cases in your function
ufunc = np.frompyfunc(safe_divide, 2, 1)
result = ufunc(np.array([10, 20, 30]), np.array([2, 0, 5]))
print(result.astype(float))
```

### Mistake 3: Assuming Vectorization Inside Custom Function

```python
import numpy as np

# WRONG - This won't work element-wise
def bad_function(x):
    return x.sum()  # Fails on scalars

# CORRECT - Use scalar operations
def good_function(x):
    return x * 2  # Works element-wise

ufunc = np.frompyfunc(good_function, 1, 1)
print(ufunc(np.array([1, 2, 3])).astype(int))
```

---

## Best Practices

### 1. Keep Custom Functions Simple

```python
import numpy as np

# Simple, single-purpose functions
def double(x):
    return x * 2

def is_positive(x):
    return x > 0

# Create ufuncs
double_ufunc = np.frompyfunc(double, 1, 1)
positive_ufunc = np.frompyfunc(is_positive, 1, 1)
```

### 2. Always Convert Output dtype

```python
import numpy as np

def calculate(x):
    return x ** 2 + 1

ufunc = np.frompyfunc(calculate, 1, 1)
arr = np.array([1, 2, 3, 4, 5])

# Always convert to appropriate dtype
result = ufunc(arr).astype(float)
print(result)
```

### 3. Test with Edge Cases

```python
import numpy as np

def safe_log(x):
    if x <= 0:
        return np.nan
    return np.log(x)

ufunc = np.frompyfunc(safe_log, 1, 1)
test_arr = np.array([1, 2, 0, -1, 10])
result = ufunc(test_arr).astype(float)
print("Result:", result)
```

### 4. Document Your Custom Ufuncs

```python
import numpy as np

def calculate_bmi(weight, height):
    """
    Calculate BMI from weight (kg) and height (m).
    
    Parameters:
    -----------
    weight : float
        Weight in kilograms
    height : float
        Height in meters
    
    Returns:
    --------
    float
        BMI value
    """
    return weight / (height ** 2)

# Create ufunc
bmi_ufunc = np.frompyfunc(calculate_bmi, 2, 1)
```

---

## Practice Exercises

### Exercise 1: Basic Custom Ufunc

```python
import numpy as np

# TODO: Create ufunc for absolute percentage change
def pct_change(old, new):
    return ((new - old) / old) * 100

pct_ufunc = np.frompyfunc(pct_change, 2, 1)

old_prices = np.array([100, 150, 200, 250])
new_prices = np.array([110, 140, 220, 240])

changes = pct_ufunc(old_prices, new_prices).astype(float)
print("Price changes:", changes.round(2))
```

### Exercise 2: String Ufunc

```python
import numpy as np

# TODO: Create ufunc to extract domain from email
def get_domain(email):
    return email.split('@')[1]

domain_ufunc = np.frompyfunc(get_domain, 1, 1)

emails = np.array(["user@gmail.com", "info@company.org", "test@yahoo.com"])
domains = domain_ufunc(emails)
print("Domains:", domains)
```

### Exercise 3: Complex Logic Ufunc

```python
import numpy as np

# TODO: Create shipping cost calculator
def shipping_cost(weight, express):
    base = 5.00
    if weight > 10:
        base += (weight - 10) * 0.50
    if express:
        base *= 2
    return base

shipping_ufunc = np.frompyfunc(shipping_cost, 2, 1)

weights = np.array([5, 15, 8, 20])
express = np.array([False, True, False, True])

costs = shipping_ufunc(weights, express).astype(float)
print("Shipping costs:", costs)
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **np.frompyfunc()** | Convert Python function to ufunc |
| **nin** | Number of input parameters |
| **nout** | Number of output values |
| **dtype conversion** | Convert object output to proper type |
| **String operations** | Custom string transformations |
| **Data transformations** | Business logic on arrays |
| **Edge cases** | Handle NaN, None, zeros |

---

## Quick Reference

```python
import numpy as np

# Create custom ufunc
def my_function(x, y):
    return x + y

my_ufunc = np.frompyfunc(my_function, 2, 1)

# Apply to arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = my_ufunc(arr1, arr2).astype(int)

# String ufunc
def format_str(s):
    return s.upper()

format_ufunc = np.frompyfunc(format_str, 1, 1)
str_arr = np.array(["hello", "world"])
result = format_ufunc(str_arr)
```

---

**Next Lecture:** [21 - Arithmetic Ufuncs](21-ufunc-arithmetic-lecture.md)
