# Matplotlib Lecture 16: 3D Wireframe Plots

## 🎯 Topic Overview

Wireframe plots show 3D surfaces as a grid of lines, making them ideal for understanding mathematical functions and surface topology. They're lighter than surface plots and don't hide features behind faces.

## 📚 Learning Objectives

1. Create 3D wireframe plots using `plot_wireframe()`
2. Customize wireframe appearance (line colors, stride, alpha)
3. Control 3D view angles (elevation and azimuth)

---

## 1. Basic 3D Wireframe

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
wire = ax.plot_wireframe(X, Y, Z, color='steelblue', linewidth=0.5)
ax.set_title('3D Wireframe: sin(sqrt(x² + y²))')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
```

---

## 2. View Angles and Stride

```python
# Control view perspective
ax.view_init(elev=30, azim=45)  # elevation, azimuth

# Reduce wire density with stride
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5,  # Every 5th row/col
                 color='steelblue', linewidth=0.5, alpha=0.7)

# Common angles:
# - top: elev=90, azim=0
# - side: elev=0, azim=0
# - isometric: elev=30, azim=45
# - reverse: elev=30, azim=-45
```

---

## 3. Multiple Wireframes

```python
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

Z1 = np.sin(np.sqrt(X**2 + Y**2))
Z2 = np.cos(np.sqrt(X**2 + Y**2))

ax.plot_wireframe(X, Y, Z1, color='steelblue', alpha=0.7, label='sin')
ax.plot_wireframe(X, Y, Z2, color='coral', alpha=0.5, label='cos')
ax.legend()
```

---

## Practice Exercises

1. Create a wireframe of the function `Z = x² - y²` (saddle)
2. Create a wireframe with reduced stride for a cleaner look
3. Create a wireframe and view it from 3 different angles in subplots
