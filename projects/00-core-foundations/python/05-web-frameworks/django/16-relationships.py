# =============================================================================
# Django Relationships - Reference Guide
# =============================================================================
# Models can be related to each other in three ways:
#   ForeignKey → Many-to-One
#   OneToOneField → One-to-One
#   ManyToManyField → Many-to-Many
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_many_to_many.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Many-to-One (ForeignKey)
# ---------------------------------------------------------------------------
# One record in Table A can be linked to many records in Table B.
# Example: One Author → Many Posts

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Author model (the 'one' side)."""
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post model (the 'many' side)."""
    title = models.CharField(max_length=200)
    content = models.TextField()

    # ForeignKey: Many Posts → One Author
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,       # Delete posts when author is deleted
        related_name='posts',           # author.posts.all()
        related_query_name='post',      # Author.objects.filter(post__title='...')
        db_index=True,                  # Index for faster lookups
    )

    def __str__(self):
        return self.title

# on_delete options:
# CASCADE        → Delete all related objects
# PROTECT        → Prevent deletion (raise ProtectedError)
# RESTRICT       → Like PROTECT but allows cascade through intermediate
# SET_NULL       → Set ForeignKey to NULL
# SET_DEFAULT    → Set ForeignKey to default value
# SET(value)     → Set ForeignKey to a specific value
# DO_NOTHING     → Do nothing (can cause integrity errors)

# Usage:
# post = Post.objects.get(pk=1)
# author = post.author          # Get the author
# posts = author.posts.all()    # Get all posts by author

# ---------------------------------------------------------------------------
# 2. One-to-One (OneToOneField)
# ---------------------------------------------------------------------------
# One record in Table A is linked to exactly one record in Table B.
# Example: One User → One Profile

class Profile(models.Model):
    """User profile (extended user info)."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=False,              # Don't make it the primary key
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

# Usage:
# user = User.objects.get(pk=1)
# profile = user.profile          # Get profile
# user = profile.user             # Get user from profile

# Auto-create profile on user creation (signal):
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# ---------------------------------------------------------------------------
# 3. Many-to-Many (ManyToManyField)
# ---------------------------------------------------------------------------
# Records in both tables can be linked to multiple records in the other.
# Example: Many Posts ↔ Many Tags

class Tag(models.Model):
    """Tag model."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article with many-to-many relationship to Tag."""
    title = models.CharField(max_length=200)
    content = models.TextField()

    # ManyToManyField: Articles ↔ Tags
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        related_query_name='article',
        # through='ArticleTag',         # Custom through model
        # through_fields=('article', 'tag'),  # Specify FK fields
    )

    def __str__(self):
        return self.title

# Usage:
# article = Article.objects.get(pk=1)
#
# # Add tags
# tag = Tag.objects.get(name='django')
# article.tags.add(tag)              # Add single tag
# article.tags.add(tag1, tag2)       # Add multiple tags
# article.tags.create(name='python') # Create and add
#
# # Remove tags
# article.tags.remove(tag)           # Remove single tag
# article.tags.clear()               # Remove all tags
#
# # Query
# tags = article.tags.all()          # All tags for article
# articles = tag.articles.all()      # All articles with tag
#
# # Filter
# Tag.objects.filter(articles__title='Django Tips')
# Article.objects.filter(tags__name='django')

# ---------------------------------------------------------------------------
# 4. Through Model (Custom M2M)
# ---------------------------------------------------------------------------
# For extra data on the relationship, use a through model.

