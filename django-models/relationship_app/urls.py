from django.urls import path
from .views import list_books, LibraryDetailView  # Import both views


urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Assuming 'views' contains your custom registration view

urlpatterns = [
    # URL for user registration
    path('register/', views.register, name='register'),

    # URL for login, specifying the template explicitly
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),

    # URL for logout, specifying the template explicitly if required
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
]
