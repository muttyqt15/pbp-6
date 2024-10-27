from django.contrib import admin
from .models import User, RestaurantOwner, Customer

# Simple UserAdmin to display basic fields
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "date_joined")
admin.site.register(RestaurantOwner)
admin.site.register(Customer)
