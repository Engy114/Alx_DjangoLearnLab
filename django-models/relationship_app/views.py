from django.shortcuts import render

from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

from django.views.generic import ListView
from .models import Book, Library

class LibraryBooksView(ListView):
    model = Book
    template_name = 'library_books.html'

    def get_queryset(self):
        library_id = self.kwargs.get('library_id')
        return Book.objects.filter(library__id=library_id)
    
    "relationship_app/list_books.html"

