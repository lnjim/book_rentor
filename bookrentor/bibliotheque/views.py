from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import pdb
from django.contrib.auth.models import Group
from .forms import NewUserForm, NewGenreForm, NewEditorForm, NewAuthorForm, NewBookForm, NewLibraryForm, NewBookInLibraryForm, NewLibraryLocationForm
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation

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
    if request.method == 'POST':
        form = NewLibraryForm(request.POST)
        if form.is_valid():
            library = Library.objects.create(name=form.cleaned_data['name'], location=form.cleaned_data['location'])
            library.save()
            return redirect("home")
    form = NewLibraryForm()
    return render(request=request, template_name="new_library.html", context={"new_library_form":form})

def new_book_in_library(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        form = NewBookInLibraryForm(request.POST)
        if form.is_valid():
            book_in_library = BooksInLibrary.objects.create(book=form.cleaned_data['book'], library=form.cleaned_data['library'], quantity=form.cleaned_data['quantity'])
            book_in_library.save()
            return redirect("home")
    form = NewBookInLibraryForm()
    return render(request=request, template_name="new_book_in_library.html", context={"new_book_in_library_form":form})

# def library_detail(request, library_id):
#     if not request.user.is_authenticated:
#         return redirect("index")
#     library = Library.objects.get(id=library_id)
#     books_in_library = BooksInLibrary.objects.filter(library=library)
#     return render(request=request, template_name="library_detail.html", context={"library":library, "books_in_library":books_in_library})