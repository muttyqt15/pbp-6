from django.contrib import admin
from .models import User, RestaurantOwner, Customer


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "date_joined")
admin.site.register(RestaurantOwner)
admin.site.register(Customer)
