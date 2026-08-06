# Pandas I/O: CSV, JSON, Excel, Parquet, SQL, HTML

> **Topic 14 — Advanced pandas series.** Reading and writing data in every
> format a real pipeline touches, with the options that actually matter.

Companion exercise: `advanced/14-io-csv-json.py`

---

## 1. CSV — The Default Exchange Format

CSV is everywhere: exports, Kaggle datasets, log dumps. The defaults work for
clean files; real files need the extras:

```python
import pandas as pd

df = pd.read_csv(
    "sales.csv",
    sep=",",                # or ";" (European exports), "\t" (TSV)
    encoding="utf-8",       # try "latin-1" or "cp1252" for legacy files
    parse_dates=["date"],   # turn date strings into datetime64
    index_col="id",         # use a column as the index
    dtype={"zip": str},     # stop pandas from eating leading zeros
    na_values=["", "N/A", "unknown"],
    usecols=["id", "date", "amount"],   # read only what you need
)
```

**Why `dtype` matters**: `zip` codes and IDs often start with `0`; pandas would
infer `int` and destroy them. Declare `str`.

Writing back:

```python
df.to_csv("out.csv", index=False, encoding="utf-8")
```

Always pass `index=False` unless the index carries meaning — otherwise you get
a surprise `Unnamed: 0` column on re-read.

## 2. JSON — Nested Data

JSON comes in two flavors:

```python
# Records: [{...}, {...}] — one dict per row
df = pd.read_json("users.json", orient="records")

# Nested — explode into columns with json_normalize
from pandas import json_normalize

df = json_normalize(
    payload["results"],
    record_path="purchases",          # nested array to expand
    meta=["name", "email", ["address", "city"]],  # fields to keep alongside
)
```

`json_normalize` is the workhorse for API responses with nested lists — it
flattens `{"user": {"name": "Ada"}, "orders": [...]}` into a tidy table.

## 3. Excel — Multiple Sheets & Formatting

```python
# Read every sheet
sheets = pd.read_excel("report.xlsx", sheet_name=None)  # dict of DataFrames

# Read one sheet by name or position
df = pd.read_excel("report.xlsx", sheet_name="Q1", header=0)

# Write multiple sheets
with pd.ExcelWriter("report.xlsx") as writer:
    q1.to_excel(writer, sheet_name="Q1", index=False)
    q2.to_excel(writer, sheet_name="Q2", index=False)
```

Requires `openpyxl` (write + modern read) or `xlrd` (legacy `.xls`).

## 4. Parquet — The Production Workhorse

Parquet is **columnar, compressed, and schema-aware** — the standard for data
lakes, Spark, and fast local analytics:

```python
df.to_parquet("data.parquet", index=False)
df = pd.read_parquet("data.parquet")
```

- 10–100× smaller than CSV (Snappy/Zstd compression).
- Preserves dtypes exactly — datetimes and categoricals survive round-trips.
- Only readable by other Parquet-aware tools, not spreadsheets.

## 5. SQL — Databases

```python
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql+psycopg2://user:pass@host:5432/db")

# Read
df = pd.read_sql("SELECT * FROM orders WHERE created_at > '2026-01-01'", engine)
# Or with parameters (SQL injection safe)
df = pd.read_sql(
    "SELECT * FROM orders WHERE region = :region",
    engine,
    params={"region": "emea"},
)

# Write
df.to_sql("orders_staging", engine, if_exists="replace", index=False)
```

`pd.read_sql_query` for raw SQL, `pd.read_sql_table` for whole tables.
`to_sql` chunks by default — good for large frames.

## 6. HTML & Other Formats

```python
# Scrape tables out of a web page
tables = pd.read_html("https://example.com/league-table")
df = tables[0]  # each <table> becomes a DataFrame
```

Other readers: `read_excel`/`to_excel` (covered), `read_feather`, `read_hdf`,
`read_stata`, `read_sas`, `read_fwf` (fixed-width text).

## 7. Real-World Use Case — Cross-Format ETL

```python
# 1. Landing zone: raw CSV from a partner
raw = pd.read_csv("partner_export.csv", dtype={"customer_id": str})

# 2. Enrich with a JSON API dump
api = json_normalize(load("api_response.json")["data"], record_path="orders",
                     meta=["customer_id", "tier"])

# 3. Merge into a clean table
clean = raw.merge(api, on="customer_id", how="left")

# 4. Store for the analytics stack
clean.to_parquet("warehouse/customers.parquet", index=False)

# 5. Publish a curated Excel report for stakeholders
with pd.ExcelWriter("reports/customers.xlsx") as writer:
    clean.to_excel(writer, sheet_name="overview", index=False)
    clean.groupby("tier").size().to_excel(writer, sheet_name="tiers")
```

## Key Takeaways

1. `read_csv` extras (`dtype`, `parse_dates`, `na_values`) are mandatory for
   production data — never trust defaults on real files.
2. `json_normalize` flattens nested API payloads; `read_html` scrapes tables.
3. Parquet is the storage format of choice for analytics workloads.
4. `read_sql` with `params=` is the safe way to talk to databases.
5. `index=False` on every write, unless the index is real data.
