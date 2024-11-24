from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# ViewSet for full CRUD operations on the Book model
class BookViewSet(ModelViewSet):
    """
    A ViewSet that provides CRUD operations for the Book model.
    Only authenticated users can access this ViewSet.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

# ListAPIView for listing all books (read-only)
class BookList(ListAPIView):
    """
    A ListAPIView that lists all books in the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
