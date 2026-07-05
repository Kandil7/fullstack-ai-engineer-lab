# =============================================================================
# Django Introduction - Reference Guide
# =============================================================================
# Django is a high-level Python web framework that encourages rapid development
# and clean, pragmatic design. Built by experienced developers, it takes care
# of much of the hassle of web development.
#
# W3Schools Django Tutorial: https://www.w3schools.com/django/
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What is Django?
# ---------------------------------------------------------------------------
# Django is a Python web framework for building web applications. Key features:
# - Full-featured: ORM, auth, admin, templating, URL routing
# - Secure: protection against SQL injection, XSS, CSRF, clickjacking
# - Scalable: handles high-traffic sites (Instagram, Pinterest, NASA)
# - Rapid development: built-in tools and conventions

# ---------------------------------------------------------------------------
# 2. Django vs Other Frameworks
# ---------------------------------------------------------------------------
# Flask  - Micro-framework, minimal core, add extensions as needed
# Django - "Batteries included", comes with ORM, admin, auth, etc.
# FastAPI- Async-first, automatic API docs, type-hint driven
#
# When to use Django:
#   - Full-featured web applications (CMS, e-commerce, SaaS)
#   - Projects needing ORM, auth, and admin out of the box
#   - Teams that prefer convention over configuration
#
# When NOT to use Django:
#   - Microservices or small APIs (use FastAPI/Flask)
#   - Real-time WebSocket-heavy apps (consider channels or other tools)
#   - You need extreme performance (Django is synchronous by default)

# ---------------------------------------------------------------------------
# 3. Core Concepts
# ---------------------------------------------------------------------------

# Django follows the MVT (Model-View-Template) pattern:
#
# ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
# │  Client   │───>│   URL    │───>│   View   │───>│ Template │
# │ (Browser) │    │  Router  │    │ (Logic)  │    │  (HTML)  │
# └──────────┘    └──────────┘    └────┬─────┘    └──────────┘
#                                      │
#                                      v
#                                 ┌──────────┐
#                                 │  Model   │
#                                 │  (Data)  │
#                                 └──────────┘
#
# Models       → Define database structure (Python classes)
# Views        → Handle HTTP request/response logic
# Templates    → HTML files with template language
# URLs         → Map URLs to views

# ---------------------------------------------------------------------------
# 4. Prerequisites
# ---------------------------------------------------------------------------
# Python 3.8+ required
# Install Django: pip install django
# Verify installation:
#   python -m django --version

# A quick check script you can actually run:
if __name__ == "__main__":
    import django
    print(f"Django version: {django.__version__}")
    print("Django is installed and ready!")
    print()
    print("To create a new project, run:")
    print("  django-admin startproject mysite")
    print()
    print("Then navigate into it:")
    print("  cd mysite")
    print()
    print("Start the development server:")
    print("  python manage.py runserver")
    print()
    print("Visit http://127.0.0.1:8000/ in your browser.")

# ---------------------------------------------------------------------------
# 5. Django Project Structure
# ---------------------------------------------------------------------------
# After running `django-admin startproject mysite`:
#
# mysite/
# ├── manage.py            # Command-line utility (runserver, migrate, etc.)
# └── mysite/              # Project package
#     ├── __init__.py      # Marks this as a Python package
#     ├── settings.py      # Project settings (DB, apps, middleware, etc.)
#     ├── urls.py          # Root URL configuration
#     ├── asgi.py          # ASGI entry point (async)
#     └── wsgi.py          # WSGI entry point (traditional)

# ---------------------------------------------------------------------------
# 6. Key Files Explained
# ---------------------------------------------------------------------------

# --- settings.py (key settings) ---
# The settings.py file contains all configuration for your Django project:

# SECRET_KEY = 'your-secret-key-here'  # Keep this secret in production!
#
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     # Your apps go here
# ]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # SQLite by default
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
#
# STATIC_URL = '/static/'
#
# ROOT_URLCONF = 'mysite.urls'

# --- urls.py (root URL conf) ---
# This maps URL patterns to views:
#
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('blog/', include('blog.urls')),
# ]

# --- manage.py ---
# The command-line tool for managing your project. Common commands:
#   python manage.py runserver          # Start dev server
#   python manage.py makemigrations     # Create migration files
#   python manage.py migrate            # Apply migrations to DB
#   python manage.py createsuperuser    # Create admin user
#   python manage.py shell              # Open interactive shell
#   python manage.py test               # Run tests

# ---------------------------------------------------------------------------
# 7. Development Server
# ---------------------------------------------------------------------------
# Django comes with a lightweight development server.
# It auto-reloads on code changes.
#
# python manage.py runserver          # Default: port 8000
# python manage.py runserver 8080     # Custom port
# python manage.py runserver 0.0.0.0  # Listen on all interfaces (LAN)
#
# NOTE: The dev server is NOT suitable for production.
#       Use Gunicorn, uWSGI, or Daphne in production.

# ---------------------------------------------------------------------------
# 8. Django Admin (preview)
# ---------------------------------------------------------------------------
# Django provides a ready-to-use admin interface for managing your data.
#
# Steps:
#   1. python manage.py createsuperuser
#   2. Register models in admin.py
#   3. Visit http://127.0.0.1:8000/admin/
#
# This is covered in detail in 08-admin.py

# ---------------------------------------------------------------------------
# 9. Virtual Environments
# ---------------------------------------------------------------------------
# Always use a virtual environment for Django projects:
#
# python -m venv venv            # Create virtual env
# venv\Scripts\activate          # Activate (Windows)
# source venv/bin/activate       # Activate (Mac/Linux)
# pip install django             # Install Django in venv
# pip freeze > requirements.txt  # Save dependencies

# ---------------------------------------------------------------------------
# 10. Quick Start Summary
# ---------------------------------------------------------------------------
# 1. Install Django:        pip install django
# 2. Create project:        django-admin startproject mysite
# 3. Start server:          python manage.py runserver
# 4. Create app:            python manage.py startapp blog
# 5. Add to INSTALLED_APPS: 'blog'
# 6. Define models:         Edit blog/models.py
# 7. Run migrations:        python manage.py makemigrations && python manage.py migrate
# 8. Create admin:          python manage.py createsuperuser
# 9. Build views:           Edit blog/views.py
# 10. Wire up URLs:         Create blog/urls.py, include in mysite/urls.py
