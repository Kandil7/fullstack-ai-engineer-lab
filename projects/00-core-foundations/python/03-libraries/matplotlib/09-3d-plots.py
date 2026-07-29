"""
Matplotlib 3D Plots: surface, scatter, wireframe, contour
===========================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# 1. BASIC 3D SCATTER
# =============================================================================

print("=" * 60)
print("1. 3D SCATTER PLOT")
print("=" * 60)

np.random.seed(42)
n = 200
x = np.random.randn(n)
y = np.random.randn(n)
z = np.random.randn(n)
colors = np.random.rand(n)
sizes = 20 + 100 * np.random.rand(n)

fig = plt.figure(figsize=(12, 10))

ax1 = fig.add_subplot(221, projection='3d')
sc = ax1.scatter(x, y, z, c=colors, s=sizes, cmap='viridis', alpha=0.6)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('3D Scatter Plot')
plt.colorbar(sc, ax=ax1, shrink=0.6)

# 3D scatter with groups
ax2 = fig.add_subplot(222, projection='3d')
for group, color in zip(['A', 'B', 'C'], ['red', 'blue', 'green']):
    n_g = n // 3
    x_g = np.random.randn(n_g) + np.random.choice([-3, 0, 3])
    y_g = np.random.randn(n_g) + np.random.choice([-3, 0, 3])
    z_g = np.random.randn(n_g) + np.random.choice([-3, 0, 3])
    ax2.scatter(x_g, y_g, z_g, c=color, label=group, alpha=0.6, s=30)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Grouped 3D Scatter')
ax2.legend()

# 3D line plot
ax3 = fig.add_subplot(223, projection='3d')
t = np.linspace(0, 20, 500)
x_line = np.sin(t)
y_line = np.cos(t)
z_line = t
ax3.plot(x_line, y_line, z_line, 'b-', linewidth=1)
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('3D Helix Line')

# 3D scatter with projection
ax4 = fig.add_subplot(224, projection='3d')
ax4.scatter(x, y, z, c=z, cmap='plasma', alpha=0.6, s=30)
# Project to XY plane
ax4.scatter(x, y, -4, c=z, cmap='plasma', alpha=0.3, s=10)
ax4.set_zlim(-4, 4)
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')
ax4.set_title('3D Scatter with XY Projection')

plt.suptitle('3D Scatter Variations', fontsize=16)
plt.tight_layout()
plt.savefig('output/3d_scatter.png', dpi=150)
plt.close()

print("3D scatter plots saved")
print()

# =============================================================================
# 2. 3D SURFACE PLOTS
# =============================================================================

print("=" * 60)
print("2. 3D SURFACE PLOTS")
print("=" * 60)

fig = plt.figure(figsize=(14, 10))

# Surface 1: Basic
ax1 = fig.add_subplot(221, projection='3d')
X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf1 = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.set_title('Surface: sin(r)')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
fig.colorbar(surf1, ax=ax1, shrink=0.6)

# Surface 2: Ripple
ax2 = fig.add_subplot(222, projection='3d')
Z2 = np.sin(R) * np.cos(R/2)
surf2 = ax2.plot_surface(X, Y, Z2, cmap='RdYlBu', alpha=0.8, 
                          rstride=2, cstride=2, linewidth=0, antialiased=True)
ax2.set_title('Surface: sin(r)*cos(r/2)')
fig.colorbar(surf2, ax=ax2, shrink=0.6)

# Surface 3: Wireframe
ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_wireframe(X, Y, Z, rstride=2, cstride=2, color='blue', alpha=0.5)
ax3.set_title('Wireframe Plot')

# Surface 4: Contour on surface
ax4 = fig.add_subplot(224, projection='3d')
surf4 = ax4.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.6, 
                          rstride=1, cstride=1, linewidth=0, antialiased=True)
# Project contours to walls
cset = ax4.contour(X, Y, Z, zdir='z', offset=-1.5, cmap='coolwarm')
cset = ax4.contour(X, Y, Z, zdir='x', offset=-6, cmap='coolwarm')
cset = ax4.contour(X, Y, Z, zdir='y', offset=6, cmap='coolwarm')
ax4.set_xlim(-6, 6)
ax4.set_ylim(-6, 6)
ax4.set_zlim(-1.5, 1.5)
ax4.set_title('Surface with Projected Contours')

plt.suptitle('3D Surface Plots', fontsize=16)
plt.tight_layout()
plt.savefig('output/3d_surface.png', dpi=150)
plt.close()

print("3D surface plots saved")
print()

# =============================================================================
# 3. ADVANCED 3D: PARAMETRIC SURFACES
# =============================================================================

print("=" * 60)
print("3. PARAMETRIC SURFACES")
print("=" * 60)

fig = plt.figure(figsize=(14, 10))

# Torus
ax1 = fig.add_subplot(221, projection='3d')
u = np.linspace(0, 2*np.pi, 30)
v = np.linspace(0, 2*np.pi, 30)
u, v = np.meshgrid(u, v)
R, r = 2, 0.8
x_torus = (R + r * np.cos(v)) * np.cos(u)
y_torus = (R + r * np.cos(v)) * np.sin(u)
z_torus = r * np.sin(v)
ax1.plot_surface(x_torus, y_torus, z_torus, cmap='plasma', alpha=0.8)
ax1.set_title('Torus')

# Klein bottle
ax2 = fig.add_subplot(222, projection='3d')
u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(0, 2*np.pi, 40)
u, v = np.meshgrid(u, v)
r = 4 * (1 - np.cos(u)/2)
x_klein = r * np.cos(u) * np.cos(v) + 6 * np.sin(u) * np.cos(v)
y_klein = r * np.sin(u) * np.cos(v) + 6 * np.sin(u) * np.sin(v)
z_klein = r * np.sin(v) + 6 * np.cos(v)
ax2.plot_surface(x_klein, y_klein, z_klein, cmap='coolwarm', alpha=0.7)
ax2.set_title('Klein Bottle')

# Möbius strip
ax3 = fig.add_subplot(223, projection='3d')
u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(-1, 1, 20)
u, v = np.meshgrid(u, v)
x_mobius = (1 + v/2 * np.cos(u/2)) * np.cos(u)
y_mobius = (1 + v/2 * np.cos(u/2)) * np.sin(u)
z_mobius = v/2 * np.sin(u/2)
ax3.plot_surface(x_mobius, y_mobius, z_mobius, cmap='viridis', alpha=0.8)
ax3.set_title('Möbius Strip')

# Sphere with texture
ax4 = fig.add_subplot(224, projection='3d')
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 50)
u, v = np.meshgrid(u, v)
x_sphere = np.cos(u) * np.sin(v)
y_sphere = np.sin(u) * np.sin(v)
z_sphere = np.cos(v)
# Color by height
colors = plt.cm.jet(z_sphere)
ax4.plot_surface(x_sphere, y_sphere, z_sphere, facecolors=colors, 
                  rstride=1, cstride=1, alpha=0.8, shade=False)
ax4.set_title('Colored Sphere')

plt.suptitle('Parametric 3D Surfaces', fontsize=16)
plt.tight_layout()
plt.savefig('output/3d_parametric.png', dpi=150)
plt.close()

print("Parametric surfaces saved")
print()

# =============================================================================
# 4. 3D CONTOUR AND VOLUME
# =============================================================================

print("=" * 60)
print("4. 3D CONTOUR AND VOLUME")
print("=" * 60)

fig = plt.figure(figsize=(14, 10))

# 3D contour
ax1 = fig.add_subplot(221, projection='3d')
X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Contour lines in 3D
cset = ax1.contour(X, Y, Z, levels=15, cmap='viridis', linewidths=1)
ax1.clabel(cset, inline=True, fontsize=8)
ax1.set_title('3D Contour Lines')

# Filled 3D contour
ax2 = fig.add_subplot(222, projection='3d')
cset = ax2.contourf(X, Y, Z, levels=15, cmap='viridis', alpha=0.7, zdir='z', offset=-1.5)
ax2.set_zlim(-1.5, 1.5)
ax2.set_title('Filled 3D Contour')

# Volume rendering concept (isosurfaces via contour)
ax3 = fig.add_subplot(223, projection='3d')
# Multiple isosurfaces
for level, alpha in zip([-0.5, 0, 0.5], [0.3, 0.5, 0.7]):
    ax3.contour(X, Y, Z, levels=[level], colors='blue', alpha=alpha, linewidths=2)
ax3.set_title('Isosurfaces (Contour Levels)')

# 3D bar chart
ax4 = fig.add_subplot(224, projection='3d')
# Create a 3D histogram
hist, xedges, yedges = np.histogram2d(x, y, bins=10)
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0
dx = dy = 0.5 * np.ones_like(zpos)
dz = hist.ravel()
ax4.bar3d(xpos, ypos, zpos, dx, dy, dz, color='skyblue', alpha=0.7, edgecolor='black')
ax4.set_title('3D Bar Chart (Histogram)')

plt.suptitle('3D Contour and Volume', fontsize=16)
plt.tight_layout()
plt.savefig('output/3d_contour.png', dpi=150)
plt.close()

print("3D contour plots saved")
print()

# =============================================================================
# 5. CUSTOMIZATION AND VIEWING
# =============================================================================

print("=" * 60)
print("5. 3D CUSTOMIZATION AND VIEWING")
print("=" * 60)

fig = plt.figure(figsize=(14, 10))

# Custom viewing angles
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.view_init(elev=30, azim=45)
ax1.set_title('view_init(30, 45)')

ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax2.view_init(elev=60, azim=135)
ax2.set_title('view_init(60, 135)')

ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax3.view_init(elev=90, azim=-90)  # Top-down
ax3.set_title('view_init(90, -90) - Top Down')

# Axis customization
ax4 = fig.add_subplot(224, projection='3d')
surf = ax4.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax4.set_xlabel('X Axis', fontsize=12, labelpad=10)
ax4.set_ylabel('Y Axis', fontsize=12, labelpad=10)
ax4.set_zlabel('Z Axis', fontsize=12, labelpad=10)
ax4.set_title('Custom Axis Labels')
# Custom ticks
ax4.set_xticks([-5, 0, 5])
ax4.set_yticks([-5, 0, 5])
ax4.set_zticks([-1, 0, 1])
# Pane colors
ax4.xaxis.pane.fill = True
ax4.xaxis.pane.set_facecolor((0.9, 0.9, 0.9, 0.5))
ax4.yaxis.pane.fill = True
ax4.yaxis.pane.set_facecolor((0.9, 0.9, 0.9, 0.5))
ax4.zaxis.pane.fill = True
ax4.zaxis.pane.set_facecolor((0.9, 0.9, 0.9, 0.5))

plt.suptitle('3D Customization', fontsize=16)
plt.tight_layout()
plt.savefig('output/3d_custom.png', dpi=150)
plt.close()

print("3D customization saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("3D PLOTS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. 3D Axes: projection='3d' subplot
2. Scatter: scatter(x, y, z) with color/size mapping
3. Line: plot(x, y, z) for parametric curves
4. Surface: plot_surface(X, Y, Z) with meshgrid
5. Wireframe: plot_wireframe for structure view
6. Contour: contour, contourf with zdir, offset
7. Parametric: Torus, Klein bottle, Möbius strip
8. Bars: bar3d for 3D histograms
9. View: view_init(elev, azim) for camera angles
10. Customization: pane colors, tick labels, axis labels

Next: Animations, embedding, backends
""")