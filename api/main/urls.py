from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import main, authenticated_page

urlpatterns: list[URLResolver] = [
    path("", main, name="main"),
    path("test", authenticated_page, name="test")
]
