from django.db import models
from api.authentication.models import User
from api.restaurant.models import Restaurant
from api.review.models import Review

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # reviews = models.ManyToManyField(Review, on_delete=models.CASCADE, blank=True)
    # bookmarks = models.ManyToManyField(Restaurant, blank=True)
    bio = models.TextField("Biography", blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField("Biography", blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

