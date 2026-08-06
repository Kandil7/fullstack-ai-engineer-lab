# Matplotlib Lecture 22: Styling and Themes

## 🎯 Topic Overview

A model report is only trustworthy if every figure renders identically
on every machine. This lecture covers the three knobs that make visual
output deterministic and honest: `rcParams` (process-wide defaults),
stylesheets (one-line theme families), and perceptually-uniform,
colorblind-safe colormaps (the alternative to `jet`, which invents
structure). It closes with `annotate()` — how to point the reader at
the evidence.

## 📚 Learning Objectives

1. Set global defaults once with `rcParams` before any figure exists.
2. Apply and scope named stylesheets with `plt.style.use` and
   `plt.style.context`.
3. Choose perceptually uniform, colorblind-safe colormaps and explain
   why `jet` is wrong for continuous data.
4. Add `annotate()` callouts (text + arrow) to highlight plateaus,
   anomalies, and operating points.
5. Assemble the full publication pipeline: rcParams → explicit ax →
   annotation → print-DPI export.

## 📋 Prerequisites

| Topic | Needed For |
|-------|-----------|
| Lecture 21 (OO API) | All demos |
| `imshow`, `colorbar` | Section 3 |
| `scatter`/`plot` basics | Sections 1-5 |

---

## 1. rcParams: Global Defaults, Set Once, Everywhere

`plt.rcParams` is a dict-like of process-wide style knobs: fonts, sizes,
DPI, grid defaults, spines. Set them at the top of a script (or in a
`matplotlibrc` file) **before any figure is created** — every figure
created afterward inherits them.

```python
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["font.size"] = 11
plt.rcParams["axes.grid"] = True
plt.rcParams["legend.frameon"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
```

Timing matters: rcParams are read when a figure is *created*, so
setting `figure.dpi` after `plt.subplots()` is too late for that
figure. The production pattern is a `set_publication_rcparams()`
function called once at startup — the same script then renders
identically on a laptop and in CI.

## 2. Stylesheets: One-Line Themes

A stylesheet is a family of rcParams under one name.
`plt.style.use("ggplot")` swaps the whole theme. To avoid leaking a
style into every later figure, scope it with a context manager:

```python
with plt.style.context("ggplot"):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, np.sin(x), lw=1.5)
    fig.savefig("style-ggplot.png", dpi=120)
```

`plt.style.available` lists the registered styles (e.g., `ggplot`,
`seaborn-v0_8-*`, `tableau-colorblind10`). Notebooks can
`plt.style.use` globally; scripts should prefer the context manager so
the visual identity of *this* figure is explicit and scoped.

## 3. Colormaps: Perceptually Uniform and Colorblind-Safe

Two properties make a colormap trustworthy:

- **Perceptually uniform**: equal data steps map to equal *perceived*
  steps in lightness — a smooth gradient in the data cannot turn into a
  fake contour.
- **Colorblind-safe**: distinguishable under deuteranopia/protanopia.

The canonical set is `viridis`, `plasma`, `inferno`, `magma`,
`cividis`. `jet` violates both: it is not uniform (banding invents
contours) and its green/orange region is hostile to red-green colorblind
readers.

```python
im = ax.imshow(data, cmap="viridis")   # honest magnitude
fig.colorbar(im, ax=ax)
```

Rule of thumb: **continuous data → a perceptually uniform map; never
`jet`/`rainbow`/`turbo`**. Use qualitative tab palettes
(`tab:blue`, `tab:orange`, …) for categorical series, not for heatmaps.

## 4. Annotation: Pointing the Reader at the Evidence

`ax.annotate(text, xy=..., xytext=...)` draws text plus an arrow from
`xytext` to the data coordinate `xy`. In ML reports this is how you mark
a plateau, an anomaly, or the chosen operating point.

```python
i_min = int(np.argmin(y))
ax.annotate(
    "observed min", xy=(x[i_min], y[i_min]),
    xytext=(7.5, 30), fontsize=10,
    arrowprops={"arrowstyle": "->", "color": "tab:red"},
)
```

`arrowprops` controls the arrow look (`"->"`, `"fancy"`, etc.).
`ax.texts` records the annotation artists, which makes them testable:
`assert len(ax.texts) == 1` in `_verify()`. Annotation is cheap and
reusable — the same call marks a different point when the data changes.

## 5. Publication Defaults End to End

The production pattern combines everything:

1. `set_publication_rcparams()` — once, before any figure.
2. Build with explicit `fig, ax` (Lecture 21).
3. Use perceptually uniform colormaps; annotate the story.
4. `fig.tight_layout()` then `fig.savefig(path, dpi=150)` and
   `plt.close(fig)`.

```python
set_publication_rcparams()
fig, ax = plt.subplots(figsize=(6, 4))
t = np.linspace(0, 2 * np.pi, 300)
ax.plot(t, np.sin(t), label="train", color="tab:blue")
ax.plot(t, np.sin(t) * np.exp(-t / 8), label="valid", color="tab:orange")
ax.set_xlabel("epoch")
ax.set_ylabel("metric")
ax.legend(loc="upper right")
fig.savefig(OUT_DIR / "22-publication.png", dpi=150)
plt.close(fig)
```

