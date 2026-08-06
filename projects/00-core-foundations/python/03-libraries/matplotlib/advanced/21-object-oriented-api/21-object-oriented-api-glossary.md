# Matplotlib Lecture 21: The Object-Oriented API — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| `Figure` | The whole canvas: size, background, DPI | `fig = plt.figure(figsize=(6, 4))` |
| `Axes` | One plot region with its own coordinate system | `fig, ax = plt.subplots()` |
| State machine | Implicit "current axes" global behind `plt.*` | `plt.plot(...)` targets `plt.gca()` |
| `plt.gca()` | Get the current axes (global state) | `plt.gca() is ax2` |
| `plt.sca(ax)` | Set the current axes (global state) | `plt.sca(ax1)` |
| `GridSpec` | Unequal grid layout with relative sizes | `fig.add_gridspec(2, 1, height_ratios=(3, 1))` |
| `subplot_mosaic` | Named-panel layout from an ASCII-art string | `plt.subplot_mosaic([["loss", "loss"], ["grad", "hist"]])` |
| Shared axes | Panels joined via `sharex`/`sharey` | `plt.subplots(2, 1, sharex=True)` |
| `plt.close(fig)` | Release a figure's canvas (memory) | `plt.close(fig)` after `savefig` |
| `tight_layout()` | Auto-space panels to avoid overlap | `fig.tight_layout()` |

## Detailed Definitions

**Figure** — The top-level container: the canvas holding all panels,
with size (inches), background, and DPI. Created explicitly with
`plt.subplots()` / `plt.figure()`; owns the savefig call.

**Axes** — One plot region inside a Figure: has its own coordinate
system, ticks, spines, and artists. All styling methods
(`set_title`, `set_xlabel`, `legend`, `grid`, `set_xlim`) live on the
Axes. A Figure can hold one or many Axes.

**State machine** — The implicit interface (`plt.plot`, `plt.title`,
…) that routes calls to whatever Axes is "current" via a
process-global pointer. Convenient in notebooks; a correctness hazard
in scripts, threads, and CI because hidden state can retarget plots.

**`plt.gca()` / `plt.sca(ax)`** — Getters/setters for the implicit
current axes. Their existence is the evidence that `plt.*` carries
global state; an explicit `ax` variable never moves on its own.

**GridSpec** — A layout object created from a figure
(`fig.add_gridspec(rows, cols, height_ratios=..., width_ratios=...)`)
whose cells are passed to `fig.add_subplot(gs[...])`. Enables unequal
row/column sizes.

**`subplot_mosaic`** — `fig, axd = plt.subplot_mosaic(layout)` where
`layout` is a list of lists (or a string) whose repeated labels create
spans. Returns `axd`, a dict of label → Axes.

**Shared axes** — `sharex=True`/`sharey=True` *joins* the axes'
coordinate systems: tick ranges align and limit changes propagate.
Checkable via `ax1.get_shared_x_axes().joined(ax1, ax2)`.

## Key Concepts Summary

- The OO API is explicit: you hold `fig` and `ax`; the state machine
  hides them behind a global pointer.
- `GridSpec` = relative sizes; `subplot_mosaic` = named panels; shared
  axes = honest comparison scales.
- Leaked figures (no `plt.close`) grow memory until the process ends.

## Practice Terms

1. Name the two objects every OO-API plot must hold explicitly.
2. What does `plt.gca()` return, and why is relying on it dangerous in
   scripts?
3. Which call creates a grid where the top panel is 3x the height of
   the bottom?
4. How do you address the top-right panel in
   `plt.subplot_mosaic([["loss", "loss"], ["grad", "hist"]])`?
5. What does `sharex=True` actually do — sync once or join forever?

*(Answers: 1. `Figure` and `Axes`. 2. The current axes from global
state — hidden state can retarget plots. 3.
`fig.add_gridspec(2, 1, height_ratios=(3, 1))`. 4. `axd["grad"]` — the
mosaic returns a label-keyed dict. 5. Join forever — limit changes
propagate.)*
