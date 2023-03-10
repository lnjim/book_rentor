from django.contrib.auth.models import Group, User
from django.db import models
from datetime import date

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Editor(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    editor = models.ForeignKey('Editor', on_delete=models.CASCADE, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class LibraryLocation(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey('LibraryLocation', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class BooksInLibrary(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    library = models.ForeignKey('Library', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.book} in {self.library}'

class Rent(models.Model):
    class RentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        RETURNED = 'RETURNED', 'Returned'
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    library = models.ForeignKey('Library', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    status = models.CharField(default=RentStatus.PENDING, max_length=10, choices=RentStatus.choices)
    rent_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f'{self.user} want to rent {self.quantity} copies of the book: {self.book} from the library: {self.library} on {self.rent_date} to {self.return_date}'
    def user_rented_book(self):
        return f'{self.user} rented {self.quantity} copies of the book: {self.book} from the library: {self.library} on {self.rent_date} to {self.return_date}'
    # days left before return date
    def days_left(self):
        return (self.return_date - date.today()).days

class ReadingGroup(models.Model):
    name = models.CharField(max_length=200)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    library = models.ForeignKey('Library', on_delete=models.CASCADE, null=True)
    date = models.DateField()
    hour = models.TimeField(default='18:00')
    limit = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.name} reading {self.book} in {self.library} on {self.date} at {self.hour} with a limit of {self.limit} members'
    # days left before date
    def days_left(self):
        return (self.date - date.today()).days
    # count members in the group
    def count_members(self):
        return self.readinggroupmember_set.filter(status='ACCEPTED').count()

class ReadingGroupMember(models.Model):
    class MemberStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey('ReadingGroup', on_delete=models.CASCADE, null=True)
    status = models.CharField(default=MemberStatus.PENDING, max_length=10, choices=MemberStatus.choices)

    def __str__(self):
        return f'{self.user} want to join the group {self.group}'
    def user_joined_group(self):
        return f'{self.user} joined the group {self.group}'

class Channel(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user2')

    def __str__(self):
        return f'conversation between {self.user1} and {self.user2}'

class Message(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.message}'
    
    def display_message(self):
        return f'{self.sender} on {self.date}: {self.message}'