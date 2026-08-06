"""
Pandas I/O: Excel, SQL (Advanced)
==================================

Advanced Excel and SQL operations including multiple sheets, formatting, and database patterns.
"""

import pandas as pd
import numpy as np
import io
import sqlite3
from sqlalchemy import create_engine, text

try:
    import openpyxl  # noqa: F401
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("[skip] openpyxl not installed — pip install openpyxl")

try:
    import xlsxwriter  # noqa: F401
    HAS_XLSXWRITER = True
except ImportError:
    HAS_XLSXWRITER = False
    print("[skip] xlsxwriter not installed — pip install xlsxwriter")

np.random.seed(42)

# =============================================================================
# 1. ADVANCED EXCEL
# =============================================================================

print("=" * 60)
print("1. ADVANCED EXCEL OPERATIONS")
print("=" * 60)

df = pd.DataFrame({
    'Product': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y'] * 25,
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'Sales': np.random.randint(1000, 10000, 100),
    'Date': pd.date_range('2023-01-01', periods=100, freq='D'),
    'Rep': np.random.choice(['Alice', 'Bob', 'Charlie'], 100)
})

if not HAS_OPENPYXL:
    print("[skip] openpyxl not installed — Excel section skipped (pip install openpyxl)")
else:
    # Write with multiple sheets and formatting
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Main data
        df.to_excel(writer, sheet_name='Sales Data', index=False)

        # Pivot table
        pivot = pd.pivot_table(df, values='Sales', index='Product', columns='Region',
                               aggfunc='sum', fill_value=0)
        pivot.to_excel(writer, sheet_name='Pivot by Region')

        # Summary stats
        summary = df.groupby('Product')['Sales'].agg(['sum', 'mean', 'count']).round(2)
        summary.to_excel(writer, sheet_name='Summary')

        # Access worksheet for formatting
        ws = writer.sheets['Sales Data']
        # Auto-filter
        ws.auto_filter.ref = ws.dimensions
        # Freeze panes
        ws.freeze_panes = 'A2'
        # Column widths
        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_length + 2

    print(f"Excel with formatting written: {len(buffer.getvalue())} bytes")
    print()

    # Read with specific options
    df_read = pd.read_excel(buffer, sheet_name='Sales Data',
                            parse_dates=['Date'],
                            dtype={'Product': 'category', 'Region': 'category', 'Rep': 'category'})
    print(f"Read with dtypes: {df_read.dtypes}")
    print()

    # Read multiple sheets
    all_sheets = pd.read_excel(buffer, sheet_name=['Sales Data', 'Pivot by Region', 'Summary'])
    for name, sheet_df in all_sheets.items():
        print(f"  {name}: {sheet_df.shape}")
    print()

# =============================================================================
# 2. EXCEL FORMATTING WITH XLSXWRITER
# =============================================================================

print("=" * 60)
print("2. EXCEL FORMATTING WITH XLSXWRITER")
print("=" * 60)

if not HAS_XLSXWRITER:
    print("[skip] xlsxwriter not installed — formatting section skipped (pip install xlsxwriter)")
else:
    buffer2 = io.BytesIO()
    with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Report', index=False, startrow=1)

        workbook = writer.book
        worksheet = writer.sheets['Report']

        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })

        money_format = workbook.add_format({'num_format': '$#,##0', 'border': 1})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
        default_format = workbook.add_format({'border': 1})

        # Write header
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Set column formats
        worksheet.set_column('A:A', 15, default_format)  # Product
        worksheet.set_column('B:B', 12, default_format)  # Region
        worksheet.set_column('C:C', 12, money_format)    # Sales
        worksheet.set_column('D:D', 12, date_format)     # Date
        worksheet.set_column('E:E', 12, default_format)  # Rep

        # Conditional formatting
        worksheet.conditional_format('C2:C101', {
            'type': '3_color_scale',
            'min_color': '#FF0000',
            'mid_color': '#FFFF00',
            'max_color': '#00FF00'
        })

        # Add chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Sales',
            'categories': '=Report!$A$2:$A$101',
            'values': '=Report!$C$2:$C$101',
        })
        chart.set_title({'name': 'Sales by Product'})
        chart.set_x_axis({'name': 'Product'})
        chart.set_y_axis({'name': 'Sales ($)'})
        worksheet.insert_chart('G2', chart)

    print(f"Formatted Excel written: {len(buffer2.getvalue())} bytes")
    print()

# =============================================================================
# 3. ADVANCED SQL WITH SQLALCHEMY
# =============================================================================

print("=" * 60)
print("3. ADVANCED SQL WITH SQLALCHEMY")
print("=" * 60)

# Create engine with connection pooling
engine = create_engine('sqlite:///:memory:', pool_pre_ping=True, echo=False)

# Write with chunking
df.to_sql('sales', engine, index=False, if_exists='replace', chunksize=1000, method='multi')

# Read with SQLAlchemy
with engine.connect() as conn:
    # Parameterized query
    result = conn.execute(text("SELECT * FROM sales WHERE Region = :region"), {"region": "North"})
    df_north = pd.DataFrame(result.fetchall(), columns=result.keys())
    print(f"Parameterized query (North): {df_north.shape}")
    
    # Complex query with CTE
    complex_query = """
    WITH monthly_sales AS (
        SELECT 
            strftime('%Y-%m', Date) as month,
            Product,
            SUM(Sales) as total_sales
        FROM sales
        GROUP BY month, Product
    )
    SELECT month, Product, total_sales,
           AVG(total_sales) OVER (PARTITION BY Product) as avg_monthly
    FROM monthly_sales
    ORDER BY month, Product
    """
    df_complex = pd.read_sql(complex_query, conn)
    print(f"Complex query with CTE: {df_complex.shape}")
    print(df_complex.head())
    print()

