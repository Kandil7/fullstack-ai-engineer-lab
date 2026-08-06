# Excel & SQL (Advanced) — Glossary

> Companion reference for the **Excel & SQL (Advanced)** lecture. Reach for it
> while working through `advanced/15-io-excel-sql.py`.

## Advanced Excel

- **`sheet_name=None`**: Read **all** sheets into `{sheet_name: DataFrame}`.
- **`sheet_name="Name"` / `sheet_name=0`**: Read one sheet by name or position.
- **`header=3`**: Skip junk rows — data starts at row 4.
- **`usecols="A:D"`**: Read only those columns (letter range) — cheaper on huge files.
- **`pd.ExcelWriter(path)`**: Context manager for writing multiple sheets.
- **`openpyxl`**: Library for reading/writing and **styling** `.xlsx`.
- **`dataframe_to_rows(df, index=False, header=True)`**: Convert a DataFrame to rows for manual cell writing.
- **`Font`, `PatternFill`, `Alignment`**: openpyxl classes for bold/fill/centering.

## SQL Read Patterns

- **`pd.read_sql_table("orders", engine)`**: Read a whole table.
- **`pd.read_sql_query(sql, engine, params={...})`**: Read with a raw SQL string — always pass `params` to avoid injection.
- **`chunksize=100_000`**: Stream a huge result set in chunks; each chunk is a DataFrame.
- **SQLAlchemy engine**: Connection object from `create_engine("dialect+driver://user:pass@host/db")`.

## SQL Write Patterns

- **`df.to_sql(name, engine, if_exists="replace"|"append", index=False)`**: Write a DataFrame to a table.
- **`dtype={col: sqlalchemy.types.X}`**: Pin SQL column types explicitly (`BigInteger`, `DateTime`, `String(20)`, ...).
- **Staging table pattern**: Write to a temp table, then `INSERT ... SELECT` for atomic, auditable loads.
- **COPY protocol**: The fastest Postgres bulk-load path (`psycopg2`/`COPY`), for millions of rows.

## Real-World Patterns

- **KPI workbooks**: aggregate with `groupby(...).agg(...)`, then export multi-sheet `.xlsx` deliverables.
- **Incremental loads**: query by `created_at >= :start`, append only new rows.
- **Column pruning**: `usecols` on read + `usecols` on SQL `SELECT` keep pipelines lean.
