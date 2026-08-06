# Data Cleaning — Glossary

> Companion reference for the **Data Cleaning** lecture. Reach for it while
> working through `advanced/16-data-cleaning.py`.

## dtype Repair

- **`astype(dtype)`**: Convert a column's type (with `errors="coerce"` on `to_numeric`/`to_datetime` to turn junk into `NaN`).
- **`pd.to_datetime(col, errors="coerce")`**: Parse date strings; `errors="coerce"` yields `NaT` on failure.
- **`str.replace(r"[\$,]", "", regex=True)`**: Strip currency symbols/commas before numeric conversion.
- **`.str.zfill(5)`**: Left-pad strings (keeps zip-code leading zeros).
- **`to_numeric(..., errors="coerce")`**: Robust string→number conversion.

## Duplicates

- **`df.duplicated(subset=[...], keep="first")`**: Boolean mask of duplicate rows.
- **`df.drop_duplicates(subset=[...], keep="first")`**: Remove duplicates, keep first occurrence.
- **Dedup key**: A normalized column (lowercased/stripped) used for reliable de-duping.

## Outliers

- **IQR rule**: `q1, q3 = col.quantile([0.25, 0.75])`; outliers beyond `q1 - 1.5*IQR` / `q3 + 1.5*IQR`.
- **`clip(lower=..., upper=...)`**: Winsorize/cap extreme values.
- **Flagging**: `is_outlier` indicator column to keep the information for models.

## Text Normalization

- **`.str.strip()`**: Remove surrounding whitespace.
- **`.str.title()` / `.str.lower()`**: Normalize casing.
- **`Series.replace({old: new})`**: Unify synonyms into canonical labels.
- **`str.split(" ", n=1, expand=True)`**: Split one column into several.

## Missing Values

- **`df.isna().sum() / df.isna().mean()`**: Missing-count / missing-fraction audit.
- **`fillna(value)`**: Fill missing with a chosen value (median, mode, `"unknown"`).
- **`ffill()` / `bfill()`**: Forward/backward fill for time series.
- **`dropna(subset=[...])`**: Drop rows missing critical columns.
- **Rule of thumb**: fill with a justifiable value or drop — never feed `NaN` to a model.

## Pipeline Patterns

- **Idempotent**: Running the clean function twice yields the same result.
- **`df.copy()` first**: Never mutate the caller's DataFrame in place.
- **Clean order**: dtypes → dedupe → text → missing values.
