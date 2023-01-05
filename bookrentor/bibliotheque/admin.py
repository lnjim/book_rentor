from django.contrib import admin
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation

admin.site.register(Genre)
admin.site.register(Editor)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(BooksInLibrary)
admin.site.register(LibraryLocation)