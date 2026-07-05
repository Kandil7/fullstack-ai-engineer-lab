# =============================================================================
# Django Static Files - Reference Guide
# =============================================================================
# Static files are CSS, JavaScript, images, and other assets that don't
# change dynamically. Django has built-in support for serving them.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_static_files.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Static Files Setup
# ---------------------------------------------------------------------------
# Django separates static files into:
#   - Static files: Your own CSS, JS, images
#   - Media files: User-uploaded content (handled separately)

# ---------------------------------------------------------------------------
# 2. Static Files Configuration (settings.py)
# ---------------------------------------------------------------------------

# Static files settings:
# STATIC_URL = '/static/'              # URL prefix for static files
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files
# STATICFILES_DIRS = [                  # Extra directories to search
#     BASE_DIR / 'static',              # Project-level static files
# ]
#
# # For development:
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
#
# # For production (with Whitenoise):
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------------------------------------------------
# 3. Static Files Directory Structure
# ---------------------------------------------------------------------------
# Project structure:
#
# mysite/
# ├── static/                   # Project-level static (STATICFILES_DIRS)
# │   ├── css/
# │   │   └── global.css
# │   ├── js/
# │   │   └── main.js
# │   └── images/
# │       └── logo.png
# └── blog/
#     └── static/
#         └── blog/             # App-specific static (app name prefix)
#             ├── css/
#             │   └── style.css
#             ├── js/
#             │   └── script.js
#             └── images/
#                 └── hero.jpg

# Important: Use app name prefix for app static files!
#   blog/static/blog/style.css   ✅ (avoids name collisions)
#   blog/static/style.css        ❌ (might conflict with other apps)

# ---------------------------------------------------------------------------
# 4. Loading Static Files in Templates
# ---------------------------------------------------------------------------
# In templates, use the {% static %} tag:

# {% load static %}
# <!DOCTYPE html>
# <html>
# <head>
#     <title>My Blog</title>
#     <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
#     <link rel="stylesheet" href="{% static 'css/global.css' %}">
# </head>
# <body>
#     <img src="{% static 'blog/images/hero.jpg' %}" alt="Hero">
#     <script src="{% static 'blog/js/script.js' %}"></script>
#     <script src="{% static 'js/main.js' %}"></script>
# </body>
# </html>

# ---------------------------------------------------------------------------
# 5. The {% static %} Tag
# ---------------------------------------------------------------------------
# The static tag generates the full URL for a static file.

# Basic usage:
# {% load static %}
# <link rel="stylesheet" href="{% static 'css/style.css' %}">
# Output: <link rel="stylesheet" href="/static/css/style.css">

# With as variable:
# {% static 'images/logo.png' as logo_url %}
# <img src="{{ logo_url }}" alt="Logo">

# Dynamic static references:
# {% for item in items %}
#     <img src="{% static item.image_path %}" alt="{{ item.name }}">
# {% endfor %}

# ---------------------------------------------------------------------------
# 6. collectstatic Command
# ---------------------------------------------------------------------------
# For production, gather all static files into STATIC_ROOT.

# Command:
#   python manage.py collectstatic
#
# What it does:
#   1. Finds all static files from:
#      - Each app's static/ directory
#      - Directories in STATICFILES_DIRS
#      - django.contrib.admin static files
#   2. Copies them to STATIC_ROOT (default: staticfiles/)
#
# Typical production workflow:
#   1. python manage.py collectstatic --noinput
#   2. Serve STATIC_ROOT with Nginx/Apache/Whitenoise

# ---------------------------------------------------------------------------
# 7. Serving Static Files in Development
# ---------------------------------------------------------------------------
# Django's dev server serves static files automatically when DEBUG=True.

# For better dev experience, add:
# INSTALLED_APPS = [
#     ...
#     'whitenoise.runserver_nostatic',  # Before other apps
# ]
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # After security
#     ...
# ]

# ---------------------------------------------------------------------------
# 8. Whitenoise for Production
# ---------------------------------------------------------------------------
# Whitenoise serves static files directly from Django (no Nginx needed).

# Install: pip install whitenoise

# settings.py:
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
#     ...
# ]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Benefits:
# - Serves files with proper cache headers
# - Compresses files (gzip/brotli)
# - Creates unique filenames for cache busting
# - Works without Nginx/Apache

# ---------------------------------------------------------------------------
# 9. Media Files (User Uploads)
# ---------------------------------------------------------------------------
# Media files are different from static files - they're uploaded by users.

# settings.py:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# urls.py (development only):
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # ... other URLs
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Model with file upload:
# from django.db import models
#
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='posts/%Y/%m/', blank=True, null=True)
#     document = models.FileField(upload_to='documents/', blank=True)

# Template usage:
# {% if post.image %}
#     <img src="{{ post.image.url }}" alt="{{ post.title }}">
# {% endif %}
# <a href="{{ post.document.url }}">Download</a>

# ---------------------------------------------------------------------------
# 10. Static Files Finders
# ---------------------------------------------------------------------------
# Django looks for static files using these finders (in order):

# Default finders:
# 1. FileSystemFinder    → Searches STATICFILES_DIRS
# 2. AppDirectoriesFinder → Searches static/ in each app (app name prefix)

# To list all found static files:
#   python manage.py findstatic blog/css/style.css

# Custom finder:
# from django.contrib.staticfiles.finders import BaseFinder
#
# class MyFinder(BaseFinder):
#     def find(self, path, all=False):
#         # Custom logic to find static files
#         pass
#
#     def list(self, ignore_patterns):
#         # Custom logic to list static files
#         pass

# ---------------------------------------------------------------------------
# 11. Cache Busting
# ---------------------------------------------------------------------------
# When you update static files, browsers might serve cached versions.
# Use cache busting to force reloads.

# Whitenoise with CompressedManifestStaticFilesStorage automatically
# creates unique filenames:
#   style.css → style.a1b2c3d4.css

# Manual cache busting in templates:
# <link rel="stylesheet" href="{% static 'css/style.css' %}?v=2">

# ---------------------------------------------------------------------------
# 12. Static Files Best Practices
# ---------------------------------------------------------------------------
# 1. Use app-namespaced static dirs: blog/static/blog/
# 2. Use project-level static for shared assets
# 3. Minify CSS/JS for production
# 4. Use Whitenoise for simple production setups
# 5. Use Nginx for high-traffic production
# 6. Set proper cache headers for static files
# 7. Use collectstatic --noinput in CI/CD
# 8. Store user uploads on cloud storage (S3, GCS)
# 9. Never serve media files through Django in production
# 10. Use CDN for static files in production
