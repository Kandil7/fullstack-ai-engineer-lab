# Glossary: Working with Datasets

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Feature | Input variable for prediction | Data |
| Target | Output variable being predicted | Data |
| Sample | A single data point | Data |
| Feature Matrix | 2D array of features (X) | Data Structure |
| Target Vector | 1D array of target values (y) | Data Structure |
| Training Set | Data used to train the model | Data Split |
| Test Set | Data used to evaluate the model | Data Split |
| train_test_split | Scikit-learn function for splitting | Tool |
| test_size | Proportion of data for testing | Parameter |
| random_state | Seed for reproducibility | Parameter |
| stratify | Maintain class proportions | Parameter |
| DataFrame | Pandas tabular data structure | Library |
| .describe() | Generate summary statistics | Method |
| .head() | View first N rows | Method |
| .shape | Dimensions of array/DataFrame | Attribute |
| .dtypes | Data types of columns | Attribute |
| .drop() | Remove rows or columns | Method |
| .fillna() | Fill missing values | Method |
| .isnull() | Detect missing values | Method |
| .values | Convert DataFrame to NumPy array | Attribute |

---

## Detailed Definitions

### D

#### DataFrame
**Definition:** A two-dimensional labeled data structure in Pandas, similar to a spreadsheet or SQL table. Columns can have different data types.

**Example:**
```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

print(df)
#       name  age  salary
# 0    Alice   25   50000
# 1      Bob   30   60000
# 2  Charlie   35   70000
```

**Related Terms:** Series, Index, Column, Row

---

### F

#### Feature
**Definition:** An individual measurable property or characteristic of the data used as input for prediction. Also called an attribute, variable, or dimension.

**Example:**
```python
# In house price prediction, these are features:
X = np.array([
    [1500, 3, 10],  # [square_feet, bedrooms, age]
    [2000, 4, 5],
    [1200, 2, 15]
])
# Features: square_feet, bedrooms, age
```

**Related Terms:** Target, Feature Matrix, Feature Engineering

#### Feature Matrix
**Definition:** A 2D NumPy array or Pandas DataFrame where rows represent samples and columns represent features. Conventionally denoted as capital X.

**Example:**
```python
X = np.array([
    [1500, 3, 10],  # Sample 1
    [2000, 4, 5],   # Sample 2
    [1200, 2, 15]   # Sample 3
])
print(f"Shape: {X.shape}")  # (3, 3) — 3 samples, 3 features
```

**Related Terms:** Target Vector, Samples, Features

---

### I

#### Index
**Definition:** The row labels of a Pandas DataFrame or Series. By default, integers starting from 0, but can be any hashable type.

**Example:**
```python
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3]}, index=['x', 'y', 'z'])
print(df)
#    A
# x  1
# y  2
# z  3
print(df.loc['x'])  # Access by label
```

**Related Terms:** DataFrame, Series, .loc, .iloc

---

### N

#### NumPy Array
**Definition:** The fundamental numerical data structure in Python, providing efficient storage and operations for homogeneous arrays of data.

**Example:**
```python
import numpy as np

# 1D array (target vector)
y = np.array([1, 2, 3, 4, 5])

# 2D array (feature matrix)
X = np.array([[1, 2], [3, 4], [5, 6]])

print(f"y shape: {y.shape}")  # (5,)
print(f"X shape: {X.shape}")  # (3, 2)
```

**Related Terms:** DataFrame, Shape, dtype

---

### P

#### Pandas
**Definition:** A Python library providing high-performance, easy-to-use data structures and data analysis tools. The standard for data manipulation in Python.

**Example:**
```python
import pandas as pd

# Create DataFrame
df = pd.read_csv('data.csv')

# Explore
print(df.head())
print(df.describe())
print(df.info())

# Manipulate
df_clean = df.dropna()
df['new_col'] = df['A'] + df['B']
```

**Related Terms:** DataFrame, Series, read_csv, dropna

#### .describe()
**Definition:** A Pandas method that generates descriptive statistics of a DataFrame, including count, mean, std, min, max, and quartiles.

**Example:**
```python
import pandas as pd
df = pd.DataFrame({
    'age': [25, 30, 35, 40, 45],
    'salary': [50000, 60000, 70000, 80000, 90000]
})
print(df.describe())
#              age        salary
# count   5.000000      5.000000
# mean   35.000000  70000.000000
# std     7.905694  15811.388301
# min    25.000000  50000.000000
# ...
```

**Related Terms:** .info(), .head(), .shape

#### .drop()
**Definition:** A Pandas method that removes specified rows or columns from a DataFrame.

**Example:**
```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})

# Drop column
df_dropped = df.drop('C', axis=1)

# Drop row
df_dropped = df.drop(0, axis=0)

# Drop multiple columns
df_dropped = df.drop(['A', 'B'], axis=1)
```

**Related Terms:** .dropna(), .drop_duplicates(), Axis

#### .dropna()
**Definition:** A Pandas method that removes rows (or columns) containing missing values (NaN).

**Example:**
```python
import numpy as np
df = pd.DataFrame({
    'A': [1, np.nan, 3],
    'B': [4, 5, np.nan]
})
print(df)
#      A    B
# 0  1.0  4.0
# 1  NaN  5.0
# 2  3.0  NaN

df_clean = df.dropna()
print(df_clean)
#      A    B
# 0  1.0  4.0
```

