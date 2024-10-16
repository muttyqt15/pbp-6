from django.contrib import admin
from django.urls import path, include, URLResolver
from .views import add_restaurant, edit_restaurant, get_restaurant_xml, get_restaurants_xml_by_id

urlpatterns: list[URLResolver] = [
        path("add/", add_restaurant, name="add_restaurant"),
        path("edit/<int:id>/", edit_restaurant, name="edit_restaurant"),
        path("get/", get_restaurant_xml, name="get_restaurant_xml"),
        path("get/<int:id>/", get_restaurants_xml_by_id, name="get_restaurants_xml_by_id"),
        
]
