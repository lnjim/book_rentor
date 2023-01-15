from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pdb
from django.contrib.auth.models import Group, User
from .forms import NewUserForm, NewGenreForm, NewEditorForm, NewAuthorForm, NewBookForm, NewLibraryForm, NewBookInLibraryForm, NewLibraryLocationForm, NewReadingGroupForm
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation, Rent, ReadingGroup, ReadingGroupMember, Channel, Message
import datetime
from django.db.models import Q

def index(request):
    return render(request=request, template_name="index.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    return render(request=request, template_name="home.html", context={"user":request.user})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            group = Group.objects.get(name='book_seller')
            user.groups.add(group)
            messages.success(request, "Registration successful.")
            if user.groups.filter(name='book_seller').exists():
                return redirect("home")
        raise ValueError("Invalid form")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.groups.filter(name='book_seller').exists():
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
                else:
                    messages.error(request, "You are not a book seller.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")

def new_genre(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewGenreForm(request.POST)
        if form.is_valid():
            genre = Genre.objects.create(name=form.cleaned_data['name'], creator=request.user)
            genre.save()
            messages.success(request, "Genre created successfully.")
            return redirect("home")
    form = NewGenreForm()
    return render(request=request, template_name="new_genre.html", context={"new_genre_form":form})

def genres(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        genre = Genre.objects.get(id=request.POST['genre_id'])
        genre.delete()
        messages.success(request, "Genre deleted successfully.")
        return redirect("genres")
    genres = Genre.objects.filter(creator=request.user)
    return render(request=request, template_name="genres.html", context={"genres":genres})

def edit_genre(request, genre_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    genre = Genre.objects.get(id=genre_id)
    if request.method == 'POST':
        form = NewGenreForm(request.POST)
        if form.is_valid():
            genre.name = form.cleaned_data['name']
            genre.save()
            messages.success(request, "Genre edited successfully.")
            return redirect("genres")
    else:
        form = NewGenreForm(initial={'name':genre.name})
        return render(request=request, template_name="edit_genre.html", context={"edit_genre_form":form, "genre":genre})

def new_editor(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewEditorForm(request.POST)
        if form.is_valid():
            editor = Editor.objects.create(name=form.cleaned_data['name'], creator=request.user)
            editor.save()
            return redirect("home")
    form = NewEditorForm()
    return render(request=request, template_name="new_editor.html", context={"new_editor_form":form})

def editors(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        editor = Editor.objects.get(id=request.POST['editor_id'])
        editor.delete()
        messages.success(request, "Editor deleted successfully.")
        return redirect("editors")
    editors = Editor.objects.filter(creator=request.user)
    return render(request=request, template_name="editors.html", context={"editors":editors})

def edit_editor(request, editor_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    editor = Editor.objects.get(id=editor_id)
    if request.method == 'POST':
        form = NewEditorForm(request.POST)
        if form.is_valid():
            editor.name = form.cleaned_data['name']
            editor.save()
            messages.success(request, "Editor edited successfully.")
            return redirect("editors")
    else:
        form = NewEditorForm(initial={'name':editor.name})
        return render(request=request, template_name="edit_editor.html", context={"edit_editor_form":form})

def new_author(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            author = Author.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], creator=request.user)
            author.save()
            return redirect("home")
    form = NewAuthorForm()
    return render(request=request, template_name="new_author.html", context={"new_author_form":form})

def authors(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        author = Author.objects.get(id=request.POST['author_id'])
        author.delete()
        messages.success(request, "Author deleted successfully.")
        return redirect("authors")
    authors = Author.objects.filter(creator=request.user)
    return render(request=request, template_name="authors.html", context={"authors":authors})

def edit_author(request, author_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    author = Author.objects.get(id=author_id)
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.save()
            messages.success(request, "Author edited successfully.")
            return redirect("authors")
    else:
        form = NewAuthorForm(initial={'first_name':author.first_name, 'last_name':author.last_name})
        return render(request=request, template_name="edit_author.html", context={"edit_author_form":form})

def new_book(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.create(
                title=form.cleaned_data['title'], 
                genre=form.cleaned_data['genre'], 
                editor=form.cleaned_data['editor'], 
                author=form.cleaned_data['author'], 
                summary=form.cleaned_data['summary'],
                creator=request.user
            )
            book.save()
            return redirect("home")
    form = NewBookForm()
    return render(request=request, template_name="new_book.html", context={"new_book_form":form})

def books(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        book = Book.objects.get(id=request.POST['book_id'])
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect("books")
    books = Book.objects.filter(creator=request.user)
    return render(request=request, template_name="books.html", context={"books":books})

def edit_book(request, book_id):
    form = NewBookForm(request.POST or None)
    book = Book.objects.get(id=book_id)
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        if request.POST['action'] == 'update':
            if form.is_valid():
                book.title = form.cleaned_data['title']
                book.author = form.cleaned_data['author']
                book.genre = form.cleaned_data['genre']
                book.editor = form.cleaned_data['editor']
                book.summary = form.cleaned_data['summary']
                book.save()
                messages.success(request, 'Book updated')
                return redirect("books")
            else:
                messages.error(request, 'Invalid form')
                return redirect("books")
        elif request.POST['action'] == 'delete':
            book = Book.objects.get(id=book_id)
            book.delete()
            messages.success(request, 'Book deleted')
            return redirect("books")
    else:
        form.fields['title'].initial = Book.objects.get(id=book_id).title
        form.fields['author'].initial = Book.objects.get(id=book_id).author
        form.fields['genre'].initial = Book.objects.get(id=book_id).genre
        form.fields['editor'].initial = Book.objects.get(id=book_id).editor
        form.fields['summary'].initial = Book.objects.get(id=book_id).summary
        return render(request=request, template_name="edit_book.html", context={"edit_book_form":form, "book":book})

def new_library_location(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewLibraryLocationForm(request.POST)
        if form.is_valid():
            location = LibraryLocation.objects.create(name=form.cleaned_data['name'], creator=request.user)
            location.save()
            return redirect("home")
    form = NewLibraryLocationForm()
    return render(request=request, template_name="new_library_location.html", context={"new_library_location_form":form})

def library_locations(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        location = LibraryLocation.objects.get(id=request.POST['location_id'])
        location.delete()
        messages.success(request, "Library location deleted successfully.")
        return redirect("library_locations")
    locations = LibraryLocation.objects.filter(creator=request.user)
    return render(request=request, template_name="library_locations.html", context={"library_locations":locations})

def edit_library_location(request, location_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    location = LibraryLocation.objects.get(id=location_id)
    if request.method == 'POST':
        form = NewLibraryLocationForm(request.POST)
        if form.is_valid():
            location.name = form.cleaned_data['name']
            location.save()
            messages.success(request, "Library location edited successfully.")
            return redirect("library_locations")
    else:
        form = NewLibraryLocationForm(initial={'name':location.name})
        return render(request=request, template_name="edit_library_location.html", context={"edit_library_location_form":form, "location":location})

def new_library(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewLibraryForm(request.POST)
        if form.is_valid():
            library = Library.objects.create(name=form.cleaned_data['name'], location=form.cleaned_data['location'], owner=request.user)
            library.save()
            return redirect("home")
    form = NewLibraryForm()
    return render(request=request, template_name="new_library.html", context={"new_library_form":form})

def libraries(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    libraries = Library.objects.filter(owner=request.user)
    return render(request=request, template_name="libraries.html", context={"libraries":libraries})

def edit_library(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    library = Library.objects.get(id=library_id)
    if request.method == 'POST':
        form = NewLibraryForm(request.POST)
        if form.is_valid():
            library.name = form.cleaned_data['name']
            library.location = form.cleaned_data['location']
            library.save()
            messages.success(request, "Library edited successfully.")
            return redirect("libraries")
    else:
        form = NewLibraryForm(initial={'name':library.name, 'location':library.location})
        return render(request=request, template_name="edit_library.html", context={"edit_library_form":form, "library":library})

def new_book_in_library(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewBookInLibraryForm(request.POST)
        if form.is_valid():
            book_in_library = BooksInLibrary.objects.create(book=form.cleaned_data['book'], library=form.cleaned_data['library'], quantity=form.cleaned_data['quantity'])
            book_in_library.save()
            return redirect("home")
    form = NewBookInLibraryForm()
    return render(request=request, template_name="new_book_in_library.html", context={"new_book_in_library_form":form})

def library(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        book_in_library = BooksInLibrary.objects.get(book__id=request.POST['book_id'], library__id=library_id)
        book_in_library.delete()
        messages.success(request, "Book removed successfully.")
        return redirect("library", library_id=library_id)
    library = Library.objects.get(id=library_id)
    books = BooksInLibrary.objects.filter(library=library)
    return render(request=request, template_name="library.html", context={"library":library, "books":books})

def edit_book_in_library(request, book_id, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    book_in_library = BooksInLibrary.objects.get(book__id=book_id, library__id=library_id)
    if request.method == 'POST':
        form = NewBookInLibraryForm(request.POST)
        if form.is_valid():
            book_in_library.book = form.cleaned_data['book']
            book_in_library.library = form.cleaned_data['library']
            book_in_library.quantity = form.cleaned_data['quantity']
            book_in_library.save()
            messages.success(request, "Book in library edited successfully.")
            return redirect("library", library_id=library_id)
    else:
        form = NewBookInLibraryForm(initial={'book':book_in_library.book, 'library':book_in_library.library, 'quantity':book_in_library.quantity})
        return render(request=request, template_name="edit_book_in_library.html", context={"edit_book_in_library_form":form, "book_in_library":book_in_library})

def pending_rent_requests(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        if request.POST['accepted'] == 'True':
            # get book in library
            book_in_library = BooksInLibrary.objects.get(book__id=request.POST['book_id'], library__id=request.POST['library_id'])
            if book_in_library.quantity > 0 and book_in_library.quantity >= int(request.POST['quantity']):
                book_in_library.quantity -= int(request.POST['quantity'])
                rent = Rent.objects.get(user=User.objects.get(id=request.POST['user_id']), book__id=request.POST['book_id'], library__id=request.POST['library_id'], status='PENDING')
                rent.status = 'ACCEPTED'
                rent.save()
                book_in_library.save()
                messages.success(request, 'Request accepted')
                return redirect("home")
            else:
                rent = Rent.objects.get(user=User.objects.get(id=request.POST['user_id']), book__id=request.POST['book_id'], library__id=request.POST['library_id'])
                rent.status = 'REJECTED'
                rent.save()
                messages.error(request, 'Not enough books in library, request rejected')
                return redirect("home")
        else:
            rent = Rent.objects.get(user=User.objects.get(id=request.POST['user_id']), book__id=request.POST['book_id'], library__id=request.POST['library_id'], status='PENDING')
            rent.status = 'REJECTED'
            rent.save()
            messages.error(request, 'Request rejected')
            return redirect("home")
    rent_requests = Rent.objects.filter(library__owner=request.user, status='PENDING')
    return render(request=request, template_name="pending_rent_requests.html", context={"rent_requests":rent_requests})

def update_rent_requests(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        rent = Rent.objects.get(user=User.objects.get(id=request.POST['user_id']), book__id=request.POST['book_id'], library__id=request.POST['library_id'], status='ACCEPTED')
        rent.status = 'RETURNED'
        book_in_library = BooksInLibrary.objects.get(book__id=request.POST['book_id'], library__id=request.POST['library_id'])
        book_in_library.quantity += int(request.POST['quantity'])
        book_in_library.save()
        rent.save()
        messages.success(request, 'Book returned')
        return redirect("home")
    rent_requests = Rent.objects.filter(library__owner=request.user, status='ACCEPTED')
    return render(request=request, template_name="update_rent_requests.html", context={"rent_requests":rent_requests})

def late_rent_requests(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        rent = Rent.objects.get(user=User.objects.get(id=request.POST['user_id']), book__id=request.POST['book_id'], library__id=request.POST['library_id'], status='ACCEPTED')
        rent.status = 'RETURNED'
        book_in_library = BooksInLibrary.objects.get(book__id=request.POST['book_id'], library__id=request.POST['library_id'])
        book_in_library.quantity += int(request.POST['quantity'])
        book_in_library.save()
        rent.save()
        messages.success(request, 'Book returned')
        return redirect("home")
    rent_requests = Rent.objects.filter(library__owner=request.user, status='ACCEPTED', return_date__lt=datetime.date.today())
    return render(request=request, template_name="late_rent_requests.html", context={"rent_requests":rent_requests})

def new_reading_group(request, library_id, book_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewReadingGroupForm(request.POST)
        if form.is_valid():
            book_in_library = BooksInLibrary.objects.filter(book=book_id, library__id=library_id)
            if book_in_library:
                if form.cleaned_data['date'] < datetime.date.today():
                    messages.error(request, 'Invalid date')
                    return redirect("home")
                reading_group = ReadingGroup.objects.create(
                    name=form.cleaned_data['name'],
                    book=Book.objects.get(id=book_id),
                    library=Library.objects.get(id=library_id),
                    date=form.cleaned_data['date'],
                    hour=form.cleaned_data['hour'],
                    limit=form.cleaned_data['limit']
                )
                reading_group.save()
                messages.success(request, 'Reading group created')
                return redirect("library_reading_groups", library_id=library_id)
            else:
                messages.error(request, 'Book not found in library')
                return redirect("home")
        else:
            messages.error(request, 'Invalid form')
            return redirect("home")
    form = NewReadingGroupForm()
    return render(request=request, template_name="new_reading_group.html", context={"new_reading_group_form":form})

def library_reading_groups(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        reading_group = ReadingGroup.objects.get(id=request.POST['reading_group_id'])
        reading_group.delete()
        messages.success(request, 'Reading group deleted')
        return redirect("library_reading_groups", library_id=library_id)
    library = Library.objects.get(id=library_id)
    reading_groups = ReadingGroup.objects.filter(library__id=library_id)
    return render(request=request, template_name="library_reading_groups.html", context={"reading_groups":reading_groups, "library":library})

def edit_reading_group(request, library_id, reading_group_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewReadingGroupForm(request.POST)
        if form.is_valid():
            reading_group = ReadingGroup.objects.get(id=reading_group_id)
            if form.cleaned_data['date'] < datetime.date.today():
                messages.error(request, 'Invalid date')
                return redirect("home")
            reading_group.name = form.cleaned_data['name']
            reading_group.date = form.cleaned_data['date']
            reading_group.hour = form.cleaned_data['hour']
            reading_group.limit = form.cleaned_data['limit']
            reading_group.save()
            messages.success(request, 'Reading group edited')
            return redirect("library_reading_groups", library_id=library_id)
        else:
            messages.error(request, 'Invalid form')
            return redirect("home")
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    form = NewReadingGroupForm(initial={'name':reading_group.name, 'date':reading_group.date, 'hour':reading_group.hour, 'limit':reading_group.limit})
    return render(request=request, template_name="edit_reading_group.html", context={"edit_reading_group_form":form, "reading_group":reading_group})

def pending_reading_group_requests(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        reading_group_member = ReadingGroupMember.objects.get(id=request.POST['reading_group_member_id'])
        if request.POST['accept'] == 'True':
            if ReadingGroupMember.objects.filter(id=request.POST['reading_group_member_id'], status='ACCEPTED').count() >= ReadingGroup.objects.get(id=request.POST['reading_group_id']).limit:
                messages.error(request, 'Limit reached, request rejected')
                reading_group_member.status = 'REJECTED'
                reading_group_member.save()
                return redirect("home")
            reading_group_member.status = 'ACCEPTED'
            reading_group_member.save()
            messages.success(request, 'Request accepted')
            return redirect("home")
        else:
            reading_group_member.status = 'REJECTED'
            reading_group_member.save()
            messages.error(request, 'Request rejected')
            return redirect("home")
    reading_group_requests = ReadingGroupMember.objects.filter(group__library__owner=request.user, status='PENDING')
    return render(request=request, template_name="pending_reading_group_requests.html", context={"reading_group_requests":reading_group_requests})

def reading_group_users(request, library_id, reading_group_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        if request.POST['action'] == 'remove_member':
            reading_group_member = ReadingGroupMember.objects.get(group__id=request.POST['reading_group_id'], user=request.POST['user_id'])
            reading_group_member.delete()
            messages.success(request, 'User removed from reading group')
            return redirect("reading_group_users", library_id=library_id, reading_group_id=reading_group_id)
        elif request.POST['action'] == 'create_channel':
            if Channel.objects.filter(user1=request.user, user2=User.objects.get(id=request.POST['user_id'])).count() > 0 or Channel.objects.filter(user1=User.objects.get(id=request.POST['user_id']), user2=request.user).count() > 0:
                channel = Channel.objects.filter(Q(user1=request.user, user2__id=request.POST['user_id']) | Q(user1__id=request.POST['user_id'], user2=request.user)).first()
                return redirect("messages", channel_id=channel.id)
            else:
                channel = Channel.objects.create(user1=request.user, user2=User.objects.get(id=request.POST['user_id']))
                channel.save()
                messages.success(request, 'Start your new conversation')
                return redirect("messages", channel_id=channel.id)
    library = Library.objects.get(id=library_id)
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    reading_group_members = ReadingGroupMember.objects.filter(group__id=reading_group_id, status='ACCEPTED')
    return render(request=request, template_name="reading_group_users.html", context={"reading_group_members":reading_group_members, "reading_group":reading_group, "library":library})

def channels(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    channels = Channel.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    # get last message for each channel
    for channel in channels:
        channel.last_message = Message.objects.filter(channel=channel).order_by('-date').first()
    return render(request=request, template_name="channels.html", context={"channels":channels})

def message(request, channel_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    channel = Channel.objects.get(id=channel_id)
    messages = Message.objects.filter(channel=channel).order_by('-date')
    return render(request=request, template_name="message.html", context={"messages":messages, "channel":channel})