from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, NestedBookSerializer
from rest_framework.permissions import IsAuthenticated

# ViewSet for CRUD operations on the Book model
class BookViewSet(ModelViewSet):
    """
    Provides CRUD operations for books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

# ViewSet for CRUD operations on the Author model
class AuthorViewSet(ModelViewSet):
    """
    Provides CRUD operations for authors.
    """
    queryset = Author.objects.all()
    serializer_class = NestedBookSerializer
    permission_classes = [IsAuthenticated]

# Read-only view for listing all books
class BookListView(ListAPIView):
    """
    Provides a read-only list of books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

