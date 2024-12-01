from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # Include nested author details

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

class NestedBookSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)  # Dynamically serialize related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model fields.
    """
class NestedBookSerializer(serializers.ModelSerializer):
    """
    Serializes the related books dynamically for an Author.
    """
