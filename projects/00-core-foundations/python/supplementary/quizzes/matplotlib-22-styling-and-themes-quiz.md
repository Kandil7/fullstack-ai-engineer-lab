# Matplotlib 22 — Styling and Themes Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 120
print(plt.rcParams["figure.dpi"])
```

- A) `120.0`
- B) `120`
- C) `None`
- D) `'120'`

**E2.** `plt.style.use("ggplot")`:

- A) swaps a whole family of rcParams for a named theme
- B) draws a grid on the current axes
- C) installs a new colormap
- D) requires internet access

**E3 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
print("ggplot" in plt.style.available)
print("dark_background" in plt.style.available)
```

- A) `True` `True`
- B) `True` `False`
- C) `False` `False`
- D) raises `KeyError`

**E4.** Which colormap is **not** perceptually uniform?

- A) `jet`
- B) `viridis`
- C) `plasma`
- D) `cividis`

**E5 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
cmap = plt.get_cmap("viridis")
print(cmap.name)
```

- A) `viridis`
- B) `V` (the first letter)
- C) `viridis_r`
- D) raises `ValueError`

**E6.** `ax.annotate("min", xy=(1, 2), xytext=(5, 5))`:

- A) draws text at (5, 5) with an arrow to (1, 2)
- B) draws text at (1, 2) with an arrow to (5, 5)
- C) moves the data point to (1, 2)
- D) requires a colorbar

---

## Medium

**M1 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["axes.grid"] = True
print(plt.rcParams["axes.grid"])
```

- A) `True`
- B) `False`
- C) `None`
- D) `'True'`

**M2.** Why must rcParams be set *before* creating figures?

- A) defaults are read at figure creation; later changes don't apply
  to existing figures
- B) setting them later raises a TypeError
- C) matplotlib only reads rcParams at import time
- D) rcParams only apply to notebooks

**M3.** The difference between `plt.style.use(...)` and
`plt.style.context(...)`:

- A) `context` restores the previous params on block exit; `use` is
  permanent
- B) `use` is scoped; `context` is permanent
- C) they are identical
- D) `context` requires a contextlib decorator

**M4 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
y = (x - 4.0) ** 2
ax.plot(x, y)
ax.annotate("min", xy=(x[int(np.argmin(y))], y.min()),
            xytext=(8, 30), arrowprops={"arrowstyle": "->"})
print(len(ax.texts))
plt.close(fig)
```

- A) `1`
- B) `0`
- C) `2`
- D) `100`

**M5.** Which is the correct way to scope a dark theme to one figure?

- A) `with plt.style.context("dark_background"): fig, ax = plt.subplots()`
- B) `plt.style.use("dark_background")` at module top
- C) `fig.style = "dark_background"`
- D) `plt.rcParams["style"] = "dark_background"`

**M6.** Continuous data (loss heatmaps, attention maps) should use:

- A) `viridis` / `plasma` / `inferno` / `magma` / `cividis`
- B) `jet` for contrast
- C) `tab:blue` everywhere
- D) any qualitative palette

**M7 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
cmaps = {"viridis", "plasma", "inferno", "magma", "cividis"}
print("jet" in cmaps)
print("viridis" in cmaps)
```

- A) `False` `True`
- B) `True` `True`
- C) `False` `False`
- D) `True` `False`

**M8.** `arrowprops={"arrowstyle": "->", "color": "tab:red"}`:

- A) styles the annotation arrow (head + color)
- B) changes the line color of the plotted data
- C) is ignored by matplotlib
- D) requires `transparency=True`

**M9.** A model report figure saved at `dpi=150` with rcParams
`savefig.dpi` set to 150 is:

- A) deterministic across machines when seeds/figsize are fixed
- B) guaranteed identical bytes across matplotlib versions
- C) only renderable on a GPU
- D) always blurry

---

## Hard

**H1.** Why is `jet` considered dishonest for continuous data?

- A) it is not perceptually uniform (banding invents contours) and
  not colorblind-safe
- B) it is too dark
- C) it only works for 2D data
- D) it is deprecated and removed from matplotlib

**H2 (code-output).** What prints?
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
with plt.style.context("ggplot"):
    a = plt.rcParams["axes.grid"]
with plt.style.context("dark_background"):
    b = plt.rcParams["figure.facecolor"]
