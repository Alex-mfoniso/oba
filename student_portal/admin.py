from django.contrib import admin

from .models import Course, Enrollment, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_number", "first_name", "last_name", "email", "status", "is_deleted")
    search_fields = ("admission_number", "first_name", "last_name", "email")
    list_filter = ("status", "department", "is_deleted")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "credit_units", "is_deleted")
    search_fields = ("code", "title")
    list_filter = ("credit_units", "is_deleted")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "session", "semester", "status", "is_deleted")
    search_fields = ("student__admission_number", "course__code")
    list_filter = ("session", "semester", "status", "is_deleted")
