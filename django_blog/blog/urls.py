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
    path('post/', ListView.as_view(), name='post-list'),  # List all posts
    path('post/<int:pk>/', DetailView.as_view(), name='post-detail'),  # View a single post
    path('post/new/', CreateView.as_view(), name='post-create'),  # Create a new post
    path('post/<int:pk>/update/', UpdateView.as_view(), name='post-update'),  # Update a post
    path('post/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),  # Delete a post
    path('post/<int:post_id>/comments/new/', views.add_comment, name='add-comment'),
    path('comments/<int:comment_id>/update/', views.update_comment, name='update-comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
]