This single pattern — default once, style explicitly, save at print
DPI — is what makes figures in papers, model cards, and dashboards
reproducible artifacts rather than one-off screenshots.

---

## ⚠️ Common Mistakes to Avoid

1. **Using `jet`/`turbo`/`rainbow` for continuous data** — banding
   invents false contours; use `viridis` (or `plasma`/`inferno`/`magma`
   /`cividis`).
2. **Mutating global style without a scope** —
   `plt.style.use("dark_background")` leaks into every later plot; use
   `plt.style.context(...)` in scripts.
3. **Setting rcParams after figures exist** — defaults are read at
   figure creation; configure before `plt.subplots()`.
4. **Red-green-only signals** — a legend that is "green = good, red =
   bad" is unreadable for colorblind readers; pair color with markers,
   linestyles, or labels.
5. **Skipping `annotate` for key findings** — a report that never
   points at the anomaly makes the reader hunt for it.

## ✅ Best Practices

- Set `rcParams` once at the top of every plotting script; keep the
  list in one function so it is testable.
- Verify style in `_verify()`: assert `plt.rcParams["figure.dpi"] ==
  120`, `"ggplot" in plt.style.available`, and
  `is_perceptually_uniform("viridis")` is True while `jet` is False.
- Prefer `tab:` colors for categories and a PU map for heatmaps.
- Annotate exactly one message per figure — the finding.
- Save at `dpi>=150` for print; keep `tight_layout()` before saving.

## 📊 Complexity and Cost

| Operation | Cost |
|-----------|------|
| `plt.rcParams[...] = v` | O(1) — dict assignment |
| `plt.style.use` | O(params) one-time — applies to later figures |
| `plt.style.context` | O(params) per enter/exit — negligible |
| Colormap choice | **free** — pure lookup at render time |
| `ax.annotate` | O(1) — one text + one arrow artist |
| Perceptual-uniform rendering | O(pixels) same as any cmap |

Styling has essentially zero runtime cost; its value is entirely in
correctness and reproducibility. The only real cost is the discipline
of configuring *before* creating figures.

## 🤖 AI Engineering Relevance

- **Reproducible model cards**: rcParams + fixed seeds mean the figure
  in the model card is byte-for-byte the same one CI produced — the
  artifact is auditable.
- **Honest heatmaps**: attention maps, saliency, and loss landscapes
  are continuous data; a PU colormap is the difference between an
  honest magnitude map and one that invents structure (`jet`).
- **Accessibility as a requirement**: colorblind-safe palettes are part
  of shipping an eval dashboard to a team — not a nicety.
- **CI verification**: `_verify()` asserts the style contract (dpi,
  style availability, colormap policy) so a future refactor cannot
  silently degrade report quality.

## 🏋️ Practice Exercises

1. Write `set_publication_rcparams()` and assert three of its knobs in
   a verify function.
2. Render the same data under `ggplot` (scoped) and default style;
   confirm the default style is unchanged after the context exits.
3. Add `is_perceptually_uniform()` to your module and assert `jet` is
   rejected while all five canonical maps pass.
4. Annotate the minimum of a noisy curve and assert `len(ax.texts) ==
   1`; then change the data and re-run — the annotation must track the
   new minimum.

## 📌 Summary

- `rcParams` = process-wide defaults; set them once, before any figure.
- Stylesheets swap whole themes; scope them with
  `plt.style.context` to avoid leaks.
- Use perceptually uniform, colorblind-safe maps (`viridis`, `plasma`,
  `inferno`, `magma`, `cividis`); never `jet` for continuous data.
- `ax.annotate` adds evidence-pointing text+arrow artists that are
  testable via `ax.texts`.
- The publication pipeline = defaults once → explicit ax → annotation
  → print DPI → close.

## 📖 Quick Reference

| Task | Code |
|------|------|
| Global default | `plt.rcParams["font.size"] = 11` |
| Whole-theme swap | `plt.style.use("ggplot")` |
| Scoped theme | `with plt.style.context("ggplot"):` |
| List themes | `plt.style.available` |
| Honest heatmap | `ax.imshow(data, cmap="viridis")` |
| Is map uniform? | `cmap_name in {"viridis","plasma","inferno","magma","cividis"}` |
| Annotate point | `ax.annotate("min", xy=(x[i], y[i]), xytext=(7, 30), arrowprops={"arrowstyle": "->"})` |
| Count callouts | `len(ax.texts)` |

## ➡️ Next Steps

- Lecture 23 (ML Visualization): apply this styling discipline to the
  six canonical model-report plots.
- Lecture 24 (Saving and Export): make DPI, format, and transparency
  choices explicit — and verify them from the file header.
- Reference:
  https://matplotlib.org/stable/tutorials/introductory/customizing.html
