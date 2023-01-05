from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_client, name='register_client'),
    path('home/', views.home_client, name='home_client'),
    path("login/", views.login_client, name="login_client"),
    path("logout", views.logout_client, name= "logout_client"),
]