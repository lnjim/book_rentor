from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_client, name='index_client'),
    path('register/', views.register_client, name='register_client'),
    path('home/', views.home_client, name='home_client'),
    path("login/", views.login_client, name="login_client"),
    path("logout", views.logout_client, name= "logout_client"),
    path("library_list", views.library_list, name="library_list"),
    path('library/<int:library_id>/detail', views.library_detail, name='library_detail'),
    path('library/<int:library_id>/rent/<int:book_id>', views.rent_book, name='rent_book'),
    path('rent_request_list/', views.rent_request_list, name='rent_request_list'),
    path('search_book/', views.search_book, name='search_book'),
    path('library/<int:library_id>/library_reading_group_list/', views.library_reading_group_list, name='library_reading_group_list'),
]