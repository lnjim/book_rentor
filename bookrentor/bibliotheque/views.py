from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
import pdb
from django.contrib.auth.models import Group

def index(request):
    return render(request=request, template_name="index.html")

def home(request):
    # render template with current user
    return render(request=request, template_name="home.html", context={"user":request.user})

def register(request):
    if request.method == 'POST':
        # pdb.set_trace()
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.POST['is_librarian'] == 'on':
                group = Group.objects.get(name='book_seller')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='user')
                user.groups.add(group)
            messages.success(request, "Registration successful.")
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