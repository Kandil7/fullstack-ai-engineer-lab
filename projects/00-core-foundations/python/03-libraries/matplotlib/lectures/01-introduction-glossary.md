# Matplotlib Lecture 01: Introduction — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Matplotlib | Python's foundational visualization library | `import matplotlib.pyplot as plt` |
| pyplot | MATLAB-like convenience module | `plt.plot()`, `plt.title()` |
| Figure | Top-level container for all plot elements | `fig = plt.figure()` |
| Axes | The actual plotting area | `ax = fig.add_subplot()` |
| Subplot | A grid of multiple axes | `fig, axes = plt.subplots(2, 2)` |
| Artist | Any element drawn on the figure | Text, Line2D, Rectangle |
| Backend | Rendering engine (Agg, Qt, SVG) | `plt.switch_backend('Agg')` |
| `savefig()` | Save figure to file | `fig.savefig('plot.png', dpi=300)` |
| `show()` | Display figure (blocking) | `plt.show()` |
| `tight_layout()` | Auto-adjust subplot spacing | `fig.tight_layout()` |
| DPI | Dots per inch (resolution) | `fig.savefig('plot.png', dpi=300)` |
| `bbox_inches='tight'` | Remove extra whitespace on save | `fig.savefig('plot.pdf', bbox_inches='tight')` |

---

## Alphabetical Glossary

### A

#### Artist

Every element visible on a Matplotlib figure is an Artist — lines, text, ticks, axes, etc.

```python
fig, ax = plt.subplots()
line = ax.plot([1, 2, 3], [1, 4, 2])[0]  # Line2D artist
text = ax.set_title("Title")               # Text artist
print(type(line))  # <class 'matplotlib.lines.Line2D'>
print(type(text))  # <class 'matplotlib.text.Text'>
```

**Related:** Figure, Axes, Renderer

---

#### Axes

The data plotting area within a figure. Contains x/y axes, ticks, labels, and plotted data.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])      # Axes method
ax.set_xlabel("X axis")             # Axes method
ax.set_ylabel("Y axis")             # Axes method
ax.grid(True)                       # Axes method
```

**Related:** Figure, Subplot, Twin Axes

---

### B

#### Backend

The rendering engine that Matplotlib uses to produce output. Can be interactive (GUI) or non-interactive (file-based).

```python
import matplotlib
print(matplotlib.get_backend())  # e.g., 'TkAgg'

# Switch to non-interactive (for scripts/servers)
matplotlib.use('Agg')  # Must be called BEFORE importing pyplot

# Common backends:
# 'Agg'       - PNG output (non-interactive)
# 'PDF'       - PDF output (non-interactive)
# 'SVG'       - SVG output (non-interactive)
# 'QtAgg'     - Qt5 interactive window
# 'TkAgg'     - Tkinter interactive window
# 'WebAgg'    - Browser-based interactive
```

**Related:** Renderer, Interactive Mode

---

#### bbox_inches='tight'

A parameter for `savefig()` that automatically removes extra whitespace around the plot.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])
ax.set_title("Plot")

# Without tight - extra whitespace
fig.savefig('plot_loose.png')

# With tight - minimal whitespace
fig.savefig('plot_tight.png', bbox_inches='tight')
```

**Related:** `savefig()`, `tight_layout()`

---

### D

#### DPI (Dots Per Inch)

The resolution of saved figures. Higher DPI = sharper but larger files.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])

# Web quality
fig.savefig('web.png', dpi=72)

# Print quality
fig.savefig('print.png', dpi=300)

# Publication quality
fig.savefig('pub.png', dpi=600)
```

**Related:** `savefig()`, Figure size

---

### F

#### Figure

The top-level container that holds all plot elements. Think of it as the canvas or window.

```python
# Create a figure
fig = plt.figure(figsize=(8, 6))           # 8 inches wide, 6 inches tall
fig.suptitle("Figure Title")                # Super-title for entire figure

# Add axes to the figure
ax = fig.add_subplot(111)                   # 1 row, 1 col, index 1
ax.plot([1, 2, 3], [1, 4, 2])

# Multiple axes
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
```

**Related:** Axes, Subplot, Artist

---

#### Figure Size

The dimensions of the figure in inches (or mm/cm with conversion).

```python
# Setting figure size
fig, ax = plt.subplots(figsize=(8, 5))     # 8" × 5"

# Golden ratio
fig, ax = plt.subplots(figsize=(8, 8/1.618))  # ~8" × 4.94"

# For publications (convert cm to inches: cm / 2.54)
fig, ax = plt.subplots(figsize=(12/2.54, 8/2.54))  # 12cm × 8cm
```

**Related:** DPI, `savefig()`

---

### I

#### Interactive Mode

When enabled, plots display immediately without requiring `plt.show()`.

```python
import matplotlib.pyplot as plt

# Enable interactive mode
plt.ion()
plt.plot([1, 2, 3], [1, 4, 2])  # Displays immediately

# Disable interactive mode
plt.ioff()

