from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuthTokenView, CourseViewSet, EnrollmentViewSet, HealthView, SchemaView, StudentViewSet, SwaggerUIView

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("auth/token/", AuthTokenView.as_view(), name="auth-token"),
    path("schema/", SchemaView.as_view(), name="schema"),
    path("docs/", SwaggerUIView.as_view(), name="swagger-ui"),
]

urlpatterns += router.urls
