from rest_framework import serializers

from .image_utils import optimize_uploaded_image
from .models import Course, Enrollment, Student


class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        model = self.child.Meta.model
        objects = [model(**item) for item in validated_data]
        created = model.objects.bulk_create(objects)
        return created


class StudentSerializer(serializers.ModelSerializer):
    profile_file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "admission_number",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "department",
            "level",
            "status",
            "profile_file",
            "profile_file_url",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "profile_file_url"]
        list_serializer_class = BulkCreateListSerializer

    def get_profile_file_url(self, obj):
        request = self.context.get("request")
        if not obj.profile_file:
            return None
        url = obj.profile_file.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def validate_profile_file(self, file):
        content_type = getattr(file, "content_type", "") or ""
        if content_type and not content_type.startswith("image/"):
            raise serializers.ValidationError("profile_file must be an image upload.")
        return file

    def validate(self, attrs):
        profile_file = attrs.get("profile_file")
        if profile_file:
            attrs["profile_file"] = optimize_uploaded_image(profile_file)
        return attrs


class StudentBulkCreateSerializer(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        list_serializer_class = BulkCreateListSerializer


class StudentUploadSerializer(serializers.Serializer):
    profile_file = serializers.FileField()


class StudentImportSerializer(serializers.Serializer):
    file = serializers.FileField()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "title", "description", "credit_units", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        list_serializer_class = BulkCreateListSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    course_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_title",
            "session",
            "semester",
            "status",
            "enrolled_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "student_name", "course_title", "enrolled_at", "created_at", "updated_at"]
        list_serializer_class = BulkCreateListSerializer

    def get_student_name(self, obj):
        return str(obj.student)

    def get_course_title(self, obj):
        return str(obj.course)


class AuthTokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
