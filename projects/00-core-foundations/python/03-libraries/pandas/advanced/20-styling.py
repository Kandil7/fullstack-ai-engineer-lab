"""
Pandas Styling: DataFrame.style, conditional formatting, export
===============================================================

Beautiful DataFrame presentation for reports and dashboards.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. BASIC STYLING
# =============================================================================

print("=" * 60)
print("1. BASIC STYLING")
print("=" * 60)

# Create sample data
df = pd.DataFrame({
    'Product': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z'],
    'Q1_Sales': [12000, 15000, 8000, 20000, 5000],
    'Q2_Sales': [13000, 14000, 9000, 22000, 6000],
    'Q3_Sales': [11000, 16000, 7000, 19000, 5500],
    'Q4_Sales': [14000, 15500, 8500, 25000, 7000],
    'Growth': [0.15, -0.05, 0.25, 0.30, 0.40],
    'Margin': [0.22, 0.18, 0.35, 0.15, 0.45]
})

# Basic style
styled = df.style
print("Style object created:", type(styled))
print()

# Format numbers
formatted = df.style.format({
    'Q1_Sales': '${:,.0f}',
    'Q2_Sales': '${:,.0f}',
    'Q3_Sales': '${:,.0f}',
    'Q4_Sales': '${:,.0f}',
    'Growth': '{:.1%}',
    'Margin': '{:.1%}'
})
print("Formatted:")
print(formatted.to_string())
print()

# =============================================================================
# 2. CONDITIONAL FORMATTING
# =============================================================================

print("=" * 60)
print("2. CONDITIONAL FORMATTING")
print("=" * 60)

# Highlight max/min
styled_max = df.style.highlight_max(axis=0, color='lightgreen')
styled_min = df.style.highlight_min(axis=0, color='lightcoral')
print("Highlight max (green) and min (red) per column")
print()

# Highlight null
df_nan = df.copy()
df_nan.loc[0, 'Q2_Sales'] = np.nan
styled_null = df_nan.style.highlight_null(null_color='yellow')
print("Highlight null values in yellow")
print()

# Background gradient
styled_grad = df.style.background_gradient(cmap='RdYlGn', subset=['Growth', 'Margin'])
print("Background gradient on Growth and Margin")
print()

# Bar charts in cells
styled_bar = df.style.bar(subset=['Q1_Sales', 'Q2_Sales', 'Q3_Sales', 'Q4_Sales'], 
                          color='#5fba7d', align='zero')
print("Bar charts in numeric cells")
print()

# Heatmap style
styled_heatmap = df.style.background_gradient(cmap='RdYlGn', axis=0)
print("Heatmap style (full DataFrame)")
print()

# =============================================================================
# 3. CUSTOM STYLING FUNCTIONS
# =============================================================================

print("=" * 60)
print("3. CUSTOM STYLING FUNCTIONS")
print("=" * 60)

# Color negative values red, positive green
def color_growth(val):
    if val > 0:
        return 'color: green; font-weight: bold'
    elif val < 0:
        return 'color: red; font-weight: bold'
    return ''

def color_margin(val):
    if val >= 0.3:
        return 'background-color: #d4edda'
    elif val >= 0.2:
        return 'background-color: #fff3cd'
    else:
        return 'background-color: #f8d7da'

styled_custom = df.style.applymap(color_growth, subset=['Growth'])
styled_custom = styled_custom.applymap(color_margin, subset=['Margin'])
print("Custom color functions applied")
print()

# Highlight entire row based on condition
def highlight_top_product(row):
    if row['Q4_Sales'] == df['Q4_Sales'].max():
        return ['background-color: #d4edda'] * len(row)
    return [''] * len(row)

styled_row = df.style.apply(highlight_top_product, axis=1)
print("Row highlighting for top Q4 product")
print()

# Format with custom function
def format_with_arrow(val):
    if val > 0:
        return f'▲ {val:.1%}'
    elif val < 0:
        return f'▼ {val:.1%}'
    return f'{val:.1%}'

styled_format = df.style.format({'Growth': format_with_arrow})
print("Custom formatting with arrows")
print()

# =============================================================================
# 4. TABLE STYLING
# =============================================================================

print("=" * 60)
print("4. TABLE STYLING (CSS)")
print("=" * 60)

# Set table attributes
styled_table = df.style.set_table_attributes('class="table table-striped table-hover"')
print("Bootstrap table classes applied")

# Set caption
styled_caption = df.style.set_caption('Quarterly Sales Report 2023')
print("Caption added")

# Hide index
styled_no_index = df.style.hide(axis='index')
print("Index hidden")

# Set UUID for multiple tables
styled_uuid = df.style.set_uuid('sales_report_2023')
print("UUID set for CSS targeting")

# =============================================================================
# 5. EXPORT TO HTML/EXCEL
# =============================================================================

print("=" * 60)
print("5. EXPORT")
print("=" * 60)

# Export to HTML
html_output = df.style.format({
    'Q1_Sales': '${:,.0f}',
    'Q2_Sales': '${:,.0f}',
    'Q3_Sales': '${:,.0f}',
    'Q4_Sales': '${:,.0f}',
    'Growth': '{:.1%}',
    'Margin': '{:.1%}'
}).background_gradient(cmap='RdYlGn', subset=['Growth', 'Margin']).to_html()

with open('output/styled_report.html', 'w') as f:
    f.write(html_output)
print("HTML exported to output/styled_report.html")

# Export to Excel (requires openpyxl)
try:
    excel_buffer = io.BytesIO()
    df.style.format({
        'Q1_Sales': '${:,.0f}',
        'Q2_Sales': '${:,.0f}',
        'Q3_Sales': '${:,.0f}',
        'Q4_Sales': '${:,.0f}',
        'Growth': '{:.1%}',
        'Margin': '{:.1%}'
    }).to_excel(excel_buffer, engine='openpyxl')
    print("Excel export successful")
except Exception as e:
    print(f"Excel export: {e}")

# =============================================================================
# 6. ADVANCED EXAMPLES
# =============================================================================

print("=" * 60)
print("6. ADVANCED EXAMPLES")
print("=" * 60)

# Example 1: Financial report with sparklines
print("Example 1: Financial Dashboard")
financial = pd.DataFrame({
    'Metric': ['Revenue', 'Cost', 'Gross Profit', 'OpEx', 'EBITDA', 'Net Income'],
    'Actual': [10_000_000, 6_000_000, 4_000_000, 2_500_000, 1_500_000, 1_000_000],
    'Budget': [9_500_000, 5_800_000, 3_700_000, 2_400_000, 1_300_000, 900_000],
    'Variance': [0.053, -0.034, 0.081, -0.042, 0.154, 0.111],
    'Trend': [
        [8, 9, 9.5, 10],
        [5.5, 5.8, 5.9, 6],
        [2.5, 3.0, 3.5, 4],
        [2.2, 2.3, 2.4, 2.5],
        [1.0, 1.1, 1.2, 1.3],
        [0.7, 0.8, 0.9, 1.0]
    ]
})

def variance_color(val):
    if val > 0:
        return 'color: green'
    return 'color: red'

def format_currency(val):
    return f'${val:,.0f}'

financial_style = financial.style.format({
    'Actual': format_currency,
    'Budget': format_currency,
    'Variance': '{:.1%}'
}).applymap(variance_color, subset=['Variance']).bar(
    subset=['Variance'], color=['#f8d7da', '#d4edda'], align='zero'
)

# Add sparkline-like bars for trend
for i, row in financial.iterrows():
    trend = row['Trend']
    sparkline = ''.join(['█' * int((v - min(trend)) / (max(trend) - min(trend)) * 10) for v in trend])
    financial.iloc[i, financial.columns.get_loc('Trend')] = sparkline

print(financial_style.to_string())
print()

# Example 2: ML Model Comparison
print("Example 2: ML Model Comparison")
models = pd.DataFrame({
    'Model': ['Logistic Regression', 'Random Forest', 'XGBoost', 'LightGBM', 'Neural Net'],
    'Accuracy': [0.823, 0.867, 0.891, 0.889, 0.875],
    'Precision': [0.810, 0.855, 0.882, 0.879, 0.865],
    'Recall': [0.835, 0.872, 0.895, 0.892, 0.880],
    'F1': [0.822, 0.863, 0.888, 0.885, 0.872],
    'AUC': [0.890, 0.925, 0.945, 0.942, 0.935],
    'Train_Time': [12, 45, 120, 80, 300]
})

model_style = models.style.format({
    'Accuracy': '{:.1%}',
    'Precision': '{:.1%}',
    'Recall': '{:.1%}',
    'F1': '{:.1%}',
    'AUC': '{:.1%}',
    'Train_Time': '{:.0f}s'
}).background_gradient(cmap='RdYlGn', subset=['Accuracy', 'Precision', 'Recall', 'F1', 'AUC'])\
 .background_gradient(cmap='RdYlGn_r', subset=['Train_Time'])\
 .highlight_max(subset=['Accuracy', 'Precision', 'Recall', 'F1', 'AUC'], color='lightgreen')\
 .highlight_min(subset=['Train_Time'], color='lightgreen')

print(model_style.to_string())
print()

# Example 3: Correlation matrix with annotations
print("Example 3: Annotated Correlation Matrix")
corr_data = pd.DataFrame({
    'Feature_1': np.random.randn(100),
    'Feature_2': np.random.randn(100),
    'Feature_3': np.random.randn(100),
    'Feature_4': np.random.randn(100),
    'Target': np.random.randn(100)
})
corr = corr_data.corr().round(2)

def annotate_corr(val):
    if abs(val) > 0.7:
        return 'background-color: #d4edda; font-weight: bold'
    elif abs(val) > 0.3:
        return 'background-color: #fff3cd'
    return 'background-color: #f8d7da'

corr_style = corr.style.format('{:.2f}').applymap(annotate_corr)
print(corr_style.to_string())
print()

# =============================================================================
# 7. STYLING BEST PRACTICES
# =============================================================================

print("=" * 60)
print("7. BEST PRACTICES")
print("=" * 60)

best_practices = """
1. USE .FORMAT() FOR CONSISTENT NUMBER DISPLAY
2. USE BACKGROUND_GRADIENT FOR QUICK HEATMAPS
3. USE .BAR() FOR IN-CELL VISUALIZATION
4. USE APPLYMAP FOR ELEMENT-WISE CONDITIONAL FORMATTING
5. USE APPLY(AXIS=1) FOR ROW-BASED STYLING
6. CHAIN STYLES: df.style.format().background_gradient().bar()
7. EXPORT TO HTML FOR WEB REPORTS
8. SET TABLE ATTRIBUTES FOR CSS FRAMEWORKS (Bootstrap, etc.)
9. HIDE INDEX WHEN NOT NEEDED
10. USE UUID FOR MULTIPLE TABLES ON SAME PAGE
11. KEEP STYLING LIGHTWEIGHT FOR LARGE DATAFRAMES
12. TEST RENDERING IN TARGET ENVIRONMENT (Jupyter, HTML, Excel)
"""
print(best_practices)

print("\n" + "=" * 60)
print("END OF STYLING")
print("=" * 60)