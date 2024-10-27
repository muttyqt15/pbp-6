from django.contrib import admin
from .models import Food, Restaurant, Menu


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "address", "operational_hours", "photo_url")

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("category", "restaurant")
    list_filter = ("restaurant",)
    search_fields = ("category", "restaurant_name")

@admin.register(Food)
class Food(admin.ModelAdmin):
    list_display = ("name", "price", "menu")
    list_filter = ("menu",)
    search_fields = ("name", "menu")