class ArticleTag(models.Model):
    """Custom through model for Article-Tag relationship."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('article', 'tag')  # Prevent duplicates
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.article} - {self.tag}'

# Update Article model:
# class Article(models.Model):
#     ...
#     tags = models.ManyToManyField(
#         Tag,
#         through='ArticleTag',
#         related_name='articles',
#     )

# Usage with through model:
# ArticleTag.objects.create(article=article, tag=tag, added_by=user)
# article_tags = ArticleTag.objects.filter(article=article)

# ---------------------------------------------------------------------------
# 5. Querying Related Objects
# ---------------------------------------------------------------------------

# --- Forward lookup (ForeignKey → related object) ---
# post = Post.objects.get(pk=1)
# author = post.author               # Get author object
# author_name = post.author.name     # Access author attribute

# --- Reverse lookup (related_name → queryset) ---
# author = Author.objects.get(pk=1)
# posts = author.posts.all()         # All posts by author
# post_count = author.posts.count()  # Count posts
# latest = author.posts.latest('created_at')  # Latest post

# --- Filter across relationships ---
# Posts by specific author
# Post.objects.filter(author__name='John')
# Post.objects.filter(author__username='john')

# Authors with most posts
# Author.objects.annotate(post_count=Count('posts')).order_by('-post_count')

# --- Select related (optimize FK queries) ---
# posts = Post.objects.select_related('author').all()
# for post in posts:
#     print(post.author.name)  # No extra query!

# --- Prefetch related (optimize M2M/reverse FK) ---
# articles = Article.objects.prefetch_related('tags').all()
# for article in articles:
#     print(article.tags.all())  # No extra query!

# ---------------------------------------------------------------------------
# 6. Reverse Relationships
# ---------------------------------------------------------------------------
# How to access related objects from the "one" side.

# Model with related_name:
# author = models.ForeignKey(Author, related_name='posts')
#
# Access:
# author.posts.all()              # All posts
# author.posts.filter(title='...') # Filter posts
# author.posts.count()            # Count posts
# author.posts.exists()           # Boolean check

# Without related_name (default: <model>_set):
# author.post_set.all()           # All posts

# ---------------------------------------------------------------------------
# 7. Deleting Related Objects
# ---------------------------------------------------------------------------
# on_delete behavior when parent is deleted:

# CASCADE: Delete all children
#   Author.objects.get(pk=1).delete()
#   → All posts by author are deleted

# PROTECT: Prevent deletion
#   Author.objects.get(pk=1).delete()
#   → Raises ProtectedError if posts exist

# SET_NULL: Set FK to NULL
#   Author.objects.get(pk=1).delete()
#   → All posts have author=None (requires null=True)

# SET_DEFAULT: Set FK to default
#   Author.objects.get(pk=1).delete()
#   → All posts have author=default_author (requires default)

# DO_NOTHING: Don't do anything
#   → Can cause IntegrityError

# ---------------------------------------------------------------------------
# 8. Self-Referential Relationships
# ---------------------------------------------------------------------------
# A model can relate to itself (e.g., tree structures).

class Category(models.Model):
    """Category with parent-child hierarchy."""
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    def __str__(self):
        return self.name

    @property
    def is_root(self):
        return self.parent is None

    @property
    def depth(self):
        """Count ancestors."""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

# Usage:
# root = Category.objects.create(name='Technology')
# child = Category.objects.create(name='Programming', parent=root)
# grandchild = Category.objects.create(name='Python', parent=child)
#
# root.children.all()      # [Programming]
# child.children.all()     # [Python]
# grandchild.parent        # Programming

# ---------------------------------------------------------------------------
# 9. Related Managers
# ---------------------------------------------------------------------------
# Each relationship creates a manager for querying related objects.

# ForeignKey creates:
#   author.posts.all()
#   author.posts.filter(...)
#   author.posts.create(...)
#   author.posts.get_or_create(...)
#   author.posts.add(post1, post2)
#   author.posts.remove(post1)
#   author.posts.clear()
#   author.posts.set([post1, post2])

# ManyToMany creates:
#   article.tags.all()
#   article.tags.add(tag1, tag2)
#   article.tags.remove(tag)
#   article.tags.clear()
#   article.tags.set([tag1, tag2])
#   article.tags.create(name='new-tag')

# ---------------------------------------------------------------------------
# 10. Relationship Best Practices
# ---------------------------------------------------------------------------
# 1. Always set on_delete explicitly (required in Django 2.0+)
# 2. Use related_name for reverse lookups (cleaner code)
# 3. Use select_related() for ForeignKey (reduces queries)
# 4. Use prefetch_related() for ManyToMany (reduces queries)
# 5. Use through models for extra relationship data
# 6. Index ForeignKey fields for better query performance
# 7. Consider CASCADE carefully - data loss can be permanent
# 8. Use PROTECT for critical relationships (don't allow deletion)
# 9. Use SET_NULL for optional relationships (null=True)
# 10. Test relationship queries for N+1 query problems
