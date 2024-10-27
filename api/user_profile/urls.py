from django.contrib import admin
from django.urls import path
from .views import login
from .views import profile_view, edit_customer_profile, edit_owner_profile, other_profile_view

urlpatterns = [
    # path("login/", login, name="login"),
    path("my-profile/", profile_view, name='profile'), 
    path("edit-customer/", edit_customer_profile, name='editcust'),  
    path("edit-owner/", edit_owner_profile, name='editowner'),
    path('user/<str:username>/', other_profile_view, name='user_profile'),
]