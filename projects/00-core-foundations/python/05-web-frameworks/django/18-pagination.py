# =============================================================================
# Django Pagination - Reference Guide
# =============================================================================
# Pagination splits large result sets into smaller pages.
# Django provides built-in pagination for both views and templates.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_pagination.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Basic Pagination
# ---------------------------------------------------------------------------

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    """Paginated list of posts."""
    post_list = Post.objects.filter(status='published').order_by('-created_at')

    # Create paginator
    paginator = Paginator(post_list, 10)  # 10 posts per page

    # Get page number from request
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})

# ---------------------------------------------------------------------------
# 2. Paginator Object
# ---------------------------------------------------------------------------
# The Paginator class handles splitting results into pages.

# paginator = Paginator(queryset, per_page)
#
# Attributes:
#   paginator.count          → Total number of objects
#   paginator.num_pages      → Total number of pages
#   paginator.page_range     → Range(1, num_pages + 1)
#   paginator.per_page       → Objects per page
#   paginator.orphans        → Minimum objects on last page
#
# Methods:
#   paginator.page(number)   → Returns a Page object
#   paginator.get_page(number)  → Returns Page or None (Django 2.0+)

# ---------------------------------------------------------------------------
# 3. Page Object
# ---------------------------------------------------------------------------
# The Page object represents a single page of results.

# page = paginator.page(1)
#
# Attributes:
#   page.object_list        → List of objects on this page
#   page.number             → Current page number (1-indexed)
#   page.paginator          → The Paginator instance
#
# Methods:
#   page.has_next()         → True if there's a next page
#   page.has_previous()     → True if there's a previous page
#   page.has_other_pages()  → True if there are other pages
#   page.next_page_number() → Next page number (raises EmptyPage if none)
#   page.previous_page_number()  → Previous page number

# ---------------------------------------------------------------------------
# 4. Simpler Pagination (get_page)
# ---------------------------------------------------------------------------
# Django 2.0+ provides get_page() which handles exceptions automatically.

def post_list_simple(request):
    """Simplified pagination using get_page()."""
    post_list = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(post_list, 10)

    page = paginator.get_page(request.GET.get('page'))
    # Returns Page object, or first page if invalid, or last if out of range

    return render(request, 'blog/post_list.html', {'posts': page})

# ---------------------------------------------------------------------------
# 5. Pagination in Class-Based Views
# ---------------------------------------------------------------------------

# Using PaginationMixin:
# from django.views.generic import ListView
#
# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'
#     paginate_by = 10

# Or manually in get_context_data:
# from django.core.paginator import Paginator
#
# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset = self.get_queryset()
#         paginator = Paginator(queryset, 10)
#         page = self.request.GET.get('page')
#         context['posts'] = paginator.get_page(page)
#         return context

# ---------------------------------------------------------------------------
# 6. Template Pagination
# ---------------------------------------------------------------------------
# Render pagination controls in your template.

# blog/post_list.html:
# {% extends "blog/base.html" %}
#
# {% block content %}
# <h1>Blog Posts</h1>
#
# {% for post in posts %}
#     <article>
#         <h2>{{ post.title }}</h2>
#         <p>{{ post.excerpt }}</p>
#     </article>
# {% empty %}
#     <p>No posts found.</p>
# {% endfor %}
#
# <!-- Pagination controls -->
# {% if posts.has_other_pages %}
# <nav aria-label="Page navigation">
#     <ul class="pagination">
#         {% if posts.has_previous %}
#             <li class="page-item">
#                 <a class="page-link" href="?page={{ posts.previous_page_number }}">
#                     &laquo; Previous
#                 </a>
#             </li>
#         {% else %}
#             <li class="page-item disabled">
#                 <span class="page-link">&laquo; Previous</span>
#             </li>
#         {% endif %}
#
#         {% for num in posts.paginator.page_range %}
#             {% if posts.number == num %}
#                 <li class="page-item active">
#                     <span class="page-link">{{ num }}</span>
#                 </li>
#             {% elif num > posts.number|add:'-3' and num < posts.number|add:'3' %}
#                 <li class="page-item">
#                     <a class="page-link" href="?page={{ num }}">{{ num }}</a>
#                 </li>
#             {% endif %}
#         {% endfor %}
#
#         {% if posts.has_next %}
#             <li class="page-item">
#                 <a class="page-link" href="?page={{ posts.next_page_number }}">
#                     Next &raquo;
#                 </a>
#             </li>
#         {% else %}
#             <li class="page-item disabled">
#                 <span class="page-link">Next &raquo;</span>
#             </li>
#         {% endif %}
#     </ul>
# </nav>
# {% endif %}
#
# <p>Page {{ posts.number }} of {{ posts.paginator.num_pages }}</p>
# {% endblock %}

