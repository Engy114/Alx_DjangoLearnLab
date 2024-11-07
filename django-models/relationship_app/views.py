from django.views.generic import DetailView, ListView
from .models import Library, Book

# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Using specified template
    context_object_name = 'library'

# Example function-based view for listing all books and their authors
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

