# Matplotlib Lecture 13: Box Plots — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Box Plot | Five-number summary visualization | `plt.boxplot(data)` |
| Median | 50th percentile (Q2) | Line inside box |
| Q1 | 25th percentile (first quartile) | Bottom of box |
| Q3 | 75th percentile (third quartile) | Top of box |
| IQR | Interquartile Range (Q3 - Q1) | Box height |
| Whisker | Lines extending from box | 1.5×IQR range |
| Outlier | Points beyond whiskers | `flierprops` |
| Notch | Indentation at median (CI) | `notch=True` |
| Violin Plot | KDE + box plot hybrid | `plt.violinplot()` |

## Glossary

### B

**Box Plot** — A standardized way of displaying data distribution based on a five-number summary.

### I

**IQR (Interquartile Range)** — The range between Q1 and Q3 (Q3 - Q1). Whiskers extend up to 1.5×IQR beyond the box.

### M

**Median** — The middle value of the dataset when sorted (50th percentile).

### N

**Notch** — A narrowing of the box around the median showing the confidence interval of the median.

### O

**Outlier** — A data point beyond the whiskers (>1.5×IQR from Q1/Q3), shown as individual points.

### Q

**Q1 (First Quartile)** — The 25th percentile; 25% of data falls below this value.

**Q3 (Third Quartile)** — The 75th percentile; 75% of data falls below this value.

### V

**Violin Plot** — A combination of a box plot and a kernel density estimate, showing the full distribution shape.

### W

**Whisker** — Lines extending from the box to the farthest data point within 1.5×IQR.
