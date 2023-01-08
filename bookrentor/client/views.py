from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from bibliotheque.models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation, Rent
from .forms import NewRentBookForm
import datetime
import pdb

def index_client(request):
    return render(request=request, template_name="index_client.html")

def home_client(request):
    if not request.user.is_authenticated:
        return redirect("index_client")
    books_rented = Rent.objects.filter(user=request.user, status="ACCEPTED")
    return render(request=request, template_name="home_client.html", context={"user":request.user, "books_rented":books_rented})

def register_client(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            group = Group.objects.get(name='user')
            user.groups.add(group)
            messages.success(request, "Registration successful.")
            if user.groups.filter(name='book_seller').exists():
                return redirect("home_client")
        raise ValueError("Invalid form")
    form = NewUserForm()
    return render (request=request, template_name="register_client.html", context={"register_form":form})

def login_client(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.groups.filter(name='user').exists():
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home_client")
                else:
                    messages.error(request, "You are not a user.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login_client.html", context={"login_form":form})

def logout_client(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index_client")

def library_list(request):
    # render the list of libraries
    libraries = Library.objects.all()
    return render(request=request, template_name="library_list.html", context={"libraries":libraries})

def library_detail(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index")
    library = Library.objects.get(id=library_id)
    books_in_library = BooksInLibrary.objects.filter(library=library)
    return render(request=request, template_name="library_detail.html", context={"library":library, "books_in_library":books_in_library})

def rent_book(request, library_id, book_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        form = NewRentBookForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('rent_date') < datetime.date.today() or form.cleaned_data.get('return_date') < form.cleaned_data.get('rent_date'):
                messages.error(request, "start date is before today's date or return date is before start date")
                return redirect("rent_book", library_id=library_id, book_id=book_id)
            # check if user has already rented this book
            if Rent.objects.filter(user=request.user, book=Book.objects.get(id=book_id), library=Library.objects.get(id=library_id), status='PENDING').exists():
                messages.error(request, "You have already made a rent request for this book.")
                return redirect("rent_book", library_id=library_id, book_id=book_id)
            rent = Rent.objects.create(
                user=request.user,
                book=Book.objects.get(id=book_id),
                library=Library.objects.get(id=library_id),
                quantity=form.cleaned_data.get('quantity'),
                rent_date=form.cleaned_data.get('rent_date'),
                return_date=form.cleaned_data.get('return_date'),
            )
            rent.save()
            messages.success(request, "Rent successful.")
            return redirect("home_client")
        else:
            messages.error(request, "Rent failed.")
            return redirect("rent_book", library_id=library_id, book_id=book_id)
    form = NewRentBookForm()
    return render(request=request, template_name="rent_book.html", context={"rent_book_form":form})

# def rent_request_list(request):
#     if not request.user.is_authenticated:
#         return redirect("index")
#     rents = Rent.objects.filter(user=request.user, status='PENDING')
#     return render(request=request, template_name="rent_request_list.html", context={"rent_requests":rents})

