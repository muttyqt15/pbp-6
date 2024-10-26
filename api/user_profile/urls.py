from django.contrib import admin
from django.urls import path
# from .views import login
from .views import profile_view, edit_customer_profile, edit_owner_profile

urlpatterns = [
    # path("login/", login, name="login"),
    path("my-profile/", profile_view, name='profile')
    # path("edit-customer/", edit_customer_profile, name='editcust' )
    # path("edit-owner/", edit_owner_profile, name='editowner')
    
]
