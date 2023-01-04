from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('user/home/', views.user_home, name='user_home'),
    path('register/', views.register, name='register'),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name= "logout"),
    path('new_genre/', views.new_genre, name='new_genre'),
    path('new_editor/', views.new_editor, name='new_editor'),
    path('new_author/', views.new_author, name='new_author'),
    path('new_book/', views.new_book, name='new_book'),
]