from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

# Create a new book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Retrieve the book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

# Update the title of the book
book.title = "Nineteen Eighty-Four"
book.save()

# Delete the book
book.delete()
