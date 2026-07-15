# Matplotlib Lecture 12: Pie Charts

## 🎯 Topic Overview

Pie charts show proportional relationships — parts of a whole. While often overused, they excel at showing simple composition when categories are few and proportions are distinct.

## 📚 Learning Objectives

1. Create basic and exploded pie charts
2. Customize colors, labels, percentages, and shadows
3. Use donut charts as a modern alternative
4. Know when NOT to use pie charts

---

## 1. Basic Pie Chart

```python
import matplotlib.pyplot as plt

sizes = [30, 25, 20, 15, 10]
labels = ['Apples', 'Bananas', 'Cherries', 'Dates', 'Elderberries']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, counterclock=False)
plt.title('Fruit Distribution')
plt.axis('equal')  # Ensures circle shape
plt.show()
```

---

## 2. Advanced Pie Charts

```python
# Exploded pie
explode = (0.1, 0, 0, 0, 0)  # Only explode first slice
plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 14})

# Donut chart
plt.pie(sizes, labels=labels, autopct='%1.1f%%',
         wedgeprops={'width': 0.3, 'edgecolor': 'white'})

# Custom wedges
wedges, texts, autotexts = plt.pie(
    sizes, labels=labels, autopct='%1.1f%%',
    pctdistance=0.85,        # Distance of percentage labels
    labeldistance=1.1,        # Distance of category labels
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

# Style the text
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')
```

---

## 3. When to Avoid Pie Charts

```python
# BAD: Too many categories → use a bar chart instead
categories = 12
sizes = np.random.uniform(1, 10, categories)
labels = [f'Category {i}' for i in range(categories)]
# Pie chart with 12 categories is unreadable!
# plt.pie(sizes, labels=labels)  ← DON'T

# GOOD: Convert to bar chart
plt.bar(labels, sizes)
plt.xticks(rotation=45)
```

### Rules of Thumb
- **3-5 categories**: Pie chart works well
- **6-8 categories**: Use with caution
- **9+ categories**: Use a bar chart instead
- **Time series**: Never use a pie chart
- **Small differences**: Bar chart shows differences better

---

## Practice Exercises

1. Create an exploded donut chart with 4 categories
2. Create two subplots: pie chart vs bar chart comparison of the same data
3. Style a pie chart with custom colors, shadows, and text properties
