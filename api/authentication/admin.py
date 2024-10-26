from django.contrib import admin
from .models import User, RestaurantOwner, Customer

# Simple UserAdmin to display basic fields
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')

# RestaurantOwnerAdmin
class RestaurantOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')

# CustomerAdmin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

# Register the models with the correct admin classes
admin.site.register(User, UserAdmin)
admin.site.register(RestaurantOwner, RestaurantOwnerAdmin)
admin.site.register(Customer, CustomerAdmin)
