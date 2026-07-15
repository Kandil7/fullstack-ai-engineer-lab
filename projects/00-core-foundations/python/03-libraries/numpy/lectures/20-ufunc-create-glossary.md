# Glossary: Creating Custom Ufuncs (Lecture 20)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| frompyfunc() | `np.frompyfunc(func, nin, nout)` | Convert Python function to ufunc |
| nin | Parameter | Number of input arguments |
| nout | Parameter | Number of output values |
| dtype | Output type | Convert object to proper type |
| String Ufunc | Custom | Element-wise string operations |
| Data Transform | Custom | Business logic on arrays |
| Edge Cases | Handling | NaN, None, zeros |

---

## Detailed Definitions

### frompyfunc()

**Definition:** A NumPy function that converts a Python function into a ufunc that operates element-wise on arrays. Returns a ufunc object.

**Example:**
```python
import numpy as np

def add_five(x):
    return x + 5

# Create ufunc from Python function
add_five_ufunc = np.frompyfunc(add_five, 1, 1)

arr = np.array([1, 2, 3, 4, 5])
result = add_five_ufunc(arr)
print(result)
# Output: [6 7 8 9 10]
```

**Related Terms:** nin, nout, ufunc

---

### nin

**Definition:** Parameter in `np.frompyfunc()` that specifies the number of input arguments the function expects.

**Example:**
```python
import numpy as np

# Function with 2 inputs
def add(x, y):
    return x + y

ufunc = np.frompyfunc(add, 2, 1)  # nin=2
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = ufunc(arr1, arr2)
print(result)
# Output: [5 7 9]
```

**Related Terms:** nout, frompyfunc()

---

### nout

**Definition:** Parameter in `np.frompyfunc()` that specifies the number of output values the function returns.

**Example:**
```python
import numpy as np

def divmod_custom(x, y):
    return x // y, x % y

# Function with 2 outputs
ufunc = np.frompyfunc(divmod_custom, 2, 2)  # nout=2
arr1 = np.array([10, 20, 30])
arr2 = np.array([3, 4, 5])
quotient, remainder = ufunc(arr1, arr2)
print("Quotient:", quotient.astype(int))
print("Remainder:", remainder.astype(int))
# Output:
# Quotient: [3 5 6]
# Remainder: [1 0 0]
```

**Related Terms:** nin, frompyfunc()

---

### dtype Conversion

**Definition:** Converting the output of a custom ufunc from object dtype to a proper numeric or string dtype. Necessary because `frompyfunc()` returns object arrays by default.

**Example:**
```python
import numpy as np

def square(x):
    return x ** 2

ufunc = np.frompyfunc(square, 1, 1)
arr = np.array([1, 2, 3, 4, 5])

# Without conversion - object dtype
result_obj = ufunc(arr)
print("Object dtype:", result_obj.dtype)  # object

# With conversion - proper dtype
result_int = ufunc(arr).astype(int)
print("Int dtype:", result_int.dtype)  # int64

result_float = ufunc(arr).astype(float)
print("Float dtype:", result_float.dtype)  # float64
```

**Related Terms:** frompyfunc(), astype()

---

### String Ufunc

**Definition:** A custom ufunc that operates element-wise on string arrays, performing transformations or extractions.

**Example:**
```python
import numpy as np

def extract_domain(email):
    return email.split('@')[1]

domain_ufunc = np.frompyfunc(extract_domain, 1, 1)

emails = np.array(["user@gmail.com", "info@company.org"])
domains = domain_ufunc(emails)
print(domains)
# Output: ['gmail.com' 'company.org']
```

**Related Terms:** np.char.*, String Operations

---

### Data Transformation

**Definition:** A custom ufunc that applies business logic or domain-specific calculations to array elements.

**Example:**
```python
import numpy as np

def tax_bracket(income):
    if income <= 10000:
        return income * 0.10
    elif income <= 40000:
        return 10000 * 0.10 + (income - 10000) * 0.12
    else:
        return 10000 * 0.10 + 30000 * 0.12 + (income - 40000) * 0.22

tax_ufunc = np.frompyfunc(tax_bracket, 1, 1)

incomes = np.array([5000, 25000, 60000])
taxes = tax_ufunc(incomes).astype(float)
print("Taxes:", taxes.round(2))
# Output: [ 500.  3400. 11000.]
```

**Related Terms:** frompyfunc(), Business Logic

---

### Edge Cases

**Definition:** Special inputs that may cause errors or unexpected behavior, such as NaN, None, zero, or negative values. Should be handled in custom functions.

**Example:**
```python
import numpy as np

def safe_divide(x, y):
    if y == 0:
        return np.nan
    return x / y

ufunc = np.frompyfunc(safe_divide, 2, 1)
arr1 = np.array([10, 20, 30])
arr2 = np.array([2, 0, 5])
result = ufunc(arr1, arr2).astype(float)
print(result)
# Output: [ 5. nan  6.]
```

**Related Terms:** NaN Handling, Input Validation

---

### Element-wise Operation

**Definition:** An operation that applies a function to each corresponding element of an array independently. Custom ufuncs enable element-wise operations with custom logic.

**Example:**
```python
import numpy as np

def classify(x):
    return "positive" if x > 0 else "non-positive"

classify_ufunc = np.frompyfunc(classify, 1, 1)

arr = np.array([-5, -1, 0, 1, 5])
result = classify_ufunc(arr)
print(result)
# Output: ['non-positive' 'non-positive' 'non-positive' 'positive' 'positive']
```

**Related Terms:** Vectorization, Broadcasting

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| frompyfunc() | Convert function to ufunc | `np.frompyfunc(func, 1, 1)` |
| nin | Number of inputs | `nin=2` |
| nout | Number of outputs | `nout=1` |
| dtype Conversion | Object to proper type | `.astype(int)` |
| String Ufunc | String element operations | Extract/format strings |
| Data Transform | Business logic | Tax/calculator functions |
| Edge Cases | Special inputs | NaN, None, zeros |

---

**Back to Lecture:** [20 - Creating Custom Ufuncs](20-ufunc-create-lecture.md)
