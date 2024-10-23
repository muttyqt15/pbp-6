from django.contrib import admin
from django.urls import path, include, URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/", include(("api.authentication.urls", "authentication"))),
    path("restaurant/", include(("api.restaurant.urls", "restaurant"))),
    path("review/", include(("api.review.urls", "review"))),

]
