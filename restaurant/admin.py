from django.contrib import admin
from .models import Food, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "address", "operational_hours")


@admin.register(Food)
class Food(admin.ModelAdmin):
    list_display = ("name", "category", "price", "restaurant")
    list_filter = ("category", "restaurant")
    search_fields = ("name", "restaurant_name")
