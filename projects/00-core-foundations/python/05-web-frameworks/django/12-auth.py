# =============================================================================
# Django Authentication - Reference Guide
# =============================================================================
# Django provides a complete authentication system out of the box.
# Handles user registration, login, logout, permissions, and groups.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_authentication.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Authentication System Overview
# ---------------------------------------------------------------------------
# Django's auth system includes:
#   - User model (username, password, email, first_name, last_name)
#   - Login/logout views
#   - Password hashing and validation
#   - Session management
#   - Permissions and groups
#   - Decorators for view protection
#   - Forms for user management

# Built-in auth apps in INSTALLED_APPS:
#   django.contrib.auth
#   django.contrib.contenttypes

# Built-in middleware:
#   django.contrib.auth.middleware.AuthenticationMiddleware
#   django.contrib.messages.middleware.MessageMiddleware

# ---------------------------------------------------------------------------
# 2. User Model
# ---------------------------------------------------------------------------
# The default User model has these fields:
#   username, password, email, first_name, last_name, is_active,
#   is_staff, is_superuser, date_joined, last_login

# Creating a user:
# from django.contrib.auth.models import User
#
# # Create a regular user
# user = User.objects.create_user(
#     username='john',
#     email='john@example.com',
#     password='securepass123'
# )
#
# # Create a superuser (admin access)
# user = User.objects.create_superuser(
#     username='admin',
#     email='admin@example.com',
#     password='adminpass123'
# )
#
# # Change password
# user.set_password('newpass123')
# user.save()
#
# # Check password
# user.check_password('newpass123')  # True or False

# ---------------------------------------------------------------------------
# 3. Login/Logout Views
# ---------------------------------------------------------------------------

# --- Using built-in views ---
# urls.py:
# from django.contrib.auth import views as auth_views
#
# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(
#         template_name='accounts/login.html'
#     ), name='login'),
#
#     path('logout/', auth_views.LogoutView.as_view(
#         next_page='home'
#     ), name='logout'),
#
#     # Password management
#     path('password-change/', auth_views.PasswordChangeView.as_view(
#         template_name='accounts/password_change.html'
#     ), name='password_change'),
#
#     path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
#         template_name='accounts/password_change_done.html'
#     ), name='password_change_done'),
#
#     # Password reset
#     path('password-reset/', auth_views.PasswordResetView.as_view(
#         template_name='accounts/password_reset.html'
#     ), name='password_reset'),
#
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='accounts/password_reset_done.html'
#     ), name='password_reset_done'),
#
#     path('password-reset-confirm/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='accounts/password_reset_confirm.html'
#          ), name='password_reset_confirm'),
#
#     path('password-reset-complete/',
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='accounts/password_reset_complete.html'
#          ), name='password_reset_complete'),
# ]

# settings.py:
# LOGIN_REDIRECT_URL = '/dashboard/'   # Where to go after login
# LOGOUT_REDIRECT_URL = '/'            # Where to go after logout
# LOGIN_URL = '/accounts/login/'       # Login URL for @login_required

# ---------------------------------------------------------------------------
# 4. Custom Login View
# ---------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def custom_login(request):
    """Custom login view with form handling."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def custom_logout(request):
    """Custom logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# ---------------------------------------------------------------------------
# 5. Registration View
# ---------------------------------------------------------------------------
from django.contrib.auth.forms import UserCreationForm


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Custom registration form:
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user

# ---------------------------------------------------------------------------
# 6. Protecting Views
# ---------------------------------------------------------------------------
# Use decorators and mixins to require authentication.

