# Django Lecture 20: Django REST Framework

## 🎯 Topic Overview

Django REST Framework — essential Django concept for building web applications.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Understand Django django rest framework concepts
2. Implement django rest framework in Django projects
3. Handle common errors and edge cases
4. Apply Django best practices
5. Integrate with other Django components

---

## 1. Introduction

This lecture covers django rest framework in Django. Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries-included" philosophy, providing built-in tools for common web development tasks.

---

## 2. Core Concepts

### 1. DRF Overview

Django REST Framework builds REST APIs on top of Django models.

### 2. Serializers

`class PostSerializer(serializers.ModelSerializer):` converts models to JSON.

### 3. ViewSets

`class PostViewSet(ModelViewSet):` provides CRUD operations automatically.

### 4. Routers

`router.register('posts', PostViewSet)` generates URL patterns automatically.

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
Create a Django app that implements the django rest framework concept covered in this lecture. Include proper URL routing and template rendering.

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
