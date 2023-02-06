from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from bibliotheque.models import Book, Library, BooksInLibrary, Rent, ReadingGroup, ReadingGroupMember, Channel, Message
from .forms import NewRentBookForm, SearchBookForm, SearchLibraryForm
# import forms from bibliotheque
from bibliotheque.forms import NewMessageForm
import datetime
from django.db.models import Q
import pdb

def index_client(request):
    return render(request=request, template_name="index_client.html")

def home_client(request):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    books_rented = Rent.objects.filter(user=request.user, status="ACCEPTED")
    # reading group where user is in and are in the future
    reading_groups = ReadingGroupMember.objects.filter(user=request.user, group__date__gte=datetime.date.today(), status="ACCEPTED")
    return render(request=request, template_name="home_client.html", context={"user":request.user, "books_rented":books_rented, "reading_groups":reading_groups})

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
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    if request.method == 'POST':
        form = SearchLibraryForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            libraries = Library.objects.filter(location=location)
            if libraries.count() == 0:
                messages.error(request, "No library found.")
            return render(request=request, template_name="library_list.html", context={"libraries_filtered":libraries, "search_library_form":form})
    libraries = Library.objects.all()
    form = SearchLibraryForm()
    return render(request=request, template_name="library_list.html", context={"libraries":libraries, "search_library_form":form})

def library_detail(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    library = Library.objects.get(id=library_id)
    books_in_library = BooksInLibrary.objects.filter(library=library)
    return render(request=request, template_name="library_detail.html", context={"library":library, "books_in_library":books_in_library})

def rent_book(request, library_id, book_id):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
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

def rent_request_list(request):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    rents = Rent.objects.filter(user=request.user)
    return render(request=request, template_name="rent_request_list.html", context={"rent_requests":rents})

def search_book(request):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    if request.method == 'POST':
        form = SearchBookForm(request.POST)
        if form.is_valid():
            books = BooksInLibrary.objects.all()
            if form.cleaned_data.get('title') != '':
                books = books.filter(book__title__icontains=form.cleaned_data.get('title'))
            if form.cleaned_data.get('author') != '':
                books = books.filter(book__author__name__icontains=form.cleaned_data.get('author'))
            if form.cleaned_data.get('genre') != None:
                books = books.filter(book__genre=form.cleaned_data.get('genre'))
            if form.cleaned_data.get('editor') != None:
                books = books.filter(book__editor=form.cleaned_data.get('editor'))
            if form.cleaned_data.get('library') != None:
                books = books.filter(library=form.cleaned_data.get('library'))
            return render(request=request, template_name="search_book.html", context={"search_book_form":form, "books":books})
    form = SearchBookForm()
    return render(request=request, template_name="search_book.html", context={"search_book_form":form})

def library_reading_group_list(request, library_id):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    if request.method == 'POST':
        reading_group = ReadingGroup.objects.get(id=request.POST.get('reading_group_id'))
        # check if user is already in the reading group
        if ReadingGroupMember.objects.filter(user=request.user, group=reading_group).exists():
            messages.error(request, "You are already in this reading group.")
            return redirect("library_reading_group_list", library_id=library_id)
        # check if there is still space in the reading group
        if ReadingGroupMember.objects.filter(group=reading_group, status='ACCEPTED').count() >= reading_group.limit:
            messages.error(request, "This reading group is full.")
            return redirect("library_reading_group_list", library_id=library_id)
        reading_group_member = ReadingGroupMember.objects.create(
            user=request.user,
            group=reading_group,
            status='PENDING'
        )
        reading_group_member.save()
        messages.success(request, "Request sent.")
        return redirect("home_client")
    library = Library.objects.get(id=library_id)
    reading_groups = ReadingGroup.objects.filter(library=library)
    return render(request=request, template_name="library_reading_group_list.html", context={"library":library, "reading_groups":reading_groups})

def reading_group_request_list(request):
    if not request.user.is_authenticated:
        return redirect("index_client")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index_client")
    reading_group_requests = ReadingGroupMember.objects.filter(user=request.user)
    return render(request=request, template_name="reading_group_request_list.html", context={"reading_group_requests":reading_group_requests})

def channels_client(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index")
    channels = Channel.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    for channel in channels:
        channel.last_message = Message.objects.filter(channel=channel).order_by('date').first()
    return render(request=request, template_name="channels_client.html", context={"channels":channels})

def message_client(request, channel_id):
    if not request.user.is_authenticated:
        return redirect("index")
    if not request.user.groups.filter(name='user').exists():
        return redirect("index")
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            current_channel = Channel.objects.get(id=channel_id)
            message = Message.objects.create(channel=current_channel, sender=request.user, message=form.cleaned_data['message'], date=datetime.datetime.now())
            message.save()
            return redirect("messages_client", channel_id=channel_id)
        else:
            messages.error(request, 'Invalid form')
            return redirect("home")
    channel = Channel.objects.get(id=channel_id)
    conversations = Message.objects.filter(channel=channel).order_by('date')
    form = NewMessageForm()
    return render(request=request, template_name="message_client.html", context={"conversations":conversations, "channel":channel, "new_message_form":form})