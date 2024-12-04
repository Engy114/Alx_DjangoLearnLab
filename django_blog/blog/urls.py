from django.urls import path
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
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
    path('posts/', ListView.as_view(), name='post-list'),  # List all posts
    path('posts/<int:pk>/', DetailView.as_view(), name='post-detail'),  # View a single post
    path('posts/new/', CreateView.as_view(), name='post-create'),  # Create a new post
    path('posts/<int:pk>/edit/', UpdateView.as_view(), name='post-update'),  # Update a post
    path('posts/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),  # Delete a post
]

