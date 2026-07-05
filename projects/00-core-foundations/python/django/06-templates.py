# =============================================================================
# Django Templates - Reference Guide
# =============================================================================
# Templates are the presentation layer in Django. They separate HTML from
# Python logic using Django's template language.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_templates.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Template Basics
# ---------------------------------------------------------------------------
# Templates are HTML files with special Django syntax for dynamic content.
# They live in a 'templates/' directory within your app.

# Project structure:
# blog/
# └── templates/
#     └── blog/          # App-namespaced templates
#         ├── base.html
#         ├── post_list.html
#         └── post_detail.html

# ---------------------------------------------------------------------------
# 2. Template Configuration (settings.py)
# ---------------------------------------------------------------------------
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],  # Project-level templates
#         'APP_DIRS': True,                   # Look in app templates/
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# ---------------------------------------------------------------------------
# 3. Template Tags ({{ }})
# ---------------------------------------------------------------------------
# Variables are enclosed in double curly braces.

# Variable examples:
# {{ variable }}            → Output variable value
# {{ user.name }}           → Access object attribute
# {{ items.0 }}             → Access list item by index
# {{ dict.key }}            → Access dictionary key
# {{ object.method }}       → Call a method

# Example context:
# {'name': 'John', 'items': ['apple', 'banana'], 'user': {'age': 30}}

# Template output:
# Hello, {{ name }}!                → Hello, John!
# First item: {{ items.0 }}        → First item: apple
# Age: {{ user.age }}              → Age: 30

# ---------------------------------------------------------------------------
# 4. Template Tags ({% %})
# ---------------------------------------------------------------------------
# Tags provide logic and control flow.

# --- For loop ---
# {% for item in items %}
#     <p>{{ forloop.counter }}. {{ item }}</p>
# {% empty %}
#     <p>No items found.</p>
# {% endfor %}
#
# forloop variables:
#   forloop.counter    → 1, 2, 3, ...
#   forloop.counter0   → 0, 1, 2, ...
#   forloop.first      → True on first iteration
#   forloop.last       → True on last iteration
#   forloop.parentloop → Reference to parent loop

# --- If/else ---
# {% if user.is_authenticated %}
#     Welcome, {{ user.username }}!
# {% elif user.is_anonymous %}
#     Please log in.
# {% else %}
#     Hello, stranger!
# {% endif %}
#
# Comparison operators: ==, !=, <, >, <=, >=, in, not in
# Logical operators: and, or, not

# --- URL tag ---
# {% url 'post_detail' post.id as post_url %}
# <a href="{{ post_url }}">View Post</a>

# --- Static files ---
# {% load static %}
# <img src="{% static 'blog/images/logo.png' %}" alt="Logo">

# --- Template inheritance ---
# {% extends "blog/base.html" %}
# {% block content %}
#     This overrides the base template's content block.
# {% endblock %}

# --- Include ---
# {% include "blog/sidebar.html" with category="django" %}

# --- Load custom tags ---
# {% load blog_tags %}
# {% recent_posts 5 as posts %}

# --- CSRF token (for forms) ---
# <form method="post">
#     {% csrf_token %}
#     ...
# </form>

# --- With (variable assignment) ---
# {% with total=items|length %}
#     There are {{ total }} items.
# {% endwith %}

# --- Comment ---
# {# This is a template comment #}
# {% comment "Optional comment" %}
#     This is a multi-line comment.
# {% endcomment %}

# ---------------------------------------------------------------------------
# 5. Template Filters
# ---------------------------------------------------------------------------
# Filters transform variables. They use the pipe (|) syntax.

# Common filters:
# {{ name|lower }}                    → "john" (lowercase)
# {{ name|upper }}                    → "JOHN" (uppercase)
# {{ name|title }}                    → "John Doe" (title case)
# {{ name|length }}                   → 8 (string length)
# {{ name|default:"N/A" }}            → Default if empty
# {{ text|truncatewords:30 }}         → First 30 words
# {{ text|linebreaks }}               → Convert newlines to <br> and <p>
# {{ list|length_is:"3" }}            → True if list has 3 items
# {{ date|date:"F j, Y" }}            → Format date
# {{ html|safe }}                     → Mark as safe (no escaping)
# {{ text|escape }}                   → Escape HTML characters
# {{ list|join:", " }}                → Join list with separator
# {{ number|floatformat:2 }}          → 2 decimal places
# {{ price|currency }}                → Format as currency
# {{ url|urlencode }}                 → URL-encode the string
# {{ html|striptags }}                → Remove all HTML tags

# Chaining filters:
# {{ name|lower|title }}              → "John Doe"

