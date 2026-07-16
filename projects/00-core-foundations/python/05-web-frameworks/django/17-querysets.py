# =============================================================================
# Django QuerySets - Reference Guide
# =============================================================================
# QuerySets are lazy, chainable database queries. They're the primary way
# to retrieve and filter data from the database.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_querysets.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What are QuerySets?
# ---------------------------------------------------------------------------
# A QuerySet represents a collection of database rows.
# QuerySets are lazy - they don't hit the database until evaluated.

# Examples of evaluation:
#   iterating        → for post in queryset
#   len()            → len(queryset)
#   list()           → list(queryset)
#   bool()           → bool(queryset)
#   slicing          → queryset[0]
#   repr()           → repr(queryset)
#   str()            → str(queryset)

# ---------------------------------------------------------------------------
# 2. Creating QuerySets
# ---------------------------------------------------------------------------

from django.db import models

# Model.objects is the default manager (returns QuerySet)
# posts = Post.objects.all()              # All posts
# posts = Post.objects.filter(status='published')  # Filtered
# posts = Post.objects.order_by('-created_at')     # Ordered
# posts = Post.objects.exclude(status='draft')     # Excluded

# Chaining:
# posts = Post.objects.filter(
#     status='published',
#     author__username='john'
# ).order_by('-created_at')[:10]

# ---------------------------------------------------------------------------
# 3. Filtering (filter, exclude, get)
# ---------------------------------------------------------------------------

# --- filter() - returns QuerySet matching conditions ---
# Post.objects.filter(status='published')
# Post.objects.filter(status='published', author__username='john')
# Post.objects.filter(title__icontains='django')  # Case-insensitive contains

# --- exclude() - returns QuerySet NOT matching conditions ---
# Post.objects.exclude(status='draft')
# Post.objects.exclude(author__username='admin')

# --- get() - returns single object or raises exception ---
# post = Post.objects.get(pk=1)           # Returns one Post
# post = Post.objects.get(slug='my-post') # Returns one Post
# post = Post.objects.get(pk=999)         # Raises Post.DoesNotExist
# post = Post.objects.get(status='x')     # Raises Post.MultipleObjectsReturned

# --- get_or_create() - get or create if not exists ---
# post, created = Post.objects.get_or_create(
#     slug='my-post',
#     defaults={'title': 'My Post', 'content': '...'}
# )
# created is True if a new object was created

# --- update_or_create() - update or create if not exists ---
# post, created = Post.objects.update_or_create(
#     slug='my-post',
#     defaults={'title': 'Updated Title'}
# )

# ---------------------------------------------------------------------------
# 4. Field Lookups
# ---------------------------------------------------------------------------
# Django provides __ lookups for filtering:

# Exact match (default):
# Post.objects.filter(title='Django Tips')

# Case-sensitive contains:
# Post.objects.filter(title__contains='django')

# Case-insensitive contains:
# Post.objects.filter(title__icontains='django')

# Starts with / Ends with:
# Post.objects.filter(title__startswith='Django')
# Post.objects.filter(title__iendswith='tips')

# In a list:
# Post.objects.filter(status__in=['published', 'featured'])

# Greater than / Less than:
# Post.objects.filter(views_count__gt=100)
# Post.objects.filter(views_count__gte=100)   # Greater than or equal
# Post.objects.filter(views_count__lt=100)
# Post.objects.filter(views_count__lte=100)   # Less than or equal

# Range:
# Post.objects.filter(created_at__range=(start_date, end_date))

# Date lookups:
# Post.objects.filter(created_at__year=2026)
# Post.objects.filter(created_at__month=7)
# Post.objects.filter(created_at__day=5)
# Post.objects.filter(created_at__week_day=2)  # Monday

# Null check:
# Post.objects.filter(category__isnull=True)
# Post.objects.filter(category__isnull=False)

# Regex:
# Post.objects.filter(title__regex=r'^Django')  # MySQL not supported
# Post.objects.filter(title__iregex=r'^django')  # Case-insensitive regex

# ---------------------------------------------------------------------------
# 5. Chaining QuerySets
# ---------------------------------------------------------------------------
# QuerySets are lazy and chainable.

# All these are equivalent:
# Post.objects.filter(status='published').filter(author__username='john')
# Post.objects.filter(status='published', author__username='john')

# Chaining operations:
# posts = (Post.objects
#     .filter(status='published')
#     .filter(category__name='Technology')
#     .exclude(is_featured=False)
#     .order_by('-created_at')
#     [:10])

# ---------------------------------------------------------------------------
# 6. Ordering (order_by)
# ---------------------------------------------------------------------------

# Order by single field:
# Post.objects.order_by('title')            # Ascending
# Post.objects.order_by('-title')           # Descending (- prefix)
# Post.objects.order_by('created_at')       # Oldest first
# Post.objects.order_by('-created_at')      # Newest first

# Order by multiple fields:
# Post.objects.order_by('category', '-created_at')

# Random ordering:
# import random
# Post.objects.order_by('?')

# Default ordering (in Meta):
# class Meta:
#     ordering = ['-created_at', 'title']

