# =============================================================================
# Django Getting Started - Reference Guide
# =============================================================================
# How to create, configure, and run your first Django project step by step.
#
# W3Schools Django Tutorial: https://www.w3schools.com/django/django_get_started.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Installation
# ---------------------------------------------------------------------------
# Step 1: Create a virtual environment
#   python -m venv venv
#
# Step 2: Activate it
#   Windows:  venv\Scripts\activate
#   Mac/Linux: source venv/bin/activate
#
# Step 3: Install Django
#   pip install django
#
# Step 4: Verify installation
#   python -m django --version

# ---------------------------------------------------------------------------
# 2. Create a Django Project
# ---------------------------------------------------------------------------
# Command: django-admin startproject <project_name>
#
# Example:
#   django-admin startproject mysite
#
# This creates:
#   mysite/
#   ├── manage.py
#   └── mysite/
#       ├── __init__.py
#       ├── settings.py
#       ├── urls.py
#       ├── asgi.py
#       └── wsgi.py

# ---------------------------------------------------------------------------
# 3. The manage.py File
# ---------------------------------------------------------------------------
# manage.py is a command-line utility that lets you interact with Django.
# It's the primary entry point for management commands.

# What manage.py does under the hood:
#   #!/usr/bin/env python
#   """Django's command-line utility for administrative tasks."""
#   import os
#   import sys
#
#   def main():
#       """Run administrative tasks."""
#       os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
#       try:
#           from django.core.management import execute_from_command_line
#       except ImportError as exc:
#           raise ImportError(
#               "Couldn't import Django. Are you sure it's installed and "
#               "available on your PYTHONPATH environment variable? Did you "
#               "forget to activate a virtual environment?"
#           ) from exc
#       execute_from_command_line(sys.argv)
#
#   if __name__ == '__main__':
#       main()

# ---------------------------------------------------------------------------
# 4. Run the Development Server
# ---------------------------------------------------------------------------
# Command: python manage.py runserver
#
# Output:
#   Watching for file changes with StatReloader
#   Performing system checks...
#   System check identified no issues (0 silenced).
#   ...
#   Starting development server at http://127.0.0.1:8000/

# Useful runserver options:
#   python manage.py runserver 8080        # Custom port
#   python manage.py runserver 0.0.0.0:80  # All interfaces, port 80
#   python manage.py runserver --nothreading  # Single-threaded
#   python manage.py runserver --nostatic    # Disable static file serving

# ---------------------------------------------------------------------------
# 5. Django Project Settings (settings.py)
# ---------------------------------------------------------------------------

# --- Basic Settings ---
# The settings.py file is where you configure your Django project.

# Example settings.py with common configurations:

DJANGO_SETTINGS_EXAMPLE = {
    # Security
    "SECRET_KEY": "your-secret-key-change-in-production",

    # Debug mode (NEVER True in production)
    "DEBUG": True,

    # Hosts/domains this site can serve
    "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],

    # Installed apps (Django's own + your apps)
    "INSTALLED_APPS": [
        # Django built-in apps
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Your apps (added after creating them)
        # "blog",
        # "accounts",
    ],

    # Middleware (request/response processing)
    "MIDDLEWARE": [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ],

    # URL configuration
    "ROOT_URLCONF": "mysite.urls",

    # Database
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    },

    # Templates
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],  # Add template directories here
            "APP_DIRS": True,  # Look for templates in app's templates/
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],

    # Static files (CSS, JavaScript, Images)
    "STATIC_URL": "/static/",
    "STATICFILES_DIRS": [],  # Extra static file directories

    # Authentication
    "AUTH_USER_MODEL": "auth.User",  # Default user model
    "LOGIN_URL": "/accounts/login/",
    "LOGIN_REDIRECT_URL": "/",
}

# ---------------------------------------------------------------------------
# 6. Database Configuration
# ---------------------------------------------------------------------------

# --- SQLite (default, great for development) ---
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# --- PostgreSQL (recommended for production) ---
# pip install psycopg2-binary
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# --- MySQL ---
# pip install mysqlclient
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mydatabase',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# ---------------------------------------------------------------------------
# 7. Creating Your First App
# ---------------------------------------------------------------------------
# A Django project can contain multiple apps. Each app handles a specific
# feature or functionality.
#
# Command: python manage.py startapp <app_name>
#
# Example: python manage.py startapp blog

# This creates:
#   blog/
#   ├── __init__.py
#   ├── admin.py          # Admin site configuration
#   ├── apps.py           # App configuration
#   ├── migrations/       # Database migrations
#   │   └── __init__.py
#   ├── models.py         # Database models
#   ├── tests.py          # Tests
#   └── views.py          # View functions/classes

# After creating an app, register it in settings.py:
#   INSTALLED_APPS = [
#       ...
#       'blog',
#   ]

# ---------------------------------------------------------------------------
# 8. Project Structure Best Practices
# ---------------------------------------------------------------------------
#
# mysite/
# ├── manage.py
# ├── db.sqlite3
# ├── requirements.txt
# ├── .env                    # Environment variables (never commit!)
# ├── .gitignore
# ├── mysite/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── asgi.py
# │   └── wsgi.py
# ├── blog/                   # First app
# │   ├── __init__.py
# │   ├── admin.py
# │   ├── apps.py
# │   ├── models.py
# │   ├── views.py
# │   ├── tests.py
# │   ├── urls.py            # App-level URLs
# │   ├── templates/
# │   │   └── blog/
# │   │       └── index.html
# │   └── static/
# │       └── blog/
# │           ├── style.css
# │           └── script.js
# └── accounts/               # Second app (auth)
#     ├── __init__.py
#     ├── admin.py
#     ├── apps.py
#     ├── models.py
#     ├── views.py
#     └── urls.py

# ---------------------------------------------------------------------------
# 9. Common Commands Cheat Sheet
# ---------------------------------------------------------------------------
# django-admin startproject mysite    # Create new project
# python manage.py startapp blog      # Create new app
# python manage.py runserver          # Start dev server
# python manage.py makemigrations     # Generate migrations
# python manage.py migrate            # Apply migrations
# python manage.py createsuperuser    # Create admin user
# python manage.py shell              # Interactive shell
# python manage.py dbshell            # Database shell
# python manage.py test               # Run tests
# python manage.py collectstatic      # Collect static files
# python manage.py loaddata fixture   # Load fixture data
# python manage.py dumpdata > dump.json  # Export data

# ---------------------------------------------------------------------------
# 10. First Run Checklist
# ---------------------------------------------------------------------------
# When starting a new Django project, follow these steps in order:
#
# 1. Create virtual environment
# 2. Install Django
# 3. Create project: django-admin startproject mysite
# 4. cd mysite
# 5. Create apps: python manage.py startapp blog
# 6. Register apps in settings.py
# 7. Configure database in settings.py
# 8. Define models in models.py
# 9. Run migrations: python manage.py makemigrations && python manage.py migrate
# 10. Create superuser: python manage.py createsuperuser
# 11. Register models in admin.py
# 12. Create views in views.py
# 13. Create URL patterns in urls.py
# 14. Create templates in templates/
# 15. Run server: python manage.py runserver
