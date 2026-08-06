# Matplotlib Lecture 24: Saving and Export

## 🎯 Topic Overview

Reports and model cards are rendered headless in CI, then embedded in
docs, papers, and slides. If your `savefig` settings are wrong, a 6x4
figure silently becomes a 0.2 MP blur or an SVG that overflows a page.
This lecture covers the export contract: **pixels = inches × dpi**,
vector vs raster formats, `bbox_inches="tight"`, transparent
backgrounds, the Agg backend for headless rendering — and how to
*verify* what you exported by parsing the PNG header with `struct`.

## 📚 Learning Objectives

1. Compute exact pixel dimensions from `figsize` and `dpi` and prove
   them by reading the PNG IHDR chunk.
2. Choose between vector (SVG/PDF) and raster (PNG) formats per
   artifact.
3. Crop whitespace with `bbox_inches="tight"`.
4. Export transparent-background figures (RGBA, PNG color type 6).
5. Use the Agg backend to render identically on any machine, including
   bare CI containers.

## 📋 Prerequisites

| Topic | Needed For |
|-------|-----------|
| Lectures 21-23 | All demos |
| `struct.unpack` | Section 1 (PNG header) |
| Binary file I/O | Section 1 |

---

## 1. DPI: The Contract Between Inches and Pixels

A figure is sized in **inches**; `dpi` (dots per inch) converts to
pixels *at export time*. `figsize=(6, 4)` at `dpi=150` →
**exactly 900 × 600 px**. This is a contract you can assert in CI.

```python
fig, ax = plt.subplots(figsize=(6, 4))
fig.savefig(path, dpi=150)      # -> 900 x 600 pixels
```

Prove it by parsing the PNG header — the file itself is the source of
truth (no image library needed):

```python
def png_dimensions(path):
    with open(path, "rb") as fh:
        data = fh.read(33)                    # signature + IHDR
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "file must be a PNG"
    assert data[12:16] == b"IHDR", "first chunk must be IHDR"
    width, height = struct.unpack(">II", data[16:24])   # big-endian
    return width, height
```

Layout: 8-byte signature, 4-byte chunk length, 4-byte `"IHDR"`, then
width (4 bytes BE) and height (4 bytes BE). O(1), deterministic —
exactly the kind of artifact assertion CI should run.

## 2. Vector vs Raster: SVG Keeps Text as Text

- **Raster (PNG)** stores pixels: zoom in and it blurs; text becomes a
  pixel pattern.
- **Vector (SVG/PDF)** stores drawing commands: infinitely sharp at any
  zoom, and labels remain selectable text (searchable in PDFs).

```python
fig.savefig("fig.svg")          # vector: sharp, editable text
fig.savefig("fig.png", dpi=120) # raster: for previews/thumbnails
```

Papers and dashboards use vector; thumbnails and web previews use
raster. A saved SVG starts with `<?xml ... <svg ...>` — checkable by
reading the first bytes.

## 3. bbox_inches="tight": Crop the Whitespace

Default saving keeps the full figure canvas, so labels near the edge
can be clipped. `bbox_inches="tight"` recomputes the bounding box from
the artists and crops to exactly what is drawn:

```python
fig.savefig("loose.png", dpi=100)
fig.savefig("tight.png", dpi=100, bbox_inches="tight")
```

Verifiable property: the tight export must be **≤** the loose export in
both dimensions and, on a canvas with edge-hugging labels, strictly
smaller. This is the standard for embedding figures in reports — no
post-hoc image cropping.

## 4. Transparent Background: Compositing onto Slides

`transparent=True` drops the facecolor from the raster so the figure
can sit on a colored slide or dark dashboard without a white box:

```python
fig.savefig(path, dpi=100, transparent=True)
```

Proof: the PNG header's byte 25 (color type) becomes **6 = RGBA**,
meaning an alpha channel is stored:

```python
def png_has_alpha(path):
    with open(path, "rb") as fh:
        data = fh.read(26)
    return data[25] == 6
```

Color type 6 is the only one with transparency in PNG; this assertion
catches `transparent=True` silently not taking effect.

## 5. The Agg Backend and Reproducibility

The Agg backend renders to memory with **no window server**, which is
why CI can run on a bare container. The rule: call
`matplotlib.use("Agg")` **before** importing `pyplot`.

```python
import matplotlib
matplotlib.use("Agg")   # MUST precede pyplot import
import matplotlib.pyplot as plt
```

