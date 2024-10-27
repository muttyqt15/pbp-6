from django.db import models
import authentication.models as auth
import restaurant.models as resto
import review.models as rev

class CustomerProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(rev.Review, on_delete=models.CASCADE, blank=True)
    # bookmarks = models.ManyToManyField(Restaurant, blank=True)
    bio = models.TextField("Biography", blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
class OwnerProfile(models.Model):
    user = models.OneToOneField(auth.User, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(resto.Restaurant, on_delete=models.CASCADE)
    bio = models.TextField("Biography", blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

