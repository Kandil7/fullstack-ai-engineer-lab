"""
Pandas Case Study: ML Data Preparation
=======================================

End-to-end feature engineering pipeline for ML models.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

np.random.seed(42)

# =============================================================================
# 1. GENERATE COMPLEX MESSY DATA
# =============================================================================

print("=" * 60)
print("1. COMPLEX MESSY DATA GENERATION")
print("=" * 60)

n = 10000

# Create base data
df = pd.DataFrame({
    'customer_id': range(1, n + 1),
    'age': np.random.randint(18, 80, n),
    'income': np.random.lognormal(10.5, 0.5, n).round(2),
    'credit_score': np.random.randint(300, 850, n),
    'account_balance': np.random.normal(5000, 10000, n).round(2),
    'num_products': np.random.randint(1, 10, n),
    'tenure_months': np.random.randint(0, 240, n),
    'is_active': np.random.choice([0, 1], n, p=[0.2, 0.8]),
    'last_login_days': np.random.exponential(30, n).astype(int),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n),
    'channel': np.random.choice(['Online', 'Branch', 'Phone', 'Mobile'], n),
    'segment': np.random.choice(['Retail', 'Premium', 'Business'], n, p=[0.6, 0.3, 0.1]),
})

# Target
df['churned'] = (
    (df['is_active'] == 0).astype(int) | 
    ((df['last_login_days'] > 90) & (np.random.random(n) < 0.3)).astype(int)
)

# Inject realistic messiness
print("Injecting messiness...")

# 1. Missing values (not completely at random)
missing_mask = np.random.random(n) < 0.15
df.loc[missing_mask, 'income'] = np.nan
df.loc[missing_mask & (df['segment'] == 'Premium'), 'credit_score'] = np.nan

# 2. Outliers
outlier_idx = np.random.choice(n, int(n * 0.02), replace=False)
df.loc[outlier_idx, 'account_balance'] *= 100

# 3. Inconsistent categories
df.loc[np.random.choice(n, 100), 'region'] = 'north'  # lowercase
df.loc[np.random.choice(n, 50), 'channel'] = 'ONLINE'  # uppercase
df.loc[np.random.choice(n, 30), 'segment'] = 'Retail '  # trailing space

# 4. Data type issues
df['age'] = df['age'].astype(str)  # string instead of int
df.loc[np.random.choice(n, 20), 'age'] = 'unknown'

# 5. Duplicate rows
dup_idx = np.random.choice(n, 50, replace=False)
df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)

# 6. Correlated noise features
for i in range(5):
    df[f'noise_feature_{i}'] = df['income'] * np.random.randn(n) * 0.1 + np.random.randn(n)

print(f"Final shape: {df.shape}")
print(f"Missing values:\n{df.isna().sum()}")
print(f"Dtypes:\n{df.dtypes.value_counts()}")
print()

# =============================================================================
# 2. DATA CLEANING PIPELINE
# =============================================================================

print("=" * 60)
print("2. DATA CLEANING PIPELINE")
print("=" * 60)

def clean_pipeline(df):
    """Complete cleaning pipeline."""
    df = df.copy()
    
    # 1. Fix dtypes
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    # 2. Standardize categories
    cat_cols = ['region', 'channel', 'segment']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # 3. Handle missing
    # Numeric: median imputation
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())
    
    # Categorical: mode imputation
    for col in cat_cols:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    
    # 4. Cap outliers (IQR method)
    for col in num_cols:
        if col not in ['customer_id', 'churned']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 3 * IQR
            upper = Q3 + 3 * IQR
            df[col] = df[col].clip(lower, upper)
    
    # 5. Remove duplicates
    df = df.drop_duplicates(subset=[c for c in df.columns if c != 'customer_id'])
    
    # 6. Reset index
    df = df.reset_index(drop=True)
    
    return df

df_clean = clean_pipeline(df)
print(f"Cleaned shape: {df_clean.shape}")
print(f"Missing after cleaning: {df_clean.isna().sum().sum()}")
print()

# =============================================================================
# 3. FEATURE ENGINEERING
# =============================================================================

print("=" * 60)
print("3. FEATURE ENGINEERING")
print("=" * 60)

def create_features(df):
    """Create ML-ready features."""
    df = df.copy()
    
    # Interaction features
    df['income_per_product'] = df['income'] / (df['num_products'] + 1)
    df['balance_per_tenure'] = df['account_balance'] / (df['tenure_months'] + 1)
    df['credit_to_income'] = df['credit_score'] / (df['income'] / 1000 + 1)
    
    # Binned features
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 65, 100], 
                              labels=['GenZ', 'Millennial', 'GenX', 'Boomer', 'Senior'])
    df['income_bracket'] = pd.qcut(df['income'], q=5, labels=['VeryLow', 'Low', 'Medium', 'High', 'VeryHigh'])
    df['balance_tier'] = pd.qcut(df['account_balance'].clip(lower=0), q=4, 
                                  labels=['Low', 'Medium', 'High', 'Premium'])
    
    # Ratio features
    df['active_ratio'] = df['is_active'] / (df['tenure_months'] / 12 + 1)
    df['login_recency_score'] = 1 / (1 + df['last_login_days'])
    
    # Polynomial features (for key numeric)
    df['age_squared'] = df['age'] ** 2
    df['income_log'] = np.log1p(df['income'])
    df['balance_log'] = np.log1p(df['account_balance'].clip(lower=0))
    
    # Regional encoding (target encoding would use target, here just frequency)
    region_freq = df['region'].value_counts(normalize=True)
    df['region_freq'] = df['region'].map(region_freq)
    
    return df

df_feat = create_features(df_clean)
print(f"Features created: {df_feat.shape[1] - df_clean.shape[1]} new columns")
print(f"New columns: {[c for c in df_feat.columns if c not in df_clean.columns]}")
print()

# =============================================================================
# 4. ENCODING CATEGORICAL VARIABLES
# =============================================================================

print("=" * 60)
print("4. CATEGORICAL ENCODING")
print("=" * 60)

from category_encoders import TargetEncoder, CatBoostEncoder

# Prepare for encoding
cat_cols = ['region', 'channel', 'segment', 'age_group', 'income_bracket', 'balance_tier']
cat_cols = [c for c in cat_cols if c in df_feat.columns]

# One-hot encoding (for low cardinality)
df_ohe = pd.get_dummies(df_feat, columns=cat_cols, drop_first=True, dtype=int)
print(f"One-hot encoded shape: {df_ohe.shape}")

# Target encoding (for high cardinality - not needed here but shown)
# target_encoder = TargetEncoder(cols=cat_cols)
# df_target = target_encoder.fit_transform(df_feat[cat_cols], df_feat['churned'])
# print(f"Target encoded shape: {df_target.shape}")

# Frequency encoding
for col in cat_cols:
    freq = df_feat[col].value_counts(normalize=True)
    df_feat[f'{col}_freq'] = df_feat[col].map(freq)

print(f"Frequency encoded columns added: {[f'{c}_freq' for c in cat_cols]}")
print()

# =============================================================================
# 5. SCALING & NORMALIZATION
# =============================================================================

print("=" * 60)
print("5. SCALING & NORMALIZATION")
print("=" * 60)

# Separate features and target
X = df_ohe.drop('churned', axis=1)
y = df_ohe['churned']

# Train/test split first (prevent data leakage!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identify numeric columns
numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
# Exclude binary/one-hot columns (0/1)
binary_cols = [c for c in numeric_cols if X_train[c].nunique() == 2]
scale_cols = [c for c in numeric_cols if c not in binary_cols]

print(f"Total numeric: {len(numeric_cols)}")
print(f"Binary (0/1): {len(binary_cols)}")
print(f"To scale: {len(scale_cols)}")

# StandardScaler
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[scale_cols] = scaler.fit_transform(X_train[scale_cols])
X_test_scaled[scale_cols] = scaler.transform(X_test[scale_cols])

# RobustScaler (alternative for outliers)
robust_scaler = RobustScaler()
X_train_robust = X_train.copy()
X_test_robust = X_test.copy()
X_train_robust[scale_cols] = robust_scaler.fit_transform(X_train[scale_cols])
X_test_robust[scale_cols] = robust_scaler.transform(X_test[scale_cols])

# MinMaxScaler (for neural networks)
minmax_scaler = MinMaxScaler()
X_train_minmax = X_train.copy()
X_test_minmax = X_test.copy()
X_train_minmax[scale_cols] = minmax_scaler.fit_transform(X_train[scale_cols])
X_test_minmax[scale_cols] = minmax_scaler.transform(X_test[scale_cols])

print("Scalers applied: Standard, Robust, MinMax")
print()

# =============================================================================
# 6. FEATURE SELECTION
# =============================================================================

print("=" * 60)
print("6. FEATURE SELECTION")
print("=" * 60)

# Univariate selection (ANOVA F-test for classification)
selector_k = SelectKBest(score_func=f_classif, k=20)
X_train_selected = selector_k.fit_transform(X_train_scaled, y_train)
X_test_selected = selector_k.transform(X_test_scaled)

selected_features = X_train_scaled.columns[selector_k.get_support()]
print(f"Selected {len(selected_features)} features (ANOVA F-test):")
for feat in selected_features:
    score = selector_k.scores_[selector_k.get_support()][list(selected_features).index(feat)]
    print(f"  {feat}: F={score:.2f}")

# Mutual Information
mi_selector = SelectKBest(score_func=mutual_info_classif, k=20)
mi_selector.fit(X_train_scaled, y_train)
mi_features = X_train_scaled.columns[mi_selector.get_support()]
print(f"\nTop 20 by Mutual Information:")
for feat in mi_features:
    score = mi_selector.scores_[mi_selector.get_support()][list(mi_features).index(feat)]
    print(f"  {feat}: MI={score:.4f}")

# Correlation-based removal
corr_matrix = X_train_scaled.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [col for col in upper.columns if any(upper[col] > 0.95)]
print(f"\nHighly correlated features to drop (>0.95): {to_drop}")

# =============================================================================
# 7. DIMENSIONALITY REDUCTION (PCA)
# =============================================================================

print("\n" + "=" * 60)
print("7. PCA FOR DIMENSIONALITY REDUCTION")
print("=" * 60)

pca = PCA(n_components=0.95, random_state=42)  # Keep 95% variance
X_train_pca = pca.fit_transform(X_train_scaled[scale_cols])
X_test_pca = pca.transform(X_test_scaled[scale_cols])

print(f"Original features: {len(scale_cols)}")
print(f"PCA components: {pca.n_components_}")
print(f"Explained variance ratio: {pca.explained_variance_ratio_.sum():.4f}")
print(f"Cumulative variance: {np.cumsum(pca.explained_variance_ratio_)[:10]}")

# =============================================================================
# 8. TRAINING PIPELINE ASSEMBLY
# =============================================================================

print("\n" + "=" * 60)
print("8. COMPLETE ML PIPELINE")
print("=" * 60)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Define column types
numeric_features = scale_cols
categorical_features = [c for c in X_train.columns if c not in numeric_features]

# Preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Full pipeline
ml_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
])

# Cross-validation
cv_scores = cross_val_score(ml_pipeline, X_train, y_train, cv=5, scoring='roc_auc', n_jobs=-1)
print(f"CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

# Fit final pipeline
ml_pipeline.fit(X_train, y_train)

# Feature importance from pipeline
feature_names = (numeric_features + 
                 list(ml_pipeline.named_steps['preprocessor']
                      .named_transformers_['cat']
                      .named_steps['encoder']
                      .get_feature_names_out(categorical_features)))

importances = ml_pipeline.named_steps['classifier'].feature_importances_
feat_imp = pd.DataFrame({'feature': feature_names, 'importance': importances})
feat_imp = feat_imp.sort_values('importance', ascending=False).head(20)
print(f"\nTop 20 Feature Importances:")
print(feat_imp.to_string(index=False))

# =============================================================================
# 9. EXPORT FOR MODEL TRAINING
# =============================================================================

print("\n" + "=" * 60)
print("9. EXPORT PREPARED DATA")
print("=" * 60)

# Save processed datasets
X_train_final = X_train_scaled
X_test_final = X_test_scaled

# Save as parquet (efficient)
output_dir = 'output/ml_ready/'
import os
os.makedirs(output_dir, exist_ok=True)

X_train_final.to_parquet(f'{output_dir}X_train.parquet')
X_test_final.to_parquet(f'{output_dir}X_test.parquet')
y_train.to_parquet(f'{output_dir}y_train.parquet')
y_test.to_parquet(f'{output_dir}y_test.parquet')

# Save preprocessing objects
import joblib
joblib.dump(scaler, f'{output_dir}scaler.joblib')
joblib.dump(preprocessor, f'{output_dir}preprocessor.joblib')
joblib.dump(ml_pipeline, f'{output_dir}full_pipeline.joblib')

print(f"Saved to {output_dir}:")
print(f"  X_train.parquet ({len(X_train_final)} rows)")
print(f"  X_test.parquet ({len(X_test_final)} rows)")
print(f"  y_train.parquet, y_test.parquet")
print(f"  scaler.joblib, preprocessor.joblib, full_pipeline.joblib")

# Save feature metadata
metadata = {
    'feature_names': X_train_final.columns.tolist(),
    'target_name': 'churned',
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'scale_cols': scale_cols,
    'binary_cols': binary_cols,
    'train_shape': X_train_final.shape,
    'test_shape': X_test_final.shape,
    'class_distribution': y_train.value_counts(normalize=True).to_dict(),
    'preprocessing_steps': [
        'dtype_fix', 'category_standardize', 'missing_impute', 
        'outlier_cap', 'deduplicate', 'feature_engineer',
        'encode_categorical', 'scale_numeric', 'select_features'
    ]
}

import json
with open(f'{output_dir}metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2, default=str)

print(f"  metadata.json")

print("\n" + "=" * 60)
print("END OF ML PREP CASE STUDY")
print("=" * 60)