# =============================================================================
# Django Migrations - Reference Guide
# =============================================================================
# Migrations track changes to your models and propagate them to the database.
# They version-control your database schema.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_migrations.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What are Migrations?
# ---------------------------------------------------------------------------
# Migrations are Django's way of propagating changes you make to your models
# into your database schema.
#
# Model changes → Migration file → Database schema update
#
# Think of migrations as version control for your database.

# ---------------------------------------------------------------------------
# 2. Creating Migrations
# ---------------------------------------------------------------------------
# After changing models.py, create a migration:

# Command:
#   python manage.py makemigrations
#
# What happens:
#   1. Django inspects all models
#   2. Compares them to the last migration
#   3. Generates a migration file for changes
#
# Example output:
#   Migrations for 'blog':
#     blog/migrations/0002_post_slug_alter_post_title.py
#       - Add field slug to post
#       - Alter field title on post

# Name your migrations:
#   python manage.py makemigrations --name add_slug_field

# Check what migrations exist:
#   python manage.py showmigrations

# ---------------------------------------------------------------------------
# 3. Applying Migrations
# ---------------------------------------------------------------------------
# Apply pending migrations to the database:

# Command:
#   python manage.py migrate
#
# What happens:
#   1. Checks for unapplied migrations
#   2. Executes SQL to update database
#   3. Updates django_migrations table

# Apply specific app:
#   python manage.py migrate blog

# Apply to specific migration:
#   python manage.py migrate blog 0003

# Fake a migration (mark as applied without running SQL):
#   python manage.py migrate blog 0003 --fake

# ---------------------------------------------------------------------------
# 4. Migration File Structure
# ---------------------------------------------------------------------------
# Migration files live in each app's migrations/ directory.

# blog/migrations/0001_initial.py:
# from django.db import migrations, models
# import django.db.models.deletion
#
# class Migration(migrations.Migration):
#     initial = True
#
#     dependencies = [
#         ('auth', '0012_alter_user_first_name_max_length'),  # Other migrations
#     ]
#
#     operations = [
#         migrations.CreateModel(
#             name='Post',
#             fields=[
#                 ('id', models.BigAutoField(auto_created=True, primary_key=True)),
#                 ('title', models.CharField(max_length=200)),
#                 ('content', models.TextField()),
#                 ('created_at', models.DateTimeField(auto_now_add=True)),
#                 ('updated_at', models.DateTimeField(auto_now=True)),
#             ],
#             options={
#                 'ordering': ['-created_at'],
#             },
#         ),
#         migrations.CreateModel(
#             name='Category',
#             fields=[
#                 ('id', models.BigAutoField(auto_created=True, primary_key=True)),
#                 ('name', models.CharField(max_length=100, unique=True)),
#             ],
#         ),
#         migrations.AddField(
#             model_name='post',
#             name='category',
#             field=models.ForeignKey(
#                 null=True,
#                 blank=True,
#                 on_delete=django.db.models.deletion.SET_NULL,
#                 to='blog.category',
#             ),
#         ),
#     ]

# ---------------------------------------------------------------------------
# 5. Migration Operations
# ---------------------------------------------------------------------------
# Common operations in migration files:

# --- Create a model ---
# migrations.CreateModel(
#     name='Post',
#     fields=[
#         ('id', models.BigAutoField(primary_key=True)),
#         ('title', models.CharField(max_length=200)),
#     ],
# )

# --- Add a field ---
# migrations.AddField(
#     model_name='post',
#     name='slug',
#     field=models.SlugField(max_length=200, null=True),
# )

# --- Remove a field ---
# migrations.RemoveField(
#     model_name='post',
#     name='legacy_field',
# )

# --- Alter a field ---
# migrations.AlterField(
#     model_name='post',
#     name='title',
#     field=models.CharField(max_length=300),  # Changed max_length
# )

# --- Rename a field ---
# migrations.RenameField(
#     model_name='post',
#     old_name='content',
#     new_name='body',
# )

# --- Rename a model ---
# migrations.RenameModel(
#     old_name='BlogPost',
#     new_name='Post',
# )

# --- Run custom data migration ---
# migrations.RunPython(forwards_func, reverse_func),

# --- Add an index ---
# migrations.AddIndex(
#     model_name='post',
#     index=models.Index(fields=['-created_at']),
# )

# --- Add a unique constraint ---
# migrations.AddConstraint(
#     model_name='post',
#     constraint=models.UniqueConstraint(fields=['title', 'author']),
# )

# ---------------------------------------------------------------------------
# 6. Data Migrations
# ---------------------------------------------------------------------------
# When you need to transform data, not just schema.

# Create a data migration:
#   python manage.py makemigrations --empty blog -n populate_slugs

# Then edit the migration file:
# from django.db import migrations
# from django.utils.text import slugify
#
# def populate_slugs(apps, schema_editor):
#     """Populate slug field from title for existing posts."""
#     Post = apps.get_model('blog', 'Post')
#     for post in Post.objects.all():
#         post.slug = slugify(post.title)
#         post.save()
#
# def reverse_func(apps, schema_editor):
#     """Reverse data migration (optional)."""
#     pass
#
# class Migration(migrations.Migration):
#     dependencies = [
#         ('blog', '0001_initial'),
#     ]
#
#     operations = [
#         migrations.RunPython(populate_slugs, reverse_func),
#     ]

# ---------------------------------------------------------------------------
# 7. Migration History
# ---------------------------------------------------------------------------
# Django tracks applied migrations in the django_migrations table.

# List all migrations and their status:
#   python manage.py showmigrations

# Output:
#   blog
#     X 0001_initial
#     X 0002_post_slug
#     X 0003_auto_20260101
#   accounts
#     X 0001_initial

# Show SQL for a migration:
#   python manage.py sqlmigrate blog 0001

# ---------------------------------------------------------------------------
# 8. Rollback Migrations
# ---------------------------------------------------------------------------
# To undo migrations:

# Roll back to a specific migration:
#   python manage.py migrate blog 0002
#   (This rolls back 0003 and later)

# Roll back all migrations for an app:
#   python manage.py migrate blog zero

# ---------------------------------------------------------------------------
# 9. Squashing Migrations
# ---------------------------------------------------------------------------
# When you have too many migrations, squash them into one.

# Command:
#   python manage.py squashmigrations blog 0001 0005
#
# This creates a single migration file combining 0001-0005.

# After squashing:
#   1. Test the squashed migration works
#   2. Remove old migration files
#   3. Deploy the squashed migration

# ---------------------------------------------------------------------------
# 10. Migration Best Practices
# ---------------------------------------------------------------------------
# 1. Create migrations immediately after model changes
# 2. Never edit applied migration files directly
# 3. Use descriptive names: makemigrations --name add_user_profile
# 4. Test migrations before deploying
# 5. Use RunPython for data migrations (not raw SQL)
# 6. Keep migrations small and focused
# 7. Squash migrations periodically for performance
# 8. Always backup before running migrations in production
# 9. Use --plan to preview migrations before running
# 10. Don't delete migrations you haven't applied yet

# Common workflow:
#   1. Edit models.py
#   2. python manage.py makemigrations
#   3. python manage.py migrate
#   4. python manage.py test  (verify nothing broke)
#   5. git add . && git commit
