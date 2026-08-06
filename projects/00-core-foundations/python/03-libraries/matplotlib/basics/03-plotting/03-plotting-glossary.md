# Matplotlib Lecture 03: Basic Plotting — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Format String | Shorthand for color/marker/line | `'r--'` |
| Axis Limits | Data range shown on axis | `plt.xlim(0, 10)` |
| Legend | Labels identifying plot elements | `plt.legend()` |
| Annotation | Text with arrow pointing to data | `plt.annotate()` |
| Grid | Reference lines on the plot | `plt.grid(True)` |
| Ticks | Markers on axis at data values | `plt.xticks()` |
| Log Scale | Logarithmic axis scaling | `plt.semilogx()` |
| Twin Axes | Second y-axis on same plot | `ax.twinx()` |

## Glossary

### A

**Annotation** — Text placed on a plot, often with an arrow pointing to a specific data point.

**Axis Limits** — The range of values shown on each axis (xmin, xmax, ymin, ymax).

### F

**Format String** — A compact way to specify color, marker, and line style: `fmt = '[color][marker][line]'`.

### G

**Grid** — Horizontal and/or vertical reference lines crossing the plot area at tick positions.

### L

**Legend** — A box identifying different data series by their label names.

**Log Scale** — Axis scaling where each major tick represents a power of 10.

### T

**Ticks** — Markers along an axis at specific data values, often with labels.

**Twin Axes** — A second y-axis sharing the same x-axis, useful for data with different scales.
