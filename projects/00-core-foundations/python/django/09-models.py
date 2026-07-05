# =============================================================================
# Django Models - Reference Guide
# =============================================================================
# Models define your database structure. Each model maps to a database table.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_models.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What are Models?
# ---------------------------------------------------------------------------
# Models are Python classes that define the structure of your database.
# Django's ORM (Object-Relational Mapper) translates models to SQL tables.
#
# You write Python, Django handles SQL.

# ---------------------------------------------------------------------------
# 2. Creating a Model
# ---------------------------------------------------------------------------

# blog/models.py:
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Blog post category."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='published_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def publish(self):
        """Publish this post."""
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()

    @property
    def is_published(self):
        return self.status == 'published'


class Tag(models.Model):
    """Tag for blog posts."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Comment on a blog post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


# ---------------------------------------------------------------------------
# 3. Field Types
# ---------------------------------------------------------------------------
# Django provides many field types for different data:

# Text fields:
# models.CharField(max_length=255)       # Short text (indexed, fast)
# models.TextField()                      # Long text (no length limit)
# models.SlugField(max_length=50)         # URL-safe slug (letters, numbers, -)
# models.EmailField()                     # Email validation
# models.URLField()                       # URL validation
# models.UUIDField()                      # UUID (primary_key=True for UUID PK)

# Number fields:
# models.IntegerField()                   # Integer
# models.PositiveIntegerField()           # Positive integer only
# models.SmallIntegerField()              # -32768 to 32767
# models.BigIntegerField()                # Very large integers
# models.FloatField()                     # Floating point
# models.DecimalField(max_digits=10, decimal_places=2)  # Exact decimal
# models.AutoField(primary_key=True)      # Auto-incrementing integer

# Date/Time fields:
# models.DateField()                      # Date only
# models.TimeField()                      # Time only
# models.DateTimeField()                  # Date and time
# models.DateTimeField(auto_now=True)     # Auto-set on save
# models.DateTimeField(auto_now_add=True) # Auto-set on creation

# Boolean:
# models.BooleanField(default=False)      # True/False

# File/Image:
# models.FileField(upload_to='files/')    # File upload
# models.ImageField(upload_to='images/')  # Image with validation

# Relationship fields:
# models.ForeignKey(User, on_delete=models.CASCADE)           # Many-to-one
# models.ManyToManyField('Tag', blank=True)                   # Many-to-many
# models.OneToOneField(User, on_delete=models.CASCADE)        # One-to-one

# Other:
# models.JSONField(default=dict)          # JSON data (Django 3.1+)
# models.IPAddressField()                 # IP address
# models.BinaryField()                    # Binary data

# ---------------------------------------------------------------------------
# 4. Field Options
# ---------------------------------------------------------------------------
# Common options for model fields:

# models.CharField(
#     max_length=100,               # Required for CharField
#     unique=True,                  # No duplicate values
#     blank=False,                  # Form validation (empty allowed?)
#     null=True,                    # Database NULL (use for non-string fields)
#     default='value',              # Default value
#     verbose_name='Human Name',    # Human-readable name (for admin)
#     help_text='Help text',        # Help text (for forms)
#     db_index=True,                # Create database index
#     editable=True,                # Show in admin forms
#     validators=[my_validator],    # Custom validators
# )

# null vs blank:
#   null=True    → Database allows NULL
#   blank=True   → Form validation allows empty
#   For strings: use blank=True (Django stores '' not NULL)
#   For non-strings: use null=True, blank=True

# ---------------------------------------------------------------------------
# 5. Model Meta Options
# ---------------------------------------------------------------------------

class Meta:
    """Options that control model behavior."""
    # Display
    verbose_name = 'blog post'               # Singular name (admin)
    verbose_name_plural = 'blog posts'       # Plural name (admin)

    # Ordering
    ordering = ['-created_at', 'title']      # Default sort order

    # Database
    db_table = 'blog_posts'                  # Custom table name
    indexes = [                              # Database indexes
        models.Index(fields=['title']),
        models.Index(fields=['-created_at'], name='idx_created'),
    ]
    unique_together = [['title', 'author']]  # Unique constraint

    # Permissions
    permissions = [
        ('can_publish', 'Can publish posts'),
        ('can_feature', 'Can feature posts'),
    ]

    # Other
    abstract = True          # Don't create table (base class only)
    managed = True           # Let Django manage migrations
    app_label = 'blog'       # Override app label

# ---------------------------------------------------------------------------
# 6. Model Methods
# ---------------------------------------------------------------------------

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation
    def __str__(self):
        return self.title

    # Custom methods
    def publish(self):
        self.published = True
        self.save()

    @property
    def word_count(self):
        """Count words in content."""
        return len(self.content.split())

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        return max(1, round(self.word_count / 200))

    # Class methods (query shortcuts)
    @classmethod
    def published_articles(cls):
        """Get all published articles."""
        return cls.objects.filter(published=True)

    @classmethod
    def recent(cls, days=7):
        """Get articles from the last N days."""
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return cls.objects.filter(created_at__gte=cutoff)

    # Static methods
    @staticmethod
    def calculate_reading_time(word_count):
        return max(1, round(word_count / 200))

# ---------------------------------------------------------------------------
# 7. Model Managers
# ---------------------------------------------------------------------------
# Managers provide QuerySet methods for models.

class PostManager(models.Manager):
    """Custom manager for Post model."""
    def published(self):
        return self.filter(status='published')

    def drafts(self):
        return self.filter(status='draft')

    def featured(self):
        return self.filter(is_featured=True, status='published')

    def by_author(self, author):
        return self.filter(author=author)

class Post(models.Model):
    # ... fields ...
    objects = PostManager()  # Default manager
    # Use: Post.objects.published()

# ---------------------------------------------------------------------------
# 8. Model Inheritance
# ---------------------------------------------------------------------------

# --- Abstract base class (no table created) ---
# class TimestampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True  # No table created
#
# class Post(TimestampedModel):
#     title = models.CharField(max_length=200)
#     # Inherits created_at and updated_at

# --- Multi-table inheritance (separate tables) ---
# class Place(models.Model):
#     name = models.CharField(max_length=100)
#
# class Restaurant(Place):
#     serves_pizza = models.BooleanField(default=False)
#     # Creates two tables: Place and Restaurant
#     # Restaurant has access to Place fields via place_ptr

# --- Proxy models (no new table, different behavior) ---
# class PublishedPost(Post):
#     objects = PublishedPostManager()
#
#     class Meta:
#         proxy = True  # No new table
#         ordering = ['-published_at']

# ---------------------------------------------------------------------------
# 9. Model Signals
# ---------------------------------------------------------------------------
# Signals let you run code when models are saved/deleted.

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=Post)
def auto_generate_slug(sender, instance, **kwargs):
    """Auto-generate slug before saving."""
    if not instance.slug:
        instance.slug = slugify(instance.title)

@receiver(post_save, sender=Post)
def notify_author_on_publish(sender, instance, created, **kwargs):
    """Notify author when post is published."""
    if instance.status == 'published':
        # Send notification logic here
        pass

# ---------------------------------------------------------------------------
# 10. Model Best Practices
# ---------------------------------------------------------------------------
# 1. Always define __str__ for readable representation
# 2. Use Meta.ordering for default sort order
# 3. Add indexes for frequently queried fields
# 4. Use related_name for reverse relationships
# 5. Use on_delete properly (CASCADE, PROTECT, SET_NULL)
# 6. Add auto_now/auto_now_add for timestamps
# 7. Use choices for fixed options (status, type, etc.)
# 8. Keep models thin - put business logic in services/managers
# 9. Use signals sparingly - prefer explicit function calls
# 10. Run makemigrations after every model change
