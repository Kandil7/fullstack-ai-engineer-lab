# =============================================================================
# Django CMS - Reference Guide
# =============================================================================
# Django CMS is a content management system built on top of Django.
# It provides a visual editor, plugin system, and multi-language support.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_cms.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What is Django CMS?
# ---------------------------------------------------------------------------
# Django CMS is an open-source content management system built on Django.
# Key features:
#   - Visual page editor (drag & drop)
#   - Plugin-based architecture
#   - Multi-language support
#   - Version control for content
#   - SEO-friendly URLs
#   - Role-based permissions

# ---------------------------------------------------------------------------
# 2. Installation
# ---------------------------------------------------------------------------
# pip install django-cms

# settings.py:
# INSTALLED_APPS = [
#     ...
#     'cms',              # Django CMS
#     'menus',            # Menu system
#     'treebeard',        # Tree structure for pages
#     'sekizai',          # JavaScript/CSS blocks
#     'djangocms_text_ckeditor',  # Rich text editor
#     # Your apps
# ]
#
# MIDDLEWARE = [
#     'cms.middleware.user.CurrentUserMiddleware',
#     'cms.middleware.page.PageAccessMiddleware',
#     'cms.middleware.toolbar.ToolbarMiddleware',
#     ...
# ]
#
# CMS_TEMPLATES = [
#     ('base.html', 'Base Template'),
#     ('blog.html', 'Blog Page'),
#     ('landing.html', 'Landing Page'),
# ]
#
# LANGUAGE_CODE = 'en'
# LANGUAGES = [
#     ('en', 'English'),
#     ('es', 'Spanish'),
# ]

# ---------------------------------------------------------------------------
# 3. Creating a CMS Site
# ---------------------------------------------------------------------------
# After installation, run migrations and create a superuser:
#   python manage.py migrate
#   python manage.py createsuperuser
#   python manage.py runserver

# Visit /admin/ and add pages using the CMS toolbar.

# ---------------------------------------------------------------------------
# 4. CMS Plugins
# ---------------------------------------------------------------------------
# Plugins are reusable content blocks that can be placed in pages.

# Creating a custom plugin:
# from cms.plugin_base import CMSPluginBase
# from cms.plugin_pool import plugin_pool
# from django.utils.translation import gettext_lazy as _
#
# @plugin_pool.register_plugin
# class TextBlockPlugin(CMSPluginBase):
#     """A simple text block plugin."""
#     model = TextBlock          # Plugin model
#     name = _('Text Block')
#     render_template = 'cms_plugins/text_block.html'
#
#     def render(self, context, instance, placeholder):
#         context.update({
#             'instance': instance,
#         })
#         return context

# Plugin model:
# from cms.models.pluginmodel import CMSPlugin
# from django.db import models
#
# class TextBlock(CMSPlugin):
#     """Text block content."""
#     title = models.CharField(max_length=200, blank=True)
#     content = models.TextField()
#     background_color = models.CharField(max_length=7, default='#ffffff')
#
#     def __str__(self):
#         return self.title or 'Text Block'

# Plugin template:
# <!-- cms_plugins/text_block.html -->
# <div class="text-block" style="background: {{ instance.background_color }}">
#     {% if instance.title %}
#         <h2>{{ instance.title }}</h2>
#     {% endif %}
#     {{ instance.content|safe }}
# </div>

# ---------------------------------------------------------------------------
# 5. App Hooks
# ---------------------------------------------------------------------------
# App hooks integrate your Django apps with Django CMS pages.

# from cms.app_base import CMSApp
# from cms.apphook_pool import apphook_pool
#
# @apphook_pool.register
# class BlogApphook(CMSApp):
#     """Apphook for the blog app."""
#     name = _('Blog')
#
#     def get_urls(self, page=None, language=None, **kwargs):
#         return ['blog.urls']

# Attach apphook to a CMS page:
#   1. Go to admin → Pages
#   2. Edit a page
#   3. Advanced Settings → Application
#   4. Select "Blog" apphook
#   5. Save

