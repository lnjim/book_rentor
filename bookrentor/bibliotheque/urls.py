from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name= "logout"),
    path('new_genre/', views.new_genre, name='new_genre'),
    path('new_editor/', views.new_editor, name='new_editor'),
    path('new_author/', views.new_author, name='new_author'),
    path('new_book/', views.new_book, name='new_book'),
    path('new_library_location/', views.new_library_location, name='new_library_location'),
    path('new_library/', views.new_library, name='new_library'),
    path('new_book_in_library/', views.new_book_in_library, name='new_book_in_library'),
    path('my_libraries/', views.my_libraries, name='my_libraries'),
    path('my_libraries/<int:library_id>/', views.library, name='library'),
    path('pending_rent_requests/', views.pending_rent_requests, name='pending_rent_requests'),
    path('update_rent_requests/', views.update_rent_requests, name='update_rent_requests'),
    path('late_rent_requests/', views.late_rent_requests, name='late_rent_requests'),
]