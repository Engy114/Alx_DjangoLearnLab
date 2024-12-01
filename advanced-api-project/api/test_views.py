from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Tests for Book API endpoints.
    """

    def setUp(self):
        """
        Create test data.
        """
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create an author
        self.author = Author.objects.create(name='J.K. Rowling')

        # Create a book
        self.book = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author
        )

        # Authentication URL
        self.login_url = '/api-token-auth/'

        # API endpoints
        self.book_list_url = '/api/books/'
        self.book_detail_url = f'/api/books/{self.book.id}/'

    def test_list_books(self):
        """
        Test retrieving a list of books.
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        """
        Test creating a new book.
        """
        self.client.login(username='testuser', password='password')
        data = {
            'title': 'Fantastic Beasts',
            'publication_year': 2016,
            'author': self.author.id
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """
        Test updating an existing book.
        """
        self.client.login(username='testuser', password='password')
        data = {
            'title': 'Harry Potter and the Chamber of Secrets',
            'publication_year': 1998,
            'author': self.author.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Harry Potter and the Chamber of Secrets')

    def test_delete_book(self):
        """
        Test deleting a book.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """
        Test filtering books by title.
        """
        response = self.client.get(f'{self.book_list_url}?title=Harry Potter')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """
        Test searching books by author name.
        """
        response = self.client.get(f'{self.book_list_url}?search=Rowling')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """
        Test ordering books by publication_year.
        """
        Book.objects.create(
            title='Fantastic Beasts',
            publication_year=2016,
            author=self.author
        )
        response = self.client.get(f'{self.book_list_url}?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Fantastic Beasts')
