# SciPy Lecture 04: Statistics — Glossary

| Term | Definition | Example |
|------|-----------|---------|
| Distribution | Mathematical description of probabilities | `stats.norm(loc=0, scale=1)` |
| PDF | Probability Density Function | `norm.pdf(0)` |
| CDF | Cumulative Distribution Function | `norm.cdf(1.96)` |
| PPF | Percent Point Function (inverse CDF) | `norm.ppf(0.975)` |
| SF | Survival Function (1 - CDF) | `norm.sf(1.96)` |
| t-test | Compares group means | `stats.ttest_ind(a, b)` |
| ANOVA | Compares multiple group means | `stats.f_oneway(a, b, c)` |
| Chi-squared | Tests categorical independence | `stats.chi2_contingency(table)` |
| Pearson r | Linear correlation coefficient | `stats.pearsonr(x, y)` |
| Spearman ρ | Rank correlation coefficient | `stats.spearmanr(x, y)` |
| p-value | Probability of extreme result under null | Compare to α=0.05 |

### Common Distributions

| Distribution | Parameters | Use Case |
|-------------|-----------|----------|
| `norm` | loc, scale | Natural phenomena |
| `t` | df | Small sample inference |
| `chi2` | df | Goodness of fit |
| `f` | dfn, dfd | ANOVA |
| `binom` | n, p | Binary outcomes |
| `poisson` | mu | Count data |
