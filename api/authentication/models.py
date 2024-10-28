from django.db import models
from django.contrib.auth.models import AbstractUser
from .constant import Role
from api.restaurant.models import Restaurant

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    # profile = models.OneToOneField()
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=150, default=Role.CUSTOMER)

    @property
    def is_customer(self):
        return self.role == Role.CUSTOMER

    @property
    def is_resto_owner(self):
        return self.role == Role.RESTO_OWNER

    @property
    def is_admin(self):
        return self.role == Role.ADMIN


class RestaurantOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.OneToOneField(
        Restaurant, on_delete=models.CASCADE, blank=True, null=True
    )
    # beritas = models.ForeignKey("berita.Berita", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.restaurant.name if self.restaurant else 'No Restaurant'}"

    @property
    def restaurant_name(self):
        return self.restaurant.name if self.restaurant else "No Restaurant"

    @classmethod
    def get_by_username(cls, username: str):
        """
        Class method to get RestaurantOwner by the associated user's username.
        Returns None if no owner is found.
        """
        try:
            return cls.objects.get(user__username=username)
        except cls.DoesNotExist:
            return None


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Added phone number field
    # reviews = models.ManyToManyField(Review, blank=True)
    # bookmarks = models.ManyToManyField(Restaurant, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} "

    @classmethod
    def get_by_username(cls, username: str):
        """
        Class method to get Customer by the associated user's username.
        Returns None if no customer is found.
        """
        try:
            return cls.objects.get(user__username=username)
        except cls.DoesNotExist:
            return None
