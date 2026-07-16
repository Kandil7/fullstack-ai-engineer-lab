# Matplotlib Lecture 19: 3D Line Plots

## 🎯 Topic Overview

3D line plots trace paths through 3D space, ideal for visualizing trajectories, parametric curves, and time-evolving systems.

## 📚 Learning Objectives

1. Create 3D line plots using `plot()`
2. Create parametric 3D curves
3. Combine 3D lines with other 3D plot types

---

## 1. Basic 3D Line

```python
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 10, 1000)
x = np.cos(t)
y = np.sin(t)
z = t / 10

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, 'b-', linewidth=2, label='Helix')
ax.set_title('3D Line: Helix')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()
```

---

## 2. Parametric 3D Curves

```python
# Toroidal spiral
t = np.linspace(0, 2*np.pi, 1000)
R, r = 3, 1
x = (R + r * np.cos(8*t)) * np.cos(t)
y = (R + r * np.cos(8*t)) * np.sin(t)
z = r * np.sin(8*t)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, linewidth=1, color='steelblue')

# Color by parameter value
points = np.array([x, y, z]).T.reshape(-1, 1, 3)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
from matplotlib.collections import LineCollection
# Color the line by position along the curve
ax.scatter(x[::20], y[::20], z[::20], c=t[::20], cmap='viridis', s=20)
```

---

## 3. Multiple 3D Lines

```python
for phase in np.linspace(0, 2*np.pi, 8):
    x = np.cos(t + phase)
    y = np.sin(t + phase)
    z = t / 10
    ax.plot(x, y, z, alpha=0.5, linewidth=1)
```

---

## Practice Exercises

1. Create a 3D helix with proper labels and title
2. Create a parametric 3D curve (Lissajous or toroidal spiral)
3. Combine a 3D line with a 3D scatter to show sample points