Combined with fixed `figsize` and `dpi`, the same script on any machine
produces the same pixel dimensions (and, with a seeded RNG, essentially
identical bytes). This is what makes figures CI-testable artifacts:
`assert png_dimensions(path) == (900, 600)`.

---

## ⚠️ Common Mistakes to Avoid

1. **`savefig` after `plt.show()`** — interactive backends may clear
   the canvas; save *before* `show`, or never call `show` in scripts.
2. **Default DPI for print** — 6x4 at default 100 dpi is 600x400 px,
   blurry in a paper; use `dpi=300` for print, `150` for screens.
3. **Relying on GUI backends in tests** — `import matplotlib.pyplot`
   without `matplotlib.use("Agg")` may open windows on dev machines;
   force Agg in CI-facing scripts.
4. **Raster for text-heavy figures** — labels in PNGs are not
   searchable/selectable; use SVG/PDF for reports.
5. **Trusting "it looks fine"** — assert `png_dimensions` and file
   size; what you cannot measure, you cannot verify in CI.

## ✅ Best Practices

- Compute expected pixels by hand (`6*150 x 4*150`) and assert them
  from the header.
- Vector for papers/dashboards, raster for previews; never the reverse
  for text-heavy figures.
- Always `bbox_inches="tight"` when embedding in reports.
- Use `transparent=True` for figures destined for slides/dark UIs, and
  verify color type 6.
- Put `matplotlib.use("Agg")` as the first two lines of every
  headless/CI script.

## 📊 Complexity and Cost

| Operation | Cost |
|-----------|------|
| `savefig` PNG | O(pixels) — dominated by rasterization |
| `savefig` SVG | O(artists) — commands, not pixels; tiny files |
| PNG header parse | O(1) — 33 bytes |
| `bbox_inches="tight"` | O(artists) — one extra layout pass |
| `transparent=True` | O(pixels), RGBA instead of RGB |

Vector files are typically orders of magnitude smaller than raster for
line plots. Header parsing is free and gives you a CI assertion that
costs nothing.

## 🤖 AI Engineering Relevance

- **CI artifact contracts**: `assert png_dimensions(path) == (900,
  600)` turns "the report renders" into a machine-checked guarantee.
- **Headless generation**: Agg means model cards, eval dashboards, and
  paper figures can be generated in containers, lambdas, and background
  jobs without a display.
- **Compositing**: transparent exports are how dashboard panels and
  slides stay visually consistent on any background color.
- **Vector for governance**: SVG/PDF keeps labels selectable and text
  searchable — important for audit-ready model documentation.

## 🏋️ Practice Exercises

1. Save a 6x4 figure at 150 dpi and assert `png_dimensions` returns
   `(900, 600)`.
2. Export the same figure as SVG and PNG; assert the SVG starts with
   `<svg` and the PNG with the 8-byte signature.
3. Compare loose vs tight exports and assert tight ≤ loose in both
   dimensions (and strictly smaller on this figure).
4. Save with `transparent=True` and assert `png_has_alpha` returns
   True; then save without it and assert False.
5. Render the same figure twice with the same seed and assert equal
   pixel dimensions (and equal file sizes if your backend is
   deterministic).

## 📌 Summary

- `pixels = inches × dpi`; assert the PNG IHDR header to prove it.
- SVG/PDF are vector (sharp, selectable text); PNG is raster.
- `bbox_inches="tight"` crops whitespace; `transparent=True` writes
  RGBA (color type 6).
- Agg renders headless — required for CI — and fixed figsize/dpi make
  exports reproducible.
- Verify exports with header parsing; never trust "looks fine".

## 📖 Quick Reference

| Task | Code |
|------|------|
| Pixels from inches | `figsize=(6, 4)`, `dpi=150` → 900×600 |
| Vector export | `fig.savefig("fig.svg")` |
| Raster export | `fig.savefig("fig.png", dpi=150)` |
| Crop whitespace | `fig.savefig("fig.png", bbox_inches="tight")` |
| Transparent | `fig.savefig("fig.png", transparent=True)` |
| Headless | `matplotlib.use("Agg")` before `import pyplot` |
| Read PNG size | `struct.unpack(">II", data[16:24])` |
| Is PNG RGBA? | `data[25] == 6` |

## ➡️ Next Steps

- Combine lectures 21-24 into a CI report generator: OO API +
  rcParams + ML plots, all exported with verified headers.
- Reference:
  https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig
