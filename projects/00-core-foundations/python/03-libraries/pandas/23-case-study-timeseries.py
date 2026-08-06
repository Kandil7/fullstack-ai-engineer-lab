"""
Pandas Case Study: Time Series Forecasting Preparation
=======================================================

Preparing time series data for forecasting models (ARIMA, Prophet, ML).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

np.random.seed(42)

# =============================================================================
# 1. GENERATE TIME SERIES DATA
# =============================================================================

print("=" * 60)
print("1. TIME SERIES DATA GENERATION")
print("=" * 60)

# Create realistic daily sales data with trend, seasonality, noise
dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
n = len(dates)

# Components
trend = np.linspace(100, 500, n)  # Upward trend
yearly_seasonal = 50 * np.sin(2 * np.pi * np.arange(n) / 365.25)  # Yearly
weekly_seasonal = 20 * np.sin(2 * np.pi * np.arange(n) / 7)  # Weekly
noise = np.random.randn(n) * 10

# Combine
sales = trend + yearly_seasonal + weekly_seasonal + noise
sales = np.maximum(sales, 0)  # No negative sales

ts_df = pd.DataFrame({
    'date': dates,
    'sales': sales
}).set_index('date')

print(f"Time series shape: {ts_df.shape}")
print(f"Date range: {ts_df.index.min()} to {ts_df.index.max()}")
print(f"Frequency: {ts_df.index.freq}")
print()

# Plot
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
ts_df['sales'].plot(ax=axes[0], title='Daily Sales (Raw)')
pd.Series(trend + yearly_seasonal + weekly_seasonal, index=dates).plot(
    ax=axes[1], title='Trend + Seasonality', color='orange'
)
pd.Series(trend, index=dates).plot(ax=axes[2], title='Trend', color='green')
pd.Series(yearly_seasonal + weekly_seasonal, index=dates).plot(ax=axes[3], title='Seasonality', color='red')
plt.tight_layout()
os.makedirs('output', exist_ok=True)
plt.savefig('output/ts_components.png', dpi=150)
plt.close()

# =============================================================================
# 2. STATIONARITY CHECK
# =============================================================================

print("=" * 60)
print("2. STATIONARITY TESTING (ADF)")
print("=" * 60)

def check_stationarity(series, name='Series'):
    """Perform Augmented Dickey-Fuller test."""
    result = adfuller(series.dropna())
    print(f"{name} ADF Test:")
    print(f"  ADF Statistic: {result[0]:.4f}")
    print(f"  p-value: {result[1]:.6f}")
    print(f"  Critical Values: {result[4]}")
    if result[1] < 0.05:
        print(f"  Result: STATIONARY (reject null)")
    else:
        print(f"  Result: NON-STATIONARY (fail to reject null)")
    print()

check_stationarity(ts_df['sales'], 'Original Sales')

# First difference
ts_df['sales_diff1'] = ts_df['sales'].diff().dropna()
check_stationarity(ts_df['sales_diff1'], 'First Difference')

# Log transform + difference
ts_df['sales_log'] = np.log1p(ts_df['sales'])
ts_df['sales_log_diff1'] = ts_df['sales_log'].diff().dropna()
check_stationarity(ts_df['sales_log_diff1'], 'Log + First Difference')

# =============================================================================
# 3. SEASONAL DECOMPOSITION
# =============================================================================

print("=" * 60)
print("3. SEASONAL DECOMPOSITION")
print("=" * 60)

# Additive decomposition
decomposition_add = seasonal_decompose(ts_df['sales'], model='additive', period=365)
# Multiplicative decomposition
decomposition_mul = seasonal_decompose(ts_df['sales'], model='multiplicative', period=365)

# Extract components
ts_df['trend_add'] = decomposition_add.trend
ts_df['seasonal_add'] = decomposition_add.seasonal
ts_df['residual_add'] = decomposition_add.resid

ts_df['trend_mul'] = decomposition_mul.trend
ts_df['seasonal_mul'] = decomposition_mul.seasonal
ts_df['residual_mul'] = decomposition_mul.resid

# Plot decomposition
fig, axes = plt.subplots(4, 1, figsize=(12, 10))
ts_df['sales'].plot(ax=axes[0], title='Original', legend=False)
ts_df['trend_add'].plot(ax=axes[1], title='Trend (Additive)', legend=False, color='green')
ts_df['seasonal_add'].plot(ax=axes[2], title='Seasonal (Additive)', legend=False, color='orange')
ts_df['residual_add'].plot(ax=axes[3], title='Residual (Additive)', legend=False, color='red')
plt.tight_layout()
plt.savefig('output/ts_decomposition.png', dpi=150)
plt.close()

# Strength of seasonality
seasonal_strength = 1 - np.var(ts_df['residual_add'].dropna()) / np.var((ts_df['seasonal_add'] + ts_df['residual_add']).dropna())
trend_strength = 1 - np.var(ts_df['residual_add'].dropna()) / np.var((ts_df['trend_add'] + ts_df['residual_add']).dropna())
print(f"Seasonal Strength: {seasonal_strength:.4f}")
print(f"Trend Strength: {trend_strength:.4f}")
print()

# =============================================================================
# 4. AUTOCORRELATION ANALYSIS
# =============================================================================

print("=" * 60)
print("4. AUTOCORRELATION (ACF/PACF)")
print("=" * 60)

# Plot ACF/PACF for differenced series
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(ts_df['sales_diff1'].dropna(), lags=40, ax=axes[0], title='ACF - First Difference')
plot_pacf(ts_df['sales_diff1'].dropna(), lags=40, ax=axes[1], title='PACF - First Difference', method='ywm')
plt.tight_layout()
plt.savefig('output/ts_acf_pacf.png', dpi=150)
plt.close()

# Seasonal ACF
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(ts_df['sales_diff1'].dropna(), lags=60, ax=axes[0], title='ACF - Seasonal Lags')
# Highlight seasonal lags (7, 14, 21, 28, 35, 42, 365...)
for lag in [7, 14, 21, 28, 35, 42, 365]:
    if lag <= 60:
        axes[0].axvline(x=lag, color='red', linestyle='--', alpha=0.5)
plot_pacf(ts_df['sales_diff1'].dropna(), lags=60, ax=axes[1], title='PACF - Seasonal Lags', method='ywm')
plt.tight_layout()
plt.savefig('output/ts_acf_pacf_seasonal.png', dpi=150)
plt.close()

print("ACF/PACF plots saved for ARIMA parameter selection")
print()

# =============================================================================
# 5. FEATURE ENGINEERING FOR ML FORECASTING
# =============================================================================

print("=" * 60)
print("5. FEATURE ENGINEERING FOR ML")
print("=" * 60)

ml_df = ts_df.copy()

# Lag features
for lag in [1, 7, 14, 28, 365]:
    ml_df[f'lag_{lag}'] = ml_df['sales'].shift(lag)

# Rolling statistics
for window in [7, 14, 30]:
    ml_df[f'roll_mean_{window}'] = ml_df['sales'].rolling(window).mean()
    ml_df[f'roll_std_{window}'] = ml_df['sales'].rolling(window).std()
    ml_df[f'roll_min_{window}'] = ml_df['sales'].rolling(window).min()
    ml_df[f'roll_max_{window}'] = ml_df['sales'].rolling(window).max()

# Expanding statistics
ml_df['expanding_mean'] = ml_df['sales'].expanding().mean()
ml_df['expanding_std'] = ml_df['sales'].expanding().std()

# Date features
ml_df['year'] = ml_df.index.year
ml_df['month'] = ml_df.index.month
ml_df['day'] = ml_df.index.day
ml_df['dayofweek'] = ml_df.index.dayofweek
ml_df['dayofyear'] = ml_df.index.dayofyear
ml_df['weekofyear'] = ml_df.index.isocalendar().week
ml_df['quarter'] = ml_df.index.quarter
ml_df['is_weekend'] = ml_df.index.dayofweek.isin([5, 6]).astype(int)
ml_df['is_month_start'] = ml_df.index.is_month_start.astype(int)
ml_df['is_month_end'] = ml_df.index.is_month_end.astype(int)

# Cyclical encoding for periodic features
ml_df['month_sin'] = np.sin(2 * np.pi * ml_df['month'] / 12)
ml_df['month_cos'] = np.cos(2 * np.pi * ml_df['month'] / 12)
ml_df['dayofweek_sin'] = np.sin(2 * np.pi * ml_df['dayofweek'] / 7)
ml_df['dayofweek_cos'] = np.cos(2 * np.pi * ml_df['dayofweek'] / 7)
ml_df['dayofyear_sin'] = np.sin(2 * np.pi * ml_df['dayofyear'] / 365)
ml_df['dayofyear_cos'] = np.cos(2 * np.pi * ml_df['dayofyear'] / 365)

# Difference features
ml_df['diff_1'] = ml_df['sales'].diff(1)
ml_df['diff_7'] = ml_df['sales'].diff(7)
ml_df['diff_365'] = ml_df['sales'].diff(365)

# Percentage change
ml_df['pct_change_1'] = ml_df['sales'].pct_change(1)
ml_df['pct_change_7'] = ml_df['sales'].pct_change(7)

# Drop NaN
ml_df_clean = ml_df.dropna()

print(f"Original shape: {ts_df.shape}")
print(f"Feature matrix shape: {ml_df_clean.shape}")
print(f"Features: {len(ml_df_clean.columns) - 1} (excluding target)")
print()

# Feature columns (excluding target and intermediate columns)
feature_cols = [c for c in ml_df_clean.columns if c not in ['sales', 'sales_diff1', 'sales_log', 'sales_log_diff1',
                                                             'trend_add', 'seasonal_add', 'residual_add',
                                                             'trend_mul', 'seasonal_mul', 'residual_mul']]

X = ml_df_clean[feature_cols]
y = ml_df_clean['sales']

print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
print()

# =============================================================================
# 6. TRAIN/TEST SPLIT (TIME SERIES)
# =============================================================================

print("=" * 60)
print("6. TIME SERIES TRAIN/TEST SPLIT")
print("=" * 60)

# Time-based split (not random!)
split_date = '2023-06-01'
train_mask = ml_df_clean.index < split_date
test_mask = ml_df_clean.index >= split_date

X_train = X[train_mask]
X_test = X[test_mask]
y_train = y[train_mask]
y_test = y[test_mask]

print(f"Train: {len(X_train)} samples ({X_train.index.min()} to {X_train.index.max()})")
print(f"Test:  {len(X_test)} samples ({X_test.index.min()} to {X_test.index.max()})")
print()

# Walk-forward validation splits
n_splits = 5
split_dates = pd.date_range('2022-01-01', '2023-06-01', periods=n_splits + 1)

print("Walk-forward validation splits:")
for i, (start, end) in enumerate(zip(split_dates[:-1], split_dates[1:])):
    train_end = end - pd.Timedelta(days=1)
    test_start = end
    test_end = split_dates[i+2] if i+2 < len(split_dates) else ml_df_clean.index.max()
    
    train_size = len(ml_df_clean[(ml_df_clean.index >= start) & (ml_df_clean.index <= train_end)])
    test_size = len(ml_df_clean[(ml_df_clean.index >= test_start) & (ml_df_clean.index <= test_end)])
    
    print(f"  Fold {i+1}: Train {start.date()} to {train_end.date()} ({train_size}), "
          f"Test {test_start.date()} to {test_end.date()} ({test_size})")

# =============================================================================
# 7. BASELINE MODELS
# =============================================================================

print("=" * 60)
print("7. BASELINE FORECASTING MODELS")
print("=" * 60)

from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_model(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    print(f"{name}: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%")
    return mae, rmse, mape

# Baseline 1: Naive (last value)
naive_pred = np.full(len(y_test), y_train.iloc[-1])
evaluate_model(y_test, naive_pred, "Naive (Last Value)")

# Baseline 2: Seasonal Naive (same day last week)
seasonal_naive = y_train.iloc[-7:].values
seasonal_pred = np.tile(seasonal_naive, len(y_test) // 7 + 1)[:len(y_test)]
evaluate_model(y_test, seasonal_pred, "Seasonal Naive (Weekly)")

# Baseline 3: Seasonal Naive (same day last year)
seasonal_naive_year = y_train.iloc[-365:].values
seasonal_pred_year = np.tile(seasonal_naive_year, len(y_test) // 365 + 1)[:len(y_test)]
evaluate_model(y_test, seasonal_pred_year, "Seasonal Naive (Yearly)")

# Baseline 4: Moving Average
ma_pred = np.full(len(y_test), y_train.rolling(7).mean().iloc[-1])
evaluate_model(y_test, ma_pred, "Moving Average (7-day)")

# Baseline 5: Linear Trend
x_train = np.arange(len(y_train))
x_test = np.arange(len(y_train), len(y_train) + len(y_test))
coeff = np.polyfit(x_train, y_train.values, 1)
trend_pred = np.polyval(coeff, x_test)
evaluate_model(y_test, trend_pred, "Linear Trend")

# Baseline 6: Trend + Seasonal (additive)
# Remove trend, forecast seasonal, add trend back
detrended = y_train - np.polyval(coeff, x_train)
# Average seasonal pattern (weekly)
seasonal_pattern = detrended.groupby(detrended.index.dayofweek).mean()
seasonal_forecast = [seasonal_pattern[d] for d in y_test.index.dayofweek]
trend_seasonal_pred = trend_pred + seasonal_forecast
evaluate_model(y_test, trend_seasonal_pred, "Trend + Weekly Seasonal")

print()

# =============================================================================
# 8. ML MODEL (RANDOM FOREST) - QUICK DEMO
# =============================================================================

print("=" * 60)
print("8. ML MODEL QUICK DEMO (RANDOM FOREST)")
print("=" * 60)

from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import RegressorChain

# Quick train (subset for speed)
sample_size = min(5000, len(X_train))
X_train_sample = X_train.iloc[-sample_size:]
y_train_sample = y_train.iloc[-sample_size:]

rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_train_sample, y_train_sample)

# Predict
rf_pred = rf.predict(X_test)

evaluate_model(y_test, rf_pred, "Random Forest")

# Feature importance
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop 15 Feature Importances:")
print(importances.head(15).to_string())
print()

# =============================================================================
# 9. FORECASTING WITH PROPHET (CONCEPT)
# =============================================================================

print("=" * 60)
print("9. PROPHET FORECASTING (CONCEPT)")
print("=" * 60)

prophet_code = """
# Install: pip install prophet
from prophet import Prophet

