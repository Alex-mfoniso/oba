from copy import deepcopy


def build_schema(request=None):
    base_schema = {
        "openapi": "3.0.3",
        "info": {
            "title": "Student Portal API",
            "version": "1.0.0",
            "description": "Student portal endpoints with bearer token, basic auth, and API key support.",
        },
        "servers": [{"url": "/"}],
        "paths": {
            "/api/auth/token/": {
                "post": {
                    "summary": "Create bearer token",
                    "description": "Exchange a username and password for a DRF bearer token.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["username", "password"],
                                    "properties": {
                                        "username": {"type": "string"},
                                        "password": {"type": "string", "format": "password"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Token issued"}},
                }
            },
            "/api/students/": {
                "get": {"summary": "List students"},
                "post": {"summary": "Create a student"},
            },
            "/api/students/bulk-create/": {
                "post": {
                    "summary": "Create students in bulk",
                    "description": "Send an array of student objects.",
                }
            },
            "/api/students/bulk-delete/": {
                "delete": {
                    "summary": "Bulk delete students",
                    "description": "Soft delete multiple students by id.",
                }
            },
            "/api/students/import/": {
                "post": {
                    "summary": "Import students from CSV or Excel",
                    "description": "Upload a CSV, XLS, or XLSX file for bulk create.",
                }
            },
            "/api/students/{id}/upload-photo/": {
                "patch": {
                    "summary": "Upload a student image",
                    "description": "Multipart PATCH upload that shows a file chooser in Swagger UI.",
                }
            },
            "/api/courses/": {
                "get": {"summary": "List courses"},
                "post": {"summary": "Create a course"},
            },
            "/api/enrollments/": {
                "get": {"summary": "List enrollments"},
                "post": {"summary": "Create an enrollment"},
            },
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {"type": "http", "scheme": "bearer"},
                "BasicAuth": {"type": "http", "scheme": "basic"},
                "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
            },
            "schemas": {
                "Student": {
                    "type": "object",
                    "description": "Student record with optional image upload and soft-delete support.",
                },
                "Course": {"type": "object"},
                "Enrollment": {"type": "object"},
            },
        },
        "security": [{"BearerAuth": []}, {"BasicAuth": []}, {"ApiKeyAuth": []}],
    }
    return deepcopy(base_schema)
