from django.contrib import admin
from django.urls import path, include, URLResolver

urlpatterns: list[URLResolver] = [
    path("", include("api.main.urls")),
    path("auth/", include("api.authentication.urls")),
    path("restaurant/", include("api.restaurant.urls")),
    path("review/", include("api.review.urls")),
    path("thread/", include("api.thread.urls")),
]