# ---------------------------------------------------------------------------
# 6. Menu System
# ---------------------------------------------------------------------------
# Django CMS has a built-in menu system.

# Custom menu:
# from menus.menu_pool import menu_pool
# from menus.base import MenuItem, Menu
#
# class BlogMenu(Menu):
#     """Blog section menu."""
#     name = _('Blog Menu')
#
#     def get_nodes(self, request):
#         nodes = []
#         nodes.append(MenuItem(
#             title=_('All Posts'),
#             url='/blog/',
#             id='blog-all',
#         ))
#         nodes.append(MenuItem(
#             title=_('Categories'),
#             url='/blog/categories/',
#             id='blog-categories',
#             parent_id='blog-all',
#         ))
#         return nodes
#
# menu_pool.register_menu(BlogMenu)

# Template usage:
# {% load menu_tags %}
# {% show_menu %}              # Full menu
# {% show_menu 1 2 100 100 %}  # Custom menu levels

# ---------------------------------------------------------------------------
# 7. Django CMS vs Other Options
# ---------------------------------------------------------------------------

# Django CMS:
#   ✅ Visual editor
#   ✅ Plugin system
#   ✅ Multi-language
#   ❌ Complex setup
#   ❌ Heavy dependencies
#
# Wagtail:
#   ✅ Modern UI
#   ✅ Image handling
#   ✅ StreamField
#   ❌ Less plugin ecosystem
#
# FeinCMS:
#   ✅ Lightweight
#   ✅ Flexible
#   ❌ Less features
#
# Plain Django:
#   ✅ Full control
#   ✅ No dependencies
#   ❌ Build everything yourself

# ---------------------------------------------------------------------------
# 8. Wagtail CMS (Alternative)
# ---------------------------------------------------------------------------
# Wagtail is another popular Django-based CMS.

# pip install wagtail

# settings.py:
# INSTALLED_APPS = [
#     ...
#     'wagtail',
#     'wagtail.admin',
#     'wagtail.core',
#     'wagtail.documents',
#     'wagtail.images',
#     'wagtail.snippets',
#     'wagtail.users',
#     'modelcluster',
#     'taggit',
# ]

# Page model:
# from wagtail.core.models import Page
# from wagtail.core.fields import RichTextField, StreamField
# from wagtail.core import blocks
# from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
#
# class BlogPage(Page):
#     body = StreamField([
#         ('heading', blocks.CharBlock()),
#         ('paragraph', blocks.RichTextBlock()),
#         ('image', blocks.ImageChooserBlock()),
#         ('code', blocks.TextBlock()),
#     ])
#
#     content_panels = Page.content_panels + [
#         StreamFieldPanel('body'),
#     ]

# ---------------------------------------------------------------------------
# 9. Building a Simple CMS with Plain Django
# ---------------------------------------------------------------------------
# If you don't want a full CMS framework, you can build a simple one.

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Page(models.Model):
    """Simple CMS page."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/{self.slug}/'


class ContentBlock(models.Model):
    """Reusable content block."""
    BLOCK_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('code', 'Code'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='blocks/', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.block_type}: {self.title}'

# Views:
# from django.shortcuts import render, get_object_or_404
#
# def cms_page(request, slug):
#     page = get_object_or_404(Page, slug=slug, is_published=True)
#     blocks = page.blocks.all()
#     return render(request, 'cms/page.html', {
#         'page': page,
#         'blocks': blocks,
#     })

# ---------------------------------------------------------------------------
# 10. CMS Best Practices
# ---------------------------------------------------------------------------
# 1. Choose the right CMS for your needs (don't over-engineer)
# 2. Use apphooks to integrate custom apps with CMS pages
# 3. Keep content and presentation separate
# 4. Use plugins for reusable content blocks
# 5. Implement SEO-friendly URLs and meta tags
# 6. Add caching for frequently accessed pages
# 7. Use version control for content changes
# 8. Set up proper permissions for content editors
# 9. Test multi-language content thoroughly
# 10. Back up your database regularly
