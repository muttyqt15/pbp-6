from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import add_restaurant, edit_restaurant, get_restaurant_xml, get_restaurants_xml_by_id, get_restaurant_menu, my_restaurant

urlpatterns: list[URLResolver] = [
        path("", my_restaurant, name="my_restaurant"),
        path("add/", add_restaurant, name="add_restaurant"),
        path("edit/<int:id>/", edit_restaurant, name="edit_restaurant"),
        path("<int:id>/menu/", get_restaurant_menu, name="get_restaurant_menu"),
        path("get/", get_restaurant_xml, name="get_restaurant_xml"),
        path("get/<int:id>/", get_restaurants_xml_by_id, name="get_restaurants_xml_by_id"),        
]
