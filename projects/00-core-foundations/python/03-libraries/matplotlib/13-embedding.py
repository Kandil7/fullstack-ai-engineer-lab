"""
Matplotlib Embedding in GUIs and Web
=====================================

Integrating matplotlib in Tkinter, PyQt, Dash, Streamlit, and Jupyter.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# 1. TKINTER EMBEDDING
# =============================================================================

print("=" * 60)
print("1. TKINTER EMBEDDING (CODE TEMPLATE)")
print("=" * 60)

tkinter_code = '''
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib in Tkinter")
        self.root.geometry("800x600")
        
        # Create figure
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Initial plot
        self.x = np.linspace(0, 10, 100)
        self.line, = self.ax.plot(self.x, np.sin(self.x))
        self.ax.set_title("Interactive Sine Wave")
        self.ax.grid(True)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        
        # Controls
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.control_frame, text="Frequency:").pack(side=tk.LEFT)
        self.freq_var = tk.DoubleVar(value=1.0)
        self.freq_scale = ttk.Scale(self.control_frame, from_=0.1, to=5.0, 
                                     variable=self.freq_var, orient=tk.HORIZONTAL,
                                     command=self.update_plot)
        self.freq_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(self.control_frame, text="Amplitude:").pack(side=tk.LEFT)
        self.amp_var = tk.DoubleVar(value=1.0)
        self.amp_scale = ttk.Scale(self.control_frame, from_=0.1, to=3.0,
                                    variable=self.amp_var, orient=tk.HORIZONTAL,
                                    command=self.update_plot)
        self.amp_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Button(self.control_frame, text="Random", 
                   command=self.random_wave).pack(side=tk.LEFT, padx=10)
        
    def update_plot(self, event=None):
        freq = self.freq_var.get()
        amp = self.amp_var.get()
        self.line.set_ydata(amp * np.sin(freq * self.x))
        self.canvas.draw_idle()
    
    def random_wave(self):
        self.freq_var.set(np.random.uniform(0.5, 3))
        self.amp_var.set(np.random.uniform(0.5, 2))
        self.update_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
'''

print(tkinter_code)
print()

# =============================================================================
# 2. PYQT EMBEDDING
# =============================================================================

print("=" * 60)
print("2. PYQT EMBEDDING (CODE TEMPLATE)")
print("=" * 60)

pyqt_code = '''
import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QWidget, QSlider, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib in PyQt5")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Canvas
        self.canvas = MplCanvas(self, width=7, height=5, dpi=100)
        layout.addWidget(self.canvas)
        
        # Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        
        # Controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        controls_layout.addWidget(QLabel("Frequency:"))
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setRange(1, 50)
        self.freq_slider.setValue(10)
        self.freq_slider.valueChanged.connect(self.update_plot)
        controls_layout.addWidget(self.freq_slider)
        
        controls_layout.addWidget(QLabel("Amplitude:"))
        self.amp_slider = QSlider(Qt.Horizontal)
        self.amp_slider.setRange(1, 30)
        self.amp_slider.setValue(10)
        self.amp_slider.valueChanged.connect(self.update_plot)
        controls_layout.addWidget(self.amp_slider)
        
        layout.addWidget(controls)
        
        # Initial plot
        self.x = np.linspace(0, 10, 200)
        self.line, = self.canvas.ax.plot(self.x, np.sin(self.x))
        self.canvas.ax.set_title("Interactive Sine Wave")
        self.canvas.ax.grid(True)
        
    def update_plot(self):
        freq = self.freq_slider.value() / 10.0
        amp = self.amp_slider.value() / 10.0
        self.line.set_ydata(amp * np.sin(freq * self.x))
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
'''

print(pyqt_code)
print()

# =============================================================================
# 3. DASH (WEB DASHBOARDS)
# =============================================================================

print("=" * 60)
print("3. DASH WEB DASHBOARDS (CODE TEMPLATE)")
print("=" * 60)

dash_code = '''
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd

app = dash.Dash(__name__)

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y1': np.sin(np.linspace(0, 10, 100)),
    'y2': np.cos(np.linspace(0, 10, 100)),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

app.layout = html.Div([
    html.H1("Interactive Dashboard with Dash", style={'textAlign': 'center'}),
    
    # Controls
    html.Div([
        html.Label("Function:"),
        dcc.Dropdown(
            id='function-dropdown',
            options=[
                {'label': 'Sine', 'value': 'sin'},
                {'label': 'Cosine', 'value': 'cos'},
                {'label': 'Tangent', 'value': 'tan'},
                {'label': 'Sine + Cosine', 'value': 'sin+cos'}
            ],
            value='sin',
            style={'width': '200px', 'display': 'inline-block'}
        ),
        
        html.Label(" Frequency:", style={'marginLeft': '20px'}),
        dcc.Slider(
            id='freq-slider',
            min=0.1, max=5, step=0.1, value=1,
            marks={i: str(i) for i in range(1, 6)},
            tooltip={'placement': 'bottom', 'always_visible': True}
        ),
        
        html.Label(" Amplitude:", style={'marginLeft': '20px'}),
        dcc.Slider(
            id='amp-slider',
            min=0.1, max=3, step=0.1, value=1,
            marks={i: str(i) for i in range(1, 4)},
            tooltip={'placement': 'bottom', 'always_visible': True}
        ),
    ], style={'padding': '20px', 'backgroundColor': '#f5f5f5'}),
    
    # Plots
    html.Div([
        dcc.Graph(id='main-plot'),
    ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    html.Div([
        dcc.Graph(id='dist-plot'),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
])

@callback(
    Output('main-plot', 'figure'),
    [Input('function-dropdown', 'value'),
     Input('freq-slider', 'value'),
     Input('amp-slider', 'value')]
)
def update_main_plot(func, freq, amp):
    x = np.linspace(0, 10, 200)
    if func == 'sin':
        y = amp * np.sin(freq * x)
    elif func == 'cos':
        y = amp * np.cos(freq * x)
    elif func == 'tan':
        y = amp * np.tan(freq * x)
        y = np.clip(y, -5, 5)  # Clip for visibility
    else:  # sin+cos
        y = amp * (np.sin(freq * x) + np.cos(freq * x))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', 
                             name=f'{amp}×{func}({freq}x)',
                             line=dict(width=2)))
    fig.update_layout(title=f'Function: {amp}×{func}({freq}x)',
                      xaxis_title='x', yaxis_title='y',
                      hovermode='x unified', template='plotly_white')
    return fig

@callback(
    Output('dist-plot', 'figure'),
    [Input('function-dropdown', 'value'),
     Input('freq-slider', 'value'),
     Input('amp-slider', 'value')]
)
def update_dist_plot(func, freq, amp):
    x = np.linspace(0, 10, 1000)
    if func == 'sin':
        y = amp * np.sin(freq * x)
    elif func == 'cos':
        y = amp * np.cos(freq * x)
    elif func == 'tan':
        y = np.clip(amp * np.tan(freq * x), -5, 5)
    else:
        y = amp * (np.sin(freq * x) + np.cos(freq * x))
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=y, nbinsx=30, name='Distribution'))
    fig.update_layout(title='Value Distribution', 
                      xaxis_title='y', yaxis_title='Count',
                      template='plotly_white')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
'''

print(dash_code)
print()

# =============================================================================
# 4. STREAMLIT
# =============================================================================

print("=" * 60)
print("4. STREAMLIT (CODE TEMPLATE)")
print("=" * 60)

streamlit_code = '''
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="ML Dashboard", layout="wide")

st.title("🔬 Interactive ML Dashboard")

# Sidebar controls
st.sidebar.header("Controls")

# Function selection
func_type = st.sidebar.selectbox(
    "Function",
    ["Sine", "Cosine", "Tangent", "Sine + Cosine", "Gaussian", "Polynomial"]
)

# Parameters
freq = st.sidebar.slider("Frequency", 0.1, 5.0, 1.0, 0.1)
amp = st.sidebar.slider("Amplitude", 0.1, 3.0, 1.0, 0.1)
phase = st.sidebar.slider("Phase Shift", 0.0, 2*np.pi, 0.0, 0.1)
noise = st.sidebar.slider("Noise Level", 0.0, 1.0, 0.0, 0.05)

# Plot type
plot_backend = st.sidebar.radio("Plot Backend", ["Matplotlib", "Plotly"])

# Generate data
x = np.linspace(0, 10, 500)
if func_type == "Sine":
    y = amp * np.sin(freq * x + phase)
elif func_type == "Cosine":
    y = amp * np.cos(freq * x + phase)
elif func_type == "Tangent":
    y = np.clip(amp * np.tan(freq * x + phase), -5, 5)
elif func_type == "Sine + Cosine":
    y = amp * (np.sin(freq * x + phase) + np.cos(freq * x + phase))
elif func_type == "Gaussian":
    y = amp * np.exp(-((x - 5) ** 2) / (2 * freq ** 2))
else:  # Polynomial
    y = amp * (freq * x ** 2 - 5 * x + phase)

if noise > 0:
    y += np.random.normal(0, noise, len(x))

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Main Visualization")
    
    if plot_backend == "Matplotlib":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, 'b-', linewidth=2, alpha=0.8)
        ax.fill_between(x, y, alpha=0.2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'{func_type}: A={amp}, f={freq}, φ={phase:.2f}')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', 
                                 line=dict(width=2, color='royalblue'),
                                 fill='tozeroy', fillcolor='rgba(65, 105, 225, 0.2)'))
        fig.update_layout(title=f'{func_type}: A={amp}, f={freq}, φ={phase:.2f}',
                          xaxis_title='x', yaxis_title='y',
                          template='plotly_white', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Statistics")
    
    # Metrics
    st.metric("Mean", f"{np.mean(y):.3f}")
    st.metric("Std Dev", f"{np.std(y):.3f}")
    st.metric("Min", f"{np.min(y):.3f}")
    st.metric("Max", f"{np.max(y):.3f}")
    
    # Distribution
    if plot_backend == "Plotly":
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(x=y, nbinsx=30, name='Distribution'))
        fig_dist.update_layout(title='Value Distribution', height=300)
        st.plotly_chart(fig_dist, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(y, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title('Distribution')
        st.pyplot(fig)
        plt.close()
    
    # Download data
    df = pd.DataFrame({'x': x, 'y': y})
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='function_data.csv',
        mime='text/csv'
    )

# Additional plots
st.subheader("Additional Views")

tab1, tab2, tab3 = st.tabs(["Derivative", "Integral", "3D Surface"])

with tab1:
    # Numerical derivative
    dy_dx = np.gradient(y, x)
    if plot_backend == "Plotly":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=dy_dx, mode='lines', name='dy/dx'))
        fig.update_layout(title='Derivative', template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(x, dy_dx, 'r-', linewidth=1)
        ax.set_title('Derivative')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()

with tab2:
    # Cumulative integral
    integral = np.cumsum(y) * (x[1] - x[0])
    if plot_backend == "Plotly":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=integral, mode='lines', name='∫y dx'))
        fig.update_layout(title='Cumulative Integral', template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(x, integral, 'g-', linewidth=1)
        ax.set_title('Cumulative Integral')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()

with tab3:
    # 3D surface from 1D function
    X, Y = np.meshgrid(np.linspace(0, 10, 50), np.linspace(0, 10, 50))
    Z = amp * np.sin(freq * X + phase) * np.cos(freq * Y + phase)
    
    if plot_backend == "Plotly":
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig.update_layout(title='3D Surface', scene=dict(
            xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("3D plots require Plotly backend")

# Code display
with st.expander("View Source Code"):
    st.code('''
import numpy as np
x = np.linspace(0, 10, 500)
y = amp * np.sin(freq * x + phase)
''', language='python')

st.sidebar.markdown("---")
st.sidebar.info("Built with Streamlit + Matplotlib/Plotly")
'''

print(streamlit_code)
print()

# =============================================================================
# 5. JUPYTER WIDGETS
# =============================================================================

print("=" * 60)
print("5. JUPYTER INTERACTIVE WIDGETS")
print("=" * 60)

jupyter_code = '''
# In Jupyter Notebook/Lab:
# %matplotlib widget  # for interactive matplotlib
# or %matplotlib ipympl

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

# Simple interactive
@interact(freq=(0.1, 5.0, 0.1), amp=(0.1, 3.0, 0.1), phase=(0, 6.28, 0.1))
def plot_sine(freq=1.0, amp=1.0, phase=0.0):
    x = np.linspace(0, 10, 200)
    y = amp * np.sin(freq * x + phase)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, 'b-', linewidth=2)
    ax.fill_between(x, y, alpha=0.2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Sine Wave: A={amp}, f={freq}, φ={phase:.2f}')
    ax.grid(True, alpha=0.3)
    plt.show()

# Multiple controls with layout
freq_slider = widgets.FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1, description='Frequency:')
amp_slider = widgets.FloatSlider(value=1.0, min=0.1, max=3.0, step=0.1, description='Amplitude:')
func_dropdown = widgets.Dropdown(options=['sin', 'cos', 'tan', 'sin+cos'], value='sin', description='Function:')
noise_slider = widgets.FloatSlider(value=0.0, min=0.0, max=1.0, step=0.05, description='Noise:')

ui = widgets.HBox([freq_slider, amp_slider, func_dropdown, noise_slider])

@interactive
def plot_function(freq=freq_slider, amp=amp_slider, func=func_dropdown, noise=noise_slider):
    x = np.linspace(0, 10, 200)
    if func == 'sin':
        y = amp * np.sin(freq * x)
    elif func == 'cos':
        y = amp * np.cos(freq * x)
    elif func == 'tan':
        y = np.clip(amp * np.tan(freq * x), -5, 5)
    else:
        y = amp * (np.sin(freq * x) + np.cos(freq * x))
    
    if noise > 0:
        y += np.random.normal(0, noise, len(x))
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, linewidth=2)
    ax.set_title(f'{func}: A={amp}, f={freq}, noise={noise}')
    ax.grid(True, alpha=0.3)
    plt.show()

display(ui)
display(plot_function)

# Linked widgets
x_range = widgets.IntRangeSlider(value=[0, 10], min=0, max=20, description='X Range:')
y_scale = widgets.FloatLogSlider(value=1, base=10, min=-2, max=2, description='Y Scale:')

@interact(x_range=x_range, y_scale=y_scale)
def plot_range(x_range=(0, 10), y_scale=1.0):
    x = np.linspace(x_range[0], x_range[1], 200)
    y = np.sin(x) * y_scale
    plt.figure(figsize=(8, 3))
    plt.plot(x, y)
    plt.ylim(-y_scale*1.5, y_scale*1.5)
    plt.grid(True, alpha=0.3)
    plt.show()

# Manual button for expensive computations
@interact_manual(n_points=(100, 10000, 100), freq=(0.1, 5.0, 0.1))
def expensive_plot(n_points=500, freq=1.0):
    x = np.linspace(0, 10, n_points)
    y = np.sin(freq * x) + np.random.normal(0, 0.1, n_points)
    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, s=1, alpha=0.5)
    plt.title(f'{n_points} points, freq={freq}')
    plt.grid(True, alpha=0.3)
    plt.show()

# Custom widget with callbacks
class PlotController:
    def __init__(self):
        self.freq = widgets.FloatSlider(value=1, min=0.1, max=5, step=0.1)
        self.amp = widgets.FloatSlider(value=1, min=0.1, max=3, step=0.1)
        self.color = widgets.ColorPicker(value='blue', description='Color:')
        self.update_btn = widgets.Button(description='Update Plot')
        self.output = widgets.Output()
        
        self.freq.observe(self.on_change, names='value')
        self.amp.observe(self.on_change, names='value')
        self.color.observe(self.on_change, names='value')
        self.update_btn.on_click(self.on_click)
    
    def on_change(self, change):
        self.plot()
    
    def on_click(self, btn):
        with self.output:
            self.output.clear_output()
            self.plot()
    
    def plot(self):
        with self.output:
            x = np.linspace(0, 10, 200)
            y = self.amp.value * np.sin(self.freq.value * x)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(x, y, color=self.color.value, linewidth=2)
            ax.set_title(f'Custom Controller')
            ax.grid(True, alpha=0.3)
            plt.show()
    
    def show(self):
        controls = widgets.VBox([self.freq, self.amp, self.color, self.update_btn])
        display(widgets.HBox([controls, self.output]))

controller = PlotController()
controller.show()
'''

print(jupyter_code)
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 60)
print("EMBEDDING COMPLETE")
print("=" * 60)
print("""
Key Concepts:
1. Tkinter: FigureCanvasTkAgg + NavigationToolbar2Tk
2. PyQt5: FigureCanvasQTAgg + NavigationToolbar2QT
3. Dash: Declarative Python web apps with Plotly
4. Streamlit: Rapid data app development
5. Jupyter: %matplotlib widget + ipywidgets interact

Production Tips:
- Use blit=True for smooth animations
- debounce/throttle slider callbacks
- Cache expensive computations
- Use Plotly for web interactivity
- matplotlib for publication-quality static plots

Next: Case studies, best practices, performance optimization
""")