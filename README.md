# Student Portal API

A Django REST Framework backend for managing students, courses, and enrollments with:

- PostgreSQL-ready settings
- Soft delete
- Bulk create and bulk delete
- CSV/XLSX import
- Image/file upload with optional optimization
- Bearer token, username/password, and API key authentication
- Swagger-style docs and OpenAPI JSON

## Quick Start

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and adjust values.
4. Run `python manage.py migrate`.
5. Start the server with `python manage.py runserver`.

## Database

SQLite works out of the box.

To use PostgreSQL, set:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=student_portal
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

## Docs

- `GET /api/docs/`
- `GET /api/schema/`

## Auth

- `POST /api/auth/token/` to exchange username/password for a bearer token
- `Authorization: Bearer <token>`
- `Authorization: Basic <base64>`
- `X-API-KEY: <key>`

## Student Endpoints

- `GET /api/students/`
- `POST /api/students/`
- `POST /api/students/bulk-create/`
- `DELETE /api/students/bulk-delete/`
- `POST /api/students/import/`
- `PATCH /api/students/<id>/upload-photo/`
- `POST /api/students/<id>/restore/`

## Course Endpoints

- `GET /api/courses/`
- `POST /api/courses/`
- `POST /api/courses/bulk-create/`
- `POST /api/courses/<id>/restore/`

## Enrollment Endpoints

- `GET /api/enrollments/`
- `POST /api/enrollments/`
- `POST /api/enrollments/<id>/restore/`
