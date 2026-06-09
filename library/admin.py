from django.contrib import admin

from .models import Author, Book, BorrowRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "created_at")
    search_fields = ("first_name", "last_name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "available_copies", "created_at")
    search_fields = ("title", "isbn", "author__first_name", "author__last_name")
    list_select_related = ("author",)


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("book", "borrower_name", "borrowed_at", "returned_at")
    search_fields = ("book__title", "borrower_name")
    list_select_related = ("book", "book__author")

