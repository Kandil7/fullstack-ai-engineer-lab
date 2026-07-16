# Matplotlib Lecture 16: 3D Wireframe — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Wireframe | 3D surface as grid lines | `ax.plot_wireframe(X, Y, Z)` |
| `projection='3d'` | Enable 3D axes | `fig.add_subplot(111, projection='3d')` |
| Stride | Wire grid density | `rstride=5, cstride=5` |
| `view_init()` | Set viewing angle | `ax.view_init(elev=30, azim=45)` |
| Elevation | Vertical viewing angle | Angle above horizon |
| Azimuth | Horizontal viewing angle | Rotation around vertical axis |

## Glossary

### A

**Azimuth** — The horizontal rotation angle of the 3D viewpoint (0 to 360 degrees).

### E

**Elevation** — The vertical angle of the 3D viewpoint above the xy-plane (0 to 90 degrees).

### S

**Stride** — The step size between grid lines in each direction. Higher stride = fewer, coarser lines.

### V

**view_init()** — Sets the viewing angle for a 3D plot by specifying elevation and azimuth.

### W

**Wireframe** — A 3D surface visualization using a grid of unconnected lines.
