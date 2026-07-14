# =============================================================================
# Django Admin - Reference Guide
# =============================================================================
# Django provides a built-in admin interface for managing your data.
# It auto-generates an admin UI from your models.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_admin.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Setting Up the Admin
# ---------------------------------------------------------------------------
# Step 1: Ensure 'django.contrib.admin' is in INSTALLED_APPS (it is by default)
#
# Step 2: Run migrations (admin needs its own tables):
#   python manage.py migrate
#
# Step 3: Create a superuser:
#   python manage.py createsuperuser
#   → Enter username, email, password
#
# Step 4: Start the server:
#   python manage.py runserver
#
# Step 5: Visit http://127.0.0.1:8000/admin/

# ---------------------------------------------------------------------------
# 2. Registering Models in Admin
# ---------------------------------------------------------------------------
# By default, models don't appear in admin. You must register them.

# blog/admin.py:
# from django.contrib import admin
# from .models import Post, Category, Comment

# --- Basic registration ---
# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Comment)

# --- Registration with custom admin class ---
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'created_at', 'is_published')
#     list_filter = ('is_published', 'category', 'created_at')
#     search_fields = ('title', 'content')
#     prepopulated_fields = {'slug': ('title',)}
#     date_hierarchy = 'created_at'
#     ordering = ('-created_at',)
#     list_editable = ('is_published',)
#     list_per_page = 20
#     autocomplete_fields = ('author',)
#     filter_horizontal = ('tags',)
#     readonly_fields = ('created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'slug', 'author')
#         }),
#         ('Content', {
#             'fields': ('excerpt', 'content'),
#             'classes': ('collapse',),
#         }),
#         ('Metadata', {
#             'fields': ('category', 'tags', 'is_published', 'created_at'),
#         }),
#     )

# ---------------------------------------------------------------------------
# 3. ModelAdmin Options
# ---------------------------------------------------------------------------

# --- Display options ---
# list_display = ('title', 'author', 'created_at')  # Columns in list view
# list_display_links = ('title',)                     # Clickable columns
# list_editable = ('is_published',)                    # Editable columns
# list_per_page = 20                                   # Pagination
# list_max_show_all = 100                              # Max items in "show all"
# list_select_related = ('author',)                    # Optimize queries

# --- Filtering ---
# list_filter = ('is_published', 'category', 'created_at')  # Sidebar filters
# date_hierarchy = 'created_at'                              # Date drill-down

# --- Search ---
# search_fields = ('title', 'content', 'author__username')  # Search bar
# search_help_text = 'Search by title, content, or author'

# --- Forms ---
# prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug from title
# autocomplete_fields = ('author',)            # Autocomplete foreign keys
# raw_id_fields = ('author',)                  # Raw ID input for FK
# filter_horizontal = ('tags',)                # Horizontal filter for M2M
# filter_vertical = ('tags',)                  # Vertical filter for M2M
# radio_fields = {'status': admin.VERTICAL}    # Radio buttons for choices

# --- Fieldsets (group fields) ---
# fieldsets = (
#     ('Basic Info', {
#         'fields': ('title', 'slug', 'author')
#     }),
#     ('Content', {
#         'fields': ('content',),
#         'classes': ('collapse',),  # Collapsible section
#     }),
#     ('Metadata', {
#         'fields': ('category', 'tags', 'is_published'),
#         'description': 'Additional metadata for this post',
#     }),
# )

# --- Read-only fields ---
# readonly_fields = ('created_at', 'updated_at', 'slug')

# --- Custom display ---
# def get_readonly_fields(self, request, obj=None):
#     if obj:  # Editing existing object
#         return ('created_at', 'slug')
#     return ()  # Creating new object

# ---------------------------------------------------------------------------
# 4. Inline Admin (Related Objects)
# ---------------------------------------------------------------------------
# Show related objects inline (e.g., comments on a post).

# from django.contrib import admin
# from .models import Post, Comment
#
# class CommentInline(admin.TabularInline):  # or StackedInline
#     model = Comment
#     extra = 1                    # Number of empty forms to show
#     readonly_fields = ('created_at',)
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [CommentInline]

# StackedInline shows fields vertically (more space)
# TabularInline shows fields horizontally (compact)

