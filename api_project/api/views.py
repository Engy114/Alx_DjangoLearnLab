from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
generics.ListAPIView
