from django.contrib import admin
from django.urls import path
from .views import login, signup

app_name = 'authentication'  # Add this line!
urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
]
