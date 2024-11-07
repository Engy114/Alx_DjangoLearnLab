from django.shortcuts import render
from django.views.generic.detail import DetailView  # Explicitly import DetailView
from django.views.generic import ListView
from .models import Library, Book

# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Ensure this template exists
    context_object_name = 'library'

# Example function-based view for listing all books and their authors
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import login

class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login after logout

class UserRegisterView(CreateView):
    template_name = 'relationship_app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login after successful registration


