# Matplotlib Lecture 20: Advanced 3D Surfaces — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Sombrero | `sinc()` 3D function | `Z = sinc(R/π)` |
| Texture | Surface color variation | `cmap='viridis'` |
| Overlay | Wireframe on surface | `alpha=0.8` + `wireframe()` |
| Animation | Time-varying 3D plot | `FuncAnimation` |
| `FuncAnimation` | Matplotlib animation | `animation.FuncAnimation(fig, func)` |
| `LineCollection` | Multi-segment collection | `LineCollection(segments)` |

## Glossary

### A

**Animation** — A sequence of frames creating the illusion of motion, used for rotating or time-varying plots.

### F

**FuncAnimation** — Matplotlib's animation class that repeatedly calls a function to update the plot.

### O

**Overlay** — Combining multiple plot types (surface + wireframe) on the same axes for richer visualization.

### S

**Sombrero** — The 3D sinc function `Z = sin(R) / R` that resembles a Mexican sombrero hat.

### T

**Texture** — Surface coloring using a colormap to encode height or another variable.
