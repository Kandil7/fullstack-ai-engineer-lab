"""
Ufunc Create
W3Schools: https://www.w3schools.com/python/numpy_ufunc_create.asp

Creating custom ufuncs using frompyfunc and ufunc.frompyfunc.
"""

import numpy as np

# ============================================================
# Example 1: frompyfunc() - Create ufunc from Python function
# Convert any Python function to a ufunc.
# ============================================================

# Simple function
def add_ten(x):
    return x + 10

# Create ufunc
add_ten_ufunc = np.frompyfunc(add_ten, 1, 1)

arr = np.array([1, 2, 3, 4, 5])
result = add_ten_ufunc(arr)
print("add_ten:", result)  # [11 12 13 14 15]
print("Type:", result.dtype)  # object
# Output:
# add_ten: [11 12 13 14 15]
# Type: object

# Convert to proper dtype
result = result.astype(int)
print("As int:", result)  # [11 12 13 14 15]

# ============================================================
# Example 2: frompyfunc with Multiple Inputs
# Functions with multiple parameters.
# ============================================================

def add_multiply(x, y, multiplier):
    return (x + y) * multiplier

# Create ufunc (3 inputs, 1 output)
add_mult = np.frompyfunc(add_multiply, 3, 1)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = add_mult(arr1, arr2, 2)
print("\nadd_multiply:", result.astype(int))  # [10 14 18]
# Output: add_multiply: [10 14 18]

# ============================================================
# Example 3: Custom Math Functions
# Create ufuncs for custom calculations.
# ============================================================

# Custom square
def square(x):
    return x ** 2

square_ufunc = np.frompyfunc(square, 1, 1)
arr = np.array([1, 2, 3, 4, 5])
print("\nSquare:", square_ufunc(arr).astype(int))  # [ 1  4  9 16 25]

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

# ============================================================
# Example 4: String Operations
# Ufuncs work with string arrays.
# ============================================================

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
# Output:
# Upper: ['HELLO' 'WORLD' 'NUMPY' 'PYTHON']
# With prefix: ['num_hello' 'num_world' 'num_numpy' 'num_python']

# ============================================================
# Example 5: ufunc for Data Transformation
# Practical data transformation examples.
# ============================================================

# Temperature conversion
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temp_convert = np.frompyfunc(celsius_to_fahrenheit, 1, 1)

temps_c = np.array([0, 20, 37, 100])
temps_f = temp_convert(temps_c).astype(float)
print("\nCelsius:", temps_c)
print("Fahrenheit:", temps_f.round(2))
# Output:
# Celsius: [  0  20  37 100]
# Fahrenheit: [ 32.   68.   98.6 212. ]

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
# Output:
# Scores: [95 82 74 66 55]
# Grades: ['A' 'B' 'C' 'D' 'F']

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
