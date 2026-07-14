# =============================================================================
# Django REST Framework - Reference Guide
# =============================================================================
# Django REST Framework (DRF) is a powerful toolkit for building Web APIs
# on top of Django. It provides serialization, authentication, and more.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_rest_framework.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. Installation and Setup
# ---------------------------------------------------------------------------
# pip install djangorestframework

# settings.py:
# INSTALLED_APPS = [
#     ...
#     'rest_framework',
#     'blog',  # Your app
# ]
#
# # Optional: REST Framework settings
# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#     ],
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.AnonRateThrottle',
#         'rest_framework.throttling.UserRateThrottle',
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '100/day',
#         'user': '1000/day',
#     },
# }

# ---------------------------------------------------------------------------
# 2. Serializers
# ---------------------------------------------------------------------------
# Serializers convert complex data (querysets, models) to JSON and back.

from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """Serialize Author model."""
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.count()


class PostSerializer(serializers.ModelSerializer):
    """Serialize Post model."""
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'author_id', 'category', 'status',
            'is_featured', 'views_count', 'created_at',
            'updated_at', 'word_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']
        extra_kwargs = {
            'content': {'write_only': False},
        }

    def get_word_count(self, obj):
        return len(obj.content.split())

    def validate_title(self, value):
        """Custom field validation."""
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters."
            )
        return value

    def validate(self, data):
        """Custom object validation."""
        if data.get('title') and data.get('content'):
            if data['title'].lower() in data['content'].lower():
                raise serializers.ValidationError(
                    "Content should not contain the title."
                )
        return data


# Nested serializer:
class PostDetailSerializer(PostSerializer):
    """Detailed post serializer with comments."""
    comments = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['comments']

    def get_comments(self, obj):
        comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    """Serialize Comment model."""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# ---------------------------------------------------------------------------
# 3. Function-Based API Views
# ---------------------------------------------------------------------------

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create(request):
    """List all posts or create a new one."""
    if request.method == 'GET':
        posts = Post.objects.filter(status='published')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, pk):
    """Retrieve, update, or delete a post."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------------
# 4. Class-Based API Views
# ---------------------------------------------------------------------------

from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PostListCreateView(ListCreateAPIView):
    """List posts or create a new one."""
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'category', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views_count']
    ordering = ['-created_at']
    pagination_class = None  # Disable pagination for this view


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'

# ---------------------------------------------------------------------------
# 5. ViewSets and Routers
# ---------------------------------------------------------------------------
# ViewSets combine related views into a single class.
# Routers automatically generate URL patterns.

from rest_framework import viewsets, permissions
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    """Full CRUD for posts with extra actions."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """Get only published posts."""
        posts = Post.objects.filter(status='published')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a draft post."""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.status = 'published'
        post.save()
        return Response({'status': 'published'})


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD for authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# URL configuration with routers:
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'posts', PostViewSet)
# router.register(r'authors', AuthorViewSet)
#
# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls')),  # Browsable API login
# ]

# Generated URLs:
# GET    /api/posts/          → List all posts
# POST   /api/posts/          → Create a post
# GET    /api/posts/{id}/     → Retrieve a post
# PUT    /api/posts/{id}/     → Update a post
# DELETE /api/posts/{id}/     → Delete a post
# GET    /api/posts/published/ → Custom action
# POST   /api/posts/{id}/publish/ → Custom action
# GET    /api/authors/        → List all authors

# ---------------------------------------------------------------------------
# 6. Authentication
# ---------------------------------------------------------------------------
# DRF supports multiple authentication methods.

# --- Token Authentication ---
# INSTALLED_APPS = [..., 'rest_framework.authtoken']
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
# }
#
# Create token:
# from rest_framework.authtoken.models import Token
# token, created = Token.objects.get_or_create(user=user)
# print(token.key)  # Your API token

# Use token in requests:
# Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# --- JWT Authentication ---
# pip install djangorestframework-simplejwt
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
# }
# urlpatterns += [
#     path('api/token/', TokenObtainPairView.as_view()),
#     path('api/token/refresh/', TokenRefreshView.as_view()),
# ]

# --- Session Authentication ---
# Good for browsable API and Django login integration
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#     ],
# }

# ---------------------------------------------------------------------------
# 7. Permissions
# ---------------------------------------------------------------------------
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow only the author to edit."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Read-only for everyone
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only admins to modify."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# Built-in permissions:
# AllowAny              → Unrestricted access
# IsAuthenticated       → Must be logged in
# IsAuthenticatedOrRead → Read for anyone, write for authenticated
# IsAdminUser           → Must be is_staff=True
# IsAdminOrReadOnly     → Admin for write, anyone for read

# ---------------------------------------------------------------------------
# 8. API Endpoints (URL Patterns)
# ---------------------------------------------------------------------------

from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#
#     # API endpoints
#     path('api/', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls')),
#
#     # Token auth endpoints
#     path('api/token/', TokenObtainPairView.as_view()),
#     path('api/token/refresh/', TokenRefreshView.as_view()),
#
#     # Custom endpoints
#     path('api/posts/', post_list_create),
#     path('api/posts/<int:pk>/', post_detail),
# ]

# ---------------------------------------------------------------------------
# 9. Testing APIs
# ---------------------------------------------------------------------------
# DRF provides a test client for API testing.

# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
#
# class PostAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#         self.post = Post.objects.create(
#             title='Test Post',
#             content='Test content',
#             author=self.user,
#             status='published'
#         )
#
#     def test_list_posts(self):
#         response = self.client.get('/api/posts/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_post(self):
#         self.client.force_authenticate(user=self.user)
#         data = {'title': 'New Post', 'content': 'Content'}
#         response = self.client.post('/api/posts/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_unauthorized_create(self):
#         data = {'title': 'New Post', 'content': 'Content'}
#         response = self.client.post('/api/posts/', data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ---------------------------------------------------------------------------
# 10. DRF Best Practices
# ---------------------------------------------------------------------------
# 1. Use serializers for data validation and transformation
# 2. Use ViewSets + Routers for standard CRUD (less code)
# 3. Use Generic Views for simple cases
# 4. Set default permissions and authentication in settings
# 5. Use pagination for list endpoints
# 6. Add filtering and search capabilities
# 7. Use throttling to prevent abuse
# 8. Version your API (api/v1/, api/v2/)
# 9. Write API tests for every endpoint
# 10. Document your API with drf-yasg or drf-spectacular