# ---------------------------------------------------------------------------
# 7. Smart Pagination Links
# ---------------------------------------------------------------------------
# Show limited page numbers with ellipsis.

# {% if posts.has_other_pages %}
# <nav>
#     <ul class="pagination">
#         {% if posts.has_previous %}
#             <li><a href="?page={{ posts.previous_page_number }}">&laquo;</a></li>
#         {% endif %}
#
#         {% for num in posts.paginator.page_range %}
#             {% if posts.number == num %}
#                 <li class="active"><span>{{ num }}</span></li>
#             {% elif num > posts.number|add:'-3' and num < posts.number|add:'3' %}
#                 <li><a href="?page={{ num }}">{{ num }}</a></li>
#             {% elif num == 1 or num == posts.paginator.num_pages %}
#                 <li><a href="?page={{ num }}">{{ num }}</a></li>
#             {% elif num == posts.number|add:'-3' or num == posts.number|add:'3' %}
#                 <li><span>...</span></li>
#             {% endif %}
#         {% endfor %}
#
#         {% if posts.has_next %}
#             <li><a href="?page={{ posts.next_page_number }}">&raquo;</a></li>
#         {% endif %}
#     </ul>
# </nav>
# {% endif %}

# ---------------------------------------------------------------------------
# 8. Preserve Query Parameters
# ---------------------------------------------------------------------------
# Keep existing GET parameters (like search, filters) when paginating.

def search_with_pagination(request):
    """Pagination that preserves search parameters."""
    query = request.GET.get('q', '')
    posts = Post.objects.filter(status='published')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator = Paginator(posts, 10)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'posts': page,
        'search_query': query,
    }
    return render(request, 'blog/search_results.html', context)

# In template, preserve query params:
# {% if posts.has_previous %}
#     <a href="?page={{ posts.previous_page_number }}&q={{ search_query }}">
#         Previous
#     </a>
# {% endif %}

# ---------------------------------------------------------------------------
# 9. Pagination Settings
# ---------------------------------------------------------------------------

# settings.py:
# PAGINATE_BY = 10  # Default page size

# Or per-view:
# paginator = Paginator(queryset, per_page=10)
#
# With orphans (minimum objects on last page):
# paginator = Paginator(queryset, 10, orphans=2)
# If last page has 2 or fewer items, merge with previous page

# ---------------------------------------------------------------------------
# 10. Infinite Scroll Pagination
# ---------------------------------------------------------------------------
# For infinite scroll, return JSON with pagination info.

from django.http import JsonResponse


def post_list_api(request):
    """API endpoint for infinite scroll pagination."""
    page = int(request.GET.get('page', 1))
    per_page = 10

    posts = Post.objects.filter(status='published').order_by('-created_at')
    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page)

    data = {
        'posts': [
            {
                'id': post.id,
                'title': post.title,
                'excerpt': post.excerpt,
                'url': post.get_absolute_url(),
            }
            for post in page_obj
        ],
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'total_pages': paginator.num_pages,
    }

    return JsonResponse(data)

# JavaScript for infinite scroll:
# let page = 1;
# let loading = false;
#
# function loadMore() {
#     if (loading) return;
#     loading = true;
#
#     fetch(`/api/posts/?page=${page}`)
#         .then(response => response.json())
#         .then(data => {
#             data.posts.forEach(post => {
#                 document.getElementById('posts').innerHTML += `
#                     <article>
#                         <h2>${post.title}</h2>
#                         <p>${post.excerpt}</p>
#                     </article>
#                 `;
#             });
#
#             if (data.has_next) {
#                 page = data.next_page;
#                 loading = false;
#             }
#         });
# }
#
# window.addEventListener('scroll', () => {
#     if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
#         loadMore();
#     }
# });

# ---------------------------------------------------------------------------
# 11. Pagination Best Practices
# ---------------------------------------------------------------------------
# 1. Use get_page() instead of manual exception handling (cleaner)
# 2. Set appropriate per_page value (10-20 is common)
# 3. Use orphans to avoid tiny last pages
# 4. Show page numbers with ellipsis for many pages
# 5. Preserve query parameters when paginating filtered results
# 6. Use index on fields used for ordering (performance)
# 7. Consider cursor-based pagination for infinite scroll
# 8. Add SEO-friendly pagination (rel="next", rel="prev")
# 9. Test pagination with edge cases (0 results, 1 result)
# 10. Use prefetch_related() for related data on paginated results
