# Matplotlib Lecture 02: Pyplot — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| pyplot | MATLAB-like plotting interface | `import matplotlib.pyplot as plt` |
| State Machine | Pyplot tracks current figure/axes | `plt.gcf()`, `plt.gca()` |
| Figure | Top-level container | `plt.figure(figsize=(8,5))` |
| Subplot | Grid of axes | `plt.subplot(2, 2, 1)` |
| `gcf()` | Get current figure | `fig = plt.gcf()` |
| `gca()` | Get current axes | `ax = plt.gca()` |
| `clf()` | Clear current figure | `plt.clf()` |
| `close()` | Close figure | `plt.close('all')` |
| `show()` | Display figure | `plt.show()` |
| `savefig()` | Save to file | `plt.savefig('plot.png')` |

## Glossary

### G

**gca()** — Get Current Axes. Returns the current axes instance.

**gcf()** — Get Current Figure. Returns the current figure instance.

### P

**pyplot** — A collection of command-style functions that make Matplotlib work like MATLAB. Each function makes some change to a figure.

### S

**State Machine** — Pyplot's internal mechanism that tracks the \"current\" figure and axes for operations.

**subplot** — Create a grid of axes in a single figure.
