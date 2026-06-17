from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related("books").all()
    serializer_class = AuthorSerializer

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        author.delete()
        return Response({"message": "Author deleted successfully."}, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request):
        count = Book.objects.all().count()
        Book.objects.all().delete()
        return Response({"message": f"Successfully deleted {count} books."}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response({"message": "Book deleted successfully."}, status=status.HTTP_200_OK)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.select_related("book", "book__author").all()
    serializer_class = BorrowRecordSerializer

    def destroy(self, request, *args, **kwargs):
        borrow_record = self.get_object()
        borrow_record.delete()
        return Response({"message": "Borrow record deleted successfully."}, status=status.HTTP_200_OK)
