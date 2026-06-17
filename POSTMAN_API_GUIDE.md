# Library API - Postman Testing Guide

## Base Configuration

**Base URL:** `http://localhost:8000/api`

### Setup Steps

1. Start the Django server: `python manage.py runserver`
2. Create a Postman environment variable for the base URL (optional)
3. All endpoints return JSON responses

---

## 1. AUTHORS ENDPOINTS

### 1.1 Get All Authors

**Method:** `GET`  
**URL:** `http://localhost:8000/api/authors/`

**Description:** Retrieve a list of all authors with their associated books.

**Response Example:**

```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Smith",
    "biography": "A renowned author",
    "created_at": "2025-06-17T10:30:45.123456Z",
    "books": [
      {
        "id": 1,
        "title": "The Great Adventure",
        "isbn": "978-1-234-56789-0",
        "published_date": "2020-05-15",
        "description": "An epic journey",
        "available_copies": 5
      }
    ]
  }
]
```

**Postman Test Steps:**

1. Create a new GET request
2. Paste the URL
3. Click "Send"
4. Verify status code is 200

---

### 1.2 Create Author

**Method:** `POST`  
**URL:** `http://localhost:8000/api/authors/`

**Description:** Create a new author.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "biography": "An acclaimed novelist with multiple awards"
}
```

**Response Example (201 Created):**

```json
{
  "id": 2,
  "first_name": "Jane",
  "last_name": "Doe",
  "biography": "An acclaimed novelist with multiple awards",
  "created_at": "2025-06-17T11:45:30.456789Z",
  "books": []
}
```

**Postman Test Steps:**

1. Create a new POST request
2. Paste the URL
3. Go to "Body" tab → Select "raw" → Choose "JSON"
4. Paste the request body
5. Click "Send"
6. Verify status code is 201
7. Note the returned `id` for use in other requests

---

### 1.3 Get Author by ID

**Method:** `GET`  
**URL:** `http://localhost:8000/api/authors/{id}/`  
_Example:_ `http://localhost:8000/api/authors/1/`

**Description:** Retrieve a specific author and their books.

**Response Example:**

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Smith",
  "biography": "A renowned author",
  "created_at": "2025-06-17T10:30:45.123456Z",
  "books": [
    {
      "id": 1,
      "title": "The Great Adventure",
      "isbn": "978-1-234-56789-0",
      "published_date": "2020-05-15",
      "description": "An epic journey",
      "available_copies": 5
    }
  ]
}
```

**Postman Test Steps:**

1. Create a new GET request
2. Enter URL: `http://localhost:8000/api/authors/1/`
3. Click "Send"
4. Verify status code is 200

---

### 1.4 Update Author (Full Update)

**Method:** `PUT`  
**URL:** `http://localhost:8000/api/authors/{id}/`  
_Example:_ `http://localhost:8000/api/authors/1/`

**Description:** Completely replace author data (all fields required).

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "biography": "Updated biography with more details"
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Smith",
  "biography": "Updated biography with more details",
  "created_at": "2025-06-17T10:30:45.123456Z",
  "books": []
}
```

**Postman Test Steps:**

1. Create a new PUT request
2. Enter URL with author ID
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body with all required fields
5. Click "Send"
6. Verify status code is 200

---

### 1.5 Partial Update Author

**Method:** `PATCH`  
**URL:** `http://localhost:8000/api/authors/{id}/`  
_Example:_ `http://localhost:8000/api/authors/1/`

**Description:** Update only specific fields (partial update).

**Headers:**

```
Content-Type: application/json
```

**Request Body (example - update only biography):**

```json
{
  "biography": "A famous author known for mystery novels"
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Smith",
  "biography": "A famous author known for mystery novels",
  "created_at": "2025-06-17T10:30:45.123456Z",
  "books": []
}
```

**Postman Test Steps:**

1. Create a new PATCH request
2. Enter URL with author ID
3. Go to "Body" → "raw" → "JSON"
4. Paste only the fields you want to update
5. Click "Send"
6. Verify status code is 200

---

### 1.6 Delete Author

**Method:** `DELETE`  
**URL:** `http://localhost:8000/api/authors/{id}/`  
_Example:_ `http://localhost:8000/api/authors/1/`

**Description:** Delete an author. Cascades delete associated books.

**Response Example (200 OK):**

```json
{
  "message": "Author deleted successfully."
}
```

**Postman Test Steps:**

