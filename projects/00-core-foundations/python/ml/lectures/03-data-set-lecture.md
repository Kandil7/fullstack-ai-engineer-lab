# Lecture 03: Working with Datasets

## Topic Overview

Understanding dataset structure is fundamental to machine learning. This lecture covers the anatomy of a dataset — features, targets, samples, and how to organize them for ML algorithms. You'll learn about train/test splitting, Pandas DataFrames for data manipulation, and how to explore and load data from various sources.

A well-structured dataset is the foundation of any ML project. Knowing how to work with data efficiently will save you hours of debugging and produce better models.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Identify and distinguish between features (X) and targets (y)
2. Understand dataset structure (samples, features, targets)
3. Split data into training and test sets properly
4. Use `train_test_split` from scikit-learn with best practices
5. Work with Pandas DataFrames for data manipulation
6. Load datasets from scikit-learn's built-in collections
7. Perform basic data exploration (shape, dtypes, describe)
8. Handle stratified splits for classification problems

---

## Key Concepts

### 1. Dataset Structure

Every ML dataset has a consistent structure:

```
┌─────────────────────────────────────────┐
│              DATASET                     │
├─────────────────────────────────────────┤
│  Features (X)        │  Target (y)      │
│  ─────────────       │  ──────────      │
│  ┌───┬───┬───┬───┐  │  ┌───┐          │
│  │ x1│ x2│ x3│ x4│  │  │ y │          │
│  ├───┼───┼───┼───┤  │  ├───┤          │
│  │   │   │   │   │  │  │   │          │
│  │   │   │   │   │  │  │   │          │
│  └───┴───┴───┴───┘  │  └───┘          │
│  (n_samples,        │  (n_samples,)    │
│   n_features)       │                  │
└─────────────────────────────────────────┘
```

- **Samples (rows):** Individual data points (observations, instances)
- **Features (columns in X):** Input variables used for prediction
- **Target (column y):** Output variable being predicted

### 2. Features vs Targets

| Component | Symbol | Description | Example |
|-----------|--------|-------------|---------|
| Features | X | Input variables | square_feet, bedrooms, age |
| Target | y | Output variable | price |
| Samples | n | Number of data points | 100 houses |

**Convention:** Capital `X` for features (2D matrix), lowercase `y` for target (1D vector).

### 3. Train/Test Split

Why split data?
- **Evaluate generalization:** Test on unseen data
- **Prevent overfitting:** Don't let model memorize training data
- **Get honest performance estimate**

```
Total Dataset
┌───────────────────────────────────────┐
│ Training Set (80%)  │  Test Set (20%) │
│ Used for learning   │  Used for eval  │
└───────────────────────────────────────┘
```

### 4. Pandas DataFrames

Pandas is the standard tool for data manipulation in Python. DataFrames provide:
- Labeled rows and columns
- Easy data selection and filtering
- Built-in statistics and visualization
- Missing data handling
- File I/O (CSV, Excel, SQL, etc.)

---

## Code Examples

### Example 1: Basic Dataset Components

```python
import numpy as np

# Features (X) — 2D array, shape (n_samples, n_features)
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])

# Target (y) — 1D array, shape (n_samples,)
y = np.array([0, 1, 0, 1])

print(f"Features shape: {X.shape}")  # (4, 2)
print(f"Target shape: {y.shape}")     # (4,)
print(f"First sample features: {X[0]}")  # [1, 2]
print(f"First sample target: {y[0]}")     # 0
```

**Explanation:**
- `X` must be 2D — each row is a sample, each column is a feature
- `y` is 1D — one target value per sample
- Shape convention: X is (n_samples, n_features), y is (n_samples,)

### Example 2: Understanding Features and Targets

```python
# House price prediction example
# Features: square_feet, bedrooms, age
house_features = np.array([
    [1500, 3, 10],   # House 1: 1500 sqft, 3 bedrooms, 10 years old
    [2000, 4, 5],    # House 2
    [1200, 2, 15],   # House 3
    [1800, 3, 8]     # House 4
])

# Target: price
house_prices = np.array([300000, 450000, 250000, 400000])

print("Features (X):")
print(house_features)
print("\nTarget (y):")
print(house_prices)
```

### Example 3: Manual Train/Test Split

```python
np.random.seed(42)
X = np.random.rand(100, 2)  # 100 samples, 2 features
y = np.random.randint(0, 2, 100)  # Binary labels

# Simple 80/20 split
split_index = int(0.8 * len(X))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

print(f"Training set: {len(X_train)} samples")  # 80
print(f"Test set: {len(X_test)} samples")        # 20
```

### Example 4: Using train_test_split

```python
from sklearn.model_selection import train_test_split

# Proper split with scikit-learn
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% for testing
    random_state=42      # For reproducibility
)

print(f"Training features: {X_train.shape}")  # (80, 2)
print(f"Test features: {X_test.shape}")        # (20, 2)
print(f"Training targets: {y_train.shape}")    # (80,)
print(f"Test targets: {y_test.shape}")         # (20,)
```

### Example 5: Stratified Split

