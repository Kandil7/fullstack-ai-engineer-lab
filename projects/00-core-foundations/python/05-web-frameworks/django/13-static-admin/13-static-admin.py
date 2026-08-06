# =============================================================================
# Django Static Files & Admin Styling - Reference Guide
# =============================================================================
# Managing static files and customizing the Django admin appearance.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_admin_static.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Static Files in Django Admin
# ---------------------------------------------------------------------------
# Django admin uses its own static files (CSS, JS, images).
# These are stored in django/contrib/admin/static/admin/.

# To customize admin appearance:
# 1. Create custom CSS
# 2. Override admin templates
# 3. Use django-contrib-admin package for theming

# ---------------------------------------------------------------------------
# 2. Custom Admin CSS
# ---------------------------------------------------------------------------

# Create directory structure:
# myapp/
# └── static/
#     └── admin/
#         └── css/
#             └── custom.css

# In custom.css:
# /* Override admin styles */
# #header {
#     background-color: #2c3e50;
# }
#
# #branding h1 a {
#     color: #ecf0f1;
# }
#
# .module {
#     border-color: #3498db;
# }
#
# .submit-row {
#     background-color: #f8f9fa;
# }

# Add to settings.py (if needed):
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]

# ---------------------------------------------------------------------------
# 3. Custom Admin Templates
# ---------------------------------------------------------------------------
# Override admin templates by placing them in your app's templates/admin/ directory.

# templates/admin/base_site.html:
# {% extends "admin/base_site.html" %}
#
# {% block title %}{{ title }} | My Site Admin{% endblock %}
#
# {% block branding %}
# <h1 id="site-name">
#     <a href="{% url 'admin:index' %}">My Custom Admin</a>
# </h1>
# {% endblock %}
#
# {% block extrastyle %}
#     {{ block.super }}
#     <link rel="stylesheet" href="{% static 'admin/css/custom.css' %}">
# {% endblock %}

# templates/admin/index.html:
# {% extends "admin/index.html" %}
#
# {% block content_title %}
# <h2>Dashboard</h2>
# {% endblock %}
#
# {% block sidebar %}
#     {{ block.super }}
#     <div class="custom-sidebar">
#         <h3>Quick Links</h3>
#         <ul>
#             <li><a href="/blog/">View Blog</a></li>
#             <li><a href="/reports/">Reports</a></li>
#         </ul>
#     </div>
# {% endblock %}

# ---------------------------------------------------------------------------
# 4. Admin Theme Packages
# ---------------------------------------------------------------------------
# Pre-built admin themes:
#
# django-grappelli     → Professional-looking admin theme
#   pip install django-grappelli
#   INSTALLED_APPS = [..., 'grappelli']
#
# django-jet           → Modern admin interface
#   pip install django-jet
#   INSTALLED_APPS = [..., 'jet']
#
# django-suit          → Another admin theme
#   pip install django-suit-v2
#   INSTALLED_APPS = [..., 'suit']
#
# django-unfold        → Modern Material Design admin
#   pip install django-unfold
#   INSTALLED_APPS = [..., 'unfold']

# ---------------------------------------------------------------------------
# 5. Customizing Admin Appearance
# ---------------------------------------------------------------------------

# --- Custom admin site branding ---
from django.contrib import admin

class MyAdminSite(admin.AdminSite):
    site_header = 'My Blog Administration'
    site_title = 'My Blog Admin'
    index_title = 'Welcome to My Blog Admin'

    # Custom URL for reports
    def get_urls(self):
        from django.urls import path
        custom_urls = [
            path('reports/', self.admin_view(self.reports_view)),
        ]
        return custom_urls + super().get_urls()

    def reports_view(self, request):
        from django.http import HttpResponse
        return HttpResponse('<h1>Reports</h1>')

# Use custom admin site:
admin_site = MyAdminSite(name='myadmin')
admin.site = admin_site

# Register models with custom site:
# admin_site.register(Post, PostAdmin)

# ---------------------------------------------------------------------------
# 6. Admin Dashboard Customization
# ---------------------------------------------------------------------------

# --- Custom admin index with app cards ---
# templates/admin/app_index.html:
# {% extends "admin/app_index.html" %}
#
# {% block content %}
# <div class="app-header">
#     <h1>{{ app_config.verbose_name }}</h1>
#     <p>{{ app_config.description }}</p>
# </div>
# {{ block.super }}
# {% endblock %}

# --- Custom admin actions dashboard ---
# templates/admin/change_list.html:
# {% extends "admin/change_list.html" %}
#
# {% block content_title %}
#     <h2>{{ title }}</h2>
#     {% if description %}
#         <p class="description">{{ description }}</p>
#     {% endif %}
# {% endblock %}

# ---------------------------------------------------------------------------
# 7. Admin Field Formatting
# ---------------------------------------------------------------------------
# Use custom admin display for better data presentation.

# from django.contrib import admin
# from django.utils.html import format_html
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'status_badge', 'created_at')
#
#     def status_badge(self, obj):
#         """Display status as colored badge."""
#         colors = {
#             'draft': '#ffc107',
#             'published': '#28a745',
#             'archived': '#6c757d',
#         }
#         color = colors.get(obj.status, '#6c757d')
#         return format_html(
#             '<span style="background:{}; color:white; padding:2px 8px; '
#             'border-radius:3px;">{}</span>',
#             color,
#             obj.get_status_display()
#         )
#     status_badge.short_description = 'Status'

# ---------------------------------------------------------------------------
# 8. Static Files Management Commands
# ---------------------------------------------------------------------------

# collectstatic:
#   python manage.py collectstatic          # Collect all static files
#   python manage.py collectstatic --noinput  # No confirmation prompt
#   python manage.py collectstatic --clear    # Clear before collecting

# findstatic:
#   python manage.py findstatic admin/css/base.css
#   # Shows all locations where a static file is found

# ---------------------------------------------------------------------------
# 9. Static File Finders Configuration
# ---------------------------------------------------------------------------

# settings.py:
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',   # STATICFILES_DIRS
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder', # app/static/
# ]
#
# # Add custom finders if needed:
# # 'myapp.finders.CustomFinder',

# ---------------------------------------------------------------------------
# 10. Admin Customization Best Practices
# ---------------------------------------------------------------------------
# 1. Use django-grappelli or django-unfold for quick theming
# 2. Keep admin customizations minimal - focus on usability
# 3. Add helpful list_display and list_filter for data management
# 4. Use fieldsets to organize complex model forms
# 5. Add custom admin actions for common operations
# 6. Test admin changes with different user permission levels
# 7. Keep admin templates DRY - extend base templates
# 8. Use format_html for safe HTML in admin displays
# 9. Add admin documentation for non-technical users
# 10. Monitor admin usage for UX improvements