1. Create a new DELETE request
2. Enter URL with author ID
3. Click "Send"
4. Verify status code is 200
5. Verify the author no longer appears in GET all authors

---

## 2. BOOKS ENDPOINTS

### 2.1 Get All Books

**Method:** `GET`  
**URL:** `http://localhost:8000/api/books/`

**Description:** Retrieve a list of all books.

**Response Example:**

```json
[
  {
    "id": 1,
    "title": "The Great Adventure",
    "isbn": "978-1-234-56789-0",
    "author": 1,
    "author_name": "Smith, John",
    "published_date": "2020-05-15",
    "description": "An epic journey filled with mystery",
    "available_copies": 5,
    "created_at": "2025-06-17T10:35:20.789012Z"
  }
]
```

**Postman Test Steps:**

1. Create a new GET request
2. Paste the URL
3. Click "Send"
4. Verify status code is 200

---

### 2.2 Create Book

**Method:** `POST`  
**URL:** `http://localhost:8000/api/books/`

**Description:** Create a new book. The author must exist first.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "The Mystery of the Lost Temple",
  "isbn": "978-1-987-65432-1",
  "author": 1,
  "published_date": "2023-03-20",
  "description": "A thrilling adventure in ancient ruins",
  "available_copies": 3
}
```

**Response Example (201 Created):**

```json
{
  "id": 2,
  "title": "The Mystery of the Lost Temple",
  "isbn": "978-1-987-65432-1",
  "author": 1,
  "author_name": "Smith, John",
  "published_date": "2023-03-20",
  "description": "A thrilling adventure in ancient ruins",
  "available_copies": 3,
  "created_at": "2025-06-17T11:50:15.234567Z"
}
```

**Postman Test Steps:**

1. Create a new POST request
2. Paste the URL
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body (make sure author ID exists)
5. Click "Send"
6. Verify status code is 201

---

### 2.3 Get Book by ID

**Method:** `GET`  
**URL:** `http://localhost:8000/api/books/{id}/`  
_Example:_ `http://localhost:8000/api/books/1/`

**Description:** Retrieve a specific book with all details.

**Response Example:**

```json
{
  "id": 1,
  "title": "The Great Adventure",
  "isbn": "978-1-234-56789-0",
  "author": 1,
  "author_name": "Smith, John",
  "published_date": "2020-05-15",
  "description": "An epic journey filled with mystery",
  "available_copies": 5,
  "created_at": "2025-06-17T10:35:20.789012Z"
}
```

**Postman Test Steps:**

1. Create a new GET request
2. Enter URL: `http://localhost:8000/api/books/1/`
3. Click "Send"
4. Verify status code is 200

---

### 2.4 Update Book (Full Update)

**Method:** `PUT`  
**URL:** `http://localhost:8000/api/books/{id}/`  
_Example:_ `http://localhost:8000/api/books/1/`

**Description:** Completely replace book data.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "The Great Adventure - Revised Edition",
  "isbn": "978-1-234-56789-0",
  "author": 1,
  "published_date": "2020-05-15",
  "description": "An epic journey - completely revised",
  "available_copies": 7
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "title": "The Great Adventure - Revised Edition",
  "isbn": "978-1-234-56789-0",
  "author": 1,
  "author_name": "Smith, John",
  "published_date": "2020-05-15",
  "description": "An epic journey - completely revised",
  "available_copies": 7,
  "created_at": "2025-06-17T10:35:20.789012Z"
}
```

**Postman Test Steps:**

1. Create a new PUT request
2. Enter URL with book ID
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body with all required fields
5. Click "Send"
6. Verify status code is 200

---

### 2.5 Partial Update Book

**Method:** `PATCH`  
**URL:** `http://localhost:8000/api/books/{id}/`  
_Example:_ `http://localhost:8000/api/books/1/`

**Description:** Update only specific book fields.

**Headers:**

```
Content-Type: application/json
```

**Request Body (example - update available copies):**

```json
{
  "available_copies": 10
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "title": "The Great Adventure",
  "isbn": "978-1-234-56789-0",
  "author": 1,
  "author_name": "Smith, John",
  "published_date": "2020-05-15",
  "description": "An epic journey filled with mystery",
  "available_copies": 10,
  "created_at": "2025-06-17T10:35:20.789012Z"
}
```

**Postman Test Steps:**

1. Create a new PATCH request
2. Enter URL with book ID
3. Go to "Body" → "raw" → "JSON"
4. Paste only the fields you want to update
5. Click "Send"
6. Verify status code is 200

---

