"""
Pandas Data Cleaning: Real-world ETL patterns
==============================================

Comprehensive data cleaning techniques for production ML pipelines.
"""

import pandas as pd
import numpy as np
import re

np.random.seed(42)

# =============================================================================
# 1. CREATE MESSY REAL-WORLD DATA
# =============================================================================

print("=" * 60)
print("1. MESSY SAMPLE DATA")
print("=" * 60)

# Simulate real-world messy data
n = 1000
messy_df = pd.DataFrame({
    'customer_id': ['CUST-001', 'CUST-002', 'CUST-003', 'CUST-004', 'CUST-005'] * 200,
    'name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'] * 200,
    'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com', 'diana@email.com', 'eve@email.com'] * 200,
    'phone': ['+1-555-123-4567', '(555) 987-6543', '555.111.2222', '555-333-4444', '555 555 5555'] * 200,
    'address': ['123 Main St, NYC, NY 10001', '456 Oak Ave, LA, CA 90001', '789 Pine Rd, Chicago, IL 60601', '321 Elm Blvd, Houston, TX 77001', '555 Cedar Ln, Phoenix, AZ 85001'] * 200,
    'age': [25, 30, 35, 28, 42] * 200,
    'income': ['$50,000', '$75,000', '$100,000', '$60,000', '$90,000'] * 200,
    'signup_date': ['2020-01-15', '2019-06-22', '2021-03-10', '2022-02-01', '2018-11-30'] * 200,
    'last_login': ['2023-01-15 10:30:00', '2023-01-14 08:15:00', '2023-01-13 14:22:00', '2023-01-12 09:45:00', '2023-01-11 16:30:00'] * 200,
    'is_active': ['Yes', 'No', 'Yes', 'Yes', 'No'] * 200,
    'tags': ['premium,active', 'basic,inactive', 'premium,active,vip', 'basic,active', 'premium,inactive'] * 200,
})

# Add realistic messiness
messy_df.loc[10:15, 'email'] = np.nan
messy_df.loc[20:25, 'phone'] = 'invalid'
messy_df.loc[30:35, 'income'] = '$'
messy_df.loc[40:45, 'age'] = -5
messy_df.loc[50:55, 'signup_date'] = 'not-a-date'
messy_df.loc[60:65, 'customer_id'] = 'DUPLICATE'
messy_df.loc[70:75, 'name'] = '  john doe  '  # whitespace, case issues

print("Messy DataFrame:")
print(messy_df.head(10))
print(f"\nShape: {messy_df.shape}")
print(f"Dtypes:\n{messy_df.dtypes}")
print(f"\nMissing:\n{messy_df.isna().sum()}")
print()

# =============================================================================
# 2. DATA TYPE CLEANING
# =============================================================================

print("=" * 60)
print("2. DATA TYPE CLEANING")
print("=" * 60)

df = messy_df.copy()

# Clean income: remove $ and commas, convert to numeric
df['income_clean'] = (df['income']
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .replace('', np.nan)
    .astype('Int64')
)
print("Income cleaning:")
print(df[['income', 'income_clean']].head(10))
print()

# Clean phone: extract digits
df['phone_digits'] = df['phone'].str.replace(r'\D', '', regex=True)
df['phone_clean'] = df['phone_digits'].apply(
    lambda x: f"+1-{x[:3]}-{x[3:6]}-{x[6:]}" if len(x) == 10 else np.nan
)
print("Phone cleaning:")
print(df[['phone', 'phone_digits', 'phone_clean']].head(10))
print()

# Clean age: handle negative values
df['age_clean'] = df['age'].where(df['age'] > 0, np.nan).astype('Int64')
print("Age cleaning:")
print(df[['age', 'age_clean']].head(10))
print()

# Clean dates
df['signup_date_clean'] = pd.to_datetime(df['signup_date'], errors='coerce')
df['last_login_clean'] = pd.to_datetime(df['last_login'], errors='coerce')
print("Date cleaning:")
print(df[['signup_date', 'signup_date_clean']].head(10))
print()

# Clean boolean
df['is_active_clean'] = df['is_active'].map({'Yes': True, 'No': False, 'true': True, 'false': False, '1': True, '0': False})
print("Boolean cleaning:")
print(df[['is_active', 'is_active_clean']].head(10))
print()

# Clean customer_id
df['customer_id_clean'] = df['customer_id'].str.upper().str.strip()
print("Customer ID cleaning:")
print(df[['customer_id', 'customer_id_clean']].head(10))
print()

# Clean name (title case, strip)
df['name_clean'] = df['name'].str.strip().str.title()
print("Name cleaning:")
print(df[['name', 'name_clean']].head(10))
print()

# =============================================================================
# 3. MISSING VALUE HANDLING
# =============================================================================

print("=" * 60)
print("3. MISSING VALUE HANDLING")
print("=" * 60)

