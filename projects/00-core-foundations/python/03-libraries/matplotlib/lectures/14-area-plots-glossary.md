# Matplotlib Lecture 14: Area Plots — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Area Plot | Filled line chart | `plt.fill_between(x, y, 0)` |
| Stacked Area | Layers on top of each other | `plt.stackplot(x, *values)` |
| `stackplot()` | Stacked area chart | `stackplot(x, y1, y2)` |
| Baseline | Reference line for fill | `fill_between(..., 0)` |
| Cumulative | Running total over time | `np.cumsum(values)` |

## Glossary

### A

**Area Plot** — A line plot with the area between the line and baseline filled with color.

### B

**Baseline** — The reference value (usually 0) from which the fill extends upward/downward.

### S

**Stacked Area** — Multiple area plots stacked on top of each other, showing both individual and total values.

**stackplot()** — A specialized function for creating stacked area charts with automatic baseline handling.
