from django.db import models
from django.contrib.auth.models import AbstractUser
import authentication.models as auth

class CustomerProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    #reviews = models.ManyToManyField(Review, blank=True)
    # bookmarks = models.ManyToManyField(Restaurant, blank=True)
    bio = models.TextField("Biography", blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
class OwnerProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    # restaurant = models.OneToOneField()
    bio = models.TextField("Biography", blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

