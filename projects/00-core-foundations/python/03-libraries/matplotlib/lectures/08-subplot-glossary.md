# Matplotlib Lecture 08: Subplots — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Subplot | Individual axes in a grid | `plt.subplot(2, 3, 1)` |
| `subplots()` | Create figure + grid | `fig, axes = plt.subplots(2, 2)` |
| GridSpec | Unequal subplot layout | `GridSpec(3, 3)` |
| Shared Axes | Linked x or y limits | `sharex=True, sharey=True` |
| Inset | Small axes inside another | `fig.add_axes([0.1, 0.1, 0.3, 0.3])` |
| Flat Index | 1D iteration over 2D grid | `for ax in axes.flat:` |
| Height Ratio | Relative row heights | `height_ratios=[2, 1]` |
| Width Ratio | Relative column widths | `width_ratios=[2, 1]` |

## Glossary

### F

**Flat Index** — Accessing a 2D axes array as if it were 1D using `.flat` for sequential iteration.

### G

**GridSpec** — A class for creating subplot grids with unequal row/column sizes.

### I

**Inset** — A smaller axes placed inside a larger axes, often used for zoomed-in views.

### S

**Shared Axes** — Subplots that share x and/or y axis limits, so zooming one zooms all.

**subplots()** — The primary function for creating a figure and grid of subplots simultaneously.

**Subplot** — A single axes within a multi-plot grid.
