# =============================================================================
# Django Apps - Reference Guide
# =============================================================================
# Django apps are modular components that handle specific functionality.
# A project is made up of one or more apps.
#
# W3Schools Django Tutorial: https://www.w3schools.com/django/django_apps.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What is a Django App?
# ---------------------------------------------------------------------------
# An app is a self-contained module that does one thing well.
# A Django project is a collection of apps that work together.
#
# Examples of apps:
#   - blog      → blog posts, comments
#   - accounts  → user registration, profiles
#   - shop      → products, orders, payments
#   - api       → REST API endpoints

# ---------------------------------------------------------------------------
# 2. Creating an App
# ---------------------------------------------------------------------------
# Command: python manage.py startapp <app_name>
#
# Example: python manage.py startapp blog

# Resulting structure:
#   blog/
#   ├── __init__.py       # Makes it a Python package
#   ├── admin.py          # Register models for admin site
#   ├── apps.py           # App configuration class
#   ├── migrations/       # Database migration files
#   │   └── __init__.py
#   ├── models.py         # Database models (your data schema)
#   ├── tests.py          # Unit tests
#   └── views.py          # Request handlers (views)

# ---------------------------------------------------------------------------
# 3. Registering Your App
# ---------------------------------------------------------------------------
# After creating an app, you MUST register it in settings.py

# settings.py:
INSTALLED_APPS_EXAMPLE = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your custom apps (use the AppConfig path or app name)
    "blog",                    # Simple way
    # "blog.apps.BlogConfig",  # Alternative (explicit)
]

# ---------------------------------------------------------------------------
# 4. App Configuration (apps.py)
# ---------------------------------------------------------------------------
# Every app has a configuration class that controls its behavior.

# blog/apps.py:
# from django.apps import AppConfig
#
# class BlogConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'blog'                    # Must match the app's directory name
#     verbose_name = 'Blog'            # Human-readable name (for admin)
#     label = 'blog'                   # Unique label (no special chars)
#     ordering = ['name']              # App ordering in admin

# ---------------------------------------------------------------------------
# 5. The apps.py File in Detail
# ---------------------------------------------------------------------------

# Example: blog/apps.py with full configuration
BLOG_APP_CONFIG = """
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Blog Application'

    def ready(self):
        # Called when Django starts. Import signals here.
        # import blog.signals  # noqa: F401
        pass
"""

# ---------------------------------------------------------------------------
# 6. App Directory Structure (Expanded)
# ---------------------------------------------------------------------------
# A well-organized app might look like:
#
# blog/
# ├── __init__.py
# ├── admin.py
# ├── apps.py
# ├── models.py
# ├── views.py
# ├── tests.py
# ├── urls.py              # App-level URL routing
# ├── forms.py             # Django forms
# ├── serializers.py       # DRF serializers (if using REST)
# ├── managers.py          # Custom model managers
# ├── signals.py           # Signal handlers
# ├── middleware.py         # Custom middleware
# ├── decorators.py        # Custom decorators
# ├── utils.py             # Utility functions
# ├── constants.py         # App constants
# ├── exceptions.py        # Custom exceptions
# ├── migrations/
# │   ├── __init__.py
# │   └── 0001_initial.py
# ├── templates/
# │   └── blog/
# │       ├── base.html
# │       ├── post_list.html
# │       ├── post_detail.html
# │       └── post_form.html
# ├── static/
# │   └── blog/
# │       ├── css/
# │       │   └── style.css
# │       ├── js/
# │       │   └── main.js
# │       └── images/
# │           └── logo.png
# └── templatetags/        # Custom template tags
#     ├── __init__.py
#     └── blog_tags.py

# ---------------------------------------------------------------------------
# 7. App-Level URLs
# ---------------------------------------------------------------------------
# Each app should have its own urls.py for clean URL organization.

# blog/urls.py:
# from django.urls import path
# from . import views
#
# app_name = 'blog'  # Namespace for reverse URL lookups
#
# urlpatterns = [
#     path('', views.post_list, name='post_list'),
#     path('<int:pk>/', views.post_detail, name='post_detail'),
#     path('create/', views.post_create, name='post_create'),
#     path('<int:pk>/update/', views.post_update, name='post_update'),
#     path('<int:pk>/delete/', views.post_delete, name='post_delete'),
# ]

# Include app URLs in project urls.py:
# mysite/urls.py
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('blog/', include('blog.urls')),       # Blog app URLs
#     path('accounts/', include('accounts.urls')), # Accounts app URLs
# ]

# ---------------------------------------------------------------------------
# 8. Multi-App Project Structure
# ---------------------------------------------------------------------------
# A typical project might have:
#
# mysite/
# ├── blog/          → Posts, comments, categories
# ├── accounts/      → User profiles, authentication
# ├── shop/          → Products, cart, orders
# ├── api/           → REST API endpoints
# └── core/          → Shared utilities, base models

# ---------------------------------------------------------------------------
# 9. Django Built-in Apps
# ---------------------------------------------------------------------------
# Django ships with these apps (in INSTALLED_APPS):
#
# django.contrib.admin       - Admin interface
# django.contrib.auth        - Authentication framework
# django.contrib.contenttypes - Content type framework
# django.contrib.sessions    - Session framework
# django.contrib.messages    - Messaging framework
# django.contrib.staticfiles - Static file management
#
# Optional built-in apps:
# django.contrib.admindocs   - Admin documentation generator
# django.contrib.humanize     - Template filters for human-friendly data
# django.contrib.postgres    - PostgreSQL-specific features
# django.contrib.gis        - GIS/geographic features

# ---------------------------------------------------------------------------
# 10. App Best Practices
# ---------------------------------------------------------------------------
# 1. Single Responsibility: Each app does ONE thing well
# 2. Loose Coupling: Apps should be independent of each other
# 3. Reusable: Design apps to be reusable across projects
# 4. Consistent Naming: Use lowercase, singular names (blog, not blogs)
# 5. Use app_name: Always set app_name in urls.py for namespacing
# 6. Keep views thin: Put business logic in models, services, or utils
# 7. One model per file: When models get complex, split into modules
# 8. Use signals sparingly: Prefer explicit function calls over signals