```python
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000, n_features=10,
    n_informative=5, n_redundant=2,
    random_state=42
)

print(f"Original class distribution: {np.bincount(y)}")

# Without stratify
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Without stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")

# With stratify — maintains class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"With stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")
```

**Explanation:**
- `stratify=y` ensures both train and test sets have the same class proportions
- Critical for imbalanced datasets where one class dominates
- Without stratification, the test set might miss minority class samples

### Example 6: Pandas DataFrame

```python
import pandas as pd

data = {
    'square_feet': [1500, 2000, 1200, 1800, 2200],
    'bedrooms': [3, 4, 2, 3, 4],
    'age': [10, 5, 15, 8, 3],
    'price': [300000, 450000, 250000, 400000, 500000]
}

df = pd.DataFrame(data)
print(df)
#    square_feet  bedrooms  age   price
# 0         1500         3   10  300000
# 1         2000         4    5  450000
# ...
```

### Example 7: DataFrame Operations

```python
print("Shape:", df.shape)           # (5, 4)
print("Columns:", list(df.columns)) # ['square_feet', 'bedrooms', 'age', 'price']
print("\nFirst 3 rows:")
print(df.head(3))

print("\nBasic Statistics:")
print(df.describe())
#        square_feet  bedrooms   age     price
# count     5.000000  5.000000  5.00       5.0
# mean   1740.000000  3.200000  8.20  380000.0
# ...
```

### Example 8: Selecting Features and Targets from DataFrame

```python
# Select feature columns
X = df[['square_feet', 'bedrooms', 'age']].values

# Select target column
y = df['price'].values

print("Features (X):")
print(X[:3])
print("\nTarget (y):")
print(y[:3])
```

### Example 9: Loading sklearn Datasets

```python
from sklearn.datasets import load_iris

iris = load_iris()

# Convert to DataFrame for easy exploration
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target

print("Iris dataset:")
print(iris_df.head())
print(f"\nShape: {iris_df.shape}")  # (150, 5)
print(f"\nFeature names: {iris.feature_names}")
print(f"Target names: {iris.target_names}")
```

### Example 10: Loading from CSV

```python
# Loading data from a CSV file
# df = pd.read_csv('data.csv')

# Separate features and target
# X = df.drop('target_column', axis=1)  # All columns except target
# y = df['target_column']                # Just the target column

# For this example, we'll create a CSV and load it
df.to_csv('houses.csv', index=False)
df_loaded = pd.read_csv('houses.csv')
print(df_loaded.head())
```

---

## Common Mistakes to Avoid

1. **Wrong shape for X** — X must be 2D: use `X.reshape(-1, 1)` for single feature
2. **Not using stratify** — Can cause class imbalance in splits
3. **Scaling before splitting** — Causes data leakage (test statistics leak into training)
4. **Using all data for training** — No way to evaluate generalization
5. **Ignoring data types** — Object columns may need encoding
6. **Not checking for duplicates** — Can bias training and test sets
7. **Forgetting random_state** — Splits won't be reproducible

---

## Best Practices

1. **Always split before any preprocessing** — Fit scalers on training data only
2. **Use stratify for classification** — Especially with imbalanced classes
3. **Set random_state** — For reproducible results
4. **Use 20-30% for test** — Enough to evaluate, not too much to waste training data
5. **Explore data first** — `df.describe()`, `df.info()`, `df.isnull().sum()`
6. **Use Pandas for data loading** — Handles CSV, Excel, SQL, JSON, etc.
7. **Document your splits** — Record the random_state and test_size used

---

## Practice Exercises

### Exercise 1: Feature Matrix
Create a feature matrix X with 100 samples and 5 features. What is the shape? What does each row represent?

### Exercise 2: Manual Split
Given 50 data points, manually split them into 40 training and 10 test samples. Verify the sizes.

### Exercise 3: Stratified Split
Create an imbalanced dataset (90% class 0, 10% class 1). Split with and without `stratify`. Compare class distributions.

### Exercise 4: DataFrame Operations
Create a DataFrame with 10 rows and 4 columns. Use `.describe()` to find the mean of each column. Select rows where column 1 > 0.5.

### Exercise 5: Loading Data
Load the `load_wine` dataset from scikit-learn. How many samples? How many features? What are the target classes?

---

## Summary

| Concept | Description |
|---------|-------------|
| **Features (X)** | Input variables, 2D array (n_samples × n_features) |
| **Target (y)** | Output variable, 1D array (n_samples,) |
| **Train/Test Split** | Separate data for training and evaluation |
| **test_size** | Proportion of data for testing (typically 0.2-0.3) |
| **random_state** | Seed for reproducible splits |
| **stratify** | Maintains class proportions in splits |
| **DataFrame** | Pandas table for data manipulation |
| **.describe()** | Quick statistics for all columns |
| **.head()** | View first N rows |

**Key Takeaway:** Proper dataset structure and splitting are essential for valid ML results. Always separate training and testing data, use stratification for classification, and explore your data before modeling.

---

## Next Lecture

In [Lecture 04: Cleaning Data](04-clean-data-lecture.md), we'll learn how to handle missing values, duplicates, outliers, and data transformation — essential preprocessing steps before any modeling.