# ---------------------------------------------------------------------------
# 7. Slicing QuerySets
# ---------------------------------------------------------------------------
# Similar to Python list slicing.

# Get first 5 posts:
# Post.objects.all()[:5]

# Skip first 10, get next 5:
# Post.objects.all()[10:15]

# Get last post:
# Post.objects.all()[-1]

# Note: Negative indexing is NOT supported
# Post.objects.all()[-1]  # Works
# Post.objects.all()[-5:]  # Doesn't work - use reversed()

# ---------------------------------------------------------------------------
# 8. Counting, Checking, and Aggregating
# ---------------------------------------------------------------------------

# --- count() - return number of objects ---
# count = Post.objects.filter(status='published').count()

# --- exists() - check if any objects exist ---
# if Post.objects.filter(status='published').exists():
#     print("There are published posts")

# --- first() / last() - get first/last object ---
# post = Post.objects.order_by('created_at').first()
# post = Post.objects.order_by('created_at').last()

# --- distinct() - remove duplicates ---
# authors = Post.objects.values('author__username').distinct()

# --- aggregate() - perform calculations ---
from django.db.models import Count, Avg, Sum, Min, Max

# stats = Post.objects.aggregate(
#     total_posts=Count('id'),
#     avg_views=Avg('views_count'),
#     total_views=Sum('views_count'),
#     oldest=Min('created_at'),
#     newest=Max('created_at'),
# )
# Returns: {'total_posts': 42, 'avg_views': 15.5, ...}

# --- annotate() - add calculated fields to each object ---
# posts = Post.objects.annotate(
#     comment_count=Count('comments'),
#     has_comments=Count('comments') > 0,
# ).order_by('-comment_count')

# Access: post.comment_count

# ---------------------------------------------------------------------------
# 9. Values and Values_list
# ---------------------------------------------------------------------------

# --- values() - return dictionaries instead of objects ---
# dicts = Post.objects.values('id', 'title', 'author__username')
# Returns: [{'id': 1, 'title': '...', 'author__username': 'john'}, ...]

# All fields:
# dicts = Post.objects.values()

# --- values_list() - return tuples ---
# tuples = Post.objects.values_list('id', 'title')
# Returns: [(1, 'Post 1'), (2, 'Post 2'), ...]

# Flat list (single field):
# titles = Post.objects.values_list('title', flat=True)
# Returns: ['Post 1', 'Post 2', ...]

# ---------------------------------------------------------------------------
# 10. Optimizing QuerySets
# ---------------------------------------------------------------------------
# Avoid N+1 query problems with select_related and prefetch_related.

# --- select_related() - for ForeignKey and OneToOne ---
# Without optimization (N+1 queries):
# posts = Post.objects.all()
# for post in posts:
#     print(post.author.name)  # Extra query for each post!

# With optimization (1 query):
# posts = Post.objects.select_related('author').all()
# for post in posts:
#     print(post.author.name)  # No extra query!

# Multiple relations:
# posts = Post.objects.select_related('author', 'category')

# --- prefetch_related() - for ManyToMany and reverse FK ---
# Without optimization:
# for post in posts:
#     print(post.tags.all())  # Extra query for each post!

# With optimization:
# posts = Post.objects.prefetch_related('tags').all()
# for post in posts:
#     print(post.tags.all())  # No extra query!

# Prefetch with custom queryset:
# from django.db.models import Prefetch
# posts = Post.objects.prefetch_related(
#     Prefetch(
#         'comments',
#         queryset=Comment.objects.filter(is_approved=True),
#         to_attr='approved_comments'
#     )
# )

# --- only() - select specific fields ---
# posts = Post.objects.only('id', 'title', 'created_at')
# # Only these fields are fetched from DB

# --- defer() - defer specific fields ---
# posts = Post.objects.defer('content')
# # content is fetched only when accessed

# ---------------------------------------------------------------------------
# 11. Bulk Operations
# ---------------------------------------------------------------------------

# --- bulk_create() - create multiple objects at once ---
# posts = [
#     Post(title=f'Post {i}', content=f'Content {i}')
#     for i in range(100)
# ]
# Post.objects.bulk_create(posts)

# --- bulk_update() - update multiple objects at once ---
# posts = Post.objects.all()
# for post in posts:
#     post.views_count = 0
# Post.objects.bulk_update(posts, ['views_count'])

# --- update() - update matching objects ---
# Post.objects.filter(status='draft').update(status='published')

# --- delete() - delete matching objects ---
# Post.objects.filter(status='archived').delete()

# ---------------------------------------------------------------------------
# 12. QuerySet Best Practices
# ---------------------------------------------------------------------------
# 1. Use select_related() for ForeignKey (reduces N+1 queries)
# 2. Use prefetch_related() for ManyToMany (reduces N+1 queries)
# 3. Use values()/values_list() when you don't need full objects
# 4. Use exists() instead of count() > 0 (faster)
# 5. Use .iterator() for large result sets (memory efficient)
# 6. Avoid slicing QuerySets multiple times
# 7. Use bulk_create() for inserting many objects
# 8. Use only()/defer() to fetch only needed fields
# 9. Profile queries with django-debug-toolbar
# 10. Use .count() instead of len() on QuerySets
