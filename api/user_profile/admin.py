from django.contrib import admin
from .models import CustomerProfile, OwnerProfile
# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(OwnerProfile)