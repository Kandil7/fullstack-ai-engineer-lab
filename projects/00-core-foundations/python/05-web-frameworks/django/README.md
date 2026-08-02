# Django Tutorial - Reference Guides

> **Note:** Unlike FastAPI (which has an `exercises/` subdirectory with hands-on practice files), Django exercises in this module are **reference-only**. Django is not installed by default in this environment, and these files serve as comprehensive code references for learning Django concepts.

A comprehensive collection of 20 reference guides covering the W3Schools Django tutorial. Each file provides complete code examples for building Django web applications.

## Files

| # | File | Topic |
|---|------|-------|
| 01 | `01-introduction.py` | What is Django, core concepts, project structure |
| 02 | `02-getting-started.py` | Installation, project setup, first run |
| 03 | `03-apps.py` | Creating and organizing Django apps |
| 04 | `04-urls.py` | URL routing, path converters, namespaces |
| 05 | `05-views.py` | Function-based and class-based views |
| 06 | `06-templates.py` | Template language, inheritance, filters |
| 07 | `07-static-files.py` | CSS, JavaScript, images management |
| 08 | `08-admin.py` | Django admin customization |
| 09 | `09-models.py` | Database models, field types, relationships |
| 10 | `10-migrations.py` | Database migrations management |
| 11 | `11-forms.py` | Form handling, validation, ModelForm |
| 12 | `12-auth.py` | Authentication, permissions, user management |
| 13 | `13-static-admin.py` | Admin static files and theming |
| 14 | `14-csrf.py` | CSRF protection and AJAX |
| 15 | `15-generics.py` | Generic class-based views |
| 16 | `16-relationships.py` | ForeignKey, OneToOne, ManyToMany |
| 17 | `17-querysets.py` | QuerySet API and optimization |
| 18 | `18-pagination.py` | Pagination for views and templates |
| 19 | `19-django-cms.py` | Django CMS and Wagtail overview |
| 20 | `20-rest-framework.py` | Django REST Framework APIs |

## How to Use

These are **reference guides**, not runnable scripts. Each file contains:

1. **Conceptual explanations** of Django features
2. **Complete code examples** you can copy into your project
3. **Best practices** and common patterns
4. **Configuration snippets** for settings.py, urls.py, views.py, etc.

## Quick Start

```bash
# Install Django
pip install django

# Create a new project
django-admin startproject mysite
cd mysite

# Create an app
python manage.py startapp blog

# Run the server
python manage.py runserver

# Visit http://127.0.0.1:8000/
```

## Recommended Reading Order

1. Start with `01-introduction.py` and `02-getting-started.py`
2. Learn `03-apps.py` and `04-urls.py` for project structure
3. Study `05-views.py` and `06-templates.py` for request handling
4. Understand `09-models.py` and `10-migrations.py` for data
5. Master `11-forms.py` and `12-auth.py` for user interaction
6. Explore `17-querysets.py` for database optimization
7. Build APIs with `20-rest-framework.py`

## Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [W3Schools Django Tutorial](https://www.w3schools.com/django/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Django Polls Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