# Prepare data (Prophet needs 'ds' and 'y' columns)
prophet_df = ts_df.reset_index()
prophet_df.columns = ['ds', 'y']

# Train
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    seasonality_mode='additive',
    changepoint_prior_scale=0.05
)
model.fit(prophet_df)

# Future dataframe
future = model.make_future_dataframe(periods=90)  # 90 days forecast

# Predict
forecast = model.predict(future)

# Plot
model.plot(forecast)
model.plot_components(forecast)

# Evaluate on test set
# ... cross-validation with prophet.diagnostics.cross_validation
"""
print(prophet_code)

# =============================================================================
# 10. PRODUCTION FORECASTING PIPELINE
# =============================================================================

print("=" * 60)
print("10. PRODUCTION PIPELINE CHECKLIST")
print("=" * 60)

checklist = """
PRODUCTION TIME SERIES FORECASTING CHECKLIST
=============================================

DATA PREPARATION:
[ ] Handle missing timestamps (resample, interpolate)
[ ] Remove outliers (cap, winsorize, or model robustly)
[ ] Check stationarity (ADF, KPSS tests)
[ ] Identify seasonality periods (ACF, domain knowledge)
[ ] Create train/test split (time-based, not random!)
[ ] Define forecast horizon (1 day, 7 days, 30 days, etc.)

