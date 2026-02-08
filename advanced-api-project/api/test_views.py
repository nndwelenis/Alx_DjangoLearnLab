from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from api.models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    """

    def setUp(self):
        """
        Set up test data for all test cases.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.author = Author.objects.create(name='Robert Martin')

        self.book = Book.objects.create(
            title='Clean Code',
            publication_year=2008,
            author=self.author
        )

        self.list_url = '/api/books/'
        self.detail_url = f'/api/books/{self.book.id}/'
        self.create_url = '/api/books/create/'
        self.update_url = f'/api/books/update/{self.book.id}/'
        self.delete_url = f'/api/books/delete/{self.book.id}/'


    def test_get_book_list(self):
        """
        Ensure unauthenticated users can retrieve the book list.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_get_book_detail(self):
        """
        Ensure unauthenticated users can retrieve a single book.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Clean Code')


    def test_create_book_authenticated(self):
        """
        Ensure authenticated users can create a book.
        """
        self.client.login(username='testuser', password='testpassword')

        data = {
            'title': 'Clean Architecture',
            'publication_year': 2017,
            'author': self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create a book.
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_filter_books_by_publication_year(self):
        """
        Ensure filtering by publication year works.
        """
        response = self.client.get(self.list_url + '?publication_year=2008')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """
        Ensure searching by title works.
        """
        response = self.client.get(self.list_url + '?search=Clean')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_order_books_by_title(self):
        """
        Ensure ordering by title works.
        """
        response = self.client.get(self.list_url + '?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

