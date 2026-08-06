# =============================================================================
# Django Generic Views - Reference Guide
# =============================================================================
# Generic views provide pre-built views for common patterns like
# CRUD operations, list/detail views, and form handling.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_generics.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What are Generic Views?
# ---------------------------------------------------------------------------
# Generic views are class-based views that handle common use cases:
#   - Displaying lists of objects
#   - Displaying single objects
#   - Creating/editing/deleting objects
#   - Handling date-based archives
#
# They reduce boilerplate code significantly.

# ---------------------------------------------------------------------------
# 2. ListView - Display a List of Objects
# ---------------------------------------------------------------------------

from django.views.generic import ListView
from django.db.models import Q


class PostListView(ListView):
    """Display a paginated list of published posts."""
    model = Post  # Replace with your actual model
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    # Filter queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status='published')

        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        return queryset

    # Add extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['total_posts'] = self.get_queryset().count()
        return context

# URL config:
# urlpatterns = [
#     path('', PostListView.as_view(), name='post_list'),
# ]

# ---------------------------------------------------------------------------
# 3. DetailView - Display a Single Object
# ---------------------------------------------------------------------------

from django.views.generic import DetailView


class PostDetailView(DetailView):
    """Display a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'  # URL parameter name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:5]
        return context

# URL config:
# urlpatterns = [
#     path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
# ]

# ---------------------------------------------------------------------------
# 4. CreateView - Create New Objects
# ---------------------------------------------------------------------------

from django.views.generic import CreateView
from django.urls import reverse_lazy


class PostCreateView(CreateView):
    """Create a new blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'category', 'status']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """Set the author to the current user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

# URL config:
# urlpatterns = [
#     path('post/new/', PostCreateView.as_view(), name='post_create'),
# ]

# ---------------------------------------------------------------------------
# 5. UpdateView - Update Existing Objects
# ---------------------------------------------------------------------------

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing blog post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'category', 'status']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        """Only allow the author to edit."""
        if form.instance.author != self.request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You can't edit this post.")
        return super().form_valid(form)

# URL config:
# urlpatterns = [
#     path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
# ]

# ---------------------------------------------------------------------------
# 6. DeleteView - Delete Objects
# ---------------------------------------------------------------------------

from django.views.generic import DeleteView


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def delete(self, request, *args, **kwargs):
        """Only allow the author to delete."""
        self.object = self.get_object()
        if self.object.author != request.user:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You can't delete this post.")
        return super().delete(request, *args, **kwargs)

# URL config:
# urlpatterns = [
#     path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
# ]

# ---------------------------------------------------------------------------
# 7. YearArchiveView - Date-Based Views
# ---------------------------------------------------------------------------

from django.views.generic import YearArchiveView, MonthArchiveView


class PostYearArchiveView(YearArchiveView):
    """Display posts for a specific year."""
    model = Post
    template_name = 'blog/archive/year.html'
    date_field = 'published_at'
    make_object_list = True
    allow_future = False

class PostMonthArchiveView(MonthArchiveView):
    """Display posts for a specific month."""
    model = Post
    template_name = 'blog/archive/month.html'
    date_field = 'published_at'
    month_format = '%m'

# URL config:
# urlpatterns = [
#     path('archive/<int:year>/',
#          PostYearArchiveView.as_view(), name='post_year_archive'),
#     path('archive/<int:year>/<str:month>/',
#          PostMonthArchiveView.as_view(), name='post_month_archive'),
# ]

# ---------------------------------------------------------------------------
# 8. TemplateView - Static Pages
# ---------------------------------------------------------------------------

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Render a simple template."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(
            is_featured=True, status='published'
        )[:5]
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

# URL config:
# urlpatterns = [
#     path('', HomePageView.as_view(), name='home'),
#     path('about/', AboutView.as_view(), name='about'),
# ]

# ---------------------------------------------------------------------------
# 9. RedirectView - Redirect to Another URL
# ---------------------------------------------------------------------------

from django.views.generic import RedirectView


class PostRedirectView(RedirectView):
    """Redirect to latest post."""
    permanent = False  # Use 302, not 301
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.filter(status='published').first()
        if post:
            return post.get_absolute_url()
        return '/blog/'

# URL config:
# urlpatterns = [
#     path('latest/', PostRedirectView.as_view(), name='latest_post'),
# ]

# ---------------------------------------------------------------------------
# 10. Custom Generic Views
# ---------------------------------------------------------------------------
# Combine multiple generic views or create custom ones.

from django.views.generic import ListView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm


class PostDetailViewWithComments(LoginRequiredMixin, DetailView, FormMixin):
    """DetailView with a comment form."""
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        """Save the comment."""
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        from django.contrib import messages
        messages.success(self.request, 'Comment added!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context

# ---------------------------------------------------------------------------
# 11. Generic Views Reference Table
# ---------------------------------------------------------------------------
# GenericView     Purpose               Key Attributes
# --------------- --------------------- -----------------------------------
# ListView        List objects          model, queryset, paginate_by
# DetailView      Single object         model, slug_url_kwarg
# CreateView      Create object         model, fields, form_class
# UpdateView      Update object         model, fields, form_class
# DeleteView      Delete object         model, template_name
# TemplateView    Static page           template_name, get_context_data
# RedirectView    Redirect              url, permanent
# YearArchiveView Year archive           date_field, make_object_list
# MonthArchiveView Month archive         date_field, month_format

# ---------------------------------------------------------------------------
# 12. Generic Views Best Practices
# ---------------------------------------------------------------------------
# 1. Use generic views for standard CRUD operations
# 2. Customize via get_queryset(), get_context_data(), form_valid()
# 3. Combine mixins for additional functionality (LoginRequiredMixin)
# 4. Use reverse_lazy for success_url (not reverse)
# 5. Set context_object_name for cleaner template variable names
# 6. Use template_name with app namespace: 'blog/post_list.html'
# 7. Keep views thin - put business logic in models/services
# 8. Test each generic view independently
# 9. Override get_object() for custom object retrieval
# 10. Use FormMixin for forms in DetailView
