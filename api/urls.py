from django.contrib import admin
from django.urls import path, include, URLResolver
from django.contrib.auth.decorators import login_required

urlpatterns: list[URLResolver] = [
    path("", include("api.main.urls")),
    path("auth/", include("api.authentication.urls")),
    path("restaurant/", include("api.restaurant.urls")),
    path("review/", include("api.review.urls")),
    path("bookmark", include("api.bookmark.urls"))
    path("thread/", include("api.thread.urls")),
    path('news/', include('api.news.urls')),
]