# ---------------------------------------------------------------------------
# 5. Custom Admin Actions
# ---------------------------------------------------------------------------
# Actions are bulk operations on selected items.

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     actions = ['publish_posts', 'unpublish_posts', 'export_csv']
#
#     @admin.action(description='Mark selected posts as published')
#     def publish_posts(self, request, queryset):
#         updated = queryset.update(is_published=True)
#         self.message_user(request, f'{updated} posts published.')
#
#     @admin.action(description='Mark selected posts as unpublished')
#     def unpublish_posts(self, request, queryset):
#         updated = queryset.update(is_published=False)
#         self.message_user(request, f'{updated} posts unpublished.')
#
#     @admin.action(description='Export selected posts as CSV')
#     def export_csv(self, request, queryset):
#         import csv
#         from django.http import HttpResponse
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="posts.csv"'
#         writer = csv.writer(response)
#         writer.writerow(['Title', 'Author', 'Created At'])
#         for post in queryset:
#             writer.writerow([post.title, post.author, post.created_at])
#         return response

# ---------------------------------------------------------------------------
# 6. Admin Templates
# ---------------------------------------------------------------------------
# Customize admin templates by extending the default ones.

# Create templates in your app:
# templates/admin/
# ├── base_site.html      → Change site header/title
# ├── index.html           → Customize admin homepage
# └── change_list.html     → Customize list view

# templates/admin/base_site.html:
# {% extends "admin/base_site.html" %}
#
# {% block branding %}
# <h1 id="site-name">
#     <a href="{% url 'admin:index' %}">My Blog Admin</a>
# </h1>
# {% endblock %}
#
# {% block title %}{{ title }} | My Blog Admin{% endblock %}

# ---------------------------------------------------------------------------
# 7. Admin URLs and Views
# ---------------------------------------------------------------------------
# Django admin provides these views automatically:
#
# /admin/                     → Admin index (list of apps)
# /admin/app/                 → App index (list of models)
# /admin/app/model/           → Model changelist (list of objects)
# /admin/app/model/add/       → Add new object
# /admin/app/model/id/change/ → Edit existing object
# /admin/app/model/id/delete/ → Delete object

# Custom admin views:
# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponse
#
# class MyAdminSite(admin.AdminSite):
#     def get_urls(self):
#         custom_urls = [
#             path('reports/', self.admin_view(self.reports_view)),
#         ]
#         return custom_urls + super().get_urls()
#
#     def reports_view(self, request):
#         return HttpResponse('<h1>Reports</h1>')
#
#     def each_context(self, request):
#         context = super().each_context(request)
#         context['custom_link'] = True
#         return context
#
# # Use custom admin site:
# admin_site = MyAdminSite(name='myadmin')
# admin_site.register(Post)

# ---------------------------------------------------------------------------
# 8. Admin Permissions
# ---------------------------------------------------------------------------
# Django admin uses the permission system to control access.

# By default, admins can:
#   - View all objects
#   - Add new objects
# - Edit existing objects
#   - Delete objects

# Custom permissions in models:
# class Post(models.Model):
#     ...
#     class Meta:
#         permissions = [
#             ('can_publish', 'Can publish posts'),
#             ('can_feature', 'Can feature posts'),
#         ]

# Check permissions in admin:
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     def has_publish_permission(self, request):
#         return request.user.has_perm('blog.can_publish')
#
#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if not request.user.has_perm('blog.can_publish'):
#             del actions['publish_posts']
#         return actions

# ---------------------------------------------------------------------------
# 9. Admin Performance Tips
# ---------------------------------------------------------------------------
# 1. Use select_related in get_queryset():
#    def get_queryset(self, request):
#        return super().get_queryset(request).select_related('author')
#
# 2. Use list_select_related = True for automatic select_related
#
# 3. Add db_index=True to frequently filtered fields
#
# 4. Use autocomplete_fields for ForeignKey/M2M (better than raw_id_fields)
#
# 5. Limit list_per_page for large tables

# ---------------------------------------------------------------------------
# 10. Admin Best Practices
# ---------------------------------------------------------------------------
# 1. Always register important models in admin
# 2. Use @admin.register(Model) decorator (cleaner)
# 3. Configure list_display for useful column views
# 4. Add search_fields for easy searching
# 5. Use fieldsets for complex models
# 6. Add admin actions for common bulk operations
# 7. Use inlines for tightly coupled related models
# 8. Create superuser with a strong password
# 9. Never use admin in production for direct data entry
# 10. Customize admin templates for brand consistency
