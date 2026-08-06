"""
Cleaning Data
W3Schools: https://www.w3schools.com/python/pandas_cleaning_dirty_data.asp

Real-world data is often messy. Pandas provides powerful tools for
handling missing values, duplicates, and inconsistencies.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Sample dirty data
# ---------------------------------------------------------------------------

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", None],
    "Age": [25, -5, 35, 28, 999, 40, 30],
    "Email": [
        "alice@email.com", "bob@", "charlie@email.com",
        "diana@email.com", "not-an-email", "frank@email.com", "grace@email.com",
    ],
    "Salary": [70000, 80000, np.nan, 75000, 65000, np.nan, 82000],
    "Department": ["Engineering", "marketing", "Engineering", "SALES", "Marketing", "engineering", "Sales"],
})

print("Dirty DataFrame:")
print(df)
print()

# ---------------------------------------------------------------------------
# Example 1: Handling missing values
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: Handling Missing Values")
print("=" * 60)

print("Null counts per column:")
print(df.isnull().sum())
print()

# Fill missing names
df["Name"] = df["Name"].fillna("Unknown")
print("After filling missing names:")
print(df[["Name"]])
print()

# Fill missing salaries with the mean
mean_salary = df["Salary"].mean()
df["Salary"] = df["Salary"].fillna(mean_salary)
print(f"Filled missing Salary with mean: ${mean_salary:,.0f}")
print(df[["Name", "Salary"]])
print()

# Drop rows where all values are missing (none here)
df_clean = df.dropna(how="all")
print("After dropping all-NaN rows:")
print(df_clean)
print()

# ---------------------------------------------------------------------------
# Example 2: Fixing invalid values
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Fixing Invalid Values")
print("=" * 60)

# Fix ages: replace negative and impossible values with NaN
df.loc[(df["Age"] < 0) | (df["Age"] > 120), "Age"] = np.nan
df["Age"] = df["Age"].fillna(df["Age"].median())
print("Fixed ages (invalid values replaced with median):")
print(df[["Name", "Age"]])
print()

# ---------------------------------------------------------------------------
# Example 3: String cleaning
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: String Cleaning")
print("=" * 60)

# Normalize department names
df["Department"] = df["Department"].str.strip().str.title()
print("Normalized Department names:")
print(df[["Name", "Department"]])
print()

# Fix email validation
def is_valid_email(email):
    """Simple email validation."""
    if not isinstance(email, str):
        return False
    return "@" in email and "." in email.split("@")[-1]

df["Email_Valid"] = df["Email"].apply(is_valid_email)
print("Email validation:")
print(df[["Name", "Email", "Email_Valid"]])
print()

# Replace invalid emails
df.loc[~df["Email_Valid"], "Email"] = "invalid@email.com"
df = df.drop(columns=["Email_Valid"])
print("After fixing invalid emails:")
print(df[["Name", "Email"]])
print()

# ---------------------------------------------------------------------------
# Example 4: Removing duplicates
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: Removing Duplicates")
print("=" * 60)

df_dup = pd.DataFrame({
    "Product": ["A", "B", "A", "C", "B", "D"],
    "Price": [10, 20, 10, 30, 20, 40],
    "Date": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02",
             "2024-01-01", "2024-01-03"],
})
print("Data with duplicates:")
print(df_dup)
print(f"Shape: {df_dup.shape}")
print()

# Drop exact duplicates
df_no_dup = df_dup.drop_duplicates()
print(f"After drop_duplicates(): {df_no_dup.shape}")
print(df_no_dup)
print()

# Keep last occurrence
df_last = df_dup.drop_duplicates(subset=["Product"], keep="last")
print("Keep last occurrence per Product:")
print(df_last)
print()

# ---------------------------------------------------------------------------
# Example 5: Data type conversion
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Data Type Conversions")
print("=" * 60)

df_types = pd.DataFrame({
    "id": ["1", "2", "3", "4"],
    "amount": ["10.5", "20.3", "30.7", "40.1"],
    "date": ["2024-01-01", "2024-02-15", "2024-03-20", "2024-04-10"],
    "active": ["True", "False", "True", "True"],
})

print("Before conversion:")
print(df_types.dtypes)
print()

df_types["id"] = df_types["id"].astype(int)
df_types["amount"] = df_types["amount"].astype(float)
df_types["date"] = pd.to_datetime(df_types["date"])
df_types["active"] = df_types["active"].map({"True": True, "False": False})

print("After conversion:")
print(df_types.dtypes)
print(df_types)
print()

print("Done!")
