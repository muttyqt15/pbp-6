from django.contrib import admin
from django.urls import path
from .views import profile_view, delete_account, edit_profile

app_name = 'profile'

urlpatterns = [
    # path("login/", login, name="login"),
    path("", profile_view, name='profile'), 
    path('delete_account/', delete_account, name='delete_account'),
    path("edit_profile/", edit_profile, name='edit_profile'),
    # path("edit-owner/", edit_owner_profile, name='editowner'),
    # path("edit-customer/", edit_profile, name='editcust'),  
    # path('user/<str:username>/', other_profile_view, name='user_profile'),
    # path('logout/', logout_user, name='logout_user'),
    # path('edit-profile/', edit_profile, name='editprofile'),
]