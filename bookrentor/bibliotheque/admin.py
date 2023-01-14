from django.contrib import admin
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation, Rent, ReadingGroup, ReadingGroupMember, ChatMessage

admin.site.register(Genre)
admin.site.register(Editor)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(BooksInLibrary)
admin.site.register(LibraryLocation)
admin.site.register(Rent)
admin.site.register(ReadingGroup)
admin.site.register(ReadingGroupMember)
admin.site.register(ChatMessage)