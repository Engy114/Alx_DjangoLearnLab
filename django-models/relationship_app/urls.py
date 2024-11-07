from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:library_id>/books/', views.LibraryBooksView.as_view(), name='library_books'),
]