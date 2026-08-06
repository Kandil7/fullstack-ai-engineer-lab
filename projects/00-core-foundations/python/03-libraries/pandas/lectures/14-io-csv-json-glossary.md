# Pandas I/O — Glossary

> Companion reference for the **Pandas I/O** lecture. Reach for it while working
> through `advanced/14-io-csv-json.py`.

## CSV

- **`pd.read_csv(path, ...)`**: Read a delimited text file into a DataFrame.
- **`sep`**: Field delimiter — `","`, `";"`, `"\t"`, or `r"\s+"` for whitespace-delimited.
- **`encoding`**: Text encoding (`"utf-8"`, `"latin-1"`, `"cp1252"`) for legacy files.
- **`parse_dates=[cols]`**: Convert listed columns to `datetime64` on read.
- **`index_col`**: Use a column as the DataFrame index.
- **`dtype={col: type}`**: Force column types — critical for IDs/zips that start with `0`.
- **`na_values=[...]`**: Extra strings to treat as missing.
- **`usecols`**: Read only the needed columns — less memory, faster.
- **`to_csv(path, index=False, ...)`**: Write; pass `index=False` unless the index is meaningful.

## JSON

- **`pd.read_json(path, orient=...)`**: Read JSON; `orient="records"` for a list of dicts.
- **`json_normalize(data, record_path=..., meta=[...])`**: Flatten nested JSON into rows — `record_path` expands an inner array, `meta` keeps sibling fields.
- **Nested payload**: API responses often nest objects and arrays; normalize before analysis.

## Excel

- **`pd.read_excel(path, sheet_name=None|"Name"|0, header=0)`**: Read sheets; `sheet_name=None` returns a dict of all sheets.
- **`pd.ExcelWriter(path)`**: Context manager for writing multiple sheets via `df.to_excel(writer, sheet_name=...)`.
- **`openpyxl`**: Required dependency for reading/writing modern `.xlsx` files.

## Parquet

- **`pd.to_parquet(path, index=False)` / `pd.read_parquet(path)`**: Columnar compressed storage.
- **Columnar format**: Data stored per-column, enabling efficient compression and predicate pushdown.
- **Schema-aware**: Dtypes (datetime, categorical) survive the round-trip losslessly.
- **Use case**: Data lakes, Spark interop, large analytical datasets.

## SQL

- **`sqlalchemy.create_engine(url)`**: DB connection string, e.g. `postgresql+psycopg2://user:pass@host/db`.
- **`pd.read_sql(sql, engine, params={...})`**: Read query results; always use `params` to avoid SQL injection.
- **`pd.read_sql_query` / `pd.read_sql_table`**: Raw SQL vs. whole-table reads.
- **`df.to_sql(name, engine, if_exists="replace|append", index=False)`**: Write a DataFrame to a table.

## Web / Other

- **`pd.read_html(url)`**: Parse all `<table>` elements from a URL into DataFrames.
- **`pd.read_fwf`**: Fixed-width text files.
- **`pd.read_feather` / `pd.read_hdf`**: Feather (fast IPC) and HDF5 formats.
- **`pd.read_stata` / `pd.read_sas`**: Statistical software formats.