# In scripts, always use plt.show() (blocking)
plt.plot([1, 2, 3], [1, 4, 2])
plt.show()  # Blocks until window is closed
```

**Related:** Backend, `show()`

---

### O

#### OOP Interface

The Object-Oriented Programming interface for Matplotlib. Uses explicit Figure and Axes objects.

```python
# OOP style - explicit and powerful
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color='red', linewidth=2, label='sin(x)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title('Sine Wave')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

**Related:** pyplot Interface, Axes, Figure

---

### P

#### pyplot

A convenience module that provides a MATLAB-like functional interface to Matplotlib.

```python
import matplotlib.pyplot as plt

# pyplot style - quick and concise
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'r-', label='sin(x)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Sine Wave')
plt.legend()
plt.grid(True)
plt.show()
```

**Related:** OOP Interface, MATLAB-style

---

### R

#### Renderer

The backend component that actually draws Artists onto the canvas. Users rarely interact with renderers directly.

```python
# Backends determine the renderer
import matplotlib
matplotlib.use('Agg')      # Anti-Grain Geometry renderer
matplotlib.use('PDF')      # PDF renderer
matplotlib.use('SVG')      # SVG renderer
```

**Related:** Backend, Artist

---

### S

#### `savefig()`

The method to save a figure to a file in various formats.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])
ax.set_title("My Plot")

# Save variations
fig.savefig('plot.png')                              # Default
fig.savefig('plot.png', dpi=300)                      # High resolution
fig.savefig('plot.pdf', format='pdf')                  # Vector format
fig.savefig('plot.svg', format='svg')                  # SVG format
fig.savefig('plot.png', transparent=True)              # Transparent bg
fig.savefig('plot.png', facecolor='lightgray')         # Custom bg color
fig.savefig('plot.pdf', bbox_inches='tight')           # Minimal whitespace
```

**Related:** DPI, `bbox_inches='tight'`, format

---

#### `show()`

Displays the figure. In scripts, this blocks execution until the window is closed. In Jupyter, it's often automatic.

```python
# Script usage - blocks until closed
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])
plt.show()  # Blocks!

# In Jupyter - not needed (automatic display)
# Just create the plot and it appears

# Non-blocking display (interactive mode)
plt.ion()
plt.plot([1, 2, 3], [1, 4, 2])
plt.show(block=False)  # Non-blocking!
```

**Related:** Interactive Mode, Backend, `plt.pause()`

---

#### Subplot

A grid of multiple axes within a single figure.

```python
# Grid of subplots
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
# axes is a 2x3 array of Axes objects

# Access individual subplots
axes[0, 0].plot([1, 2, 3], [1, 4, 2])
axes[0, 1].scatter([1, 2, 3], [1, 4, 2])
axes[1, 2].bar([1, 2, 3], [1, 4, 2])

# Unequal layout - GridSpec
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(10, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])    # Full width top row
ax2 = fig.add_subplot(gs[1, :-1])   # Middle row, left 2/3
ax3 = fig.add_subplot(gs[1:, -1])   # Right column, bottom 2 rows
ax4 = fig.add_subplot(gs[-1, 0])    # Bottom-left
ax5 = fig.add_subplot(gs[-1, 1])    # Bottom-center
```

**Related:** Axes, Figure, GridSpec

---

### T

#### `tight_layout()`

Automatically adjusts subplot parameters to prevent overlapping elements.

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

for i, ax in enumerate(axes.flat):
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title(f"Very Long Title That Would Overlap {i+1}")
    ax.set_xlabel("This x-label would also overlap")

# Auto-fix spacing
fig.tight_layout()  # Now everything fits!

# Alternative: constrained_layout (usually better)
fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
```

**Related:** `bbox_inches='tight'`, constrained_layout

---

### Twin Axes

Creating a second y-axis on the same plot (for data with different scales).

```python
fig, ax1 = plt.subplots(figsize=(8, 5))

x = [1, 2, 3, 4, 5]
y1 = [10, 20, 15, 25, 30]
y2 = [1000, 800, 600, 400, 200]

ax1.plot(x, y1, 'b-', label='Temperature')
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature (°C)', color='blue')

ax2 = ax1.twinx()  # Create twin axes sharing x-axis
ax2.plot(x, y2, 'r--', label='Pressure')
ax2.set_ylabel('Pressure (hPa)', color='red')

fig.legend()
plt.show()
```

**Related:** Axes, Figure, Subplot

---

## Conceptual Map

```
Matplotlib
├── Interfaces
│   ├── pyplot (functional, MATLAB-like)
│   └── OOP (explicit, Figure/Axes objects)
│
├── Architecture
│   ├── Figure (canvas/container)
│   │   └── Axes (plot area)
│   │       ├── XAxis, YAxis
│   │       ├── Spines (axes borders)
│   │       ├── Tick, TickLabel
│   │       └── Artists (lines, text, patches)
│   └── Subplot (grid of axes)
│
├── Output
│   ├── Backend (rendering engine)
│   ├── Formats (PNG, PDF, SVG, EPS)
│   └── Save (savefig with DPI and tight layout)
│
└── Workflow
    ├── Create Figure
    ├── Create Axes (or subplots)
    ├── Plot Data on Axes
    ├── Customize (labels, title, legend)
    ├── Adjust Layout (tight_layout)
    └── Save & Show
```