# Analyze missing
print("Missing value analysis:")
missing_pct = df.isna().mean() * 100
print(missing_pct[missing_pct > 0].round(2))
print()

# Strategy 1: Drop rows with critical missing
critical_cols = ['customer_id_clean', 'email', 'signup_date_clean']
df_dropped = df.dropna(subset=critical_cols)
print(f"After dropping critical missing: {len(df_dropped)} rows (was {len(df)})")
print()

# Strategy 2: Fill with appropriate values
df_filled = df.copy()
# Fill income with median
df_filled['income_clean'] = df_filled['income_clean'].fillna(df_filled['income_clean'].median())
# Fill age with median
df_filled['age_clean'] = df_filled['age_clean'].fillna(df_filled['age_clean'].median())
# Fill phone with 'Unknown'
df_filled['phone_clean'] = df_filled['phone_clean'].fillna('Unknown')
# Fill is_active with False (conservative)
df_filled['is_active_clean'] = df_filled['is_active_clean'].fillna(False)

print("After filling:")
print(df_filled[['income_clean', 'age_clean', 'phone_clean', 'is_active_clean']].isna().sum())
print()

# Strategy 3: Add missing indicator columns (for ML)
for col in ['income_clean', 'age_clean', 'phone_clean']:
    df_filled[f'{col}_was_missing'] = df[col].isna().astype(int)

print("Missing indicators added:")
print(df_filled[['income_clean_was_missing', 'age_clean_was_missing']].head(10))
print()

# =============================================================================
# 4. DUPLICATE HANDLING
# =============================================================================

print("=" * 60)
print("4. DUPLICATE HANDLING")
print("=" * 60)

# Find duplicates
dupes = df_filled.duplicated(subset=['customer_id_clean'], keep=False)
print(f"Duplicate customer_ids: {dupes.sum()}")

# Keep first
df_deduped = df_filled.drop_duplicates(subset=['customer_id_clean'], keep='first')
print(f"After dedup (keep first): {len(df_deduped)} rows")
print()

# Keep last
df_deduped_last = df_filled.drop_duplicates(subset=['customer_id_clean'], keep='last')
print(f"After dedup (keep last): {len(df_deduped_last)} rows")
print()

# Custom dedup: keep row with most complete data
completeness = df_filled.notna().sum(axis=1)
df_filled['completeness'] = completeness
df_best = df_filled.sort_values('completeness', ascending=False).drop_duplicates(subset=['customer_id_clean'], keep='first')
print(f"After dedup (most complete): {len(df_best)} rows")
print()

# =============================================================================
# 5. OUTLIER DETECTION & HANDLING
# =============================================================================

print("=" * 60)
print("5. OUTLIER DETECTION & HANDLING")
print("=" * 60)

# IQR method
Q1 = df_best['income_clean'].quantile(0.25)
Q3 = df_best['income_clean'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_iqr = df_best[(df_best['income_clean'] < lower_bound) | (df_best['income_clean'] > upper_bound)]
print(f"IQR outliers in income: {len(outliers_iqr)}")
print(f"  Bounds: [{lower_bound:.0f}, {upper_bound:.0f}]")
print()

# Z-score method
z_scores = np.abs((df_best['income_clean'] - df_best['income_clean'].mean()) / df_best['income_clean'].std())
outliers_z = df_best[z_scores > 3]
print(f"Z-score (>3) outliers in income: {len(outliers_z)}")
print()

# Isolation Forest (for multivariate)
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.01, random_state=42)
numeric_cols = df_best.select_dtypes(include=[np.number]).columns
df_numeric = df_best[numeric_cols].fillna(df_best[numeric_cols].median())
outlier_pred = iso.fit_predict(df_numeric)
outliers_iso = df_best[outlier_pred == -1]
print(f"Isolation Forest outliers: {len(outliers_iso)}")
print()

# Handle outliers: cap (winsorize)
df_capped = df_best.copy()
df_capped['income_capped'] = df_capped['income_clean'].clip(lower=lower_bound, upper=upper_bound)
print(f"Original income range: [{df_best['income_clean'].min()}, {df_best['income_clean'].max()}]")
print(f"Capped income range: [{df_capped['income_capped'].min()}, {df_capped['income_capped'].max()}]")
print()

# =============================================================================
# 6. INCONSISTENCY RESOLUTION
# =============================================================================

print("=" * 60)
print("6. INCONSISTENCY RESOLUTION")
print("=" * 60)

# Text standardization
df_clean = df_capped.copy()

# Standardize tags
def standardize_tags(tag_str):
    if pd.isna(tag_str):
        return ''
    tags = [t.strip().lower() for t in tag_str.split(',')]
    # Map synonyms
    tag_map = {'vip': 'premium', 'basic': 'standard'}
    tags = [tag_map.get(t, t) for t in tags]
    # Remove duplicates, sort
    tags = sorted(set(tags))
    return ','.join(tags)

