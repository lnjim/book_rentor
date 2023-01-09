from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pdb
from django.contrib.auth.models import Group, User
from .forms import NewUserForm, NewGenreForm, NewEditorForm, NewAuthorForm, NewBookForm, NewLibraryForm, NewBookInLibraryForm, NewLibraryLocationForm, NewReadingGroupForm
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation, Rent, ReadingGroup, ReadingGroupMember
import datetime

def index(request):
    return render(request=request, template_name="index.html")

def home(request):
    if not request.user.is_authenticated:
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
            genre = Genre.objects.create(name=form.cleaned_data['name'])
            genre.save()
            return redirect("home")
    form = NewGenreForm()
    return render(request=request, template_name="new_genre.html", context={"new_genre_form":form})

def new_editor(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewEditorForm(request.POST)
        if form.is_valid():
            editor = Editor.objects.create(name=form.cleaned_data['name'])
            editor.save()
            return redirect("home")
    form = NewEditorForm()
    return render(request=request, template_name="new_editor.html", context={"new_editor_form":form})

def new_author(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            author = Author.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            author.save()
            return redirect("home")
    form = NewAuthorForm()
    return render(request=request, template_name="new_author.html", context={"new_author_form":form})

def new_book(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            book = Book.objects.create(title=form.cleaned_data['title'], genre=form.cleaned_data['genre'], editor=form.cleaned_data['editor'], author=form.cleaned_data['author'], summary=form.cleaned_data['summary'])
            book.save()
            return redirect("home")
    form = NewBookForm()
    return render(request=request, template_name="new_book.html", context={"new_book_form":form})

def new_library_location(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewLibraryLocationForm(request.POST)
        if form.is_valid():
            location = LibraryLocation.objects.create(name=form.cleaned_data['name'])
            location.save()
            return redirect("home")
    form = NewLibraryLocationForm()
    return render(request=request, template_name="new_library_location.html", context={"new_library_location_form":form})

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

def my_libraries(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    libraries = Library.objects.filter(owner=request.user)
    return render(request=request, template_name="my_libraries.html", context={"libraries":libraries})

def library(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='book_seller').exists():
        return redirect("index")
    library = Library.objects.get(id=library_id)
    books = BooksInLibrary.objects.filter(library=library)
    return render(request=request, template_name="library.html", context={"library":library, "books":books})

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
                return redirect("home")
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
    library = Library.objects.get(id=library_id)
    reading_groups = ReadingGroup.objects.filter(library__id=library_id)
    return render(request=request, template_name="library_reading_groups.html", context={"reading_groups":reading_groups, "library":library})

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
