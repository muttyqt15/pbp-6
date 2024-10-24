from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import index, authenticated_page

app_name = 'main'

urlpatterns: list[URLResolver] = [
    path("", index, name="index"),
    path("test", authenticated_page, name="test")
]
