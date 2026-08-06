# Matplotlib Lecture 21: The Object-Oriented API

## 🎯 Topic Overview

The Object-Oriented (OO) API is the production-grade way to drive
Matplotlib: you create an explicit `Figure` (the canvas) and one or more
explicit `Axes` (plot regions) and style everything through those
objects. This lecture explains why the implicit `plt.*` state machine is
a correctness hazard in scripts, and covers the three layout tools that
make complex figures manageable: `GridSpec` for unequal grids,
`subplot_mosaic` for named panels, and `sharex`/`sharey` for aligned,
joined axes.

## 📚 Learning Objectives

1. Build and style figures exclusively through explicit `Figure`/`Axes`
   objects.
2. Explain why the `plt.*` state machine leaks state between cells,
   threads, and CI runs.
3. Create unequal grid layouts with `GridSpec` (relative row/column
   ratios).
4. Build named multi-panel layouts with `subplot_mosaic` and address
   panels by label, not by index arithmetic.
5. Use `sharex`/`sharey` to align scales across panels and understand
   that shared axes are *joined* (limit changes propagate).

## 📋 Prerequisites

| Topic | Needed For |
|-------|-----------|
| Basic `plt.subplots()` | Sections 1-5 |
| `np.linspace`, `np.sin/cos` | All demos |
| Figures in loops / notebooks | Section 2 (state machine) |

---

## 1. Figure and Axes: the Explicit Contract

A `Figure` is the whole canvas (paper, size, background). An `Axes` is
one plot region inside it — the thing that actually has a coordinate
system and artists. The discipline is: **hold both explicitly, never
ask "where is the current axes?"**

```python
fig, ax = plt.subplots(figsize=(6, 4))
x = np.linspace(0, 2 * np.pi, 100)
ax.plot(x, np.sin(x), label="sin(x)")
ax.set_title("Explicit fig/ax")
ax.set_xlabel("x (rad)")
ax.set_ylabel("sin(x)")
ax.legend()
fig.tight_layout()
fig.savefig("fig.png", dpi=120)
plt.close(fig)      # release the canvas (critical in loops)
```

Every styling call — `set_title`, `set_xlabel`, `legend`, `grid`,
`set_xlim` — lives on the `Axes`. With explicit objects, any panel can
be re-styled, re-drawn, or unit-tested in isolation because there is no
hidden state to corrupt.

## 2. Why the plt.\* State Machine Breaks in Scripts

`plt.plot(x, y)` targets "the current axes", a process-global. In a
notebook that is convenient; in a script or a test runner it is a
correctness hazard:

- Another call, a style change, or a context manager can silently
  retarget the next plot into a figure you thought you closed.
- Two figures created in the same run share one implicit "current
  axes"; `plt.gca()` follows whichever figure was touched last
  (`plt.sca(ax)` sets it explicitly).
- Threaded or CI-reused code makes the ordering non-deterministic.

```python
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
plt.sca(ax2)                     # "set current axes"
assert plt.gca() is ax2          # gca() follows global state
```

The fix is not "be careful with `plt.sca`" — it is to stop using the
implicit target entirely. One figure, one `ax` variable, and everything
becomes inspectable, testable, and exportable.

## 3. GridSpec: Unequal Grid Layouts

`fig.add_gridspec(nrows, ncols, height_ratios=..., width_ratios=...)`
creates a layout where rows and columns can have **relative** sizes.
The classic use: a wide/tall main panel above a small summary panel
(e.g., a raw signal above its step indicator, or a loss curve above a
learning-rate schedule).

```python
fig = plt.figure(figsize=(6, 5))
gs = fig.add_gridspec(2, 1, height_ratios=(3, 1), hspace=0.35)
ax_top = fig.add_subplot(gs[0])      # 3 parts tall
ax_bottom = fig.add_subplot(gs[1])   # 1 part tall
```

`hspace`/`wspace` control the gaps between panels. Because the ratios
are relative, the same code adapts to any total figure height — this is
what makes figures with a "hero panel + detail strip" stable across
report sizes.

## 4. subplot_mosaic: Named Panels

`subplot_mosaic` replaces positional bookkeeping with a **layout
string** that reads like ASCII art, and returns a dict of `Axes` keyed
by the labels:

```python
fig, axd = plt.subplot_mosaic(
    [["loss", "loss"],
     ["grad", "hist"]],
    figsize=(8, 5),
    width_ratios=(2, 1),
)
axd["loss"].plot(epochs, 1.0 / np.sqrt(epochs))   # spans both columns
axd["grad"].plot(epochs, np.sin(epochs / 3.0))
axd["hist"].hist(rng.normal(size=500), bins=20)
```

Repeating a label (`"loss"` twice) makes that panel span columns.
Fetching panels by name (`axd["loss"]`) removes the `(row, col)`
arithmetic that breaks whenever the layout changes — and it makes the
layout self-documenting: `[["loss", "loss"], ["grad", "hist"]]` is the
picture.

## 5. Shared Axes: One Scale, Many Panels

`sharex=True`/`sharey=True` (passed to `plt.subplots` or
`subplot_mosaic`) makes panels share the same tick range, so comparing
two signals is honest — a spike in one panel cannot be visually
exaggerated by a different scale in the other.

```python
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
ax1.plot(x, np.cos(x))
ax2.plot(x, np.sin(x))
ax1.set_xlim(2, 8)        # propagates to ax2: shared axes are JOINED
```

