from django.contrib import admin
from django.urls import path, include, URLResolver
from . import views

urlpatterns: list[URLResolver] = [
    path("", views.index, name="index"),
    path("like/<int:id>/", views.like_thread, name="like_thread"),
    path("edit/<int:id>/", views.edit_thread, name="edit_thread"),
    path("delete/<int:id>/", views.delete_thread, name="delete_thread"),
    path("like/comment/<int:comment_id>/", views.like_comment, name="like_comment"),
    path("delete/comment/<int:id>/", views.delete_comment, name="delete_comment"),
    path("<int:id>/", views.detail_thread, name="detail_thread"),
]
