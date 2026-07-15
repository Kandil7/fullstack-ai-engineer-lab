"""
Unit tests for Pandas examples.
"""

import pytest
import pandas as pd
import numpy as np


class TestPandasBasics:
    """Test Pandas basic functionality."""

    def test_introduction_imports(self):
        """Test that introduction imports work."""
        from pandas.introduction import myseries, mydf

        assert isinstance(myseries, pd.Series)
        assert isinstance(mydf, pd.DataFrame)
        assert len(myseries) == 5
        assert len(mydf) == 3

    def test_series(self):
        """Test Series operations."""
        from pandas.series import s, s_named

        assert s[0] == 10
        assert s_named["b"] == 200
        assert s_named.iloc[0] == 100

    def test_dataframe(self):
        """Test DataFrame operations."""
        from pandas.dataframes import df

        assert df.shape == (4, 4)
        assert list(df.columns) == ["Product", "Price", "Quantity", "In_Stock"]
        assert df["Product"].iloc[0] == "Laptop"

    def test_key_capabilities(self):
        """Test key Pandas capabilities."""
        from pandas.introduction import df_with_nan, df_dropped, df_filled

        assert df_with_nan.isna().sum().sum() == 2
        assert len(df_dropped) == 2
        assert df_filled.isna().sum().sum() == 0

    def test_data_alignment(self):
        """Test data alignment."""
        from pandas.introduction import s1, s2, aligned

        # s1 has index a,b,c; s2 has index b,c,d
        # Alignment should produce NaN for non-matching indices
        assert np.isnan(aligned["a"])
        assert aligned["b"] == 22  # 2 + 20
        assert aligned["c"] == 33  # 3 + 30
        assert np.isnan(aligned["d"])

    def test_series_operations(self):
        """Test Series operations."""
        from pandas.series import s

        assert s.sum() == 150
        assert s.mean() == 30.0
        assert s.max() == 50

    def test_dataframe_operations(self):
        """Test DataFrame operations."""
        from pandas.dataframes import df

        assert df["Price"].sum() == 2446
        assert df["Quantity"].mean() == 22.5
        assert df["In_Stock"].sum() == 3

    def test_reading_json(self):
        """Test reading JSON."""
        from pandas.reading_json import df

        assert len(df) == 3
        assert list(df.columns) == ["Name", "Age", "City"]

    def test_load_data(self):
        """Test loading data."""
        from pandas.load_data import df

        assert len(df) > 0

    def test_data_viewing(self):
        """Test data viewing."""
        from pandas.data_viewing import df

        assert df.shape == (4, 4)

    def test_data_selecting(self):
        """Test data selecting."""
        from pandas.data_selecting import df, laptop, price_qty

        assert laptop["Product"] == "Laptop"
        assert len(price_qty) == 4

    def test_data_loc(self):
        """Test .loc accessor."""
        from pandas.data_loc import df, first_two, laptop_phone

        assert len(first_two) == 2
        assert len(laptop_phone) == 2

    def test_data_drop(self):
        """Test dropping data."""
        from pandas.data_drop import df, df_dropped_col, df_dropped_row

        assert "In_Stock" not in df_dropped_col.columns
        assert len(df_dropped_row) == 3

    def test_rename_columns(self):
        """Test renaming columns."""
        from pandas.rename_columns import df

        assert "Cost" in df.columns
        assert "Count" in df.columns
        assert "Price" not in df.columns

    def test_data_new_column(self):
        """Test adding new column."""
        from pandas.data_new_column import df

        assert "Total_Value" in df.columns
        assert df["Total_Value"].iloc[0] == 9990  # 999 * 10

    def test_clearing_data(self):
        """Test clearing data."""
        from pandas.clearing_data import df, df_filled

        assert df.isna().sum().sum() > 0
        assert df_filled.isna().sum().sum() == 0

    def test_iterating(self):
        """Test iterating over DataFrame."""
        from pandas.iterating import df

        assert len(df) == 4

    def test_statistics(self):
        """Test statistics."""
        from pandas.statistics import df

        assert "mean" in df.describe().index
        assert "std" in df.describe().index

    def test_scatter_plot(self):
        """Test scatter plot creation."""
        from pandas.scatter_plot import df

        assert len(df) == 100

    def test_histogram(self):
        """Test histogram."""
        from pandas.histogram import df

        assert len(df) == 1000

    def test_pie_chart(self):
        """Test pie chart."""
        from pandas.pie_chart import df

        assert len(df) == 4

    def test_bar_chart(self):
        """Test bar chart."""
        from pandas.bar_chart import df

        assert len(df) == 5

    def test_concat(self):
        """Test concatenation."""
        from pandas.concat import result

        assert len(result) == 6

    def test_merge(self):
        """Test merge."""
        from pandas.merge import merged

        assert len(merged) == 3

    def test_groupby(self):
        """Test groupby."""
        from pandas.groupby import grouped

        assert len(grouped) == 3

    def test_corr(self):
        """Test correlation."""
        from pandas.corr import corr_matrix

        assert corr_matrix.shape == (3, 3)

    def test_plotting(self):
        """Test plotting."""
        from pandas.plotting import df

        assert len(df) == 100
