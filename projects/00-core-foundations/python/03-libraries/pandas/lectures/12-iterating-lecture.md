# Lecture 12: Iterating

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Iterate over DataFrame rows and columns
- Use iterrows() and itertuples() effectively
- Apply functions with apply() and map()
- Understand performance implications of iteration
- Use vectorized operations instead of loops

---

## 📖 1. Why Iterate?

Pandas is designed for vectorized operations, which are much faster than Python loops. However, iteration is sometimes necessary for:

- Complex row-wise operations
- External API calls per row
- Conditional logic that can't be vectorized
- Debugging and inspection

```python
import pandas as pd
import numpy as np

# Vectorized (fast)
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
df["C"] = df["A"] + df["B"]

# Loop (slow)
for i in range(len(df)):
    df.loc[i, "C"] = df.loc[i, "A"] + df.loc[i, "B"]
```

---

## 📖 2. Iterating Over Rows

### iterrows()

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
})

# iterrows() returns (index, Series) pairs
for index, row in df.iterrows():
    print(f"{row['Name']} is {row['Age']} years old from {row['City']}")
# Alice is 28 years old from New York
# Bob is 35 years old from London
# Charlie is 42 years old from Paris
```

### itertuples()

```python
# itertuples() returns named tuples (faster)
for row in df.itertuples():
    print(f"{row.Name} is {row.Age} years old from {row.City}")
# Alice is 28 years old from New York
# Bob is 35 years old from London
# Charlie is 42 years old from Paris
```

### Performance Comparison

```python
import pandas as pd
import numpy as np
import time

# Create large DataFrame
df = pd.DataFrame({
    "A": np.random.randint(0, 100, 100000),
    "B": np.random.randint(0, 100, 100000)
})

# Method 1: iterrows
start = time.time()
for index, row in df.iterrows():
    pass
print(f"iterrows: {time.time() - start:.4f}s")

# Method 2: itertuples
start = time.time()
for row in df.itertuples():
    pass
print(f"itertuples: {time.time() - start:.4f}s")

# Method 3: Vectorized (much faster)
start = time.time()
df["C"] = df["A"] + df["B"]
print(f"vectorized: {time.time() - start:.4f}s")
```

---

## 📖 3. Iterating Over Columns

### Iterating Over Column Names

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35],
    "City": ["New York", "London"]
})

# Iterate over column names
for col in df.columns:
    print(f"Column: {col}, dtype: {df[col].dtype}")
# Column: Name, dtype: object
# Column: Age, dtype: int64
# Column: City, dtype: object
```

### Iterating Over Column Values

```python
# Iterate over each column's values
for col in df.columns:
    print(f"\n{col}:")
    for value in df[col]:
        print(f"  {value}")
```

---

## 📖 4. apply() Method

### Apply Function to Each Column

```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2, 3, 4, 5],
    "B": [10, 20, 30, 40, 50],
    "C": [100, 200, 300, 400, 500]
})

# Apply function to each column
print(df.apply(lambda x: x.max()))
# A      5
# B     50
# C    500

# Apply function to each row
print(df.apply(lambda x: x.sum(), axis=1))
# 0    111
# 1    222
# 2    333
# 3    444
# 4    555
```

### Apply with Custom Function

```python
def classify_age(age):
    if age < 30:
        return "Young"
    elif age < 40:
        return "Middle"
    else:
        return "Senior"

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
})

df["Category"] = df["Age"].apply(classify_age)
print(df)
#       Name  Age Category
# 0    Alice   28    Young
# 1      Bob   35   Middle
# 2  Charlie   42   Senior
# 3    Diana   31   Middle
```

### Apply with Lambda

```python
# Square each value
print(df["Age"].apply(lambda x: x ** 2))

# Conditional
print(df["Age"].apply(lambda x: "Senior" if x >= 35 else "Junior"))
```

---

## 📖 5. map() Method

### Map with Dictionary

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Department": ["Eng", "Mkt", "Eng"]
})

# Map values
dept_mapping = {"Eng": "Engineering", "Mkt": "Marketing", "Sales": "Sales"}
df["Department_Full"] = df["Department"].map(dept_mapping)
print(df)
#       Name Department Department_Full
# 0    Alice        Eng     Engineering
# 1      Bob        Mkt       Marketing
# 2  Charlie        Eng     Engineering
```

### Map with Function

```python
# Map with a function
df["Name_Upper"] = df["Name"].map(lambda x: x.upper())
print(df)
#       Name Department  Name_Upper
# 0    Alice        Eng       ALICE
# 1      Bob        Mkt         BOB
# 2  Charlie        Eng     CHARLIE
```

---

## 📖 6. applymap() (Element-wise)

### Apply to Every Element

```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

