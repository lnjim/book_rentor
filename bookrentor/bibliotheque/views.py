from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import pdb
from django.contrib.auth.models import Group
from .forms import NewUserForm, NewGenreForm, NewEditorForm, NewAuthorForm, NewBookForm, NewLibraryForm, NewBooksInLibraryForm
from .models import Genre, Editor, Author, Book, Library, BooksInLibrary

def index(request):
    return render(request=request, template_name="index.html")

def home(request):
    return render(request=request, template_name="home.html", context={"user":request.user})

def user_home(request):
    return render(request=request, template_name="user_home.html", context={"user":request.user})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'is_librarian' in request.POST:
                if request.POST['is_librarian'] == 'on':
                    group = Group.objects.get(name='book_seller')
                    user.groups.add(group)
            else:
                group = Group.objects.get(name='user')
                user.groups.add(group)
            messages.success(request, "Registration successful.")
            if user.groups.filter(name='book_seller').exists():
                return redirect("home")
            elif user.groups.filter(name='user').exists():
                return redirect("user_home")
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
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.groups.filter(name='book_seller').exists():
                    return redirect("home")
                elif user.groups.filter(name='user').exists():
                    return redirect("user_home")
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
    if request.method == 'POST':
        form = NewGenreForm(request.POST)
        if form.is_valid():
            genre = Genre.objects.create(name=form.cleaned_data['name'])
            genre.save()
            return redirect("home")
    form = NewGenreForm()
    return render(request=request, template_name="new_genre.html", context={"new_genre_form":form})