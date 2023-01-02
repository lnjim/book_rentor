from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name= "logout"),
]