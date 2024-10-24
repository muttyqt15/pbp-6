from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import index

urlpatterns: list[URLResolver] = [
    path("", index, name="index"),
]
