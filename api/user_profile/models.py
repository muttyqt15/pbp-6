from django.db import models
from api.authentication.models import Customer, RestaurantOwner, User

class CustomerProfile(models.Model):
    user = models.OneToOneField(Customer, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.png')
    # name = user.user.username
    # email = user.user.email
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png')

class OwnerProfile(models.Model):
    user = models.OneToOneField(RestaurantOwner, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.png')
    # name = user.user.username
    # email = user.user.email
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png')
