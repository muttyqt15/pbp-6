from django.contrib import admin
from django.urls import path, include, URLResolver
from . import views

urlpatterns: list[URLResolver] = [
    path("", views.index, name="index"),
    path("like/<int:id>/", views.like_thread, name="like"),
]
