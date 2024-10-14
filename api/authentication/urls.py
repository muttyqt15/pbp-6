from django.contrib import admin
from django.urls import path
from .views import login, sign_up

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", sign_up, name="sign-up"),
]
