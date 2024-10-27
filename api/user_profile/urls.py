from django.contrib import admin
from django.urls import path
# from .views import login
from .views import profile_view,other_profile_view, logout_user, delete_account, edit_profile

urlpatterns = [
    # path("login/", login, name="login"),
    path("", profile_view, name='profile'), 
    # path("edit-customer/", edit_customer_profile, name='editcust'),  
    # path("edit-owner/", edit_owner_profile, name='editowner'),
    path('user/<str:username>/', other_profile_view, name='user_profile'),
    path('logout/', logout_user, name='logout_user'),
    path('delete-account/', delete_account, name='delete_account'),
    path('edit-profile/', edit_profile, name='editprofile'),
]