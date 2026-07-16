# Matplotlib Lecture 18: 3D Scatter Plots

## 🎯 Topic Overview

3D scatter plots reveal relationships between three continuous variables. They're essential for exploring multi-dimensional datasets and identifying clusters in 3D space.

## 📚 Learning Objectives

1. Create 3D scatter plots with `scatter()`
2. Encode additional dimensions with color and size
3. Rotate and animate 3D scatter views

---

## 1. Basic 3D Scatter

```python
import matplotlib.pyplot as plt
import numpy as np

n = 200
x = np.random.randn(n)
y = np.random.randn(n)
z = np.random.randn(n)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='steelblue', s=20, alpha=0.6)
ax.set_title('3D Scatter Plot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
```

---

## 2. Multi-Dimensional 3D Scatter

```python
# Encode 5 dimensions: X, Y, Z, color (category), size (value)
colors = ['red', 'green', 'blue']
sizes = np.random.uniform(10, 100, n)

for i, (label, color) in enumerate(zip(['A', 'B', 'C'], colors)):
    mask = (cluster == i)
    ax.scatter(x[mask], y[mask], z[mask],
               c=color, s=sizes[mask], alpha=0.7,
               label=label, edgecolors='black', linewidth=0.5)

ax.legend()
```

---

## 3. Animated Rotation

```python
import matplotlib.animation as animation

def animate(frame):
    ax.view_init(elev=30, azim=frame)
    return fig,

ani = animation.FuncAnimation(fig, animate, frames=360, interval=50)
# ani.save('rotation.gif', fps=20)
plt.show()
```

---

## Practice Exercises

1. Create a 3D scatter of 3 clusters with different colors
2. Encode 5 dimensions using X, Y, Z, color, and marker size
3. Create an animated 3D scatter that rotates through 360°
