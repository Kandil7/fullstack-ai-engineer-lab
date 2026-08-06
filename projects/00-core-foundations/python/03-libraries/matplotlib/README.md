# Matplotlib Exercises — W3Schools Tutorial

Complete, runnable exercise scripts covering every major Matplotlib topic from the W3Schools tutorial. Each script contains 3–5 self-contained examples with `savefig()` output (no display required).

## Quick Start

```bash
# Run any single exercise
python 01-introduction.py

# Run all exercises
for f in [0-2]*.py; do python "$f"; done

# Output images appear in ./output/
```

## Requirements

- Python 3.8+
- `matplotlib`
- `numpy`
- `scipy` (used in exercises 11, 14)

```bash
pip install matplotlib numpy scipy
```

## File Reference

| # | File | Topic | Exercises |
|---|------|-------|-----------|
| 01 | `01-introduction.py` | Getting started, basic plots | 5 |
| 02 | `02-pyplot.py` | pyplot module basics | 5 |
| 03 | `03-plotting.py` | Line & marker customization | 5 |
| 04 | `04-markers.py` | Marker types & styles | 5 |
| 05 | `05-line.py` | Line plot techniques | 5 |
| 06 | `06-labels.py` | Titles, labels, annotations | 5 |
| 07 | `07-grid.py` | Grid line styling | 5 |
| 08 | `08-subplot.py` | Multi-panel layouts | 5 |
| 09 | `09-scatter.py` | Scatter plots | 5 |
| 10 | `10-bars.py` | Bar charts | 5 |
| 11 | `11-histograms.py` | Histograms & distributions | 5 |
| 12 | `12-pie-charts.py` | Pie & donut charts | 5 |
| 13 | `13-box-plots.py` | Box & violin plots | 5 |
| 14 | `14-area-plots.py` | Area / stacked area | 5 |
| 15 | `15-contour-plots.py` | Contour & filled contour | 5 |
| 16 | `16-wireframe.py` | 3D wireframe plots | 5 |
| 17 | `17-surface-plot.py` | 3D surface rendering | 5 |
| 18 | `18-3d-scatter.py` | 3D scatter plots | 5 |
| 19 | `19-3d-line.py` | 3D line / parametric curves | 5 |
| 20 | `20-3d-surface.py` | Advanced 3D surfaces | 5 |
| 21 | `21-object-oriented-api.py` | OO API: fig/ax, GridSpec, mosaic, shared axes | 5 |
| 22 | `22-styling-and-themes.py` | rcParams, stylesheets, colormaps, annotation | 5 |
| 23 | `23-ml-visualization.py` | Learning curves, confusion, ROC/PR, residuals | 6 |
| 24 | `24-saving-and-export.py` | DPI, vector vs raster, tight bbox, Agg | 5 |

**Total: 106 exercises across 24 scripts**

## Design Decisions

- All scripts use `matplotlib.use('Agg')` for headless rendering
- All plots save to `./output/` as PNG files (100 dpi)
- Each exercise is a standalone function — no global state leaks
- Uses `numpy` for data generation throughout
- 3D plots use `matplotlib`'s built-in `projection="3d"` (no external 3D libs)
- `scipy` is only imported where needed (KDE in exercise 11, smoothing in exercise 14)

## Exercise Highlights

### 2D Fundamentals (01–12)
- Line plots, markers, styles, colors
- Labels, titles, annotations, LaTeX notation
- Grids (major/minor, axis-specific)
- Subplots (shared axes, GridSpec, insets)
- Scatter (size/color mapping, regression, bubble charts)
- Bars (grouped, stacked, horizontal, error bars)
- Histograms (normalized, overlapping, KDE, 2D hexbin)
- Pies (exploded, donut, side-by-side)

### Statistical Plots (13–14)
- Box plots (horizontal, custom colors, outliers)
- Violin plot comparison
- Area plots (stacked, conditional fill, streamgraph)

### 3D Visualization (15–20)
- Contour & filled contour (terrain maps, label annotations)
- Wireframe (stride control, color mapping, saddle surfaces)
- Surface plots (lighting, wireframe overlay, multiple surfaces)
- 3D scatter (clusters, color-mapped, variable size)
- 3D lines (helix, Lissajous, parametric torus)
- Advanced 3D surfaces (projections, monkey saddle, view angles)

### Production Plotting (21–24)
- Object-Oriented API: explicit fig/ax, GridSpec, `subplot_mosaic`, shared axes
- Styling & themes: rcParams, scoped stylesheets, perceptually-uniform colormaps
- ML visualization: learning curves, confusion matrices, ROC/PR, residuals,
  feature importance, embedding scatter (sklearn metrics + numpy fallback)
- Saving & export: DPI contract, vector vs raster, `bbox_inches="tight"`,
  transparency, PNG-header verification for CI

## Advanced Series

Exercises 21–24 are the production-focused series (each self-verifying with
`--verify`). Companion material lives in `lectures/` (lecture + glossary per
topic) and `challenges/` (3-tier Bronze/Silver/Gold with pytest tests):

```bash
python 21-object-oriented-api.py --verify
python -m pytest 03-libraries/matplotlib/challenges/21-object-oriented-api -v
```