### 2.6 Delete Book

**Method:** `DELETE`  
**URL:** `http://localhost:8000/api/books/{id}/`  
_Example:_ `http://localhost:8000/api/books/1/`

**Description:** Delete a book.

**Response Example (200 OK):**

```json
{
  "message": "Book deleted successfully."
}
```

**Postman Test Steps:**

1. Create a new DELETE request
2. Enter URL with book ID
3. Click "Send"
4. Verify status code is 200
5. Try to GET the deleted book - should return 404

---

### 2.7 Delete All Books

**Method:** `DELETE`  
**URL:** `http://localhost:8000/api/books/delete-all/`

**Description:** Delete all books in the database.

**Response Example (200 OK):**

```json
{
  "message": "Successfully deleted 15 books."
}
```

**Postman Test Steps:**

1. Create a new DELETE request
2. Enter URL: `http://localhost:8000/api/books/delete-all/`
3. Click "Send"

---

## 3. BORROW RECORDS ENDPOINTS

### 3.1 Get All Borrow Records

**Method:** `GET`  
**URL:** `http://localhost:8000/api/borrow-records/`

**Description:** Retrieve all borrow records with latest records first.

**Response Example:**

```json
[
  {
    "id": 1,
    "book": 1,
    "borrower_name": "Alice Johnson",
    "borrowed_at": "2025-06-17T09:15:30.123456Z",
    "returned_at": null,
    "is_returned": false
  },
  {
    "id": 2,
    "book": 2,
    "borrower_name": "Bob Smith",
    "borrowed_at": "2025-06-16T14:20:45.654321Z",
    "returned_at": "2025-06-17T10:30:00.123456Z",
    "is_returned": true
  }
]
```

**Postman Test Steps:**

1. Create a new GET request
2. Paste the URL
3. Click "Send"
4. Verify status code is 200

---

### 3.2 Create Borrow Record

**Method:** `POST`  
**URL:** `http://localhost:8000/api/borrow-records/`

**Description:** Create a new borrow record (marks when someone borrows a book). The book must exist.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "book": 1,
  "borrower_name": "Charlie Brown"
}
```

**Response Example (201 Created):**

```json
{
  "id": 3,
  "book": 1,
  "borrower_name": "Charlie Brown",
  "borrowed_at": "2025-06-17T12:00:15.789012Z",
  "returned_at": null,
  "is_returned": false
}
```

**Postman Test Steps:**

1. Create a new POST request
2. Paste the URL
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body (make sure book ID exists)
5. Click "Send"
6. Verify status code is 201
7. Note the `id` for marking as returned later

---

### 3.3 Get Borrow Record by ID

**Method:** `GET`  
**URL:** `http://localhost:8000/api/borrow-records/{id}/`  
_Example:_ `http://localhost:8000/api/borrow-records/1/`

**Description:** Retrieve a specific borrow record.

**Response Example:**

```json
{
  "id": 1,
  "book": 1,
  "borrower_name": "Alice Johnson",
  "borrowed_at": "2025-06-17T09:15:30.123456Z",
  "returned_at": null,
  "is_returned": false
}
```

**Postman Test Steps:**

1. Create a new GET request
2. Enter URL: `http://localhost:8000/api/borrow-records/1/`
3. Click "Send"
4. Verify status code is 200

---

### 3.4 Mark Book as Returned

**Method:** `PATCH`  
**URL:** `http://localhost:8000/api/borrow-records/{id}/`  
_Example:_ `http://localhost:8000/api/borrow-records/1/`

**Description:** Update a borrow record to mark the book as returned.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "returned_at": "2025-06-17T14:30:00Z"
}
```

**Alternative (let server set current time):**

```json
{
  "returned_at": "2025-06-17T14:30:00.000000Z"
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "book": 1,
  "borrower_name": "Alice Johnson",
  "borrowed_at": "2025-06-17T09:15:30.123456Z",
  "returned_at": "2025-06-17T14:30:00.000000Z",
  "is_returned": true
}
```

**Postman Test Steps:**

1. Create a new PATCH request
2. Enter URL with borrow record ID
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body with return date/time
5. Click "Send"
6. Verify status code is 200 and `is_returned` is true

---

### 3.5 Update Borrow Record (Full Update)

**Method:** `PUT`  
**URL:** `http://localhost:8000/api/borrow-records/{id}/`  
_Example:_ `http://localhost:8000/api/borrow-records/1/`