FEATURE ENGINEERING:
[ ] Lag features (1, 7, 14, 30, 365 days)
[ ] Rolling statistics (mean, std, min, max, quantiles)
[ ] Expanding statistics
[ ] Date features (year, month, dayofweek, etc.)
[ ] Cyclical encoding for periodic features
[ ] Holiday/event indicators
[ ] External regressors (weather, promotions, etc.)

MODEL SELECTION:
[ ] Statistical: ARIMA, SARIMA, ETS, TBATS
[ ] Prophet (good for business time series with holidays)
[ ] ML: Random Forest, XGBoost, LightGBM, Linear Regression
[ ] Deep Learning: LSTM, GRU, Transformer, N-BEATS
[ ] Ensemble multiple models

VALIDATION:
[ ] Walk-forward validation (expanding window)
[ ] Blocked cross-validation
[ ] Metrics: MAE, RMSE, MAPE, SMAPE, MASE
[ ] Backtesting on historical data
[ ] Residual analysis (autocorrelation, normality)

MONITORING:
[ ] Prediction drift detection
[ ] Feature drift detection
[ ] Performance degradation alerts
[ ] Automated retraining triggers
[ ] A/B testing framework

DEPLOYMENT:
[ ] Model serialization (joblib, pickle, ONNX)
[ ] API endpoint for predictions
[ ] Batch vs real-time inference
[ ] Caching for repeated predictions
[ ] Fallback to baseline models
"""
print(checklist)

print("\n" + "=" * 60)
print("END OF TIME SERIES CASE STUDY")
print("=" * 60)