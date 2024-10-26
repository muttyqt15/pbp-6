from django.db import models
from django.contrib.auth.models import AbstractUser
from .constant import Role
from api.restaurant.models import Restaurant

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    # profile = models.OneToOneField()
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=150, default=Role.CUSTOMER)


class RestaurantOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    # beritas = models.ForeignKey("berita.Berita", blank=True)

    def __str__(self) -> str:
        return f"{self.restaurant_name} - {self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # reviews = models.ManyToManyField(Review, blank=True)
    # bookmarks = models.ManyToManyField(Restaurant, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} "