**Related Terms:** .fillna(), .isnull(), Missing Values

---

### S

#### Sample
**Definition:** A single observation or data point in a dataset. Also called an instance, record, or row.

**Example:**
```python
# Each row is a sample
X = np.array([
    [1500, 3, 10],  # Sample 1 (house 1)
    [2000, 4, 5],   # Sample 2 (house 2)
    [1200,  2, 15]  # Sample 3 (house 3)
])
print(f"Number of samples: {len(X)}")  # 3
```

**Related Terms:** Feature, Target, Instance, Observation

#### Series
**Definition:** A one-dimensional labeled array in Pandas, representing a single column of data.

**Example:**
```python
import pandas as pd
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s)
# a    10
# b    20
# c    30
print(s['b'])  # 20
```

**Related Terms:** DataFrame, Index, Column

#### Shape
**Definition:** A tuple representing the dimensions of an array or DataFrame. For 2D data: (rows, columns).

**Example:**
```python
import numpy as np
X = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Shape: {X.shape}")  # (2, 3) — 2 rows, 3 columns

import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(f"Shape: {df.shape}")  # (2, 2)
```

**Related Terms:** Dimensions, Rows, Columns, len()

#### stratify
**Definition:** A parameter in `train_test_split` that ensures the split maintains the same class proportions as the original dataset. Essential for imbalanced classification problems.

**Example:**
```python
from sklearn.model_selection import train_test_split
import numpy as np

y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # Imbalanced: 80% class 0

# Without stratify
_, y_test_no_strat = train_test_split(y, test_size=0.3, random_state=42)
print(f"Without stratify: {np.bincount(y_test_no_strat)}")

# With stratify
_, y_test_strat = train_test_split(y, test_size=0.3, stratify=y, random_state=42)
print(f"With stratify: {np.bincount(y_test_strat)}")
```

**Related Terms:** Class Imbalance, train_test_split, random_state

---

### T

#### Target
**Definition:** The output variable that a model is trying to predict. Also called the label, dependent variable, or response variable. Conventionally denoted as lowercase y.

**Example:**
```python
# In house price prediction
y = np.array([300000, 450000, 250000])  # Prices (target)
# In classification
y = np.array([0, 1, 0, 1])  # Class labels (target)
```

**Related Terms:** Feature, Label, Dependent Variable

#### Target Vector
**Definition:** A 1D NumPy array containing the target values for all samples. Conventionally denoted as lowercase y.

**Example:**
```python
y = np.array([300000, 450000, 250000, 400000])
print(f"Shape: {y.shape}")  # (4,)
print(f"Values: {y}")
```

**Related Terms:** Feature Matrix, Target, Labels

#### test_size
**Definition:** A parameter in `train_test_split` that specifies the proportion of the dataset to include in the test split. Typically 0.2 (20%) or 0.3 (30%).

**Example:**
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2  # 20% for testing, 80% for training
)
print(f"Train size: {len(X_train)}")  # 80% of total
print(f"Test size: {len(X_test)}")    # 20% of total
```

**Related Terms:** train_test_split, Training Set, Test Set

#### Training Set
**Definition:** The subset of data used to train a machine learning model. The model learns patterns from this data. Typically 70-80% of the total dataset.

**Example:**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_train, y_train)  # Train on training set
```

**Related Terms:** Test Set, Validation Set, train_test_split

---

### V

#### .values
**Definition:** A Pandas attribute that returns the data as a NumPy array, useful for converting DataFrames for use with scikit-learn.

**Example:**
```python
import pandas as pd
df = pd.DataFrame({
    'square_feet': [1500, 2000],
    'price': [300000, 400000]
})

X = df[['square_feet']].values  # Convert to NumPy
y = df['price'].values

print(type(X))  # <class 'numpy.ndarray'>
print(X.shape)   # (2, 1)
```

**Related Terms:** DataFrame, NumPy, Feature Matrix

---

## Key Attributes and Methods

| Attribute/Method | Description | Example |
|-----------------|-------------|---------|
| `.shape` | Dimensions (rows, cols) | `df.shape` → `(100, 5)` |
| `.dtypes` | Data types per column | `df.dtypes` |
| `.columns` | Column names | `df.columns` |
| `.index` | Row labels | `df.index` |
| `.head(n)` | First n rows | `df.head(5)` |
| `.describe()` | Summary statistics | `df.describe()` |
| `.info()` | Column types and non-null counts | `df.info()` |
| `.values` | Convert to NumPy array | `df.values` |
| `.drop()` | Remove rows/columns | `df.drop('col', axis=1)` |
| `.isnull()` | Detect missing values | `df.isnull().sum()` |
| `.fillna(val)` | Fill missing values | `df.fillna(0)` |

---

## Python Import Cheat Sheet

```python
# NumPy
import numpy as np

# Pandas
import pandas as pd

# Scikit-learn splitting
from sklearn.model_selection import train_test_split

# Built-in datasets
from sklearn.datasets import load_iris, load_wine, load_digits

# Create DataFrame from dict
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

# Load CSV
df = pd.read_csv('data.csv')

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Convert DataFrame to arrays
X = df[['feature1', 'feature2']].values
y = df['target'].values
```
