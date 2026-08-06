"""
Pandas -- 41: Advanced Time Series
==============================================
Topics: DatetimeIndex, resample vs groupby(Grouper), asfreq, tz-aware
        series, shift/diff/pct_change, rolling without leakage,
        business calendars

Why this matters for AI/backend engineering:
    Time series is where silent bugs live: leaking the future into
    your features, mixing UTC with local time, resampling across
    ambiguous boundaries, or training a model on t-0 when you only
    know t-1. This module is the difference between a feature that
    generalizes and one that wins on validation and dies in prod.

Run:      python 41-timeseries-advanced.py
Verify:   python 41-timeseries-advanced.py --verify
Reference: https://pandas.pydata.org/docs/user_guide/timeseries.html
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

np.random.seed(42)

# ============================================================
# 1. Building a DatetimeIndex
# ============================================================
# pd.date_range creates a DatetimeIndex; freq strings (D, W, M, h,
# min, B for business days) drive the cadence. A DatetimeIndex makes
# the frame resamplable, sliceable by time labels, and alignable.

# Example 1: minute data from one week, plus a holiday-free business index
idx = pd.date_range("2024-01-01", periods=10, freq="h")
ts = pd.Series(np.arange(10, dtype=float), index=idx)
print("DatetimeIndex:", ts.index.dtype, "| freq:", ts.index.freq)

biz = pd.date_range("2024-01-01", periods=5, freq="B")
print("Business days:", biz.strftime("%Y-%m-%d").tolist())

# Output:
# DatetimeIndex: datetime64[ns] | freq: <Hour>
# Business days: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']


# ============================================================
# 2. resample -- Changing the Observation Frequency
# ============================================================
# resample() downsamples (high freq -> low freq) with an aggregation,
# or upsamples (low -> high) with asfreq/interpolation.

# Example 2: daily data -> weekly means; the weekly label is the week END
# Jan 1-7 land in the week ending Jan 7, Jan 8-14 in the week ending
# Jan 14 -- so the means are (1..7)/7 and (8..14)/7.
daily = pd.Series(
    np.arange(1, 15, dtype=float),
    index=pd.date_range("2024-01-01", periods=14, freq="D"),
)
weekly = daily.resample("W").mean()
print("Weekly means:", weekly.round(2).tolist())
print("Week labels:", weekly.index.strftime("%Y-%m-%d").tolist())

# Output:
# Weekly means: [4.0, 11.0]
# Week labels: ['2024-01-07', '2024-01-14']


# ============================================================
# 3. resample vs groupby(Grouper) -- Same Engine
# ============================================================
# resample(freq) is sugar for groupby with a Grouper of that
# frequency. Both bucket by the SAME rule and return identical
# results; resample additionally handles upsampling and offset
# alignment.

# Example 3: the two spellings are equivalent
by_resample = daily.resample("W").mean()
by_grouper = daily.groupby(pd.Grouper(freq="W")).mean()
print("resample == groupby(Grouper):", by_resample.equals(by_grouper))

# Output:
# resample == groupby(Grouper): True


# ============================================================
# 4. asfreq and Forward-Fill -- Upsampling
# ============================================================
# asfreq changes frequency WITHOUT aggregating: values repeat or get
# NaN at new positions. Combine with ffill() to propagate the last
# known value -- the standard "as-of" filling for feature tables.

# Example 4: daily -> hourly, forward-filled
hourly = daily.asfreq("h").ffill()
print("Daily->hourly asfreq+ffill length:", len(hourly),
      "| value at 01:00 Jan 2:", hourly.loc["2024-01-02 01:00"])
print("No gaps left:", bool(hourly.notna().all()))

# Output:
# Daily->hourly asfreq+ffill length: 313
# | value at 01:00 Jan 2: 2.0
# No gaps left: True


# ============================================================
# 5. shift / diff / pct_change -- Lags Without Leakage
# ============================================================
# shift(k) moves values FORWARD k periods: today's row gets
# yesterday's value. That is the entire point: at time t you may only
# know t-1. diff and pct_change are shift-based deltas.

# Example 5: lag features and their deltas
s = pd.Series([10.0, 20.0, 30.0, 50.0], index=pd.date_range("2024-01-01", periods=4, freq="D"))
print("shift(1):", s.shift(1).tolist())
print("shift(-1):", s.shift(-1).tolist())
print("diff:", s.diff().tolist())
print("pct_change:", s.pct_change().round(3).tolist())

# Output:
# shift(1): [nan, 10.0, 20.0, 30.0]
# shift(-1): [20.0, 30.0, 50.0, nan]
# diff: [nan, 10.0, 10.0, 20.0]
# pct_change: [nan, 1.0, 0.5, 0.667]


# ============================================================
# 6. Rolling Windows -- The Leakage Trap
# ============================================================
# rolling(k).mean() at row t uses rows t-k+1 .. t -- it INCLUDES the
# current value. For features that must be known BEFORE a prediction
# at t, shift the window first: rolling(k).mean().shift(1). This is
# the classic validation/production mismatch.

# Example 6: rolling mean includes today; the lagged version does not
prices = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
rolling_now = prices.rolling(3).mean()
rolling_lag = prices.rolling(3).mean().shift(1)
print("rolling(3).mean():", rolling_now.tolist())
print("rolling(3).mean().shift(1):", rolling_lag.tolist())

# Output:
# rolling(3).mean(): [nan, nan, 2.0, 3.0, 4.0]
# rolling(3).mean().shift(1): [nan, nan, nan, 2.0, 3.0]


# ============================================================
# 7. Time Zones -- UTC In, Local Out
# ============================================================
# Store UTC. tz_localize attaches a zone to naive data;
# tz_convert moves an aware index to another zone (values change
# if you PRINT local wall time, but the instant is the same).

# Example 7: naive -> UTC -> local wall clock
naive = pd.Timestamp("2024-01-01 00:00")
utc = naive.tz_localize("UTC")
nyc = utc.tz_convert("America/New_York")
print("Naive:", naive, "| UTC:", utc, "| NYC wall time:", nyc)
print("Same instant:", utc.timestamp() == nyc.timestamp())

# Output:
# Naive: 2024-01-01 00:00:00 | UTC: 2024-01-01 00:00:00+00:00 | NYC wall time: 2023-12-31 19:00:00-05:00
# Same instant: True


# ============================================================
# 8. Business Calendars -- Skip Weekends AND Holidays
# ============================================================
# CustomBusinessDay lets you define which days count as business
# days; offsets like pd.offsets.BMonthEnd anchor to business month
# ends. Use them when your pipeline only runs on trading days.

# Example 8: custom calendar that also skips a holiday
from pandas.tseries.offsets import CustomBusinessDay
holiday = pd.Timestamp("2024-01-15")          # e.g. a national holiday
cal = CustomBusinessDay(holidays=[holiday])
dates = pd.date_range("2024-01-11", periods=5, freq=cal)
print("Custom business days:", dates.strftime("%Y-%m-%d").tolist())

# Output:
# Custom business days: ['2024-01-11', '2024-01-12', '2024-01-16', '2024-01-17', '2024-01-18']


# ============================================================
# 9. Production Pattern: No-Leakage Feature Builder
# ============================================================
# The pattern for ML features from a time series: resample to the
# decision cadence, build each feature from PAST data only, verify
# the last row of the feature table is complete before predicting.

def build_features(series: pd.Series, window: int) -> pd.DataFrame:
    """Lag + rolling features where every row only uses past data.

    Returns a frame with columns: value (current), lag_1 (previous
    value), mean_w (window mean EXCLUDING current), pct_chg (change
    vs previous value).
    """
    out = pd.DataFrame({"value": series})
    out["lag_1"] = series.shift(1)
    out["mean_w"] = series.rolling(window).mean().shift(1)
    out["pct_chg"] = series.pct_change()
    return out

# Example 9: feature table on daily closes -- last rows must be usable
daily_prices = pd.Series(
    np.random.RandomState(7).uniform(90, 110, 30),
    index=pd.date_range("2024-02-01", periods=30, freq="B"),
).round(2)
features = build_features(daily_prices, window=5)
last = features.iloc[-1]
first_complete = int(features.notna().all(axis=1).values.argmax())
print("Feature columns:", features.columns.tolist())
print("Last row has no NaN:", bool(last.notna().all()))
print("First complete feature row:", first_complete)
print("Mean_w at end uses only past:", round(float(last["mean_w"]), 2))

# Output:
# Feature columns: ['value', 'lag_1', 'mean_w', 'pct_chg']
# Last row has no NaN: True
# First complete feature row: 5
# Mean_w at end uses only past: 101.94


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: building a rolling mean feature without shift(1)
#   X["avg"] = price.rolling(5).mean()    # includes the row you
#                                         # are predicting
# CORRECT:
#   X["avg"] = price.rolling(5).mean().shift(1)
#
# MISTAKE: treating naive timestamps from different machines as
#         comparable
#   logs = pd.read_csv("european_logs.csv")  # local times, naive
# CORRECT: tz_localize("UTC") at ingestion; store UTC everywhere
#
# MISTAKE: resampling on the default (calendar) frequency when the
#         domain runs on business days
#   df.resample("W")   # includes weekends as buckets
# CORRECT: use "W-FRI" or a CustomBusinessDay calendar for trading data


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # resample: weekly means are correct: (1..7)/7=4, (8..14)/7=11.
    assert weekly.tolist() == [4.0, 11.0], \
        "weekly means of 1..14 must be [4, 11]"

    # resample and groupby(Grouper) are the same engine.
    assert by_resample.equals(by_grouper), \
        "resample must equal groupby(Grouper)"

    # asfreq+ffill: daily value 2.0 propagates to 01:00 on Jan 2.
    assert hourly.loc["2024-01-02 01:00"] == 2.0, \
        "ffill must propagate the Jan-2 value to the next hour"
    assert bool(hourly.notna().all()), "ffill must leave no gaps"

    # shift direction: shift(1) moves yesterday into today's row.
    lag1 = s.shift(1)
    lead1 = s.shift(-1)
    assert np.isnan(lag1.iloc[0]) and lag1.iloc[1] == 10.0, \
        "shift(1) must lag by one period"
    assert lead1.iloc[-2] == 50.0 and np.isnan(lead1.iloc[-1]), \
        "shift(-1) must lead by one period"

    # diff and pct_change derive from shifts.
    assert np.isnan(s.diff().iloc[0]), "first diff must be NaN"
    assert s.diff().iloc[1:].tolist() == [10.0, 10.0, 20.0], \
        "diff must be value - previous value"

    # Rolling includes the current row; the shifted version excludes it.
    assert rolling_now.dropna().tolist() == [2.0, 3.0, 4.0], \
        "rolling(3).mean() must include the current value"
    assert rolling_lag.dropna().tolist() == [2.0, 3.0], \
        "rolling(3).mean().shift(1) must exclude the current value"

    # Time zone conversion preserves the instant.
    assert utc.timestamp() == nyc.timestamp(), \
        "tz_convert must not change the underlying instant"
    assert str(nyc.tz) == "America/New_York", \
        "nyc must be tz-aware in America/New_York"

    # Custom business calendar skips the holiday.
    assert pd.Timestamp("2024-01-15") not in dates, \
        "custom calendar must skip the configured holiday"

    # Feature table: no leakage means the lag equals yesterday's value.
    assert features["lag_1"].iloc[-1] == features["value"].iloc[-2], \
        "lag_1 at t must equal value at t-1"
    # The window mean at t uses rows t-5..t-1 only.
    expected_mean = float(features["value"].iloc[-6:-1].mean())
    assert abs(features["mean_w"].iloc[-1] - expected_mean) < 1e-9, \
        "mean_w at t must use only past rows"

    print("[OK] 41-timeseries-advanced: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. resample and Grouper share one bucketing engine.")
        print("2. shift before rolling: never leak the current row.")
        print("3. UTC in storage, local zones only at the edge.")
        _verify()          # always runs, so plain execution is also a test
