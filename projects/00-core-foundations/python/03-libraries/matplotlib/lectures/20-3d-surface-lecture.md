# Matplotlib Lecture 20: 3D Surface Advanced

## 🎯 Topic Overview

Advanced 3D surface techniques for creating publication-quality visualizations of complex surfaces and terrain data.

## 📚 Learning Objectives

1. Create complex 3D surfaces with custom colormaps
2. Add texture, wireframe overlays, and contour projections
3. Create animated 3D surfaces
4. Combine multiple 3D visualization techniques

---

## 1. Complex Surface with Texture

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

# Sombrero function
R = np.sqrt(X**2 + Y**2)
Z = np.sinc(R / np.pi)

fig = plt.figure(figsize=(12, 5))

ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf1 = ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0,
                         antialiased=True)
ax1.set_title('Sombrero Function')
fig.colorbar(surf1, ax=ax1, shrink=0.5)

# With wireframe overlay
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf2 = ax2.plot_surface(X, Y, Z, cmap=cm.viridis, linewidth=0,
                         antialiased=True, alpha=0.8)
ax2.plot_wireframe(X[::5, ::5], Y[::5, ::5], Z[::5, ::5],
                   color='black', linewidth=0.3, alpha=0.3)
ax2.set_title('Surface + Wireframe Overlay')
fig.colorbar(surf2, ax=ax2, shrink=0.5)

plt.tight_layout()
plt.show()
```

---

## 2. 3D Surface with Contour Projection

```python
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7,
                       linewidth=0, antialiased=True)

# Contour projections on all three planes
ax.contour(X, Y, Z, zdir='z', offset=-0.5, cmap='viridis', linewidths=1)
ax.contour(X, Y, Z, zdir='x', offset=-4, cmap='viridis', linewidths=1)
ax.contour(X, Y, Z, zdir='y', offset=4, cmap='viridis', linewidths=1)

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-0.5, 1.0)

fig.colorbar(surf, shrink=0.5)
plt.show()
```

---

## 3. Animated Surface

```python
import matplotlib.animation as animation

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

def animate_surface(frame):
    ax.clear()
    phase = frame / 20.0
    Z_animated = np.sin(np.sqrt(X**2 + Y**2) - phase)
    ax.plot_surface(X, Y, Z_animated, cmap='viridis', linewidth=0)
    ax.set_zlim(-1.5, 1.5)
    ax.view_init(elev=30, azim=frame)
    return ax,

ani = animation.FuncAnimation(fig, animate_surface, frames=60, interval=100)
plt.show()
```

---

## Practice Exercises

1. Create the Sombrero function with a wireframe overlay
2. Add contour projections to all three axes of a surface plot
3. Create an animated surface that rotates and oscillates simultaneously
