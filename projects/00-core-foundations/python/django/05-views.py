# =============================================================================
# Django Views - Reference Guide
# =============================================================================
# Views are the heart of Django's request/response cycle. They receive an
# HTTP request and return an HTTP response.
#
# W3Schools Django Tutorial: https://www.w3schools.com/django/django_views.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Function-Based Views (FBVs)
# ---------------------------------------------------------------------------
# The simplest way to create a view - a Python function that takes a
# request and returns a response.

# blog/views.py:
# from django.http import HttpResponse
#
# def home(request):
#     return HttpResponse("<h1>Welcome to My Blog</h1>")

# ---------------------------------------------------------------------------
# 2. Returning Different Response Types
# ---------------------------------------------------------------------------

# --- HttpResponse (raw content) ---
# from django.http import HttpResponse
#
# def simple_view(request):
#     return HttpResponse("Hello, World!")             # Plain text
#     return HttpResponse("<h1>HTML</h1>")            # HTML
#     return HttpResponse("text", content_type="text/plain")  # Plain text
#     return HttpResponse(b"\x89PNG", content_type="image/png")  # Binary

# --- JsonResponse (API responses) ---
# from django.http import JsonResponse
#
# def api_view(request):
#     data = {
#         'name': 'John',
#         'age': 30,
#         'hobbies': ['reading', 'coding'],
#     }
#     return JsonResponse(data)
#
#     # For lists (non-dict data), set safe=False
#     items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
#     return JsonResponse(items, safe=False)

# --- HttpResponseRedirect (redirects) ---
# from django.http import HttpResponseRedirect
#
# def redirect_view(request):
#     return HttpResponseRedirect('/blog/')
#     return HttpResponseRedirect('https://example.com')

# --- TemplateResponse (rendering templates) ---
# from django.template.response import TemplateResponse
#
# def template_view(request):
#     context = {'title': 'Hello', 'items': [1, 2, 3]}
#     return TemplateResponse(request, 'blog/template.html', context)

# ---------------------------------------------------------------------------
# 3. Template Rendering
# ---------------------------------------------------------------------------
# The most common pattern - render a template with context data.

# blog/views.py:
from django.shortcuts import render

