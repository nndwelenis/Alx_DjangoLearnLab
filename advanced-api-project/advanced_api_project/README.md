## Book API Views

This project implements Django REST Framework generic views for the Book model.

### Available Endpoints

- GET /api/books/
  Retrieves all books. Public access.

- GET /api/books/<id>/
  Retrieves a single book by ID. Public access.

- POST /api/books/create/
  Creates a new book. Authentication required.

- PUT /api/books/<id>/update/
  Updates an existing book. Authentication required.

- DELETE /api/books/<id>/delete/
  Deletes a book. Authentication required.

### Permissions

Read operations are open to all users.
Write operations require authenticated users.

### Validation

Book publication years are validated to ensure they are not set in the future.


## Filtering, Searching, and Ordering

The Book list endpoint supports advanced query capabilities.

### Filtering
Available filters:
- title
- publication_year
- author

Example:
GET /api/books/?publication_year=2020

### Searching
Searchable fields:
- title
- author name

Example:
GET /api/books/?search=python

### Ordering
Orderable fields:
- title
- publication_year

Examples:
GET /api/books/?ordering=title  
GET /api/books/?ordering=-publication_year
