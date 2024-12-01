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

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# List all books
class BookListView(ListAPIView):
    """
    Provides a read-only list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

# Retrieve a single book by ID
class BookDetailView(RetrieveAPIView):
    """
    Provides detailed information about a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Create a new book
class BookCreateView(CreateAPIView):
    """
    Allows authenticated users to add a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

# Update an existing book
class BookUpdateView(UpdateAPIView):
    """
    Allows authenticated users to update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Delete a book
class BookDeleteView(DestroyAPIView):
    """
    Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(ListAPIView):
    """
    Provides a list of books with filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,  # Enables filtering
        SearchFilter,         # Enables searching
        OrderingFilter        # Enables ordering
    ]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Search fields
    search_fields = ['title', 'author__name']

    # Ordering fields
    ordering_fields = ['title', 'publication_year']
