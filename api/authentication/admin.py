from django.contrib import admin
from .models import User, Customer, RestaurantOwner


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    list_filter = ("role",)
    search_fields = ("username", "email")


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ("user", "phone_number", "address")
    search_fields = ("user",)


@admin.register(RestaurantOwner)
class RestaurantOwner(admin.ModelAdmin):
    list_display = ("user", "phone_number", "restaurant")
    search_fields = ("user", "restaurant")