Key subtlety: shared axes are *joined*, not merely *synchronized at
creation*. Setting limits on one propagates to the other, and
`ax1.get_shared_x_axes().joined(ax1, ax2)` returns `True`. Use this to
guarantee alignment; be aware that zooming one panel zooms its partner.

---

## ⚠️ Common Mistakes to Avoid

1. **Mixing interfaces** — `plt.plot(x, y)` (implicit) next to
   `ax.set_title(...)` (explicit) means the line lands on whatever
   "current" axes exists, possibly a different panel. Pick one
   interface: the explicit one.
2. **Leaking figures in a loop** — `for i in range(100): fig, ax =
   plt.subplots()` without `plt.close(fig)` keeps 100 canvases alive
   until the process ends. Close every figure you are done with.
3. **Index-arithmetic layouts** — hard-coding `fig.add_subplot(gs[2, 1])`
   breaks the moment the grid changes; use `subplot_mosaic` labels or
   `GridSpec` slices instead.
4. **Forgetting `tight_layout()`** — overlapping titles/labels are the
   #1 "why does my report look broken" complaint; call it after
   styling, before `savefig`.

## ✅ Best Practices

- Always write `fig, ax = plt.subplots()` and pass `ax` around — never
  rely on `plt.gca()`.
- Close figures: `plt.close(fig)` immediately after `savefig`, inside
  `finally` if exceptions are possible.
- Use `subplot_mosaic` for anything with more than two panels; the
  layout string is documentation.
- Use `sharex`/`sharey` whenever panels compare the same variable
  across conditions.
- Save with an explicit `dpi` and verify the artifact exists with a
  size assertion in CI.

## 📊 Complexity and Cost

| Operation | Cost |
|-----------|------|
| Create `Figure` | O(1) memory; each `Axes` holds its artists |
| Draw 100-point line | O(n) per artist, negligible |
| `subplot_mosaic` layout | O(panels) — cheap; layout string parsed once |
| `GridSpec` | O(1) — pure bookkeeping, no extra draw cost |
| `tight_layout()` | O(artists) — the only step that scans all artists |
| **Leaked figures** | O(1) per figure but memory grows until `close()` — unbounded in loops |

Plot rendering cost scales with points/artists, not with the API you
use. The expensive part of the OO API is *development-time*: it forces
explicit decisions that the state machine hides.

## 🤖 AI Engineering Relevance

- **Deterministic reports**: every eval report, model card, or
  dashboard figure is drawn against explicit objects with a fixed seed,
  so the same script renders identically in a notebook and in CI.
- **Unit-testable figures**: `_verify()` can assert `len(ax.lines)`,
  `isinstance(fig, plt.Figure)`, or that a mosaic produced the exact
  keys `{"loss", "grad", "hist"}` — impossible with implicit state.
- **Multi-panel dashboards**: `subplot_mosaic` + shared axes is the
  standard layout for training dashboards (loss / grad norm / weight
  histograms in one grid) and for eval reports (ROC + PR + calibration
  side by side).
- **Headless generation**: figures generated in background jobs use
  exactly this API with `matplotlib.use("Agg")`; no window server is
  touched, so containerized pipelines never hang on a display.

## 🏋️ Practice Exercises

1. Build a 2×2 mosaic labeled `["loss", "loss"], ["acc", "lr"]` and
   verify `set(axd) == {"loss", "acc", "lr"}`.
2. Recreate the signal/step layout with `GridSpec(height_ratios=(3,
   1))` and add `sharex=True`; assert
   `ax_top.get_shared_x_axes().joined(ax_top, ax_bottom)`.
3. Write a loop that creates and *closes* 10 figures; then verify with
   `len(plt.get_fignums()) == 0`.
4. Demonstrate the state machine hazard: create two figures, plot into
   one via `plt.plot`, and show `plt.gca()` does not point at the axes
   you intended after `plt.sca` juggling.

## 📌 Summary

- `Figure` = canvas, `Axes` = plot region; hold both explicitly and
  style through the `Axes`.
- The `plt.*` state machine targets an implicit "current axes" — a
  correctness hazard in scripts, threads, and CI.
- `GridSpec` gives relative row/column sizes; `subplot_mosaic` names
  panels so layouts read like ASCII art; `sharex`/`sharey` join axes so
  scales stay aligned.
- Close every figure you create; run `tight_layout()` before saving.

## 📖 Quick Reference

| Task | Code |
|------|------|
| One figure, one axes | `fig, ax = plt.subplots(figsize=(6, 4))` |
| Unequal grid | `gs = fig.add_gridspec(2, 1, height_ratios=(3, 1))` |
| Named layout | `fig, axd = plt.subplot_mosaic([["a"], ["b"]])` |
| Address panel | `axd["a"].plot(...)` |
| Share x across panels | `plt.subplots(2, 1, sharex=True)` |
| Are axes joined? | `ax1.get_shared_x_axes().joined(ax1, ax2)` |
| Release canvas | `plt.close(fig)` |
| Avoid overlapping | `fig.tight_layout()` |

## ➡️ Next Steps

- Lecture 22 (Styling and Themes): make these explicit figures render
  identically everywhere via `rcParams` and stylesheets.
- Lecture 23 (ML Visualization): combine `subplot_mosaic` + shared axes
  into the six standard model-report plots.
- Reference:
  https://matplotlib.org/stable/tutorials/intermediate/artists.html