plt.style.use("default")
print(a)
print(type(b).__name__)
```

- A) `True` `str`
- B) `False` `str`
- C) `True` `float`
- D) `None` `str`

**H3.** The production pattern for reproducible report styling is:

- A) one `set_publication_rcparams()` called before any figure +
  explicit ax + fixed seeds
- B) ad-hoc `plt.rcParams` mutations inside each plotting function
- C) a different stylesheet per figure, chosen at random
- D) saving rcParams to a PNG

**H4.** `assert len(ax.texts) == 1` after an `annotate` call verifies:

- A) exactly one annotation was added (annotations are artists)
- B) the arrow pointed at the right pixel
- C) the figure has one title
- D) the text is visible

**H5.** Which statement about scoped styles is true?

- A) `plt.style.context` restores the previous params even if the
  block raises
- B) `plt.style.use` inside a context leaks out after the block
- C) context managers cannot nest
- D) styles only affect the next figure ever created

---

## Answer Key

**E1 — A.** rcParams assignments take effect immediately; dpi reads
back as a float, so it prints `120.0` (verified). These are
process-wide defaults read at figure creation.
*Distractors:* B is the int spelling — Python prints the float;
C/D are the wrong types.

**E2 — A.** A stylesheet is a named family of rcParams applied as a
whole.
*Distractors:* B is `axes.grid`; C is a cmap; D is false.

**E3 — A.** Both `ggplot` and `dark_background` are registered styles.
*Distractors:* B/C deny real styles; D is false (`in` never raises).

**E4 — A.** `jet` is the classic non-uniform, non-colorblind-safe
map.
*Distractors:* B/C/D are the canonical PU set.

**E5 — A.** `get_cmap("viridis")` returns the named colormap object;
`.name` is `viridis`.
*Distractors:* B is a letter; C is the reversed variant; D is false.

**E6 — A.** Text lands at `xytext`; the arrow points at `xy`.
*Distractors:* B swaps the points; C is false; D is false.

**M1 — A.** The assignment takes effect immediately in the params
dict.
*Distractors:* B is the old value; C/D are wrong types.

**M2 — A.** Defaults bind at figure creation — the timing rule.
*Distractors:* B/C/D are false.

**M3 — A.** `context` is the scoped variant; `use` is permanent.
*Distractors:* B reverses; C is false; D is false.

**M4 — A.** One `annotate` → one text artist; `ax.texts` counts it.
*Distractors:* B is pre-annotation; C double-counts; D is the number
of data points.

**M5 — A.** The context manager scopes the theme to the block.
*Distractors:* B leaks globally; C/D are invalid.

**M6 — A.** Continuous data → perceptually uniform maps.
*Distractors:* B is the anti-pattern; C is for categories; D is wrong
kind of palette.

**M7 — A.** The PU set contains viridis but not jet.
*Distractors:* B/C/D flip membership.

**M8 — A.** `arrowprops` styles the arrow (style, color, etc.).
*Distractors:* B/C are false; D is unrelated.

**M9 — A.** Fixed seeds + figsize + dpi + rcParams = deterministic
rendering.
*Distractors:* B overclaims (versions can change glyphs); C/D false.

**H1 — A.** Banding invents structure and red-green regions fail
colorblind readers — both "honesty" violations.
*Distractors:* B/C are false; D is false (jet still exists).

**H2 — A.** `ggplot` sets `axes.grid` True; `figure.facecolor` is a
color string under dark_background.
*Distractors:* B/C/D misreport values/types.

**H3 — A.** Configure once at startup, then explicit ax + seeds —
reproducibility by construction.
*Distractors:* B is scattered state; C is chaos; D is nonsense.

**H4 — A.** Annotations are artists on the axes; counting them verifies
the callout was added.
*Distractors:* B needs pixel inspection; C/D are unrelated.

**H5 — A.** `context` is exception-safe: params are restored on any
exit path.
*Distractors:* B is false (`use` inside would leak, but that's misuse);
C is false; D is false.

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 22](03-libraries/matplotlib/lectures/22-styling-and-themes-lecture.md) ·
[Glossary 22](03-libraries/matplotlib/lectures/22-styling-and-themes-glossary.md) ·
[Challenge 22](03-libraries/matplotlib/challenges/22-styling-and-themes/README.md)
