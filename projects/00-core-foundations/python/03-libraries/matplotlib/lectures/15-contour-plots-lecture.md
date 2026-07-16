# Matplotlib Lecture 15: Contour Plots

## 🎯 Topic Overview

Contour plots visualize 3D data on a 2D surface using contour lines and filled contours. They're essential for understanding topography, potential fields, and optimization landscapes.

## 📚 Learning Objectives

1. Create contour and filled contour plots
2. Customize contour levels, colors, and labels
3. Understand when to use contour vs contourf

---

## 1. Basic Contour Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))  # Gaussian

plt.figure(figsize=(12, 5))

# Contour lines
plt.subplot(1, 2, 1)
plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(label='Z value')
plt.title('Contour Lines')
plt.xlabel('X')
plt.ylabel('Y')

# Filled contour
plt.subplot(1, 2, 2)
plt.contourf(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(label='Z value')
plt.title('Filled Contour')
plt.xlabel('X')
plt.ylabel('Y')

plt.tight_layout()
plt.show()
```

---

## 2. Advanced Contour Customization

```python
# Custom levels
levels = np.linspace(0, 1, 10)
CS = plt.contour(X, Y, Z, levels=levels, colors='black', linewidths=1)
plt.clabel(CS, inline=True, fontsize=10, fmt='%.2f')

# Combined contourf + contour
plt.contourf(X, Y, Z, levels=20, cmap='RdYlBu_r')
CS = plt.contour(X, Y, Z, levels=5, colors='black', linewidths=0.5)
plt.clabel(CS, inline=True, fontsize=10)

# Custom colormap with discrete levels
plt.contourf(X, Y, Z, levels=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
             colors=['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60'])
```

---

## Practice Exercises

1. Create a contour plot of a 2D Gaussian function with labeled contour lines
2. Create filled contours of the function `Z = sin(X) * cos(Y)`
3. Overlay contour lines on a filled contour plot for clarity