# --- Function-based views ---
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Only accessible to logged-in users."""
    return render(request, 'dashboard.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    """Custom login URL."""
    return render(request, 'profile.html')

# --- Class-based views ---
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'dashboard.html'
#     login_url = '/accounts/login/'

# --- Require specific permissions ---
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('blog.add_post', raise_exception=True)
def create_post(request):
    """Only users with 'add_post' permission can access."""
    return render(request, 'blog/post_form.html')

# From class-based views:
# from django.contrib.auth.mixins import PermissionRequiredMixin
#
# class PostCreateView(PermissionRequiredMixin, CreateView):
#     permission_required = 'blog.add_post'
#     raise_exception = True  # Return 403 instead of redirect to login

# ---------------------------------------------------------------------------
# 7. User Object in Templates
# ---------------------------------------------------------------------------
# The request.user object is available in every template.

# In templates:
# {% if user.is_authenticated %}
#     <p>Welcome, {{ user.username }}!</p>
#     <p>Email: {{ user.email }}</p>
#     <a href="{% url 'logout' %}">Logout</a>
# {% else %}
#     <a href="{% url 'login' %}">Login</a>
#     <a href="{% url 'register' %}">Register</a>
# {% endif %}
#
# User methods available:
#   user.is_authenticated   → True if logged in
#   user.is_anonymous       → True if not logged in
#   user.is_staff           → True if admin access
#   user.is_superuser       → True if superuser
#   user.has_perm('app.permission') → Check single permission
#   user.has_perms(['app.perm1', 'app.perm2']) → Check multiple
#   user.get_full_name()    → "John Doe"
#   user.get_short_name()   → "John"

# ---------------------------------------------------------------------------
# 8. Permissions and Groups
# ---------------------------------------------------------------------------
# Django has a built-in permission system.

# --- Creating permissions ---
# class Post(models.Model):
#     ...
#     class Meta:
#         permissions = [
#             ('can_publish', 'Can publish posts'),
#             ('can_feature', 'Can feature posts'),
#         ]

# --- Using permissions in views ---
# Check permission:
# user.has_perm('blog.can_publish')
#
# Get all permissions:
# user.get_all_permissions()
# # {'blog.add_post', 'blog.change_post', 'blog.can_publish', ...}
#
# Get permissions for a specific app:
# user.get_all_permissions()  # or filter by app

# --- Groups ---
# from django.contrib.auth.models import Group
#
# # Create groups
# editors_group = Group.objects.create(name='Editors')
# authors_group = Group.objects.create(name='Authors')
#
# # Add permissions to groups
# from django.contrib.auth.models import Permission
# can_publish = Permission.objects.get(codename='can_publish')
# editors_group.permissions.add(can_publish)
#
# # Add users to groups
# user.groups.add(editors_group)
#
# # Check group membership
# user.groups.filter(name='Editors').exists()

# --- Using groups in views ---
# def publish_post(request):
#     if request.user.groups.filter(name='Editors').exists():
#         # Allow publishing
#         pass
#     else:
#         # Deny access
#         pass

# ---------------------------------------------------------------------------
# 9. Custom User Model
# ---------------------------------------------------------------------------
# For extending the User model, create a custom one BEFORE first migration.

# accounts/models.py:
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# class CustomUser(AbstractUser):
#     """Extended user model with additional fields."""
#     bio = models.TextField(max_length=500, blank=True)
#     avatar = models.ImageField(upload_to='avatars/', blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#
#     def __str__(self):
#         return self.username

# settings.py:
# AUTH_USER_MODEL = 'accounts.CustomUser'

# IMPORTANT: Set this BEFORE running any migrations!

# ---------------------------------------------------------------------------
# 10. Authentication Best Practices
# ---------------------------------------------------------------------------
# 1. Always use @login_required for protected views
# 2. Use HTTPS in production (set SECURE_SSL_REDIRECT)
# 3. Never store passwords in plain text (Django hashes automatically)
# 4. Use PASSWORD_HASHERS for custom hashing algorithms
# 5. Set SESSION_COOKIE_SECURE = True in production
# 6. Use django-axes for brute-force protection
# 7. Implement rate limiting on login forms
# 8. Add email verification for registration
# 9. Use custom user model from the start (can't change later)
# 10. Keep password requirements strong (min length, complexity)
