# Matplotlib 21 — The Object-Oriented API Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1.** `fig, ax = plt.subplots()` returns:

- A) a `Figure` and an `Axes`
- B) two `Figure` objects
- C) a `Canvas` and a `Plot`
- D) an `Axes` and a `GridSpec`

**E2.** Which object holds the coordinate system, ticks, and artists?

- A) the `Axes`
- B) the `Figure`
- C) the backend
- D) `plt.gca()` only

**E3 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
plt.sca(ax2)
print(plt.gca() is ax2)
plt.close("all")
```

- A) `True`
- B) `False`
- C) `None`
- D) raises `ValueError`

**E4 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.close(fig)
print(len(plt.get_fignums()))
```

- A) `0`
- B) `1`
- C) `2`
- D) `None`

**E5.** The `plt.plot(x, y)` state machine writes into:

- A) the "current axes" — a process-global implicit target
- B) the last figure created, always
- C) a new figure each time
- D) the first axes ever created

**E6 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
print(a1.get_shared_x_axes().joined(a1, a2))
print(len(fig.axes))
plt.close(fig)
```

- A) `True` `2`
- B) `False` `2`
- C) `True` `1`
- D) `True` `0`

---

## Medium

**M1.** `plt.subplot_mosaic([["loss", "loss"], ["grad", "hist"]])`
returns:

- A) a dict of label → Axes: `{"loss", "grad", "hist"}`
- B) a list of Axes in row-major order
- C) a tuple `(fig, ax)`
- D) a `GridSpec`

**M2 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axd = plt.subplot_mosaic([["a", "b"], ["a", "c"]])
print(set(axd))
print(len(fig.axes))
plt.close(fig)
```

- A) `{'a', 'b', 'c'}` `3`
- B) `{'a', 'b', 'c'}` `4`
- C) `{'a', 'b'}` `2`
- D) `{'a', 'b', 'c', 'a'}` `4`

**M3.** `fig.add_gridspec(2, 1, height_ratios=(3, 1))` creates:

- A) two rows where the top row is 3× the height of the bottom
- B) three rows where the first is 2× the second
- C) two columns with width ratio 3:1
- D) two rows of exactly equal height

**M4 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
a1.set_xlim(2, 8)
print(a2.get_xlim())
plt.close(fig)
```

- A) `(2.0, 8.0)`
- B) `(0.0, 1.0)`
- C) `(2, 8)`
- D) `(-0.05, 1.05)`

**M5.** What is the risk of calling `plt.plot()` inside a function
that also uses `ax.set_title()`?

- A) the line may land on a different axes than the title (hidden
  current-axes state)
- B) the function raises a TypeError
- C) the figure is automatically closed
- D) rcParams are reset

**M6.** After `fig, axd = plt.subplot_mosaic([["top"], ["bot"]])`,
how do you plot into the bottom panel?

- A) `axd["bot"].plot(...)`
- B) `axd[1].plot(...)`
- C) `fig.axes[1].plot(...)` only
- D) `plt.plot(...)` then `plt.sca("bot")`

**M7 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([0, 1], [0, 1])
print(len(ax.lines))
plt.close(fig)
```

- A) `1`
- B) `2`
- C) `0`
- D) `6`

**M8.** Which is the correct "close every figure" loop?

- A) `for i in range(10): fig, ax = plt.subplots(); ...; plt.close(fig)`
- B) `for i in range(10): fig, ax = plt.subplots(); ...` (no close)
- C) `for i in range(10): plt.close("all"); fig, ax = plt.subplots()`
- D) `plt.close()` before the loop only

**M9.** `GridSpec` is best used when:

- A) panels need unequal relative sizes
- B) you need a single figure with one axes
- C) you want named labels
- D) you are rendering in a notebook

---

## Hard

**H1.** Why does `subplot_mosaic` beat positional indexing for
multi-panel layouts?

- A) labels make the layout self-documenting and immune to (row, col)
  arithmetic drift
- B) it renders faster
- C) it supports 3D projections only
- D) it returns a Figure instead of Axes

