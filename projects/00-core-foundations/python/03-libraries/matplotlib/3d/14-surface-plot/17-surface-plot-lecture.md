# Matplotlib Lecture 17: 3D Surface Plots

## 🎯 Topic Overview

Surface plots create shaded 3D representations of functions, ideal for visualizing complex mathematical surfaces, optimization landscapes, and terrain data.

## 📚 Learning Objectives

1. Create surface plots with `plot_surface()`
2. Apply colormaps to surface height
3. Customize lighting, shading, and perspective

---

## 1. Basic Surface Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(12, 5))

# Surface
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf1 = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax1.set_title('Surface Plot')
fig.colorbar(surf1, ax=ax1, shrink=0.5)

# Surface with shading
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf2 = ax2.plot_surface(X, Y, Z, cmap='viridis',
                         edgecolor='none', shade=True,
                         antialiased=True)
ax2.set_title('Shaded Surface')
fig.colorbar(surf2, ax=ax2, shrink=0.5)

plt.tight_layout()
plt.show()
```

---

## 2. Surface Customization

```python
# Custom view
ax.view_init(elev=25, azim=-60)

# Custom colormap and alpha
surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9,
                       linewidth=0, antialiased=True)

# Add contour projection
ax.contour(X, Y, Z, zdir='z', offset=-1, cmap='viridis')
ax.contour(X, Y, Z, zdir='x', offset=-6, cmap='viridis')
ax.contour(X, Y, Z, zdir='y', offset=6, cmap='viridis')

# Adjust stride for performance
ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap='viridis')
```

---

## Practice Exercises

1. Create a surface plot of `Z = cos(X) * sin(Y)` with a coolwarm colormap
2. Add contour projections on all three axes
3. Create a surface with custom striding and shading