# Apply function to every element
# Note: applymap is deprecated, use map instead
df_squared = df.map(lambda x: x ** 2)
print(df_squared)
#    A   B
# 0  1  16
# 1  4  25
# 2  9  36
```

---

## 📖 7. Vectorized vs Iteration

### When to Use Vectorized

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "A": [1, 2, 3, 4, 5],
    "B": [10, 20, 30, 40, 50]
})

# Vectorized — fast
df["C"] = df["A"] + df["B"]
df["D"] = df["A"] * df["B"]
df["E"] = np.where(df["A"] > 3, "High", "Low")
```

### When to Use Iteration

```python
# Complex conditional logic
def complex_calculation(row):
    if row["A"] > 3 and row["B"] < 40:
        return "Special"
    elif row["A"] + row["B"] > 30:
        return "Large"
    else:
        return "Normal"

df["Category"] = df.apply(complex_calculation, axis=1)
```

### Performance Tips

```python
# 1. Use vectorized when possible
df["C"] = df["A"] + df["B"]  # Fast

# 2. Use numpy for math operations
df["D"] = np.sqrt(df["A"])  # Fast

# 3. Use apply() for complex row-wise operations
df["E"] = df.apply(complex_function, axis=1)  # Medium

# 4. Use iterrows() only when necessary
for index, row in df.iterrows():  # Slow
    process(row)
```

---

## 📖 8. Real-World Example

```python
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"],
    "Price": [999, 699, 449, 299, 79],
    "Quantity": [5, 12, 8, 15, 25],
    "Category": ["Electronics", "Electronics", "Electronics", "Peripherals", "Peripherals"]
})

# Vectorized operations
df["Total_Value"] = df["Price"] * df["Quantity"]
df["Price_Category"] = pd.cut(
    df["Price"],
    bins=[0, 100, 500, 1000],
    labels=["Budget", "Mid-Range", "Premium"]
)

# Apply for complex logic
def get_recommendation(row):
    if row["Total_Value"] > 5000:
        return "Bulk Discount Available"
    elif row["Quantity"] > 10:
        return "Volume Pricing"
    else:
        return "Standard Price"

df["Recommendation"] = df.apply(get_recommendation, axis=1)

# Map for categorical mapping
category_map = {
    "Electronics": "Tech",
    "Peripherals": "Accessories"
}
df["Category_Group"] = df["Category"].map(category_map)

print(df)
```

---

## ❌ 9. Common Mistakes

### Mistake 1: Using iterrows() Unnecessarily

```python
# Bad — slow
for index, row in df.iterrows():
    df.loc[index, "C"] = row["A"] + row["B"]

# Good — vectorized
df["C"] = df["A"] + df["B"]
```

### Mistake 2: Modifying During Iteration

```python
# Bad — may cause unexpected behavior
for index, row in df.iterrows():
    df.loc[index, "A"] = row["A"] * 2

# Good — create new column
df["A_doubled"] = df["A"] * 2
```

### Mistake 3: Using applymap() (Deprecated)

```python
# Bad — deprecated
# df.applymap(lambda x: x ** 2)

# Good — use map
df.map(lambda x: x ** 2)
```

---

## ✅ 10. Best Practices

1. **Prefer vectorized operations** — they are much faster
2. **Use numpy for math** — np.sqrt, np.where, etc.
3. **Use apply() for complex logic** — when vectorization isn't possible
4. **Use map() for mapping** — dictionary or function mapping
5. **Use itertuples() over iterrows()** — when iteration is needed
6. **Avoid modifying during iteration** — create new columns instead
7. **Profile performance** — measure before optimizing
8. **Use numba for hot loops** — if iteration is unavoidable

---

## 🏋️ 11. Exercises

### Exercise 1: Basic Iteration

```python
import pandas as pd

# TODO: Create a DataFrame with 10 rows
# TODO: Iterate over rows using iterrows()
# TODO: Iterate over rows using itertuples()
# TODO: Compare performance
```

### Exercise 2: apply() Operations

```python
import pandas as pd

# TODO: Create a DataFrame with numeric columns
# TODO: Use apply() to calculate row-wise statistics
# TODO: Use apply() with custom function
# TODO: Use apply() with lambda
```

### Exercise 3: Vectorized vs Iteration

```python
import pandas as pd
import numpy as np

# TODO: Create a large DataFrame (100K rows)
# TODO: Perform calculation using vectorized operations
# TODO: Perform same calculation using iteration
# TODO: Compare performance
```

---

## 📝 12. Summary

| Method | Purpose | Speed |
|---|---|---|
| Vectorized | Element-wise operations | Fastest |
| apply() | Row/column-wise functions | Medium |
| map() | Element-wise mapping | Fast |
| itertuples() | Row iteration | Medium |
| iterrows() | Row iteration | Slow |

### Next Steps

Congratulations on completing the Pandas lecture series! Continue exploring:

- Advanced groupby operations
- Time series analysis
- Data visualization with Matplotlib/Seaborn
- Machine learning with Scikit-learn

---

## 📚 Further Reading

- [Pandas User Guide: Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)
- [Pandas apply Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html)
- [NumPy Vectorization](https://numpy.org/doc/stable/reference/arrays.nditer.html)
