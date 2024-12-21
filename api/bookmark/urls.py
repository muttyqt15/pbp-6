from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('toggle/<int:restaurant_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('delete/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
    path('bookmarks/', views.get_bookmarks, name='get_bookmarks'),
]