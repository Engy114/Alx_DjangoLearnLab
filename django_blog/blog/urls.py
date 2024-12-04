from django.urls import path
from . import views

urlpatterns = [
    # Example URL patterns
    path('', views.home, name='home'),  # Add your view function names here
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
