from django.contrib import admin
from django.urls import path
from .views import profile_view, delete_account, edit_profile, show_json, edit_profile_picture, edit_profile_flutter, delete_account_flutter, fetch_profile, edit_profile_picture_flutter

app_name = 'profile'

urlpatterns = [
    # path("login/", login, name="login"),
    path("", profile_view, name='profile'), 
    path('delete_account/', delete_account, name='delete_account'),
    path("edit_profile/", edit_profile, name='edit_profile'),
    path("json/", show_json, name='json'),
    path('edit_profile_picture/', edit_profile_picture, name='edit_profile_picture'),
    
    path('fetch_profile/', fetch_profile, name='fetch_profile'),
    path('delete_account_flutter/', delete_account_flutter, name='delete_account_flutter'),
    path('edit_profile_flutter/', edit_profile_flutter, name='edit_profile_flutter'),
    path('edit_profile_picture_flutter/', edit_profile_picture_flutter, name='edit_profile_picture_flutter'),

]