# Quiz 09: Data Ethics

## Topic Overview

This quiz covers fast.ai's data-ethics bonus lesson (Rachel Thomas): engineer
responsibility, feedback loops and Goodhart's Law, the bias taxonomy
(historical, representation, measurement, aggregation, evaluation),
disaggregated evaluation, recourse and accountability, automation bias and the
human in the loop, privacy/consent/provenance, and practical tooling (model
cards, datasheets, the ethics checklist, and the consequentialist/rights/justice
lenses).

---

## Questions

### Question 1
**In the fast.ai framing, who is responsible for the harm a deployed ML system causes?**

- A) Only the executives who approved the budget
- B) Only the legal and policy teams
- C) Responsibility is shared, and the engineers who built it are part of that share
- D) No one, if the team followed the written specification

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** fast.ai insists responsibility is shared across a system, and
that engineers cannot offload their part of it. "I was just following the spec"
is explicitly rejected as a defense — building the system involves real choices
(data, objective, edge cases) with real consequences.
</details>

---

### Question 2
**What does Goodhart's Law state?**

- A) Any metric will eventually be measured incorrectly
- B) When a measure becomes a target, it ceases to be a good measure
- C) More data always improves a model
- D) Aggregate accuracy is the most reliable metric

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Once you optimize a proxy directly (e.g., engagement/watch-time),
the system games it and it stops tracking the value you cared about. The fix is
to pair any target with guardrail metrics and never optimize a single number in
isolation.
</details>

---

### Question 3
**Predictive policing trained on historical arrest data is a classic example of what?**

- A) A perfectly unbiased objective ground truth
- B) A runaway feedback loop that concentrates policing where police already were
- C) Aggregation bias only
- D) A privacy violation only

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Arrests reflect past *police activity*, not crime. Sending more
patrol to already-policed areas produces more arrests there, which becomes new
training data, amplifying the initial imbalance. The model measures its own past
actions and runs away.
</details>

---

### Question 4
**A hiring model trained on who a company hired in the past reproduces prior discrimination even with perfect sampling. This is:**

- A) Representation bias
- B) Measurement bias
- C) Historical bias
- D) Evaluation bias

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Historical bias is present when the data faithfully encodes an
already-unequal world. It cannot be fixed by collecting more of the same data;
it requires deciding what outcomes *should* be, not just replicating what they
*were*.
</details>

---

### Question 5
**A health algorithm used past healthcare spending as a stand-in for health need, under-referring some groups. The core problem is best described as:**

- A) A runaway feedback loop
- B) Measurement bias via a proxy variable
- C) Automation bias
- D) Lack of informed consent

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Cost is a proxy for need. Because less was historically spent on
some patients at equal illness, cost systematically under-measured their need —
measurement bias through a proxy. Notably, no protected attribute was in the
model, yet the outcome was disparate.
</details>

---

### Question 6
**Why does fast.ai insist you report disaggregated metrics rather than a single aggregate score?**

- A) Aggregate metrics are always mathematically wrong
- B) A high aggregate can hide large error disparities across subgroups
- C) Regulators forbid aggregate metrics
- D) Disaggregated metrics are faster to compute

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A model that is 95% accurate overall might be 99% for the
majority group and 70% for a minority group. The aggregate is designed *not* to
show this; only per-group error rates (FPR/FNR, precision/recall) reveal it.
</details>

---

### Question 7
**When deciding whether a false-positive or false-negative disparity matters more, the deciding factor is:**

- A) Whichever number is larger
- B) What a false positive versus a false negative actually costs a person
- C) The overall accuracy
- D) The size of the training set

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The cost is context-dependent. A false positive on a fraud model
freezes an innocent person's account; a false negative on a disease screen
misses a sick patient. You must reason about human cost, and different fairness
definitions can conflict, forcing an explicit, justified choice.
</details>

---

### Question 8
**What is "recourse" in the context of algorithmic decisions?**

- A) A backup model used when the primary fails
- B) A real mechanism for an affected person to understand, contest, and correct a decision
- C) The legal right to sue the vendor
- D) A rollback of the model to a previous version

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Recourse means affected people can see the reasons, dispute the
outcome, and get errors fixed through a working appeals path — which requires
logging inputs, decisions, and reasons *before* launch. It pairs with
accountability, where a named party owns the outcome rather than blaming "the
algorithm."
</details>

---

### Question 9
**Why can adding a "human in the loop" fail to be a real safeguard?**

