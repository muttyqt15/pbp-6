from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import add_restaurant, edit_restaurant, get_restaurant_xml, get_restaurants_xml_by_id, get_restaurant_menu, restaurant

urlpatterns: list[URLResolver] = [
        path("<int:id>", restaurant, name="restaurant"),
        path("add/", add_restaurant, name="add_restaurant"),
        path("<int:id>/menu/", get_restaurant_menu, name="get_restaurant_menu"),
        path("get/", get_restaurant_xml, name="get_restaurant_xml"),
        path("get/<int:id>/", get_restaurants_xml_by_id, name="get_restaurants_xml_by_id"),        
]
