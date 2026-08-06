# Matplotlib Lecture 22: Styling and Themes — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| `rcParams` | Process-wide matplotlib defaults | `plt.rcParams["font.size"] = 11` |
| Stylesheet | Named family of rcParams | `plt.style.use("ggplot")` |
| `plt.style.context` | Scope a style to a block | `with plt.style.context("dark_background"):` |
| Perceptually uniform | Equal data steps → equal perceived steps | `viridis`, `plasma`, `inferno`, `magma`, `cividis` |
| Colorblind-safe | Distinguishable under deuteranopia/protanopia | `viridis`, `tableau-colorblind10` |
| `jet` | Legacy rainbow map: banding + unsafe | *avoid for continuous data* |
| `annotate()` | Text + arrow to a data coordinate | `ax.annotate("min", xy=..., xytext=...)` |
| `arrowprops` | Arrow style for annotations | `{"arrowstyle": "->", "color": "tab:red"}` |
| `ax.texts` | List of text artists (testable) | `assert len(ax.texts) == 1` |
| `matplotlibrc` | rcParams file loaded at startup | `matplotlib.rc_file("style.rc")` |

## Detailed Definitions

**rcParams** — A dict-like of ~300 process-global style knobs read
when figures are *created*. Setting them at the top of a script makes
every later figure inherit the same fonts, sizes, DPI, grids, and
spines. Setting them after figure creation is too late for that figure.

**Stylesheet** — A registered family of rcParams under one name
(`ggplot`, `seaborn-v0_8-darkgrid`, `tableau-colorblind10`, …).
`plt.style.available` lists them. Swaps the whole visual theme in one
line.

**`plt.style.context(name)`** — Context manager that applies a
stylesheet inside the block and restores the previous params on exit.
The script-safe way to use a theme without leaking it into later
figures.

**Perceptually uniform colormap** — A map whose perceived lightness is
a monotonic function of the data value, so equal data steps read as
equal visual steps. Prevents fake contours from banding. The canonical
set: `viridis`, `plasma`, `inferno`, `magma`, `cividis`.

**Colorblind-safe** — Perceptible by readers with deuteranopia /
protanopia (red-green deficiency). `jet` fails this because its
green/orange region collapses for such readers.

**`jet`** — The classic rainbow colormap. Not perceptually uniform
(banding invents structure) and not colorblind-safe. Fine for
qualitative decoration, never for continuous magnitude data.

**`annotate(text, xy, xytext, arrowprops)`** — Draws text at `xytext`
plus an arrow to the data point `xy`. The standard way to highlight a
plateau, anomaly, or operating point in a report figure.

## Key Concepts Summary

- Style is a correctness concern: reproducible figures need defaults
  set once, scoped themes, and honest colormaps.
- Continuous data → PU map; categories → `tab:` palette.
- Annotations are artists (`ax.texts`) — testable like any other
  artist.

## Practice Terms

1. Why must `rcParams` be set before `plt.subplots()`?
2. What is the difference between `plt.style.use` and
   `plt.style.context`?
3. Name the five canonical perceptually-uniform colormaps.
4. Why is `jet` wrong for a loss heatmap?
5. Which attribute lets you count annotations in a verify function?

*(Answers: 1. Defaults are read at figure creation. 2. `use` is
permanent; `context` restores on block exit. 3. viridis, plasma,
inferno, magma, cividis. 4. Banding invents false contours and it is
not colorblind-safe. 5. `ax.texts`.)*
