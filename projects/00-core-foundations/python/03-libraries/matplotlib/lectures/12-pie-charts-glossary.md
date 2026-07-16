# Matplotlib Lecture 12: Pie Charts — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Pie Chart | Proportional parts of a whole | `plt.pie(sizes, labels=labels)` |
| Explode | Separate a slice from center | `explode=(0.1, 0, 0, 0)` |
| Autopct | Percentage label formatting | `autopct='%1.1f%%'` |
| Donut Chart | Pie chart with hole | `wedgeprops={'width': 0.3}` |
| Start Angle | First slice rotation | `startangle=90` |
| Wedge | Individual pie slice | `plt.pie()` returns wedges |

## Glossary

### A

**Autopct** — A format string or function for labeling pie wedges with their percentage value.

### D

**Donut Chart** — A pie chart with a hole in the center, created by setting wedge width < 1.

### E

**Explode** — Pulling one or more slices away from the center for emphasis.

### P

**Pie Chart** — A circular statistical graphic divided into slices representing proportional quantities.

### S

**Start Angle** — The rotation angle of the first pie slice, default 0 (3 o'clock).

### W

**Wedge** — Each individual slice of a pie chart, represented as a `matplotlib.patches.Wedge` object.
