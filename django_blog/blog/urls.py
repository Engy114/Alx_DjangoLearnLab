from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,  # Import for tagging functionality
    search,
    home,
    login,
    register,
    profile,
)

urlpatterns = [
    # Non-CRUD view URLs
    path('', home, name='home'),  # Home page
    path('login/', login, name='login'),  # Login page
    path('register/', register, name='register'),  # Register page
    path('profile/', profile, name='profile'),  # Profile page

    # CRUD URLs for Post model
    path('post/', PostListView.as_view(), name='post-list'),  # List all posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View a single post
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Update a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete a post

    # CRUD URLs for Comment model
    path('post/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-create'),  # Create a new comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),  # Update a comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),  # Delete a comment

    # Search URL
    path('search/', search, name='search'),

    # Tagging URL
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tagged-posts'),  # View posts by tag
]