# ---------------------------------------------------------------------------
# 6. Template Inheritance
# ---------------------------------------------------------------------------
# The most powerful template feature - create a base layout and extend it.

# --- base.html (parent template) ---
# <!DOCTYPE html>
# <html>
# <head>
#     <title>{% block title %}My Site{% endblock %}</title>
#     {% load static %}
#     <link rel="stylesheet" href="{% static 'css/style.css' %}">
# </head>
# <body>
#     <nav>
#         <a href="{% url 'home' %}">Home</a>
#         <a href="{% url 'blog:post_list' %}">Blog</a>
#         {% if user.is_authenticated %}
#             <a href="{% url 'logout' %}">Logout</a>
#         {% else %}
#             <a href="{% url 'login' %}">Login</a>
#         {% endif %}
#     </nav>
#
#     <main>
#         {% block content %}
#         <!-- Child templates override this -->
#         {% endblock %}
#     </main>
#
#     <footer>
#         {% block footer %}
#         <p>&copy; 2026 My Site</p>
#         {% endblock %}
#     </footer>
#
#     {% block extra_js %}{% endblock %}
# </body>
# </html>

# --- post_list.html (child template) ---
# {% extends "blog/base.html" %}
#
# {% block title %}Blog Posts{% endblock %}
#
# {% block content %}
# <h1>Blog Posts</h1>
# {% for post in posts %}
#     <article>
#         <h2><a href="{% url 'blog:post_detail' post.slug %}">{{ post.title }}</a></h2>
#         <p>{{ post.excerpt|truncatewords:30 }}</p>
#         <time>{{ post.created_at|date:"F j, Y" }}</time>
#     </article>
# {% empty %}
#     <p>No posts yet.</p>
# {% endfor %}
# {% endblock %}

# ---------------------------------------------------------------------------
# 7. Template Rendering in Views
# ---------------------------------------------------------------------------

# --- Function-based view ---
from django.shortcuts import render

def post_list(request):
    context = {
        'title': 'Blog Posts',
        'posts': [],  # QuerySet or list
    }
    return render(request, 'blog/post_list.html', context)

# --- Class-based view ---
# from django.views.generic import ListView
# from .models import Post
#
# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'

# ---------------------------------------------------------------------------
# 8. Template Tags (Custom Tags)
# ---------------------------------------------------------------------------
# Create custom template tags and filters.

# blog/templatetags/blog_tags.py:
# from django import template
# from ..models import Post
#
# register = template.Library()
#
# @register.simple_tag
# def total_posts():
#     return Post.objects.count()
#
# @register.inclusion_tag('blog/latest_posts.html')
# def show_latest_posts(count=5):
#     latest_posts = Post.objects.order_by('-created_at')[:count]
#     return {'latest_posts': latest_posts}
#
# @register.filter(name='minutes_read')
# def minutes_read(text):
#     """Estimate reading time"""
#     words = len(text.split())
#     return max(1, round(words / 200))

# Usage in template:
# {% load blog_tags %}
# Total posts: {% total_posts %}
# {% show_latest_posts 3 %}
# Reading time: {{ post.content|minutes_read }} min

# ---------------------------------------------------------------------------
# 9. Context Processors
# ---------------------------------------------------------------------------
# Context processors add variables to every template automatically.

# Built-in context processors:
# - django.template.context_processors.debug    → Adds DEBUG setting
# - django.template.context_processors.request  → Adds request object
# - django.contrib.auth.context_processors.auth → Adds user, messages
# - django.contrib.messages.context_processors.messages → Adds messages

# Custom context processor:
# myapp/context_processors.py:
# def site_settings(request):
#     return {
#         'site_name': 'My Blog',
#         'analytics_id': 'UA-XXXXXXX',
#     }
#
# Add to settings.py:
# TEMPLATES[0]['OPTIONS']['context_processors'].append(
#     'myapp.context_processors.site_settings'
# )

# ---------------------------------------------------------------------------
# 10. Template Best Practices
# ---------------------------------------------------------------------------
# 1. Use app-namespaced templates: templates/blog/post_list.html
# 2. Never put business logic in templates
# 3. Use template inheritance for DRY layouts
# 4. Keep templates simple - heavy logic belongs in views
# 5. Use {% load static %} for all static files
# 6. Always use {% csrf_token %} in forms
# 7. Use |escape or auto-escaping to prevent XSS
# 8. Use {% block %} for extensible points in base templates
# 9. Name template blocks descriptively (title, content, sidebar)
# 10. Don't repeat yourself - use {% include %} for reusable fragments
