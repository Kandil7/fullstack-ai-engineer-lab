# Matplotlib Lecture 10: Bar Charts

## 🎯 Topic Overview

Bar charts compare discrete categories or track changes over time. Matplotlib supports vertical bars, horizontal bars, stacked bars, grouped bars, and error bars.

## 📚 Learning Objectives

1. Create vertical and horizontal bar charts
2. Build grouped and stacked bar charts
3. Add error bars and custom bar widths/colors
4. Combine bars with other plot types

---

## 1. Basic Bar Chart

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['Apples', 'Bananas', 'Cherries', 'Dates', 'Elderberries']
values = [25, 40, 15, 30, 20]

plt.figure(figsize=(10, 6))
plt.bar(categories, values, color='steelblue', edgecolor='black', alpha=0.8)
plt.title('Fruit Sales')
plt.xlabel('Fruit')
plt.ylabel('Units Sold')
plt.grid(axis='y', alpha=0.3)
plt.show()
```

---

## 2. Horizontal and Grouped Bars

```python
# Horizontal bars
plt.barh(categories, values, color='coral', edgecolor='black')

# Grouped bars
x = np.arange(len(categories))
width = 0.35

plt.bar(x - width/2, values_2023, width, label='2023', color='steelblue')
plt.bar(x + width/2, values_2024, width, label='2024', color='coral')
plt.xticks(x, categories)
plt.legend()
```

---

## 3. Stacked Bars

```python
plt.bar(categories, values_A, label='Product A', color='steelblue')
plt.bar(categories, values_B, bottom=values_A, label='Product B', color='coral')
plt.bar(categories, values_C, bottom=np.array(values_A) + np.array(values_B),
        label='Product C', color='green')
plt.legend()
```

---

## 4. Error Bars

```python
means = [25, 40, 15]
errors = [3, 5, 2]
plt.bar(categories[:3], means, yerr=errors, capsize=5,
        color='steelblue', edgecolor='black', error_kw={'linewidth': 2})
```

---

## Practice Exercises

1. Create a grouped bar chart comparing two datasets across 5 categories
2. Build a stacked bar chart showing quarterly sales by product line
3. Add error bars to a bar chart representing experimental measurements
