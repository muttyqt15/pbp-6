from django.contrib import admin
from django.urls import path
from .views import login, signup, logout

app_name = 'authentication'
urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout")
]
