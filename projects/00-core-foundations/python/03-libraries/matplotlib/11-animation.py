"""
Matplotlib Animations: FuncAnimation, saving, interactive
===========================================================
"""

import pathlib
import matplotlib.pyplot as plt
OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent / "outputs" / "matplotlib"
import pathlib
import matplotlib.animation as animation
import numpy as np

# =============================================================================
# 1. BASIC ANIMATION
# =============================================================================

print("=" * 60)
print("1. BASIC ANIMATION WITH FUNCANIMATION")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Animated Sine Wave')
ax.grid(True, alpha=0.3)

def init():
    line.set_ydata([np.nan] * len(x))
    return line,

def animate(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=50, blit=True)

# Save as GIF
ani.save('output/animation_sine.gif', writer='pillow', fps=20)
plt.close()

print("Basic animation saved as GIF")
print()

# =============================================================================
# 2. MULTIPLE ELEMENTS ANIMATION
# =============================================================================

print("=" * 60)
print("2. MULTIPLE ELEMENTS ANIMATION")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0, 2*np.pi, 200)

# Multiple lines
line1, = ax.plot(x, np.sin(x), 'b-', label='sin(x)', linewidth=2)
line2, = ax.plot(x, np.cos(x), 'r-', label='cos(x)', linewidth=2)
line3, = ax.plot(x, np.sin(x) * np.cos(x), 'g-', label='sin*cos', linewidth=2)

# Moving points
point1, = ax.plot([], [], 'bo', markersize=10)
point2, = ax.plot([], [], 'ro', markersize=10)
point3, = ax.plot([], [], 'go', markersize=10)

# Text annotations
text1 = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
text2 = ax.text(0.02, 0.90, '', transform=ax.transAxes, fontsize=12)
text3 = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=12)

ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Multi-Line Animation')
ax.legend()
ax.grid(True, alpha=0.3)

def animate_multi(frame):
    phase = frame * 0.05
    line1.set_ydata(np.sin(x + phase))
    line2.set_ydata(np.cos(x + phase))
    line3.set_ydata(np.sin(x + phase) * np.cos(x + phase))
    
    # Moving points
    point1.set_data([phase % (2*np.pi)], [np.sin(phase)])
    point2.set_data([phase % (2*np.pi)], [np.cos(phase)])
    point3.set_data([phase % (2*np.pi)], [np.sin(phase) * np.cos(phase)])
    
    # Update text
    text1.set_text(f'sin({phase:.2f}) = {np.sin(phase):.3f}')
    text2.set_text(f'cos({phase:.2f}) = {np.cos(phase):.3f}')
    text3.set_text(f'sin*cos = {np.sin(phase)*np.cos(phase):.3f}')
    
    return line1, line2, line3, point1, point2, point3, text1, text2, text3

ani = animation.FuncAnimation(fig, animate_multi, frames=200, 
                               interval=30, blit=True)

ani.save('output/animation_multi.gif', writer='pillow', fps=30)
plt.close()

print("Multi-element animation saved")
print()

# =============================================================================
# 3. SCATTER ANIMATION
# =============================================================================

print("=" * 60)
print("3. SCATTER ANIMATION")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 6))
np.random.seed(42)
n_points = 100
x = np.random.randn(n_points)
y = np.random.randn(n_points)
colors = np.random.rand(n_points)

scat = ax.scatter(x, y, c=colors, s=50, alpha=0.7, cmap='viridis')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title('Animated Scatter')
ax.grid(True, alpha=0.3)

def animate_scatter(frame):
    # Move points slightly
    new_x = x + 0.02 * np.sin(frame * 0.1 + x)
    new_y = y + 0.02 * np.cos(frame * 0.1 + y)
    scat.set_offsets(np.c_[new_x, new_y])
    # Change colors cyclically
    new_colors = (colors + frame * 0.01) % 1.0
    scat.set_array(new_colors)
    return scat,

ani = animation.FuncAnimation(fig, animate_scatter, frames=200,
                               interval=40, blit=True)

ani.save('output/animation_scatter.gif', writer='pillow', fps=25)
plt.close()

print("Scatter animation saved")
print()

# =============================================================================
# 4. 3D ANIMATION
# =============================================================================

print("=" * 60)
print("4. 3D ANIMATION")
print("=" * 60)

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Rotating 3D surface
X = np.linspace(-5, 5, 40)
Y = np.linspace(-5, 5, 40)
X, Y = np.meshgrid(X, Y)

def animate_3d(frame):
    ax.clear()
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R - frame * 0.1)
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                           rstride=1, cstride=1, linewidth=0)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title(f'3D Wave Animation (frame {frame})')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return surf,

ani = animation.FuncAnimation(fig, animate_3d, frames=100,
                               interval=50, blit=False)

