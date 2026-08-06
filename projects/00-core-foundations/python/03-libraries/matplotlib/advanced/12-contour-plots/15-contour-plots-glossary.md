# Matplotlib Lecture 15: Contour Plots — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Contour | 3D surface as 2D lines | `plt.contour(X, Y, Z)` |
| Contourf | Filled contour | `plt.contourf(X, Y, Z)` |
| Levels | Number/position of contours | `levels=20` |
| `meshgrid()` | Create 2D coordinate matrices | `np.meshgrid(x, y)` |
| `clabel()` | Label contour lines | `plt.clabel(CS)` |
| Colormap | Color mapping for levels | `cmap='viridis'` |

## Glossary

### C

**clabel()** — Adds numerical labels to contour lines, placed inline.

**Contour** — Lines connecting points of equal value on a 3D surface.

**contourf()** — Filled contour plot where areas between levels are colored.

### L

**Levels** — The number or specific values at which contour lines are drawn.

### M

**meshgrid()** — Creates coordinate matrices from 1D x and y vectors for 3D plotting.
