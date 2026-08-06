# Matplotlib Lecture 11: Histograms — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Histogram | Distribution of continuous data | `plt.hist(data, bins=30)` |
| Bins | Intervals grouping data values | `bins=20` |
| Density | Normalized histogram | `density=True` |
| Cumulative | Running total | `cumulative=True` |
| 2D Histogram | Two-variable distribution | `plt.hist2d(x, y)` |
| Hexbin | Hexagonal binning | `plt.hexbin(x, y)` |

## Glossary

### B

**Bins** — Non-overlapping intervals that data values are sorted into. More bins = more detail but potentially noisier.

### C

**Cumulative** — A histogram showing the running total (count of values ≤ each bin boundary).

### D

**Density** — A normalized histogram where the total area equals 1, making it comparable to a probability distribution.

### H

**Hexbin** — A 2D histogram using hexagonal bins instead of rectangular, useful for dense scatter data.

**Histogram** — A graphical representation of data distribution by binning values into intervals.

### 2

**2D Histogram** — A histogram showing the joint distribution of two variables.
