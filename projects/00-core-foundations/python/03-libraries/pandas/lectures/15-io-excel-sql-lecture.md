# Pandas I/O: Excel & SQL (Advanced)

> **Topic 15 — Advanced pandas series.** Advanced Excel and SQL patterns:
> multiple sheets, formatting, `ExcelWriter` styling, and production database
> read/write patterns.

Companion exercise: `advanced/15-io-excel-sql.py`

---

## 1. Advanced Excel — Multiple Sheets & Selective Reads

Real reports rarely fit one sheet. `pd.read_excel` handles the mess:

```python
import pandas as pd

# Read ALL sheets into a dict of DataFrames
all_sheets = pd.read_excel("company.xlsx", sheet_name=None)
for name, df in all_sheets.items():
    print(name, df.shape)

# Read specific sheets by name
q1 = pd.read_excel("company.xlsx", sheet_name="Q1")

# Skip junk rows above the header
df = pd.read_excel("company.xlsx", sheet_name="Q1", header=3)

# Only some columns — cheaper when the file is huge
df = pd.read_excel("company.xlsx", sheet_name="Q1", usecols="A:D")
```

## 2. Writing Multi-Sheet Workbooks

```python
with pd.ExcelWriter("report.xlsx") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False)
    monthly.to_excel(writer, sheet_name="Monthly", index=False)
    raw.to_excel(writer, sheet_name="Raw", index=False)
```

The `ExcelWriter` context manager is the canonical pattern: one file, many
sheets, zero cleanup worries.

## 3. Excel Formatting — `openpyxl` Styling

For stakeholder-facing workbooks you can style cells directly:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

wb = Workbook()
ws = wb.active
ws.title = "Summary"

# Write the DataFrame, cell by cell (keeps styling control)
for r_idx, row in enumerate(dataframe_to_rows(summary, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        cell = ws.cell(row=r_idx, column=c_idx, value=value)

# Style the header
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="4F81BD")
    cell.alignment = Alignment(horizontal="center")

wb.save("styled_report.xlsx")
```

## 4. SQL — Read Patterns

```python
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql+psycopg2://user:pass@localhost:5432/db")

# Whole table
df = pd.read_sql_table("orders", engine)

# Parameterized query (SQL-injection safe)
df = pd.read_sql_query(
    "SELECT * FROM orders WHERE region = :r AND amount > :min",
    engine,
    params={"r": "emea", "min": 1000},
)

# Chunked reads for gigantic tables
for chunk in pd.read_sql_query("SELECT * FROM events", engine, chunksize=100_000):
    process(chunk)
```

## 5. SQL — Write Patterns

```python
# Replace or append
df.to_sql("orders_staging", engine, if_exists="replace", index=False)

# Incremental load — append only new rows
new_rows.to_sql("orders", engine, if_exists="append", index=False)

# Round-trip data types: SQLAlchemy infers types from dtypes, but
# you can pin them explicitly
from sqlalchemy.types import BigInteger, DateTime, Float, String, Integer

df.to_sql(
    "orders",
    engine,
    if_exists="replace",
    index=False,
    dtype={
        "order_id": BigInteger,
        "amount": Float,
        "created_at": DateTime,
        "status": String(20),
    },
)
```

**Production tip**: for bulk loads into Postgres, write to a staging table
then `INSERT ... SELECT` — or use the COPY protocol via `psycopg2` for
millions of rows.

## 6. Real-World Use Case — Finance Report Pipeline

```python
# 1. Pull data from the warehouse
orders = pd.read_sql_query(
    "SELECT * FROM orders WHERE created_at >= :start",
    engine,
    params={"start": "2026-01-01"},
)

# 2. Compute KPIs
monthly = orders.groupby(orders["created_at"].dt.to_period("M")).agg(
    revenue=("amount", "sum"), orders=("order_id", "count")
)

# 3. Multi-sheet workbook with styling
with pd.ExcelWriter("finance/monthly_report.xlsx") as writer:
    monthly.to_excel(writer, sheet_name="KPIs", index=True)
    orders.head(100).to_excel(writer, sheet_name="Recent", index=False)
```

## Key Takeaways

1. `sheet_name=None` reads every sheet; `usecols`/`header` tame messy files.
2. `ExcelWriter` + openpyxl give you styled, multi-sheet deliverables.
3. Parameterized `read_sql_query` is the safe, fast way to query databases.
4. Pin `dtype=` on `to_sql` when the inferred types matter downstream.
5. For very large tables: `chunksize=` on read, staging-table writes.
