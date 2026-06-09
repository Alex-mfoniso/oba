from rest_framework import serializers

from .models import Author, Book, BorrowRecord


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "biography", "created_at"]
        read_only_fields = ["id", "created_at"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return str(obj.author)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "author",
            "author_name",
            "published_date",
            "description",
            "available_copies",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "author_name"]


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ["id", "book", "borrower_name", "borrowed_at", "returned_at", "is_returned"]
        read_only_fields = ["id", "borrowed_at", "is_returned"]