# =============================================================================
# 4. DATABASE PATTERNS
# =============================================================================

print("=" * 60)
print("4. DATABASE PATTERNS")
print("=" * 60)

# Pattern 1: Upsert (Insert or Update)
print("Pattern 1: Upsert with SQLite")
conn = sqlite3.connect(':memory:')
conn.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        last_login TIMESTAMP
    )
""")

# Insert initial data
conn.executemany(
    "INSERT INTO users (id, name, email, last_login) VALUES (?, ?, ?, ?)",
    [(1, 'Alice', 'alice@test.com', '2023-01-01'),
     (2, 'Bob', 'bob@test.com', '2023-01-02')]
)

# Upsert: Insert or Update on conflict
upsert_data = [
    (1, 'Alice Updated', 'alice@test.com', '2023-06-01'),  # Update existing
    (3, 'Charlie', 'charlie@test.com', '2023-06-01')       # Insert new
]

for row in upsert_data:
    conn.execute("""
        INSERT INTO users (id, name, email, last_login)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            name = excluded.name,
            last_login = excluded.last_login
    """, row)

df_users = pd.read_sql("SELECT * FROM users", conn)
print("After upsert:")
print(df_users)
print()

# Pattern 2: Bulk insert with chunksize
print("Pattern 2: Bulk insert performance")
large_data = pd.DataFrame({
    'id': range(10000),
    'value': np.random.randn(10000)
})

import time

# Method 1: to_sql with chunksize
start = time.time()
large_data.to_sql('bulk_test', conn, index=False, if_exists='replace', chunksize=1000, method='multi')
print(f"  to_sql chunksize=1000: {time.time() - start:.4f}s")

# Method 2: Raw executemany
start = time.time()
conn.execute("DELETE FROM bulk_test")
data_tuples = list(large_data.itertuples(index=False, name=None))
conn.executemany("INSERT INTO bulk_test (id, value) VALUES (?, ?)", data_tuples)
print(f"  executemany: {time.time() - start:.4f}s")

# Method 3: copy_from (PostgreSQL only, shown for reference)
# cursor.copy_from(StringIO(csv_data), 'table', sep=',')

# Pattern 3: Read with dtype specification
print("\nPattern 3: Type-safe reads")
# NOTE: 'sales' was written via the SQLAlchemy engine's in-memory DB, not the
# sqlite3 'conn' — read it back through the engine
df_typed = pd.read_sql("SELECT * FROM sales", engine, dtype={
    'Product': 'category',
    'Region': 'category',
    'Rep': 'category'
})
print(f"  Typed read dtypes: {df_typed.dtypes.tolist()}")
print()

# Pattern 4: Streaming large results
print("Pattern 4: Streaming large results")
chunk_size = 5000
total_rows = 0
for chunk in pd.read_sql("SELECT * FROM sales", engine, chunksize=chunk_size):
    total_rows += len(chunk)
    # Process chunk
print(f"  Streamed {total_rows} rows in chunks of {chunk_size}")
print()

# =============================================================================
# 5. CLOUD STORAGE (CONCEPTS)
# =============================================================================

print("=" * 60)
print("5. CLOUD STORAGE PATTERNS (CONCEPTS)")
print("=" * 60)

cloud_patterns = """
# S3 (AWS) - requires s3fs or boto3
import s3fs
fs = s3fs.S3FileSystem()

# Read
df = pd.read_parquet('s3://my-bucket/data/year=2023/month=01/', filesystem=fs)

# Write
df.to_parquet('s3://my-bucket/output/', filesystem=fs, partition_cols=['year', 'month'])

# GCS (Google Cloud) - requires gcsfs
import gcsfs
fs = gcsfs.GCSFileSystem()
df = pd.read_parquet('gs://my-bucket/data/', filesystem=fs)

# Azure Blob - requires adlfs
import adlfs
fs = adlfs.AzureBlobFileSystem(account_name='myaccount', credential='key')
df = pd.read_parquet('az://mycontainer/data/', filesystem=fs)

# Common options:
# - storage_options: dict with credentials
# - filesystem: fsspec filesystem object
# - partition_cols: for partitioned datasets
# - filters: for partition pruning
"""
print(cloud_patterns)

# =============================================================================
# 6. DATA QUALITY CHECKS ON READ
# =============================================================================

print("=" * 60)
print("6. DATA QUALITY ON READ")
print("=" * 60)

# Create test CSV with issues
test_csv = """id,name,age,salary,join_date
1,Alice,30,50000,2020-01-01
2,Bob,25,abc,2020-01-02
3,Charlie,,60000,2020-01-03
4,Diana,35,70000,invalid-date
5,Eve,28,55000,2020-01-05
"""

# Read with error handling
df_qc = pd.read_csv(io.StringIO(test_csv), 
                     na_values=['abc', 'invalid-date', ''],
                     dtype={'id': 'Int64', 'age': 'Int64', 'salary': 'Int64'},
                     parse_dates=['join_date'],
                     on_bad_lines='warn')

print("Data quality read:")
print(df_qc)
print(f"\nDtypes:\n{df_qc.dtypes}")
print(f"\nMissing values:\n{df_qc.isna().sum()}")
print()

# Validate after read
assert df_qc['id'].notna().all(), "ID cannot be null"
assert df_qc['salary'].between(0, 200000).all(), "Salary out of range"
assert df_qc['age'].between(18, 100).all(), "Age out of range"
print("Validation passed!")

print("\n" + "=" * 60)
print("END OF EXCEL & SQL ADVANCED")
print("=" * 60)