**Description:** Completely replace borrow record data.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "book": 1,
  "borrower_name": "Alice Johnson Updated",
  "returned_at": null
}
```

**Response Example (200 OK):**

```json
{
  "id": 1,
  "book": 1,
  "borrower_name": "Alice Johnson Updated",
  "borrowed_at": "2025-06-17T09:15:30.123456Z",
  "returned_at": null,
  "is_returned": false
}
```

**Postman Test Steps:**

1. Create a new PUT request
2. Enter URL with borrow record ID
3. Go to "Body" → "raw" → "JSON"
4. Paste the request body with all required fields
5. Click "Send"
6. Verify status code is 200

---

### 3.6 Delete Borrow Record

**Method:** `DELETE`  
**URL:** `http://localhost:8000/api/borrow-records/{id}/`  
_Example:_ `http://localhost:8000/api/borrow-records/1/`

**Description:** Delete a borrow record.

**Response Example (200 OK):**

```json
{
  "message": "Borrow record deleted successfully."
}
```

**Postman Test Steps:**

1. Create a new DELETE request
2. Enter URL with borrow record ID
3. Click "Send"
4. Verify status code is 200

---

## Common Testing Workflows

### Workflow 1: Complete Borrow Flow

1. **Create Author** → POST `/authors/`
2. **Create Book** → POST `/books/` (with author from step 1)
3. **Borrow Book** → POST `/borrow-records/` (with book from step 2)
4. **Return Book** → PATCH `/borrow-records/{id}/` (from step 3)
5. **Verify Return** → GET `/borrow-records/{id}/` (should have returned_at and is_returned=true)

### Workflow 2: Update Book Inventory

1. **Get Book** → GET `/books/{id}/`
2. **Note current available_copies**
3. **Update Copies** → PATCH `/books/{id}/` with new available_copies
4. **Verify Update** → GET `/books/{id}/`

### Workflow 3: Author Management

1. **Create Author** → POST `/authors/`
2. **Add Books** → POST `/books/` (multiple times with same author)
3. **Get Author** → GET `/authors/{id}/` (should show all books)
4. **Update Author** → PATCH `/authors/{id}/`
5. **Delete Author** → DELETE `/authors/{id}/` (cascades to books)

---

## HTTP Status Codes Reference

| Code | Meaning      | Common Scenarios                      |
| ---- | ------------ | ------------------------------------- |
| 200  | OK           | Successful GET, PUT, PATCH, DELETE    |
| 201  | Created      | Successful POST                       |
| 400  | Bad Request  | Invalid JSON, missing required fields |
| 404  | Not Found    | Invalid ID or resource doesn't exist  |
| 500  | Server Error | Database or server issues             |

---

## Error Examples

### Missing Required Field

**Request:** POST `/authors/` with missing `first_name`

```json
{
  "last_name": "Doe",
  "biography": "Test"
}
```

**Response (400 Bad Request):**

```json
{
  "first_name": ["This field is required."]
}
```

### Invalid Author ID

**Request:** GET `/authors/999/`
**Response (404 Not Found):**

```json
{
  "detail": "Not found."
}
```

### Invalid Foreign Key

**Request:** POST `/books/` with non-existent author ID

```json
{
  "title": "Test Book",
  "isbn": "978-1-234-56789-0",
  "author": 999,
  "available_copies": 1
}
```

**Response (400 Bad Request):**

```json
{
  "author": ["Invalid pk \"999\" - object does not exist."]
}
```

---

## Quick Reference Summary

| Resource           | Create | List | Read      | Update    | Partial     | Delete       |
| ------------------ | ------ | ---- | --------- | --------- | ----------- | ------------ |
| **Authors**        | POST   | GET  | GET /{id} | PUT /{id} | PATCH /{id} | DELETE /{id} |
| **Books**          | POST   | GET  | GET /{id} | PUT /{id} | PATCH /{id} | DELETE /{id} |
| **Borrow Records** | POST   | GET  | GET /{id} | PUT /{id} | PATCH /{id} | DELETE /{id} |

---

## Tips for Postman Testing

1. **Use Variables:** Set base_url = `http://localhost:8000/api` and use `{{base_url}}/authors/` in requests
2. **Save Responses:** Use Postman's environment to save IDs from creation responses
3. **Test Collections:** Create a Postman collection with all endpoints for easy sharing
4. **Pre-request Scripts:** Use to dynamically set values before requests
5. **Tests:** Add test scripts to validate responses automatically
6. **Documentation:** Add descriptions to requests for team reference
