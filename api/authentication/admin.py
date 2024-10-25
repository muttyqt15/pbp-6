from django.contrib import admin
from .models import User, RestaurantOwner


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")

class RestaurantOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')  # Menampilkan user dan restaurant
    search_fields = ('user__username',)  # Mencari berdasarkan username

# Mendaftarkan model RestaurantOwner
admin.site.register(RestaurantOwner, RestaurantOwnerAdmin)