df_clean['tags_clean'] = df_clean['tags'].apply(standardize_tags)
print("Tag standardization:")
print(df_clean[['tags', 'tags_clean']].head(10))
print()

# Fuzzy matching for names
from difflib import get_close_matches

# Create reference list
known_names = df_clean['name_clean'].unique()
# Find potential typos
def find_typos(name, reference, threshold=0.8):
    if pd.isna(name):
        return name
    matches = get_close_matches(name, reference, n=1, cutoff=threshold)
    return matches[0] if matches else name

df_clean['name_fuzzy'] = df_clean['name_clean'].apply(lambda x: find_typos(x, known_names))
print("Fuzzy name matching:")
print(df_clean[['name_clean', 'name_fuzzy']].head(10))
print()

# =============================================================================
# 7. FEATURE ENGINEERING FROM CLEAN DATA
# =============================================================================

print("=" * 60)
print("7. FEATURE ENGINEERING")
print("=" * 60)

df_feat = df_clean.copy()

# Date features
df_feat['signup_year'] = df_feat['signup_date_clean'].dt.year
df_feat['signup_month'] = df_feat['signup_date_clean'].dt.month
df_feat['signup_dayofweek'] = df_feat['signup_date_clean'].dt.dayofweek
df_feat['days_since_signup'] = (pd.Timestamp.now() - df_feat['signup_date_clean']).dt.days
df_feat['days_since_login'] = (pd.Timestamp.now() - df_feat['last_login_clean']).dt.days

# Income features
df_feat['income_log'] = np.log1p(df_feat['income_clean'])
df_feat['income_bracket'] = pd.qcut(df_feat['income_clean'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# Age features
df_feat['age_group'] = pd.cut(df_feat['age_clean'], bins=[0, 25, 35, 50, 100], labels=['Gen Z', 'Millennial', 'Gen X', 'Boomer'])

# Engagement features
df_feat['is_recently_active'] = (df_feat['days_since_login'] < 30).astype(int)
df_feat['has_phone'] = df_feat['phone_clean'].ne('Unknown').astype(int)

# Tag features
df_feat['tag_count'] = df_feat['tags_clean'].apply(lambda x: len(x.split(',')) if x else 0)
for tag in ['premium', 'active', 'standard', 'inactive']:
    df_feat[f'has_{tag}'] = df_feat['tags_clean'].str.contains(tag).astype(int)

print("Engineered features:")
print(df_feat[['customer_id_clean', 'signup_year', 'income_bracket', 'age_group', 
               'days_since_signup', 'is_recently_active', 'tag_count', 'has_premium']].head(10))
print()

# =============================================================================
# 8. VALIDATION PIPELINE
# =============================================================================

print("=" * 60)
print("8. VALIDATION PIPELINE")
print("=" * 60)

from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

class DataValidator:
    """Production data validation class."""
    
    def __init__(self, df):
        self.df = df
        self.errors = []
        self.warnings = []
    
    def check_not_null(self, columns):
        for col in columns:
            null_count = self.df[col].isna().sum()
            if null_count > 0:
                self.errors.append(f"{col}: {null_count} null values")
        return self
    
    def check_range(self, column, min_val=None, max_val=None):
        if min_val is not None:
            violations = (self.df[column] < min_val).sum()
            if violations:
                self.errors.append(f"{column}: {violations} values below {min_val}")
        if max_val is not None:
            violations = (self.df[column] > max_val).sum()
            if violations:
                self.errors.append(f"{column}: {violations} values above {max_val}")
        return self
    
    def check_unique(self, column):
        dupes = self.df[column].duplicated().sum()
        if dupes:
            self.errors.append(f"{column}: {dupes} duplicate values")
        return self
    
    def check_dtype(self, column, expected_type):
        actual = str(self.df[column].dtype)
        if expected_type not in actual:
            self.warnings.append(f"{column}: expected {expected_type}, got {actual}")
        return self
    
    def check_regex(self, column, pattern):
        invalid = ~self.df[column].astype(str).str.match(pattern)
        count = invalid.sum()
        if count:
            self.errors.append(f"{column}: {count} values don't match pattern {pattern}")
        return self
    
    def validate(self):
        if self.errors:
            raise ValueError(f"Validation failed:\n" + "\n".join(self.errors))
        if self.warnings:
            print(f"Warnings:\n" + "\n".join(self.warnings))
        print("All validations passed!")
        return self

# Run validation
try:
    validator = DataValidator(df_feat)
    validator.check_not_null(['customer_id_clean', 'email', 'signup_date_clean'])
    validator.check_range('age_clean', 18, 100)
    validator.check_range('income_clean', 0, 1000000)
    validator.check_unique('customer_id_clean')
    validator.check_dtype('signup_date_clean', 'datetime')
    validator.check_regex('email', r'.+@.+\..+')
    validator.validate()
except ValueError as e:
    print(e)

print("\n" + "=" * 60)
print("END OF DATA CLEANING")
print("=" * 60)