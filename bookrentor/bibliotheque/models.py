from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Editor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    editor = models.ForeignKey('Editor', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class LibraryLocation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey('LibraryLocation', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class BooksInLibrary(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.book} in {self.library}'

class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True)
    rent_date = models.DateField()
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} rented {self.book} from {self.library} on {self.date}'

class ReadingGroup(models.Model):
    name = models.CharField(max_length=200)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    limit = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.name} reading {self.book} in {self.library} on {self.date}'

class ReadingGroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey('ReadingGroup', on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} is a member of {self.group}'