def post_list(request):
    """Render a list of blog posts."""
    # In a real app, you'd query the database here
    context = {
        'title': 'My Blog',
        'posts': [
            {'id': 1, 'title': 'First Post', 'content': 'Hello!'},
            {'id': 2, 'title': 'Second Post', 'content': 'Django is great!'},
        ]
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    """Render a single blog post."""
    context = {
        'post': {
            'id': pk,
            'title': f'Post {pk}',
            'content': f'This is the content of post {pk}',
            'author': 'John Doe',
        }
    }
    return render(request, 'blog/post_detail.html', context)

# ---------------------------------------------------------------------------
# 4. Class-Based Views (CBVs)
# ---------------------------------------------------------------------------
# CBVs use classes instead of functions. They're more organized and
# support inheritance for code reuse.

# --- Simple CBV ---
# from django.views import View
# from django.shortcuts import render
# from django.http import JsonResponse
#
# class PostListView(View):
#     def get(self, request):
#         """Handle GET requests"""
#         posts = Post.objects.all()
#         return render(request, 'blog/post_list.html', {'posts': posts})
#
#     def post(self, request):
#         """Handle POST requests"""
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         Post.objects.create(title=title, content=content)
#         return HttpResponseRedirect('/blog/')

# --- URL config for CBVs ---
# from django.urls import path
# from .views import PostListView
#
# urlpatterns = [
#     path('', PostListView.as_view(), name='post_list'),
# ]

# ---------------------------------------------------------------------------
# 5. Common Class-Based Views (Django's Generic Views)
# ---------------------------------------------------------------------------

# Django provides pre-built CBVs for common patterns:

# --- ListView - display a list of objects ---
# from django.views.generic import ListView
# from .models import Post
#
# class PostListView(ListView):
#     model = Post                          # Which model
#     template_name = 'blog/post_list.html' # Template to render
#     context_object_name = 'posts'         # Variable name in template
#     paginate_by = 10                      # Pagination
#     ordering = ['-created_at']            # Sort order

# --- DetailView - display a single object ---
# from django.views.generic import DetailView
# from .models import Post
#
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'

# --- CreateView - create a new object ---
# from django.views.generic import CreateView
# from .models import Post
# from .forms import PostForm
#
# class PostCreateView(CreateView):
#     model = Post
#     template_name = 'blog/post_form.html'
#     form_class = PostForm
#     success_url = '/blog/'

# --- UpdateView - update an existing object ---
# from django.views.generic import UpdateView
# from .models import Post
# from .forms import PostForm
#
# class PostUpdateView(UpdateView):
#     model = Post
#     template_name = 'blog/post_form.html'
#     form_class = PostForm
#     success_url = '/blog/'

# --- DeleteView - delete an object ---
# from django.views.generic import DeleteView
# from .models import Post
#
# class PostDeleteView(DeleteView):
#     model = Post
#     template_name = 'blog/post_confirm_delete.html'
#     success_url = '/blog/'

# ---------------------------------------------------------------------------
# 6. Handling Request Data
# ---------------------------------------------------------------------------

# --- GET parameters ---
def search_view(request):
    """Access query parameters: /search/?q=django"""
    query = request.GET.get('q', '')  # Get 'q' parameter, default ''
    page = request.GET.get('page', 1)
    context = {
        'query': query,
        'page': page,
    }
    return render(request, 'blog/search_results.html', context)

# --- POST data ---
def post_create(request):
    """Handle form submissions"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        # Process the data...
        return HttpResponseRedirect('/blog/')
    else:
        # GET request - show form
        return render(request, 'blog/post_form.html')

# --- Request metadata ---
def debug_view(request):
    """Access request metadata"""
    info = {
        'method': request.method,           # 'GET', 'POST', etc.
        'path': request.path,               # '/blog/'
        'user': request.user,               # Current user object
        'META': request.META,               # All headers and metadata
        'session': request.session,         # Session data
    }
    return JsonResponse(info)

# ---------------------------------------------------------------------------
# 7. View Decorators
# ---------------------------------------------------------------------------
# Decorators modify view behavior.

# --- Require HTTP methods ---
# from django.views.decorators.http import require_http_methods
#
# @require_http_methods(["GET", "POST"])
# def my_view(request):
#     ...

# --- Require safe methods (GET, HEAD, OPTIONS) ---
# from django.views.decorators.http import require_safe
#
# @require_safe
# def safe_view(request):
#     ...  # Only GET, HEAD, OPTIONS allowed

# --- Login required ---
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def protected_view(request):
#     ...  # Only logged-in users
#
# @login_required(login_url='/accounts/login/')
# def protected_view_2(request):
#     ...

# --- Cache control ---
# from django.views.decorators.cache import cache_page
#
# @cache_page(60 * 15)  # Cache for 15 minutes
# def cached_view(request):
#     ...  # Response is cached

# ---------------------------------------------------------------------------
# 8. Sending Email
# ---------------------------------------------------------------------------
# Django has built-in email support.

# from django.core.mail import send_mail
#
# def send_welcome_email(request):
#     send_mail(
#         subject='Welcome!',
#         message='Thanks for signing up.',
#         from_email='noreply@example.com',
#         recipient_list=['user@example.com'],
#         fail_silently=False,
#     )
#     return HttpResponse("Email sent!")

# ---------------------------------------------------------------------------
# 9. File Uploads
# ---------------------------------------------------------------------------
# Handle file uploads in views.

# def upload_file(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES.get('file')
#         if uploaded_file:
#             # uploaded_file is a Django UploadedFile object
#             # Save it somewhere
#             with open(f'uploads/{uploaded_file.name}', 'wb+') as f:
#                 for chunk in uploaded_file.chunks():
#                     f.write(chunk)
#             return HttpResponse("File uploaded!")
#     return render(request, 'upload.html')

# ---------------------------------------------------------------------------
# 10. FBV vs CBV Comparison
# ---------------------------------------------------------------------------
# Function-Based Views:          Class-Based Views:
# ✅ Simple and explicit          ✅ Code reuse via inheritance
# ✅ Easy to understand           ✅ Built-in generic views
# ✅ No boilerplate               ✅ Consistent patterns
# ✅ Great for simple views       ✅ Method dispatching
# ❌ No code reuse (without       ❌ More complex for simple views
#    wrappers)                    ❌ Can be harder to follow
#
# Rule of thumb:
# - Use FBVs for simple views (< 50 lines)
# - Use CBVs for CRUD operations and complex views
# - Use Generic CBVs for standard database operations
