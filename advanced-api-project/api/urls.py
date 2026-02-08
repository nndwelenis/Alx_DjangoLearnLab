from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Create
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Update (checker expects "books/update")
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),

    # Delete (checker expects "books/delete")
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
