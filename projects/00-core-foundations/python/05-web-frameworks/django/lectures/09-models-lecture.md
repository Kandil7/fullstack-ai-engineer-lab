# Django Lecture 09: Models

## 🎯 Topic Overview

Models — essential Django concept for building web applications.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand Django models concepts
2. Implement models in Django projects
3. Handle common errors and edge cases
4. Apply Django best practices
5. Integrate with other Django components

---

## 1. Introduction

This lecture covers models in Django. Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries-included" philosophy, providing built-in tools for common web development tasks.

---

## 2. Core Concepts

### 1. Model Definition

`class BlogPost(models.Model):` with field definitions as class attributes.

### 2. Field Types

CharField, TextField, IntegerField, BooleanField, DateTimeField, ForeignKey, ManyToManyField.

### 3. Meta Class

`class Meta:` with db_table, ordering, verbose_name, unique_together.

### 4. __str__ Method

Defines human-readable representation for admin and shell.

---

## 3. Common Mistakes

### Wrong import paths
Django apps are Python packages - always use full import paths:
```python
# WRONG - will cause ImportError
from views import index

# RIGHT - includes the app name
from blog.views import index
```

### Missing app registration
Every app must be registered in INSTALLED_APPS:
```python
# WRONG - app won't be recognized
INSTALLED_APPS = [
    'django.contrib.admin',
    # 'blog' is missing!
]

# RIGHT - app is registered
INSTALLED_APPS = [
    'django.contrib.admin',
    'blog.apps.BlogConfig',
]
```

### Not running migrations after model changes
```bash
# After creating or modifying models, always run:
python manage.py makemigrations
python manage.py migrate
```

---

## 4. Best Practices

1. Keep apps **small and focused** with single responsibility
2. Use **class-based views** for reusable, DRY view logic
3. Use **template inheritance** (`extends`, `block`) for DRY templates
4. Always **validate form input** with Django Forms
5. Use **database indexes** on frequently queried fields
6. Follow **PEP 8** and Django's coding style guide
7. Write **tests** for models, views, and forms
8. Use **environment variables** for secrets (SECRET_KEY, DB passwords)

---

## 5. Practice Exercises

### Exercise 1: Basic Implementation
Create a Django app that implements the models concept covered in this lecture. Include proper URL routing and template rendering.

### Exercise 2: Error Handling
Add comprehensive error handling, input validation, and edge case coverage to your implementation.

### Exercise 3: Testing
Write unit tests for your Django implementation, covering normal cases, edge cases, and error conditions.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Django | Batteries-included Python web framework |
| MVT | Model-View-Template architecture |
| Convention | Follow Django's conventions for rapid development |
| DRY | Don't Repeat Yourself - reuse templates and views |
| Security | Django has built-in protection against common attacks |
| Scalability | Django powers high-traffic sites (Instagram, Pinterest) |
