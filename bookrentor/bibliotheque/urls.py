from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name= "logout"),
    path('new_genre/', views.new_genre, name='new_genre'),
    path('genres/', views.genres, name='genres'),
    path('edit/genre/<int:genre_id>/', views.edit_genre, name='edit_genre'),
    path('new_editor/', views.new_editor, name='new_editor'),
    path('editors/', views.editors, name='editors'),
    path('edit/editor/<int:editor_id>/', views.edit_editor, name='edit_editor'),
    path('new_author/', views.new_author, name='new_author'),
    path('authors/', views.authors, name='authors'),
    path('edit/author/<int:author_id>/', views.edit_author, name='edit_author'),
    path('new_book/', views.new_book, name='new_book'),
    path('books/', views.books, name='books'),
    path('edit/book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('new_library_location/', views.new_library_location, name='new_library_location'),
    path('library_locations/', views.library_locations, name='library_locations'),
    path('edit/library_location/<int:location_id>/', views.edit_library_location, name='edit_library_location'),
    path('new_library/', views.new_library, name='new_library'),
    path('new_book_in_library/', views.new_book_in_library, name='new_book_in_library'),
    path('edit/<int:library_id>/book_in_library/<int:book_id>/', views.edit_book_in_library, name='edit_book_in_library'),
    path('libraries/', views.libraries, name='libraries'),
    path('edit/library/<int:library_id>/', views.edit_library, name='edit_library'),
    path('libraries/<int:library_id>/', views.library, name='library'),
    path('pending_rent_requests/', views.pending_rent_requests, name='pending_rent_requests'),
    path('update_rent_requests/', views.update_rent_requests, name='update_rent_requests'),
    path('late_rent_requests/', views.late_rent_requests, name='late_rent_requests'),
    path('libraries/<int:library_id>/new_reading_group/<int:book_id>/', views.new_reading_group, name='new_reading_group'),
    path('libraries/<int:library_id>/reading_groups/', views.library_reading_groups, name='library_reading_groups'),
    path('edit/library/<int:library_id>/reading_group/<int:reading_group_id>/', views.edit_reading_group, name='edit_reading_group'),
    path('pending_reading_group_requests/', views.pending_reading_group_requests, name='pending_reading_group_requests'),
    path('my_libraries/<int:library_id>/reading_groups/<int:reading_group_id>/reading_group_users/', views.reading_group_users, name='reading_group_users'),
]