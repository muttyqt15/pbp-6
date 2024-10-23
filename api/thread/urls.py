from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import (
    get_thread_json,
    get_thread_json_by_id,
    create_thread,
    update_thread,
    delete_thread,
)

urlpatterns: list[URLResolver] = [
    path("", get_thread_json, name="get_thread_json"),
    path("create/", create_thread, name="create_thread"),
    path("update/", update_thread, name="update_thread"),
    path("delete/", delete_thread, name="delete_thread"),
    path("view/<int:thread_id>/", get_thread_json_by_id, name="get_thread_json_by_id"),
]
