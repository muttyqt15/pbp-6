from django.db import models
from django.contrib.auth.models import AbstractUser
from .constant import Role
from uuid import uuid4
from os import path
from django.db.models.signals import post_save
from django.dispatch import receiver


class RestaurantOwner(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    restaurant = models.OneToOneField("restaurant.Restaurant", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.restaurant_name} - {self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.phone_number}"


class User(AbstractUser):
    def generate_profile_path(self, filename: str) -> str:
        extension: str = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{extension}"
        return path.join("profile", filename)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=150, default=Role.CUSTOMER)
    profile_image = models.ImageField(
        upload_to=generate_profile_path, null=True, blank=True
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="custom_user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="custom_user_permissions",
    )

    def __str__(self) -> str:
        return f"{self.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == Role.RESTO_OWNER:
            RestaurantOwner.objects.create(user=instance)
        elif instance.role == Role.CUSTOMER:
            Customer.objects.create(user=instance)
