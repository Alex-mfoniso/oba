import pandas as pd
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import authenticate_user, issue_bearer_token
from .docs import build_schema
from .models import Course, Enrollment, Student
from .responses import success_response
from .serializers import (
    AuthTokenRequestSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    StudentBulkCreateSerializer,
    StudentImportSerializer,
    StudentSerializer,
    StudentUploadSerializer,
)


class StandardResponseMixin:
    list_message = "Records retrieved successfully."
    create_message = "Record created successfully."
    update_message = "Record updated successfully."
    delete_message = "Record deleted successfully."

    def success(self, data=None, message="", status_code=status.HTTP_200_OK, meta=None):
        return success_response(data=data, message=message, status_code=status_code, meta=meta)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self.success(serializer.data, self.list_message)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success(serializer.data, "Record retrieved successfully.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success(serializer.data, self.create_message, status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success(serializer.data, self.update_message)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return self.success({"id": instance.pk, "deleted": True}, self.delete_message)


class StudentViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create(self, request):
        serializer = StudentBulkCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        output = StudentSerializer(created, many=True, context={"request": request}).data
        return self.success(output, f"{len(created)} students created successfully.", status_code=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"], url_path="bulk-delete")
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return Response(
                {"success": False, "message": "ids must be a non-empty list.", "errors": {"ids": "Required."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = Student.objects.filter(id__in=ids)
        count = queryset.count()
        queryset.delete()
        return self.success({"deleted_count": count, "deleted_ids": ids}, f"{count} students deleted successfully.")

    @action(detail=False, methods=["post"], url_path="import")
    def import_students(self, request):
        serializer = StudentImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        extension = uploaded_file.name.rsplit(".", 1)[-1].lower()

        if extension == "csv":
            uploaded_file.seek(0)
            data_frame = pd.read_csv(uploaded_file)
        elif extension in {"xls", "xlsx"}:
            uploaded_file.seek(0)
            data_frame = pd.read_excel(uploaded_file)
        else:
            return Response(
                {"success": False, "message": "Upload a CSV, XLS, or XLSX file.", "errors": {"file": "Unsupported file type."}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        records = data_frame.where(pd.notnull(data_frame), None).to_dict(orient="records")
        prepared = []
        for row in records:
            prepared.append(
                {
                    "admission_number": row.get("admission_number") or row.get("student_id") or row.get("admission_no"),
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "email": row.get("email"),
                    "phone_number": row.get("phone_number") or row.get("phone"),
                    "date_of_birth": row.get("date_of_birth"),
                    "department": row.get("department", ""),
                    "level": row.get("level"),
                    "status": row.get("status", Student.Status.ACTIVE),
                    "notes": row.get("notes", ""),
                }
            )

        bulk_serializer = StudentBulkCreateSerializer(data=prepared, many=True)
        bulk_serializer.is_valid(raise_exception=True)
        created = bulk_serializer.save()
        output = StudentSerializer(created, many=True, context={"request": request}).data
        return self.success(output, f"{len(created)} students imported successfully.", status_code=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="upload-photo")
    def upload_photo(self, request, pk=None):
        student = self.get_object()
        serializer = StudentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student.profile_file = serializer.validated_data["profile_file"]
        student.save()
        output = StudentSerializer(student, context={"request": request}).data
        return self.success(output, "Student photo uploaded successfully.")

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        student = get_object_or_404(Student.all_objects, pk=pk)
        student.restore()
        output = StudentSerializer(student, context={"request": request}).data
        return self.success(output, "Student restored successfully.")


class CourseViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create(self, request):
        serializer = CourseSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        output = CourseSerializer(created, many=True).data
        return self.success(output, f"{len(created)} courses created successfully.", status_code=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        course = get_object_or_404(Course.all_objects, pk=pk)
        course.restore()
        output = CourseSerializer(course).data
        return self.success(output, "Course restored successfully.")


class EnrollmentViewSet(StandardResponseMixin, viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        enrollment = get_object_or_404(Enrollment.all_objects, pk=pk)
        enrollment.restore()
        output = EnrollmentSerializer(enrollment).data
        return self.success(output, "Enrollment restored successfully.")


class AuthTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate_user(
            serializer.validated_data["username"],
            serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"success": False, "message": "Invalid username or password.", "errors": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token = issue_bearer_token(user)
        return Response(
            {
                "success": True,
                "message": "Bearer token issued successfully.",
                "data": {
                    "token_type": "Bearer",
                    "token": token,
                    "user": {
                        "id": user.id,
                        "username": user.get_username(),
                        "email": getattr(user, "email", ""),
                    },
                },
            },
            status=status.HTTP_200_OK,
        )


class SchemaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(build_schema(request))


class SwaggerUIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        context = {"schema_url": "/api/schema/"}
        return TemplateResponse(request, "student_portal/swagger_ui.html", context)


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"success": True, "message": "API is healthy.", "data": {"status": "ok"}})
