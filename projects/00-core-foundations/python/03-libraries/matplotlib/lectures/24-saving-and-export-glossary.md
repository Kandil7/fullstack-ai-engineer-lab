# Matplotlib Lecture 24: Saving and Export — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| DPI | Dots per inch: inches × dpi = pixels | `fig.savefig(p, dpi=150)` |
| Vector format | Drawing commands, infinitely sharp | `fig.savefig("fig.svg")` |
| Raster format | Pixel grid, blurs when zoomed | `fig.savefig("fig.png")` |
| `bbox_inches="tight"` | Crop canvas to the artists | `fig.savefig(p, bbox_inches="tight")` |
| `transparent=True` | Drop facecolor → RGBA PNG | `fig.savefig(p, transparent=True)` |
| Agg backend | Headless renderer, no window server | `matplotlib.use("Agg")` before pyplot |
| IHDR | First PNG chunk: width/height/color type | `struct.unpack(">II", data[16:24])` |
| Color type 6 | RGBA — PNG with transparency | `data[25] == 6` |
| `figsize` | Figure size in inches | `plt.subplots(figsize=(6, 4))` |
| `savefig` | Export a figure to a file | `fig.savefig(path, dpi=150)` |

## Detailed Definitions

**DPI (dots per inch)** — The resolution at export time converting
figure inches to output pixels: `figsize=(6, 4)` at `dpi=150` gives
exactly `900 × 600` px. Print uses ≥300; screens ~150; the value is a
contract you can assert.

**Vector format (SVG/PDF)** — Stores drawing commands, not pixels:
infinitely sharp at any zoom, text remains selectable/searchable.
Preferred for papers, dashboards, and auditable model docs. SVG files
start with `<?xml ... <svg ...>`.

**Raster format (PNG/JPEG)** — Stores a pixel grid: sharp only at
native resolution, text is not selectable. Preferred for previews and
thumbnails. PNG adds lossless compression and an alpha channel option.

**`bbox_inches="tight"`** — Tells `savefig` to recompute the canvas
bounding box from the drawn artists and crop whitespace. The standard
for embedding figures in reports; verifiable as ≤ the loose export's
dimensions.

**`transparent=True`** — Drops the figure facecolor from the raster,
writing an RGBA image (PNG color type 6) that composites onto colored
slides/dashboards. Verified by reading byte 25 of the PNG header.

**Agg backend** — Matplotlib's headless renderer: draws into memory,
requires no display server. `matplotlib.use("Agg")` must run *before*
`import matplotlib.pyplot as plt`. What makes CI rendering possible.

**IHDR chunk** — The first PNG data chunk; its payload holds width
(4 bytes BE), height (4 bytes BE), bit depth, and color type. Reading
33 bytes + `struct.unpack(">II", data[16:24])` gives exact pixel
dimensions with no image library.

**Color type 6** — PNG color type meaning RGBA (red, green, blue,
alpha). A transparent export writes type 6; an opaque one writes type
2 (RGB). Byte 25 of the file distinguishes them.

## Key Concepts Summary

- `pixels = inches × dpi`; verify from the header, never by eye.
- Vector for text-heavy/governance artifacts; raster for previews.
- Agg + fixed figsize/dpi = reproducible, CI-testable exports.

## Practice Terms

1. What pixel size does `figsize=(6, 4)` at `dpi=150` produce?
2. Why does a PNG blur when zoomed but an SVG does not?
3. What does `bbox_inches="tight"` do, and how do you verify it?
4. How can you prove a PNG has a transparent background?
5. Where must `matplotlib.use("Agg")` appear in a script?

*(Answers: 1. 900×600. 2. PNG stores pixels; SVG stores drawing
commands. 3. Crops the canvas to the artists; assert tight ≤ loose in
both dimensions. 4. Read the header: byte 25 == 6 (RGBA). 5. Before
`import matplotlib.pyplot`.)*
