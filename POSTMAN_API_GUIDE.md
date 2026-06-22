# Student Portal API - Postman Testing Guide

## Base Configuration

**Base URL:** `http://localhost:8000/api`

### Setup Steps

1. Start the Django server: `python manage.py runserver`
2. Create a Postman environment variable for the base URL if you want
3. Add an `Authorization` header when testing protected endpoints

---

## 1. AUTHENTICATION

### 1.1 Get Bearer Token

**Method:** `POST`  
**URL:** `http://localhost:8000/api/auth/token/`

**Request Body:**

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

**Response Example (200 OK):**

```json
{
  "success": true,
  "message": "Bearer token issued successfully.",
  "data": {
    "token_type": "Bearer",
    "token": "your-token-value",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    }
  }
}
```

### 1.2 Use the Token

Set one of these headers:

- `Authorization: Bearer <token>`
- `Authorization: Basic <base64 username:password>`
- `X-API-KEY: <your-api-key>`

---

## 2. STANDARD RESPONSE FORMAT

### Success

```json
{
  "success": true,
  "message": "Record created successfully.",
  "data": {}
}
```

### Error

```json
{
  "success": false,
  "message": "Validation error.",
  "errors": {}
}
```

---

## 3. STUDENTS

### 3.1 Get All Students

**Method:** `GET`  
**URL:** `http://localhost:8000/api/students/`

### 3.2 Create Student

**Method:** `POST`  
**URL:** `http://localhost:8000/api/students/`

```json
{
  "admission_number": "STD-001",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "phone_number": "08030000000",
  "department": "Computer Science",
  "level": 300,
  "status": "active",
  "notes": "New student"
}
```

### 3.3 Partial Update Student

**Method:** `PATCH`  
**URL:** `http://localhost:8000/api/students/{id}/`

```json
{
  "phone_number": "08039999999"
}
```

### 3.4 Bulk Create Students

**Method:** `POST`  
**URL:** `http://localhost:8000/api/students/bulk-create/`

```json
[
  {
    "admission_number": "STD-002",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john@example.com"
  },
  {
    "admission_number": "STD-003",
    "first_name": "Mary",
    "last_name": "James",
    "email": "mary@example.com"
  }
]
```

### 3.5 Bulk Delete Students

**Method:** `DELETE`  
**URL:** `http://localhost:8000/api/students/bulk-delete/`

```json
{
  "ids": [1, 2, 3]
}
```

### 3.6 Import Students from CSV or Excel

**Method:** `POST`  
**URL:** `http://localhost:8000/api/students/import/`

**Body type:** `form-data`

- `file`: CSV, XLS, or XLSX file

Required columns:

- `admission_number`
- `first_name`
- `last_name`
- `email`

### 3.7 Upload Student Photo

**Method:** `PATCH`  
**URL:** `http://localhost:8000/api/students/{id}/upload-photo/`

**Body type:** `form-data`

- `profile_file`: image file

### 3.8 Restore Student

**Method:** `POST`  
**URL:** `http://localhost:8000/api/students/{id}/restore/`

---

## 4. COURSES

- `GET /api/courses/`
- `POST /api/courses/`
- `POST /api/courses/bulk-create/`
- `POST /api/courses/{id}/restore/`

---

## 5. ENROLLMENTS

- `GET /api/enrollments/`
- `POST /api/enrollments/`
- `POST /api/enrollments/{id}/restore/`

---

## 6. DOCS

- `GET /api/docs/` opens Swagger UI
- `GET /api/schema/` returns the OpenAPI JSON
