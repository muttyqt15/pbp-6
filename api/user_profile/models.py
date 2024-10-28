from django.db import models
from api.authentication.models import Customer, RestaurantOwner

class CustomerProfile(models.Model):
    user = models.OneToOneField(Customer, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
class OwnerProfile(models.Model):
    user = models.OneToOneField(RestaurantOwner, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

