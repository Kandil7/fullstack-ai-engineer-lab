# =============================================================================
# Django URLs - Reference Guide
# =============================================================================
# URL routing maps web addresses (URLs) to views that handle them.
#
# W3Schools Django Tutorial: https://www.w3schools.com/django/django_urls.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. URL Basics
# ---------------------------------------------------------------------------
# In Django, URLs are defined in Python files (not .html config files).
# Each URL pattern maps a URL path to a view function or class.

# The URL resolver is configured in mysite/urls.py (ROOT_URLCONF in settings.py)

# ---------------------------------------------------------------------------
# 2. Project-Level URLs (mysite/urls.py)
# ---------------------------------------------------------------------------
# This is the root URL configuration for your entire project.

# mysite/urls.py:
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),       # Django admin
#     path('', include('blog.urls')),         # Blog app
#     path('accounts/', include('accounts.urls')),  # Accounts app
# ]

# ---------------------------------------------------------------------------
# 3. The path() Function
# ---------------------------------------------------------------------------
# Django 2.0+ uses path() for URL routing (re_path() for regex)

from django.urls import path

# Basic path examples:
urlpatterns = [
    # path('route', view, name='optional-name')
    # Examples:
    # path('', views.home),                           # Home page
    # path('blog/', views.post_list),                 # Blog listing
    # path('blog/<int:pk>/', views.post_detail),      # Blog detail
    # path('blog/create/', views.post_create),         # Create post
]

# ---------------------------------------------------------------------------
# 4. Path Converters
# ---------------------------------------------------------------------------
# Path converters extract values from URLs and pass them to views.

# Available converters:
# str    → Matches any non-empty string (excluding /)
# int    → Matches positive integers (0, 1, 2, ...)
# slug   → Matches slug strings (letters, numbers, hyphens, underscores)
# uuid   → Matches UUID strings
# path   → Matches any non-empty string (including /)

# Examples:
path_converters_example = [
    # str - default converter
    path('articles/<str:title>/', 'view_article'),
    # Matches: /articles/hello-world/, /articles/django-tips/

    # int
    path('posts/<int:id>/', 'view_post'),
    # Matches: /posts/1/, /posts/42/

    # slug
    path('pages/<slug:slug>/', 'view_page'),
    # Matches: /pages/about/, /pages/contact-us/

    # uuid
    path('users/<uuid:user_id>/', 'view_user'),
    # Matches: /users/550e8400-e29b-41d4-a716-446655440000/

    # path (includes /)
    path('files/<path:filepath>/', 'view_file'),
    # Matches: /files/docs/readme.txt/, /files/a/b/c/
]

# ---------------------------------------------------------------------------
# 5. URL Parameters
# ---------------------------------------------------------------------------
# Parameters extracted from URLs are passed as arguments to views.

# blog/urls.py:
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.post_list, name='post_list'),
#     path('<int:pk>/', views.post_detail, name='post_detail'),
#     path('<int:pk>/edit/', views.post_edit, name='post_edit'),
#     path('category/<slug:slug>/', views.category_posts, name='category_posts'),
# ]

# Views receive these as function arguments:
# def post_detail(request, pk):
#     """pk comes from <int:pk> in the URL pattern"""
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# ---------------------------------------------------------------------------
# 6. URL Names
# ---------------------------------------------------------------------------
# The 'name' parameter gives URLs a unique name for reverse lookups.

# Named URLs in urls.py:
# path('blog/<int:pk>/', views.post_detail, name='post_detail')

# Reverse URL lookup in Python:
# from django.urls import reverse
# url = reverse('post_detail', args=[42])  # → '/blog/42/'
# url = reverse('post_detail', kwargs={'pk': 42})  # → '/blog/42/'

# Reverse URL lookup in templates:
# {{ post_detail|arg:post.id }}  → '/blog/42/'
# {% url 'post_detail' post.id %}  → '/blog/42/'

# ---------------------------------------------------------------------------
# 7. URL Namespacing
# ---------------------------------------------------------------------------
# Namespaces prevent URL name collisions between apps.

# blog/urls.py:
# app_name = 'blog'  # Set the namespace
# urlpatterns = [
#     path('', views.post_list, name='post_list'),
# ]

# mysite/urls.py:
# urlpatterns = [
#     path('blog/', include('blog.urls', namespace='blog')),
# ]

# Using namespaced URLs:
# In Python: reverse('blog:post_list')  → '/blog/'
# In templates: {% url 'blog:post_list' %}  → '/blog/'

# ---------------------------------------------------------------------------
# 8. Including Other URL Files
# ---------------------------------------------------------------------------
# Use include() to split URL patterns across multiple files.

# mysite/urls.py:
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('blog/', include('blog.urls')),
#     path('accounts/', include('accounts.urls')),
#     path('api/', include('api.urls')),
# ]

# The URL prefix is stripped before matching:
# 'blog/' → blog/urls.py sees '' (not 'blog/')

# ---------------------------------------------------------------------------
# 9. re_path() for Regex Patterns
# ---------------------------------------------------------------------------
# For complex URL patterns, use re_path() with regular expressions.

# from django.urls import re_path
#
# urlpatterns = [
#     # Year/month/day pattern
#     re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
#             views.article_archive),
#
#     # Optional parameter (with ?)
#     re_path(r'^blog/page/(?P<page>[0-9]+)?/$', views.post_list),
# ]

# In views, regex named groups are passed as kwargs:
# def article_archive(request, year, month):
#     ...

# ---------------------------------------------------------------------------
# 10. URL Patterns Best Practices
# ---------------------------------------------------------------------------
# 1. Use named URLs always - enables reverse lookups and refactoring
# 2. Use path() over re_path() when possible (cleaner, more readable)
# 3. Keep URLs at the app level - each app has its own urls.py
# 4. Use namespaces to avoid name collisions
# 5. Use trailing slashes: 'blog/' not 'blog'
# 6. Use slugs over IDs in URLs (better for SEO)
# 7. Keep URLs descriptive: '/blog/my-post-title/' not '/blog/42/'
#
# Example of good URL design:
# GET  /blog/              → List all posts
# GET  /blog/create/       → Create new post form
# GET  /blog/my-post/      → View post (slug-based)
# GET  /blog/my-post/edit/ → Edit post
# POST /blog/my-post/delete/ → Delete post

# ---------------------------------------------------------------------------
# 11. Dynamic URL Example
# ---------------------------------------------------------------------------
# Complete example of a blog URL configuration:

# blog/urls.py:
from django.urls import path

app_name = 'blog'

urlpatterns = [
    # List all posts
    path('', views.post_list, name='post_list'),

    # View single post by slug
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Create new post
    path('post/new/', views.post_create, name='post_create'),

    # Edit post
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    # Delete post
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),

    # Category filter
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

    # Search
    path('search/', views.search_posts, name='search_posts'),
]
