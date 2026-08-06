# Matplotlib Lecture 05: Line Customization — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Line Style | Pattern of the plotted line | `linestyle='--'` |
| Line Width | Thickness of the line in points | `linewidth=2` |
| Dash Pattern | Custom on/off lengths | `(0, (5, 5))` |
| Alpha | Transparency (0=invisible, 1=opaque) | `alpha=0.7` |
| Color | Line color (name, hex, RGB) | `color='steelblue'` |
| `axhline()` | Horizontal line across axes | `plt.axhline(y=0)` |
| `axvline()` | Vertical line across axes | `plt.axvline(x=0)` |
| `axhspan()` | Horizontal shaded region | `plt.axhspan(ymin, ymax)` |
| `axvspan()` | Vertical shaded region | `plt.axvspan(xmin, xmax)` |
| `fill_between()` | Fill between two curves | `plt.fill_between(x, y1, y2)` |

## Glossary

### A

**Alpha** — Transparency value from 0 (fully transparent) to 1 (fully opaque).

**axhline/axvline** — Utility functions that draw infinite horizontal/vertical lines across the axes.

**axhspan/axvspan** — Utility functions that draw shaded rectangular regions across the axes.

### C

**Color** — Line color specified as name (`'red'`), hex (`'#FF0000'`), RGB tuple (`(1, 0, 0)`), or HTML color name (`'steelblue'`).

### D

**Dash Pattern** — A tuple `(offset, (on_length, off_length, ...))` defining custom dashes.

### F

**fill_between** — Fills the area between two curves or between a curve and a baseline.

### L

**Line Style** — The pattern of a plotted line: solid (`-`), dashed (`--`), dash-dot (`-.`), dotted (`:`), or custom.

**Line Width** — Thickness of the line in points (1/72 inch).