- A) Humans are always slower than models
- B) Automation bias leads reviewers to over-trust and rubber-stamp model output
- C) Humans cannot read model outputs
- D) It always violates privacy law

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Automation bias is the tendency to over-trust automated output.
A reviewer approving hundreds of decisions per hour with no context — and
penalized for overriding — launders errors rather than catching them. Effective
human-in-the-loop design gives time, context, model uncertainty, and a
penalty-free override.
</details>

---

### Question 10
**Which practical tools and lenses does the lesson recommend for institutionalizing ethics?**

- A) Model cards, datasheets for datasets, a pre-deployment checklist, and the consequentialist/rights/justice lenses
- B) Only a legal disclaimer in the terms of service
- C) A single aggregate accuracy report signed by a manager
- D) Encrypting the model weights

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** fast.ai points to datasheets for datasets (Gebru et al.), model
cards (Mitchell et al.), and ethical-risk checklists run before deployment, plus
the Markkula Center's "ethics as a practice" framing examined through
consequentialist (outcomes), rights (whose rights are at stake), and justice
(fair distribution of benefits and harms) lenses.
</details>

---

### Question 11
**What does Rachel Thomas mean by "dark flow" in the context of AI-assisted coding?**

- A) A state of deep concentration and peak productive flow
- B) A superficial, addictive state of high-frequency, low-reward AI iterations that *feels* productive
- C) Working late at night without sufficient lighting
- D) A debugging technique for neural networks

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** "Dark flow" (from "Breaking the Spell of Vibe Coding," Jan 2026) adapts Csikszentmihalyi's concept: unlike true flow (growth-producing), vibe coding induces a slot-machine-like addiction where each AI-generated block triggers a dopamine hit regardless of quality. METR research shows developers in this state often *feel* more productive while actually producing harder-to-maintain code.
</details>

---

### Question 12
**What is "vibe coding" as critiqued in the Data Ethics supplement?**

- A) Writing code while listening to music
- B) Generating large blocks from vague prompts with minimal review, accumulating understanding debt
- C) A collaborative coding technique used by fast.ai
- D) An approved methodology for production code

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Vibe coding means giving the AI high-level prompts, accepting output without reading it carefully, and moving on quickly. It induces dark flow, accrues understanding debt, and — per the Build to Last interview with Chris Lattner — creates architectural debt as well.
</details>

---

### Question 13
**According to Rachel Thomas's "Close Reading with AI" essay, what is the recommended way to use LLMs for reading?**

- A) Ask the LLM to summarize the text so you do not have to read it
- B) Use the LLM as a dialogue partner to interrogate, test interpretations, and explore counterexamples
- C) Only read texts the LLM recommends
- D) Use the LLM to generate new texts instead of reading old ones

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Close reading with AI means active engagement: asking "why?", testing hypotheses, exploring alternative readings, and creating flashcards for retention. The goal is to *deepen* understanding, not outsource it. Thomas's workflow is: prepare context → generate grounding summary → iterate in dialogue → create flashcards.
</details>

---

### Question 14
**What is "architectural debt," as discussed in the "Build to Last" interview?**

- A) A loan taken to pay for cloud architecture
- B) The hidden fragility caused by merging AI-generated code without understanding integration points
- C) The cost of refactoring legacy systems
- D) A type of database indexing strategy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Jeremy Howard and Chris Lattner (Oct 2025) warn that each AI-generated function might work in isolation, but when developers do not understand how pieces fit together architecturally, the system becomes fragile. Unlike regular technical debt, architectural debt is invisible to unit tests.
</details>

---

### Question 15
**What is the recommended antidote to understanding debt?**

- A) Using more powerful AI models
- B) Generating more code faster to overwhelm the debt
- C) Taking "side quests" — pausing to learn unfamiliar concepts before accepting AI output
- D) Ignoring it, as it resolves itself over time

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Every time the AI suggests something unfamiliar, going on a "side quest" to understand it (asking the AI to explain, writing a small test, creating a flashcard) builds durable knowledge instead of accruing understanding debt. This is a core practice of Dialog Engineering.
</details>

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | C | 9 | B |
| 2 | B | 10 | A |
| 3 | B | 11 | B |
| 4 | C | 12 | B |
| 5 | B | 13 | B |
| 6 | B | 14 | B |
| 7 | B | 15 | C |
| 8 | B |  |  |

---

*Generated for fast.ai Deep Learning — Quiz 09 (Data Ethics bonus, updated with 2025–2026 supplement).*
