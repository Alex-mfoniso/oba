from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")
router.register(r"borrow-records", BorrowRecordViewSet, basename="borrowrecord")

urlpatterns = router.urls

