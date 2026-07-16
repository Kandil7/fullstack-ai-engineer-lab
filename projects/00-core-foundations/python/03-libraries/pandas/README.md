# Pandas Tutorial Exercises

Complete, working Python scripts covering every topic in the [W3Schools Pandas Tutorial](https://www.w3schools.com/python/pandas/default.asp).

Each script has 3–5 runnable examples with output comments. Run them directly:

```bash
python 01-introduction.py
```

## Exercises

| # | File | Topic | W3Schools Link |
|---|------|-------|----------------|
| 01 | `01-introduction.py` | What is Pandas, Series, DataFrame basics | [Link](https://www.w3schools.com/python/pandas_intro.asp) |
| 02 | `02-getting-started.py` | Create Series/DataFrames, inspection methods | [Link](https://www.w3schools.com/python/pandas_getting_started.asp) |
| 03 | `03-series.py` | Series creation, indexing, operations | [Link](https://www.w3schools.com/python/pandas_series.asp) |
| 04 | `04-dataframes.py` | DataFrame creation, column access, inspection | [Link](https://www.w3schools.com/python/pandas_dataframes.asp) |
| 05 | `05-load-data.py` | CSV, JSON, Parquet read/write | [Link](https://www.w3schools.com/python/pandas_csv.asp) |
| 06 | `06-reading-json.py` | JSON reading, nested data, orientations | [Link](https://www.w3schools.com/python/pandas_json.asp) |
| 07 | `07-data-viewing.py` | head, tail, info, describe, dtypes | [Link](https://www.w3schools.com/python/pandas_viewing_data.asp) |
| 08 | `08-data-selecting.py` | Column/row selection, boolean indexing | [Link](https://www.w3schools.com/python/pandas_dataframe_loc.asp) |
| 09 | `09-data-loc.py` | loc[] label-based selection, conditional access | [Link](https://www.w3schools.com/python/pandas_dataframe_loc.asp) |
| 10 | `10-data-drop.py` | Drop rows, columns, duplicates, NaN | [Link](https://www.w3schools.com/python/pandas_dataframe_drop.asp) |
| 11 | `11-rename-columns.py` | Rename, prefix/suffix, set_axis | [Link](https://www.w3schools.com/python/pandas_dataframe_rename.asp) |
| 12 | `12-iterating.py` | iterrows, itertuples, apply | [Link](https://www.w3schools.com/python/pandas_dataframe_iterrows.asp) |
| 13 | `13-clearing-data.py` | Clean dirty data, fill NaN, fix types | [Link](https://www.w3schools.com/python/pandas_cleaning_dirty_data.asp) |
| 14 | `14-data-new-column.py` | Add columns, assign, insert, np.where | [Link](https://www.w3schools.com/python/pandas_dataframe_add_column.asp) |
| 15 | `15-statistics.py` | Mean, median, describe, correlation, rolling | [Link](https://www.w3schools.com/python/pandas_stat.asp) |
| 16 | `16-scatter-plot.py` | Scatter plots, trend lines, annotations | [Link](https://www.w3schools.com/python/pandas_plotting_scatter.asp) |
| 17 | `17-histogram.py` | Histograms, KDE, grouped histograms | [Link](https://www.w3schools.com/python/pandas_plotting_hist.asp) |
| 18 | `18-pie-chart.py` | Pie charts, donut, exploded, side-by-side | [Link](https://www.w3schools.com/python/pandas_plotting_pie.asp) |
| 19 | `19-bar-chart.py` | Bar charts, horizontal, stacked, grouped | [Link](https://www.w3schools.com/python/pandas_plotting_bar.asp) |
| 20 | `20-merge.py` | Inner/left/right/outer merge, index merge | [Link](https://www.w3schools.com/python/pandas_dataframe_merge.asp) |
| 21 | `21-concat.py` | Vertical/horizontal concat, keys, pivot | [Link](https://www.w3schools.com/python/pandas_dataframe_concat.asp) |
| 22 | `22-groupby.py` | GroupBy, agg, transform, filter | [Link](https://www.w3schools.com/python/pandas_dataframe_groupby.asp) |
| 23 | `23-corr.py` | Correlation matrix, heatmap, scatter matrix | [Link](https://www.w3schools.com/python/pandas_dataframe_corr.asp) |
| 24 | `24-plotting.py` | Line, area, box, dashboard, dual-axis | [Link](https://www.w3schools.com/python/pandas_plotting.asp) |

## Prerequisites

```bash
pip install pandas numpy matplotlib
```

## How to Use

1. Navigate to this directory
2. Run any script: `python 01-introduction.py`
3. Each script is self-contained and prints results to stdout
4. Plotting scripts (16–19, 23–24) save PNG images to your temp directory

## Topics Covered

- **Basics**: Series, DataFrame, creation from dicts/lists/arrays
- **I/O**: CSV, JSON, Excel, Parquet reading and writing
- **Inspection**: head, tail, info, describe, shape, dtypes
- **Selection**: loc, iloc, boolean indexing, column access
- **Cleaning**: Missing values, duplicates, string cleaning, type conversion
- **Transformation**: Rename, add/drop columns, apply functions
- **Aggregation**: GroupBy, agg, statistics, correlation
- **Visualization**: Scatter, histogram, pie, bar, line, area, box plots, dashboards
- **Combining**: Merge, concat, join, pivot tables