**H2 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig = plt.figure()
gs = fig.add_gridspec(2, 1, height_ratios=(3, 1))
a = fig.add_subplot(gs[0])
b = fig.add_subplot(gs[1])
print(a is not b)
print(len(fig.axes))
plt.close(fig)
```

- A) `True` `2`
- B) `False` `2`
- C) `True` `1`
- D) `True` `0`

**H3.** "Shared axes are joined, not just synchronized" means:

- A) limit changes propagate both ways at runtime
- B) the join is fixed at construction and never changes
- C) only tick labels are shared, limits are not
- D) shared axes must have identical data

**H4.** Which is the correct production rule for figures in loops?

- A) create → draw → save → `plt.close(fig)` (often in `finally`)
- B) create → draw → save (GC handles the rest)
- C) reuse one global figure for everything
- D) call `plt.clf()` before creating each figure

**H5.** `len(fig.axes)` counts:

- A) the axes currently attached to the figure
- B) the axes ever attached, including closed ones
- C) the number of lines drawn
- D) the number of figures in the process

---

## Answer Key

**E1 — A.** `subplots()` returns (Figure, Axes) — the canonical pair.
*Distractors:* B/C/D invent other pairs.

**E2 — A.** The Axes owns coordinate system, ticks, spines, artists.
*Distractors:* B is the canvas; C is the renderer; D is a state-machine
query.

**E3 — A.** `plt.sca(ax2)` sets the current axes; `gca()` returns it.
*Distractors:* B ignores sca; C/D are wrong types.

**E4 — A.** After `plt.close(fig)`, `plt.get_fignums()` is empty —
closing releases the canvas (the anti-leak discipline).
*Distractors:* B/C count unclosed figures; D is the wrong type.

**E5 — A.** `plt.*` routes to the implicit "current axes".
*Distractors:* B/C/D describe other rules that don't exist.

**E6 — A.** `sharex=True` joins the axes (`joined` → True); `fig.axes`
holds 2 panels.
*Distractors:* B ignores the join; C/D mis-count panels.

**M1 — A.** Mosaic returns a dict keyed by labels; the repeated
"loss" spans the row.
*Distractors:* B is the wrong structure; C is subplots; D is a layout
object, not axes.

**M2 — A.** Labels are a set of 3; the mosaic has 3 panels (a spans
the left column).
*Distractors:* B counts the label repetition as panels; C drops one;
D is a list of labels, not a set.

**M3 — A.** `height_ratios=(3, 1)` → top row 3× the bottom's height.
*Distractors:* B/C misread the parameters; D ignores ratios.

**M4 — A.** Shared axes are joined: setting `a1` limits propagates to
`a2` → (2.0, 8.0).
*Distractors:* B/D are the default limits; C is the int input (limits
are stored as floats).

**M5 — A.** The implicit call targets the current axes — possibly a
different panel than the explicit `ax`.
*Distractors:* B/C/D are false.

**M6 — A.** Panels are addressed by label: `axd["bot"]`.
*Distractors:* B is positional (not the API); C works but bypasses
labels; D is a state-machine hybrid.

**M7 — A.** One `ax.plot` call → one line artist.
*Distractors:* B counts something else; C is pre-draw; D is figsize.

**M8 — A.** Create-draw-close per iteration is the leak-free loop.
*Distractors:* B leaks; C closes before creation (wasteful, still
works); D closes once.

**M9 — A.** GridSpec exists for unequal relative sizes.
*Distractors:* B is overkill; C is mosaic; D is irrelevant.

**H1 — A.** Labels document the layout and survive layout edits
without index re-arithmetic.
*Distractors:* B/C/D are false.

**H2 — A.** `gs[0]` and `gs[1]` create two distinct axes on the same
figure.
*Distractors:* B claims they're the same; C/D miscount.

**H3 — A.** The join propagates runtime changes (e.g., `set_xlim`)
between panels.
*Distractors:* B is false (behavior is live); C/D are false.

**H4 — A.** The create→draw→save→close discipline (with `finally`
when needed) is the production rule.
*Distractors:* B relies on GC (unreliable timing); C/D are false.

**H5 — A.** `fig.axes` lists the axes currently attached.
*Distractors:* B confuses history; C is artists; D is `get_fignums`.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 21](03-libraries/matplotlib/lectures/21-object-oriented-api-lecture.md) ·
[Glossary 21](03-libraries/matplotlib/lectures/21-object-oriented-api-glossary.md) ·
[Challenge 21](03-libraries/matplotlib/challenges/21-object-oriented-api/README.md)