ani.save('output/animation_3d.gif', writer='pillow', fps=20)
plt.close()

print("3D animation saved")
print()

# =============================================================================
# 5. SAVING FORMATS
# =============================================================================

print("=" * 60)
print("5. SAVING IN DIFFERENT FORMATS")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-1.5, 1.5)

def animate_save(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(fig, animate_save, frames=50, interval=50, blit=True)

# Save as GIF (requires pillow)
try:
    ani.save('output/animation.gif', writer='pillow', fps=20)
    print("Saved as GIF (pillow)")
except Exception as e:
    print(f"GIF save failed: {e}")

# Save as MP4 (requires ffmpeg)
try:
    ani.save('output/animation.mp4', writer='ffmpeg', fps=20, 
             extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
    print("Saved as MP4 (ffmpeg)")
except Exception as e:
    print(f"MP4 save failed (ffmpeg not installed?): {e}")

# Save as HTML5 (requires jshtml)
try:
    html = ani.to_jshtml()
    with open('output/animation.html', 'w') as f:
        f.write(html)
    print("Saved as HTML (jshtml)")
except Exception as e:
    print(f"HTML save failed: {e}")

plt.close()

print()

# =============================================================================
# 6. INTERACTIVE ANIMATION (JUPYTER)
# =============================================================================

print("=" * 60)
print("6. INTERACTIVE (JUPYTER) - CODE TEMPLATE")
print("=" * 60)

jupyter_code = """
# In Jupyter Notebook:
# %matplotlib widget  # or %matplotlib notebook for older versions

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x))

def animate(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True)

# Display in notebook
from IPython.display import HTML
HTML(ani.to_jshtml())

# Or save and display
ani.save('animation.gif', writer='pillow')
"""

print(jupyter_code)

# =============================================================================
# 7. ADVANCED: PARTICLE SYSTEM
# =============================================================================

print("=" * 60)
print("7. ADVANCED: PARTICLE SYSTEM")
print("=" * 60)

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.set_title('Particle System with Gravity')
ax.axis('off')

n_particles = 50
particles = {
    'x': np.random.uniform(-8, 8, n_particles),
    'y': np.random.uniform(5, 10, n_particles),
    'vx': np.random.uniform(-1, 1, n_particles),
    'vy': np.random.uniform(-1, 1, n_particles),
    'size': np.random.uniform(20, 100, n_particles),
    'color': np.random.rand(n_particles),
    'life': np.ones(n_particles)
}

scat = ax.scatter(particles['x'], particles['y'], 
                  s=particles['size'], c=particles['color'],
                  cmap='plasma', alpha=0.7, edgecolors='white')

def animate_particles(frame):
    # Physics
    particles['vy'] -= 0.05  # Gravity
    particles['x'] += particles['vx']
    particles['y'] += particles['vy']
    particles['life'] -= 0.01
    
    # Reset dead particles
    dead = particles['life'] <= 0
    if np.any(dead):
        particles['x'][dead] = np.random.uniform(-8, 8, np.sum(dead))
        particles['y'][dead] = np.random.uniform(5, 10, np.sum(dead))
        particles['vx'][dead] = np.random.uniform(-1, 1, np.sum(dead))
        particles['vy'][dead] = np.random.uniform(0, 1, np.sum(dead))
        particles['life'][dead] = 1.0
        particles['size'][dead] = np.random.uniform(20, 100, np.sum(dead))
    
    # Bounce off walls
    bounce_x = (particles['x'] < -10) | (particles['x'] > 10)
    particles['vx'][bounce_x] *= -0.8
    particles['x'][bounce_x] = np.clip(particles['x'][bounce_x], -10, 10)
    
    bounce_y = (particles['y'] < -10)
    particles['vy'][bounce_y] *= -0.5
    particles['y'][bounce_y] = -10
    
    # Alpha by life
    alphas = np.clip(particles['life'], 0.1, 1.0)
    
    scat.set_offsets(np.c_[particles['x'], particles['y']])
    scat.set_sizes(particles['size'] * alphas)
    scat.set_alpha(alphas)
    
    return scat,

ani = animation.FuncAnimation(fig, animate_particles, frames=200,
                               interval=30, blit=True)

ani.save('output/animation_particles.gif', writer='pillow', fps=30)
plt.close()

print("Particle system animation saved")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("ANIMATIONS COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. FuncAnimation(fig, func, frames, interval, blit)
2. init_func for initialization
3. Multiple artists returned as tuple for blit=True
4. Save formats: GIF (pillow), MP4 (ffmpeg), HTML (jshtml)
5. 3D animations with ax.clear() and replot
5. Particle systems with physics simulation
6. Jupyter: %matplotlib widget + HTML(ani.to_jshtml())

Next: Embedding in GUIs (Tkinter, PyQt), Web (Dash, Streamlit)
""")