### API Endpoints

1. **List Books** (GET `/books/`):
   - Retrieves a list of all books.
   - No authentication required (read-only access).

2. **Retrieve Book Details** (GET `/books/<id>/`):
   - Retrieves details of a specific book by ID.
   - No authentication required (read-only access).

3. **Create Book** (POST `/books/create/`):
   - Adds a new book to the database.
   - Requires authentication (token required).

4. **Update Book** (PUT `/books/<id>/update/`):
   - Updates details of an existing book.
   - Requires authentication (token required).

5. **Delete Book** (DELETE `/books/<id>/delete/`):
   - Deletes a book from the database.
   - Requires authentication (token required).
