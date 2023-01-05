from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return render(request=request, template_name="index_client.html")

def home_client(request):
    # redirect to index if user is not logged in
    if not request.user.is_authenticated:
        return redirect("index")
    return render(request=request, template_name="home_client.html", context={"user":request.user})

def register_client(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            group = Group.objects.get(name='user')
            user.groups.add(group)
            messages.success(request, "Registration successful.")
            if user.groups.filter(name='book_seller').exists():
                return redirect("home")
            elif user.groups.filter(name='user').exists():
                return redirect("user_home")
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
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home_client")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_client(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")