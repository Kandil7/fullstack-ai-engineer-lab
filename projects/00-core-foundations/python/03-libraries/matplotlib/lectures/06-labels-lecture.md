# Matplotlib Lecture 06: Labels, Titles, and Legends

## 🎯 Topic Overview

Labels, titles, and legends provide context for your data visualizations. Without them, even the most beautifully styled plot is meaningless. 

## 📚 Learning Objectives

1. Add and customize axis labels, title, and suptitle
2. Create and position legends with full control
3. Use LaTeX formatting and font properties
4. Handle overlapping text and auto-layout

---

## 1. Axis Labels and Titles

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), linewidth=2)

# Basic labels
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.title('Sine Wave Over Time', fontsize=14, fontweight='bold')

# Suptitle for entire figure
plt.suptitle('Figure-Level Title', fontsize=16, y=0.98)

# Label properties
plt.xlabel('X Axis',
           fontsize=14,
           fontweight='bold',
           color='darkblue',
           fontfamily='serif',
           labelpad=10)  # Padding from axis
```

### LaTeX Formatting

```python
plt.title(r'$\sin(x)$ vs $\cos(x)$', fontsize=16)
plt.xlabel(r'Angle $\theta$ (radians)', fontsize=14)
plt.ylabel(r'Amplitude $A$', fontsize=14)
# Requires: rcParams['text.usetex'] = True
# Or use built-in mathtext (no LaTeX needed)
```

---

## 2. Legend Customization

```python
plt.plot(x, np.sin(x), label='sin(x)')
plt.plot(x, np.cos(x), label='cos(x)')

# Legend location
plt.legend(loc='upper right')      # String position
plt.legend(loc=1)                   # Numeric alias

# Valid locations:
# 'best' (0), 'upper right' (1), 'upper left' (2),
# 'lower left' (3), 'lower right' (4), 'right' (5),
# 'center left' (6), 'center right' (7), 'lower center' (8),
# 'upper center' (9), 'center' (10)

# Custom legend
plt.legend(
    loc='upper right',
    fontsize=12,
    title='Functions',           # Legend title
    title_fontsize=14,
    frameon=True,                 # Box border
    framealpha=0.8,               # Box transparency
    facecolor='lightgray',        # Box color
    edgecolor='black',            # Border color
    shadow=True,                  # Drop shadow
    ncol=2,                       # Number of columns
    borderpad=1,                  # Padding inside box
    fancybox=True                 # Rounded corners
)
```

---

## 3. Font Properties and rcParams

```python
import matplotlib as mpl

# Global font settings
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 12
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['legend.fontsize'] = 11
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10

# Or use FontProperties
from matplotlib.font_manager import FontProperties
font = FontProperties(family='monospace', size=14, weight='bold')
plt.xlabel('Custom Font', fontproperties=font)
```

---

## Practice Exercises

1. Create a plot with LaTeX-formatted axis labels and legend
2. Customize legend: position, frame style, title, and columns
3. Change global font settings using rcParams
